from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import (
    CATEGORICAL_COLUMNS,
    ENGINEERED_CATEGORICAL_COLUMNS,
    ENGINEERED_NUMERIC_COLUMNS,
    NUMERIC_COLUMNS,
)
from src.feature_engineering import ObesityFeatureEngineer


def build_preprocessor(
    include_bmi: bool = True,
    include_behavioral_features: bool = True,
    include_age_group: bool = True,
    include_weight_class: bool = True,
    excluded_columns: list[str] | None = None,
) -> ColumnTransformer:
    excluded_columns = excluded_columns or []
    numeric_columns = [column for column in NUMERIC_COLUMNS if column not in excluded_columns]
    engineered_numeric_columns = ENGINEERED_NUMERIC_COLUMNS.copy()
    if not include_bmi:
        engineered_numeric_columns.remove("BMI")
    if not include_behavioral_features:
        engineered_numeric_columns = [
            column for column in engineered_numeric_columns if column == "BMI"
        ]

    numeric_columns.extend(engineered_numeric_columns)
    categorical_columns = [column for column in CATEGORICAL_COLUMNS if column not in excluded_columns]
    engineered_categorical_columns = ENGINEERED_CATEGORICAL_COLUMNS.copy()
    if not include_bmi:
        engineered_categorical_columns.remove("BMI_Class")
    if not include_age_group:
        engineered_categorical_columns.remove("Faixa_Etaria")
    if not include_weight_class:
        engineered_categorical_columns.remove("Weight_Class")
    categorical_columns.extend(engineered_categorical_columns)

    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_columns),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
        ],
        remainder="drop",
    )


def build_model_pipeline(
    classifier,
    include_bmi: bool = True,
    include_behavioral_features: bool = True,
    include_age_group: bool = True,
    include_weight_class: bool = True,
    excluded_columns: list[str] | None = None,
) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "feature_engineering",
                ObesityFeatureEngineer(
                    include_bmi=include_bmi,
                    include_behavioral_features=include_behavioral_features,
                    include_age_group=include_age_group,
                    include_weight_class=include_weight_class,
                ),
            ),
            (
                "preprocessor",
                build_preprocessor(
                    include_bmi=include_bmi,
                    include_behavioral_features=include_behavioral_features,
                    include_age_group=include_age_group,
                    include_weight_class=include_weight_class,
                    excluded_columns=excluded_columns,
                ),
            ),
            ("classifier", classifier),
        ]
    )
