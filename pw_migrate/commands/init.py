import os

from rich.console import Console

console = Console()


def init_command():
    """Initialize the migration environment."""
    console.print("[blue]Initializing pw-migrate environment...[/blue]\n")

    # 1. Create migrations/
    if not os.path.exists("migrations"):
        os.makedirs("migrations")
        console.print("  [green]✓ Created[/green] migrations/ directory")
    else:
        console.print(
            "  [yellow]- Skipped[/yellow] migrations/ directory (already exists)"
        )

    # 2. Create seeds/
    if not os.path.exists("seeds"):
        os.makedirs("seeds")
        console.print("  [green]✓ Created[/green] seeds/ directory")
    else:
        console.print("  [yellow]- Skipped[/yellow] seeds/ directory (already exists)")

    # 3. Create pw_migrate.toml
    if not os.path.exists("pw_migrate.toml"):
        with open("pw_migrate.toml", "w") as f:
            f.write(
                'database = "sqlite:///local.db"\nhistory_table = "_pw_migrate_internal"\n'
            )
        console.print("  [green]✓ Created[/green] pw_migrate.toml")
    else:
        console.print("  [yellow]- Skipped[/yellow] pw_migrate.toml (already exists)")

    # 4. Create .env.example
    if not os.path.exists(".env.example"):
        with open(".env.example", "w") as f:
            f.write(
                "DATABASE_URL=sqlite:///local.db\nPEEWEE_MIGRATION_TABLE=_pw_migrate_internal\n"
            )
        console.print("  [green]✓ Created[/green] .env.example")
    else:
        console.print("  [yellow]- Skipped[/yellow] .env.example (already exists)")

    # 5. Update .gitignore
    gitignore_additions = "\n# pw-migrate\n/migrations\n/seeds\npw_migrate.toml\n*.db\n"
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            content = f.read()
        if "/migrations" not in content and "migrations/" not in content:
            with open(".gitignore", "a") as f:
                f.write(gitignore_additions)
            console.print("  [green]✓ Updated[/green] .gitignore")
        else:
            console.print(
                "  [yellow]- Skipped[/yellow] .gitignore (rules already exist)"
            )
    else:
        with open(".gitignore", "w") as f:
            f.write(gitignore_additions)
        console.print("  [green]✓ Created[/green] .gitignore")

    console.print(
        "\n[bold green]Initialization complete! You are ready to start migrating.[/bold green]"
    )
