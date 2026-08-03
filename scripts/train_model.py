from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    FINAL_PIPELINE_PATH,
    LABEL_ENCODER_PATH,
    METRICS_PATH,
    MODEL_METADATA_PATH,
    RAW_DATA_PATH,
)
from src.data_loading import load_obesity_data
from src.data_validation import duplicate_count
from src.modeling import train_and_save_final_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and export the final obesity prediction model.")
    parser.add_argument(
        "--without-bmi",
        action="store_true",
        help="Train a behavioral/preventive model without engineered BMI.",
    )
    parser.add_argument(
        "--keep-duplicates",
        action="store_true",
        help="Mantém as linhas duplicadas em vez de removê-las antes do treinamento.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = load_obesity_data(RAW_DATA_PATH)

    duplicates = duplicate_count(df)
    if duplicates and not args.keep_duplicates:
        df = df.drop_duplicates().reset_index(drop=True)

    _, _, metrics = train_and_save_final_model(df, include_bmi=not args.without_bmi)

    print("Training finished.")
    print(f"Rows used: {len(df)}")
    print(f"Duplicatas encontradas: {duplicates}")
    print(f"Duplicatas removidas: {duplicates if duplicates and not args.keep_duplicates else 0}")
    print(f"Vencedor: {metrics['winner']}")
    print(f"Acurácia: {metrics['accuracy']:.4f}")
    print(f"F1 macro: {metrics['f1_macro']:.4f}")
    print("Artifacts:")
    print(f"- {FINAL_PIPELINE_PATH}")
    print(f"- {LABEL_ENCODER_PATH}")
    print(f"- {METRICS_PATH}")
    print(f"- {MODEL_METADATA_PATH}")


if __name__ == "__main__":
    main()
