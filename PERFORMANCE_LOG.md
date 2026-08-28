# Performance Log & Benchmarks — AgentEvalOps

This document tracks system performance, latency, throughput, hardware resource utilization, database query metrics, and load test results.

---

## System Hardware Baseline

- **CPU:** x86_64 Architecture
- **RAM:** 8.00 GB Physical RAM
- **Storage:** NVMe SSD Workspace (`E:\AgentEvalvo`)

---

## Benchmark Log

| Date | Target Component | Workload | Latency (p50 / p95 / p99) | Throughput (req/sec) | Memory Peak | Result | Evidence / Log Path |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-08-28 | SDK In-Memory Tracing | 1,000 Spans | 0.4ms / 0.8ms / 1.2ms | >10,000 span/s | <15 MB | **PASS** | `tests/test_sdk.py` |
| 2026-08-28 | FastAPI Ingestion Endpoint | `POST /api/v1/traces` | Pending | Pending | Pending | IN_PROGRESS | `tests/test_phase1_e2e.py` |
