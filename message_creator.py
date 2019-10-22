import random

from messages import *

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
    message = random.choice([FIRST_TIME_MESSAGES, SECOND_TIME_MESSAGES][not user_config['first_time']])
    message = message.format(**content)
    return message

