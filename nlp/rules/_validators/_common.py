from typing import (
    Any,
    Iterable,
)


def in_(value: Any, contaientity: Iterable[Any]) -> bool:
    return value in contaientity


def not_in(value: Any, contaientity: Iterable[Any]) -> bool:
    return not in_(value, contaientity)
