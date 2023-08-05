import json
from datetime import date, datetime
from decimal import Decimal
from logging import getLogger

from flask_sqlalchemy.model import Model
from pika import BasicProperties, BlockingConnection, URLParameters
from pydantic import BaseModel

from . import ActionBase

logger = getLogger(__name__)


def _json_dumps_default(obj: any) -> any:
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)

    return str(obj)


class PublisherAction(ActionBase):
    def __init__(
        self, amqp_url: str, amqp_app: str, base_topic_name: str, serializer_class: BaseModel
    ) -> None:
        self._amqp_url = amqp_url
        self._amqp_app = amqp_app
        self._base_topic_name = base_topic_name
        self._serializer_class = serializer_class

    def publish(self, topic: str, router: str, body: dict[str, any]) -> None:
        logger.info(f"publish message on {topic}")
        logger.debug(f"{body=}")

        with BlockingConnection(URLParameters(self._amqp_url)) as amqp:
            with amqp.channel() as channel:
                channel.exchange_declare(topic, "topic", durable=True)
                channel.basic_publish(
                    topic,
                    router,
                    json.dumps({"body": body}, default=_json_dumps_default).encode(),
                    BasicProperties(content_type="application/json", app_id=self._amqp_app),
                )

    def after_create(self, instance: Model, older: Model | None) -> Model | None:
        self.publish(f"{self._base_topic_name}", "created", self._serializer_class.from_orm(instance).dict())

        return super().after_create(instance, older)

    def after_update(self, instance: Model, older: Model | None) -> Model | None:
        self.publish(f"{self._base_topic_name}", "updated", self._serializer_class.from_orm(instance).dict())

        return super().after_create(instance, older)

    def after_delete(self, instance: Model, older: Model | None) -> Model | None:
        self.publish(f"{self._base_topic_name}", "deleted", self._serializer_class.from_orm(older).dict())

        return super().after_create(instance, older)
