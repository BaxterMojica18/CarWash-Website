# Granular Permissions System

## Overview
Implemented detailed permission management allowing admin and owner to control exactly what each user can do.

## New Permissions

### Invoice Permissions
- `add_invoice` - Create new invoices
- `edit_invoice` - Modify existing invoices
- `delete_invoice` - Delete invoices

### Product Permissions
- `add_product` - Add new products
- `edit_product` - Modify existing products
- `delete_product` - Delete products

### Service Permissions
- `add_service` - Add new services
- `edit_service` - Modify existing services
- `delete_service` - Delete services

### Bay Permissions
- `add_bay` - Add new washing bays
- `edit_bay` - Modify existing bays
- `delete_bay` - Delete bays

### Other Permissions
- `edit_theme` - Edit theme customization options
- `view_reports` - View sales reports
- `manage_users` - Manage users and permissions (admin/owner only)

## Features

### 1. Permission Management UI
**Location:** Settings → User Management → Permissions button

**Features:**
- Edit individual user permissions
- Checkbox interface for easy selection
- Grouped by category (Invoice, Product, Service, Bay, Other)
- Only accessible to admin and owner roles

### 2. Custom Permissions
- Users can have custom permission sets beyond their role
- System creates a `custom_{user_id}` role for individual permissions
- Custom permissions are added on top of role-based permissions

### 3. API Endpoints

**Get User Details:**
```
GET /api/auth/users/{user_id}
Response: {
  "user_id": 3,
  "email": "user@example.com",
  "roles": ["staff"],
  "permissions": ["add_invoice", "view_reports"]
}
```

**Update User Permissions:**
```
PUT /api/auth/users/permissions
Body: {
  "user_id": 3,
  "permissions": ["add_invoice", "edit_invoice", "view_reports"]
}
Response: { "message": "User permissions updated successfully" }
```

## Default Role Permissions

### Admin & Owner
- All permissions (full access)

### Staff
- `add_invoice` - Can create invoices
- `view_reports` - Can view sales reports

## Usage

### For Admin/Owner:
1. Login with admin or owner account
2. Navigate to Settings
3. Go to User Management section
4. Click "Permissions" button on any user
5. Select/deselect permissions as needed
6. Click "Save Permissions"

### Permission Inheritance:
- Users inherit permissions from their role
- Custom permissions are added on top
- Custom permissions don't override role permissions

## UI Updates

### User Card Display:
- Shows user email
- Shows assigned roles
- Shows permission count
- Two buttons: "Edit Role" and "Permissions"

### Permissions Modal:
- Organized by category
- Checkboxes for each permission
- Shows current user email
- Toast notification on save

## Database Changes

**New Permissions Added:**
- 15 granular permissions (replacing 6 broad ones)
- More specific control over user actions
- Better security and access control

**Custom Roles:**
- System automatically creates custom roles for users with individual permissions
- Format: `custom_{user_id}`
- Allows per-user permission customization
