from pathlib import Path

import pandas as pd

from src.config import RAW_DATA_PATH
from src.data_validation import validate_schema


def load_obesity_data(path: str | Path = RAW_DATA_PATH, validate: bool = True) -> pd.DataFrame:
    data_path = Path(path)
    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {data_path}. Place Obesity.csv under data/raw/."
        )

    df = pd.read_csv(data_path)
    if validate:
        validate_schema(df)
    return df.copy()

