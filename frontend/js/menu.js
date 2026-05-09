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
        btn.innerHTML = isCollapsed
            ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width: 14px; height: 14px;"><path d="M9 18l6-6-6-6"/></svg>'
            : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width: 14px; height: 14px;"><path d="M15 18l-6-6 6-6"/></svg>';
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
        closeBtn.onclick = (e) => {
            e.stopPropagation();
            toggleMenu(e);
        };
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
        
        // Use sidebar click to expand if collapsed (but not on link clicks that navigate away)
        sidebar.onclick = (e) => {
            if (sidebar.classList.contains('collapsed')) {
                const link = e.target.closest('a');
                if (link && link.getAttribute('href')) {
                    // User clicked a nav link — let it navigate without expanding
                    return;
                }
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
    
    // Inject the Top Navbar
    injectTopNavbar();

    // Load trial banner for authenticated users
    if (localStorage.getItem('token')) {
        const bannerScript = document.createElement('script');
        bannerScript.src = 'js/trial-banner.js';
        bannerScript.onload = function() {
            if (typeof initTrialBanner === 'function') {
                initTrialBanner();
            }
        };
        document.head.appendChild(bannerScript);
    }
});

function getInitials(name) {
    if (!name || !name.trim()) return '?';
    const parts = name.trim().split(/\s+/);
    if (parts.length === 1) return parts[0][0].toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('roles');
    localStorage.removeItem('role');
    localStorage.removeItem('user_sidebar_data');
    window.location.href = 'login.html';
}

function injectTopNavbar() {
    const content = document.querySelector('.content');
    if (!content) return;
    
    // Check if it already exists
    if (document.querySelector('.top-navbar')) return;

    const role = localStorage.getItem('role') || 'User';

    const navbar = document.createElement('div');
    navbar.className = 'top-navbar';
    navbar.style.background = 'var(--sidebar-color)';
    navbar.style.color = '#ffffff';
    let roles = [];
    try {
        const roleStr = localStorage.getItem('roles');
        if (roleStr) roles = JSON.parse(roleStr);
        else roles = [role];
    } catch(e) {
        roles = [role];
    }
    
    // Case-insensitive check for admin/owner
    const isAdmin = roles.some(r => {
        if (!r) return false;
        const lower = r.toLowerCase();
        return lower === 'superadmin' || lower === 'admin' || lower === 'owner';
    });

    // Get profile data from localStorage
    const profileName = localStorage.getItem('profileName') || '';
    const cachedSidebarData = localStorage.getItem('user_sidebar_data');
    let profileEmail = '';
    try {
        if (cachedSidebarData) {
            const parsed = JSON.parse(cachedSidebarData);
            profileEmail = parsed.email || '';
        }
    } catch(e) {}

    const initials = getInitials(profileName);
    const avatarHtml = `<div class="navbar-avatar-initials" style="width:40px;height:40px;border-radius:50%;background:var(--primary-color);color:white;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex-shrink:0;">${initials}</div>`;

    navbar.innerHTML = `
        <div class="top-navbar-left" style="display: flex; align-items: center; gap: 10px;">
            <span id="topNavbarLogo" style="display: flex; align-items: center; justify-content: center; font-size: 24px;"></span>
            <div style="display: flex; flex-direction: column; line-height: 1.2;">
                <h2 id="topNavbarName" style="color: white; font-size: 16px; font-weight: 600; margin: 0; white-space: nowrap; letter-spacing: 0.5px;">CarWash / Portal</h2>
                <span id="topNavbarSubName" style="color: rgba(255,255,255,0.7); font-size: 12px; font-weight: 400; display: none;"></span>
            </div>
        </div>

        <div class="top-navbar-right" style="display: flex; align-items: center; gap: 20px;">
            <div class="search-container" style="position: relative; display: flex; align-items: center;">
                <input type="text" id="topSearchInput" placeholder="Search..." style="width: 0; opacity: 0; transition: all 0.3s ease; background: rgba(255,255,255,0.1); border: none; border-bottom: 1px solid rgba(255,255,255,0.3); color: white; padding: 5px; outline: none; margin-right: 10px; pointer-events: none;">
                <button class="navbar-icon-btn" style="color: white;" onclick="toggleSearchField()">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                </button>
            </div>
            ${isAdmin ? `
            <button class="navbar-icon-btn" style="color: white;" title="Edit Dashboard" onclick="window.location.href='edit-dashboard.html'">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </button>` : ''}
            <button class="navbar-icon-btn" id="notificationBellBtn" style="color: white; position: relative;" onclick="toggleNotificationDropdown(event)">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                <span class="navbar-badge" id="notificationBadge" style="display: none;">0</span>
            </button>
            <div class="profile-dropdown" onclick="this.classList.toggle('active')">
                <button class="profile-btn" style="color: white; display: flex; align-items: center; gap: 10px;">
                    ${avatarHtml}
                    <div style="display: flex; flex-direction: column; align-items: flex-start; line-height: 1.2;">
                        <span class="profile-name" style="color: white; font-size: 13px; font-weight: 600;">${profileName || role}</span>
                        <span style="color: rgba(255,255,255,0.6); font-size: 11px;">${profileEmail}</span>
                    </div>
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
                </button>
                <div class="profile-menu">
                    <a href="#" onclick="openNavbarProfileEdit(event)"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> Edit Profile</a>
                    <a href="settings.html"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg> Settings</a>
                    <div class="profile-menu-divider"></div>
                    <a href="#" onclick="logout()"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg> Logout</a>
                </div>
            </div>
        </div>
    `;

    // Only remove old profile if it exists to clean up
    const oldProfile = document.querySelector('header .profile-dropdown');
    if (oldProfile) oldProfile.remove();

    content.insertBefore(navbar, content.firstChild);
}

// Click outside profile menu to close
document.addEventListener('click', (e) => {
    const dropdown = document.querySelector('.profile-dropdown');
    if (dropdown && !dropdown.contains(e.target)) {
        dropdown.classList.remove('active');
    }
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
        'coupons': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7v10c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2z"/><path d="M7 5v14"/><path d="M17 5v14"/></svg>',
        'flash-sales': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        'users': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
        'payment-methods': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>',
        'tickets': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
        'audit-logs': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
        'tickets': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
        'tickets': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
        'notifications': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>'
    };

    const links = document.querySelectorAll('.sidebar ul li a');
    links.forEach(link => {
        // Skip links inside nav-sub (User Management sub-items)
        if (link.closest('.nav-sub')) return;
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
        else if (lowerText.includes('flash')) key = 'flash-sales';
        else if (lowerText.includes('user')) key = 'users';
        else if (lowerText.includes('payment')) key = 'payment-methods';
        else if (lowerText.includes('audit')) key = 'audit-logs';
        else if (lowerText.includes('ticket')) key = 'tickets';
        else if (lowerText.includes('ticket')) key = 'tickets';
        else if (lowerText.includes('ticket')) key = 'tickets';
        else if (lowerText.includes('notification')) key = 'notifications';

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
                localStorage.setItem('businessSubName', business.business_sub_name || '');
                
                // Real-time update UI
                const nameElement = document.getElementById('topNavbarName');
                if (nameElement) nameElement.textContent = business.business_name || 'CarWash Portal';
                
                const logoElement = document.getElementById('topNavbarLogo');
                if (logoElement) {
                    updateSidebarLogo(logoElement, business.logo, business.logo_type);
                }

                // Update sub-name
                const subNameElement = document.getElementById('topNavbarSubName');
                if (subNameElement) {
                    if (business.business_sub_name && business.business_sub_name.trim()) {
                        subNameElement.textContent = business.business_sub_name;
                        subNameElement.style.display = 'block';
                    } else {
                        subNameElement.style.display = 'none';
                    }
                }
            } else {
                // No business — hide logo and name
                const nameElement = document.getElementById('topNavbarName');
                if (nameElement) nameElement.textContent = 'CarWash Portal';
                const logoElement = document.getElementById('topNavbarLogo');
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
    const businessSubName = localStorage.getItem('businessSubName');
    
    const nameElement = document.getElementById('topNavbarName');
    if (nameElement) {
        nameElement.textContent = businessName || 'CarWash Portal';
    }
    
    const logoElement = document.getElementById('topNavbarLogo');
    if (logoElement) {
        updateSidebarLogo(logoElement, logo, logoType);
    }

    // Apply cached sub-name
    const subNameElement = document.getElementById('topNavbarSubName');
    if (subNameElement) {
        if (businessSubName && businessSubName.trim()) {
            subNameElement.textContent = businessSubName;
            subNameElement.style.display = 'block';
        } else {
            subNameElement.style.display = 'none';
        }
    }

    // Apply cached custom theme colors first (from last API fetch)
    const cachedColors = localStorage.getItem('cachedThemeColors');
    if (cachedColors) {
        try {
            const theme = JSON.parse(cachedColors);
            document.documentElement.style.setProperty('--bg-color', theme.bg_color);
            document.documentElement.style.setProperty('--text-color', theme.text_color);
            document.documentElement.style.setProperty('--primary-color', theme.button_color || theme.sidebar_color);
            document.documentElement.style.setProperty('--sidebar-color', theme.sidebar_color);
            document.documentElement.style.setProperty('--card-bg', theme.card_color);
            document.documentElement.style.setProperty('--card-text', theme.text_color);
            if (theme.sidebar_active_color) {
                document.documentElement.style.setProperty('--sidebar-active-color', theme.sidebar_active_color);
            }
            return; // Custom theme applied, skip predefined fallback
        } catch (e) { /* fall through to predefined themes */ }
    }

    // Fallback to predefined theme if no cached custom colors
    const savedTheme = localStorage.getItem('selectedTheme') || 'default';
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
    document.documentElement.style.setProperty('--primary-color', theme.button_color || theme.sidebar_color);
    document.documentElement.style.setProperty('--sidebar-color', theme.sidebar_color);
    document.documentElement.style.setProperty('--card-bg', theme.card_color);
    document.documentElement.style.setProperty('--card-text', theme.text_color);
    if (theme.sidebar_active_color) {
        document.documentElement.style.setProperty('--sidebar-active-color', theme.sidebar_active_color);
    }
    // Cache theme colors in localStorage for instant apply on next page load
    localStorage.setItem('cachedThemeColors', JSON.stringify({
        bg_color: theme.bg_color,
        text_color: theme.text_color,
        button_color: theme.button_color || theme.sidebar_color,
        sidebar_color: theme.sidebar_color,
        card_color: theme.card_color,
        sidebar_active_color: theme.sidebar_active_color
    }));
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
        'reports.html', 'settings.html', 
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
    const adminOnlyPages = ['settings.html', 'permissions-management.html', 'sidebar-management.html', 'coupon-management.html', 'flash-sale-management.html', 'audit-logs.html'];
    
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
            { name: 'Coupons', href: 'coupon-management.html', icon: 'coupons' },
            { name: 'Settings', href: 'settings.html', icon: 'settings' }
        ];
    }

    // Owner/superadmin only: Tickets tab
    const isOwner = roles.includes('superadmin') || roles.includes('owner');
    if (!isClient && isOwner) {
        tabsToRender = [...tabsToRender, { name: 'Tickets', href: 'tickets.html', icon: 'tickets' }];
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
                ${roles.includes('superadmin') ? `<li><a href="permissions-management.html" ${isPermActive ? 'class="active"' : ''}><span class="nav-text">Permissions</span></a></li>` : ''}
                <li><a href="sidebar-management.html" ${isSidebarActive ? 'class="active"' : ''}><span class="nav-text">Sidebar Tabs</span></a></li>
            </ul>`;
        sidebarUl.appendChild(li);
    }

    // Finalize icons
    normalizeSidebarIcons();

    // Add Collapse Sidebar Button at the bottom
    const sidebar = document.querySelector('.sidebar');
    if (sidebar && !document.querySelector('.sidebar-collapse-btn')) {
        // Add a line divider before the collapse button
        const divider = document.createElement('div');
        divider.className = 'sidebar-divider';
        sidebar.appendChild(divider);

        const collapseBtn = document.createElement('button');
        collapseBtn.className = 'sidebar-collapse-btn';
        collapseBtn.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" style="transition: transform 0.3s ease;">
                <path d="M15 18l-6-6 6-6" />
            </svg>
            <span class="btn-text">COLLAPSE SIDEBAR</span>
        `;
        collapseBtn.onclick = (e) => {
            e.stopPropagation();
            toggleMenu(e);
        };
        sidebar.appendChild(collapseBtn);
    }

    // Re-apply sidebar collapsed state after re-render (fixes tab-switch issue)
    const _sidebar = document.getElementById('sidebar');
    const _content = document.querySelector('.content');
    if (_sidebar && localStorage.getItem('sidebarCollapsed') === '1') {
        _sidebar.classList.add('collapsed');
        if (_content) _content.classList.add('sidebar-collapsed');
    }
    updateToggleButton();

    // Inject client bottom nav on mobile for client accounts
    if (isClient && window.innerWidth <= 768 && !document.querySelector('.client-bottom-nav')) {
        const s = document.createElement('script');
        s.src = '/js/client-nav.js';
        document.body.appendChild(s);
    }
}

window.toggleSearchField = function() {
    const input = document.getElementById('topSearchInput');
    if (input.style.width === '0px' || input.style.width === '') {
        input.style.width = '200px';
        input.style.opacity = '1';
        input.style.pointerEvents = 'auto';
        input.focus();
    } else {
        input.style.width = '0px';
        input.style.opacity = '0';
        input.style.pointerEvents = 'none';
        input.value = '';
    }
};

// ===== Notification Dropdown System =====

function formatRelativeTime(dateStr) {
    const now = new Date();
    const date = new Date(dateStr);
    const diffMs = now - date;
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHour = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHour / 24);

    if (diffSec < 60) return 'just now';
    if (diffMin < 60) return `${diffMin} min ago`;
    if (diffHour < 24) return `${diffHour} hour${diffHour > 1 ? 's' : ''} ago`;
    if (diffDay < 30) return `${diffDay} day${diffDay > 1 ? 's' : ''} ago`;
    return date.toLocaleDateString();
}

async function loadNotificationBadge() {
    const token = getToken();
    if (!token) return;

    try {
        const response = await fetch(`${API_BASE}/notifications?page_size=1`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) return;
        const data = await response.json();
        const badge = document.getElementById('notificationBadge');
        if (!badge) return;

        const count = data.unread_count || 0;
        if (count > 0) {
            badge.textContent = count > 99 ? '99+' : count;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    } catch (e) {
        console.warn('Failed to load notification badge', e);
    }
}

async function toggleNotificationDropdown(event) {
    if (event) event.stopPropagation();

    let dropdown = document.getElementById('notificationDropdown');

    // If dropdown exists, toggle it
    if (dropdown) {
        dropdown.remove();
        return;
    }

    // Create and inject dropdown
    dropdown = document.createElement('div');
    dropdown.id = 'notificationDropdown';
    dropdown.className = 'notification-dropdown';
    dropdown.innerHTML = '<div class="notif-loading" style="padding: 20px; text-align: center; color: #888;">Loading...</div>';

    const bellBtn = document.getElementById('notificationBellBtn');
    if (bellBtn) {
        bellBtn.style.position = 'relative';
        bellBtn.appendChild(dropdown);
    }

    // Inject styles if not already present
    injectNotificationStyles();

    // Fetch notifications
    const token = getToken();
    if (!token) return;

    try {
        const response = await fetch(`${API_BASE}/notifications?page_size=10`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) {
            dropdown.innerHTML = '<div style="padding: 20px; text-align: center; color: #888;">Failed to load notifications</div>';
            return;
        }
        const data = await response.json();
        renderNotificationDropdown(dropdown, data);
    } catch (e) {
        dropdown.innerHTML = '<div style="padding: 20px; text-align: center; color: #888;">Failed to load notifications</div>';
    }
}

function renderNotificationDropdown(dropdown, data) {
    const notifications = data.notifications || [];
    const unreadCount = data.unread_count || 0;

    let html = `
        <div class="notif-header">
            <span class="notif-title">Notifications${unreadCount > 0 ? ` (${unreadCount})` : ''}</span>
            ${unreadCount > 0 ? '<button class="notif-mark-all" onclick="markAllNotificationsRead(event)">Mark all read</button>' : ''}
        </div>
        <div class="notif-list">
    `;

    if (notifications.length === 0) {
        html += '<div class="notif-empty">No notifications yet</div>';
    } else {
        notifications.forEach(notif => {
            const unreadClass = notif.is_read ? '' : ' notif-unread';
            const messagePreview = notif.message && notif.message.length > 60
                ? notif.message.substring(0, 60) + '...'
                : (notif.message || '');
            html += `
                <div class="notif-item${unreadClass}" data-id="${notif.id}" data-link="${notif.link || ''}" onclick="handleNotificationClick(event, ${notif.id}, '${(notif.link || '').replace(/'/g, "\\'")}')">
                    ${!notif.is_read ? '<span class="notif-dot"></span>' : ''}
                    <div class="notif-content">
                        <div class="notif-item-title">${notif.title || 'Notification'}</div>
                        <div class="notif-item-message">${messagePreview}</div>
                        <div class="notif-item-time">${formatRelativeTime(notif.created_at)}</div>
                    </div>
                </div>
            `;
        });
    }

    html += `
        </div>
        <div class="notif-footer">
            <a href="settings.html" class="notif-view-all">View all</a>
        </div>
    `;

    dropdown.innerHTML = html;
}

async function handleNotificationClick(event, notifId, link) {
    event.stopPropagation();
    const token = getToken();
    if (!token) return;

    // Mark as read
    try {
        await fetch(`${API_BASE}/notifications/${notifId}/read`, {
            method: 'PATCH',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    } catch (e) {
        console.warn('Failed to mark notification as read', e);
    }

    // Close dropdown
    const dropdown = document.getElementById('notificationDropdown');
    if (dropdown) dropdown.remove();

    // Refresh badge
    loadNotificationBadge();

    // Navigate if link present
    if (link) {
        window.location.href = link;
    }
}

async function markAllNotificationsRead(event) {
    if (event) event.stopPropagation();
    const token = getToken();
    if (!token) return;

    try {
        await fetch(`${API_BASE}/notifications/read-all`, {
            method: 'PATCH',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    } catch (e) {
        console.warn('Failed to mark all notifications as read', e);
    }

    // Refresh badge
    loadNotificationBadge();

    // Close dropdown
    const dropdown = document.getElementById('notificationDropdown');
    if (dropdown) dropdown.remove();
}

function injectNotificationStyles() {
    if (document.getElementById('notificationDropdownStyles')) return;

    const style = document.createElement('style');
    style.id = 'notificationDropdownStyles';
    style.textContent = `
        .notification-dropdown {
            position: absolute;
            top: 100%;
            right: 0;
            width: 340px;
            max-height: 480px;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.18);
            z-index: 9999;
            overflow: hidden;
            margin-top: 8px;
            animation: notifSlideIn 0.2s ease;
        }
        @keyframes notifSlideIn {
            from { opacity: 0; transform: translateY(-8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .notif-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 16px 10px;
            border-bottom: 1px solid #eee;
        }
        .notif-title {
            font-weight: 600;
            font-size: 15px;
            color: #333;
        }
        .notif-mark-all {
            background: none;
            border: none;
            color: var(--primary-color, #667eea);
            font-size: 13px;
            cursor: pointer;
            font-weight: 500;
            padding: 4px 8px;
            border-radius: 4px;
            transition: background 0.2s;
        }
        .notif-mark-all:hover {
            background: rgba(102, 126, 234, 0.08);
        }
        .notif-list {
            max-height: 360px;
            overflow-y: auto;
        }
        .notif-empty {
            padding: 32px 16px;
            text-align: center;
            color: #999;
            font-size: 14px;
        }
        .notif-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 12px 16px;
            cursor: pointer;
            transition: background 0.15s;
            border-bottom: 1px solid #f5f5f5;
            position: relative;
        }
        .notif-item:hover {
            background: #f8f9fa;
        }
        .notif-item.notif-unread {
            background: #f0f4ff;
        }
        .notif-item.notif-unread:hover {
            background: #e8eeff;
        }
        .notif-dot {
            width: 8px;
            height: 8px;
            min-width: 8px;
            border-radius: 50%;
            background: var(--primary-color, #667eea);
            margin-top: 6px;
        }
        .notif-content {
            flex: 1;
            min-width: 0;
        }
        .notif-item-title {
            font-weight: 600;
            font-size: 13px;
            color: #333;
            margin-bottom: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .notif-item-message {
            font-size: 12px;
            color: #666;
            line-height: 1.4;
            margin-bottom: 3px;
        }
        .notif-item-time {
            font-size: 11px;
            color: #999;
        }
        .notif-footer {
            padding: 10px 16px;
            text-align: center;
            border-top: 1px solid #eee;
        }
        .notif-view-all {
            color: var(--primary-color, #667eea);
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
        }
        .notif-view-all:hover {
            text-decoration: underline;
        }
        .notif-loading {
            padding: 20px;
            text-align: center;
            color: #888;
        }
    `;
    document.head.appendChild(style);
}

// Close notification dropdown when clicking outside
document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('notificationDropdown');
    const bellBtn = document.getElementById('notificationBellBtn');
    if (dropdown && bellBtn && !bellBtn.contains(e.target)) {
        dropdown.remove();
    }
});

// Load notification badge on page load
document.addEventListener('DOMContentLoaded', function() {
    // Small delay to ensure navbar is injected first
    setTimeout(loadNotificationBadge, 500);
});

document.addEventListener('DOMContentLoaded', applySidebarSettings);

// ===== Navbar Profile Edit Modal =====

function openNavbarProfileEdit(e) {
    if (e) e.stopPropagation();
    document.querySelector('.profile-dropdown')?.classList.remove('active');

    if (!document.getElementById('navbarProfileModal')) {
        const modal = document.createElement('div');
        modal.id = 'navbarProfileModal';
        modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:99999;display:flex;align-items:center;justify-content:center;';
        modal.innerHTML = `
            <div style="background:#fff;border-radius:16px;padding:30px;width:360px;max-width:90vw;box-shadow:0 20px 60px rgba(0,0,0,0.3);">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                    <h3 style="margin:0;font-size:18px;color:#2c3e50;">Edit Profile</h3>
                    <button onclick="document.getElementById('navbarProfileModal').remove()" style="background:none;border:none;font-size:20px;cursor:pointer;color:#999;">&times;</button>
                </div>
                <div style="text-align:center;margin-bottom:20px;">
                    <div id="navProfileAvatarPreview" style="width:80px;height:80px;border-radius:50%;background:var(--primary-color,#667eea);color:white;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700;margin:0 auto 10px;overflow:hidden;"></div>
                    <label style="cursor:pointer;color:var(--primary-color,#667eea);font-size:13px;font-weight:500;">
                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-right:4px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                        Upload Photo
                        <input type="file" id="navProfilePhotoInput" accept="image/*" style="display:none;" onchange="previewNavProfilePhoto(this)">
                    </label>
                </div>
                <div style="margin-bottom:14px;">
                    <label style="font-size:13px;font-weight:600;color:#555;display:block;margin-bottom:6px;">Display Name</label>
                    <input id="navProfileName" type="text" style="width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:8px;font-size:14px;box-sizing:border-box;" placeholder="Your name">
                </div>
                <button onclick="saveNavbarProfile()" style="width:100%;padding:12px;background:var(--primary-color,#667eea);color:white;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;">Save Changes</button>
            </div>
        `;
        modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });
        document.body.appendChild(modal);
    }

    // Pre-fill current values
    const name = localStorage.getItem('profileName') || '';
    document.getElementById('navProfileName').value = name;
    const avatar = document.getElementById('navProfileAvatarPreview');
    const photo = localStorage.getItem('profilePhoto');
    if (photo) {
        avatar.innerHTML = `<img src="${photo}" style="width:100%;height:100%;object-fit:cover;">`;
    } else {
        avatar.textContent = getInitials(name) || '?';
    }
}

function previewNavProfilePhoto(input) {
    const file = input.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        const avatar = document.getElementById('navProfileAvatarPreview');
        avatar.innerHTML = `<img src="${e.target.result}" style="width:100%;height:100%;object-fit:cover;">`;
        avatar._pendingPhoto = e.target.result;
    };
    reader.readAsDataURL(file);
}

async function saveNavbarProfile() {
    const name = document.getElementById('navProfileName').value.trim();
    if (!name) return;

    const avatar = document.getElementById('navProfileAvatarPreview');
    const photo = avatar._pendingPhoto || localStorage.getItem('profilePhoto') || null;

    const token = localStorage.getItem('token');
    try {
        const cachedData = JSON.parse(localStorage.getItem('user_sidebar_data') || '{}');
        const role = (cachedData.roles || [])[0] || localStorage.getItem('role') || 'User';

        await fetch(`${API_BASE}/settings/profile`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, role, photo })
        });

        localStorage.setItem('profileName', name);
        if (photo) localStorage.setItem('profilePhoto', photo);

        // Update navbar display
        const nameEl = document.querySelector('.top-navbar .profile-name');
        if (nameEl) nameEl.textContent = name;
        const avatarEl = document.querySelector('.top-navbar .navbar-avatar-initials');
        if (avatarEl) {
            if (photo) {
                avatarEl.innerHTML = `<img src="${photo}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`;
            } else {
                avatarEl.textContent = getInitials(name);
            }
        }

        document.getElementById('navbarProfileModal')?.remove();
        if (typeof showToast === 'function') showToast('Profile updated!', 'success');
    } catch (err) {
        if (typeof showToast === 'function') showToast('Failed to save profile', 'error');
    }
}
