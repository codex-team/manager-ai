from logging import getLogger

logger = getLogger("general")


class TaskException(Exception):
    pass


class BaseTask:
    """Base task wrapper"""
    __notifiers = None

    def __init__(self, name, schedule, notifiers=None, **kwargs):
        # TODO: explicitly specify the parameters that are used in all tasks
        self.name = name
        self._arg_names = list(kwargs.keys()) + ["name", "schedule"]  # saving arg names for serialization
        self._other_arg_names = ["_BaseTask__notifiers"]
        self.__dict__.update(kwargs)  # setting all the passed parameters
        self.schedule = schedule

        if self.__class__._BaseTask__notifiers is None:
            if notifiers is None and kwarg.get("_BaseTask__notifiers") is not None:
                notifiers = kwargs.get("_BaseTask__notifiers")
            self.__class__._BaseTask__notifiers = notifiers

    def run(self):
        """
        Executes the task. Base class level.
        :raise TaskException: If notifiers is not specified
        :raise NotImplementedError: If `_run` method is not implemented
        """
        if self.__class__._BaseTask__notifiers is None:
            raise TaskException("You did not specify notifiers, use BaseTask.set_notifiers method")
        self._run()

    def _run(self):
        """
        Executes the task. Implemented class level.
        :raise NotImplementedError: If `_run` method is not implemented
        """
        raise NotImplementedError("Implement this method in an inherited class")

    def serialize(self, full=False) -> dict:
        """Converts the task object to an dict consisting of primitive types"""
        serialized_task = {}
        for key in self._arg_names:
            serialized_task.update({key: self.__getattribute__(key)})
        if not full:
            return serialized_task

        for key in self._other_arg_names:
            serialized_task.update({key: getattr(self, key, getattr(self.__class__, key))})
        return serialized_task

    @classmethod
    def deserialize(cls, kwargs: dict) -> "BaseTask":
        """Deserializes task

        :param kwargs: dict with src task fields
        """
        return cls(**kwargs)

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
        notifier = tuple(filter(lambda ntfr: ntfr.get("name") == self.notifier, self.__class__._BaseTask__notifiers))
        if not notifier:
            logger.error(f"{self.notifier} notifier not found in self.notifiers [task_name:{self.name}]")
            return None
        notifier = notifier[0]
        notify = self.__getattribute__(f"{notifier.get('type')}_notify")  # getting class method by name
        notify("Hello World!")
        return None
