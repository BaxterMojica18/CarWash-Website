# 🚗 Car Wash Management System

> **Version 2.0** — Full-stack car wash management platform with e-commerce, multi-tenant support, Stripe payments, and live production deployment.

[![Frontend](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)](https://car-wash-website-khaki.vercel.app)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7?logo=render)](https://carwash-website-jzr2.onrender.com)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql)](https://render.com)
[![Auth](https://img.shields.io/badge/Auth-Firebase-FFCA28?logo=firebase)](https://firebase.google.com)
[![Email](https://img.shields.io/badge/Email-Gmail_SMTP-EA4335?logo=gmail)](https://gmail.com)
[![Payments](https://img.shields.io/badge/Payments-Stripe-635BFF?logo=stripe)](https://stripe.com)

---

## 🌐 Live Deployment

| Service | Platform | URL |
|---------|----------|-----|
| Frontend | Vercel | https://car-wash-website-khaki.vercel.app |
| Backend API | Render | https://carwash-website-jzr2.onrender.com |
| Database | Render PostgreSQL | Singapore region |
| Google Login | Firebase Auth | `carwash-mgmt-system-41402` |
| Email | Gmail SMTP | Transactional emails |
| Payments | Stripe | Test mode (card payments) |

---

## 📚 Documentation

- **[SYSTEM_UPDATES_DATA_HISTORY_LOGS.md](SYSTEM_UPDATES_DATA_HISTORY_LOGS.md)** — Full feature history and change log
- **[PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)** — Planned features and implementation phases
- **[GIT_BRANCH_GUIDE.md](GIT_BRANCH_GUIDE.md)** — Git workflow reference

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python FastAPI |
| Database | PostgreSQL (Docker locally, Render in production) |
| Frontend | HTML / CSS / JavaScript |
| Authentication | JWT + Google Firebase Auth |
| Email | Gmail SMTP |
| Payments | Stripe (card payments + webhooks) |
| Containerization | Docker + Docker Compose |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |

---

## ✨ Features — V2.0

### 🔐 Authentication
- ✅ Email/password login with JWT tokens
- ✅ Google Sign-In via Firebase Auth
- ✅ Forgot password — reset link or 6-digit OTP
- ✅ Styled HTML email templates for password reset
- ✅ Role-based access control (RBAC)

### 📊 Dashboard & Reports
- ✅ Dynamic dashboard with customizable modules
- ✅ Revenue charts (weekly, monthly, quarterly, annual)
- ✅ Sales reports with CSV and PDF export
- ✅ Drag-and-drop dashboard editor (superadmin)
- ✅ 17 predefined dashboard module templates

### 🧾 Invoicing
- ✅ Invoice creation and PDF generation
- ✅ Invoice customization (address, phone, email)
- ✅ Invoice status tracking

### 🛒 E-Commerce
- ✅ Product and service shopping cart
- ✅ Order management with status flow (pending → accepted → processing → completed)
- ✅ Service reservation with FIFO queue system
- ✅ Client dashboard (orders, reservations, history)
- ✅ Queue management for owner/admin
- ✅ Delayed and cancelled order/reservation statuses

### 💳 Stripe Payments *(New in V2)*
- ✅ Stripe Elements card payment form (separate number/expiry/CVC fields)
- ✅ PaymentIntent API integration
- ✅ Webhook auto-creates order on successful payment
- ✅ Test mode with copy buttons for test card details
- ✅ "Pay with Card" button in cart alongside cash/QR options
- ✅ Dedicated `/checkout.html` page

### 📦 Client Orders Page *(New in V2)*
- ✅ Dedicated `/client-orders.html` with filter buttons (All, Pending, Accepted, Processing, Completed, Cancelled)
- ✅ My Orders tab in client sidebar with clipboard icon
- ✅ Distinct SVG icons for all client sidebar tabs (Shop, Cart, Reserve, My Orders)
- ✅ Auto-refreshes every 30 seconds

### 📧 Email Notifications *(New in V2)*
- ✅ Client receives confirmation email when order is placed
- ✅ Client receives email on every order status change
- ✅ Client receives confirmation email when reservation is created
- ✅ Client receives email on every reservation status change
- ✅ Owner receives new order alert with **"View Order"** action button
- ✅ Owner receives new reservation alert with **"View Queue"** action button
- ✅ All emails sent asynchronously (non-blocking background threads)

### 🏢 Multi-Tenant Business System *(New in V2)*
- ✅ Business code system — owner shares code, staff/clients join via code
- ✅ Data isolation by `business_number` — each business sees only their own data
- ✅ Shared business branding (name, logo, theme) across all staff in same business
- ✅ Client-specific theme system separate from staff/admin theme
- ✅ Owner-scoped saves for all shared settings

### 👥 User & Permissions Management *(New in V2)*
- ✅ Role hierarchy: Superadmin → Admin → Staff → Client
- ✅ 8 granular permissions (products, locations, invoices, reports, settings, users)
- ✅ Visual permissions management UI with toggle switches
- ✅ Sidebar tab visibility control per role
- ✅ User management in Settings (add users, assign roles)

### 🎨 UI & Navigation *(New in V2)*
- ✅ Collapsible sidebar with localStorage persistence across all pages
- ✅ SVG icon set for all sidebar navigation items
- ✅ Profile dropdown with photo, name, role on all pages
- ✅ Sidebar logo/name hidden when no business info set
- ✅ Centered filter buttons and empty states in order/queue management
- ✅ No-cache middleware for HTML/CSS/JS files
- ✅ Theme customization with 10 presets + custom color picker

### ⚙️ Settings
- ✅ Business information (name, logo, address, phone)
- ✅ Payment methods with QR code upload and account number
- ✅ Invoice customization
- ✅ Theme presets (staff and client-facing)
- ✅ Washing bay management
- ✅ SMS opt-in preferences

---

## 🔒 Security

### Current Implementation
- JWT tokens with configurable expiry
- Password hashing with bcrypt
- Firebase token verification for Google login
- Environment variables for all secrets
- CORS configured for allowed origins only
- No-cache headers on frontend assets
- `.env` and credential files excluded from version control

### Best Practices Before Production
1. Rotate `SECRET_KEY` to a strong random value
2. Change all default passwords in the database
3. Never commit `.env` or credential files
4. Enable HTTPS (handled by Vercel/Render automatically)
5. Use strong, unique database passwords

---

## 🚀 Setup Instructions

### Option 1: Docker (Recommended for Local Dev)

```bash
git clone https://github.com/BaxterMojica18/CarWash-Website.git
cd CarWash-Website

# Start all services
docker-compose up -d

# Create superadmin account
docker-compose exec web python commands/users/create_superadmin.py

# Access at http://localhost:8000
```

### Option 2: Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Create database tables
python commands/database/seed_data.py

# Create superadmin
python commands/users/create_superadmin.py

# Start server
uvicorn app.main:app --reload --port 8000
```

---

## 🔑 Login Credentials

> ⚠️ **Development only.** Change all passwords before production deployment.

| Role | Email | Password |
|------|-------|----------|
| Superadmin/Owner | `owner@carwash.com` | `owner123` |
| Admin | `admin@carwash.com` | `admin123` |
| Staff | `staff@carwash.com` | `staff123` |
| Client | `client@carwash.com` | `client123` |
| Demo Client | `demo-client@carwash.com` | `demo123` |
| Demo Staff | `demo-staff@carwash.com` | `demo123` |

> Run `docker-compose exec web python commands/users/create_superadmin.py` to create the owner account.

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Email/password login |
| POST | `/api/auth/firebase-login` | Google Firebase login |
| POST | `/api/auth/register` | Register new account |
| POST | `/api/auth/forgot-password` | Request password reset |
| POST | `/api/auth/verify-otp` | Verify 6-digit OTP |
| POST | `/api/auth/reset-password` | Reset password with token |
| GET | `/api/auth/me/permissions` | Get current user permissions |

### Settings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/settings/business` | Business info |
| GET/POST | `/api/settings/profile` | User profile |
| GET/POST | `/api/settings/theme` | Theme management |
| GET | `/api/settings/business-code` | Get business join code |
| POST | `/api/settings/join-business` | Join a business by code |
| GET/POST/PUT/DELETE | `/api/settings/locations` | Washing bays |
| GET/POST/PUT/DELETE | `/api/settings/products` | Products & services |
| GET/POST/PUT/DELETE | `/api/settings/payment-methods` | Payment methods |

### Orders & Reservations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orders/` | Create order from cart |
| GET | `/api/orders/` | List orders |
| PATCH | `/api/orders/{id}/status` | Update order status |
| POST | `/api/reservations/` | Create reservation |
| GET | `/api/reservations/` | List reservations |
| PATCH | `/api/reservations/{id}/status` | Update reservation status |

### Payments
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/payments/config` | Get Stripe publishable key |
| POST | `/api/payments/create-payment-intent` | Create PaymentIntent from cart |
| POST | `/api/payments/create-checkout-session` | Create Stripe Checkout Session |
| POST | `/api/payments/webhook` | Stripe webhook handler |
| POST | `/api/contact-sales` | Send sales inquiry email |

### Other
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST/PATCH/DELETE | `/api/cart` | Shopping cart |
| GET | `/api/invoices/` | Invoices |
| GET | `/api/reports/sales` | Sales reports |
| GET | `/api/health` | Health check |

> **API Docs:** https://carwash-website-jzr2.onrender.com/docs

---

## 📄 Pages

### Client Pages
- `/shop.html` — Browse products and services
- `/cart.html` — Shopping cart and checkout (cash/QR or Stripe card)
- `/checkout.html` — Stripe card payment page
- `/reserve.html` — Reserve car wash service
- `/client-dashboard.html` — Orders, reservations, join business
- `/client-orders.html` — View all orders with status tracking

### Owner/Admin Pages
- `/dashboard.html` — Stats and revenue charts
- `/invoices.html` — Invoice management
- `/order-management.html` — Manage customer orders
- `/queue-management.html` — Manage service queue
- `/products.html` / `/services.html` — Product/service management
- `/reports.html` — Sales reports
- `/settings.html` — All settings including business code
- `/permissions-management.html` — User permissions (superadmin)

---

## 🗺️ Next Implementations

### 💳 Stripe Payment Integration
- ✅ Online card payment processing via Stripe Elements
- ✅ PaymentIntent + webhook integration
- ✅ Test mode with demo card details
- ⏳ Live mode activation (add live Stripe keys when ready)
- ⏳ Payment history and receipts page
- ⏳ Refund processing

### ⚛️ Frontend Overhaul — React + Next.js
- Migrate from plain HTML/CSS/JS to Next.js 14 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Reusable component library
- Server-side rendering for better SEO and performance

### 🔒 Security Enhancements (Recommended)
The following security improvements are planned for the next phase:

#### Backend
- **Rate Limiting** — `slowapi` middleware to prevent brute-force and DDoS attacks on API endpoints
- **Input Validation & Sanitization** — Stricter Pydantic schemas + SQL injection prevention
- **HTTPS-only Cookies** — Move JWT from localStorage to `HttpOnly` + `Secure` cookies to prevent XSS token theft
- **Refresh Token Rotation** — Short-lived access tokens (15 min) + long-lived refresh tokens stored in HttpOnly cookies
- **API Key Management** — Per-client API keys for third-party integrations
- **Audit Logging** — Log all sensitive actions (login, permission changes, data deletions) to a dedicated table
- **CORS Hardening** — Restrict allowed origins to exact production domains only

#### Frontend
- **Content Security Policy (CSP)** — HTTP headers to prevent XSS attacks
- **Subresource Integrity (SRI)** — Hash verification for CDN-loaded scripts (Chart.js, Firebase SDK)
- **HTTPS Enforcement** — Redirect all HTTP to HTTPS (handled by Vercel/Render)
- **Sensitive Data Cleanup** — Remove tokens/permissions from localStorage, use memory or HttpOnly cookies instead

#### Infrastructure
- **Secrets Scanning** — GitHub secret scanning already enabled; add pre-commit hooks with `detect-secrets`
- **Dependency Auditing** — Regular `pip audit` and `npm audit` checks in CI/CD
- **Database Backups** — Automated daily backups on Render with point-in-time recovery
- **Environment Separation** — Separate `.env` configs for dev, staging, and production

### 🔔 Real-time Features
- WebSocket integration for live queue updates
- Browser push notifications for order status changes

### 📱 Mobile PWA
- Progressive Web App support
- Offline capability with service workers
- Mobile-optimized UI

---

## 📝 Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/carwash_db

# Authentication
SECRET_KEY=your-strong-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (Gmail SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# Firebase (Render only — paste full JSON as single line)
FIREBASE_CREDENTIALS_JSON={"type":"service_account",...}

# Stripe Payments
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Frontend URL (for email action buttons)
FRONTEND_URL=https://car-wash-website-khaki.vercel.app
```

---

## 📊 Database Schema (Key Tables)

| Table | Description |
|-------|-------------|
| `users` | User accounts with roles, business_number, account_type |
| `roles` / `permissions` | RBAC system |
| `locations` | Washing bays |
| `products_services` | Products and services |
| `invoices` / `invoice_items` | Invoice management |
| `orders` / `order_items` | E-commerce orders |
| `reservations` | Service queue reservations |
| `cart_items` | Shopping cart |
| `payment_methods` | Payment options with QR codes |
| `business_info` | Business branding per owner |
| `settings_theme_selection` | Custom themes (staff + client) |
| `dashboard_settings` / `dashboard_modules` | Dashboard customization |
| `password_reset_tokens` | Password reset with OTP |
| `user_profiles` | Profile photos and display names |

---

*Built with ❤️ by BuxTek Inc.*
