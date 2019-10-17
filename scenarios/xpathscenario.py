import json
from os import path
from datetime import datetime
from hashlib import md5 as make_hash

import requests
from lxml import html


class XPathScenario:

    DEFAULT_TIMESTAMPS_FILE = ".xpath_timestamps.json"

    """Sample timestamps file:
    
    {
        '<hashed (url+xpath)>': {
            'element': '<hashed_element>',
            'timestamp': '<datetime>'
        }
    }
    
    Hashes are used to make strings shorter.
    
    """

    def __init__(self, params: dict):
        self.url = params['url']
        self.xpath = params['xpath']
        self.proxies = params.get('proxies')
        self.timestamp_key: str = self.get_hash(self.url + self.xpath)

    def get_html_element_by_xpath(self):
        """Makes a GET request to the {self.url}. Searches for an html element by
        its xpath and returns its string representation.
        """

        try:
            response = requests.get(self.url, proxies=self.proxies).text
        except requests.RequestException as e:
            # logging.error("Request error: {}".format(e))
            # TODO: exception handling
            return None

        tree = html.fromstring(response)
        try:
            elem_lst = tree.xpath(self.xpath)
        except Exception as e:
            # logging.error("XPathError: {}".format(e))
            # TODO: exception handling
            return None

        return html.tostring(elem_lst[0])

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
    def get_hash(string) -> str:
        """Returns md5 hash of the given string / byte sequence."""

        if type(string) is str:
            string = bytes(string, "utf-8")
        elif type(string) is not bytes:
            raise TypeError("Illegal argument given.")

        return make_hash(string).hexdigest()

    def __read_json(self) -> dict:
        """Loads timestamp data from DEFAULT_TIMESTAMPS_FILE."""

        with open(self.DEFAULT_TIMESTAMPS_FILE, 'r') as timestamps_file:
            timestamps_dict = json.loads(timestamps_file.read())

        return timestamps_dict

    def __write_json(self, timestamps_dict):
        """Writes data to DEFAULT_TIMESTAMPS_FILE."""

        with open(self.DEFAULT_TIMESTAMPS_FILE, 'w') as timestamps_file:
            timestamps_file.write(json.dumps(timestamps_dict, indent=4))

    # def update_timestamps_file(self, new_element: dict):
    #     timestamps_dict = self.__read_json()
    #     timestamps_dict[self.timestamp_key] = new_element
    #     self.__write_json(timestamps_dict)

    def run(self):
        """Runs an XPathScenario.

        1. Searches for an html element by xpath.

        2. Writes its timestamp into a timestamps file,
        if it doesn't contain one.

        """

        searched_element = self.get_html_element_by_xpath()

        # if nothing is found
        if not searched_element:
            raise NotImplementedError()

        timestamp = {
            "element": self.get_hash(searched_element),
            "timestamp": str(datetime.now()).split(".")[0]
        }

        # if a timestamps file doesn't exist, create one and
        # write the first timestamp into it
        if not path.exists(self.DEFAULT_TIMESTAMPS_FILE):
            with open(self.DEFAULT_TIMESTAMPS_FILE, 'w') as timestamps_file:
                timestamps_file.write("{ \"" + self.timestamp_key + "\": "
                                      + json.dumps(timestamp) + " }")
            return

        timestamps_dict = self.__read_json()

        if not timestamps_dict.get(self.timestamp_key):
            timestamps_dict[self.timestamp_key] = timestamp
            self.__write_json(timestamps_dict)
