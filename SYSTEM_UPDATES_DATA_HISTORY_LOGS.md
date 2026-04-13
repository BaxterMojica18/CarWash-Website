# System Updates, Data & History Logs

> **Last Updated:** April 7, 2026  
> **Version:** 4.2.0  
> **Branch:** main

---

## 📋 Table of Contents
1. [Latest Updates (Nov 23, 2025)](#latest-updates-nov-23-2025)
2. [Dashboard Customization System](#dashboard-customization-system)
3. [Permissions Management System](#permissions-management-system)
4. [Demo Accounts System](#demo-accounts-system)
5. [E-Commerce Features](#e-commerce-features)
6. [Superadmin Role](#superadmin-role)
7. [Setup Instructions](#setup-instructions)
8. [API Documentation](#api-documentation)

---

## Latest Updates (April 7, 2026)

### 🚀 Production Deployment Fixes & Email CC System
**Status:** ✅ Completed

#### Issues Fixed:
- **Password Reset Links Pointed to Localhost:**
  - `send_password_reset_email()` was using `http_request.base_url` (= Render backend URL) instead of the Vercel frontend URL.
  - Fix: Now uses `FRONTEND_URL` env var (`https://car-wash-website-khaki.vercel.app`) for all reset links.
  - Console fallback also updated.

- **Emails Not Working / No CC on Emails:**
  - Added `CC_EMAIL` env var — every email sent by the system now CCs `baxterdavid.mojica@gmail.com`.
  - Updated `send_email()` to build a `recipients` list (To + CC) and set the `Cc` header.
  - All email types affected: password reset, OTP, order confirmation, order status, reservation confirmation, reservation status.

- **Sidebar Tabs Not Reflecting Per-Business Changes:**
  - `RoleSidebarSetting` was global (no business scoping) — if Business A hid a tab, it also hid for Business B.
  - Added `business_number` column to `role_sidebar_settings` table (defaults to `'__global__'`).
  - All 4 queries updated: `GET /me/permissions`, `GET /users`, `GET /users/{id}`, `GET/PUT /roles/{id}/sidebar`.
  - Now each business has independent sidebar configurations.

- **Render Deployment Not Running Migrations:**
  - Dockerfile used bare `uvicorn` command — no migrations ran on deploy.
  - Created `start.sh` startup script that runs `create_tables()`, `migrate_db.py`, `add_signup_columns.py`, and column migrations before starting uvicorn.
  - Updated `Dockerfile` to use `start.sh` as CMD.

- **CORS Origins Hardcoded:**
  - Made `allow_origins` dynamic by reading `FRONTEND_URL` from env var.

#### New Environment Variables:
| Variable | Default | Purpose |
|----------|---------|----------|
| `FRONTEND_URL` | `https://car-wash-website-khaki.vercel.app` | Used in reset links, email buttons, CORS |
| `CC_EMAIL` | `baxterdavid.mojica@gmail.com` | CCs all system emails for trailing |

#### Files Created/Modified:
- ✅ `app/email_service.py` — CC on every email, `FRONTEND_URL` for reset links
- ✅ `app/routers/auth.py` — Removed `base_url` from forgot-password, business-scoped sidebar queries
- ✅ `app/database.py` — Added `business_number` to `RoleSidebarSetting`
- ✅ `app/main.py` — Dynamic CORS origins from `FRONTEND_URL`
- ✅ `Dockerfile` — Runs `start.sh` for migration-first startup
- ✅ `start.sh` — NEW: Startup script with all migrations
- ✅ `render.yaml` — Added `FRONTEND_URL` and `CC_EMAIL` env vars
- ✅ `.env` — Added `FRONTEND_URL` and `CC_EMAIL`
- ✅ `docker-compose.yml` — Added `business_number` column migration

#### Deployment Checklist (Render):
> [!IMPORTANT]
> After pushing, set these env vars in Render dashboard:
> - `FRONTEND_URL` = `https://car-wash-website-khaki.vercel.app`
> - `CC_EMAIL` = `baxterdavid.mojica@gmail.com`
> - `SMTP_SERVER` = `smtp.gmail.com`
> - `SMTP_PORT` = `587`
> - `SMTP_USERNAME` = `baxterdavid.mojica@gmail.com`
> - `SMTP_PASSWORD` = *(Gmail app password)*
> - `FROM_EMAIL` = `baxterdavid.mojica@gmail.com`

---

## Updates (April 4, 2026 — Session 2)

### 🏢 Shared Business Branding & Client Theme System
**Status:** ✅ Completed

#### Features Added:
- **Multi-Tenant Demo Account Overhaul:**
  - Created `commands/users/setup_demo_accounts.py` — full automated setup script.
  - **Business 1 — BuxWash (BXTK-001):**
    - `owner@carwash.com` / `owner123` (superadmin)
    - `admin@carwash.com` / `admin123` (admin)
    - `staff@carwash.com` / `staff123` (user/staff)
    - `demo-client@carwash.com` / `demo123` (client)
  - **Business 2 — SparkleWash (WASH-002):** (for data isolation testing)
    - `owner2@sparklewash.com` / `owner123` (owner)
    - `client@sparklewash.com` / `client123` (client)
  - Each business has unique products, services, locations, invoices, orders, and reservations.
  - Script runs automatically on Docker startup.

- **Shared Business Branding (Owner-Scoped Saves):**
  - When admin/owner saves business name, logo, or invoice settings → saves to the **owner's DB record**.
  - All staff/admin in the same business see the same branding in their sidebar.
  - Affected endpoints: `POST /settings/business`, `POST /settings/theme`, `PUT /settings/theme/{id}/activate`, `POST /settings/invoice-custom`.
  - Powered by `get_business_owner_id()` resolving all saves to the owner.

- **Client-Specific Theme System:**
  - Added `for_client` boolean column to `settings_theme_selection` table.
  - Admin can check "🛒 Save for Client Only" to create a separate color scheme for client-facing pages.
  - `GET /settings/theme/active` auto-detects if user is a client and serves the client theme if one exists.
  - New endpoints: `GET /settings/theme/client/active`, `GET /settings/theme/client/all`.
  - New UI: "Client Theme Presets" section with its own dropdown in Settings.

- **Demo Login Credentials Updated:**
  - `frontend/js/demo.js` now uses `staff@carwash.com` (staff), `admin@carwash.com` (admin), `demo-client@carwash.com` (client).
  - Old `demo@carwash.com` with incorrect admin privileges is no longer used.

#### Files Created/Modified:
- ✅ `commands/users/setup_demo_accounts.py` — Multi-tenant demo data setup (NEW)
- ✅ `app/routers/settings.py` — All saves use `owner_id`; client theme endpoints added
- ✅ `app/crud.py` — Theme functions support `for_client` filtering
- ✅ `app/schemas.py` — Added `for_client: bool` to CustomTheme schemas
- ✅ `app/database.py` — Added `for_client` column to CustomTheme model
- ✅ `frontend/settings.html` — "Save for Client Only" toggle + Client Theme Presets section
- ✅ `frontend/js/settings.js` — Theme form sends `for_client`, client preset management
- ✅ `frontend/js/demo.js` — Updated demo credentials
- ✅ `docker-compose.yml` — Added demo setup script + `for_client` migration to startup

#### Verified Results:
- ✅ Admin changes business name → Staff sees updated name in sidebar
- ✅ BuxWash (61 invoices) vs SparkleWash (25 invoices) — data fully isolated
- ✅ Staff sidebar: Settings tab hidden
- ✅ Client theme saves and loads independently from staff theme

---

## Updates (April 4, 2026 — Session 1)

### 🔒 Multi-Tenant Data Isolation & Deployment Configuration
**Status:** ✅ Completed

#### Features Added:
- **Multi-Tenant Data Isolation (Business Number Scoping):**
  - Added `get_business_user_ids()` helper that finds all users sharing the same `business_number`.
  - Added `get_business_owner_id()` helper that resolves the owner for shared settings (themes, business info).
  - **Locations**: Only returns locations created by users in the same business.
  - **Products/Services**: Only returns products/services created by users in the same business.
  - **Invoices**: Only returns invoices created by users in the same business.
  - **Orders**: Admin/owner views now scoped to orders from clients in the same business.
  - **Reservations**: Admin/owner views now scoped to reservations from clients in the same business.
  - **Reports**: Sales reports filtered to business-scoped invoices.
  - **Dashboard**: Settings and modules resolved via the business owner, so all staff see consistent dashboard.
  - **Themes/Business Info**: Looked up via the business owner, shared across all business members.
  - **User Listing**: Admins only see users with the same `business_number`.

- **Staff Sidebar Permissions Fix:**
  - Removed "Settings" from `STAFF_TABS` array in `menu.js`.
  - Settings tab now dynamically added only for `admin`, `owner`, and `superadmin` roles.
  - Staff (role=user) will no longer see the Settings link in the sidebar.

- **Production Deployment Configuration:**
  - Created `vercel.json` for deploying to Vercel (routes API to backend, serves static frontend).
  - Created `render.yaml` for deploying to Render (Docker + managed PostgreSQL).
  - Updated `frontend/js/api.js` with dynamic `API_BASE` detection (localhost vs production origin).
  - Dashboard management endpoints relaxed from `is_superadmin` to `is_admin_or_owner` for broader access.

#### Files Created/Modified:
- ✅ `app/crud.py` — Added `get_business_user_ids()`, `get_business_owner_id()`, scoped all read queries
- ✅ `app/routers/settings.py` — Business-scoped locations, products, themes, business info
- ✅ `app/routers/invoices.py` — Business-scoped invoice listing and dashboard stats
- ✅ `app/routers/orders.py` — Business-scoped order listing for admins
- ✅ `app/routers/reservations.py` — Business-scoped reservation listing for admins
- ✅ `app/routers/reports.py` — Business-scoped sales reports
- ✅ `app/routers/dashboard.py` — Owner-resolved dashboard settings/modules
- ✅ `app/routers/auth.py` — Business-scoped user listing
- ✅ `frontend/js/menu.js` — Staff sidebar: Settings removed, role-guarded
- ✅ `frontend/js/api.js` — Dynamic API_BASE for production
- ✅ `vercel.json` — Vercel deployment config (NEW)
- ✅ `render.yaml` — Render deployment config (NEW)

---

## Latest Updates (April 1, 2026)

### 🏎️ Advanced Sidebar & Registration Flow
**Status:** ✅ Completed

#### Features Added:
- **Premium Sidebar UX:**
  - **Mini-Sidebar Mode**: Implemented a responsive "icon-only" state for desktop.
  - **Dynamic Visibility**: Labels and Logos are hidden in mini-mode, showing only centered SVG icons.
  - **Invisible Toggle**: The sidebar is now clickable anywhere on its strip to expand from mini-mode.
  - **Minimal Navigation**: Replaced "X" and Hamburger buttons with a sleek, semi-transparent left-arrow chevron that disappears when collapsed.
  - **Normalization**: Created a global Icon Normalizer that converts all legacy icons to a consistent, high-performance SVG set.
- **Enhanced Registration Flow:**
  - **Account Triage**: New `account-type.html` selection page (Client vs Owner vs Admin).
  - **Role-Based Provisioning**: 
    - **Owners**: Automatically assigned "owner" role and prompted for a Business Number.
    - **Admins**: Assigned "admin" role (restricted creation).
    - **Clients**: Standard user onboarding.
  - **Validation**: Added `account_type` and `business_number` columns to the PostgreSQL User model with automatic database migration.
- **Environment & Dev Productivity:**
  - **VENV Automation**: Created `setup.ps1` and `start.ps1` for one-click environment management.
  - **Auto-Migrations**: The backend now automatically checks for and applies database migrations (`add_signup_columns.py`) on startup.
- **Reactive Branding & UI Reliability (Latest):**
  - **Storage-First Rendering**: Implemented `localStorage` caching for both Business Branding (Name/Logo) and Sidebar Tabs/Permissions. This eliminates the 0.5s "network flash" on page transitions.
  - **Real-time Sync**: Sidebar branding now updates instantly across all open tabs when changes are saved in the Settings panel.
  - **"No Logo" Support**: Introduced `none` logo type to allow users to completely remove their business logo via settings without fallback icons reappearing.
  - **Template Hygiene**: Scrubbed hardcoded list items and placeholders from over 10+ HTML files to ensure a single source of truth (JS-driven).

#### Files Created/Modified:
- ✅ `frontend/js/menu.js` (Major Sidebar Overhaul)
- ✅ `frontend/css/style.css` (Fluid Transitions & Mini-Mode)
- ✅ `frontend/account-type.html` (New Triage Page)
- ✅ `frontend/signup.html` (Dynamic Role Forms)
- ✅ `app/database.py` & `app/schemas.py` (Extended User Model)
- ✅ `commands/database/add_signup_columns.py` (Schema Migration)
- ✅ `setup.ps1` / `start.ps1` (Dev Environment)

---

## Latest Updates (March 30, 2026)

### 🔥 Firebase Authentication Migration
**Status:** ✅ Completed

#### Features Added:
- **Client-Side Firebase Integration:**
  - Initialized Firebase web SDK pointing to personal project `carwash-mgmt-system-41402`.
  - Added Firebase Google Sign-in alongside legacy local email/password authentication.
  - Intercepted frontend login flow using `signInWithPopup` to return fresh ID tokens.
- **Backend Admin SDK Token Verification:**
  - Installed `firebase-admin` into the FastAPI backend Docker image.
  - Added `clock_skew_seconds=60` tolerance to `verify_id_token` to fix intermittent clock desync errors during Google Login.
  - Hardened backend against spoofed tokens powered by securely injected `firebase-credentials.json` Service Account.
- **Bi-directional PostgreSQL Auto-Syncing & Schema Fixes:**
  - Built `get_or_create_firebase_user` mapping function that instantly replicates validated Firebase Identities into native PostgreSQL rows via standard JWT exchanges.
  - Expanded `app/database.py` with `DashboardSettings` and `DashboardModule` declarative models to resolve 500 errors when hybrid users load the dashboard.
  - Modified `crud.get_user_profile` to gracefully build default user profiles on-the-fly, fixing 404 `/profile` errors on newly migrated or demo accounts.
  - Updated `login.js` UI hooks by stripping deferred `DOMContentLoaded` listeners, allowing the demo login buttons to function seamlessly with ES Modules.

#### Files Created/Modified:
- ✅ `frontend/js/firebase-config.js`
- ✅ `frontend/js/login.js`
- ✅ `frontend/signup.html`
- ✅ `app/firebase_auth.py`
- ✅ `app/crud.py`
- ✅ `app/database.py`
- ✅ `app/routers/auth.py`
- ✅ `app/firebase-credentials.json`

---

### 🔐 Password Reset & Email Integration
**Status:** ✅ Completed

#### Features Added:
- **Forgot Password Flow:**
  - Secure token generation and 15-minute expiration logic.
  - Dedicated `/forgot-password.html` and `/reset-password.html` UI flows.
  - Database table `password_reset_tokens` for token management.
- **Gmail SMTP Integration:**
  - Configurable SMTP environment variables (`SMTP_SERVER`, `SMTP_PORT`, etc.).
  - Centralized `email_service.py` to handle HTML and plain text emails.
  - Professional HTML email template for password reset.
- **SMS Infrastructure (Prepared):**
  - Database schema updated to include `phone_number` in users and new `user_preferences` table.
  - CRUD operations and API endpoints (`/api/settings/profile`) created.
  - Frontend profile UI updated to collect phone numbers and SMS opt-in status.
  - *Note: Actual Twilio dispatch is currently commented out pending subscription.*

#### Files Created/Modified:
- ✅ `frontend/forgot-password.html`
- ✅ `frontend/reset-password.html`
- ✅ `app/email_service.py`
- ✅ `app/sms_service.py`
- ✅ `app/routers/auth.py`
- ✅ `app/routers/settings.py`
- ✅ `app/crud.py`
- ✅ `app/schemas.py`

---

### 🔢 6-Digit OTP Password Reset
**Status:** ✅ Completed  
**Date:** March 29, 2026

#### Features Added:
- **OTP Generation & Validation:**
  - 6-digit random numeric OTP generated alongside UUID reset token.
  - `otp_code` column added to `password_reset_tokens` table with index.
  - OTP verification endpoint: `POST /api/auth/verify-otp`.
  - OTP expires after 15 minutes (same as token).
- **Method Selection UI:**
  - 3-step forgot-password flow: Email → Choose Method → Reset.
  - Two selectable method cards: "Email Reset Link" (🔗) and "6-Digit Verification Code" (🔢).
  - Only ONE email is sent based on the user's chosen method (no duplicate emails).
  - Button text dynamically updates based on selection.
- **OTP Entry UI:**
  - 6 individual digit input boxes with auto-advance on input.
  - Paste support (distribute pasted digits across all 6 boxes).
  - Backspace navigation between boxes.
  - 60-second resend cooldown timer.
  - "← Use a different method" link to go back and choose another option.
- **Styled OTP Email Template:**
  - Professional HTML email with gradient header.
  - Large, monospace OTP code displayed prominently.
  - Expiry warning and security notice.

#### API Changes:
- `POST /api/auth/forgot-password` — now accepts `reset_method` parameter (`"link"` or `"otp"`).
- `POST /api/auth/verify-otp` — new endpoint; validates OTP and returns reset token.

#### Files Created/Modified:
- ✅ `app/database.py` — added `otp_code` column to `PasswordResetToken` model
- ✅ `app/crud.py` — OTP generation in `create_password_reset_token()`, new `validate_otp_code()`
- ✅ `app/schemas.py` — added `reset_method` to `ForgotPasswordRequest`, new `VerifyOtpRequest`/`VerifyOtpResponse`
- ✅ `app/routers/auth.py` — updated `forgot_password()` to branch by method, new `verify_otp()` endpoint
- ✅ `app/email_service.py` — new `send_otp_email()` with styled HTML template
- ✅ `frontend/forgot-password.html` — redesigned as 3-step flow with method selection cards
- ✅ `frontend/js/api.js` — added `verifyOtp()` method, updated `forgotPassword()` to pass `reset_method`
- ✅ `commands/database/upgrade_otp.py` — migration script for `otp_code` column

#### Database Changes:
```sql
ALTER TABLE password_reset_tokens ADD COLUMN otp_code VARCHAR(6);
CREATE INDEX ix_password_reset_tokens_otp_code ON password_reset_tokens (otp_code);
```

---

### 📊 Database Seeding & Order Management Fixes
**Status:** ✅ Completed  
**Date:** March 14-29, 2026

#### Features Added:
- **Database Seeding Script** (`commands/fill_db_with_data.py`):
  - Populates all tables: products, services, orders, invoices, queue reservations.
  - Includes sample data across all order statuses.
- **New Order/Queue Statuses:**
  - Added `delayed` and `cancelled` statuses to orders and reservations.
- **Superadmin Role Fix:**
  - Fixed `superadmin` role not being included in global data visibility checks.
  - Updated `orders.py` and `reservations.py` to allow `superadmin` role full access.

#### Files Modified:
- ✅ `app/routers/orders.py` — added `superadmin` to role checks
- ✅ `app/routers/reservations.py` — added `superadmin` to role checks
- ✅ `commands/fill_db_with_data.py` — comprehensive sample data seeder

---

## E-Commerce Features
**Status:** ✅ Completed

#### Features Added:
- **8 Customizable Colors:**
  - Sidebar Color
  - Background Color
  - Primary Color
  - Button Color
  - Text Color
  - Sidebar Active Color
  - Card Color
  - Card Text Color

- **Interactive Dashboard Editor:**
  - Drag-and-drop module reordering
  - Resizable modules (Full, Half, Third, Quarter width)
  - 17 predefined module templates
  - Live preview of changes
  - Collapsible customization panel with resize handle

- **Module Templates:**
  - Revenue (7 types): Total, Average, Weekly, Monthly, Bi-Monthly, Semi-Annual, Annual
  - Invoices (2 types): Total, Average
  - Services (2 types): Total, Popular
  - Products (2 types): Total, Popular
  - Recent Activity
  - Custom Chart
  - Custom Table

- **UI Enhancements:**
  - Floating edit button (bottom-right, superadmin only)
  - 12-column grid system
  - Clean card design with colored borders
  - Responsive layout options (Grid, List, Compact)

#### Files Created/Modified:
- ✅ `frontend/edit-dashboard.html` - Visual dashboard editor
- ✅ `frontend/dashboard.html` - Updated with floating button
- ✅ `frontend/js/dashboard.js` - Dashboard rendering logic
- ✅ `app/routers/dashboard.py` - Dashboard API endpoints
- ✅ `create_dashboard_customization.py` - Database setup script
- ✅ `add_color_columns.py` - Add color columns to database

#### Database Changes:
```sql
-- New Tables
CREATE TABLE dashboard_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    website_name VARCHAR(255) DEFAULT 'CarWash',
    primary_color VARCHAR(7) DEFAULT '#667eea',
    background_color VARCHAR(7) DEFAULT '#f5f5f5',
    sidebar_color VARCHAR(7) DEFAULT '#2c3e50',
    button_color VARCHAR(7) DEFAULT '#667eea',
    text_color VARCHAR(7) DEFAULT '#333333',
    sidebar_active_color VARCHAR(7) DEFAULT '#34495e',
    card_color VARCHAR(7) DEFAULT '#ffffff',
    card_text_color VARCHAR(7) DEFAULT '#333333',
    layout_type VARCHAR(50) DEFAULT 'grid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dashboard_modules (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    module_name VARCHAR(255) NOT NULL,
    module_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    position INTEGER DEFAULT 0,
    width VARCHAR(50) DEFAULT 'full',
    is_visible BOOLEAN DEFAULT TRUE,
    config JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Dashboard Customization System

### Access
**Superadmin Only:**
- Login: `owner@carwash.com` / `owner123`
- Click floating ✏️ button on dashboard
- Or go to: `http://localhost:8000/edit-dashboard.html`

### How to Use

#### 1. Customize Colors
```
Right Panel → Colors Section
- Pick any of 8 colors
- Changes apply instantly to preview
```

#### 2. Add Modules
```
Right Panel → Add Module Section
1. Select module type from dropdown
2. Enter module title (auto-filled)
3. Select width (Full/Half/Third/Quarter)
4. Click "+ Add Module"
```

#### 3. Reorder Modules
```
Dashboard Preview Area
1. Click and hold on any module
2. Drag to new position
3. Drop to place
```

#### 4. Resize Modules
```
Module Width Controls (bottom-left of each module)
- Full: 12 columns (100%)
- 1/2: 6 columns (50%)
- 1/3: 4 columns (33%)
- 1/4: 3 columns (25%)
```

#### 5. Delete Modules
```
Click ✕ button in top-right corner of module
```

#### 6. Save Changes
```
Right Panel → Bottom
Click "💾 Save Changes"
→ Redirects to dashboard with new settings
```

### API Endpoints
```http
GET  /api/dashboard/settings          - Get dashboard settings
POST /api/dashboard/settings          - Save dashboard settings
GET  /api/dashboard/modules           - Get dashboard modules
POST /api/dashboard/modules           - Create module
PUT  /api/dashboard/modules/{id}      - Update module
DELETE /api/dashboard/modules/{id}    - Delete module
```

---

## Permissions Management System

### Overview
Comprehensive role-based access control (RBAC) system with 8 granular permissions.

### Available Permissions

| Permission | Description | Default Roles |
|------------|-------------|---------------|
| `manage_products` | Add, edit, delete products | Superadmin, Admin |
| `manage_locations` | Add, edit, delete washing bays | Superadmin, Admin |
| `view_locations` | View washing bays (read-only) | Superadmin, Admin, User |
| `manage_invoices` | Create, edit, delete invoices | Superadmin, Admin, User |
| `view_invoices` | View invoices (read-only) | Superadmin, Admin, User |
| `view_reports` | Access sales reports | Superadmin, Admin, User |
| `manage_settings` | Modify theme and settings | Superadmin, Admin |
| `manage_users` | Manage user permissions | Superadmin |

### User Roles

#### Role Hierarchy
```
superadmin (owner)
    ↓
admin
    ↓
user (staff)
    ↓
client
```

#### Role Permissions Matrix

| Permission | Superadmin | Admin | User (Staff) | Client |
|------------|-----------|-------|--------------|--------|
| manage_products | ✅ | ✅ | ❌ | ❌ |
| manage_locations | ✅ | ✅ | ❌ | ❌ |
| view_locations | ✅ | ✅ | ✅ | ❌ |
| manage_invoices | ✅ | ✅ | ✅ | ❌ |
| view_invoices | ✅ | ✅ | ✅ | ❌ |
| view_reports | ✅ | ✅ | ✅ | ❌ |
| manage_settings | ✅ | ✅ | ❌ | ❌ |
| manage_users | ✅ | ❌ | ❌ | ❌ |

### Access Permissions Management

**For Admin/Superadmin:**
1. Login with admin/superadmin account
2. Go to Settings → User Management
3. Click "🔐 Manage Permissions"
4. Or directly: `http://localhost:8000/permissions-management.html`

### Features
- 📊 Statistics dashboard (Total users, Admin users, Staff users)
- 🔍 Search users by email
- 🎯 Filter by role
- 🎛️ Toggle switches for each permission
- 💾 Auto-save on toggle
- 🎨 Modern, responsive UI

### API Endpoints
```http
GET  /api/auth/users                  - List all users with permissions
GET  /api/auth/permissions/all        - Get all available permissions
GET  /api/auth/roles/all              - Get all roles
PUT  /api/auth/users/permissions      - Update user permissions
PUT  /api/auth/users/roles            - Update user roles
GET  /api/auth/me/permissions         - Get current user permissions
```

---

## Demo Accounts System

### Overview
Three demo accounts with usage limits to prevent abuse while allowing full exploration.

### Demo Account Credentials

#### 1. Client Perspective
```
Email: demo-client@carwash.com
Password: demo123
Role: Client
Limits: 10 orders, 10 reservations
```

**Features:**
- Browse products and services
- Add items to cart
- Place orders
- Make service reservations
- View order history

#### 2. Staff Perspective
```
Email: demo-staff@carwash.com
Password: demo123
Role: User (Staff)
Limits: 10 invoices
```

**Features:**
- Create invoices
- View sales reports
- View dashboard statistics
- Limited admin features

#### 3. Admin Perspective (Limited)
```
Email: demo-admin@carwash.com
Password: demo123
Role: Demo Admin
Limits: 1 product, 1 service, 10 invoices
```

**Features:**
- Create invoices
- View reports
- Limited product management
- Cannot manage users

### Usage Limits

| Account | Products | Services | Orders | Reservations | Invoices |
|---------|----------|----------|--------|--------------|----------|
| demo-client | - | - | 10 | 10 | - |
| demo-staff | - | - | - | - | 10 |
| demo-admin | 1 | 1 | - | - | 10 |

### Setup
```bash
# Create demo accounts
python create_demo_users.py
# or
create_demo_users.bat
```

### Database Table
```sql
CREATE TABLE demo_usage_limits (
    user_id INTEGER PRIMARY KEY,
    products_created INTEGER DEFAULT 0,
    services_created INTEGER DEFAULT 0,
    orders_created INTEGER DEFAULT 0,
    reservations_created INTEGER DEFAULT 0,
    invoices_created INTEGER DEFAULT 0,
    max_products INTEGER DEFAULT 1,
    max_services INTEGER DEFAULT 1,
    max_orders INTEGER DEFAULT 10,
    max_reservations INTEGER DEFAULT 10,
    max_invoices INTEGER DEFAULT 10
);
```

---

## E-Commerce Features

### Overview
Complete shopping cart, order management, and service reservation system with FIFO queue.

### Features

#### For Clients
- 🛒 Shopping Cart - Add products and checkout
- 📦 Order Management - Place orders and track status
- 🚗 Service Reservations - Reserve car wash with queue position
- 📊 Client Dashboard - View orders, reservations, and history

#### For Owner/Admin
- 📋 Order Management - Accept/reject orders, update status
- 🎯 Queue Management - Manage service reservations and queue
- 👥 Client Role - New role for customers

### New Pages

#### Client Pages
- `/shop.html` - Browse products and services
- `/cart.html` - Shopping cart
- `/reserve.html` - Reserve car wash service
- `/client-dashboard.html` - Client dashboard

#### Owner/Admin Pages
- `/order-management.html` - Manage customer orders
- `/queue-management.html` - Manage service queue

### API Endpoints

#### Cart
```http
GET    /api/cart              - Get cart items
POST   /api/cart              - Add to cart
PATCH  /api/cart/{id}         - Update quantity
DELETE /api/cart/{id}         - Remove item
DELETE /api/cart/clear/all    - Clear cart
```

#### Orders
```http
POST   /api/orders            - Create order
GET    /api/orders            - List orders
GET    /api/orders/{id}       - Get order details
PATCH  /api/orders/{id}/status - Update status
```

#### Reservations
```http
POST   /api/reservations      - Create reservation
GET    /api/reservations      - List reservations
GET    /api/reservations/queue - Get queue
GET    /api/reservations/{id} - Get reservation details
PATCH  /api/reservations/{id}/status - Update status
```

### Queue Management Logic

#### How Queue Works
1. Client creates reservation → Assigned next queue position
2. Owner accepts → Stays in queue with same position
3. Owner starts service → Status: "in_progress"
4. Owner completes → Removed from queue, positions shift down
5. Client cancels → Removed from queue, positions recalculated

#### Status Flow
```
pending → accepted → in_progress → completed
   ↓
cancelled
```

### Database Tables
```sql
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES users(id),
    product_service_id INTEGER REFERENCES product_service(id),
    quantity INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR UNIQUE,
    client_id INTEGER REFERENCES users(id),
    total_amount DECIMAL(10,2),
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_service_id INTEGER REFERENCES product_service(id),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    subtotal DECIMAL(10,2)
);

CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    reservation_number VARCHAR UNIQUE,
    client_id INTEGER REFERENCES users(id),
    service_id INTEGER REFERENCES product_service(id),
    location_id INTEGER REFERENCES locations(id),
    vehicle_plate VARCHAR,
    queue_position INTEGER,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Superadmin Role

### Overview
Highest level of access with complete control over all users including admins.

### Superadmin Account
```
Email: owner@carwash.com
Password: owner123
```

### Setup
```bash
python create_superadmin.py
# or
create_superadmin.bat
```

### Key Features
- ✅ Can see ALL users including admins
- ✅ Can modify admin permissions
- ✅ Can create/delete any user
- ✅ Hidden from admin view
- ✅ Complete system access

### Differences from Admin

| Feature | Superadmin | Admin |
|---------|-----------|-------|
| See all users | ✅ Yes | ⚠️ No (can't see superadmins) |
| Manage admins | ✅ Yes | ❌ No |
| Manage superadmins | ✅ Yes | ❌ No |
| Full system access | ✅ Yes | ✅ Yes |
| Hidden from lower roles | ✅ Yes | ❌ No |

---

## Setup Instructions

### Complete Setup

#### 1. Database Setup
```bash
# Create database
python create_db.py

# Seed data
python seed_data.py
```

#### 2. Create Accounts
```bash
# Create superadmin
python create_superadmin.py

# Create demo accounts
python create_demo_users.py
```

#### 3. Setup E-Commerce
```bash
# Create e-commerce tables
python add_ecommerce_tables.py

# Create client user
python create_client_user.py
```

#### 4. Setup Dashboard Customization
```bash
# Create dashboard tables
python create_dashboard_customization.py

# Add color columns
python add_color_columns.py
```

#### 5. Setup Permissions
```bash
# Add permissions
python add_permissions.py

# Add new permissions
python add_new_permissions.py
```

#### 6. Start Server
```bash
start_server.bat
```

### Quick Setup (Automated)
```bash
# E-commerce setup
setup_ecommerce.bat

# Permissions setup
RUN_PERMISSION_SETUP.bat
```

---

## API Documentation

### Access
Once server is running:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Authentication
All API endpoints require JWT token:
```http
Authorization: Bearer {token}
```

### Get Token
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

---

## Change Log

### Version 4.0.0 (April 4, 2026)
- ✅ **Multi-Tenant Data Isolation**: All data queries (locations, products, invoices, orders, reservations, reports, dashboard) now scoped by `business_number`
- ✅ Added `get_business_user_ids()` and `get_business_owner_id()` helpers to `crud.py`
- ✅ **Staff Sidebar Fix**: Settings tab hidden from staff, visible only to admin/owner/superadmin
- ✅ **Vercel Deployment**: Created `vercel.json` for production deployment
- ✅ **Render Deployment**: Created `render.yaml` with Docker + managed PostgreSQL blueprint
- ✅ **Dynamic API_BASE**: Frontend auto-detects production vs local environment
- ✅ Dashboard settings/modules endpoints relaxed from superadmin-only to admin/owner access
- ✅ User listing scoped to same business (admins can't see users from other businesses)

### Version 3.0.0 (March 30, 2026)
- ✅ **New Feature**: Role-Based dynamic Sidebar Navigation hiding via `RoleSidebarSetting` database schema
- ✅ Created `sidebar-management.html` giving Adms/Owners power to toggle tab visibility per user role
- ✅ Added `hidden_sidebar_tabs` payload to `/me/permissions` endpoint in `auth.py`
- ✅ Upgraded `menu.js` to automatically parse and hide dynamically disabled sidebar links for the active user
- ✅ **Frontend UI Rewrite**: Completely modernized the landing page (`index.html`) using a stunning glassmorphism design with `landing.css`. Added fade-in scroll animations via Javascript IntersectionObserver, CSS floating background orbs, fluid gradients, and integrated the modern `Outfit` Google Font.
- ✅ **About Us Overhaul**: Fully redesigned `about.html` using the core Indigo/Pink theme, featuring a high-impact CEO spotlight and modern company history layout for **BuxTek Inc.**
- ✅ Implemented Firebase Google Sign-In with robust backend validation (`verify_id_token`)
- ✅ Fixed `Token used too early` Firebase errors by adding `clock_skew_seconds=60` tolerance
- ✅ Added `DashboardSettings` & `DashboardModule` models to eliminate 500 errors on dashboard visits
- ✅ Designed automatic `UserProfile` creation fallback logic in `crud.py` to prevent 404s
- ✅ Fixed login.js ES Module rendering issues to restore demo account functionalities
- ✅ Added 6-digit OTP password reset with method selection UI
- ✅ Added styled OTP email template with gradient design
- ✅ Added 3-step forgot-password flow (email → method choice → reset)
- ✅ Added `POST /api/auth/verify-otp` endpoint
- ✅ Added `reset_method` parameter to forgot-password API
- ✅ Fixed superadmin global data visibility in orders and reservations
- ✅ Added `delayed` and `cancelled` order/queue statuses
- ✅ Created database seeding script (`fill_db_with_data.py`)
- ✅ Created AI coding assistant workflow instructions (`.agents/workflows/instructions.md`)
- ✅ Gmail SMTP password reset emails working end-to-end
- ✅ Database migration for `otp_code` column

### Version 2.0.0 (November 23, 2025)
- ✅ Added dynamic dashboard customization with 8 colors
- ✅ Added interactive dashboard editor with drag-and-drop
- ✅ Added 17 predefined module templates
- ✅ Added floating edit button for superadmin
- ✅ Added card text color customization
- ✅ Improved dashboard module rendering
- ✅ Fixed module persistence issues
- ✅ Updated database schema for dashboard settings

### Version 1.5.0 (November 2025)
- ✅ Added permissions management system
- ✅ Added 8 granular permissions
- ✅ Added superadmin role
- ✅ Added demo accounts with usage limits
- ✅ Added view_locations and view_invoices permissions

### Version 1.0.0 (November 2025)
- ✅ Added e-commerce features
- ✅ Added shopping cart system
- ✅ Added order management
- ✅ Added service reservations with queue
- ✅ Added client dashboard
- ✅ Added queue management for owner/admin

---

## Support & Troubleshooting

### Common Issues

#### Dashboard not loading custom modules
```bash
# Check if tables exist
python create_dashboard_customization.py

# Restart server
start_server.bat
```

#### Permissions not working
```bash
# Initialize permissions
python add_permissions.py

# Restart server
start_server.bat
```

#### Demo accounts not working
```bash
# Create demo accounts
python create_demo_users.py

# Restart server
start_server.bat
```

### Contact
For issues or questions:
1. Check server logs
2. Check browser console (F12)
3. Review API documentation at `/docs`
4. Verify database connection

---

## Future Enhancements

### Planned Features
- [ ] Real-time WebSocket updates for queue
- [ ] Email notifications for orders
- [ ] Payment gateway integration
- [ ] Customer profiles with saved vehicles
- [ ] Rating/review system
- [ ] Loyalty points system
- [ ] SMS notifications
- [ ] Two-factor authentication
- [ ] Audit log for permission changes
- [ ] Role templates
- [ ] Bulk permission updates

---

**End of System Updates, Data & History Logs**

---

## Latest Updates (April 5, 2026 — Session 3)

> **Version:** 5.0.0 | **Branch:** main

---

### 🎨 UI: Sidebar Icons, Profile Dropdown & Filter Centering
**Status:** ✅ Completed | **Branch:** `update/icons-profile-ui-update`

#### Changes:
- Replaced all colorful emoji sidebar icons with clean white Unicode symbols (■ ▣ ☐ ⧗ ▢ ⚙ ▤ ⎋)
- Added profile dropdown to all sidebar pages (dashboard, invoices, products, services, reports, order-management, queue-management)
- Created reusable `frontend/js/profile.js` with `toggleProfileMenu()`, `showEditProfile()`, `closeEditProfile()`, `loadProfileData()`
- Default white user icon SVG used when no profile photo exists
- Centered filter buttons row and empty state messages in `order-management.html` and `queue-management.html`
- Enhanced location dropdown styling with hover/focus effects in both order and queue management pages
- Fixed corrupted HTML in queue-management.html empty state message

#### Files Modified:
- ✅ `frontend/js/profile.js` — NEW reusable profile dropdown script
- ✅ `frontend/css/style.css` — Sidebar icon flexbox, profile dropdown styles
- ✅ `frontend/dashboard.html`, `invoices.html`, `products.html`, `services.html`, `reports.html`, `order-management.html`, `queue-management.html` — Profile dropdown added
- ✅ `frontend/settings.html`, `edit-dashboard.html`, `permissions-management.html` — Queue menu item added

---

### 🔲 Sidebar: Collapsible Close/Open Button
**Status:** ✅ Completed | **Branch:** `update/sidebar-navigation-button-update`

#### Changes:
- Added `✕` close button injected dynamically into sidebar via `menu.js` (no HTML changes needed)
- Desktop: clicking `✕` collapses sidebar to `width: 0`, content expands to fill space
- Mobile: clicking `✕` closes the slide-in sidebar overlay
- `☰` hamburger button restores sidebar when clicked
- Sidebar collapsed state persisted in `localStorage` — survives page navigation across all HTML files
- Added `padding-left: 60px` to content when sidebar is collapsed to prevent `☰` button overlapping title text
- Fixed broken `updateSidebarLogo` function brace structure that caused entire sidebar to disappear

#### Files Modified:
- ✅ `frontend/js/menu.js` — `closeSidebar()`, `toggleMenu()`, `DOMContentLoaded` injection, localStorage persistence
- ✅ `frontend/css/style.css` — `.sidebar-close`, `.sidebar.collapsed`, `.content.sidebar-collapsed` styles

---

### 🚀 Production Deployment: Vercel + Render
**Status:** ✅ Completed

#### Changes:
- Fixed all hardcoded `http://localhost:8000` URLs across 6 frontend files — replaced with `${API_BASE}`
- Fixed `client-dashboard.html` calling localhost causing redirect to login on Vercel
- Added `FRONTEND_URL` env var support in `email_service.py` (defaults to Vercel URL)
- Restored Render PostgreSQL database from local Docker dump using ordered SQL restore
- Fixed Firebase credentials on Render by loading from `FIREBASE_CREDENTIALS_JSON` env var instead of file
- Fixed private key newline escaping when parsing Firebase credentials from env var
- Removed `app/firebase-credentials.json` from git tracking, added to `.gitignore`
- Added `.dump` and `.sql` to `.gitignore`
- Fixed `SECRET_KEY` mismatch between local and Render causing 401 on dashboard load

#### Files Modified:
- ✅ `frontend/client-dashboard.html` — Fixed localhost URL
- ✅ `frontend/order-management.html` — 3 localhost URLs fixed
- ✅ `frontend/queue-management.html` — 3 localhost URLs fixed
- ✅ `frontend/cart.html` — 5 localhost URLs fixed
- ✅ `frontend/shop.html` — 3 localhost URLs fixed
- ✅ `frontend/reserve.html` — 3 localhost URLs fixed
- ✅ `app/firebase_auth.py` — Load credentials from env var, handle escaped newlines
- ✅ `.gitignore` — Added `.dump`, `.sql`, `firebase-credentials.json`, log files

---

### 🏢 Business Code / Join Business System
**Status:** ✅ Completed

#### Features:
- Owner/admin sees their **Business Code** (from `business_number` field) in Settings → User Management section with a **📋 Copy Code** button
- Client can enter the business code in their dashboard to **join a business** — links their account to the owner
- Business code for `owner@carwash.com` set to `CARWASH001` in both local and Render databases
- Code box only shown to superadmin/admin/owner roles

#### API Endpoints Added:
- `GET /api/settings/business-code` — Returns current user's business code
- `POST /api/settings/join-business` — Links client account to a business by code

#### Files Modified:
- ✅ `app/routers/settings.py` — Added `JoinBusinessRequest` Pydantic model, `get_business_code()`, `join_business()` endpoints
- ✅ `frontend/settings.html` — Business code display box with copy button in User Management section
- ✅ `frontend/client-dashboard.html` — Join Business section with current business status display

---

### 🔒 Sidebar: Permissions Icon + Logo Hide Fix
**Status:** ✅ Completed

#### Changes:
- Added `permissions` key to `normalizeSidebarIcons()` icon map with a lock SVG icon
- Added `permissions` text detection in icon key matching
- Fixed `updateSidebarLogo()` — now hides logo and sidebar name when no business info exists (instead of showing default car SVG)
- Fixed broken brace structure in `updateSidebarLogo` that caused entire sidebar to disappear after icon update

#### Files Modified:
- ✅ `frontend/js/menu.js` — Permissions icon added, logo hide logic fixed, brace structure corrected

---

### 📧 Email Notifications: Orders & Reservations
**Status:** ✅ Completed

#### Features:
- **Client receives emails for:**
  - Order placed — items list, total, payment method
  - Order status changed — accepted, processing, completed, cancelled, delayed
  - Reservation created — service, location, vehicle plate, queue position
  - Reservation status changed — accepted, in_progress, completed, cancelled, delayed
- **Owner receives emails for:**
  - New order placed — client email, items, total, **"View Order" button** → order-management.html
  - New reservation — client email, service, location, vehicle, queue position, **"View Queue" button** → queue-management.html
- All emails sent in **background threads** (non-blocking)
- Reusable `_base_template()`, `_action_button()`, `_items_table()` helpers for consistent HTML email design
- Owner email resolved via `business_number` matching

#### New Email Functions in `email_service.py`:
- `send_order_confirmation_client()`
- `send_order_notification_owner()`
- `send_order_status_update()`
- `send_reservation_confirmation_client()`
- `send_reservation_notification_owner()`
- `send_reservation_status_update()`

#### Files Modified:
- ✅ `app/email_service.py` — 6 new email functions + base template helpers
- ✅ `app/routers/orders.py` — Email on order create + status update; `_get_owner_email()` helper
- ✅ `app/routers/reservations.py` — Email on reservation create + status update; `_get_owner_email()` helper

---

### 📝 Git Branch Management
**Status:** ✅ Completed

#### Branches Created & Pushed:
- `update/icons-profile-ui-update` — Sidebar icons, profile dropdown, filter centering
- `update/sidebar-navigation-button-update` — Sidebar close/open button
- `update/gmail-smtp-password-reset-dbfill-update` — Email/SMTP and DB fill updates
- `update/email-ui-forget-pass-update` — Email UI and forgot password flow
- Created `GIT_BRANCH_GUIDE.md` — Local reference guide for creating, naming, and pushing branches

---

## Change Log

### Version 5.0.0 (April 5, 2026)
- ✅ Sidebar icons replaced with SVG set; permissions icon added (lock SVG)
- ✅ Profile dropdown added to all sidebar pages via reusable `profile.js`
- ✅ Sidebar collapsible with localStorage persistence across all pages
- ✅ Fixed sidebar disappearing due to broken brace in `updateSidebarLogo`
- ✅ Logo/name hidden in sidebar when no business info exists
- ✅ All hardcoded `localhost:8000` URLs replaced with `API_BASE` across 6 frontend files
- ✅ Firebase credentials loaded from Render env var (`FIREBASE_CREDENTIALS_JSON`)
- ✅ Business code system: owner shares code, clients/staff join via code
- ✅ Email notifications for all order/reservation events (client + owner)
- ✅ Owner email includes action button linking to order/queue management page
- ✅ Production deployment working on Vercel (frontend) + Render (backend + PostgreSQL)

---

## Latest Updates (April 5, 2026 — Session 4)

> **Version:** 6.0.0 | **Branch:** `feature/stripe-payment-integration` → merged to `main`

---

### 💳 Stripe Payment Integration
**Status:** ✅ Completed

#### Features:
- New `app/routers/payments.py` with 4 endpoints:
  - `GET /api/payments/config` — returns Stripe publishable key to frontend
  - `POST /api/payments/create-payment-intent` — creates PaymentIntent from cart total
  - `POST /api/payments/create-checkout-session` — creates Stripe Checkout Session
  - `POST /api/payments/webhook` — handles `checkout.session.completed` and `payment_intent.succeeded` to auto-create order
- New `frontend/checkout.html` — full Stripe Elements checkout page with:
  - Separate card number, expiry, CVC fields (individual Stripe Elements iframes)
  - Name on Card + ZIP regular inputs
  - Test Mode panel always visible with **📋 Copy** buttons for each test card field
  - **⚡ Fill Name & ZIP** button auto-fills those fields
  - Error handling with visible error banner if Stripe keys not configured
  - On success → creates order via `/api/orders/` then redirects to client dashboard
- `frontend/cart.html` — added **"💳 Pay with Card (Stripe)"** button alongside existing cash/QR checkout
- `requirements.txt` — added `stripe`
- `docker-compose.yml` — added `STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` env vars
- `.env.example` — added Stripe env var documentation
- Demo accounts show test card panel: `4242 4242 4242 4242` | `12/29` | `123` | `12345`

#### Files Created/Modified:
- ✅ `app/routers/payments.py` — NEW Stripe router
- ✅ `app/main.py` — registered payments router, added `Request` import, added `/api/contact-sales` endpoint
- ✅ `frontend/checkout.html` — NEW Stripe checkout page
- ✅ `frontend/cart.html` — Stripe pay button + dashboard back button
- ✅ `requirements.txt` — added `stripe`
- ✅ `docker-compose.yml` — Stripe env vars added
- ✅ `.env.example` — Stripe keys documented

---

### 📦 Client Orders Page & Sidebar
**Status:** ✅ Completed

#### Features:
- New `frontend/client-orders.html` — dedicated orders page for clients with:
  - Filter buttons: All, Pending, Accepted, Processing, Completed, Cancelled
  - Order cards showing number, date, status badge, total, payment method, itemized list
  - Auto-refreshes every 30 seconds
- Added **My Orders** tab to `CLIENT_TABS` in `menu.js`
- Added dedicated SVG icons for all client sidebar tabs:
  - Dashboard — grid squares
  - My Orders — clipboard with lines
  - Shop — shopping bag
  - Cart — shopping cart
  - Reserve — calendar
  - Logout — exit door

#### Files Modified:
- ✅ `frontend/client-orders.html` — NEW client orders page
- ✅ `frontend/js/menu.js` — My Orders tab added, shop/cart/reserve/myorders icons added

---

### 📧 Demo Notification Email & Settings
**Status:** ✅ Completed

#### Features:
- Default fallback notification email: `baxterdavid.mojica@gmail.com`
- Configurable via `DEMO_NOTIFICATION_EMAIL` env var
- Owner/superadmin can edit it in **Settings → Notification Email** section
- All orders/reservations from unlinked accounts now always send owner alerts to fallback email
- `POST /api/settings/notification-email` endpoint saves it

#### Files Modified:
- ✅ `app/email_service.py` — added `DEMO_NOTIFICATION_EMAIL` constant
- ✅ `app/routers/orders.py` — fallback to `DEMO_NOTIFICATION_EMAIL`
- ✅ `app/routers/reservations.py` — fallback to `DEMO_NOTIFICATION_EMAIL`
- ✅ `app/routers/settings.py` — added `notification-email` endpoint
- ✅ `frontend/settings.html` — Notification Email section (owner/superadmin only)

---

### 🌐 Landing Page Updates
**Status:** ✅ Completed

#### Features:
- One-Time Payment card: price hidden, replaced with **"Contact Sales"** text and **"Get a Quote"** button
- Contact Sales modal with fields: Full Name, Email, Business Name, Phone, Message
- On submit → `POST /api/contact-sales` → sends styled HTML email to `baxterdavid.mojica@gmail.com`
- Email includes all form fields with reply-to hint
- Success message shown, modal auto-closes after 2.5 seconds
- Clipboard fallback for browsers blocking `navigator.clipboard`
- Updated pricing: Lite ₱990/mo, Plus ₱1,990/mo, Pro ₱2,990/mo
- Fixed `/month` overflow on Pro card by reducing price font size to 48px and using flexbox

#### Files Modified:
- ✅ `frontend/index.html` — Contact Sales modal, pricing updates
- ✅ `frontend/css/landing.css` — price flexbox fix
- ✅ `app/main.py` — `/api/contact-sales` endpoint

---

## Change Log

### Version 6.0.0 (April 5, 2026)
- ✅ Stripe payment integration with test card support
- ✅ Client orders page with filter buttons and status tracking
- ✅ My Orders tab added to client sidebar with dedicated icon
- ✅ All client sidebar tabs now have distinct SVG icons
- ✅ Demo notification email fallback (`baxterdavid.mojica@gmail.com`)
- ✅ Owner can edit notification email in Settings
- ✅ Landing page: One-Time Payment shows "Contact Sales" instead of price
- ✅ Contact Sales modal sends email inquiry to owner
- ✅ Pricing updated: Lite ₱990, Plus ₱1,990, Pro ₱2,990
- ✅ Cart page: added Dashboard back button
- ✅ Fixed `/month` text overflow on Pro pricing card

---

## Latest Updates (April 5, 2026 — Session 5)

> **Version:** 6.1.0 | **Branch:** `main`

---

### 🧹 Repository Cleanup
**Status:** ✅ Completed

#### Removed unnecessary root-level files:
- `change_db_password.sql` — one-time SQL script no longer needed
- `create_db.py` — replaced by Docker + `commands/` folder
- `force_delete_user.py` — debug/utility script
- `setup_database.py` — replaced by Docker + `commands/` folder
- `start_server.bat` — replaced by `docker-compose up`
- `start_server_local.bat` — replaced by `docker-compose up`
- `temp.json` — leftover temporary file

#### Kept (still useful):
- `setup.ps1` / `start.ps1` — Windows dev environment automation
- `render.yaml` — Render deployment blueprint
- `vercel.json` — Vercel deployment config
- `docker-compose.yml` — local Docker setup
- `Dockerfile` — container build

---

### 📄 README Update
**Status:** ✅ Completed

#### Changes:
- Added **Stripe** badge to header
- Added Stripe to deployment table and tech stack table
- Added **Stripe Payments** and **Client Orders Page** feature sections
- Added **Payments API endpoints** table (`/config`, `/create-payment-intent`, `/create-checkout-session`, `/webhook`, `/contact-sales`)
- Added `/checkout.html` and `/client-orders.html` to Pages section
- Added `STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` to environment variables
- Updated Next Implementations — Stripe section shows ✅ done vs ⏳ pending

---

## Change Log

### Version 6.1.0 (April 5, 2026)
- ✅ Removed 7 unused root-level files for cleaner repository
- ✅ README updated with Stripe badge, payments section, new API endpoints, pricing

---

## Latest Updates (April 5, 2026 — Session 6)

> **Version:** 6.2.0 | **Branch:** `main`

---

### 📧 Email Service Overhaul — Gmail SMTP → Resend API
**Status:** ✅ Completed | **Pushed to production**

#### Changes:
- Replaced Gmail SMTP (`smtplib`) with **Resend API** (`resend` Python SDK)
- Removed `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD` env vars
- Added `RESEND_API_KEY` env var
- Added `CC_EMAIL` env var (defaults to `baxterdavid.mojica@gmail.com`) — all emails CC this address
- `FROM_EMAIL` defaults to `onboarding@resend.dev` (Resend's shared domain until custom domain verified)
- CC is automatically skipped when using `onboarding@resend.dev` (Resend restriction on shared domain)
- `requirements.txt` updated — replaced loose package names with pinned versions, added `resend==2.27.0`
- `docker-compose.yml` updated — removed SMTP vars, added `RESEND_API_KEY`
- `frontend/forgot-password.html` — updated for new email flow
- `app/routers/auth.py` — updated email sending calls

#### New Environment Variables:
| Variable | Description |
|----------|-------------|
| `RESEND_API_KEY` | Resend API key from resend.com dashboard |
| `FROM_EMAIL` | Sender email (use `onboarding@resend.dev` until domain verified) |
| `CC_EMAIL` | CC recipient for all emails (default: `baxterdavid.mojica@gmail.com`) |
| `DEMO_NOTIFICATION_EMAIL` | Fallback owner email for demo accounts |

#### Files Modified:
- ✅ `app/email_service.py` — full rewrite using Resend SDK
- ✅ `app/routers/auth.py` — updated email calls
- ✅ `docker-compose.yml` — SMTP vars removed, RESEND_API_KEY added
- ✅ `frontend/forgot-password.html` — updated for Resend flow
- ✅ `requirements.txt` — pinned versions, added `resend==2.27.0`

---

## Change Log

### Version 6.2.0 (April 5, 2026)
- ✅ Email service migrated from Gmail SMTP to Resend API
- ✅ All transactional emails (orders, reservations, password reset, OTP, contact sales) now use Resend
- ✅ CC_EMAIL added — all emails CC `baxterdavid.mojica@gmail.com` by default
- ✅ requirements.txt pinned to exact versions for reproducible builds

### Version 6.3.0 (April 12, 2026)
- ?? Refactored Sidebar Tab Management from Role-Based (RoleSidebarSetting) to User-Based (UserSidebarSetting).
- ??? Owners can now manage tab visibility specifically mapped to user accounts (user_id) rather than wide Net Roles, allowing individual client customization.
- ?? Added all Client-specific tabs (Shop, Cart, Reserve, My Orders) to the Sidebar Management view.
- ?? Replaced /auth/roles/*/sidebar endpoints to /auth/users/*/sidebar APIs.

---

## Latest Updates (April 13, 2026 — Session 7)

> **Version:** 6.3.0 (Public: V2.3) | **Branch:** `feature/user-sidebar-visibility-refactor`

---

### 🔀 Sidebar Visibility Refactor — Role-Based → User-Based
**Status:** ✅ Completed | **Verified working in production**

#### Problem Solved:
- Sidebar tab visibility was tied to **Roles** (`RoleSidebarSetting`) — hiding a tab for the "Client" role affected ALL clients universally, making individual customization impossible.
- Client-specific tabs (`Shop`, `Cart`, `Reserve`, `My Orders`) were missing from `sidebar-management.html` so admins couldn't toggle them at all.
- Tab name mismatches (e.g. "Orders" vs "My Orders") caused toggles to silently fail.

#### Changes Made:

**Database (`app/database.py`):**
- Removed `RoleSidebarSetting` model
- Added new `UserSidebarSetting` model — links to `users.id` via `user_id` FK instead of `role_id`
- New table: `user_sidebar_settings`

**Backend (`app/routers/auth.py`):**
- `GET /me/permissions` — fetches `hidden_sidebar_tabs` from `UserSidebarSetting` by `current_user.id`
- `GET /users/{user_id}/sidebar` — replaced role-based lookup with user-based lookup
- `PUT /users/{user_id}/sidebar` — stores visibility booleans mapped to `user_id`
- Removed all `/auth/roles/{role_id}/sidebar` endpoints

**Frontend (`frontend/sidebar-management.html`):**
- Refactored `loadRoles()` → `loadUsers()` — lists individual user accounts (email + role) instead of generic role cards
- Expanded `ALL_TABS` to include `My Orders`, `Shop`, `Cart`, `Reserve`
- Updated `toggleTabVisibility` to send `user_id` instead of `role_id`

**Other frontend files (35 pages):**
- Updated all pages referencing old role-sidebar API to use new user-sidebar endpoints
- `profile.js` updated to reflect new permission fetch logic

#### API Changes:
| Old Endpoint | New Endpoint |
|---|---|
| `GET /auth/roles/{role_id}/sidebar` | `GET /auth/users/{user_id}/sidebar` |
| `PUT /auth/roles/{role_id}/sidebar` | `PUT /auth/users/{user_id}/sidebar` |

#### Files Modified:
- ✅ `app/database.py` — `UserSidebarSetting` replaces `RoleSidebarSetting`
- ✅ `app/routers/auth.py` — user-based sidebar endpoints
- ✅ `app/schemas.py` — updated sidebar schemas
- ✅ `app/routers/settings.py` — updated references
- ✅ `frontend/sidebar-management.html` — user-centric UI, client tabs added
- ✅ `frontend/js/profile.js` — updated permission fetch
- ✅ 35 frontend HTML files — updated to new sidebar API

---

## Change Log

### Version 6.3.0 / V2.3 (April 13, 2026)
- ✅ Sidebar visibility refactored from role-based to user-based (`UserSidebarSetting`)
- ✅ Admins can now manage sidebar tabs per individual user account
- ✅ Client tabs (Shop, Cart, Reserve, My Orders) added to Sidebar Management UI
- ✅ Fixed tab name mismatches that caused silent toggle failures
- ✅ Removed `/auth/roles/{role_id}/sidebar` endpoints, replaced with `/auth/users/{user_id}/sidebar`
- ✅ README updated to V2.3

---

## ✅ Completed in Session 8 (April 2026)

> **Version:** 6.4.0 (Public: V2.4) | **Branch:** `main`

---

### 🔐 Feature 1: Staff Product/Service Permissions Fix
**Status:** ✅ Completed

#### Problem Solved:
Staff (`user` role) had `manage_products` permission allowing them to add, edit, and delete products/services. The frontend was not respecting this — Edit/Delete buttons were always visible because `hideElementsWithoutPermission()` ran on `DOMContentLoaded` before cards were dynamically rendered.

#### Changes Made:
- **`frontend/js/products.js`** — Added `permissionManager.hideElementsWithoutPermission()` call after `grid.innerHTML` is set in `loadProducts()` so dynamically injected Edit/Delete buttons are hidden for staff
- **`frontend/js/services.js`** — Same fix after `grid.innerHTML` in `loadServices()`
- **`commands/users/setup_demo_accounts.py`** — Explicitly sets `user` (staff) role permissions to `[view_locations, manage_invoices, view_invoices, view_reports]`, ensuring `manage_products` is never inherited
- **`commands/database/seed_data.py`** — Already correct (staff only had `add_invoice` + `view_reports`), no change needed

#### Result:
| Button | Superadmin | Admin | Staff | Client |
|--------|-----------|-------|-------|--------|
| + Add Product/Service | ✅ | ✅ | ❌ hidden | ❌ hidden |
| Edit (per card) | ✅ | ✅ | ❌ hidden | ❌ hidden |
| Delete (per card) | ✅ | ✅ | ❌ hidden | ❌ hidden |

---

### 👥 User Management Submodules in Sidebar
**Status:** ✅ Completed

#### Changes:
- **`frontend/js/menu.js`** — Replaced standalone "Permissions" and "Sidebar Tabs" sidebar links with a collapsible "User Management" nav group containing both as sub-items
  - Clicking the parent toggles `.open` class → slides sub-items in/out via CSS `max-height` transition
  - Auto-opens if current page is `permissions-management.html` or `sidebar-management.html`
  - "Permissions" sub-item only shows for `superadmin`
  - "Sidebar Tabs" sub-item shows for `superadmin`, `admin`, `owner`
- **`frontend/css/style.css`** — Added `.nav-group`, `.nav-group-header`, `.nav-group-arrow`, `.nav-sub` styles with smooth slide animation and collapsed-sidebar hiding

---

### 🔒 Owner Self-Protection in Permissions & Sidebar Management
**Status:** ✅ Completed

#### `permissions-management.html`:
- `currentUserId` stored from `meData.user_id` on load
- Owner's own card gets blue border + `(you)` label + warning message
- All permission toggles `disabled` + `opacity: 0.45` + `cursor: not-allowed`
- Delete 🗑️ button replaced with 🔒 `Owner` badge
- `togglePermission()` and `deleteUser()` both have early-return guards for self

#### `sidebar-management.html`:
- Same `currentUserId` pattern
- Owner's own card locked with disabled toggles and warning message
- `toggleTabVisibility()` has early-return guard for self

---

### 🐛 Bug Fixes
**Status:** ✅ Completed

#### Reports page — Broken emoji characters:
- Fixed mojibake in `reports.html`: `ðŸ"Š` → `📊`, `ðŸ"¦` → `📦`, `ðŸ"§` → `🔧`, `â˜°` → `☰`, `ðŸš—` → `🚗`, `â‚±` → `₱`
- Same fixes applied to `dashboard.html` filter dropdown options (`ðŸ"…` → `📅`) and floating edit button (`âœï¸` → `✏️`)
- Same fixes applied to `invoices.html` search placeholder

#### Dashboard filter dropdown:
- All 6 filter options now correctly show `📅` emoji
- `semiannually` option value restored correctly

---

### 📄 Pagination — Reports & Invoices
**Status:** ✅ Completed

#### `frontend/js/reports.js`:
- Added `reportInvoices`, `reportPage`, `REPORT_PAGE_SIZE = 10` state
- `renderReportPage()` slices 10 rows per page, renders prev/number/next buttons into `#reportPagination`
- `displayReport()` now sets state and calls `renderReportPage()`

#### `frontend/js/invoices.js`:
- Added `invoicePage`, `INVOICE_PAGE_SIZE = 10` state
- `renderInvoicePage()` handles slicing and pagination bar into `#invoicePagination`
- `displayInvoices()` delegates to `renderInvoicePage()`

#### HTML:
- `reports.html` — added `<div id="reportPagination" class="pagination-bar">` after report table
- `invoices.html` — added `<div id="invoicePagination" class="pagination-bar">` after invoice table, removed fixed-height scroll wrapper

#### `frontend/css/style.css`:
- Added `.pagination-bar`, `.page-btn`, `.page-btn.active`, `.page-btn:disabled` styles

---

### 🎨 Page Load Float-Fade Animation
**Status:** ✅ Completed

- Added `@keyframes fadeSlideIn` (opacity 0→1 + translateY 18px→0) to `style.css`
- Applied to: `.stat-card`, `.chart-card`, `.settings-section`, `.table-container`, `.product-card`, `.bay-card`, `.user-card`, `.role-card`, `.permissions-grid > div`, `.roles-grid > div`, `header`
- Staggered delays per nth-child for cascading entrance effect
- `stat-card` and `header` use opacity-only `fadeInOnly` animation (no transform) to prevent stacking context from breaking profile dropdown z-index

---

### 🔧 Settings — No Logo Fix
**Status:** ✅ Completed

- **`frontend/js/settings.js`** — `selectPredefinedLogo()` now clears `innerHTML` AND resets the file input value when "No Logo" is selected
- `businessForm` submit sends `logo: null` when `logoType === 'none'` instead of passing the string `"null"`

---

### 📱 Mobile — Hamburger Removed, Edge Tab Added
**Status:** ✅ Completed

- `.menu-toggle { display: none !important }` — hamburger hidden on all screen sizes
- **`frontend/js/menu.js`** — injects a `sidebar-edge-tab` button on mobile (18px wide, vertically centered on left edge, matches sidebar color)
- `MutationObserver` hides the tab when sidebar is open, shows it when closed
- Click-outside handler updated to remove null reference to `.menu-toggle`
- Mobile content padding reduced from `70px` → `20px` (no hamburger taking space)

---

### 🖼️ Sidebar — Logo Area & Close Button Overlap Fix
**Status:** ✅ Completed

- Added `padding-right: 36px` to `.sidebar .logo` so business name text doesn't run under the absolute-positioned close button

---

### 👋 Sidebar — Welcome Greeting Hidden When Collapsed
**Status:** ✅ Completed

- Added `.sidebar.collapsed .welcome-section { display: none !important }` to `style.css`
- Client dashboard greeting disappears cleanly when sidebar collapses

---

### 📊 Client Dashboard — Pagination on All Tables
**Status:** ✅ Completed

- Added reusable `paginate(containerId, rows, renderRow, headers)` helper in `client-dashboard.html`
- All 4 tables paginated at 8 rows/page: `active-orders`, `order-history`, `active-reservations`, `reservation-history`
- Each table's pagination is independent via `window.__pg_<containerId>` function
- Pagination bar only renders when total pages > 1
- Added `setTimeout(() => window.dispatchEvent(new Event('resize')), 450)` on load to fix table width compression after sidebar transition

---

### 🔝 Profile Dropdown Z-Index Fix (All Pages)
**Status:** ✅ Completed

- Root cause: animated cards with `transform` create stacking contexts that override `z-index` from outside
- Fix: `header { position: relative; z-index: 200 }` makes header a stacking context above all animated cards
- `.profile-dropdown { z-index: 201 }`, `.profile-menu { z-index: 202 !important }`
- `stat-card` and `header` animations changed to `fadeInOnly` (opacity only, no transform) to prevent stacking context creation

---

## Change Log

### Version 6.4.0 / V2.4 (April 2026)
- ✅ Staff product/service permissions fixed — Edit/Delete buttons hidden after dynamic render
- ✅ User Management collapsible submodule in sidebar (Permissions + Sidebar Tabs)
- ✅ Owner self-protection in Permissions Management and Sidebar Management
- ✅ Mojibake emoji fixed in reports.html, dashboard.html, invoices.html
- ✅ Pagination added to Reports invoices table and Invoices page (10 rows/page)
- ✅ Page load float-fade animation on all cards and sections
- ✅ Settings No Logo fix — clears file input and sends null to backend
- ✅ Hamburger button removed on mobile, replaced with left-edge tap tab
- ✅ Sidebar logo area padding fix — close button no longer overlaps business name
- ✅ Sidebar welcome greeting hidden when collapsed
- ✅ Client dashboard tables paginated (8 rows/page, 4 tables)
- ✅ Profile dropdown z-index fixed on all pages — no longer hidden behind stat cards
