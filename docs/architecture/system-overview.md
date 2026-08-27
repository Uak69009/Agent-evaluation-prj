# System Architecture Overview — AgentEvalOps

> **AgentEvalOps is a multi-tenant AI-agent evaluation and LLMOps platform designed to continuously observe, evaluate, diagnose, test, and govern AI agents across correctness, trajectory quality, tool usage, RAG quality, reliability, safety, state integrity, latency, and cost.**

---

## 1. High-Level Architecture Diagram

```text
                                 ┌─────────────────────────────────┐
                                 │       Agent Frameworks          │
                                 │ (LangGraph / OpenAI / Custom)   │
                                 └────────────────┬────────────────┘
                                                  │ (Python SDK / OpenTelemetry)
                                                  ▼
┌──────────────────┐               ┌───────────────────────────────┐
│ Next.js Frontend │ ── (HTTP) ──▶ │     FastAPI Control Plane     │
│   (apps/web)     │ ◄─ (JSON) ─── │          (apps/api)           │
└──────────────────┘               └──────────────┬────────────────┘
                                                  │
                      ┌───────────────────────────┼───────────────────────────┐
                      ▼                           ▼                           ▼
            ┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
            │ PostgreSQL (DB)   │       │ Redis (Queue/Cache│       │ Qdrant (Vector)   │
            │ Multi-Tenant ORM  │       │ Worker Jobs)      │       │ Failure Search    │
            └───────────────────┘       └─────────┬─────────┘       └───────────────────┘
                                                  │
                                                  ▼
                                        ┌───────────────────┐
                                        │ Worker Services   │
                                        │ Evaluator Core    │
                                        └───────────────────┘
```

---

## 2. Core Architectural Principles

### 2.1 Multi-Tenancy by Design
Every persistent database entity belongs to an `Organization` and `Project`. Isolation is maintained at the query level (`organization_id`, `project_id`) across traces, datasets, evaluators, experiments, and deployments.

### 2.2 Framework Independence
AgentEvalOps normalizes incoming execution traces into a framework-agnostic schema supporting `Trace`, `Span` (LLM, Tool, Retrieval, Embedding, Custom), `Run`, and `ToolCall` primitives regardless of whether the source agent uses LangGraph, OpenAI Agents SDK, CrewAI, AutoGen, or custom Python loops.

### 2.3 Modular Monolith Strategy
The control plane is implemented as a cohesive modular service (`apps/api`) with decoupled subpackage boundaries (`packages/shared-schemas`, `packages/evaluator-core`, `packages/python-sdk`, `services/workers`, `ml/failure-prediction`). This allows immediate local execution while supporting future horizontal microservice separation.
