import os
import re
from typing import List

MIGRATION_PATTERN = re.compile(r"^\d{14}_[a-zA-Z0-9_]+\.py$")

def discover_migrations(directory: str) -> List[str]:
    """Discover and sort valid migration files in the given directory."""
    if not os.path.isdir(directory):
        return []

    migrations = []
    for filename in os.listdir(directory):
        if MIGRATION_PATTERN.match(filename):
            migrations.append(filename)
    
    return sorted(migrations)
