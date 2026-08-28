from typing import Any

from agentevalops_eval.evaluators import TrajectoryEvaluator
from agentevalops_schemas.eval import EvaluationResultSchema, EvaluationStatus, SeverityLevel


class StepEfficiencyEvaluator(TrajectoryEvaluator):
    """Evaluates agent execution step efficiency and checks for redundant or infinite loops."""

    name = "step_efficiency"
    version = "1.0.0"
    description = "Checks that agent step sequence is concise without infinite loops or excessive tool retries"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        ctx = context or {}
        max_steps = ctx.get("max_allowed_steps", 10)
        spans = run_data.get("spans", [])
        total_steps = len(spans)

        # Loop detection: repeated tool names sequentially
        tool_names = [s.get("name") for s in spans if s.get("span_type") == "tool"]
        has_loop = False
        if len(tool_names) >= 3:
            for i in range(len(tool_names) - 2):
                if tool_names[i] == tool_names[i + 1] == tool_names[i + 2]:
                    has_loop = True
                    break

        if has_loop:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=0.0,
                status=EvaluationStatus.FAILED,
                reason="Detected infinite loop or repeated tool calls (>2 consecutive identical tools).",
                severity=SeverityLevel.HIGH,
            )

        if total_steps <= max_steps:
            score = 1.0
            status = EvaluationStatus.PASSED
            reason = f"Execution step efficiency passed ({total_steps}/{max_steps} allowed steps)."
        else:
            score = round(max_steps / total_steps, 2)
            status = EvaluationStatus.FAILED
            reason = f"Agent exceeded maximum allowed step threshold ({total_steps}/{max_steps} steps)."

        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=score,
            status=status,
            reason=reason,
            severity=SeverityLevel.MEDIUM if status == EvaluationStatus.FAILED else SeverityLevel.INFO,
        )


class RecoveryEvaluator(TrajectoryEvaluator):
    """Evaluates agent resilience and recovery after encountering intermediate errors."""

    name = "trajectory_recovery"
    version = "1.0.0"
    description = "Assesses whether agent successfully recovered after initial tool/step failures"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        spans = run_data.get("spans", [])
        has_initial_error = any(s.get("status") == "error" or s.get("error_message") for s in spans[:-1])
        final_status = run_data.get("status", "ok")

        if not has_initial_error:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.PASSED,
                reason="Clean trajectory execution with zero intermediate errors.",
            )

        if str(final_status).lower() == "ok":
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.PASSED,
                reason="Agent successfully self-corrected and recovered after an intermediate error.",
            )
        else:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=0.0,
                status=EvaluationStatus.FAILED,
                reason="Agent failed to recover after intermediate step failure.",
                severity=SeverityLevel.HIGH,
            )
