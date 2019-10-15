from typing import Tuple, List

from celery.schedules import crontab

from settings import *


class Service:
    """Set of class/static methods for various purposes"""

    @classmethod
    def get_tasks(cls) -> List[Tuple["task wrapper", crontab]]:
        raise NotImplementedError()

    @classmethod
    def deserialize_task(cls, src: "serialized task wrapper") -> "task wrapper":
        raise NotImplementedError()

    @classmethod
    def serialize_task(cls, task: "task wrapper") -> Dict[list, str, int, "etc"]:
        raise NotImplementedError()

    @classmethod
    def run_task(cls, task: "task wrapper") -> None:
        raise NotImplementedError()
