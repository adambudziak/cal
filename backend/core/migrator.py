import peewee
from playhouse.migrate import PostgresqlMigrator

from core import logger
from core.database import db
from core.models import Migrations, registered_models
from migrations import migrations_iterator

logger = logger.get_logger(__name__)

migrator = PostgresqlMigrator(db)


def init_tables():
    db.create_tables(list(registered_models()))


def run_migrations():
    done_migrations = set(m.module for m in Migrations.select(Migrations.module))
    for migration in migrations_iterator():
        migration_name = migration.__name__
        if migration_name not in done_migrations:
            logger.info(f"Running migration {migration_name}")
            try:
                with db.atomic():
                    migration.commands(migrator)
            except peewee.ProgrammingError as e:
                logger.warn(f"Migration {migration_name} failed. Exception: {e}")
            Migrations.create(module=migration_name)
        else:
            logger.info(f"Skipping migration {migration_name}")


def run():
    init_tables()
    run_migrations()
