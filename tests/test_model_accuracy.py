import pytest

from src.config import RAW_DATA_PATH
from src.data_loading import load_obesity_data
from src.modeling import encode_target, split_features_target, train_and_save_final_model


@pytest.mark.skipif(not RAW_DATA_PATH.exists(), reason="Obesity.csv is not available")
def test_final_model_accuracy_is_above_challenge_threshold():
    df = load_obesity_data(RAW_DATA_PATH).drop_duplicates().reset_index(drop=True)
    _, _, metrics = train_and_save_final_model(df)

    assert metrics["accuracy"] >= 0.75
    assert metrics["f1_macro"] >= 0.75
    assert metrics["include_bmi"] is False
    assert set(metrics["excluded_columns"]) == {"Weight", "Height"}


@pytest.mark.skipif(not RAW_DATA_PATH.exists(), reason="Obesity.csv is not available")
def test_target_encoding_matches_available_classes():
    df = load_obesity_data(RAW_DATA_PATH).drop_duplicates().reset_index(drop=True)
    _, y_raw = split_features_target(df)
    y, encoder = encode_target(y_raw)

    assert len(set(y)) == len(encoder.classes_)
