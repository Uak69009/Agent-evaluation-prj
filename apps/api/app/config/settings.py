from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AgentEvalOps API"
    APP_ENV: str = "development"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "dev-secret-key-32bytes-agentevalops-local"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = (
        "postgresql+asyncpg://agentevalops:agentevalops_dev_pass@localhost:5432/agentevalops"
    )
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Vector Search (Qdrant)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None

    # Telemetry
    OTEL_SERVICE_NAME: str = "agentevalops-api"
    OTEL_EXPORTER_OTLP_ENDPOINT: str | None = "http://localhost:4317"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
