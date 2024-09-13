from __future__ import annotations

from typing import (
    Dict,
    ClassVar,
    Optional,
    List,
    Type,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from .base import Word


class WordFactory:

    __words__: ClassVar[Dict[Word, Type[Word]]] = {}

    @classmethod
    def get_class_by_text(cls, text: str) -> Optional[Type[Word]]:
        for instance, class_ in cls.__words__.items():
            if instance == text.lower():
                return class_

    @classmethod
    def get_class_by_type(cls, type_: str) -> Optional[Type[Word]]:
        for instance in cls.__words__:
            if instance.type == type_:
                return instance.__class__

    @classmethod
    def register_word(cls, word: Type[Word]) -> None:
        word = word(word.words[0]) if len(word.words) else word()
        cls.__words__[word] = word.__class__

    @classmethod
    def register_words(cls, words: List[Type[Word]]) -> None:
        for word in words:
            cls.register_word(word)
