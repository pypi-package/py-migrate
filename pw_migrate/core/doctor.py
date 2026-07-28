import os
from peewee import Database
from pw_migrate.models.migration_history import MigrationHistory
from pw_migrate.core.migration_history import setup_history_table
from pw_migrate.core.discovery import discover_migrations
from pw_migrate.core.checksum import calculate_checksum

class Doctor:
    def __init__(self, db: Database, migrate_dir: str = "migrations"):
        self.db = db
        self.migrate_dir = migrate_dir
        setup_history_table(db)
        
    def check_connection(self):
        try:
            self.db.connect(reuse_if_open=True)
            return True, "Database connection successful."
        except Exception as e:
            return False, f"Failed to connect to database: {e}"
            
    def check_history_table(self):
        try:
            count = MigrationHistory.select().count()
            return True, f"Migration history table exists (found {count} records)."
        except Exception as e:
            return False, f"Migration history table error: {e}"
            
    def check_missing_files(self):
        try:
            applied = MigrationHistory.select().where(MigrationHistory.status == "UP")
            missing = []
            for record in applied:
                path = os.path.join(self.migrate_dir, record.name)
                if not os.path.exists(path):
                    missing.append(record.name)
                    
            if missing:
                return False, f"Missing files for applied migrations: {', '.join(missing)}"
            return True, "All applied migrations have corresponding files."
        except Exception as e:
            return False, f"Could not verify missing files: {e}"
            
    def check_checksums(self):
        try:
            applied = MigrationHistory.select().where(MigrationHistory.status == "UP")
            mismatches = []
            for record in applied:
                path = os.path.join(self.migrate_dir, record.name)
                if os.path.exists(path):
                    current_checksum = calculate_checksum(path)
                    if current_checksum != record.checksum:
                        mismatches.append(record.name)
                        
            if mismatches:
                return False, f"Checksum mismatches found for: {', '.join(mismatches)}"
            return True, "All applied migration checksums match."
        except Exception as e:
            return False, f"Could not verify checksums: {e}"
            
    def check_pending(self):
        try:
            discovered = discover_migrations(self.migrate_dir)
            applied = [r.name for r in MigrationHistory.select().where(MigrationHistory.status == "UP")]
            pending = [m for m in discovered if m not in applied]
            return True, f"Found {len(pending)} pending migrations ready to run."
        except Exception as e:
            return False, f"Could not check pending migrations: {e}"
            
    def run_all(self):
        return [
            ("Connectivity", *self.check_connection()),
            ("History Table", *self.check_history_table()),
            ("Missing Files", *self.check_missing_files()),
            ("Checksum Integrity", *self.check_checksums()),
            ("Pending Migrations", *self.check_pending())
        ]
