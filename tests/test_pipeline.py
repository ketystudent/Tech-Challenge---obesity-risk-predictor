from sklearn.ensemble import RandomForestClassifier

from src.preprocessing import build_model_pipeline


def test_build_model_pipeline_contains_expected_steps():
    pipeline = build_model_pipeline(RandomForestClassifier(random_state=42))
    assert list(pipeline.named_steps) == ["feature_engineering", "preprocessor", "classifier"]

