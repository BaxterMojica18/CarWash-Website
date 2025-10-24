async function loadDashboard() {
    try {
        const stats = await API.invoices.getStats();
        
        document.querySelector('.stats-grid').innerHTML = `
            <div class="stat-card">
                <h3>Total Revenue</h3>
                <p class="stat-value">$${stats.total_revenue.toFixed(2)}</p>
            </div>
            <div class="stat-card">
                <h3>Total Invoices</h3>
                <p class="stat-value">${stats.total_invoices}</p>
            </div>
            <div class="stat-card">
                <h3>Active Locations</h3>
                <p class="stat-value">${stats.active_locations}</p>
            </div>
            <div class="stat-card">
                <h3>Monthly Washes</h3>
                <p class="stat-value">${stats.monthly_wash_count}</p>
            </div>
        `;
        
        const userEmail = localStorage.getItem('userEmail') || 'User';
        document.querySelector('header p').textContent = `Welcome back, ${userEmail}!`;
    } catch (error) {
        console.error('Failed to load dashboard:', error);
    }
}

loadDashboard();
