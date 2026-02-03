// static/js/bulk_handling.js
// Bulk Handling Tab Switching and Form Management

(function() {
    'use strict';
    
    let initialized = false;
    
    function initBulkHandling() {
        // Prevent multiple initializations
        if (initialized) {
            console.log('Bulk handling already initialized, skipping...');
            return;
        }
        
        console.log('=== Initializing Bulk Handling ===');
        
        const tabButtons = document.querySelectorAll('.bulk-tab-btn');
        const tabContents = document.querySelectorAll('.bulk-tab-content');
        
        console.log('Found tab buttons:', tabButtons.length);
        console.log('Found tab contents:', tabContents.length);
        
        if (tabButtons.length === 0 || tabContents.length === 0) {
            console.warn('No tabs found, will retry...');
            return;
        }
        
        // Add click handlers to each tab button
        tabButtons.forEach((button, index) => {
            console.log(`Setting up tab ${index}:`, button.getAttribute('data-tab'));
            
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const targetTab = this.getAttribute('data-tab');
                console.log('>>> Tab clicked:', targetTab);
                
                // Remove active from all
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active to current
                this.classList.add('active');
                const targetContent = document.getElementById(targetTab);
                
                if (targetContent) {
                    targetContent.classList.add('active');
                    console.log('>>> Tab activated successfully:', targetTab);
                } else {
                    console.error('>>> Tab content NOT FOUND:', targetTab);
                }
            });
        });
        
        initialized = true;
        console.log('=== Bulk Handling Initialized Successfully ===');
    }
    
    function initLineCounters() {
        console.log('Initializing line counters...');
        
        const textareas = [
            { id: 'retry-input', counter: 'retry-line-count' },
            { id: 'force-input', counter: 'force-line-count' },
            { id: 'reexec-input', counter: 'reexec-line-count' },
            { id: 'resolve-input', counter: 'resolve-line-count' },
            { id: 'stuck-input', counter: 'stuck-line-count' },
            { id: 'flag-input', counter: 'flag-line-count' }
        ];
        
        textareas.forEach(({ id, counter }) => {
            const textarea = document.getElementById(id);
            const counterElement = document.getElementById(counter);
            
            if (textarea && counterElement) {
                textarea.addEventListener('input', function() {
                    const lines = window.parseIds ? window.parseIds(this.value) : this.value.split(/[\n,]+/).filter(x => x.trim()).length;
                    counterElement.textContent = lines;
                });
                console.log(`Line counter set up for: ${id}`);
            }
        });
    }
    
    // Try to initialize immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initBulkHandling, 100);
            setTimeout(initLineCounters, 100);
        });
    } else {
        setTimeout(initBulkHandling, 100);
        setTimeout(initLineCounters, 100);
    }
    
    // Listen for page loaded event (when navigating via hash)
    document.addEventListener('pageLoaded', function(e) {
        console.log('pageLoaded event received:', e.detail);
        if (e.detail && e.detail.pageId === 'bulk-handling') {
            initialized = false; // Reset flag to allow re-initialization
            setTimeout(function() {
                initBulkHandling();
                initLineCounters();
            }, 300);
        }
    });
    
    // Also try on window load as a fallback
    window.addEventListener('load', function() {
        setTimeout(function() {
            if (!initialized) {
                console.log('Window loaded, trying to initialize...');
                initBulkHandling();
                initLineCounters();
            }
        }, 200);
    });
    
})();
