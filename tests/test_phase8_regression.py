from fastapi.testclient import TestClient

from agentevalops_eval.gate import DeploymentGateEngine, PolicyProfile
from app.main import app

client = TestClient(app)


def test_phase8_deployment_gate():
    """Verify Phase 8 Deployment Gate engine and API endpoint."""
    engine = DeploymentGateEngine()

    # 1. PASS Decision
    res_pass = engine.evaluate_gate(
        candidate_metrics={"accuracy": 0.95, "cost_usd": 0.010, "duration_ms": 1050.0},
        baseline_metrics={"accuracy": 0.94, "cost_usd": 0.010, "duration_ms": 1000.0},
    )
    assert res_pass.decision == "PASS"
    assert res_pass.passed is True

    # 2. BLOCK Decision (Accuracy Regression)
    res_block = engine.evaluate_gate(
        candidate_metrics={"accuracy": 0.85, "cost_usd": 0.010, "duration_ms": 1000.0},
        policy=PolicyProfile(minimum_task_success=0.90),
    )
    assert res_block.decision == "BLOCK"
    assert res_block.passed is False

    # 3. Test API Endpoint POST /api/v1/gates/evaluate
    api_res = client.post(
        "/api/v1/gates/evaluate",
        json={
            "candidate_metrics": {"accuracy": 0.96, "cost_usd": 0.011, "duration_ms": 1100.0},
            "baseline_metrics": {"accuracy": 0.95, "cost_usd": 0.010, "duration_ms": 1000.0},
        },
    )
    assert api_res.status_code == 200
    assert api_res.json()["decision"] == "PASS"
