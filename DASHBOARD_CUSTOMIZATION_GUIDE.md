# Dashboard Customization Guide

## Overview

Superadmin can now fully customize the dashboard appearance and modules through the Settings page.

## Features

### 1. Website Branding
- **Website Name**: Change the name displayed in the dashboard
- **Primary Color**: Main theme color for buttons and accents
- **Background Color**: Page background color
- **Sidebar Color**: Navigation sidebar color
- **Layout Type**: Grid, List, or Compact layout

### 2. Dashboard Modules
- **Add Modules**: Create custom dashboard widgets
- **Edit Modules**: Modify existing modules
- **Delete Modules**: Remove unwanted modules
- **Reorder Modules**: Change display order with position field
- **Toggle Visibility**: Show/hide modules

## Access

**Only Superadmin** can access dashboard customization:
- Login: `owner@carwash.com` / `owner123`
- Go to: Settings → Dashboard Customization

## Dashboard Settings

### Website Name
```
Default: CarWash
Custom: Your Business Name
```

### Colors
```
Primary Color: #667eea (Purple)
Background Color: #f5f5f5 (Light Gray)
Sidebar Color: #2c3e50 (Dark Blue)
```

### Layout Types
- **Grid**: Card-based grid layout (default)
- **List**: Vertical list layout
- **Compact**: Condensed view

## Dashboard Modules

### Module Types

1. **Statistic Card**
   - Display key metrics
   - Example: Total Revenue, Cars Washed

2. **Chart**
   - Visual data representation
   - Example: Revenue Chart, Sales Trend

3. **Table**
   - Tabular data display
   - Example: Recent Invoices, Top Products

4. **List**
   - Simple list view
   - Example: Recent Activity, Notifications

### Module Properties

| Property | Description | Options |
|----------|-------------|---------|
| Module Name | Internal identifier | Any string |
| Module Type | Widget type | stat, chart, table, list |
| Title | Display title | Any string |
| Width | Module width | full, half, third |
| Position | Display order | 0, 1, 2, ... |
| Visible | Show/hide | true/false |

## How to Use

### Step 1: Access Settings
```
1. Login as superadmin
2. Go to Settings page
3. Scroll to "Dashboard Customization" section
```

### Step 2: Customize Appearance
```
1. Change Website Name
2. Pick colors using color pickers
3. Select layout type
4. Click "Save Dashboard Settings"
```

### Step 3: Manage Modules
```
1. Click "+ Add Module"
2. Fill in module details:
   - Module Name: revenue_card
   - Module Type: stat
   - Title: Total Revenue
   - Width: half
   - Position: 0
   - Visible: checked
3. Click "Add Module"
```

### Step 4: Edit Module
```
1. Find module in list
2. Click "Edit" button
3. Modify properties
4. Click "Update Module"
```

### Step 5: Delete Module
```
1. Find module in list
2. Click "Delete" button
3. Confirm deletion
```

## API Endpoints

### Get Dashboard Settings
```http
GET /api/dashboard/settings
Authorization: Bearer {token}
```

### Save Dashboard Settings
```http
POST /api/dashboard/settings
Authorization: Bearer {token}
Content-Type: application/json

{
  "website_name": "My Car Wash",
  "primary_color": "#667eea",
  "background_color": "#f5f5f5",
  "sidebar_color": "#2c3e50",
  "layout_type": "grid"
}
```

### Get Modules
```http
GET /api/dashboard/modules
Authorization: Bearer {token}
```

### Create Module
```http
POST /api/dashboard/modules
Authorization: Bearer {token}
Content-Type: application/json

{
  "module_name": "revenue_card",
  "module_type": "stat",
  "title": "Total Revenue",
  "position": 0,
  "width": "half",
  "is_visible": true,
  "config": {}
}
```

### Update Module
```http
PUT /api/dashboard/modules/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "module_name": "revenue_card",
  "module_type": "stat",
  "title": "Monthly Revenue",
  "position": 1,
  "width": "full",
  "is_visible": true,
  "config": {}
}
```

### Delete Module
```http
DELETE /api/dashboard/modules/{id}
Authorization: Bearer {token}
```

## Database Schema

### dashboard_settings
```sql
CREATE TABLE dashboard_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    website_name VARCHAR(255) DEFAULT 'CarWash',
    primary_color VARCHAR(50) DEFAULT '#667eea',
    background_color VARCHAR(50) DEFAULT '#f5f5f5',
    sidebar_color VARCHAR(50) DEFAULT '#2c3e50',
    layout_type VARCHAR(50) DEFAULT 'grid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### dashboard_modules
```sql
CREATE TABLE dashboard_modules (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    module_name VARCHAR(255) NOT NULL,
    module_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    position INTEGER DEFAULT 0,
    width VARCHAR(50) DEFAULT 'full',
    is_visible BOOLEAN DEFAULT TRUE,
    config JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Example Configurations

### Example 1: Revenue Dashboard
```json
{
  "website_name": "Premium Car Wash",
  "primary_color": "#4CAF50",
  "background_color": "#ffffff",
  "sidebar_color": "#1a237e",
  "layout_type": "grid"
}

Modules:
1. Total Revenue (stat, half, position 0)
2. Cars Washed (stat, half, position 1)
3. Revenue Chart (chart, full, position 2)
4. Recent Activity (list, full, position 3)
```

### Example 2: Compact Dashboard
```json
{
  "website_name": "Quick Wash",
  "primary_color": "#FF5722",
  "background_color": "#f5f5f5",
  "sidebar_color": "#263238",
  "layout_type": "compact"
}

Modules:
1. Today's Stats (stat, third, position 0)
2. Active Bays (stat, third, position 1)
3. Pending Orders (stat, third, position 2)
```

## Setup Instructions

### Step 1: Create Tables
```bash
python create_dashboard_customization.py
```

### Step 2: Restart Server
```bash
start_server.bat
```

### Step 3: Login as Superadmin
```
Email: owner@carwash.com
Password: owner123
```

### Step 4: Customize
```
Go to Settings → Dashboard Customization
```

## Security

- ✅ Only superadmin can access customization
- ✅ Settings are user-specific
- ✅ Backend validation on all endpoints
- ✅ SQL injection protection with parameterized queries

## Summary

✅ Superadmin can customize website name
✅ Superadmin can change all colors
✅ Superadmin can select layout type
✅ Superadmin can add/edit/delete dashboard modules
✅ Superadmin can reorder modules
✅ All changes saved to database
✅ Settings persist across sessions
