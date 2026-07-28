import typer
from rich.console import Console
from peewee import SqliteDatabase
from pw_migrate.core.seeder import Seeder
from pw_migrate.exceptions import MigrationError

console = Console()

def seed_command(
    seeds_dir: str = "seeds", 
    db_url: str = "sqlite:///pw_migrate.db",
) -> None:
    """Run database seeders."""
    db = SqliteDatabase(db_url.replace("sqlite:///", ""))
    seeder = Seeder(db, seeds_dir=seeds_dir)
    
    console.print("[blue]Starting database seeder...[/blue]")
    try:
        executed = seeder.run_all()
    except MigrationError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
        
    if not executed:
        console.print("[green]No seeds found to run.[/green]")
        return
        
    for filename in executed:
        console.print(f"  [green]✓ Seeded[/green] {filename}")
        
    console.print(f"[bold green]Successfully ran {len(executed)} seeders.[/bold green]")
