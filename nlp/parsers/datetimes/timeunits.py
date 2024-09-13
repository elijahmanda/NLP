from functools import lru_cache

from nlp.utils.sequences import AllEqual
from .constants import (
    TIMEUNITS_SINGULAR,
    TIMEUNITS_PLURAL,
    TIMEUNITS_ALIAS
)
from .base import Word


class TimeUnit(Word):

    words = [
        *TIMEUNITS_SINGULAR,
        *TIMEUNITS_PLURAL,
        *TIMEUNITS_ALIAS,
    ]
    type = "timeunit"

    __eq_cache = {}

    @property
    @lru_cache()
    def is_singular(self) -> bool:
        word = self.word.lower()
        if word in TIMEUNITS_SINGULAR:
            return True
        elif word in TIMEUNITS_ALIAS:
            alias = TIMEUNITS_ALIAS[word]
            return len(alias) > 1 or alias[0][-1] != "s"
        return False

    @property
    @lru_cache()
    def is_plural(self) -> bool:
        word = self.word.lower()
        if word in TIMEUNITS_PLURAL:
            return True
        elif word in TIMEUNITS_ALIAS:
            alias = TIMEUNITS_ALIAS[word]
            return len(alias) > 1 or alias[0][-1] == "s"
        return False

    def eq_unit(self, unit: str):
        if self.__eq_cache:
            return self.word.lower() == self.__eq_cache.get(unit.lower(), None)
        temp = {}
        for key, value in TIMEUNITS_ALIAS.items():
            value = tuple(value)
            for item in value:
                if item not in temp:
                    temp[item] = set()
                temp[item].update((key, item))
        for key, items in temp.items():
            temp[key] = AllEqual(items)
        self.__eq_cache = temp
        return self.word.lower() == self.__eq_cache.get(unit, None)


def register_words() -> None:
    words = [TimeUnit]
    from .factory import WordFactory
    WordFactory.register_words(words)


register_words()
