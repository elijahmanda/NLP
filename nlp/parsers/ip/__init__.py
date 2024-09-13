import re
import ipaddress
from typing import List

from nlp.entity import EntityParser
from nlp.tokens import Token
from nlp.constants import (
    IPADDRESS,
    ENTITY,
    CUSTOM,
)

IPV4 = "ipv4"
IPV6 = "ipv6"


IPV4_PATTERN = r'\b(?P<ipv4>(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))\b'


IPV6_PATTERN = r'\b(?P<ipv6>(?!.*::.*::)(?:(?!:)|:(?=:))(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)){6}(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)[0-9a-f]{0,4}(?:(?<=::)|(?<!:)|(?<=:)(?<!::):)|(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))\b'

IP_PATTERN = IPV4_PATTERN + "|" + IPV6_PATTERN

IP_REGEX = re.compile(IP_PATTERN, re.IGNORECASE |
                      re.VERBOSE | re.DOTALL | re.UNICODE)


class IPAddressParser(EntityParser):

    def __call__(self, text: str) -> List[Token]:
        results = []
        parse_res = self._parse(text)
        for res in parse_res:
            results.append(Token(
                text=res["text"],
                span=res["span"],
                entity=IPADDRESS,
                metadata={
                    CUSTOM: {**res["metadata"]},
                },
            ))
        return results

    def _parse(self, text: str):
        res = []
        for m in IP_REGEX.finditer(text):
            span = m.span()
            group_dict = m.groupdict()
            ip_type = IPV4 if group_dict.get(IPV4) else IPV6
            match = group_dict[ip_type]
            try:
                ipaddress.ip_address(match)
            except ValueError:
                continue
            res.append(
                dict(
                    text=match,
                    span=span,
                    metadata=dict(
                        ip_type=ip_type,
                    ),
                )
            )
        return res


def get_parser() -> IPAddressParser:
    return IPAddressParser


parser = get_parser()()

text = "127.0.0.1 3 3.5.824 8.8.8.8:8080"

res = parser(text)

for rs in res:
    print(rs, end="\n\n")
