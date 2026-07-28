import sys
from dotenv import load_dotenv
import typer
from rich.console import Console

# Load environment variables from .env file automatically
load_dotenv()

app = typer.Typer(
    help="Migration Framework for Peewee ORM",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help", "help"]}
)

from pw_migrate.commands.status import status_command
from pw_migrate.commands.pending import pending_command
from pw_migrate.commands.current import current_command
from pw_migrate.commands.up import up_command
from pw_migrate.commands.down import down_command
from pw_migrate.commands.rollback import rollback_command
from pw_migrate.commands.redo import redo_command
from pw_migrate.commands.reset import reset_command
from pw_migrate.commands.fresh import fresh_command
from pw_migrate.commands.create import create_command
from pw_migrate.commands.run import run_command
from pw_migrate.commands.create_db import create_db_command
from pw_migrate.commands.drop_db import drop_db_command
from pw_migrate.commands.seed import seed_command
from pw_migrate.commands.doctor import doctor_command
from pw_migrate.commands.init import init_command
from pw_migrate.config import load_config

@app.command()
def init() -> None:
    """Initialize the migration environment."""
    typer.echo("Initialized pw-migrate environment.")

def _set_history_table(history_table: str):
    if history_table:
        import os
        os.environ["PW_MIGRATE_HISTORY_TABLE"] = history_table

def _get_db_url(db_url: str) -> str:
    if db_url:
        return db_url
    import os
    if "PW_MIGRATE_DATABASE" in os.environ:
        return os.environ["PW_MIGRATE_DATABASE"]
    if "DATABASE_URL" in os.environ:
        return os.environ["DATABASE_URL"]
    config = load_config()
    return config.get("database", "sqlite:///pw_migrate.db")

@app.command("create-db")
def create_db(history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
              db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Create the database."""
    _set_history_table(history_table)
    create_db_command(db_url=_get_db_url(db_url))

@app.command("drop-db")
def drop_db(force: bool = typer.Option(False, "--force", "-f", help="Force drop without confirmation"),
            history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
            db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Drop the database."""
    _set_history_table(history_table)
    drop_db_command(force=force, db_url=_get_db_url(db_url))

@app.command()
def run(version: str = typer.Argument(..., help="Version of the migration"),
        direction: str = typer.Option("up", help="Direction: 'up' or 'down'"),
        fake: bool = typer.Option(False, help="Fake the execution"),
        history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
        db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Force run or rollback a single specific migration."""
    _set_history_table(history_table)
    run_command(version=version, direction=direction, fake=fake, db_url=_get_db_url(db_url))

@app.command()
def init() -> None:
    """Initialize the migration environment."""
    init_command()

@app.command()
def create(name: str = typer.Argument(..., help="Name of the migration (e.g., add_users_table)")) -> None:
    """Create a new migration file scaffold."""
    create_command(name=name)

@app.command()
def seed(history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
         db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Run database seeders."""
    _set_history_table(history_table)
    seed_command(db_url=_get_db_url(db_url))

@app.command()
def doctor(history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
           db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Diagnose migration state and history integrity."""
    _set_history_table(history_table)
    doctor_command(db_url=_get_db_url(db_url))

@app.command()
def up(steps: int = typer.Option(None, help="Number of migrations to run"),
       fake: bool = typer.Option(False, help="Fake the execution"),
       history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
       db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Run pending migrations."""
    _set_history_table(history_table)
    up_command(steps=steps, fake=fake, db_url=_get_db_url(db_url))

@app.command()
def down(steps: int = typer.Option(1, help="Number of migrations to rollback"),
         fake: bool = typer.Option(False, help="Fake the execution"),
         history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
         db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Rollback the latest migrations."""
    _set_history_table(history_table)
    down_command(steps=steps, fake=fake, db_url=_get_db_url(db_url))

@app.command()
def rollback(version: str = typer.Argument(..., help="Version to rollback to"),
             fake: bool = typer.Option(False, help="Fake the execution"),
             history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
             db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Rollback to a specific version."""
    _set_history_table(history_table)
    rollback_command(version=version, fake=fake, db_url=_get_db_url(db_url))

@app.command()
def redo(fake: bool = typer.Option(False, help="Fake the execution"),
         history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
         db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Rollback then rerun the latest migration."""
    _set_history_table(history_table)
    redo_command(fake=fake, db_url=_get_db_url(db_url))

@app.command()
def reset(fake: bool = typer.Option(False, help="Fake the execution"),
          history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
          db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Rollback everything."""
    _set_history_table(history_table)
    reset_command(fake=fake, db_url=_get_db_url(db_url))

@app.command()
def fresh(fake: bool = typer.Option(False, help="Fake the execution"),
          history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
          db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Drop/Reset database and run all migrations."""
    _set_history_table(history_table)
    fresh_command(fake=fake, db_url=_get_db_url(db_url))

@app.command()
def status(history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
           db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Show the current status of all migrations."""
    _set_history_table(history_table)
    status_command(db_url=_get_db_url(db_url))

@app.command()
def pending(history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
            db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """List pending migrations."""
    _set_history_table(history_table)
    pending_command(db_url=_get_db_url(db_url))

@app.command()
def current(history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
            db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)")) -> None:
    """Show the current database version."""
    _set_history_table(history_table)
    current_command(db_url=_get_db_url(db_url))

@app.command()
def version() -> None:
    """Show the current version."""
    from pw_migrate import __version__
    typer.echo(f"pw-migrate version {__version__}")

@app.command()
def help(ctx: typer.Context) -> None:
    """Show the help message."""
    typer.echo(ctx.parent.get_help())

@app.callback()
def main(
    history_table: str = typer.Option(None, "--history-table", help="Override history table name (Fallback: PEEWEE_MIGRATION_TABLE env)"),
    db_url: str = typer.Option(None, "--database", help="Override database URL (Fallback: DATABASE_URL env)"),
    env: str = typer.Option(None, "--env", "-e", help="Set the environment (Fallback: PW_MIGRATE_ENV env)")
) -> None:
    """Migration Framework for Peewee ORM."""
    if history_table:
        import os
        os.environ["PW_MIGRATE_HISTORY_TABLE"] = history_table
    if db_url:
        import os
        os.environ["PW_MIGRATE_DATABASE"] = db_url
    if env:
        import os
        os.environ["PW_MIGRATE_ENV"] = env

if __name__ == "__main__":
    main()
