from playhouse.db_url import connect
from rich.console import Console

from pw_migrate.core.runner import MigratorRunner

console = Console()


def rollback_command(
    version: str,
    migration_dir: str = "migrations",
    db_url: str = "sqlite:///pw_migrate.db",
    fake: bool = False,
) -> None:
    """Rollback to a specific version."""
    db = connect(db_url)
    runner = MigratorRunner(db, migrate_dir=migration_dir)

    console.print(f"[blue]Rolling back to version {version}...[/blue]")
    executed = runner.run_rollback(version=version, fake=fake)

    if not executed:
        console.print(
            "[green]No migrations to rollback (or version not applied).[/green]"
        )
        return

    for filename in executed:
        console.print(f"  [yellow]✓ Reverted[/yellow] {filename}")

    console.print(
        f"[bold green]Successfully reverted {len(executed)} migrations.[/bold green]"
    )
