from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import RAW_DATA_PATH, REPORTS_DIR
from src.data_loading import load_obesity_data
from src.data_validation import duplicate_count
from src.modeling import compare_models, encode_target, split_features_target


def main() -> None:
    df = load_obesity_data(RAW_DATA_PATH)
    duplicates = duplicate_count(df)
    if duplicates:
        df = df.drop_duplicates().reset_index(drop=True)

    X, y_raw = split_features_target(df)
    y, _ = encode_target(y_raw)
    results = compare_models(X, y, include_bmi=True)

    output_dir = REPORTS_DIR / "model_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "accuracy_comparison.csv"
    json_path = output_dir / "accuracy_comparison.json"

    results.to_csv(csv_path, index=False)
    json_path.write_text(
        json.dumps(results.to_dict(orient="records"), indent=2),
        encoding="utf-8",
    )

    print(results.to_string(index=False))
    print(f"\nSaved: {csv_path}")
    print(f"Saved: {json_path}")


if __name__ == "__main__":
    main()
