from tests.factories.base import PeeweeModelFactory

import factory
from factory.fuzzy import FuzzyInteger
from meals.models import Ingredient, Meal


class IngredientFactory(PeeweeModelFactory):
    class Meta:
        model = Ingredient

    name = factory.Faker("name")
    calories = FuzzyInteger(1, 100)


class MealFactory(PeeweeModelFactory):
    class Meta:
        model = Meal

    name = factory.Faker("name")
    ingredient = factory.SubFactory(IngredientFactory)
