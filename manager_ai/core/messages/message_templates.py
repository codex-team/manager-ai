import csv
import functools
import operator
from typing import List


def flatten(a):
    return functools.reduce(operator.iconcat, a, [])


"""Format keys:
    {days_count} -- days since last post
    {sad_emoji}
    {evil_emoji}
"""
with open('./templates/evil_emoji.csv', encoding='utf-8') as file:
    EVIL_EMOJI: List[str] = flatten(csv.reader(file, delimiter=' '))

with open('./templates/sad_emoji.csv', encoding='utf-8') as file:
    SAD_EMOJI: List[str] = flatten(csv.reader(file, delimiter=' '))

with open('./templates/first_time_messages.csv', encoding='utf-8') as file:
    FIRST_TIME_MESSAGES: List[str] = flatten(csv.reader(file, delimiter=' '))

with open('./templates/cycling_messages.csv', encoding='utf-8') as file:
    CYCLING_MESSAGES: List[str] = flatten(csv.reader(file, delimiter=' '))
