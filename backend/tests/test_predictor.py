from app.models.prediction import PredictionRequest
from app.ml.predictor import Predictor


def test_predictor_returns_expected_contract() -> None:
    request = PredictionRequest(
        diaperSize="M",
        topsheetMaterial="Nonwoven",
        sapType="SuperAbsorbent",
        pulpType="SoftPulp",
        additives="NoAdditives",
        supplier="SupplierA",
        sapRatio=0.24,
        coreGsm=220,
        hydroScore=8.5,
        channels=3,
        coreShaping="Round",
    )

    response = Predictor().predict(request)

    assert response.materialCost >= 0
    assert response.absorption >= 0
    assert 0 <= response.confidence <= 100
    assert isinstance(response.prediction, str)
