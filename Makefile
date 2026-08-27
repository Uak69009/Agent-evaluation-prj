.PHONY: help install dev dev-api dev-web test test-api test-sdk lint typecheck format db-up db-down db-migrate db-reset docker-up docker-down docker-build cleanup

help:
	@echo "AgentEvalOps Developer Commands:"
	@echo "  make install      - Install Python virtualenv & dependencies via uv"
	@echo "  make dev          - Run local development services"
	@echo "  make test         - Run all pytest test suites"
	@echo "  make lint         - Run ruff linter & frontend lint"
	@echo "  make typecheck    - Run mypy & TypeScript type checking"
	@echo "  make format       - Format Python & TypeScript codebase"
	@echo "  make db-up        - Start PostgreSQL & Redis in Docker"
	@echo "  make db-migrate   - Run Alembic database migrations"
	@echo "  make docker-up    - Run full docker compose stack"
	@echo "  make docker-down  - Stop docker compose stack"
	@echo "  make cleanup      - Clean build artifacts & temp caches"

install:
	uv venv
	uv pip install -e ".[dev,test,docs,ml]"
	uv pip install -e packages/shared-schemas
	uv pip install -e packages/python-sdk
	uv pip install -e packages/evaluator-core
	uv pip install -e apps/api

dev-api:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-web:
	npm --prefix apps/web run dev

dev: db-up
	@echo "Starting API and Web apps..."

test:
	uv run pytest tests/ apps/api/ packages/

lint:
	uv run ruff check .
	npm --prefix apps/web run lint

typecheck:
	uv run mypy apps/api packages/
	npm --prefix apps/web run typecheck

format:
	uv run ruff format .

db-up:
	docker compose up -d postgres redis

db-down:
	docker compose stop postgres redis

db-migrate:
	uv run alembic upgrade head

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

cleanup:
	powershell -ExecutionPolicy Bypass -File ./scripts/cleanup.ps1
