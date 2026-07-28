import os
import sys
from typing import Any, Dict

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

def load_config(path: str = "pw_migrate.toml", env: str = None) -> Dict[str, Any]:
    """Load and parse the pw-migrate configuration file."""
    if not os.path.exists(path):
        return {}
        
    env = env or os.environ.get("PW_MIGRATE_ENV")
    
    with open(path, "rb") as f:
        try:
            config = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Invalid TOML config in {path}: {e}")
            
    if env and "envs" in config and env in config["envs"]:
        env_config = config["envs"][env]
        for k, v in env_config.items():
            config[k] = v
            
    return config
