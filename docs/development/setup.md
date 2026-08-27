# Developer Environment Setup Guide

## Step-by-Step Local Setup

1. **Verify Tool Prerequisites**:
   - Python 3.12+ (`python --version`)
   - `uv` installed (`uv --version`)
   - Node.js 20+ & npm (`node -v`, `npm -v`)
   - Docker & Docker Compose (`docker compose version`)

2. **Clone & Bootstrap**:
   ```bash
   git clone https://github.com/your-org/agentevalops.git
   cd agentevalops
   ```

3. **Run PowerShell Setup Script (Windows)**:
   ```powershell
   .\scripts\setup.ps1
   ```
   Or using Makefile:
   ```bash
   make install
   ```

4. **Boot PostgreSQL & Redis Containers**:
   ```bash
   docker compose up -d postgres redis
   ```

5. **Apply Database Migrations**:
   ```bash
   uv run alembic upgrade head
   ```

6. **Start Local Backend Server**:
   ```bash
   uv run uvicorn apps.api.app.main:app --reload --port 8000
   ```

7. **Start Local Next.js Web App**:
   ```bash
   cd apps/web && npm run dev
   ```
   Open `http://localhost:3000/status` to view live service status.
