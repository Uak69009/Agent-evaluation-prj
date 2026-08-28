from typing import Any

from pydantic import BaseModel, Field

from app.infrastructure.trace_store import trace_store


class ModelMetrics(BaseModel):
    model: str
    call_count: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    avg_latency_ms: float = 0.0


class ToolMetrics(BaseModel):
    tool_name: str
    call_count: int = 0
    success_count: int = 0
    error_count: int = 0
    avg_duration_ms: float = 0.0


class AnalyticsOverview(BaseModel):
    total_traces: int = 0
    total_spans: int = 0
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_cost_usd: float = 0.0
    avg_duration_ms: float = 0.0
    error_rate_pct: float = 0.0
    models_summary: list[ModelMetrics] = Field(default_factory=list)
    tools_summary: list[ToolMetrics] = Field(default_factory=list)


class AnalyticsEngine:
    """Computes real-time observability metrics over trace and span telemetry."""

    def get_overview(self, project_id: str | None = None) -> AnalyticsOverview:
        traces = trace_store.list_traces(project_id=project_id, limit=5000)
        total_traces = len(traces)
        if total_traces == 0:
            return AnalyticsOverview()

        total_spans = 0
        total_tokens = 0
        prompt_tokens = 0
        completion_tokens = 0
        total_cost_usd = 0.0
        total_duration_ms = 0.0
        error_traces = 0

        model_map: dict[str, dict[str, Any]] = {}
        tool_map: dict[str, dict[str, Any]] = {}

        for t in traces:
            if t.status.value.lower() == "error":
                error_traces += 1
            if t.duration_ms:
                total_duration_ms += t.duration_ms

            for s in t.spans:
                total_spans += 1
                # Aggregate LLM metrics
                if s.llm:
                    m_name = s.llm.model or "unknown_model"
                    if m_name not in model_map:
                        model_map[m_name] = {
                            "model": m_name,
                            "call_count": 0,
                            "prompt_tokens": 0,
                            "completion_tokens": 0,
                            "total_tokens": 0,
                            "total_cost_usd": 0.0,
                            "durations": [],
                        }
                    m_entry = model_map[m_name]
                    m_entry["call_count"] += 1
                    p_tok = s.llm.prompt_tokens or 0
                    c_tok = s.llm.completion_tokens or 0
                    tot_tok = s.llm.total_tokens or (p_tok + c_tok)
                    cost = s.llm.cost_usd or 0.0

                    m_entry["prompt_tokens"] += p_tok
                    m_entry["completion_tokens"] += c_tok
                    m_entry["total_tokens"] += tot_tok
                    m_entry["total_cost_usd"] += cost
                    if s.duration_ms:
                        m_entry["durations"].append(s.duration_ms)

                    prompt_tokens += p_tok
                    completion_tokens += c_tok
                    total_tokens += tot_tok
                    total_cost_usd += cost

                # Aggregate Tool metrics
                if s.tool_call:
                    t_name = s.tool_call.name or "unknown_tool"
                    if t_name not in tool_map:
                        tool_map[t_name] = {
                            "tool_name": t_name,
                            "call_count": 0,
                            "success_count": 0,
                            "error_count": 0,
                            "durations": [],
                        }
                    t_entry = tool_map[t_name]
                    t_entry["call_count"] += 1
                    if s.status.value.lower() == "error" or s.tool_call.error:
                        t_entry["error_count"] += 1
                    else:
                        t_entry["success_count"] += 1
                    if s.duration_ms:
                        t_entry["durations"].append(s.duration_ms)

        # Build Model Metrics
        models_summary = []
        for m_data in model_map.values():
            durs = m_data["durations"]
            avg_lat = sum(durs) / len(durs) if durs else 0.0
            models_summary.append(
                ModelMetrics(
                    model=m_data["model"],
                    call_count=m_data["call_count"],
                    prompt_tokens=m_data["prompt_tokens"],
                    completion_tokens=m_data["completion_tokens"],
                    total_tokens=m_data["total_tokens"],
                    total_cost_usd=round(m_data["total_cost_usd"], 6),
                    avg_latency_ms=round(avg_lat, 2),
                )
            )

        # Build Tool Metrics
        tools_summary = []
        for t_data in tool_map.values():
            durs = t_data["durations"]
            avg_dur = sum(durs) / len(durs) if durs else 0.0
            tools_summary.append(
                ToolMetrics(
                    tool_name=t_data["tool_name"],
                    call_count=t_data["call_count"],
                    success_count=t_data["success_count"],
                    error_count=t_data["error_count"],
                    avg_duration_ms=round(avg_dur, 2),
                )
            )

        avg_dur_overall = round(total_duration_ms / total_traces, 2)
        err_rate = round((error_traces / total_traces) * 100, 2)

        return AnalyticsOverview(
            total_traces=total_traces,
            total_spans=total_spans,
            total_tokens=total_tokens,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_cost_usd=round(total_cost_usd, 6),
            avg_duration_ms=avg_dur_overall,
            error_rate_pct=err_rate,
            models_summary=models_summary,
            tools_summary=tools_summary,
        )


analytics_engine = AnalyticsEngine()
