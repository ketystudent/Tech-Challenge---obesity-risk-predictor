import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class ObesityFeatureEngineer(BaseEstimator, TransformerMixin):
    """Create deterministic patient features without fitting on the full dataset."""

    def __init__(
        self,
        include_behavioral_features: bool = True,
        include_bmi: bool = True,
        include_age_group: bool = True,
        include_weight_class: bool = True,
    ):
        self.include_behavioral_features = include_behavioral_features
        self.include_bmi = include_bmi
        self.include_age_group = include_age_group
        self.include_weight_class = include_weight_class

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = pd.DataFrame(X).copy()

        if self.include_bmi:
            df["BMI"] = df["Weight"] / np.power(df["Height"], 2)
            df["BMI_Class"] = pd.cut(
                df["BMI"],
                bins=[0, 18.5, 25, 30, 35, 40, np.inf],
                labels=[
                    "Underweight",
                    "Normal",
                    "Overweight",
                    "Obesity_I",
                    "Obesity_II",
                    "Obesity_III",
                ],
                include_lowest=True,
            ).astype(str)
        else:
            df["BMI"] = 0.0
            df["BMI_Class"] = "Not_Used"

        if self.include_age_group:
            df["Faixa_Etaria"] = pd.cut(
                df["Age"],
                bins=[0, 18, 25, 35, 50, np.inf],
                labels=["Ate_18", "19_25", "26_35", "36_50", "Acima_50"],
                include_lowest=True,
            ).astype(str)
        else:
            df["Faixa_Etaria"] = "Not_Used"

        if self.include_weight_class:
            df["Weight_Class"] = pd.cut(
                df["Weight"],
                bins=[0, 60, 80, 100, np.inf],
                labels=["Ate_60kg", "60_80kg", "80_100kg", "Acima_100kg"],
                include_lowest=True,
            ).astype(str)
        else:
            df["Weight_Class"] = "Not_Used"

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
        else:
            df["Active_Lifestyle"] = 0
            df["Healthy_Diet"] = 0
            df["Good_Hydration"] = 0
            df["High_Screen_Time"] = 0
            df["Healthy_Score"] = 0

        return df
