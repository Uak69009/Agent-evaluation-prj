# Security Log & Audit — AgentEvalOps

This document tracks security architecture, API key hashing policies, RBAC access controls, secret redaction, dependency vulnerability scans, and security test results.

---

## Security Policies & Controls

1. **Tenant Isolation:** Every trace read/write operation requires valid API Key or JWT authentication. Scope is strictly constrained to `organization_id` and `project_id`. Server-side validation prevents cross-tenant data access.
2. **API Key Storage:** Raw API keys are prefixed with `aeo_live_` or `aeo_test_` and stored strictly as SHA-256 hashed digests. Raw secret strings are never written to disk or logs.
3. **PII & Secret Redaction:** Tracing SDK and ingestion workers apply regex pattern scrubbers for API keys, JWT tokens, Bearer headers, passwords, and sensitive credentials prior to persistence.
4. **Tool Execution Sandboxing:** Any custom code execution or evaluator tool runner must be executed in restricted environments.

---

## Security Audit Log

| Date | Type | Component | Findings | Status / Remediation |
| :--- | :--- | :--- | :--- | :--- |
| 2026-08-28 | Static Audit | `apps/api` | Confirmed no hardcoded API keys or secrets in codebase. | **PASS** |
| 2026-08-28 | Dependency Scan | Monorepo dependencies | Verified all dependencies pinned in `uv.lock`. | **PASS** |
