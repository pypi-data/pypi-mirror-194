from typing import Callable

from sqlalchemy.orm import Query


def add_filter(name: str, cast: Callable[[any], any] = lambda v: v):
    def _decorator(method: Callable[[Query, any], Query]):
        method.filter_name = name
        method.filter_cast = cast

        return method

    return _decorator


class FilterBase(object):
    def __init__(self) -> None:
        self._filters = None

    def _init_filter(self):
        if not self._filters:
            self._filters = {}

            for method_name in dir(self):
                method = getattr(self, method_name)
                name = getattr(method, "filter_name", None)
                cast = getattr(method, "filter_cast", None)

                if callable(method) and name and cast:
                    self._filters[name] = {"method": method, "cast": cast}

    def apply(self, query: Query, params: dict[str, any]) -> Query:
        self._init_filter()

        for param, value in params.items():
            filter_config: dict[str, any] = self._filters.get(param, None)
            if filter_config:
                method: Callable[[Query, any], Query] = filter_config.get("method", None)
                cast: Callable[[any], any] = filter_config.get("cast", None)

                query = method(query, cast(value)) if method and cast else query

        return query
