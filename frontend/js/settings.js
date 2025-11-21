async function loadBays() {
    try {
        const locations = await API.locations.getAll();
        const grid = document.getElementById('baysGrid');
        grid.innerHTML = locations.map(loc => `
            <div class="bay-card">
                <h3>${loc.name}</h3>
                <p>${loc.address}</p>
                <div class="bay-actions">
                    <button class="btn-edit" onclick="editBay(${loc.id}, '${loc.name}', '${loc.address}')">Edit</button>
                    <button class="btn-delete" onclick="deleteBay(${loc.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        showToast('Failed to load bays', 'error');
    }
}

function showAddBay() {
    document.getElementById('addBayModal').style.display = 'block';
    document.getElementById('bayModalTitle').textContent = 'Add Washing Bay';
    document.getElementById('bayForm').reset();
    document.getElementById('editBayId').value = '';
}

function closeBayModal() {
    document.getElementById('addBayModal').style.display = 'none';
}

function editBay(id, name, address) {
    document.getElementById('addBayModal').style.display = 'block';
    document.getElementById('bayModalTitle').textContent = 'Edit Washing Bay';
    document.getElementById('editBayId').value = id;
    document.getElementById('bayName').value = name;
}

async function deleteBay(id) {
    if (confirm('Delete this bay?')) {
        try {
            await API.locations.delete(id);
            loadBays();
            showToast('Bay deleted successfully', 'success');
        } catch (error) {
            showToast('Failed to delete bay', 'error');
        }
    }
}

document.getElementById('bayForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const id = document.getElementById('editBayId').value;
    const name = document.getElementById('bayName').value;
    const address = 'Default Address';
    
    try {
        if (id) {
            await API.locations.update(id, { name, address });
            showToast('Bay updated successfully', 'success');
        } else {
            await API.locations.create({ name, address });
            showToast('Bay created successfully', 'success');
        }
        closeBayModal();
        loadBays();
    } catch (error) {
        showToast('Failed to save bay', 'error');
    }
});

const colorMap = {
    'black': '#000000',
    'dark-grey': '#666666',
    'white': '#ffffff',
    'grey': '#cccccc',
    'dark-blue': '#1a237e'
};

function adjustBrightness(color, brightness) {
    const hex = colorMap[color] || color;
    const num = parseInt(hex.replace('#', ''), 16);
    const r = Math.min(255, Math.max(0, ((num >> 16) & 0xff) * (brightness / 100)));
    const g = Math.min(255, Math.max(0, ((num >> 8) & 0xff) * (brightness / 100)));
    const b = Math.min(255, Math.max(0, (num & 0xff) * (brightness / 100)));
    return `#${Math.round(r).toString(16).padStart(2, '0')}${Math.round(g).toString(16).padStart(2, '0')}${Math.round(b).toString(16).padStart(2, '0')}`;
}

function previewTheme() {
    const textColor = adjustBrightness(document.getElementById('textColor').value, document.getElementById('textBrightness').value);
    const cardColor = adjustBrightness(document.getElementById('cardColor').value, document.getElementById('cardBrightness').value);
    const inputColor = adjustBrightness(document.getElementById('inputColor').value, document.getElementById('inputBrightness').value);
    const dropdownColor = adjustBrightness(document.getElementById('dropdownColor').value, document.getElementById('dropdownBrightness').value);
    const buttonColor = document.getElementById('buttonColor').value;
    const sidebarColor = document.getElementById('sidebarColor').value;
    const sidebarActiveColor = document.getElementById('sidebarActiveColor').value;
    const bgColor = document.getElementById('bgColor').value;
    const deleteBrightness = document.getElementById('deleteBrightness').value;
    const deleteSaturation = document.getElementById('deleteSaturation').value;
    
    document.documentElement.style.setProperty('--text-color', textColor);
    document.documentElement.style.setProperty('--card-bg', cardColor);
    document.documentElement.style.setProperty('--card-text', textColor);
    document.documentElement.style.setProperty('--primary-color', buttonColor);
    document.documentElement.style.setProperty('--sidebar-color', sidebarColor);
    document.documentElement.style.setProperty('--sidebar-active-color', sidebarActiveColor);
    document.documentElement.style.setProperty('--bg-color', bgColor);
    document.documentElement.style.setProperty('--delete-brightness', deleteBrightness);
    document.documentElement.style.setProperty('--delete-saturation', deleteSaturation);
    
    document.querySelectorAll('input, select, textarea').forEach(el => {
        el.style.backgroundColor = inputColor;
    });
}

document.getElementById('themeForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const data = {
        preset_name: document.getElementById('presetName').value,
        text_color: document.getElementById('textColor').value,
        text_brightness: parseInt(document.getElementById('textBrightness').value),
        card_color: document.getElementById('cardColor').value,
        card_brightness: parseInt(document.getElementById('cardBrightness').value),
        input_color: document.getElementById('inputColor').value,
        input_brightness: parseInt(document.getElementById('inputBrightness').value),
        dropdown_color: document.getElementById('dropdownColor').value,
        dropdown_brightness: parseInt(document.getElementById('dropdownBrightness').value),
        button_color: document.getElementById('buttonColor').value,
        sidebar_color: document.getElementById('sidebarColor').value,
        sidebar_active_color: document.getElementById('sidebarActiveColor').value,
        bg_color: document.getElementById('bgColor').value,
        delete_button_brightness: parseInt(document.getElementById('deleteBrightness').value),
        delete_button_saturation: parseInt(document.getElementById('deleteSaturation').value)
    };
    
    try {
        await API.settings.saveTheme(data);
        showToast('Theme preset saved!', 'success');
        loadPresets();
    } catch (error) {
        showToast('Failed to save theme', 'error');
    }
});

async function loadPresets() {
    try {
        const themes = await API.settings.getAllThemes();
        const select = document.getElementById('presetSelect');
        if (Array.isArray(themes) && themes.length > 0) {
            select.innerHTML = '<option value="">-- Select Preset --</option>' +
                themes.map(t => `<option value="${t.id}">${t.preset_name}</option>`).join('');
        } else {
            select.innerHTML = '<option value="">-- No Presets Yet --</option>';
        }
    } catch (error) {
        console.error('Failed to load presets:', error);
        document.getElementById('presetSelect').innerHTML = '<option value="">-- Error Loading --</option>';
    }
}

async function loadPreset() {
    const id = document.getElementById('presetSelect').value;
    if (!id) return;
    
    try {
        await API.settings.activateTheme(id);
        const theme = await API.settings.getActiveTheme();
        applyThemeFromData(theme);
    } catch (error) {
        console.error('Failed to load preset');
    }
}

function applyThemeFromData(theme) {
    document.getElementById('presetName').value = theme.preset_name;
    document.getElementById('textColor').value = theme.text_color;
    document.getElementById('textBrightness').value = theme.text_brightness;
    document.getElementById('cardColor').value = theme.card_color;
    document.getElementById('cardBrightness').value = theme.card_brightness;
    document.getElementById('inputColor').value = theme.input_color;
    document.getElementById('inputBrightness').value = theme.input_brightness;
    document.getElementById('dropdownColor').value = theme.dropdown_color;
    document.getElementById('dropdownBrightness').value = theme.dropdown_brightness;
    document.getElementById('buttonColor').value = theme.button_color;
    document.getElementById('sidebarColor').value = theme.sidebar_color;
    document.getElementById('sidebarActiveColor').value = theme.sidebar_active_color;
    document.getElementById('bgColor').value = theme.bg_color;
    document.getElementById('deleteBrightness').value = theme.delete_button_brightness || 100;
    document.getElementById('deleteSaturation').value = theme.delete_button_saturation || 100;
    previewTheme();
}

['textBrightness', 'cardBrightness', 'inputBrightness', 'dropdownBrightness', 'deleteBrightness', 'deleteSaturation'].forEach(id => {
    document.getElementById(id).addEventListener('input', function() {
        const valId = id.includes('Saturation') ? 'deleteSatVal' : id.replace('ness', 'Val');
        document.getElementById(valId).textContent = this.value;
    });
});

function selectPredefinedLogo() {
    const emoji = document.getElementById('logoSelect').value;
    document.getElementById('currentLogo').textContent = emoji;
    localStorage.setItem('logo', emoji);
    localStorage.setItem('logoType', 'emoji');
}

function previewLogo() {
    const file = document.getElementById('logoFile').files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('currentLogo').innerHTML = 
                `<img src="${e.target.result}" style="width:40px;height:40px;object-fit:contain;">`;
            localStorage.setItem('logo', e.target.result);
            localStorage.setItem('logoType', 'image');
        };
        reader.readAsDataURL(file);
    }
}

document.getElementById('businessForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const data = {
        business_name: document.getElementById('businessName').value,
        logo: localStorage.getItem('logo'),
        logo_type: localStorage.getItem('logoType'),
        address: document.querySelector('#businessForm input[type="text"]:nth-of-type(2)').value,
        phone: document.querySelector('#businessForm input[type="tel"]').value
    };
    
    try {
        await API.settings.saveBusiness(data);
        showToast('Business information saved!', 'success');
    } catch (error) {
        showToast('Failed to save business info', 'error');
    }
});

document.getElementById('invoiceCustomForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const data = {
        invoice_address: document.getElementById('invoiceAddress').value,
        invoice_phone: document.getElementById('invoicePhone').value,
        invoice_email: document.getElementById('invoiceEmail').value
    };
    
    try {
        await API.settings.saveInvoiceCustom(data);
        showToast('Invoice settings saved!', 'success');
    } catch (error) {
        showToast('Failed to save invoice settings', 'error');
    }
});

async function checkUserPermissions() {
    try {
        const response = await fetch(`${API_BASE}/auth/me/permissions`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const data = await response.json();
        const roles = data.roles || [];
        if (roles.includes('admin') || roles.includes('owner')) {
            document.getElementById('userManagementSection').style.display = 'block';
            loadUsers();
        }
    } catch (error) {
        console.error('Failed to check permissions:', error);
    }
}

async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE}/auth/users`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const users = await response.json();
        const grid = document.getElementById('usersGrid');
        grid.innerHTML = users.map(user => `
            <div class="bay-card">
                <h3>${user.email}</h3>
                <p>Roles: ${user.roles.join(', ') || 'Custom'}</p>
                <p style="font-size: 12px; color: #666;">${user.permissions.length} permissions</p>
                <div class="bay-actions">
                    <button class="btn-edit" onclick="editUser(${user.user_id}, '${user.email}', '${user.roles[0] || 'staff'}')">Edit Role</button>
                    <button class="btn-primary" onclick="editPermissions(${user.user_id})">Permissions</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load users:', error);
    }
}

function showAddUser() {
    document.getElementById('addUserModal').style.display = 'block';
    document.getElementById('userModalTitle').textContent = 'Add User';
    document.getElementById('userForm').reset();
    document.getElementById('editUserId').value = '';
    document.getElementById('userName').disabled = false;
    document.getElementById('userEmail').disabled = false;
    document.getElementById('userSubmitBtn').textContent = 'Add User';
}

function closeUserModal() {
    document.getElementById('addUserModal').style.display = 'none';
}

function editUser(id, email, role) {
    document.getElementById('addUserModal').style.display = 'block';
    document.getElementById('userModalTitle').textContent = 'Edit User Role';
    document.getElementById('editUserId').value = id;
    document.getElementById('userName').value = '';
    document.getElementById('userName').disabled = true;
    document.getElementById('userEmail').value = email;
    document.getElementById('userEmail').disabled = true;
    document.getElementById('userRole').value = role;
    document.getElementById('userSubmitBtn').textContent = 'Update Role';
}

async function editPermissions(userId) {
    try {
        const response = await fetch(`${API_BASE}/auth/users/${userId}`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const user = await response.json();
        
        document.getElementById('editPermissionsModal').style.display = 'block';
        document.getElementById('permUserId').value = userId;
        document.getElementById('permUserEmail').textContent = `User: ${user.email}`;
        
        const checkboxes = document.querySelectorAll('#permissionsForm input[name="permission"]');
        checkboxes.forEach(cb => {
            cb.checked = user.permissions.includes(cb.value);
        });
    } catch (error) {
        showToast('Failed to load user permissions', 'error');
    }
}

function closePermissionsModal() {
    document.getElementById('editPermissionsModal').style.display = 'none';
}

async function deleteUser(id) {
    if (confirm('Delete this user?')) {
        alert('User deletion not yet implemented');
    }
}

document.getElementById('userForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const id = document.getElementById('editUserId').value;
    const name = document.getElementById('userName').value;
    const email = document.getElementById('userEmail').value;
    const role = document.getElementById('userRole').value;
    
    try {
        if (id) {
            // Update existing user
            const response = await fetch(`${API_BASE}/auth/users/roles`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ user_id: parseInt(id), roles: [role] })
            });
            
            if (response.ok) {
                closeUserModal();
                loadUsers();
                showToast('User role updated successfully!', 'success');
            } else {
                showToast('Failed to update user', 'error');
            }
        } else {
            // Create new user
            const response = await fetch(`${API_BASE}/auth/users`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ name, email, role })
            });
            
            if (response.ok) {
                closeUserModal();
                loadUsers();
                showToast('User created successfully! Default password: password123', 'success');
            } else {
                const error = await response.json();
                showToast(error.detail || 'Failed to create user', 'error');
            }
        }
    } catch (error) {
        showToast('Failed to save user', 'error');
    }
});

document.getElementById('permissionsForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const userId = parseInt(document.getElementById('permUserId').value);
    const selectedPermissions = Array.from(document.querySelectorAll('#permissionsForm input[name="permission"]:checked'))
        .map(cb => cb.value);
    
    try {
        const response = await fetch(`${API_BASE}/auth/users/permissions`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ user_id: userId, permissions: selectedPermissions })
        });
        
        if (response.ok) {
            closePermissionsModal();
            loadUsers();
            showToast('User permissions updated successfully!', 'success');
        } else {
            showToast('Failed to update permissions', 'error');
        }
    } catch (error) {
        showToast('Failed to update permissions', 'error');
    }
});

// Payment Methods Management
let paymentMethods = [];

async function loadPaymentMethods() {
    try {
        const response = await fetch(`${API_BASE}/settings/payment-methods`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        paymentMethods = await response.json();
        renderPaymentMethods();
    } catch (error) {
        console.error('Failed to load payment methods:', error);
    }
}

function renderPaymentMethods() {
    const grid = document.getElementById('paymentMethodsGrid');
    if (paymentMethods.length === 0) {
        grid.innerHTML = '<p style="color: #666;">No payment methods configured yet.</p>';
        return;
    }
    grid.innerHTML = paymentMethods.map(pm => `
        <div class="bay-card">
            <h3>${pm.icon} ${pm.name}</h3>
            <p>Status: <span style="color: ${pm.is_active ? '#28a745' : '#dc3545'};">${pm.is_active ? 'Active' : 'Inactive'}</span></p>
            <div class="bay-actions">
                <button class="btn-edit" onclick="editPaymentMethod(${pm.id}, '${pm.name}', '${pm.icon}', ${pm.is_active})">Edit</button>
                <button class="btn-delete" onclick="deletePaymentMethod(${pm.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

function showAddPaymentMethod() {
    document.getElementById('addPaymentMethodModal').style.display = 'block';
    document.getElementById('paymentMethodModalTitle').textContent = 'Add Payment Method';
    document.getElementById('paymentMethodForm').reset();
    document.getElementById('editPaymentMethodId').value = '';
    document.getElementById('paymentMethodSubmitBtn').textContent = 'Add Payment Method';
}

function closePaymentMethodModal() {
    document.getElementById('addPaymentMethodModal').style.display = 'none';
}

function editPaymentMethod(id, name, icon, isActive) {
    document.getElementById('addPaymentMethodModal').style.display = 'block';
    document.getElementById('paymentMethodModalTitle').textContent = 'Edit Payment Method';
    document.getElementById('editPaymentMethodId').value = id;
    document.getElementById('paymentMethodName').value = name;
    document.getElementById('paymentMethodIcon').value = icon;
    document.getElementById('paymentMethodStatus').value = isActive ? 'active' : 'inactive';
    document.getElementById('paymentMethodSubmitBtn').textContent = 'Update Payment Method';
}

async function deletePaymentMethod(id) {
    if (confirm('Delete this payment method?')) {
        try {
            await fetch(`${API_BASE}/settings/payment-methods/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            loadPaymentMethods();
            showToast('Payment method deleted', 'success');
        } catch (error) {
            showToast('Failed to delete payment method', 'error');
        }
    }
}

document.getElementById('paymentMethodForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const id = document.getElementById('editPaymentMethodId').value;
    const data = {
        name: document.getElementById('paymentMethodName').value,
        icon: document.getElementById('paymentMethodIcon').value,
        is_active: document.getElementById('paymentMethodStatus').value === 'active'
    };
    
    try {
        if (id) {
            await fetch(`${API_BASE}/settings/payment-methods/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(data)
            });
            showToast('Payment method updated', 'success');
        } else {
            await fetch(`${API_BASE}/settings/payment-methods`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(data)
            });
            showToast('Payment method added', 'success');
        }
        closePaymentMethodModal();
        loadPaymentMethods();
    } catch (error) {
        showToast('Failed to save payment method', 'error');
    }
});

checkUserPermissions();
loadBays();
loadPresets();
loadPaymentMethods();
