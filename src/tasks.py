class TaskWrapper:
    """Simple wrapper for task data"""

    def __init__(self, src):
        # TODO: fix hardcode
        self.src = src  # saving src data for serialization
        self.schedule = src.get("schedule", "").strip()

    def run(self):
        """Executes the task, namely checks and, if necessary, sends data."""

        # TODO: implement this method when creating the controller
        pass

    def serialize(self) -> dict:
        """Converts the task object to an dict consisting of primitive types"""
        # TODO: fix hardcode
        return self.src

    @classmethod
    def deserialize(cls, src) -> "TaskWrapper":
        """Deserializes task

        :param kwargs: dict with src task fields
        """
        return cls(src)

