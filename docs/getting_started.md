# Getting Started with pw-migrate

`pw-migrate` is a comprehensive migration framework for Peewee ORM.

## Installation

Install using pip:
```bash
pip install pw-migrate
```

## Initialization

Run the init command to set up your environment:
```bash
pw-migrate init
```
This will ensure your project is ready for migrations.

## Basic Workflow

1. **Create the Database:**
```bash
pw-migrate create-db
```

2. **Generate your first migration:**
```bash
pw-migrate create initial_schema
```
This creates a file in the `migrations/` folder (e.g., `migrations/20260728120000_initial_schema.py`).

3. **Write your migration:**
Open the generated file and write your Peewee schema changes. You can write raw SQL or use the `peewee_migrate` migrator object provided.

4. **Run the migration:**
```bash
pw-migrate up
```

## Next Steps
- Learn about configuring multiple environments in [configuration.md](configuration.md).
- Discover all available commands in [commands.md](commands.md).
