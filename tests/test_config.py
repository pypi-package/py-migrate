import os
import pytest
from pw_migrate.config import load_config

def test_load_config_not_found():
    config = load_config("nonexistent.toml")
    assert config == {}

def test_load_config_valid(tmp_path):
    config_path = tmp_path / "pw_migrate.toml"
    config_path.write_text('migration_dir = "my_migrations"\n[development]\ndatabase = "sqlite:///:memory:"')
    
    config = load_config(str(config_path))
    assert config["migration_dir"] == "my_migrations"
    assert config["development"]["database"] == "sqlite:///:memory:"

def test_load_config_invalid(tmp_path):
    config_path = tmp_path / "pw_migrate.toml"
    config_path.write_text('invalid toml = = = ')
    
    with pytest.raises(ValueError, match="Invalid TOML config"):
        load_config(str(config_path))

def test_config_env_override(tmp_path):
    config_file = tmp_path / "pw_migrate.toml"
    config_file.write_text('''
database = "sqlite:///dev.db"
history_table = "dev_history"

[envs.prod]
database = "postgres://user:pass@localhost/prod"
history_table = "prod_history"
''')

    # Default load
    config = load_config(str(config_file))
    assert config["database"] == "sqlite:///dev.db"
    assert config["history_table"] == "dev_history"
    
    # Env load
    config = load_config(str(config_file), env="prod")
    assert config["database"] == "postgres://user:pass@localhost/prod"
    assert config["history_table"] == "prod_history"
