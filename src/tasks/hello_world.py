from src.settings import logger
from src.tasks.base import BaseTask


class HelloWorldTask(BaseTask):
    """Simple task example"""

    def stdout_notify(self, message):
        logger.info(f"Notifies about {self.name} task by ")
        print(message)

    def _run(self) -> None:
        """Task execution logic"""

        logger.info(f"Executes {self.name} task")
        notifier = tuple(filter(lambda ntfr: ntfr.get("name") == self.notifier, self.__class__._BaseTask__notifiers))
        if not notifier:
            logger.error(f"{self.notifier} notifier not found in self.notifiers [task_name:{self.name}]")
            return None
        notifier = notifier[0]
        notify = self.__getattribute__(f"{notifier.get('type')}_notify")  # getting class method by name
        notify("Hello World!")
        return None
