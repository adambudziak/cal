from datetime import datetime
from typing import List

from fastapi import Depends, APIRouter, Response
from starlette import status

from core.database import get_db
from core.schemas import BaseSchema
from core.utils import get_or_404
from meals.models import Ingredient

router = APIRouter()


class IngredientResponse(BaseSchema):
    id: int
    created_at: datetime
    name: str
    calories: float


@router.get(
    "/", response_model=List[IngredientResponse], dependencies=[Depends(get_db)],
)
def get_ingredients():
    return list(Ingredient.select())


class IngredientCreate(BaseSchema):
    name: str
    calories: float

    def to_orm(self):
        return Ingredient(**self.dict())


@router.post("/", response_model=IngredientResponse)
def create_ingredient(ingredient: IngredientCreate, response: Response):
    response.status_code = status.HTTP_201_CREATED
    return ingredient.to_orm().save()


@router.get(
    "/{ingredient_id}", response_model=IngredientResponse,
)
def get_ingredient(ingredient_id: int):
    return get_or_404(Ingredient, Ingredient.id == ingredient_id)


class IngredientUpdate(BaseSchema):
    name: str
    calories: float


@router.post(
    "/{ingredient_id}", response_model=IngredientResponse,
)
def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate):
    db_ingredient = get_or_404(Ingredient, Ingredient.id == ingredient_id)
    db_ingredient.row_update(**ingredient.dict()).save()
    return db_ingredient
