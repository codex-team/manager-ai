import logging

import requests
from retrying import retry
from src.notifiers.base import BaseNotifier


def retry_if_connection_error(exception):
    """If Connection error in requests return True, False otherwise"""
    return isinstance(exception, requests.exceptions.ConnectionError)


class TelegramNotifier(BaseNotifier):
    def __init__(self, webhook):
        self.webhook = webhook

    @retry(retry_on_exception=retry_if_connection_error, stop_max_attempt_number=3)# retry if ConnectingError error for 3 time
    def notify(self, message):
        """
        Method for delivering a message in telegram
        message - it is a message you want to send in telegram
        webhook - webhook for telegram
        """
        try:
            requests.post(self.webhook, data={"message": message}, timeout=10)  # sending the message by webhook
            return True
        except ValueError:
            logging.error("Wrong webhook")
            return False
        except requests.exceptions.ConnectionError:
            logging.error("Connection Error")
        return False
