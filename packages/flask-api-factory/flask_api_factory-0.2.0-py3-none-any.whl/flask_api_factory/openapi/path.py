from typing import Type

from flask import Blueprint
from flask_sqlalchemy.model import Model

from flask_api_factory.constants import (
    ENABLE_RESOURCE_CREATE,
    ENABLE_RESOURCE_DESTROY,
    ENABLE_RESOURCE_LIST,
    ENABLE_RESOURCE_PARTIAL_UPDATE,
    ENABLE_RESOURCE_RETRIVE,
    ENABLE_RESOURCE_UPDATE,
)

from .models import APIDoc


def _build_api_path_base(tags: list[str], summary: str = "undefined") -> dict[str, any]:
    return {"tags": tags, "summary": summary}


def _build_api_path_id_parameters():
    return {
        "parameters": [
            {
                "name": "id",
                "required": True,
                "description": "id of item",
                "in": "path",
                "schema": {"type": "string"},
            }
        ],
    }


def _build_api_path_default_responses(
    object: str, success_status: str = "200", success_description: str = "Ok", with_content: bool = True
):
    success_response = {success_status: {"description": success_description}}

    if with_content:
        success_response[success_status]["content"] = {
            "application/json": {
                "schema": {
                    "$ref": f"#/components/schemas/{object}",
                }
            }
        }

    return {
        **success_response,
        "401": {
            "description": "Un Autheticated",
            "content": {
                "application/json": {
                    "schema": {"type": "object", "properties": {"detail": {"type": "string"}}}
                }
            },
        },
        "403": {
            "description": "Un Authorized",
            "content": {
                "application/json": {
                    "schema": {"type": "object", "properties": {"detail": {"type": "string"}}}
                }
            },
        },
    }


def _build_api_path_retrive(tags: list[str]):
    return {
        **_build_api_path_base(tags, "retrive one item by id"),
        **_build_api_path_id_parameters(),
        "responses": {**_build_api_path_default_responses(tags[0])},
    }


def _build_api_path_request_body(object: str):
    return {
        "requestBody": {
            "content": {"application/json": {"schema": {"$ref": f"#/components/schemas/{object}"}}}
        },
    }


def _build_api_path_create(tags: list[str]):
    return {
        **_build_api_path_base(tags, "create one item"),
        **_build_api_path_request_body(tags[0]),
        "responses": {**_build_api_path_default_responses(tags[0], "201", "Created with success")},
    }


def _build_api_path_update(tags: list[str]):
    return {
        **_build_api_path_base(tags, "update one item by id"),
        **_build_api_path_id_parameters(),
        **_build_api_path_request_body(tags[0]),
        "responses": {
            **_build_api_path_default_responses(tags[0], success_description="Updated with success")
        },
    }


def _build_api_path_partial_update(tags: list[str]):
    return {
        **_build_api_path_base(tags, "patch one item by id"),
        **_build_api_path_id_parameters(),
        **_build_api_path_request_body(tags[0]),
        "responses": {
            **_build_api_path_default_responses(tags[0], success_description="Updated with success")
        },
    }


def _build_api_path_destroy(tags: list[str]):
    return {
        **_build_api_path_base(tags, "destroy one item by id"),
        **_build_api_path_id_parameters(),
        "responses": {**_build_api_path_default_responses(tags[0], "204", "Deleted with success", False)},
    }


def _build_api_path_list(tags: list[str]):
    return {
        **_build_api_path_base(tags, "retrive one list of items"),
        "responses": {
            **_build_api_path_default_responses(tags[0]),
            "200": {
                "description": "Ok",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "count": {"type": "number"},
                                "next": {"type": "string"},
                                "previus": {"type": "string"},
                                "results": {
                                    "type": "array",
                                    "items": {"$ref": f"#/components/schemas/{tags[0]}"},
                                },
                            },
                        }
                    }
                },
            },
        },
    }


def fill_api_doc_paths(
    api_doc: APIDoc, router: Blueprint, enable_resource: int, model_class: Type[Model]
) -> None:
    tags = [model_class.__name__]

    if enable_resource & (ENABLE_RESOURCE_RETRIVE | ENABLE_RESOURCE_CREATE):
        paths = {}

        (enable_resource | ENABLE_RESOURCE_RETRIVE) and paths.update(get=_build_api_path_list(tags))
        (enable_resource | ENABLE_RESOURCE_RETRIVE) and paths.update(post=_build_api_path_create(tags))

        api_doc.paths[f"{router.url_prefix}/"] = paths

    if enable_resource & (
        ENABLE_RESOURCE_RETRIVE
        | ENABLE_RESOURCE_UPDATE
        | ENABLE_RESOURCE_PARTIAL_UPDATE
        | ENABLE_RESOURCE_DESTROY
    ):
        paths = {}

        (enable_resource | ENABLE_RESOURCE_LIST) and paths.update(get=_build_api_path_retrive(tags))
        (enable_resource | ENABLE_RESOURCE_UPDATE) and paths.update(put=_build_api_path_update(tags))
        (enable_resource | ENABLE_RESOURCE_PARTIAL_UPDATE) and paths.update(
            patch=_build_api_path_partial_update(tags)
        )
        (enable_resource | ENABLE_RESOURCE_DESTROY) and paths.update(delete=_build_api_path_destroy(tags))

        api_doc.paths["/".join([router.url_prefix, "{id}", ""])] = paths
