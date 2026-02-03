// AI Spectrum India - Unified Header Component
(function() {
    // Detect current page
    function getCurrentPage() {
        const path = window.location.pathname.toLowerCase();
        if (path.includes('companies')) return 'companies';
        if (path.includes('jobs')) return 'jobs';
        if (path.includes('abroad')) return 'abroad';
        if (path.includes('hr-contact')) return 'hr';
        if (path.includes('ai-tools')) return 'ai-tools';
        if (path.includes('git-repos')) return 'git-repos';
        if (path.includes('community')) return 'community';
        if (path.includes('resources')) return 'resources';
        if (path.includes('roadmap')) return 'roadmaps';
        if (path.includes('referral')) return 'referrals';
        if (path.includes('dashboard')) return 'dashboard';
        return 'home';
    }

    function createHeader() {
        const activePage = getCurrentPage();
        
        const header = document.createElement('header');
        header.className = 'site-header';
        header.innerHTML = `
            <div class="header-container">
                <a href="index.html" class="site-logo">
                    <span class="icon">🎯</span>
                    <span>AI Spectrum <span class="highlight">India</span></span>
                </a>
                
                <ul class="main-menu">
                    <li><a href="index.html" class="${activePage === 'home' ? 'active' : ''}">Home</a></li>
                    <li><a href="companies.html" class="${activePage === 'companies' ? 'active' : ''}">Companies</a></li>
                    <li><a href="abroad.html" target="_blank" class="${activePage === 'abroad' ? 'active' : ''}">Abroad 🌍</a></li>
                    <li><a href="hr-contacts.html" class="${activePage === 'hr' ? 'active' : ''}">HR Contacts<span class="badge-hot">HOT</span></a></li>
                    <li><a href="ai-tools.html" class="${activePage === 'ai-tools' ? 'active' : ''}">AI Tools</a></li>
                    <li><a href="git-repos.html" class="${activePage === 'git-repos' ? 'active' : ''}">Git Repos<span class="badge-hot">NEW</span></a></li>
                    <li><a href="resources.html" class="${activePage === 'resources' ? 'active' : ''}">Resources</a></li>
                    <li><a href="community.html" class="${activePage === 'community' ? 'active' : ''}">Community</a></li>
                </ul>
                
                <div class="header-actions">
                    <div id="guest-actions">
                        <a href="login.html" class="btn btn-secondary">Login</a>
                        <a href="signup.html" class="btn btn-primary">Sign Up Free</a>
                    </div>
                    <div id="user-actions" style="display:none;">
                        <span class="user-badge badge-free" id="user-plan">FREE</span>
                        <a href="dashboard.html" class="btn btn-secondary">Dashboard</a>
                        <button class="btn btn-ghost" onclick="logoutUser()">Logout</button>
                    </div>
                </div>
            </div>
        `;
        
        return header;
    }

    function updateAuthState() {
        const token = localStorage.getItem('accessToken');
        const userData = localStorage.getItem('user');
        
        const guestActions = document.getElementById('guest-actions');
        const userActions = document.getElementById('user-actions');
        const userPlan = document.getElementById('user-plan');
        
        if (token && userData) {
            try {
                const user = JSON.parse(userData);
                if (guestActions) guestActions.style.display = 'none';
                if (userActions) userActions.style.display = 'flex';
                
                if (userPlan && user.subscription_plan) {
                    const plan = user.subscription_plan.toLowerCase();
                    userPlan.textContent = plan.toUpperCase();
                    userPlan.className = 'user-badge badge-' + plan;
                }
            } catch (e) {
                console.error('Auth parse error:', e);
            }
        }
    }

    // Logout function
    window.logoutUser = function() {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
        window.location.href = 'index.html';
    };

    // Initialize
    function init() {
        // Remove any existing header/nav
        const existingHeader = document.querySelector('header.site-header');
        const existingNav = document.querySelector('nav');
        if (existingHeader) existingHeader.remove();
        if (existingNav) existingNav.remove();
        
        // Insert new header
        const header = createHeader();
        document.body.insertBefore(header, document.body.firstChild);
        
        // Update auth state
        updateAuthState();
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
