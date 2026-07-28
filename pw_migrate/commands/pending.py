from playhouse.db_url import connect
from rich.console import Console
from rich.table import Table

from pw_migrate.core.discovery import discover_migrations
from pw_migrate.core.migration_history import (
    get_applied_migrations,
    setup_history_table,
)

console = Console()


def pending_command(
    migration_dir: str = "migrations", db_url: str = "sqlite:///pw_migrate.db"
) -> None:
    """List pending migrations."""
    db = connect(db_url)
    setup_history_table(db)

    applied_versions = {m.version for m in get_applied_migrations(db)}
    discovered = discover_migrations(migration_dir)

    pending = []
    for filename in discovered:
        version = filename.split("_")[0]
        if version not in applied_versions:
            pending.append(filename)

    if not pending:
        console.print("[green]No pending migrations.[/green]")
        return

    table = Table(title="Pending Migrations")
    table.add_column("Version", style="magenta")
    table.add_column("File", style="green")

    for filename in pending:
        version = filename.split("_")[0]
        table.add_row(version, filename)

    console.print(table)
