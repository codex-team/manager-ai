from os import path
from logging.config import dictConfig
from typing import Dict

# set it in local_settings.py
PROXY: Dict[str] = None

# File path with specified tasks
TASKS_FILE_PATH = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'tasks.txt')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
            'datefmt': '%y %b %d, %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'tmp/log.log',
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 100,
        },
    },
    'loggers': {
        'general': {
            'handlers': ['celery', 'console'],
            'level': 'INFO',
        },
    }
}

try:
    from .local_settings import *
except ImportError:
    pass

dictConfig(LOGGING)
