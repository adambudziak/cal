from meals.models import Ingredient
from starlette import status


def test_create_ingredient(app_client):
    response = app_client.post(
        "/meals/ingredients/", json={"name": "Chicken breasts", "calories": 153}
    )
    assert response.status_code == status.HTTP_201_CREATED, response.content
    ingredient = Ingredient.get()
    assert all((ingredient.calories == 153, ingredient.name == "Chicken breasts"))


def test_no_ingredients(app_client):
    response = app_client.get("/meals/ingredients/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_ingredient(app_client, ingredient):
    response = app_client.get("/meals/ingredients/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "calories": ingredient.calories,
            "created_at": ingredient.created_at.isoformat(),
            "name": ingredient.name,
            "id": ingredient.id,
        }
    ]
