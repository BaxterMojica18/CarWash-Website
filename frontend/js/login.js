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
        
        // Redirect based on permissions
        const permissions = response.permissions || [];
        const isClient = permissions.includes('manage_cart') && !permissions.includes('manage_users');
        window.location.href = isClient ? '/shop.html' : '/dashboard.html';
    } catch (error) {
        alert('Login failed: ' + error.message);
    }
});

let currentIndex = 0;
let cards;
const totalCards = 3;

window.addEventListener('DOMContentLoaded', () => {
    cards = document.querySelectorAll('.demo-card');
    
    cards.forEach(card => {
        card.addEventListener('click', (e) => {
            const index = parseInt(card.getAttribute('data-index'));
            if (index === 0) {
                const type = card.getAttribute('data-type');
                quickLogin(type);
            } else if (index === 1) {
                rotateCarousel(-1);
            } else if (index === 2) {
                rotateCarousel(1);
            }
        });
    });
});

function rotateCarousel(direction) {
    currentIndex = (currentIndex + direction + totalCards) % totalCards;
    updateCarousel();
}

function updateCarousel() {
    cards.forEach((card, index) => {
        card.classList.remove('active');
        const position = (index - currentIndex + totalCards) % totalCards;
        card.setAttribute('data-index', position);
        if (position === 0) {
            card.classList.add('active');
        }
    });
}

async function quickLogin(type) {
    const credentials = {
        staff: { email: 'demo@carwash.com', password: 'demo123' },
        admin: { email: 'admin@carwash.com', password: 'admin123' },
        client: { email: 'client@carwash.com', password: 'client123' }
    };
    
    const cred = credentials[type];
    if (!cred) return;
    
    try {
        const response = await API.auth.login(cred.email, cred.password);
        setToken(response.access_token);
        localStorage.setItem('userEmail', cred.email);
        localStorage.setItem('isDemo', response.is_demo);
        localStorage.setItem('user_permissions', JSON.stringify(response.permissions || []));
        
        const permissions = response.permissions || [];
        const isClient = permissions.includes('manage_cart') && !permissions.includes('manage_users');
        window.location.href = isClient ? '/shop.html' : '/dashboard.html';
    } catch (error) {
        alert(`${type.charAt(0).toUpperCase() + type.slice(1)} login failed: ` + error.message);
    }
}
