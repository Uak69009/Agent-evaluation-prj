import logging
from typing import Any

from agentevalops_schemas.trace import SpanStatus, TraceSchema

logger = logging.getLogger("agentevalops.worker.trace")


class TraceWorker:
    """Async background worker for trace processing, metric rollup, and normalization."""

    def __init__(self) -> None:
        self.processed_count = 0

    def process_trace(self, trace_data: dict[str, Any] | TraceSchema) -> dict[str, Any]:
        """Normalize trace schema, rollup span execution metrics, and compute stats."""
        if isinstance(trace_data, dict):
            trace = TraceSchema.model_validate(trace_data)
        else:
            trace = trace_data

        total_spans = len(trace.spans)
        total_tokens = 0
        total_cost_usd = 0.0
        tool_call_count = 0
        llm_span_count = 0
        error_count = 0

        for span in trace.spans:
            if span.status == SpanStatus.ERROR or span.error_message:
                error_count += 1
            if span.llm:
                llm_span_count += 1
                if span.llm.total_tokens:
                    total_tokens += span.llm.total_tokens
                if span.llm.cost_usd:
                    total_cost_usd += span.llm.cost_usd
            if span.tool_call:
                tool_call_count += 1

        summary = {
            "trace_id": trace.trace_id,
            "run_id": trace.run_id,
            "agent_id": trace.agent_id,
            "status": trace.status.value,
            "duration_ms": trace.duration_ms or 0.0,
            "total_spans": total_spans,
            "llm_span_count": llm_span_count,
            "tool_call_count": tool_call_count,
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost_usd, 6),
            "error_count": error_count,
        }

        self.processed_count += 1
        logger.info(f"Processed trace {trace.trace_id}: {summary}")
        return summary
