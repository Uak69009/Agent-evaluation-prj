from typing import Any

from pydantic import BaseModel, Field


class DatasetCaseSchema(BaseModel):
    case_id: str
    input_data: dict[str, Any]
    expected_output: Any | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DatasetSchema(BaseModel):
    dataset_id: str
    name: str
    description: str | None = None
    organization_id: str = "org_default"
    project_id: str = "proj_default"
    cases: list[DatasetCaseSchema] = Field(default_factory=list)


class ExperimentRunSchema(BaseModel):
    experiment_id: str
    dataset_id: str
    agent_id: str
    agent_version: str
    status: str = "completed"
    total_cases: int = 0
    passed_cases: int = 0
    failed_cases: int = 0
    overall_accuracy: float = 0.0
