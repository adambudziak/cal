from datetime import datetime

import peewee
from playhouse.postgres_ext import TSVectorField

from core.models import BaseModel, register_model


@register_model
class Ingredient(BaseModel):
    created_at = peewee.DateTimeField(default=datetime.now())
    name = peewee.CharField(max_length=50)
    search_name = TSVectorField()
    calories = peewee.FloatField()

    def save(self, force_insert=False, only=None):
        self.search_name = peewee.fn.to_tsvector(self.name)
        return super().save(force_insert=force_insert, only=only)


@register_model
class Meal(BaseModel):
    created_at = peewee.DateTimeField(default=datetime.now())
    name = peewee.CharField(max_length=50)
    ingredient = peewee.ForeignKeyField(
        Ingredient, null=True, backref="meals", on_delete="SET NULL"
    )
    parent = peewee.ForeignKeyField("self", null=True, backref="sub_meals")
