import os
from datetime import datetime

import pandas as pd


def store_object(
    data: dict, table_name: str, date: datetime, base_dir: str = "./data"
) -> None:
    """Store object in parquet format"""

    df = pd.DataFrame(data)
    provider = os.environ.get("PROVIDER")
    if not provider:
        raise ValueError("Please set the PROVIDER environment variable")
    if provider.lower() == "local":
        store_object_local(df=df, table_name=table_name, date=date, base_dir=base_dir)
    elif provider.lower() == "gcp":
        store_object_gcp(df=df, table_name=table_name, date=date, base_dir=base_dir)
    elif provider.lower() == "aws":
        store_object_aws(df=df, table_name=table_name, date=date, base_dir=base_dir)
    elif provider.lower() == "azure":
        store_object_azure()
    else:
        raise ValueError(f"Invalid provider {provider=}")


def store_object_local(
    df: pd.DataFrame, table_name: str, date: datetime, base_dir: str
) -> None:
    """Store object in parquet format, locally"""
    directory = f"{base_dir}/{table_name}/{date.year}/{date.month}/{date.day}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    df.to_parquet(f"{directory}/file.parquet", index=False)


def store_object_gcp(
    df: pd.DataFrame, table_name: str, date: datetime, base_dir: str
) -> None:
    """Store object in parquet format, in Google Cloud Storage"""
    bucket_name = os.environ.get("GCP_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("Please set the GCP_BUCKET_NAME environment variable")
    base_dir = base_dir.split("./")[-1]
    directory = f"{base_dir}/{table_name}/{date.year}/{date.month}/{date.day}"
    df.to_parquet(f"gs://{bucket_name}/{directory}/file.parquet", index=False)


def store_object_aws(
    df: pd.DataFrame, table_name: str, date: datetime, base_dir: str
) -> None:
    """Store object in parquet format, in Amazon Web Services"""
    bucket_name = os.environ.get("AWS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("Please set the AWS_BUCKET_NAME environment variable")
    base_dir = base_dir.split("./")[-1]
    directory = f"{base_dir}/{table_name}/{date.year}/{date.month}/{date.day}"
    df.to_parquet(f"s3://{bucket_name}/{directory}/file.parquet", index=False)


def store_object_azure() -> None:
    """Store object in parquet format, in Microsoft Azure"""
    raise NotImplementedError
