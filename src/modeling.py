import json
from importlib.util import find_spec
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from src.config import (
    CLASS_ORDER,
    FINAL_PIPELINE_PATH,
    LABEL_ENCODER_PATH,
    METRICS_PATH,
    MODEL_METADATA_PATH,
    MODELS_DIR,
    RANDOM_STATE,
    TARGET_COLUMN,
)
from src.evaluation import evaluate_predictions
from src.preprocessing import build_model_pipeline


def split_features_target(df: pd.DataFrame):
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    return X, y


def encode_target(y: pd.Series) -> tuple[np.ndarray, LabelEncoder]:
    encoder = LabelEncoder()
    encoder.fit(CLASS_ORDER)
    return encoder.transform(y), encoder


def candidate_models() -> dict:
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "DecisionTree": DecisionTreeClassifier(random_state=RANDOM_STATE),
        "RandomForest": RandomForestClassifier(n_estimators=300, random_state=RANDOM_STATE),
        "ExtraTrees": ExtraTreesClassifier(n_estimators=300, random_state=RANDOM_STATE),
        "GradientBoosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
        "KNN": KNeighborsClassifier(),
        "SVM": SVC(random_state=RANDOM_STATE, probability=True),
    }

    if find_spec("xgboost"):
        from xgboost import XGBClassifier

        models["XGBoost"] = XGBClassifier(
            random_state=RANDOM_STATE,
            eval_metric="mlogloss",
        )

    if find_spec("lightgbm"):
        from lightgbm import LGBMClassifier

        models["LightGBM"] = LGBMClassifier(random_state=RANDOM_STATE, verbose=-1)

    if find_spec("catboost"):
        from catboost import CatBoostClassifier

        models["CatBoost"] = CatBoostClassifier(
            random_state=RANDOM_STATE,
            verbose=0,
            allow_writing_files=False,
        )

    return models


def compare_models(
    X,
    y,
    include_bmi: bool = True,
    cv_splits: int = 5,
    include_behavioral_features: bool = True,
    include_age_group: bool = True,
    include_weight_class: bool = True,
    excluded_columns: list[str] | None = None,
) -> pd.DataFrame:
    cv = StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=RANDOM_STATE)
    rows = []

    for name, classifier in candidate_models().items():
        pipeline = build_model_pipeline(
            classifier,
            include_bmi=include_bmi,
            include_behavioral_features=include_behavioral_features,
            include_age_group=include_age_group,
            include_weight_class=include_weight_class,
            excluded_columns=excluded_columns,
        )
        scores = cross_validate(
            pipeline,
            X,
            y,
            cv=cv,
            scoring=["accuracy", "f1_macro", "precision_macro", "recall_macro"],
            n_jobs=-1,
        )
        rows.append(
            {
                "model": name,
                "accuracy_mean": scores["test_accuracy"].mean(),
                "accuracy_std": scores["test_accuracy"].std(),
                "f1_macro_mean": scores["test_f1_macro"].mean(),
                "f1_macro_std": scores["test_f1_macro"].std(),
                "precision_macro_mean": scores["test_precision_macro"].mean(),
                "recall_macro_mean": scores["test_recall_macro"].mean(),
            }
        )

    return pd.DataFrame(rows).sort_values("f1_macro_mean", ascending=False).reset_index(drop=True)


def train_and_save_final_model(
    df: pd.DataFrame,
    include_bmi: bool = False,
    include_behavioral_features: bool = True,
    include_age_group: bool = True,
    include_weight_class: bool = False,
    excluded_columns: list[str] | None = None,
):
    if excluded_columns is None:
        excluded_columns = ["Weight", "Height"]
    X, y_raw = split_features_target(df)
    y, label_encoder = encode_target(y_raw)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    pipeline_params = {
        "include_bmi": include_bmi,
        "include_behavioral_features": include_behavioral_features,
        "include_age_group": include_age_group,
        "include_weight_class": include_weight_class,
        "excluded_columns": excluded_columns,
    }
    comparison = compare_models(X_train, y_train, **pipeline_params)
    winner_name = comparison.iloc[0]["model"]
    pipeline = build_model_pipeline(candidate_models()[winner_name], **pipeline_params)
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test) if hasattr(pipeline, "predict_proba") else None
    metrics = evaluate_predictions(
        y_test,
        y_pred,
        y_proba,
        class_names=list(label_encoder.classes_),
    )
    metrics["winner"] = winner_name
    metrics["include_bmi"] = include_bmi
    metrics["excluded_columns"] = excluded_columns
    metrics["model_purpose"] = "preventive_behavioral_tendency"
    metrics["comparison"] = comparison.to_dict(orient="records")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, FINAL_PIPELINE_PATH)
    joblib.dump(label_encoder, LABEL_ENCODER_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    MODEL_METADATA_PATH.write_text(
        json.dumps(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "target": TARGET_COLUMN,
                "classes": list(label_encoder.classes_),
                "model_name": winner_name,
                "include_bmi": include_bmi,
                "include_weight_class": include_weight_class,
                "include_behavioral_features": include_behavioral_features,
                "excluded_columns": excluded_columns,
                "model_purpose": "preventive_behavioral_tendency",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return pipeline, label_encoder, metrics
