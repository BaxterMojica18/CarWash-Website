async function loadBays() {
    try {
        const locations = await API.locations.getAll();
        const grid = document.getElementById('baysGrid');
        grid.innerHTML = locations.map(loc => `
            <div class="bay-card">
                <h3>${loc.name}</h3>
                <p>${loc.address}</p>
                <div class="bay-actions">
                    <button onclick="editBay(${loc.id}, '${loc.name}', '${loc.address}')">Edit</button>
                    <button onclick="deleteBay(${loc.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load bays:', error);
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
        } catch (error) {
            alert('Failed to delete bay');
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
        } else {
            await API.locations.create({ name, address });
        }
        closeBayModal();
        loadBays();
    } catch (error) {
        alert('Failed to save bay');
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
    
    document.documentElement.style.setProperty('--text-color', textColor);
    document.documentElement.style.setProperty('--card-bg', cardColor);
    document.documentElement.style.setProperty('--card-text', textColor);
    document.documentElement.style.setProperty('--primary-color', buttonColor);
    document.documentElement.style.setProperty('--sidebar-color', sidebarColor);
    document.documentElement.style.setProperty('--sidebar-active-color', sidebarActiveColor);
    document.documentElement.style.setProperty('--bg-color', bgColor);
    
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
        bg_color: document.getElementById('bgColor').value
    };
    
    try {
        await API.settings.saveTheme(data);
        alert('Theme preset saved!');
        loadPresets();
    } catch (error) {
        alert('Failed to save theme');
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
    previewTheme();
}

['textBrightness', 'cardBrightness', 'inputBrightness', 'dropdownBrightness'].forEach(id => {
    document.getElementById(id).addEventListener('input', function() {
        document.getElementById(id.replace('ness', 'Val')).textContent = this.value;
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
        alert('Business information saved!');
    } catch (error) {
        alert('Failed to save business info');
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
        alert('Invoice settings saved!');
    } catch (error) {
        alert('Failed to save invoice settings');
    }
});

loadBays();
loadPresets();
