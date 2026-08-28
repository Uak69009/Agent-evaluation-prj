from fastapi.testclient import TestClient

from agentevalops.client import AgentEvalOps
from agentevalops.tracer import AgentTracer
from agentevalops_schemas.trace import SpanType
from app.infrastructure.analytics import analytics_engine
from app.infrastructure.trace_store import trace_store
from app.main import app

client = TestClient(app)


def test_phase2_observability_analytics():
    """Verify Phase 2 telemetry analytics engine and API endpoints."""
    # 1. Reset Trace Store
    trace_store.clear()

    # 2. Ingest Sample Spans with LLM & Tool Telemetry
    sdk = AgentEvalOps(api_key="aeo_test_obs")
    tracer = AgentTracer(client=sdk, auto_export=False)

    with tracer.trace("obs_run_1", agent_id="obs_agent", project_id="proj_obs") as t1:
        with t1.span("llm_call_1", span_type=SpanType.LLM) as s1:
            s1.set_llm_data(
                model="gpt-4o",
                prompt_tokens=500,
                completion_tokens=150,
                total_tokens=650,
                cost_usd=0.005,
            )
        with t1.span("tool_call_1", span_type=SpanType.TOOL) as s2:
            s2.set_tool_call("web_search", {"query": "agent evaluation"}, output={"results": 5})

    with tracer.trace("obs_run_2", agent_id="obs_agent", project_id="proj_obs") as t2:
        with t2.span("llm_call_2", span_type=SpanType.LLM) as s3:
            s3.set_llm_data(
                model="claude-3-5-sonnet",
                prompt_tokens=300,
                completion_tokens=100,
                total_tokens=400,
                cost_usd=0.003,
            )
        with t2.span("tool_call_2", span_type=SpanType.TOOL) as s4:
            s4.set_tool_call("calculator", {"expr": "2+2"}, error="Syntax error in expression")

    # Ingest Traces via Store
    trace_store.save_trace(t1.to_schema())
    trace_store.save_trace(t2.to_schema())

    # 3. Test Analytics Engine Overview Calculation
    overview = analytics_engine.get_overview(project_id="proj_obs")
    assert overview.total_traces == 2
    assert overview.total_tokens == 1050
    assert overview.prompt_tokens == 800
    assert overview.completion_tokens == 250
    assert round(overview.total_cost_usd, 4) == 0.0080
    assert len(overview.models_summary) == 2
    assert len(overview.tools_summary) == 2

    # 4. Test GET /api/v1/analytics/overview Endpoint
    res = client.get("/api/v1/analytics/overview?project_id=proj_obs")
    assert res.status_code == 200
    data = res.json()
    assert data["total_traces"] == 2
    assert data["total_tokens"] == 1050

    # 5. Test GET /api/v1/analytics/models Endpoint
    models_res = client.get("/api/v1/analytics/models?project_id=proj_obs")
    assert models_res.status_code == 200
    models = models_res.json()
    model_names = [m["model"] for m in models]
    assert "gpt-4o" in model_names
    assert "claude-3-5-sonnet" in model_names

    # 6. Test GET /api/v1/analytics/tools Endpoint
    tools_res = client.get("/api/v1/analytics/tools?project_id=proj_obs")
    assert tools_res.status_code == 200
    tools = tools_res.json()
    tool_names = [t["tool_name"] for t in tools]
    assert "web_search" in tool_names
    assert "calculator" in tool_names

    calc_tool = next(t for t in tools if t["tool_name"] == "calculator")
    assert calc_tool["error_count"] == 1
