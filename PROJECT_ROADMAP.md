# 🚀 Car Wash Management System - Project Roadmap

## 🎯 Priority Features (Next 2-4 weeks)

### 1. Password Reset System ✅
- [x] **Forgot Password API**
  - Password reset token generation
  - Secure token validation (expires in 15 minutes)
  - Password update endpoint
- [x] **6-Digit OTP Reset** ✅ *(Added March 29, 2026)*
  - OTP generation alongside UUID token
  - `POST /api/auth/verify-otp` endpoint
  - Method selection UI (link vs OTP)
  - Styled OTP email template
  - 6-digit input with auto-advance & paste support
  - 60-second resend cooldown
- [x] **Frontend Integration**
  - 3-step forgot password flow (email → method choice → reset)
  - Reset password page with token validation
  - Success/error notifications
- [x] **Database Changes**
  - Add `password_reset_tokens` table
  - Add `otp_code` column with index
  - Token cleanup job (tokens auto-invalidated on new request)

### 2. Gmail SMTP Integration
- [x] **Email Service Setup**
  - Gmail SMTP configuration
  - Email templates (HTML + text)
  - Queue system for bulk emails
- [ ] **Email Features**
  - Welcome emails for new users
  - [x] Password reset emails
  - Order confirmation emails
  - Service completion notifications
- [x] **Environment Variables**
  ```
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USERNAME=your-email@gmail.com
  SMTP_PASSWORD=your-app-password
  ```

### 3. SMS Integration
- [ ] **SMS Provider Setup** (Twilio recommended)
  - Account setup and API keys
  - Phone number validation
  - SMS templates
- [ ] **SMS Notifications**
  - Order status updates
  - Service queue position updates
  - Appointment reminders
  - Promotional messages
- [ ] **User Preferences**
  - SMS opt-in/opt-out
  - Notification preferences dashboard

## 🔧 Technical Improvements (Next 4-6 weeks)

### 4. Enhanced Authentication
- [x] **OTP-Based Password Reset** ✅
  - Email-based 6-digit OTP verification
  - User choice between reset link and OTP
- [x] **Hybrid Firebase Authentication (Google Sign-In)** ✅ *(Added March 2026)*
  - Preserved standard local DB email/password architecture
  - Leveraged Firebase strictly as an Identity Provider for Google Sign-In
  - Configured Python Firebase Admin SDK with `clock_skew_seconds=60` tolerance for robust token verification (`verify_id_token`)
  - Automatic `get_or_create_firebase_user` mapping bridging Firebase to local PostgreSQL databases
  - Implemented lazy `UserProfile` schema generation to gracefully handle missing profiles on new or demo accounts
  - Automatic injection of default Roles (`client`)
  - Backwards-compatible fallback routes mimicking JWT issuing for both sign-in paths
- [ ] **Multi-Factor Authentication (MFA)**
  - SMS-based 2FA
  - Email-based 2FA
  - Backup codes
- [ ] **Social Login**
  - Google OAuth integration
  - Facebook login option
- [ ] **Session Management**
  - Remember me functionality
  - Device management
  - Force logout from all devices

### 5. Real-time Features
- [ ] **WebSocket Integration**
  - Real-time queue updates
  - Live order status changes
  - Admin notifications
- [ ] **Push Notifications**
  - Browser push notifications
  - Service worker implementation
  - Notification preferences

### 6. Payment Integration
- [ ] **Payment Gateway**
  - Stripe integration
  - PayPal support
  - Credit card processing
- [ ] **Payment Features**
  - Save payment methods
  - Recurring payments for subscriptions
  - Refund processing
  - Payment history

## 📱 Mobile & UX Enhancements (Next 6-8 weeks)

### 7. Progressive Web App (PWA)
- [ ] **PWA Features**
  - Service worker for offline functionality
  - App manifest for installation
  - Push notification support
- [ ] **Mobile Optimization**
  - Responsive design improvements
  - Touch-friendly interfaces
  - Mobile-specific features

### 8. Advanced Dashboard
- [ ] **Analytics Dashboard**
  - Revenue charts and trends
  - Customer analytics
  - Service performance metrics
  - Predictive analytics
- [ ] **Reporting Enhancements**
  - Custom date ranges
  - Automated report scheduling
  - Email report delivery
  - Advanced filtering options

## 🎨 Frontend Modernization (Next 8-12 weeks)

### 9. Next.js Migration
- [ ] **Framework Setup**
  - Next.js 14 with App Router
  - TypeScript integration
  - Tailwind CSS styling
- [ ] **Component Library**
  - Reusable UI components
  - Design system implementation
  - Accessibility improvements

### 10. Enhanced User Experience
- [ ] **Customer Portal**
  - Vehicle management
  - Service history
  - Loyalty program
  - Subscription management
- [ ] **Staff Portal**
  - Task management
  - Performance tracking
  - Schedule management

## 🔒 Security & Performance (Ongoing)

### 11. Security Enhancements
- [ ] **API Security**
  - Rate limiting implementation
  - API key management
  - Request validation
  - SQL injection prevention
- [x] **Data Protection — Multi-Tenant Isolation** ✅ *(Added April 4, 2026)*
  - Business-scoped data queries via `business_number`
  - Admins can't see other businesses' data
  - Staff sidebar restricted (Settings hidden)
  - Owner-scoped saves for shared branding (name, logo, themes)
  - Client-specific theme system (`for_client` flag)
- [ ] GDPR compliance
- [ ] Data encryption at rest
- [x] Audit logging *(partial — via report cache)*
- [ ] Backup automation

### 12. Performance Optimization
- [ ] **Database Optimization**
  - Query optimization
  - Database indexing
  - Connection pooling
  - Caching layer (Redis)
- [ ] **API Performance**
  - Response caching
  - Pagination improvements
  - Background job processing
  - CDN integration

## 🚀 Advanced Features (Future)

### 13. AI & Automation
- [ ] **Smart Scheduling**
  - AI-powered queue optimization
  - Predictive maintenance alerts
  - Dynamic pricing
- [ ] **Customer Insights**
  - Behavior analytics
  - Personalized recommendations
  - Churn prediction

### 14. Integration & Expansion
- [ ] **Third-party Integrations**
  - Calendar sync (Google/Outlook)
  - Accounting software integration
  - CRM system integration
- [ ] **Multi-location Support**
  - Franchise management
  - Location-specific settings
  - Centralized reporting

## 📋 Implementation Priority

### Phase 1 (Immediate - 2 weeks) ✅ COMPLETED
1. ✅ Gmail SMTP integration
2. ✅ Forgot password system (link + OTP)
3. ✅ Database seeding script
4. ✅ Superadmin role fix for global data visibility
5. ✅ Hybrid Firebase Google Sign-in configuration
6. ✅ Missing Dashboard & Profile DB fixes
7. ✅ **Advanced Registration Flow Upgrade** (Owner/Admin/Client triage)
8. ✅ **Sidebar UX Modernization** (Mini-mode, SVG icons, Click-to-Expand)
9. ✅ **DevOps Automation** (setup.ps1, auto-migrations)

### Phase 2 (Short-term - 1-2 weeks)
1. ✅ **Production Deployment**: Created `vercel.json` and `render.yaml` configs for Vercel/Render with managed Postgres. *(April 4, 2026)*
2. ✅ **Multi-Tenant Data Isolation**: All data scoped by `business_number` — admins can't see other businesses' data. *(April 4, 2026)*
3. ✅ **Staff Sidebar Permissions**: Settings hidden from staff, only visible to admin/owner/superadmin. *(April 4, 2026)*
4. ✅ **Demo Account Overhaul**: Replaced legacy demo accounts with properly scoped BuxWash (BXTK-001) + SparkleWash (WASH-002) businesses. *(April 4, 2026)*
5. ✅ **Shared Business Branding**: Owner/admin saves to business name, logo, themes now shared across all staff via owner-scoped writes. *(April 4, 2026)*
6. ✅ **Client-Specific Themes**: `for_client` flag on themes, separate client presets dropdown, auto-detect on login. *(April 4, 2026)*
7. ✅ **Production Deployment Fixes**: Fixed password reset links (localhost → Vercel), Dockerfile migration startup, dynamic CORS, business-scoped sidebar settings. *(April 7, 2026)*
8. ✅ **Email CC System**: All system emails now CC `baxterdavid.mojica@gmail.com` for audit trailing. *(April 7, 2026)*
9. ✅ **Dynamic Client Notifications**: Automatic email/SMS notifications to clients when their service status (Queue) or order (Product) is updated via Resend API HTTP Threads. *(April 13, 2026)*
10. **Dynamic Business Dashboards**: Tailor modules based on account_type (Owner vs Client).
11. Payment gateway integration
12. Real-time features (WebSockets for Queue)

### Phase 3 (Medium-term - 8 weeks)
1. PWA implementation
2. Advanced dashboard
3. Mobile optimization

### Phase 4 (Long-term - 12+ weeks)
1. Next.js migration
2. AI features
3. Multi-location support

## 🛠️ Required Dependencies

### New Python Packages
```txt
# Email & SMS
fastapi-mail==1.4.1
twilio==8.10.0
celery==5.3.4
redis==5.0.1

# Authentication
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Payment
stripe==7.8.0

# WebSocket
fastapi-websocket==0.1.7
```

### Environment Variables to Add
```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@carwash.com

# Frontend & Trailing
FRONTEND_URL=https://car-wash-website-khaki.vercel.app
CC_EMAIL=baxterdavid.mojica@gmail.com

# SMS Configuration
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Payment Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
```

## 📝 Notes

- Prioritize features based on user feedback and business needs
- Implement proper testing for each feature
- Document API changes and new endpoints
- Consider backward compatibility when making changes
- Regular security audits and dependency updates

---

## ✅ Completed in Session 3 (April 5, 2026)

### UI & Navigation
- [x] **Sidebar Icons** — Replaced emoji icons with clean white Unicode/SVG icons across all pages
- [x] **Profile Dropdown** — Added to all sidebar pages via reusable `profile.js`
- [x] **Sidebar Close/Open Button** — Collapsible sidebar with localStorage persistence across all pages
- [x] **Filter Centering** — Centered filter buttons and empty states in order/queue management
- [x] **Permissions Icon** — Added lock SVG icon to Permissions sidebar tab
- [x] **Logo Hide** — Sidebar logo/name hidden when account has no business info

### Production Deployment
- [x] **Vercel + Render Live** — Frontend on Vercel, backend + PostgreSQL on Render
- [x] **API_BASE Fix** — All hardcoded `localhost:8000` URLs replaced with dynamic `API_BASE`
- [x] **Firebase on Render** — Credentials loaded from `FIREBASE_CREDENTIALS_JSON` env var
- [x] **Database Restore** — Local Docker DB dumped and restored to Render PostgreSQL
- [x] **SECRET_KEY Sync** — Matched between local and Render to fix 401 token errors

### Business Code System
- [x] **Owner Business Code** — Displayed in Settings → User Management with copy button
- [x] **Join Business** — Client can enter code in dashboard to link their account to a business
- [x] **API Endpoints** — `GET /api/settings/business-code`, `POST /api/settings/join-business`

### Email Notifications ✅ *(Added April 5, 2026)*
- [x] **Order Confirmation** — Client receives email when order is placed
- [x] **Order Status Updates** — Client notified on every status change
- [x] **New Order Alert (Owner)** — Owner receives email with items + "View Order" button
- [x] **Reservation Confirmation** — Client receives email when reservation is created
- [x] **Reservation Status Updates** — Client notified on every status change
- [x] **New Reservation Alert (Owner)** — Owner receives email with details + "View Queue" button
- [x] **Background Threading** — All emails sent async (non-blocking)

### Documentation
- [x] **GIT_BRANCH_GUIDE.md** — Local reference for creating, naming, and pushing branches
- [x] **SYSTEM_UPDATES_DATA_HISTORY_LOGS.md** — Updated with all session 3 changes
- [x] **PROJECT_ROADMAP.md** — Updated with all completed items

---

## 🔄 Updated Phase 2 Status (April 5, 2026)

| Feature | Status |
|---------|--------|
| Production Deployment (Vercel + Render) | ✅ Done |
| Multi-Tenant Data Isolation | ✅ Done |
| Staff Sidebar Permissions | ✅ Done |
| Shared Business Branding | ✅ Done |
| Client-Specific Themes | ✅ Done |
| Business Code / Join Business | ✅ Done |
| Email Notifications (Orders + Reservations) | ✅ Done |
| Real-time WebSockets for Queue | ⬜ Pending |
| Payment Gateway Integration | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |


---

## ✅ Completed in Session 4 (April 5, 2026)

### 💳 Stripe Payments
- [x] Stripe PaymentIntent integration with card Elements
- [x] Separate card number / expiry / CVC fields
- [x] Test card panel with copy buttons on checkout page
- [x] Webhook auto-creates order on payment success
- [x] Demo accounts show test card details
- [x] Cart page has "Pay with Card (Stripe)" button

### 📦 Client Orders
- [x] Dedicated `/client-orders.html` page with filter buttons
- [x] My Orders tab in client sidebar
- [x] Distinct SVG icons for all client sidebar tabs (Shop, Cart, Reserve, My Orders)

### 📧 Notifications
- [x] Demo notification email fallback — `baxterdavid.mojica@gmail.com`
- [x] Owner can edit notification email in Settings
- [x] All unlinked accounts send alerts to fallback email

### 🌐 Landing Page
- [x] One-Time Payment: price hidden, "Contact Sales" + "Get a Quote" button
- [x] Contact Sales modal with email inquiry form
- [x] Pricing updated: Lite ₱990, Plus ₱1,990, Pro ₱2,990
- [x] Fixed `/month` overflow on Pro card

---

## 🔄 Updated Phase 2 Status (April 5, 2026 — Session 4)

| Feature | Status |
|---------|--------|
| Stripe Payment Integration | ✅ Done |
| Client Orders Page | ✅ Done |
| Client Sidebar Icons | ✅ Done |
| Demo Notification Email | ✅ Done |
| Contact Sales Modal | ✅ Done |
| Landing Page Pricing Update | ✅ Done |
| Real-time WebSockets for Queue | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |
| React + Next.js Frontend | ⬜ Pending |

---

## ✅ Completed in Session 5 (April 5, 2026)

### 🧹 Repository Cleanup
- [x] Removed `change_db_password.sql`, `create_db.py`, `force_delete_user.py`, `setup_database.py`, `start_server.bat`, `start_server_local.bat`, `temp.json`
- [x] README updated with Stripe badge, payments API table, client orders page, updated pricing

### 📊 Current Version: 6.1.0


---

## ✅ Completed in Session 6 (April 5, 2026)

### 📧 Email Service Overhaul
- [x] Migrated from Gmail SMTP to **Resend API**
- [x] All transactional emails use Resend SDK
- [x] CC_EMAIL auto-copies all emails to `baxterdavid.mojica@gmail.com`
- [x] `requirements.txt` pinned to exact versions
- [x] `docker-compose.yml` updated with `RESEND_API_KEY`

### 📊 Current Version: 6.2.0

### 🔑 Required Render Environment Variables (add to Render dashboard):
```
RESEND_API_KEY=re_your_api_key_here
FROM_EMAIL=onboarding@resend.dev
CC_EMAIL=baxterdavid.mojica@gmail.com
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### Extended User UX Customization
- [x] **User UI Customization** ? *(Added April 2026)*
  - Granular Sidebar module access via \UserSidebarSetting\ mapping.
  - Sidebar toggling scoped strictly to individual users over blanket roles.
  - Extended dynamic visibility rules to Client modules.

---

## ✅ Completed in Session 7 (April 13, 2026)

### 🔀 User-Based Sidebar Visibility
- [x] `UserSidebarSetting` model — sidebar tabs stored per `user_id` not `role_id`
- [x] `GET /auth/users/{user_id}/sidebar` — fetch per-user sidebar config
- [x] `PUT /auth/users/{user_id}/sidebar` — save per-user sidebar config
- [x] `sidebar-management.html` — shows individual user cards instead of role cards
- [x] Client tabs (Shop, Cart, Reserve, My Orders) added to management UI
- [x] All 35 frontend pages updated to new user-sidebar API
- [x] `profile.js` updated for new permission fetch

### 📊 Current Version: 6.3.0 (Public: V2.3)

## 🔄 Updated Phase 2 Status (April 13, 2026 — Session 7)

| Feature | Status |
|---------|--------|
| User-Based Sidebar Visibility | ✅ Done |
| Stripe Payment Integration | ✅ Done |
| Email Notifications (Resend API) | ✅ Done |
| Multi-Tenant Data Isolation | ✅ Done |
| Real-time WebSockets for Queue | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |
| React + Next.js Frontend | ⬜ Pending |

---

## 🔜 Planned — Session 8

### 🔐 Feature 1: Staff Product/Service Permissions Fix
**Target Version:** V2.4 | **Priority:** High

#### Problem:
Staff (role: `user`) currently has `manage_products` permission which allows them to add, edit, and soft-delete products/services. This should be restricted — staff should only be able to **view** products/services, not modify them.

#### What Needs to Change:

**Backend (`commands/database/seed_data.py` + `commands/users/setup_demo_accounts.py`):**
- Remove `manage_products` from the default `user` (staff) role permissions
- Staff role should only retain: `view_locations`, `manage_invoices`, `view_invoices`, `view_reports`

**Frontend (`frontend/products.html`, `frontend/services.html`):**
- Hide Add / Edit / Delete buttons when logged-in user is staff (no `manage_products` permission)
- Show read-only view of products/services for staff
- Permission check already exists via `has_permission("manage_products")` on the backend — frontend just needs to respect it

**Permissions Matrix (Updated):**

| Permission | Superadmin | Admin | Staff | Client |
|---|---|---|---|---|
| `manage_products` | ✅ | ✅ | ❌ | ❌ |
| `manage_locations` | ✅ | ✅ | ❌ | ❌ |
| `view_locations` | ✅ | ✅ | ✅ | ❌ |
| `manage_invoices` | ✅ | ✅ | ✅ | ❌ |
| `view_invoices` | ✅ | ✅ | ✅ | ❌ |
| `view_reports` | ✅ | ✅ | ✅ | ❌ |
| `manage_settings` | ✅ | ✅ | ❌ | ❌ |
| `manage_users` | ✅ | ❌ | ❌ | ❌ |

**Files to Modify:**
- [ ] `commands/database/seed_data.py` — remove `manage_products` from staff role defaults
- [ ] `commands/users/setup_demo_accounts.py` — update demo staff permissions
- [ ] `frontend/products.html` — hide add/edit/delete for non-`manage_products` users
- [ ] `frontend/services.html` — hide add/edit/delete for non-`manage_products` users
- [ ] `frontend/permissions-management.html` — reflect updated default matrix

---

### 🛍️ Feature 2: Client Shopping Experience Overhaul (Lazada/Shopee/TikTok Shop Style)
**Target Version:** V2.5 | **Priority:** High

#### Goal:
Redesign the client-facing shopping experience (`shop.html`, `cart.html`) to match the modern e-commerce UX of Lazada, Shopee, and TikTok Shop — product cards with images, ratings display, quantity selectors, sticky cart, flash banners, and a smooth checkout flow.

#### Planned UI/UX Changes:

**`frontend/shop.html`:**
- [ ] **Product Grid** — responsive card grid (2 cols mobile, 3-4 cols desktop)
- [ ] **Product Cards** — image thumbnail, name, price with strikethrough original price, "Add to Cart" button, stock badge
- [ ] **Category Filter Bar** — horizontal scrollable tabs (All, Products, Services, Featured)
- [ ] **Search Bar** — live search/filter by name
- [ ] **Flash Sale Banner** — promotional banner at top (configurable by owner)
- [ ] **Sort Options** — Price: Low to High / High to Low, Newest
- [ ] **Empty State** — illustrated empty state when no products match filter
- [ ] **Floating Cart Button** — sticky bottom-right cart icon with item count badge

**`frontend/cart.html`:**
- [ ] **Cart Item Cards** — product image, name, unit price, quantity stepper (+/-), subtotal, remove button
- [ ] **Order Summary Panel** — sticky sidebar with subtotal, fees, total
- [ ] **Voucher/Promo Code Field** — input for discount codes (UI only for now)
- [ ] **Payment Method Selector** — visual cards for Cash, QR, Stripe
- [ ] **Checkout CTA** — prominent "Place Order" button with total amount
- [ ] **Empty Cart State** — illustrated empty state with "Continue Shopping" link

**`frontend/checkout.html` (Stripe):**
- [ ] Cleaner card layout matching the new shop theme
- [ ] Order summary visible alongside payment form

**New CSS (`frontend/css/shop.css`):**
- [ ] Shopee/Lazada-inspired color palette (orange accent or brand color)
- [ ] Card hover effects, shadows, smooth transitions
- [ ] Mobile-first responsive grid
- [ ] Skeleton loading states for product cards

**Backend (no changes needed)** — existing `/api/settings/products`, `/api/cart`, `/api/orders` endpoints are sufficient.

#### Inspiration References:
- Shopee: category tabs, card grid, floating cart, flash sale banners
- Lazada: clean product cards with image, price, ratings area
- TikTok Shop: sticky add-to-cart, quantity selector on card, smooth animations

#### Files to Create/Modify:
- [ ] `frontend/shop.html` — full redesign
- [ ] `frontend/cart.html` — full redesign
- [ ] `frontend/checkout.html` — minor layout improvements
- [ ] `frontend/css/shop.css` — NEW dedicated shop stylesheet
