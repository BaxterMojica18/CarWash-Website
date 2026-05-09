import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { firebaseConfig } from "./firebase-config.js";

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

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
        
        // Check onboarding status and redirect
        await checkOnboardingAndRedirect(response.permissions || []);

    } catch (error) {
        alert('Login failed: ' + error.message);
    }
});

// Add Google Login Handler
document.getElementById('googleLoginBtn').addEventListener('click', async function() {
    try {
        const result = await signInWithPopup(auth, googleProvider);
        const user = result.user;
        const idToken = await user.getIdToken();
        
        // Pass the Firebase ID token to the backend
        const response = await API.auth.firebaseLogin(idToken, user.email, user.displayName);
        handleLoginSuccess(response, user.email);
        
    } catch (error) {
        console.error("Google Auth error:", error);
        alert('Google Login failed: ' + error.message);
    }
});

function handleLoginSuccess(response, email) {
    setToken(response.access_token);
    localStorage.setItem('userEmail', email);
    localStorage.setItem('isDemo', response.is_demo);
    localStorage.setItem('user_permissions', JSON.stringify(response.permissions || []));
    
    // Check onboarding status and redirect
    checkOnboardingAndRedirect(response.permissions || []);
}

let currentIndex = 0;
let cards;
const totalCards = 3;

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
        
        // Check onboarding status and redirect
        await checkOnboardingAndRedirect(response.permissions || []);
    } catch (error) {
        alert(`${type.charAt(0).toUpperCase() + type.slice(1)} login failed: ` + error.message);
    }
}

async function checkOnboardingAndRedirect(permissions) {
    try {
        const meData = await fetch(`${API_BASE}/auth/me/permissions`, {
            headers: { 'Authorization': `Bearer ${getToken()}` }
        }).then(r => r.json());

        const onboardingCompleted = meData.onboarding_completed;
        localStorage.setItem('onboarding_completed', onboardingCompleted ? 'true' : 'false');

        if (meData.roles) {
            localStorage.setItem('roles', JSON.stringify(meData.roles));
        }

        if (onboardingCompleted === false) {
            window.location.href = '/onboarding.html';
            return;
        }
    } catch(e) {
        console.warn('Could not check onboarding status:', e);
    }

    // Default redirect based on permissions
    const isClient = permissions.includes('manage_cart') && !permissions.includes('manage_users');
    window.location.href = isClient ? '/shop.html' : '/dashboard.html';
}
