import os

import pytest
from peewee import SqliteDatabase

from pw_migrate.core.seeder import Seeder
from pw_migrate.exceptions import MigrationError


def test_seeder(tmp_path):
    seeds_dir = tmp_path / "seeds"
    seeds_dir.mkdir()

    # Create valid seed
    seed1 = seeds_dir / "01_test_seed.py"
    seed1.write_text("def seed(db):\n    pass")

    # Create invalid seed
    seed2 = seeds_dir / "02_invalid_seed.py"
    seed2.write_text("def not_seed(db):\n    pass")

    db = SqliteDatabase(":memory:")
    seeder = Seeder(db, seeds_dir=str(seeds_dir))

    discovered = seeder.discover_seeds()
    assert len(discovered) == 2

    # Test valid and invalid seeds execution
    with pytest.raises(MigrationError):
        seeder.run_all()

    # Remove invalid seed and run
    os.remove(str(seed2))
    executed = seeder.run_all()
    assert len(executed) == 1
    assert executed[0] == "01_test_seed.py"
