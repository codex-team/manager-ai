from logging.config import dictConfig
from typing import Dict

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/2'
CELERY_RESULT_BACKEND = 'redis://localhost'

PROXY: Dict[str] = None

# File path with specified tasks
TASKS_FILE_PATH = None

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
        'celery': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'celery.log',
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
    from local_settings import *
except ImportError:
    pass

dictConfig(LOGGING)
