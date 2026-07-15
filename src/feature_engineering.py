import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class ObesityFeatureEngineer(BaseEstimator, TransformerMixin):
    """Create deterministic patient features without fitting on the full dataset."""

    def __init__(self, include_behavioral_features: bool = True, include_bmi: bool = True):
        self.include_behavioral_features = include_behavioral_features
        self.include_bmi = include_bmi

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = pd.DataFrame(X).copy()

        if self.include_bmi:
            df["BMI"] = df["Weight"] / np.power(df["Height"], 2)

        if self.include_behavioral_features:
            df["Active_Lifestyle"] = (df["FAF"] >= 2).astype(int)
            df["Healthy_Diet"] = ((df["FCVC"] >= 2) & (df["FAVC"].astype(str).str.lower() == "no")).astype(int)
            df["Good_Hydration"] = (df["CH2O"] >= 2).astype(int)
            df["High_Screen_Time"] = (df["TUE"] >= 2).astype(int)
            df["Healthy_Score"] = (
                df["Active_Lifestyle"]
                + df["Healthy_Diet"]
                + df["Good_Hydration"]
                + (1 - df["High_Screen_Time"])
            )

        return df

