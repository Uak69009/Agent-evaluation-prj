from typing import Any

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from agentevalops_eval.engine import EvaluationSuiteRunSchema, evaluation_engine
from agentevalops_eval.registry import evaluator_registry
from app.infrastructure.trace_store import trace_store

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])


class RunEvaluationRequest(BaseModel):
    trace_id: str | None = Field(None, description="Optional ingested trace ID to evaluate")
    run_data: dict[str, Any] | None = Field(None, description="Optional inline run/trace data payload")
    evaluators: list[str] | None = Field(None, description="List of evaluator names to execute")
    context: dict[str, Any] | None = Field(None, description="Context (expected_output, SLA limits, keywords)")


# In-memory store for evaluation suite run records
evaluation_history: list[dict[str, Any]] = []


@router.post(
    "/run",
    response_model=EvaluationSuiteRunSchema,
    status_code=status.HTTP_200_OK,
    summary="Execute evaluation suite against an agent run or trace",
)
async def run_evaluation(payload: RunEvaluationRequest) -> EvaluationSuiteRunSchema:
    """Execute rule-based evaluators against a target trace ID or inline run payload."""
    data_to_eval = payload.run_data or {}
    if payload.trace_id:
        t = trace_store.get_trace(payload.trace_id)
        if not t:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trace with ID '{payload.trace_id}' not found.",
            )
        data_to_eval = t.model_dump(mode="json")

    if not data_to_eval:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'trace_id' or 'run_data' must be provided.",
        )

    res = evaluation_engine.evaluate_run(
        run_data=data_to_eval,
        evaluator_names=payload.evaluators,
        context=payload.context,
    )

    # Save to history
    record = {
        "trace_id": payload.trace_id,
        "overall_status": res.overall_status.value,
        "overall_score": res.overall_score,
        "total_evaluators": res.total_evaluators,
        "passed_count": res.passed_count,
        "failed_count": res.failed_count,
    }
    evaluation_history.append(record)
    return res


@router.get(
    "/evaluators",
    summary="List available registered evaluators",
)
async def list_evaluators() -> list[dict[str, str]]:
    """Retrieve list of registered evaluators and descriptions."""
    return evaluator_registry.list_evaluators()


@router.get(
    "",
    summary="List evaluation run history",
)
async def list_evaluation_history(
    limit: int = Query(50, ge=1, le=500),
) -> list[dict[str, Any]]:
    """Retrieve history of completed evaluation suite runs."""
    return evaluation_history[-limit:]
