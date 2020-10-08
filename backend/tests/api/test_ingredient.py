from core.database import Settings
from main import app
from models import Ingredient
from starlette import status
from starlette.testclient import TestClient

settings = Settings()

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


def test_no_ingredients():
    response = client.get("/ingredients")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_ingredient(ingredient):
    ingredient.save()
    response = client.get("/ingredients")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "calories": ingredient.calories,
            "created_at": ingredient.created_at.isoformat(),
            "name": ingredient.name,
            "id": ingredient.id,
        }
    ]
