from functools import wraps


_CACHE = {}


def single_cache():
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            key = id(fn)
            try:
                return _CACHE[key]
            except KeyError:
                pass
            _CACHE[key] = value = fn(*args, **kwargs)
            return value
        return inner
    return wrapper
