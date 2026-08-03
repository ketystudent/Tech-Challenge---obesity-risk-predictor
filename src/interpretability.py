import pandas as pd
from sklearn.inspection import permutation_importance

from src.config import RANDOM_STATE


def compute_permutation_importance(pipeline, X, y, n_repeats: int = 10) -> pd.DataFrame:
    result = permutation_importance(
        pipeline,
        X,
        y,
        n_repeats=n_repeats,
        random_state=RANDOM_STATE,
        scoring="f1_macro",
    )
    return pd.DataFrame(
        {
            "feature": X.columns,
            "importance_mean": result.importances_mean,
            "importance_std": result.importances_std,
        }
    ).sort_values("importance_mean", ascending=False)


def get_model_feature_importance(pipeline) -> pd.DataFrame:
    classifier = pipeline.named_steps["classifier"]
    preprocessor = pipeline.named_steps["preprocessor"]

    if not hasattr(classifier, "feature_importances_"):
        raise ValueError("O classificador final não disponibiliza feature_importances_.")

    feature_names = preprocessor.get_feature_names_out()
    return pd.DataFrame(
        {
            "feature": feature_names,
            "importance": classifier.feature_importances_,
        }
    ).sort_values("importance", ascending=False)
