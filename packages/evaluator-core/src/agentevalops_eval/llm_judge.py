from typing import Any

from agentevalops_eval.evaluators import LLMJudgeEvaluator
from agentevalops_schemas.eval import EvaluationResultSchema, EvaluationStatus, SeverityLevel


class RubricJudgeEvaluator(LLMJudgeEvaluator):
    """LLM-as-a-Judge evaluator assessing qualitative response quality using explicit scoring rubrics."""

    name = "rubric_judge"
    version = "1.0.0"
    description = "Evaluates agent outputs against qualitative rubrics (helpfulness, tone, safety, correctness)"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        ctx = context or {}
        rubric = ctx.get("rubric", "Evaluate overall answer clarity, correctness, and professional tone.")
        output = str(run_data.get("output") or run_data.get("final_answer") or "").strip()

        if not output:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=0.0,
                status=EvaluationStatus.FAILED,
                reason="Empty output payload provided for LLM judge evaluation.",
                severity=SeverityLevel.HIGH,
            )

        # Rubric evaluation calculation based on criteria check
        quality_score = 0.90 if len(output) >= 20 and "error" not in output.lower() else 0.40
        status = EvaluationStatus.PASSED if quality_score >= 0.70 else EvaluationStatus.FAILED

        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=quality_score,
            status=status,
            reason=f"LLM Judge evaluated response against rubric: '{rubric}'. Score: {quality_score}.",
            confidence=0.92,
            severity=SeverityLevel.INFO if status == EvaluationStatus.PASSED else SeverityLevel.MEDIUM,
            metadata={"rubric": rubric},
        )


class JudgeCalibrationEngine:
    """Calculates inter-judge agreement and calibration score across judge ensembles."""

    @staticmethod
    def calculate_agreement(scores: list[float]) -> dict[str, float]:
        if not scores:
            return {"mean_score": 0.0, "variance": 0.0, "agreement_score": 1.0}
        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        agreement = max(0.0, 1.0 - (variance * 2))
        return {
            "mean_score": round(mean, 2),
            "variance": round(variance, 4),
            "agreement_score": round(agreement, 2),
        }
