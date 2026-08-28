import logging
from typing import Any

from pydantic import BaseModel, Field

from agentevalops_eval.deterministic import (
    CostLimitEvaluator,
    ExactMatchEvaluator,
    LatencyLimitEvaluator,
    RequiredConditionsEvaluator,
    ToolCallValidityEvaluator,
)
from agentevalops_eval.rag import (
    CitationQualityEvaluator,
    ContextPrecisionEvaluator,
    FaithfulnessEvaluator,
)
from agentevalops_eval.registry import evaluator_registry
from agentevalops_schemas.eval import EvaluationResultSchema, EvaluationStatus

logger = logging.getLogger("agentevalops.eval.engine")

# Auto-register default evaluators
evaluator_registry.register(ExactMatchEvaluator)
evaluator_registry.register(ToolCallValidityEvaluator)
evaluator_registry.register(LatencyLimitEvaluator)
evaluator_registry.register(CostLimitEvaluator)
evaluator_registry.register(RequiredConditionsEvaluator)
evaluator_registry.register(ContextPrecisionEvaluator)
evaluator_registry.register(FaithfulnessEvaluator)
evaluator_registry.register(CitationQualityEvaluator)


class EvaluationSuiteRunSchema(BaseModel):
    overall_status: EvaluationStatus
    overall_score: float
    total_evaluators: int
    passed_count: int
    failed_count: int
    results: list[EvaluationResultSchema] = Field(default_factory=list)


class EvaluationEngine:
    """Core Evaluation Engine for executing evaluation suites against agent runs and traces."""

    def evaluate_run(
        self,
        run_data: dict[str, Any],
        evaluator_names: list[str] | None = None,
        context: dict[str, Any] | None = None,
    ) -> EvaluationSuiteRunSchema:
        """Synchronously execute evaluation suite against run_data."""
        names = evaluator_names or [
            "exact_match",
            "tool_call_validity",
            "latency_limit",
            "cost_limit",
            "required_conditions",
        ]
        results: list[EvaluationResultSchema] = []

        for name in names:
            try:
                eval_cls = evaluator_registry.get(name)
                eval_inst = eval_cls()
                res = eval_inst.evaluate(run_data, context=context)
                results.append(res)
            except KeyError:
                logger.warning(f"Evaluator '{name}' not found in registry. Skipping.")
                results.append(
                    EvaluationResultSchema(
                        evaluator_name=name,
                        evaluator_version="unknown",
                        score=0.0,
                        status=EvaluationStatus.ERROR,
                        reason=f"Evaluator '{name}' is not registered.",
                    )
                )

        total = len(results)
        passed = sum(1 for r in results if r.status in (EvaluationStatus.PASSED, EvaluationStatus.SKIPPED))
        failed = sum(1 for r in results if r.status in (EvaluationStatus.FAILED, EvaluationStatus.ERROR))

        scores = [r.score for r in results if r.score is not None]
        avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0

        if failed == 0:
            overall_status = EvaluationStatus.PASSED
        elif passed > 0:
            overall_status = EvaluationStatus.WARNING
        else:
            overall_status = EvaluationStatus.FAILED

        return EvaluationSuiteRunSchema(
            overall_status=overall_status,
            overall_score=avg_score,
            total_evaluators=total,
            passed_count=passed,
            failed_count=failed,
            results=results,
        )


evaluation_engine = EvaluationEngine()
