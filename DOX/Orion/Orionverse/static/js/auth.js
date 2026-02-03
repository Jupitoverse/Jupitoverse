// static/js/auth.js
const Auth = {
    currentUser: null,

    init() {
        // Check if user info is stored in the browser's session storage
        const storedUser = sessionStorage.getItem('orionverseUser');
        if (storedUser) {
            this.currentUser = JSON.parse(storedUser);
        }
        this.render();
    },

    render() {
        const container = document.getElementById('user-actions-container');
        if (this.currentUser) {
            container.innerHTML = `
                <span>Welcome, ${this.currentUser.fullname}</span>
                <button id="logout-btn" class="secondary-btn">Sign Out</button>
            `;
            document.getElementById('logout-btn').addEventListener('click', () => this.logout());
        } else {
            container.innerHTML = `<button id="login-signup-btn" class="primary-btn">Sign In / Sign Up</button>`;
            document.getElementById('login-signup-btn').addEventListener('click', () => this.showModal());
        }
    },

    showModal(isLogin = true) {
        const container = document.getElementById('auth-modal-container');
        const formTitle = isLogin ? 'Sign In' : 'Sign Up';
        const submitText = isLogin ? 'Sign In' : 'Create Account';
        const switchText = isLogin ? 'Need an account? Sign Up' : 'Already have an account? Sign In';
        
        container.innerHTML = `
            <div class="modal-overlay ${isLogin ? 'login-visible' : 'signup-visible'}">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>${formTitle}</h2>
                        <button class="modal-close-btn">&times;</button>
                    </div>
                    <form id="auth-form">
                        ${!isLogin ? `
                        <div class="form-group">
                            <label for="fullname">Full Name</label>
                            <input type="text" id="fullname" name="fullname" required>
                        </div>` : ''}
                        <div class="form-group">
                            <label for="email">Email</label>
                            <input type="email" id="email" name="email" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <div id="form-error" class="error-message" style="display:none;"></div>
                        <button type="submit" class="primary-btn">${submitText}</button>
                    </form>
                    <p style="margin-top: 15px; text-align: center;">
                        <a href="#" class="form-switch-link">${switchText}</a>
                    </p>
                </div>
            </div>
        `;

        // Event listeners
        container.querySelector('.modal-overlay').classList.add('visible');
        container.querySelector('.modal-close-btn').addEventListener('click', () => this.hideModal());
        container.querySelector('.form-switch-link').addEventListener('click', (e) => {
            e.preventDefault();
            this.showModal(!isLogin);
        });
        container.querySelector('#auth-form').addEventListener('submit', (e) => {
            e.preventDefault();
            isLogin ? this.handleLogin(e.target) : this.handleSignup(e.target);
        });
    },

    hideModal() {
        const modal = document.querySelector('#auth-modal-container .modal-overlay');
        if (modal) modal.classList.remove('visible');
    },

    async handleLogin(form) {
        const email = form.email.value;
        const password = form.password.value;
        const errorEl = document.getElementById('form-error');
        try {
            const data = await API.login(email, password);
            this.currentUser = data.user;
            sessionStorage.setItem('orionverseUser', JSON.stringify(data.user)); // Store session
            this.render();
            this.hideModal();
        } catch (error) {
            errorEl.textContent = error.message;
            errorEl.style.display = 'block';
        }
    },

    async handleSignup(form) {
        const fullname = form.fullname.value;
        const email = form.email.value;
        const password = form.password.value;
        const errorEl = document.getElementById('form-error');
        try {
            const data = await API.signup(fullname, email, password);
            alert(`Account created for ${data.fullname}. It is currently pending admin approval.`);
            this.showModal(true); // Switch to login view
        } catch (error) {
            errorEl.textContent = error.message;
            errorEl.style.display = 'block';
        }
    },

    logout() {
        this.currentUser = null;
        sessionStorage.removeItem('orionverseUser');
        this.render();
    }
};