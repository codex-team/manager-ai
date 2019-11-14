import re
from logging import getLogger
from typing import Tuple, List, Union

from apscheduler.schedulers.blocking import BlockingScheduler
from yaml import load

from config.settings import *

__module__ = sys.modules[__name__]

logger = getLogger("test")
scheduler = BlockingScheduler()
scheduler.configure(**SCHEDULER)


class TaskWrapperException(Exception):
    pass


class BaseTask:
    """Base task wrapper"""
    notifiers = None

    def __init__(self, name, **kwargs):
        # TODO: explicitly specify the parameters that are used in all tasks
        self.name = name
        self._arg_names = list(kwargs.keys()) + ["name"]  # saving arg names for serialization
        self.__dict__.update(kwargs)  # setting all the passed parameters

    def run(self):
        """
        Executes the task. Base class level.

        :raise TaskWrapperException: If notifiers is not specified
        :raise NotImplementedError: If `_run` method is not implemented
        """
        if self.__class__.notifiers is None:
            raise TaskWrapperException("You did not specify notifiers, use BaseTask.set_notifiers method")
        self._run()

    def _run(self):
        """
        Executes the task. Implemented class level.

        :raise NotImplementedError: If `_run` method is not implemented
        """
        raise NotImplementedError("Implement this method in an inherited class")

    def serialize(self) -> dict:
        """Converts the task object to an dict consisting of primitive types"""
        serialized_task = {}
        for key in self._arg_names:
            serialized_task.update({key: self.__getattribute__(key)})
        return serialized_task

    @classmethod
    def deserialize(cls, kwargs: dict) -> "BaseTask":
        """Deserializes task

        :param kwargs: dict with src task fields
        """
        return cls(**kwargs)

    @classmethod
    def set_notifiers(cls, notifiers: List[Dict]):
        """Sets task notifiers"""
        cls.notifiers = notifiers

    def __eq__(self, other):
        if other is None or type(other) is not type(self):
            return False
        for field_name in self._arg_names:
            if getattr(self, field_name, None) != getattr(other, field_name, None):
                return False
        return True

    def __hash__(self):
        result = hash(self.__class__.__name__)
        result += sum((hash(f"{field_name}:{getattr(self, field_name)}") for field_name in self._arg_names))
        return hash(result)


class HelloWorldTask(BaseTask):
    """Simple task"""
    def stdout_notify(self, message):
        logger.info(f"Notifies about {self.name} task by ")
        print(message)

    def _run(self) -> None:
        """Task execution logic"""
        logger.info(f"Executes {self.name} task")
        notifier = tuple(filter(lambda ntfr: ntfr.get("name") == self.notifier, self.__class__.notifiers))
        if not notifier:
            logger.error(f"{self.notifier} notifier not found in self.notifiers [task_name:{self.name}]")
            return None
        notifier = notifier[0]
        notify = self.__getattribute__(f"{notifier.get('type')}_notify")  # getting class method by name
        notify("Hello World!")
        return None


def get_task_class(scenario_name: str):
    """
    Looking for class by scenario name.

    Example:
         get_task_class("hello_world") -> :class:`HelloWorldTask`

    :param scenario_name: name of scenario
    :return: TaskBase class implementation or None [If task class for `scenario_name` is not found]
    """
    task_class_name = f"{''.join(word.title() for word in scenario_name.split('_'))}Task"
    cls = getattr(__module__, task_class_name, None)
    if cls is None:
        logger.error(f"{task_class_name} not found")
    return cls


def get_tasks_and_notifiers(data) -> Union[Tuple[List[Tuple[BaseTask, Dict]], List[Dict]], Tuple[None, None]]:
    """
    Wraps src data in a wrapper class, creates a crontab and returns
    a list with tuples that contain the BaseTask and dict with cron
    fields ("minute", "hour", "day", "month", "day_of_week")
    """

    if not data:
        logger.exception(f"Wrong tasks data")
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

        cron = cron.groups()
        cron = {f: cron[i] for i, f in enumerate(("minute", "hour", "day", "month", "day_of_week"))}

        task_class = get_task_class(src.get("scenario"))
        if task_class is None:
            continue

        tasks.append((task_class(**src), cron))

    return tasks, src_notifiers


def process(serialized_task: dict):
    """
    Runs scenario

    :param serialized_task: dict consisting of primitive types
    """
    task: BaseTask = BaseTask.deserialize(serialized_task)
    logger.info(f"Started task processing <{hash(serialized_task)}>")
    try:
        task.run()
    except Exception as e:
        logger.exception(f"Failed to complete task <{hash(serialized_task)}>: {e}")


def add_tasks(task: BaseTask, cron: dict):
    """
    Adds task to scheduler

    :param task: task object
    :param cron: dict with cron fields ("minute", "hour", "day", "month", "day_of_week")
    """
    serialized_task = task.serialize()
    scheduler.add_job(process, "cron", args=[serialized_task], replace_existing=True, **cron)
    logger.info(f"Added new periodic task: #{task.name}")


def run():
    """Gets tasks, adds them to the scheduler, and launches"""
    logger.info(f"Run manager-ai")

    data = None
    with open(TASKS_FILE_PATH, "r") as file:
        data = load(file)

    tasks_with_cron, notifiers = get_tasks_and_notifiers(data)
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
