import factory
from factory.fuzzy import FuzzyInteger
from models import Ingredient


class IngredientFactory(factory.Factory):
    class Meta:
        model = Ingredient

    name = factory.Faker("name")
    calories = FuzzyInteger(1, 100)
