from typing import (
    Any,
    Dict,
)

from nlp.tokens import Token
from nlp.constants import ENTITY, NUMBER, CUSTOM
from nlp.rules.validation import VALIDATION, register_validator


def number(token: Token, rule: Dict[str, Any]) -> bool:
    entity = token.metadata.get(ENTITY)
    if entity != NUMBER:
        return False
    custom = token.metadata.get(CUSTOM)
    validation = rule.get(VALIDATION)
    if validation is None:
        return False
    valid = {True}
    number_types = validation.get("type")
    if number_types:
        number_types = {number_types} if isinstance(
            number_types, str) else set(number_types)
        if custom["number_type"] not in number_types:
            valid.add(False)

    value = custom["value"]
    min = validation.get("min")
    if min is not None and value < float(min):
        valid.add(False)
    max = validation.get("max")
    if max is not None and value > float(max):
        valid.add(False)
    return all(valid)


def register():
    register_validator(NUMBER, number)
