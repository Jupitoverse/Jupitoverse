// Additional Companies Database - Extended 10
// 100+ More Companies - Global Tech & Consulting

const COMPANIES_DATABASE_EXTENDED_10 = [
    // ==================== CONSULTING & PROFESSIONAL SERVICES ====================
    {name: "McKinsey", type: "Consulting", category: "Strategy", salary: "₹35-90 LPA", location: "Mumbai, Delhi, Bangalore", remote: false, hiring: true, rating: 4.4, employees: "45,000+", description: "Top management consulting"},
    {name: "BCG", type: "Consulting", category: "Strategy", salary: "₹35-85 LPA", location: "Mumbai, Delhi", remote: false, hiring: true, rating: 4.4, employees: "30,000+", description: "Strategy consulting"},
    {name: "Bain & Company", type: "Consulting", category: "Strategy", salary: "₹35-85 LPA", location: "Mumbai, Delhi", remote: false, hiring: true, rating: 4.5, employees: "14,000+", description: "Strategy consulting"},
    {name: "Deloitte", type: "Consulting", category: "Big 4", salary: "₹12-50 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 4.0, employees: "400,000+", description: "Professional services"},
    {name: "PwC", type: "Consulting", category: "Big 4", salary: "₹12-50 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 4.0, employees: "300,000+", description: "Professional services"},
    {name: "EY", type: "Consulting", category: "Big 4", salary: "₹12-50 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 4.0, employees: "365,000+", description: "Professional services"},
    {name: "KPMG", type: "Consulting", category: "Big 4", salary: "₹12-50 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 4.0, employees: "265,000+", description: "Professional services"},
    {name: "Accenture", type: "Consulting", category: "Tech Consulting", salary: "₹8-45 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 4.0, employees: "700,000+", description: "Tech & consulting"},
    {name: "Capgemini", type: "Consulting", category: "Tech Consulting", salary: "₹6-35 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 3.8, employees: "350,000+", description: "Tech services"},
    {name: "Cognizant", type: "IT Services", category: "Tech Consulting", salary: "₹6-35 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 3.7, employees: "350,000+", description: "IT services"},
    
    // ==================== IT SERVICES ====================
    {name: "TCS", type: "IT Services", category: "Large IT", salary: "₹4-25 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 3.8, employees: "600,000+", description: "India's largest IT company"},
    {name: "Infosys", type: "IT Services", category: "Large IT", salary: "₹5-30 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 3.9, employees: "340,000+", description: "Global IT services"},
    {name: "Wipro", type: "IT Services", category: "Large IT", salary: "₹5-28 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 3.7, employees: "250,000+", description: "IT services company"},
    {name: "HCL Technologies", type: "IT Services", category: "Large IT", salary: "₹5-30 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 3.8, employees: "225,000+", description: "IT and engineering"},
    {name: "Tech Mahindra", type: "IT Services", category: "Large IT", salary: "₹5-28 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 3.7, employees: "150,000+", description: "IT services"},
    {name: "LTIMindtree", type: "IT Services", category: "Large IT", salary: "₹5-30 LPA", location: "All Major Cities", remote: true, hiring: true, rating: 3.9, employees: "90,000+", description: "IT consulting"},
    {name: "Mphasis", type: "IT Services", category: "Mid-sized IT", salary: "₹6-30 LPA", location: "Bangalore, Pune", remote: true, hiring: true, rating: 3.8, employees: "35,000+", description: "IT solutions"},
    {name: "Persistent Systems", type: "IT Services", category: "Mid-sized IT", salary: "₹7-35 LPA", location: "Pune, Bangalore", remote: true, hiring: true, rating: 4.0, employees: "22,000+", description: "Digital engineering"},
    {name: "Coforge", type: "IT Services", category: "Mid-sized IT", salary: "₹6-30 LPA", location: "Noida, Bangalore", remote: true, hiring: true, rating: 3.8, employees: "25,000+", description: "IT solutions"},
    {name: "Birlasoft", type: "IT Services", category: "Mid-sized IT", salary: "₹6-28 LPA", location: "Noida, Pune", remote: true, hiring: true, rating: 3.7, employees: "15,000+", description: "Enterprise solutions"},
    
    // ==================== PRODUCT COMPANIES ====================
    {name: "Intuit", type: "Product", category: "Fintech", salary: "₹28-70 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.4, employees: "15,000+", description: "TurboTax, QuickBooks"},
    {name: "Adobe", type: "Product", category: "Creative", salary: "₹25-65 LPA", location: "Noida, Bangalore", remote: true, hiring: true, rating: 4.3, employees: "28,000+", description: "Creative software"},
    {name: "SAP", type: "Product", category: "Enterprise", salary: "₹18-55 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.1, employees: "105,000+", description: "Enterprise software"},
    {name: "Oracle", type: "Product", category: "Database", salary: "₹18-55 LPA", location: "Bangalore, Hyderabad", remote: true, hiring: true, rating: 4.0, employees: "140,000+", description: "Database & cloud"},
    {name: "VMware", type: "Product", category: "Infrastructure", salary: "₹22-60 LPA", location: "Bangalore, Pune", remote: true, hiring: true, rating: 4.2, employees: "35,000+", description: "Cloud infrastructure"},
    {name: "Nutanix", type: "Product", category: "Infrastructure", salary: "₹22-60 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.3, employees: "8,000+", description: "HCI platform"},
    {name: "NetApp", type: "Product", category: "Storage", salary: "₹20-55 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.1, employees: "11,000+", description: "Data management"},
    {name: "Commvault", type: "Product", category: "Data Protection", salary: "₹18-50 LPA", location: "Bangalore, Hyderabad", remote: true, hiring: true, rating: 4.0, employees: "3,000+", description: "Data protection"},
    {name: "Veritas", type: "Product", category: "Data Management", salary: "₹18-50 LPA", location: "Pune", remote: true, hiring: true, rating: 3.9, employees: "6,000+", description: "Data management"},
    {name: "Citrix", type: "Product", category: "Virtualization", salary: "₹18-50 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.0, employees: "10,000+", description: "Virtualization"},
    
    // ==================== SEMICONDUCTOR & HARDWARE ====================
    {name: "Intel", type: "Semiconductor", category: "Chips", salary: "₹18-55 LPA", location: "Bangalore, Hyderabad", remote: true, hiring: true, rating: 4.2, employees: "130,000+", description: "Semiconductor giant"},
    {name: "AMD", type: "Semiconductor", category: "Chips", salary: "₹20-60 LPA", location: "Bangalore, Hyderabad", remote: true, hiring: true, rating: 4.3, employees: "25,000+", description: "Semiconductor company"},
    {name: "NVIDIA", type: "Semiconductor", category: "GPU", salary: "₹30-80 LPA", location: "Bangalore, Pune", remote: true, hiring: true, rating: 4.6, employees: "26,000+", description: "GPU and AI chips"},
    {name: "Qualcomm", type: "Semiconductor", category: "Mobile", salary: "₹22-60 LPA", location: "Bangalore, Hyderabad", remote: true, hiring: true, rating: 4.2, employees: "51,000+", description: "Mobile chips"},
    {name: "Broadcom", type: "Semiconductor", category: "Networking", salary: "₹20-55 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.0, employees: "20,000+", description: "Semiconductor company"},
    {name: "Texas Instruments", type: "Semiconductor", category: "Analog", salary: "₹18-50 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.1, employees: "30,000+", description: "Semiconductor company"},
    {name: "Micron", type: "Semiconductor", category: "Memory", salary: "₹18-50 LPA", location: "Bangalore, Hyderabad", remote: true, hiring: true, rating: 4.0, employees: "43,000+", description: "Memory solutions"},
    {name: "Samsung Semiconductor", type: "Semiconductor", category: "Memory", salary: "₹20-55 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.1, employees: "270,000+", description: "Semiconductor division"},
    {name: "Arm", type: "Semiconductor", category: "IP", salary: "₹25-65 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.3, employees: "6,500+", description: "Chip architecture"},
    {name: "Synopsys", type: "Semiconductor", category: "EDA", salary: "₹20-55 LPA", location: "Bangalore, Noida", remote: true, hiring: true, rating: 4.2, employees: "19,000+", description: "Chip design tools"},
    {name: "Cadence", type: "Semiconductor", category: "EDA", salary: "₹20-55 LPA", location: "Bangalore, Noida", remote: true, hiring: true, rating: 4.2, employees: "10,000+", description: "Electronic design"},
    {name: "MediaTek", type: "Semiconductor", category: "Mobile", salary: "₹18-50 LPA", location: "Bangalore, Noida", remote: true, hiring: true, rating: 4.0, employees: "17,000+", description: "Fabless chip company"},
    
    // ==================== NETWORKING ====================
    {name: "Cisco", type: "Networking", category: "Infrastructure", salary: "₹18-55 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.1, employees: "80,000+", description: "Networking giant"},
    {name: "Juniper Networks", type: "Networking", category: "Infrastructure", salary: "₹18-50 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.0, employees: "10,000+", description: "Networking solutions"},
    {name: "Arista Networks", type: "Networking", category: "Cloud Networking", salary: "₹25-65 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.4, employees: "3,500+", description: "Cloud networking"},
    {name: "F5 Networks", type: "Networking", category: "Application Delivery", salary: "₹18-50 LPA", location: "Bangalore, Hyderabad", remote: true, hiring: true, rating: 4.0, employees: "6,500+", description: "Application security"},
    {name: "Fortinet", type: "Networking", category: "Security", salary: "₹18-50 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.1, employees: "12,000+", description: "Cybersecurity"},
    
    // ==================== TELECOMMUNICATIONS ====================
    {name: "Nokia", type: "Telecom", category: "Equipment", salary: "₹15-45 LPA", location: "Bangalore, Chennai", remote: true, hiring: true, rating: 3.9, employees: "86,000+", description: "Telecom equipment"},
    {name: "Ericsson", type: "Telecom", category: "Equipment", salary: "₹15-45 LPA", location: "Bangalore, Chennai", remote: true, hiring: true, rating: 3.9, employees: "100,000+", description: "Telecom infrastructure"},
    {name: "Samsung Networks", type: "Telecom", category: "Equipment", salary: "₹18-50 LPA", location: "Bangalore, Noida", remote: true, hiring: true, rating: 4.0, employees: "270,000+", description: "Network solutions"},
    {name: "Jio (Reliance)", type: "Telecom", category: "Operator", salary: "₹12-40 LPA", location: "Mumbai, All Cities", remote: false, hiring: true, rating: 4.0, employees: "100,000+", description: "Telecom operator"},
    {name: "Airtel", type: "Telecom", category: "Operator", salary: "₹10-35 LPA", location: "Delhi, All Cities", remote: false, hiring: true, rating: 3.8, employees: "30,000+", description: "Telecom operator"},
    {name: "Vi (Vodafone Idea)", type: "Telecom", category: "Operator", salary: "₹8-30 LPA", location: "Mumbai, All Cities", remote: false, hiring: true, rating: 3.5, employees: "15,000+", description: "Telecom operator"},
    
    // ==================== GAMING ====================
    {name: "Electronic Arts", type: "Gaming", category: "Games", salary: "₹18-50 LPA", location: "Hyderabad", remote: true, hiring: true, rating: 4.1, employees: "12,500+", description: "Video game company"},
    {name: "Ubisoft", type: "Gaming", category: "Games", salary: "₹15-45 LPA", location: "Pune, Mumbai", remote: true, hiring: true, rating: 4.0, employees: "20,000+", description: "Video game publisher"},
    {name: "Rockstar Games", type: "Gaming", category: "Games", salary: "₹18-50 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.2, employees: "2,000+", description: "AAA game studio"},
    {name: "Zynga", type: "Gaming", category: "Mobile Games", salary: "₹18-50 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.0, employees: "3,000+", description: "Mobile games"},
    {name: "MPL", type: "Gaming", category: "Esports", salary: "₹15-45 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.0, employees: "800+", description: "Mobile esports"},
    {name: "Dream11", type: "Gaming", category: "Fantasy Sports", salary: "₹20-55 LPA", location: "Mumbai", remote: false, hiring: true, rating: 4.2, employees: "1,500+", description: "Fantasy sports"},
    {name: "Games24x7", type: "Gaming", category: "Online Gaming", salary: "₹18-50 LPA", location: "Mumbai, Bangalore", remote: false, hiring: true, rating: 4.1, employees: "1,000+", description: "RummyCircle, My11Circle"},
];

// Export
if (typeof window !== 'undefined') {
    window.COMPANIES_DATABASE_EXTENDED_10 = COMPANIES_DATABASE_EXTENDED_10;
}

