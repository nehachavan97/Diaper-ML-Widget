"""Pydantic models for prediction requests and responses."""

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Structured input payload for the prediction endpoint."""

    diaperSize: str = Field(..., min_length=1, description="Requested diaper size")
    topsheetMaterial: str = Field(..., min_length=1, description="Topsheet material")
    sapType: str = Field(..., min_length=1, description="Superabsorbent polymer type")
    pulpType: str = Field(..., min_length=1, description="Pulp type")
    additives: str = Field(..., min_length=1, description="Additives used")
    supplier: str = Field(..., min_length=1, description="Material supplier")
    sapRatio: float = Field(..., ge=0.0, description="Superabsorbent polymer ratio")
    coreGsm: int = Field(..., ge=0, description="Core grammage")
    hydroScore: float = Field(..., ge=0.0, description="Hydro score")
    channels: int = Field(..., ge=0, description="Number of channels")
    coreShaping: str = Field(..., min_length=1, description="Core shaping method")


class PredictionResponse(BaseModel):
    """Structured output payload for the prediction endpoint."""

    materialCost: float
    absorption: int
    confidence: float
    prediction: str
