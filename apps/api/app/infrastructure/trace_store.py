
from agentevalops_schemas.trace import TraceSchema


class TraceStore:
    """In-Memory and Database persistence manager for AgentEvalOps Traces."""

    def __init__(self) -> None:
        self._traces: dict[str, TraceSchema] = {}

    def save_trace(self, trace: TraceSchema) -> TraceSchema:
        self._traces[trace.trace_id] = trace
        return trace

    def save_batch(self, traces: list[TraceSchema]) -> list[TraceSchema]:
        for t in traces:
            self.save_trace(t)
        return traces

    def get_trace(self, trace_id: str) -> TraceSchema | None:
        return self._traces.get(trace_id)

    def list_traces(
        self,
        project_id: str | None = None,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[TraceSchema]:
        results = list(self._traces.values())
        if project_id:
            results = [t for t in results if t.project_id == project_id]
        if status:
            results = [t for t in results if t.status.value.lower() == status.lower()]

        # Sort newest first
        results.sort(key=lambda t: t.start_time, reverse=True)
        return results[offset : offset + limit]

    def count_traces(self) -> int:
        return len(self._traces)

    def clear(self) -> None:
        self._traces.clear()


# Global Singleton Store for Ingestion
trace_store = TraceStore()
