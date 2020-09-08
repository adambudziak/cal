from datetime import datetime

import peewee

from core.database import db

__REGISTERED_MODELS = []


def register_model(model):
    __REGISTERED_MODELS.append(model)
    return model


def registered_models():
    return (model for model in __REGISTERED_MODELS)


class BaseModel(peewee.Model):
    class Meta:
        database = db


@register_model
class Migrations(BaseModel):
    created_at = peewee.DateTimeField(default=datetime.now)
    module = peewee.CharField(max_length=100)
