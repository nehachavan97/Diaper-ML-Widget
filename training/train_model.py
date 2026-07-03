from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "dataset" / "diaper_training_data.csv"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_COLUMNS = [
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
TARGET_COLUMNS = ["materialCost", "absorption"]
CATEGORICAL_COLUMNS = [
    "diaperSize",
    "topsheetMaterial",
    "sapType",
    "pulpType",
    "additives",
    "supplier",
    "coreShaping",
]
NUMERIC_COLUMNS = ["sapRatio", "coreGsm", "hydroScore", "channels"]


def build_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
            ("numeric", "passthrough", NUMERIC_COLUMNS),
        ],
        remainder="drop",
    )
    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", RandomForestRegressor(n_estimators=250, random_state=42, n_jobs=-1)),
        ]
    )


def main() -> None:
    frame = pd.read_csv(DATA_PATH)
    if frame.empty:
        raise ValueError(f"Training data is empty at {DATA_PATH}")

    for target_name in TARGET_COLUMNS:
        model = build_pipeline()
        model.fit(frame[FEATURE_COLUMNS], frame[target_name])
        artifact_name = "material_cost_model.pkl" if target_name == "materialCost" else "absorption_model.pkl"
        joblib.dump(model, MODEL_DIR / artifact_name)

        predictions = model.predict(frame[FEATURE_COLUMNS])
        score = r2_score(frame[target_name], predictions)
        print(f"Trained {target_name} model with R^2={score:.3f}")

    print(f"Saved model artifacts to {MODEL_DIR}")


if __name__ == "__main__":
    main()
