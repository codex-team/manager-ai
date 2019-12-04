from time import sleep

from settings import logger
from tasks.base import BaseTask


class HelloWorldTask(BaseTask):
    """Simple task example"""

    def run(self) -> None:
        """Task execution logic"""

        logger.info(f"Executes {self.name} task")
        sleep(1)
        notifier = self.notifier()
        notifier.notify("Hello World!")

        return None
