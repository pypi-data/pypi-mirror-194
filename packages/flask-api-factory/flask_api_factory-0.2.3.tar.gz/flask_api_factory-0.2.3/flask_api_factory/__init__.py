from http import HTTPStatus
from typing import Callable, Type

from flask import Blueprint, Request, request
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from flask_sqlalchemy.query import Query
from pydantic import BaseModel, schema_of

from .actions import ActionBase, ActionManage
from .auth import allow_any, factory_authorize_config
from .constants import ResourceTypes
from .decorators import is_authorized
from .filter import FilterBase
from .openapi import fill_api_doc
from .openapi.models import APIDoc
from .order import Order
from .page import Page


def factory_api(
    router: Blueprint,
    db: SQLAlchemy,
    Model: Model,
    Serializer: BaseModel | tuple[BaseModel, BaseModel],
    api_doc: APIDoc | None = None,
    get_query: Callable[[any, dict[str, any]], Query] | None = None,
    context: Callable[[Request], dict[str, any]] = (lambda: {}),
    page_class: Type[Page] = Page,
    actions: list[ActionBase] = [],
    filter_class: Type[FilterBase] | None = None,
    ordering: list[str] = ["id"],
    authorizers: dict[str, Callable[[Request], None]] = factory_authorize_config(),
    default_authorizer: Callable[[Request], None] = allow_any,
    enable_resource: ResourceTypes = ResourceTypes.ALL,
) -> None:
    action_manager = ActionManage(actions)

    InputSerializer = None
    OutputSerializer = None

    if isinstance(Serializer, tuple):
        InputSerializer, OutputSerializer = Serializer
    else:
        InputSerializer = OutputSerializer = Serializer

    is_allowed_create = authorizers.get("create", default_authorizer)
    is_allowed_update = authorizers.get("update", default_authorizer)
    is_allowed_delete = authorizers.get("delete", default_authorizer)
    is_allowed_retrive = authorizers.get("retrive", default_authorizer)

    if api_doc:
        fill_api_doc(api_doc, Model, InputSerializer, router, enable_resource)

    @is_authorized(is_allowed_delete)
    def destroy(id: str) -> tuple[dict[str, any] | str, int]:
        result: dict[str, any] | str = {"detail": "not implemented"}
        status = HTTPStatus.NOT_IMPLEMENTED

        with db.session() as session:
            query = get_query(session, context(request)) if get_query else session.query(Model)
            instance = query.get(id)

            if not instance:
                result["detail"] = f"{Model.__name__} with id '{id}' not found in database"
                status = HTTPStatus.NOT_FOUND
            else:
                action_manager.fire("before_delete", instance, None)
                query.where(Model.id == id).delete()
                session.commit()
                action_manager.fire("after_delete", None, instance)

                result = ""
                status = HTTPStatus.NO_CONTENT

        return result, status

    @is_authorized(is_allowed_update)
    def update(id: str) -> tuple[dict[str, any], int]:
        result = {"detail": "not implemented"}
        status = HTTPStatus.NOT_IMPLEMENTED

        with db.session() as session:
            query = get_query(session, context(request)) if get_query else session.query(Model)
            instance = query.get(id)

            if not instance:
                result["detail"] = f"{Model.__name__} with id '{id}' not found in database"
                status = HTTPStatus.NOT_FOUND
            else:
                values = {
                    **InputSerializer(**request.json).dict(),
                    "id": id,
                }

                instance = action_manager.fire("before_update", Model(**values), instance)
                query.where(Model.id == id).update(values)
                session.commit()
                instance = action_manager.fire("after_update", instance, instance)

                instance = query.get(id)
                result = OutputSerializer.from_orm(instance).dict()
                status = HTTPStatus.OK

        return result, status

    @is_authorized(is_allowed_update)
    def partial_update(id: str) -> tuple[dict[str, any], int]:
        result = {"detail": "not implemented"}
        status = HTTPStatus.NOT_IMPLEMENTED

        with db.session() as session:
            query = get_query(session, context(request)) if get_query else session.query(Model)
            instance = query.get(id)

            if not instance:
                result["detail"] = f"{Model.__name__} with id '{id}' not found in database"
                status = HTTPStatus.NOT_FOUND
            else:
                values = {**request.json}

                if "id" in values:
                    result["detail"] = "id not allowed in payload"
                    status = HTTPStatus.BAD_REQUEST
                else:
                    new_instance = action_manager.fire(
                        "before_update",
                        Model(**{**InputSerializer.from_orm(instance).dict(), **values}),
                        instance,
                    )
                    query.where(Model.id == id).update(InputSerializer.from_orm(new_instance).dict())
                    session.commit()
                    action_manager.fire("after_update", instance, instance)

                    instance = query.get(id)
                    result = OutputSerializer.from_orm(instance).dict()
                    status = HTTPStatus.OK

        return result, status

    @is_authorized(is_allowed_retrive)
    def retrive(id: str) -> tuple[dict[str, any], int]:
        result = {"detail": "not implemented"}
        status = HTTPStatus.NOT_IMPLEMENTED

        with db.session() as session:
            query = get_query(session, context(request)) if get_query else session.query(Model)
            instance = query.get(id)

            if not instance:
                result["detail"] = f"{Model.__name__} with id '{id}' not found in database"
                status = HTTPStatus.NOT_FOUND
            else:
                result = OutputSerializer.from_orm(instance).dict()
                status = HTTPStatus.OK

        return result, status

    @is_authorized(is_allowed_create)
    def create() -> tuple[dict[str, any], int]:
        result = {"detail": "not implemented"}
        status = HTTPStatus.NOT_IMPLEMENTED

        with db.session() as session:
            data = InputSerializer(**request.json)

            instance = Model(**data.dict())
            action_manager.fire("before_create", instance, None)
            session.add(instance)
            session.commit()
            action_manager.fire("after_create", instance, None)

            result = OutputSerializer.from_orm(instance).dict()
            status = HTTPStatus.CREATED

        return result, status

    @is_authorized(is_allowed_retrive)
    def list_items() -> tuple[dict[str, any], int]:
        result = {"detail": "not implemented"}
        status = HTTPStatus.NOT_IMPLEMENTED

        with db.session() as session:
            query = get_query(session, context(request)) if get_query else session.query(Model)
            query = Order(ordering).apply(query)

            if filter_class:
                query = filter_class().apply(query, request.args)

            offset = int(request.args.get("offset", 0))
            limit = int(request.args.get("limit", 0))

            result = page_class(query, OutputSerializer, 30).apply(offset, limit)
            status = HTTPStatus.OK

        return result, status

    (enable_resource & ResourceTypes.RETRIVE) and router.get("/<string:id>/")(retrive)
    (enable_resource & ResourceTypes.LIST) and router.get("/")(list_items)
    (enable_resource & ResourceTypes.CREATE) and router.post("/")(create)
    (enable_resource & ResourceTypes.UPDATE) and router.put("/<string:id>/")(update)
    (enable_resource & ResourceTypes.PARTIAL_UPDATE) and router.patch("/<string:id>/")(partial_update)
    (enable_resource & ResourceTypes.DESTROY) and router.delete("/<string:id>/")(destroy)
