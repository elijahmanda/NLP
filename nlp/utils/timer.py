from time import perf_counter
from functools import wraps
from humanize import naturaldelta
from inspect import getmodule

_DEFAULT_MSG = "Took {duration}"


def timer(msg=None):

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if msg:
                Timer.set_msg(msg)
            else:
                Timer.set_msg(
                    f"{func.__name__!r} in module: {getmodule(func)!r} executed in {{duration}}")
            Timer.start()
            res = func(*args, **kwargs)
            Timer.end()
            Timer.msg()
            Timer.reset()
            return res
        return inner
    return wrapper


class Timer:

    _start = 0
    _end = 0
    _msg = _DEFAULT_MSG

    @classmethod
    def reset(cls):
        cls.set_msg(_DEFAULT_MSG)

    @classmethod
    def set_msg(cls, msg: str):
        cls._msg = msg

    @classmethod
    def start(cls):
        cls._start = perf_counter()

    @classmethod
    def end(cls):
        cls._end = perf_counter()

    @classmethod
    def msg(cls):
        duration = cls._end - cls._start
        msg = cls._msg.format(duration=naturaldelta(
            duration, minimum_unit="microseconds"))
        print(msg)
