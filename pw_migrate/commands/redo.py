from pw_migrate.commands.down import down_command
from pw_migrate.commands.up import up_command


def redo_command(
    migration_dir: str = "migrations",
    db_url: str = "sqlite:///pw_migrate.db",
    fake: bool = False,
) -> None:
    """Rollback then rerun the latest migration."""
    down_command(migration_dir=migration_dir, db_url=db_url, steps=1, fake=fake)
    up_command(migration_dir=migration_dir, db_url=db_url, steps=1, fake=fake)
