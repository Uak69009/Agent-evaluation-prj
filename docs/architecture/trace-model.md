# Trace Data Model Specification

## 1. Normalized Trace Structure

A `Trace` represents a single execution graph of an agent handling a user task.

```text
Trace (trace_id, run_id, agent_id, status, duration_ms)
 │
 ├── Span: Agent Step (parent_span_id=None)
 │    │
 │    ├── Span: LLM Call (provider, model, prompt_tokens, completion_tokens, cost_usd)
 │    │
 │    ├── Span: Tool Execution (tool_name, arguments, output, error)
 │    │
 │    └── Span: Vector Retrieval (query, top_k, returned_documents)
```

## 2. Span Attributes & Schema

Each `SpanSchema` includes:
- `span_id`: Unique identifier (UUID/string)
- `trace_id`: Associated parent trace ID
- `parent_span_id`: Optional parent span ID for nested execution trees
- `span_type`: `LLM`, `TOOL`, `RETRIEVAL`, `AGENT`, `EMBEDDING`, or `CUSTOM`
- `start_time` & `end_time`: ISO 8601 timestamps
- `duration_ms`: Duration in milliseconds
- `status`: `OK`, `ERROR`, `UNSET`
- `attributes`: Key-value metadata dictionary
- Dedicated sub-objects: `LLMData`, `ToolCallData`, `RetrievalData`
