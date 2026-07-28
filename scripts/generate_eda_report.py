from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from src.config import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS, RAW_DATA_PATH, REPORTS_DIR, TARGET_COLUMN
from src.data_loading import load_obesity_data
from src.data_validation import duplicate_count


FIGURES_DIR = REPORTS_DIR / "figures"
EDA_DIR = REPORTS_DIR / "eda"


def save_bar(series: pd.Series, title: str, xlabel: str, ylabel: str, path: Path) -> None:
    plt.figure(figsize=(11, 6))
    plt.barh(series.index.astype(str), series.values, color="#2f6f73")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_numeric_histograms(df: pd.DataFrame, path: Path) -> None:
    axes = df[NUMERIC_COLUMNS].hist(figsize=(14, 10), bins=30, color="#2f6f73", edgecolor="white")
    for row in axes:
        for ax in row:
            ax.set_title(ax.get_title(), fontsize=10)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_correlation_heatmap(df: pd.DataFrame, path: Path) -> None:
    plt.figure(figsize=(10, 8))
    corr = df[NUMERIC_COLUMNS].corr()
    plt.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    plt.colorbar(label="Correlacao")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr.index)), corr.index)
    for i, row in enumerate(corr.index):
        for j, col in enumerate(corr.columns):
            plt.text(j, i, f"{corr.loc[row, col]:.2f}", ha="center", va="center", fontsize=8)
    plt.title("Correlacao entre variaveis numericas")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_weight_height_scatter(df: pd.DataFrame, path: Path) -> None:
    plt.figure(figsize=(11, 7))
    classes = sorted(df[TARGET_COLUMN].unique())
    cmap = plt.get_cmap("tab10")
    for idx, class_name in enumerate(classes):
        subset = df[df[TARGET_COLUMN] == class_name]
        plt.scatter(subset["Height"], subset["Weight"], label=class_name, alpha=0.75, s=35, color=cmap(idx))
    plt.title("Peso e altura por nivel de obesidade")
    plt.xlabel("Altura (m)")
    plt.ylabel("Peso (kg)")
    plt.legend(title="Nivel", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_boxplot(df: pd.DataFrame, column: str, path: Path) -> None:
    plt.figure(figsize=(12, 7))
    classes = sorted(df[TARGET_COLUMN].unique())
    values = [df.loc[df[TARGET_COLUMN] == class_name, column].values for class_name in classes]
    plt.boxplot(values, tick_labels=classes, patch_artist=True)
    plt.title(f"{column} por nivel de obesidade")
    plt.xlabel("Nivel de obesidade")
    plt.ylabel(column)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def build_summary(df: pd.DataFrame, df_clean: pd.DataFrame) -> dict:
    return {
        "rows_original": int(len(df)),
        "rows_without_duplicates": int(len(df_clean)),
        "columns": int(df.shape[1]),
        "duplicate_rows": duplicate_count(df),
        "missing_values": df.isna().sum().astype(int).to_dict(),
        "target_distribution": df_clean[TARGET_COLUMN].value_counts().astype(int).to_dict(),
        "target_distribution_pct": (
            df_clean[TARGET_COLUMN].value_counts(normalize=True).mul(100).round(2).to_dict()
        ),
        "numeric_summary": df_clean[NUMERIC_COLUMNS].describe().round(4).to_dict(),
        "categorical_unique_values": {
            column: sorted(df_clean[column].dropna().astype(str).unique().tolist())
            for column in CATEGORICAL_COLUMNS + [TARGET_COLUMN]
        },
    }


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    EDA_DIR.mkdir(parents=True, exist_ok=True)

    df = load_obesity_data(RAW_DATA_PATH)
    df_clean = df.drop_duplicates().reset_index(drop=True)

    summary = build_summary(df, df_clean)
    (EDA_DIR / "eda_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    df_clean[NUMERIC_COLUMNS].describe().round(4).to_csv(EDA_DIR / "numeric_summary.csv")
    df_clean[TARGET_COLUMN].value_counts().rename_axis(TARGET_COLUMN).reset_index(name="count").to_csv(
        EDA_DIR / "target_distribution.csv", index=False
    )

    save_bar(
        df_clean[TARGET_COLUMN].value_counts(),
        "Distribuicao do nivel de obesidade",
        "Quantidade de registros",
        "Nivel de obesidade",
        FIGURES_DIR / "target_distribution.png",
    )
    save_numeric_histograms(df_clean, FIGURES_DIR / "numeric_histograms.png")
    save_correlation_heatmap(df_clean, FIGURES_DIR / "numeric_correlation_heatmap.png")
    save_weight_height_scatter(df_clean, FIGURES_DIR / "weight_height_by_obesity.png")
    save_boxplot(df_clean, "Age", FIGURES_DIR / "age_by_obesity.png")
    save_boxplot(df_clean, "Weight", FIGURES_DIR / "weight_by_obesity.png")

    print(f"EDA summary saved: {EDA_DIR / 'eda_summary.json'}")
    print(f"Figures saved under: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
