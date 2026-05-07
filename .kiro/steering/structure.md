# Project Structure

```
├── app/                        # Backend application (FastAPI)
│   ├── main.py                 # App entry point, middleware, router registration
│   ├── database.py             # SQLAlchemy models, engine, session factory
│   ├── schemas.py              # Pydantic request/response models
│   ├── crud.py                 # Database operations (all CRUD logic)
│   ├── dependencies.py         # FastAPI dependency injection (get current user, etc.)
│   ├── permissions.py          # Permission checking utilities
│   ├── email_service.py        # Resend API email sending
│   ├── sms_service.py          # SMS service
│   ├── firebase_auth.py        # Firebase token verification
│   ├── demo_limits.py          # Demo account restrictions
│   └── routers/                # API route handlers (one file per domain)
│       ├── auth.py             # Login, register, password reset, Firebase login
│       ├── settings.py         # Business info, themes, locations, products
│       ├── invoices.py         # Invoice CRUD + PDF generation
│       ├── reports.py          # Sales reports
│       ├── cart.py             # Shopping cart
│       ├── orders.py           # Order management
│       ├── reservations.py     # Reservation queue
│       ├── client.py           # Client dashboard aggregation
│       ├── dashboard.py        # Dashboard modules/settings
│       ├── payment_methods.py  # Payment method CRUD
│       ├── payments.py         # Stripe integration
│       ├── coupons.py          # Coupon/voucher management
│       └── flash_sales.py      # Flash sale management
│
├── frontend/                   # Static frontend (no build step)
│   ├── index.html              # Landing page
│   ├── css/
│   │   ├── style.css           # Main application styles
│   │   └── landing.css         # Landing page styles
│   ├── js/
│   │   ├── api.js              # API client (fetch wrapper, auth headers)
│   │   ├── dashboard.js        # Dashboard page logic
│   │   ├── login.js            # Login/auth page logic
│   │   ├── products.js         # Product management
│   │   ├── services.js         # Service management
│   │   ├── invoices.js         # Invoice page logic
│   │   ├── reports.js          # Reports page logic
│   │   ├── settings.js         # Settings page logic
│   │   ├── permissions.js      # Permissions management
│   │   ├── profile.js          # User profile
│   │   ├── menu.js             # Sidebar/navigation
│   │   ├── toast.js            # Toast notification utility
│   │   ├── firebase-config.js  # Firebase SDK initialization
│   │   └── ...
│   └── *.html                  # One HTML file per page (SPA-like navigation)
│
├── commands/                   # CLI scripts for setup, migrations, seeding
│   ├── database/               # DB migrations and seed scripts
│   ├── users/                  # User creation scripts
│   ├── permissions/            # Permission setup scripts
│   ├── ecommerce/              # E-commerce data setup
│   ├── dashboard/              # Dashboard customization scripts
│   └── testing/                # Test/verification scripts
│
├── docker-compose.yml          # Local dev: PostgreSQL + FastAPI
├── Dockerfile                  # Production container image
├── render.yaml                 # Render deployment blueprint
├── vercel.json                 # Vercel frontend routing config
├── requirements.txt            # Python dependencies (pinned versions)
└── .env                        # Local environment variables (not committed)
```

## Architecture Patterns

- **Backend**: All business logic lives in `crud.py`. Routers are thin — they validate input, call CRUD functions, and return responses.
- **Multi-tenancy**: `business_number` field on users. `get_business_user_ids()` in crud.py resolves all users in the same business for data filtering.
- **Soft deletes**: Records use `status = "A"/"D"` and `deleted_at` timestamp instead of hard deletes.
- **Frontend routing**: Each page is a separate HTML file. `api.js` provides a centralized API client object. No SPA router — navigation is full page loads.
- **Migrations**: No Alembic. Manual Python scripts in `commands/database/` that run `ALTER TABLE` statements directly.
- **Auth flow**: JWT stored in localStorage. `api.js` attaches Bearer token to all requests. 401 responses redirect to login.
- **API prefix**: All backend endpoints are under `/api/`. Frontend is served from root `/`.
