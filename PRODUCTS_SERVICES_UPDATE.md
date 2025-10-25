# Products & Services Separation Update

## Changes Made

### 1. Database Schema Updates
- Added `quantity_unit` column to `products_services` table (ML, L, Gallons)
- Added `delete_button_brightness` and `delete_button_saturation` to theme customization
- Run migration: `python update_products_schema.py`

### 2. Separate Pages
- **Products Page** (`products.html`): Manages products with quantity units
- **Services Page** (`services.html`): Manages services (no quantity units)
- Both pages now have separate navigation items in sidebar

### 3. Product Features
- Products require a quantity unit (ML, L, or Gallons)
- Each product must have a unique combination of name + quantity_unit
- Products are filtered by type='product'

### 4. Service Features
- Services remain simple with name, price, description
- Services are filtered by type='service'

### 5. Button Styling
- **Edit Button**: Uses primary color (customizable via theme)
- **Delete Button**: Always red with customizable brightness and saturation
- CSS variables: `--delete-brightness` and `--delete-saturation`

### 6. Reports Enhancement
- Added **Product Category Sales** chart
- Shows breakdown of product sales by name and quantity unit
- Example: "Car Wax (ML)", "Car Wax (L)", "Car Wax (Gallons)"

### 7. Sidebar Updates
All pages now have:
```
- Dashboard
- Invoices
- Products (new)
- Services (new)
- Reports
- Settings
- Logout
```

## Setup Instructions

1. Run the database migration:
```bash
python update_products_schema.py
```

2. Restart the server:
```bash
start_server.bat
```

3. Access the new pages:
- Products: http://localhost:8000/products.html
- Services: http://localhost:8000/services.html

## API Endpoints (No Changes)
The existing `/api/settings/products` endpoints work for both products and services.
The `type` field differentiates between 'product' and 'service'.

## Theme Customization
In Settings > Theme Customization, you can now adjust:
- Delete Button Brightness (0-100%)
- Delete Button Saturation (0-100%)

The delete button will always be red, but you can control its intensity.
