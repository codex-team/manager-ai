class TaskWrapper:
    """Simple wrapper for task data"""

    def __init__(self, **kwargs):
        # TODO: fix hardcode
        self._kwargs = kwargs  # saving src data for serialization
        self.__dict__.update(kwargs)  # setting all the passed parameters
        self.schedule = kwargs.get("schedule", "").strip()

    def run(self):
        """Executes the task, namely checks and, if necessary, sends data."""

        # TODO: implement this method when creating the controller
        pass

    def serialize(self) -> dict:
        """Converts the task object to an dict consisting of primitive types"""
        # TODO: fix hardcode
        return self._kwargs

    @classmethod
    def deserialize(cls, kwargs: dict) -> "TaskWrapper":
        """Deserializes task

        :param kwargs: dict with src task fields
        """
        return cls(**kwargs)

