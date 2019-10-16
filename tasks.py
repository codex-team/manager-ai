import crontab as crontab
from logging import getLogger
from typing import Tuple, List
from config.settings import *

logger = getLogger('general')


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


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """It runs after script has been launched.
       It gets specified tasks from a file and 
       starts their periodic launching"""
    logger.info("Start worker")
    tasks_with_crontab = Service.get_tasks()
    logger.info(f"Found {len(tasks_with_crontab)} tasks")
    for task, crntb in tasks_with_crontab:
        serialized_task = Service.serialize_task(task)
        sender.add_periodic_task(crntb, task_process.s(serialized_task), )
        logger.info(f"Added new periodic task: #{task.name}")


@app.task
def task_process(serialized_task: Dict[list, str, int, "etc"]):
    """Task processing"""
    task: "task wrapper" = Service.deserialize_task(serialized_task)
    Service.run_task(task)
