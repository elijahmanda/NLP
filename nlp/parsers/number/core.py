from __future__ import annotations
import regex as re
from .ejtoken import tokenize
from .normalize import (
    Pipe,
    recover_real_indices_and_match,
    normalize_and,
)

from .utils import text_span_replace, count_spaces, HashableDict
from .words2num import _words2num
from .constants import (
    FIRST_EXTRACTION_REGEXES,
    LAST_EXTRACTION_REGEXES,
    FLAGS,
    _REPLACEMENT,
)
from .logic import Logic
from .classes import NumberInfo


def get_idxs_from_bool(bool_container: Tuple[bool]) -> List[List[int]]:
    built_idxs = []
    for i, truth in enumerate(bool_container):
        if not truth:
            built_idxs.append(i)
    return built_idxs


def get_numbers_from_idxs(numbers: Tuple[Union[int, str]], idxs: Tuple[int]) -> List[List[int]]:
    prev_idx = 0
    nums = []
    for end in idxs:
        nums.append(numbers[prev_idx:end+1])
        prev_idx = end + 1
    return nums


def check_and_point(numbers, data):
    logic = Logic(numbers, data)
    return logic.apply_sequence_logic()


def first_extraction(text, data):
    """ extract direct numbers like:
            -6.7 4'444 1e-35 23.8k' """
    rreturn = []
    regexes = getattr(data, FIRST_EXTRACTION_REGEXES, [])
    text = replace(text, regexes, rreturn, data=data)
    return (text,  # we pass the text to the next Pipeline
            rreturn)


def replace(text, regexes, rreturn, data):
    for i, regex in enumerate(regexes):
        try:
            matches = regex.finditer(text)
        except Exception as e:
            raise e
        if matches:
            for match in matches:
                if match.group():
                    lc, rc = count_spaces(match.group())
                    start, end = (
                        match.span()[0] + lc,
                        match.span()[1] - rc
                    )
                    rreturn.append(
                        (
                            match.group().strip(),
                            (start, end)
                        ))
                    # we replace the found number with `$` to avoid the next Pipeline extracting the same number again
                    text = text_span_replace(
                        text, _REPLACEMENT * (end - start), (start, end))
    return text


def parse(text, data):

    # extract numbers 1
    remaining_words, matches = first_extraction(text, data)
    cleaned = Pipe(data)(remaining_words)
    tokens = tokenize(cleaned)
    bools = check_and_point(tokens, data)
    end_idxs = get_idxs_from_bool(bools)
    nums = get_numbers_from_idxs(tokens, end_idxs)
    nums = normalize_and(nums, data=data)
    # get real indices
    real, text_repl = recover_real_indices_and_match(
        remaining_words, nums, data)
    real.extend(matches)
    # extract remaining numbers 3
    text_repl = replace(text_repl, data.LAST_EXTRACTION_REGEXES, real, data)
    rt_final = []
    spans = set()
    for n in real:
        num_string = n[0]
        span = n[1]
        tokens = tokenize(num_string)
        try:
            tokens = n[2]
        except IndexError:
            pass

        info = generate_info(num_string, tokens, span, data)
        info["text"] = num_string
        if info.get("value") is None or span[1] in spans:
            continue
        spans.add(span[1])
        rt_final.append(info)
    rt_final.sort(key=lambda x: x["span"])
    return rt_final


def generate_info(num_string, tokens, span, data, value=None):
    if value is None:
        value = _words2num(tokens, data)
    d = HashableDict()
    info_generator = NumberInfo(num_string, tokens, value, data)
    info = info_generator.generate()
    d.update(info)
    d["span"] = span
    d["value"] = value
    return d
