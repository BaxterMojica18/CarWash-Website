@echo off
echo Starting Car Wash Server (Local Mode)...
echo.
echo Make sure PostgreSQL is running in Docker:
echo   docker-compose up -d db
echo.
set DATABASE_URL=postgresql://postgres:password12025@localhost:5432/carwash_db
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
