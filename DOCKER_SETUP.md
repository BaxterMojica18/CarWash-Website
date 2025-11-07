# Docker Setup Guide

## Option 1: Full Docker Setup (Recommended)

Run everything in Docker:

```bash
# Stop any existing containers
docker-compose down

# Rebuild and start
docker-compose up --build

# Access at http://localhost:8000
```

## Option 2: Database in Docker, Server Local

Run only PostgreSQL in Docker, server on your machine:

```bash
# Start only the database
docker-compose up -d db

# Wait 5 seconds for database to be ready
timeout /t 5

# Run migrations and setup
python migrate_db.py
python seed_data.py
python add_permissions.py
python assign_user_roles.py

# Start server locally
start_server_local.bat
```

## Troubleshooting

### Cannot reach 0.0.0.0:8000 in Docker

Check logs:
```bash
docker-compose logs web
```

Restart containers:
```bash
docker-compose down
docker-compose up --build
```

### Local server cannot connect to database

Make sure:
1. Database is running: `docker-compose ps`
2. Port 5432 is exposed: `docker-compose up -d db`
3. Use correct DATABASE_URL in .env:
   - Docker: `postgresql://postgres:password12025@db:5432/carwash_db`
   - Local: `postgresql://postgres:password12025@localhost:5432/carwash_db`

### Check database connection

```bash
docker exec -it car-wash-website-db-1 psql -U postgres -d carwash_db -c "\dt"
```

## Environment Variables

### For Docker (docker-compose.yml)
```
DATABASE_URL: postgresql://postgres:password12025@db:5432/carwash_db
```

### For Local (.env)
```
DATABASE_URL=postgresql://postgres:password12025@localhost:5432/carwash_db
```
