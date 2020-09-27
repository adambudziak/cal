from datetime import datetime
from typing import List

from core import migrator
from core.database import get_db, init_db
from fastapi import Depends, FastAPI

from core.utils import get_or_404
from models import Ingredient
from schemas import IngredientOutput, IngredientCreate, IngredientUpdate
from settings import AppSettings

app = FastAPI()
init_db(AppSettings())


@app.on_event("startup")
async def initialize_database():
    with get_db():
        migrator.run()


@app.get(
    "/ingredients",
    response_model=List[IngredientOutput],
    dependencies=[Depends(get_db)],
)
def get_ingredients():
    return list(Ingredient.select())


@app.post(
    "/ingredients", response_model=IngredientOutput, dependencies=[Depends(get_db)]
)
def create_ingredient(ingredient: IngredientCreate):
    return Ingredient.create(**ingredient.dict(), created_at=datetime.now())


@app.get(
    "/ingredients/{ingredient_id}", response_model=IngredientOutput,
)
def get_ingredient(ingredient_id: int, db=Depends(get_db)):
    return get_or_404(Ingredient, Ingredient.id == ingredient_id)


@app.post(
    "/ingredients/{ingredient_id}",
    response_model=IngredientOutput,
    dependencies=[Depends(get_db)],
)
def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate):
    db_ingredient = get_or_404(Ingredient, Ingredient.id == ingredient_id)
    db_ingredient.row_update(**ingredient.dict()).save()
    return db_ingredient
