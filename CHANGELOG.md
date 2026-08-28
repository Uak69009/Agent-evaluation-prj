# Changelog — AgentEvalOps

All notable changes to the AgentEvalOps platform will be documented in this file.

## [Unreleased] - Phase 1 Development

### Added
- Monorepo structure with `apps/api`, `apps/web`, `packages/python-sdk`, `packages/shared-schemas`, `packages/evaluator-core`, `services/workers`, and `ml/failure-prediction`.
- Docker Compose configuration for PostgreSQL 16, Redis 7, and Qdrant vector database.
- Production Python Tracing SDK (`agentevalops-sdk`) supporting sync/async context managers and batch HTTP exporter.
- FastAPI trace ingestion API endpoints (`POST /api/v1/traces`, `POST /api/v1/traces/batch`, `GET /api/v1/traces`).
- Next.js Trace Explorer UI console with live span tree hierarchy and metric cards.
