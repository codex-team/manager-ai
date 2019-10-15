from celery import Celery
from celery.utils.log import get_task_logger

from services import Service
from settings import *

logger = get_task_logger('general')
app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


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
