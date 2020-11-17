from typing import Type

import peewee
from fastapi import HTTPException
from starlette import status


def get_or_404(model: Type[peewee.Model], *args):
    try:
        instance = model.get(*args)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return instance
