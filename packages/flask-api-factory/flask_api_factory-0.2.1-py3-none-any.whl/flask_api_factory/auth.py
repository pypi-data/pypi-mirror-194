from flask import Request


def allow_any(request: Request):
    pass


def factory_authorize_config(
    allow_create=allow_any, allow_update=allow_any, allow_delete=allow_any, allow_retrive=allow_any
):
    return {
        "create": allow_create,
        "update": allow_update,
        "delete": allow_delete,
        "retrive": allow_retrive,
    }
