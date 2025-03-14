import os
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from freezegun import freeze_time

from src.utils.storage import (
    store_object,
    store_object_aws,
    store_object_azure,
    store_object_gcp,
    store_object_local,
)


@pytest.mark.parametrize("provider", ["local", "gcp", "aws", "azure"])
def test_store_object(provider: str) -> None:
    """Test store_object function"""
    with (
        patch.dict(os.environ, {"PROVIDER": provider}),
        patch(f"src.utils.storage.store_object_{provider}") as mock_store_object_local,
    ):
        store_object({"col1": [1, 2, 3], "col2": [4, 5, 6]}, "table", datetime.now())
        assert mock_store_object_local.called
        # NOTE: ADD ASSERT WITH ARGS


@freeze_time("2025-01-01")
def test_store_object_local(tmp_path: Path) -> None:
    """Test store_object function"""
    data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    table_name = "table1"
    date = datetime.now()

    tmp_dir = tmp_path / "./data"
    tmp_dir.mkdir()

    store_object_local(df=data, table_name=table_name, date=date, base_dir=tmp_dir)

    assert (
        os.path.exists(
            f"{tmp_dir}/{table_name}/{date.year}/{date.month}/{date.day}/file.parquet"
        )
        is True
    )


@freeze_time("2025-01-01")
@patch.dict(os.environ, {"PROVIDER": "local"})
def test_store_object_if_path_does_not_exists(tmp_path: Path) -> None:
    """Test store_object function when the given path does not exists"""
    data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}
    table_name = "table1"
    date = datetime.now()

    tmp_dir = tmp_path / "./data"
    store_object(data, table_name, date, base_dir=tmp_dir)

    assert (
        os.path.exists(
            f"{tmp_dir}/{table_name}/{date.year}/{date.month}/{date.day}/file.parquet"
        )
        is True
    )


@freeze_time("2025-01-01")
def test_store_object_gcp() -> None:
    """Test store_object_gcp function"""
    data = MagicMock()
    table_name = "table1"
    date = datetime.now()

    with patch.dict(os.environ, {"GCP_BUCKET_NAME": "bucket"}):
        store_object_gcp(data, table_name, date, base_dir="./data")

    data.to_parquet.assert_called_once_with(
        "gs://bucket/data/table1/2025/1/1/file.parquet", index=False
    )


def test_store_object_aws() -> None:
    """Test store_object_aws function"""
    pass
    #with pytest.raises(NotImplementedError):
    #    store_object_gcp(MagicMock(), MagicMock(), MagicMock(),MagicMock())


def test_store_object_azure() -> None:
    """Test store_object_azure function"""
    pass
    #with pytest.raises(NotImplementedError):
    #   store_object_azure(MagicMock(), MagicMock(), MagicMock(),MagicMock())
