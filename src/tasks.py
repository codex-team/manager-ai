import re
from logging import getLogger
from typing import Tuple, List, Union

from apscheduler.schedulers.blocking import BlockingScheduler
from yaml import load

from config.settings import *

logger = getLogger("general")
scheduler = BlockingScheduler()
scheduler.configure(**SCHEDULER)


class BaseTask:
    """Base task wrapper"""

    def __init__(self, name, **kwargs):
        # TODO: explicitly specify the parameters that are used in all tasks
        self.name = name
        self.notifiers = None
        # TODO: edit this logic if we change the task config (one field notifiers for all tasks)
        self._arg_names = list(kwargs.keys()) + ["name", "notifiers"]  # saving arg names for serialization
        self.__dict__.update(kwargs)  # setting all the passed parameters

    def run(self):
        """Executes the task. Base class level."""
        assert self.notifiers is not None, "You did not specify notifiers, use BaseTask.set_notifiers method"
        self._run()

    def _run(self):
        """Executes the task. Implemented class level."""
        raise NotImplementedError("Implement this method in an inherited class")

    def serialize(self) -> dict:
        """Converts the task object to an dict consisting of primitive types"""
        serialized_task = {}
        for key in self._arg_names:
            serialized_task.update({key: self.__getattribute__(key)})
        return serialized_task

    @classmethod
    def deserialize(cls, args: dict) -> "BaseTask":
        """Deserializes task

        :param args: dict with src task fields
        """
        return cls(**args)

    @classmethod
    def set_notifiers(cls, notifiers: List[Dict]):
        """Task notifiers"""
        cls.notifiers = notifiers


def get_tasks_and_notifiers() -> Union[Tuple[List[Tuple[BaseTask, Dict]], List[Dict]], Tuple[None, None]]:
    """Parses the task file, wraps it in a wrapper
    class, creates a crontab and returns a list with
    tuples that contain the BaseTask and dict
    with cron fields ("minute", "hour", "day",
    "month", "day_of_week")"""
    data = None
    with open(TASKS_FILE_PATH, "r") as file:
        data = load(file)
    if not data:
        logger.exception(f"Wrong tasks structure in {TASKS_FILE_PATH}")
        return None, None

    src_tasks = data.get("tasks", [])
    src_notifiers = data.get("notifiers", [])

    # TODO: write normal wrapping data to BaseTask when creating the controller
    tasks = []
    for src in src_tasks:
        schedule = src.get("schedule", "").strip()
        cron = re.fullmatch(
            " ".join("([0-9*/,a-z]*)" for _ in range(5)),
            schedule,
            flags=re.IGNORECASE
        )  # parse cron fields

        if cron is None:
            logger.exception(f"Wrong cron for {src.get('name', 'task')}")
            continue

        cron = {f: cron[i] for f, i in enumerate(("minute", "hour", "day", "month", "day_of_week"))}
        tasks.append((BaseTask(**src), cron))

    return tasks, src_notifiers


def process(serialized_task: dict):
    """Runs scenario

    :param serialized_task: dict consisting of primitive types
    """
    task: BaseTask = BaseTask.deserialize(serialized_task)
    logger.info(f"Started task processing <{hash(serialized_task)}>")
    try:
        task.run()
    except Exception as e:
        logger.exception(f"Failed to complete task <{hash(serialized_task)}>: {e}")


def add_tasks(task: BaseTask, cron: dict):
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
    tasks_with_cron, notifiers = get_tasks_and_notifiers()
    BaseTask.set_notifiers(notifiers)
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
