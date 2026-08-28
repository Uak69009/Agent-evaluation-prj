from fastapi import APIRouter

from app.api.v1.analytics import router as analytics_router
from app.api.v1.auth import router as auth_router
from app.api.v1.datasets import router as datasets_router
from app.api.v1.evaluations import router as evaluations_router
from app.api.v1.failure_intelligence import router as failure_intelligence_router
from app.api.v1.gates import router as gates_router
from app.api.v1.health import router as health_router
from app.api.v1.traces import router as traces_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(traces_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(evaluations_router)
api_v1_router.include_router(datasets_router)
api_v1_router.include_router(gates_router)
api_v1_router.include_router(failure_intelligence_router)
api_v1_router.include_router(auth_router)
