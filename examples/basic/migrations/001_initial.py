def migrate(migrator, database, fake=False, **kwargs):
    migrator.sql("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL UNIQUE
        );
    """)

    migrator.sql("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(255) NOT NULL UNIQUE,
            role_id INTEGER,
            FOREIGN KEY (role_id) REFERENCES roles (id)
        );
    """)


def rollback(migrator, database, fake=False, **kwargs):
    migrator.sql("DROP TABLE users")
    migrator.sql("DROP TABLE roles")
