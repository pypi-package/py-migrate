import pytest
from pw_migrate.core.discovery import discover_migrations

def test_discover_migrations_no_dir():
    assert discover_migrations("nonexistent_dir") == []

def test_discover_migrations_valid(tmp_path):
    mig_dir = tmp_path / "migrations"
    mig_dir.mkdir()
    
    (mig_dir / "20260728124500_create_users.py").write_text("")
    (mig_dir / "20260728124600_create_posts.py").write_text("")
    (mig_dir / "invalid_migration.py").write_text("")
    (mig_dir / "20260728124700_create_tags.txt").write_text("")
    
    migrations = discover_migrations(str(mig_dir))
    
    assert len(migrations) == 2
    assert migrations == [
        "20260728124500_create_users.py",
        "20260728124600_create_posts.py"
    ]
