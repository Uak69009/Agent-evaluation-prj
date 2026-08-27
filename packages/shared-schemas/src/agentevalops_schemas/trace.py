from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SpanType(str, Enum):
    LLM = "llm"
    TOOL = "tool"
    RETRIEVAL = "retrieval"
    AGENT = "agent"
    EMBEDDING = "embedding"
    CUSTOM = "custom"


class SpanStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
    UNSET = "unset"


class ToolCallData(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    output: Any | None = None
    error: str | None = None


class RetrievalData(BaseModel):
    query: str
    documents: list[dict[str, Any]] = Field(default_factory=list)
    top_k: int = 5
    score_threshold: float | None = None


class LLMData(BaseModel):
    model: str
    provider: str
    prompt: Any | None = None
    completion: Any | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    cost_usd: float | None = None
    temperature: float | None = None


class SpanSchema(BaseModel):
    span_id: str
    trace_id: str
    parent_span_id: str | None = None
    name: str
    span_type: SpanType = SpanType.CUSTOM
    start_time: datetime
    end_time: datetime | None = None
    duration_ms: float | None = None
    status: SpanStatus = SpanStatus.UNSET
    error_message: str | None = None
    input: Any | None = None
    output: Any | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    llm: LLMData | None = None
    tool_call: ToolCallData | None = None
    retrieval: RetrievalData | None = None


class TraceSchema(BaseModel):
    trace_id: str
    run_id: str
    agent_id: str
    agent_version: str
    organization_id: str
    project_id: str
    start_time: datetime
    end_time: datetime | None = None
    duration_ms: float | None = None
    status: SpanStatus = SpanStatus.UNSET
    metadata: dict[str, Any] = Field(default_factory=dict)
    spans: list[SpanSchema] = Field(default_factory=list)
