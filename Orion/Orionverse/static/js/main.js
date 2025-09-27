// static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    // This is the single source of truth for all navigation links.
    const NAV_CONFIG = {
        links: [
            { id: 'home', text: 'Home', file: 'templates/home.html' },
            { id: 'search-anything', text: 'Search Anything', file: 'templates/search_anything.html' },
            { id: 'billing', text: 'Billing', file: 'templates/billing.html' },
            { id: 'training', text: 'Training', file: 'templates/training.html' },
            { id: 'automation', text: 'Automation', file: 'templates/automation.html' },
            { id: 'release', text: 'Release', file: 'templates/release.html' },
            { id: 'welcome-kit', text: 'Welcome Kit', file: 'templates/welcome-kit.html' },
            { id: 'applications', text: 'Applications', file: 'templates/applications.html' },
            { id: 'abbreviation', text: 'Abbreviation', file: 'templates/abbreviation.html' },
            { id: 'teams', text: 'Teams', file: 'templates/teams.html' },
            { id: 'imp-links', text: 'Imp Links', file: 'templates/imp-links.html' },
            { id: 'database', text: 'DataBase', file: 'templates/database.html' },
            { id: 'events', text: 'Events', file: 'templates/events.html' },
            { id: 'assignments', text: 'Assignments', file: 'templates/assignments.html' },
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

    window.addEventListener('hashchange', handleNavigation);
    handleNavigation(); 
});