# How to Access Permissions Management

## 🎯 Quick Access Guide

### Method 1: Via Settings Page (Recommended)

```
1. Login to the system
   └─> Email: admin@carwash.com
   └─> Password: admin123

2. Click "Settings" in the sidebar
   └─> Look for "User Management" section

3. Click "🔐 Manage Permissions" button
   └─> Opens permissions-management.html
```

**Visual Flow:**
```
Login Page → Dashboard → Settings → User Management → 🔐 Manage Permissions
```

### Method 2: Direct URL

```
1. Login to the system

2. Navigate directly to:
   http://localhost:8000/permissions-management.html
```

### Method 3: Via Sidebar (If Enabled)

```
1. Login as Admin/Owner

2. Look in the sidebar menu for:
   🔐 Permissions

3. Click to access
```

## 👀 What You'll See

### Page Layout:

```
┌─────────────────────────────────────────────────────────────────┐
│  🔐 Permissions Management                                      │
│  Manage user roles and permissions                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Total Users  │  │ Admin Users  │  │ Staff Users  │         │
│  │     12       │  │      3       │  │      8       │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 🔍 Search by email...    [All Roles ▼]  [🔄 Refresh]  │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────┐  ┌─────────────────────────┐     │
│  │ user1@example.com       │  │ user2@example.com       │     │
│  │ [admin]                 │  │ [user]                  │     │
│  │                         │  │                         │     │
│  │ Manage Products   [ON]  │  │ Manage Products   [OFF] │     │
│  │ Manage Locations  [ON]  │  │ Manage Locations  [OFF] │     │
│  │ Manage Invoices   [ON]  │  │ Manage Invoices   [ON]  │     │
│  │ View Reports      [ON]  │  │ View Reports      [ON]  │     │
│  │ Manage Settings   [ON]  │  │ Manage Settings   [OFF] │     │
│  │ Manage Users      [ON]  │  │ Manage Users      [OFF] │     │
│  └─────────────────────────┘  └─────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## 🔑 Access Requirements

### Who Can Access:
- ✅ Users with `admin` role
- ✅ Users with `owner` role
- ❌ Users with `user` role
- ❌ Users with `client` role

### Default Admin Accounts:

**Admin Account:**
```
Email: admin@carwash.com
Password: admin123
```

**Owner Account:**
```
Email: demo@carwash.com
Password: demo123
```

## 🎮 How to Use

### 1. Search for a User
```
Type in the search box: "user@example.com"
→ Results filter in real-time
```

### 2. Filter by Role
```
Click the dropdown: [All Roles ▼]
→ Select: Admin, Owner, User, or Client
→ Only users with that role will show
```

### 3. Toggle Permissions
```
Find the user card
→ Locate the permission you want to change
→ Click the toggle switch
→ Green = Enabled, Gray = Disabled
→ Changes save automatically
→ Toast notification confirms success
```

### 4. View Permission Details
```
Each permission shows:
→ Permission name (e.g., "Manage Products")
→ Description (e.g., "Add, edit, and delete products")
→ Current status (toggle switch)
```

## 📱 Screenshots Guide

### Settings Page - User Management Section:
```
┌─────────────────────────────────────────────────────┐
│ User Management                                      │
│ ┌──────────────────────┐  ┌──────────────────────┐ │
│ │ 🔐 Manage Permissions│  │ + Add User           │ │
│ └──────────────────────┘  └──────────────────────┘ │
│                                                      │
│ [User cards displayed here...]                      │
└─────────────────────────────────────────────────────┘
```

### Permissions Management Page - User Card:
```
┌─────────────────────────────────────────────────────┐
│ john.doe@example.com                    [user]      │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Manage Products                              [OFF]  │
│ Add, edit, and delete products                      │
│                                                      │
│ Manage Locations                             [OFF]  │
│ Add, edit, and delete washing bays                  │
│                                                      │
│ Manage Invoices                              [ON]   │
│ Create, edit, and delete invoices                   │
│                                                      │
│ View Reports                                 [ON]   │
│ Access sales reports and analytics                  │
│                                                      │
│ Manage Settings                              [OFF]  │
│ Modify theme and business settings                  │
│                                                      │
│ Manage Users                                 [OFF]  │
│ Manage user accounts and permissions                │
└─────────────────────────────────────────────────────┘
```

## 🚨 Troubleshooting

### Issue: Can't see "Manage Permissions" button

**Solution:**
1. Check if you're logged in as admin/owner
2. Verify your role:
   ```
   Go to: http://localhost:8000/api/auth/me/permissions
   Check: "roles" field should include "admin" or "owner"
   ```

### Issue: Page shows "Failed to load users"

**Solution:**
1. Check if server is running
2. Verify database connection
3. Run: `python add_permissions.py`
4. Restart server

### Issue: Permission toggles don't work

**Solution:**
1. Check browser console for errors (F12)
2. Verify JWT token is valid
3. Check if you have `manage_users` permission
4. Try logging out and back in

### Issue: 403 Forbidden error

**Solution:**
1. You don't have admin/owner role
2. Contact system administrator
3. Or run: `python assign_user_roles.py` to assign roles

## 📋 Step-by-Step Tutorial

### Complete Walkthrough:

**Step 1: Login**
```
1. Open browser
2. Go to: http://localhost:8000
3. Click "Login"
4. Enter admin credentials
5. Click "Login" button
```

**Step 2: Navigate to Settings**
```
1. Look at left sidebar
2. Click "Settings"
3. Scroll down to "User Management" section
```

**Step 3: Open Permissions Management**
```
1. Find "🔐 Manage Permissions" button
2. Click it
3. New page opens
```

**Step 4: Find a User**
```
1. See all users displayed in cards
2. Or use search box to find specific user
3. Or use role filter dropdown
```

**Step 5: Change Permissions**
```
1. Find the user card
2. Locate the permission to change
3. Click the toggle switch
4. Wait for green success message
5. Permission is now updated!
```

**Step 6: Verify Changes**
```
1. Click "🔄 Refresh" button
2. Check if toggle stayed in new position
3. Or ask the user to login and test
```

## 🎯 Common Use Cases

### Use Case 1: Give User Access to Reports
```
1. Search for user email
2. Find "View Reports" permission
3. Toggle it ON (green)
4. User can now access reports page
```

### Use Case 2: Restrict Product Management
```
1. Search for user email
2. Find "Manage Products" permission
3. Toggle it OFF (gray)
4. User can no longer add/edit/delete products
```

### Use Case 3: Promote User to Admin
```
1. Go to Settings → User Management
2. Click "Edit Role" on user card
3. Change role to "admin"
4. All permissions automatically granted
```

### Use Case 4: Create Custom Permission Set
```
1. Open Permissions Management
2. Find the user
3. Toggle ON only specific permissions:
   - Manage Invoices: ON
   - View Reports: ON
   - Everything else: OFF
4. User now has custom access
```

## 📞 Need Help?

### Resources:
- **Full Guide:** See `PERMISSIONS_GUIDE.md`
- **API Docs:** http://localhost:8000/docs
- **Implementation Details:** See `PERMISSIONS_IMPLEMENTATION_SUMMARY.md`

### Quick Commands:
```bash
# Initialize permissions
python add_permissions.py

# Assign roles to users
python assign_user_roles.py

# Test permissions
python test_permissions.py

# Start server
start_server.bat
```

## ✅ Checklist

Before using permissions management, ensure:

- [ ] Server is running (`start_server.bat`)
- [ ] Database is initialized (`python create_db.py`)
- [ ] Permissions are created (`python add_permissions.py`)
- [ ] You're logged in as admin/owner
- [ ] You can access Settings page
- [ ] "User Management" section is visible

If all checked, you're ready to manage permissions! 🎉
