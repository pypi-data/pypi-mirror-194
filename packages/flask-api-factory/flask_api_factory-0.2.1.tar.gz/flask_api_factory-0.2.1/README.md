The initial idea is to be a Rest API factory, with the aim of making it easy to create from models defined using the SQLAlchemy ORM.

We still use pydantic to serialize objects and payloads.

## Install

You can install using pip:

```shell
$ pip install flask-api-factory
```

You can install with the database driver you want to be supported by SQLAlchemy, but if you prefer, you can install the driver as an extra library, with the command:

```shell
$ pip install flask-api-factory[postgres]
```

This will install `psycopg2` together with our library.

You can still install using `poetry` with the command:

```shell
$ poetry add flask-api-factory
```

## A simple example

Having the `Pet` model already defined and the initialization of the `Flask` application already started, just use the following code:

```python
from flask import Flask, Blueprint
from flask_api_factory import factory_api

from .models import Pet
from .serializers import PetSerializer


blueprint = Blueprint("pets", __name__, url_prefix="/pets")


def init_app(app: Flask) -> None:
    app.register_blueprint(blueprint)

factory_api(blueprint, Pet, PetSerializer)
```

This way we will have a `/pets` endpoint capable of responding to all HTTP verbs. Consulting the documentation you can check other options for configurations and functionalities.

## Roadmap

 * [ ] Documentation;
 * [X] `openapi.json` generation mechanism;
 * [ ] A way to provide `Swagger` and/or `Redoc`;
 * [ ] Write unit tests.
