
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.infrastructure.rate_limiter import rate_limiter
from app.infrastructure.security import security_manager

router = APIRouter(prefix="/auth", tags=["Auth & Security"])


class CreateAPIKeyRequest(BaseModel):
    name: str
    environment: str | None = "test"


class APIKeyResponse(BaseModel):
    raw_key: str
    key_hash: str
    prefix: str
    name: str
    message: str = "Store raw_key securely. It will not be shown again."


@router.post("/api-keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(payload: CreateAPIKeyRequest) -> APIKeyResponse:
    gen = security_manager.generate_api_key(environment=payload.environment or "test")
    return APIKeyResponse(
        raw_key=gen.raw_key,
        key_hash=gen.key_hash,
        prefix=gen.prefix,
        name=payload.name,
    )


@router.get("/me")
async def verify_auth_tenant(tenant_id: str = "org_default") -> dict[str, str]:
    if not rate_limiter.is_allowed(tenant_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again in 60 seconds.",
        )
    return {"tenant_id": tenant_id, "status": "authenticated"}
