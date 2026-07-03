# Diaper ML Widget Backend

This backend provides a modular FastAPI service for diaper prediction.

## Structure

- app/main.py: Application entry point
- app/api/prediction.py: Prediction API routes
- app/models/prediction.py: Pydantic request and response models
- app/services/prediction_service.py: Business logic orchestration
- app/ml/predictor.py: Mock prediction engine placeholder
- app/core/config.py: Application settings

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
