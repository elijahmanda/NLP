# cython: c_string_type=unicode, c_string_encoding=utf8

from typing import (
    List,
    Tuple,
    Optional,
    Union,
)
import re


# List of tuple[pattern, entity name]
PatternsT = List[Tuple[str, Union[str, "re.Pattern"]]]
DEFAULT_RE_FLAGS = re.I | re.VERBOSE | re.M
SPACE = " "


def text_span_replace(text, replacement, start, end):
    """ Replace text[span[0] : span[1]] with `replacement` """
    return (text[0: start] + replacement + text[end:])


def missing_indexes(indexes, total):
    if not len(indexes):
        return [(0, total)]
    missing = []
    i = next_start = 0
    last_index = 0
    if indexes[0][0] > 0:
        missing.append((0, indexes[0][0]))
    if indexes[last_index][1] < total:
        missing.append((indexes[last_index][1], total))
        last_index += 1
    for i, index in enumerate(indexes):
        if i < len(indexes) - 1:
            first_end = index[1]
            next_start = indexes[i + 1][0]
            if (next_start - first_end) > 0:
                missing.append((first_end, next_start))
    missing.sort(key=lambda x: x[0])
    return missing


def make_flags(flags_re):
    if not isinstance(flags_re, str):
        return flags_re
    flags = None
    if "(?i)" in flags_re:
        flags = re.I
    if "(?m)" in flags_re:
        if flags is not None:
            flags |= re.M
        else:
            flags = re.M
    if "(?x)" in flags_re:
        if flags is not None:
            flags |= re.VERBOSE
        else:
            flags = re.VERBOSE
    flags |= re.UNICODE | re.DOTALL
    return flags


class RegexTokenizer:

    def __init__(self, patterns: Optional[PatternsT] = None, flags=None):
        self._patterns = patterns or []
        self._compiled_patterns = []
        self._compiled = False
        if self._patterns:
            self.compile(flags=flags)

    def patterns(self) -> PatternsT:
        return self._patterns

    def compile(self, flags=None, sort=False):
        self._compile(flags, sort)

    def _compile(
        self,
        flags=None,
        sort=False
    ):
        if flags is None:
            flags = DEFAULT_RE_FLAGS
        else:
            flags = make_flags(flags)
        if sort:
            self._patterns.sort(key=lambda x: len(x[0]) if isinstance(
                x[0], str) else len(x[0].pattern), reverse=True)
        for entity, pattern in self._patterns:
            if isinstance(pattern,  re.Pattern):
                self._compiled_patterns.append((pattern, entity))
                continue
            self._compiled_patterns.append(
                (re.compile(pattern, flags), entity))
        if len(self._compiled_patterns) > 0:
            self._compiled = True

    def _merge_non_entity_tokens(self, text, tokens):
        self._sort(tokens)
        indexes = [n[2] for n in self._map_idx(tokens, 2)]
        missing = missing_indexes(indexes, len(text))
        for start, end in missing:
            tokens.append(
                (
                    text[start:end],  # text
                    None,  # entity
                    (start, end)  # span
                )
            )
        return tokens

    def _sort(self, tokens):
        tokens.sort(key=lambda x: x[2])

    def tokenize(self, text, merge=False):
        original_text = text
        if not self._compiled:
            self.compile()
        tokens = []
        for compiled_pattern, entity in self._compiled_patterns:
            for match in compiled_pattern.finditer(text):
                start, end = match.span()
                tokens.append((match.group(), entity, (start, end)))
                text = text_span_replace(text, " " * (end-start), start, end)
        if merge:
            tokens = self._merge_non_entity_tokens(original_text, tokens)
        self._sort(tokens)

        return tokens

    def _map_idx(self, container, index):
        return map(lambda x: x[index], container)

    def add_pattern(self, pattern: str, entity: str) -> None:
        assert not self._compiled
        self._patterns.append((pattern, entity))

    def clear_patterns(self) -> None:
        self._patterns.clear()
        self._compiled_patterns.clear()
        self._compiled = False

    def set_patterns(self, patterns: PatternsT, compile=True) -> None:
        assert not self._compiled
        self._patterns = patterns
        if compile:
            self.compile()

    def get_entities(self) -> List[str]:
        entities = list(set(self._map_idx(self._patterns, 0)))
        entities.sort()
        return entities

    def get_pattern_count(self) -> int:
        return len(self._patterns)

    def get_entity_count(self) -> int:
        return len(self.get_entities())


try:
    import fast_nlp
    FastRegexTokenizer = fast_nlp.tokenizers.FastRegexTokenizer
except Exception:
    pass
