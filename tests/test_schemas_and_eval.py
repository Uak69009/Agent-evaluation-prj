from datetime import UTC, datetime

from agentevalops_eval import DeterministicEvaluator
from agentevalops_schemas import (
    EvaluationResultSchema,
    EvaluationStatus,
    SpanSchema,
    SpanStatus,
    SpanType,
    TraceSchema,
)


class DummyExactMatchEvaluator(DeterministicEvaluator):
    name = "dummy_exact_match"
    version = "1.0.0"

    def evaluate(self, run_data, context=None):
        target = run_data.get("output")
        expected = (context or {}).get("expected")
        if target == expected:
            return EvaluationResultSchema(
                evaluator_name=self.name,
                evaluator_version=self.version,
                score=1.0,
                status=EvaluationStatus.PASSED,
                reason="Exact match verified",
            )
        return EvaluationResultSchema(
            evaluator_name=self.name,
            evaluator_version=self.version,
            score=0.0,
            status=EvaluationStatus.FAILED,
            reason=f"Expected {expected}, got {target}",
        )


def test_trace_and_span_schema():
    span = SpanSchema(
        span_id="spn_1",
        trace_id="trc_1",
        name="llm_call",
        span_type=SpanType.LLM,
        start_time=datetime.now(UTC),
        status=SpanStatus.OK,
    )
    trace = TraceSchema(
        trace_id="trc_1",
        run_id="run_1",
        agent_id="agt_1",
        agent_version="1.0.0",
        organization_id="org_1",
        project_id="prj_1",
        start_time=datetime.now(UTC),
        spans=[span],
    )
    assert len(trace.spans) == 1
    assert trace.spans[0].span_type == SpanType.LLM


def test_evaluator_interface():
    evaluator = DummyExactMatchEvaluator()
    res_pass = evaluator.evaluate({"output": "hello"}, {"expected": "hello"})
    assert res_pass.status == EvaluationStatus.PASSED
    assert res_pass.score == 1.0

    res_fail = evaluator.evaluate({"output": "hello"}, {"expected": "world"})
    assert res_fail.status == EvaluationStatus.FAILED
    assert res_fail.score == 0.0
