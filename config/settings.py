import sys
from logging.config import dictConfig
from os import path
from typing import Dict

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pytz import utc

# set it in local_settings.py
PROXY: Dict[str, str] = None

# File path with specified tasks
TASKS_FILE_PATH = path.join(path.dirname(path.dirname(path.abspath(__file__))), "tasks.yml")

# default apscheduler config
SCHEDULER = {
    "jobstores": {
        "default": MongoDBJobStore(database="scheduler", collection="jobs", host="localhost", port=27017)
    }, "executors": {
        "default": {"type": "threadpool", "max_workers": 20},
        "processpool": ProcessPoolExecutor(max_workers=5)
    }, "job_defaults": {
        "coalesce": False,
        "max_instances": 3
    }, "timezone": utc
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "(%(process)d) %(asctime)s %(name)s (line %(lineno)s) %(levelname)s %(message)s",
            "datefmt": "%y %b %d, %H:%M:%S",
        },
    },
    "handlers": {
        "console_stderr": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": sys.stderr
        },
    },
    "loggers": {
        "general": {
            "handlers": ["console_stderr"],
            "level": "INFO",
        },
    }
}

try:
    from .local_settings import *
except ImportError:
    pass

dictConfig(LOGGING)
