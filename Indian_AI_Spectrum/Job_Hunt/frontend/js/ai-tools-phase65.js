// AI Tools Database - Phase 65: More CRM & Sales AI
// 150+ Additional CRM and sales tools

const AI_TOOLS_PHASE65 = [
    // ==================== CRM PLATFORMS ====================
    {name: "Salesforce", category: "CRM", subcategory: "Enterprise", desc: "Enterprise CRM", url: "salesforce.com", pricing: "Paid", rating: 4.4, tags: ["enterprise", "cloud", "comprehensive"], featured: true},
    {name: "HubSpot CRM", category: "CRM", subcategory: "All-in-One", desc: "Free CRM", url: "hubspot.com/crm", pricing: "Freemium", rating: 4.5, tags: ["free", "marketing", "all-in-one"]},
    {name: "Zoho CRM", category: "CRM", subcategory: "SMB", desc: "Zoho CRM platform", url: "zoho.com/crm", pricing: "Freemium", rating: 4.3, tags: ["affordable", "india", "suite"]},
    {name: "Pipedrive", category: "CRM", subcategory: "Sales", desc: "Sales-focused CRM", url: "pipedrive.com", pricing: "Paid", rating: 4.4, tags: ["sales", "pipeline", "visual"]},
    {name: "Freshsales", category: "CRM", subcategory: "Sales", desc: "Freshworks CRM", url: "freshworks.com/crm/sales", pricing: "Freemium", rating: 4.3, tags: ["freshworks", "ai", "sales"]},
    {name: "Close", category: "CRM", subcategory: "Sales", desc: "Sales CRM", url: "close.com", pricing: "Paid", rating: 4.4, tags: ["sales", "calling", "smb"]},
    {name: "Copper", category: "CRM", subcategory: "Google", desc: "Google Workspace CRM", url: "copper.com", pricing: "Paid", rating: 4.2, tags: ["google", "workspace", "integration"]},
    {name: "Insightly", category: "CRM", subcategory: "SMB", desc: "SMB CRM", url: "insightly.com", pricing: "Freemium", rating: 4.1, tags: ["smb", "project", "marketing"]},
    {name: "Monday CRM", category: "CRM", subcategory: "Work OS", desc: "CRM on Monday", url: "monday.com/crm", pricing: "Paid", rating: 4.3, tags: ["work-os", "visual", "customizable"]},
    {name: "Capsule", category: "CRM", subcategory: "Simple", desc: "Simple CRM", url: "capsulecrm.com", pricing: "Freemium", rating: 4.2, tags: ["simple", "contacts", "tasks"]},
    {name: "Nutshell", category: "CRM", subcategory: "SMB", desc: "SMB CRM & sales", url: "nutshell.com", pricing: "Paid", rating: 4.2, tags: ["smb", "sales", "marketing"]},
    {name: "Less Annoying CRM", category: "CRM", subcategory: "Simple", desc: "Simple CRM", url: "lessannoyingcrm.com", pricing: "Paid", rating: 4.4, tags: ["simple", "affordable", "small-business"]},
    {name: "Streak", category: "CRM", subcategory: "Gmail", desc: "CRM in Gmail", url: "streak.com", pricing: "Freemium", rating: 4.2, tags: ["gmail", "inbox", "integration"]},
    {name: "Nimble", category: "CRM", subcategory: "Social", desc: "Social CRM", url: "nimble.com", pricing: "Paid", rating: 4.1, tags: ["social", "contacts", "enrichment"]},
    {name: "Zendesk Sell", category: "CRM", subcategory: "Sales", desc: "Zendesk sales CRM", url: "zendesk.com/sell", pricing: "Paid", rating: 4.1, tags: ["zendesk", "sales", "support"]},
    
    // ==================== SALES INTELLIGENCE ====================
    {name: "ZoomInfo", category: "Sales", subcategory: "Intelligence", desc: "B2B database", url: "zoominfo.com", pricing: "Paid", rating: 4.3, tags: ["data", "prospecting", "enterprise"], featured: true},
    {name: "Apollo.io", category: "Sales", subcategory: "Intelligence", desc: "Sales intelligence", url: "apollo.io", pricing: "Freemium", rating: 4.4, tags: ["data", "outreach", "engagement"]},
    {name: "LinkedIn Sales Navigator", category: "Sales", subcategory: "Prospecting", desc: "LinkedIn sales", url: "linkedin.com/sales", pricing: "Paid", rating: 4.3, tags: ["linkedin", "prospecting", "social"]},
    {name: "Clearbit", category: "Sales", subcategory: "Enrichment", desc: "Data enrichment", url: "clearbit.com", pricing: "Paid", rating: 4.3, tags: ["enrichment", "data", "api"]},
    {name: "Lusha", category: "Sales", subcategory: "Data", desc: "Contact data", url: "lusha.com", pricing: "Freemium", rating: 4.2, tags: ["contacts", "data", "extension"]},
    {name: "LeadIQ", category: "Sales", subcategory: "Prospecting", desc: "Prospecting platform", url: "leadiq.com", pricing: "Freemium", rating: 4.2, tags: ["prospecting", "data", "salesforce"]},
    {name: "Cognism", category: "Sales", subcategory: "Intelligence", desc: "Sales intelligence", url: "cognism.com", pricing: "Paid", rating: 4.2, tags: ["data", "compliance", "europe"]},
    {name: "Seamless.AI", category: "Sales", subcategory: "Data", desc: "Contact finding", url: "seamless.ai", pricing: "Freemium", rating: 4.0, tags: ["contacts", "ai", "real-time"]},
    {name: "Hunter.io", category: "Sales", subcategory: "Email Finding", desc: "Email finder", url: "hunter.io", pricing: "Freemium", rating: 4.4, tags: ["email", "finding", "verification"]},
    {name: "Snov.io", category: "Sales", subcategory: "Outreach", desc: "Sales automation", url: "snov.io", pricing: "Freemium", rating: 4.2, tags: ["email", "finding", "automation"]},
    {name: "RocketReach", category: "Sales", subcategory: "Data", desc: "Contact data", url: "rocketreach.co", pricing: "Paid", rating: 4.1, tags: ["contacts", "data", "api"]},
    {name: "FullContact", category: "Sales", subcategory: "Enrichment", desc: "Identity resolution", url: "fullcontact.com", pricing: "Paid", rating: 4.0, tags: ["identity", "enrichment", "api"]},
    {name: "Datanyze", category: "Sales", subcategory: "Technographics", desc: "Tech data", url: "datanyze.com", pricing: "Paid", rating: 4.0, tags: ["technographics", "data", "zoominfo"]},
    
    // ==================== SALES ENGAGEMENT ====================
    {name: "Outreach", category: "Sales", subcategory: "Engagement", desc: "Sales engagement", url: "outreach.io", pricing: "Paid", rating: 4.4, tags: ["engagement", "sequences", "enterprise"], featured: true},
    {name: "Salesloft", category: "Sales", subcategory: "Engagement", desc: "Revenue platform", url: "salesloft.com", pricing: "Paid", rating: 4.4, tags: ["engagement", "cadences", "enterprise"]},
    {name: "Gong", category: "Sales", subcategory: "Intelligence", desc: "Revenue intelligence", url: "gong.io", pricing: "Paid", rating: 4.5, tags: ["conversation", "ai", "coaching"]},
    {name: "Chorus.ai", category: "Sales", subcategory: "Intelligence", desc: "Conversation intelligence", url: "chorus.ai", pricing: "Paid", rating: 4.3, tags: ["conversation", "zoominfo", "coaching"]},
    {name: "Clari", category: "Sales", subcategory: "Revenue", desc: "Revenue platform", url: "clari.com", pricing: "Paid", rating: 4.3, tags: ["revenue", "forecasting", "ai"]},
    {name: "People.ai", category: "Sales", subcategory: "Intelligence", desc: "Revenue intelligence", url: "people.ai", pricing: "Paid", rating: 4.1, tags: ["revenue", "ai", "activity"]},
    {name: "Groove", category: "Sales", subcategory: "Engagement", desc: "Sales engagement", url: "groove.co", pricing: "Paid", rating: 4.2, tags: ["engagement", "clari", "salesforce"]},
    {name: "Mixmax", category: "Sales", subcategory: "Email", desc: "Sales email", url: "mixmax.com", pricing: "Freemium", rating: 4.2, tags: ["email", "scheduling", "sequences"]},
    {name: "Yesware", category: "Sales", subcategory: "Email", desc: "Email tracking", url: "yesware.com", pricing: "Freemium", rating: 4.1, tags: ["email", "tracking", "templates"]},
    {name: "PersistIQ", category: "Sales", subcategory: "Outreach", desc: "Sales outreach", url: "persistiq.com", pricing: "Paid", rating: 4.0, tags: ["outreach", "sequences", "simple"]},
    
    // ==================== PROPOSAL & CPQ ====================
    {name: "PandaDoc", category: "Sales", subcategory: "Proposals", desc: "Document automation", url: "pandadoc.com", pricing: "Freemium", rating: 4.4, tags: ["proposals", "contracts", "esign"], featured: true},
    {name: "Proposify", category: "Sales", subcategory: "Proposals", desc: "Proposal software", url: "proposify.com", pricing: "Paid", rating: 4.3, tags: ["proposals", "design", "tracking"]},
    {name: "DocuSign", category: "Sales", subcategory: "E-Signature", desc: "Electronic signatures", url: "docusign.com", pricing: "Paid", rating: 4.5, tags: ["esign", "contracts", "enterprise"]},
    {name: "HelloSign", category: "Sales", subcategory: "E-Signature", desc: "E-signatures", url: "hellosign.com", pricing: "Freemium", rating: 4.4, tags: ["esign", "dropbox", "simple"]},
    {name: "SignNow", category: "Sales", subcategory: "E-Signature", desc: "E-signature solution", url: "signnow.com", pricing: "Paid", rating: 4.2, tags: ["esign", "affordable", "airslate"]},
    {name: "Salesforce CPQ", category: "Sales", subcategory: "CPQ", desc: "Configure price quote", url: "salesforce.com/cpq", pricing: "Paid", rating: 4.1, tags: ["cpq", "salesforce", "quotes"]},
    {name: "DealHub", category: "Sales", subcategory: "CPQ", desc: "Revenue platform", url: "dealhub.io", pricing: "Paid", rating: 4.2, tags: ["cpq", "proposals", "clm"]},
    {name: "Conga", category: "Sales", subcategory: "CLM", desc: "Revenue lifecycle", url: "conga.com", pricing: "Paid", rating: 4.0, tags: ["clm", "cpq", "apttus"]},
    {name: "Qwilr", category: "Sales", subcategory: "Proposals", desc: "Web proposals", url: "qwilr.com", pricing: "Paid", rating: 4.3, tags: ["proposals", "web", "interactive"]},
    {name: "Better Proposals", category: "Sales", subcategory: "Proposals", desc: "Proposal software", url: "betterproposals.io", pricing: "Paid", rating: 4.3, tags: ["proposals", "templates", "tracking"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE65 = AI_TOOLS_PHASE65;
}


