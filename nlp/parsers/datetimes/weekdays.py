
from .constants import (
    WEEKDAYS,
    WEEKDAY_ALIAS,
)
from .base import Word


class Weekday(Word):
    """
    Monday -> at 6pm| on the 23rd|
        12:30AM CAT | 12 feb 1990
    """

    type = "weekday"
    words = [*WEEKDAYS, *WEEKDAY_ALIAS]
    follows_types = [
        "at",
        "on",
        "time",
        "date",
    ]


def register_words() -> None:
    words = [Weekday]
    from .factory import WordFactory
    WordFactory.register_words(words)


register_words()
