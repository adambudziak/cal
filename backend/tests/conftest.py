from pytest import fixture

from core import database
from core import migrator
from core.database import get_db

from pytest_factoryboy import register
from tests.factories.ingredient import IngredientFactory

TEST_DB_NAME = "test_db"


@fixture(scope="session", autouse=True)
def initialize_database():
    db_settings = database.Settings()
    database.create_database(db_settings, TEST_DB_NAME, delete=True)
    db_settings.database_name = TEST_DB_NAME
    database.init_db(db_settings)


@fixture(autouse=True)
def reset_database():
    with get_db():
        migrator.reset_tables()


register(IngredientFactory)
