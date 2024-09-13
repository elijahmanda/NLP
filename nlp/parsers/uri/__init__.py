from typing import List

from nlp.tokens import Token
from nlp.constants import (
    URI,
    ENTITY,
    CUSTOM,
)
from nlp.entity import EntityParser
from .parser import parse


def get_parser() -> "URIParser":
    return URIParser


class URIParser(EntityParser):

    def __call__(self, text: str):
        results = []
        parse_res = parse(text)
        for res in parse_res:
            results.append(Token(
                text=res["text"],
                span=res["span"],
                entity=URI,
                metadata=res["metadata"],
            ))
        return results
