from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS
from src.feature_engineering import ObesityFeatureEngineer


def build_preprocessor(include_bmi: bool = True) -> ColumnTransformer:
    numeric_columns = NUMERIC_COLUMNS.copy()
    if include_bmi:
        numeric_columns.append("BMI")

    behavioral_columns = ["Active_Lifestyle", "Healthy_Diet", "Good_Hydration", "High_Screen_Time", "Healthy_Score"]
    numeric_columns.extend(behavioral_columns)

    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_columns),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
        ],
        remainder="drop",
    )


def build_model_pipeline(classifier, include_bmi: bool = True) -> Pipeline:
    return Pipeline(
        steps=[
            ("feature_engineering", ObesityFeatureEngineer(include_bmi=include_bmi)),
            ("preprocessor", build_preprocessor(include_bmi=include_bmi)),
            ("classifier", classifier),
        ]
    )

