import os
import time
import socket
import platform
from peewee import Database
from peewee_migrate.router import Router
from pw_migrate.models.migration_history import MigrationHistory
from pw_migrate.core.migration_history import setup_history_table
from pw_migrate.core.discovery import discover_migrations
from pw_migrate.core.checksum import calculate_checksum
from pw_migrate.core.locking import LockManager
from pw_migrate.exceptions import ChecksumMismatch, MigrationError

class MigratorRunner:
    def __init__(self, db: Database, migrate_dir: str = "migrations"):
        self.db = db
        self.migrate_dir = migrate_dir
        setup_history_table(self.db)
        
        # We use peewee-migrate's Router for executing the actual python file,
        # but we use a distinct table for its internal history so it doesn't conflict
        # with our richer MigrationHistory model.
        self.router = Router(self.db, migrate_dir=self.migrate_dir, migrate_table='peewee_migrate_history')

    def run_up(self, steps: int = None, fake: bool = False) -> list:
        with LockManager(self.db):
            return self._do_run_up(steps, fake)
            
    def _do_run_up(self, steps: int = None, fake: bool = False) -> list:
        applied = MigrationHistory.select().where(MigrationHistory.status == "UP")
        
        # Checksum Validation
        for m in applied:
            filepath = os.path.join(self.migrate_dir, f"{m.version}_{m.name}.py")
            if os.path.exists(filepath):
                current_checksum = calculate_checksum(filepath)
                if m.checksum and m.checksum != current_checksum:
                    raise ChecksumMismatch(f"Migration {m.version}_{m.name}.py has been modified since it was applied!")

        applied_versions = {m.version for m in applied}
        discovered = discover_migrations(self.migrate_dir)
        
        pending = []
        for filename in discovered:
            version = filename.split("_")[0]
            if version not in applied_versions:
                pending.append(filename)
                
        if steps is not None and steps > 0:
            pending = pending[:steps]
            
        executed = []
        for filename in pending:
            version = filename.split("_")[0]
            name = "_".join(filename.split("_")[1:]).replace(".py", "")
            migration_name = filename.replace(".py", "")
            
            start_time = time.time()
            if not fake:
                self.router.run(migration_name)
            
            exec_time = int((time.time() - start_time) * 1000)
            
            filepath = os.path.join(self.migrate_dir, filename)
            file_checksum = calculate_checksum(filepath)
            
            MigrationHistory.create(
                version=version,
                name=name,
                checksum=file_checksum,
                status="UP",
                execution_time_ms=exec_time,
                hostname=socket.gethostname(),
                python_version=platform.python_version()
            )
            executed.append(filename)
            
        return executed

    def run_down(self, steps: int = 1, fake: bool = False) -> list:
        with LockManager(self.db):
            applied = MigrationHistory.select().where(MigrationHistory.status == "UP").order_by(MigrationHistory.version.desc())
            to_rollback = list(applied)[:steps]
            
            return self._do_rollback(to_rollback, fake)

    def run_rollback(self, version: str, fake: bool = False) -> list:
        with LockManager(self.db):
            m = MigrationHistory.get_or_none(version=version, status="UP")
            if not m:
                raise MigrationError(f"Migration {version} is not applied.")
                
            return self._do_rollback([m], fake)

    def run_reset(self, fake: bool = False) -> list:
        with LockManager(self.db):
            applied = MigrationHistory.select().where(MigrationHistory.status == "UP").order_by(MigrationHistory.version.desc())
            to_rollback = list(applied)
            
            return self._do_rollback(to_rollback, fake)
        
    def _do_rollback(self, to_rollback: list, fake: bool) -> list:
        executed = []
        for m in to_rollback:
            migration_name = f"{m.version}_{m.name}"
            start_time = time.time()
            
            if not fake:
                self.router.run_one(migration_name, self.router.migrator, fake=False, downgrade=True)
                
            m.status = "DOWN"
            m.execution_time_ms = int((time.time() - start_time) * 1000)
            m.save()
            
            executed.append(f"{migration_name}.py")
            
        return executed

    def run_single(self, version: str, direction: str = "up", fake: bool = False) -> str:
        """Run or rollback a single specific migration by version."""
        with LockManager(self.db):
            return self._do_run_single(version, direction, fake)
            
    def _do_run_single(self, version: str, direction: str = "up", fake: bool = False) -> str:
        discovered = discover_migrations(self.migrate_dir)
        target_file = None
        for filename in discovered:
            if filename.startswith(version):
                target_file = filename
                break
                
        if not target_file:
            raise MigrationError(f"Migration version {version} not found.")
            
        migration_name = target_file.replace(".py", "")
        name = "_".join(target_file.split("_")[1:]).replace(".py", "")
        
        start_time = time.time()
        
        if direction == "up":
            if MigrationHistory.select().where(MigrationHistory.version == version, MigrationHistory.status == "UP").exists():
                raise MigrationError(f"Migration {version} is already applied.")
                
            if not fake:
                self.router.run(migration_name)
                
            filepath = os.path.join(self.migrate_dir, target_file)
            file_checksum = calculate_checksum(filepath)
                
            MigrationHistory.create(
                version=version,
                name=name,
                checksum=file_checksum,
                status="UP",
                execution_time_ms=int((time.time() - start_time) * 1000),
                hostname=socket.gethostname(),
                python_version=platform.python_version()
            )
        else:
            m = MigrationHistory.get_or_none(version=version, status="UP")
            if not m:
                raise MigrationError(f"Migration {version} is not applied.")
                
            if not fake:
                self.router.run_one(migration_name, self.router.migrator, fake=False, downgrade=True)
                
            m.status = "DOWN"
            m.execution_time_ms = int((time.time() - start_time) * 1000)
            m.save()
            
        return target_file
