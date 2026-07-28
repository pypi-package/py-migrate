# pw-migrate

A production-grade migration framework for Peewee ORM.

[![PyPI version](https://badge.fury.io/py/pw-migrate.svg)](https://badge.fury.io/py/pw-migrate)
[![Python versions](https://img.shields.io/pypi/pyversions/pw-migrate.svg)](https://pypi.org/project/pw-migrate/)

`pw-migrate` brings robust, framework-agnostic database migrations to Peewee. It provides comprehensive tooling for managing your database state, tracking migration history, ensuring integrity with SHA256 checksums, and supporting multi-environment configurations seamlessly.

---

## 🚀 Features

- **Integrity First:** SHA256 checksums prevent tampered migrations from being run.
- **Comprehensive CLI:** `up`, `down`, `rollback`, `redo`, `reset`, `fresh`, `create-db`, `drop-db`, `seed`.
- **Targeted Execution:** Force run or rollback specific single migrations seamlessly.
- **Environment Support:** Define configuration overlays for `dev`, `staging`, `prod`.
- **Database Management:** Automate creating and dropping database instances right from the CLI.
- **Database Seeding:** Built-in Python-based data seeding system.

---

## 📦 Installation

Install the package via pip:

```bash
pip install pw-migrate
```

Initialize your project to generate the `migrations/` directory:

```bash
pw-migrate init
```

---

## ⚙️ Configuration

Create a `pw_migrate.toml` in your project root to configure your database connection and environment overlays:

```toml
# Default configuration
database = "sqlite:///dev.db"
history_table = "dev_migration_history"

# Environment specific configuration (pw-migrate --env prod)
[envs.prod]
database = "postgres://user:pass@localhost/prod"
history_table = "prod_migration_history"
```

### Environment Variables

If you are deploying via Docker or CI/CD pipelines, you can skip the configuration file and configure `pw-migrate` entirely via native environment variables.

The following variables are checked automatically if their respective CLI flags are omitted:
- `DATABASE_URL`: Defines the database connection string.
- `PEEWEE_MIGRATION_TABLE`: Overrides the table name used for tracking applied migrations (default: `migration_history`).
- `PW_MIGRATE_ENV`: Automatically sets the target environment block to load from your `.toml` file.

---

## 🛠 Quick Start

### 1. Create the Database
```bash
pw-migrate create-db
```

### 2. Generate a Migration
```bash
pw-migrate create add_users_table
```
This generates a scaffold file (e.g., `migrations/20260728120000_add_users_table.py`). Open it and write your Peewee schema changes.

### 3. Run Migrations
```bash
pw-migrate up            # Run all pending migrations
pw-migrate up --steps 2  # Run only the next 2 pending migrations
pw-migrate down          # Rollback the last applied migration
pw-migrate reset         # Rollback all applied migrations
```

---

## 📚 Advanced Usage

### Global CLI Overrides
You can explicitly target an environment or override settings on the fly for *any* command:

```bash
pw-migrate --env prod up
pw-migrate --database "sqlite:///custom.db" status
pw-migrate up --database "sqlite:///custom.db"
```

### Targeted Execution
Force run a specific migration file (ignoring normal execution order):
```bash
pw-migrate run 20260728120000 --direction up
```

### Database Seeding
Populate your database with initial data using the `seed` command. Create Python scripts in a `seeds/` folder with a `seed(db)` function:

```python
# seeds/01_roles.py
def seed(db):
    db.execute_sql("INSERT INTO roles (name) VALUES ('admin'), ('user')")
```

Run them sequentially:
```bash
pw-migrate seed
```

---

## 📖 Detailed Documentation

For a deep dive into the framework's architecture and usage, please check out the [documentation](docs/).
