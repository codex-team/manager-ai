from typing import List

"""
    Format keys:
        {days_count}: days since last post
        {evil_emoji}: ... 
        {sad_emoji}:  ...
"""

EVIL_EMOJI: List[str] = ['😡', '🦍', '☹', '️😤', '🤬', '😡', '😑', '😐', '👿', '😾']

SAD_EMOJI: List[str] = ['😓', '🤥', '😞', '😒', '😔', '😟', '😕', '🙁', '☹', '😣', '😖',
                        '😫', '😩', '😢', '😭', '😧', '😦', '😯', '😬', '🤕', '😿']

FIRST_TIME_MESSAGES: List[str] = [
    'Надо что-нибудь опубликовать в канале',
    'Пора что-нибудь поставить в телеграм',
    'Пришло время опубликовать новый пост в канале',
    'Нам надо опубликовать что-нибудь новое',
    'Напишите что-нибудь для телеграма',
    'Постов в канале не было уже {days_count} дней',
    'В канале {days_count} дней ничего не было, поставьте пост',
]

SECOND_TIME_MESSAGES: List[str] = [
    'Ну же',
    'Пожалуйста',
    'Сделайте это',
    'Пора',
    'Выделите 15 минут',
    'Я никуда не уйду',
    'Поставьте уже',
    'Нужен пост',
    'Надо',
    'Когда будет?',
    'Это важно',
    'Давайте сделаем уже',
    'Я жду',
    'Все ждут',
    'Когда будет пост?',
    'Надо что-нибудь придумать',
    'У кого есть идеи?',
    'Скидывайте идеи',
    'Ну хоть кто-то?',
    'Ребята',
    'Напоминаю',
    'Напоминаю про пост',
    'Сегодня надо сделать',
    'Это дело важное',
    'Будет пост?',
    'Пост будет?',
    'Можно рассказать о какой-нибудь библиотеке',
    'Я уже устал',
    '{evil_emoji}',
    '{sad_emoji}',
]
