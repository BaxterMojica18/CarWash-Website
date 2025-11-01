document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await API.auth.login(email, password);
        setToken(response.access_token);
        localStorage.setItem('userEmail', email);
        localStorage.setItem('isDemo', response.is_demo);
        localStorage.setItem('user_permissions', JSON.stringify(response.permissions || []));
        window.location.href = '/dashboard.html';
    } catch (error) {
        alert('Login failed: ' + error.message);
    }
});

async function demoLogin() {
    try {
        const response = await API.auth.demoLogin();
        setToken(response.access_token);
        localStorage.setItem('userEmail', 'demo@carwash.com');
        localStorage.setItem('isDemo', true);
        localStorage.setItem('user_permissions', JSON.stringify(response.permissions || []));
        window.location.href = '/dashboard.html';
    } catch (error) {
        alert('Demo login failed: ' + error.message);
    }
}
