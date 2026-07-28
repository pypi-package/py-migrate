import typer
from rich.console import Console
from peewee import SqliteDatabase
from pw_migrate.core.runner import MigratorRunner

console = Console()

def up_command(
    migration_dir: str = "migrations", 
    db_url: str = "sqlite:///pw_migrate.db",
    steps: int = None,
    fake: bool = False
) -> None:
    """Run pending migrations."""
    db = SqliteDatabase(db_url.replace("sqlite:///", ""))
    runner = MigratorRunner(db, migrate_dir=migration_dir)
    
    console.print("[blue]Starting migrations...[/blue]")
    executed = runner.run_up(steps=steps, fake=fake)
    
    if not executed:
        console.print("[green]No pending migrations to run.[/green]")
        return
        
    for filename in executed:
        console.print(f"  [green]✓ Applied[/green] {filename}")
        
    console.print(f"[bold green]Successfully applied {len(executed)} migrations.[/bold green]")
