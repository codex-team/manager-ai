import logging
from datetime import datetime
from hashlib import md5 as make_hash

import requests
from lxml import html

from config.settings import MONGO_CLIENT, DATABASE_NAME


class XPathScenario:

    # mongoDB collection where elements and their timestamps are stored
    XPATH_COLLECTION = MONGO_CLIENT[DATABASE_NAME]["xpath_collection"]

    """Sample document in xpath_collection:
    
    {
        '_id': '<hashed (url+xpath)>', 
        'element': '<hashed_element>',
        'timestamp': <datetime>
    }
    
    Hashes are used to make strings shorter.
    """

    def __init__(self, params: dict):
        self.url = params['url']
        self.xpath = params['xpath']
        self.proxies = params.get('proxies')
        self.timestamp_key: str = self.__get_hash(self.url + self.xpath)

    def get_element(self, document):
        """Searches for an html element in {document} by
        its xpath and returns its string representation.
        """

        tree = html.fromstring(document)
        try:
            elem_lst = tree.xpath(self.xpath)
        except Exception as e:
            logging.error("XPathError: {}".format(e))
            # TODO: exception handling
            return None

        return html.tostring(elem_lst[0]) if elem_lst else None

    def get_page_content(self, url=None):
        """Makes a GET request to the {self.url} or
        to the {url} if specified."""

        url = url if url else self.url
        try:
            response = requests.get(url, proxies=self.proxies)
        except requests.RequestException as e:
            logging.error("Request error: {}".format(e))
            # TODO: exception handling
            return None

        return response.text

    # def checkout_timestamp(self, element_info: dict):
    #     # get date of the last change
    #     timestamp = datetime.strptime(element_info['timestamp'],
    #                                   "%Y-%m-%d %H:%M:%S")
    #
    #     now = datetime.now()   # get current date
    #     delta = now - timestamp  # calculate time difference
    #
    #     return delta.total_seconds() >= self.params['max-secs-without-changes']

    @staticmethod
    def __get_hash(string) -> str:
        """Returns md5 hash of the given string / byte sequence."""

        if type(string) is str:
            string = bytes(string, "utf-8")
        elif type(string) is not bytes:
            raise TypeError("Illegal argument given.")

        return make_hash(string).hexdigest()

    def run(self):
        """Runs an XPathScenario.

        1. Searches for an html element by xpath.

        2. Writes its timestamp into xpath_collection,
        if it doesn't contain one.

        """

        page_content = self.get_page_content()
        searched_element = self.get_element(page_content)

        # if nothing is found
        if not searched_element:
            raise NotImplementedError()

        timestamp = {
            "_id": self.timestamp_key,
            "element": self.__get_hash(searched_element),
            "timestamp": datetime.now()  # str(datetime.now()).split(".")[0]
        }

        old_timestamp = self.XPATH_COLLECTION.find_one({"_id": self.timestamp_key})

        # if there is no such element in collection
        if not old_timestamp:
            self.XPATH_COLLECTION.insert_one(timestamp)
            return False
