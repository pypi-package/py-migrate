import os
import pytest
from peewee import SqliteDatabase
from pw_migrate.core.doctor import Doctor
from pw_migrate.models.migration_history import MigrationHistory

def test_doctor_healthy(tmp_path):
    db = SqliteDatabase(':memory:')
    migrate_dir = tmp_path / "migrations"
    migrate_dir.mkdir()
    
    doctor = Doctor(db, str(migrate_dir))
    results = doctor.run_all()
    
    # Check all are successful
    for name, success, message in results:
        assert success is True
        
def test_doctor_missing_file(tmp_path):
    db = SqliteDatabase(':memory:')
    migrate_dir = tmp_path / "migrations"
    migrate_dir.mkdir()
    
    doctor = Doctor(db, str(migrate_dir))
    
    # Fake an applied migration
    MigrationHistory.create(version="123", name="123_fake.py", status="UP", checksum="fake")
    
    results = doctor.run_all()
    missing_files_result = next(r for r in results if r[0] == "Missing Files")
    assert missing_files_result[1] is False
    assert "123_fake.py" in missing_files_result[2]
