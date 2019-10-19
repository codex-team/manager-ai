import random
from messages import *

""" A function that creates new notification using user-config 
    user-config should contain:
        int days_count - days since last post
        bool first_time - means did we send a message already
"""


def create_message(user_config):
    content = {
        'days_count': user_config['days_count'],
        'evil_emoji': random.choice(EVIL_EMOJI),
        'sad_emoji': random.choice(SAD_EMOJI),
    }
    message = random.choice([FIRST_TIME_MESSAGES, SECOND_TIME_MESSAGES][not user_config['first_time']])
    message = message.format(**content)
    return message


# Test driver
if __name__ == '__main__':
    for _ in range(10):
        user_conf = {
            'days_count': random.randrange(1, 10),
            'first_time': random.choice([True, False]),
        }
        print(create_message(user_conf))
