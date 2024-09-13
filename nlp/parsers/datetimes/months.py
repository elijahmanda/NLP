
from .constants import (
    MONTHS,
    MONTH_ALIAS,
)
from .base import Word


class Month(Word):
    """
    January -> on Monday | last year |
        next month |
    """

    type = "month"
    words = [*MONTHS, *MONTH_ALIAS]
    follows_types = [
        "on",
        "last",
        "next",
        "day",
        "year",
    ]


def register_words() -> None:
    words = [Month]
    from .factory import WordFactory
    WordFactory.register_words(words)


register_words()
