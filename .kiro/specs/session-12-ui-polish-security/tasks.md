# Implementation Plan: Session 12 UI Polish & Security

## Overview

This plan implements five features: CSS theme color propagation to action buttons, order management filter button theming, sidebar FOUC prevention, URL obfuscation via a hash-based router, and sub-tab theming. The approach groups CSS-only changes first, then tackles the JS refactor and new router module, with property-based tests for the router's correctness properties.

## Tasks

- [x] 1. Add CSS theme rules for action buttons, filter buttons, and sub-tab theming
  - [x] 1.1 Add theme color propagation rules to `frontend/css/style.css`
    - Add `.btn-primary:not(.btn-danger):not(.btn-delete) { background: var(--sidebar-color, #2c3e50) !important; }` rule
    - Add `.btn-edit { background: var(--sidebar-color, #2c3e50) !important; }` rule
    - Ensure `.btn-delete` and `.btn-danger` retain their existing red-toned styles
    - _Requirements: 1.1, 1.3_

  - [x] 1.2 Add active filter button CSS rule to `frontend/css/style.css`
    - Add `.filter-btn.active { background: var(--sidebar-color, #667eea) !important; border-color: var(--sidebar-color, #667eea) !important; color: white !important; }`
    - Add inactive filter button base styles to ensure consistent reset
    - _Requirements: 2.1, 2.3, 2.4_

  - [x] 1.3 Add sub-tab theming CSS rules to `frontend/css/style.css`
    - Add `.nav-sub li a:hover, .nav-sub li a.active { background: color-mix(in srgb, var(--sidebar-color, #2c3e50) 40%, transparent) !important; }`
    - Add `.nav-group-header:hover { background: color-mix(in srgb, var(--sidebar-color, #2c3e50) 30%, transparent) !important; }`
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [x] 2. Refactor order management filter button JS to use CSS classes
  - [x] 2.1 Refactor `filterOrders()` function in `frontend/order-management.html`
    - Replace inline style manipulation with `classList.toggle('active', ...)` pattern
    - Remove hardcoded `#667eea` color references from the JS function
    - Remove inline `style` attributes from filter button HTML elements (keep only class-based styling)
    - Verify active state toggles correctly between buttons
    - _Requirements: 2.1, 2.2_

- [x] 3. Implement sidebar FOUC prevention
  - [x] 3.1 Add FOUC prevention CSS rules to `frontend/css/style.css`
    - Add `.sidebar-pre-collapsed .sidebar { width: 76px; padding-left: 10px; padding-right: 10px; overflow: hidden; }`
    - Add `.sidebar-pre-collapsed .content { margin-left: 0; }`
    - _Requirements: 3.1, 3.2, 3.4_

  - [x] 3.2 Add inline `<script>` to `<head>` of all sidebar pages
    - Add synchronous script that reads `localStorage.getItem('sidebarCollapsed')` and adds `sidebar-pre-collapsed` class to `document.documentElement` if value is `'1'`
    - Pages to update: `dashboard.html`, `invoices.html`, `order-management.html`, `queue-management.html`, `products.html`, `services.html`, `reports.html`, `settings.html`, `permissions-management.html`, `sidebar-management.html`, `coupon-management.html`, `flash-sale-management.html`, `client-dashboard.html`, `client-orders.html`, `shop.html`, `cart.html`, `reserve.html`, `vouchers.html`, `checkout.html`, `users.html`, `payment-methods.html`, `edit-dashboard.html`
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 4. Checkpoint - Ensure CSS and FOUC changes work correctly
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement URL obfuscation router module
  - [x] 5.1 Create `frontend/js/router.js` with route map and core functions
    - Define `ROUTE_MAP` object mapping 8-char hex hashes to page filenames for all pages
    - Define `PAGE_TO_HASH` reverse map (computed from `ROUTE_MAP`)
    - Implement `resolveHash(hash)` function returning page filename or null
    - Implement `getHashForPage(page)` function returning hash or null
    - _Requirements: 4.1, 4.7_

  - [x] 5.2 Implement `initRouter()` function in `frontend/js/router.js`
    - On page load: use `history.replaceState` to update URL bar to show `/#/{hash}` for current page
    - Intercept sidebar link clicks to navigate normally but with hash URL display
    - Handle direct hash URL entry: if page loads with a hash, resolve it and redirect to correct page if needed
    - Redirect to `login.html` for invalid/unrecognized hashes
    - Ensure browser back/forward navigation works correctly
    - _Requirements: 4.2, 4.3, 4.4, 4.5, 4.6_

  - [x] 5.3 Include `router.js` in all HTML pages
    - Add `<script src="js/router.js"></script>` to all pages that include `menu.js`
    - Add gateway logic to `frontend/index.html` to resolve hash URLs on entry
    - _Requirements: 4.2, 4.3_

  - [ ]* 5.4 Write property test for route map bijectivity (round-trip)
    - **Property 1: Route Map Bijectivity (Round-Trip)**
    - For any page in the route map, `resolveHash(getHashForPage(page))` returns the original page; for any hash, `getHashForPage(resolveHash(hash))` returns the original hash
    - Use fast-check with minimum 100 iterations
    - **Validates: Requirements 4.1, 4.2, 4.3**

  - [ ]* 5.5 Write property test for invalid hash rejection
    - **Property 2: Invalid Hash Rejection**
    - For any arbitrary string not in the route map keys, `resolveHash(string)` returns null
    - Use fast-check with minimum 100 iterations
    - **Validates: Requirements 4.4**

  - [ ]* 5.6 Write property test for hash non-reversibility
    - **Property 3: Hash Non-Reversibility**
    - For any entry in the route map, the hash is not producible by applying Base64, hex encoding, string reversal, or ROT13 to the page filename
    - Use fast-check with minimum 100 iterations
    - **Validates: Requirements 4.7**

- [x] 6. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate the URL router's correctness properties using fast-check
- Features 1, 2 (CSS part), 3, and 5 are CSS-only and require no backend changes
- The router module (Feature 4) is the only new JavaScript file
