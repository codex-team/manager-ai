import unittest
import sys
from logging import getLogger
from io import StringIO
from src.tasks import BaseTask, HelloWorldTask
from src.controller import Controller
from src.settings import SRC_NOTIFIERS

logger = getLogger("test")

_src_config = {
    "tasks": [
        {
            "name": "Hello World",
            "schedule": "* * * * 1",
            "scenario": "hello_world",
            "notifier": "stdout writer"
        },
    ],
    "notifiers": [
        {
            "name": "Telegram",
            "type": "telegram",
            "webhook": "https://notify.bot.codex.so/u/R4ND0M"
        }, {
            "name": "Work Email",
            "type": "email",
            "address": "work@me.ru"
        }, {
            "name": "stdout writer",
            "type": "stdout"
        }
    ]
}


class TestBaseTask(unittest.TestCase):
    """
        BaseTask testing
    """

    def setUp(self):
        self.tasks = Controller.get_tasks(src_tasks=_src_config.get("tasks"), src_notifiers=_src_config.get("notifiers"))
        assert self.tasks, "Wrong config"
        self.saved_stdout, sys.stdout = sys.stdout, StringIO()

    def test_run(self):
        task: HelloWorldTask = self.tasks[0]
        task.run()
        current_result = sys.stdout.getvalue().strip()
        right_result = "Hello World!"
        self.assertEqual(current_result, right_result)

    def test_serialize(self):
        task: HelloWorldTask = self.tasks[0]
        current_result = task.serialize()
        right_result = _src_config.get("tasks")[0]
        self.assertEqual(current_result, right_result)

    def test_deserialize(self):
        task: HelloWorldTask = self.tasks[0]
        serialized_task = task.serialize(full=True)
        deserialized_task: HelloWorldTask = HelloWorldTask.deserialize(serialized_task)
        self.assertEqual(deserialized_task, task)

    def tearDown(self):
        sys.stdout.close()
        sys.stdout = self.saved_stdout


if __name__ == "__main__":
    unittest.main()
