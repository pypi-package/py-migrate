import pytest
from peewee import SqliteDatabase
from pw_migrate.core.locking import LockManager
from pw_migrate.models.migration_lock import MigrationLock
from pw_migrate.exceptions import MigrationLocked

def test_lock_manager():
    db = SqliteDatabase(':memory:')
    
    # Test basic acquisition and release
    with LockManager(db):
        lock = MigrationLock.get_by_id(1)
        assert lock.is_locked is True
        assert lock.locked_by is not None
        assert lock.pid is not None
        
    # Test it gets released
    lock = MigrationLock.get_by_id(1)
    assert lock.is_locked is False
    
    # Test concurrent acquisition failure
    with pytest.raises(MigrationLocked):
        with LockManager(db):
            # Try to acquire again while locked
            with LockManager(db):
                pass
