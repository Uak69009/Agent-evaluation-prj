# Architectural Decision Records (ADR) — AgentEvalOps

This document logs key architectural decisions, rationale, alternatives considered, and consequences.

---

## ADR-001: Framework-Neutral Python Tracing SDK Architecture

- **Status:** Approved
- **Context:** Agent developers use various frameworks (LangChain, LangGraph, LlamaIndex, AutoGen, custom OpenAI wrappers). Standardizing telemetry without framework lock-in is critical.
- **Decision:** Implement a lightweight, zero-dependency core SDK (`agentevalops-sdk`) using Python standard library `contextlib` and `asyncio` with OpenTelemetry/OpenInference compatible semantic attribute conventions (`llm.model`, `llm.prompt`, `llm.tokens.prompt`, `llm.tokens.completion`, `tool.name`, `tool.args`).
- **Consequences:** Low overhead (<1ms per span creation), framework neutral, easy adapter creation for LangChain/LangGraph/OpenAI.

---

## ADR-002: PostgreSQL & Redis Async Queue Architecture for Ingestion

- **Status:** Approved
- **Context:** Ingestion endpoint `POST /api/v1/traces` must support high burst throughput from thousands of agent spans without blocking agent execution or overloading the main relational database.
- **Decision:** Fast-ingest traces into a Redis queue using non-blocking API handlers, then process span tree normalization and write to PostgreSQL asynchronously via background workers (`agentevalops-workers`).
- **Consequences:** Sub-10ms response time on ingestion API, decoupled write pipeline, resilient to database query spikes.
