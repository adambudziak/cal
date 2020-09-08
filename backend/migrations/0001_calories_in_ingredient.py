import peewee
from playhouse.migrate import SchemaMigrator, migrate


def commands(migrator: SchemaMigrator):
    migrate(migrator.add_column("ingredient", "calories", peewee.FloatField(default=0)))
