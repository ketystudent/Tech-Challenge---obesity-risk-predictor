from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from src.config import (
    FINAL_PIPELINE_PATH,
    LABEL_ENCODER_PATH,
    RANDOM_STATE,
    RAW_DATA_PATH,
    REPORTS_DIR,
)
from src.data_loading import load_obesity_data
from src.interpretability import compute_permutation_importance, get_model_feature_importance
from src.modeling import encode_target, split_features_target


FIGURES_DIR = REPORTS_DIR / "figures"
MODEL_RESULTS_DIR = REPORTS_DIR / "model_results"


def save_confusion_matrix(y_true, y_pred, class_names: list[str], path: Path) -> None:
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(10, 8))
    image = ax.imshow(cm, cmap="Blues")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    ax.set_xticks(range(len(class_names)))
    ax.set_yticks(range(len(class_names)))
    ax.set_xticklabels(class_names, rotation=35, ha="right")
    ax.set_yticklabels(class_names)
    ax.set_xlabel("Predicao")
    ax.set_ylabel("Real")
    ax.set_title("Matriz de confusao - modelo final")

    threshold = cm.max() / 2
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            color = "white" if cm[i, j] > threshold else "black"
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", color=color)

    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close(fig)


def save_importance_bar(df: pd.DataFrame, value_column: str, title: str, path: Path, top_n: int = 15) -> None:
    top = df.head(top_n).sort_values(value_column)
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.barh(top["feature"], top[value_column], color="#2f6f73")
    ax.set_title(title)
    ax.set_xlabel(value_column)
    ax.set_ylabel("Feature")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close(fig)


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

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

    pipeline = joblib.load(FINAL_PIPELINE_PATH)
    saved_label_encoder = joblib.load(LABEL_ENCODER_PATH)
    class_names = [str(class_name) for class_name in saved_label_encoder.classes_]

    y_pred = pipeline.predict(X_test)
    report = classification_report(
        y_test,
        y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )

    report_path = MODEL_RESULTS_DIR / "classification_report.json"
    report_csv_path = MODEL_RESULTS_DIR / "classification_report.csv"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    pd.DataFrame(report).transpose().to_csv(report_csv_path)

    cm_path = FIGURES_DIR / "confusion_matrix_final_model.png"
    save_confusion_matrix(y_test, y_pred, class_names, cm_path)

    feature_importance = get_model_feature_importance(pipeline)
    feature_importance_path = MODEL_RESULTS_DIR / "feature_importance.csv"
    feature_importance.to_csv(feature_importance_path, index=False)
    save_importance_bar(
        feature_importance,
        "importance",
        "Top 15 features - importancia do modelo",
        FIGURES_DIR / "feature_importance_top15.png",
    )

    permutation = compute_permutation_importance(pipeline, X_test, y_test, n_repeats=5)
    permutation_path = MODEL_RESULTS_DIR / "permutation_importance.csv"
    permutation.to_csv(permutation_path, index=False)
    save_importance_bar(
        permutation,
        "importance_mean",
        "Top 15 features - permutation importance",
        FIGURES_DIR / "permutation_importance_top15.png",
    )

    summary = {
        "classification_report": str(report_path),
        "classification_report_csv": str(report_csv_path),
        "confusion_matrix_figure": str(cm_path),
        "feature_importance_csv": str(feature_importance_path),
        "feature_importance_figure": str(FIGURES_DIR / "feature_importance_top15.png"),
        "permutation_importance_csv": str(permutation_path),
        "permutation_importance_figure": str(FIGURES_DIR / "permutation_importance_top15.png"),
    }
    summary_path = MODEL_RESULTS_DIR / "interpretability_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Model interpretability artifacts generated.")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
