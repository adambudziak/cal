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

    def row_update(self, **fields):
        for name, value in fields.items():
            setattr(self, name, value)
        return self

    def save(self, force_insert=False, only=None):
        super().save(force_insert=force_insert, only=only)
        return self


@register_model
class Migrations(BaseModel):
    created_at = peewee.DateTimeField(default=datetime.now)
    module = peewee.CharField(max_length=100)
