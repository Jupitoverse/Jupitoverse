// static/js/bulk_handling_tabs.js

function initializeBulkHandling() {
    const tabButtons = document.querySelectorAll('.bulk-tab-btn');
    const tabContents = document.querySelectorAll('.bulk-tab-content');
    
    if (tabButtons.length === 0) return;
    
    // Remove existing listeners by cloning
    tabButtons.forEach((button, index) => {
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
    });
    
    // Get fresh references
    const freshTabButtons = document.querySelectorAll('.bulk-tab-btn');
    const freshTabContents = document.querySelectorAll('.bulk-tab-content');
    
    freshTabButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const targetTab = this.getAttribute('data-tab');
            
            console.log('Tab clicked:', targetTab);
            
            // Remove active class from all buttons and contents
            freshTabButtons.forEach(btn => btn.classList.remove('active'));
            freshTabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
                console.log('Tab activated:', targetTab);
            } else {
                console.error('Tab content not found:', targetTab);
            }
        });
    });
    
    // Line counter for all textareas
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
            // Remove existing listener by cloning
            const newTextarea = textarea.cloneNode(true);
            textarea.parentNode.replaceChild(newTextarea, textarea);
            
            newTextarea.addEventListener('input', function() {
                const lines = parseIds(this.value);
                counterElement.textContent = lines.length;
            });
        }
    });
}

// Listen for page loaded event
document.addEventListener('pageLoaded', function(e) {
    if (e.detail.pageId === 'bulk-handling') {
        setTimeout(function() {
            initializeBulkHandling();
        }, 100);
    }
});


