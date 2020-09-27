from contextlib import contextmanager
from contextvars import ContextVar

import peewee

from fastapi import Depends
from pydantic import BaseSettings, Field
from settings import AppSettings


class Settings(BaseSettings):
    database_name: str = Field(..., env="POSTGRES_DB")
    database_user: str = Field(..., env="POSTGRES_USER")
    database_password: str = Field(..., env="POSTGRES_PASSWORD")
    database_host: str = Field(..., env="POSTGRES_HOST")


class TestSettings(Settings):
    database_name = "test_db"


db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        self._state.get()[key] = value

    def __getattr__(self, key):
        return self._state.get()[key]


db = peewee.DatabaseProxy()


def init_db(app_settings: AppSettings):
    settings = TestSettings() if app_settings.test else Settings()
    _init_db(settings)


def _init_db(settings: Settings):
    db.initialize(
        peewee.PostgresqlDatabase(
            settings.database_name,
            user=settings.database_user,
            host=settings.database_host,
            password=settings.database_password,
        )
    )
    db.obj._state = PeeweeConnectionState()


async def reset_db_state():
    db.obj._state._state.set(db_state_default.copy())
    db.obj._state.reset()


@contextmanager
def get_db(db_state=Depends(reset_db_state)):
    try:
        db.obj.connect()
        yield
    finally:
        if not db.obj.is_closed():
            db.obj.close()
