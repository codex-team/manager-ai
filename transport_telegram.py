import requests
from retrying import retry
import logging


# retry if Connecting or timeout error for 3 time
@retry((ConnectionError, requests.exceptions.ConnectTimeout), stop_max_attempt_number=3)
def transport_telegram(message, webhook):
    """
    Method for delivering a message in telegram
    message - it is a message you want to send in telegram
    webhook - webhook for telegram
    """
    try:
        requests.post(webhook, data={"message": message}, timeout=(0.00001, 10))  # sending the message by webhook
        return True
    except ValueError:
        logging.error('Wrong webhook')
        return False
    except ConnectionError:
        logging.error("Connection Error")
    except requests.exceptions.ConnectTimeout:
        logging.error("Timeout error")
    return False
