from flask import request
from sqlalchemy.orm import Query
from sqlalchemy.sql import text


def query_order_param(param: str) -> str:
    return f"{param[1:]} DESC" if param.startswith("-") else param


class Order(object):
    def __init__(self, default_order_params: list[str]) -> None:
        self._default_order_params = default_order_params

    def _order_params(self) -> list[str]:
        user_order_params = self._user_order_params()
        return user_order_params if user_order_params else self._default_order_params

    def _user_order_params(self) -> list[str]:
        ordering: str = request.args.get("ordering", None)

        if ordering:
            return ordering.split(",")

        return []

    def _query_order_params(self) -> list[str]:
        return [query_order_param(param) for param in self._order_params()]

    def apply(self, query: Query) -> Query:
        return query.order_by(text(", ".join(self._query_order_params())))
