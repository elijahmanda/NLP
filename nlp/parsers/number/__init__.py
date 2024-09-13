from typing import List

from nlp.entity import EntityParser
from nlp.tokens import Token
from nlp.constants import (
    NUMBER,
    CUSTOM,
    ENTITY,
)
from .config import Config
from .core import parse
from .data import Data
from .merger import Merger

__all__ = [
    "NumberParser",
    "Data",
    "Config"
]


class NumberParser(EntityParser):

    def __init__(self, config: Config = None):
        super().__init__()
        self.config = config or Config()
        self.data = Data(self.config)
        self._merger = Merger(self.data)

    def __call__(self, text: str) -> List[Token]:
        if not text.strip():
            return super().__call__(text)
        tokens: List[Token] = []
        numbers = parse(text, self.data)
        if not len(numbers):
            return super().__call__(text)
        for n in numbers:
            num = n.copy()
            num_string = num.pop("text")
            span = num.pop("span")
            metadata = num
            token = Token(
                num_string,
                span=span,
                entity=NUMBER,
                metadata=metadata,
            )
            tokens.append(token)
        if self.config.merge:
            tokens = self._merger.merge(tokens, text)
        last_start = tokens[0].span[0]
        last_end = tokens[0].span[1]
        i = 1
        while True:
            try:
                if tokens[i].span[0] == last_start or tokens[i].span[1] == last_end:
                    tokens.pop(i)
                else:
                    last_start, last_end = tokens[i].span
                    i += 1
            except IndexError:
                break
        return tokens


def get_parser() -> NumberParser:
    return NumberParser
