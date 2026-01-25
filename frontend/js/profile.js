function toggleProfileMenu() {
    const menu = document.getElementById('profileMenu');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
}

function showEditProfile() {
    document.getElementById('editProfileModal').style.display = 'block';
    document.getElementById('profileMenu').style.display = 'none';
}

function closeEditProfile() {
    document.getElementById('editProfileModal').style.display = 'none';
}

// Load profile data
async function loadProfileData() {
    try {
        const response = await fetch(`${API_BASE}/settings/profile`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const profile = await response.json();
        
        const defaultPhoto = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Ccircle cx="50" cy="50" r="50" fill="%23667eea"/%3E%3Cpath d="M50 45c8.284 0 15-6.716 15-15s-6.716-15-15-15-15 6.716-15 15 6.716 15 15 15zm0 7.5c-10 0-30 5-30 15v7.5h60v-7.5c0-10-20-15-30-15z" fill="white"/%3E%3C/svg%3E';
        
        document.getElementById('profilePhoto').src = profile.photo || defaultPhoto;
        document.getElementById('menuProfilePhoto').src = profile.photo || defaultPhoto;
        document.getElementById('profileName').textContent = profile.name || 'User';
        document.getElementById('profileRole').textContent = profile.role || 'Role';
    } catch (error) {
        console.error('Failed to load profile:', error);
        const defaultPhoto = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Ccircle cx="50" cy="50" r="50" fill="%23667eea"/%3E%3Cpath d="M50 45c8.284 0 15-6.716 15-15s-6.716-15-15-15-15 6.716-15 15 6.716 15 15 15zm0 7.5c-10 0-30 5-30 15v7.5h60v-7.5c0-10-20-15-30-15z" fill="white"/%3E%3C/svg%3E';
        document.getElementById('profilePhoto').src = defaultPhoto;
        document.getElementById('menuProfilePhoto').src = defaultPhoto;
    }
}

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('editProfileModal')) {
        closeEditProfile();
    }
    if (!event.target.matches('.profile-icon') && !event.target.matches('.profile-icon img')) {
        const menu = document.getElementById('profileMenu');
        if (menu && menu.style.display === 'block') {
            menu.style.display = 'none';
        }
    }
});

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadProfileData);
} else {
    loadProfileData();
}
