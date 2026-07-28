# Basic Example

This folder demonstrates a fully working example of `pw-migrate`.

## Getting Started

1. Navigate into this directory:
```bash
cd examples/basic
```

2. Look at `pw_migrate.toml`. It defines the database as `local.db`.

3. Create the database:
```bash
pw-migrate create-db
```

4. Run the migrations defined in `migrations/001_initial.py`:
```bash
pw-migrate up
```

5. Check the status of your migrations:
```bash
pw-migrate status
```

6. Seed the database with the initial roles defined in `seeds/01_roles.py`:
```bash
pw-migrate seed
```

## Environment Testing

Try running a targeted environment override using the `staging` environment defined in the `.toml` file!

```bash
pw-migrate --env staging create-db
pw-migrate --env staging up
pw-migrate --env staging status
```
