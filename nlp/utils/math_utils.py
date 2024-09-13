from typing import (
    Union,
    Callable,
    Optional,
)


def clip_int(value: Optional[Union[Callable[[...], Union[int, float]], int, float]] = None, /, gt: float = 1e12):
    """
    Return an int version of a value if the
    decimal part of the value equal to
    zero and the value exceeds gt.

    Args:
        gt: A max value to consider when trimming the value.
    Usage:
        >>> import operator as op

        >>> @clip_int(gt=0.1e11)
        >>> def mult(a, b):
        >>>     return a * b
        >>>
        >>> print(3e7 * 4.0)
        120000000.0
        >>> print(mult(3e7, 4.0))
        120000000
        >>> print(clip_int(op.mul, gt=0.1e11)(3e7, 4.0))
        120000000
        >>> print(clip_int(3e7 * 4.0, gt=0.1e11))
        120000000
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            nonlocal value, gt
            if callable(value or func):
                value = func(*args, **kwargs)
            if value is float("nan"):
                return value
            if not hasattr(value, "__float__"):
                return value
            if value > gt:
                return value
            try:
                return int(float(value)) if int(float(value)) == value and "e" not in str(float(value)) else value
            except ValueError:
                return value
        return inner
    if value is None:
        return wrapper
    elif not callable(value):
        return wrapper(value)()
    return wrapper(value)


@clip_int(gt=0.1e11)
def mult(a, b):
    return a * b

# print(3e7 * 4.0)
# print(mult(3e7, 4.0))
# print(clip_int(3e7 * 4.0, gt=0.1e11))
# print(clip_int(lambda x, y: x * y, gt=0.1e11)(3e7, 4.0))
