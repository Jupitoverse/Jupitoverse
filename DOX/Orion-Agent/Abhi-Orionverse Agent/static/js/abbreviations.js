// static/js/abbreviations.js

const abbreviations = [
    { term: "AMIL", definition: "Amdocs Isolation Layer, Amdocs product to provide a gateway to isolate other Amdocs products from third party interfaces" },
    { term: "ARM", definition: "Amdocs Resource Manager, Amdocs product used for resource inventory" },
    { term: "BI", definition: "Business Internet" },
    { term: "CLIPS", definition: "Comcast Logical Inventory and Provisioning Services" },
    { term: "CLLI", definition: "Common Language Location Identifier" },
    { term: "CFS", definition: "Customer Facing Service" },
    { term: "CPE", definition: "Customer Premise Equipment" },
    { term: "CRM", definition: "Customer Relationship Management system" },
    { term: "DE", definition: "Design Engineer" },
    { term: "DHCP", definition: "Dynamic Host Configuration Protocol" },
    { term: "ENUM", definition: "Enumerated type" },
    { term: "EPL", definition: "Ethernet Private Line" },
    { term: "EVC", definition: "Ethernet Virtual Connection" },
    { term: "EVPL", definition: "Ethernet Virtual Private Line" },
    { term: "FQDN", definition: "Fully Qualified Domain Name" },
    { term: "GT", definition: "Guided Task, a manual activity in ODO that requires human interaction" },
    { term: "GUI", definition: "Graphical User Interface" },
    { term: "HFC", definition: "Hybrid Fiber-Coaxial" },
    { term: "IP", definition: "Internet Protocol" },
    { term: "MEC", definition: "Master Enterprise Catalog, Amdocs product used to model the product catalog" },
    { term: "MetroE", definition: "Metro Ethernet" },
    { term: "MRS", definition: "Manage Resource Services" },
    { term: "ODO", definition: "Order Delivery Orchestrator, Amdocs product used for orchestration of workflows. Used for serviceability, site survey, sales to delivery and fulfillment processes" },
    { term: "OH", definition: "Order Handling, Amdocs product responsible for submitting orders to ODO for fulfillment" },
    { term: "OM", definition: "Orion Middleware" },
    { term: "OSS", definition: "Operational Support Systems" },
    { term: "RFS", definition: "Resource Facing Service" },
    { term: "ROE", definition: "Right of entry, its process of gaining the relevant permissions to enter a property to perform construction activities" },
    { term: "SOM", definition: "Service Order Management, Amdocs product used to manage service fulfillment" },
    { term: "SOO", definition: "Sales Quote Order, Amdocs product for selecting products for customer orders based on catalog guidance" },
    { term: "TET", definition: "Task Engine Catalog" },
    { term: "TMS", definition: "Task Management Service" },
    { term: "USM", definition: "Unified Service Manager, Amdocs product for service inventory" },
    { term: "VPN", definition: "Virtual Private Network" },
    { term: "WBS", definition: "Work Breakdown Structure, a subflow in ODO" },
    { term: "WFX", definition: "Workforce Express" },
    { term: "WS", definition: "Web Services" },
    { term: "ACP", definition: "Access Circuit Provisioning" },
    { term: "ALI", definition: "Automatic Location Identification" },
    { term: "ANI", definition: "Automatic Number Identification" },
    { term: "ARO", definition: "Asset Recovery Order" },
    { term: "ASR", definition: "Access Service Request" },
    { term: "AUA", definition: "Amdocs Universal Activator" },
    { term: "BTN", definition: "Basic Telephone Number" },
    { term: "CDDDC/RC", definition: "Customer Desired due date" },
    { term: "CHQ", definition: "Customer Has a Question" },
    { term: "CIC", definition: "Carrier Identifier Code (in SMS800/Lucid)" },
    { term: "CID", definition: "Caller ID" },
    { term: "CMP", definition: "Customer Messaging Platform" },
    { term: "CNR", definition: "Customer Not Ready" },
    { term: "COP", definition: "Customer Ordered Product" },
    { term: "CPM", definition: "Customer Project Manager" },
    { term: "CRC/CRCR/CP/CRCP", definition: "X-Rate Center Porting Cross Rate Center Porting" },
    { term: "CSR", definition: "Customer Service Record" },
    { term: "DLR", definition: "Design Layout Record (-)" },
    { term: "DNIS", definition: "Dialed Number Identification Service" },
    { term: "DOC", definition: "Date of Install" },
    { term: "DOI", definition: "Date of Install" },
    { term: "DRW", definition: "Design Review Worksheet" },
    { term: "DTG", definition: "Direct Trunk Overflow" },
    { term: "DTO", definition: "Direct Trunk Overflow" },
    { term: "EDI", definition: "Ethernet Dedicated Internet" },
    { term: "EDP", definition: "Engineering Design Package" },
    { term: "ENS", definition: "Ethernet Network Service" },
    { term: "ESN", definition: "Equipment Serial Number" },
    { term: "FOC", definition: "Firm Order Commitment Date" },
    { term: "IAD", definition: "Integrated Access Device" },
    { term: "IPM", definition: "IP Address Management" },
    { term: "KOM", definition: "Kick off Call (meeting)" },
    { term: "LATA", definition: "Local access and transport area" },
    { term: "LNP", definition: "Local Number Portability" },
    { term: "LOA", definition: "Letter of Agency" },
    { term: "LOCN", definition: "Location" },
    { term: "MRC", definition: "Monthly Recurring Charge" },
    { term: "MSAG", definition: "Master Street Address Guide" },
    { term: "MSP", definition: "Manage Service Provider" },
    { term: "MVT", definition: "Manage Verification Test" },
    { term: "NANP", definition: "North American Numbering Plan" },
    { term: "NPA", definition: "Numbering Plan Area code" },
    { term: "NPANXX", definition: "exchange code" },
    { term: "ODR", definition: "Order Delivery Orchestration" },
    { term: "OTF", definition: "Order Test and Turn-up Orchestration tool" },
    { term: "PAT", definition: "Port Allocation Tool (PAT)" },
    { term: "RCF", definition: "Remote Call Forwarding" },
    { term: "RespOrg", definition: "Responsible Organization for TF number in SMS800" },
    { term: "ROD", definition: "Resp Org Desk" },
    { term: "RTN", definition: "Ring to Number aka translation # for Toll Free" },
    { term: "SCD", definition: "Schedule" },
    { term: "SMB", definition: "Small Medium Business" },
    { term: "SCM", definition: "Service Orchestration Manager" },
    { term: "SRWQ", definition: "Service Request Work Queue" },
    { term: "TF", definition: "Toll Free" },
    { term: "TNO", definition: "Translation Number Organization (TNO)" },
    { term: "TTUA", definition: "Test and Turn-up Access" },
    { term: "WFX", definition: "Work Force Express" }
];

// Initialize abbreviations
function initializeAbbreviations() {
    const container = document.getElementById('abbreviations-container');
    if (!container) return;
    
    // Clear existing content
    container.innerHTML = '';
    
    abbreviations.forEach(item => {
        const card = document.createElement('div');
        card.className = 'abbr-card';
        card.innerHTML = `
            <div class="abbr-term">${item.term}</div>
            <div class="abbr-definition">${item.definition}</div>
        `;
        container.appendChild(card);
    });
}

// Search functionality
function setupAbbreviationSearch() {
    const searchInput = document.getElementById('abbr-search');
    if (!searchInput) return;
    
    // Remove any existing listeners
    const newSearchInput = searchInput.cloneNode(true);
    searchInput.parentNode.replaceChild(newSearchInput, searchInput);
    
    newSearchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const cards = document.querySelectorAll('.abbr-card');
        let visibleCount = 0;
        
        cards.forEach(card => {
            const term = card.querySelector('.abbr-term').textContent.toLowerCase();
            const definition = card.querySelector('.abbr-definition').textContent.toLowerCase();
            
            if (term.includes(searchTerm) || definition.includes(searchTerm)) {
                card.classList.remove('hidden');
                visibleCount++;
            } else {
                card.classList.add('hidden');
            }
        });
        
        // Show/hide no results message
        const container = document.getElementById('abbreviations-container');
        let noResults = container.querySelector('.no-results');
        
        if (visibleCount === 0 && searchTerm) {
            if (!noResults) {
                noResults = document.createElement('div');
                noResults.className = 'no-results';
                noResults.textContent = `No abbreviations found for "${searchTerm}"`;
                container.appendChild(noResults);
            }
        } else if (noResults) {
            noResults.remove();
        }
    });
}

// Listen for page loaded event
document.addEventListener('pageLoaded', function(e) {
    if (e.detail.pageId === 'abbreviation') {
        setTimeout(function() {
            initializeAbbreviations();
            setupAbbreviationSearch();
        }, 100);
    }
});


