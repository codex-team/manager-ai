import sys
from logging import getLogger
from logging.config import dictConfig
from os import path
from typing import Dict

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pymongo import MongoClient
from yaml import safe_load
from pytz import utc

# default configuration for logger
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
        "test": {
            "handlers": ["console_stderr"],
            "level": "INFO",
        },
    }
}

dictConfig(LOGGING)

# default logger
logger = getLogger("general")

# dict with proxies
# PROXY = {
#     "http": "socks5://127.0.0.1:9050",
#     "https": "socks5://127.0.0.1:9050"
# }
PROXY: Dict[str, str] = None

# path to the file with specified tasks and settings
CONFIG_FILE_PATH = path.join(path.dirname(path.dirname(path.abspath(__file__))), "config.yml")

# default database settings
MONGO_HOST = MongoClient.HOST
MONGO_PORT = MongoClient.PORT
DATABASE_NAME = "manager"

SRC_TASKS = None
SRC_NOTIFIERS = None

# load db settings from configuration file
if path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as config_file:
        try:
            config_dict = safe_load(config_file.read())
            db_config_dict = config_dict.get('database')

            if db_config_dict:
                if db_config_dict.get('host'):
                    MONGO_HOST = db_config_dict.get('host')

                if db_config_dict.get('port'):
                    MONGO_PORT = db_config_dict.get('port')

                if db_config_dict.get('name'):
                    DATABASE_NAME = db_config_dict.get('name')

            if config_dict.get("tasks", []):
                SRC_TASKS = config_dict.get("tasks", [])

            if config_dict.get("notifiers", []):
                SRC_NOTIFIERS = config_dict.get("notifiers", [])
        except:
            logger.exception("Failed to load info from configuration file.")

# mongo client setup
MONGO_CLIENT = MongoClient(host=MONGO_HOST, port=MONGO_PORT)

# default apscheduler config
SCHEDULER = {
    "jobstores": {
        "default": MongoDBJobStore(database=DATABASE_NAME, collection="jobs", client=MONGO_CLIENT)
    }, "executors": {
        "default": {"type": "threadpool", "max_workers": 20},
        "processpool": ProcessPoolExecutor(max_workers=5)
    }, "job_defaults": {
        "coalesce": False,
        "max_instances": 3
    }, "timezone": utc
}