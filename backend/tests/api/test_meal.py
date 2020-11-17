from starlette import status

from meals.models import Meal


def test_create_meal_with_ingredient(app_client):
    response = app_client.post(
        "/meals/meals/",
        json={"name": "French toast", "ingredient": {"name": "Bread", "calories": 100}},
    )
    assert response.status_code == status.HTTP_201_CREATED
    meal = Meal.get()
    assert all(
        (
            meal.name == "French toast",
            meal.ingredient.calories == 100,
            meal.ingredient.name == "Bread",
        )
    )


def test_get_meals_ingredient(app_client, meal):
    response = app_client.get("/meals/meals/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "sub_meals": [],
            "name": meal.name,
            "created_at": meal.created_at.isoformat(),
            "id": meal.id,
            "ingredient": {
                "name": meal.ingredient.name,
                "calories": meal.ingredient.calories,
                "created_at": meal.ingredient.created_at.isoformat(),
                "id": meal.ingredient.id,
            },
        }
    ]


def test_get_meals_submeals(app_client, meal_tree):
    response = app_client.get("/meals/meals/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    actual_parent = next(meal for meal in data if meal["id"] == meal_tree.id)
    assert actual_parent["sub_meals"] == [
        meal for meal in data if meal["id"] != meal_tree.id
    ]
