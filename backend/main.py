import meals.router
from core import migrator
from core.database import get_db, init_db
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def initialize_database():
    init_db()
    with get_db():
        migrator.run()


app.include_router(meals.router.router, prefix="/meals", tags=["Meal"])
