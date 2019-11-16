from copy import deepcopy
from typing import Tuple, List, Union

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from src.tasks import BaseTask, TaskException
from src.settings import *
from . import tasks

logger = getLogger("general")
scheduler = BlockingScheduler()
scheduler.configure(**SCHEDULER)


def task_handler(serialized_task: dict):
    """Runs scenario

    :param serialized_task: dict consisting of primitive types
    """

    task = BaseTask.deserialize(serialized_task)
    logger.info(f"Started task processing <{serialized_task['name']}>")
    try:
        task.run()
    except Exception as e:
        logger.exception(f"Failed to complete task <{serialized_task['name']}>: {e}")


class Controller:
    """
    A class that parses a configuration file,
    sets tasks to be executed using apscheduler
    """

    _notifiers = SRC_NOTIFIERS

    @classmethod
    def _create_task_class_name(cls, task_name):
        """
        Create task class name.
        Example:
             controller._create_task_class_name("hello_world") -> "HelloWorldTask"

        :param task_class_name: name of task class
        """

        task_class_name = f"{''.join(word.title() for word in task_name.split('_'))}Task"
        return task_class_name

    @classmethod
    def _get_task_class(cls, task_class_name: str):
        """
        Looking for class by task name.
        Example:
             _get_task_class("HelloWorldTask") -> :class:`HelloWorldTask`
        :param task_class_name: name of task class
        :return: TaskBase class implementation or None [If task class for `scenario_name` is not found]
        """

        task_class = getattr(tasks, task_class_name, None)
        if task_class is None:
            logger.error(f"{task_class_name} not found")
        return task_class

    @classmethod
    def get_tasks(cls, src_tasks: List[dict] = SRC_TASKS, src_notifiers: List[dict] = SRC_NOTIFIERS) -> Union[List[BaseTask], None]:
        """
        Wraps src src_tasks in a wrapper class, creates a crontab and returns
        a list that contain :class:`BaseTask` objects.
        """

        src_tasks = deepcopy(src_tasks)
        cls._notifiers = src_notifiers

        if not src_tasks or type(src_tasks) is not list:
            logger.exception(f"Wrong tasks src_tasks")
            return None

        # TODO: write normal wrapping src_tasks to BaseTask when creating the controller
        tasks = []
        for src_task in src_tasks:
            task_class_name = cls._create_task_class_name(src_task.get("scenario"))
            task_class = cls._get_task_class(task_class_name)
            src_task.update({"notifiers": src_notifiers})
            if task_class is None:
                logger.exception(f"Wrong scenario for {src_task.get('name', 'task')}")
                continue

            tasks.append(task_class(**src_task))

        return tasks

    @classmethod
    def _add_tasks(cls, task: BaseTask):
        """
        Adds task to scheduler

        :param task: task object
        """

        schedule = task.schedule
        serialized_task = task.serialize()
        scheduler.add_job(
            task_handler,
            CronTrigger.from_crontab(schedule),
            [serialized_task],
            replace_existing=True
        )
        logger.info(f"Added new periodic task: <{task.name}>")

    @classmethod
    def run(cls):
        """Gets tasks, adds them to the scheduler, and launches"""

        if SRC_NOTIFIERS:
            logger.error(f"Notifiers is wrongs")
            return None

        logger.info(f"Run manager-ai")
        tasks = cls.get_tasks()

        logger.info(f"Found {len(tasks)} new tasks in {CONFIG_FILE_PATH}")

        for task in tasks:
            cls._add_tasks(task)

        scheduler.start()


if __name__ == "__main__":
    controller = Controller()
    controller.run()
