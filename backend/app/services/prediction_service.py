"""Application service layer for prediction use cases."""

from app.ml.predictor import BasePredictor, Predictor
from app.models.prediction import PredictionRequest, PredictionResponse


class PredictionService:
    """Orchestrates request handling and delegates prediction work."""

    def __init__(self, predictor: BasePredictor | None = None) -> None:
        self.predictor = predictor or Predictor()

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """Invoke the configured predictor engine and return a response."""
        return self.predictor.predict(request)
