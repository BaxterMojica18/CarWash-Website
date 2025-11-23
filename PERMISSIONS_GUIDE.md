# Permissions Management Guide

## Overview

The Car Wash Management System includes a comprehensive role-based access control (RBAC) system that allows admin and owner users to manage permissions for all users in the system.

## Accessing Permissions Management

### For Admin/Owner Users:
1. Log in with an admin or owner account
2. Navigate to **Settings** page
3. Click on **🔐 Manage Permissions** button in the User Management section
4. Or directly access: `http://localhost:8000/permissions-management.html`

### Direct Link:
- The permissions management page is available at: `/permissions-management.html`
- Only accessible to users with `admin` or `owner` roles

## Available Permissions

The system includes 6 core permissions:

| Permission | Description | Default Roles |
|------------|-------------|---------------|
| `manage_products` | Add, edit, and delete products | Admin, Owner |
| `manage_locations` | Add, edit, and delete washing bays | Admin, Owner |
| `manage_invoices` | Create, edit, and delete invoices | Admin, Owner, User |
| `view_reports` | Access sales reports and analytics | Admin, Owner, User |
| `manage_settings` | Modify theme and business settings | Admin, Owner |
| `manage_users` | Manage user accounts and permissions | Admin, Owner |

## User Roles

### Predefined Roles:

1. **Admin** - Full system access with all permissions
2. **Owner** - Full system access with all permissions
3. **User** - Limited access (invoices and reports only)
4. **Client** - Customer-facing features (shop, cart, reservations)

### Custom Permissions:
- Admin/Owner can grant individual permissions to any user
- Custom permissions override role-based permissions
- Each user can have a unique combination of permissions

## Using the Permissions Management Page

### Features:

1. **User Statistics Dashboard**
   - Total users count
   - Admin users count
   - Staff users count

2. **Search and Filter**
   - Search users by email
   - Filter by role (Admin, Owner, User, Client)
   - Real-time filtering

3. **Permission Toggle**
   - Each user card shows all 6 permissions
   - Toggle switches to enable/disable permissions
   - Changes are saved immediately
   - Visual feedback with toast notifications

4. **User Cards Display**
   - User email
   - Current roles (badges)
   - All permissions with descriptions
   - Toggle switches for each permission

### How to Manage Permissions:

1. **Search for a User**
   ```
   Type the user's email in the search box
   ```

2. **Toggle Permissions**
   ```
   Click the toggle switch next to any permission
   Green = Enabled
   Gray = Disabled
   ```

3. **View Permission Details**
   ```
   Each permission shows:
   - Permission name
   - Description of what it allows
   - Current status (enabled/disabled)
   ```

## API Endpoints

### Get All Users with Permissions
```http
GET /api/auth/users
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "user_id": 1,
    "email": "admin@carwash.com",
    "roles": ["admin"],
    "permissions": ["manage_products", "manage_locations", ...]
  }
]
```

### Get All Available Permissions
```http
GET /api/auth/permissions/all
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "name": "manage_products",
    "description": "Add, edit, delete products/services"
  }
]
```

### Get All Roles
```http
GET /api/auth/roles/all
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "name": "admin",
    "description": "Full system access",
    "permissions": ["manage_products", "manage_locations", ...]
  }
]
```

### Update User Permissions
```http
PUT /api/auth/users/permissions
Authorization: Bearer {token}
Content-Type: application/json

{
  "user_id": 5,
  "permissions": ["manage_invoices", "view_reports"]
}
```

### Update User Roles
```http
PUT /api/auth/users/roles
Authorization: Bearer {token}
Content-Type: application/json

{
  "user_id": 5,
  "roles": ["user"]
}
```

## Frontend Implementation

### Permission Checking in JavaScript

```javascript
// Check if user has permission
const permissionManager = new PermissionManager();
if (permissionManager.canManageProducts()) {
    // Show product management UI
}

// Hide elements without permission
permissionManager.hideElementsWithoutPermission();
```

### HTML Data Attributes

```html
<!-- This button will be hidden if user lacks permission -->
<button data-permission="manage_products">Add Product</button>
```

## Security Best Practices

1. **Always verify permissions on the backend**
   - Frontend checks are for UX only
   - Backend enforces actual security

2. **Use the `has_permission` decorator**
   ```python
   @router.post("/products")
   def create_product(
       product: ProductServiceCreate,
       current_user = Depends(has_permission("manage_products"))
   ):
       # Only users with manage_products permission can access
   ```

3. **Check user roles**
   ```python
   @router.get("/admin-only")
   def admin_endpoint(
       current_user = Depends(is_admin_or_owner)
   ):
       # Only admin/owner can access
   ```

## Database Schema

### Tables:

1. **users** - User accounts
2. **roles** - Role definitions
3. **permissions** - Permission definitions
4. **user_roles** - Many-to-many relationship
5. **role_permissions** - Many-to-many relationship

### Relationships:

```
User ←→ user_roles ←→ Role ←→ role_permissions ←→ Permission
```

## Setup Instructions

### 1. Initialize Permissions System

```bash
python add_permissions.py
```

This creates:
- All 6 permissions
- 3 default roles (admin, owner, user)
- Role-permission assignments

### 2. Assign Roles to Users

```bash
python assign_user_roles.py
```

Or use the API:
```bash
python test_permissions.py
```

### 3. Access the UI

1. Log in as admin/owner
2. Go to Settings → Manage Permissions
3. Toggle permissions for any user

## Troubleshooting

### Issue: Permissions not showing
**Solution:** Run `python add_permissions.py` to initialize the system

### Issue: User can't access permissions page
**Solution:** Ensure user has `admin` or `owner` role

### Issue: Permission changes not taking effect
**Solution:** 
1. Clear browser cache
2. Log out and log back in
3. Check backend logs for errors

### Issue: Custom permissions not working
**Solution:** Verify the permission exists in the database:
```sql
SELECT * FROM permissions;
```

## Future Enhancements

- [ ] Role templates for quick assignment
- [ ] Permission groups/categories
- [ ] Audit log for permission changes
- [ ] Bulk permission updates
- [ ] Permission inheritance
- [ ] Time-based permissions (temporary access)
- [ ] IP-based restrictions
- [ ] Two-factor authentication for sensitive permissions

## Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review backend logs
3. Test with `test_permissions.py`
4. Verify database schema with `python -c "from app.database import *; create_tables()"`
