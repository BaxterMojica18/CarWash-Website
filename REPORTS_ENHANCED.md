# Enhanced Reports Feature

## New Features Added

### 1. Range Filters
Added comprehensive range filtering options:

#### Date Range Filter
- Filter sales from a specific start date to end date
- Example: January 1, 2025 to January 31, 2025

#### Month Range Filter
- Filter sales from start month to end month within a year
- Example: January to March 2025

#### Year Range Filter
- Filter sales from start year to end year
- Example: 2023 to 2025

### 2. Visual Charts

#### Line Chart (Sales Trend)
- Displays sales data over time
- Shows daily sales amounts
- Located on the left side (2/3 width)
- Responsive design with gradient fill
- Y-axis shows currency format (₱)

#### Pie Chart (Sales by Category)
- Shows sales breakdown by product/service categories
- Located on the right side (1/3 width)
- Color-coded categories
- Legend at bottom
- Responsive design

## API Updates

### Enhanced Endpoints
All endpoints now support range parameters:

**GET /api/reports/sales**
- New parameters:
  - `start_date` & `end_date` - For date range
  - `start_month` & `end_month` - For month range (with year)
  - `start_year` & `end_year` - For year range

**Response includes:**
```json
{
  "chart_data": {
    "labels": ["2025-01-01", "2025-01-02", ...],
    "values": [1250.00, 890.50, ...]
  },
  "category_data": {
    "labels": ["Wash", "Wax", "Detail"],
    "values": [5000, 3000, 2000]
  }
}
```

## Frontend Updates

### Filter Options
- Daily (single day)
- Date Range (start to end date)
- Monthly (single month)
- Month Range (start to end month in a year)
- Yearly (single year)
- Year Range (start to end year)

### Chart Integration
- Chart.js library integrated
- Automatic chart rendering on report generation
- Charts update dynamically with new data
- Responsive layout (stacks on mobile)

### Default Values
- Date filters: Current date
- Date range: First day of month to today
- Month range: January to current month
- Year range: Last year to current year

## Usage Example

1. Select "Date Range" from Report Period dropdown
2. Choose start date: 2025-01-01
3. Choose end date: 2025-01-31
4. Click "Generate Report"
5. View:
   - Total sales and invoice count
   - Line chart showing daily sales trend
   - Pie chart showing category breakdown
   - Detailed invoice table
6. Download as PDF or CSV

## Technical Details

### Backend
- SQLAlchemy queries with date range filtering
- Category aggregation from invoice items
- Chart data preparation in API response

### Frontend
- Chart.js for rendering
- Dynamic filter field management
- Responsive grid layout
- Color palette for pie chart segments

### Styling
- Responsive charts grid (2fr 1fr)
- Mobile-friendly (stacks vertically)
- Consistent with existing design
- Max height constraints for charts
