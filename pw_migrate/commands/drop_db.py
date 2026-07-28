import typer
from rich.console import Console

from pw_migrate.core.database_manager import DatabaseManager
from pw_migrate.exceptions import MigrationError

console = Console()


def drop_db_command(
    db_url: str = "sqlite:///pw_migrate.db", force: bool = False
) -> None:
    """Drop the database."""
    if not force:
        confirm = typer.confirm(
            f"Are you sure you want to drop the database at {db_url}?"
        )
        if not confirm:
            console.print("[yellow]Aborted.[/yellow]")
            return

    manager = DatabaseManager(db_url)
    try:
        manager.drop_database()
        console.print(
            f"[bold green]Successfully dropped database at {db_url}[/bold green]"
        )
    except MigrationError as e:
        console.print(f"[yellow]{e}[/yellow]")
    except NotImplementedError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)
