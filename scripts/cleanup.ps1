# AgentEvalOps — Workspace & Cache Cleanup Script (PowerShell)
Write-Host "Cleaning Python caches, build artifacts, and temporary test directories..." -ForegroundColor Yellow

Get-ChildItem -Path . -Recurse -Include "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -Include "*.pyc", "*.pyo", "*.pyd" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "Cleaning Node build caches (.next, dist)..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -Include ".next", "dist", "out" -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Cleanup completed successfully!" -ForegroundColor Green
