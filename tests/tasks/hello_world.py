import unittest
import sys
from logging import getLogger
from io import StringIO

from src.controller import Controller
from src.notifiers.stdout import StdoutNotifier
from src.tasks.hello_world import HelloWorldTask

logger = getLogger("test")

_src_config = {
    "tasks": {
        "HelloWorld": {
            "name": "Hello World",
            "schedule": "1 2 3 4 5",
            "scenario": "hello_world",
            "notifier": "stdout"
        },
    }
}


class TestBaseTask(unittest.TestCase):
    """
        BaseTask testing
    """

    def setUp(self):
        self.tasks = Controller.get_tasks(src_tasks=_src_config.get("tasks"))
        assert self.tasks, "Wrong config"
        self.saved_stdout, sys.stdout = sys.stdout, StringIO()

    def test_run(self):
        task: HelloWorldTask = self.tasks[0]
        task.notifier = StdoutNotifier
        task.run()
        current_result = sys.stdout.getvalue().strip()
        right_result = "Hello World!"
        self.assertEqual(current_result, right_result)

    def test_serialize(self):
        task: HelloWorldTask = self.tasks[0]
        current_result = task.serialize()
        right_result = list(_src_config.get("tasks").values())[0]
        self.assertEqual(current_result, right_result)

    def test_deserialize(self):
        task: HelloWorldTask = self.tasks[0]
        serialized_task = task.serialize()
        deserialized_task: HelloWorldTask = HelloWorldTask.deserialize(serialized_task, HelloWorldTask)
        self.assertEqual(deserialized_task, task)

    def tearDown(self):
        sys.stdout.close()
        sys.stdout = self.saved_stdout


if __name__ == "__main__":
    unittest.main()
