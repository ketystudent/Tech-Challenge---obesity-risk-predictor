import time
from datetime import datetime, timezone

import joblib
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold

from src.config import RANDOM_STATE
from src.preprocessing import build_model_pipeline


def tuning_candidates() -> dict:
    return {
        "RandomForest": {
            "estimator": build_model_pipeline(
                RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1)
            ),
            "params": {
                "classifier__n_estimators": [200, 300, 500],
                "classifier__max_depth": [None, 8, 12, 16, 24],
                "classifier__min_samples_split": [2, 5, 10],
                "classifier__min_samples_leaf": [1, 2, 4],
                "classifier__max_features": ["sqrt", "log2", None],
            },
        },
        "ExtraTrees": {
            "estimator": build_model_pipeline(
                ExtraTreesClassifier(random_state=RANDOM_STATE, n_jobs=-1)
            ),
            "params": {
                "classifier__n_estimators": [200, 300, 500],
                "classifier__max_depth": [None, 8, 12, 16, 24],
                "classifier__min_samples_split": [2, 5, 10],
                "classifier__min_samples_leaf": [1, 2, 4],
                "classifier__max_features": ["sqrt", "log2", None],
            },
        },
        "GradientBoosting": {
            "estimator": build_model_pipeline(
                GradientBoostingClassifier(random_state=RANDOM_STATE)
            ),
            "params": {
                "classifier__n_estimators": [100, 150, 200],
                "classifier__learning_rate": [0.03, 0.05, 0.1, 0.2],
                "classifier__max_depth": [2, 3, 4],
                "classifier__subsample": [0.8, 0.9, 1.0],
                "classifier__min_samples_leaf": [1, 2, 4],
            },
        },
    }


def tune_candidate_models(X_train, y_train, n_iter: int = 10, cv_splits: int = 3) -> tuple[pd.DataFrame, dict]:
    cv = StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=RANDOM_STATE)
    rows = []
    best_estimators = {}

    for model_name, config in tuning_candidates().items():
        search = RandomizedSearchCV(
            estimator=config["estimator"],
            param_distributions=config["params"],
            n_iter=n_iter,
            scoring="f1_macro",
            cv=cv,
            n_jobs=-1,
            random_state=RANDOM_STATE,
            refit=True,
            return_train_score=True,
        )

        start = time.time()
        search.fit(X_train, y_train)
        duration = time.time() - start
        best_estimators[model_name] = search.best_estimator_

        rows.append(
            {
                "model": model_name,
                "best_cv_f1_macro": float(search.best_score_),
                "best_params": search.best_params_,
                "fit_time_seconds": float(duration),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    results = pd.DataFrame(rows).sort_values("best_cv_f1_macro", ascending=False).reset_index(drop=True)
    return results, best_estimators


def save_tuned_artifacts(pipeline, label_encoder, pipeline_path, label_encoder_path) -> None:
    pipeline_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, pipeline_path)
    joblib.dump(label_encoder, label_encoder_path)
