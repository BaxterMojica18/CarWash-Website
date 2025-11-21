# E-Commerce Feature Setup Guide

## Overview
This guide will help you set up the new e-commerce features including shopping cart, orders, and service reservations with queue management.

## New Features Added

### For Clients (Customers)
- 🛒 **Shopping Cart** - Add products to cart and checkout
- 📦 **Order Management** - Place orders and track status
- 🚗 **Service Reservations** - Reserve car wash services with queue position
- 📊 **Client Dashboard** - View active orders, reservations, and history

### For Owner/Admin
- 📋 **Order Management** - Accept/reject orders and update status
- 🎯 **Queue Management** - Manage service reservations and queue
- 👥 **Client Role** - New role for customers with appropriate permissions

## Setup Instructions

### Step 1: Create New Database Tables
Run the migration script to add the new tables:
```bash
python add_ecommerce_tables.py
```

This will create:
- `cart_items` - Shopping cart storage
- `orders` - Customer orders
- `order_items` - Order line items
- `reservations` - Service reservations with queue

### Step 2: Update Roles and Permissions
Run the seed data script to add the client role and new permissions:
```bash
python seed_data.py
```

This will add:
- **Client role** with permissions:
  - view_products
  - manage_cart
  - place_order
  - reserve_service
  - view_own_orders

- **New permissions** for owner/admin:
  - manage_orders
  - manage_queue

### Step 3: Start the Server
```bash
start_server.bat
```

## New API Endpoints

### Cart Endpoints
- `GET /api/cart` - Get cart items
- `POST /api/cart` - Add item to cart
- `PATCH /api/cart/{item_id}` - Update quantity
- `DELETE /api/cart/{item_id}` - Remove item
- `DELETE /api/cart/clear/all` - Clear cart

### Order Endpoints
- `POST /api/orders` - Create order from cart
- `GET /api/orders` - List orders
- `GET /api/orders/{id}` - Get order details
- `PATCH /api/orders/{id}/status` - Update order status (owner/admin)

### Reservation Endpoints
- `POST /api/reservations` - Create reservation
- `GET /api/reservations` - List reservations
- `GET /api/reservations/queue?location_id={id}` - Get queue (owner/admin)
- `GET /api/reservations/{id}` - Get reservation details
- `PATCH /api/reservations/{id}/status` - Update status (owner/admin)

### Client Dashboard
- `GET /api/client/dashboard` - Get client dashboard data

## New Frontend Pages

### Client Pages
- `/shop.html` - Browse products and services
- `/cart.html` - Shopping cart
- `/reserve.html` - Reserve car wash service
- `/client-dashboard.html` - Client dashboard

### Owner/Admin Pages
- `/order-management.html` - Manage customer orders
- `/queue-management.html` - Manage service queue

## Testing the Features

### 1. Create a Test Client User
You can create a client user through the API or database:

```python
# Using Python
from app.database import SessionLocal
from app import crud, database

db = SessionLocal()

# Create client user
client = crud.create_user(db, "client@test.com", "client123", is_demo=False)

# Assign client role
client_role = db.query(database.Role).filter(database.Role.name == "client").first()
if client_role:
    client.roles.append(client_role)
    db.commit()

print("Client user created!")
print("Email: client@test.com")
print("Password: client123")
```

### 2. Test Shopping Flow
1. Login as client user
2. Go to `/shop.html`
3. Add products to cart
4. Go to `/cart.html`
5. Checkout to create order
6. View order in `/client-dashboard.html`

### 3. Test Reservation Flow
1. Login as client user
2. Go to `/shop.html`
3. Click "Reserve" on a service
4. Fill in vehicle plate and location
5. Submit reservation
6. View queue position in `/client-dashboard.html`

### 4. Test Order Management (Owner/Admin)
1. Login as owner or admin
2. Go to `/order-management.html`
3. View pending orders
4. Accept/reject orders
5. Update order status

### 5. Test Queue Management (Owner/Admin)
1. Login as owner or admin
2. Go to `/queue-management.html`
3. Select location
4. View active queue
5. Accept reservations
6. Move to in_progress
7. Complete reservations

## Queue Management Logic

### How Queue Works
1. **Client creates reservation** → Assigned next queue position at selected location
2. **Owner accepts** → Reservation stays in queue with same position
3. **Owner starts service** → Status changes to "in_progress"
4. **Owner completes** → Removed from queue, all positions behind it shift down by 1
5. **Client cancels** → Removed from queue, positions recalculated

### Queue Position Calculation
- Queue position is per location
- Only active reservations (pending, accepted, in_progress) have queue positions
- Position 1 = next to be served
- Estimated wait time = (position - 1) × service duration

## Order Status Flow

### Product Orders
1. **pending** - Order placed, awaiting acceptance
2. **accepted** - Order accepted by owner/admin
3. **processing** - Order being prepared
4. **completed** - Order fulfilled
5. **cancelled** - Order cancelled

### Service Reservations
1. **pending** - Reservation created, awaiting acceptance
2. **accepted** - Reservation accepted, in queue
3. **in_progress** - Service currently being performed
4. **completed** - Service completed
5. **cancelled** - Reservation cancelled

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Tables not created
- Make sure PostgreSQL is running
- Check DATABASE_URL in .env file
- Run `python add_ecommerce_tables.py` again

### Permissions not working
- Run `python seed_data.py` to update roles and permissions
- Check user roles in database
- Verify JWT token includes correct permissions

### Queue positions not updating
- Check database transactions are committing
- Verify location_id is correct
- Check reservation status is in active states

## Next Steps

### Recommended Enhancements
- [ ] Add email notifications for order status changes
- [ ] Add real-time WebSocket updates for queue positions
- [ ] Add payment gateway integration
- [ ] Add customer profiles with saved vehicles
- [ ] Add service duration estimates
- [ ] Add SMS notifications for queue updates
- [ ] Add rating/review system
- [ ] Add loyalty points system

## Support

For issues or questions, check:
1. Server logs for errors
2. Browser console for frontend errors
3. API documentation at `/docs`
4. Database connection and tables
