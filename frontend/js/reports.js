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
    
    if (periodType === 'day') {
        const date = document.getElementById('filterDate').value;
        if (!date) {
            alert('Please select a date');
            return;
        }
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
        const response = await apiRequest(`/reports/sales?${params}`);
        currentReportData = response;
        displayReport(response);
    } catch (error) {
        console.error('Error generating report:', error);
        alert('Error generating report: ' + error.message);
    }
}

function displayReport(data) {
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
    
    if (data.chart_data && data.chart_data.labels && data.chart_data.labels.length > 0) {
        renderLineChart(data.chart_data);
    }
    
    if (data.category_data && data.category_data.labels && data.category_data.labels.length > 0) {
        renderPieChart(data.category_data);
    }
    
    if (data.product_category_data && data.product_category_data.labels && data.product_category_data.labels.length > 0) {
        renderProductPieChart(data.product_category_data);
    }
}

function renderLineChart(chartData) {
    const canvas = document.getElementById('lineChart');
    if (!canvas) return;
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
    const canvas = document.getElementById('pieChart');
    if (!canvas) return;
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
    const canvas = document.getElementById('productPieChart');
    if (!canvas) return;
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

function showSalesReport() {
    document.getElementById('salesReportSection').style.display = 'block';
    document.getElementById('productStatsSection').style.display = 'none';
    document.getElementById('serviceStatsSection').style.display = 'none';
}

function showProductStats() {
    document.getElementById('salesReportSection').style.display = 'none';
    document.getElementById('productStatsSection').style.display = 'block';
    document.getElementById('serviceStatsSection').style.display = 'none';
    
    const savedFilter = localStorage.getItem('productFilter');
    if (savedFilter) {
        document.getElementById('productFilter').value = savedFilter;
        localStorage.removeItem('productFilter');
        filterProducts();
    }
}

function showServiceStats() {
    document.getElementById('salesReportSection').style.display = 'none';
    document.getElementById('productStatsSection').style.display = 'none';
    document.getElementById('serviceStatsSection').style.display = 'block';
    
    const savedFilter = localStorage.getItem('serviceFilter');
    if (savedFilter) {
        document.getElementById('serviceFilter').value = savedFilter;
        localStorage.removeItem('serviceFilter');
        filterServices();
    }
}

async function filterProducts() {
    const period = document.getElementById('productFilter').value;
    if (!period) {
        document.getElementById('productStatsContent').style.display = 'none';
        return;
    }
    
    const now = new Date();
    let startDate = new Date();
    
    switch(period) {
        case 'weekly': startDate.setDate(now.getDate() - 7); break;
        case 'monthly': startDate.setMonth(now.getMonth() - 1); break;
        case 'quarterly': startDate.setMonth(now.getMonth() - 3); break;
        case 'annually': startDate.setFullYear(now.getFullYear() - 1); break;
    }
    
    const allProducts = await API.products.getAll();
    const allInvoices = await API.invoices.getAll();
    const filteredInvoices = allInvoices.filter(inv => {
        const invDate = new Date(inv.date);
        return invDate >= startDate && invDate <= now;
    });
    
    const productStats = {};
    let totalRevenue = 0, totalSold = 0;
    
    filteredInvoices.forEach(inv => {
        inv.items.forEach(item => {
            const product = allProducts.find(p => p.id === item.product_service_id && p.type === 'product');
            if (product) {
                if (!productStats[product.id]) {
                    productStats[product.id] = { name: product.name, quantity: 0, revenue: 0 };
                }
                productStats[product.id].quantity += item.quantity;
                productStats[product.id].revenue += item.subtotal;
                totalRevenue += item.subtotal;
                totalSold += item.quantity;
            }
        });
    });
    
    let topProduct = 'N/A', maxQuantity = 0;
    Object.values(productStats).forEach(stat => {
        if (stat.quantity > maxQuantity) {
            maxQuantity = stat.quantity;
            topProduct = stat.name;
        }
    });
    
    document.getElementById('productStatsContent').style.display = 'block';
    document.getElementById('totalProductsSold').textContent = totalSold;
    document.getElementById('productsRevenue').textContent = `$${totalRevenue.toFixed(2)}`;
    document.getElementById('topProductName').textContent = topProduct;
    document.getElementById('avgProductSale').textContent = totalSold > 0 ? `$${(totalRevenue / totalSold).toFixed(2)}` : '$0';
    
    document.getElementById('productStatsTable').innerHTML = Object.values(productStats)
        .sort((a, b) => b.quantity - a.quantity)
        .map(stat => `
            <tr>
                <td>${stat.name}</td>
                <td>${stat.quantity}</td>
                <td>$${stat.revenue.toFixed(2)}</td>
                <td>$${(stat.revenue / stat.quantity).toFixed(2)}</td>
            </tr>
        `).join('');
}

async function filterServices() {
    const period = document.getElementById('serviceFilter').value;
    if (!period) {
        document.getElementById('serviceStatsContent').style.display = 'none';
        return;
    }
    
    const now = new Date();
    let startDate = new Date();
    
    switch(period) {
        case 'weekly': startDate.setDate(now.getDate() - 7); break;
        case 'monthly': startDate.setMonth(now.getMonth() - 1); break;
        case 'quarterly': startDate.setMonth(now.getMonth() - 3); break;
        case 'annually': startDate.setFullYear(now.getFullYear() - 1); break;
    }
    
    const allProducts = await API.products.getAll();
    const allInvoices = await API.invoices.getAll();
    const filteredInvoices = allInvoices.filter(inv => {
        const invDate = new Date(inv.date);
        return invDate >= startDate && invDate <= now;
    });
    
    const serviceStats = {};
    let totalRevenue = 0, totalPerformed = 0;
    
    filteredInvoices.forEach(inv => {
        inv.items.forEach(item => {
            const service = allProducts.find(p => p.id === item.product_service_id && p.type === 'service');
            if (service) {
                if (!serviceStats[service.id]) {
                    serviceStats[service.id] = { name: service.name, quantity: 0, revenue: 0 };
                }
                serviceStats[service.id].quantity += item.quantity;
                serviceStats[service.id].revenue += item.subtotal;
                totalRevenue += item.subtotal;
                totalPerformed += item.quantity;
            }
        });
    });
    
    let topService = 'N/A', maxQuantity = 0;
    Object.values(serviceStats).forEach(stat => {
        if (stat.quantity > maxQuantity) {
            maxQuantity = stat.quantity;
            topService = stat.name;
        }
    });
    
    document.getElementById('serviceStatsContent').style.display = 'block';
    document.getElementById('totalServicesPerformed').textContent = totalPerformed;
    document.getElementById('servicesRevenue').textContent = `$${totalRevenue.toFixed(2)}`;
    document.getElementById('topServiceName').textContent = topService;
    document.getElementById('avgServicePrice').textContent = totalPerformed > 0 ? `$${(totalRevenue / totalPerformed).toFixed(2)}` : '$0';
    
    document.getElementById('serviceStatsTable').innerHTML = Object.values(serviceStats)
        .sort((a, b) => b.quantity - a.quantity)
        .map(stat => `
            <tr>
                <td>${stat.name}</td>
                <td>${stat.quantity}</td>
                <td>$${stat.revenue.toFixed(2)}</td>
                <td>$${(stat.revenue / stat.quantity).toFixed(2)}</td>
            </tr>
        `).join('');
}

// Check if navigated from dashboard with filter
const savedFilter = localStorage.getItem('reportFilter');
if (savedFilter) {
    const periodMap = {
        'weekly': { type: 'day_range', days: 7 },
        'biweekly': { type: 'day_range', days: 14 },
        'monthly': { type: 'month', months: 1 },
        'quarterly': { type: 'month_range', months: 3 },
        'semiannually': { type: 'month_range', months: 6 },
        'annually': { type: 'year', years: 1 }
    };
    
    const config = periodMap[savedFilter];
    if (config) {
        document.getElementById('periodType').value = config.type;
        updateFilterFields();
        
        if (config.type === 'year') {
            document.getElementById('filterYear').value = now.getFullYear();
        } else if (config.type === 'month') {
            document.getElementById('filterMonth').value = now.getMonth() + 1;
            document.getElementById('filterMonthYear').value = now.getFullYear();
        } else if (config.type === 'month_range') {
            const startMonth = config.months === 3 ? now.getMonth() - 2 : now.getMonth() - 5;
            document.getElementById('startMonth').value = Math.max(1, startMonth + 1);
            document.getElementById('endMonth').value = now.getMonth() + 1;
            document.getElementById('rangeYear').value = now.getFullYear();
        } else if (config.type === 'day_range') {
            const startDate = new Date(now);
            startDate.setDate(now.getDate() - config.days);
            document.getElementById('startDate').value = startDate.toISOString().split('T')[0];
            document.getElementById('endDate').value = now.toISOString().split('T')[0];
        }
        
        localStorage.removeItem('reportFilter');
        setTimeout(() => generateReport(), 100);
    }
}
