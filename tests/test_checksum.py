import pytest
import os
from pw_migrate.core.checksum import calculate_checksum

def test_calculate_checksum(tmp_path):
    test_file = tmp_path / "test_migration.py"
    test_file.write_text("def migrate(): pass")
    
    checksum = calculate_checksum(str(test_file))
    assert checksum is not None
    assert len(checksum) == 64  # SHA256 length
    
    # Modify file
    test_file.write_text("def migrate(): print('changed')")
    new_checksum = calculate_checksum(str(test_file))
    
    assert checksum != new_checksum

def test_checksum_missing_file():
    assert calculate_checksum("nonexistent.py") == ""
