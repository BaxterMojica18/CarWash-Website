# Troubleshooting Charts Not Showing

## Steps to Debug

### 1. Test Chart.js Loading
Open http://localhost:8000/test_charts.html
- Should see a simple line chart
- If not, Chart.js CDN might be blocked

### 2. Check Browser Console
1. Open Reports page
2. Press F12 to open Developer Tools
3. Go to Console tab
4. Click "Generate Report"
5. Look for:
   - "Report data:" log
   - "Chart data:" log
   - "Category data:" log
   - "Rendering line chart with:" log
   - "Rendering pie chart with:" log
   - Any errors in red

### 3. Check Network Tab
1. In Developer Tools, go to Network tab
2. Click "Generate Report"
3. Look for `/api/reports/sales` request
4. Click on it and check Response tab
5. Verify it has:
   ```json
   {
     "chart_data": {"labels": [...], "values": [...]},
     "category_data": {"labels": [...], "values": [...]}
   }
   ```

### 4. Common Issues

#### Issue: "Chart is not defined"
**Solution**: Chart.js not loading
- Check internet connection
- Try different CDN: `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js`

#### Issue: Charts section not visible
**Solution**: CSS display issue
- Check if `reportResults` div has `display: block` after clicking Generate

#### Issue: Empty chart data
**Solution**: No invoices for selected date
- Try "Date Range": 2025-09-26 to 2025-10-25
- This should have 102 invoices from dummy data

#### Issue: "canvas not found"
**Solution**: HTML structure issue
- Verify `lineChart` and `pieChart` canvas elements exist in HTML

### 5. Manual Test in Console
After clicking Generate Report, run in browser console:
```javascript
// Check if Chart.js is loaded
console.log('Chart available:', typeof Chart !== 'undefined');

// Check current report data
console.log('Current data:', currentReportData);

// Check canvas elements
console.log('Line canvas:', document.getElementById('lineChart'));
console.log('Pie canvas:', document.getElementById('pieChart'));

// Try rendering manually
if (currentReportData) {
    renderLineChart(currentReportData.chart_data);
    renderPieChart(currentReportData.category_data);
}
```

### 6. Force Refresh
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Restart browser

### 7. Check Date Format
The dummy data is from Sept 26 - Oct 25, 2025
Make sure you're selecting dates in that range!

### 8. Verify Dummy Data Exists
Run in terminal:
```bash
python -c "from app.database import SessionLocal, Invoice; db = SessionLocal(); print(f'Total invoices: {db.query(Invoice).count()}'); db.close()"
```

Should show at least 102 invoices.

## Quick Fix Steps

1. **Restart server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

2. **Clear browser cache and refresh**

3. **Try Date Range filter**:
   - Start: 2025-09-26
   - End: 2025-10-25

4. **Check console for errors** (F12)

5. **If still not working**, share console errors for further debugging
