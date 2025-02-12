import pandas as pd
from datetime import datetime
import os

def store_object(data: dict, table_name: str, date: datetime, base_dir: str = "./data") -> None:
    """Store object in parquet format
    
    NOTE: right now, this function stores the data locally,
    but it should be modified to store the data in a cloud storage
    """
    df = pd.DataFrame(data)
    directory = f"{base_dir}/{table_name}/{date.year}/{date.month}/{date.day}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    df.to_parquet(f"{directory}/file.parquet", index=False)
