# 🔐 Superadmin Role Guide

## Overview

The **superadmin** role is the highest level of access in the system. It has complete control over all users, including admins.

## Hierarchy

```
superadmin (owner)
    ↓
admin
    ↓
user (staff)
    ↓
client
```

## Superadmin Account

**Credentials:**
```
Email: owner@carwash.com
Password: owner123
```

**Setup:**
```bash
python create_superadmin.py
# or
create_superadmin.bat
```

## Key Features

### 1. Full User Management
- ✅ Can see ALL users including admins
- ✅ Can modify admin permissions
- ✅ Can create/delete any user
- ✅ Can assign any role

### 2. Visibility Control
- ✅ Superadmin users are HIDDEN from admin view
- ✅ Only superadmin can see other superadmins
- ✅ Admins cannot modify superadmin accounts

### 3. Complete System Access
- ✅ All permissions granted
- ✅ Access to all features
- ✅ No restrictions

## Differences from Admin

| Feature | Superadmin | Admin |
|---------|-----------|-------|
| See all users | ✅ Yes | ⚠️ No (can't see superadmins) |
| Manage admins | ✅ Yes | ❌ No |
| Manage superadmins | ✅ Yes | ❌ No (can't even see them) |
| Full system access | ✅ Yes | ✅ Yes |
| Hidden from lower roles | ✅ Yes | ❌ No |

## User Management Visibility

### What Superadmin Sees:
```
- owner@carwash.com (superadmin) ← Can see this
- admin@carwash.com (admin)
- staff@carwash.com (user)
- client@carwash.com (client)
```

### What Admin Sees:
```
- admin@carwash.com (admin)
- staff@carwash.com (user)
- client@carwash.com (client)
(Superadmin users are hidden)
```

### What Staff Sees:
```
(No user management access)
```

## Settings Page Access

### Superadmin:
- ✅ Can see "User Management" section
- ✅ Can access "Manage Permissions"
- ✅ Can see all users

### Admin:
- ✅ Can see "User Management" section
- ✅ Can access "Manage Permissions"
- ⚠️ Cannot see superadmin users

### Staff:
- ❌ Cannot see "User Management" section
- ❌ Cannot access "Manage Permissions"

## API Endpoints

### List Users (Filtered)
```http
GET /api/auth/users
Authorization: Bearer {token}
```

**Superadmin Response:**
```json
[
  {"email": "owner@carwash.com", "roles": ["superadmin"]},
  {"email": "admin@carwash.com", "roles": ["admin"]},
  {"email": "staff@carwash.com", "roles": ["user"]}
]
```

**Admin Response:**
```json
[
  {"email": "admin@carwash.com", "roles": ["admin"]},
  {"email": "staff@carwash.com", "roles": ["user"]}
]
```
(Superadmin users filtered out)

## Security Implementation

### Backend Filter:
```python
@router.get("/users")
def list_users(current_user = Depends(is_admin_or_owner)):
    users = db.query(User).all()
    current_user_roles = [role.name for role in current_user.roles]
    is_superadmin_user = "superadmin" in current_user_roles
    
    result = []
    for user in users:
        user_roles = [role.name for role in user.roles]
        
        # Hide superadmin from non-superadmin
        if "superadmin" in user_roles and not is_superadmin_user:
            continue
        
        result.append(user)
    return result
```

### Frontend Check:
```javascript
// Only show user management to admin/superadmin
if (roles.includes('admin') || roles.includes('superadmin')) {
    showUserManagement();
}
```

## Setup Instructions

### Step 1: Create Superadmin
```bash
python create_superadmin.py
```

### Step 2: Login
```
Email: owner@carwash.com
Password: owner123
```

### Step 3: Verify Access
- Go to Settings → User Management
- You should see ALL users including admins
- Go to Permissions Management
- You should see ALL users

### Step 4: Test Admin View
- Login as admin@carwash.com
- Go to Settings → User Management
- Verify you CANNOT see owner@carwash.com

## Use Cases

### Use Case 1: System Owner
```
The business owner needs full control over all accounts
→ Use superadmin role
```

### Use Case 2: Multiple Admins
```
You have several admins but want one master account
→ Create one superadmin, rest as admin
```

### Use Case 3: Security Separation
```
Protect owner account from being modified by admins
→ Superadmin is hidden from admin view
```

## Best Practices

1. **Limit Superadmin Accounts**
   - Only create 1-2 superadmin accounts
   - Use for business owners only

2. **Use Admin for Daily Operations**
   - Create admin accounts for managers
   - Use superadmin only when needed

3. **Protect Superadmin Credentials**
   - Change default password immediately
   - Use strong, unique password
   - Enable 2FA (if implemented)

4. **Regular Audits**
   - Review superadmin access logs
   - Monitor user management changes
   - Track permission modifications

## Troubleshooting

### Issue: Can't see all users as admin
**Solution:** You're not superadmin. This is intentional. Login as owner@carwash.com

### Issue: Superadmin account not working
**Solution:** Run `python create_superadmin.py` to create/update the account

### Issue: Staff can see user management
**Solution:** Check role assignment. Staff should have "user" role, not "admin"

## Summary

- ✅ Superadmin = Highest access level
- ✅ Hidden from admin view
- ✅ Can manage all users including admins
- ✅ Only for business owners
- ✅ Use admin for daily operations
