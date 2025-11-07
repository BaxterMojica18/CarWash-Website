# Sidebar Navigation & User Management Update

## Changes Made

### 1. Standardized Sidebar Navigation
All HTML files now have consistent navigation with these menu items:
- Dashboard
- Invoices
- Products
- Services
- Reports
- Settings
- Logout

**Files Updated:**
- `frontend/dashboard.html`
- `frontend/invoices.html`
- `frontend/products.html` (already correct)
- `frontend/services.html` (already correct)
- `frontend/reports.html` (already correct)
- `frontend/settings.html`

### 2. User Management Feature Added to Settings

**Location:** Settings page (only visible to Admin and Owner roles)

**Features:**
- View all users with their roles
- Add new users (Name, Email, Role)
- Edit user roles
- Delete users (UI ready, backend pending)

**Roles Available:**
1. **Admin** - Full access to all features including user management
2. **Owner** - Full access to all features including user management
3. **Staff** - Limited permissions (least access)

**Access Control:**
- User Management section is hidden by default
- Only visible to users with "admin" or "owner" roles
- Checked via `/api/auth/me/permissions` endpoint

### 3. Frontend Implementation

**New Functions in `settings.js`:**
- `checkUserPermissions()` - Checks if user is admin/owner
- `loadUsers()` - Loads all users from API
- `showAddUser()` - Opens add user modal
- `closeUserModal()` - Closes user modal
- `editUser()` - Opens edit modal with user data
- `deleteUser()` - Deletes user (placeholder)

**New HTML in `settings.html`:**
- User Management section (hidden by default)
- Add/Edit User modal with form fields:
  - Name (text input)
  - Email (email input)
  - Role (dropdown: staff, owner, admin)

### 4. API Endpoints Used

**User Management:**
- `GET /api/auth/me/permissions` - Get current user's roles and permissions
- `GET /api/auth/users` - Get all users (admin/owner only)
- `PUT /api/auth/users/roles` - Update user roles (admin/owner only)

### 5. Permission Structure

**Admin & Owner can:**
- Manage users (add, edit, delete)
- Manage locations
- Manage products/services
- View reports
- Manage invoices
- Access all settings

**Staff can:**
- View dashboard
- Create invoices
- View products/services
- Limited access to reports

## Testing

1. Login as admin or owner
2. Navigate to Settings
3. User Management section should appear at the top
4. Click "+ Add User" to add new users
5. Assign roles: staff, owner, or admin
6. Edit existing user roles
