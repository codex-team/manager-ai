
class TaskException(Exception):
    pass


class BaseTask:
    """Base task wrapper"""

    def __init__(self, name, schedule, transport, scenario, **kwargs):
        # TODO: explicitly specify the parameters that are used in all tasks
        self.name = name
        self.transport = transport
        self.scenario = scenario
        self._arg_names = list(kwargs.keys()) + ["name", "scenario", "schedule", "transport"]  # saving arg names for serialization
        self.__dict__.update(kwargs)  # setting all the passed parameters
        self.schedule = schedule


    def run(self):
        """
        Executes the task. Base class level.

        :raise NotImplementedError: If `_run` method is not implemented
        """
        # TODO: add some checks here
        self._run()

    def _run(self):
        """
        Executes the task. Implemented class level.
        :raise NotImplementedError: If `_run` method is not implemented
        """
        raise NotImplementedError("Implement this method in an inherited class")

    def serialize(self, full=False) -> dict:
        """Converts the task object to a dict consisting of primitive types"""

        serialized_task = {}
        for key in self._arg_names:
            serialized_task.update({key: self.__getattribute__(key)})

        return serialized_task

    @classmethod
    def deserialize(cls, kwargs: dict, task_class) -> "BaseTask":
        """Deserializes task

        :param task_class: task class
        :param kwargs: dict with src task fields
        """
        return task_class(**kwargs)

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