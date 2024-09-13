import re
from typing import List

from nlp.entity import EntityParser
from nlp.tokens import Token
from nlp.constants import (
    EMAIL,
    ENTITY,
    CUSTOM,
)


# taken hostname, domainname, tld from URL regex below
EMAIL_REGEX = re.compile(
    r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-](@|[(<{\[]at[)>}\]])(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))\b",
    flags=re.IGNORECASE | re.UNICODE,
)


class EmailParser(EntityParser):

    def __call__(self, text: str) -> List[Token]:
        results = []
        parse_res = self._parse(text)
        for res in parse_res:
            results.append(Token(
                text=res["text"],
                span=res["span"],
                entity=EMAIL,
                metadata=res["metadata"],
            ))
        return results

    def _parse(self, text: str):
        res = []
        for m in EMAIL_REGEX.finditer(text):
            match = m.group()
            span = m.span()
            username, provider = match.split("@")
            res.append(
                dict(
                    text=match,
                    span=span,
                    metadata=dict(
                        username=username,
                        provider=provider,
                    ),
                )
            )
        return res


def get_parser() -> EmailParser:
    return EmailParser
