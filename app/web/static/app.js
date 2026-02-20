// Authentication token management
const getToken = () => localStorage.getItem('auth_token');
const setToken = (token) => localStorage.setItem('auth_token', token);
const clearToken = () => localStorage.removeItem('auth_token');

// API base URL
const API_BASE = '';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const token = getToken();
    if (token) {
        showDashboard();
        loadSystemStatus();
    } else {
        showLogin();
    }

    // Event listeners
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    document.getElementById('assistant-form').addEventListener('submit', handleAssistant);
});

// Show/Hide functions
function showLogin() {
    document.getElementById('login-container').style.display = 'block';
    document.getElementById('dashboard-container').style.display = 'none';
}

function showDashboard() {
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('dashboard-container').style.display = 'block';
}

// Login handler
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('login-error');

    try {
        const response = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            throw new Error('Invalid credentials');
        }

        const data = await response.json();
        setToken(data.access_token);
        errorEl.classList.remove('show');
        showDashboard();
        loadSystemStatus();
    } catch (error) {
        errorEl.textContent = error.message;
        errorEl.classList.add('show');
    }
}

// Logout handler
function handleLogout() {
    clearToken();
    document.getElementById('login-form').reset();
    showLogin();
}

// Load system status
async function loadSystemStatus() {
    const statusEl = document.getElementById('status');
    try {
        const response = await fetch(`${API_BASE}/api/ping`);
        const data = await response.json();
        
        if (data.ok) {
            statusEl.innerHTML = `
                <p><strong>✓ System Status: Operational</strong></p>
                <p>Server Time: ${new Date(data.t).toLocaleString()}</p>
            `;
            statusEl.classList.add('success');
        } else {
            statusEl.innerHTML = '<p>System status unavailable</p>';
        }
    } catch (error) {
        statusEl.innerHTML = `<p>Error checking system status: ${error.message}</p>`;
        statusEl.classList.add('error');
    }
}

// Assistant handler
async function handleAssistant(e) {
    e.preventDefault();
    const prompt = document.getElementById('prompt').value;
    const responseEl = document.getElementById('response');
    const token = getToken();

    responseEl.classList.add('loading', 'show');
    responseEl.innerHTML = 'Processing...';

    try {
        const response = await fetch(`${API_BASE}/api/assistant`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) {
            throw new Error('Request failed');
        }

        const data = await response.json();
        responseEl.classList.remove('loading');
        responseEl.innerHTML = `<p>${data.text}</p>`;
        document.getElementById('prompt').value = '';
    } catch (error) {
        responseEl.classList.remove('loading');
        responseEl.innerHTML = `<p style="color: #dc3545;">Error: ${error.message}</p>`;
    }
}