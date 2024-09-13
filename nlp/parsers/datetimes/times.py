
from .base import Word


class Time(Word):
    """
    12:30 AM -> to 16:30 | from monday to 
        Friday | February 16th | on Saturday
    """

    type = "time"
    follows_types = [
        "to",
        "from",
        "date",
        "on",
    ]


def register_words() -> None:
    words = [Time]
    from .factory import WordFactory
    WordFactory.register_words(words)


register_words()
