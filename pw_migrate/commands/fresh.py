from rich.console import Console

from pw_migrate.commands.up import up_command
from pw_migrate.core.database_manager import DatabaseManager
from pw_migrate.exceptions import MigrationError

console = Console()


def fresh_command(
    migration_dir: str = "migrations",
    db_url: str = "sqlite:///pw_migrate.db",
    fake: bool = False,
) -> None:
    """Drop/Reset database and run all migrations."""
    console.print("[blue]Dropping database...[/blue]")
    manager = DatabaseManager(db_url)
    try:
        manager.drop_database()
    except (MigrationError, NotImplementedError) as e:
        console.print(f"[yellow]Could not drop DB: {e}[/yellow]")

    console.print("[blue]Creating database...[/blue]")
    try:
        manager.create_database()
    except (MigrationError, NotImplementedError) as e:
        console.print(f"[yellow]Could not create DB: {e}[/yellow]")

    console.print("[blue]Running all migrations...[/blue]")
    up_command(migration_dir=migration_dir, db_url=db_url, fake=fake)
