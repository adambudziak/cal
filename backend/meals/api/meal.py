from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Union

from fastapi import APIRouter
from fastapi import Response
from more_itertools import partition
from pydantic import Field, validator
from starlette import status

from core.schemas import BaseSchema
from meals.api.ingredient import IngredientCreate, IngredientResponse
from meals.models import Meal

router = APIRouter()


class MealWithIngredientCreate(BaseSchema):
    name: str
    ingredient: IngredientCreate

    def to_orm(self):
        return Meal(name=self.name, ingredient=self.ingredient.to_orm())

    def save(self):
        meal = self.to_orm()
        meal.ingredient.save()
        meal.save()
        return meal


class MealWithSubMealsCreate(BaseSchema):
    name: str
    sub_meals: List[
        Union[MealWithIngredientCreate, MealWithSubMealsCreate, int]
    ] = Field(
        ...,
        description="A list of meals used as sub-meals. "
        "Each can be specified either by an `object` to *create* a new sub-meal, "
        "or by an `ID:int` to *use an existing one*. Note: Using an existing `sub-meal` "
        "that already has a parent will result in making a copy of it.",
    )

    @validator("sub_meals")
    def all_ids_must_exist(cls, sub_meals):
        ids = [meal for meal in sub_meals if isinstance(meal, int)]
        meals = Meal.select().where(Meal.id.in_(ids))
        existing_ids = {meal.id for meal in meals}
        missing_ids = set(ids) - existing_ids
        if len(meals) != len(ids):
            raise ValueError(f"Meal ids {missing_ids} do not exist.")

        for meal in meals:
            # we need to make sure that sub-meals used in other meal-trees are not
            # stolen from there, so we make a copy by removing the id.
            meal.id = None
        return meals

    def to_orm(self):
        meal = Meal(name=self.name)
        sub_meals = [
            sub_meal.to_orm() if not isinstance(sub_meal, Meal) else sub_meal
            for sub_meal in self.sub_meals
        ]
        for sub_meal in sub_meals:
            sub_meal.parent = meal

        meal.sub_meals = sub_meals
        return meal

    @staticmethod
    def _exists(meal):
        return meal.id is not None

    def save(self):
        meal = self.to_orm()
        existing_, new_ = partition(self._exists, meal.sub_meals)
        Meal.bulk_update(list(existing_), fields=["parent"])
        Meal.bulk_create(list(new_) + [meal])
        return meal


MealType = Union[MealWithIngredientCreate, MealWithSubMealsCreate]


MealWithSubMealsCreate.update_forward_refs()


class MealResponse(BaseSchema):
    id: int
    created_at: datetime
    name: str
    ingredient: Optional[IngredientResponse] = None
    sub_meals: List[MealResponse] = []


MealResponse.update_forward_refs()


@router.post("/", response_model=MealResponse)
def create_meal(meal: MealType, response: Response):
    response.status_code = status.HTTP_201_CREATED
    return meal.save()


@router.get("/", response_model=List[MealResponse])
def get_meals():
    return list(Meal.select())
