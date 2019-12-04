import random
from logging import getLogger
from yaml import safe_load
from os import path

logger = getLogger("general")


def create_message(name_file_with_messages):
    """A function that creates random message to notify
    :param name_file_with_messages: it is a path if yaml file with messages
    """
    message_name = path.join(path.dirname(path.dirname(path.abspath(__file__))), name_file_with_messages)
    with open(message_name, 'r', encoding='utf-8') as message_file:
        message = ''
        try:
            message_dict = safe_load(message_file.read())
            first_time_messages = message_dict.get("FIRST_TIME_MESSAGES")
            message = random.choice(first_time_messages)
        except:
            logger.exception("Failed to load info from configuration file.")
    return message

