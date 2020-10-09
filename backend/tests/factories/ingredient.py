from tests.factories.base import PeeweeModelFactory

import factory
from factory.fuzzy import FuzzyInteger
from models import Ingredient


class IngredientFactory(PeeweeModelFactory):
    class Meta:
        model = Ingredient

    name = factory.Faker("name")
    calories = FuzzyInteger(1, 100)
