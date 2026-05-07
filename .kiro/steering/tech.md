# Tech Stack & Build System

## Backend
- **Language**: Python 3.11
- **Framework**: FastAPI
- **ORM**: SQLAlchemy (declarative base, not Alembic — migrations are manual scripts)
- **Database**: PostgreSQL 16
- **Auth**: python-jose (JWT), passlib/bcrypt (password hashing), firebase-admin (Google login verification)
- **Validation**: Pydantic v2
- **PDF generation**: ReportLab
- **Email**: Resend API
- **Payments**: Stripe (stripe Python SDK)
- **Admin panel**: SQLAdmin
- **Server**: Uvicorn

## Frontend
- **No framework** — vanilla HTML, CSS, JavaScript
- **No build step** — files served as static assets
- **API client**: Custom `api.js` wrapper around `fetch()`
- **Charts**: Chart.js (CDN)
- **Auth SDK**: Firebase JS SDK (CDN)

## Infrastructure
- **Containerization**: Docker + Docker Compose
- **Backend hosting**: Render (Docker deployment)
- **Frontend hosting**: Vercel (static)
- **Database hosting**: Render PostgreSQL (free tier)

## Key Libraries (requirements.txt)
| Library | Purpose |
|---------|---------|
| fastapi | Web framework |
| sqlalchemy | ORM |
| psycopg2-binary | PostgreSQL driver |
| pydantic | Request/response validation |
| python-jose | JWT token creation/verification |
| passlib + bcrypt | Password hashing |
| firebase-admin | Firebase token verification |
| stripe | Payment processing |
| resend | Transactional email |
| reportlab | PDF generation |
| sqladmin | Admin UI |
| python-dotenv | Environment variable loading |

## Common Commands

```bash
# Start locally with Docker (recommended)
docker-compose up -d

# Start without Docker
uvicorn app.main:app --reload --port 8000

# Create database tables / run migrations
python commands/database/migrate_db.py
python commands/database/seed_data.py

# Create superadmin account
python commands/users/create_superadmin.py

# Create demo users
python commands/users/create_demo_users.py

# Install dependencies
pip install -r requirements.txt
```

## Environment Variables
Defined in `.env` (local) or Render dashboard (production). Key vars:
- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — JWT signing key
- `RESEND_API_KEY` — Email service
- `STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` — Payments
- `FIREBASE_CREDENTIALS_JSON` — Firebase service account (production only)
- `FRONTEND_URL` — Used in email action buttons
