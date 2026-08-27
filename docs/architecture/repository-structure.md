# Monorepo Repository Structure — AgentEvalOps

```text
agentevalops/
│
├── apps/
│   ├── web/                     # Next.js App Router dashboard shell & status UI
│   └── api/                     # FastAPI control plane API service
│
├── packages/
│   ├── python-sdk/              # Official Python SDK (agentevalops)
│   ├── shared-schemas/          # Normalized Pydantic trace & evaluation schemas
│   └── evaluator-core/          # Evaluator plugin interface definitions & abstractions
│
├── services/
│   └── workers/                 # Asynchronous Redis background evaluation workers
│
├── ml/
│   └── failure-prediction/      # Trajectory failure prediction research & feature extraction
│
├── infra/
│   ├── docker/                  # Multi-stage slim Dockerfiles for API and Web
│   ├── postgres/                # PostgreSQL init scripts
│   ├── redis/                   # Redis configuration
│   └── scripts/                 # Infra helper scripts
│
├── docs/                        # Complete technical documentation suite
│   ├── architecture/            # System overview, data models, trace models, scalability
│   ├── development/             # Setup, commands, testing, troubleshooting, dependencies
│   ├── api/                     # API OpenAPI specs and conventions
│   ├── deployment/              # Local and production deployment guides
│   └── research/                # Product research roadmap
│
├── tests/                       # Integration and end-to-end test fixtures
│
├── .github/
│   └── workflows/               # GitHub Actions CI & evaluation gate workflows
│
├── scripts/                     # Developer setup and cleanup automation scripts
│
├── .env.example                 # Environment variables template
├── .gitignore                   # Comprehensive workspace git ignore
├── .dockerignore                # Slim docker context ignore
├── docker-compose.yml           # Local docker compose stack (Postgres, Redis, API, Web, Qdrant)
├── Makefile                     # Developer task runner
├── pyproject.toml               # Root uv workspace configuration
├── package.json                 # Monorepo root Node configuration
├── README.md                    # Repository quickstart & documentation
└── LICENSE                      # Apache 2.0 License
```
