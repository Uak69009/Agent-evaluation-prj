
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from agentevalops_schemas.trace import TraceSchema
from app.infrastructure.trace_store import trace_store

router = APIRouter(prefix="/traces", tags=["Traces"])


class IngestResponse(BaseModel):
    status: str = "accepted"
    trace_id: str
    run_id: str
    message: str = "Trace ingested successfully"


class BatchIngestRequest(BaseModel):
    traces: list[TraceSchema] = Field(..., min_length=1)


class BatchIngestResponse(BaseModel):
    status: str = "accepted"
    ingested_count: int
    trace_ids: list[str]


class TraceSummaryResponse(BaseModel):
    total: int
    limit: int
    offset: int
    traces: list[TraceSchema]


@router.post(
    "",
    response_model=IngestResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingest a single agent trace",
)
async def ingest_trace(trace: TraceSchema) -> IngestResponse:
    """Ingest a single telemetry trace with span hierarchy."""
    trace_store.save_trace(trace)
    return IngestResponse(
        status="accepted",
        trace_id=trace.trace_id,
        run_id=trace.run_id,
        message="Trace ingested successfully",
    )


@router.post(
    "/batch",
    response_model=BatchIngestResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingest a batch of agent traces",
)
async def ingest_trace_batch(payload: BatchIngestRequest) -> BatchIngestResponse:
    """Batch ingest multiple trace schemas."""
    trace_store.save_batch(payload.traces)
    trace_ids = [t.trace_id for t in payload.traces]
    return BatchIngestResponse(
        status="accepted",
        ingested_count=len(payload.traces),
        trace_ids=trace_ids,
    )


@router.get(
    "",
    response_model=TraceSummaryResponse,
    summary="Query agent traces",
)
async def list_traces(
    project_id: str | None = Query(None, description="Filter by project ID"),
    status_filter: str | None = Query(None, alias="status", description="Filter by status (ok, error)"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> TraceSummaryResponse:
    """Retrieve list of ingested traces with filtering and pagination."""
    traces = trace_store.list_traces(
        project_id=project_id, status=status_filter, limit=limit, offset=offset
    )
    total = trace_store.count_traces()
    return TraceSummaryResponse(
        total=total,
        limit=limit,
        offset=offset,
        traces=traces,
    )


@router.get(
    "/{trace_id}",
    response_model=TraceSchema,
    summary="Get detailed trace by ID",
)
async def get_trace(trace_id: str) -> TraceSchema:
    """Retrieve full trace details including span tree hierarchy."""
    trace = trace_store.get_trace(trace_id)
    if not trace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trace with ID '{trace_id}' not found",
        )
    return trace
