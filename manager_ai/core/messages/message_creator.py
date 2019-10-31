import random

from .message_templates import FIRST_TIME_MESSAGES, CYCLING_MESSAGES, EVIL_EMOJI, SAD_EMOJI


def create_message(user_config) -> str:
    """A function that creates new notification using user-config

        user-config dict should contain:
        days_count -- days since last post (type int)
        first_time -- did we send a message already (type bool)
    """
    content = {
        'days_count': user_config['days_count'],
        'evil_emoji': random.choice(EVIL_EMOJI),
        'sad_emoji': random.choice(SAD_EMOJI),
    }
    message = random.choice(FIRST_TIME_MESSAGES if user_config['first_time'] else CYCLING_MESSAGES)
    message = message.format(**content)
    return message
