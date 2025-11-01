# User Permissions System

## Overview
Role-based permission system with three user roles: **Admin**, **Owner**, and **User**.

## Roles & Permissions

### Admin & Owner (Full Access)
- ✅ Manage products/services (add, edit, delete)
- ✅ Manage locations (add, edit, delete)
- ✅ Manage invoices (create, view, edit)
- ✅ View reports
- ✅ Manage settings (theme, customization)
- ✅ Manage user permissions

### User (Limited Access)
- ✅ Manage invoices (create, view)
- ✅ View reports
- ❌ Cannot manage products/services
- ❌ Cannot manage locations
- ❌ Cannot manage settings/theme
- ❌ Cannot manage user permissions

## Setup Instructions

### 1. Run Permission Migration
```bash
python add_permissions.py
```

This creates:
- `roles` table (admin, owner, user)
- `permissions` table (6 permissions)
- `role_permissions` mapping
- `user_roles` mapping

### 2. Assign Roles to Existing Users

```python
from app.database import SessionLocal, User, Role
from sqlalchemy import text

db = SessionLocal()

# Assign admin role to admin user
admin_user = db.query(User).filter(User.email == "admin@carwash.com").first()
admin_role = db.query(Role).filter(Role.name == "admin").first()
if admin_user and admin_role:
    admin_user.roles.append(admin_role)

# Assign user role to demo user
demo_user = db.query(User).filter(User.email == "demo@carwash.com").first()
user_role = db.query(Role).filter(Role.name == "user").first()
if demo_user and user_role:
    demo_user.roles.append(user_role)

db.commit()
db.close()
```

### 3. Update Frontend Pages

Add permission checks to HTML pages by including:

```html
<script src="js/permissions.js"></script>
<script>
    // Hide elements based on permissions
    document.addEventListener('DOMContentLoaded', () => {
        permissionManager.hideElementsWithoutPermission();
    });
</script>
```

Mark elements with permission attributes:
```html
<!-- Only visible to users with manage_products permission -->
<button data-permission="manage_products" onclick="addProduct()">Add Product</button>

<!-- Only visible to users with manage_settings permission -->
<div data-permission="manage_settings">
    <h2>Theme Settings</h2>
    <!-- theme customization UI -->
</div>
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Returns permissions in response
- `GET /api/auth/me/permissions` - Get current user permissions
- `GET /api/auth/users` - List all users (admin/owner only)
- `PUT /api/auth/users/roles` - Update user roles (admin/owner only)

### Protected Endpoints
All endpoints now check permissions:
- Products: `manage_products`
- Locations: `manage_locations`
- Invoices: `manage_invoices`
- Reports: `view_reports`
- Settings: `manage_settings`

## Frontend Integration

### Login Flow
```javascript
const response = await API.auth.login(email, password);
localStorage.setItem('user_permissions', JSON.stringify(response.permissions));
```

### Check Permissions
```javascript
if (permissionManager.canManageProducts()) {
    // Show product management UI
}

if (!permissionManager.canManageSettings()) {
    // Hide settings menu
}
```

## User Management UI

Access at: `/users.html` (admin/owner only)

Features:
- View all users with their roles and permissions
- Edit user roles
- Assign multiple roles to users

## Testing

### Test as Admin
```
Email: admin@carwash.com
Password: admin123
Expected: Full access to all features
```

### Test as User
```
Email: demo@carwash.com
Password: demo123
Expected: Limited access (no products/settings management)
```

## Database Schema

```sql
-- Roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE,
    description VARCHAR
);

-- Permissions table
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE,
    description VARCHAR
);

-- Role-Permission mapping
CREATE TABLE role_permissions (
    role_id INTEGER REFERENCES roles(id),
    permission_id INTEGER REFERENCES permissions(id)
);

-- User-Role mapping
CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id),
    role_id INTEGER REFERENCES roles(id)
);
```

## Permission List

1. `manage_products` - Add, edit, delete products/services
2. `manage_locations` - Add, edit, delete washing bays
3. `manage_invoices` - Create, edit invoices
4. `view_reports` - View sales reports
5. `manage_settings` - Manage theme and customization
6. `manage_users` - Manage user permissions

## Notes

- Users can have multiple roles
- Permissions are cumulative (union of all role permissions)
- Frontend hides UI elements without permission
- Backend enforces permission checks on API calls
- 403 error returned when permission denied
