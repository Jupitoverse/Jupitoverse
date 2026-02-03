// main.js - Navigation and App Initialization

document.addEventListener('DOMContentLoaded', () => {
    // Configuration - Change API_BASE for deployment
    const CONFIG = {
        API_BASE: getAPIBase(),
        TABS: [
            { id: 'sqo', text: '⚡ SQO', file: 'templates/sqo.html', icon: '⚡' },
            { id: 'oni', text: '🔮 ONI', file: 'templates/oni.html', icon: '🔮' },
            { id: 'bulk-handling', text: '📦 Bulk Handling', file: 'templates/bulk.html', icon: '📦' }
        ]
    };

    // Determine API base URL based on environment
    function getAPIBase() {
        const hostname = window.location.hostname;
        // If running locally, use localhost
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://127.0.0.1:5003/api';
        }
        // For remote deployment, use same hostname with port 5003
        return `http://${hostname}:5003/api`;
    }

    // Make config globally accessible
    window.APP_CONFIG = CONFIG;

    const mainContent = document.getElementById('app-content');
    const mainNav = document.getElementById('main-nav');
    const statusDot = document.getElementById('connection-status');
    const statusText = document.getElementById('connection-text');

    // Build navigation
    function buildNav() {
        const hash = window.location.hash.substring(1) || 'sqo';
        mainNav.innerHTML = CONFIG.TABS
            .map(tab => `<a href="#${tab.id}" class="${tab.id === hash ? 'active' : ''}">${tab.text}</a>`)
            .join('');
    }

    // Load page content
    async function loadPage(pageId) {
        const tab = CONFIG.TABS.find(t => t.id === pageId);
        if (!tab) {
            loadPage('sqo');
            return;
        }

        try {
            const response = await fetch(tab.file);
            if (!response.ok) throw new Error('Page not found');
            mainContent.innerHTML = await response.text();
            
            // Initialize page-specific modules
            initializePage(pageId);
            
        } catch (error) {
            mainContent.innerHTML = `
                <div class="page">
                    <h1>❌ Error</h1>
                    <p>Failed to load page: ${error.message}</p>
                </div>
            `;
        }
    }

    // Initialize page-specific functionality
    function initializePage(pageId) {
        switch (pageId) {
            case 'sqo':
                if (typeof SQOAPI !== 'undefined') SQOAPI.init();
                break;
            case 'oni':
                if (typeof ONIAPI !== 'undefined') ONIAPI.init();
                break;
            case 'bulk-handling':
                if (typeof BulkAPI !== 'undefined') BulkAPI.init();
                break;
        }
    }

    // Handle navigation
    function handleNavigation() {
        const hash = window.location.hash.substring(1) || 'sqo';
        buildNav();
        loadPage(hash);
    }

    // Check API connectivity
    async function checkConnection() {
        try {
            const response = await fetch(`${CONFIG.API_BASE}/sqo/status`, { 
                method: 'GET',
                timeout: 5000 
            });
            const data = await response.json();
            
            statusDot.className = 'status-dot connected';
            statusText.textContent = 'Connected';
        } catch (error) {
            statusDot.className = 'status-dot error';
            statusText.textContent = 'Disconnected';
        }
    }

    // Initialize
    window.addEventListener('hashchange', handleNavigation);
    handleNavigation();
    checkConnection();
    
    // Periodically check connection
    setInterval(checkConnection, 30000);
});
