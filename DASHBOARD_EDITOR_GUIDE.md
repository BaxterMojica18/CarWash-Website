# Dashboard Editor Guide

## Overview

Superadmin can now visually edit the dashboard with drag-and-drop functionality through an interactive editor.

## Features

### Visual Dashboard Editor
- ✅ Drag-and-drop module reordering
- ✅ Add new modules with live preview
- ✅ Delete modules with one click
- ✅ Real-time color customization
- ✅ Live preview of changes
- ✅ Save changes to apply to actual dashboard

### Customization Panel
- **Colors**: Sidebar, Background, Primary
- **Add Modules**: Select type and title
- **Layout**: Grid, List, Compact
- **Save/Cancel**: Apply or discard changes

## Access

**Only Superadmin:**
1. Login: `owner@carwash.com` / `owner123`
2. Go to: Settings → Dashboard Customization
3. Click: "✏️ Edit Dashboard" button
4. Opens: `edit-dashboard.html`

## How to Use

### Step 1: Open Editor
```
Settings → Dashboard Customization → ✏️ Edit Dashboard
```

### Step 2: Customize Colors
```
Right Panel → Colors Section
- Pick Sidebar Color
- Pick Background Color
- Pick Primary Color
→ Changes apply instantly to preview
```

### Step 3: Add Modules
```
Right Panel → Add Module Section
1. Select module type (Stat/Chart/Table/List)
2. Enter module title
3. Click "+ Add Module"
→ Module appears in preview
```

### Step 4: Reorder Modules
```
Dashboard Preview Area
1. Click and hold on any module
2. Drag to new position
3. Drop to place
→ Order updates automatically
```

### Step 5: Delete Modules
```
Dashboard Preview Area
1. Find module to delete
2. Click "✕" button in top-right corner
3. Confirm deletion
→ Module removed from preview
```

### Step 6: Save Changes
```
Right Panel → Bottom
1. Click "💾 Save Changes"
→ All changes saved to database
→ Redirects to dashboard with new settings
```

## Module Types

### 1. Statistic Card
- Display key metrics
- Shows title and value
- Example: Total Revenue, Cars Washed

### 2. Chart
- Visual data representation
- Placeholder in editor
- Example: Revenue Chart, Sales Trend

### 3. Table
- Tabular data display
- Shows sample rows in editor
- Example: Recent Invoices, Top Products

### 4. Activity List
- Simple list view
- Shows sample items in editor
- Example: Recent Activity, Notifications

## Editor Interface

```
┌─────────────────────────────────────────────────────────────┐
│ Dashboard Preview                    │ Customization Panel  │
│                                      │                      │
│ ┌──────────────────────────────┐    │ Colors               │
│ │ Module 1 (Draggable)      ✕ │    │ ├─ Sidebar Color     │
│ └──────────────────────────────┘    │ ├─ Background Color  │
│                                      │ └─ Primary Color     │
│ ┌──────────────────────────────┐    │                      │
│ │ Module 2 (Draggable)      ✕ │    │ Add Module           │
│ └──────────────────────────────┘    │ ├─ Type Dropdown     │
│                                      │ ├─ Title Input       │
│ ┌──────────────────────────────┐    │ └─ + Add Button      │
│ │ Module 3 (Draggable)      ✕ │    │                      │
│ └──────────────────────────────┘    │ Layout               │
│                                      │ └─ Type Dropdown     │
│                                      │                      │
│                                      │ [💾 Save Changes]    │
│                                      │ [Cancel]             │
└─────────────────────────────────────────────────────────────┘
```

## Workflow

### Example: Create Custom Dashboard

**Step 1: Open Editor**
```
Settings → Edit Dashboard
```

**Step 2: Set Colors**
```
Sidebar: #1a237e (Dark Blue)
Background: #ffffff (White)
Primary: #4CAF50 (Green)
```

**Step 3: Add Modules**
```
1. Add "Total Revenue" (Stat)
2. Add "Cars Washed Today" (Stat)
3. Add "Revenue Chart" (Chart)
4. Add "Recent Activity" (List)
```

**Step 4: Reorder**
```
Drag modules to desired order:
1. Total Revenue
2. Cars Washed Today
3. Revenue Chart
4. Recent Activity
```

**Step 5: Save**
```
Click "💾 Save Changes"
→ Dashboard updated!
```

## Technical Details

### Files Created
- ✅ `frontend/edit-dashboard.html` - Visual editor
- ✅ Modified `frontend/settings.html` - Added Edit button
- ✅ Modified `frontend/js/dashboard.js` - Apply settings on load

### Features
- **Drag-and-Drop**: Native HTML5 drag API
- **Live Preview**: Changes apply instantly
- **Color Picker**: HTML5 color input
- **Module Management**: Add/Delete/Reorder
- **Persistence**: Saves to database via API

### API Calls
```javascript
// Load settings
GET /api/dashboard/settings

// Save settings
POST /api/dashboard/settings

// Load modules
GET /api/dashboard/modules

// Create module
POST /api/dashboard/modules

// Delete module
DELETE /api/dashboard/modules/{id}
```

## Dashboard Application

When you save changes in the editor:

1. **Settings Applied**:
   - Website name updates
   - Colors change throughout dashboard
   - Layout type applied

2. **Modules Updated**:
   - Old modules deleted
   - New modules created
   - Order preserved

3. **Dashboard Loads**:
   - Reads settings from database
   - Applies colors automatically
   - Shows configured modules

## Tips

### Best Practices
1. **Preview First**: Test colors before saving
2. **Logical Order**: Put important stats at top
3. **Balance Layout**: Mix stat cards with charts
4. **Consistent Colors**: Use complementary colors

### Common Workflows
- **Quick Color Change**: Edit colors → Save
- **Add One Module**: Add module → Save
- **Complete Redesign**: Change everything → Save
- **Reorder Only**: Drag modules → Save

## Troubleshooting

### Issue: Changes not saving
**Solution**: Check browser console for errors, verify superadmin login

### Issue: Drag-and-drop not working
**Solution**: Ensure modules have draggable="true" attribute

### Issue: Colors not applying
**Solution**: Clear browser cache, reload page

### Issue: Modules not showing
**Solution**: Check if modules are marked as visible

## Summary

✅ Visual drag-and-drop editor
✅ Real-time color customization
✅ Add/Delete/Reorder modules
✅ Live preview of changes
✅ One-click save to database
✅ Changes apply to actual dashboard
✅ Superadmin only access

The dashboard editor provides a complete visual customization experience!
