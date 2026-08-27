# Local Deployment Guide (Docker Compose)

## 1. Local Containerized Stack Setup

The `docker-compose.yml` file configures all core services for local execution:

- **`postgres`**: PostgreSQL 16 Alpine (`localhost:5432`)
- **`redis`**: Redis 7 Alpine (`localhost:6379`)
- **`api`**: FastAPI Control Plane (`localhost:8000`)
- **`web`**: Next.js App Router (`localhost:3000`)
- **`qdrant`** (Optional): Vector database (`localhost:6333`)

## 2. Launch Commands

### Start default infrastructure & app stack:
```bash
docker compose up --build -d
```

### Start stack including optional Qdrant vector DB:
```bash
docker compose --profile optional up -d
```

### Stop container stack:
```bash
docker compose down
```
