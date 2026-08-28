from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from agentevalops_eval.gate import GateDecisionSchema, PolicyProfile, deployment_gate_engine

router = APIRouter(prefix="/gates", tags=["Deployment Gates"])


class EvaluateGateRequest(BaseModel):
    candidate_metrics: dict[str, Any]
    baseline_metrics: dict[str, Any] | None = None
    policy: PolicyProfile | None = None


@router.post("/evaluate", response_model=GateDecisionSchema)
async def evaluate_deployment_gate(payload: EvaluateGateRequest) -> GateDecisionSchema:
    return deployment_gate_engine.evaluate_gate(
        candidate_metrics=payload.candidate_metrics,
        baseline_metrics=payload.baseline_metrics,
        policy=payload.policy,
    )
