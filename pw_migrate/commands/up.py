import typer
from rich.console import Console
from playhouse.db_url import connect
from pw_migrate.core.runner import MigratorRunner

console = Console()

def up_command(
    version: str = None,
    migration_dir: str = "migrations", 
    db_url: str = "sqlite:///pw_migrate.db",
    steps: int = None,
    fake: bool = False
) -> None:
    """Run pending migrations or a specific migration."""
    db = connect(db_url)
    runner = MigratorRunner(db, migrate_dir=migration_dir)
    
    if version:
        console.print(f"[blue]Starting specific migration {version}...[/blue]")
        try:
            executed_file = runner.run_single(version=version, direction="up", fake=fake)
            console.print(f"  [green]✓ Applied[/green] {executed_file}")
            console.print("[bold green]Successfully applied 1 migration.[/bold green]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            import typer
            raise typer.Exit(code=1)
    else:
        console.print("[blue]Starting migrations...[/blue]")
        executed = runner.run_up(steps=steps, fake=fake)
        
        if not executed:
            console.print("[green]No pending migrations to run.[/green]")
            return
            
        for filename in executed:
            console.print(f"  [green]✓ Applied[/green] {filename}")
            
        console.print(f"[bold green]Successfully applied {len(executed)} migrations.[/bold green]")
