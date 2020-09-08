from typing import List

from core import migrator
from core.database import get_db
from fastapi import Depends, FastAPI
from models import Ingredient
from schemas import IngredientSchema

app = FastAPI()


@app.on_event("startup")
async def initialize_database(_=Depends(get_db)):
    migrator.run()


@app.get("/", response_model=List[IngredientSchema], dependencies=[Depends(get_db)])
def get_ingredients():
    ingredients = list(Ingredient.select())
    return ingredients


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
