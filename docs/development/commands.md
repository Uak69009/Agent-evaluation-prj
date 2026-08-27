# Developer Commands Quick Reference

| Action | PowerShell Command | Makefile Equivalent |
| :--- | :--- | :--- |
| **Setup Virtualenv & Install** | `.\scripts\setup.ps1` | `make install` |
| **Run All Tests** | `uv run pytest` | `make test` |
| **Run Python Linter** | `uv run ruff check .` | `make lint` |
| **Format Python Code** | `uv run ruff format .` | `make format` |
| **Run Python Type Check** | `uv run mypy apps/api packages/` | `make typecheck` |
| **Run Frontend Dev** | `cd apps/web; npm run dev` | `make dev-web` |
| **Frontend Typecheck** | `npm --prefix apps/web run typecheck` | `make typecheck` |
| **Start Docker Databases** | `docker compose up -d postgres redis` | `make db-up` |
| **Run Alembic Migrations** | `uv run alembic upgrade head` | `make db-migrate` |
| **Clean Build Artifacts** | `.\scripts\cleanup.ps1` | `make cleanup` |
