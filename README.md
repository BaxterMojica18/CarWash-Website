# Car Wash Management System

A full-stack web application for managing car wash operations with dashboard, invoicing, and settings management.

## Tech Stack

- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Frontend**: HTML/CSS/JS (Next.js coming soon)

## Features

### Core Features
- ✅ User Authentication (Demo & Admin accounts)
- ✅ Dashboard with stats and reports
- ✅ Invoice creation and PDF generation
- ✅ Manage washing bays (locations)
- ✅ Manage products and services
- ✅ Sales reports with filtering (day/month/year)
- ✅ Export reports as PDF or CSV
- ✅ Demo account for testing

### E-Commerce Features (NEW!)
- ✅ Shopping cart for products
- ✅ Order management system
- ✅ Service reservation with queue
- ✅ Client dashboard
- ✅ Queue management for owner/admin
- ✅ Order status tracking
- ✅ FIFO queue system for car wash services

### Permissions Management (NEW!)
- ✅ Role-based access control (RBAC)
- ✅ 6 granular permissions (products, locations, invoices, reports, settings, users)
- ✅ Visual permissions management UI
- ✅ Real-time permission toggling
- ✅ Search and filter users
- ✅ Admin/Owner dashboard for user management

## Security Best Practices

**Before deploying to production:**
1. Change all default passwords in the database
2. Generate a strong `SECRET_KEY` in your `.env` file
3. Use environment variables for all sensitive data
4. Never commit `.env` files to version control
5. Enable HTTPS/SSL for production deployments
6. Use strong, unique passwords for database access

## Setup Instructions

### Option 1: Docker Setup (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd car-wash-website

# Start with Docker Compose
docker-compose up -d

# Access the application at http://localhost:8000
```

### Option 2: Local Setup

#### 1. Database Setup

```bash
# Create the database
python create_db.py

# Create tables and seed data
python seed_data.py
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment

```bash
# Copy .env.example to .env and update with your settings
cp .env.example .env
```

#### 4. Start the Server

```bash
# Windows
start_server.bat

# Or manually
uvicorn app.main:app --reload --port 8000
```

#### 5. Test the API

```bash
python test_api.py
```

## Login Credentials

> **⚠️ SECURITY NOTE:** These are demo/test credentials for development only. 
> Never use these passwords in production. Change all default passwords before deploying.

### Demo Account (Development Only)
- Email: `demo@carwash.com`
- Password: `demo123`

### Superadmin Account (Development Only)
- Email: `owner@carwash.com`
- Password: `owner123`
- Note: Run `python create_superadmin.py` to create this account

### Admin Account (Development Only)
- Email: `admin@carwash.com`
- Password: `admin123`

### Demo Accounts (For Testing)
- **Client:** `demo-client@carwash.com` / `demo123` (10 orders, 10 reservations max)
- **Staff:** `demo-staff@carwash.com` / `demo123` (10 invoices max)
- **Admin:** `demo-admin@carwash.com` / `demo123` (1 product, 1 service, 10 invoices max)
- Note: Run `python create_demo_users.py` to create these accounts

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/demo-login` - Quick demo login

### Settings
- `GET /api/settings/locations` - Get all washing bays
- `POST /api/settings/locations` - Create new location
- `PUT /api/settings/locations/{id}` - Update location
- `DELETE /api/settings/locations/{id}` - Delete location
- `GET /api/settings/products` - Get all products/services
- `POST /api/settings/products` - Create new product
- `PUT /api/settings/products/{id}` - Update product
- `DELETE /api/settings/products/{id}` - Delete product

### Invoices
- `POST /api/invoices/` - Create new invoice
- `GET /api/invoices/` - Get all invoices
- `GET /api/invoices/{id}` - Get specific invoice
- `GET /api/invoices/{id}/pdf` - Download invoice as PDF
- `GET /api/invoices/dashboard/stats` - Get dashboard statistics

### Reports
- `GET /api/reports/sales` - Get sales report with filters (period, date, month, year)
- `GET /api/reports/sales/download/csv` - Download sales report as CSV
- `GET /api/reports/sales/download/pdf` - Download sales report as PDF

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Schema

### Users
- id, email, password_hash, is_demo

### Locations (Washing Bays)
- id, name, address

### ProductService
- id, name, price, description, type

### Invoice
- id, invoice_number, date, customer_name, total_amount, location_id, user_id

### InvoiceItem
- id, invoice_id, product_service_id, quantity, unit_price, subtotal

## E-Commerce Setup

To enable the new e-commerce features:

```bash
# 1. Create new database tables
python add_ecommerce_tables.py

# 2. Update roles and permissions
python seed_data.py

# 3. Create test client user
python create_client_user.py

# 4. Start the server
start_server.bat
```

See [ECOMMERCE_SETUP.md](ECOMMERCE_SETUP.md) for detailed documentation.

## New Pages

### Client Pages
- `/shop.html` - Browse and shop products/services
- `/cart.html` - Shopping cart
- `/reserve.html` - Reserve car wash service
- `/client-dashboard.html` - View orders and reservations

### Owner/Admin Pages
- `/order-management.html` - Manage customer orders
- `/queue-management.html` - Manage service queue
- `/permissions-management.html` - Manage user permissions (Admin/Owner only)

## Next Steps

- [ ] Add email notifications for orders
- [ ] Add real-time WebSocket for queue updates
- [ ] Add payment gateway integration
- [ ] Build Next.js frontend
- [ ] Deploy to Vercel/Netlify
- [ ] Add more dashboard charts
- [ ] Customer profiles with saved vehicles
