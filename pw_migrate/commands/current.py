from playhouse.db_url import connect
from rich.console import Console

from pw_migrate.core.migration_history import get_current_version, setup_history_table

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
