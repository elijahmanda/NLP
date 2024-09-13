import re
from typing import List

from nlp.constants import CURRENCY
from nlp.parsers import load_parser
from nlp.entity import (
    RegexEntityParser,
    ExtractionPipeline
)
from nlp.tokens import Token
from nlp.utils.regex import (
    bound,
    join,
    preprocess_names_to_patterns,
    B_LEFT_NO_LETTER,
    B_RIGHT_NO_LETTER,
)
from nlp.utils.sequences import flatten_sequences
from nlp.constants import CURRENCY
from nlp.parsers.currency.db import CurrencyDB
from nlp.parsers.currency import constants as C


CURRENCY_SYMBOL_REGEX = bound(
    join(map(
        re.escape,
        CurrencyDB.all_entries(C.SYMBOL)
    )),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

CURRENCY_SYMBOL_NATIVE_REGEX = bound(
    join(map(
        re.escape,
        CurrencyDB.all_entries(C.SYMBOL_NATIVE)
    )),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

CURRENCY_NAME_REGEX = bound(
    join(
        preprocess_names_to_patterns(
            CurrencyDB.all_entries(C.NAME)
        )
    ),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

CURRENCY_MAJOR_SINGLE_REGEX = bound(
    join(
        preprocess_names_to_patterns(
            CurrencyDB.all_entries(C.MAJOR_SINGLE)
        )
    ),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

CURRENCY_MAJOR_PLURAL_REGEX = bound(
    join(
        preprocess_names_to_patterns(
            CurrencyDB.all_entries(C.MAJOR_PLURAL)
        )
    ),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

CURRENCY_MINOR_SINGLE_REGEX = bound(
    join(
        preprocess_names_to_patterns(
            CurrencyDB.all_entries(C.MINOR_SINGLE)
        )
    ),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

CURRENCY_MINOR_PLURAL_REGEX = bound(
    join(
        preprocess_names_to_patterns(
            CurrencyDB.all_entries(C.MINOR_PLURAL)
        )
    ),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

CURRENCY_ALIAS_MAJOR_SINGLE_REGEX = bound(
    join(
        preprocess_names_to_patterns(
            flatten_sequences(CurrencyDB.all_entries(C.MAJOR_SINGLE, alias=True)
                              ))
    ),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

CURRENCY_ALIAS_MAJOR_PLURAL_REGEX = bound(
    join(
        preprocess_names_to_patterns(
            flatten_sequences(CurrencyDB.all_entries(C.MAJOR_PLURAL, alias=True)
                              ))
    ),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

CURRENCY_ALIAS_MINOR_SINGLE_REGEX = bound(
    join(
        preprocess_names_to_patterns(
            flatten_sequences(CurrencyDB.all_entries(C.MINOR_SINGLE, alias=True)
                              ))
    ),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

CURRENCY_ALIAS_MINOR_PLURAL_REGEX = bound(
    join(
        preprocess_names_to_patterns(
            flatten_sequences(CurrencyDB.all_entries(C.MINOR_PLURAL, alias=True)
                              ))
    ),
    sides=[B_LEFT_NO_LETTER, B_RIGHT_NO_LETTER]
)

PATTERNS = [
    # Symbols
    (CURRENCY_SYMBOL_REGEX, CURRENCY + "-" + C.SYMBOL),
    (CURRENCY_SYMBOL_NATIVE_REGEX, CURRENCY + "-" + C.SYMBOL_NATIVE),
    # Name. eg: Zambian kwacha
    (CURRENCY_NAME_REGEX, CURRENCY + "-" + C.NAME),
    # Major
    (CURRENCY_MAJOR_PLURAL_REGEX, CURRENCY + "-" + C.MAJOR_PLURAL),
    (CURRENCY_MAJOR_SINGLE_REGEX, CURRENCY + "-" + C.MAJOR_SINGLE),
    # Minor
    (CURRENCY_MINOR_PLURAL_REGEX, CURRENCY + "-" + C.MINOR_PLURAL),
    (CURRENCY_MINOR_SINGLE_REGEX, CURRENCY + "-" + C.MINOR_SINGLE),
    # Alias Plural
    (CURRENCY_ALIAS_MAJOR_PLURAL_REGEX, CURRENCY + "-" + C.MAJOR_PLURAL + "-alias"),
    (CURRENCY_ALIAS_MINOR_PLURAL_REGEX, CURRENCY + "-" + C.MINOR_PLURAL + "-alias"),
    # Alias Single
    (CURRENCY_ALIAS_MAJOR_SINGLE_REGEX, CURRENCY + "-" + C.MAJOR_SINGLE + "-alias"),
    (CURRENCY_ALIAS_MINOR_SINGLE_REGEX, CURRENCY + "-" + C.MINOR_SINGLE + "-alias")
]

PATTERNS.extend(
    zip(
        ["OTHER-CURRENCIES"]
        * len(C.OTHER_CURRENCIES),
        map(re.escape, C.OTHER_CURRENCIES),
    )
)

PATTERNS = filter(
    lambda p: p[0] not in (
        bound(join([])),
        bound(
            join([]),
            sides=[
                B_LEFT_NO_LETTER,
                B_RIGHT_NO_LETTER,
            ]
        )
    ),
    PATTERNS,
)
PATTERNS = [(name.upper(), pattern) for (pattern, name) in PATTERNS]


class CurrencyTokenizer:

    def __init__(self):
        self._parser = RegexEntityParser(PATTERNS)

    @property
    def parser(self) -> RegexEntityParser:
        return self._parser

    def tokenize(self, text: str):
        tokens = self._parser(text)
        self._merge_demonym(tokens)
        self._norm_entities(tokens)
        return tokens

    def _merge_demonym(self, tokens):
        pass

    def _norm_entities(self, tokens: List[Token]) -> None:
        for token in tokens:
            token.metadata["fine_grained_entity"] = token.entity
            token.entity = CURRENCY


if __name__ == "__main__":
    tokenizer = CurrencyTokenizer()
    while True:
        test_text = input("> ").strip()
        if not test_text:
            continue
        for token in tokenizer.tokenize(test_text):
            print(token.dumps())
