from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from src.config import RAW_DATA_PATH, REPORTS_DIR
from src.data_loading import load_obesity_data
from src.data_validation import duplicate_count
from src.modeling import compare_models, encode_target, split_features_target


SCENARIOS = {
    "full_current": {
        "description": "Pipeline atual com variaveis originais e features derivadas.",
        "params": {
            "include_bmi": True,
            "include_behavioral_features": True,
            "include_age_group": True,
            "include_weight_class": True,
            "excluded_columns": [],
        },
    },
    "no_derived_redundant": {
        "description": "Mantem colunas originais e remove features derivadas redundantes.",
        "params": {
            "include_bmi": False,
            "include_behavioral_features": False,
            "include_age_group": False,
            "include_weight_class": False,
            "excluded_columns": [],
        },
    },
    "preventive_behavioral": {
        "description": "Remove peso e derivados antropometricos para estimar um modelo mais preventivo/comportamental.",
        "params": {
            "include_bmi": False,
            "include_behavioral_features": False,
            "include_age_group": False,
            "include_weight_class": False,
            "excluded_columns": ["Weight"],
        },
    },
}


def main() -> None:
    df = load_obesity_data(RAW_DATA_PATH)
    duplicates = duplicate_count(df)
    if duplicates:
        df = df.drop_duplicates().reset_index(drop=True)

    X, y_raw = split_features_target(df)
    y, _ = encode_target(y_raw)

    all_rows = []
    full_results = {}
    for scenario_name, config in SCENARIOS.items():
        results = compare_models(X, y, **config["params"])
        results.insert(0, "scenario", scenario_name)
        results.insert(1, "scenario_description", config["description"])
        full_results[scenario_name] = results.to_dict(orient="records")
        all_rows.append(results)

    comparison = pd.concat(all_rows, ignore_index=True)
    best_by_scenario = (
        comparison.sort_values(["scenario", "f1_macro_mean"], ascending=[True, False])
        .groupby("scenario", as_index=False)
        .head(1)
        .reset_index(drop=True)
    )

    output_dir = REPORTS_DIR / "model_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    comparison_csv = output_dir / "redundancy_scenarios_all_models.csv"
    best_csv = output_dir / "redundancy_scenarios_best_models.csv"
    json_path = output_dir / "redundancy_scenarios.json"

    comparison.to_csv(comparison_csv, index=False)
    best_by_scenario.to_csv(best_csv, index=False)
    json_path.write_text(json.dumps(full_results, indent=2), encoding="utf-8")

    print("Best model by scenario:")
    print(
        best_by_scenario[
            [
                "scenario",
                "model",
                "accuracy_mean",
                "f1_macro_mean",
                "precision_macro_mean",
                "recall_macro_mean",
            ]
        ].to_string(index=False)
    )
    print(f"\nSaved: {comparison_csv}")
    print(f"Saved: {best_csv}")
    print(f"Saved: {json_path}")


if __name__ == "__main__":
    main()
