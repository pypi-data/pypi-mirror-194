from typing import Callable

from flask import Request, request


def is_authorized(validate_access: Callable[[Request], None]):
    def _decorator(method: Callable[[], any]):
        def _wrapper(*args, **kwargs) -> any:
            validate_access(request)
            return method(*args, **kwargs)

        _wrapper.__name__ = method.__name__
        return _wrapper

    return _decorator
