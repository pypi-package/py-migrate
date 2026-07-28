import typer
from rich.console import Console
from playhouse.db_url import connect
from pw_migrate.core.migration_history import setup_history_table, get_current_version

console = Console()

def current_command(db_url: str = "sqlite:///pw_migrate.db") -> None:
    """Show the current database version."""
    db = connect(db_url)
    setup_history_table(db)
    
    version = get_current_version(db)
    if version:
        console.print(f"Current Version: [bold magenta]{version}[/bold magenta]")
    else:
        console.print("Current Version: [yellow]None[/yellow]")
