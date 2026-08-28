from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_phase7_datasets_and_experiments():
    """Verify Phase 7 Datasets & Experiments API endpoints."""
    # 1. Create Dataset
    res = client.post(
        "/api/v1/datasets",
        json={"name": "Golden Support Queries", "description": "Customer support benchmark cases"},
    )
    assert res.status_code == 201
    ds = res.json()
    ds_id = ds["dataset_id"]
    assert ds["name"] == "Golden Support Queries"

    # 2. Add Dataset Case
    case_payload = {
        "case_id": "case_001",
        "input_data": {"query": "Refund order #100"},
        "expected_output": "Refund processed.",
    }
    case_res = client.post(f"/api/v1/datasets/{ds_id}/cases", json=case_payload)
    assert case_res.status_code == 200
    assert len(case_res.json()["cases"]) == 1

    # 3. Run Experiment
    exp_res = client.post(
        "/api/v1/datasets/experiments/run",
        json={
            "experiment_id": "exp_v1_vs_v2",
            "dataset_id": ds_id,
            "agent_id": "support_agent",
            "agent_version": "1.0.0",
        },
    )
    assert exp_res.status_code == 200
    exp = exp_res.json()
    assert exp["total_cases"] == 1
    assert exp["overall_accuracy"] == 1.0
