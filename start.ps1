# Car Wash Website - Start Script
# Activates venv and starts the project via docker-compose

Write-Host "=== Car Wash Website ===`n" -ForegroundColor Cyan

# Activate venv (for running migration scripts and CLI tools directly)
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & ".venv\Scripts\Activate.ps1"
    Write-Host "Virtual environment active." -ForegroundColor Green
} else {
    Write-Host "Virtual environment not found. Run .\setup.ps1 first." -ForegroundColor Yellow
}

# Check Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Docker is not found on PATH." -ForegroundColor Red
    Write-Host "Make sure Docker Desktop is running." -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting services via docker-compose..." -ForegroundColor Cyan
Write-Host "(Migrations run automatically on startup)`n" -ForegroundColor Gray

docker-compose up
