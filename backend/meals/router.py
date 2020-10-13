from fastapi import APIRouter, Depends

from core.database import get_db
from meals.api import ingredient, meal

router = APIRouter()

router.include_router(
    ingredient.router, prefix="/ingredients", dependencies=[Depends(get_db)]
)
router.include_router(meal.router, prefix="/meals", dependencies=[Depends(get_db)])
