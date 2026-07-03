"""API router for prediction endpoints."""

from fastapi import APIRouter, status

from app.models.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/predict", tags=["prediction"])
prediction_service = PredictionService()


@router.post("", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
def predict(request: PredictionRequest) -> PredictionResponse:
    """Receive a prediction request and return a prediction response."""
    return prediction_service.predict(request)
