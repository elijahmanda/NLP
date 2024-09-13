from typing import Optional, Union

from loguru import logger


def is_positive(number: Union[int, float]) -> bool:
    return number > 0


def assert_positive_int(number: int) -> None:
    assert isinstance(number, int) and is_positive(
        number), "must be a positive integer"


def is_valid_time(
    hour: int,
    minute: Optional[int] = None,
    second: Optional[int] = None,
    millisecond: Optional[int] = None,
    microsecond: Optional[int] = None,
    period: bool = False,
) -> Optional[bool]:
    logger.info("hour: {} minute: {} second: {} millisecond: {} microsecond: {}",
                hour, minute, second, millisecond, microsecond)
    for unit in (hour, minute, second, millisecond, microsecond):
        if unit is not None:
            assert_positive_int(unit)
    if period and (hour == 0) or (hour > 12):
        return False
    if hour > 24:
        return False
    if minute is not None:
        if minute > 59:
            return False
    if second is not None:
        if second > 59:
            return False
    if millisecond is not None:
        if millisecond > 999999:
            return False
    if microsecond is not None:
        if microsecond > 999999:
            return False
    return True


def func_or_none(func, value):
    return func(value) if value is not None else None
