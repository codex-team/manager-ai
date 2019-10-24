import random
import unittest

from manager_ai.core.messages.message_creator import create_message


class TestMessageCreator(unittest.TestCase):

    def test_first_time(self) -> None:
        user_conf = {
            'days_count': random.randrange(1, 10),
            'first_time': True,
        }
        print(create_message(user_conf))

    def test_second_time(self) -> None:
        user_conf = {
            'days_count': random.randrange(1, 10),
            'first_time': False,
        }
        print(create_message(user_conf))

    def test_full_random(self) -> None:
        user_conf = {
            'days_count': random.randrange(1, 10),
            'first_time': random.choice([True, False]),
        }
        print(create_message(user_conf))


if __name__ == '__main__':
    unittest.main()
