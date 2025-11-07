// Permission management for frontend
class PermissionManager {
    constructor() {
        this.permissions = [];
        this.loadPermissions();
    }

    loadPermissions() {
        const permissions = localStorage.getItem('user_permissions');
        this.permissions = permissions ? JSON.parse(permissions) : [];
    }

    setPermissions(permissions) {
        this.permissions = permissions;
        localStorage.setItem('user_permissions', JSON.stringify(permissions));
    }

    hasPermission(permission) {
        return this.permissions.includes(permission);
    }

    canManageProducts() {
        return this.hasPermission('manage_products');
    }

    canManageLocations() {
        return this.hasPermission('manage_locations');
    }

    canManageInvoices() {
        return this.hasPermission('manage_invoices');
    }

    canViewReports() {
        return this.hasPermission('view_reports');
    }

    canManageSettings() {
        return this.hasPermission('manage_settings');
    }

    canManageUsers() {
        return this.hasPermission('manage_users');
    }

    hideElementsWithoutPermission() {
        // Hide product/service management buttons
        if (!this.canManageProducts()) {
            document.querySelectorAll('[data-permission="manage_products"]').forEach(el => {
                el.style.display = 'none';
            });
        }

        // Hide location management buttons
        if (!this.canManageLocations()) {
            document.querySelectorAll('[data-permission="manage_locations"]').forEach(el => {
                el.style.display = 'none';
            });
        }

        // Hide settings/customization options
        if (!this.canManageSettings()) {
            document.querySelectorAll('[data-permission="manage_settings"]').forEach(el => {
                el.style.display = 'none';
            });
        }

        // Hide user management
        if (!this.canManageUsers()) {
            document.querySelectorAll('[data-permission="manage_users"]').forEach(el => {
                el.style.display = 'none';
            });
        }
    }
}

const permissionManager = new PermissionManager();
