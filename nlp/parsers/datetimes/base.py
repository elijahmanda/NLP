from __future__ import annotations

from contextlib import suppress
from typing import (
    List,
    ClassVar,
    Callable,
    TypeVar,
    Union,

)

from nlp.utils.sequences import AllEqual
from nlp.utils.strings import remove_multiple_spaces


T = TypeVar("T")
NEG_INFINITY = -float("inf")


class Word:

    words: List[str] = []
    follows_words: List[str] = []
    follows_types: List[str] = []
    follow_validators: List[Callable[[Union[str, Word]], bool]] = []
    type: str = None

    def __init__(self, word: str = None):
        if self.words:
            assert word.lower() == AllEqual(self.words)
        self.word = word
        self.__validators_setup: bool = False
        self.setup_validators()

    def _setup_validators(self) -> None:
        pass

    def setup_validators(self) -> None:
        if not self.__validators_setup:
            self._setup_validators()
            self.__validators_setup = True

    def add_validator(self, validator: Callable[[Union[str, Word]], bool]):
        if validator in self.follow_validators:
            return
        self.follow_validators.append(validator)

    def can_follow(self, word: Word) -> bool:
        if self.follows_words:
            all_equal = AllEqual(self.follows_words)
            if all_equal == str(word.word).lower():
                return True
        if self.follows_types:
            if word.type in self.follows_types:
                return True
        if self.follow_validators:
            for validator in self.follow_validators:
                with suppress(Exception):
                    if validator(word):
                        return True
        return False

    def __eq__(self, other: Union[str, Word]) -> bool:
        if self.is_word(other):
            return self.type == other.type
        if not isinstance(other, str):
            return False

        other = str(other).lower().strip()
        other = remove_multiple_spaces(other)
        all_equal = AllEqual(self.words)
        return all_equal.__eq__(other)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.word!r})"

    def __str__(self):
        return self.word

    def __hash__(self):
        return hash(tuple(self.words)) + hash(self.word)

    @classmethod
    def is_word(cls, other):
        return issubclass(other.__class__, Word)


class Phrase:

    type: ClassVar[str] = None
    connections: ClassVar[List[List[Word]]]

    def __init__(self):
        self._words: List[Word] = []
        self._current_index: int = 0
        self._correct_paths = self.connections.copy()
        self._startswith = [conn[0] for conn in self._correct_paths]
        self._is_complete = False

    def is_complete(self) -> bool:
        return self._is_complete

    def connect(self, word: Word) -> bool:
        can_follow, to_remove = self._can_follow(word)
        if can_follow:
            self._words.append(word)
            minus = 0
            for index in to_remove:
                self._correct_paths.pop(index - minus)
                minus += 1
            self._startswith = [conn[0] for conn in self._correct_paths]
            self._current_index += 1
        return can_follow

    def _can_follow(self, word: Word) -> bool:

        to_remove = []
        follow = False
        for i, conns in enumerate(self._correct_paths):
            try:
                if conns[self._current_index] == word.type and (self._words[-1].can_follow(word) if self._words else True):
                    follow = True
                else:
                    to_remove.append(i)
            except IndexError:
                self._is_complete = True
        return follow, to_remove

    def can_follow(self, word: Union[str, Word]) -> bool:
        return self._can_follow(word)[0]


class Sentence:

    type: ClassVar[str] = None
    connections: ClassVar[List[List[Phrase]]]

    def __init__(self):
        self._phrases: List[Phrase] = []
        self._current_index: int = 0
        self._correct_paths = self.connections.copy()
        self._startswith = [conn[0] for conn in self._correct_paths]
        self._is_complete = False

    def is_complete(self) -> bool:
        return self._is_complete

    def connect(self, phrase: Phrase) -> bool:
        can_follow, to_remove = self._can_follow(phrase)
        if can_follow:
            self._phrases.append(phrase)
            minus = 0
            for index in to_remove:
                self._correct_paths.pop(index - minus)
                minus += 1
            self._startswith = [conn[0] for conn in self._correct_paths]
            self._correct_paths = list(
                filter(lambda x: x > len(self._phrases), self._phrases))
            self._current_index += 1
        return can_follow

    def _can_follow(self, phrase: Phrase) -> bool:
        to_remove = []
        follow = False
        for i, conns in enumerate(self._correct_paths):
            try:
                if conns[self._current_index] == phrase.type \
                        and (self._phrases[-1].can_follow(phrase._words[-1]) if self._phrases else True):
                    follow = True
                else:
                    to_remove.append(i)
            except IndexError:
                self._is_complete = True
        return follow, to_remove

    def can_follow(self, phrase: Phrase) -> bool:
        return self._can_follow(phrase)[0]
