// static/js/api_console.js
// API Console Module - Handles SQO and ONI API interactions

const API_BASE = 'http://127.0.0.1:5001/api';

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

        // Clear previous highlights
        container.innerHTML = container.innerHTML.replace(/<mark class="json-highlight">([^<]*)<\/mark>/g, '$1');

        this.searchMatches = [];
        this.currentMatchIndex = -1;

        if (!searchTerm || searchTerm.length < 2) return 0;

        const regex = new RegExp(`(${searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        container.innerHTML = container.innerHTML.replace(regex, '<mark class="json-highlight">$1</mark>');

        this.searchMatches = container.querySelectorAll('.json-highlight');
        return this.searchMatches.length;
    },

    navigateSearch(containerId, direction) {
        if (this.searchMatches.length === 0) return '';

        if (this.currentMatchIndex >= 0 && this.searchMatches[this.currentMatchIndex]) {
            this.searchMatches[this.currentMatchIndex].style.background = 'rgba(251, 191, 36, 0.3)';
        }

        if (direction === 'next') {
            this.currentMatchIndex = (this.currentMatchIndex + 1) % this.searchMatches.length;
        } else {
            this.currentMatchIndex = this.currentMatchIndex <= 0 ? this.searchMatches.length - 1 : this.currentMatchIndex - 1;
        }

        const current = this.searchMatches[this.currentMatchIndex];
        if (current) {
            current.style.background = 'rgba(139, 92, 246, 0.5)';
            current.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        return `${this.currentMatchIndex + 1}/${this.searchMatches.length}`;
    }
};

// ===== SQO API Module =====
const SQOAPI = {
    currentAPI: null,
    responseData: null,
    startTime: null,

    selectAPI(apiName) {
        // Update card selection
        document.querySelectorAll('.sqo-api-card').forEach(c => c.classList.remove('active'));
        const activeCard = document.querySelector(`.sqo-api-card[data-api="${apiName}"]`);
        if (activeCard) activeCard.classList.add('active');

        // Hide all forms
        document.querySelectorAll('.sqo-form').forEach(f => f.style.display = 'none');
        
        // Show selected form
        const form = document.getElementById(`form-${apiName}`);
        if (form) form.style.display = 'block';

        // Show form container
        const formSection = document.getElementById('sqo-form-section');
        if (formSection) formSection.style.display = 'block';

        // Update title
        const titles = {
            'billing-manual': 'Billing Manual Call',
            'submit-delivery': 'Submit to Delivery',
            'set-product-status': 'Set Product Status',
            'send-fulfillment': 'Send to Fulfillment',
            'quote-alignment': 'Quote Alignment'
        };
        const titleEl = document.getElementById('sqo-form-title');
        if (titleEl) titleEl.textContent = titles[apiName] || apiName;
        
        this.currentAPI = apiName;
    },

    closeForm() {
        const formSection = document.getElementById('sqo-form-section');
        if (formSection) formSection.style.display = 'none';
        document.querySelectorAll('.sqo-api-card').forEach(c => c.classList.remove('active'));
        this.currentAPI = null;
    },

    clearForm() {
        if (!this.currentAPI) return;
        const form = document.getElementById(`form-${this.currentAPI}`);
        if (form) {
            form.querySelectorAll('input:not([type="number"]), textarea').forEach(el => el.value = '');
            form.querySelectorAll('select').forEach(el => el.selectedIndex = 0);
        }
    },

    async executeRequest() {
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

            console.log('SQO Request:', endpoint, payload);

            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            this.responseData = data;
            this.displayResponse(data, response.ok);

        } catch (error) {
            console.error('SQO Error:', error);
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
        const section = document.getElementById('sqo-response-section');
        const statusEl = document.getElementById('sqo-response-status');
        const timeEl = document.getElementById('sqo-response-time');

        if (section) section.style.display = 'block';

        if (statusEl) {
            statusEl.textContent = success ? 'Success' : 'Error';
            statusEl.className = `sqo-status-badge ${success ? 'success' : 'error'}`;
        }

        if (timeEl) {
            const elapsed = Date.now() - this.startTime;
            timeEl.textContent = `${elapsed}ms`;
        }

        JSONViewer.render(data, 'sqo-json-viewer');
        
        // Scroll to response
        section.scrollIntoView({ behavior: 'smooth' });
    },

    showLoading(show) {
        let overlay = document.getElementById('sqo-loading-overlay');
        if (show) {
            if (!overlay) {
                overlay = document.createElement('div');
                overlay.id = 'sqo-loading-overlay';
                overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(10,10,18,0.8);display:flex;align-items:center;justify-content:center;z-index:9999';
                overlay.innerHTML = '<div style="width:50px;height:50px;border:3px solid #2c2a3a;border-top-color:#8B5CF6;border-radius:50%;animation:spin 0.8s linear infinite"></div>';
                document.body.appendChild(overlay);
            }
            overlay.style.display = 'flex';
        } else if (overlay) {
            overlay.style.display = 'none';
        }
    },

    searchInResponse() {
        const searchBar = document.getElementById('sqo-search-bar');
        if (!searchBar) return;
        const isVisible = searchBar.style.display !== 'none';
        searchBar.style.display = isVisible ? 'none' : 'flex';
        if (!isVisible) {
            const input = document.getElementById('sqo-search-input');
            if (input) {
                input.focus();
                input.oninput = (e) => {
                    const count = JSONViewer.search('sqo-json-viewer', e.target.value);
                    document.getElementById('sqo-search-count').textContent = `${count} matches`;
                };
            }
        }
    },

    closeSearch() {
        document.getElementById('sqo-search-bar').style.display = 'none';
        document.getElementById('sqo-search-input').value = '';
        JSONViewer.search('sqo-json-viewer', '');
    },

    findNext() {
        const result = JSONViewer.navigateSearch('sqo-json-viewer', 'next');
        if (result) document.getElementById('sqo-search-count').textContent = result;
    },

    findPrev() {
        const result = JSONViewer.navigateSearch('sqo-json-viewer', 'prev');
        if (result) document.getElementById('sqo-search-count').textContent = result;
    },

    expandAll() { JSONViewer.expandAll('sqo-json-viewer'); },
    collapseAll() { JSONViewer.collapseAll('sqo-json-viewer'); },

    copyResponse() {
        if (!this.responseData) return;
        navigator.clipboard.writeText(JSON.stringify(this.responseData, null, 2))
            .then(() => alert('Copied to clipboard!'))
            .catch(() => alert('Failed to copy'));
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

    selectAPI(apiName) {
        // Update card selection
        document.querySelectorAll('.oni-api-card').forEach(c => c.classList.remove('active'));
        const activeCard = document.querySelector(`.oni-api-card[data-api="${apiName}"]`);
        if (activeCard) activeCard.classList.add('active');

        // Hide all forms
        document.querySelectorAll('.oni-form').forEach(f => f.style.display = 'none');
        
        // Show selected form
        const form = document.getElementById(`form-${apiName}`);
        if (form) form.style.display = 'block';

        // Show form container
        const formSection = document.getElementById('oni-form-section');
        if (formSection) formSection.style.display = 'block';

        // Update title
        const titles = {
            'find-by-customer-id': 'Search by Customer ID',
            'find-by-external-service-id': 'Search by External Service ID',
            'find-by-product-id': 'Search by Product ID',
            'find-by-site-id': 'Search by Site ID',
            'custom-query': 'Custom Query'
        };
        const titleEl = document.getElementById('oni-form-title');
        if (titleEl) titleEl.textContent = titles[apiName] || apiName;
        
        this.currentAPI = apiName;
    },

    closeForm() {
        const formSection = document.getElementById('oni-form-section');
        if (formSection) formSection.style.display = 'none';
        document.querySelectorAll('.oni-api-card').forEach(c => c.classList.remove('active'));
        this.currentAPI = null;
    },

    clearForm() {
        if (!this.currentAPI) return;
        const form = document.getElementById(`form-${this.currentAPI}`);
        if (form) {
            form.querySelectorAll('input, textarea').forEach(el => el.value = '');
            form.querySelectorAll('select').forEach(el => el.selectedIndex = 0);
        }
    },

    async executeRequest() {
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
                    const customerId = document.getElementById('oni-customerId')?.value;
                    if (!customerId) {
                        alert('Please enter Customer ID');
                        this.showLoading(false);
                        return;
                    }
                    payload = { customerId };
                    break;

                case 'find-by-external-service-id':
                    endpoint = '/oni/find-by-external-service-id';
                    const externalServiceId = document.getElementById('oni-externalServiceId')?.value;
                    if (!externalServiceId) {
                        alert('Please enter External Service ID');
                        this.showLoading(false);
                        return;
                    }
                    payload = {
                        externalServiceId,
                        externalSystemId: document.getElementById('oni-externalSystemId')?.value || 'SOM'
                    };
                    break;

                case 'find-by-product-id':
                    endpoint = '/oni/find-by-product-id';
                    const productId = document.getElementById('oni-productId')?.value;
                    if (!productId) {
                        alert('Please enter Product ID');
                        this.showLoading(false);
                        return;
                    }
                    payload = { productId };
                    break;

                case 'find-by-site-id':
                    endpoint = '/oni/find-by-site-id';
                    const siteId = document.getElementById('oni-siteId')?.value;
                    if (!siteId) {
                        alert('Please enter Site ID');
                        this.showLoading(false);
                        return;
                    }
                    payload = { siteId };
                    break;

                case 'custom-query':
                    endpoint = '/oni/custom-query';
                    const properties = this.parseJSON(document.getElementById('oni-customProperties')?.value);
                    if (!properties || properties.length === 0) {
                        alert('Please enter valid query properties');
                        this.showLoading(false);
                        return;
                    }
                    payload = { properties };
                    break;
            }

            console.log('ONI Request:', endpoint, payload);

            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            this.responseData = data;
            this.displayResponse(data, response.ok && data.success !== false);

        } catch (error) {
            console.error('ONI Error:', error);
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
        const section = document.getElementById('oni-response-section');
        const statusEl = document.getElementById('oni-response-status');
        const timeEl = document.getElementById('oni-response-time');
        const countEl = document.getElementById('oni-response-count');

        if (section) section.style.display = 'block';

        if (statusEl) {
            statusEl.textContent = success ? 'Success' : 'Error';
            statusEl.className = `oni-status-badge ${success ? 'success' : 'error'}`;
        }

        if (timeEl) {
            const elapsed = Date.now() - this.startTime;
            timeEl.textContent = `${elapsed}ms`;
        }

        // Count results
        if (countEl) {
            if (data.data && Array.isArray(data.data)) {
                countEl.textContent = `${data.data.length} results`;
            } else {
                countEl.textContent = '';
            }
        }

        JSONViewer.render(data, 'oni-json-viewer');
        
        // Scroll to response
        section.scrollIntoView({ behavior: 'smooth' });
    },

    showLoading(show) {
        let overlay = document.getElementById('oni-loading-overlay');
        if (show) {
            if (!overlay) {
                overlay = document.createElement('div');
                overlay.id = 'oni-loading-overlay';
                overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(10,10,18,0.8);display:flex;align-items:center;justify-content:center;z-index:9999';
                overlay.innerHTML = '<div style="width:50px;height:50px;border:3px solid #2c2a3a;border-top-color:#8B5CF6;border-radius:50%;animation:spin 0.8s linear infinite"></div>';
                document.body.appendChild(overlay);
            }
            overlay.style.display = 'flex';
        } else if (overlay) {
            overlay.style.display = 'none';
        }
    },

    searchInResponse() {
        const searchBar = document.getElementById('oni-search-bar');
        if (!searchBar) return;
        const isVisible = searchBar.style.display !== 'none';
        searchBar.style.display = isVisible ? 'none' : 'flex';
        if (!isVisible) {
            const input = document.getElementById('oni-search-input');
            if (input) {
                input.focus();
                input.oninput = (e) => {
                    const count = JSONViewer.search('oni-json-viewer', e.target.value);
                    document.getElementById('oni-search-count').textContent = `${count} matches`;
                };
            }
        }
    },

    closeSearch() {
        document.getElementById('oni-search-bar').style.display = 'none';
        document.getElementById('oni-search-input').value = '';
        JSONViewer.search('oni-json-viewer', '');
    },

    findNext() {
        const result = JSONViewer.navigateSearch('oni-json-viewer', 'next');
        if (result) document.getElementById('oni-search-count').textContent = result;
    },

    findPrev() {
        const result = JSONViewer.navigateSearch('oni-json-viewer', 'prev');
        if (result) document.getElementById('oni-search-count').textContent = result;
    },

    expandAll() { JSONViewer.expandAll('oni-json-viewer'); },
    collapseAll() { JSONViewer.collapseAll('oni-json-viewer'); },

    copyResponse() {
        if (!this.responseData) return;
        navigator.clipboard.writeText(JSON.stringify(this.responseData, null, 2))
            .then(() => alert('Copied to clipboard!'))
            .catch(() => alert('Failed to copy'));
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

// Add animation keyframe
const style = document.createElement('style');
style.textContent = '@keyframes spin { to { transform: rotate(360deg); } }';
document.head.appendChild(style);

// Export for global access
window.SQOAPI = SQOAPI;
window.ONIAPI = ONIAPI;
window.JSONViewer = JSONViewer;
