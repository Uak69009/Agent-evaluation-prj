# Scalability & Evolution Strategy

## 1. Phase 0 Local Architecture
- **Control Plane**: FastAPI async single-instance server.
- **Relational Storage**: PostgreSQL 16 for metadata, users, trace indexes, and evaluations.
- **Cache & Queue**: Redis 7 for task queuing and fast session caching.

## 2. Production Target System Architecture (Section 33 Documented Vision)

```text
Users / Web UI
      │
      ▼
Load Balancer (TLS Termination)
      │
      ▼
Stateless FastAPI API Replicas
      │
  ┌───┴──────────────────────────────┐
  ▼                                  ▼
PostgreSQL                      Redis Queue
(Transactional Metadata)        (Evaluation Jobs)
                                     │
                                     ▼
                        Worker Autoscaling Pool
                                     │
                 ┌───────────────────┼───────────────────┐
                 ▼                   ▼                   ▼
            ClickHouse         S3 / MinIO          Qdrant
         (High-Volume Tracing) (Raw Payloads)   (Vector Search)
```

## 3. High-Volume Payload Offloading
To prevent PostgreSQL database bloat when ingesting millions of trace payloads:
- Structured metadata (IDs, metrics, durations, token counts) is stored in relational DB / ClickHouse.
- Large raw LLM prompt/completion payloads and full JSON trajectories are streamed directly to S3 / Object Storage.
