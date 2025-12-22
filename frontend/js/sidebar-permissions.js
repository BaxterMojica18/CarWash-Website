// Add permissions link to sidebar for admin/owner users
async function addPermissionsLinkToSidebar() {
    try {
        const response = await fetch(`${API_BASE}/auth/me/permissions`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        
        if (!response.ok) return;
        
        const data = await response.json();
        const roles = data.roles || [];
        
        // Only show permissions link for superadmin
        if (roles.includes('superadmin')) {
            const sidebar = document.querySelector('.sidebar ul');
            if (sidebar && !document.querySelector('a[href="permissions-management.html"]')) {
                // Find the settings link
                const settingsLink = sidebar.querySelector('a[href="settings.html"]');
                if (settingsLink) {
                    // Create permissions link
                    const permissionsLi = document.createElement('li');
                    permissionsLi.innerHTML = '<a href="permissions-management.html">🔐 Permissions</a>';
                    
                    // Insert after settings
                    settingsLink.parentElement.insertAdjacentElement('afterend', permissionsLi);
                }
            }
        }
    } catch (error) {
        console.error('Failed to check permissions for sidebar:', error);
    }
}

// Run on page load
if (localStorage.getItem('token')) {
    addPermissionsLinkToSidebar();
}
