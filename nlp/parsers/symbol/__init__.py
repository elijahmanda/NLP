import string
from typing import List

import regex as re

from nlp.entity import EntityParser
from nlp.tokens import Token
from nlp.tokenizers import RegexTokenizer
from nlp.constants import SYMBOL, ENTITY, CUSTOM

_puncts = "".join(string.punctuation.split())
_puncts = re.escape(_puncts)
_PUNCT_PATTERN = f"[{_puncts}]"
_tokenizer = RegexTokenizer([(_PUNCT_PATTERN, SYMBOL)])


def get_parser() -> "SymbolParser":
    return SymbolParser


class SymbolParser(EntityParser):

    def __call__(self, text: str) -> List[Token]:
        results = []
        for token in _tokenizer.tokenize(text):
            if not token[0].strip():
                continue
            results.append(Token(
                text=token[0],
                span=token[2],
                entity=token[1],
                metadata={
                    "name": get_symbol_name(token[0]),
                }
            ))
        return results


def get_symbol_name(char: str):
    name = _PUNCT_TO_NAME.get(char)
    return name


_PUNCT_TO_NAME = {
    ".": "full_stop",
    ",": "comma",
    "?": "question_mark",
    "!": "exclamation_mark",
    "'": "apostrophe",
    "(": "open_curly_bracket",
    ")": "closed_curly_bracket",
    "[": "open_square_bracket",
    "]": "closed_square_bracket",
    "{": "open_bracket",
    "}": "closed_bracket",
    "/": ["forward_slash", "divide"],
    "\\": "back_slash",
    "@": "at",
    "#": "hash_tag",
    "+": "plus",
    "×": "times",
    "÷": "division",
    "&": "ampersand",
    "_": "underscore",
    ":": "colon",
    ";": "semi_colon",
    "π": "pi",
    "-": ["minus", "hyphen"],
    "*": ["star", "times"],
    "√": "square_root",
    "%": "percent",
}
