from playhouse.migrate import PostgresqlMigrator

from core.database import db
from core.models import Migrations, registered_models
from migrations import migrations_iterator

migrator = PostgresqlMigrator(db)


def init_tables():
    db.create_tables(list(registered_models()))


def run_migrations():
    done_migrations = set(m.module for m in Migrations.select(Migrations.module))
    for migration in migrations_iterator():
        migration_name = migration.__name__

        if migration_name not in done_migrations:
            migration.commands(migrator)
            Migrations.create(module=migration_name)


def run():
    init_tables()
    run_migrations()
