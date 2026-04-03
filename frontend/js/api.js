// Auto-detect API base URL: production (Render) vs local development
const PRODUCTION_API_URL = 'https://carwash-website-jzr2.onrender.com/api';
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : PRODUCTION_API_URL;

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function clearToken() {
    localStorage.removeItem('token');
}

function getHeaders() {
    const token = getToken();
    return {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };
}

async function apiRequest(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: getHeaders()
    });
    
    if (response.status === 401) {
        clearToken();
        window.location.href = '/login.html';
        throw new Error('Unauthorized');
    }
    
    return response.json();
}

// Public API request (no auth redirect, proper error handling for non-authenticated endpoints)
async function apiRequestPublic(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: { 'Content-Type': 'application/json' }
    });
    
    const data = await response.json();
    
    if (!response.ok) {
        throw new Error(data.detail || 'Something went wrong');
    }
    
    return data;
}

const API = {
    auth: {
        login: (email, password) => 
            apiRequestPublic('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            }),
        register: (data) =>
            apiRequestPublic('/auth/register', {
                method: 'POST',
                body: JSON.stringify(data)
            }),
        firebaseLogin: (id_token, email, display_name) =>
            apiRequestPublic('/auth/firebase-login', {
                method: 'POST',
                body: JSON.stringify({ id_token, email, display_name })
            }),
        demoLogin: () => 
            apiRequest('/auth/demo-login', { method: 'POST' }),
        forgotPassword: (email, reset_method = 'link') =>
            apiRequestPublic('/auth/forgot-password', {
                method: 'POST',
                body: JSON.stringify({ email, reset_method })
            }),
        resetPassword: (token, new_password) =>
            apiRequestPublic('/auth/reset-password', {
                method: 'POST',
                body: JSON.stringify({ token, new_password })
            }),
        verifyOtp: (email, otp_code) =>
            apiRequestPublic('/auth/verify-otp', {
                method: 'POST',
                body: JSON.stringify({ email, otp_code })
            })
    },
    
    locations: {
        getAll: () => apiRequest('/settings/locations'),
        create: (data) => 
            apiRequest('/settings/locations', {
                method: 'POST',
                body: JSON.stringify(data)
            }),
        update: (id, data) => 
            apiRequest(`/settings/locations/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            }),
        delete: (id) => 
            apiRequest(`/settings/locations/${id}`, { method: 'DELETE' })
    },
    
    products: {
        getAll: () => apiRequest('/settings/products'),
        create: (data) => 
            apiRequest('/settings/products', {
                method: 'POST',
                body: JSON.stringify(data)
            }),
        update: (id, data) => 
            apiRequest(`/settings/products/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            }),
        delete: (id) => 
            apiRequest(`/settings/products/${id}`, { method: 'DELETE' })
    },
    
    invoices: {
        getAll: () => apiRequest('/invoices/'),
        getById: (id) => apiRequest(`/invoices/${id}`),
        create: (data) => 
            apiRequest('/invoices/', {
                method: 'POST',
                body: JSON.stringify(data)
            }),
        downloadPDF: (id) => `${API_BASE}/invoices/${id}/pdf`,
        getStats: () => apiRequest('/invoices/dashboard/stats')
    },
    
    settings: {
        getActiveTheme: () => apiRequest('/settings/theme/active'),
        getAllThemes: () => apiRequest('/settings/theme/all'),
        saveTheme: (data) => 
            apiRequest('/settings/theme', {
                method: 'POST',
                body: JSON.stringify(data)
            }),
        activateTheme: (id) => 
            apiRequest(`/settings/theme/${id}/activate`, {
                method: 'PUT'
            }),
        deleteTheme: (id) => 
            apiRequest(`/settings/theme/${id}`, {
                method: 'DELETE'
            }),
        getBusiness: () => apiRequest('/settings/business'),
        saveBusiness: (data) => 
            apiRequest('/settings/business', {
                method: 'POST',
                body: JSON.stringify(data)
            }),
        getInvoiceCustom: () => apiRequest('/settings/invoice-custom'),
        saveInvoiceCustom: (data) => 
            apiRequest('/settings/invoice-custom', {
                method: 'POST',
                body: JSON.stringify(data)
            })
    },
    
    reservations: {
        create: (data) => 
            apiRequest('/reservations/', {
                method: 'POST',
                body: JSON.stringify(data)
            }),
        getAll: (locationId = null) => 
            apiRequest(`/reservations/${locationId ? `?location_id=${locationId}` : ''}`),
        getById: (id) => apiRequest(`/reservations/${id}`),
        updateStatus: (id, status) => 
            apiRequest(`/reservations/${id}/status`, {
                method: 'PATCH',
                body: JSON.stringify({ status })
            }),
        getQueue: (locationId) => apiRequest(`/reservations/queue?location_id=${locationId}`)
    }
};
