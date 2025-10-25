# Soft Delete Implementation

## Overview
Implemented soft delete functionality across all tables with delete operations. Records are marked as deleted instead of being permanently removed from the database.

## Database Changes

### New Columns Added
All tables with delete functionality now have:
- `status` VARCHAR - Values: "A" (Active) or "D" (Deleted)
- `deleted_at` TIMESTAMP - Records when the item was soft deleted

### Affected Tables
1. **locations** - Washing bays
2. **products_services** - Products and services
3. **invoices** - Invoice records

## Migration Required

Run this command to add the soft delete columns:
```bash
python add_soft_delete_columns.py
```

## How It Works

### Before (Hard Delete)
- Record was permanently removed from database
- Data was lost forever
- Could cause referential integrity issues

### After (Soft Delete)
- Record status changed from "A" to "D"
- `deleted_at` timestamp is set to current date/time
- Record remains in database but hidden from queries
- Can be restored if needed

## Query Changes

All GET queries now filter by `status = "A"`:
- `get_locations()` - Only returns active locations
- `get_products_services()` - Only returns active products/services
- `get_invoices()` - Only returns active invoices

## Delete Functions Updated

1. **delete_location()** - Sets status="D", deleted_at=now()
2. **delete_product_service()** - Sets status="D", deleted_at=now()
3. **delete_invoice()** - Sets status="D", deleted_at=now()

## UI Changes

### Settings Page
- Added "Delete Button Configuration" section
- Brightness slider (50-150%)
- Saturation slider (0-100%)
- Separated from main theme grid for clarity

### Button Styling
- Washing bay buttons now properly styled
- Edit button: Blue (primary color)
- Delete button: Red (customizable via settings)

## Benefits

1. **Data Recovery** - Deleted items can be restored
2. **Audit Trail** - Know when items were deleted
3. **Referential Integrity** - No broken foreign key relationships
4. **Compliance** - Meet data retention requirements
5. **Analytics** - Analyze deletion patterns

## Future Enhancements

Potential additions:
- Admin panel to view deleted items
- Restore functionality
- Permanent delete after X days
- Deleted by user tracking
