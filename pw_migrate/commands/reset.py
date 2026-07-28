import typer
from rich.console import Console
from peewee import SqliteDatabase
from pw_migrate.core.runner import MigratorRunner

console = Console()

def reset_command(
    migration_dir: str = "migrations", 
    db_url: str = "sqlite:///pw_migrate.db",
    fake: bool = False
) -> None:
    """Rollback everything."""
    db = SqliteDatabase(db_url.replace("sqlite:///", ""))
    runner = MigratorRunner(db, migrate_dir=migration_dir)
    
    console.print("[blue]Resetting all migrations...[/blue]")
    executed = runner.run_reset(fake=fake)
    
    if not executed:
        console.print("[green]Database is already empty (no migrations applied).[/green]")
        return
        
    for filename in executed:
        console.print(f"  [yellow]✓ Reverted[/yellow] {filename}")
        
    console.print(f"[bold green]Successfully reverted all {len(executed)} migrations.[/bold green]")
