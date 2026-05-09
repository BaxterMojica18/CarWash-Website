/**
 * Trial Banner Component
 * Shows expiring/expired trial notifications for Owner/Admin users.
 * Injected at top of .content area after the top navbar.
 */
function initTrialBanner() {
    'use strict';

    // Only show for authenticated users
    const token = getToken();
    if (!token) return;

    // Only show for Owner/Admin users
    const roles = getUserRolesForBanner();
    const isOwnerAdmin = roles.some(r => {
        const lower = (r || '').toLowerCase();
        return lower === 'owner' || lower === 'admin' || lower === 'superadmin';
    });
    if (!isOwnerAdmin) return;

    // Fetch subscription status and show banner if needed
    API.subscriptions.getStatus().then(function(status) {
        if (!status || !status.status) return;

        // Only show for trial or expired
        if (status.status !== 'trial' && status.status !== 'expired') return;

        let bannerHtml = '';
        let bannerClass = '';

        if (status.status === 'expired') {
            bannerClass = 'trial-banner-expired';
            bannerHtml = buildBannerHTML(
                'Your trial has expired. Subscribe now to continue using all features.',
                'expired'
            );
        } else if (status.status === 'trial') {
            const daysRemaining = status.days_remaining;
            if (daysRemaining === undefined || daysRemaining === null || daysRemaining > 3) return;

            if (daysRemaining <= 1) {
                bannerClass = 'trial-banner-urgent';
                bannerHtml = buildBannerHTML(
                    daysRemaining <= 0
                        ? 'Your trial expires today! Subscribe now to keep access.'
                        : 'Your trial expires tomorrow! Subscribe now to avoid interruption.',
                    'urgent'
                );
            } else {
                bannerClass = 'trial-banner-warning';
                bannerHtml = buildBannerHTML(
                    `Your trial expires in ${daysRemaining} days. Subscribe now to continue.`,
                    'warning'
                );
            }
        }

        if (!bannerHtml) return;

        // Inject banner
        const content = document.querySelector('.content');
        if (!content) return;

        // Remove existing banner if any
        const existing = document.querySelector('.trial-banner');
        if (existing) existing.remove();

        const bannerEl = document.createElement('div');
        bannerEl.className = 'trial-banner ' + bannerClass;
        bannerEl.innerHTML = bannerHtml;
        bannerEl.style.cssText = getBannerStyles(bannerClass);

        // Insert after top navbar
        const topNavbar = content.querySelector('.top-navbar');
        if (topNavbar && topNavbar.nextSibling) {
            content.insertBefore(bannerEl, topNavbar.nextSibling);
        } else {
            content.insertBefore(bannerEl, content.firstChild);
        }
    }).catch(function(e) {
        console.warn('Trial banner: could not fetch status', e);
    });
}

function getUserRolesForBanner() {
    try {
        const rolesStr = localStorage.getItem('roles');
        if (rolesStr) return JSON.parse(rolesStr);
    } catch(e) {}
    try {
        const sidebarData = localStorage.getItem('user_sidebar_data');
        if (sidebarData) {
            const parsed = JSON.parse(sidebarData);
            if (parsed.roles) return parsed.roles;
        }
    } catch(e) {}
    return [];
}

function buildBannerHTML(message, type) {
    const icon = type === 'expired'
        ? '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>'
        : '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>';

    return `
        <div style="display:flex;align-items:center;gap:10px;flex:1;">
            ${icon}
            <span>${message}</span>
        </div>
        <a href="/plan-selection.html" style="color:inherit;font-weight:700;text-decoration:none;white-space:nowrap;padding:6px 14px;border-radius:6px;background:rgba(0,0,0,0.1);transition:background 0.2s;">Subscribe Now</a>
    `;
}

function getBannerStyles(bannerClass) {
    let bg, color;
    if (bannerClass === 'trial-banner-expired' || bannerClass === 'trial-banner-urgent') {
        bg = '#f8d7da';
        color = '#721c24';
    } else {
        bg = '#fff3cd';
        color = '#856404';
    }
    return `display:flex;align-items:center;justify-content:space-between;padding:12px 20px;background:${bg};color:${color};border-radius:8px;margin-bottom:15px;font-size:14px;font-weight:500;gap:15px;flex-wrap:wrap;`;
}
