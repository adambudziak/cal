from pytest import fixture

from core import database, migrator
from core.database import get_db
from main import app
from starlette.testclient import TestClient

from .factories.conftest import *  # noqa

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


client = TestClient(app)


@fixture
def app_client():
    return client
