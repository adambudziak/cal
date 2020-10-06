import factory
from factory.fuzzy import FuzzyFloat

from models import Ingredient


class IngredientFactory(factory.Factory):
    class Meta:
        model = Ingredient

    name = factory.Faker("name")
    calories = FuzzyFloat(1, 100)
