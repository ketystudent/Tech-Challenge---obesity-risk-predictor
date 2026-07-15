import joblib
import pandas as pd

from src.config import CLASS_LABELS_PT, FINAL_PIPELINE_PATH, LABEL_ENCODER_PATH
from src.data_validation import validate_input_frame


def load_prediction_artifacts():
    if not FINAL_PIPELINE_PATH.exists() or not LABEL_ENCODER_PATH.exists():
        raise FileNotFoundError("Model artifacts not found. Train the final model first.")
    return joblib.load(FINAL_PIPELINE_PATH), joblib.load(LABEL_ENCODER_PATH)


def predict_obesity(input_data: dict | pd.DataFrame) -> dict:
    df = pd.DataFrame([input_data]) if isinstance(input_data, dict) else input_data.copy()
    validate_input_frame(df)

    pipeline, label_encoder = load_prediction_artifacts()
    prediction = pipeline.predict(df)
    predicted_class = str(label_encoder.inverse_transform(prediction)[0])

    result = {
        "predicted_class": predicted_class,
        "predicted_label": CLASS_LABELS_PT.get(predicted_class, predicted_class),
        "probabilities": {},
    }

    if hasattr(pipeline, "predict_proba"):
        probabilities = pipeline.predict_proba(df)[0]
        for class_name, probability in zip(label_encoder.classes_, probabilities):
            result["probabilities"][str(class_name)] = float(probability)

    return result
