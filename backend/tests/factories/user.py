import factory

from tests.factories.base import PeeweeModelFactory
from users.models import User


class UserFactory(PeeweeModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    nickname = factory.Faker("name")
    password = factory.Faker("password")
