import requests


def transport_telegram(message, webhook):
    requests.post(webhook, data={"message": message.encode('utf-8')})


transport_telegram('Мяу', 'https://notify.bot.codex.so/u/H97FIRDA')
