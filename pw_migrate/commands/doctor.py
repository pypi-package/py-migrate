import typer
from rich.console import Console
from rich.table import Table
from playhouse.db_url import connect
from pw_migrate.core.doctor import Doctor

console = Console()

def doctor_command(
    migrate_dir: str = "migrations", 
    db_url: str = "sqlite:///pw_migrate.db",
) -> None:
    """Run diagnostic checks on the migration environment."""
    db = connect(db_url)
    doctor = Doctor(db, migrate_dir=migrate_dir)
    
    console.print("[blue]Running Diagnostics...[/blue]\n")
    
    results = doctor.run_all()
    
    table = Table(title="Diagnostic Report", show_header=True, header_style="bold magenta")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Message")
    
    has_errors = False
    
    for name, success, message in results:
        status_icon = "[green]✓[/green]" if success else "[red]✗[/red]"
        msg_style = "green" if success else "red"
        
        table.add_row(name, status_icon, f"[{msg_style}]{message}[/{msg_style}]")
        
        if not success:
            has_errors = True
            
    console.print(table)
    
    if has_errors:
        console.print("\n[bold red]Doctor found critical issues that require manual intervention![/bold red]")
        raise typer.Exit(code=1)
    else:
        console.print("\n[bold green]Environment is perfectly healthy![/bold green]")
