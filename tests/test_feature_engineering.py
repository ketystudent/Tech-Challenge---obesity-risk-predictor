import pandas as pd

from src.feature_engineering import ObesityFeatureEngineer


def test_feature_engineering_creates_expected_features():
    df = pd.DataFrame(
        [
            {
                "Age": 25,
                "Height": 1.70,
                "Weight": 70,
                "FCVC": 3,
                "NCP": 3,
                "CH2O": 2,
                "FAF": 2,
                "TUE": 1,
                "FAVC": "no",
            }
        ]
    )

    transformed = ObesityFeatureEngineer().fit_transform(df)

    assert "BMI" in transformed.columns
    assert "Healthy_Score" in transformed.columns
    assert transformed.loc[0, "Active_Lifestyle"] == 1

