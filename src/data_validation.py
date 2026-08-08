import pandas as pd

from src.config import (
    CATEGORICAL_COLUMNS,
    EXPECTED_COLUMNS,
    NUMERIC_COLUMNS,
    PREVENTIVE_INPUT_COLUMNS,
    TARGET_COLUMN,
)


def validate_schema(df: pd.DataFrame) -> None:
    missing = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")


def validate_input_frame(df: pd.DataFrame, require_target: bool = False) -> None:
    required = EXPECTED_COLUMNS if require_target else PREVENTIVE_INPUT_COLUMNS
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Campos de entrada obrigatórios ausentes: {missing}")

    for column in NUMERIC_COLUMNS:
        if column in df.columns and not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(f"Column {column} must be numeric.")

    for column in CATEGORICAL_COLUMNS:
        if column in df.columns and df[column].isna().any():
            raise ValueError(f"A coluna {column} contém valores ausentes.")


def duplicate_count(df: pd.DataFrame) -> int:
    return int(df.duplicated().sum())
