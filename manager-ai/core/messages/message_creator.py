import random

from .messages_templates import FIRST_TIME_MESSAGES, SECOND_TIME_MESSAGES, EVIL_EMOJI, SAD_EMOJI

""" A function that creates new notification using user-config 
    user-config should contain:
        int days_count - days since last post
        bool first_time - means did we send a message already
"""


def create_message(user_config) -> str:
    content = {
        'days_count': user_config['days_count'],
        'evil_emoji': random.choice(EVIL_EMOJI),
        'sad_emoji': random.choice(SAD_EMOJI),
    }
    message = random.choice(FIRST_TIME_MESSAGES if user_config['first_time'] else SECOND_TIME_MESSAGES)
    message = message.format(**content)
    return message
