---
description: Pre-coding checklist and workflow instructions for the AI coding assistant
---

# 🤖 AI Coding Assistant — Instructions

> **ALWAYS read this file FIRST before writing any code.**

## Pre-Coding Checklist

### Step 1: Read Project Context
1. Read `SYSTEM_UPDATES_DATA_HISTORY_LOGS.md` — understand what was done in previous sessions.
2. Read `PROJECT_ROADMAP.md` — know the current state of features and what's planned next.
3. Check the **Change Log** section at the bottom of `SYSTEM_UPDATES_DATA_HISTORY_LOGS.md` for the latest version and date.

### Step 2: Initialize lean-ctx (Token Savings)
```
# Clear cache at the start of a new session
ctx_cache action=clear

# Read files using lean-ctx tools instead of built-in Read:
ctx_read / ctx_multi_read / ctx_smart_read   — for reading files
ctx_search                                    — for grep/search
ctx_tree                                      — for directory listings
ctx_shell                                     — for shell command output
ctx_delta                                     — for incremental file updates
```

### Step 3: Understand the User Request
- Ask for clarification if the request is ambiguous.
- Identify which files need to be modified.
- Use `ctx_multi_read` with `signatures` mode to scan multiple files quickly.
- Use `ctx_read` with `full` mode only for files you'll actually edit.

## During Development

### Coding Guidelines
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL (runs in Docker)
- **Frontend**: Vanilla HTML/CSS/JS served as static files
- **Auth**: JWT-based, roles = `superadmin`, `admin`, `user`, `client`
- **Database changes**: Always create a migration script in `commands/database/` — never assume tables/columns exist
- **Docker**: After backend code changes, run `docker-compose up --build -d` to rebuild
- **Testing**: Use `Invoke-RestMethod` (PowerShell) for API testing, use browser subagents for UI testing

### Key Project Files
| Purpose | Path |
|---------|------|
| Database models | `app/database.py` |
| API schemas | `app/schemas.py` |
| CRUD operations | `app/crud.py` |
| Auth routes | `app/routers/auth.py` |
| Settings routes | `app/routers/settings.py` |
| Order routes | `app/routers/orders.py` |
| Reservation routes | `app/routers/reservations.py` |
| Invoice routes | `app/routers/invoices.py` |
| Email service | `app/email_service.py` |
| SMS service (paused) | `app/sms_service.py` |
| Frontend API layer | `frontend/js/api.js` |
| DB seed script | `commands/fill_db_with_data.py` |
| Docker compose | `docker-compose.yml` |

### Important Accounts
| Role | Email | Password |
|------|-------|----------|
| Superadmin/Owner | `owner@carwash.com` | `owner123` |
| Demo Client | `demo-client@carwash.com` | `demo123` |
| Demo Staff | `demo-staff@carwash.com` | `demo123` |
| Demo Admin | `demo-admin@carwash.com` | `demo123` |

## Post-Coding Checklist

### Step 4: Update Documentation
After completing a feature or debugging session, **always update**:

1. **`PROJECT_ROADMAP.md`**
   - Mark completed items with `[x]`
   - Add new items if new features were discussed
   - Update the phase priorities if needed

2. **`SYSTEM_UPDATES_DATA_HISTORY_LOGS.md`**
   - Update the `Last Updated` date at the top
   - Add a new section under "Latest Updates" describing what was done
   - List files created/modified
   - Add database changes if any
   - Update the **Change Log** at the bottom with a new version entry

### Step 5: Verify
- Confirm Docker containers are running: `docker-compose ps`
- Test the feature via browser or API
- Check Docker logs for errors: `docker-compose logs --tail=20 web`

## Notes
- SMS service (Twilio) is currently **commented out** — no subscription yet
- Lint errors about missing imports (`sqlalchemy`, `pydantic`, etc.) are false positives — those packages exist inside the Docker container, not locally
- The `.env` file contains sensitive credentials — never commit it
- Database migrations go in `commands/database/` and are run inside Docker via: `docker-compose exec web python commands/database/<script>.py`
