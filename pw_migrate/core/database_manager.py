import os
from pw_migrate.exceptions import MigrationError

class DatabaseManager:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def create_database(self) -> None:
        if self.db_url.startswith("sqlite:///"):
            db_path = self.db_url.replace("sqlite:///", "")
            # In memory DB doesn't need physical creation
            if db_path == ":memory:":
                return
            if not os.path.exists(db_path):
                open(db_path, "a").close()
            else:
                raise MigrationError("Database already exists.")
        else:
            raise NotImplementedError("Only SQLite database creation is supported in this version.")

    def drop_database(self) -> None:
        if self.db_url.startswith("sqlite:///"):
            db_path = self.db_url.replace("sqlite:///", "")
            if db_path == ":memory:":
                return
            if os.path.exists(db_path):
                os.remove(db_path)
            else:
                raise MigrationError("Database does not exist.")
        else:
            raise NotImplementedError("Only SQLite database deletion is supported in this version.")
