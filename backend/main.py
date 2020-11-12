import meals.router
import users.api.router
from core import migrator
from core.database import get_db, init_db
from fastapi import Depends, FastAPI
from fastapi.responses import Response

app = FastAPI()


@app.on_event("startup")
async def initialize_database():
    init_db()
    with get_db():
        migrator.run()


def inject_cors(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:19006"


app.include_router(
    meals.router.router,
    prefix="/meals",
    tags=["Meal"],
    dependencies=[Depends(inject_cors)],
)

app.include_router(
    users.api.router.router,
    prefix="/users",
    tags=["User"],
    dependencies=[Depends(inject_cors)],
)
