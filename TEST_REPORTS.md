# Testing Reports Feature

## Setup Complete ✓

### 1. Fixed Issues
- ✓ Changed `apiCall` to `apiRequest` in reports.js
- ✓ Generated 102 dummy invoices with items
- ✓ Date range: September 26, 2025 to October 25, 2025
- ✓ Multiple product categories (Wash, Wax, Detail)

### 2. Dummy Data Generated
- **Invoices**: 102 invoices over 30 days
- **Customers**: 10 different customers
- **Products**: 5 different services
  - Basic Wash (₱500) - Wash category
  - Premium Wash (₱800) - Wash category
  - Wax Service (₱600) - Wax category
  - Interior Detail (₱1,200) - Detail category
  - Full Detail (₱2,000) - Detail category
- **Items per invoice**: 1-3 items randomly
- **Invoices per day**: 2-5 invoices randomly

## How to Test

### 1. Start the Server
```bash
uvicorn app.main:app --reload --port 8000
```

### 2. Login
- Go to http://localhost:8000/login.html
- Use demo credentials:
  - Email: demo@carwash.com
  - Password: demo123

### 3. Navigate to Reports
- Click "Reports" in the sidebar
- You should see the filter options

### 4. Test Filters

#### Test 1: Date Range (Recommended)
1. Select "Date Range" from dropdown
2. Start Date: 2025-09-26
3. End Date: 2025-10-25
4. Click "Generate Report"
5. **Expected**: Line chart showing daily sales, pie chart showing category breakdown

#### Test 2: Monthly
1. Select "Monthly" from dropdown
2. Month: October (10)
3. Year: 2025
4. Click "Generate Report"
5. **Expected**: Charts and table with October data

#### Test 3: Month Range
1. Select "Month Range" from dropdown
2. Start Month: September (9)
3. End Month: October (10)
4. Year: 2025
5. Click "Generate Report"
6. **Expected**: Charts showing 2 months of data

### 5. Verify Charts
- **Line Chart (Left)**: Should show sales trend over time
- **Pie Chart (Right)**: Should show breakdown by Wash, Wax, and Detail categories

### 6. Test Downloads
- Click "Download PDF" - should download a PDF report
- Click "Download CSV" - should download a CSV file

## Troubleshooting

### If charts don't show:
1. Check browser console (F12) for errors
2. Verify Chart.js is loading (check Network tab)
3. Verify API response includes chart_data and category_data

### If no data appears:
1. Verify you're logged in as demo user
2. Check that dummy data was generated (run generate_dummy_sales.py again)
3. Check browser console for API errors

### If API errors:
1. Verify server is running on port 8000
2. Check that reports router is registered in main.py
3. Verify database connection is working

## Expected Results

### Line Chart
- X-axis: Dates
- Y-axis: Sales amounts in ₱
- Smooth line with gradient fill
- Should show variation over 30 days

### Pie Chart
- 3 segments: Wash, Wax, Detail
- Different colors for each category
- Legend at bottom
- Percentages visible

### Summary Stats
- Total Sales: Should be around ₱80,000-120,000 (varies due to random data)
- Total Invoices: 102 invoices

### Invoice Table
- All invoices listed with details
- Sorted by date
- Shows invoice number, date, customer, amount
