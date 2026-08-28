from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class EvaluationStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"
    ERROR = "error"


class SeverityLevel(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EvaluationResultSchema(BaseModel):
    evaluator_name: str
    evaluator_version: str
    score: float | None = Field(None, ge=0.0, le=1.0)
    status: EvaluationStatus
    reason: str
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    severity: SeverityLevel = SeverityLevel.INFO
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
