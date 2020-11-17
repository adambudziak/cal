from datetime import datetime

import peewee

from core.models import register_model, BaseModel


@register_model
class User(BaseModel):
    first_name = peewee.CharField(max_length=30, null=True)
    last_name = peewee.CharField(max_length=30, null=True)
    nickname = peewee.CharField(max_length=30, unique=True)
    email = peewee.CharField(max_length=50, unique=True)
    disabled = peewee.BooleanField(default=False)
    created_at = peewee.DateTimeField(default=datetime.now())
    password = peewee.CharField(max_length=100, null=True)
