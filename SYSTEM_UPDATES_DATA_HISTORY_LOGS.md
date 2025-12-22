# System Updates, Data & History Logs

> **Last Updated:** November 23, 2025  
> **Version:** 2.0.0  
> **Branch:** update/dynamicdashboardupdate11232025

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

## Latest Updates (Nov 23, 2025)

### 🎨 Dynamic Dashboard Customization
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
