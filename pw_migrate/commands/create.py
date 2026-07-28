import os
import datetime
import typer
from rich.console import Console

console = Console()

TEMPLATE = '''def migrate(migrator, database, fake=False):
    pass

def rollback(migrator, database, fake=False):
    pass
'''

def create_command(name: str, migration_dir: str = "migrations") -> None:
    """Create a new migration file scaffold."""
    if not os.path.exists(migration_dir):
        os.makedirs(migration_dir)
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{name}.py"
    filepath = os.path.join(migration_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(TEMPLATE)
        
    console.print(f"[bold green]Created migration:[/bold green] {filepath}")
