# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_api_factory',
 'flask_api_factory.actions',
 'flask_api_factory.filter',
 'flask_api_factory.openapi']

package_data = \
{'': ['*']}

install_requires = \
['flask-migrate>=4.0.4,<5.0.0',
 'flask-sqlalchemy>=3.0.3,<4.0.0',
 'flask>=2.2.2,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pika>=1.3.1,<2.0.0',
 'prometheus-flask-exporter>=0.21.0,<0.22.0',
 'pydantic[dotenv]>=1.10.4,<2.0.0']

extras_require = \
{'mysql': ['mysql>=0.0.3,<0.0.4'],
 'postgres': ['psycopg2-binary>=2.9.5,<3.0.0']}

setup_kwargs = {
    'name': 'flask-api-factory',
    'version': '0.2.0',
    'description': 'one small flask rest api factory',
    'long_description': 'The initial idea is to be a Rest API factory, with the aim of making it easy to create from models defined using the SQLAlchemy ORM.\n\nWe still use pydantic to serialize objects and payloads.\n\n## Install\n\nYou can install using pip:\n\n```shell\n$ pip install flask-api-factory\n```\n\nYou can install with the database driver you want to be supported by SQLAlchemy, but if you prefer, you can install the driver as an extra library, with the command:\n\n```shell\n$ pip install flask-api-factory[postgres]\n```\n\nThis will install `psycopg2` together with our library.\n\nYou can still install using `poetry` with the command:\n\n```shell\n$ poetry add flask-api-factory\n```\n\n## A simple example\n\nHaving the `Pet` model already defined and the initialization of the `Flask` application already started, just use the following code:\n\n```python\nfrom flask import Flask, Blueprint\nfrom flask_api_factory import factory_api\n\nfrom .models import Pet\nfrom .serializers import PetSerializer\n\n\nblueprint = Blueprint("pets", __name__, url_prefix="/pets")\n\n\ndef init_app(app: Flask) -> None:\n    app.register_blueprint(blueprint)\n\nfactory_api(blueprint, Pet, PetSerializer)\n```\n\nThis way we will have a `/pets` endpoint capable of responding to all HTTP verbs. Consulting the documentation you can check other options for configurations and functionalities.\n\n## Roadmap\n\n1. Documentation;\n1. `openapi.json` generation mechanism;\n1. A way to provide `Swagger` and/or `Redoc`;\n1. Write unit tests.\n',
    'author': 'Rodrigo Pinheiro Matias',
    'author_email': 'rodrigopmatias@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rodrigopmatias/flask-api-factory/blob/main/README.md',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
