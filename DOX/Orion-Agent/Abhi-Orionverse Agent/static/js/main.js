// static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    // This is the single source of truth for all navigation links.
    // RAG Integration: Smart SR Assignment, Smart Team, My Dashboard
    const NAV_CONFIG = {
        links: [
            { id: 'home', text: 'Home', file: 'templates/home.html' },
            { id: 'my-dashboard', text: '📊 My Dashboard', file: 'templates/my_dashboard.html' },
            { id: 'smart-sr', text: '🤖 Smart SR Assignment', file: 'templates/smart_sr_assignment.html' },
            { id: 'smart-team', text: '👥 Smart Team', file: 'templates/smart_team.html' },
            { id: 'bulk-handling', text: 'Bulk Handling', file: 'templates/bulk_handling.html' },
            { id: 'search-anything', text: 'Search Anything', file: 'templates/search_anything.html' },
            { id: 'dashboard', text: 'Dashboard', file: 'templates/dashboard.html' },
            { id: 'stuck-activities', text: 'Stuck Activities', file: 'templates/stuck_activities.html' },
            { id: 'top-offender', text: 'Top Offender', file: 'templates/top_offender.html' },
            { id: 'welcome-kit', text: 'Welcome Kit', file: 'templates/welcome-kit.html' },
            { id: 'billing', text: 'Billing', file: 'templates/billing.html' },
            { id: 'sr-handling', text: 'SR Handling', file: 'templates/sr_handling.html' },
            { id: 'links', text: 'Links', file: 'templates/links.html' },
            { id: 'release', text: 'Release', file: 'templates/release.html' },
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
    SmartSR.init();  // Initialize Smart SR Assignment module

    window.addEventListener('hashchange', handleNavigation);
    handleNavigation(); 
});