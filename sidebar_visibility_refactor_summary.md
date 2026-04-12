# Changes Summary: Sidebar Visibility Refactor (Role -> User ID)

## Problem Addressed:
The user reported that when updating sidebar tab visibility (specifically trying to disable a tab for the Client role), it was not reflecting correctly for the `demo-client@carwash.com` account. Furthermore, the user explicitly requested that sidebar tab visibility should be stored and remembered specifically for an individual account (User ID) rather than broadly by Role.

There were two core issues causing the failure:
1. **Visibility was tied to Roles, not Users:** If an Owner edited the "Client" role, it applied to *all* clients universally, making it impossible to tailor experiences for individual accounts.
2. **Missing Client Tabs in Management UI:** The frontend `sidebar-management.html` did not include client-specific tabs (e.g., `Shop`, `Cart`, `Reserve`, `My Orders`) in its `ALL_TABS` list. Because the tabs were missing from the UI, the Admin could not disable them. Even if an admin disabled "Orders", the client tab is named "My Orders", so the names did not match and the tab remained visible.

## Modifications Made:

### 1. Database Schema Refactor (`app/database.py`)
- Removed `RoleSidebarSetting` and replaced it with a new `UserSidebarSetting` model.
- The new model links specifically to `users.id` via `user_id` foreign key instead of `role_id`.
- Created the corresponding `user_sidebar_settings` table directly in the PostgreSQL container via SQL.

### 2. Backend API Modifications (`app/routers/auth.py`)
- **`GET /me/permissions`**: Updated to fetch the `hidden_sidebar_tabs` strictly from `UserSidebarSetting` referencing `current_user.id` rather than searching through all assigned role IDs.
- **`GET /users/{user_id}/sidebar`**: Replaced the previous `roles/{role_id}/sidebar` logic entirely. It now fetches sidebar configs purely by `user_id`.
- **`PUT /users/{user_id}/sidebar`**: Replaced the role updater to instead store visibility booleans specifically mapped to the `user_id`.

### 3. Frontend UI Modifications (`frontend/sidebar-management.html`)
- **User-Centric Management UI:** Refactored `loadRoles()` to `loadUsers()`. The Management Interface now queries `/auth/users` and lists individual user accounts under the company (showing their Email and assigned Roles) instead of generic Role cards.
- **Added Client Tabs:** Expanded the `ALL_TABS` variable to include `"My Orders"`, `"Shop"`, `"Cart"`, and `"Reserve"`. Owners can now properly hide or show these client-specific links for individual users.
- **Per-User Toggling:** Updated the `toggleTabVisibility` logic to send API requests with `user.user_id` instead of `role.id`.

## Conclusion
The Admin can now navigate to `Sidebar Tabs` on their dashboard and see a separate card for `demo-client@carwash.com`. They can tailor the navigation experience for that exact user, completely independent of other clients or roles. Any hidden tabs are remembered server-side, tied to the User ID exactly as requested.
