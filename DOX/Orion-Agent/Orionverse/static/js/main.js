// static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    // This is the single source of truth for all navigation links.
    const NAV_CONFIG = {
        links: [
            // Requested order (main tabs first)
            { id: 'home', text: 'Home', file: 'templates/home.html' },
            { id: 'welcome-kit', text: 'Welcome Kit', file: 'templates/welcome-kit.html' },
            { id: 'links', text: 'Link', file: 'templates/links.html' },
            { id: 'dashboard', text: 'Operational Dashboard', file: 'templates/dashboard.html' },
            { id: 'billing', text: 'Billing', file: 'templates/billing.html' },
            { id: 'activity-data', text: '📊 Activity Data', file: 'templates/activity_data.html' },
            { id: 'oni', text: '🔮 ONI', file: 'templates/oni.html' },
            { id: 'sqo', text: '⚡ SQO', file: 'templates/sqo.html' },
            { id: 'stuck-activities', text: 'Fallout Team', file: 'templates/stuck_activities.html' },
            { id: 'release', text: 'Release', file: 'templates/release.html' },
            // All other original tabs (kept visible - no tabs removed)
            { id: 'bulk-handling', text: 'Bulk Handling', file: 'templates/bulk_handling.html' },
            { id: 'search-anything', text: 'Search Anything', file: 'templates/search_anything.html' },
            { id: 'top-offender', text: 'Top Offender', file: 'templates/top_offender.html' },
            { id: 'sr-handling', text: 'SR Handling', file: 'templates/sr_handling.html' },
            { id: 'training', text: 'Training', file: 'templates/training.html' },
        ],
    };

    const mainContent = document.getElementById('app-content');
    const mainNav = document.getElementById('main-nav');

    async function loadPage(pageId, url) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Page not found: ${url}`);
            mainContent.innerHTML = await response.text();
            
            const event = new CustomEvent('pageLoaded', { detail: { pageId: pageId } });
            document.dispatchEvent(event);

        } catch (error) {
            mainContent.innerHTML = `<p class="error-message">Error loading page: ${error.message}</p>`;
        }
    }

    function handleNavigation() {
        const hash = window.location.hash.substring(1) || 'home';
        const activeLink = NAV_CONFIG.links.find(link => link.id === hash);

        mainNav.innerHTML = NAV_CONFIG.links
            .map(link => `<a href="#${link.id}" class="${link.id === hash ? 'active' : ''}">${link.text}</a>`)
            .join('');

        if (activeLink) {
            loadPage(activeLink.id, activeLink.file);
        } else {
            loadPage('home', '/templates/home.html');
        }
    }

    // --- Application Initialization ---
    Auth.init();
    SearchAnything.init();
    
    // Initialize API Console for SQO and ONI tabs
    if (typeof APIConsole !== 'undefined') {
        APIConsole.init();
    }

    window.addEventListener('hashchange', handleNavigation);
    handleNavigation(); 
});