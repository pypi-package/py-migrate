import os
import socket
import datetime
from peewee import Database
from pw_migrate.models.migration_lock import MigrationLock
from pw_migrate.config import load_config
from pw_migrate.exceptions import MigrationLocked

class LockManager:
    def __init__(self, db: Database, lock_table: str = None):
        self.db = db
        if lock_table is None:
            config = load_config()
            lock_table = config.get("lock_table", "migration_lock")
            
        MigrationLock._meta.database = db
        MigrationLock._meta.table_name = lock_table
        db.create_tables([MigrationLock], safe=True)
        
    def __enter__(self):
        lock, created = MigrationLock.get_or_create(id=1, defaults={'is_locked': False})
        
        with self.db.atomic():
            lock = MigrationLock.get_by_id(1)
            if lock.is_locked:
                raise MigrationLocked(f"Database is currently locked by {lock.locked_by} (PID: {lock.pid}) since {lock.locked_at}")
                
            lock.is_locked = True
            lock.locked_at = datetime.datetime.now()
            lock.locked_by = socket.gethostname()
            lock.pid = os.getpid()
            lock.save()
            
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            with self.db.atomic():
                lock = MigrationLock.get_by_id(1)
                lock.is_locked = False
                lock.locked_at = None
                lock.locked_by = None
                lock.pid = None
                lock.save()
        except Exception:
            pass # Best effort release
