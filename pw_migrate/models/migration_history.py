import datetime
from peewee import Model, CharField, DateTimeField, BigIntegerField

class MigrationHistory(Model):
    version = CharField(max_length=14, unique=True)
    name = CharField(max_length=255)
    checksum = CharField(max_length=64, null=True)
    status = CharField(max_length=20)
    executed_at = DateTimeField(default=datetime.datetime.now)
    execution_time_ms = BigIntegerField(null=True)
    executed_by = CharField(max_length=255, null=True)
    hostname = CharField(max_length=255, null=True)
    git_commit = CharField(max_length=255, null=True)
    python_version = CharField(max_length=50, null=True)

    class Meta:
        table_name = "migration_history"
