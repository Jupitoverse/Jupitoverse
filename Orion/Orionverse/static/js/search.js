// static/js/search.js
const SearchAnything = {
    workarounds: [],
    quill: null,
    editingId: null, // NEW: To track which workaround is being edited

    init() {
        document.addEventListener('pageLoaded', (e) => {
            if (e.detail.pageId === 'search-anything') {
                this.setupPage();
            }
        });
    },
    

    setupPage() {
        this.fetchWorkarounds();
        this.attachEventListeners();
        this.initDataTables();
        this.fetchAllData(); // Fetch initial top 10 data
        this.attachEventListeners();
    },
    initDataTables() {
        if ($.fn.DataTable.isDataTable('#sr-results-table')) {
            $('#sr-results-table').DataTable().destroy();
        }
        if ($.fn.DataTable.isDataTable('#defect-results-table')) {
            $('#defect-results-table').DataTable().destroy();
        }

        this.srTable = $('#sr-results-table').DataTable({
            data: [], // Start with empty data
            columns: [
                { data: 'SR_ID', title: 'SR ID' },
                { data: 'CUSTOMER_ID', title: 'Customer ID' },
                { data: 'DETAILS', title: 'Details' },
                { data: 'RCA', title: 'RCA' }
            ],
            pageLength: 10,
            lengthChange: false,
            info: false
        });
        this.defectTable = $('#defect-results-table').DataTable({
            data: [],
            columns: [
                { data: 'ID', title: 'Defect ID' },
                { data: 'Name', title: 'Name' },
                { data: 'Description', title: 'Description' }
            ],
            pageLength: 10,
            lengthChange: false,
            info: false
        });
    },
    async fetchAllData() {
        $('#search-loader').show();
        try {
            // This API call now correctly fetches the top 10 of each
            const data = await API.getAllSearchData();
            this.renderAllResults(data);
        } catch (error) {
            const container = document.getElementById('sa-blog-posts-container');
            container.innerHTML = `<p class="error-message">Error: Could not fetch workarounds. Is the backend server running?</p>`;
        } finally {
            $('#search-loader').hide();
        }
    },

    async fetchWorkarounds() {
        try {
            this.workarounds = await API.getWorkarounds();
            this.renderCards(this.workarounds);
        } catch (error) {
            document.getElementById('sa-blog-posts-container').innerHTML = `<p class="error-message">Error: Could not fetch workarounds.</p>`;
        }
    },
    
    renderCards(posts) {
        const container = document.getElementById('sa-blog-posts-container');
        if (!container) return;
        if (!posts || posts.length === 0) {
            container.innerHTML = '<p>No workarounds found.</p>';
            return;
        }
        container.innerHTML = posts.map(post => {
            const postDate = new Date(post.created_date).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', dateStyle: 'long', timeStyle: 'short' });
            return `
            <article class="wa-card" data-id="${post.id}">
                <div class="wa-card-header">
                    <span class="wa-card-category">${post.category}</span>
                    <h3 class="wa-card-issue">${post.issue}</h3>
                </div>
                <p class="wa-card-meta">By ${post.created_by} on ${postDate}</p>
                <div class="wa-card-description"><div class="sa-post-content">${post.description}</div></div>
                <div class="wa-card-footer">
                    <div class="wa-card-actions">
                        <button class="wa-read-more-btn secondary-btn">Read More</button>
                        <button class="wa-like-btn secondary-btn">👍 Like</button>
                        <button class="wa-edit-btn secondary-btn">✏️ Edit</button>
                        <button class="wa-delete-btn secondary-btn danger-btn">🗑️ Delete</button>
                    </div>
                    <div class="wa-card-stats">
                        <span class="wa-likes-count">${post.likes} Likes</span>
                        <span class="wa-views-count">${post.views} Views</span>
                    </div>
                </div>
            </article>`;
        }).join('');
        this.attachDynamicEventListeners();
    },
    
    attachEventListeners() { /* ... same as before ... */ },
    
    attachDynamicEventListeners() {
        document.querySelectorAll('.wa-card').forEach(card => {
            card.addEventListener('click', e => {
                if (e.target.matches('.wa-read-more-btn')) this.handleReadMore(e);
                if (e.target.matches('.wa-like-btn')) this.handleLike(e);
                if (e.target.matches('.wa-edit-btn')) this.handleEdit(e);
                if (e.target.matches('.wa-delete-btn')) this.handleDelete(e);
            });
        });
    },

    // NEW: Handler for the Edit button
    handleEdit(e) {
        const card = e.target.closest('.wa-card');
        const id = parseInt(card.dataset.id);
        const workaroundToEdit = this.workarounds.find(wa => wa.id === id);
        if (workaroundToEdit) {
            this.showModal(workaroundToEdit);
        }
    },

    // NEW: Handler for the Delete button
    async handleDelete(e) {
        const card = e.target.closest('.wa-card');
        const id = card.dataset.id;
        
        if (window.confirm('Are you sure you want to delete this workaround?')) {
            try {
                await API.deleteWorkaround(id);
                this.fetchWorkarounds(); // Refresh the list from the database
            } catch (error) {
                alert('Failed to delete workaround.');
            }
        }
    },

    // MODIFIED: showModal now accepts an optional object to pre-fill the form
    showModal(workaroundToEdit = null) {
        const modalTitle = document.querySelector('#workaround-modal .modal-header h2');
        const form = document.getElementById('workaround-form');

        if (workaroundToEdit) {
            this.editingId = workaroundToEdit.id;
            modalTitle.textContent = 'Edit Workaround';
            form.querySelector('#wa-category').value = workaroundToEdit.category;
            form.querySelector('#wa-issue').value = workaroundToEdit.issue;
        } else {
            this.editingId = null;
            modalTitle.textContent = 'New Workaround Details';
            form.reset();
        }
        
        document.getElementById('workaround-modal').classList.add('visible');
        if (!this.quill) {
            this.quill = new Quill('#editor-container', { theme: 'snow' });
        }
        this.quill.root.innerHTML = workaroundToEdit ? workaroundToEdit.description : '';
    },
    
    // MODIFIED: handleSubmit now handles both creating and updating
    async handleSubmit(e) {
        e.preventDefault();
        const workaroundData = {
            issue: document.getElementById('wa-issue').value,
            category: document.getElementById('wa-category').value,
            description: this.quill.root.innerHTML,
        };

        try {
            if (this.editingId) {
                // We are updating an existing workaround
                await API.updateWorkaround(this.editingId, workaroundData);
            } else {
                // We are creating a new one
                workaroundData.created_by = Auth.currentUser ? Auth.currentUser.fullname : 'Anonymous';
                await API.addWorkaround(workaroundData);
            }
            this.hideModal();
            this.fetchWorkarounds(); // Refresh list
        } catch (error) {
            alert('Failed to save workaround.');
        }
    },
    
    // All other functions (hideModal, handleReadMore, handleLike) remain the same.
};