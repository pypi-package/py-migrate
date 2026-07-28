import importlib.util
import os

from peewee import Database

from pw_migrate.exceptions import MigrationError


class Seeder:
    def __init__(self, db: Database, seeds_dir: str = "seeds"):
        self.db = db
        self.seeds_dir = seeds_dir

    def discover_seeds(self) -> list:
        if not os.path.exists(self.seeds_dir):
            return []
        files = [
            f
            for f in os.listdir(self.seeds_dir)
            if f.endswith(".py") and not f.startswith("__")
        ]
        return sorted(files)

    def run_all(self) -> list:
        seeds = self.discover_seeds()
        if not seeds:
            return []

        executed = []
        for seed_file in seeds:
            seed_path = os.path.join(self.seeds_dir, seed_file)
            seed_name = seed_file.replace(".py", "")

            spec = importlib.util.spec_from_file_location(seed_name, seed_path)
            module = importlib.util.module_from_spec(spec)  # type: ignore

            try:
                spec.loader.exec_module(module)  # type: ignore
            except Exception as e:
                raise MigrationError(f"Failed to load seed {seed_file}: {e}")

            if not hasattr(module, "seed"):
                raise MigrationError(
                    f"Seed file {seed_file} must have a 'seed(database)' function."
                )

            try:
                module.seed(self.db)
            except Exception as e:
                raise MigrationError(f"Failed to execute seed {seed_file}: {e}")

            executed.append(seed_file)

        return executed
