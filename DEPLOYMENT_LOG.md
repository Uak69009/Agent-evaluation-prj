# Deployment Log — AgentEvalOps

This document logs deployment environments, version tags, database migrations, service infrastructure, health check evidence, and smoke test results.

---

## Environment Configurations

| Environment | Host / Container Engine | DB Engine | Queue | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Local Dev** | Windows 10 / `uv` / Docker | PostgreSQL 16 Alpine / SQLite | Redis 7 Alpine | **ACTIVE** |
| **Staging** | Docker Compose / Managed | PostgreSQL 16 | Redis 7 | PLANNED |
| **Production** | Container Runtime / Managed Cloud | Managed Postgres | Managed Redis | PLANNED |

---

## Deployment Audit History

| Date (UTC) | Environment | Version / Commit | Schema Revision | Deployment Status | Verification Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-08-28 00:20 | Local Dev | `6f3bb8a` | Baseline | **SUCCESS** | `docs/environment-report.md` |
| 2026-08-28 10:20 | Local Dev | `master` | Initial Alembic schema | **SUCCESS** | `uv run pytest` (7 passed) |
