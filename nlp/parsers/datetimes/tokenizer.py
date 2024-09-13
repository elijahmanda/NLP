from typing import (
    List,
    Tuple,
)

from nlp.parsers import load_parser
from nlp.tokens import Token
from nlp.entity import (
    RegexEntityParser,
    ExtractionPipeline,
)
from nlp.parsers.number.config import Config as NumConfig
from nlp.utils.timer import timer

from nlp.parsers.datetimes import patterns as p


PATTERNS: List[Tuple[str, str]] = [
    *p.DATETIME_PATTERNS,
    *p.DATE_PATTERNS,
    *p.OTHER_DATE_PATTERNS,
    *p.TIME_PATTERNS,
    (p.MONTH_PATTERN, "month"),
    (p.MONTH_ALIAS_PATTERN, "month_alias"),
    (p.WEEKDAY_PATTERN, "weekday"),
    (p.WEEKDAY_ALIAS_PATTERN, "weekday_alias"),
    (p.TIMEUNITS_PLURAL_PATTERN, "time_unit_plural"),
    (p.TIMEUNITS_SINGULAR_PATTERN, "time_unit_singular"),
    (p.TIMEUNITS_ALIAS_PATTERN, "time_unit_alias"),
    (TIME_MODIFIER_WORD_PATTERN, "time_modifier_word"),
    (p.TIME_WORD_PATTERN, "time_word"),
    (p.OTHER_WORD_PATTERN, "other_word"),
    (p.TIME_PERIOD_PATTERN, "time_period"),
]


class Tokenizer:

    def __init__(self):
        self._token_extractor = None

    def _setup_extractor(self):
        self._token_extractor = ExtractionPipeline(
            [
                RegexEntityParser(PATTERNS),
                load_parser(
                    "number",
                    config=NumConfig(
                        signs_allowed=False,
                    )
                )
            ]
        )

    def tokenize(self, text: str) -> List[Token]:
        if self._token_extractor is None:
            self._setup_extractor()
        tokens: List[Token] = self._token_extractor.extract(text)
        return tokens


if __name__ == "__main__":
    tokenizer = Tokenizer()
    while True:
        test_text = input("> ").strip()
        if not test_text:
            continue
        for token in tokenizer.tokenize(test_text):
            print(token.dumps())
