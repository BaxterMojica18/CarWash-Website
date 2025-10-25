# Car Wash Management System

A full-stack web application for managing car wash operations with dashboard, invoicing, and settings management.

## Tech Stack

- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Frontend**: HTML/CSS/JS (Next.js coming soon)

## Features

- ✅ User Authentication (Demo & Admin accounts)
- ✅ Dashboard with stats and reports
- ✅ Invoice creation and PDF generation
- ✅ Manage washing bays (locations)
- ✅ Manage products and services
- ✅ Sales reports with filtering (day/month/year)
- ✅ Export reports as PDF or CSV
- ✅ Demo account for testing

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

### Demo Account
- Email: `demo@carwash.com`
- Password: `demo123`

### Admin Account
- Email: `admin@carwash.com`
- Password: `admin123`

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

## Next Steps

- [ ] Build Next.js frontend
- [ ] Deploy to Vercel/Netlify
- [ ] Add more dashboard charts
- [ ] Email invoice receipts
- [ ] Customer management
