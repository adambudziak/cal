from pytest import fixture
from tests.factories.meal import IngredientFactory, MealFactory

from pytest_factoryboy import register

from tests.factories.user import UserFactory

register(UserFactory)

register(IngredientFactory)
register(MealFactory)

@fixture
def meal_tree(meal_factory):
    parent_meal = meal_factory.create(ingredient=None)
    meal_factory.create_batch(3, parent=parent_meal)
    return parent_meal
