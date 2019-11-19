from typing import List, Union

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from src.settings import *
from importlib import import_module

from src.tasks import TaskWrapper

logger = getLogger("general")
scheduler = BlockingScheduler()
scheduler.configure(**SCHEDULER)


class TasksController:
    """A class that parses a configuration file,
    sets tasks to be executed using apscheduler"""

    def get_tasks(self) -> Union[List[TaskWrapper], None]:
        """Parses the task file, wraps it in a wrapper
        class, returns a list with
        tuples that contain the TaskWrapper and schedule"""

        # TODO: write normal wrapping data to TaskWrapper when creating the controller
        tasks = []
        for src in SRC_TASKS:
            scenario = import_module("src.scenarios."+src["scenario"])
            task = scenario.export
            tasks.append(task(**src))

        TaskWrapper.notifiers = SRC_NOTIFIERS
        return tasks

    def process(self, serialized_task: dict):
        """Runs scenario

        :param serialized_task: dict consisting of primitive types
        """

        task = TaskWrapper.deserialize(serialized_task)
        logger.info(f"Started task processing <{serialized_task['name']}>")
        try:
            task.run()
        except Exception as e:
            logger.exception(f"Failed to complete task <{serialized_task['name']}>: {e}")

    def add_tasks(self, task: TaskWrapper):
        """Adds task to scheduler

        :param task: task object
        """
        schedule = task.schedule
        serialized_task = task.serialize()
        scheduler.add_job(
            self.process,
            CronTrigger.from_crontab(schedule),
            [serialized_task],
            replace_existing=True
        )
        logger.info(f"Added new periodic task: #{task.name}")

    def run(self):
        """Gets tasks, adds them to the scheduler, and launches"""

        logger.info(f"Run manager-ai")
        tasks_with_cron = self.get_tasks()
        logger.info(f"Found {len(tasks_with_cron)} new tasks in {CONFIG_FILE_PATH}")

        for task in tasks_with_cron:
            self.add_tasks(task)

        scheduler.start()


if __name__ == "__main__":
    controller = TasksController()
    controller.run()
