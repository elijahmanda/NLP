from __future__ import annotations

from math import log10
from typing import Iterator, List, Optional

from more_itertools import windowed

from nlp.tokens import Token
from nlp.constants import NUMBER
from .core import generate_info
from .ejtoken import tokenize
from .normalize import Pipe


def _tok(text, data):
    return tokenize(Pipe(data)(text))


class Merger:

    def __init__(
        self,
        data,
        exceptions: List[str] = None,
        **kwargs,
    ) -> None:
        self.data = data
        self.config = data.config
        if exceptions is None:
            exceptions = ("hundred",)
        self.exceptions = set(exceptions)

    def merge_multiples(self, tokens: List[Token], og_text: str) -> Iterator[Token]:
        # num < 1000 -> multiple thousand, million, billion, ...

        multiples = set(filter(
            lambda x: x not in self.exceptions,
            self.data.MULTIPLES.keys()
        ))
        iterator = list(windowed(tokens, 2))
        i = 0
        last_start = None
        while True:
            try:
                t1, t2 = iterator[i]
                last_start = t2.span[0]
                value1 = t1.metadata["value"]
                value2 = t2.metadata["value"]

            except (IndexError, KeyError):
                break
            if t2 is None:
                if t1.span[0] != last_start:
                    yield t1
                break

            # or value1 > 1000:
            if _tok(t2.text.lower().strip(), self.data)[0] not in multiples:
                if t1.span[0] != last_start:

                    yield t1
                if (i + 1) == len(iterator) and t2 is not None:
                    yield t2
            else:
                span = (t1.span[0], t2.span[1])
                text = og_text[span[0]: span[1]]
                exponent = int(log10(value2))
                if abs(value1) >= 1:
                    value = (value1 * pow(10, exponent + 1)) + \
                        (value2 - pow(10, exponent))
                else:
                    value = value1 * value2
                tokens = _tok(text, self.data)
                info = generate_info(text, tokens, span,
                                     self.data, value=value)
                info.pop("span")
                yield Token(text, span=span, entity=NUMBER, metadata=info)
            i += 1

    def merge_points(self, tokens: List[Token], og_text: str) -> Iterator[Token]:
        return tokens

    def merge_informals(self, tokens: List[Token], og_text: str) -> Iterator[Token]:
        """
        5 and a quarter
        """

        i = 0
        last_start = None
        iterator = list(windowed(tokens, 2))
        while True:
            try:
                yielded = False
                t1, t2 = iterator[i]
                last_start = t2.span[0]
            except Exception:
                break
            if t2 is None:
                if t1.span[0] != last_start:
                    yield t1
                break
            t_and = og_text[t1.span[1]: t2.span[0]].strip().lower().split()
            _and = t_and == ["and"] or t_and == ["and", "a"] and t2.text.lower(
            ) in [*self.data.INFORMAL_EXACT, *self.data.INFORMALS_MULTIPLYABLE]

            if not _and:
                if t1.span[0] != last_start:
                    yield t1
                if (i + 1) == len(iterator) and t2 is not None:
                    yield t2
            else:
                span = t1.span[0], t2.span[1]
                text = og_text[span[0]: span[1]]
                value = t1.metadata["value"] + t2.metadata["value"]
                metadata = {
                    "value": value,
                    "number_type": "spoken",
                    "value_type": "integer" if isinstance(value, int) else "float"
                }
                yielded = True
                yield Token(text, span=span, metadata=metadata, entity=NUMBER)

            i += 1

    def merge(self, tokens: List[Token], og_text: str) -> List[Token]:
        if len(tokens) <= 1:
            return tokens
        new_tokens = tokens
        if self.config.merge_multiples:
            new_tokens = list(self.merge_multiples(
                tokens, og_text)) or new_tokens

        if self.config.merge_points:
            new_tokens = list(self.merge_points(
                new_tokens, og_text)) or new_tokens
        if self.config.merge_informals:
            new_tokens = list(self.merge_informals(
                new_tokens, og_text)) or new_tokens
        return new_tokens
