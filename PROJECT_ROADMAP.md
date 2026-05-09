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
- [x] Audit logging ✅ *(Full audit_logs table + viewer page + CUD logging across all routers — May 2026)*
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

---

## ✅ Completed in Session 8 (April 2026)

### 🔐 Feature 1: Staff Product/Service Permissions Fix
- [x] `hideElementsWithoutPermission()` called after dynamic card render in `products.js` and `services.js`
- [x] `setup_demo_accounts.py` explicitly sets staff role to `[view_locations, manage_invoices, view_invoices, view_reports]`
- [x] Edit/Delete buttons correctly hidden for staff on Products and Services pages

### 👥 User Management Sidebar Submodules
- [x] "Permissions" and "Sidebar Tabs" moved under collapsible "User Management" nav group in sidebar
- [x] Smooth slide animation, auto-opens on active page, collapsed-sidebar safe
- [x] `.nav-group`, `.nav-sub` CSS added to `style.css`

### 🔒 Owner Self-Protection
- [x] `permissions-management.html` — owner's own card locked (no delete, no permission toggles)
- [x] `sidebar-management.html` — owner's own sidebar tabs locked (no toggles)
- [x] Both pages have JS-level guards in addition to UI locks

### 🐛 Mojibake Emoji Fixes
- [x] `reports.html` — fixed `📊`, `📦`, `🔧`, `☰`, `🚗`, `₱`
- [x] `dashboard.html` — fixed `📅` filter options, `✏️` floating button
- [x] `invoices.html` — fixed `🔍` search placeholder

### 📄 Pagination
- [x] Reports invoices table — 10 rows/page with `reportPagination` bar
- [x] Invoices page — 10 rows/page with `invoicePagination` bar
- [x] `.pagination-bar` + `.page-btn` CSS added to `style.css`

### 🎨 Page Load Animation
- [x] `@keyframes fadeSlideIn` applied to all major card/section types
- [x] Staggered delays for cascading entrance effect
- [x] `stat-card` and `header` use opacity-only animation to avoid stacking context issues

### 🔧 Settings No Logo Fix
- [x] File input cleared when "No Logo" selected
- [x] `businessForm` sends `logo: null` correctly

### 📱 Mobile UX
- [x] Hamburger button removed (`display: none !important`)
- [x] Left-edge tap tab injected via JS — opens sidebar on mobile
- [x] Mobile content padding reduced from 70px → 20px

### 🖼️ Sidebar Fixes
- [x] `padding-right: 36px` on `.sidebar .logo` — close button no longer overlaps business name
- [x] `.sidebar.collapsed .welcome-section { display: none }` — greeting hidden when collapsed

### 📊 Client Dashboard Pagination
- [x] Reusable `paginate()` helper added
- [x] All 4 tables paginated at 8 rows/page
- [x] Resize dispatch on load fixes table width compression

### 🔝 Profile Dropdown Z-Index
- [x] `header { position: relative; z-index: 200 }` — header stacking context above animated cards
- [x] Profile dropdown always visible on all pages for all account types

### 📊 Current Version: 6.4.0 (Public: V2.4)

## 🔄 Updated Phase 2 Status (April 2026 — Session 8)

| Feature | Status |
|---------|--------|
| Staff Permissions Fix | ✅ Done |
| User Management Sidebar Submodules | ✅ Done |
| Owner Self-Protection | ✅ Done |
| Pagination (Reports + Invoices + Client Dashboard) | ✅ Done |
| Page Load Animations | ✅ Done |
| Mobile Edge Tab (no hamburger) | ✅ Done |
| Profile Dropdown Z-Index Fix | ✅ Done |
| Real-time WebSockets for Queue | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |
| React + Next.js Frontend | ⬜ Pending |
| Client Shopping Experience Overhaul | ⬜ Pending (Session 9) |

---

## ✅ Completed — Session 9 *(April 15, 2026)*

### 🛍️ Feature 1: Client Shopping Experience Overhaul (Lazada/Shopee/TikTok Shop Style)
**Version:** V2.5 | **Priority:** High ✅

#### Goal:
Full redesign of the client-facing shopping experience to match modern e-commerce UX — product cards with images, category filters, quantity selectors, sticky cart, and smooth checkout flow.

#### Changes Implemented:

**`frontend/shop.html`:** ✅
- [x] Responsive product card grid (2 cols mobile → 5 cols desktop)
- [x] Product cards — emoji/image thumbnail, name, description, price, Add to Cart / Reserve button, type badge
- [x] Category filter bar — horizontal scrollable tabs (All, Products, Services, Featured)
- [x] Live search/filter by name and description
- [x] Flash sale countdown banner with live timer
- [x] Sort options — Best Match, Price Low→High / High→Low, Name A-Z
- [x] Illustrated empty state when no products match filter
- [x] Floating sticky cart button (bottom-right) with item count badge
- [x] Sticky top header with search bar (Lazada-style)
- [x] Promo top bar with free delivery messaging
- [x] Voucher collection row (UI)
- [x] Cart nudge toast on Add to Cart
- [x] Mobile bottom navigation bar
- [x] Skeleton loading cards while fetching

**`frontend/cart.html`:** ✅
- [x] Cart item rows — thumbnail, name, type badge, FREE SHIPPING tag, unit price, qty stepper (+/-), remove button
- [x] Per-item and Select All checkboxes (Lazada-style)
- [x] Sticky right-side order summary panel (desktop)
- [x] Voucher/promo code input with hardcoded test codes (SAVE10, CARWASH50, PROMO20)
- [x] Visual payment method selector cards (loaded from backend + fallback defaults)
- [x] Prominent "Check Out (N)" CTA button with total amount
- [x] Stripe "Pay with Card" secondary CTA
- [x] Illustrated empty cart state with "Continue Shopping" link
- [x] Mobile sticky bottom checkout bar with total + checkout button

**`frontend/checkout.html`:**
- [ ] Cleaner layout matching new shop theme *(pending)*

- [x] **Standardized Mobile Headers** — Implemented rigid 3-column flex layout (Back/Title/Actions) for consistency across pages.
- [x] **Corner Button Anchoring** — Fixed width containers (44px) for side buttons to prevent centering/stacking issues.
- [x] **Advanced Search Integration** — Unified real-time filtering for both Cart (by Name) and Vouchers (Text + Category).
- [x] **UX Spacing Polish** — Increased header padding (24px) for better visual alignment on narrow displays.
- [x] **Cart Logic Refinement** — Removed global trash buttons; implemented safer per-item row deletion.

**Backend:** No changes needed — existing `/api/settings/products`, `/api/cart`, `/api/orders` endpoints sufficient.


---

## 🔜 Phase 3 — Medium-term (Next 4-8 weeks)

### 📱 Feature 1: Progressive Web App (PWA)
**Target Version:** V3.0 | **Priority:** Medium

- [ ] `manifest.json` — app name, icons, theme color, display mode
- [ ] Service worker (`sw.js`) — cache-first strategy for static assets
- [ ] Offline fallback page (`offline.html`)
- [ ] "Add to Home Screen" prompt on mobile
- [ ] Background sync for cart/order actions when offline
- [ ] Push notification support (browser-level)

### 📊 Feature 2: Advanced Dashboard & Analytics
**Target Version:** V3.1 | **Priority:** Medium

- [ ] Revenue trend charts (weekly, monthly, quarterly, annual) with real data
- [ ] Customer analytics — new vs returning, top spenders
- [ ] Service performance metrics — most booked, avg completion time
- [ ] Product sales breakdown — units sold, revenue per product
- [ ] Custom date range picker for all report filters
- [ ] Automated report scheduling — email PDF report weekly/monthly
- [ ] Advanced filtering — by location, staff, product category
- [ ] Dashboard widgets draggable and resizable (superadmin)

### 🔔 Feature 3: Real-time Features (WebSockets)
**Target Version:** V3.2 | **Priority:** Medium

- [ ] WebSocket endpoint (`/ws/queue`) — live queue position updates
- [ ] WebSocket endpoint (`/ws/orders`) — live order status changes
- [ ] Client dashboard auto-updates without polling
- [ ] Admin queue management shows live position changes
- [ ] Browser push notifications for order/reservation status changes
- [ ] Service worker integration for background push delivery
- [x] Notification preferences per user (opt-in/out per event type) ✅ *(Session 13 — in-app notification preferences UI)*

### 📱 Feature 4: Mobile Optimization
**Target Version:** V3.3 | **Priority:** Medium

- [ ] Touch-friendly tap targets (min 44px) across all pages
- [ ] Swipe gestures for sidebar open/close
- [ ] Bottom navigation bar for client pages on mobile
- [ ] Pinch-to-zoom disabled on form inputs (prevent iOS zoom)
- [ ] Mobile-optimized table layouts (card view on small screens)
- [ ] Responsive chart sizing for Chart.js on mobile

---

## 🔜 Phase 4 — Long-term (Next 8-16 weeks)

### ⚛️ Feature 1: Next.js Frontend Migration
**Target Version:** V4.0 | **Priority:** Low (future)

- [ ] Next.js 14 with App Router setup
- [ ] TypeScript integration across all components
- [ ] Tailwind CSS replacing `style.css`
- [ ] Reusable component library (Button, Card, Table, Modal, Sidebar)
- [ ] Server-side rendering (SSR) for SEO-critical pages (landing, shop)
- [ ] Static generation for product/service pages
- [ ] React Query for API state management
- [ ] Zustand for global auth/cart state
- [ ] Migrate all 35+ HTML pages to Next.js routes
- [ ] Preserve all existing API endpoints (FastAPI backend unchanged)

### 🤖 Feature 2: AI & Smart Automation
**Target Version:** V4.1 | **Priority:** Low (future)

- [ ] AI-powered queue optimization — predict service duration, auto-assign bays
- [ ] Smart scheduling — suggest optimal appointment slots based on historical data
- [ ] Dynamic pricing — surge pricing during peak hours (configurable)
- [ ] Customer churn prediction — flag clients who haven't visited in X days
- [ ] Personalized service recommendations based on order history
- [ ] Predictive inventory alerts — low stock warnings based on usage trends
- [ ] Automated promotional emails triggered by AI insights

### 🏢 Feature 3: Multi-location & Franchise Support
**Target Version:** V4.2 | **Priority:** Low (future)

- [ ] Multiple physical locations per business (beyond washing bays)
- [ ] Location-specific products, pricing, and staff
- [ ] Centralized reporting across all locations
- [ ] Franchise management — parent account oversees child businesses
- [ ] Location-based client routing (nearest branch)
- [ ] Per-location theme customization
- [ ] Cross-location inventory transfers

### 🔒 Feature 4: Security Hardening
**Target Version:** V4.3 | **Priority:** Medium (ongoing)

- [ ] Rate limiting via `slowapi` — prevent brute-force on `/auth/login`
- [ ] JWT moved from `localStorage` to `HttpOnly` + `Secure` cookies
- [ ] Refresh token rotation — 15min access tokens + long-lived refresh tokens
- [ ] Content Security Policy (CSP) headers on all pages
- [ ] Subresource Integrity (SRI) for CDN scripts (Chart.js, Firebase SDK)
- [x] Audit log table — log all sensitive actions (login, permission changes, deletions) ✅ *(Session 13)*
- [ ] CORS hardening — restrict to exact production domains only
- [ ] `pip audit` + `npm audit` in CI/CD pipeline
- [ ] Automated daily database backups on Render
- [ ] Secrets scanning pre-commit hook (`detect-secrets`)

### 💳 Feature 5: Payments Expansion
**Target Version:** V4.4 | **Priority:** Medium

- [ ] Stripe live mode activation (swap test keys for live keys)
- [ ] Payment history page — all transactions with status and receipt download
- [ ] Refund processing via Stripe API
- [ ] Saved payment methods (Stripe Customer + PaymentMethod)
- [ ] Recurring payments / subscriptions for loyalty members
- [ ] GCash / Maya integration (Philippines-specific)
- [ ] Invoice PDF with payment receipt attached

---

## 📋 Full Phase Summary

| Phase | Target | Key Deliverables | Status |
|-------|--------|-----------------|--------|
| Phase 1 | ✅ Done | Auth, email, Firebase, sidebar, deployment | ✅ Complete |
| Phase 2 | ✅ Done | Multi-tenant, Stripe, e-commerce, user sidebar, V2.4 | ✅ Complete |
| Session 9 | V2.5 | Client shopping experience overhaul | ✅ Done |
| Session 10 | V2.6 | Admin Side: Voucher CRUD, Flash Sales, Order UI | ✅ Done |
| Session 11 | V2.7 | Top navbar, dashboard stat redesign, coupon UI | ✅ Done |
| Session 12 | V2.8 | Dashboard grid refinement, dynamic theming, sidebar polish | ✅ Done |
| Session 13 | V2.9 | Queue/permissions theme fix, URL encryption, audit logging, notifications | ✅ Done |
| Phase 3 | V3.x | PWA, advanced dashboard, WebSockets, mobile UX | 📅 Planned |
| Phase 4 | V4.x | Next.js migration, AI, multi-location, security, payments | 🚀 Future |

---

### 🐛 Session 8 — Additional Fixes (Order & Queue Management)

#### Mojibake & Animation Fix
- [x] `order-management.html` — all emoji artifact text fixed (`🔭`, `🧾`, `📅`, `💰`, `💳`, `📦`, `×`, etc.)
- [x] `queue-management.html` — same emoji fixes + `All Reservations` button text corrected
- [x] `.order-card` and `.queue-card` now animate with `fadeSlideIn` + staggered delays on load
- [x] Hardcoded sidebar logo emoji removed from both pages (now dynamic via `menu.js`)
- [x] `body { background: white }` override removed from queue page (was breaking theme system)
- [x] Container ID corrected in queue page (`reservations-list`)

---

## ✅ Completed in Session 10

### ⚡ Flash Sale Management (Admin/Owner)
- [x] `FlashSale` + `FlashSaleItem` models in `database.py`
- [x] `app/routers/flash_sales.py` — GET, POST, PUT, PATCH toggle, DELETE (soft)
- [x] `frontend/flash-sale-management.html` — stats row, live countdown, product multi-select, create/edit modal, toggle, soft delete
- [x] Registered in `main.py`

### 🎟️ Coupon Management (Admin/Owner)
- [x] `frontend/coupon-management.html` — stats row, search/filter by status & type, coupon cards, create/edit modal, toggle, soft delete
- [x] Backend already complete from V2.5 (`coupons.py`)

### 📱 UI Responsiveness & UX Standardization
- [x] **Desktop Layout Stabilization**: Migrated `coupon-management.html`, `flash-sale-management.html`, `shop.html`, `reserve.html`, `cart.html`, and `vouchers.html` to a unified sidebar-and-content layout.
- [x] **Dashboard Interactions**: Added clickable active orders tile on client dashboard linking to `client-orders.html`.
- [x] **Mobile Adjustments**: Standardized hamburger menu and sidebar behavior for mobile view across all dashboard modules.

### 🔒 Role-Based Access Control (RBAC) Isolation
- [x] **Frontend Route Guards**: Implemented `enforcePageAccess` in `menu.js` to block unauthorized role redirection (e.g., Staff accessing Client pages via direct URL).
- [x] **Backend Security Hardening**: Added `is_client` and `is_staff_or_admin` dependencies in `app/permissions.py` and enforced them on sensitive endpoints (`client/dashboard`, `cart/`, etc.).

### 🐛 Mojibake Fix
- [x] Fixed corrupted emoji in 7 frontend pages: `dashboard.html`, `invoices.html`, `reports.html`, `order-management.html`, `queue-management.html`, `sidebar-management.html`, `products.html`, `services.html`
- [x] All emoji replaced with HTML entities for encoding safety

### 📊 Current Version: 6.7.0 (Public: V2.6)

## 🔄 Updated Phase 2 / Session 10 Status

| Feature | Status |
|---------|--------|
| Flash Sale Management (Admin) | ✅ Done |
| Coupon Management (Admin) | ✅ Done |
| Mojibake Fix (7 pages) | ✅ Done |
| Real-time WebSockets for Queue | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |
| React + Next.js Frontend | ⬜ Pending |

## 🔜 Next Session (Session 11) — V2.7

### Planned:
- [x] Link flash sales to shop.html — show sale price/badge on product cards when a flash sale is active ✅ *(Done in Session 12)*
- [x] Link coupons to cart.html — validate coupon code against backend on apply ✅ *(Done in Session 12)*
- [ ] Admin order UI improvements — bulk status update, order search/filter
- [x] Add `coupon-management.html` and `flash-sale-management.html` to admin sidebar navigation ✅ *(Done in Session 13)*

---

## ✅ Completed in Session 9 (April 2026)

### 🏷️ Admin Coupon UI — Theme Colors
- [x] `coupons.html` — all hardcoded `#f02d55` replaced with `var(--primary-color)` and `var(--sidebar-color)`
- [x] Buttons, stat values, code badges, focus rings, checkbox accent all use CSS variables
- [x] Coupon management page now matches owner's theme automatically

### 📱 Client Mobile Facebook-Style Bottom Navbar
- [x] `frontend/js/client-nav.js` — NEW shared script injecting unified SVG bottom nav
- [x] 5 tabs: Home, Shop, Reserve, Cart (with badge), Orders
- [x] Active tab highlighted with `var(--primary-color)` + indicator dot
- [x] Cart badge fetches live count from `/api/cart`
- [x] `menu.js` dynamically loads `client-nav.js` for client accounts on mobile only
- [x] Desktop: sidebar retained as-is (no change)
- [x] `style.css` — `body.client-page` hides sidebar on mobile, adds bottom padding

### 🎨 Theme Colors — Client Pages
- [x] `shop.html` — `--brand: #f02d55` → `var(--primary-color, #667eea)`
- [x] `reserve.html` — `--brand: #8b5cf6` → `var(--primary-color, #667eea)`
- [x] `cart.html` — `--brand: #f02d55` → `var(--primary-color, #667eea)`
- [x] All three pages now match owner's theme settings automatically

### 🗑️ Old Emoji Mobile Nav Removed
- [x] `shop.html` — old emoji nav HTML removed, CSS `display: none !important`
- [x] `reserve.html` — old emoji nav HTML removed, CSS `display: none !important`
- [x] `cart.html` — old emoji nav HTML removed, CSS `display: none !important`

### 🖥️ Cart Desktop Layout Fix
- [x] `cart.html` — `.page-body { max-width: 960px; margin: 0 auto }` on desktop

### 🚨 Render Hotfix
- [x] `start.sh` — added `add_user_soft_delete_columns.py` + inline `ALTER TABLE IF NOT EXISTS` for `is_active` and `deleted_at` columns

### 📊 Current Version: 6.5.0 (Public: V2.5)

## 🔄 Updated Phase 2 Status (April 2026 — Session 9)

| Feature | Status |
|---------|--------|
| Client Shopping Experience Overhaul | ✅ Done (theme + mobile nav) |
| Admin Coupon UI Theme Integration | ✅ Done |
| Facebook-style Mobile Bottom Nav | ✅ Done |
| Render Production Hotfix (is_active) | ✅ Done |
| Real-time WebSockets for Queue | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |
| React + Next.js Frontend | ⬜ Pending (Phase 4) |

---

## ✅ Completed in Session 11

### 🔝 Top Navbar
- [x] `injectTopNavbar()` in `menu.js` — global injection, no per-page HTML needed
- [x] Business logo + name in top navbar (synced with branding API)
- [x] Search field with slide-in animation
- [x] Notification bell with badge
- [x] Settings gear icon shortcut
- [x] Profile dropdown (role name, Settings, Logout)
- [x] Click-outside closes dropdown
- [x] Sidebar branding (`sidebarLogo`/`sidebarName`) replaced with `topNavbarLogo`/`topNavbarName`
- [x] Sidebar logo area hidden — branding lives in top navbar only
- [x] Collapse sidebar button at bottom of sidebar with chevron + label
- [x] Logout removed from sidebar tab list

### 📊 Dashboard Stat Cards
- [x] 8 stat cards (was 4): Today's Revenue, Monthly Revenue, Cars Washed, Active Bays, Pending Invoices, Completed Orders, Average Rating, Total Clients
- [x] SVG icons per card, colored accent top border, hover lift
- [x] 4-column responsive grid (2-col at 1200px, 1-col at 768px)

### 🎟️ Coupon Management UI
- [x] Migrated to standard sidebar + `<main class="content">` layout
- [x] Desktop row-list (ticket-stub style) + mobile card grid (responsive toggle at 900px)
- [x] All emoji replaced with HTML entities
- [x] Stats row uses theme variables (no hardcoded colors)

### 📊 Current Version: 6.7.0 (Public: V2.7)

## 🔄 Updated Status (Session 11)

| Feature | Status |
|---------|--------|
| Top Navbar (global injection) | ✅ Done |
| Dashboard stat card redesign | ✅ Done |
| Coupon management UI overhaul | ✅ Done |
| Flash sale linked to shop.html | ⬜ Pending |
| Coupon validation in cart.html | ⬜ Pending |
| Real-time WebSockets for Queue | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |
| React + Next.js Frontend | ⬜ Pending |

## ✅ Completed in Session 12 *(May 5, 2026)* — V2.8

### 🎨 Dashboard & Grid System Refinement
- [x] **High-Density Grid (1/6)** — Added `1/6` width (span 2) to the 12-column grid, enabling up to 6 modules per row
- [x] **Dynamic Theming** — Stat cards inherit owner's sidebar theme via `var(--sidebar-color)`, replacing hardcoded accents
- [x] **Edit Dashboard UI** — Module editor updated with visual width selector for the new 1/6 size

### 🧭 App Shell & Sidebar Polish
- [x] **Top Navbar "Edit Dashboard"** — Moved edit entry point from floating button to permanent Top Navbar button (Owner/Admin only)
- [x] **Role Access Fix** — Case-insensitive role check for Edit Dashboard button (`Owner`, `Admin`, `Superadmin`)
- [x] **Sidebar Collapse Centering** — Fixed vertical alignment of collapse button in mini/collapsed state
- [x] **Sub-menu Spacing Fix** — Resolved `.sidebar ul` 40px margin specificity issue; tightened User Management dropdown spacing

### 📊 Current Version: 6.8.0 (Public: V2.8)

## 🔄 Updated Status (Session 12)

| Feature | Status |
|---------|--------|
| Dashboard high-density grid (1/6) | ✅ Done |
| Stat card dynamic theming | ✅ Done |
| Top Navbar Edit Dashboard button | ✅ Done |
| Sidebar collapse + sub-menu fixes | ✅ Done |
| Flash sale linked to shop.html | ⬜ Pending |
| Coupon validation in cart.html | ⬜ Pending |
| Real-time WebSockets for Queue | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |

## 🔜 Next Session (Session 13) — V2.9

### Planned:
- [x] Connect flash sales to `shop.html` — show sale badge + discounted price on product cards when a flash sale is active ✅ *(Done in Session 12)*
- [x] Connect coupon validation to `cart.html` — call `POST /coupons/validate` on apply, show discount in order summary ✅ *(Done in Session 12)*
- [x] Add `coupon-management.html` and `flash-sale-management.html` to admin sidebar navigation ✅ *(Done in Session 13)*
- [ ] Apply top navbar to remaining pages that haven't been updated yet

---

## ✅ Completed in Session 12

### ⚡ Flash Sales → Shop
- [x] `loadFlashSales()` fetches active sales from API on shop init
- [x] Flash banner text updated with live sale title
- [x] Product cards show strikethrough price + discounted price + `⚡ X% OFF` badge
- [x] Countdown timer driven by real `ends_at` timestamp from API
- [x] Auto-refresh when sale expires

### 🎟️ Coupon Validation → Cart
- [x] `appliedCoupon` state tracks applied coupon
- [x] Auth check before applying coupon
- [x] `renderAppliedCoupon()` — input ↔ applied pill toggle
- [x] `removeCoupon()` — clears coupon and resets discount
- [x] Fixed double-parse crash on error response

### 🔀 URL Obfuscation Router
- [x] `frontend/js/router.js` — 22 pages mapped to random hex hashes
- [x] `history.replaceState` hides real filenames from URL bar
- [x] Direct hash URL entry handled (bookmarks, shared links)
- [x] `index.html` gateway resolver for hash-based entry
- [x] Added to all pages

### 🎨 Theme & UX
- [x] `.btn-primary`, `.btn-edit`, `.filter-btn.active` use `var(--sidebar-color)`
- [x] Order management filter buttons use CSS classes (no inline styles)
- [x] Order card header gradient uses theme color
- [x] Sidebar FOUC prevention via inline script + `.sidebar-pre-collapsed` CSS

### 📊 Current Version: 6.8.0 (Public: V2.8)

## 🔄 Updated Status (Session 12)

| Feature | Status |
|---------|--------|
| Flash sales → shop.html | ✅ Done |
| Coupon validation → cart.html | ✅ Done |
| URL obfuscation router | ✅ Done |
| Theme color propagation | ✅ Done |
| Sidebar FOUC prevention | ✅ Done |
| Real-time WebSockets for Queue | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |
| React + Next.js Frontend | ⬜ Pending |

## ✅ Completed in Session 13 *(May 8, 2026)* — V2.9

### 🎨 UI/Theme Fixes
- [x] **Queue Management Tiles** — Updated `queue-management.html` tiles to use `var(--sidebar-color)` instead of hardcoded gradients
- [x] **Permissions Page Cleanup** — Removed all emoji from `permissions-management.html`, replaced with SVG icons, flat card style with themed border-top
- [x] **Sidebar Tabs Emoji Removal** — Added icon entries for flash-sales, users, payment-methods, audit-logs, notifications in `normalizeSidebarIcons()`

### 🔒 URL Encryption Improvement
- [x] **32-char Route Tokens** — Upgraded `router.js` from 8-char to 32-char hex tokens with legacy backward compatibility
- [x] **Full URL Obfuscation** — Intercepted all navigation paths (link clicks, JS assignments, direct URL entry) so `.html` never appears in URL bar

### 📋 Audit Logging
- [x] **Audit Log Table** — Created `audit_logs` table with indexes via `commands/database/add_audit_logs_table.py`
- [x] **AuditLog Model** — Added SQLAlchemy model to `app/database.py`
- [x] **Audit Utility** — Created `app/audit.py` with `log_audit()` and `get_client_ip()` helpers
- [x] **Audit API Router** — `GET /api/audit-logs` with pagination, filtering, business scoping, admin-only access
- [x] **CUD Logging Integration** — Added `log_audit()` calls to all write operations across 9 routers (settings, invoices, orders, reservations, cart, payment_methods, coupons, flash_sales, auth)
- [x] **Audit Log Viewer Page** — `frontend/audit-logs.html` with filterable table (user, action, resource type, date range), pagination, expandable JSON details

### 🔔 Notification System
- [x] **Notifications Tables** — Created `notifications` + `notification_preferences` tables via `commands/database/add_notifications_tables.py`
- [x] **Notification Models** — Added `Notification` and `NotificationPreference` SQLAlchemy models
- [x] **Notification Service** — Created `app/notification_service.py` with `create_notification()`, `notify_business_admins()`, `get_or_create_preferences()`
- [x] **Notification API** — Full CRUD: `GET /api/notifications` (paginated + unread count), `PATCH /{id}/read`, `PATCH /read-all`, `DELETE /{id}` (soft-delete), `GET/PUT /preferences`
- [x] **Bell Icon Dropdown** — Dynamic badge, dropdown panel with 10 recent notifications, mark-as-read, relative timestamps, click-outside-to-close
- [x] **Auto-generate Notifications** — Triggers on: new order, order status change, reservation status change, payment received, coupon applied, flash sale activated, permission changes
- [x] **Notification Preferences** — Toggle switches in Settings page for 6 notification types, persisted immediately on change

### 📊 Current Version: 6.9.0 (Public: V2.9)

## 🔄 Updated Status (Session 13)

| Feature | Status |
|---------|--------|
| Queue/permissions theme fix | ✅ Done |
| URL encryption (32-char tokens) | ✅ Done |
| Audit logging (full system) | ✅ Done |
| Notification system (full) | ✅ Done |
| Bell icon dropdown | ✅ Done |
| Notification preferences UI | ✅ Done |
| Real-time WebSockets for Queue | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |
| React + Next.js Frontend | ⬜ Pending |

## 🔜 Next Session (Session 14) — V3.0

### Planned:
- [ ] Connect flash sales to `shop.html` — show sale badge + discounted price on product cards when a flash sale is active
- [ ] Progressive Web App (PWA) — manifest.json, service worker, offline fallback
- [ ] WebSocket integration for real-time queue updates
- [ ] Browser push notifications for order/reservation status changes


---

## ✅ Completed in Session 13 *(May 8, 2026)* — V2.9

### 🐛 Bug Fixes
- [x] **Sidebar collapse re-open** — collapsed sidebar now shows expand chevron; `.sidebar-close` no longer hidden when collapsed
- [x] **business_sub_name migration** — column added to DB + `start.sh` for Render
- [x] **Dashboard sidebar active color** — fixed CSS variable override conflict

### 👤 Profile Edit in Top Navbar
- [x] Inline edit modal from navbar dropdown — name + photo upload, saves to API, updates navbar live

### 🖼️ Business Logo Update Button
- [x] Dedicated "Update Logo" button in Settings — saves logo independently from full business form

### 🌐 Footer & Support Tickets
- [x] Footer updated to BuxTek Inc. 2025 branding
- [x] "Contact Customer Support" button in footer opens ticket submission modal
- [x] `SupportTicket` model + `/api/support-tickets` router (submit, list, view, reply, close)
- [x] `tickets.html` — owner-only tickets management page with reply-by-email feature
- [x] Tickets tab in owner/superadmin sidebar

### 📊 Current Version: 6.9.0 (Public: V2.9)

## 🔄 Updated Status (Session 13)

| Feature | Status |
|---------|--------|
| Sidebar collapse fix | ✅ Done |
| Profile edit in navbar | ✅ Done |
| Business logo update button | ✅ Done |
| Footer BuxTek branding | ✅ Done |
| Support ticket system | ✅ Done |
| Flash sale → shop.html | ⬜ Pending |
| Coupon validation → cart.html | ⬜ Pending |
| Real-time WebSockets for Queue | ⬜ Pending |

## 🔜 Next Session (Session 14) — V3.0

### Planned:
- [ ] Connect flash sales to `shop.html` — show sale badge + discounted price on product cards
- [ ] Connect coupon validation to `cart.html` — validate against backend on apply
- [ ] Apply top navbar to remaining pages not yet updated
- [ ] PWA manifest + service worker (offline support)


---

## 🔜 Next Session (Session 14) — V2.9 Bugfix + DB Migration

### 🐛 Bug Fixes (Priority)

#### 1. Upload Photo — Edit Profile Modal
- [ ] Base64 photo upload in `saveNavbarProfile()` not persisting correctly
- [ ] Investigate whether large base64 payload exceeds request body limit
- [ ] Consider resizing image client-side before encoding (canvas resize to max 200px)

#### 2. Sidebar Stuck After Collapse
- [ ] Clicking collapse button does not immediately re-open sidebar — requires a nav tab click first
- [ ] Root cause likely: `sidebar.onclick` handler and `closeBtn.onclick` conflict — both fire on the same click event
- [ ] Fix: ensure the close/expand button's click does not bubble to the sidebar's own click handler

#### 3. Dashboard Sidebar Hover Color Mismatch
- [ ] Hover/active color on `dashboard.html` does not match theme
- [ ] `dashboard.js` sets `--sidebar-active-color` via `setProperty` but the injected `<style>` tag from a previous session may still be overriding it
- [ ] Audit all `dashboard-colors` style injections and ensure no leftover hardcoded hover rules

### 🗄️ Database Migration — Render → Aiven
- [ ] Create Aiven PostgreSQL instance (free tier or paid)
- [ ] Export current Render DB: `pg_dump` → `.sql` file
- [ ] Import to Aiven: `psql` with new connection string
- [ ] Update `DATABASE_URL` in Render environment variables
- [ ] Update `docker-compose.yml` `.env.example` with Aiven connection string format
- [ ] Test all endpoints after migration
- [ ] Update `README.md` database badge and connection docs

### 📊 Version Target: V2.9.1 (bugfix patch)

---

## ✅ Completed in Session 15

### 🚀 Onboarding & Paywall System (V3.0)
- [x] `add_subscriptions_table.py` — migration for subscriptions table + onboarding_completed column
- [x] `Subscription` model in `database.py`
- [x] `onboarding_completed` column on `User` model
- [x] `SubscriptionStatus`, `CreateCheckoutRequest`, `OnboardingStatusResponse` schemas
- [x] `get_business_subscription()`, `activate_trial()`, `update_subscription_from_webhook()`, `mark_onboarding_completed()` in `crud.py`
- [x] `subscriptions.py` router — activate-trial, create-checkout, status, billing-history, webhook
- [x] `onboarding.py` router — complete, status endpoints
- [x] `check_subscription_active` feature gate in `dependencies.py`
- [x] `/me/permissions` extended with `onboarding_completed` + `subscription` data
- [x] `onboarding.html` — multi-step onboarding with role-based slides + paywall
- [x] `plan-selection.html` — standalone plan management page
- [x] `trial-banner.js` — trial expiry warning banner (≤3 days)
- [x] `login.js` — onboarding redirect logic after login
- [x] `menu.js` — trial banner auto-loading on all admin pages
- [x] `api.js` — API.subscriptions + API.onboarding namespaces
- [x] `router.js` — new page tokens for onboarding + plan-selection
- [x] `vercel.json` — rewrites for new pages
- [x] `start.sh` — migration added to startup sequence

### 🗄️ Database & Infrastructure (Session 15)
- [x] Aiven PostgreSQL migration completed — all tables synced
- [x] All sequences reset to correct values
- [x] role_permissions duplicates cleaned up
- [x] Demo accounts seeded to Aiven via `setup_demo_accounts.py`
- [x] SSL connect_args fix for Aiven in `database.py`
- [x] schemas.py SubscriptionStatus ordering fix

### 📊 Current Version: 7.0.0 (Public: V3.0)

## 🔄 Updated Status (Session 15)

| Feature | Status |
|---------|--------|
| Onboarding flow (multi-step slides) | ✅ Done |
| Paywall + plan selection | ✅ Done |
| Free trial activation (14 days) | ✅ Done |
| Stripe subscription checkout | ✅ Done |
| Trial expiry banner | ✅ Done |
| Subscription webhook handler | ✅ Done |
| Aiven database migration | ✅ Done |
| Demo data seeded to Aiven | ✅ Done |
| SMS Notifications (Twilio) | ⬜ Pending |
| Real-time WebSockets for Queue | ⬜ Pending |
| React + Next.js Frontend | ⬜ Pending |

## 🔜 Next Session (Session 16) — V3.1

### Planned:
- [ ] Stripe live mode activation (swap test keys for live keys)
- [ ] Payment history page — all transactions with receipt download
- [ ] Refund processing via Stripe API
- [ ] Add `STRIPE_PRICE_LITE`, `STRIPE_PRICE_PLUS`, `STRIPE_PRICE_PRO` to Render env vars
- [ ] Test full onboarding → trial → upgrade flow end-to-end on production

---

## ✅ Completed in Session 16

### 🐛 Bug Fixes (V3.0.1)
- [x] Profile photo upload — base64 conversion, JSON payload, instant navbar update
- [x] Profile form submit handler added to `profile.js` (was missing entirely)
- [x] Photo preview on file select before saving
- [x] Success/error toast after profile save
- [x] Sidebar collapsed state persists on tab switch (re-applied after `renderTabs()`)
- [x] Dashboard quick actions widget visible (`#quickActionsContainer` div added)
- [x] Quick actions CSS — responsive grid, hover lift, theme color icon backgrounds

### 🗄️ Infrastructure (Session 15-16)
- [x] Aiven PostgreSQL fully migrated and operational
- [x] All sequences reset, role_permissions cleaned, demo data seeded
- [x] `schemas.py` SubscriptionStatus ordering fix
- [x] SSL connect_args fix for Aiven in `database.py`

### 📊 Current Version: 7.0.1 (Public: V3.0.1)

## 🔄 Updated Status (Session 16)

| Feature | Status |
|---------|--------|
| Profile photo upload fix | ✅ Done |
| Sidebar collapsed state on tab switch | ✅ Done |
| Dashboard quick actions widget | ✅ Done |
| Onboarding + paywall system | ✅ Done |
| Aiven database migration | ✅ Done |
| Stripe live mode activation | ⬜ Pending |
| Payment history page | ⬜ Pending |
| Real-time WebSockets for Queue | ⬜ Pending |
| SMS Notifications (Twilio) | ⬜ Pending |

## 🔜 Next Session (Session 17) — V3.1

### Planned:
- [ ] Add `STRIPE_PRICE_LITE`, `STRIPE_PRICE_PLUS`, `STRIPE_PRICE_PRO` to Render env vars
- [ ] Test full onboarding → trial → upgrade flow end-to-end on production
- [ ] Payment history page — all transactions with receipt download
- [ ] Refund processing via Stripe API
- [ ] Queue management real-time updates (polling improvement or WebSocket)
