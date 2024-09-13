
from .base import Word


class Event(Word):
    """
    Christmas Eve -> at night | 25 dec | 
        6AM | last year | next week | 
        after 2PM | this month 
    """

    type = "event"
    follows_types = [
        "at",
        "date",
        "time",
        "last",
        "next",
        "after",
        "this",
    ]


def register_words() -> None:
    words = [Event]
    from .factory import WordFactory
    WordFactory.register_words(words)


register_words()
