from freezegun import freeze_time
from src.utils.storage import store_object
from datetime import datetime
import os
from pathlib import Path

@freeze_time("2025-01-01")
def test_store_object(tmp_path: Path) -> None:
    """Test store_object function"""
    data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}
    table_name = "table1"
    date = datetime.now()
    
    tmp_dir = tmp_path / "./data"
    tmp_dir.mkdir()
    store_object(data, table_name, date, base_dir=tmp_dir)
    
    assert os.path.exists(f"{tmp_dir}/{table_name}/{date.year}/{date.month}/{date.day}/file.parquet") is True

@freeze_time("2025-01-01")
def test_store_object_if_path_does_not_exists(tmp_path: Path)->None:
    """Test store_object function when the given path does not exists"""
    data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}
    table_name = "table1"
    date = datetime.now()
    
    tmp_dir = tmp_path / "./data"
    store_object(data, table_name, date, base_dir=tmp_dir)
    
    assert os.path.exists(f"{tmp_dir}/{table_name}/{date.year}/{date.month}/{date.day}/file.parquet") is True
