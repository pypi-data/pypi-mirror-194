from typing import Type

from flask import request
from pydantic import BaseModel
from sqlalchemy.orm import Query


class Page(object):
    def __init__(
        self, query: Query, serializer_class: Type[BaseModel], default_limit: int = 20, max_limit: int = 100
    ) -> None:
        self._query = query
        self._serializer_class = serializer_class
        self._default_limit = default_limit
        self._max_limit = max_limit

    def count(self) -> int:
        count = getattr(self, "__cache_count", None)

        if not count:
            count = self._query.count()

        setattr(self, "__cache_count", count)
        return count

    def _make_url_params(self, offset: int, limit: int) -> str:
        params = [
            f"{param}={value}" for param, value in request.args.items() if param not in ("offset", "limit")
        ]

        params.append(f"offset={offset}")
        params.append(f"limit={limit}")

        return "&".join(params)

    def next(self, offset: int, limit: int) -> str | None:
        if self.count() > (offset + limit):
            return f"{request.base_url}?{self._make_url_params(offset + limit, limit)}"

        return None

    def previus(self, offset: int, limit: int) -> str | None:
        if offset > 0:
            target_offset = offset - limit
            target_offset = target_offset if target_offset >= 0 else 0

            return f"{request.base_url}?{self._make_url_params(target_offset, limit)}"

        return None

    def _do(self, offset: int, limit: int = 0) -> list[dict[str, any]]:
        return [
            self._serializer_class.from_orm(entity).dict()
            for entity in self._query.limit(limit).offset(offset)
        ]

    def apply(self, offset: int, limit: int = 0) -> dict[str, any]:
        limit = limit if limit < self._max_limit else self._max_limit
        limit = limit if limit > 0 else self._default_limit

        offset = offset if offset < self.count() else self.count()

        return {
            "count": self.count(),
            "next": self.next(offset, limit),
            "previus": self.previus(offset, limit),
            "results": self._do(offset, limit),
        }
