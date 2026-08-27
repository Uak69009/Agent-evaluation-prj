# AgentEvalOps — Multi-Tenant AI Agent Evaluation & LLMOps Platform

> **Continuous observation, evaluation, diagnosis, testing, and governance of AI agents across correctness, trajectory quality, tool usage, RAG quality, reliability, safety, state integrity, latency, and cost.**

---

## 🚀 Overview

**AgentEvalOps** is an enterprise-grade, multi-tenant AI-agent evaluation and LLMOps platform designed to evaluate autonomous AI agents beyond conventional task-success metrics. It supports normalized tracing across diverse framework ecosystems (LangGraph, OpenAI Agents SDK, custom Python agents) and provides automated evaluation gates, failure prediction, and continuous trajectory governance.

---

## 🏗 Monorepo Architecture

```text
agentevalops/
├── apps/
│   ├── api/                  # FastAPI Control Plane API
│   └── web/                  # Next.js App Router Frontend Dashboard Shell
├── packages/
│   ├── python-sdk/           # Lightweight Python SDK (agentevalops)
│   ├── shared-schemas/       # Normalized Trace, Span, and Eval Pydantic Schemas
│   └── evaluator-core/       # Abstract Evaluator Plugin Core
├── services/
│   └── workers/              # Asynchronous Evaluation Worker Service
├── ml/
│   └── failure-prediction/   # Trajectory Failure Prediction ML Research Module
├── infra/
│   ├── docker/               # Dockerfiles for API & Web
│   └── postgres/             # Database initialization & migrations
├── docs/                     # Architecture, Development, API, and Research Docs
└── tests/                    # Integration and End-to-End Test Fixtures
```

---

## ⚡ Quickstart Setup

### Prerequisites

- Python 3.12+ (managed with `uv`)
- Node.js v24+ (managed with `npm` / `pnpm`)
- Docker Engine & Docker Compose v5+

### Installation & Local Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/agentevalops.git
   cd agentevalops
   ```

2. **Automated Setup Script:**
   ```powershell
   # Windows PowerShell
   .\scripts\setup.ps1
   ```
   Or using `Makefile`:
   ```bash
   make install
   ```

3. **Start Infrastructure Services (PostgreSQL & Redis):**
   ```bash
   docker compose up -d postgres redis
   ```

4. **Run Database Migrations:**
   ```bash
   uv run alembic upgrade head
   ```

5. **Start Development Services:**
   - **Backend Control Plane:**
     ```bash
     uv run uvicorn apps.api.app.main:app --reload --port 8000
     ```
     Access Swagger Docs at `http://localhost:8000/docs`
   - **Frontend Dashboard Shell:**
     ```bash
     cd apps/web && npm run dev
     ```
     Access Dashboard Status at `http://localhost:3000/status`

---

## 🛠 Developer Commands Reference

| Command | Purpose |
| :--- | :--- |
| `make install` | Create virtual environment and install all workspace packages via `uv` |
| `make dev` | Start infrastructure and development services |
| `make test` | Run `pytest` test suites across backend, SDK, and evaluators |
| `make lint` | Run `ruff check .` and frontend ESLint |
| `make typecheck` | Run `mypy` and TypeScript type checking (`tsc --noEmit`) |
| `make format` | Format Python code with `ruff format .` |
| `make db-migrate` | Execute Alembic database migrations (`alembic upgrade head`) |
| `make docker-up` | Build and bring up full Docker Compose stack |
| `make cleanup` | Clean Python `__pycache__`, `.next` build caches, and temp files |

---

## 🧪 Testing & Verification

Run all test suites:
```bash
uv run pytest
```

Run linter & type checker:
```bash
uv run ruff check .
uv run mypy apps/api packages/
npm --prefix apps/web run typecheck
```

---

## 🗺 Platform Roadmap & Research

- **Phase 0 (Completed):** Monorepo foundation, multi-tenant DB schema, trace schemas, Python SDK base, Evaluator interfaces, Docker Compose environment, CI/CD foundation.
- **Phase 1:** Real-time OpenTelemetry ingestion pipeline, trace normalization adapters for LangGraph & OpenAI Agents SDK.
- **Phase 2:** Core evaluation engine execution (Deterministic, LLM-as-a-Judge, Trajectory Quality).
- **Phase 3:** Automated PR evaluation gating & failure prediction ML model integration.

---

## 📜 License

Distributed under the Apache 2.0 License. See `LICENSE` for details.
