import pytest
from peewee import SqliteDatabase
from pw_migrate.models.migration_history import MigrationHistory
from pw_migrate.core.migration_history import setup_history_table, get_applied_migrations, get_current_version
import datetime

@pytest.fixture
def db():
    database = SqliteDatabase(":memory:")
    setup_history_table(database)
    yield database
    database.close()

def test_setup_history_table(db):
    assert db.table_exists("migration_history")

def test_get_applied_migrations(db):
    MigrationHistory.create(version="20260728124500", name="create_users", status="UP")
    MigrationHistory.create(version="20260728124600", name="create_posts", status="DOWN")
    
    applied = get_applied_migrations(db)
    assert len(applied) == 1
    assert applied[0].version == "20260728124500"

def test_get_current_version(db):
    assert get_current_version(db) is None
    
    MigrationHistory.create(version="20260728124500", name="create_users", status="UP")
    assert get_current_version(db) == "20260728124500"
    
    MigrationHistory.create(version="20260728124600", name="create_posts", status="UP")
    assert get_current_version(db) == "20260728124600"
