// Authentication Module
const API_BASE = 'http://localhost:8000/api/v1';

// Store tokens
const Auth = {
    getToken: () => localStorage.getItem('access_token'),
    getRefreshToken: () => localStorage.getItem('refresh_token'),
    getUser: () => JSON.parse(localStorage.getItem('user') || 'null'),
    
    setAuth: (data) => {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('user', JSON.stringify(data.user));
    },
    
    clearAuth: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
    },
    
    isLoggedIn: () => !!localStorage.getItem('access_token'),
    
    isAdmin: () => {
        const user = Auth.getUser();
        return user && (user.role === 'admin' || user.role === 'super_admin');
    },
    
    isPro: () => {
        const user = Auth.getUser();
        return user && user.subscription_plan === 'pro';
    },
    
    isPremium: () => {
        const user = Auth.getUser();
        return user && (user.subscription_plan === 'premium' || user.subscription_plan === 'pro');
    }
};

// API Helpers
async function apiRequest(endpoint, options = {}) {
    const token = Auth.getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.headers
    };
    
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        // Try to refresh token
        const refreshed = await refreshToken();
        if (refreshed) {
            // Retry with new token
            headers['Authorization'] = `Bearer ${Auth.getToken()}`;
            return fetch(`${API_BASE}${endpoint}`, { ...options, headers });
        } else {
            Auth.clearAuth();
            window.location.href = '/frontend/login.html';
        }
    }
    
    return response;
}

async function refreshToken() {
    const refreshToken = Auth.getRefreshToken();
    if (!refreshToken) return false;
    
    try {
        const response = await fetch(`${API_BASE}/auth/refresh`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh_token: refreshToken })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            return true;
        }
    } catch (error) {
        console.error('Token refresh failed:', error);
    }
    return false;
}

// Auth Functions
async function signup(email, password, fullName, referralCode = null) {
    try {
        const response = await fetch(`${API_BASE}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                email, 
                password, 
                full_name: fullName,
                referral_code: referralCode 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            Auth.setAuth(data);
            return { success: true, data };
        } else {
            return { success: false, error: data.detail || 'Signup failed' };
        }
    } catch (error) {
        return { success: false, error: error.message };
    }
}

async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            Auth.setAuth(data);
            return { success: true, data };
        } else {
            return { success: false, error: data.detail || 'Login failed' };
        }
    } catch (error) {
        return { success: false, error: error.message };
    }
}

function logout() {
    Auth.clearAuth();
    window.location.href = 'index.html';
}

// UI Update
function updateNavAuth() {
    const authButtons = document.getElementById('auth-buttons');
    const userMenu = document.getElementById('user-menu');
    
    if (!authButtons || !userMenu) return;
    
    if (Auth.isLoggedIn()) {
        const user = Auth.getUser();
        authButtons.classList.add('hidden');
        userMenu.classList.remove('hidden');
        
        // Update user name
        const userName = userMenu.querySelector('.user-name');
        if (userName) userName.textContent = user.full_name || user.email;
        
        // Show badge based on plan
        const badge = userMenu.querySelector('.user-badge');
        if (badge) {
            if (user.subscription_plan === 'pro') {
                badge.textContent = 'PRO';
                badge.className = 'badge badge-pro';
            } else if (user.subscription_plan === 'premium') {
                badge.textContent = 'PREMIUM';
                badge.className = 'badge badge-premium';
            } else {
                badge.textContent = 'FREE';
                badge.className = 'badge badge-free';
            }
        }
        
        // Show verified badge
        const verifiedBadge = userMenu.querySelector('.verified-badge');
        if (verifiedBadge && user.is_verified_employee) {
            verifiedBadge.classList.remove('hidden');
        }
        
        // Show admin link
        const adminLink = document.getElementById('admin-link');
        if (adminLink && Auth.isAdmin()) {
            adminLink.classList.remove('hidden');
        }
    } else {
        authButtons.classList.remove('hidden');
        userMenu.classList.add('hidden');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', updateNavAuth);

// Export
window.Auth = Auth;
window.apiRequest = apiRequest;
window.signup = signup;
window.login = login;
window.logout = logout;


