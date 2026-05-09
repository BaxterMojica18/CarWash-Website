function toggleProfileMenu() {
    const menu = document.getElementById('profileMenu');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
}

function showEditProfile() {
    const modal = document.getElementById('editProfileModal');
    if (!modal) return;
    modal.style.display = 'block';
    const menu = document.getElementById('profileMenu');
    if (menu) menu.style.display = 'none';

    // Pre-fill current values
    const name = document.getElementById('profileName')?.textContent || '';
    const role = document.getElementById('profileRole')?.textContent || '';
    const editName = document.getElementById('editName');
    const editRole = document.getElementById('editRole');
    if (editName && name !== 'User') editName.value = name;
    if (editRole && role !== 'Role') editRole.value = role;

    initProfileForm();
}

function closeEditProfile() {
    const modal = document.getElementById('editProfileModal');
    if (modal) modal.style.display = 'none';
}

// Load profile data
async function loadProfileData() {
    try {
        const response = await fetch(`${API_BASE}/settings/profile`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const profile = await response.json();

        const defaultPhoto = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Ccircle cx="50" cy="50" r="50" fill="%23667eea"/%3E%3Cpath d="M50 45c8.284 0 15-6.716 15-15s-6.716-15-15-15-15 6.716-15 15 6.716 15 15 15zm0 7.5c-10 0-30 5-30 15v7.5h60v-7.5c0-10-20-15-30-15z" fill="white"/%3E%3C/svg%3E';

        const profilePhoto = document.getElementById('profilePhoto');
        const menuProfilePhoto = document.getElementById('menuProfilePhoto');
        if (profilePhoto) profilePhoto.src = profile.photo || defaultPhoto;
        if (menuProfilePhoto) menuProfilePhoto.src = profile.photo || defaultPhoto;

        const profileName = document.getElementById('profileName');
        const profileRole = document.getElementById('profileRole');
        if (profileName) profileName.textContent = profile.name || 'User';
        if (profileRole) profileRole.textContent = profile.role || 'Role';

        const bizElement = document.getElementById('profileBiz');
        if (bizElement && profile.business_number) {
            bizElement.textContent = `Biz Code: ${profile.business_number}`;
            bizElement.style.display = 'inline-block';
        } else if (bizElement) {
            bizElement.style.display = 'none';
        }
    } catch (error) {
        console.error('Failed to load profile:', error);
        const defaultPhoto = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Ccircle cx="50" cy="50" r="50" fill="%23667eea"/%3E%3Cpath d="M50 45c8.284 0 15-6.716 15-15s-6.716-15-15-15-15 6.716-15 15 6.716 15 15 15zm0 7.5c-10 0-30 5-30 15v7.5h60v-7.5c0-10-20-15-30-15z" fill="white"/%3E%3C/svg%3E';
        const profilePhoto = document.getElementById('profilePhoto');
        const menuProfilePhoto = document.getElementById('menuProfilePhoto');
        if (profilePhoto) profilePhoto.src = defaultPhoto;
        if (menuProfilePhoto) menuProfilePhoto.src = defaultPhoto;
    }
}

// Profile form submit handler — photo upload + name/role save
function initProfileForm() {
    const form = document.getElementById('profileForm');
    if (!form || form.dataset.handlerAttached) return;
    form.dataset.handlerAttached = 'true';

    // Photo preview on file select
    const photoInput = document.getElementById('editPhoto');
    if (photoInput) {
        photoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (!file) return;
            const preview = document.getElementById('photoPreview');
            if (preview) {
                preview.src = URL.createObjectURL(file);
                preview.style.display = 'block';
            }
        });
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const saveBtn = form.querySelector('button[type="submit"]');
        const originalText = saveBtn ? saveBtn.textContent : 'Save Profile';
        if (saveBtn) { saveBtn.textContent = 'Saving...'; saveBtn.disabled = true; }

        try {
            const name = document.getElementById('editName')?.value?.trim() || '';
            const role = document.getElementById('editRole')?.value?.trim() || '';
            const photoFile = document.getElementById('editPhoto')?.files[0];

            // Convert photo to base64 if provided
            let photoBase64 = null;
            if (photoFile) {
                photoBase64 = await new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = e => resolve(e.target.result);
                    reader.onerror = reject;
                    reader.readAsDataURL(photoFile);
                });
            }

            const payload = { name, role };
            if (photoBase64) payload.photo = photoBase64;

            const res = await fetch(`${API_BASE}/settings/profile`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail || 'Failed to save profile');
            }

            const updated = await res.json();

            // Update UI immediately
            const defaultPhoto = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Ccircle cx="50" cy="50" r="50" fill="%23667eea"/%3E%3Cpath d="M50 45c8.284 0 15-6.716 15-15s-6.716-15-15-15-15 6.716-15 15 6.716 15 15 15zm0 7.5c-10 0-30 5-30 15v7.5h60v-7.5c0-10-20-15-30-15z" fill="white"/%3E%3C/svg%3E';
            const photo = updated.photo || defaultPhoto;

            const profilePhotoEl = document.getElementById('profilePhoto');
            const menuPhotoEl = document.getElementById('menuProfilePhoto');
            if (profilePhotoEl) profilePhotoEl.src = photo;
            if (menuPhotoEl) menuPhotoEl.src = photo;

            const profileNameEl = document.getElementById('profileName');
            if (profileNameEl) profileNameEl.textContent = updated.name || name;

            // Show success toast
            if (typeof showToast === 'function') {
                showToast('Profile updated successfully!', 'success');
            } else {
                const toast = document.createElement('div');
                toast.textContent = 'Profile updated successfully!';
                toast.style.cssText = 'position:fixed;bottom:24px;right:24px;background:#27ae60;color:white;padding:12px 20px;border-radius:8px;font-weight:600;z-index:9999;box-shadow:0 4px 12px rgba(0,0,0,0.2);';
                document.body.appendChild(toast);
                setTimeout(() => toast.remove(), 3000);
            }

            closeEditProfile();
        } catch (err) {
            console.error('Profile save error:', err);
            if (typeof showToast === 'function') {
                showToast(err.message || 'Failed to save profile', 'error');
            } else {
                alert(err.message || 'Failed to save profile');
            }
        } finally {
            if (saveBtn) { saveBtn.textContent = originalText; saveBtn.disabled = false; }
        }
    });
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
    document.addEventListener('DOMContentLoaded', () => { loadProfileData(); initProfileForm(); });
} else {
    loadProfileData();
    initProfileForm();
}
