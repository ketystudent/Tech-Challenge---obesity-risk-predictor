from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sklearn.model_selection import train_test_split

from src.config import (
    FINAL_PIPELINE_PATH,
    LABEL_ENCODER_PATH,
    METRICS_PATH,
    MODEL_METADATA_PATH,
    RANDOM_STATE,
    RAW_DATA_PATH,
    REPORTS_DIR,
    TUNED_LABEL_ENCODER_PATH,
    TUNED_METRICS_PATH,
    TUNED_MODEL_METADATA_PATH,
    TUNED_PIPELINE_PATH,
)
from src.data_loading import load_obesity_data
from src.evaluation import evaluate_predictions
from src.modeling import encode_target, split_features_target
from src.tuning import save_tuned_artifacts, tune_candidate_models


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run reproducible hyperparameter tuning.")
    parser.add_argument("--n-iter", type=int, default=10, help="RandomizedSearchCV iterations per model.")
    parser.add_argument("--cv", type=int, default=3, help="Number of cross-validation folds.")
    parser.add_argument(
        "--promote",
        action="store_true",
        help="Replace final_pipeline.joblib if the tuned model beats the current final F1 macro.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = load_obesity_data(RAW_DATA_PATH).drop_duplicates().reset_index(drop=True)
    X, y_raw = split_features_target(df)
    y, label_encoder = encode_target(y_raw)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    tuning_results, best_estimators = tune_candidate_models(
        X_train,
        y_train,
        n_iter=args.n_iter,
        cv_splits=args.cv,
    )
    winner_name = tuning_results.iloc[0]["model"]
    winner_pipeline = best_estimators[winner_name]

    y_pred = winner_pipeline.predict(X_test)
    y_proba = winner_pipeline.predict_proba(X_test) if hasattr(winner_pipeline, "predict_proba") else None
    metrics = evaluate_predictions(
        y_test,
        y_pred,
        y_proba,
        class_names=list(label_encoder.classes_),
    )
    metrics["winner"] = winner_name
    metrics["best_params"] = tuning_results.iloc[0]["best_params"]
    metrics["cv_f1_macro"] = float(tuning_results.iloc[0]["best_cv_f1_macro"])
    metrics["n_iter"] = args.n_iter
    metrics["cv"] = args.cv

    output_dir = REPORTS_DIR / "model_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    tuning_csv = output_dir / "tuning_results.csv"
    tuning_json = output_dir / "tuning_results.json"
    tuning_results.to_csv(tuning_csv, index=False)
    tuning_json.write_text(
        json.dumps(tuning_results.to_dict(orient="records"), indent=2, default=str),
        encoding="utf-8",
    )

    save_tuned_artifacts(
        winner_pipeline,
        label_encoder,
        TUNED_PIPELINE_PATH,
        TUNED_LABEL_ENCODER_PATH,
    )
    TUNED_METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    TUNED_MODEL_METADATA_PATH.write_text(
        json.dumps(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "model_name": winner_name,
                "classes": list(label_encoder.classes_),
                "artifact": str(TUNED_PIPELINE_PATH),
                "source": "RandomizedSearchCV",
                "n_iter": args.n_iter,
                "cv": args.cv,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    promoted = False
    current_f1 = None
    if METRICS_PATH.exists():
        current_f1 = json.loads(METRICS_PATH.read_text(encoding="utf-8")).get("f1_macro")

    if args.promote and (current_f1 is None or metrics["f1_macro"] > current_f1):
        save_tuned_artifacts(winner_pipeline, label_encoder, FINAL_PIPELINE_PATH, LABEL_ENCODER_PATH)
        METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        MODEL_METADATA_PATH.write_text(
            json.dumps(
                {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "model_name": winner_name,
                    "classes": list(label_encoder.classes_),
                    "artifact": str(FINAL_PIPELINE_PATH),
                    "source": "promoted_tuned_model",
                    "n_iter": args.n_iter,
                    "cv": args.cv,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        promoted = True

    print("Tuning finished.")
    print(tuning_results.to_string(index=False))
    print(f"\nBest tuned model: {winner_name}")
    print(f"Tuned test accuracy: {metrics['accuracy']:.4f}")
    print(f"Tuned test F1 macro: {metrics['f1_macro']:.4f}")
    if current_f1 is not None:
        print(f"Current final F1 macro: {current_f1:.4f}")
    print(f"Promoted to final artifacts: {promoted}")
    print(f"Saved: {tuning_csv}")
    print(f"Saved: {tuning_json}")
    print(f"Saved: {TUNED_PIPELINE_PATH}")


if __name__ == "__main__":
    main()
