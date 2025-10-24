function toggleMenu() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
}

// Close menu when clicking outside on mobile
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.querySelector('.menu-toggle');
    
    if (sidebar && sidebar.classList.contains('active')) {
        if (!sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    }
});

// Predefined Themes (same as settings.js)
const themes = {
    default: { bgColor: '#f5f5f5', textColor: '#333', primaryColor: '#667eea', sidebarColor: '#2c3e50', cardBg: '#ffffff', cardText: '#333' },
    ocean: { bgColor: '#e0f7fa', textColor: '#004d40', primaryColor: '#00acc1', sidebarColor: '#006064', cardBg: '#ffffff', cardText: '#004d40' },
    sunset: { bgColor: '#fff3e0', textColor: '#bf360c', primaryColor: '#ff6f00', sidebarColor: '#e64a19', cardBg: '#ffffff', cardText: '#bf360c' },
    forest: { bgColor: '#f1f8e9', textColor: '#33691e', primaryColor: '#689f38', sidebarColor: '#558b2f', cardBg: '#ffffff', cardText: '#33691e' },
    midnight: { bgColor: '#1a237e', textColor: '#e8eaf6', primaryColor: '#5c6bc0', sidebarColor: '#283593', cardBg: '#3f51b5', cardText: '#ffffff' },
    charcoal: { bgColor: '#212121', textColor: '#e0e0e0', primaryColor: '#ff5722', sidebarColor: '#424242', cardBg: '#424242', cardText: '#ffffff' },
    royal: { bgColor: '#f3e5f5', textColor: '#4a148c', primaryColor: '#ab47bc', sidebarColor: '#6a1b9a', cardBg: '#ffffff', cardText: '#4a148c' },
    crimson: { bgColor: '#1a1a1a', textColor: '#ffebee', primaryColor: '#ef5350', sidebarColor: '#c62828', cardBg: '#424242', cardText: '#ffffff' },
    mint: { bgColor: '#e8f5e9', textColor: '#1b5e20', primaryColor: '#66bb6a', sidebarColor: '#388e3c', cardBg: '#ffffff', cardText: '#1b5e20' },
    slate: { bgColor: '#eceff1', textColor: '#263238', primaryColor: '#546e7a', sidebarColor: '#37474f', cardBg: '#ffffff', cardText: '#263238' }
};

// Load business branding
function loadBranding() {
    const businessName = localStorage.getItem('businessName');
    const logo = localStorage.getItem('logo');
    const savedTheme = localStorage.getItem('selectedTheme') || 'default';
    
    if (businessName) {
        const nameElement = document.getElementById('sidebarName');
        if (nameElement) nameElement.textContent = businessName;
    }
    
    const logoType = localStorage.getItem('logoType');
    if (logo) {
        const logoElement = document.getElementById('sidebarLogo');
        if (logoElement) {
            if (logoType === 'emoji') {
                logoElement.textContent = logo;
                logoElement.style.fontSize = '32px';
            } else if (logoType === 'image') {
                logoElement.innerHTML = `<img src="${logo}" alt="Logo" style="width: 40px; height: 40px; border-radius: 5px; object-fit: contain;">`;
            }
        }
    }
    
    const theme = themes[savedTheme];
    document.documentElement.style.setProperty('--bg-color', theme.bgColor);
    document.documentElement.style.setProperty('--text-color', theme.textColor);
    document.documentElement.style.setProperty('--primary-color', theme.primaryColor);
    document.documentElement.style.setProperty('--sidebar-color', theme.sidebarColor);
    document.documentElement.style.setProperty('--card-bg', theme.cardBg);
    document.documentElement.style.setProperty('--card-text', theme.cardText);
}

loadBranding();
