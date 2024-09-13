from __future__ import annotations

import json
import difflib
from functools import lru_cache
import typing as t

from nltk.corpus import words
from nlp.data import DATA_PATH
from nlp.utils.strings import CaseLessString


class _Dictionary:

    def __init__(self):
        self.dict = json.load((DATA_PATH / "english_dictionary.json").open())
        self.all_words = set(w.split()[0] for w in self.dict.keys())
        self.all_words |= set(words.words())

    def get_close(self, key: str, n=3, cutoff=0.6) -> t.Dict:
        key = CaseLessString(key)
        matches = difflib.get_close_matches(
            key, self.dict.keys(), n=n, cutoff=cutoff)
        return {k: self.dict[k] for k in matches}

    @lru_cache()
    def get(self, key: str) -> str | None:
        matches = self.get_close(key, n=1, cutoff=1.0)
        if matches:
            return list(matches.values())[0]

    @lru_cache()
    def is_word(self, key: str) -> bool:
        key = CaseLessString(key)
        return key in self.all_words

    def __contains__(self, key: str) -> bool:
        return bool(self.get(key))


Dictionary = _Dictionary()
