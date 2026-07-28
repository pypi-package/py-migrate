import typer
from rich.console import Console

from pw_migrate.core.database_manager import DatabaseManager
from pw_migrate.exceptions import MigrationError

console = Console()


def create_db_command(db_url: str = "sqlite:///pw_migrate.db") -> None:
    """Create the database."""
    manager = DatabaseManager(db_url)
    try:
        manager.create_database()
        console.print(
            f"[bold green]Successfully created database at {db_url}[/bold green]"
        )
    except MigrationError as e:
        console.print(f"[yellow]{e}[/yellow]")
    except NotImplementedError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)
