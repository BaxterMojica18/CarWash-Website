# E-Commerce + Car Wash Service Queue: Implementation Specification

## Overview
Extend the existing car wash management system to support:
1. **Client role** - customers who can browse products/services, add to cart, place orders, and reserve car wash services
2. **Queue management** - FIFO queue system for car wash service reservations
3. **Order management** - owner/admin can accept/reject orders and update statuses

---

## Current System Architecture
- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL
- **Auth**: JWT tokens with role-based permissions
- **Existing Roles**: admin, owner, staff
- **Existing Models**: User, Role, Permission, Location, ProductService, Invoice, InvoiceItem

---

## New Role & Permissions

### Client Role
Add new role: `client` with permissions:
- `view_products` - Browse products and services
- `manage_cart` - Add/remove items from cart
- `place_order` - Create product orders
- `reserve_service` - Reserve car wash services
- `view_own_orders` - View own orders and reservations

### Updated Permission Matrix
| Permission | client | staff | owner | admin |
|------------|--------|-------|-------|-------|
| view_products | ✓ | ✓ | ✓ | ✓ |
| manage_cart | ✓ | - | - | - |
| place_order | ✓ | - | - | - |
| reserve_service | ✓ | - | - | - |
| view_own_orders | ✓ | - | - | - |
| manage_orders | - | - | ✓ | ✓ |
| manage_queue | - | - | ✓ | ✓ |

---

## Database Schema Changes

### New Tables

#### CartItem
```python
class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    product_service_id = Column(Integer, ForeignKey("products_services.id"))
    quantity = Column(Integer)
    price_at_add = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### Order
```python
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")  # pending, accepted, processing, completed, cancelled
    total_amount = Column(Float)
    payment_method = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    client = relationship("User")
    items = relationship("OrderItem", back_populates="order")
```

#### OrderItem
```python
class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_service_id = Column(Integer, ForeignKey("products_services.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    subtotal = Column(Float)
    
    order = relationship("Order", back_populates="items")
    product_service = relationship("ProductService")
```

#### Reservation
```python
class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    reservation_number = Column(String, unique=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("products_services.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    vehicle_plate = Column(String)
    status = Column(String, default="pending")  # pending, accepted, in_progress, completed, cancelled
    queue_position = Column(Integer, nullable=True)
    estimated_start_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    client = relationship("User")
    service = relationship("ProductService")
    location = relationship("Location")
```

---

## API Endpoints

### Cart Management (`/api/cart`)
- `GET /api/cart` - Get current user's cart items
- `POST /api/cart` - Add item to cart `{product_service_id, quantity}`
- `PATCH /api/cart/{item_id}` - Update quantity
- `DELETE /api/cart/{item_id}` - Remove item
- `DELETE /api/cart/clear` - Clear entire cart

### Orders (`/api/orders`)
- `POST /api/orders` - Create order from cart `{payment_method?}`
- `GET /api/orders` - List orders (client: own, owner/admin: all)
- `GET /api/orders/{id}` - Get order details
- `PATCH /api/orders/{id}/status` - Update status (owner/admin only) `{status}`

### Reservations (`/api/reservations`)
- `POST /api/reservations` - Create reservation `{service_id, location_id, vehicle_plate}`
- `GET /api/reservations` - List reservations (client: own, owner/admin: all)
- `GET /api/reservations/{id}` - Get reservation details
- `PATCH /api/reservations/{id}/status` - Update status (owner/admin only) `{status}`
- `GET /api/reservations/queue` - Get current queue (owner/admin)

### Client Dashboard (`/api/client`)
- `GET /api/client/dashboard` - Get client dashboard data (orders, reservations, queue position)

---

## Queue Management Logic

### Queue Position Assignment
1. When client creates reservation with `status="pending"`:
   - Calculate `queue_position = max(queue_position) + 1` for active reservations at same location
   - Active = status in ['pending', 'accepted', 'in_progress']
   - Return queue position and estimated wait time

2. Estimated wait time calculation:
   - `estimated_wait = (queue_position - 1) * service.duration_minutes`
   - Use service duration from ProductService table

3. When owner/admin accepts reservation (`status="accepted"`):
   - Keep queue position
   - Calculate `estimated_start_time = now + (position - 1) * duration`

4. When reservation moves to `in_progress`:
   - Keep current position
   - Notify client

5. When reservation completes or cancels:
   - Remove from queue
   - Decrement queue_position for all reservations behind it at same location
   - Use database transaction with row locking

---

## Pydantic Schemas

### Cart Schemas
```python
class CartItemCreate(BaseModel):
    product_service_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int

class CartItem(BaseModel):
    id: int
    product_service_id: int
    quantity: int
    price_at_add: float
    product_service: ProductService
```

### Order Schemas
```python
class OrderCreate(BaseModel):
    payment_method: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: str  # pending, accepted, processing, completed, cancelled

class OrderItem(BaseModel):
    id: int
    product_service_id: int
    quantity: int
    unit_price: float
    subtotal: float
    product_service: ProductService

class Order(BaseModel):
    id: int
    order_number: str
    client_id: int
    status: str
    total_amount: float
    payment_method: Optional[str]
    created_at: datetime
    items: List[OrderItem]
```

### Reservation Schemas
```python
class ReservationCreate(BaseModel):
    service_id: int
    location_id: int
    vehicle_plate: str

class ReservationStatusUpdate(BaseModel):
    status: str  # pending, accepted, in_progress, completed, cancelled

class Reservation(BaseModel):
    id: int
    reservation_number: str
    client_id: int
    service_id: int
    location_id: int
    vehicle_plate: str
    status: str
    queue_position: Optional[int]
    estimated_start_time: Optional[datetime]
    created_at: datetime
    service: ProductService
    location: Location

class ClientDashboard(BaseModel):
    active_orders: List[Order]
    order_history: List[Order]
    active_reservations: List[Reservation]
    reservation_history: List[Reservation]
```

---

## CRUD Operations

### Cart CRUD
- `get_cart_items(db, client_id)` - Get all cart items
- `add_to_cart(db, client_id, product_service_id, quantity)` - Add or update cart item
- `update_cart_item(db, item_id, quantity)` - Update quantity
- `remove_cart_item(db, item_id, client_id)` - Remove item
- `clear_cart(db, client_id)` - Clear all items

### Order CRUD
- `create_order_from_cart(db, client_id, payment_method)` - Create order, clear cart
- `get_orders(db, client_id=None)` - Get orders (filter by client if provided)
- `get_order(db, order_id)` - Get single order with items
- `update_order_status(db, order_id, status)` - Update order status

### Reservation CRUD
- `create_reservation(db, client_id, service_id, location_id, vehicle_plate)` - Create with queue position
- `get_reservations(db, client_id=None, location_id=None)` - Get reservations
- `get_reservation(db, reservation_id)` - Get single reservation
- `update_reservation_status(db, reservation_id, status)` - Update status and recompute queue
- `get_queue(db, location_id)` - Get active queue for location
- `recompute_queue_positions(db, location_id)` - Recalculate positions after completion/cancellation

---

## Frontend Pages

### Client Pages
1. **Shop/Catalog** (`/shop.html`)
   - Product grid with "Add to Cart" buttons
   - Service cards with "Reserve" buttons
   - Cart icon with item count

2. **Cart** (`/cart.html`)
   - List cart items with quantities
   - Update quantity or remove items
   - Show subtotal and total
   - "Checkout" button

3. **Service Reservation** (`/reserve.html`)
   - Select service and location
   - Enter vehicle plate
   - Show estimated wait time
   - "Reserve" button

4. **Client Dashboard** (`/client-dashboard.html`)
   - Active orders section
   - Order history
   - Active reservations with queue position
   - Reservation history

### Owner/Admin Pages
1. **Order Management** (`/order-management.html`)
   - List pending orders
   - Accept/reject orders
   - Update order status
   - View order details

2. **Queue Management** (`/queue-management.html`)
   - View current queue by location
   - Accept/reject reservations
   - Move reservations to in_progress
   - Complete reservations

---

## Implementation Steps

### Phase 1: Database & Models
1. Add new models to `app/database.py`: CartItem, Order, OrderItem, Reservation
2. Create migration script to add tables
3. Update `seed_data.py` to add client role and new permissions

### Phase 2: Backend - Cart & Orders
1. Create `app/routers/cart.py` with cart endpoints
2. Create `app/routers/orders.py` with order endpoints
3. Add CRUD functions to `app/crud.py`
4. Add schemas to `app/schemas.py`

### Phase 3: Backend - Reservations & Queue
1. Create `app/routers/reservations.py` with reservation endpoints
2. Add queue management logic to CRUD
3. Add client dashboard endpoint

### Phase 4: Frontend - Client Views
1. Create `frontend/shop.html` - product/service catalog
2. Create `frontend/cart.html` - shopping cart
3. Create `frontend/reserve.html` - service reservation
4. Create `frontend/client-dashboard.html` - client dashboard
5. Add JS files: `cart.js`, `orders.js`, `reservations.js`, `client-dashboard.js`

### Phase 5: Frontend - Owner/Admin Views
1. Create `frontend/order-management.html`
2. Create `frontend/queue-management.html`
3. Add JS files: `order-management.js`, `queue-management.js`

### Phase 6: Testing & Polish
1. Test cart flow
2. Test order creation and status updates
3. Test reservation and queue management
4. Test permissions and role access
5. Add error handling and validation

---

## Acceptance Criteria

### Cart Functionality
- ✓ Client can add products to cart
- ✓ Cart persists across sessions
- ✓ Client can update quantities
- ✓ Client can remove items
- ✓ Cart shows correct totals

### Order Functionality
- ✓ Client can checkout and create order
- ✓ Order gets unique order number (ORD-YYYYMMDDHHMMSS)
- ✓ Cart clears after order creation
- ✓ Owner/admin can view all orders
- ✓ Owner/admin can update order status
- ✓ Client can view own orders

### Reservation & Queue
- ✓ Client can reserve service with vehicle plate
- ✓ Reservation gets unique number (RES-YYYYMMDDHHMMSS)
- ✓ Queue position assigned correctly (FIFO)
- ✓ Estimated wait time calculated
- ✓ Owner/admin can accept/reject reservations
- ✓ Queue positions update when reservation completes/cancels
- ✓ Client sees current queue position in dashboard

### Permissions
- ✓ Client role has correct permissions
- ✓ Client can only see own orders/reservations
- ✓ Owner/admin can see all orders/reservations
- ✓ Unauthorized access returns 403

---

## Notes
- Use existing JWT authentication system
- Follow existing code patterns (FastAPI routers, SQLAlchemy models, Pydantic schemas)
- Reuse existing permission system with `has_permission()` decorator
- Use existing soft delete pattern (status + deleted_at)
- Generate order/reservation numbers similar to invoice numbers
- Use database transactions for queue position updates to prevent race conditions
