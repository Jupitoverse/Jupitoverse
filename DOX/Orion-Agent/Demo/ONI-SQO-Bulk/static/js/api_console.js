// api_console.js - API Console Modules for SQO, ONI, and Bulk

// ===== JSON Viewer Utility =====
const JSONViewer = {
    currentData: null,
    searchMatches: [],
    currentMatchIndex: -1,

    render(data, containerId) {
        this.currentData = data;
        const container = document.getElementById(containerId);
        if (!container) return;

        const html = this.toHTML(data, 0);
        container.innerHTML = `<div class="json-content">${html}</div>`;
        this.attachCollapsibleListeners(container);
    },

    toHTML(data, indent = 0) {
        const indentStr = '  '.repeat(indent);
        
        if (data === null) return `<span class="json-null">null</span>`;
        if (typeof data === 'boolean') return `<span class="json-boolean">${data}</span>`;
        if (typeof data === 'number') return `<span class="json-number">${data}</span>`;
        
        if (typeof data === 'string') {
            const escaped = data.replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            return `<span class="json-string">"${escaped}"</span>`;
        }
        
        if (Array.isArray(data)) {
            if (data.length === 0) return `<span class="json-bracket">[]</span>`;
            
            let html = `<span class="json-collapsible json-bracket">[</span>`;
            html += `<div class="json-collapsible-content">`;
            data.forEach((item, index) => {
                html += `<div class="json-line">${indentStr}  ${this.toHTML(item, indent + 1)}`;
                if (index < data.length - 1) html += ',';
                html += `</div>`;
            });
            html += `</div><span class="json-bracket">${indentStr}]</span>`;
            return html;
        }
        
        if (typeof data === 'object') {
            const keys = Object.keys(data);
            if (keys.length === 0) return `<span class="json-bracket">{}</span>`;
            
            let html = `<span class="json-collapsible json-bracket">{</span>`;
            html += `<div class="json-collapsible-content">`;
            keys.forEach((key, index) => {
                html += `<div class="json-line">${indentStr}  <span class="json-key">"${key}"</span>: ${this.toHTML(data[key], indent + 1)}`;
                if (index < keys.length - 1) html += ',';
                html += `</div>`;
            });
            html += `</div><span class="json-bracket">${indentStr}}</span>`;
            return html;
        }
        
        return String(data);
    },

    attachCollapsibleListeners(container) {
        container.querySelectorAll('.json-collapsible').forEach(el => {
            el.addEventListener('click', (e) => {
                e.stopPropagation();
                el.classList.toggle('collapsed');
                const content = el.nextElementSibling;
                if (content && content.classList.contains('json-collapsible-content')) {
                    content.classList.toggle('json-collapsed');
                }
            });
        });
    },

    expandAll(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.querySelectorAll('.json-collapsible').forEach(el => el.classList.remove('collapsed'));
        container.querySelectorAll('.json-collapsible-content').forEach(el => el.classList.remove('json-collapsed'));
    },

    collapseAll(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.querySelectorAll('.json-collapsible').forEach(el => el.classList.add('collapsed'));
        container.querySelectorAll('.json-collapsible-content').forEach(el => el.classList.add('json-collapsed'));
    },

    search(containerId, searchTerm) {
        const container = document.getElementById(containerId);
        if (!container) return 0;

        container.innerHTML = container.innerHTML.replace(/<mark class="json-highlight">([^<]*)<\/mark>/g, '$1');

        this.searchMatches = [];
        this.currentMatchIndex = -1;

        if (!searchTerm || searchTerm.length < 2) return 0;

        const regex = new RegExp(`(${searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        container.innerHTML = container.innerHTML.replace(regex, '<mark class="json-highlight">$1</mark>');

        this.searchMatches = container.querySelectorAll('.json-highlight');
        return this.searchMatches.length;
    }
};

// ===== SQO API Module =====
const SQOAPI = {
    currentAPI: null,
    responseData: null,
    startTime: null,

    init() {
        this.checkStatus();
    },

    async checkStatus() {
        try {
            const response = await fetch(`${window.APP_CONFIG.API_BASE}/sqo/status`);
            const data = await response.json();
            const statusEl = document.getElementById('sqo-status');
            if (statusEl) {
                statusEl.innerHTML = data.connected 
                    ? '<span class="status-dot connected"></span> Connected'
                    : '<span class="status-dot error"></span> Disconnected';
            }
        } catch (e) {
            const statusEl = document.getElementById('sqo-status');
            if (statusEl) statusEl.innerHTML = '<span class="status-dot error"></span> Disconnected';
        }
    },

    selectAPI(apiName) {
        document.querySelectorAll('.api-card').forEach(c => c.classList.remove('active'));
        const activeCard = document.querySelector(`.api-card[data-api="${apiName}"]`);
        if (activeCard) activeCard.classList.add('active');

        document.querySelectorAll('.api-form').forEach(f => f.style.display = 'none');
        const form = document.getElementById(`form-${apiName}`);
        if (form) form.style.display = 'block';

        const formSection = document.getElementById('form-section');
        if (formSection) formSection.style.display = 'block';

        const titles = {
            'billing-manual': 'Billing Manual Call',
            'submit-delivery': 'Submit to Delivery',
            'set-product-status': 'Set Product Status',
            'send-fulfillment': 'Send to Fulfillment',
            'quote-alignment': 'Quote Alignment'
        };
        const titleEl = document.getElementById('form-title');
        if (titleEl) titleEl.textContent = titles[apiName] || apiName;
        
        this.currentAPI = apiName;
    },

    closeForm() {
        const formSection = document.getElementById('form-section');
        if (formSection) formSection.style.display = 'none';
        document.querySelectorAll('.api-card').forEach(c => c.classList.remove('active'));
        this.currentAPI = null;
    },

    async execute() {
        if (!this.currentAPI) {
            alert('Please select an API first');
            return;
        }

        this.startTime = Date.now();
        this.showLoading(true);

        try {
            let payload = {};
            let endpoint = '';

            switch (this.currentAPI) {
                case 'billing-manual':
                    endpoint = '/sqo/billing-manual';
                    payload = {
                        correlationId: document.getElementById('billing-correlationId')?.value || '',
                        resend: document.getElementById('billing-resend')?.value === 'true',
                        products: this.parseJSON(document.getElementById('billing-products')?.value)
                    };
                    break;

                case 'submit-delivery':
                    endpoint = '/sqo/submit-delivery';
                    payload = {
                        correlationId: document.getElementById('delivery-correlationId')?.value || '',
                        frameworkAgreementRef: {
                            id: document.getElementById('delivery-faId')?.value || '',
                            version: parseInt(document.getElementById('delivery-faVersion')?.value) || 1
                        },
                        productAgreementItems: this.parseJSON(document.getElementById('delivery-items')?.value)
                    };
                    break;

                case 'set-product-status':
                    endpoint = '/sqo/set-product-status';
                    payload = {
                        correlationId: document.getElementById('status-correlationId')?.value || '',
                        products: this.parseJSON(document.getElementById('status-products')?.value)
                    };
                    break;

                case 'send-fulfillment':
                    endpoint = '/sqo/send-fulfillment';
                    payload = {
                        correlationId: document.getElementById('fulfillment-correlationId')?.value || '',
                        fulfillmentGroupId: document.getElementById('fulfillment-groupId')?.value || '',
                        fulfillmentGroupAction: document.getElementById('fulfillment-action')?.value || 'CREATE',
                        fulfillmentGroupVersion: document.getElementById('fulfillment-version')?.value || '1',
                        products: this.parseJSON(document.getElementById('fulfillment-products')?.value)
                    };
                    break;

                case 'quote-alignment':
                    endpoint = '/sqo/quote-alignment';
                    payload = {
                        frameworkAgreementId: document.getElementById('quote-faId')?.value || '',
                        requestType: document.getElementById('quote-requestType')?.value || 'Quote'
                    };
                    break;
            }

            const response = await fetch(`${window.APP_CONFIG.API_BASE}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            this.responseData = data;
            this.displayResponse(data, response.ok && data.success !== false);

        } catch (error) {
            this.responseData = { error: error.message };
            this.displayResponse({ error: error.message }, false);
        } finally {
            this.showLoading(false);
        }
    },

    parseJSON(str) {
        if (!str || !str.trim()) return [];
        try {
            return JSON.parse(str);
        } catch (e) {
            alert('Invalid JSON format');
            return [];
        }
    },

    displayResponse(data, success) {
        const section = document.getElementById('response-section');
        const statusEl = document.getElementById('response-status');
        const timeEl = document.getElementById('response-time');

        if (section) section.style.display = 'block';

        if (statusEl) {
            statusEl.textContent = success ? 'Success' : 'Error';
            statusEl.className = `status-badge ${success ? 'success' : 'error'}`;
        }

        if (timeEl) {
            const elapsed = Date.now() - this.startTime;
            timeEl.textContent = `${elapsed}ms`;
        }

        JSONViewer.render(data, 'json-viewer');
        section.scrollIntoView({ behavior: 'smooth' });
    },

    showLoading(show) {
        let overlay = document.getElementById('loading-overlay');
        if (show) {
            if (!overlay) {
                overlay = document.createElement('div');
                overlay.id = 'loading-overlay';
                overlay.className = 'loading-overlay';
                overlay.innerHTML = '<div class="loading-spinner"></div>';
                document.body.appendChild(overlay);
            }
            overlay.style.display = 'flex';
        } else if (overlay) {
            overlay.style.display = 'none';
        }
    },

    expandAll() { JSONViewer.expandAll('json-viewer'); },
    collapseAll() { JSONViewer.collapseAll('json-viewer'); },

    copyResponse() {
        if (!this.responseData) return;
        navigator.clipboard.writeText(JSON.stringify(this.responseData, null, 2))
            .then(() => alert('Copied to clipboard!'));
    },

    downloadResponse() {
        if (!this.responseData) return;
        const blob = new Blob([JSON.stringify(this.responseData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sqo-response-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
};

// ===== ONI API Module =====
const ONIAPI = {
    currentAPI: null,
    responseData: null,
    startTime: null,

    init() {
        this.checkStatus();
    },

    async checkStatus() {
        try {
            const response = await fetch(`${window.APP_CONFIG.API_BASE}/oni/status`);
            const data = await response.json();
            const statusEl = document.getElementById('oni-status');
            if (statusEl) {
                statusEl.innerHTML = data.connected 
                    ? '<span class="status-dot connected"></span> Connected'
                    : '<span class="status-dot error"></span> Disconnected';
            }
        } catch (e) {
            const statusEl = document.getElementById('oni-status');
            if (statusEl) statusEl.innerHTML = '<span class="status-dot error"></span> Disconnected';
        }
    },

    selectAPI(apiName) {
        document.querySelectorAll('.api-card').forEach(c => c.classList.remove('active'));
        const activeCard = document.querySelector(`.api-card[data-api="${apiName}"]`);
        if (activeCard) activeCard.classList.add('active');

        document.querySelectorAll('.api-form').forEach(f => f.style.display = 'none');
        const form = document.getElementById(`form-${apiName}`);
        if (form) form.style.display = 'block';

        const formSection = document.getElementById('form-section');
        if (formSection) formSection.style.display = 'block';

        const titles = {
            'find-by-customer-id': 'Search by Customer ID',
            'find-by-external-service-id': 'Search by External Service ID',
            'find-by-product-id': 'Search by Product ID',
            'find-by-site-id': 'Search by Site ID',
            'custom-query': 'Custom Query'
        };
        const titleEl = document.getElementById('form-title');
        if (titleEl) titleEl.textContent = titles[apiName] || apiName;
        
        this.currentAPI = apiName;
    },

    closeForm() {
        const formSection = document.getElementById('form-section');
        if (formSection) formSection.style.display = 'none';
        document.querySelectorAll('.api-card').forEach(c => c.classList.remove('active'));
        this.currentAPI = null;
    },

    async execute() {
        if (!this.currentAPI) {
            alert('Please select a search method first');
            return;
        }

        this.startTime = Date.now();
        this.showLoading(true);

        try {
            let payload = {};
            let endpoint = '';

            switch (this.currentAPI) {
                case 'find-by-customer-id':
                    endpoint = '/oni/find-by-customer-id';
                    payload = { customerId: document.getElementById('oni-customerId')?.value };
                    break;

                case 'find-by-external-service-id':
                    endpoint = '/oni/find-by-external-service-id';
                    payload = {
                        externalServiceId: document.getElementById('oni-externalServiceId')?.value,
                        externalSystemId: document.getElementById('oni-externalSystemId')?.value || 'SOM'
                    };
                    break;

                case 'find-by-product-id':
                    endpoint = '/oni/find-by-product-id';
                    payload = { productId: document.getElementById('oni-productId')?.value };
                    break;

                case 'find-by-site-id':
                    endpoint = '/oni/find-by-site-id';
                    payload = { siteId: document.getElementById('oni-siteId')?.value };
                    break;

                case 'custom-query':
                    endpoint = '/oni/custom-query';
                    payload = { properties: this.parseJSON(document.getElementById('oni-customProperties')?.value) };
                    break;
            }

            const response = await fetch(`${window.APP_CONFIG.API_BASE}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            this.responseData = data;
            this.displayResponse(data, response.ok && data.success !== false);

        } catch (error) {
            this.responseData = { error: error.message };
            this.displayResponse({ error: error.message }, false);
        } finally {
            this.showLoading(false);
        }
    },

    parseJSON(str) {
        if (!str || !str.trim()) return [];
        try {
            return JSON.parse(str);
        } catch (e) {
            alert('Invalid JSON format');
            return [];
        }
    },

    displayResponse(data, success) {
        const section = document.getElementById('response-section');
        const statusEl = document.getElementById('response-status');
        const timeEl = document.getElementById('response-time');

        if (section) section.style.display = 'block';

        if (statusEl) {
            statusEl.textContent = success ? 'Success' : 'Error';
            statusEl.className = `status-badge ${success ? 'success' : 'error'}`;
        }

        if (timeEl) {
            const elapsed = Date.now() - this.startTime;
            timeEl.textContent = `${elapsed}ms`;
        }

        JSONViewer.render(data, 'json-viewer');
        section.scrollIntoView({ behavior: 'smooth' });
    },

    showLoading(show) {
        let overlay = document.getElementById('loading-overlay');
        if (show) {
            if (!overlay) {
                overlay = document.createElement('div');
                overlay.id = 'loading-overlay';
                overlay.className = 'loading-overlay';
                overlay.innerHTML = '<div class="loading-spinner"></div>';
                document.body.appendChild(overlay);
            }
            overlay.style.display = 'flex';
        } else if (overlay) {
            overlay.style.display = 'none';
        }
    },

    expandAll() { JSONViewer.expandAll('json-viewer'); },
    collapseAll() { JSONViewer.collapseAll('json-viewer'); },

    copyResponse() {
        if (!this.responseData) return;
        navigator.clipboard.writeText(JSON.stringify(this.responseData, null, 2))
            .then(() => alert('Copied to clipboard!'));
    },

    downloadResponse() {
        if (!this.responseData) return;
        const blob = new Blob([JSON.stringify(this.responseData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `oni-response-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
};

// ===== Bulk API Module =====
const BulkAPI = {
    tasks: [],
    selectedTask: null,
    currentTaskResult: null,

    init() {
        console.log('BulkAPI initializing...');
        this.checkStatus();
        this.loadTasks();
    },

    async checkStatus() {
        try {
            const response = await fetch(`${window.APP_CONFIG.API_BASE}/bulk/status`);
            const data = await response.json();
            const statusEl = document.getElementById('bulk-status');
            if (statusEl) {
                statusEl.innerHTML = data.connected 
                    ? '<span class="status-dot connected"></span> Connected'
                    : '<span class="status-dot error"></span> Disconnected';
            }
        } catch (e) {
            const statusEl = document.getElementById('bulk-status');
            if (statusEl) statusEl.innerHTML = '<span class="status-dot error"></span> Disconnected';
        }
    },

    async loadTasks() {
        const container = document.getElementById('task-list');
        if (container) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">⏳</div>
                    <p>Loading tasks...</p>
                </div>
            `;
        }

        try {
            const response = await fetch(`${window.APP_CONFIG.API_BASE}/bulk/tasks`);
            const data = await response.json();
            this.tasks = data.tasks || [];
            this.renderTasks();
            this.updateStats();
        } catch (e) {
            console.error('Failed to load tasks:', e);
            if (container) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">❌</div>
                        <p>Failed to connect to backend. Make sure the server is running.</p>
                        <button class="btn btn-primary" onclick="BulkAPI.loadTasks()" style="margin-top: 12px;">🔄 Retry</button>
                    </div>
                `;
            }
        }
    },

    updateStats() {
        const total = this.tasks.length;
        const pending = this.tasks.filter(t => t.status === 'pending').length;
        const completed = this.tasks.filter(t => t.status === 'completed').length;
        const failed = this.tasks.reduce((sum, t) => sum + (t.failed_items || 0), 0);

        const statTotal = document.getElementById('stat-total');
        const statPending = document.getElementById('stat-pending');
        const statCompleted = document.getElementById('stat-completed');
        const statFailed = document.getElementById('stat-failed');

        if (statTotal) statTotal.textContent = total;
        if (statPending) statPending.textContent = pending;
        if (statCompleted) statCompleted.textContent = completed;
        if (statFailed) statFailed.textContent = failed;
    },

    renderTasks() {
        const container = document.getElementById('task-list');
        if (!container) return;

        if (this.tasks.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📦</div>
                    <p>No bulk tasks yet. Click "Create Task" or use Quick Actions to get started!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.tasks.map(task => `
            <div class="task-item" data-id="${task.id}">
                <div class="task-info">
                    <h3>${task.name}</h3>
                    <div class="task-meta">
                        ${task.total_items} items • ${task.type} • 
                        Created: ${new Date(task.created_at).toLocaleString()}
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${task.progress}%"></div>
                    </div>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <span class="task-status ${task.status}">${task.status}</span>
                    ${task.status === 'pending' ? `<button class="btn btn-sm btn-primary" onclick="BulkAPI.executeTask(${task.id})">▶ Run</button>` : ''}
                    <button class="btn btn-sm btn-secondary" onclick="BulkAPI.viewTask(${task.id})">👁 View</button>
                    <button class="btn btn-sm btn-secondary" onclick="BulkAPI.exportTask(${task.id})">📤 Export</button>
                    <button class="btn btn-sm btn-danger" onclick="BulkAPI.deleteTask(${task.id})">✕</button>
                </div>
            </div>
        `).join('');
    },

    showCreateForm() {
        const formSection = document.getElementById('create-form-section');
        if (formSection) formSection.style.display = 'block';
        const titleEl = document.getElementById('bulk-form-title');
        if (titleEl) titleEl.textContent = 'Create Bulk Task';
    },

    hideCreateForm() {
        const formSection = document.getElementById('create-form-section');
        if (formSection) formSection.style.display = 'none';
    },

    showImportForm() {
        const formSection = document.getElementById('import-form-section');
        if (formSection) formSection.style.display = 'block';
    },

    hideImportForm() {
        const formSection = document.getElementById('import-form-section');
        if (formSection) formSection.style.display = 'none';
    },

    quickAction(action) {
        const templates = {
            'product-status': {
                name: 'Bulk Product Status Update',
                type: 'status-change',
                items: `[
  {"correlationId": "CORR-001", "products": [{"productId": "PROD-001", "status": "active"}]},
  {"correlationId": "CORR-002", "products": [{"productId": "PROD-002", "status": "active"}]}
]`
            },
            'billing': {
                name: 'Bulk Billing Request',
                type: 'billing',
                items: `[
  {"correlationId": "BILL-001", "resend": false, "products": [{"productId": "123"}]},
  {"correlationId": "BILL-002", "resend": false, "products": [{"productId": "456"}]}
]`
            },
            'fulfillment': {
                name: 'Bulk Fulfillment',
                type: 'fulfillment',
                items: `[
  {"correlationId": "FF-001", "fulfillmentGroupId": "FG-001", "action": "CREATE", "products": []},
  {"correlationId": "FF-002", "fulfillmentGroupId": "FG-002", "action": "CREATE", "products": []}
]`
            },
            'data-export': {
                action: 'export'
            },
            'clear-all': {
                action: 'clear'
            }
        };

        const template = templates[action];
        
        if (action === 'data-export') {
            this.exportAllTasks();
            return;
        }
        
        if (action === 'clear-all') {
            this.clearAllTasks();
            return;
        }

        if (template) {
            this.showCreateForm();
            const nameEl = document.getElementById('task-name');
            const typeEl = document.getElementById('task-type');
            const itemsEl = document.getElementById('task-items');
            
            if (nameEl) nameEl.value = template.name;
            if (typeEl) typeEl.value = template.type;
            if (itemsEl) itemsEl.value = template.items;
        }
    },

    importData() {
        const dataText = document.getElementById('import-data')?.value;
        const format = document.getElementById('import-format')?.value;

        if (!dataText) {
            alert('Please enter data to import');
            return;
        }

        let items = [];
        try {
            if (format === 'json') {
                items = JSON.parse(dataText);
            } else if (format === 'csv-ids') {
                const ids = dataText.split(',').map(id => id.trim()).filter(id => id);
                items = ids.map(id => ({ id, productId: id }));
            } else if (format === 'newline-ids') {
                const ids = dataText.split('\n').map(id => id.trim()).filter(id => id);
                items = ids.map(id => ({ id, productId: id }));
            }

            // Populate the create form with imported data
            this.hideImportForm();
            this.showCreateForm();
            
            const itemsEl = document.getElementById('task-items');
            if (itemsEl) itemsEl.value = JSON.stringify(items, null, 2);
            
            alert(`Imported ${items.length} items! Review and create the task.`);

        } catch (e) {
            alert('Invalid data format: ' + e.message);
        }
    },

    async createTask() {
        const name = document.getElementById('task-name')?.value;
        const type = document.getElementById('task-type')?.value;
        const itemsText = document.getElementById('task-items')?.value;
        const endpoint = document.getElementById('task-endpoint')?.value;

        if (!name || !itemsText) {
            alert('Please fill in Task Name and Items');
            return;
        }

        let items;
        try {
            items = JSON.parse(itemsText);
            if (!Array.isArray(items)) {
                alert('Items must be a JSON array');
                return;
            }
        } catch (e) {
            alert('Invalid JSON format for items: ' + e.message);
            return;
        }

        try {
            const response = await fetch(`${window.APP_CONFIG.API_BASE}/bulk/tasks`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, type, items, endpoint })
            });

            const data = await response.json();
            if (data.success) {
                alert(`Task "${name}" created with ${items.length} items!`);
                this.hideCreateForm();
                this.loadTasks();
                // Clear form
                document.getElementById('task-name').value = '';
                document.getElementById('task-items').value = '';
            } else {
                alert('Failed to create task: ' + (data.error || 'Unknown error'));
            }
        } catch (e) {
            alert('Error creating task: ' + e.message);
        }
    },

    async executeTask(taskId) {
        if (!confirm('Execute this task? This will process all items.')) return;

        try {
            const response = await fetch(`${window.APP_CONFIG.API_BASE}/bulk/tasks/${taskId}/execute`, {
                method: 'POST'
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                this.loadTasks();
                // Auto-view the results
                this.viewTask(taskId);
            } else {
                alert('Failed: ' + (data.error || 'Unknown error'));
            }
        } catch (e) {
            alert('Error: ' + e.message);
        }
    },

    async viewTask(taskId) {
        try {
            const response = await fetch(`${window.APP_CONFIG.API_BASE}/bulk/tasks/${taskId}`);
            const data = await response.json();
            
            if (data.success) {
                this.currentTaskResult = data.task;
                const resultSection = document.getElementById('task-result-section');
                const statusEl = document.getElementById('task-result-status');
                
                if (resultSection) {
                    resultSection.style.display = 'block';
                    
                    if (statusEl) {
                        statusEl.textContent = data.task.status;
                        statusEl.className = `status-badge ${data.task.status === 'completed' ? 'success' : data.task.status === 'pending' ? '' : 'error'}`;
                    }
                    
                    JSONViewer.render(data.task, 'task-result-viewer');
                    resultSection.scrollIntoView({ behavior: 'smooth' });
                }
            }
        } catch (e) {
            alert('Error: ' + e.message);
        }
    },

    async exportTask(taskId) {
        try {
            const response = await fetch(`${window.APP_CONFIG.API_BASE}/bulk/export/${taskId}`);
            const data = await response.json();
            
            if (data.success) {
                const blob = new Blob([JSON.stringify(data.export_data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `bulk-task-${taskId}-${Date.now()}.json`;
                a.click();
                URL.revokeObjectURL(url);
            }
        } catch (e) {
            alert('Error: ' + e.message);
        }
    },

    async exportAllTasks() {
        if (this.tasks.length === 0) {
            alert('No tasks to export');
            return;
        }

        const exportData = {
            exported_at: new Date().toISOString(),
            total_tasks: this.tasks.length,
            tasks: this.tasks
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `bulk-all-tasks-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    },

    async deleteTask(taskId) {
        if (!confirm('Delete this task?')) return;

        try {
            const response = await fetch(`${window.APP_CONFIG.API_BASE}/bulk/tasks/${taskId}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            if (data.success) {
                this.loadTasks();
            }
        } catch (e) {
            alert('Error: ' + e.message);
        }
    },

    async clearAllTasks() {
        if (!confirm('Clear ALL tasks? This cannot be undone.')) return;

        try {
            const response = await fetch(`${window.APP_CONFIG.API_BASE}/bulk/clear`, {
                method: 'POST'
            });
            const data = await response.json();
            if (data.success) {
                alert('All tasks cleared');
                this.loadTasks();
            }
        } catch (e) {
            alert('Error: ' + e.message);
        }
    },

    hideResults() {
        const resultSection = document.getElementById('task-result-section');
        if (resultSection) resultSection.style.display = 'none';
    },

    expandAll() { JSONViewer.expandAll('task-result-viewer'); },
    collapseAll() { JSONViewer.collapseAll('task-result-viewer'); },

    copyTaskResult() {
        if (!this.currentTaskResult) return;
        navigator.clipboard.writeText(JSON.stringify(this.currentTaskResult, null, 2))
            .then(() => alert('Copied to clipboard!'));
    },

    downloadTaskResult() {
        if (!this.currentTaskResult) return;
        const blob = new Blob([JSON.stringify(this.currentTaskResult, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `task-result-${this.currentTaskResult.id || Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
};

// Export for global access
window.SQOAPI = SQOAPI;
window.ONIAPI = ONIAPI;
window.BulkAPI = BulkAPI;
window.JSONViewer = JSONViewer;
