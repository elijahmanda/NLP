from __future__ import annotations

import re
import operator
from typing import (
    Union,
    List,
    Tuple,
    TYPE_CHECKING
)

from nlp.parsers.number.normalize import Pipe
from nlp.parsers.number.utils import pair
from nlp.utils.strings import CaseLessString
from nlp.parsers.number.ejtoken import tokenize

if TYPE_CHECKING:
    from .data import Data


Number = (int, float)
NumberT = Union[int, float, str]


def _clean(string, lower=False):
    if not isinstance(string, str):
        return string
    string = re.sub(r"[\,'_]", "", string)
    if lower:
        string = string.lower()
    return string


def _be_string(fn):
    def wrapper(n):
        if not isinstance(n, str):
            return n
        return fn(n)
    return wrapper


def convert_to_number(tokens: List[NumberT],  data) -> List[NumberT]:
    bases = {
        "b": 2,
        "o": 8,
        "x": 16
    }

    @_be_string
    def _inner_conv(n):
        cleaned = _clean(n, lower=True)
        base = 10
        try:
            base = bases.get(cleaned[1], 10)
        except IndexError:
            pass
        try:
            return int(cleaned, base)
        except Exception:
            try:
                return float(cleaned)
            except Exception:
                try:
                    return complex(eval(cleaned.replace("i", "j")))
                except Exception:
                    pass
        return n
    for i, token in enumerate(tokens):
        tokens[i] = _inner_conv(token)
    return tokens


def _word_to_number(tokens: List[NumberT], data) -> List[NumberT]:
    all_n = {}
    all_n.update(data.ALL_NUMS)
    all_n.update(data.INFORMAL_ALL)

    @_be_string
    def _inner_conv(word):
        val = all_n.get(_clean(word, lower=True))
        if val is not None:
            return val
        return word
    for i, token in enumerate(tokens):
        tokens[i] = _inner_conv(token)


def convert_suffixes(tokens, data):
    pattern = data.NUMBER_FOLLOWED_BY_SUFFIX_REGEX

    @_be_string
    def _inner_conv(n):
        if not n[-1].isalpha():
            return n
        if match := pattern.search(n):
            if match.group() != n:
                return n
            num = match.groupdict()["number"]
            suffix = match.groupdict()["suffix"]
            num = convert_to_number([_clean(num)], data)[0]
            multiplier = data.get_suffix_value(suffix)
            if multiplier is None:
                return n
            n = num * multiplier
        return n
    for i, token in enumerate(tokens):
        tokens[i] = _inner_conv(token)


def convert_ordinals(tokens, data):
    pattern = data.ORDINAL_NUMERAL_REGEX

    @_be_string
    def _inner_conv(n):
        if match := pattern.match(_clean(n)):
            num = match.groupdict()["number"]
            ordinal = match.groupdict()["ordinal"]
            if ordinal.lower() in data.ORDINAL_SUFFIXES:
                n = convert_to_number([num], data=data)[0]
            else:
                n = convert_to_number([num], data=data)[
                    0] * data.ORDINALS[ordinal.lower()]
        return n
    for i, token in enumerate(tokens):
        tokens[i] = _inner_conv(token)


def convert_supersubscript(tokens, data):

    @_be_string
    def _inner_conv(n):
        first = n[0]
        if first in data.SUPERSCRIPT_ONES:
            num = ""
            for c in n:
                num += str(data.SUPERSCRIPT_ONES[c])
            n = int(num)
        elif first in data.SUBSCRIPT_ONES:
            num = ""
            for c in n:
                num += str(data.SUBSCRIPT_ONES[c])
            n = int(num)
        elif n in data.SUPERSCRIPT_FRACTIONS:
            n = data.SUPERSCRIPT_FRACTIONS[n]
        return n
    for i, token in enumerate(tokens):
        tokens[i] = _inner_conv(token)


class _ConversionPipe:
    def __init__(self, data):
        self.data = data

    def __call__(self, tokens: List[NumberT]) -> List[NumberT]:
        convert_to_number(tokens, self.data)
        convert_ordinals(tokens, self.data)
        convert_suffixes(tokens, self.data)
        convert_supersubscript(tokens, self.data)
        _word_to_number(tokens, self.data)
        return tokens


def pair_tokens(tokens: List[int]) -> List[List[int, ...]]:
    build = []
    final = []
    for token in tokens:
        if token <= 100:
            build.append(token)
        else:
            final.append(build)
            build = []
            final.append([token])
    final.append(build)
    return final


def sum_nums(tokens: List[List[float]]) -> List[float]:
    total = []
    hundred = 0
    for token in tokens:
        if len(token) == 1 and not token[0] % 1000:
            total.append(token[0])
        else:
            hundred = 0
            for j, n in enumerate(token):
                if j == 0:
                    hundred += n
                    continue
                if n == 100:
                    hundred *= 100
                    continue
                else:
                    hundred += n
            total.append(hundred)
    return total


def find_total(tokens: List[Tuple[int, int]]):
    total = 0
    for n in tokens:
        num, multiplier = n
        if not num:
            total += multiplier
        elif not multiplier:
            total += num
        else:
            total += num * multiplier
    return total


def _ensure_iterable(obj):
    if hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [str(i) for i in obj]
    return [str(obj),]


def try_power(n: List[str], data):
    neg = 1
    if len(n) == 3:
        if n[0] not in data.NEGATIVES:
            return
        n.pop(0)
        neg = -1
    num, mult = _ConversionPipe(data)(n)
    if not isinstance(num, Number) or not isinstance(mult, Number):
        return
    op = operator.mul
    if num > mult and not str(n[1]).lower() in data.INFORMAL_ALL:
        op = operator.add
    value = None
    value = op(neg * num, mult)
    return value


def point_num(tokens):
    last = 1.0
    if tokens[-1] > 9:
        last = tokens.pop()
    point_index = tokens.index("point")
    whole = tokens[:point_index]
    dec = tokens[point_index+1:]
    whole = filter(lambda x: x != "and", whole)
    paired = pair_tokens(whole)
    summed = sum_nums(paired)
    new_tokens = []
    for token in summed:
        if isinstance(token, (list, tuple)):
            new_tokens.append(token[0])
        else:
            new_tokens.append(token)
    paired = pair(new_tokens, holder=0)
    whole = find_total(paired)
    dec = "".join(map(str, dec))
    dec = float("0." + dec)
    return (whole + dec) * last


def filter_tokens(tokens, unwanted: str, leave_last: bool = False, inplace: bool = False):
    tokens = tokens if inplace else list(tokens)
    i = -1
    if leave_last and tokens.count(CaseLessString(unwanted)) < 3:
        return tokens
    seen = False
    while True:
        try:
            x = tokens[i]
            if isinstance(x, str) and x.lower() == unwanted.lower():
                if leave_last:
                    if seen:
                        tokens.pop(i)
                    else:
                        seen = True
                else:
                    tokens.pop(i)
            i -= 1
        except IndexError:
            break
    if not inplace:
        return tokens


def _words2num(tokens: List[NumberT], data):
    filter_tokens(tokens, "a", inplace=True)
    if len(tokens) == 1:
        number = tokens[0]
        num = _ConversionPipe(data)(tokens)
        if isinstance(num[0], (int, float, complex)):
            return num[0]

    filter_tokens(tokens, "and", leave_last=True, inplace=True)
    tokens = [_clean(token, lower=True) for token in tokens if token]
    og_tokens = tokens.copy()
    if 1 < len(tokens) <= 3:
        value = try_power(tokens, data=data)
        if isinstance(value, Number):
            return value
    string_tokens = tokens.copy()
    _ConversionPipe(data)(tokens)
    if "point" in tokens:
        value = point_num(tokens)
        if isinstance(value, Number):
            return value
    if len(tokens) == 2 and all(isinstance(n, Number) for n in tokens):
        first = "".join(string_tokens[0].split())
        if len(first) == 5 and first[1] == ",":
            tokens[0] /= 1000.0
        op = operator.mul
        if tokens[0] > tokens[1]:
            op = operator.add
        return op(*tokens)
    tokens = og_tokens.copy()
    _ConversionPipe(data)(tokens)
    if not len(tokens):
        return
    if tokens[-1] == ".":
        tokens.pop()
    points = None
    negative = 1
    if tokens[0] in data.NEGATIVES:
        tokens.pop(0)
        negative = -1
    operation = None
    fraction = 0
    if len(tokens) >= 2:
        if isinstance(tokens[-1], float) and tokens[-1] < 1:
            if tokens[-2] == "and":
                operation = operator.add
                fraction = tokens.pop()
            elif isinstance(tokens[-2], Number):
                operation = operator.mul
    if operation is operator.mul:
        fraction = tokens.pop()
    filter_tokens(tokens, "and", inplace=True)
    if "point" in tokens:
        point_idx = tokens.index("point")
        points = "0." + "".join(_ensure_iterable(tokens[(point_idx + 1):]))
        tokens = tokens[:point_idx]
    try:
        paired = pair_tokens(tokens)
    except TypeError:
        return

    summed = sum_nums(paired)
    new_tokens = []
    for token in summed:
        if isinstance(token, list):
            new_tokens.append(token[0])
        else:
            new_tokens.append(token)
    paired = pair(new_tokens, holder=0)
    total = find_total(paired)
    if points:
        total += float(points)
    if operation is not None:
        total = operation(total, fraction)
    return negative * total
