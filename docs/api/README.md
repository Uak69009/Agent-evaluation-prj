# AgentEvalOps Control Plane API Documentation

## 1. OpenAPI Specs & Interactive Explorer URLs
When running locally (`uv run uvicorn apps.api.app.main:app --port 8000`):
- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **ReDoc Document Explorer**: `http://localhost:8000/redoc`
- **Raw OpenAPI JSON Spec**: `http://localhost:8000/openapi.json`

## 2. API Versioning Strategy
- Primary API base path is versioned under `/api/v1` (e.g. `/api/v1/health`).
- Non-breaking additions will be introduced cleanly within `/api/v1`.
- Deprecations or breaking schema modifications will introduce `/api/v2`.

## 3. Standardized Error Response Structure
All error responses adhere to the following JSON schema:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error explanation",
    "request_id": "req_uuid_001"
  }
}
```

## 4. Health & Status Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Basic service health check |
| `GET` | `/health/live` | Liveness probe for container orchestrators |
| `GET` | `/health/ready` | Dependency readiness probe (Database & Redis ping) |
| `GET` | `/version` | Platform and API version information |
