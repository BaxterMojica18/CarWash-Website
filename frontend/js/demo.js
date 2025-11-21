let currentIndex = 0;
let cards;
const totalCards = 3;

const credentials = {
    staff: { email: 'demo@carwash.com', password: 'demo123', title: '👨💼 Staff Login' },
    admin: { email: 'admin@carwash.com', password: 'admin123', title: '🔑 Admin Login' },
    client: { email: 'client@carwash.com', password: 'client123', title: '🛒 Client Login' }
};

window.addEventListener('DOMContentLoaded', () => {
    cards = document.querySelectorAll('.demo-card');
    
    cards.forEach(card => {
        card.addEventListener('click', (e) => {
            const index = parseInt(card.getAttribute('data-index'));
            if (index === 0) {
                const type = card.getAttribute('data-type');
                showLoginForm(type);
            } else if (index === 1) {
                rotateCarousel(-1);
            } else if (index === 2) {
                rotateCarousel(1);
            }
        });
    });

    document.getElementById('demoLoginForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const email = document.getElementById('demoEmail').value;
        const password = document.getElementById('demoPassword').value;
        
        try {
            const response = await API.auth.login(email, password);
            setToken(response.access_token);
            localStorage.setItem('userEmail', email);
            localStorage.setItem('isDemo', response.is_demo);
            localStorage.setItem('user_permissions', JSON.stringify(response.permissions || []));
            
            const permissions = response.permissions || [];
            const isClient = permissions.includes('manage_cart') && !permissions.includes('manage_users');
            window.location.href = isClient ? '/client-dashboard.html' : '/dashboard.html';
        } catch (error) {
            alert('Login failed: ' + error.message);
        }
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

function showLoginForm(type) {
    const cred = credentials[type];
    document.getElementById('loginTitle').textContent = cred.title;
    document.getElementById('demoEmail').value = cred.email;
    document.getElementById('demoPassword').value = cred.password;
    document.querySelector('.carousel-container').style.display = 'none';
    document.getElementById('loginSection').style.display = 'block';
}

function hideLoginForm() {
    document.querySelector('.carousel-container').style.display = 'flex';
    document.getElementById('loginSection').style.display = 'none';
}
