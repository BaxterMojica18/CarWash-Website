# Requirements Document

## Introduction

This document specifies the requirements for Session 12 UI Polish & Security enhancements to the Car Wash Management System (v6.7.0). The scope covers five features: theme color propagation to action buttons across pages, active filter button theming on order management, sidebar state persistence across page navigation, URL obfuscation for security, and User Management sub-tab theming.

## Glossary

- **Theme_System**: The mechanism in `menu.js` that loads the active theme from the API and sets CSS custom properties (including `--sidebar-color`) on the `:root` element.
- **Action_Button**: Any `.btn-primary`, `.btn-edit`, or similar action button on admin pages that is NOT a delete button (`.btn-delete`, `.btn-danger`).
- **Filter_Button**: The status filter buttons (`.filter-btn`) on `order-management.html` used to filter orders by status (All, Pending, Accepted, Processing, Completed, Delayed, Cancelled).
- **Sidebar**: The collapsible left navigation panel managed by `menu.js`, which stores its collapsed state in `localStorage` under the key `sidebarCollapsed`.
- **URL_Router**: A client-side hash-based routing system that maps obfuscated URL fragments to actual HTML page filenames.
- **Nav_Sub_Link**: The sub-navigation links (`.nav-sub li a`) within the User Management collapsible nav-group in the sidebar, specifically the "Permissions" and "Sidebar Tabs" items.
- **Sidebar_Color**: The CSS custom property `--sidebar-color` set on `:root` by the Theme_System, representing the current theme's sidebar/accent color.

## Requirements

### Requirement 1: Theme Color Propagation to Action Buttons

**User Story:** As an admin/owner, I want all action buttons (except delete buttons) across products, services, reports, and settings pages to use the sidebar theme color, so that the UI feels cohesive and dynamically reflects my chosen theme.

#### Acceptance Criteria

1. THE Theme_System SHALL apply `var(--sidebar-color)` as the background color to all Action_Buttons on `products.html`, `services.html`, `reports.html`, and `settings.html`.
2. WHEN the Sidebar_Color is changed in the settings theme customization, THE Action_Buttons on all pages SHALL update their background color to match the new Sidebar_Color without requiring a page reload on the current page.
3. THE Theme_System SHALL NOT modify the background color of delete buttons (`.btn-delete`, `.btn-danger`, or buttons with `reject-btn` class), which SHALL remain red-toned for danger indication.
4. WHEN a page loads, THE Action_Buttons SHALL render with the current Sidebar_Color immediately, without a flash of the default color.

### Requirement 2: Order Management Active Filter Button Theming

**User Story:** As an admin/owner, I want the active filter button on the order management page to match my sidebar theme color, so that the active state is visually consistent with the rest of the themed UI.

#### Acceptance Criteria

1. WHEN a Filter_Button is in the active state on `order-management.html`, THE Filter_Button SHALL display a background color matching `var(--sidebar-color)` and a border color matching `var(--sidebar-color)`.
2. WHEN the user clicks a different Filter_Button, THE previously active Filter_Button SHALL revert to the default inactive style (white background, grey border) and THE newly clicked Filter_Button SHALL adopt the Sidebar_Color background.
3. WHEN the Sidebar_Color changes via theme update, THE currently active Filter_Button SHALL dynamically update its background color to the new Sidebar_Color without requiring a page reload.
4. THE inactive Filter_Buttons SHALL retain their default styling (white background, `#e0e0e0` border, dark text) regardless of the active theme.

### Requirement 3: Sidebar State Persistence Across Page Navigation

**User Story:** As a user, I want the sidebar to remain collapsed when I navigate between pages, so that my layout preference is preserved without visual flicker.

#### Acceptance Criteria

1. WHEN the user collapses the Sidebar and navigates to another page, THE Sidebar SHALL render in the collapsed state on the new page without briefly appearing expanded.
2. THE Sidebar SHALL read the `sidebarCollapsed` value from `localStorage` and apply the collapsed class before the sidebar becomes visible to the user.
3. WHILE the Sidebar is in the collapsed state, THE Sidebar SHALL remain collapsed across all page navigations until the user explicitly expands it.
4. WHEN the page loads with `sidebarCollapsed` set to `'1'` in `localStorage`, THE content area SHALL also have the `sidebar-collapsed` class applied immediately to prevent layout shift.
5. IF the `localStorage` value for `sidebarCollapsed` is absent or empty, THEN THE Sidebar SHALL render in the expanded (default) state.

### Requirement 4: URL Obfuscation for Security

**User Story:** As a system owner, I want page URLs to be obfuscated so that attackers cannot easily guess or enumerate page names from the URL bar.

#### Acceptance Criteria

1. THE URL_Router SHALL map each internal HTML page filename to a unique obfuscated hash identifier (e.g., `/#/a3f2b1c8` maps to `dashboard.html`).
2. WHEN a user navigates via the sidebar or any internal link, THE URL_Router SHALL update the browser URL to display the obfuscated hash instead of the raw HTML filename.
3. WHEN a user directly enters an obfuscated hash URL in the browser, THE URL_Router SHALL load the corresponding HTML page content.
4. IF a user enters an unrecognized or invalid hash URL, THEN THE URL_Router SHALL redirect the user to the login page.
5. THE URL_Router SHALL preserve all existing authentication checks and page access restrictions enforced by `menu.js`.
6. WHEN the user navigates using browser back/forward buttons, THE URL_Router SHALL correctly load the corresponding page for each hash in the history.
7. THE URL_Router SHALL generate obfuscated identifiers that do not reveal the original page name through simple decoding (no plain Base64 of the filename).

### Requirement 5: User Management Sub-Tab Theming

**User Story:** As an admin/owner, I want the "Permissions" and "Sidebar Tabs" sub-navigation items under User Management in the sidebar to use the sidebar theme color for their active and hover states, so that the entire sidebar navigation is visually consistent.

#### Acceptance Criteria

1. WHEN a Nav_Sub_Link is in the active state (current page matches the link), THE Nav_Sub_Link SHALL display a background color derived from the Sidebar_Color.
2. WHEN the user hovers over a Nav_Sub_Link, THE Nav_Sub_Link SHALL display a background color derived from the Sidebar_Color.
3. WHEN the Sidebar_Color changes via theme update, THE Nav_Sub_Link active and hover colors SHALL dynamically update to match the new Sidebar_Color.
4. THE Nav_Group_Header (the "User Management" parent item) hover state SHALL also use the Sidebar_Color-derived background, consistent with other sidebar link hover states.
