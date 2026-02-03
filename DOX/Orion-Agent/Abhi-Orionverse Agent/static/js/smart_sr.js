// static/js/smart_sr.js
/**
 * Smart SR Assignment Module
 * Handles RAG-based SR analysis functionality
 */

// Use the API_BASE_URL from api.js (should be http://127.0.0.1:5002)
const SMART_SR_API_BASE = (typeof API_BASE_URL !== 'undefined' ? API_BASE_URL : 'http://127.0.0.1:5002') + '/api/smart-sr';
console.log('[SmartSR] API Base:', SMART_SR_API_BASE);

const SmartSR = {
    // API Base URL - use full URL for cross-port communication
    API_BASE: SMART_SR_API_BASE,
    
    // State
    isInitialized: false,
    currentAnalysis: null,
    
    /**
     * Initialize the Smart SR module
     */
    init() {
        document.addEventListener('pageLoaded', (e) => {
            if (e.detail.pageId === 'smart-sr') {
                console.log('[SmartSR] Page loaded, initializing...');
                this.setupPage();
            }
        });
    },
    
    /**
     * Setup the page - attach event listeners and load initial data
     */
    async setupPage() {
        this.attachEventListeners();
        await this.checkSystemStatus();
        await this.loadStats();
        this.isInitialized = true;
        console.log('[SmartSR] Setup complete');
    },
    
    /**
     * Attach all event listeners
     */
    attachEventListeners() {
        // Tab switching
        document.querySelectorAll('.smart-sr-tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
        
        // Analyze form
        const analyzeForm = document.getElementById('analyze-sr-form');
        if (analyzeForm) {
            analyzeForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.analyzeSR();
            });
        }
        
        // Clear form button
        const clearBtn = document.getElementById('clear-form-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearForm());
        }
        
        // Copy results button
        const copyBtn = document.getElementById('copy-results-btn');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => this.copyResults());
        }
        
        // Semantic search button
        const searchBtn = document.getElementById('semantic-search-btn');
        if (searchBtn) {
            searchBtn.addEventListener('click', () => this.performSemanticSearch());
        }
        
        // File upload
        const dropzone = document.getElementById('upload-dropzone');
        const fileInput = document.getElementById('batch-file-input');
        
        if (dropzone) {
            dropzone.addEventListener('click', () => fileInput.click());
            dropzone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropzone.classList.add('dragover');
            });
            dropzone.addEventListener('dragleave', () => {
                dropzone.classList.remove('dragover');
            });
            dropzone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropzone.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length) this.handleFileUpload(files[0]);
            });
        }
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length) {
                    this.handleFileUpload(e.target.files[0]);
                }
            });
        }
        
        console.log('[SmartSR] Event listeners attached');
    },
    
    /**
     * Switch between tabs
     */
    switchTab(tabId) {
        // Update tab buttons
        document.querySelectorAll('.smart-sr-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabId);
        });
        
        // Update content sections
        document.querySelectorAll('.smart-sr-content').forEach(content => {
            content.classList.toggle('active', content.id === `tab-${tabId}`);
        });
    },
    
    /**
     * Check RAG system status
     */
    async checkSystemStatus() {
        const banner = document.getElementById('rag-status-banner');
        const dot = banner?.querySelector('.status-dot');
        const text = banner?.querySelector('.status-text');
        
        try {
            const response = await fetch(`${this.API_BASE}/status`);
            const status = await response.json();
            
            if (status.pipeline_status === 'ready') {
                dot.classList.add('ready');
                text.textContent = 'RAG System Ready';
            } else if (status.pipeline_status.startsWith('error')) {
                dot.classList.add('error');
                text.textContent = 'RAG System Error - ' + status.pipeline_status;
            } else {
                text.textContent = 'RAG System Initializing...';
            }
            
            console.log('[SmartSR] System status:', status);
        } catch (error) {
            console.error('[SmartSR] Status check failed:', error);
            if (dot) dot.classList.add('error');
            if (text) text.textContent = 'Cannot connect to backend';
        }
    },
    
    /**
     * Load system statistics
     */
    async loadStats() {
        try {
            const response = await fetch(`${this.API_BASE}/stats`);
            const stats = await response.json();
            
            document.getElementById('stat-vectorstore').textContent = 
                stats.vectorstore_records?.toLocaleString() || '-';
            document.getElementById('stat-processed').textContent = 
                stats.total_srs_processed?.toLocaleString() || '-';
            document.getElementById('stat-team').textContent = 
                stats.team_members || '-';
            document.getElementById('stat-categories').textContent = 
                stats.categories?.length || '-';
                
        } catch (error) {
            console.error('[SmartSR] Failed to load stats:', error);
        }
    },
    
    /**
     * Analyze a single SR
     */
    async analyzeSR() {
        const srId = document.getElementById('sr-id-input').value;
        const description = document.getElementById('sr-description-input').value;
        const category = document.getElementById('sr-category-input').value;
        const customerId = document.getElementById('sr-customer-input').value;
        const updates = document.getElementById('sr-updates-input').value;
        
        if (!description) {
            alert('Please enter SR description');
            return;
        }
        
        this.showLoader('Analyzing SR with AI...');
        
        try {
            const response = await fetch(`${this.API_BASE}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sr_id: srId,
                    description: description,
                    category: category,
                    customer_id: customerId,
                    update_details: updates
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.currentAnalysis = result;
                this.displayResults(result.analysis);
            } else {
                alert('Analysis failed: ' + result.error);
            }
            
        } catch (error) {
            console.error('[SmartSR] Analysis failed:', error);
            alert('Analysis failed: ' + error.message);
        } finally {
            this.hideLoader();
        }
    },
    
    /**
     * Display analysis results
     */
    displayResults(analysis) {
        const resultsSection = document.getElementById('analysis-results');
        resultsSection.style.display = 'block';
        
        // Update result fields
        document.getElementById('result-workaround').innerHTML = 
            analysis.semantic_workaround || analysis.suggested_workaround || 'No workaround found';
        
        document.getElementById('result-java').innerHTML = 
            analysis.is_java_error ? 
                '<span style="color: #059669;">Yes - Java Error Detected</span>' : 
                '<span style="color: #6b7280;">No - Non-Java Issue</span>';
        
        document.getElementById('result-category').textContent = 
            analysis.categorization || analysis.category || 'Uncategorized';
        
        document.getElementById('result-assignment').textContent = 
            analysis.assigned_to || analysis.team_assignment || 'Not assigned';
        
        document.getElementById('result-resolution').innerHTML = 
            analysis.ai_resolution || analysis.resolution || 'No resolution generated';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    },
    
    /**
     * Clear the analysis form
     */
    clearForm() {
        document.getElementById('sr-id-input').value = '';
        document.getElementById('sr-description-input').value = '';
        document.getElementById('sr-category-input').value = '';
        document.getElementById('sr-customer-input').value = '';
        document.getElementById('sr-updates-input').value = '';
        document.getElementById('analysis-results').style.display = 'none';
        this.currentAnalysis = null;
    },
    
    /**
     * Copy results to clipboard
     */
    copyResults() {
        if (!this.currentAnalysis) {
            alert('No results to copy');
            return;
        }
        
        const analysis = this.currentAnalysis.analysis;
        const text = `
SR Analysis Results
===================
SR ID: ${this.currentAnalysis.sr_id}
Category: ${analysis.categorization || 'N/A'}
Java Error: ${analysis.is_java_error ? 'Yes' : 'No'}
Assigned To: ${analysis.assigned_to || 'N/A'}

Workaround:
${analysis.semantic_workaround || analysis.suggested_workaround || 'N/A'}

Resolution:
${analysis.ai_resolution || analysis.resolution || 'N/A'}
        `.trim();
        
        navigator.clipboard.writeText(text).then(() => {
            alert('Results copied to clipboard!');
        });
    },
    
    /**
     * Perform semantic search
     */
    async performSemanticSearch() {
        const query = document.getElementById('semantic-query').value;
        const limit = document.getElementById('search-limit').value;
        
        if (!query) {
            alert('Please enter a search query');
            return;
        }
        
        this.showLoader('Searching...');
        
        try {
            const response = await fetch(`${this.API_BASE}/semantic-search`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, limit: parseInt(limit) })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.displaySearchResults(result.results);
            } else {
                alert('Search failed: ' + result.error);
            }
            
        } catch (error) {
            console.error('[SmartSR] Search failed:', error);
            alert('Search failed: ' + error.message);
        } finally {
            this.hideLoader();
        }
    },
    
    /**
     * Display semantic search results
     */
    displaySearchResults(results) {
        const container = document.getElementById('semantic-results');
        
        if (!results || results.length === 0) {
            container.innerHTML = '<p class="empty-state">No similar SRs found</p>';
            return;
        }
        
        container.innerHTML = results.map((result, index) => `
            <div class="search-result-card">
                <div class="result-header">
                    <span class="result-rank">#${index + 1}</span>
                    <span class="result-id">${result.sr_id || result.call_id || 'Unknown'}</span>
                    <span class="result-score">Score: ${(result.score * 100).toFixed(1)}%</span>
                </div>
                <p class="result-description">${result.description || result.details || ''}</p>
                ${result.workaround ? `
                    <div class="result-workaround">
                        <strong>Workaround:</strong> ${result.workaround}
                    </div>
                ` : ''}
            </div>
        `).join('');
    },
    
    /**
     * Handle file upload for batch analysis
     */
    async handleFileUpload(file) {
        console.log('[SmartSR] File uploaded:', file.name);
        
        // For now, show a message - batch upload requires more backend work
        alert('Batch upload feature coming soon! Use the single SR analysis for now.');
    },
    
    /**
     * Show loading overlay
     */
    showLoader(text = 'Processing...') {
        const loader = document.getElementById('smart-sr-loader');
        const loaderText = loader?.querySelector('.loader-text');
        if (loader) {
            loader.style.display = 'flex';
            if (loaderText) loaderText.textContent = text;
        }
    },
    
    /**
     * Hide loading overlay
     */
    hideLoader() {
        const loader = document.getElementById('smart-sr-loader');
        if (loader) loader.style.display = 'none';
    }
};

// Export for global use
window.SmartSR = SmartSR;


/**
 * Smart Team Module
 * Handles team management and skill-based assignment configuration
 */
const SmartTeam = {
    API_BASE: SMART_SR_API_BASE,
    currentMember: null,
    teamData: [],
    
    init() {
        document.addEventListener('pageLoaded', (e) => {
            if (e.detail.pageId === 'smart-team') {
                console.log('[SmartTeam] Page loaded, initializing...');
                this.setupPage();
            }
        });
    },
    
    async setupPage() {
        this.attachEventListeners();
        await this.loadTeamData();
    },
    
    attachEventListeners() {
        // Add member button
        const addBtn = document.getElementById('add-member-btn');
        if (addBtn) addBtn.addEventListener('click', () => this.openAddMemberModal());
        
        // Reassign button
        const reassignBtn = document.getElementById('reassign-srs-btn');
        if (reassignBtn) reassignBtn.addEventListener('click', () => this.reassignTodaysSRs());
        
        // Refresh button
        const refreshBtn = document.getElementById('refresh-team-btn');
        if (refreshBtn) refreshBtn.addEventListener('click', () => this.loadTeamData());
        
        // Search input
        const searchInput = document.getElementById('team-search');
        if (searchInput) searchInput.addEventListener('input', (e) => this.filterMembers(e.target.value));
        
        // Add member form
        const addForm = document.getElementById('add-member-form');
        if (addForm) addForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitAddMember();
        });
    },
    
    async loadTeamData() {
        const container = document.getElementById('team-members-container');
        container.innerHTML = '<div class="loading-state"><div class="loader-spinner"></div><p>Loading team members...</p></div>';
        
        console.log('[SmartTeam] Loading team data from:', `${this.API_BASE}/team/members`);
        
        try {
            const response = await fetch(`${this.API_BASE}/team/members`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('[SmartTeam] Team data received:', data);
            
            if (data.success) {
                this.teamData = data.people || [];
                this.renderMembers(this.teamData);
                this.updateStats(this.teamData);
            } else {
                const errorMsg = data.error || 'Unknown error loading team data';
                container.innerHTML = `<div class="error-state">
                    <div class="error-icon">⚠️</div>
                    <p>Failed to load team data</p>
                    <p class="error-detail">${errorMsg}</p>
                </div>`;
            }
        } catch (error) {
            console.error('[SmartTeam] Load failed:', error);
            container.innerHTML = `<div class="error-state">
                <div class="error-icon">❌</div>
                <p>Cannot connect to backend</p>
                <p class="error-detail">API: ${this.API_BASE}/team/members</p>
                <p class="error-detail">Error: ${error.message}</p>
                <button class="primary-btn" onclick="SmartTeam.loadTeamData()">🔄 Retry</button>
            </div>`;
        }
    },
    
    updateStats(people) {
        document.getElementById('total-members').textContent = people.length;
        let totalSkills = 0;
        let available = 0;
        let totalLoad = 0;
        
        people.forEach(p => {
            if (p.skills) totalSkills += p.skills.length;
            if (p.availability_percent >= 50) available++;
            totalLoad += p.current_load || 0;
        });
        
        document.getElementById('total-skills').textContent = totalSkills;
        document.getElementById('available-members').textContent = available;
        document.getElementById('todays-load').textContent = totalLoad;
    },
    
    renderMembers(people) {
        const container = document.getElementById('team-members-container');
        
        if (!people || people.length === 0) {
            container.innerHTML = '<p class="empty-state">No team members found</p>';
            return;
        }
        
        container.innerHTML = people.map(person => {
            const loadPercent = person.max_load ? Math.round((person.current_load / person.max_load) * 100) : 0;
            let capacityClass = 'available';
            if (loadPercent >= 100) capacityClass = 'full';
            else if (loadPercent >= 70) capacityClass = 'busy';
            
            const skillsHtml = person.skills && person.skills.length > 0 
                ? `<table class="skills-table">
                    <tr><th>App</th><th>Level</th><th>Max Load</th></tr>
                    ${person.skills.map(s => `
                        <tr>
                            <td class="skill-app">${s.application}</td>
                            <td class="skill-level">${s.skill_level}/5</td>
                            <td>${s.max_load}</td>
                        </tr>
                    `).join('')}
                   </table>`
                : '<p class="no-skills">No skills configured</p>';
            
            return `
                <div class="member-card" data-name="${person.name.toLowerCase()}">
                    <div class="member-card-header">
                        <span class="member-name">👤 ${person.name}</span>
                        <div class="member-header-actions">
                            <button onclick="SmartTeam.openEditSkillsModal('${person.name}')">✏️ Edit</button>
                            <button class="danger-btn" onclick="SmartTeam.removeMember('${person.name}')">🗑️</button>
                        </div>
                    </div>
                    <div class="member-card-body">
                        <div class="member-info-row">
                            <span class="info-label">Current Load</span>
                            <span class="info-value">${person.current_load || 0} / ${person.max_load || 10}</span>
                        </div>
                        <div class="member-info-row">
                            <span class="info-label">Status</span>
                            <span class="capacity-badge ${capacityClass}">${loadPercent}% Capacity</span>
                        </div>
                        <div class="member-info-row">
                            <span class="info-label">Availability</span>
                            <span class="info-value">${person.availability_percent || 100}%</span>
                        </div>
                        <div class="member-skills">
                            <span class="skills-title">🎯 Skills</span>
                            ${skillsHtml}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    },
    
    filterMembers(searchText) {
        const cards = document.querySelectorAll('.member-card');
        const search = searchText.toLowerCase();
        
        cards.forEach(card => {
            const name = card.dataset.name;
            const text = card.textContent.toLowerCase();
            card.style.display = (name.includes(search) || text.includes(search)) ? 'block' : 'none';
        });
    },
    
    openAddMemberModal() {
        document.getElementById('add-member-modal').classList.add('visible');
    },
    
    closeAddMemberModal() {
        document.getElementById('add-member-modal').classList.remove('visible');
        document.getElementById('add-member-form').reset();
    },
    
    async submitAddMember() {
        const memberName = document.getElementById('new-member-name').value.trim();
        const application = document.getElementById('new-application').value;
        const skillLevel = parseInt(document.getElementById('new-skill-level').value);
        const specializations = document.getElementById('new-specializations').value;
        const maxLoad = parseInt(document.getElementById('new-max-load').value);
        
        if (!memberName) {
            this.showToast('Please enter member name', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.API_BASE}/team/add-member`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ member_name: memberName, application, skill_level: skillLevel, specializations, max_load: maxLoad })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast(`✅ ${memberName} added successfully`, 'success');
                this.closeAddMemberModal();
                this.loadTeamData();
            } else {
                this.showToast(`❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showToast('❌ Failed to add member', 'error');
        }
    },
    
    async removeMember(memberName) {
        if (!confirm(`Are you sure you want to remove ${memberName}?`)) return;
        
        try {
            const response = await fetch(`${this.API_BASE}/team/remove-member`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ member_name: memberName })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast(`✅ ${memberName} removed`, 'success');
                this.loadTeamData();
            } else {
                this.showToast(`❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showToast('❌ Failed to remove member', 'error');
        }
    },
    
    openEditSkillsModal(memberName) {
        this.currentMember = memberName;
        document.getElementById('edit-skills-member-name').textContent = memberName;
        document.getElementById('edit-skills-modal').classList.add('visible');
        this.loadMemberSkills(memberName);
    },
    
    closeEditSkillsModal() {
        document.getElementById('edit-skills-modal').classList.remove('visible');
        this.currentMember = null;
    },
    
    async loadMemberSkills(memberName) {
        const container = document.getElementById('member-skills-container');
        container.innerHTML = '<p>Loading skills...</p>';
        
        try {
            const response = await fetch(`${this.API_BASE}/team/member-skills?member_name=${encodeURIComponent(memberName)}`);
            const data = await response.json();
            
            if (data.success && data.skills.length > 0) {
                container.innerHTML = `
                    <table class="skills-table">
                        <tr><th>Application</th><th>Level</th><th>Specializations</th><th>Max Load</th><th></th></tr>
                        ${data.skills.map(s => `
                            <tr>
                                <td class="skill-app">${s.application}</td>
                                <td>${s.skill_level}/5</td>
                                <td>${(s.specializations || []).join(', ') || '-'}</td>
                                <td>${s.max_load}</td>
                                <td><button class="secondary-btn" onclick="SmartTeam.removeSkill('${s.application}')">🗑️</button></td>
                            </tr>
                        `).join('')}
                    </table>
                `;
            } else {
                container.innerHTML = '<p class="no-skills">No skills configured</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="error-message">Failed to load skills</p>';
        }
    },
    
    async saveNewSkill() {
        const application = document.getElementById('skill-app').value;
        const skillLevel = parseFloat(document.getElementById('skill-level').value);
        const specs = document.getElementById('skill-specs').value;
        const maxLoad = parseInt(document.getElementById('skill-max-load').value);
        
        try {
            const response = await fetch(`${this.API_BASE}/team/save-skill`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ member_name: this.currentMember, application, skill_level: skillLevel, specializations: specs, max_load: maxLoad })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast('✅ Skill saved', 'success');
                this.loadMemberSkills(this.currentMember);
            } else {
                this.showToast(`❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showToast('❌ Failed to save skill', 'error');
        }
    },
    
    async removeSkill(application) {
        try {
            const response = await fetch(`${this.API_BASE}/team/remove-skill`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ member_name: this.currentMember, application })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast('✅ Skill removed', 'success');
                this.loadMemberSkills(this.currentMember);
            } else {
                this.showToast(`❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showToast('❌ Failed to remove skill', 'error');
        }
    },
    
    async reassignTodaysSRs() {
        if (!confirm('This will reassign ALL SRs uploaded today using AI. Continue?')) return;
        
        this.showToast('🔄 Reassigning SRs...', 'info');
        
        try {
            const response = await fetch(`${this.API_BASE}/team/batch-reassign`, { method: 'POST' });
            const data = await response.json();
            
            if (data.success) {
                this.showToast(`✅ Reassigned ${data.assigned_count} SRs`, 'success');
            } else {
                this.showToast(`❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showToast('❌ Reassignment failed', 'error');
        }
    },
    
    showToast(message, type = 'info') {
        const toast = document.getElementById('team-toast');
        toast.textContent = message;
        toast.className = `toast-message ${type} show`;
        setTimeout(() => toast.classList.remove('show'), 4000);
    }
};

window.SmartTeam = SmartTeam;


/**
 * My Dashboard Module
 * Personal SR analysis portal with AI-powered workarounds
 */
const MyDashboard = {
    API_BASE: SMART_SR_API_BASE,
    currentSR: null,
    
    init() {
        document.addEventListener('pageLoaded', (e) => {
            if (e.detail.pageId === 'my-dashboard') {
                console.log('[MyDashboard] Page loaded, initializing...');
                this.setupPage();
            }
        });
    },
    
    async setupPage() {
        this.attachEventListeners();
        await this.loadDatabaseInfo();
    },
    
    attachEventListeners() {
        // Search button
        const searchBtn = document.getElementById('search-sr-btn');
        if (searchBtn) searchBtn.addEventListener('click', () => this.searchSR());
        
        // Search on Enter
        const searchInput = document.getElementById('sr-search-input');
        if (searchInput) searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchSR();
        });
        
        // Feedback form
        const feedbackForm = document.getElementById('feedback-form');
        if (feedbackForm) feedbackForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitWorkaround();
        });
        
        // Clear button
        const clearBtn = document.getElementById('clear-workaround-btn');
        if (clearBtn) clearBtn.addEventListener('click', () => {
            document.getElementById('user-workaround-input').value = '';
        });
    },
    
    async loadDatabaseInfo() {
        console.log('[MyDashboard] Loading database info from:', `${this.API_BASE}/database-info`);
        
        try {
            const response = await fetch(`${this.API_BASE}/database-info`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('[MyDashboard] Database info received:', data);
            
            const infoSpan = document.getElementById('database-info');
            if (data.has_upload) {
                infoSpan.textContent = data.message || `Database: ${data.historical_count} total SRs | Last update: ${data.upload_date}`;
            } else {
                infoSpan.textContent = 'No data available. Contact admin to upload SR data.';
            }
        } catch (error) {
            console.error('[MyDashboard] Database info load failed:', error);
            const infoSpan = document.getElementById('database-info');
            infoSpan.innerHTML = `Cannot connect to backend (${this.API_BASE}). <button class="link-btn" onclick="MyDashboard.loadDatabaseInfo()">Retry</button>`;
        }
    },
    
    async searchSR() {
        const srId = document.getElementById('sr-search-input').value.trim();
        
        if (!srId) {
            this.showToast('Please enter an SR ID', 'error');
            return;
        }
        
        this.showLoader();
        
        try {
            const response = await fetch(`${this.API_BASE}/search-sr`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sr_id: srId })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentSR = data.sr;
                this.displaySRDetails(data.sr);
            } else {
                this.showToast(`❌ ${data.error}`, 'error');
                document.getElementById('sr-details-section').style.display = 'none';
            }
        } catch (error) {
            console.error('[MyDashboard] Search failed:', error);
            this.showToast('❌ Search failed - cannot connect to backend', 'error');
        } finally {
            this.hideLoader();
        }
    },
    
    displaySRDetails(sr) {
        const section = document.getElementById('sr-details-section');
        section.style.display = 'block';
        
        // Basic info
        document.getElementById('result-sr-id').textContent = sr.sr_id;
        
        const priorityEl = document.getElementById('result-priority');
        priorityEl.textContent = sr.priority || 'N/A';
        priorityEl.className = 'sr-priority ' + (sr.priority || 'p3').toLowerCase();
        
        document.getElementById('result-status').textContent = sr.status || 'N/A';
        document.getElementById('result-assignee').textContent = sr.assigned_to || sr.current_assignee || 'Not Assigned';
        document.getElementById('result-age').textContent = sr.age_info?.display || 'N/A';
        
        // Description
        document.getElementById('result-description').textContent = sr.description || 'N/A';
        
        // Workarounds
        const aiCard = document.getElementById('ai-workaround-card');
        const userCard = document.getElementById('user-workaround-card');
        const semanticCard = document.getElementById('semantic-workaround-card');
        const noWaMsg = document.getElementById('no-workaround-msg');
        
        let hasWorkaround = false;
        
        // AI Workaround
        if (sr.ai_workaround && sr.ai_workaround !== 'N/A') {
            aiCard.style.display = 'block';
            document.getElementById('ai-workaround-content').textContent = sr.ai_workaround;
            hasWorkaround = true;
        } else {
            aiCard.style.display = 'none';
        }
        
        // User Corrected Workaround
        if (sr.user_corrected_workaround || sr.corrected_workaround) {
            userCard.style.display = 'block';
            document.getElementById('user-workaround-content').textContent = sr.user_corrected_workaround || sr.corrected_workaround;
            hasWorkaround = true;
        } else {
            userCard.style.display = 'none';
        }
        
        // Semantic Workaround
        if (sr.summarized_semantic_workaround || sr.semantic_workaround) {
            semanticCard.style.display = 'block';
            document.getElementById('semantic-workaround-content').textContent = sr.summarized_semantic_workaround || sr.semantic_workaround;
            document.getElementById('similar-srs-count').textContent = `Based on ${sr.similar_sr_count || sr.similar_srs?.length || 0} similar SRs`;
            hasWorkaround = true;
        } else {
            semanticCard.style.display = 'none';
        }
        
        noWaMsg.style.display = hasWorkaround ? 'none' : 'block';
        
        // Similar SRs
        const similarSection = document.getElementById('similar-srs-section');
        const similarList = document.getElementById('similar-srs-list');
        
        if (sr.similar_srs && sr.similar_srs.length > 0) {
            similarSection.style.display = 'block';
            similarList.innerHTML = sr.similar_srs.slice(0, 5).map(s => `
                <div class="similar-sr-item">
                    <div class="similar-sr-header">
                        <span class="similar-sr-id">${s.sr_id}</span>
                        <span class="similarity-score">${s.similarity}% Match</span>
                    </div>
                    <p class="similar-sr-summary">${s.summary || 'No summary available'}</p>
                    ${s.workaround && s.workaround !== 'N/A' ? `<p class="similar-sr-workaround"><strong>Workaround:</strong> ${s.workaround.substring(0, 200)}...</p>` : ''}
                </div>
            `).join('');
        } else {
            similarSection.style.display = 'none';
        }
        
        // Resolution Info
        const resolutionSection = document.getElementById('resolution-section');
        if (sr.resolution_categorization || sr.sla_resolution_display) {
            resolutionSection.style.display = 'block';
            document.getElementById('result-resolution').textContent = sr.resolution_categorization || 'N/A';
            document.getElementById('result-sla-resolution').textContent = sr.sla_resolution_display || 'N/A';
        } else {
            resolutionSection.style.display = 'none';
        }
        
        // Scroll to results
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    },
    
    async submitWorkaround() {
        if (!this.currentSR) {
            this.showToast('Please search for an SR first', 'error');
            return;
        }
        
        const workaround = document.getElementById('user-workaround-input').value.trim();
        
        if (!workaround) {
            this.showToast('Please enter a workaround', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.API_BASE}/submit-feedback`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sr_id: this.currentSR.sr_id,
                    corrected_workaround: workaround,
                    description: this.currentSR.description
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast('✅ Workaround submitted successfully!', 'success');
                document.getElementById('user-workaround-input').value = '';
                // Refresh SR data
                this.searchSR();
            } else {
                this.showToast(`❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showToast('❌ Failed to submit workaround', 'error');
        }
    },
    
    voteWorkaround(type, vote) {
        this.showToast(`👍 Thanks for your feedback!`, 'success');
        // Future: Implement voting API
    },
    
    showLoader() {
        document.getElementById('dashboard-loader').style.display = 'flex';
    },
    
    hideLoader() {
        document.getElementById('dashboard-loader').style.display = 'none';
    },
    
    showToast(message, type = 'info') {
        const toast = document.getElementById('dashboard-toast');
        toast.textContent = message;
        toast.className = `toast-message ${type} show`;
        setTimeout(() => toast.classList.remove('show'), 4000);
    }
};

window.MyDashboard = MyDashboard;

// Initialize all modules
document.addEventListener('DOMContentLoaded', () => {
    SmartTeam.init();
    MyDashboard.init();
});

