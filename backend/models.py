import peewee

from core.models import BaseModel, register_model


@register_model
class Ingredient(BaseModel):
    created_at = peewee.DateTimeField()
    name = peewee.CharField(max_length=50)
    calories = peewee.FloatField()
