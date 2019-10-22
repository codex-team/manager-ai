import requests
from retrying import retry
import logging


def retry_if_connection_error(exception):
    """If Connection error in requests return True, False otherwise"""
    return isinstance(exception, requests.exceptions.ConnectionError)


# retry if Connecting or timeout error for 3 time
@retry(retry_on_exception=retry_if_connection_error, stop_max_attempt_number=3)
def transport_telegram(message, webhook):
    """
    Method for delivering a message in telegram
    message - it is a message you want to send in telegram
    webhook - webhook for telegram
    """
    try:
        requests.post(webhook, data={"message": message}, timeout=10)  # sending the message by webhook
        return True
    except ValueError:
        logging.error('Wrong webhook')
        return False
    except requests.exceptions.ConnectionError:
        logging.error("Connection Error")
    return False

