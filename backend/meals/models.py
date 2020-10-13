from datetime import datetime

import peewee

from core.models import BaseModel, register_model


@register_model
class Ingredient(BaseModel):
    created_at = peewee.DateTimeField(default=datetime.now())
    name = peewee.CharField(max_length=50)
    calories = peewee.FloatField()


@register_model
class Meal(BaseModel):
    created_at = peewee.DateTimeField(default=datetime.now())
    name = peewee.CharField(max_length=50)
    ingredient = peewee.ForeignKeyField(
        Ingredient, null=True, backref="meals", on_delete="SET NULL"
    )
    parent = peewee.ForeignKeyField("self", null=True, backref="sub_meals")
