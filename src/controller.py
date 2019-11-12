import re
from logging import getLogger
from typing import Tuple, List, Union

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import yaml

from src.tasks import TaskWrapper
from config.settings import *

logger = getLogger("general")
scheduler = BlockingScheduler()
scheduler.configure(**SCHEDULER)


class Controller:
    def get_tasks(self) -> Union[List[Tuple[TaskWrapper, Dict]], None]:
        """Parses the task file, wraps it in a wrapper
        class, creates a crontab and returns a list with
        tuples that contain the TaskWrapper and dict
        with cron fields ("minute", "hour", "day",
        "month", "day_of_week")"""
        data = None
        with open(TASKS_FILE_PATH, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        if not data:
            logger.exception(f"Wrong tasks structure in {TASKS_FILE_PATH}")
            return None

        src_tasks = data.get("tasks", [])
        src_notifiers = data.get("notifiers", [])

        # TODO: write normal wrapping data to TaskWrapper when creating the controller
        tasks = []
        for src in src_tasks:
            schedule = src.get("schedule", "").strip()
            print(schedule)
            tasks.append((TaskWrapper(**src), schedule))

        TaskWrapper.notifiers = src_notifiers
        return tasks

    @staticmethod
    def process(serialized_task: dict):
        """Runs scenario

        :param serialized_task: dict consisting of primitive types
        """
        task: TaskWrapper = TaskWrapper.deserialize(serialized_task)
        logger.info(f"Started task processing <{serialized_task['name']}>")
        try:
            task.run()
        except Exception as e:
            logger.exception(f"Failed to complete task <{serialized_task['name']}>: {e}")

    def add_tasks(self, task: TaskWrapper, schedule):
        """Adds task to scheduler

        :param task: task object
        :param schedule: string with cron
        """
        serialized_task = task.serialize()
        scheduler.add_job(
            self.process,
            CronTrigger.from_crontab(schedule),
            args=[serialized_task],
            replace_existing=True
        )
        logger.info(f"Added new periodic task: #{task.name}")

    def run(self):
        """Gets tasks, adds them to the scheduler, and launches"""
        logger.info(f"Run manager-ai")
        tasks_with_cron = self.get_tasks()
        logger.info(f"Found {len(tasks_with_cron)} new tasks in {TASKS_FILE_PATH}")
        for task, schedule in tasks_with_cron:
            self.add_tasks(task, schedule)
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass


if __name__ == "__main__":
    controller = Controller()
    controller.run()
