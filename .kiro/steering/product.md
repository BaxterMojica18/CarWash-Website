# Product Overview

Car Wash Management System — a multi-tenant SaaS platform for car wash businesses. Owners register a business, get a business code, and staff/clients join using that code.

## Core Capabilities

- **Multi-tenant business system**: Data isolation via `business_number`. Each business sees only its own data.
- **Role-based access**: Superadmin → Owner → Admin → Staff → Client. Granular permissions and per-user sidebar visibility.
- **E-commerce**: Product/service catalog, shopping cart, order management with status flow (pending → accepted → processing → completed).
- **Reservations**: FIFO queue system for car wash services with real-time queue position tracking.
- **Invoicing**: Create invoices, generate PDFs, track status.
- **Payments**: Stripe integration (PaymentIntent + webhooks), plus cash/QR payment methods.
- **Coupons & Flash Sales**: Discount codes and time-limited promotions.
- **Dashboard**: Customizable modules, revenue charts, sales reports with CSV/PDF export.
- **Authentication**: Email/password with JWT, Google Sign-In via Firebase, password reset (link or OTP).
- **Email notifications**: Async transactional emails via Resend API for order/reservation status changes.
- **Theming**: Custom color themes for both staff and client-facing interfaces.

## Deployment

- Frontend: Vercel (static HTML/CSS/JS)
- Backend API: Render (Docker)
- Database: PostgreSQL on Render
- Auth provider: Firebase (Google login)
