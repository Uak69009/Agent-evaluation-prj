from typing import Any

from agentevalops_eval.evaluators import DeterministicEvaluator
from agentevalops_schemas.eval import EvaluationResultSchema, EvaluationStatus, SeverityLevel


class ExactMatchEvaluator(DeterministicEvaluator):
    """Evaluates whether agent output matches expected target exactly."""

    name = "exact_match"
    version = "1.0.0"
    description = "Exact string or structure match against expected output"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        ctx = context or {}
        expected = ctx.get("expected_output")
        actual = run_data.get("output") or run_data.get("final_answer")

        if expected is None:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.SKIPPED,
                reason="No 'expected_output' provided in context.",
            )

        match = str(actual).strip() == str(expected).strip()
        score = 1.0 if match else 0.0
        status = EvaluationStatus.PASSED if match else EvaluationStatus.FAILED
        reason = "Output matched expected target exactly." if match else f"Expected '{expected}', got '{actual}'."

        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=score,
            status=status,
            reason=reason,
            severity=SeverityLevel.HIGH if not match else SeverityLevel.INFO,
        )


class ToolCallValidityEvaluator(DeterministicEvaluator):
    """Evaluates whether all tool calls in trace spans executed without errors."""

    name = "tool_call_validity"
    version = "1.0.0"
    description = "Validates that tool calls executed successfully without schema/runtime errors"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        spans = run_data.get("spans", [])
        tool_spans = [s for s in spans if s.get("span_type") == "tool" or s.get("tool_call")]

        if not tool_spans:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.PASSED,
                reason="No tool calls recorded in trace.",
            )

        failed_tools = []
        for s in tool_spans:
            tc = s.get("tool_call") or {}
            err = s.get("error_message") or tc.get("error")
            status = s.get("status")
            if err or (status and str(status).lower() == "error"):
                failed_tools.append(tc.get("name") or s.get("name") or "unknown_tool")

        total = len(tool_spans)
        failed = len(failed_tools)
        passed = total - failed
        score = round(passed / total, 2)

        if failed == 0:
            status = EvaluationStatus.PASSED
            reason = f"All {total} tool calls executed successfully."
        else:
            status = EvaluationStatus.FAILED
            reason = f"{failed}/{total} tool calls failed: {', '.join(failed_tools)}."

        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=score,
            status=status,
            reason=reason,
            severity=SeverityLevel.HIGH if failed > 0 else SeverityLevel.INFO,
        )


class LatencyLimitEvaluator(DeterministicEvaluator):
    """Evaluates whether total trace duration complies with maximum SLA latency threshold."""

    name = "latency_limit"
    version = "1.0.0"
    description = "Checks total trace execution duration against maximum allowed SLA (ms)"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        ctx = context or {}
        max_ms = ctx.get("max_latency_ms", 5000.0)
        actual_ms = run_data.get("duration_ms") or 0.0

        if actual_ms <= max_ms:
            status = EvaluationStatus.PASSED
            score = 1.0
            reason = f"Execution duration ({actual_ms} ms) within SLA limit ({max_ms} ms)."
        else:
            status = EvaluationStatus.FAILED
            score = 0.0
            reason = f"Execution duration ({actual_ms} ms) exceeded SLA limit ({max_ms} ms)."

        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=score,
            status=status,
            reason=reason,
            severity=SeverityLevel.MEDIUM if actual_ms > max_ms else SeverityLevel.INFO,
        )


class CostLimitEvaluator(DeterministicEvaluator):
    """Evaluates whether total token consumption/cost remains within budget limits."""

    name = "cost_limit"
    version = "1.0.0"
    description = "Checks total USD cost and token counts against budget cap"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        ctx = context or {}
        max_cost = ctx.get("max_cost_usd", 0.05)
        spans = run_data.get("spans", [])

        total_cost = 0.0
        for s in spans:
            llm = s.get("llm") or {}
            if llm.get("cost_usd"):
                total_cost += llm.get("cost_usd")

        total_cost = round(total_cost, 6)

        if total_cost <= max_cost:
            status = EvaluationStatus.PASSED
            score = 1.0
            reason = f"Total USD cost (${total_cost}) within budget cap (${max_cost})."
        else:
            status = EvaluationStatus.FAILED
            score = 0.0
            reason = f"Total USD cost (${total_cost}) exceeded budget cap (${max_cost})."

        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=score,
            status=status,
            reason=reason,
            severity=SeverityLevel.HIGH if total_cost > max_cost else SeverityLevel.INFO,
        )


class RequiredConditionsEvaluator(DeterministicEvaluator):
    """Evaluates whether required keywords/strings exist in agent output."""

    name = "required_conditions"
    version = "1.0.0"
    description = "Validates that required strings/keywords are present in the final output"

    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        ctx = context or {}
        required = ctx.get("required_keywords", [])
        output = str(run_data.get("output") or run_data.get("final_answer") or "")

        if not required:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.SKIPPED,
                reason="No 'required_keywords' provided in context.",
            )

        missing = [kw for kw in required if kw.lower() not in output.lower()]
        passed = len(required) - len(missing)
        score = round(passed / len(required), 2)

        if not missing:
            status = EvaluationStatus.PASSED
            reason = f"All {len(required)} required keywords found in output."
        else:
            status = EvaluationStatus.FAILED
            reason = f"Missing required keywords: {', '.join(missing)}."

        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=score,
            status=status,
            reason=reason,
            severity=SeverityLevel.MEDIUM if missing else SeverityLevel.INFO,
        )
