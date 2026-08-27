import os

from pydantic import BaseModel, Field


class SDKConfig(BaseModel):
    api_key: str = Field(default_factory=lambda: os.getenv("AGENTEVALOPS_API_KEY", ""))
    api_url: str = Field(
        default_factory=lambda: os.getenv("AGENTEVALOPS_API_URL", "http://localhost:8000")
    )
    environment: str = Field(default_factory=lambda: os.getenv("AGENTEVALOPS_ENV", "development"))
    organization_id: str | None = Field(default_factory=lambda: os.getenv("AGENTEVALOPS_ORG_ID"))
    project_id: str | None = Field(default_factory=lambda: os.getenv("AGENTEVALOPS_PROJECT_ID"))
    timeout_seconds: float = 10.0
    max_retries: int = 3
    enabled: bool = True
