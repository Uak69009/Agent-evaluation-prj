from fastapi.testclient import TestClient

from agentevalops_eval.deterministic import (
    CostLimitEvaluator,
    ExactMatchEvaluator,
    LatencyLimitEvaluator,
    RequiredConditionsEvaluator,
    ToolCallValidityEvaluator,
)
from agentevalops_eval.engine import evaluation_engine
from agentevalops_schemas.eval import EvaluationStatus
from app.main import app

client = TestClient(app)


def test_deterministic_evaluators_unit():
    """Unit test individual deterministic rule evaluators."""
    # 1. Exact Match Evaluator
    exact_eval = ExactMatchEvaluator()
    res1 = exact_eval.evaluate({"output": "Paris"}, context={"expected_output": "Paris"})
    assert res1.status == EvaluationStatus.PASSED
    assert res1.score == 1.0

    res1_fail = exact_eval.evaluate({"output": "London"}, context={"expected_output": "Paris"})
    assert res1_fail.status == EvaluationStatus.FAILED
    assert res1_fail.score == 0.0

    # 2. Tool Call Validity Evaluator
    tool_eval = ToolCallValidityEvaluator()
    run_with_tools = {
        "spans": [
            {"span_type": "tool", "tool_call": {"name": "search", "arguments": {}}},
            {"span_type": "tool", "tool_call": {"name": "calc", "error": "Division by zero"}},
        ]
    }
    res2 = tool_eval.evaluate(run_with_tools)
    assert res2.status == EvaluationStatus.FAILED
    assert res2.score == 0.5

    # 3. Latency Limit Evaluator
    latency_eval = LatencyLimitEvaluator()
    res3 = latency_eval.evaluate({"duration_ms": 1200.0}, context={"max_latency_ms": 2000.0})
    assert res3.status == EvaluationStatus.PASSED

    # 4. Cost Limit Evaluator
    cost_eval = CostLimitEvaluator()
    run_cost = {"spans": [{"llm": {"cost_usd": 0.002}}, {"llm": {"cost_usd": 0.003}}]}
    res4 = cost_eval.evaluate(run_cost, context={"max_cost_usd": 0.01})
    assert res4.status == EvaluationStatus.PASSED

    # 5. Required Conditions Evaluator
    cond_eval = RequiredConditionsEvaluator()
    res5 = cond_eval.evaluate(
        {"output": "Order refund processed successfully for user."},
        context={"required_keywords": ["refund", "processed"]},
    )
    assert res5.status == EvaluationStatus.PASSED


def test_evaluation_engine_and_api():
    """Integration test EvaluationEngine and FastAPI /api/v1/evaluations routes."""
    sample_run = {
        "output": "Portfolio rebalanced successfully.",
        "duration_ms": 1500.0,
        "spans": [
            {"span_type": "tool", "tool_call": {"name": "broker_api", "arguments": {}}},
            {"llm": {"cost_usd": 0.001}},
        ],
    }

    # 1. Engine Direct Execution
    suite_res = evaluation_engine.evaluate_run(
        run_data=sample_run,
        context={
            "expected_output": "Portfolio rebalanced successfully.",
            "max_latency_ms": 3000.0,
            "max_cost_usd": 0.05,
            "required_keywords": ["portfolio", "rebalanced"],
        },
    )
    assert suite_res.overall_status == EvaluationStatus.PASSED
    assert suite_res.total_evaluators == 5
    assert suite_res.passed_count == 5

    # 2. Test GET /api/v1/evaluations/evaluators
    eval_res = client.get("/api/v1/evaluations/evaluators")
    assert eval_res.status_code == 200
    evaluators_list = eval_res.json()
    names = [e["name"] for e in evaluators_list]
    assert "exact_match" in names
    assert "tool_call_validity" in names
    assert "latency_limit" in names

    # 3. Test POST /api/v1/evaluations/run Endpoint
    post_res = client.post(
        "/api/v1/evaluations/run",
        json={
            "run_data": sample_run,
            "context": {
                "expected_output": "Portfolio rebalanced successfully.",
                "max_latency_ms": 3000.0,
            },
        },
    )
    assert post_res.status_code == 200
    res_data = post_res.json()
    assert res_data["overall_status"] == "passed"
    assert res_data["total_evaluators"] == 5
