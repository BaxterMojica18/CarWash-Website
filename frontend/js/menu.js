function toggleMenu(event) {
    if (event) event.stopPropagation();
    const sidebar = document.getElementById('sidebar');
    const content = document.querySelector('.content');
    const isMobile = window.innerWidth <= 768;

    if (isMobile) {
        sidebar.classList.toggle('active');
        sidebar.classList.remove('collapsed');
    } else {
        sidebar.classList.toggle('collapsed');
        if (content) content.classList.toggle('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed') ? '1' : '');
    }
    updateToggleButton();
}

function updateToggleButton() {
    const sidebar = document.getElementById('sidebar');
    const btn = document.querySelector('.sidebar-close');
    if (!btn) return;
    
    const isCollapsed = sidebar.classList.contains('collapsed');
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        btn.innerHTML = '✕';
    } else {
        btn.innerHTML = isCollapsed ? '' : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width: 14px; height: 14px;"><path d="M15 18l-6-6 6-6"/></svg>';
    }
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.querySelector('.content');
    const isMobile = window.innerWidth <= 768;

    if (isMobile) {
        sidebar.classList.remove('active');
    } else {
        sidebar.classList.add('collapsed');
        if (content) content.classList.add('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', '1');
    }
    updateToggleButton();
}

// Inject close button into sidebar
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.querySelector('.menu-toggle');
    const isCollapsed = localStorage.getItem('sidebarCollapsed');

    if (isCollapsed) {
        if (sidebar) sidebar.classList.add('collapsed');
        const content = document.querySelector('.content');
        if (content) content.classList.add('sidebar-collapsed');
    }

    if (sidebar) {
        const closeBtn = document.createElement('button');
        closeBtn.className = 'sidebar-close';
        closeBtn.onclick = toggleMenu;
        sidebar.insertBefore(closeBtn, sidebar.firstChild);
        updateToggleButton();
        
        // Inject mobile edge tab to open sidebar
        if (window.innerWidth <= 768) {
            const edgeTab = document.createElement('button');
            edgeTab.className = 'sidebar-edge-tab';
            edgeTab.setAttribute('aria-label', 'Open menu');
            edgeTab.onclick = toggleMenu;
            document.body.appendChild(edgeTab);

            // Hide edge tab when sidebar opens, show when it closes
            const observer = new MutationObserver(() => {
                edgeTab.style.display = sidebar.classList.contains('active') ? 'none' : '';
            });
            observer.observe(sidebar, { attributes: true, attributeFilter: ['class'] });
        }
        
        // Use sidebar click to expand if collapsed
        sidebar.onclick = (e) => {
            if (sidebar.classList.contains('collapsed')) {
                toggleMenu(e);
            }
        };

        // Add smooth transition listener to handle layout shift
        sidebar.addEventListener('transitionend', () => {
             window.dispatchEvent(new Event('resize'));
        });
    }
    
    // Normalize all icons to premium SVGs
    normalizeSidebarIcons();
});

function normalizeSidebarIcons() {
    const icons = {
        'dashboard': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>',
        'invoices': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>',
        'orders': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
        'queue': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        'products': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>',
        'services': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
        'reports': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>',
        'settings': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1Z"/></svg>',
        'logout': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>',
        'tabs': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>',
        'permissions': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
        'shop': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
        'cart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
        'reserve': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
        'myorders': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12h6"/><path d="M9 16h4"/></svg>',
        'coupons': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7v10c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2z"/><path d="M7 5v14"/><path d="M17 5v14"/></svg>'
    };

    const links = document.querySelectorAll('.sidebar ul li a');
    links.forEach(link => {
        const textNode = Array.from(link.childNodes).find(node => node.nodeType === 3);
        const originalText = textNode ? textNode.textContent.trim() : '';
        const lowerText = originalText.toLowerCase();
        
        let key = '';
        if (lowerText.includes('dashboard')) key = 'dashboard';
        else if (lowerText.includes('invoice')) key = 'invoices';
        else if (lowerText.includes('order')) key = 'orders';
        else if (lowerText.includes('queue')) key = 'queue';
        else if (lowerText.includes('product')) key = 'products';
        else if (lowerText.includes('service')) key = 'services';
        else if (lowerText.includes('report')) key = 'reports';
        else if (lowerText.includes('settings')) key = 'settings';
        else if (lowerText.includes('logout')) key = 'logout';
        else if (lowerText.includes('sidebar tabs')) key = 'tabs';
        else if (lowerText.includes('permissions')) key = 'permissions';
        else if (lowerText.includes('my orders')) key = 'myorders';
        else if (lowerText.includes('shop')) key = 'shop';
        else if (lowerText.includes('cart')) key = 'cart';
        else if (lowerText.includes('reserve')) key = 'reserve';
        else if (lowerText.includes('coupon')) key = 'coupons';

        if (key && icons[key]) {
            const iconSpan = link.querySelector('.icon');
            if (iconSpan) {
                iconSpan.innerHTML = icons[key];
            }
            if (textNode) {
                const newSpan = document.createElement('span');
                newSpan.className = 'nav-text';
                newSpan.textContent = originalText;
                textNode.remove();
                link.appendChild(newSpan);
            }
        }
    });
}

// Close menu when clicking outside on mobile
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    
    if (sidebar && sidebar.classList.contains('active')) {
        if (!sidebar.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    }
});

// Predefined Themes (same as settings.js)
const themes = {
    default: { bgColor: '#f5f5f5', textColor: '#333', primaryColor: '#667eea', sidebarColor: '#2c3e50', cardBg: '#ffffff', cardText: '#333' },
    ocean: { bgColor: '#e0f7fa', textColor: '#004d40', primaryColor: '#00acc1', sidebarColor: '#006064', cardBg: '#ffffff', cardText: '#004d40' },
    sunset: { bgColor: '#fff3e0', textColor: '#bf360c', primaryColor: '#ff6f00', sidebarColor: '#e64a19', cardBg: '#ffffff', cardText: '#bf360c' },
    forest: { bgColor: '#f1f8e9', textColor: '#33691e', primaryColor: '#689f38', sidebarColor: '#558b2f', cardBg: '#ffffff', cardText: '#33691e' },
    midnight: { bgColor: '#1a237e', textColor: '#e8eaf6', primaryColor: '#5c6bc0', sidebarColor: '#283593', cardBg: '#3f51b5', cardText: '#ffffff' },
    charcoal: { bgColor: '#212121', textColor: '#e0e0e0', primaryColor: '#ff5722', sidebarColor: '#424242', cardBg: '#424242', cardText: '#ffffff' },
    royal: { bgColor: '#f3e5f5', textColor: '#4a148c', primaryColor: '#ab47bc', sidebarColor: '#6a1b9a', cardBg: '#ffffff', cardText: '#4a148c' },
    crimson: { bgColor: '#1a1a1a', textColor: '#ffebee', primaryColor: '#ef5350', sidebarColor: '#c62828', cardBg: '#424242', cardText: '#ffffff' },
    mint: { bgColor: '#e8f5e9', textColor: '#1b5e20', primaryColor: '#66bb6a', sidebarColor: '#388e3c', cardBg: '#ffffff', cardText: '#1b5e20' },
    slate: { bgColor: '#eceff1', textColor: '#263238', primaryColor: '#546e7a', sidebarColor: '#37474f', cardBg: '#ffffff', cardText: '#263238' }
};

// Pre-apply from storage for performance (prevents white flash)
applyBrandingFromStorage();

// Load business branding and sync with server
async function loadBranding() {
    // 1. Initial load from localStorage (instant)
    applyBrandingFromStorage();
    
    // 2. Fetch latest from API (dynamic sync)
    if (localStorage.getItem('token')) {
        try {
            // Use the API object defined in api.js
            const business = await API.settings.getBusiness();
            if (business) {
                // Sync storage
                localStorage.setItem('businessName', business.business_name || '');
                localStorage.setItem('logo', business.logo || '');
                localStorage.setItem('logoType', business.logo_type || '');
                
                // Real-time update UI
                const nameElement = document.getElementById('sidebarName');
                if (nameElement) nameElement.textContent = business.business_name || '';
                
                const logoElement = document.getElementById('sidebarLogo');
                if (logoElement) {
                    updateSidebarLogo(logoElement, business.logo, business.logo_type);
                }
            } else {
                // No business — hide logo and name
                const nameElement = document.getElementById('sidebarName');
                if (nameElement) nameElement.textContent = '';
                const logoElement = document.getElementById('sidebarLogo');
                if (logoElement) { logoElement.innerHTML = ''; logoElement.style.display = 'none'; }
            }

            const activeTheme = await API.settings.getActiveTheme();
            if (activeTheme) {
                applyThemeColors(activeTheme);
            }
        } catch (e) {
            console.warn("Branding sync failed", e);
        }
    }
}

function applyBrandingFromStorage() {
    const businessName = localStorage.getItem('businessName');
    const logo = localStorage.getItem('logo');
    const logoType = localStorage.getItem('logoType');
    const savedTheme = localStorage.getItem('selectedTheme') || 'default';
    
    const nameElement = document.getElementById('sidebarName');
    if (nameElement) {
        nameElement.textContent = businessName || '';
    }
    
    const logoElement = document.getElementById('sidebarLogo');
    if (logoElement) {
        updateSidebarLogo(logoElement, logo, logoType);
    }

    if (themes[savedTheme]) {
        const theme = themes[savedTheme];
        document.documentElement.style.setProperty('--bg-color', theme.bgColor);
        document.documentElement.style.setProperty('--text-color', theme.textColor);
        document.documentElement.style.setProperty('--primary-color', theme.primaryColor);
        document.documentElement.style.setProperty('--sidebar-color', theme.sidebarColor);
        document.documentElement.style.setProperty('--card-bg', theme.cardBg);
        document.documentElement.style.setProperty('--card-text', theme.cardText);
    }
}

function updateSidebarLogo(el, logo, logoType) {
    if (!logo || !logoType || logoType === 'none') {
        el.innerHTML = '';
        el.style.display = 'none';
        return;
    }
    if (logoType === 'emoji') {
        el.textContent = logo;
        el.style.fontSize = '32px';
    } else if (logoType === 'image') {
        el.innerHTML = `<img src="${logo}" alt="Logo" style="width: 40px; height: 40px; border-radius: 5px; object-fit: contain; transition: transform 0.3s ease;">`;
    }
    el.style.display = 'block';
}

function applyThemeColors(theme) {
    document.documentElement.style.setProperty('--bg-color', theme.bg_color);
    document.documentElement.style.setProperty('--text-color', theme.text_color);
    document.documentElement.style.setProperty('--primary-color', theme.button_color);
    document.documentElement.style.setProperty('--sidebar-color', theme.sidebar_color);
    document.documentElement.style.setProperty('--card-bg', theme.card_color);
    document.documentElement.style.setProperty('--card-text', theme.text_color);
    if (theme.sidebar_active_color) {
        document.documentElement.style.setProperty('--sidebar-active-color', theme.sidebar_active_color);
    }
}

// Initial sync call
loadBranding();

const DEFAULT_TABS = [
    { name: 'Dashboard', href: 'dashboard.html', icon: 'dashboard' },
    { name: 'Invoices', href: 'invoices.html', icon: 'invoices' },
    { name: 'Orders', href: 'order-management.html', icon: 'orders' },
    { name: 'Queue', href: 'queue-management.html', icon: 'queue' },
    { name: 'Products', href: 'products.html', icon: 'products' },
    { name: 'Services', href: 'services.html', icon: 'services' },
    { name: 'Reports', href: 'reports.html', icon: 'reports' },
    { name: 'Settings', href: 'settings.html', icon: 'settings' }
];

loadBranding();

const STAFF_TABS = [
    { name: 'Dashboard', href: 'dashboard.html', icon: 'dashboard' },
    { name: 'Invoices', href: 'invoices.html', icon: 'invoices' },
    { name: 'Orders', href: 'order-management.html', icon: 'orders' },
    { name: 'Queue', href: 'queue-management.html', icon: 'queue' },
    { name: 'Products', href: 'products.html', icon: 'products' },
    { name: 'Services', href: 'services.html', icon: 'services' },
    { name: 'Reports', href: 'reports.html', icon: 'reports' }
];

const CLIENT_TABS = [
    { name: 'Dashboard', href: 'client-dashboard.html', icon: 'dashboard' },
    { name: 'My Orders', href: 'client-orders.html', icon: 'myorders' },
    { name: 'Shop', href: 'shop.html', icon: 'shop' },
    { name: 'Cart', href: 'cart.html', icon: 'cart' },
    { name: 'Reserve', href: 'reserve.html', icon: 'reserve' }
];

async function applySidebarSettings() {
    const token = localStorage.getItem('token');
    const sidebarUl = document.querySelector('.sidebar ul');
    if (!sidebarUl) return;

    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const normalizedPath = currentPath.startsWith('/') ? currentPath : `/${currentPath}`;

    // 1. Initial render from localStorage (Instant)
    const cachedData = localStorage.getItem('user_sidebar_data');
    if (cachedData) {
        try {
            const parsedData = JSON.parse(cachedData);
            const roles = parsedData.roles || [];
            const isClient = roles.includes('client') && !roles.includes('admin') && !roles.includes('staff') && !roles.includes('superadmin') && !roles.includes('owner');
            enforcePageAccess(isClient, roles);
            renderTabs(sidebarUl, parsedData, currentPath, normalizedPath);
        } catch (e) { console.error("Cached sidebar error", e); }
    }

    if (!token) return;

    // 2. Fetch fresh permissions/tabs (Background Sync)
    try {
        const response = await fetch(`${API_BASE}/auth/me/permissions`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) return;
        const data = await response.json();
        
        // Update storage and re-render if needed
        localStorage.setItem('user_sidebar_data', JSON.stringify(data));
        const roles = data.roles || [];
        const isClient = roles.includes('client') && !roles.includes('admin') && !roles.includes('staff') && !roles.includes('superadmin') && !roles.includes('owner');
        enforcePageAccess(isClient, roles);
        renderTabs(sidebarUl, data, currentPath, normalizedPath);

    } catch (e) {
        console.error("Failed to load sidebar settings", e);
    }
}

function enforcePageAccess(isClient, roles) {
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    if (!currentPath || currentPath === 'login.html' || currentPath === 'index.html') return;

    const clientOnlyPages = [
        'client-dashboard.html', 'client-orders.html', 'shop.html', 
        'cart.html', 'reserve.html', 'vouchers.html', 'checkout.html'
    ];
    
    const staffAdminPages = [
        'dashboard.html', 'invoices.html', 'order-management.html', 
        'queue-management.html', 'products.html', 'services.html', 
        'reports.html', 'coupons.html', 'settings.html', 
        'permissions-management.html', 'sidebar-management.html', 
        'coupon-management.html', 'flash-sale-management.html'
    ];
    
    // Restrict Client access to Staff pages
    if (staffAdminPages.includes(currentPath) && isClient) {
        window.location.replace('/client-dashboard.html');
        return;
    }
    
    // Restrict Staff access to Client pages
    if (clientOnlyPages.includes(currentPath) && !isClient) {
        window.location.replace('/dashboard.html');
        return;
    }
    
    // Restrict Staff from Admin-only pages
    const isOwnerOrAdmin = roles.includes('admin') || roles.includes('superadmin') || roles.includes('owner');
    const adminOnlyPages = ['settings.html', 'permissions-management.html', 'sidebar-management.html', 'coupons.html', 'coupon-management.html', 'flash-sale-management.html'];
    
    if (adminOnlyPages.includes(currentPath) && !isOwnerOrAdmin && !isClient) {
        window.location.replace('/dashboard.html');
        return;
    }
}

function renderTabs(sidebarUl, data, currentPath, normalizedPath) {
    sidebarUl.innerHTML = ''; // Clear for fresh render

    const hiddenTabs = (data.hidden_sidebar_tabs || []).map(t => t.toLowerCase());
    const roles = data.roles || [];
    const isClient = roles.includes('client') && !roles.includes('admin') && !roles.includes('staff') && !roles.includes('superadmin') && !roles.includes('owner');
    const isAdminOrOwner = roles.includes('admin') || roles.includes('owner') || roles.includes('superadmin');

    let tabsToRender = isClient ? CLIENT_TABS : STAFF_TABS;
    
    // If the user is admin/owner/superadmin, add Settings and Coupons to their tabs
    if (!isClient && isAdminOrOwner) {
        tabsToRender = [...tabsToRender, 
            { name: 'Coupons', href: 'coupons.html', icon: 'coupons' },
            { name: 'Settings', href: 'settings.html', icon: 'settings' }
        ];
    }

    // 1. Add Role-specific Tabs
    tabsToRender.forEach(tab => {
        if (!hiddenTabs.includes(tab.name.toLowerCase())) {
            const li = document.createElement('li');
            const isActive = (currentPath === tab.href || normalizedPath === `/${tab.href}`) ? 'class="active"' : '';
            li.innerHTML = `<a href="${tab.href}" ${isActive}><span class="icon"></span> ${tab.name}</a>`;
            sidebarUl.appendChild(li);
        }
    });

    // 2. Add Admin/Owner specific modules
    if (!isClient && (roles.includes('superadmin') || roles.includes('admin') || roles.includes('owner'))) {
        const isPermActive = currentPath === 'permissions-management.html';
        const isSidebarActive = currentPath === 'sidebar-management.html';
        const isGroupActive = isPermActive || isSidebarActive;

        const li = document.createElement('li');
        li.className = 'nav-group' + (isGroupActive ? ' open' : '');
        li.innerHTML = `
            <div class="nav-group-header" onclick="this.parentElement.classList.toggle('open')">
                <span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>
                <span class="nav-text">User Management</span>
                <span class="nav-group-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:12px;height:12px"><path d="M6 9l6 6 6-6"/></svg></span>
            </div>
            <ul class="nav-sub">
                ${roles.includes('superadmin') ? `<li><a href="permissions-management.html" ${isPermActive ? 'class="active"' : ''}><span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span><span class="nav-text">Permissions</span></a></li>` : ''}
                <li><a href="sidebar-management.html" ${isSidebarActive ? 'class="active"' : ''}><span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg></span><span class="nav-text">Sidebar Tabs</span></a></li>
            </ul>`;
        sidebarUl.appendChild(li);
    }

    // 3. Add Logout (Always last)
    const logoutLi = document.createElement('li');
    logoutLi.innerHTML = `<a href="login.html" onclick="logout()"><span class="icon"></span> Logout</a>`;
    sidebarUl.appendChild(logoutLi);

    // Finalize icons
    normalizeSidebarIcons();

    // Inject client bottom nav on mobile for client accounts
    if (isClient && window.innerWidth <= 768 && !document.querySelector('.client-bottom-nav')) {
        const s = document.createElement('script');
        s.src = '/js/client-nav.js';
        document.body.appendChild(s);
    }
}

document.addEventListener('DOMContentLoaded', applySidebarSettings);
