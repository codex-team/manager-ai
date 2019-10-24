from logging import getLogger
from typing import Tuple, List

from apscheduler.schedulers.blocking import BlockingScheduler

from config.settings import *

logger = getLogger("general")
scheduler = BlockingScheduler()
scheduler.configure(**SCHEDULER)


class Service:
    """Set of class/static methods for various purposes"""

    @classmethod
    def get_tasks(cls) -> List[Tuple["task wrapper", Dict["cron fields"]]]:
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


def process(serialized_task: Dict[list, str, int, "etc"]):
    """Execute scenario"""
    task: "task wrapper" = Service.deserialize_task(serialized_task)
    logger.info(f"Started task processing <{hash(serialized_task)}>")
    try:
        Service.run_task(task)
    except Exception as e:
        logger.exception(f"Failed to complete task <{hash(serialized_task)}>: {e}")


def add_tasks(task: "task wrapper", cron: Dict["cron fields"]):
    """Add task to scheduler"""
    serialized_task = Service.serialize_task(task)
    scheduler.add_job(process, "cron", args=[serialized_task], replace_existing=True, **cron)
    logger.info(f"Added new periodic task: #{task.name}")


def run():
    logger.info(f"Run manager-ai")
    tasks_with_cron = Service.get_tasks()
    # TODO: implement a lambda func that selects only new tasks
    tasks_with_cron = filter(lambda task_with_cron: task_with_cron, tasks_with_cron)
    logger.info(f"Found {len(tasks_with_cron)} new tasks in {TASKS_FILE_PATH}")
    for task, cron in tasks_with_cron:
        add_tasks(task, cron)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    run()
