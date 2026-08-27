from collections.abc import Generator
from contextlib import contextmanager
from typing import Any


class TraceContext:
    def __init__(self, trace_id: str, name: str):
        self.trace_id = trace_id
        self.name = name
        self.spans: list[dict[str, Any]] = []

    def add_span(self, name: str, attributes: dict[str, Any] | None = None) -> str:
        span_id = f"span_{len(self.spans) + 1}"
        self.spans.append({"span_id": span_id, "name": name, "attributes": attributes or {}})
        return span_id


class TracerPlaceholder:
    """Trace context placeholder abstraction for Phase 0 SDK foundation."""

    def __init__(self, client: Any):
        self.client = client

    @contextmanager
    def start_trace(
        self, name: str, agent_id: str = "default_agent"
    ) -> Generator[TraceContext, None, None]:
        ctx = TraceContext(trace_id="trc_placeholder_001", name=name)
        try:
            yield ctx
        finally:
            # Trace completion placeholder
            pass
