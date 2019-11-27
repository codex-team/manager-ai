from settings import logger
from tasks.base import BaseTask


class HelloWorldTask(BaseTask):
    """Simple task example"""

    def stdout_notify(self, message):
        logger.info(f"Notifies about {self.name} task by stdout_notify")
        print(message)

    def run(self) -> None:
        """Task execution logic"""

        logger.info(f"Executes {self.name} task")

        notify = getattr(self, f"{self.transport}_notify", None)
        if notify is None:
            logger.error(f"{self.transport} notifier not found in self.notifiers [task_name:{self.name}]")
            return None

        notify("Hello World!")
        return None
