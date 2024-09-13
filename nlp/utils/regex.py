import re
from typing import (
    Tuple,
    Optional,
)

from retrie.retrie import Whitelist


REPLACEMENTS = [
    (r"\*", ""),
    (r"\s*\(.+\)\s*", ""),
    (r"(.+)([\[].+[\]])", r"\1|\2"),
    (r"(.+)[;](.+)", r"\1|\2"),
    (r"(.+)[/](.+)", r"\1|\2"),
    (r"[\[\]]", ""),
]
SUBSTITUTIONS = [
    # Year's -> Year'?s?
    (r"[']s\b", r"[']?s?"),
    # New Year's Day -> New Year'? Day
    (r"['](?=[^\]])", r"[']?"),
    # Bla,Bla -> Bla[,]?Bla
    (",", ",?"),
    # Blaa. -> Bla[\.]?
    (r"([\-\.])", r"(?:[\\\g<0>]|\\s+)"),
    # (r"\s+", r"(?:\s+)?")
    # Add_To -> Add[_\s]*To
    ("([_]+)", r"[\\\g<0>]*")
]

B_LEFT = r"(?<![a-zA-Z\d'])"
B_RIGHT = r"(?![a-zA-Z\d])"
B_LEFT_NO_LETTER = r"(?<![a-zA-Z'])"
B_RIGHT_NO_LETTER = r"(?![a-zA-Z])"
B_LEFT_NO_DIGIT = r"(?<![\d])"
B_RIGHT_NO_DIGIT = r"(?![\d])"


def preprocess(sent):
    for regex, replacement in REPLACEMENTS:
        sent = re.sub(regex, replacement, sent, re.I | re.U | re.VERBOSE)
    return sent.lower()


def substitute(name):
    for regex, substitution in SUBSTITUTIONS:
        name = re.sub(regex, substitution, name, re.I | re.VERBOSE)
    return name


def preprocess_names_to_patterns(names):
    seen = set()
    for name in names:
        name = preprocess(name)
        name = name.strip()
        name = r"\s+".join(name.split())
        name = substitute(name)
        seen.add(name)

    seen = list(sorted(seen, key=len, reverse=True))
    return seen


def process_string_for_pattern(string):
    return preprocess_names_to_patterns([string])[0]


def bound(pattern: str, sides: Optional[Tuple[str, str]] = None) -> str:
    if not pattern:
        return pattern
    if sides is None:
        sides = B_LEFT, B_RIGHT
    else:
        assert len(sides) == 2
    pattern = "".join([sides[0], "(?:", pattern, ")", sides[1]])
    return pattern


def no_digits_bound(pattern):
    return bound(pattern, sides=[B_LEFT_NO_DIGIT, B_RIGHT_NO_DIGIT])


def all_cases(string: str) -> str:
    string = string.lower()
    result = ""
    for ch in string:
        if ch.isalpha():
            result += f"({ch}|{ch.upper()})"
        else:
            result += ch
    return result


def join(patterns, sep="|"):
    patterns = list(patterns)
    patterns = list(filter(str.strip, patterns))
    if not len(patterns):
        return ""
    patterns.sort(key=len, reverse=True)
    return "(?:" + sep.join(patterns) + ")"


def retrie(patterns):
    return Whitelist(patterns).pattern()


def group_strings(strings, reverse=True, escape=False, bounds=None):
    if escape:
        strings = [re.escape(string.strip()) for string in strings]
    grouped_regex = []
    strings_by_length = {}

    # Group strings by length
    for string in strings:
        length = len(string.lstrip("\\"))
        if length not in strings_by_length:
            strings_by_length[length] = []
        strings_by_length[length].append(string)

    # Create regex for single characters
    if 1 in strings_by_length:
        single_char_regex = "[" + "".join(strings_by_length[1]) + "]"
        grouped_regex.append(single_char_regex)

    # Create regex for strings of equal length
    for length, string_list in strings_by_length.items():
        if length == 1:
            continue
        if len(string_list) == 1:
            grouped_regex.append(string_list[0])
        else:
            regex_str = "(" + "|".join(string_list) + ")"
            grouped_regex.append(regex_str)

    def key(string):
        string = string.strip("(").strip(")")
        if string.startswith("[") and string.endswith("]"):
            return 1
        strings = string.split("|")
        return len(strings[0])

    if reverse:
        grouped_regex = sorted(grouped_regex, key=key, reverse=True)
    grouped_regex = "|".join(grouped_regex)
    left, right = (B_LEFT_NO_LETTER,
                   B_RIGHT_NO_LETTER) if bounds is None else bounds
    grouped_regex = f"{left}(?:{grouped_regex}){right}"
    return grouped_regex
