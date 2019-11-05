import re
from logging import getLogger
from typing import Tuple, List, Union

from apscheduler.schedulers.blocking import BlockingScheduler
from yaml import load

from config.settings import *

logger = getLogger("general")
scheduler = BlockingScheduler()
scheduler.configure(**SCHEDULER)


class TaskWrapper:
    """Simple wrapper for task data"""

    def __init__(self, **kwargs):
        self._kwargs = kwargs  # saving src data for serialization
        self.__dict__.update(kwargs)  # setting all the passed parameters

    def run(self):
        """Executes the task, namely checks and, if necessary, sends data."""
        # TODO: implement this method when creating the controller
        pass

    def serialize(self) -> dict:
        """Converts the task object to an dict consisting of primitive types"""
        return self._kwargs

    @classmethod
    def deserialize(cls, kwargs: dict) -> TaskWrapper:
        """Deserializes task

        :param kwargs: dict with src task fields
        """
        return cls(**kwargs)


def get_tasks() -> Union[List[Tuple[TaskWrapper, Dict]], None]:
    """Parses the task file, wraps it in a wrapper
    class, creates a crontab and returns a list with
    tuples that contain the TaskWrapper and dict
    with cron fields ("minute", "hour", "day",
    "month", "day_of_week")"""
    data = None
    with open(TASKS_FILE_PATH, "r") as file:
        data = load(file)
    if not data:
        logger.exception(f"Wrong tasks structure in {TASKS_FILE_PATH}")
        return None

    src_tasks = data.get("tasks", [])
    src_notifiers = data.get("notifiers", [])

    # TODO: write normal wrapping data to TaskWrapper when creating the controller
    tasks = []
    for src in src_tasks:
        cron = re.fullmatch(
            " *" + 4 * "([0-9\*/,a-z]*) +" + "([0-9\*/,a-z]*) *",
            src.get("schedule", ""),
            flags=re.IGNORECASE
        )

        if cron is None:
            logger.exception(f"Wrong cron for {src.get('name', 'task')}")
            continue

        cron = {f: cron[i] for f, i in enumerate(("minute", "hour", "day", "month", "day_of_week"))}
        tasks.append((TaskWrapper(**src), cron))

    TaskWrapper.notifiers = src_notifiers
    return tasks


def process(serialized_task: dict):
    """Runs scenario

    :param serialized_task: dict consisting of primitive types
    """
    task: TaskWrapper = TaskWrapper.deserialize(serialized_task)
    logger.info(f"Started task processing <{hash(serialized_task)}>")
    try:
        task.run()
    except Exception as e:
        logger.exception(f"Failed to complete task <{hash(serialized_task)}>: {e}")


def add_tasks(task: TaskWrapper, cron: dict):
    """Adds task to scheduler

    :param task: task object
    :param cron: dict with cron fields ("minute", "hour", "day", "month", "day_of_week")
    """
    serialized_task = task.serialize()
    scheduler.add_job(process, "cron", args=[serialized_task], replace_existing=True, **cron)
    logger.info(f"Added new periodic task: #{task.name}")


def run():
    """Gets tasks, adds them to the scheduler, and launches"""
    logger.info(f"Run manager-ai")
    tasks_with_cron = get_tasks()
    # TODO: implement a lambda func that selects only new tasks
    tasks_with_cron = list(filter(lambda task_with_cron: task_with_cron, tasks_with_cron))
    logger.info(f"Found {len(tasks_with_cron)} new tasks in {TASKS_FILE_PATH}")
    for task, cron in tasks_with_cron:
        add_tasks(task, cron)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    run()
