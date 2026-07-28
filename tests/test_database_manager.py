import os
import pytest
from pw_migrate.core.database_manager import DatabaseManager
from pw_migrate.exceptions import MigrationError

def test_database_manager_sqlite(tmp_path):
    db_file = tmp_path / "test.db"
    db_url = f"sqlite:///{db_file}"
    manager = DatabaseManager(db_url)
    
    # Test Create
    manager.create_database()
    assert os.path.exists(db_file)
    
    # Test Create Again (should raise error)
    with pytest.raises(MigrationError):
        manager.create_database()
        
    # Test Drop
    manager.drop_database()
    assert not os.path.exists(db_file)
    
    # Test Drop Again (should raise error)
    with pytest.raises(MigrationError):
        manager.drop_database()

def test_database_manager_memory():
    # Should not raise any errors, should just return
    manager = DatabaseManager("sqlite:///:memory:")
    manager.create_database()
    manager.drop_database()

def test_database_manager_unsupported():
    manager = DatabaseManager("oracle://localhost/test")
    with pytest.raises(NotImplementedError):
        manager.create_database()
    with pytest.raises(NotImplementedError):
        manager.drop_database()
