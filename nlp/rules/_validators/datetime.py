from typing import (
    Any,
    Dict,
)

from nlp.tokens import Token
from nlp.constants import (
    DATETIME,
    CUSTOM,
)
from nlp.rules.validation import (
    VALIDATION,
    IN,
    NOT_IN,
    register_validator,
)


from nlp.parsers.datetimes.constants import TAG
from nlp.parsers.datetimes.vocab import Word, all_in


def _validate_word(token_word: Word, rule_word: Dict[str, Any]) -> bool:
    valid = {True}
    if rule_word.get("word") and rule_word["word"] != token_word.word:
        valid.add(False)
    if rule_word.get(TAG) and rule_word[TAG] != token_word.tag:
        valid.add(False)
    if rule_word.get("category") and rule_word["category"] != token_word.category:
        valid.add(False)
    if rule_word.get("features") and not all_in(rule_word["features"], token_word.features):
        valid.add(False)
    return all(valid)


def _validate_words(token: Token, rule_words: Dict[str, Any]) -> bool:
    if in_ := rule_words.get("in"):
        if token.text.lower() not in in_:
            return False
    if not_in := rule_words.get("not_in"):
        if token.text.lower() in not_in:
            return False
    return True


"""
validation:
    metadata:
        custom:
            word:
                word: the
                tag: article
                category: article
validation:
    metadata:
        custom:
            word:
                category: modifier
            words:
                in:
                    - past
                    - next
                    - following
                    - upcoming
                    - up coming
                    - last
"""


def datetime(token: Token, rule: Dict[str, Any]) -> bool:
    token_data = token.metadata.get(CUSTOM, {})
    try:
        data = rule[VALIDATION]
    except KeyError:
        return False
    valid = set()
    if tag := data.get("tag"):
        if tag == token_data.get("tag"):
            valid.add(True)
    if words := data.get("words"):
        if wordz := words.get(IN):
            if token.text.lower() in wordz:
                valid.add(True)
        elif wordz := words.get(NOT_IN):
            if token.text.lower() not in wordz:
                valid.add(True)
    if word := data.get("word"):
        if isinstance(word, str) and word == token.text.lower():
            valid.add(True)
        elif isinstance(word, dict):
            if word.get("tag") and token_data.get("word"):
                if token_data["word"].tag == word["tag"]:
                    valid.add(True)

            if word.get("category") and token_data.get("word") and (word["category"] == token_data["word"].category):
                valid.add(True)
            if word.get("features") and token_data.get("features") and set(word["features"]).issubset(set(token_data["word"].features)):
                valid.add(True)

    valid = any(valid)
    if valid:
        ...  # logger.debug("Token: {}\nRule: {}", token, rule)
    return valid


def register():
    register_validator(DATETIME, datetime)
