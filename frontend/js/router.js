/**
 * URL Obfuscation Router
 * Maps obfuscated hash identifiers to actual page filenames.
 * Hashes are pre-computed random hex strings (not reversible from page names).
 */
(function() {
    'use strict';

    const ROUTE_MAP = {
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

    // Reverse map: filename → hash
    const PAGE_TO_HASH = {};
    for (const [hash, page] of Object.entries(ROUTE_MAP)) {
        PAGE_TO_HASH[page] = hash;
    }

    /**
     * Resolve a hash to a page filename.
     * @param {string} hash - The obfuscated hash (without #!/)
     * @returns {string|null} The page filename or null if invalid
     */
    function resolveHash(hash) {
        return ROUTE_MAP[hash] || null;
    }

    /**
     * Get the obfuscated hash for a page filename.
     * @param {string} page - The HTML filename
     * @returns {string|null} The hash or null if not mapped
     */
    function getHashForPage(page) {
        return PAGE_TO_HASH[page] || null;
    }

    /**
     * Get the current page filename from the URL path.
     * @returns {string} The current page filename (e.g., 'dashboard.html')
     */
    function getCurrentPage() {
        const path = window.location.pathname;
        const page = path.split('/').pop() || 'index.html';
        return page;
    }

    /**
     * Initialize the router.
     * - On page load: replaces URL with obfuscated hash using history.replaceState
     * - Intercepts sidebar link clicks to maintain hash-based URLs
     * - Handles direct hash URL entry
     */
    function initRouter() {
        const currentPage = getCurrentPage();
        const currentHash = getHashForPage(currentPage);

        // Check if we arrived via a hash URL (direct entry or bookmark)
        const urlHash = window.location.hash;
        if (urlHash && urlHash.startsWith('#!/')) {
            const hashValue = urlHash.slice(3); // Remove '#!/'
            const targetPage = resolveHash(hashValue);
            if (targetPage && targetPage !== currentPage) {
                // We're on the wrong page — redirect to the correct one
                window.location.replace('/' + targetPage + '#!/' + hashValue);
                return;
            } else if (!targetPage) {
                // Invalid hash — redirect to login
                window.location.replace('/login.html');
                return;
            }
        }

        // Replace current URL with obfuscated hash (if page is in the map)
        if (currentHash) {
            const newUrl = window.location.pathname + '#!/' + currentHash;
            history.replaceState({ page: currentPage, hash: currentHash }, '', newUrl);
        }

        // Intercept sidebar and internal link clicks
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a[href]');
            if (!link) return;

            const href = link.getAttribute('href');
            if (!href || href.startsWith('http') || href.startsWith('#') || href.startsWith('mailto:')) return;

            // Extract the page filename from the href
            const pageName = href.split('/').pop().split('?')[0].split('#')[0];
            const hash = getHashForPage(pageName);

            if (hash) {
                // Navigate to the real page but with hash in URL
                e.preventDefault();
                window.location.href = '/' + pageName + '#!/' + hash;
            }
        });

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

    // Expose for testing
    window._router = { resolveHash, getHashForPage, ROUTE_MAP, PAGE_TO_HASH };

    // Auto-initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initRouter);
    } else {
        initRouter();
    }
})();
