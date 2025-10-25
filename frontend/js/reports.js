let currentReportData = null;
let lineChart = null;
let pieChart = null;
let productPieChart = null;

function updateFilterFields() {
    const periodType = document.getElementById('periodType').value;
    
    document.getElementById('dayFilter').style.display = periodType === 'day' ? 'block' : 'none';
    document.getElementById('dayRangeFilter').style.display = periodType === 'day_range' ? 'block' : 'none';
    document.getElementById('monthFilter').style.display = periodType === 'month' ? 'block' : 'none';
    document.getElementById('monthRangeFilter').style.display = periodType === 'month_range' ? 'block' : 'none';
    document.getElementById('yearFilter').style.display = periodType === 'year' ? 'block' : 'none';
    document.getElementById('yearRangeFilter').style.display = periodType === 'year_range' ? 'block' : 'none';
}

async function generateReport() {
    const periodType = document.getElementById('periodType').value;
    let params = `period=${periodType}`;
    
    console.log('Generating report for period:', periodType);
    
    if (periodType === 'day') {
        const date = document.getElementById('filterDate').value;
        if (!date) {
            alert('Please select a date');
            return;
        }
        console.log('Selected date:', date);
        params += `&date=${date}`;
    } else if (periodType === 'day_range') {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        if (!startDate || !endDate) {
            alert('Please select start and end dates');
            return;
        }
        params += `&start_date=${startDate}&end_date=${endDate}`;
    } else if (periodType === 'month') {
        const month = document.getElementById('filterMonth').value;
        const year = document.getElementById('filterMonthYear').value;
        params += `&month=${month}&year=${year}`;
    } else if (periodType === 'month_range') {
        const startMonth = document.getElementById('startMonth').value;
        const endMonth = document.getElementById('endMonth').value;
        const year = document.getElementById('rangeYear').value;
        params += `&start_month=${startMonth}&end_month=${endMonth}&year=${year}`;
    } else if (periodType === 'year') {
        const year = document.getElementById('filterYear').value;
        params += `&year=${year}`;
    } else if (periodType === 'year_range') {
        const startYear = document.getElementById('startYear').value;
        const endYear = document.getElementById('endYear').value;
        params += `&start_year=${startYear}&end_year=${endYear}`;
    }
    
    try {
        console.log('API call:', `/reports/sales?${params}`);
        const response = await apiRequest(`/reports/sales?${params}`);
        console.log('API response:', response);
        currentReportData = response;
        displayReport(response);
    } catch (error) {
        console.error('Error details:', error);
        alert('Error generating report: ' + error.message);
    }
}

function displayReport(data) {
    console.log('Report data:', data);
    document.getElementById('reportResults').style.display = 'block';
    document.getElementById('totalSales').textContent = `₱${data.total_sales.toFixed(2)}`;
    document.getElementById('totalInvoices').textContent = data.total_invoices;
    
    const tbody = document.getElementById('reportTableBody');
    tbody.innerHTML = '';
    
    data.invoices.forEach(invoice => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${invoice.invoice_number}</td>
            <td>${new Date(invoice.date).toLocaleDateString()}</td>
            <td>${invoice.customer_name}</td>
            <td>₱${invoice.total_amount.toFixed(2)}</td>
        `;
        tbody.appendChild(row);
    });
    
    console.log('Chart data:', data.chart_data);
    console.log('Category data:', data.category_data);
    
    if (data.chart_data && data.chart_data.labels && data.chart_data.labels.length > 0) {
        renderLineChart(data.chart_data);
    } else {
        console.warn('No chart data available');
    }
    
    if (data.category_data && data.category_data.labels && data.category_data.labels.length > 0) {
        renderPieChart(data.category_data);
    } else {
        console.warn('No category data available');
    }
    
    if (data.product_category_data && data.product_category_data.labels && data.product_category_data.labels.length > 0) {
        renderProductPieChart(data.product_category_data);
    }
}

function renderLineChart(chartData) {
    console.log('Rendering line chart with:', chartData);
    const canvas = document.getElementById('lineChart');
    if (!canvas) {
        console.error('Line chart canvas not found');
        return;
    }
    const ctx = canvas.getContext('2d');
    
    if (lineChart) {
        lineChart.destroy();
    }
    
    lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Sales',
                data: chartData.values,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₱' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

function renderPieChart(categoryData) {
    console.log('Rendering pie chart with:', categoryData);
    const canvas = document.getElementById('pieChart');
    if (!canvas) {
        console.error('Pie chart canvas not found');
        return;
    }
    const ctx = canvas.getContext('2d');
    
    if (pieChart) {
        pieChart.destroy();
    }
    
    const colors = [
        '#667eea', '#764ba2', '#f093fb', '#4facfe',
        '#43e97b', '#fa709a', '#fee140', '#30cfd0'
    ];
    
    pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categoryData.labels.length > 0 ? categoryData.labels : ['No Data'],
            datasets: [{
                data: categoryData.values.length > 0 ? categoryData.values : [1],
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

async function downloadPDF() {
    if (!currentReportData) {
        alert('Please generate a report first');
        return;
    }
    
    const periodType = document.getElementById('periodType').value;
    let params = `period=${periodType}`;
    
    if (periodType === 'day') {
        const date = document.getElementById('filterDate').value;
        params += `&date=${date}`;
    } else if (periodType === 'day_range') {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        params += `&start_date=${startDate}&end_date=${endDate}`;
    } else if (periodType === 'month') {
        const month = document.getElementById('filterMonth').value;
        const year = document.getElementById('filterMonthYear').value;
        params += `&month=${month}&year=${year}`;
    } else if (periodType === 'month_range') {
        const startMonth = document.getElementById('startMonth').value;
        const endMonth = document.getElementById('endMonth').value;
        const year = document.getElementById('rangeYear').value;
        params += `&start_month=${startMonth}&end_month=${endMonth}&year=${year}`;
    } else if (periodType === 'year') {
        const year = document.getElementById('filterYear').value;
        params += `&year=${year}`;
    } else if (periodType === 'year_range') {
        const startYear = document.getElementById('startYear').value;
        const endYear = document.getElementById('endYear').value;
        params += `&start_year=${startYear}&end_year=${endYear}`;
    }
    
    const token = localStorage.getItem('token');
    window.open(`/api/reports/sales/download/pdf?${params}&token=${token}`, '_blank');
}

async function downloadCSV() {
    if (!currentReportData) {
        alert('Please generate a report first');
        return;
    }
    
    const periodType = document.getElementById('periodType').value;
    let params = `period=${periodType}`;
    
    if (periodType === 'day') {
        const date = document.getElementById('filterDate').value;
        params += `&date=${date}`;
    } else if (periodType === 'day_range') {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        params += `&start_date=${startDate}&end_date=${endDate}`;
    } else if (periodType === 'month') {
        const month = document.getElementById('filterMonth').value;
        const year = document.getElementById('filterMonthYear').value;
        params += `&month=${month}&year=${year}`;
    } else if (periodType === 'month_range') {
        const startMonth = document.getElementById('startMonth').value;
        const endMonth = document.getElementById('endMonth').value;
        const year = document.getElementById('rangeYear').value;
        params += `&start_month=${startMonth}&end_month=${endMonth}&year=${year}`;
    } else if (periodType === 'year') {
        const year = document.getElementById('filterYear').value;
        params += `&year=${year}`;
    } else if (periodType === 'year_range') {
        const startYear = document.getElementById('startYear').value;
        const endYear = document.getElementById('endYear').value;
        params += `&start_year=${startYear}&end_year=${endYear}`;
    }
    
    const token = localStorage.getItem('token');
    window.open(`/api/reports/sales/download/csv?${params}&token=${token}`, '_blank');
}

function renderProductPieChart(productData) {
    console.log('Rendering product pie chart with:', productData);
    const canvas = document.getElementById('productPieChart');
    if (!canvas) {
        console.error('Product pie chart canvas not found');
        return;
    }
    const ctx = canvas.getContext('2d');
    
    if (productPieChart) {
        productPieChart.destroy();
    }
    
    const colors = [
        '#667eea', '#764ba2', '#f093fb', '#4facfe',
        '#43e97b', '#fa709a', '#fee140', '#30cfd0'
    ];
    
    productPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: productData.labels.length > 0 ? productData.labels : ['No Data'],
            datasets: [{
                data: productData.values.length > 0 ? productData.values : [1],
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Set default date to today
const now = new Date();
document.getElementById('filterDate').valueAsDate = now;
document.getElementById('startDate').valueAsDate = new Date(now.getFullYear(), now.getMonth(), 1);
document.getElementById('endDate').valueAsDate = now;

// Set default month to current month
document.getElementById('filterMonth').value = now.getMonth() + 1;
document.getElementById('filterMonthYear').value = now.getFullYear();
document.getElementById('startMonth').value = 1;
document.getElementById('endMonth').value = now.getMonth() + 1;
document.getElementById('rangeYear').value = now.getFullYear();
document.getElementById('filterYear').value = now.getFullYear();
document.getElementById('startYear').value = now.getFullYear() - 1;
document.getElementById('endYear').value = now.getFullYear();
