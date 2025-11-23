# New Permissions Implementation Summary

## New Permissions Added

### 1. view_locations
- **Description:** View washing bays/locations
- **Access:** Can see locations list but cannot add/edit/delete
- **Assigned to:** Superadmin, Admin, User (Staff)

### 2. view_invoices
- **Description:** View invoices
- **Access:** Can see invoices but cannot create/edit/delete
- **Assigned to:** Superadmin, Admin, User (Staff)

## Permission Hierarchy

### Location Permissions:
- **manage_locations** (Create, Edit, Delete) → Superadmin, Admin
- **view_locations** (Read Only) → Superadmin, Admin, User

### Invoice Permissions:
- **manage_invoices** (Create, Edit, Delete) → Superadmin, Admin, User
- **view_invoices** (Read Only) → Superadmin, Admin, User

## UI Changes

### Settings Page - Washing Bays Section:

**For users with manage_locations:**
```
Washing Bays                    [+ Add Bay]
┌─────────────────────────────────────────┐
│ Bay 1                                   │
│ Address                                 │
│ [Edit] [Delete]                         │
└─────────────────────────────────────────┘
```

**For users with only view_locations:**
```
Washing Bays
┌─────────────────────────────────────────┐
│ Bay 1                                   │
│ Address                                 │
│ (No action buttons)                     │
└─────────────────────────────────────────┘
```

**For users without view_locations:**
```
(Section hidden completely)
```

## Backend Protection

### Location Endpoints:
```python
GET /api/settings/locations
- Requires: view_locations OR manage_locations

POST /api/settings/locations
- Requires: manage_locations

PUT /api/settings/locations/{id}
- Requires: manage_locations

DELETE /api/settings/locations/{id}
- Requires: manage_locations
```

### Invoice Endpoints:
```python
GET /api/invoices/
- Requires: view_invoices OR manage_invoices

GET /api/invoices/{id}
- Requires: view_invoices OR manage_invoices

POST /api/invoices/
- Requires: manage_invoices

PUT /api/invoices/{id}
- Requires: manage_invoices

DELETE /api/invoices/{id}
- Requires: manage_invoices
```

## Role Permissions Matrix

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

## Setup Instructions

### Step 1: Add Permissions
```bash
python add_new_permissions.py
```

### Step 2: Restart Server
```bash
start_server.bat
```

### Step 3: Test Permissions
1. Login as superadmin (owner@carwash.com)
2. Go to Permissions Management
3. Toggle permissions for test users
4. Verify UI changes based on permissions

## Testing Scenarios

### Test 1: Staff with view_locations only
1. Create user with "user" role
2. Remove manage_locations permission
3. Keep view_locations permission
4. Login as that user
5. Go to Settings
6. Verify: Can see locations but no Add/Edit/Delete buttons

### Test 2: Staff with view_invoices only
1. Create user with "user" role
2. Remove manage_invoices permission
3. Keep view_invoices permission
4. Login as that user
5. Go to Invoices page
6. Verify: Can see invoices but no Create/Edit/Delete buttons

### Test 3: Admin with all permissions
1. Login as admin@carwash.com
2. Go to Settings
3. Verify: Can see and manage locations
4. Go to Invoices
5. Verify: Can create and manage invoices

## Files Modified

### Backend:
- ✅ `add_new_permissions.py` - Script to add permissions
- ✅ `app/routers/settings.py` - Added view_locations check
- ✅ `app/routers/invoices.py` - Added view_invoices check

### Frontend:
- ✅ `frontend/settings.html` - Hide Add Bay button by default
- ✅ `frontend/js/settings.js` - Show/hide buttons based on permissions
- ✅ `frontend/permissions-management.html` - Added new permissions

## Summary

✅ Added 2 new permissions: view_locations, view_invoices
✅ Updated all roles with appropriate permissions
✅ Added backend permission checks
✅ Updated UI to show/hide buttons based on permissions
✅ Tested with superadmin, admin, and user roles

Users can now have granular control over who can view vs manage locations and invoices!
