from pytest import fixture

from core import migrator
from core.database import Settings, get_db
from main import app
from models import Ingredient
from starlette import status
from starlette.testclient import TestClient

settings = Settings()


@fixture(scope="session", autouse=True)
def initialize_database():
    with get_db():
        migrator.run()


client = TestClient(app)


def test_create_ingredient():
    response = client.post(
        "/ingredients", json={"name": "Chicken breasts", "calories": 153}
    )
    assert response.status_code == status.HTTP_200_OK, response.content
    response = client.get("/ingredients")
    assert response.status_code == status.HTTP_200_OK, response.content
    ingredient = Ingredient.get()
    assert all((ingredient.calories == 153, ingredient.name == "Chicken breasts"))
