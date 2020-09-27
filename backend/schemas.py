from datetime import datetime
from typing import Any, Optional

import peewee

from pydantic import BaseModel, validator
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class BasePeeweeSchema(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = GetterDict


class IngredientOutput(BasePeeweeSchema):
    id: int
    created_at: datetime
    name: str
    calories: float


class IngredientCreate(BasePeeweeSchema):
    name: str
    calories: float


class IngredientUpdate(BasePeeweeSchema):
    name: str
    calories: float
