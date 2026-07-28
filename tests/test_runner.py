import pytest
import os
from peewee import SqliteDatabase
from pw_migrate.core.runner import MigratorRunner
from pw_migrate.core.migration_history import setup_history_table, get_applied_migrations

def test_migrator_runner(tmp_path):
    mig_dir = tmp_path / "migrations"
    mig_dir.mkdir()
    
    mig_file = mig_dir / "20260728124500_create_users.py"
    mig_file.write_text('''
def migrate(migrator, database, fake=False):
    pass

def rollback(migrator, database, fake=False):
    pass
''')
    
    db = SqliteDatabase(":memory:")
    runner = MigratorRunner(db, migrate_dir=str(mig_dir))
    
    executed = runner.run_up(fake=True)
    assert len(executed) == 1
    assert executed[0] == "20260728124500_create_users.py"
    
    applied = get_applied_migrations(db)
    assert len(applied) == 1
    assert applied[0].version == "20260728124500"
    
    # Run again should be 0
    executed2 = runner.run_up(fake=True)
    assert len(executed2) == 0
