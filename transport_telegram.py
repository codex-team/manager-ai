import requests
import time


def transport_telegram(message, webhook):
    """
    Method for delivering a message in telegram
    message - it is a message you want to send in telegram
    webhook - webhook for telegram
    """
    flag = 0
    while flag < 10:  # if connecting error reconnects up to 10 times every second
        try:
            requests.post(webhook, data={"message": message}, timeout=(0.00001, 10))  # sending the message by webhook
            return True
        except ValueError:
            print('Wrong webhook')
            return False
        except ConnectionError:
            print("Connection Error")
            flag += 1
            time.sleep(1)
        except requests.exceptions.ConnectTimeout:
            print("Timeout error")
            flag += 1
            time.sleep(1)
    return False
