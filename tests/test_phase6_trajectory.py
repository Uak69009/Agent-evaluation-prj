from agentevalops_eval.trajectory import RecoveryEvaluator, StepEfficiencyEvaluator
from agentevalops_schemas.eval import EvaluationStatus


def test_trajectory_evaluators():
    """Verify Phase 6 StepEfficiencyEvaluator and RecoveryEvaluator."""
    # 1. Step Efficiency Evaluator (Normal)
    step_eval = StepEfficiencyEvaluator()
    normal_trace = {"spans": [{"name": "llm_1", "span_type": "llm"}, {"name": "tool_1", "span_type": "tool"}]}
    res = step_eval.evaluate(normal_trace, context={"max_allowed_steps": 5})
    assert res.evaluator_name == "step_efficiency"
    assert res.status == EvaluationStatus.PASSED

    # 2. Step Efficiency Evaluator (Infinite Loop)
    loop_trace = {
        "spans": [
            {"name": "fetch_api", "span_type": "tool"},
            {"name": "fetch_api", "span_type": "tool"},
            {"name": "fetch_api", "span_type": "tool"},
        ]
    }
    res_loop = step_eval.evaluate(loop_trace)
    assert res_loop.status == EvaluationStatus.FAILED
    assert res_loop.score == 0.0

    # 3. Recovery Evaluator
    rec_eval = RecoveryEvaluator()
    recovered_trace = {
        "status": "ok",
        "spans": [
            {"name": "query_db", "status": "error", "error_message": "Connection lost"},
            {"name": "retry_query_db", "status": "ok"},
        ],
    }
    res_rec = rec_eval.evaluate(recovered_trace)
    assert res_rec.status == EvaluationStatus.PASSED
