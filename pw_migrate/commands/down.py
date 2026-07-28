import typer
from rich.console import Console
from playhouse.db_url import connect
from pw_migrate.core.runner import MigratorRunner

console = Console()

def down_command(
    migration_dir: str = "migrations", 
    db_url: str = "sqlite:///pw_migrate.db",
    steps: int = 1,
    fake: bool = False
) -> None:
    """Rollback the latest migrations."""
    db = connect(db_url)
    runner = MigratorRunner(db, migrate_dir=migration_dir)
    
    console.print(f"[blue]Rolling back {steps} migration(s)...[/blue]")
    executed = runner.run_down(steps=steps, fake=fake)
    
    if not executed:
        console.print("[green]No migrations to rollback.[/green]")
        return
        
    for filename in executed:
        console.print(f"  [yellow]✓ Reverted[/yellow] {filename}")
        
    console.print(f"[bold green]Successfully reverted {len(executed)} migrations.[/bold green]")
