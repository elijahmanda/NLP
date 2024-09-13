from __future__ import annotations

import regex as re
from functools import lru_cache

from .ejtoken import tokenize as _tokenize
from .utils import text_span_replace
from .constants import _REPLACEMENT


def _filter(tokens, unwanted, sides=(True, True)):
    sides = list(sides)
    for i, n in enumerate(tokens):
        if not isinstance(unwanted, tuple):
            if str(n)[0].isalpha() and str(n).lower() not in unwanted.ALL_VALID:
                tokens.pop(i)
            continue
        if sides[0]:
            if str(n).lower() in unwanted:
                tokens.pop(i)
                continue
            else:
                sides[0] = False
        if sides[1]:
            if str(tokens[-(i+1)]).lower() in unwanted:
                tokens.pop(-(i+1))
            else:
                sides[1] = False


def _normalize_and_inner(numbers: List[List[str]], data: Data) -> bool:
    for i, n in enumerate(numbers):
        _filter(n, ("and", "a"))
        _filter(n, data)
        if len(n) > 1:
            first = n[0]
            last = n[len(n)-1]
            second_last = n[len(n)-2]
            if (last in data.ANDS + data.POINTS + data.NEGATIVES):
                numbers.insert(i+1, [n[len(n)-1]])
                n.pop()
            elif (second_last in data.ANDS and last in data.ZEROS):
                numbers.insert(i+1, [n[len(n)-2]])
                numbers.insert(i+2, [n[len(n)-1]])
                n.pop(len(n)-2)
                n.pop()
            elif first in [*data.ANDS, *data.A]:
                numbers.insert(i, [n[0]])
                n.pop(0)


def normalize_and(numbers: List[List[str]], data: Data):
    _normalize_and_inner(numbers, data)
    final = []
    for n in numbers:
        n_len = len(n)
        if n_len and (n_len > 1 or check_valid(n[0], data)):
            final.append(n)
    return final


def check_valid(text: str, data: Data) -> bool:
    regex_pipes = [
        data.ORDINAL_NUMERAL_REGEX,
        data.NUMBER_FOLLOWED_BY_SUFFIX_REGEX,
        data.SUFFIX_NAME_REGEX,
        data.HEX_REGEX,
        data.OCT_REGEX,
        data.BINARY_REGEX,
        data.ANY_NUMBER_REGEX,
    ]
    for pattern in regex_pipes:
        match = pattern.match(text)
        if match and match.group() == text:
            return True
    text = text.lower()
    valid = text in data.ALL_NUMS or text in data.INFORMAL_ALL
    return valid


def recover_real_indices_and_match(
    text: str,
    nums: List[List[str]],
    data: Data,
) -> Tuple[List[Tuple[str, Tuple[int, int]]], str]:
    last_start = 0
    real = []
    for n in nums:
        pattern = " ".join([re.escape(num)
                           for num in n]).replace(" ", r"\s*[,\-]?\s*")
        m = re.search(fr"\b{pattern}", text[last_start:])
        if m and m.group():
            start, end = m.span()
            start, end = start + last_start, end + last_start
            real.append((m.group(), (start, end), n))
            last_start = m.span()[0]
            text = text_span_replace(
                text,
                _REPLACEMENT * (end - start), (start, end),
            )
    return real, text


def _detokenize(tokens) -> str:
    return " ".join(tokens)


def _normalize_hyphen(text: str, data: Data) -> str:
    """
    Normalize numbers such as: "twenty-five" to "twenty five", "seventy-nine" to "seventy nine" not 
    "re-enroll", "up-front", "made-up"
    """
    rtokens = []
    tokens = _tokenize(text)
    for n in tokens:
        if data.HYPHEN.match(n):
            t1, t2 = n.split("-")
            rtokens.extend([t1, t2])
        else:
            rtokens.append(n)
    return _detokenize(rtokens)


def _rep_commas(text: str, data: Data) -> str:
    multiples = [
        m for m in data.MULTIPLES
        if isinstance(m, str)
        and m not in data.ORDINAL_MULTIPLES
    ]
    multiples = [m for m in multiples if (
        m not in data.SUFFIXES_BY_NAME or m != "hundred")]
    multiples = "|".join(multiples)
    # orig_text = text
    # Can only have a comma after a
    # multiple of 1000
    text = re.sub(
        fr"({multiples})\s?,",
        r"\1",
        text,
        re.VERBOSE | re.I | re.M,
    )
    return text


def _normalize(text: str, data: Data) -> str:
    suffixes = "|".join(data.SUFFIXES)
    suffixes = "(?:" + suffixes + ")"
    # `two    hundred` -> `two SPACE hundred`
    text = re.sub(r"\s{4,}", " SPACE ", text)
    text = re.sub(r",\s*,", " COMMA ", text)

    # `, ,` -> ` COMMA `

    # replace commas
    # 5,000 -> 5000 at numbers
    # million, -> thousand at
    # multiples of 1000
    # not => two, -> two
    text = _rep_commas(text, data)
    # normalize where numbers may express a possible range eg 2-3; this may be 2 minus 3, or 2 to 3 to avoid false negatives we remove the hyphen
    # normalize hyphen concatenated written numbers
    # twenty-one -> twenty one
    text = _normalize_hyphen(text, data)
    # two-two -> two two

    text = re.sub(r"(\D)\-(\D)", r"\1 \2", text)
    # 5-7 -> 5 7
    # these could mean 5 to 7 or
    # 5 minus 7
    # so we avoid interpreting
    # this as a negative
    text = re.sub(r"(\d)\-(\d)", r"\1 - \2", text)
    # `3.^w` -> `3  .  SPACE `
    text = re.sub(r"\.(\s+)", r"  .  SPACE ", text)
    # `thousand.` -> `thousand .`
    text = re.sub(r"\.(\D)", r" .  \1", text)
    # ` h7` -> ` h 5`
    if not data.config.bounded_numbers:
        text = re.sub(r"(?<=(\s))([^\-\+\.\d])(\d)", r"\1  \2   \3", text)
    # possible range
    text = re.sub(r"(\d)\-(\d)", "\1  -   \2", text)
    # 5^10 -> 5 ^ 10
    # 5'272' -> 5'272 '
    text = re.sub(r"([`',\.])(\D)", r" \1\2", text)
    text = re.sub(r"(\d)([',])(\d{4,})", r" \1 \2 \3", text)
    text = re.sub(r"(?<!\d[eE])([-+])", r" SPACE  \1", text)
    text = re.sub(fr"\d(^[eE',\d]|{suffixes})(?=>[\W\b])", r" SPACE \1", text)
    text = re.sub(r"([\-\+])([a-df-zA-DF-Z])", r"\1 \2", text)
    return text


class Pipe:

    def __init__(self, data: Data):
        self.data = data

    def normalize(self, text: str) -> str:
        text = _normalize(text, self.data)
        text = _detokenize(text.split())
        return text.strip()

    def __call__(self, text: str) -> str:
        return self.normalize(text)
