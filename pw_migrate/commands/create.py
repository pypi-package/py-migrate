import os
import datetime
import typer
from rich.console import Console

console = Console()

def create_command(name: str, migration_dir: str = "migrations") -> None:
    """Create a new migration file scaffold."""
    if not os.path.exists(migration_dir):
        os.makedirs(migration_dir)
        
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "migration.py.tpl")
    
    with open(template_path, "r") as f:
        template_content = f.read()
        
    template = template_content.replace("{name}", name)
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{name}.py"
    filepath = os.path.join(migration_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(template)
        
    console.print(f"[bold green]Created migration:[/bold green] {filepath}")
