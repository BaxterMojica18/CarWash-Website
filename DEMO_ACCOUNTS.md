# 🎮 Demo Accounts Guide

## Overview

Three demo accounts are available for users to explore the system from different perspectives. Each account has **limited permissions** to prevent abuse while allowing full exploration of features.

## 📋 Demo Account Credentials

### 1. 👤 Client Perspective
```
Email: demo-client@carwash.com
Password: demo123
```

**What you can do:**
- Browse products and services
- Add items to cart
- Place orders (max 10)
- Make service reservations (max 10)
- View your order history
- Track reservation status

**Limits:**
- Maximum 10 orders
- Maximum 10 reservations

---

### 2. 👔 Staff Perspective
```
Email: demo-staff@carwash.com
Password: demo123
```

**What you can do:**
- Create invoices (max 10)
- View sales reports
- View dashboard statistics
- Access limited admin features

**Limits:**
- Maximum 10 invoices created
- Cannot add/edit products or services
- Cannot manage users
- Cannot change settings

---

### 3. 👨‍💼 Admin Perspective (Limited)
```
Email: demo-admin@carwash.com
Password: demo123
```

**What you can do:**
- Create invoices (max 10)
- View sales reports
- View dashboard statistics
- Limited product management

**Limits:**
- Maximum 1 product can be created
- Maximum 1 service can be created
- Maximum 10 invoices
- Cannot manage users
- Cannot change critical settings

---

## 🚀 Quick Start

### Step 1: Create Demo Accounts
```bash
python create_demo_users.py
# or
create_demo_users.bat
```

### Step 2: Start Server
```bash
start_server.bat
```

### Step 3: Login
```
http://localhost:8000/login.html
```

Use any of the demo credentials above.

---

## 🎯 Usage Scenarios

### Scenario 1: Test Client Shopping Experience
1. Login as `demo-client@carwash.com`
2. Go to Shop page
3. Add products to cart
4. Checkout and place order
5. View order in client dashboard

### Scenario 2: Test Staff Invoice Creation
1. Login as `demo-staff@carwash.com`
2. Go to Invoices page
3. Create new invoice
4. View reports

### Scenario 3: Test Admin Features
1. Login as `demo-admin@carwash.com`
2. Access dashboard
3. View reports
4. Create limited products/services

---

## ⚠️ Important Notes

### Limits Enforcement
- Limits are enforced at the **backend API level**
- When limit is reached, you'll see: `"Demo account limit reached"`
- Limits reset only by database admin

### What Happens at Limit?
```
❌ "Demo account limit reached: Maximum 10 orders allowed"
❌ "Demo account limit reached: Maximum 1 product allowed"
```

### Current Usage
Check your usage via API:
```bash
GET /api/auth/me/demo-limits
```

---

## 🔧 Technical Details

### Database Table: `demo_usage_limits`
```sql
CREATE TABLE demo_usage_limits (
    user_id INTEGER PRIMARY KEY,
    products_created INTEGER DEFAULT 0,
    services_created INTEGER DEFAULT 0,
    orders_created INTEGER DEFAULT 0,
    reservations_created INTEGER DEFAULT 0,
    max_products INTEGER DEFAULT 1,
    max_services INTEGER DEFAULT 1,
    max_orders INTEGER DEFAULT 10,
    max_reservations INTEGER DEFAULT 10
);
```

### Enforcement Points
- **Products/Services:** `POST /api/settings/products`
- **Orders:** `POST /api/orders/`
- **Reservations:** `POST /api/reservations/`

### Middleware: `app/demo_limits.py`
```python
DemoLimits.check_limit(db, user, "orders")  # Check before action
DemoLimits.increment_usage(db, user, "orders")  # Increment after success
```

---

## 📊 Comparison Table

| Feature | Client | Staff | Admin (Limited) |
|---------|--------|-------|-----------------|
| Shop Products | ✅ | ❌ | ❌ |
| Place Orders | ✅ (10 max) | ❌ | ❌ |
| Make Reservations | ✅ (10 max) | ❌ | ❌ |
| Create Invoices | ❌ | ✅ (10 max) | ✅ (10 max) |
| View Reports | ❌ | ✅ | ✅ |
| Add Products | ❌ | ❌ | ✅ (1 max) |
| Add Services | ❌ | ❌ | ✅ (1 max) |
| Manage Users | ❌ | ❌ | ❌ |
| Change Settings | ❌ | ❌ | ❌ |

---

## 🔄 Reset Demo Accounts

### Reset Usage Counters
```sql
UPDATE demo_usage_limits 
SET products_created = 0, 
    services_created = 0, 
    orders_created = 0, 
    reservations_created = 0;
```

### Delete Demo Data
```sql
-- Delete orders from demo users
DELETE FROM orders WHERE client_id IN (
    SELECT id FROM users WHERE email LIKE 'demo-%@carwash.com'
);

-- Delete reservations from demo users
DELETE FROM reservations WHERE client_id IN (
    SELECT id FROM users WHERE email LIKE 'demo-%@carwash.com'
);

-- Reset counters
UPDATE demo_usage_limits SET 
    products_created = 0, 
    services_created = 0, 
    orders_created = 0, 
    reservations_created = 0;
```

---

## 🎨 UI Indicators

### Show Remaining Limits (Optional Enhancement)
```javascript
// In frontend, show remaining usage
fetch('/api/auth/me/demo-limits')
    .then(r => r.json())
    .then(data => {
        console.log(`Orders: ${data.orders.used}/${data.orders.max}`);
    });
```

### Display Warning
```
⚠️ Demo Account: 7/10 orders used
```

---

## 🛡️ Security Features

### What's Protected:
- ✅ Backend API validation
- ✅ Database constraints
- ✅ Real-time limit checking
- ✅ Automatic counter increment

### What's NOT Protected:
- ❌ Direct database manipulation
- ❌ Admin account bypass

---

## 📞 Support

### Common Issues

**Issue: "Demo account limit reached"**
- You've hit the maximum allowed actions
- Contact admin to reset counters
- Or wait for scheduled reset

**Issue: Can't create products**
- Demo-admin can only create 1 product and 1 service
- This is intentional to prevent abuse

**Issue: Can't access certain pages**
- Each demo account has different permissions
- Try logging in with different demo account

---

## ✅ Setup Checklist

- [ ] Run `python create_demo_users.py`
- [ ] Verify demo accounts created
- [ ] Test login with each account
- [ ] Verify limits are enforced
- [ ] Test limit reached error messages

---

## 🎉 Ready to Test!

All demo accounts are now set up with appropriate limits. Users can explore the system safely without breaking anything!

**Next Steps:**
1. Share demo credentials with testers
2. Monitor usage via database
3. Reset limits as needed
4. Collect feedback
