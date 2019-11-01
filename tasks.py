import re
from logging import getLogger
from typing import Tuple, List

from apscheduler.schedulers.blocking import BlockingScheduler
from yaml import load

from config.settings import *

logger = getLogger("general")
scheduler = BlockingScheduler()
scheduler.configure(**SCHEDULER)


class TaskWrapper:
    """Simple wrapper for task data"""
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self.__dict__.update(kwargs)

    def run(self):
        """Complete the task, namely check and, if necessary, send data."""
        # TODO: implement this method when creating the controller
        pass

    def serialize(self) -> Dict[str, list or str or int or "etc"]:
        """Convert the task object
        to an object consisting of primitive types"""
        return self._kwargs

    @classmethod
    def deserialize(cls, kwargs: Dict[str, list or str or int or "etc"]):
        """Task deserialization"""
        return cls(**kwargs)


def get_tasks() -> List[Tuple[TaskWrapper, Dict["cron fields"]]]:
    """Parse the task file,
    wrap it in a wrapper class, create a crontab
    and return a list with tuples that contain
    the wrapped task and crontab"""
    data = None
    with open(TASKS_FILE_PATH, 'r') as file:
        data = load(file)
    if not data:
        logger.exception(f"Wrong tasks structure in {TASKS_FILE_PATH}")
        return

    src_tasks = data.get("tasks", [])
    src_notifiers = data.get("notifiers", [])

    # TODO: write normal wrapping data to TaskWrapper when creating the controller
    tasks: list = []
    for src in src_tasks:
        cron = re.fullmatch(
            " *" + 4 * "([0-9\*/,a-z]*) +" + "([0-9\*/,a-z]*) *",
            src.get("schedule", ''),
            flags=re.IGNORECASE
        )

        if cron is None:
            logger.exception(f"Wrong cron for {src.get('name', 'task')}")
            continue

        cron = {f: cron[i] for f, i in enumerate(("minute", "hour", "day", "month", "day_of_week"))}
        tasks.append((TaskWrapper(**src), cron))

    TaskWrapper.notifiers = src_notifiers
    return tasks


def process(serialized_task: Dict[list, str, int, "etc"]):
    """Execute scenario"""
    task: TaskWrapper = TaskWrapper.deserialize(serialized_task)
    logger.info(f"Started task processing <{hash(serialized_task)}>")
    try:
        task.run()
    except Exception as e:
        logger.exception(f"Failed to complete task <{hash(serialized_task)}>: {e}")


def add_tasks(task: TaskWrapper, cron: Dict["cron fields"]):
    """Add task to scheduler"""
    serialized_task = task.serialize()
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
