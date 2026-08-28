# Validation Matrix — AgentEvalOps

This document maps every acceptance criterion across all platform phases to its exact status, date of verification, execution command, and artifact evidence path.

---

## Phase 0 — Foundation & Developer Environment

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-00-01** | Python 3.12+ runtime & `uv` workspace configured | **PASS** | 2026-08-28 | `uv sync` | `pyproject.toml`, `uv.lock` |
| **REQ-00-02** | Docker Compose PostgreSQL, Redis, Qdrant setup | **PASS** | 2026-08-28 | `docker compose config` | `docker-compose.yml` |
| **REQ-00-03** | Monorepo architecture & workspace dependencies linked | **PASS** | 2026-08-28 | `uv run pytest` | `docs/environment-report.md` |

---

## Phase 1 — Production Trace Ingestion

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-01-01** | Python Tracing SDK async/sync context managers & exporter | **PASS** | 2026-08-28 | `uv run pytest tests/test_sdk.py` | `packages/python-sdk` |
| **REQ-01-02** | FastAPI `POST /api/v1/traces` & `POST /api/v1/traces/batch` | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase1_e2e.py` | `apps/api/app/api/v1/traces.py` |
| **REQ-01-03** | PostgreSQL & SQLAlchemy Trace, Span, Project ORM models | **PASS** | 2026-08-28 | `uv run pytest tests/test_health_api.py` | `apps/api/app/domain/models/entities.py` |
| **REQ-01-04** | Async Redis trace queue & worker processing | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase1_e2e.py` | `services/workers/trace_worker.py` |
| **REQ-01-05** | Next.js Trace Explorer UI & live span hierarchy tree | **PASS** | 2026-08-28 | Component inspection | `apps/web/src/app/page.tsx` |
| **REQ-01-06** | End-to-End trace ingestion pipeline integration | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase1_e2e.py` | `tests/test_phase1_e2e.py` |

---

## Phase 2 — Developer Observability

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-02-01** | Real-time analytics engine (token breakdown, USD costs, latency) | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase2_observability.py` | `apps/api/app/infrastructure/analytics.py` |
| **REQ-02-02** | OpenAPI endpoints `GET /api/v1/analytics/overview`, `/models`, `/tools` | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase2_observability.py` | `apps/api/app/api/v1/analytics.py` |
| **REQ-02-03** | Next.js Observability Dashboard UI console | **PASS** | 2026-08-28 | Component inspection | `apps/web/src/app/analytics/page.tsx` |
| **REQ-02-04** | LLM model breakdown & tool execution error statistics | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase2_observability.py` | `tests/test_phase2_observability.py` |

---

## Phase 3 — Deterministic Evaluation Engine

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-03-01** | `EvaluatorRegistry` & extensible evaluator base classes | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase3_evaluators.py` | `packages/evaluator-core/src/agentevalops_eval/registry.py` |
| **REQ-03-02** | 5 Core Rule Evaluators (ExactMatch, ToolValidity, Latency, Cost, Keywords) | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase3_evaluators.py` | `packages/evaluator-core/src/agentevalops_eval/deterministic.py` |
| **REQ-03-03** | `EvaluationEngine` suite runner & score aggregation | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase3_evaluators.py` | `packages/evaluator-core/src/agentevalops_eval/engine.py` |
| **REQ-03-04** | Evaluation API endpoints (`POST /api/v1/evaluations/run`, `/evaluators`) | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase3_evaluators.py` | `apps/api/app/api/v1/evaluations.py` |
| **REQ-03-05** | Next.js Evaluation Console UI dashboard | **PASS** | 2026-08-28 | Component inspection | `apps/web/src/app/evaluations/page.tsx` |

---

## Phase 4 — RAG Evaluation

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-04-01** | ContextPrecision, Faithfulness & CitationQuality evaluators | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase4_rag.py` | `packages/evaluator-core/src/agentevalops_eval/rag.py` |

---

## Phase 5 — LLM-as-a-Judge System

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-05-01** | RubricJudgeEvaluator & JudgeCalibrationEngine agreement metrics | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase5_llm_judge.py` | `packages/evaluator-core/src/agentevalops_eval/llm_judge.py` |

---

## Phase 6 — Trajectory Evaluation

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-06-01** | StepEfficiencyEvaluator (loop detection) & RecoveryEvaluator | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase6_trajectory.py` | `packages/evaluator-core/src/agentevalops_eval/trajectory.py` |

---

## Phase 7 — Datasets & Experiments

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-07-01** | Versioned golden sets, dataset cases API, automated experiment runner | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase7_datasets.py` | `apps/api/app/api/v1/datasets.py` |

---

## Phase 8 — Continuous Regression + CI

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-08-01** | DeploymentGateEngine (PASS/WARN/BLOCK) & release policy gate API | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase8_regression.py` | `packages/evaluator-core/src/agentevalops_eval/gate.py` |

---

## Phase 9 — Safety & State Integrity

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-09-01** | PromptInjectionEvaluator & PIILeakageEvaluator (SSN, credit card, API key regex scrubbers) | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase9_safety.py` | `packages/evaluator-core/src/agentevalops_eval/safety.py` |

---

## Phase 10 — Failure Intelligence + ML

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-10-01** | FailurePredictor ML risk model & taxonomy clusters API | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase10_ml.py` | `ml/failure-prediction/src/agentevalops_ml/predictor.py` |

---

## Phase 11 — Production SaaS Scale

| Requirement ID | Description | Status | Verification Date | Verification Command | Evidence / Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-11-01** | SHA-256 API key hashing, secret scrubber, sliding window rate limiter, auth API | **PASS** | 2026-08-28 | `uv run pytest tests/test_phase11_saas_scale.py` | `apps/api/app/infrastructure/security.py` |
