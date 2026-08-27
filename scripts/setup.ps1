# AgentEvalOps — Developer Environment Setup Script (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  AgentEvalOps — Phase 0 Environment Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# 1. Check Python & uv
Write-Host "`n[1/5] Checking Python & uv..." -ForegroundColor Yellow
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "uv is not installed. Please install uv (https://github.com/astral-sh/uv) or run 'pip install uv'."
}
Write-Host "uv version: $(uv --version)" -ForegroundColor Green

# 2. Create Python Virtual Environment
Write-Host "`n[2/5] Setting up Python virtual environment (.venv)..." -ForegroundColor Yellow
uv venv .venv
Write-Host "Virtual environment created at .venv" -ForegroundColor Green

# 3. Install Monorepo Dependencies
Write-Host "`n[3/5] Installing dependencies via uv..." -ForegroundColor Yellow
uv pip install -e ".[dev,test,docs,ml]" --quiet
Write-Host "Installed monorepo root dependencies." -ForegroundColor Green

# 4. Copy .env if not exists
Write-Host "`n[4/5] Checking environment configuration (.env)..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example" -ForegroundColor Green
} else {
    Write-Host ".env already exists." -ForegroundColor Green
}

# 5. Summary & Next Steps
Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete! Ready to launch services." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Next steps:"
Write-Host "  1. Start Database & Redis:  docker compose up -d postgres redis"
Write-Host "  2. Run DB Migrations:       uv run alembic upgrade head"
Write-Host "  3. Start Backend (API):     uv run uvicorn apps.api.app.main:app --reload"
Write-Host "  4. Start Frontend (Web):    cd apps/web; npm run dev"
Write-Host "================================================" -ForegroundColor Cyan
