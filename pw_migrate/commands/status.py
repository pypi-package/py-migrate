import typer
from rich.console import Console
from rich.table import Table
from peewee import SqliteDatabase
from pw_migrate.core.migration_history import setup_history_table, get_applied_migrations
from pw_migrate.core.discovery import discover_migrations
import os

console = Console()

def status_command(migration_dir: str = "migrations", db_url: str = "sqlite:///pw_migrate.db") -> None:
    """Show the current status of all migrations."""
    db = SqliteDatabase(db_url.replace("sqlite:///", ""))
    setup_history_table(db)
    
    applied = {m.version: m for m in get_applied_migrations(db)}
    discovered = discover_migrations(migration_dir)
    
    table = Table(title="Migration Status")
    table.add_column("Status", style="cyan")
    table.add_column("Version", style="magenta")
    table.add_column("Name", style="green")
    
    for filename in discovered:
        version = filename.split("_")[0]
        name = "_".join(filename.split("_")[1:]).replace(".py", "")
        
        if version in applied:
            status = "[green]✓ UP[/green]"
        else:
            status = "[yellow]✗ DOWN[/yellow]"
            
        table.add_row(status, version, name)
        
    console.print(table)
