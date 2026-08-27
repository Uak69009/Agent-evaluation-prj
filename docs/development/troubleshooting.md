# Developer Troubleshooting Guide

## Common Setup Issues & Solutions

### 1. `uv` virtualenv or package build errors
- **Symptom**: `Failed to build package` or missing wheel package configuration.
- **Solution**: Ensure subpackage `pyproject.toml` files include `[tool.hatch.build.targets.wheel] packages = ["..."]` and run `uv venv .venv`.

### 2. Docker database connection refused
- **Symptom**: API log reports `ConnectionRefusedError: [Errno 111] Connect call failed ('127.0.0.1', 5432)`.
- **Solution**: Verify PostgreSQL container status with `docker compose ps`. Run `docker compose up -d postgres redis`.

### 3. Alembic migration conflicts
- **Symptom**: Alembic reports target database is not up to date.
- **Solution**: Run `uv run alembic upgrade head` to apply all pending revisions.

### 4. Next.js build errors or module not found
- **Symptom**: `Cannot find module '@/lib/api'`.
- **Solution**: Verify `tsconfig.json` path mapping `"@/*": ["./src/*"]` and run `npm install` inside `apps/web`.
