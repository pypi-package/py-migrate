import typer
from rich.console import Console
from peewee import SqliteDatabase
from pw_migrate.core.runner import MigratorRunner
from pw_migrate.exceptions import MigrationError

console = Console()

def run_command(
    version: str,
    direction: str = "up",
    migration_dir: str = "migrations", 
    db_url: str = "sqlite:///pw_migrate.db",
    fake: bool = False
) -> None:
    """Force run or rollback a single specific migration."""
    if direction not in ("up", "down"):
        console.print("[red]Direction must be 'up' or 'down'[/red]")
        raise typer.Exit(code=1)
        
    db = SqliteDatabase(db_url.replace("sqlite:///", ""))
    runner = MigratorRunner(db, migrate_dir=migration_dir)
    
    action_text = "Running" if direction == "up" else "Rolling back"
    console.print(f"[blue]{action_text} single migration {version}...[/blue]")
    
    try:
        executed_file = runner.run_single(version=version, direction=direction, fake=fake)
        console.print(f"  [green]✓ {action_text} successful:[/green] {executed_file}")
    except MigrationError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
