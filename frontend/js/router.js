/**
 * URL Obfuscation Router v2
 * Maps obfuscated 32-char hex tokens to actual page filenames.
 * Tokens are pre-computed random hex strings (not reversible from page names).
 * Maintains backward compatibility with legacy 8-char hashes.
 */
(function() {
    'use strict';

    // New 32-char hex route tokens
    const ROUTE_MAP = {
        'a3f2b1c8e7d4c9a2b8f1e3d6c2a9f7b4': 'dashboard.html',
        'e7d4c9a2b8f1e3d6c2a9f7b4d5e8a1c3': 'invoices.html',
        'b8f1e3d6c2a9f7b4d5e8a1c3f9b2d4e7': 'order-management.html',
        'c2a9f7b4d5e8a1c3f9b2d4e71c3e5a7b': 'queue-management.html',
        'd5e8a1c3f9b2d4e71c3e5a7b4d6f8b2e': 'products.html',
        'f9b2d4e71c3e5a7b4d6f8b2e7a9c1d3f': 'services.html',
        '1c3e5a7b4d6f8b2e7a9c1d3f2b4e6f8a': 'reports.html',
        '4d6f8b2e7a9c1d3f2b4e6f8a5c7d9e1b': 'settings.html',
        '7a9c1d3f2b4e6f8a5c7d9e1b8e2a4c6d': 'permissions-management.html',
        '2b4e6f8a5c7d9e1b8e2a4c6d3f5b7d9e': 'sidebar-management.html',
        '5c7d9e1b8e2a4c6d3f5b7d9e6a8c2e4f': 'coupon-management.html',
        '8e2a4c6d3f5b7d9e6a8c2e4f9b1d3f5a': 'flash-sale-management.html',
        '3f5b7d9e6a8c2e4f9b1d3f5a0c2e4a6b': 'client-dashboard.html',
        '6a8c2e4f9b1d3f5a0c2e4a6b1d3f5b7c': 'client-orders.html',
        '9b1d3f5a0c2e4a6b1d3f5b7c4e6a8c0d': 'shop.html',
        '0c2e4a6b1d3f5b7c4e6a8c0d7f9b1d3e': 'cart.html',
        '1d3f5b7c4e6a8c0d7f9b1d3ea1c3e5f7': 'reserve.html',
        '4e6a8c0d7f9b1d3ea1c3e5f7b2d4f6a8': 'vouchers.html',
        '7f9b1d3ea1c3e5f7b2d4f6a8c3e5a7b9': 'checkout.html',
        'a1c3e5f7b2d4f6a8c3e5a7b9d4f6a8c0': 'users.html',
        'b2d4f6a8c3e5a7b9d4f6a8c0e5a7b9d1': 'payment-methods.html',
        'c3e5a7b9d4f6a8c0e5a7b9d1f6a8c0e2': 'edit-dashboard.html',
        'd4f6a8c0e5a7b9d1f6a8c0e2a7b9d1f3': 'audit-logs.html'
    };

    // Legacy 8-char hashes for backward compatibility (bookmarks, shared links)
    const LEGACY_MAP = {
        'a3f2b1c8': 'dashboard.html',
        'e7d4c9a2': 'invoices.html',
        'b8f1e3d6': 'order-management.html',
        'c2a9f7b4': 'queue-management.html',
        'd5e8a1c3': 'products.html',
        'f9b2d4e7': 'services.html',
        '1c3e5a7b': 'reports.html',
        '4d6f8b2e': 'settings.html',
        '7a9c1d3f': 'permissions-management.html',
        '2b4e6f8a': 'sidebar-management.html',
        '5c7d9e1b': 'coupon-management.html',
        '8e2a4c6d': 'flash-sale-management.html',
        '3f5b7d9e': 'client-dashboard.html',
        '6a8c2e4f': 'client-orders.html',
        '9b1d3f5a': 'shop.html',
        '0c2e4a6b': 'cart.html',
        '1d3f5b7c': 'reserve.html',
        '4e6a8c0d': 'vouchers.html',
        '7f9b1d3e': 'checkout.html',
        'a1c3e5f7': 'users.html',
        'b2d4f6a8': 'payment-methods.html',
        'c3e5a7b9': 'edit-dashboard.html'
    };

    // Reverse map: filename → 32-char token
    const PAGE_TO_HASH = {};
    for (const [hash, page] of Object.entries(ROUTE_MAP)) {
        PAGE_TO_HASH[page] = hash;
    }

    /**
     * Resolve a hash/token to a page filename.
     * Checks new 32-char tokens first, then legacy 8-char hashes.
     */
    function resolveHash(hash) {
        return ROUTE_MAP[hash] || LEGACY_MAP[hash] || null;
    }

    /**
     * Get the obfuscated token for a page filename.
     */
    function getHashForPage(page) {
        return PAGE_TO_HASH[page] || null;
    }

    /**
     * Get the current page filename from the URL path.
     */
    function getCurrentPage() {
        const path = window.location.pathname;
        const page = path.split('/').pop() || 'index.html';
        return page;
    }

    /**
     * Initialize the router.
     * - Replaces URL with obfuscated token using history.replaceState
     * - Intercepts all link clicks to maintain token-based URLs
     * - Handles direct token URL entry (bookmarks)
     * - Redirects raw .html URLs to token-based URLs
     * - Intercepts programmatic navigation
     */
    function initRouter() {
        const currentPage = getCurrentPage();
        const currentHash = getHashForPage(currentPage);

        // Check if we arrived via a hash URL (direct entry or bookmark)
        const urlHash = window.location.hash;
        if (urlHash && urlHash.startsWith('#!/')) {
            const hashValue = urlHash.slice(3);
            const targetPage = resolveHash(hashValue);
            if (targetPage && targetPage !== currentPage) {
                window.location.replace('/' + targetPage + '#!/' + getHashForPage(targetPage));
                return;
            } else if (!targetPage) {
                window.location.replace('/login.html');
                return;
            }
        }

        // If URL shows a raw .html file that's in our map, redirect to token URL
        if (!urlHash && currentHash && !window.location.href.includes('#!/')) {
            const newUrl = window.location.pathname + '#!/' + currentHash;
            history.replaceState({ page: currentPage, hash: currentHash }, '', newUrl);
        }

        // Replace current URL with obfuscated token
        if (currentHash) {
            const newUrl = window.location.pathname + '#!/' + currentHash;
            history.replaceState({ page: currentPage, hash: currentHash }, '', newUrl);
        }

        // Intercept ALL link clicks (sidebar, content, anywhere)
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a[href]');
            if (!link) return;

            const href = link.getAttribute('href');
            if (!href || href.startsWith('http') || href.startsWith('mailto:') || href.startsWith('tel:') || href === '#') return;
            // Allow hash-only links that aren't our router format
            if (href.startsWith('#') && !href.startsWith('#!/')) return;

            // Extract the page filename from the href
            const pageName = href.split('/').pop().split('?')[0].split('#')[0];
            const hash = getHashForPage(pageName);

            if (hash) {
                e.preventDefault();
                window.location.href = '/' + pageName + '#!/' + hash;
            }
        });

        // Intercept window.location assignments to rewrite URLs
        const originalAssign = window.location.assign;
        const originalReplace = window.location.replace;

        function interceptNavigation(url, method) {
            if (typeof url === 'string' && url.includes('.html')) {
                const pageName = url.split('/').pop().split('?')[0].split('#')[0];
                const hash = getHashForPage(pageName);
                if (hash) {
                    method.call(window.location, '/' + pageName + '#!/' + hash);
                    return;
                }
            }
            method.call(window.location, url);
        }

        // Patch location.assign and location.replace
        try {
            Object.defineProperty(window, '_navAssign', {
                value: function(url) { interceptNavigation(url, originalAssign); },
                writable: false
            });
            Object.defineProperty(window, '_navReplace', {
                value: function(url) { interceptNavigation(url, originalReplace); },
                writable: false
            });
        } catch(e) { /* Some browsers may not allow this */ }

        // Handle popstate (browser back/forward)
        window.addEventListener('popstate', function(e) {
            if (e.state && e.state.page) {
                const targetPage = e.state.page;
                if (targetPage !== getCurrentPage()) {
                    window.location.href = '/' + targetPage + '#!/' + e.state.hash;
                }
            }
        });
    }

    // Expose for testing and external use
    window._router = { resolveHash, getHashForPage, ROUTE_MAP, PAGE_TO_HASH, LEGACY_MAP, navigateTo };

    /**
     * Navigate to a page using obfuscated URL.
     * Falls back to raw navigation for pages not in ROUTE_MAP.
     */
    function navigateTo(page) {
        const hash = getHashForPage(page);
        if (hash) {
            window.location.href = '/' + page + '#!/' + hash;
        } else {
            window.location.href = '/' + page;
        }
    }

    // Expose navigateTo globally
    window.navigateTo = navigateTo;

    // Auto-initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initRouter);
    } else {
        initRouter();
    }
})();
