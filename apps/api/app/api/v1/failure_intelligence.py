from typing import Any

from agentevalops_ml.predictor import FailurePredictionResult, failure_predictor
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/failure-intelligence", tags=["Failure Intelligence & ML"])


class PredictRequest(BaseModel):
    trace_data: dict[str, Any]


class FailureClusterSchema(BaseModel):
    cluster_id: str
    category: str
    count: int
    description: str


@router.post("/predict", response_model=FailurePredictionResult)
async def predict_trace_failure(payload: PredictRequest) -> FailurePredictionResult:
    return failure_predictor.predict_failure_risk(payload.trace_data)


@router.get("/clusters", response_model=list[FailureClusterSchema])
async def list_failure_clusters() -> list[FailureClusterSchema]:
    return [
        FailureClusterSchema(
            cluster_id="cluster_01",
            category="Tool Timeout",
            count=12,
            description="External API rate limits or HTTP connection timeouts",
        ),
        FailureClusterSchema(
            cluster_id="cluster_02",
            category="Context Window Truncation",
            count=5,
            description="Prompt exceeded model max context window",
        ),
    ]
