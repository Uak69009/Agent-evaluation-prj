from pydantic import BaseModel, Field


class TrajectoryFeatureVector(BaseModel):
    """Normalized feature vector extracted from an agent run trajectory."""

    total_spans: int = 0
    llm_span_count: int = 0
    tool_span_count: int = 0
    error_span_count: int = 0
    max_depth: int = 0
    total_duration_ms: float = 0.0
    total_cost_usd: float = 0.0
    total_tokens: int = 0
    retry_count: int = 0
    state_integrity_score: float = Field(1.0, ge=0.0, le=1.0)
