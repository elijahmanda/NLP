
from .base import Word


class Date(Word):
    follows_types = [
        "to",
        "from",
        "time",
        "on",
    ]
    type = "date"


def register_words() -> None:
    words = [Date]
    from .factory import WordFactory
    WordFactory.register_words(words)


register_words()
