import unittest
import sys
from logging import getLogger
from io import StringIO
from src.tasks import BaseTask, HelloWorldTask, get_tasks_and_notifiers


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
        self.tasks_with_cron, notifiers = get_tasks_and_notifiers(_src_config)
        assert self.tasks_with_cron and notifiers, "Wrong config"
        self.saved_stdout, sys.stdout = sys.stdout, StringIO()
        BaseTask.set_notifiers(notifiers)

    def test_run(self):
        task: HelloWorldTask = self.tasks_with_cron[0][0]
        task.run()
        current_result = sys.stdout.getvalue().strip()
        right_result = "Hello World!"
        self.assertEqual(current_result, right_result)

    def test_serialize(self):
        task: HelloWorldTask = self.tasks_with_cron[0][0]
        current_result = task.serialize()
        right_result = _src_config.get("tasks")[0]
        self.assertEqual(current_result, right_result)

    def test_deserialize(self):
        task: HelloWorldTask = self.tasks_with_cron[0][0]
        serialized_task = task.serialize()
        deserialized_task: HelloWorldTask = HelloWorldTask.deserialize(serialized_task)
        self.assertEqual(deserialized_task, task)

    def tearDown(self):
        sys.stdout.close()
        sys.stdout = self.saved_stdout


if __name__ == "__main__":
    unittest.main()
