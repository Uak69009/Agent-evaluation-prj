# Final Operations Runbook — AgentEvalOps

This runbook guides engineers through running, managing, and maintaining the AgentEvalOps platform in local, staging, and production environments.

---

## 1. Local Startup Guide

### Prerequisites:
- Python 3.12+ / `uv`
- Node.js v20+ / `npm`
- Docker (for PostgreSQL & Redis containers)

### Start Backend Services (FastAPI):
```bash
# In repository root
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- **Control Plane API:** `http://localhost:8000`
- **Interactive OpenAPI Documentation:** `http://localhost:8000/docs`

### Start Frontend Console (Next.js):
```bash
# In repository root
npm run dev:web
# Or directly inside apps/web
cd apps/web && npm run dev
```
- **Web Console UI:** `http://localhost:3000`
- **Trace Explorer:** `http://localhost:3000`
- **Observability Dashboard:** `http://localhost:3000/analytics`
- **Evaluation Engine Console:** `http://localhost:3000/evaluations`

---

## 2. Running Automated Quality Tests & Gates

```bash
# Run all 20 monorepo test suites
uv run pytest

# Check code formatting & types
uv run ruff check .
```

---

## 3. Incident Response & Troubleshooting

- **Error: Port 8000 or 3000 already in use**:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
  ```
- **Rate Limit Triggered (`429 Too Many Requests`)**:
  - The default sliding window rate limiter permits 120 requests/minute per tenant. Rate limits can be adjusted in `apps/api/app/infrastructure/rate_limiter.py`.
