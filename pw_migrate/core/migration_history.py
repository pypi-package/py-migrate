from typing import List, Optional
from peewee import Database
from pw_migrate.models.migration_history import MigrationHistory
from pw_migrate.config import load_config

def setup_history_table(db: Database, table_name: str = None) -> None:
    """Ensure the history table exists in the given database."""
    if table_name is None:
        import os
        if "PW_MIGRATE_HISTORY_TABLE" in os.environ:
            table_name = os.environ["PW_MIGRATE_HISTORY_TABLE"]
        else:
            config = load_config()
            table_name = config.get("history_table", "migration_history")
        
    MigrationHistory._meta.database = db
    MigrationHistory._meta.table_name = table_name
    db.create_tables([MigrationHistory], safe=True)

def get_applied_migrations(db: Database) -> List[MigrationHistory]:
    """Get all migrations that have been applied (status='UP')."""
    MigrationHistory._meta.database = db
    return list(
        MigrationHistory.select()
        .where(MigrationHistory.status == "UP")
        .order_by(MigrationHistory.version)
    )

def get_current_version(db: Database) -> Optional[str]:
    """Get the version of the most recently applied migration."""
    MigrationHistory._meta.database = db
    latest = (
        MigrationHistory.select()
        .where(MigrationHistory.status == "UP")
        .order_by(MigrationHistory.version.desc())
        .first()
    )
    return latest.version if latest else None
