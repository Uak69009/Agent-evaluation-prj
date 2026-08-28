from agentevalops_eval.llm_judge import JudgeCalibrationEngine, RubricJudgeEvaluator
from agentevalops_schemas.eval import EvaluationStatus


def test_llm_judge_and_calibration():
    """Verify Phase 5 RubricJudgeEvaluator and JudgeCalibrationEngine."""
    # 1. Rubric Judge Evaluator
    judge = RubricJudgeEvaluator()
    res = judge.evaluate(
        {"output": "The current account balance is $12,450.00 USD."},
        context={"rubric": "Check if response contains explicit monetary figure and polite tone."},
    )
    assert res.evaluator_name == "rubric_judge"
    assert res.status == EvaluationStatus.PASSED
    assert res.score >= 0.70

    # 2. Judge Calibration Engine
    calibration = JudgeCalibrationEngine.calculate_agreement([0.90, 0.85, 0.95])
    assert calibration["mean_score"] == 0.90
    assert calibration["agreement_score"] >= 0.90
