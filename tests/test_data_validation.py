import pandas as pd
import pytest

from src.config import EXPECTED_COLUMNS, PREVENTIVE_INPUT_COLUMNS
from src.data_validation import duplicate_count, validate_input_frame, validate_schema


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


def test_preventive_input_does_not_require_height_or_weight():
    assert "Height" not in PREVENTIVE_INPUT_COLUMNS
    assert "Weight" not in PREVENTIVE_INPUT_COLUMNS

    input_frame = pd.DataFrame(
        [
            {
                "Gender": "Male",
                "Age": 25,
                "family_history": "yes",
                "FAVC": "yes",
                "FCVC": 2,
                "NCP": 3,
                "CAEC": "Sometimes",
                "SMOKE": "no",
                "CH2O": 2,
                "SCC": "no",
                "FAF": 1,
                "TUE": 1,
                "CALC": "Sometimes",
                "MTRANS": "Walking",
            }
        ]
    )

    validate_input_frame(input_frame)
