from peewee import BooleanField, CharField, DateTimeField, IntegerField, Model


class MigrationLock(Model):
    id = IntegerField(primary_key=True)
    is_locked = BooleanField(default=False)
    locked_at = DateTimeField(null=True)
    locked_by = CharField(max_length=255, null=True)
    pid = IntegerField(null=True)
