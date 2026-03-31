from __future__ import annotations

import os
from pathlib import Path
import joblib
import pandas as pd

from ml.feature_engineering import extract_features_from_url, FEATURE_COLUMNS
from backend.app.utils import extract_reason_flags


class Predictor:
    def __init__(self, model_path: str | None = None):
        self.model_path = Path(model_path or os.getenv("MODEL_PATH", "models/phishguard_model.joblib"))
        self.bundle = None
        self.model = None
        self.feature_columns = FEATURE_COLUMNS
        self.load()

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {self.model_path}. Train first with: python ml/train.py"
            )
        self.bundle = joblib.load(self.model_path)
        self.model = self.bundle["model"]
        self.feature_columns = self.bundle.get("feature_columns", FEATURE_COLUMNS)

    def predict_one(self, url: str) -> dict:
        feature_dict = extract_features_from_url(url)
        X = pd.DataFrame([feature_dict])[self.feature_columns]
        prob = float(self.model.predict_proba(X)[0][1])
        label = "phishing" if prob >= 0.5 else "legitimate"
        risk_score = max(1, min(99, int(round(prob * 100))))
        reasons = extract_reason_flags(url, feature_dict)
        return {
            "url": url,
            "prediction": label,
            "phishing_probability": round(prob, 4),
            "risk_score": risk_score,
            "reasons": reasons,
            "features": feature_dict,
        }

    def predict_batch(self, urls: list[str]) -> list[dict]:
        return [self.predict_one(url) for url in urls]
