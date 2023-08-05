from typing import Type

from flask import Blueprint, Flask
from flask_sqlalchemy.model import Model
from pydantic import BaseModel, schema_of

from .models import APIDoc, APITag
from .path import fill_api_doc_paths

blueprint = Blueprint("flask-api-factory-openapi", __name__, url_prefix="")


def init_app(app: Flask, api_doc: APIDoc) -> None:
    @blueprint.get("/openapi.json")
    def get():
        return api_doc.dict(), 200

    app.register_blueprint(blueprint)


def _schema_of(serializer_class: BaseModel, model_class: Model) -> dict[str, any]:
    return {
        **schema_of(serializer_class)["definitions"][serializer_class.__name__],
        "title": model_class.__name__,
    }


def fill_api_doc(
    api_doc: APIDoc,
    model_class: Type[Model],
    serializer_class: Type[BaseModel],
    router: Blueprint,
    enable_resource: int,
) -> None:
    api_doc.tags.append(
        APITag(
            name=model_class.__name__,
            description=getattr(Model, "__description__", "no model description defined"),
        )
    )

    schemas = api_doc.components.get("schemas", {})
    schemas[model_class.__name__] = _schema_of(serializer_class, model_class)

    api_doc.components.update(schemas=schemas)

    fill_api_doc_paths(api_doc, router, enable_resource, model_class)
