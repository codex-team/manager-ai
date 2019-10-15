from typing import Tuple, List

from celery.schedules import crontab

from settings import *


class Service:
    """Set of class/static methods for various purposes"""

    @classmethod
    def get_tasks(cls) -> List[Tuple["task wrapper", crontab]]:
        """Parse the task file,
        wrap it in a wrapper class, create a crontab
        and return a list with tuples that contain
        the wrapped task and crontab"""
        raise NotImplementedError()

    @classmethod
    def deserialize_task(cls, src: "serialized task wrapper") -> "task wrapper":
        """Task deserialization"""
        raise NotImplementedError()

    @classmethod
    def serialize_task(cls, task: "task wrapper") -> Dict[list, str, int, "etc"]:
        """Convert the task object
        to an object consisting of primitive types"""
        raise NotImplementedError()

    @classmethod
    def run_task(cls, task: "task wrapper") -> None:
        """Process the task, namely check and, if necessary, send data"""
        raise NotImplementedError()
