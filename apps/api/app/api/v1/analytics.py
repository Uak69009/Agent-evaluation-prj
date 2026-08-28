
from fastapi import APIRouter, Query

from app.infrastructure.analytics import (
    AnalyticsOverview,
    ModelMetrics,
    ToolMetrics,
    analytics_engine,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/overview",
    response_model=AnalyticsOverview,
    summary="Get aggregated telemetry analytics overview",
)
async def get_analytics_overview(
    project_id: str | None = Query(None, description="Filter analytics by project ID"),
) -> AnalyticsOverview:
    """Retrieve top-level platform analytics including cost, token metrics, and error rates."""
    return analytics_engine.get_overview(project_id=project_id)


@router.get(
    "/models",
    response_model=list[ModelMetrics],
    summary="Get LLM model performance breakdown",
)
async def get_model_analytics(
    project_id: str | None = Query(None, description="Filter analytics by project ID"),
) -> list[ModelMetrics]:
    """Retrieve usage, cost, and latency breakdown by LLM model."""
    overview = analytics_engine.get_overview(project_id=project_id)
    return overview.models_summary


@router.get(
    "/tools",
    response_model=list[ToolMetrics],
    summary="Get agent tool call performance breakdown",
)
async def get_tool_analytics(
    project_id: str | None = Query(None, description="Filter analytics by project ID"),
) -> list[ToolMetrics]:
    """Retrieve tool execution metrics, success/error rates, and duration breakdown."""
    overview = analytics_engine.get_overview(project_id=project_id)
    return overview.tools_summary
