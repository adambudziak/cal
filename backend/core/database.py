from contextlib import contextmanager
from contextvars import ContextVar

import peewee

import psycopg2
from fastapi import Depends
from psycopg2 import OperationalError, sql
from psycopg2.errorcodes import DUPLICATE_DATABASE
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_name: str = Field(..., env="POSTGRES_DB")
    database_user: str = Field(..., env="POSTGRES_USER")
    database_password: str = Field(..., env="POSTGRES_PASSWORD")
    database_host: str = Field(..., env="POSTGRES_HOST")


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


def init_db(settings: Settings = None):
    if not settings:
        settings = Settings()

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
        if db.obj.is_closed():
            db.obj.connect()
        yield
    finally:
        if not db.obj.is_closed():
            db.obj.close()


def create_database(
    settings: Settings, dbname: str, ignore_duplicate=False, delete=False
):
    assert not (
        ignore_duplicate and delete
    ), "You cannot set both `ignore_duplicate` and `delete`."
    conn = psycopg2.connect(
        database=settings.database_name,
        user=settings.database_user,
        password=settings.database_password,
        host=settings.database_host,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    if delete:
        cursor.execute(
            sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(dbname))
        )

    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
    except OperationalError as e:
        if e.pgcode != DUPLICATE_DATABASE or not ignore_duplicate:
            raise e
