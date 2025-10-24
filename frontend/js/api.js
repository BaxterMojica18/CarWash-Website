const API_BASE = 'http://localhost:8000/api';

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

const API = {
    auth: {
        login: (email, password) => 
            apiRequest('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            }),
        demoLogin: () => 
            apiRequest('/auth/demo-login', { method: 'POST' })
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
    }
};
