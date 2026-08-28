from fastapi.testclient import TestClient

from agentevalops.client import AgentEvalOps
from agentevalops.tracer import AgentTracer
from agentevalops_schemas.trace import SpanStatus, SpanType
from app.infrastructure.trace_store import trace_store
from app.main import app
from services.workers.trace_worker import TraceWorker

client = TestClient(app)


def test_phase1_full_e2e_pipeline():
    """End-to-end telemetry verification: SDK -> Ingestion API -> Worker -> Store -> Query API."""
    # 1. Reset Store
    trace_store.clear()

    # 2. Simulate AI Agent Execution with Python SDK
    sdk = AgentEvalOps(api_key="aeo_test_key_phase1")
    tracer = AgentTracer(client=sdk, auto_export=False)

    with tracer.trace(
        name="multi_step_reasoning_agent",
        agent_id="finance_advisor_v1",
        agent_version="1.0.0",
        project_id="proj_phase1_e2e",
    ) as trace_ctx:
        # LLM Span
        with trace_ctx.span("intent_recognition", span_type=SpanType.LLM) as s1:
            s1.set_llm_data(
                model="gpt-4o",
                provider="openai",
                prompt="Parse user portfolio request",
                completion="User wants tech stock analysis",
                prompt_tokens=120,
                completion_tokens=45,
                cost_usd=0.0008,
            )

        # Tool Span
        with trace_ctx.span("stock_ticker_api", span_type=SpanType.TOOL) as s2:
            s2.set_tool_call(
                name="get_stock_price",
                arguments={"ticker": "AAPL"},
                output={"price": 225.50, "currency": "USD"},
            )

    trace_schema = trace_ctx.to_schema()

    # 3. Verify SDK Schema Structure
    assert trace_schema.agent_id == "finance_advisor_v1"
    assert trace_schema.status == SpanStatus.OK
    assert len(trace_schema.spans) == 2
    assert trace_schema.spans[0].llm.model == "gpt-4o"
    assert trace_schema.spans[0].llm.total_tokens == 165

    # 4. Ingest Trace via FastAPI Endpoint using TestClient
    payload = trace_schema.model_dump(mode="json")
    res = client.post("/api/v1/traces", json=payload)
    assert res.status_code == 202
    res_data = res.json()
    assert res_data["status"] == "accepted"
    assert res_data["trace_id"] == trace_schema.trace_id

    # 5. Process Trace via Background Worker
    worker = TraceWorker()
    summary = worker.process_trace(trace_schema)
    assert summary["trace_id"] == trace_schema.trace_id
    assert summary["total_spans"] == 2
    assert summary["llm_span_count"] == 1
    assert summary["tool_call_count"] == 1
    assert summary["total_tokens"] == 165

    # 6. Query Ingested Trace via GET API
    query_res = client.get(f"/api/v1/traces/{trace_schema.trace_id}")
    assert query_res.status_code == 200
    retrieved_trace = query_res.json()
    assert retrieved_trace["trace_id"] == trace_schema.trace_id
    assert retrieved_trace["agent_id"] == "finance_advisor_v1"
    assert len(retrieved_trace["spans"]) == 2

    # 7. Query List API with Project Filter
    list_res = client.get("/api/v1/traces?project_id=proj_phase1_e2e")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total"] == 1
    assert list_data["traces"][0]["trace_id"] == trace_schema.trace_id
