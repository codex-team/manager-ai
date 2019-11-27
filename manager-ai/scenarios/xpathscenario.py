import logging
from datetime import datetime
from hashlib import md5 as make_hash

import requests
from lxml import html

from settings import MONGO_CLIENT, DATABASE_NAME


class XPathScenario:
    """
    A class representing a scenario in which you need to get an html element by xpath
    from specified web page and save its string representation and timestamp
    (datetime of the last check).

    It uses MongoDB to store data:
        Elements and their timestamps are stored as a document in xpath_collection
        (config.settings.DATABASE_NAME.xpath_collection).

        Sample document in xpath_collection:

            {
                '_id': '<hashed (url+xpath)>',
                'element': '<hashed_element>',
                'timestamp': <datetime>
            }

        Hashes are used to make strings shorter.

    Attributes:
        - XPATH_COLLECTION: mongoDB collection where elements and their timestamps are stored
        - url: URL for making GET request
        - xpath: xpath expression for searching element
        - proxies: dictionary with proxies to use for GET request
        - timestamp_id: id used to get document with element and its timestamp from XPATH_COLLECTION
    """

    XPATH_COLLECTION = MONGO_CLIENT[DATABASE_NAME]["xpath_collection"]

    def __init__(self, params: dict):
        """Initialize XPathScenario.

        :param params: A dictionary with initial parameters for XPathScenario
            object. It must contain 'url' and 'xpath' keys.
        """

        try:
            self.url = params['url']
            self.xpath = params['xpath']
        except (KeyError, TypeError):
            raise TypeError("Illegal initial argument given. Expected 'dict' "
                            "with keys 'url' and 'xpath'.")

        self.proxies = params.get('proxies')
        self.timestamp_id: str = self.__get_hash(self.url + self.xpath)

    def get_element(self, document: str):
        """Searches for an html element in {document} by
        its xpath and returns its string representation.

        :param document: A string to search element in.
        """

        tree = html.fromstring(document)
        try:
            elem_lst = tree.xpath(self.xpath)
        except:
            logging.exception("XPathError")
            # TODO: exception handling
            return None

        return html.tostring(elem_lst[0]).decode().strip() if elem_lst else None

    def get_page_content(self, url=None):
        """Makes a GET request to the {self.url} or
        to the {url} if specified.

        :param url: URL for making GET request.
        """

        url = url if url else self.url
        try:
            response = requests.get(url, proxies=self.proxies)
        except requests.RequestException:
            logging.exception("Request error")
            # TODO: exception handling
            return None

        return response.text

    @staticmethod
    def __get_hash(string) -> str:
        """Returns md5 hash of the given string / byte sequence.

        :param string: A string / byte sequence to make hash of.
        """

        if type(string) is str:
            string = bytes(string, "utf-8")
        elif type(string) is not bytes:
            raise TypeError("Illegal argument given.")

        return make_hash(string).hexdigest()

    def run(self):
        """Runs an XPathScenario.

        1. Searches for an html element by xpath.

        2. Writes its timestamp into xpath_collection
        if it doesn't contain one.

        3. Returns True if the element has already been
        added to the collection, False otherwise.

        """

        page_content = self.get_page_content()
        # if request have failed
        if not page_content:
            raise NotImplementedError()

        searched_element = self.get_element(page_content)
        # if nothing is found
        if not searched_element:
            raise NotImplementedError()

        timestamp = {
            "_id": self.timestamp_id,
            "element": self.__get_hash(searched_element),
            "timestamp": datetime.now()
        }

        old_timestamp = self.XPATH_COLLECTION.find_one({"_id": self.timestamp_id})

        # if there is no such element in collection
        if not old_timestamp:
            self.XPATH_COLLECTION.insert_one(timestamp)
            return False

        return True
