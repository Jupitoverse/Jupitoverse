// Additional Companies Database - Extended 9
// 100+ More Companies

const COMPANIES_DATABASE_EXTENDED_9 = [
    // ==================== GLOBAL TECH GIANTS ====================
    {name: "Salesforce", type: "Big Tech", category: "CRM", salary: "₹25-65 LPA", location: "Hyderabad, Bangalore", remote: true, hiring: true, rating: 4.3, employees: "70,000+", description: "Cloud-based CRM leader"},
    {name: "ServiceNow", type: "Big Tech", category: "Enterprise", salary: "₹28-60 LPA", location: "Hyderabad, Bangalore", remote: true, hiring: true, rating: 4.4, employees: "18,000+", description: "Digital workflow company"},
    {name: "Workday", type: "Big Tech", category: "HR Tech", salary: "₹25-55 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.3, employees: "15,000+", description: "Enterprise HR software"},
    {name: "Snowflake", type: "Big Tech", category: "Data", salary: "₹35-80 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.5, employees: "5,000+", description: "Cloud data platform"},
    {name: "Databricks", type: "Big Tech", category: "Data", salary: "₹35-85 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.6, employees: "5,000+", description: "Data and AI company"},
    {name: "Confluent", type: "Big Tech", category: "Data", salary: "₹30-70 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.4, employees: "3,000+", description: "Data streaming platform"},
    {name: "MongoDB", type: "Big Tech", category: "Database", salary: "₹28-65 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.4, employees: "4,500+", description: "NoSQL database company"},
    {name: "Elastic", type: "Big Tech", category: "Search", salary: "₹25-60 LPA", location: "Bangalore, Pune", remote: true, hiring: true, rating: 4.3, employees: "3,000+", description: "Search and observability"},
    {name: "HashiCorp", type: "Big Tech", category: "DevOps", salary: "₹30-70 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.4, employees: "2,500+", description: "Infrastructure automation"},
    {name: "Palo Alto Networks", type: "Big Tech", category: "Security", salary: "₹28-65 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.3, employees: "13,000+", description: "Cybersecurity leader"},
    
    // ==================== FINTECH UNICORNS ====================
    {name: "Stripe", type: "Fintech", category: "Payments", salary: "₹35-85 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.6, employees: "8,000+", description: "Payment infrastructure"},
    {name: "Plaid", type: "Fintech", category: "Banking", salary: "₹30-70 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.4, employees: "1,500+", description: "Financial data network"},
    {name: "Brex", type: "Fintech", category: "Corporate Cards", salary: "₹28-65 LPA", location: "Bangalore", remote: true, hiring: false, rating: 4.3, employees: "1,200+", description: "Corporate credit cards"},
    {name: "Affirm", type: "Fintech", category: "BNPL", salary: "₹28-60 LPA", location: "Remote", remote: true, hiring: true, rating: 4.2, employees: "2,500+", description: "Buy now pay later"},
    {name: "Coinbase", type: "Fintech", category: "Crypto", salary: "₹35-80 LPA", location: "Remote", remote: true, hiring: false, rating: 4.1, employees: "5,000+", description: "Cryptocurrency exchange"},
    {name: "Revolut", type: "Fintech", category: "Neobank", salary: "₹25-55 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.0, employees: "6,000+", description: "Digital banking"},
    {name: "Wise", type: "Fintech", category: "Remittance", salary: "₹22-50 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.3, employees: "4,500+", description: "International transfers"},
    {name: "Klarna", type: "Fintech", category: "BNPL", salary: "₹25-55 LPA", location: "Remote", remote: true, hiring: false, rating: 4.1, employees: "5,000+", description: "Buy now pay later"},
    
    // ==================== INDIAN FINTECH ====================
    {name: "PhonePe", type: "Fintech", category: "Payments", salary: "₹20-50 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.2, employees: "5,000+", description: "UPI payments leader"},
    {name: "Paytm", type: "Fintech", category: "Payments", salary: "₹15-40 LPA", location: "Noida", remote: false, hiring: true, rating: 3.8, employees: "10,000+", description: "Digital payments ecosystem"},
    {name: "CRED", type: "Fintech", category: "Credit Cards", salary: "₹25-60 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.4, employees: "1,500+", description: "Credit card payments app"},
    {name: "BharatPe", type: "Fintech", category: "Payments", salary: "₹18-45 LPA", location: "Delhi", remote: false, hiring: true, rating: 3.9, employees: "2,000+", description: "Merchant payments"},
    {name: "Groww", type: "Fintech", category: "Investment", salary: "₹18-45 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.2, employees: "1,500+", description: "Investment platform"},
    {name: "Zerodha", type: "Fintech", category: "Trading", salary: "₹20-50 LPA", location: "Bangalore", remote: false, hiring: false, rating: 4.5, employees: "1,500+", description: "Discount broker"},
    {name: "INDmoney", type: "Fintech", category: "Wealth", salary: "₹15-40 LPA", location: "Gurgaon", remote: false, hiring: true, rating: 4.1, employees: "500+", description: "Super money app"},
    {name: "Slice", type: "Fintech", category: "Credit Cards", salary: "₹15-40 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.0, employees: "1,000+", description: "Credit card for millennials"},
    {name: "Jupiter", type: "Fintech", category: "Neobank", salary: "₹18-45 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.2, employees: "500+", description: "Digital banking app"},
    {name: "Fi Money", type: "Fintech", category: "Neobank", salary: "₹20-50 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.3, employees: "400+", description: "AI-powered neobank"},
    
    // ==================== ECOMMERCE & CONSUMER ====================
    {name: "Meesho", type: "E-commerce", category: "Social Commerce", salary: "₹18-45 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.0, employees: "2,000+", description: "Social commerce platform"},
    {name: "Myntra", type: "E-commerce", category: "Fashion", salary: "₹18-45 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.1, employees: "3,000+", description: "Fashion e-commerce"},
    {name: "Nykaa", type: "E-commerce", category: "Beauty", salary: "₹15-40 LPA", location: "Mumbai", remote: false, hiring: true, rating: 4.0, employees: "3,500+", description: "Beauty e-commerce"},
    {name: "Lenskart", type: "E-commerce", category: "Eyewear", salary: "₹15-40 LPA", location: "Delhi NCR", remote: false, hiring: true, rating: 4.1, employees: "10,000+", description: "Eyewear brand"},
    {name: "FirstCry", type: "E-commerce", category: "Baby", salary: "₹12-35 LPA", location: "Pune", remote: false, hiring: true, rating: 3.9, employees: "5,000+", description: "Baby products"},
    {name: "BigBasket", type: "E-commerce", category: "Grocery", salary: "₹15-40 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.0, employees: "15,000+", description: "Online grocery"},
    {name: "Blinkit", type: "E-commerce", category: "Quick Commerce", salary: "₹18-45 LPA", location: "Gurgaon", remote: false, hiring: true, rating: 4.1, employees: "5,000+", description: "Quick delivery"},
    {name: "Zepto", type: "E-commerce", category: "Quick Commerce", salary: "₹18-45 LPA", location: "Mumbai", remote: false, hiring: true, rating: 4.2, employees: "3,000+", description: "10-min delivery"},
    {name: "Dunzo", type: "E-commerce", category: "Quick Commerce", salary: "₹15-40 LPA", location: "Bangalore", remote: false, hiring: false, rating: 3.8, employees: "1,500+", description: "Hyperlocal delivery"},
    
    // ==================== FOODTECH ====================
    {name: "Zomato", type: "FoodTech", category: "Food Delivery", salary: "₹18-50 LPA", location: "Gurgaon", remote: false, hiring: true, rating: 4.0, employees: "8,000+", description: "Food delivery platform"},
    {name: "Swiggy", type: "FoodTech", category: "Food Delivery", salary: "₹18-50 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.1, employees: "10,000+", description: "Food delivery platform"},
    {name: "EatFit", type: "FoodTech", category: "Health Food", salary: "₹12-30 LPA", location: "Mumbai", remote: false, hiring: true, rating: 3.9, employees: "500+", description: "Healthy food delivery"},
    {name: "Rebel Foods", type: "FoodTech", category: "Cloud Kitchen", salary: "₹15-40 LPA", location: "Mumbai", remote: false, hiring: true, rating: 4.0, employees: "3,000+", description: "Cloud kitchen company"},
    {name: "Licious", type: "FoodTech", category: "Meat Delivery", salary: "₹15-40 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.1, employees: "2,000+", description: "Fresh meat delivery"},
    {name: "Country Delight", type: "FoodTech", category: "Dairy", salary: "₹12-35 LPA", location: "Gurgaon", remote: false, hiring: true, rating: 4.0, employees: "1,500+", description: "Dairy delivery"},
    
    // ==================== EDTECH ====================
    {name: "BYJU'S", type: "EdTech", category: "K-12", salary: "₹12-40 LPA", location: "Bangalore", remote: false, hiring: false, rating: 3.5, employees: "50,000+", description: "Learning app"},
    {name: "Unacademy", type: "EdTech", category: "Test Prep", salary: "₹15-45 LPA", location: "Bangalore", remote: false, hiring: false, rating: 3.8, employees: "10,000+", description: "Online learning"},
    {name: "Vedantu", type: "EdTech", category: "Live Classes", salary: "₹12-40 LPA", location: "Bangalore", remote: false, hiring: false, rating: 3.9, employees: "5,000+", description: "Live learning"},
    {name: "upGrad", type: "EdTech", category: "Higher Ed", salary: "₹15-45 LPA", location: "Mumbai", remote: false, hiring: true, rating: 4.0, employees: "4,000+", description: "Online degrees"},
    {name: "Scaler", type: "EdTech", category: "Tech Education", salary: "₹20-50 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.3, employees: "1,500+", description: "Tech upskilling"},
    {name: "Physics Wallah", type: "EdTech", category: "Test Prep", salary: "₹10-30 LPA", location: "Noida", remote: false, hiring: true, rating: 4.2, employees: "5,000+", description: "Affordable education"},
    {name: "Cuemath", type: "EdTech", category: "Math", salary: "₹12-35 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.0, employees: "1,000+", description: "Math learning"},
    {name: "Eruditus", type: "EdTech", category: "Executive Ed", salary: "₹18-50 LPA", location: "Mumbai", remote: false, hiring: true, rating: 4.1, employees: "2,000+", description: "Executive education"},
    
    // ==================== HEALTHTECH ====================
    {name: "Practo", type: "HealthTech", category: "Healthcare", salary: "₹15-45 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.0, employees: "3,000+", description: "Healthcare platform"},
    {name: "PharmEasy", type: "HealthTech", category: "Pharmacy", salary: "₹12-40 LPA", location: "Mumbai", remote: false, hiring: true, rating: 3.9, employees: "5,000+", description: "Online pharmacy"},
    {name: "1mg", type: "HealthTech", category: "Pharmacy", salary: "₹12-40 LPA", location: "Gurgaon", remote: false, hiring: true, rating: 4.0, employees: "4,000+", description: "Healthcare platform"},
    {name: "Netmeds", type: "HealthTech", category: "Pharmacy", salary: "₹10-35 LPA", location: "Chennai", remote: false, hiring: true, rating: 3.8, employees: "2,000+", description: "Online pharmacy"},
    {name: "Cure.fit", type: "HealthTech", category: "Fitness", salary: "₹15-45 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.1, employees: "3,000+", description: "Health and fitness"},
    {name: "MediBuddy", type: "HealthTech", category: "Healthcare", salary: "₹12-40 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.0, employees: "1,000+", description: "Healthcare platform"},
    {name: "Portea", type: "HealthTech", category: "Home Care", salary: "₹10-30 LPA", location: "Bangalore", remote: false, hiring: true, rating: 3.9, employees: "3,000+", description: "Home healthcare"},
    
    // ==================== MOBILITY ====================
    {name: "Ola", type: "Mobility", category: "Ride Hailing", salary: "₹18-50 LPA", location: "Bangalore", remote: false, hiring: true, rating: 3.9, employees: "8,000+", description: "Ride-hailing platform"},
    {name: "Uber India", type: "Mobility", category: "Ride Hailing", salary: "₹22-55 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.2, employees: "3,000+", description: "Ride-hailing platform"},
    {name: "Rapido", type: "Mobility", category: "Bike Taxi", salary: "₹15-40 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.0, employees: "1,500+", description: "Bike taxi platform"},
    {name: "Ather Energy", type: "Mobility", category: "EV", salary: "₹15-45 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.3, employees: "2,000+", description: "Electric vehicles"},
    {name: "Ola Electric", type: "Mobility", category: "EV", salary: "₹18-50 LPA", location: "Bangalore", remote: false, hiring: true, rating: 4.0, employees: "5,000+", description: "Electric scooters"},
    {name: "Bounce", type: "Mobility", category: "Bike Rental", salary: "₹12-35 LPA", location: "Bangalore", remote: false, hiring: true, rating: 3.8, employees: "1,000+", description: "Bike sharing"},
    {name: "Yulu", type: "Mobility", category: "Micro Mobility", salary: "₹10-30 LPA", location: "Bangalore", remote: false, hiring: true, rating: 3.9, employees: "500+", description: "Electric bikes"},
    
    // ==================== SAAS COMPANIES ====================
    {name: "Freshworks", type: "SaaS", category: "Business Software", salary: "₹20-55 LPA", location: "Chennai", remote: true, hiring: true, rating: 4.2, employees: "6,000+", description: "Business software suite"},
    {name: "Zoho", type: "SaaS", category: "Business Software", salary: "₹12-40 LPA", location: "Chennai", remote: true, hiring: true, rating: 4.0, employees: "12,000+", description: "Business apps"},
    {name: "Chargebee", type: "SaaS", category: "Billing", salary: "₹22-55 LPA", location: "Chennai", remote: true, hiring: true, rating: 4.3, employees: "1,000+", description: "Subscription billing"},
    {name: "Postman", type: "SaaS", category: "API Tools", salary: "₹25-60 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.4, employees: "1,000+", description: "API platform"},
    {name: "CleverTap", type: "SaaS", category: "Marketing", salary: "₹18-50 LPA", location: "Mumbai", remote: true, hiring: true, rating: 4.1, employees: "800+", description: "Customer engagement"},
    {name: "WebEngage", type: "SaaS", category: "Marketing", salary: "₹15-45 LPA", location: "Mumbai", remote: true, hiring: true, rating: 4.0, employees: "700+", description: "Marketing automation"},
    {name: "MoEngage", type: "SaaS", category: "Marketing", salary: "₹18-50 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.1, employees: "700+", description: "Customer engagement"},
    {name: "Whatfix", type: "SaaS", category: "DAP", salary: "₹18-50 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.2, employees: "600+", description: "Digital adoption platform"},
    {name: "Druva", type: "SaaS", category: "Data Protection", salary: "₹22-55 LPA", location: "Pune", remote: true, hiring: true, rating: 4.2, employees: "1,500+", description: "Cloud data protection"},
    {name: "BrowserStack", type: "SaaS", category: "Testing", salary: "₹22-55 LPA", location: "Mumbai", remote: true, hiring: true, rating: 4.3, employees: "1,000+", description: "Browser testing"},
    {name: "LeadSquared", type: "SaaS", category: "CRM", salary: "₹15-45 LPA", location: "Bangalore", remote: true, hiring: true, rating: 4.0, employees: "500+", description: "Marketing automation"},
    {name: "Darwinbox", type: "SaaS", category: "HR Tech", salary: "₹18-50 LPA", location: "Hyderabad", remote: true, hiring: true, rating: 4.2, employees: "800+", description: "HR platform"},
    {name: "Sprinklr", type: "SaaS", category: "CXM", salary: "₹20-55 LPA", location: "Gurgaon", remote: true, hiring: true, rating: 4.1, employees: "4,000+", description: "Customer experience"},
];

// Export
if (typeof window !== 'undefined') {
    window.COMPANIES_DATABASE_EXTENDED_9 = COMPANIES_DATABASE_EXTENDED_9;
}

