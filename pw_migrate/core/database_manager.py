import os

from playhouse.db_url import parse

from pw_migrate.exceptions import MigrationError


class DatabaseManager:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def _get_postgres_conn(self, parsed):
        import psycopg2

        # Connect to 'postgres' maintenance db
        conn = psycopg2.connect(
            dbname="postgres",
            user=parsed.get("user"),
            password=parsed.get("password"),
            host=parsed.get("host", "localhost"),
            port=parsed.get("port", 5432),
        )
        conn.autocommit = True
        return conn

    def _get_mysql_conn(self, parsed):
        import pymysql

        conn = pymysql.connect(
            user=parsed.get("user"),
            password=parsed.get("password"),
            host=parsed.get("host", "localhost"),
            port=parsed.get("port", 3306),
        )
        conn.autocommit(True)
        return conn

    def create_database(self) -> None:
        if self.db_url.startswith("sqlite"):
            db_path = self.db_url.replace("sqlite:///", "")
            if db_path == ":memory:":
                return
            if not os.path.exists(db_path):
                open(db_path, "a").close()
            else:
                raise MigrationError("Database already exists.")
        else:
            parsed = parse(self.db_url)
            db_name = parsed.get("database")

            if self.db_url.startswith("postgres"):
                conn = self._get_postgres_conn(parsed)
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(f"CREATE DATABASE {db_name}")
                except Exception as e:
                    raise MigrationError(f"Could not create database: {e}")
                finally:
                    conn.close()
            elif self.db_url.startswith("mysql"):
                conn = self._get_mysql_conn(parsed)
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(f"CREATE DATABASE {db_name}")
                except Exception as e:
                    raise MigrationError(f"Could not create database: {e}")
                finally:
                    conn.close()
            else:
                raise NotImplementedError(
                    "Database creation for this URL is not supported yet."
                )

    def drop_database(self) -> None:
        if self.db_url.startswith("sqlite"):
            db_path = self.db_url.replace("sqlite:///", "")
            if db_path == ":memory:":
                return
            if os.path.exists(db_path):
                os.remove(db_path)
            else:
                raise MigrationError("Database does not exist.")
        else:
            parsed = parse(self.db_url)
            db_name = parsed.get("database")

            if self.db_url.startswith("postgres"):
                conn = self._get_postgres_conn(parsed)
                try:
                    with conn.cursor() as cursor:
                        # Terminate connections first so drop doesn't fail
                        cursor.execute(
                            f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{db_name}' AND pid <> pg_backend_pid();"
                        )
                        cursor.execute(f"DROP DATABASE {db_name}")
                except Exception as e:
                    raise MigrationError(f"Could not drop database: {e}")
                finally:
                    conn.close()
            elif self.db_url.startswith("mysql"):
                conn = self._get_mysql_conn(parsed)
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(f"DROP DATABASE {db_name}")
                except Exception as e:
                    raise MigrationError(f"Could not drop database: {e}")
                finally:
                    conn.close()
            else:
                raise NotImplementedError(
                    "Database deletion for this URL is not supported yet."
                )
