# Reports Feature Documentation

## Overview
Added a comprehensive sales reporting system with filtering and export capabilities.

## Database Changes

### New Table: `reports_cache`
- `id` - Primary key
- `user_id` - Foreign key to users table
- `report_type` - Type of report (e.g., "sales")
- `filter_period` - Period type (day/month/year)
- `filter_value` - Filter value used
- `generated_at` - Timestamp of report generation
- `total_sales` - Cached total sales amount
- `total_invoices` - Cached invoice count

## API Endpoints

### GET /api/reports/sales
Filter sales data by period:
- **Query Parameters:**
  - `period` - "day", "month", or "year"
  - `date` - Date string (YYYY-MM-DD) for daily reports
  - `month` - Month number (1-12) for monthly reports
  - `year` - Year number for monthly/yearly reports

**Response:**
```json
{
  "period": "day",
  "filter": {"date": "2025-01-15", "month": null, "year": null},
  "total_sales": 1250.00,
  "total_invoices": 15,
  "invoices": [...]
}
```

### GET /api/reports/sales/download/csv
Download filtered sales report as CSV file.
- Same query parameters as above
- Returns CSV file with invoice details

### GET /api/reports/sales/download/pdf
Download filtered sales report as PDF file.
- Same query parameters as above
- Returns formatted PDF with summary and invoice table

## Frontend

### New Page: reports.html
- Filter controls for day/month/year
- Real-time report generation
- Summary statistics display
- Invoice table with results
- Download buttons for PDF and CSV

### New JavaScript: reports.js
- Dynamic filter field management
- API integration for report generation
- Download functionality
- Default date/month/year initialization

## Navigation
Reports link added to all dashboard pages:
- Dashboard
- Invoices
- Products & Services
- Settings

## Usage

1. Navigate to Reports page from sidebar
2. Select report period (Daily/Monthly/Yearly)
3. Choose specific date/month/year
4. Click "Generate Report"
5. View results and download as PDF or CSV

## Migration

Run the migration script to create the table:
```bash
python add_reports_table.py
```

## Dependencies
- reportlab (already in requirements.txt)
- All other dependencies already installed
