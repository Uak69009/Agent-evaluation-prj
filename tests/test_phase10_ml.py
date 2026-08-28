from agentevalops_ml.predictor import FailurePredictor
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_phase10_ml_failure_prediction():
    """Verify Phase 10 FailurePredictor ML model and API routes."""
    predictor = FailurePredictor()

    # 1. Normal Trace Prediction
    normal_trace = {"duration_ms": 500.0, "spans": [{"status": "ok"}]}
    res_normal = predictor.predict_failure_risk(normal_trace)
    assert res_normal.predicted_failure is False
    assert res_normal.risk_level == "LOW"

    # 2. High Risk Trace Prediction
    risky_trace = {
        "duration_ms": 6000.0,
        "spans": [{"status": "error", "error_message": "Timeout"}] * 5,
    }
    res_risky = predictor.predict_failure_risk(risky_trace)
    assert res_risky.predicted_failure is True
    assert res_risky.risk_level in ("HIGH", "CRITICAL")

    # 3. Test API Endpoint POST /api/v1/failure-intelligence/predict
    api_res = client.post("/api/v1/failure-intelligence/predict", json={"trace_data": risky_trace})
    assert api_res.status_code == 200
    assert api_res.json()["predicted_failure"] is True
