import pandas as pd
import pytest

from src.config import EXPECTED_COLUMNS
from src.data_validation import duplicate_count, validate_schema


def test_validate_schema_accepts_expected_columns():
    df = pd.DataFrame(columns=EXPECTED_COLUMNS)
    validate_schema(df)


def test_validate_schema_rejects_missing_column():
    df = pd.DataFrame(columns=EXPECTED_COLUMNS[:-1])
    with pytest.raises(ValueError):
        validate_schema(df)


def test_duplicate_count():
    df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})
    assert duplicate_count(df) == 1

