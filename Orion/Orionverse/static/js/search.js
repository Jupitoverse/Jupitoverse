// static/js/search.js
const SearchAnything = {
    // Data storage
    allData: {
        sr: [],
        defect: [],
        wa: []
    },
    currentData: {
        sr: [],
        defect: [],
        wa: []
    },
    
    // UI state
    quill: null,
    editingId: null,
    currentTab: 'wa',
    
    // DataTables instances
    srTable: null,
    defectTable: null,

    /**
     * Initialize the Search Anything module
     */
    init() {
        document.addEventListener('pageLoaded', (e) => {
            if (e.detail.pageId === 'search-anything') {
                console.log('🚀 Search Anything page loaded');
                this.setupPage();
            }
        });
    },

    /**
     * Setup the page - initialize components and load data
     */
    async setupPage() {
        console.log('⚙️ Setting up Search Anything page...');
        this.initDataTables();
        this.attachEventListeners();
        await this.fetchAllData();
    },

    /**
     * Initialize DataTables for SR and Defect sheets
     */
    initDataTables() {
        // Destroy existing tables if they exist
        if ($.fn.DataTable.isDataTable('#sr-results-table')) {
            $('#sr-results-table').DataTable().destroy();
        }
        if ($.fn.DataTable.isDataTable('#defect-results-table')) {
            $('#defect-results-table').DataTable().destroy();
        }

        // Initialize SR Table
        this.srTable = $('#sr-results-table').DataTable({
            data: [],
            columns: [
                { 
                    data: 'SR_ID', 
                    title: 'SR ID',
                    width: '120px',
                    render: function(data) {
                        return `<span class="table-highlight">${data}</span>`;
                    }
                },
                { 
                    data: 'CUSTOMER_ID', 
                    title: 'Customer ID',
                    width: '120px'
                },
                { 
                    data: 'CUSTOMER_NAME', 
                    title: 'Customer Name',
                    width: '150px'
                },
                { 
                    data: 'LBGUPS_Subcategory', 
                    title: 'Category',
                    width: '150px'
                },
                { 
                    data: 'DETAILS', 
                    title: 'Details',
                    render: function(data) {
                        if (!data) return '';
                        const truncated = data.length > 200 ? data.substring(0, 200) + '...' : data;
                        return `<div class="table-cell-content" title="${data}">${truncated}</div>`;
                    }
                },
                { 
                    data: 'RCA', 
                    title: 'RCA',
                    width: '150px',
                    render: function(data) {
                        if (!data) return '';
                        const truncated = data.length > 100 ? data.substring(0, 100) + '...' : data;
                        return `<div class="table-cell-content" title="${data}">${truncated}</div>`;
                    }
                },
                { 
                    data: 'Create_Date', 
                    title: 'Created',
                    width: '100px'
                },
                {
                    data: null,
                    title: 'Actions',
                    width: '100px',
                    orderable: false,
                    render: function(data, type, row) {
                        return `
                            <button class="table-action-btn view-details-btn" title="View Full Details">
                                👁️
                            </button>
                        `;
                    }
                }
            ],
            pageLength: 25,
            lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
            order: [[6, 'desc']], // Sort by Create_Date descending
            responsive: true,
            dom: 'lfrtip',
            language: {
                search: "Search in results:",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ SR records",
                emptyTable: "No Service Requests found"
            }
        });

        // Initialize Defect Table
        this.defectTable = $('#defect-results-table').DataTable({
            data: [],
            columns: [
                { 
                    data: 'ID', 
                    title: 'Defect ID',
                    width: '100px',
                    render: function(data) {
                        return `<span class="table-highlight">${data}</span>`;
                    }
                },
                { 
                    data: 'Name', 
                    title: 'Name',
                    render: function(data) {
                        if (!data) return '';
                        const truncated = data.length > 150 ? data.substring(0, 150) + '...' : data;
                        return `<div class="table-cell-content" title="${data}">${truncated}</div>`;
                    }
                },
                { 
                    data: 'Description', 
                    title: 'Description',
                    render: function(data) {
                        if (!data) return '';
                        const truncated = data.length > 300 ? data.substring(0, 300) + '...' : data;
                        return `<div class="table-cell-content" title="${data}">${truncated}</div>`;
                    }
                },
                { 
                    data: 'Phase', 
                    title: 'Phase',
                    width: '100px'
                },
                { 
                    data: 'Release', 
                    title: 'Release',
                    width: '100px'
                },
                {
                    data: null,
                    title: 'Actions',
                    width: '100px',
                    orderable: false,
                    render: function(data, type, row) {
                        return `
                            <button class="table-action-btn view-defect-btn" title="View Full Details">
                                👁️
                            </button>
                        `;
                    }
                }
            ],
            pageLength: 25,
            lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
            order: [[0, 'desc']], // Sort by ID descending
            responsive: true,
            dom: 'lfrtip',
            language: {
                search: "Search in results:",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ defect records",
                emptyTable: "No Defects found"
            }
        });

        console.log('✅ DataTables initialized');
    },

    /**
     * Fetch all data from backend
     */
    async fetchAllData() {
        $('#search-loader').show();
        
        try {
            console.log('📡 Fetching data from backend...');
            const data = await API.getAllSearchData();
            
            // Store all data
            this.allData.sr = data.sr_data || [];
            this.allData.defect = data.defect_data || [];
            this.allData.wa = data.wa_data || [];
            
            // Set current data to all data initially
            this.currentData.sr = this.allData.sr;
            this.currentData.defect = this.allData.defect;
            this.currentData.wa = this.allData.wa;
            
            console.log(`✅ Data loaded: ${this.allData.sr.length} SRs, ${this.allData.defect.length} Defects, ${this.allData.wa.length} WAs`);
            
            // Update stats
            this.updateStats();
            
            // Render all results
            this.renderAllResults();
            
            // Show navigation tabs
            document.getElementById('sa-nav-tabs').style.display = 'flex';
            
        } catch (error) {
            console.error('❌ Error fetching data:', error);
            this.showError('Failed to load data. Please ensure backend is running.');
        } finally {
            $('#search-loader').hide();
        }
    },

    /**
     * Update statistics display
     */
    updateStats() {
        document.getElementById('sr-count').textContent = this.allData.sr.length.toLocaleString();
        document.getElementById('defect-count').textContent = this.allData.defect.length.toLocaleString();
        document.getElementById('wa-count').textContent = this.allData.wa.length;
    },

    /**
     * Render all results
     */
    renderAllResults() {
        // Update result counts
        this.updateResultCounts();
        
        // Render each section
        this.renderWorkarounds(this.currentData.wa);
        this.renderSRData(this.currentData.sr);
        this.renderDefectData(this.currentData.defect);
        
        // Show the active tab
        this.switchTab(this.currentTab);
    },

    /**
     * Update result count badges
     */
    updateResultCounts() {
        const srCount = this.currentData.sr.length;
        const defectCount = this.currentData.defect.length;
        const waCount = this.currentData.wa.length;
        
        document.getElementById('sr-result-count').textContent = srCount;
        document.getElementById('defect-result-count').textContent = defectCount;
        document.getElementById('wa-result-count').textContent = waCount;
        
        document.getElementById('sr-badge').textContent = `${srCount} results`;
        document.getElementById('defect-badge').textContent = `${defectCount} results`;
        document.getElementById('wa-badge').textContent = `${waCount} results`;
    },

    /**
     * Render Workarounds as cards
     */
    renderWorkarounds(workarounds) {
        const container = document.getElementById('sa-blog-posts-container');
        if (!container) return;

        if (!workarounds || workarounds.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <span class="empty-icon">💡</span>
                    <h3>No Workarounds Found</h3>
                    <p>No workarounds match your search criteria.</p>
                    <button id="add-wa-empty" class="primary-btn">Add First Workaround</button>
                </div>
            `;
            return;
        }

        container.innerHTML = workarounds.map(wa => {
            const postDate = wa.created_date 
                ? new Date(wa.created_date).toLocaleString('en-IN', { 
                    timeZone: 'Asia/Kolkata', 
                    dateStyle: 'medium', 
                    timeStyle: 'short' 
                  })
                : 'Unknown date';
            
            // Truncate description for card view
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = wa.description;
            const textContent = tempDiv.textContent || tempDiv.innerText || '';
            const truncatedDesc = textContent.length > 200 
                ? textContent.substring(0, 200) + '...' 
                : textContent;

            return `
                <article class="wa-card" data-id="${wa.id}">
                    <div class="wa-card-header">
                        <span class="wa-card-category">${wa.category || 'General'}</span>
                        <h3 class="wa-card-issue">${wa.issue || 'No Issue Title'}</h3>
                    </div>
                    <p class="wa-card-meta">
                        👤 ${wa.created_by || 'Anonymous'} | 📅 ${postDate}
                    </p>
                    <div class="wa-card-description">
                        <div class="wa-description-preview">${truncatedDesc}</div>
                    </div>
                    <div class="wa-card-footer">
                        <div class="wa-card-actions">
                            <button class="wa-read-more-btn secondary-btn" title="View Full Details">
                                📖 Read More
                            </button>
                            <button class="wa-like-btn secondary-btn" title="Like this workaround">
                                👍 ${wa.likes || 0}
                            </button>
                            <button class="wa-edit-btn secondary-btn" title="Edit">
                                ✏️ Edit
                            </button>
                            <button class="wa-delete-btn danger-btn" title="Delete">
                                🗑️ Delete
                            </button>
                            <button class="wa-download-btn secondary-btn" title="Download as PDF">
                                📥 PDF
                            </button>
                        </div>
                        <div class="wa-card-stats">
                            <span class="wa-stat">👁️ ${wa.views || 0} views</span>
                        </div>
                    </div>
                </article>
            `;
        }).join('');

        // Attach event listeners to cards
        this.attachWorkaroundEventListeners();
    },

    /**
     * Render SR data in DataTable
     */
    renderSRData(srData) {
        this.srTable.clear();
        this.srTable.rows.add(srData);
        this.srTable.draw();
        console.log(`✅ Rendered ${srData.length} SR records`);
    },

    /**
     * Render Defect data in DataTable
     */
    renderDefectData(defectData) {
        this.defectTable.clear();
        this.defectTable.rows.add(defectData);
        this.defectTable.draw();
        console.log(`✅ Rendered ${defectData.length} Defect records`);
    },

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Search button
        const filterBtn = document.getElementById('filter-btn');
        if (filterBtn) {
            filterBtn.addEventListener('click', () => this.handleSearch());
        }

        // Clear filters button
        const clearBtn = document.getElementById('clear-filters-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearFilters());
        }

        // Enter key on search inputs
        ['search-anything-input', 'customer-id-input', 'osite-id-input', 'sr-id-input', 'id-input'].forEach(id => {
            const input = document.getElementById(id);
            if (input) {
                input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.handleSearch();
                    }
                });
            }
        });

        // Tab navigation
        document.querySelectorAll('.sa-tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.tab;
                this.switchTab(tab);
            });
        });

        // Add workaround button
        const addBtn = document.getElementById('add-workaround-btn');
        if (addBtn) {
            addBtn.addEventListener('click', () => this.showWorkaroundModal());
        }

        // Export buttons
        const exportResultsBtn = document.getElementById('export-results-btn');
        if (exportResultsBtn) {
            exportResultsBtn.addEventListener('click', () => this.exportAllResults());
        }

        const downloadSRBtn = document.getElementById('download-sr-btn');
        if (downloadSRBtn) {
            downloadSRBtn.addEventListener('click', () => this.exportToExcel(this.currentData.sr, 'SR_Data'));
        }

        const downloadDefectBtn = document.getElementById('download-defect-btn');
        if (downloadDefectBtn) {
            downloadDefectBtn.addEventListener('click', () => this.exportToExcel(this.currentData.defect, 'Defect_Data'));
        }

        const downloadWAAllBtn = document.getElementById('download-wa-all-btn');
        if (downloadWAAllBtn) {
            downloadWAAllBtn.addEventListener('click', () => this.downloadAllWorkarounds());
        }

        console.log('✅ Event listeners attached');
    },

    /**
     * Attach workaround-specific event listeners
     */
    attachWorkaroundEventListeners() {
        document.querySelectorAll('.wa-card').forEach(card => {
            const id = parseInt(card.dataset.id);
            
            card.querySelector('.wa-read-more-btn')?.addEventListener('click', () => this.viewWorkaround(id));
            card.querySelector('.wa-like-btn')?.addEventListener('click', () => this.likeWorkaround(id));
            card.querySelector('.wa-edit-btn')?.addEventListener('click', () => this.editWorkaround(id));
            card.querySelector('.wa-delete-btn')?.addEventListener('click', () => this.deleteWorkaround(id));
            card.querySelector('.wa-download-btn')?.addEventListener('click', () => this.downloadWorkaround(id));
        });

        // Empty state button
        document.getElementById('add-wa-empty')?.addEventListener('click', () => this.showWorkaroundModal());
    },

    /**
     * Handle search with filters
     */
    async handleSearch() {
        $('#search-loader').show();

        try {
            // Get filter values
            const filters = {
                search_anything: document.getElementById('search-anything-input').value.trim(),
                customer_id: document.getElementById('customer-id-input').value.trim(),
                osite_id: document.getElementById('osite-id-input').value.trim(),
                sr_id: document.getElementById('sr-id-input').value.trim(),
                id: document.getElementById('id-input').value.trim()
            };

            console.log('🔍 Searching with filters:', filters);

            // Call backend API
            const data = await API.filterAllData(filters);

            // Update current data
            this.currentData.sr = data.sr_data || [];
            this.currentData.defect = data.defect_data || [];
            this.currentData.wa = data.wa_data || [];

            console.log(`✅ Search complete: ${this.currentData.sr.length} SRs, ${this.currentData.defect.length} Defects, ${this.currentData.wa.length} WAs`);

            // Render results
            this.renderAllResults();

        } catch (error) {
            console.error('❌ Search error:', error);
            this.showError('Search failed. Please try again.');
        } finally {
            $('#search-loader').hide();
        }
    },

    /**
     * Clear all filters and show all data
     */
    clearFilters() {
        document.getElementById('search-anything-input').value = '';
        document.getElementById('customer-id-input').value = '';
        document.getElementById('osite-id-input').value = '';
        document.getElementById('sr-id-input').value = '';
        document.getElementById('id-input').value = '';

        // Reset to all data
        this.currentData.sr = this.allData.sr;
        this.currentData.defect = this.allData.defect;
        this.currentData.wa = this.allData.wa;

        // Re-render
        this.renderAllResults();

        console.log('🔄 Filters cleared');
    },

    /**
     * Switch between tabs
     */
    switchTab(tab) {
        this.currentTab = tab;

        // Update tab buttons
        document.querySelectorAll('.sa-tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.tab === tab) {
                btn.classList.add('active');
            }
        });

        // Show/hide sections
        document.getElementById('wa-results-section').style.display = tab === 'wa' ? 'block' : 'none';
        document.getElementById('sr-results-section').style.display = tab === 'sr' ? 'block' : 'none';
        document.getElementById('defect-results-section').style.display = tab === 'defect' ? 'block' : 'none';

        // Redraw tables if switched to them (for responsive sizing)
        if (tab === 'sr') {
            this.srTable.columns.adjust().draw();
        } else if (tab === 'defect') {
            this.defectTable.columns.adjust().draw();
        }

        console.log(`📑 Switched to ${tab} tab`);
    },

    /**
     * Show workaround modal for create/edit
     */
    showWorkaroundModal(workaround = null) {
        const container = document.getElementById('workaround-modal-container');
        const isEdit = workaround !== null;
        
        this.editingId = isEdit ? workaround.id : null;

        container.innerHTML = `
            <div class="modal-overlay visible" id="workaround-modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>${isEdit ? '✏️ Edit Workaround' : '➕ New Workaround'}</h2>
                        <button class="modal-close-btn" id="close-wa-modal">&times;</button>
                    </div>
                    <form id="workaround-form">
                        <div class="form-group">
                            <label for="wa-category">Category *</label>
                            <input type="text" id="wa-category" required 
                                   placeholder="e.g., Billing, OSS, CRM, Provisioning"
                                   value="${isEdit ? workaround.category : ''}">
                        </div>
                        <div class="form-group">
                            <label for="wa-issue">Issue Title *</label>
                            <input type="text" id="wa-issue" required 
                                   placeholder="e.g., Order stuck in fallout"
                                   value="${isEdit ? workaround.issue : ''}">
                        </div>
                        <div class="form-group">
                            <label for="editor-container">Solution Description *</label>
                            <div id="editor-container"></div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="secondary-btn" id="cancel-wa-btn">Cancel</button>
                            <button type="submit" class="primary-btn">${isEdit ? 'Update' : 'Create'} Workaround</button>
                        </div>
                    </form>
                </div>
            </div>
        `;

        // Initialize Quill editor
        this.quill = new Quill('#editor-container', {
            theme: 'snow',
            placeholder: 'Describe the solution in detail. You can add images, code blocks, and formatting...',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'color': [] }, { 'background': [] }],
                    ['link', 'image'],
                    ['clean']
                ]
            }
        });

        // Set existing content if editing
        if (isEdit) {
            this.quill.root.innerHTML = workaround.description;
        }

        // Attach modal event listeners
        document.getElementById('close-wa-modal').addEventListener('click', () => this.hideWorkaroundModal());
        document.getElementById('cancel-wa-btn').addEventListener('click', () => this.hideWorkaroundModal());
        document.getElementById('workaround-form').addEventListener('submit', (e) => this.submitWorkaround(e));
        document.getElementById('workaround-modal').addEventListener('click', (e) => {
            if (e.target.id === 'workaround-modal') {
                this.hideWorkaroundModal();
            }
        });
    },

    /**
     * Hide workaround modal
     */
    hideWorkaroundModal() {
        const modal = document.getElementById('workaround-modal');
        if (modal) {
            modal.classList.remove('visible');
            setTimeout(() => {
                document.getElementById('workaround-modal-container').innerHTML = '';
            }, 300);
        }
        this.editingId = null;
        this.quill = null;
    },

    /**
     * Submit workaround (create or update)
     */
    async submitWorkaround(e) {
        e.preventDefault();

        const workaroundData = {
            category: document.getElementById('wa-category').value,
            issue: document.getElementById('wa-issue').value,
            description: this.quill.root.innerHTML
        };

        try {
            if (this.editingId) {
                // Update existing
                await API.updateWorkaround(this.editingId, workaroundData);
                console.log('✅ Workaround updated');
            } else {
                // Create new
                workaroundData.created_by = Auth.currentUser ? Auth.currentUser.fullname : 'Anonymous';
                await API.addWorkaround(workaroundData);
                console.log('✅ Workaround created');
            }

            this.hideWorkaroundModal();
            await this.fetchAllData(); // Refresh data

        } catch (error) {
            console.error('❌ Failed to save workaround:', error);
            alert('Failed to save workaround. Please try again.');
        }
    },

    /**
     * View full workaround details
     */
    viewWorkaround(id) {
        const wa = this.currentData.wa.find(w => w.id === id);
        if (!wa) return;

        // Increment view count
        API.incrementView(id).catch(err => console.error('Failed to increment view:', err));

        // Show in modal
        const container = document.getElementById('workaround-modal-container');
        const postDate = wa.created_date 
            ? new Date(wa.created_date).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })
            : 'Unknown date';

        container.innerHTML = `
            <div class="modal-overlay visible" id="view-wa-modal">
                <div class="modal-content modal-large">
                    <div class="modal-header">
                        <div>
                            <span class="wa-card-category">${wa.category}</span>
                            <h2>${wa.issue}</h2>
                        </div>
                        <button class="modal-close-btn" id="close-view-modal">&times;</button>
                    </div>
                    <div class="wa-view-meta">
                        <span>👤 ${wa.created_by}</span>
                        <span>📅 ${postDate}</span>
                        <span>👁️ ${wa.views || 0} views</span>
                        <span>👍 ${wa.likes || 0} likes</span>
                    </div>
                    <div class="wa-view-content">
                        ${wa.description}
                    </div>
                </div>
            </div>
        `;

        document.getElementById('close-view-modal').addEventListener('click', () => {
            document.getElementById('view-wa-modal').classList.remove('visible');
            setTimeout(() => container.innerHTML = '', 300);
        });

        document.getElementById('view-wa-modal').addEventListener('click', (e) => {
            if (e.target.id === 'view-wa-modal') {
                document.getElementById('view-wa-modal').classList.remove('visible');
                setTimeout(() => container.innerHTML = '', 300);
            }
        });
    },

    /**
     * Like a workaround
     */
    async likeWorkaround(id) {
        try {
            await API.incrementLike(id);
            console.log('✅ Workaround liked');
            await this.fetchAllData(); // Refresh to show updated like count
        } catch (error) {
            console.error('❌ Failed to like workaround:', error);
        }
    },

    /**
     * Edit workaround
     */
    editWorkaround(id) {
        const wa = this.currentData.wa.find(w => w.id === id);
        if (wa) {
            this.showWorkaroundModal(wa);
        }
    },

    /**
     * Delete workaround
     */
    async deleteWorkaround(id) {
        if (!confirm('Are you sure you want to delete this workaround? This action cannot be undone.')) {
            return;
        }

        try {
            await API.deleteWorkaround(id);
            console.log('✅ Workaround deleted');
            await this.fetchAllData(); // Refresh data
        } catch (error) {
            console.error('❌ Failed to delete workaround:', error);
            alert('Failed to delete workaround. Please try again.');
        }
    },

    /**
     * Download single workaround as HTML (PDF generation would require additional library)
     */
    downloadWorkaround(id) {
        const wa = this.currentData.wa.find(w => w.id === id);
        if (!wa) return;

        const htmlContent = `
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>${wa.issue}</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }
                    h1 { color: #333; }
                    .meta { color: #666; margin-bottom: 30px; }
                    .category { background: #8B5CF6; color: white; padding: 5px 15px; border-radius: 5px; display: inline-block; }
                    .content { line-height: 1.6; }
                </style>
            </head>
            <body>
                <span class="category">${wa.category}</span>
                <h1>${wa.issue}</h1>
                <div class="meta">
                    <p>Created by: ${wa.created_by}</p>
                    <p>Date: ${new Date(wa.created_date).toLocaleString()}</p>
                </div>
                <div class="content">
                    ${wa.description}
                </div>
            </body>
            </html>
        `;

        const blob = new Blob([htmlContent], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `workaround_${id}_${wa.issue.substring(0, 30).replace(/[^a-z0-9]/gi, '_')}.html`;
        a.click();
        URL.revokeObjectURL(url);

        console.log('✅ Workaround downloaded');
    },

    /**
     * Download all workarounds
     */
    downloadAllWorkarounds() {
        this.currentData.wa.forEach(wa => {
            setTimeout(() => this.downloadWorkaround(wa.id), 100);
        });
    },

    /**
     * Export data to CSV/Excel format
     */
    exportToExcel(data, filename) {
        if (!data || data.length === 0) {
            alert('No data to export');
            return;
        }

        // Convert to CSV
        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(','),
            ...data.map(row => 
                headers.map(header => {
                    const cell = row[header] || '';
                    // Escape quotes and wrap in quotes if contains comma
                    return typeof cell === 'string' && (cell.includes(',') || cell.includes('"'))
                        ? `"${cell.replace(/"/g, '""')}"`
                        : cell;
                }).join(',')
            )
        ].join('\n');

        // Download
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${filename}_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        URL.revokeObjectURL(url);

        console.log(`✅ Exported ${data.length} rows to ${filename}`);
    },

    /**
     * Export all current results
     */
    exportAllResults() {
        this.exportToExcel(this.currentData.sr, 'SR_Results');
        setTimeout(() => this.exportToExcel(this.currentData.defect, 'Defect_Results'), 100);
        console.log('✅ All results exported');
    },

    /**
     * Show error message
     */
    showError(message) {
        const container = document.getElementById('sa-blog-posts-container');
        if (container) {
            container.innerHTML = `
                <div class="error-state">
                    <span class="error-icon">❌</span>
                    <h3>Error</h3>
                    <p>${message}</p>
                </div>
            `;
        }
    }
};

// Initialize the module
SearchAnything.init();
