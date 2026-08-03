from pathlib import Path

RANDOM_STATE = 42
TARGET_COLUMN = "Obesity"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

RAW_DATA_PATH = RAW_DATA_DIR / "Obesity.csv"
FINAL_PIPELINE_PATH = MODELS_DIR / "final_pipeline.joblib"
LABEL_ENCODER_PATH = MODELS_DIR / "label_encoder.joblib"
METRICS_PATH = MODELS_DIR / "metrics.json"
MODEL_METADATA_PATH = MODELS_DIR / "model_metadata.json"
TUNED_PIPELINE_PATH = MODELS_DIR / "tuned_pipeline.joblib"
TUNED_LABEL_ENCODER_PATH = MODELS_DIR / "tuned_label_encoder.joblib"
TUNED_METRICS_PATH = MODELS_DIR / "tuned_metrics.json"
TUNED_MODEL_METADATA_PATH = MODELS_DIR / "tuned_model_metadata.json"

CLASS_ORDER = [
    "Insufficient_Weight",
    "Normal_Weight",
    "Overweight_Level_I",
    "Overweight_Level_II",
    "Obesity_Type_I",
    "Obesity_Type_II",
    "Obesity_Type_III",
]

CLASS_LABELS_PT = {
    "Insufficient_Weight": "Peso insuficiente",
    "Normal_Weight": "Peso normal",
    "Overweight_Level_I": "Sobrepeso nível I",
    "Overweight_Level_II": "Sobrepeso nível II",
    "Obesity_Type_I": "Obesidade tipo I",
    "Obesity_Type_II": "Obesidade tipo II",
    "Obesity_Type_III": "Obesidade tipo III",
}

NUMERIC_COLUMNS = ["Age", "Height", "Weight", "FCVC", "NCP", "CH2O", "FAF", "TUE"]
CATEGORICAL_COLUMNS = [
    "Gender",
    "family_history",
    "FAVC",
    "CAEC",
    "SMOKE",
    "SCC",
    "CALC",
    "MTRANS",
]
EXPECTED_COLUMNS = NUMERIC_COLUMNS + CATEGORICAL_COLUMNS + [TARGET_COLUMN]

YES_NO_COLUMNS = ["family_history", "FAVC", "SMOKE", "SCC"]

ENGINEERED_NUMERIC_COLUMNS = [
    "BMI",
    "Active_Lifestyle",
    "Healthy_Diet",
    "Good_Hydration",
    "High_Screen_Time",
    "Healthy_Score",
]

ENGINEERED_CATEGORICAL_COLUMNS = [
    "Faixa_Etaria",
    "BMI_Class",
    "Weight_Class",
]
