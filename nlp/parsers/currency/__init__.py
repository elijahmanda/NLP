from typing import List, Type

from nlp.entity import EntityParser
from nlp.tokens import Token


from .tokenizer import CurrencyTokenizer


class CurrencyParser(EntityParser):

    def __init__(self):
        super().__init__()
        self.tokenizer = CurrencyTokenizer()

    def __call__(self, text: str) -> List[Token]:
        if not text.strip():
            return super().__call__(text)
        return self.tokenizer.tokenize(text)


def get_parser(**kwargs) -> Type[EntityParser]:
    return CurrencyParser
