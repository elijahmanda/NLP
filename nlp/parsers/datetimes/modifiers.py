
from .base import Word


class At(Word):

    type = "at"
    words = ["at"]
    follows_words = ["the"]
    follows_types = [
        "date",
        "time",
    ]


class On(Word):

    type = "on"
    words = ["on"]
    follows_words = ["the"]
    follows_types = [
        "weekday",
        "event",
    ]


class In(Word):

    type = "in"
    words = ["in"]
    follows_types = [
        "month",
    ]


class Of(Word):

    type = "of"
    words = ["of"]
    follows_types = [
        "month",
        # on the 27th of last/next month
        "next",
        "last",
    ]


class To(Word):

    type = "to"
    words = ["to"]
    follows_types = [
        "time",
        "date",
        "the",
    ]


class By(Word):

    type = "by"
    words = ["by"]
    follows_types = [
        "weekday",
        "time",
        "date",
        "month",
    ]


class From(Word):

    type = "from"
    words = ["from"]
    follows_types = [
        "month",
        "weekday",
        "next",
        "last",
        "date",
        "time",
        "the",
    ]


class After(Word):

    type = "after"
    words = ["after"]
    follows_types = [
        "the",
        "event",
        "date",
        "time",
        "next",
        "last",
    ]


class This(Word):

    type = "this"
    words = ["this"]
    follows_types = [
        "event",
        "weekday",
        "month",
    ]

    def _setup_validators(self):
        self.add_validator(self._validate_timeunit)

    def _validate_timeunit(self, word: Word):
        if word.type != "timeunit":
            return False
        return word.is_singular


class Before(Word):

    type = "before"
    words = ["before"]


class Last(Word):

    type = "last"
    words = ["last", "past", "previous"]
    follows_types = [
        "month",
        "weekday",
    ]

    def _setup_validators(self):
        self.add_validator(self._validate_timeunit)

    def _validate_timeunit(self, word: Word):
        if word.type != "timeunit":
            return False
        return word.is_singular


class Next(Word):

    type = "next"
    words = [
        "next",
        "following",
        "coming",
        "up coming",
    ]

    def _setup_validators(self):
        self.add_validator(self._validate_timeunit)

    def _validate_timeunit(self, word: Word):
        if word.type != "timeunit":
            return False
        return word.is_singular


class Until(Word):

    type = "until"
    words = ["until", "untill", "till"]
    follows_types = [
        "next", "last",
        "date", "time",
        "event", "month",
        "weekday", "the",
        "this",
    ]

    def _setup_validators(self):
        self.add_validator(self._validate_timeunit)

    def _validate_timeunit(self, word: Word):
        if word.type != "timeunit":
            return False
        return word.is_singular


class EndOf(Word):

    type = "end_of"
    words = ["end of"]
    follows_words = ["this", "the"]
    type = "endof"


class Ago(Word):

    type = "ago"
    words = ["ago"]
    type = "ago"


class The(Word):

    type = "the"
    words = ["the"]
    follows_types = ["last", "next"]
    type = "the"

    def _setup_validators(self):
        self.add_validator(self._validate_timeunit)

    def _validate_timeunit(self, word: Word):
        if word.type != "timeunit":
            return False
        return word.is_singular


class An(Word):

    type = "an"
    words = ["an"]
    type = "an"

    def _setup_validators(self):
        self.add_validator(self._validate_timeunit)

    def _validate_timeunit(self, word: Word):
        if word.type != "timeunit":
            return False
        return word.is_singular


class A(Word):

    type = "a"
    words = ["a"]
    type = "a"

    def _setup_validators(self):
        self.add_validator(self._validate_timeunit)

    def _validate_timeunit(self, word: Word):
        if word.type != "timeunit":
            return False
        return word.is_singular


def register_words() -> None:
    words = [
        At, On, In, Of, To, By, From, After,
        This, Before, Last, Next, Until, EndOf,
        Ago, The, An, A,
    ]
    from .factory import WordFactory
    WordFactory.register_words(words)


register_words()
