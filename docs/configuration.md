# Configuration (`pw_migrate.toml`)

`pw-migrate` uses a TOML file for configuration, allowing you to seamlessly manage databases across multiple environments (e.g., development, staging, production).

## Basic Setup

Create `pw_migrate.toml` in your project root:

```toml
database = "sqlite:///dev.db"
history_table = "_pw_migrate_internal"
```

## Environment Overlays

You can define specific overlays for different environments using `[envs.<env_name>]` blocks. These blocks override the root keys when that environment is active.

```toml
database = "sqlite:///dev.db"
history_table = "dev_migration_history"

[envs.staging]
database = "postgres://user:pass@staging-db.com/staging"
history_table = "staging_migration_history"

[envs.prod]
database = "postgres://user:pass@prod-db.com/prod"
history_table = "prod_migration_history"
```

## Using Environments

To activate an environment, use the global `--env` flag (or `-e`):

```bash
pw-migrate --env prod up
pw-migrate -e staging status
```

This dynamically maps the `database` and `history_table` to the ones defined in the `[envs.<env>]` block.
