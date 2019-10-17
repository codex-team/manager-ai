import requests


def transport_telegram(message, webhook):
    requests.post(webhook, data={message.encode('cp1251')})
