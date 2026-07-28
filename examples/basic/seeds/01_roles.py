def seed(db):
    print("Seeding roles...")
    db.execute_sql(
        "INSERT OR IGNORE INTO roles (name) VALUES ('admin'), ('editor'), ('user');"
    )

    print("Seeding users...")
    db.execute_sql(
        "INSERT OR IGNORE INTO users (username, role_id) VALUES ('superadmin', 1);"
    )
