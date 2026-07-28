from peewee import Database

from pw_migrate.config import load_config
from pw_migrate.models.migration_history import MigrationHistory


def setup_history_table(db: Database, table_name: str = None) -> None:
    """Ensure the history table exists in the given database."""
    if table_name is None:
        import os

        if "PW_MIGRATE_HISTORY_TABLE" in os.environ:
            table_name = os.environ["PW_MIGRATE_HISTORY_TABLE"]
        elif "PEEWEE_MIGRATION_TABLE" in os.environ:
            table_name = os.environ["PEEWEE_MIGRATION_TABLE"]
        else:
            config = load_config()
            table_name = config.get("history_table", "_pw_migrate_internal")

    MigrationHistory._meta.database = db
    MigrationHistory._meta.table_name = table_name

    try:
        db.create_tables([MigrationHistory], safe=True)
    except Exception as e:
        import typer
        from rich.console import Console

        Console().print(f"[bold red]Database connection failed:[/bold red] {e}")
        Console().print(
            "[yellow]Hint: Ensure the database server is running and the database exists. You can create it using 'pw-migrate create-db'.[/yellow]"
        )
        raise typer.Exit(code=1)


def get_applied_migrations(db: Database) -> list[MigrationHistory]:
    """Get all migrations that have been applied (status='UP')."""
    MigrationHistory._meta.database = db
    return list(
        MigrationHistory.select()
        .where(MigrationHistory.status == "UP")
        .order_by(MigrationHistory.version)
    )


def get_current_version(db: Database) -> str | None:
    """Get the version of the most recently applied migration."""
    MigrationHistory._meta.database = db
    latest = (
        MigrationHistory.select()
        .where(MigrationHistory.status == "UP")
        .order_by(MigrationHistory.version.desc())
        .first()
    )
    return latest.version if latest else None
