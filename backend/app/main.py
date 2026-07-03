"""FastAPI application entry point for the Diaper ML Widget backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.prediction import router as prediction_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description=settings.app_description,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return basic service metadata for the API root endpoint."""
    return {
        "status": "Running",
        "service": "Diaper ML Prediction API",
    }


@app.get("/health")
def health_check() -> dict[str, bool]:
    """Return a simple health status for the backend service."""
    return {"healthy": True}
