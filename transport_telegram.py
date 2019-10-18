import requests


# method for delivering a message in telegram
def transport_telegram(message, webhook):
    try:
        requests.post(webhook, data={"message": message})  # sending the message by webhook
        return True
    except ValueError:
        print('Wrong webhook')
        return False
