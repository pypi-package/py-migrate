# CLI Commands

The CLI is built with `Typer` and provides comprehensive tooling for managing your database state.

## Global Flags

These flags can be provided either before or after a subcommand.

- `--env`, `-e`: Set the environment (reads from `pw_migrate.toml`).
- `--database`: Override the Database URL directly.
- `--history-table`: Override the migration history tracking table.

Example:
```bash
pw-migrate up --database "sqlite:///memory.db"
pw-migrate --env prod drop-db
```

## Command Reference

### Database Lifecycle
- `create-db`: Creates the physical database store based on the configured Database URL.
- `drop-db`: Completely drops the database. Requires a Y/N confirmation prompt unless passed with `-f` or `--force`.

### Migration Execution
- `up`: Runs all pending migrations in order.
  - `--steps <N>`: Runs only the next N migrations.
- `down`: Rolls back the last applied migration.
  - `--steps <N>`: Rolls back the last N migrations.
- `rollback <version>`: Rolls back all migrations up to and including the specified version.
- `redo`: Rolls back the last migration and immediately re-runs it (great for local testing).
- `reset`: Rolls back every single applied migration, leaving an empty database.
- `fresh`: Drops the database entirely, recreates it, and runs all migrations. (Faster than `reset`).

### Targeted Operations
- `run <version>`: Ignores sequence tracking and forces a specific migration to run or rollback.
  - `--direction up` (default): Forces the migration to apply.
  - `--direction down`: Forces the migration to rollback.

### Tracking
- `status`: Prints a detailed Rich UI table of every migration ever run, including its execution time, checksum, host, and python version.
- `pending`: Lists all discovered migrations that have not yet been applied.
- `current`: Prints the version identifier of the most recently applied migration.
