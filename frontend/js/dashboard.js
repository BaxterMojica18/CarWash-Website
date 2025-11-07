let revenueChart = null;

async function loadDashboard(period = 'weekly') {
    try {
        const stats = await API.invoices.getStats();
        const invoices = await API.invoices.getAll();
        
        // Calculate filtered stats based on period
        const filteredData = await filterDataByPeriod(invoices, period);
        
        document.querySelector('.stats-grid').innerHTML = `
            <div class="stat-card" onclick="navigateToReports('${period}')" style="cursor: pointer;">
                <h3>Total Revenue</h3>
                <p class="stat-value">$${filteredData.totalRevenue.toFixed(2)}</p>
            </div>
            <div class="stat-card" onclick="navigateToInvoices('${period}')" style="cursor: pointer;">
                <h3>Total Invoices</h3>
                <p class="stat-value">${filteredData.totalInvoices}</p>
            </div>
            <div class="stat-card" onclick="navigateToServices()" style="cursor: pointer;">
                <h3>Most Popular Service</h3>
                <p class="stat-value" style="font-size: 20px;">${filteredData.topService || 'N/A'}</p>
                <span class="stat-change">${filteredData.topServiceCount || 0} sold</span>
            </div>
            <div class="stat-card" onclick="navigateToProducts()" style="cursor: pointer;">
                <h3>Top Product Sold</h3>
                <p class="stat-value" style="font-size: 20px;">${filteredData.topProduct || 'N/A'}</p>
                <span class="stat-change">${filteredData.topProductCount || 0} sold</span>
            </div>
        `;
        
        // Update chart title
        const titles = {
            'weekly': 'Weekly Revenue',
            'biweekly': 'Bi-Weekly Revenue',
            'monthly': 'Monthly Revenue',
            'quarterly': 'Quarterly Revenue',
            'semiannually': 'Semi-Annual Revenue',
            'annually': 'Annual Revenue'
        };
        document.getElementById('revenueChartTitle').textContent = titles[period] || 'Revenue';
        
        // Render chart
        renderRevenueChart(filteredData.chartData);
        loadProfile();
    } catch (error) {
        console.error('Failed to load dashboard:', error);
    }
}

async function filterDataByPeriod(invoices, period) {
    const now = new Date();
    let startDate = new Date();
    
    // Calculate start date based on period
    switch(period) {
        case 'weekly':
            startDate.setDate(now.getDate() - 7);
            break;
        case 'biweekly':
            startDate.setDate(now.getDate() - 14);
            break;
        case 'monthly':
            startDate.setMonth(now.getMonth() - 1);
            break;
        case 'quarterly':
            startDate.setMonth(now.getMonth() - 3);
            break;
        case 'semiannually':
            startDate.setMonth(now.getMonth() - 6);
            break;
        case 'annually':
            startDate.setFullYear(now.getFullYear() - 1);
            break;
    }
    
    // Filter invoices
    const filtered = invoices.filter(inv => {
        const invDate = new Date(inv.date);
        return invDate >= startDate && invDate <= now;
    });
    
    // Calculate totals
    const totalRevenue = filtered.reduce((sum, inv) => sum + inv.total_amount, 0);
    const totalInvoices = filtered.length;
    const avgPerInvoice = totalInvoices > 0 ? totalRevenue / totalInvoices : 0;
    
    // Get products to determine top service and product
    const products = await API.products.getAll();
    const productMap = {};
    products.forEach(p => productMap[p.id] = p);
    
    // Count services and products
    const serviceCounts = {};
    const productCounts = {};
    
    filtered.forEach(inv => {
        inv.items.forEach(item => {
            const product = productMap[item.product_service_id];
            if (product) {
                if (product.type === 'service') {
                    serviceCounts[product.name] = (serviceCounts[product.name] || 0) + item.quantity;
                } else {
                    productCounts[product.name] = (productCounts[product.name] || 0) + item.quantity;
                }
            }
        });
    });
    
    // Find top service and product
    let topService = 'N/A';
    let topServiceCount = 0;
    Object.entries(serviceCounts).forEach(([name, count]) => {
        if (count > topServiceCount) {
            topService = name;
            topServiceCount = count;
        }
    });
    
    let topProduct = 'N/A';
    let topProductCount = 0;
    Object.entries(productCounts).forEach(([name, count]) => {
        if (count > topProductCount) {
            topProduct = name;
            topProductCount = count;
        }
    });
    
    // Prepare chart data
    const chartData = prepareChartData(filtered, period);
    
    return { totalRevenue, totalInvoices, avgPerInvoice, chartData, topService, topServiceCount, topProduct, topProductCount };
}

function prepareChartData(invoices, period) {
    const dataMap = {};
    
    invoices.forEach(inv => {
        const date = new Date(inv.date);
        let key;
        
        if (period === 'weekly' || period === 'biweekly') {
            key = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        } else if (period === 'monthly' || period === 'quarterly') {
            key = date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
        } else {
            key = date.toLocaleDateString('en-US', { year: 'numeric' });
        }
        
        dataMap[key] = (dataMap[key] || 0) + inv.total_amount;
    });
    
    return {
        labels: Object.keys(dataMap),
        values: Object.values(dataMap)
    };
}

function renderRevenueChart(chartData) {
    const ctx = document.getElementById('revenueChart');
    
    if (revenueChart) {
        revenueChart.destroy();
    }
    
    revenueChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Revenue',
                data: chartData.values,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6
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
                            return '$' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

function loadProfile() {
    const name = localStorage.getItem('profileName') || 'Demo User';
    const role = localStorage.getItem('profileRole') || 'Admin';
    const photo = localStorage.getItem('profilePhoto');
    
    // Placeholder user icon SVG
    const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiBmaWxsPSIjNjY3ZWVhIi8+CjxjaXJjbGUgY3g9IjUwIiBjeT0iMzUiIHI9IjE1IiBmaWxsPSJ3aGl0ZSIvPgo8cGF0aCBkPSJNMjAgNzVDMjAgNjUgMzAgNTUgNTAgNTVDNzAgNTUgODAgNjUgODAgNzVWODVIMjBWNzVaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4=';
    
    document.getElementById('profileName').textContent = name;
    document.getElementById('profileRole').textContent = role;
    
    const profileImg = photo || placeholderImage;
    document.getElementById('profilePhoto').src = profileImg;
    document.getElementById('menuProfilePhoto').src = profileImg;
}

function toggleProfileMenu() {
    const menu = document.getElementById('profileMenu');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
}

function showEditProfile() {
    document.getElementById('editProfileModal').style.display = 'block';
    document.getElementById('editName').value = localStorage.getItem('profileName') || 'Demo User';
    document.getElementById('editRole').value = localStorage.getItem('profileRole') || 'Admin';
    
    const photo = localStorage.getItem('profilePhoto');
    if (photo) {
        document.getElementById('photoPreview').src = photo;
        document.getElementById('photoPreview').style.display = 'block';
    }
    
    toggleProfileMenu();
}

function closeEditProfile() {
    document.getElementById('editProfileModal').style.display = 'none';
}

document.getElementById('editPhoto').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            document.getElementById('photoPreview').src = event.target.result;
            document.getElementById('photoPreview').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('profileForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('editName').value;
    const role = document.getElementById('editRole').value;
    const photo = document.getElementById('photoPreview').src;
    
    localStorage.setItem('profileName', name);
    localStorage.setItem('profileRole', role);
    if (photo && photo !== window.location.href) {
        localStorage.setItem('profilePhoto', photo);
    }
    
    loadProfile();
    closeEditProfile();
    alert('Profile updated successfully!');
});

// Close profile menu when clicking outside
document.addEventListener('click', function(event) {
    const profileDropdown = document.querySelector('.profile-dropdown');
    const profileMenu = document.getElementById('profileMenu');
    
    if (profileDropdown && !profileDropdown.contains(event.target)) {
        profileMenu.style.display = 'none';
    }
});

function filterDashboard() {
    const period = document.getElementById('dashboardFilter').value;
    loadDashboard(period);
}

function navigateToReports(period) {
    localStorage.setItem('reportFilter', period);
    window.location.href = 'reports.html';
}

function navigateToInvoices(period) {
    localStorage.setItem('invoiceFilter', period);
    window.location.href = 'invoices.html';
}

function navigateToServices() {
    const period = document.getElementById('dashboardFilter').value;
    localStorage.setItem('serviceFilter', period);
    window.location.href = 'services.html';
}

function navigateToProducts() {
    const period = document.getElementById('dashboardFilter').value;
    localStorage.setItem('productFilter', period);
    window.location.href = 'products.html';
}

loadDashboard();
