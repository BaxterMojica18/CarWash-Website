let revenueChart = null;

async function loadDashboard(period = 'weekly') {
    try {
        const stats = await API.invoices.getStats();
        const invoices = await API.invoices.getAll();
        
        // Calculate filtered stats based on period
        const filteredData = await filterDataByPeriod(invoices, period);
        
        document.querySelector('.stats-grid').innerHTML = `
            <div class="stat-card" onclick="navigateToReports('${period}')" style="cursor: pointer; --card-accent: #2196f3; --icon-bg: rgba(33, 150, 243, 0.1);">
                <div class="stat-header">
                    <div class="stat-icon">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M7 15h0M2 9h20"/></svg>
                    </div>
                </div>
                <div>
                    <h3>Total Revenue</h3>
                    <p class="stat-value">$${filteredData.totalRevenue.toFixed(2)}</p>
                </div>
            </div>
            <div class="stat-card" onclick="navigateToInvoices('${period}')" style="cursor: pointer; --card-accent: #ffeb3b; --icon-bg: rgba(255, 235, 59, 0.1);">
                <div class="stat-header">
                    <div class="stat-icon">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                    </div>
                </div>
                <div>
                    <h3>Total Invoices</h3>
                    <p class="stat-value">${filteredData.totalInvoices}</p>
                </div>
            </div>
            <div class="stat-card" onclick="navigateToServices()" style="cursor: pointer; --card-accent: #4caf50; --icon-bg: rgba(76, 175, 80, 0.1);">
                <div class="stat-header">
                    <div class="stat-icon">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
                    </div>
                </div>
                <div>
                    <h3>Most Popular Service</h3>
                    <p class="stat-value" style="font-size: 20px;">${filteredData.topService || 'N/A'}</p>
                    <p class="stat-subtext">${filteredData.topServiceCount || 0} sold</p>
                </div>
            </div>
            <div class="stat-card" onclick="navigateToProducts()" style="cursor: pointer; --card-accent: #9c27b0; --icon-bg: rgba(156, 39, 176, 0.1);">
                <div class="stat-header">
                    <div class="stat-icon">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>
                    </div>
                </div>
                <div>
                    <h3>Top Product Sold</h3>
                    <p class="stat-value" style="font-size: 20px;">${filteredData.topProduct || 'N/A'}</p>
                    <p class="stat-subtext">${filteredData.topProductCount || 0} sold</p>
                </div>
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
        if (settings.sidebar_color) document.documentElement.style.setProperty('--sidebar-color', settings.sidebar_color);
        document.querySelector('.content').style.color = settings.text_color || '#333333';
        
        const buttonColor = settings.button_color || settings.primary_color;
        const sidebarActive = settings.sidebar_active_color || '#34495e';
        const style = document.createElement('style');
        style.id = 'dashboard-colors';
        const existingStyle = document.getElementById('dashboard-colors');
        if (existingStyle) existingStyle.remove();
        
        const cardColor = settings.card_color || '#ffffff';
        const cardTextColor = settings.card_text_color || '#333333';
        style.textContent = `
            .btn-primary { background: ${buttonColor} !important; }
            .stat-card { 
                background: ${cardColor} !important;
            }
            .stat-card h3 { color: ${cardTextColor} !important; }
            .stat-card .stat-value { color: ${cardTextColor} !important; }
            .stat-card .stat-subtext { color: ${cardTextColor} !important; opacity: 0.7; }
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
                
                // Set dynamic accent colors and icons based on module type
                let accentColor = 'var(--primary-color)';
                let iconBg = 'rgba(102, 126, 234, 0.1)';
                let iconSvg = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>';

                if (mod.module_type.includes('revenue')) { 
                    accentColor = '#2196f3'; iconBg = 'rgba(33, 150, 243, 0.1)'; 
                    iconSvg = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M7 15h0M2 9h20"/></svg>'; 
                } else if (mod.module_type.includes('invoice')) { 
                    accentColor = '#ffeb3b'; iconBg = 'rgba(255, 235, 59, 0.1)'; 
                    iconSvg = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>'; 
                } else if (mod.module_type.includes('service') || mod.module_type.includes('bay')) { 
                    accentColor = '#4caf50'; iconBg = 'rgba(76, 175, 80, 0.1)'; 
                    iconSvg = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>'; 
                } else if (mod.module_type.includes('product') || mod.module_type.includes('coupon')) { 
                    accentColor = '#9c27b0'; iconBg = 'rgba(156, 39, 176, 0.1)'; 
                    iconSvg = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>'; 
                } else if (mod.module_type.includes('client') || mod.module_type.includes('rating')) {
                    accentColor = '#00bcd4'; iconBg = 'rgba(0, 188, 212, 0.1)';
                    iconSvg = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>';
                } else if (mod.module_type.includes('queue') || mod.module_type.includes('order')) {
                    accentColor = '#ff9800'; iconBg = 'rgba(255, 152, 0, 0.1)';
                    iconSvg = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>';
                }

                card.style.setProperty('--card-accent', accentColor);
                card.style.setProperty('--icon-bg', iconBg);
                
                if (mod.width === 'half') {
                    card.style.gridColumn = 'span 6';
                } else if (mod.width === 'third') {
                    card.style.gridColumn = 'span 4';
                } else if (mod.width === 'quarter') {
                    card.style.gridColumn = 'span 3';
                } else {
                    card.style.gridColumn = 'span 12';
                }
                
                const cardContent = (title, val, sub) => `
                    <div class="stat-header">
                        <div class="stat-icon" style="color: ${accentColor};">${iconSvg}</div>
                    </div>
                    <div>
                        <h3>${title}</h3>
                        <p class="stat-value" ${val.length > 8 ? 'style="font-size: 20px;"' : ''}>${val}</p>
                        ${sub ? `<p class="stat-subtext">${sub}</p>` : ''}
                    </div>
                `;

                const templates = {
                    'revenue_total': cardContent('Total Revenue', '$12,450', '+15%'),
                    'revenue_average': cardContent('Average Revenue', '$1,245', 'Per invoice'),
                    'revenue_weekly': cardContent('Weekly Revenue', '$3,200', '+8%'),
                    'revenue_monthly': cardContent('Monthly Revenue', '$12,800', '+12%'),
                    'revenue_bimonthly': cardContent('Bi-Monthly Revenue', '$25,600', '2 months'),
                    'revenue_semiannual': cardContent('Semi-Annual Revenue', '$76,800', '6 months'),
                    'revenue_annual': cardContent('Annual Revenue', '$153,600', 'Year total'),
                    'invoice_total': cardContent('Total Invoices', '245', 'This month'),
                    'invoice_average': cardContent('Average Invoice', '$85', 'Per transaction'),
                    'orders_completed': cardContent('Completed Orders', '124', 'This month'),
                    'queue_pending': cardContent('Pending Appointments', '7', 'Awaiting service'),
                    'service_total': cardContent('Total Services', '189', 'Completed'),
                    'service_popular': cardContent('Most Popular Service', 'Premium Wash', '87 times'),
                    'product_total': cardContent('Products Sold', '456', 'Total units'),
                    'product_popular': cardContent('Top Product', 'Car Wax', '123 sold'),
                    'client_total': cardContent('Total Clients', '850', 'Registered users'),
                    'client_new': cardContent('New Clients', '45', 'This month'),
                    'rating_average': cardContent('Average Rating', '4.8', 'From 120 reviews'),
                    'coupon_used': cardContent('Coupons Used', '1,240', 'Lifetime redemptions'),
                    'bay_active': cardContent('Active Bays', '3 / 5', 'Currently in use'),
                    'recent_activity': `<h3>Recent Activity</h3><ul class="activity-list" style="max-height: 200px; overflow-y: auto; text-align: left; list-style: none; padding: 0;"><li style="padding: 8px; border-bottom: 1px solid #eee;">✓ Invoice #1023 created - $85</li><li style="padding: 8px; border-bottom: 1px solid #eee;">✓ Bay 2 completed service</li><li style="padding: 8px; border-bottom: 1px solid #eee;">✓ New product added</li><li style="padding: 8px;">✓ Invoice #1022 paid - $120</li></ul>`,
                    'chart': `<h3>${mod.title}</h3><div style="background: #f0f0f0; height: 150px; display: flex; align-items: center; justify-content: center; border-radius: 8px; margin-top: 10px;">Chart Placeholder</div>`,
                    'table': `<h3>${mod.title}</h3><table style="width: 100%; margin-top: 10px; border-collapse: collapse;"><tr style="background: #f8f9fa;"><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Column 1</th><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Column 2</th></tr><tr><td style="padding: 8px; border: 1px solid #ddd;">Data 1</td><td style="padding: 8px; border: 1px solid #ddd;">Data 2</td></tr></table>`
                };
                
                card.innerHTML = templates[mod.module_type] || cardContent(mod.title, 'Data', '');
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
