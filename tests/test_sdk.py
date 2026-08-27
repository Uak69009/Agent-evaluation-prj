from agentevalops import AgentEvalOps


def test_sdk_init():
    client = AgentEvalOps(api_key="test-key-123", api_url="http://localhost:8000")
    assert client.config.api_key == "test-key-123"
    assert client.config.api_url == "http://localhost:8000"


def test_sdk_tracer_context():
    client = AgentEvalOps(api_key="test-key-123")
    with client.tracer.start_trace("unit_test_trace") as ctx:
        span_id = ctx.add_span("tool_call_span", {"tool": "calculator"})
        assert span_id == "span_1"
        assert len(ctx.spans) == 1
