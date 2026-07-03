"""Application configuration values."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Central settings for the FastAPI application."""

    app_title: str = "Diaper ML Prediction API"
    app_version: str = "1.0.0"
    app_description: str = "Backend service for Diaper ML Widget"


settings = Settings()
