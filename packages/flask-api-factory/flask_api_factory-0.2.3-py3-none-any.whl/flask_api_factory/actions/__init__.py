from logging import getLogger

from flask_sqlalchemy.model import Model

logger = getLogger(__name__)


class ActionBase(object):
    def before_create(self, instance: Model, older: Model | None) -> Model | None:
        return instance

    def after_create(self, instance: Model, older: Model | None) -> Model | None:
        return instance

    def before_update(self, instance: Model, older: Model | None) -> Model | None:
        return instance

    def after_update(self, instance: Model, older: Model | None) -> Model | None:
        return instance

    def before_delete(self, instance: Model, older: Model | None) -> Model | None:
        return instance

    def after_delete(self, instance: Model, older: Model | None) -> Model | None:
        return instance


class LoggerAction(ActionBase):
    def before_create(self, instance: Model, older: Model | None) -> Model | None:
        logger.info(f"before create {type(instance).__name__}")
        return super().before_create(instance, older)

    def after_create(self, instance: Model, older: Model | None) -> Model | None:
        logger.info(f"after create {type(instance).__name__} with id {instance.id}")
        return super().before_create(instance, older)

    def before_update(self, instance: Model, older: Model | None) -> Model | None:
        logger.info(f"before update {type(instance).__name__} with id {instance.id}")
        return super().before_update(instance, older)

    def after_update(self, instance: Model, older: Model | None) -> Model | None:
        logger.info(f"after update {type(instance).__name__} with id {instance.id}")
        return super().before_update(instance, older)

    def before_delete(self, instance: Model, older: Model | None) -> Model | None:
        logger.info(f"before delete {type(instance).__name__} with id {instance.id}")
        return super().before_delete(instance, older)

    def after_delete(self, instance: Model, older: Model | None) -> Model | None:
        logger.info(f"after delete {type(instance).__name__} with id {older.id}")
        return super().before_delete(instance, older)


class ActionManage(object):
    def __init__(self, actions: list[ActionBase]) -> None:
        self._actions = actions

    def fire(self, event_name: str, instance: Model, older: Model | None = None) -> Model | None:
        for action in self._actions:
            method = getattr(action, event_name, None)

            if method:
                instance = method(instance, older)

        return instance
