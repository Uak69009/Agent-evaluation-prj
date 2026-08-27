# Testing Guide & Strategy

## 1. Backend & SDK Unit Testing (`pytest`)

Tests are located under `tests/`, `apps/api/tests/`, and `packages/*/tests/`.

### Run all tests:
```bash
uv run pytest
```

### Run API endpoint tests only:
```bash
uv run pytest tests/api/
```

### Run Python SDK client tests:
```bash
uv run pytest tests/sdk/
```

## 2. Test Database Configuration
For unit tests, `aiosqlite` in-memory database (`sqlite+aiosqlite:///:memory:`) is used to allow fast, isolated async testing without requiring a running PostgreSQL server.

## 3. Frontend Testing
- **Typecheck**: `npm --prefix apps/web run typecheck`
- **Lint**: `npm --prefix apps/web run lint`
- **Build**: `npm --prefix apps/web run build`
