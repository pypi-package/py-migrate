# Database Seeding

Seeding allows you to populate your database with initial required data (such as default roles, an initial admin user, or mock data for local testing).

## How It Works

1. Create a folder named `seeds/` in your project root.
2. Inside `seeds/`, create Python scripts. They will be executed in alphabetical order, so it's best to prefix them with numbers (e.g., `01_...`, `02_...`).
3. Each script must contain a `def seed(db):` function.
4. `pw-migrate seed` will dynamically load and execute these functions sequentially.

## Example

**`seeds/01_roles.py`**:
```python
def seed(db):
    # You can run raw SQL queries against the database object
    db.execute_sql("INSERT INTO roles (name) VALUES ('admin'), ('editor'), ('user');")
```

**`seeds/02_admin_user.py`**:
```python
# You can also import your Peewee Models to use the ORM directly!
from my_app.models import User, Role

def seed(db):
    admin_role = Role.get(Role.name == 'admin')
    User.create(username="superadmin", role=admin_role)
```

## Running Seeds

To run all seeds:
```bash
pw-migrate seed
```

You can combine this with environment flags to seed specific environments:
```bash
pw-migrate --env staging seed
```
