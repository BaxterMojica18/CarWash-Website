/**
 * client-nav.js
 * Injects the mobile bottom navbar on all client pages.
 * Include after api.js on every client HTML page.
 */
(function () {
    // Mark body so CSS can hide sidebar on mobile
    document.body.classList.add('client-page');

    const currentPage = window.location.pathname.split('/').pop() || 'client-dashboard.html';

    const tabs = [
        {
            href: 'client-dashboard.html',
            label: 'Home',
            icon: `<svg viewBox="0 0 24 24"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V9.5z"/><path d="M9 21V12h6v9"/></svg>`
        },
        {
            href: 'shop.html',
            label: 'Shop',
            icon: `<svg viewBox="0 0 24 24"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>`
        },
        {
            href: 'reserve.html',
            label: 'Reserve',
            icon: `<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`
        },
        {
            href: 'cart.html',
            label: 'Cart',
            badge: true,
            icon: `<svg viewBox="0 0 24 24"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>`
        },
        {
            href: 'client-orders.html',
            label: 'Orders',
            icon: `<svg viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12h6"/><path d="M9 16h4"/></svg>`
        }
    ];

    const nav = document.createElement('nav');
    nav.className = 'client-bottom-nav';
    nav.innerHTML = tabs.map(tab => {
        const isActive = currentPage === tab.href || currentPage === tab.href.replace('.html', '');
        return `
            <a href="${tab.href}" class="${isActive ? 'active' : ''}">
                ${tab.icon}
                ${tab.badge ? `<span class="client-nav-badge hidden" id="clientNavCartBadge"></span>` : ''}
                <span>${tab.label}</span>
            </a>`;
    }).join('');

    document.body.appendChild(nav);

    // Load cart count for badge
    async function updateCartBadge() {
        const badge = document.getElementById('clientNavCartBadge');
        if (!badge) return;
        try {
            const token = typeof getToken === 'function' ? getToken() : localStorage.getItem('token');
            if (!token) return;
            const res = await fetch(`${API_BASE}/cart`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!res.ok) return;
            const cart = await res.json();
            const count = cart.reduce((s, i) => s + (i.quantity || 1), 0);
            badge.textContent = count > 99 ? '99+' : count;
            badge.classList.toggle('hidden', count === 0);
        } catch {}
    }

    // Run after DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', updateCartBadge);
    } else {
        updateCartBadge();
    }
})();
