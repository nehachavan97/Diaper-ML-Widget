"""Prediction engine abstraction backed by trained regression models."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from app.models.prediction import PredictionRequest, PredictionResponse

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_DIR = PROJECT_ROOT / "models"


class BasePredictor:
    """Abstract interface for prediction backends."""

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        raise NotImplementedError


class Predictor(BasePredictor):
    """Load persisted regression models and produce predictions for the API."""

    def __init__(self) -> None:
        self.material_cost_model = self._load_model("material_cost_model.pkl", "materialCost_model.pkl")
        self.absorption_model = self._load_model("absorption_model.pkl")
        self.feature_columns = [
            "diaperSize",
            "topsheetMaterial",
            "sapType",
            "pulpType",
            "additives",
            "supplier",
            "sapRatio",
            "coreGsm",
            "hydroScore",
            "channels",
            "coreShaping",
        ]

    def _load_model(self, *candidate_names: str) -> Any:
        for name in candidate_names:
            model_path = MODEL_DIR / name
            if model_path.exists():
                return joblib.load(model_path)
        raise FileNotFoundError(f"No model artifacts found in {MODEL_DIR} for {candidate_names}")

    def _build_frame(self, request: PredictionRequest) -> pd.DataFrame:
        return pd.DataFrame([request.model_dump()], columns=self.feature_columns)

    def _predict_with_model(self, model: Any, request: PredictionRequest) -> float:
        frame = self._build_frame(request)
        prediction = model.predict(frame)[0]
        return float(prediction)

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        material_cost = self._predict_with_model(self.material_cost_model, request)
        absorption = self._predict_with_model(self.absorption_model, request)
        confidence = round(
            min(99.9, max(85.0, 97.0 - abs(material_cost - 0.22) * 100 + abs(absorption - 7000) / 1000)),
            1,
        )

        if material_cost > 0.26 or absorption > 7800:
            prediction = "Premium Quality"
        elif material_cost < 0.18 or absorption < 6200:
            prediction = "Economy Quality"
        else:
            prediction = "Balanced Quality"

        return PredictionResponse(
            materialCost=round(material_cost, 3),
            absorption=int(round(absorption)),
            confidence=confidence,
            prediction=prediction,
        )
