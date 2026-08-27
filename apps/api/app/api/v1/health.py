from typing import Any

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.infrastructure.database import get_db_session
from app.infrastructure.redis import get_redis_client

router = APIRouter(tags=["Health & Status"])


@router.get("/health", summary="Basic service health check")
async def health_check() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "version": settings.APP_VERSION,
    }


@router.get("/health/live", summary="Liveness check for container orchestration")
async def liveness_check() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/health/ready", summary="Readiness check for database and cache dependencies")
async def readiness_check(
    db: AsyncSession = Depends(get_db_session),
    redis: aioredis.Redis = Depends(get_redis_client),
) -> dict[str, Any]:
    db_status = "ok"
    redis_status = "ok"

    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    try:
        await redis.ping()
    except Exception as e:
        redis_status = f"error: {str(e)}"

    is_ready = (db_status == "ok") and (redis_status == "ok")

    return {
        "status": "ready" if is_ready else "degraded",
        "components": {
            "database": db_status,
            "redis": redis_status,
        },
    }


@router.get("/version", summary="Platform API version endpoint")
async def version_check() -> dict[str, str]:
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "api_prefix": settings.API_PREFIX,
    }
