from __future__ import annotations

from typing import Optional
from dataclasses import dataclass, asdict

from nlp.parsers import load_parser
from .base import Word


class Updateable:

    def update(self, new):
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)


@dataclass
class TimeNumber(Word, Updateable):
    word: Optional[str] = None
    lt: Optional[float] = None
    gt: Optional[float] = None
    eq: Optional[float] = None
    be_int: bool = False
    be_float: bool = False
    be_ordinal: bool = False

    type = "number"
    follows_types = ["timeunit"]

    def __post_init__(self):
        if issubclass(self.word.__class__, TimeNumber):
            new = asdict(self.word)
            new["word"] = str(new["word"])
            self.update(new)

        assert not ((self.lt or self.gt) and self.eq)
        assert not (self.be_int and self.be_float)
        self._value = None
        self._metadata = {}
        self._np = load_parser("number")
        self.setup()
        if self.word is not None:
            if not isinstance(self.word, (int, float)):
                v, m = self.get_value(self.word)
                self._value = v
                self._metadata = m
            else:
                self._value = self.word
                self.word = str(self.word)
            assert self.validate()

    @property
    def value(self):
        return self._value

    def setup(self):
        pass

    def get_value(self, word):

        if word is None:
            return None, {}
        value = word
        metadata = {}
        if not isinstance(word, (int, float)):
            value = str(word)
            tks = self._np(value)
            if 1 < len(tks) > 1:
                return None, {}
            token = tks[0]
            if token.text != value:
                return None, {}
            metadata = token.metadata
            value = token.metadata["value"]
        return value, metadata

    def validate(self, value=None):

        if value is None:
            value, metadata = self._value, self._metadata
        else:
            value, metadata = self.get_value(value)

        try:
            if self.be_ordinal and metadata.get("number_type") != "ordinal":
                return False
            if self.be_int:
                assert isinstance(value, int)
            if self.be_float:
                assert isinstance(value, float)
            if self.lt is not None:
                assert value < self.lt
            if self.gt is not None:
                assert value > self.gt
            if self.eq is not None:
                assert (self._value is not None and value == self._value)
            return True
        except AssertionError:

            return False

    def __eq__(self, other: TimeNumber):
        if not isinstance(other, (TimeNumber, str, float, int)):
            return False
        if isinstance(other, self.__class__):
            if other.value is not None:
                return self.value == other.value
            return True
        return self.validate(other)

    def __repr__(self):
        if self.word:
            return f"{self.__class__.__name__}({self.word!r})"
        return f"{self.__class__.__name__}()"


class Microsecond(TimeNumber):

    type = "microsecond"

    def setup(self):
        self.lt = 1e6
        self.gt = 0
        self.be_int = True

    def _setup_validators(self):
        self.add_validator(self.validate_microsecond)
        self.add_validator(self.validate_microseconds)

    def validate_microsecond(self, word: Word) -> bool:
        if self.value in range(-1, 2) and word.type == "timeunit" and word.eq_unit("microsecond"):
            return True
        return False

    def validate_microseconds(self, word: Word) -> bool:
        if self.value not in range(-1, 2) and word.type == "timeunit" and word.eq_unit("microseconds"):
            return True
        return False


class Millisecond(TimeNumber):

    type = "millisecond"

    def setup(self):
        self.lt = 1000
        self.gt = 0

    def _setup_validators(self):
        self.add_validator(self.validate_millisecond)
        self.add_validator(self.validate_milliseconds)

    def validate_millisecond(self, word: Word) -> bool:
        if self.value in range(-1, 2) and word.type == "timeunit" and word.eq_unit("microsecond"):
            return True
        return False

    def validate_milliseconds(self, word: Word) -> bool:
        if self.value not in range(-1, 2) and word.type == "timeunit" and word.eq_unit("milliseconds"):
            return True
        return False


class Second(TimeNumber):

    type = "second"

    def setup(self):
        self.lt = 60
        self.gt = 0
        self.be_int = True

    def _setup_validators(self):
        self.add_validator(self.validate_second)
        self.add_validator(self.validate_seconds)

    def validate_second(self, word: Word) -> bool:
        if self.value in range(-1, 2) and word.type == "timeunit" and word.eq_unit("second"):
            return True
        return False

    def validate_seconds(self, word: Word) -> bool:
        if self.value not in range(-1, 2) and word.type == "timeunit" and word.eq_unit("seconds"):
            return True
        return False


class Minute(TimeNumber):

    type = "minute"

    def setup(self):
        self.lt = 60
        self.gt = -1
        self.be_int = True

    def _setup_validators(self):
        self.add_validator(self.validate_minute)
        self.add_validator(self.validate_minutes)

    def validate_minute(self, word: Word) -> bool:
        if self.value in range(-1, 2) and word.type == "timeunit" and word.eq_unit("minute"):
            return True
        return False

    def validate_minutes(self, word: Word) -> bool:
        if self.value not in range(-1, 2) and word.type == "timeunit" and word.eq_unit("minutes"):
            return True
        return False


class Hour(TimeNumber):

    type = "hour"

    def setup(self):
        self.lt = 24
        self.gt = -1
        self.be_int = True

    def _setup_validators(self):
        self.add_validator(self.validate_hour)
        self.add_validator(self.validate_hours)

    def validate_hour(self, word: Word) -> bool:
        if self.value in range(-1, 2) and word.type == "timeunit" and word.eq_unit("hour"):
            return True
        return False

    def validate_hours(self, word: Word) -> bool:
        if self.value not in range(-1, 2) and word.type == "timeunit" and word.eq_unit("hours"):
            return True
        return False


class Day(TimeNumber):

    type = "day"
    follows_types = ["month"]

    def setup(self):
        self.lt = 32
        self.gt = 0
        self.be_int = True

    def _setup_validators(self):
        self.add_validator(self.validate_day)
        self.add_validator(self.validate_days)

    def validate_day(self, word: Word) -> bool:
        if self.value in range(-1, 2) and word.type == "timeunit" and word.eq_unit("day"):
            return True
        return False

    def validate_days(self, word: Word) -> bool:
        if self.value not in range(-1, 2) and word.type == "timeunit" and word.eq_unit("days"):
            return True
        return False


class Month(TimeNumber):

    type = "month_number"

    def setup(self):
        self.lt = 13
        self.gt = 0
        self.be_int = True

    def _setup_validators(self):
        self.add_validator(self.validate_month_number)
        self.add_validator(self.validate_months_number)

    def validate_month_number(self, word: Word) -> bool:
        if self.value == 0 and word.type == "timeunit" and word.eq_unit("month"):
            return True
        return False

    def validate_months_number(self, word: Word) -> bool:
        if self.value > 0 and word.type == "timeunit" and word.eq_unit("months"):
            return True
        return False


class Year(TimeNumber):

    type = "year"

    def setup(self):
        self.lt = 2100
        self.gt = 1600
        self.be_int = True

    def _setup_validators(self):
        self.add_validator(self.validate_year)
        self.add_validator(self.validate_years)

    def validate_year(self, word: Word) -> bool:
        if self.value == 1 and word.type == "timeunit" and word.eq_unit("year"):
            return True
        return False

    def validate_years(self, word: Word) -> bool:
        if self.value > 1 and word.type == "timeunit" and word.eq_unit("years"):
            return True
        return False


class Int(TimeNumber):

    type = "integer"

    def setup(self):
        self.be_int = True


class Float(TimeNumber):

    type = "float"

    def setup(self):
        self.be_float = True


class GT_0_Int(TimeNumber):

    type = "gt_0_int"

    def setup(self):
        self.gt = 0
        self.be_int = True


class GT_0_Float(TimeNumber):

    type = "gt_0_float"

    def setup(self):
        self.gt = 0
        self.be_float = True
