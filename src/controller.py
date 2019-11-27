from copy import deepcopy
from importlib import import_module
from typing import Tuple, List, Union, Dict

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from src.settings import *
from src.tasks.base import BaseTask

scheduler = BlockingScheduler()
scheduler.configure(**SCHEDULER)


class Controller:
    """
    A class that parses a configuration file,
    sets tasks to be executed using apscheduler.
    """

    @classmethod
    def _create_class_name(cls, module_name: str, class_type: str):
        """
        Create {class_type} class name by its {module_name}.
        Example:
             controller._create_class_name("hello_world", "Task") -> "HelloWorldTask"

        :param module_name: name of the module
        :param class_type: type of the class (Task / Notifier)
        """

        class_name = f"{''.join(word.title() for word in module_name.split('_'))}{class_type.title()}"
        return class_name

    @classmethod
    def _get_class(cls, folder: str, module_name: str, class_name: str):
        """
        Get reference to a class.
            Example:
                 _get_class("src.tasks", "hello_world", "HelloWorldTask") ->
                                                        :class:`src.tasks.hello_world.HelloWorldTask`

        :param folder: name of the folder with class module
        :param module_name: name of the class module
        :param class_name: name of the class

        :return: Ref to a class or None [If class is not found]
        """

        try:
            _class = getattr(import_module(f"{folder}.{module_name}"),
                             class_name, None)
        except ModuleNotFoundError:
            _class = None

        if not _class:
            logger.error(f"{class_name} not found in '{folder}.{module_name}'.")
            return None

        return _class

    @classmethod
    def _get_task_class(cls, scenario_name: str):
        """Get reference to a task class by scenario name."""

        return cls._get_class("src.tasks", scenario_name,
                              cls._create_class_name(scenario_name, "Task"))

    @classmethod
    def _get_notifier_class(cls, notifier_name: str):
        """Get reference to a notifier class by its name."""

        return cls._get_class("src.transports", notifier_name,
                              cls._create_class_name(notifier_name, "Notifier"))

    @classmethod
    def task_handler(cls, serialized_task: dict):
        """Runs scenario

        :param serialized_task: dict consisting of primitive types
        """

        task_class = cls._get_task_class(serialized_task.get("scenario"))
        task = BaseTask.deserialize(serialized_task, task_class)
        task.transport = cls._get_notifier_class(serialized_task.get("transport"))

        logger.info(f"Started task processing <{serialized_task['name']}>")
        try:
            task.run()
        except Exception as e:
            logger.exception(f"Failed to complete task <{serialized_task['name']}>: {e}")
            return

        logger.info(f"Finished task processing <{serialized_task['name']}>")

    @classmethod
    def get_tasks(cls, src_tasks: Dict[str, dict] = SRC_TASKS) -> Union[List[BaseTask], None]:
        """
        Wraps src src_tasks in a wrapper class, creates a crontab and returns
        a list that contains :class:`BaseTask` objects.
        """

        src_tasks = deepcopy(src_tasks)

        if not src_tasks or type(src_tasks) is not dict:
            logger.exception(f"Wrong tasks src_tasks")
            return None

        tasks = []
        for src_task in src_tasks.values():
            task_class = cls._get_task_class(src_task.get("scenario"))
            if task_class is None:
                logger.error(f"Wrong scenario for <{src_task.get('name', 'task')}>.")
                continue

            task_notifier = cls._get_notifier_class(src_task.get("transport"))
            if task_notifier is None:
                logger.error(f"Wrong transport for <{src_task.get('name', 'task')}>.")
                continue

            tasks.append(task_class(**src_task))

        return tasks

    @classmethod
    def _add_task(cls, task: BaseTask):
        """
        Adds task to scheduler

        :param task: task object
        """

        schedule = task.schedule
        serialized_task = task.serialize()
        scheduler.add_job(
            cls.task_handler,
            CronTrigger.from_crontab(schedule),
            [serialized_task],
            replace_existing=True
        )
        logger.info(f"Added new periodic task: <{task.name}>")

    @classmethod
    def run(cls):
        """Gets tasks, adds them to the scheduler, and launches"""

        logger.info(f"Run manager-ai")
        tasks = cls.get_tasks()

        if tasks:
            logger.info(f"Found {len(tasks)} new tasks in {CONFIG_FILE_PATH}")

            for task in tasks:
                cls._add_task(task)

            scheduler.start()
        else:
            logger.error(f"Failed to load tasks from {CONFIG_FILE_PATH}.")


if __name__ == "__main__":
    controller = Controller()
    controller.run()
