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

async function applyDashboardSettings() {
    try {
        const meResponse = await fetch(`${API_BASE}/auth/me/permissions`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const meData = await meResponse.json();
        if (meData.roles && meData.roles.includes('superadmin')) {
            document.getElementById('floatingEditBtn').style.display = 'block';
        }
        
        const response = await fetch(`${API_BASE}/dashboard/settings`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const settings = await response.json();
        
        document.documentElement.style.setProperty('--primary-color', settings.primary_color);
        document.documentElement.style.setProperty('--bg-color', settings.background_color);
        document.querySelector('.sidebar').style.background = settings.sidebar_color;
        document.querySelector('.content').style.color = settings.text_color || '#333333';
        document.getElementById('sidebarName').textContent = settings.website_name;
        document.getElementById('sidebarLogo').textContent = '🚗';
        
        const buttonColor = settings.button_color || settings.primary_color;
        const sidebarActive = settings.sidebar_active_color || '#34495e';
        const style = document.createElement('style');
        style.id = 'dashboard-colors';
        const existingStyle = document.getElementById('dashboard-colors');
        if (existingStyle) existingStyle.remove();
        
        const cardColor = settings.card_color || '#ffffff';
        const cardTextColor = settings.card_text_color || '#333333';
        style.textContent = `
            .btn-primary, button { background: ${buttonColor} !important; }
            .stat-card { 
                background: ${cardColor} !important;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
                border-left: 4px solid ${settings.primary_color} !important;
            }
            .stat-card h3 { color: ${cardTextColor} !important; font-size: 14px !important; }
            .stat-card .stat-value { color: ${cardTextColor} !important; font-size: 32px !important; font-weight: bold !important; }
            .stat-card .stat-change { 
                display: inline-block;
                padding: 4px 8px;
                background: #f0f0f0;
                border-radius: 4px;
                font-size: 12px;
                color: ${cardTextColor};
            }
            .sidebar a.active, .sidebar a:hover { background: ${sidebarActive} !important; }
        `;
        document.head.appendChild(style);
        
        return await loadCustomModules(settings.layout_type);
    } catch (error) {
        console.error('Failed to apply dashboard settings:', error);
        return false;
    }
}

function adjustColor(color, percent) {
    const num = parseInt(color.replace('#', ''), 16);
    const amt = Math.round(2.55 * percent);
    const R = (num >> 16) + amt;
    const G = (num >> 8 & 0x00FF) + amt;
    const B = (num & 0x0000FF) + amt;
    return '#' + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (G<255?G<1?0:G:255)*0x100 + (B<255?B<1?0:B:255)).toString(16).slice(1);
}

async function loadCustomModules(layoutType) {
    try {
        const response = await fetch(`${API_BASE}/dashboard/modules`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const modules = await response.json();
        
        if (modules && modules.length > 0) {
            const statsGrid = document.querySelector('.stats-grid');
            statsGrid.innerHTML = '';
            statsGrid.style.display = 'grid';
            statsGrid.style.gap = '20px';
            
            if (layoutType === 'list') {
                statsGrid.style.gridTemplateColumns = '1fr';
            } else if (layoutType === 'compact') {
                statsGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(200px, 1fr))';
            } else {
                statsGrid.style.gridTemplateColumns = 'repeat(12, 1fr)';
            }
            
            modules.filter(m => m.is_visible).sort((a, b) => a.position - b.position).forEach(mod => {
                const card = document.createElement('div');
                card.className = 'stat-card';
                card.style.cursor = 'pointer';
                
                if (mod.width === 'half') {
                    card.style.gridColumn = 'span 6';
                } else if (mod.width === 'third') {
                    card.style.gridColumn = 'span 4';
                } else if (mod.width === 'quarter') {
                    card.style.gridColumn = 'span 3';
                } else {
                    card.style.gridColumn = 'span 12';
                }
                
                const templates = {
                    'revenue_total': `<h3>Total Revenue</h3><p class="stat-value">$12,450</p><span class="stat-change positive">+15%</span>`,
                    'revenue_average': `<h3>Average Revenue</h3><p class="stat-value">$1,245</p><span class="stat-change">Per invoice</span>`,
                    'revenue_weekly': `<h3>Weekly Revenue</h3><p class="stat-value">$3,200</p><span class="stat-change positive">+8%</span>`,
                    'revenue_monthly': `<h3>Monthly Revenue</h3><p class="stat-value">$12,800</p><span class="stat-change positive">+12%</span>`,
                    'revenue_bimonthly': `<h3>Bi-Monthly Revenue</h3><p class="stat-value">$25,600</p><span class="stat-change">2 months</span>`,
                    'revenue_semiannual': `<h3>Semi-Annual Revenue</h3><p class="stat-value">$76,800</p><span class="stat-change">6 months</span>`,
                    'revenue_annual': `<h3>Annual Revenue</h3><p class="stat-value">$153,600</p><span class="stat-change">Year total</span>`,
                    'invoice_total': `<h3>Total Invoices</h3><p class="stat-value">245</p><span class="stat-change">This month</span>`,
                    'invoice_average': `<h3>Average Invoice</h3><p class="stat-value">$85</p><span class="stat-change">Per transaction</span>`,
                    'service_total': `<h3>Total Services</h3><p class="stat-value">189</p><span class="stat-change">Completed</span>`,
                    'service_popular': `<h3>Most Popular Service</h3><p class="stat-value" style="font-size: 20px;">Premium Wash</p><span class="stat-change">87 times</span>`,
                    'product_total': `<h3>Products Sold</h3><p class="stat-value">456</p><span class="stat-change">Total units</span>`,
                    'product_popular': `<h3>Top Product</h3><p class="stat-value" style="font-size: 20px;">Car Wax</p><span class="stat-change">123 sold</span>`,
                    'recent_activity': `<h3>Recent Activity</h3><ul class="activity-list" style="max-height: 200px; overflow-y: auto; text-align: left; list-style: none; padding: 0;"><li style="padding: 8px; border-bottom: 1px solid #eee;">✓ Invoice #1023 created - $85</li><li style="padding: 8px; border-bottom: 1px solid #eee;">✓ Bay 2 completed service</li><li style="padding: 8px; border-bottom: 1px solid #eee;">✓ New product added</li><li style="padding: 8px;">✓ Invoice #1022 paid - $120</li></ul>`,
                    'chart': `<h3>${mod.title}</h3><div style="background: #f0f0f0; height: 150px; display: flex; align-items: center; justify-content: center; border-radius: 8px; margin-top: 10px;">Chart Placeholder</div>`,
                    'table': `<h3>${mod.title}</h3><table style="width: 100%; margin-top: 10px; border-collapse: collapse;"><tr style="background: #f8f9fa;"><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Column 1</th><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Column 2</th></tr><tr><td style="padding: 8px; border: 1px solid #ddd;">Data 1</td><td style="padding: 8px; border: 1px solid #ddd;">Data 2</td></tr></table>`
                };
                
                card.innerHTML = templates[mod.module_type] || `<h3>${mod.title}</h3><p class="stat-value">Module content</p>`;
                statsGrid.appendChild(card);
            });
            return true;
        }
        return false;
    } catch (error) {
        console.error('Failed to load custom modules:', error);
        return false;
    }
}

applyDashboardSettings().then(hasCustomModules => {
    if (hasCustomModules) {
        document.querySelector('.charts-section').style.display = 'none';
        document.getElementById('dashboardFilter').parentElement.style.display = 'none';
    } else {
        loadDashboard();
    }
    loadProfile();
});
