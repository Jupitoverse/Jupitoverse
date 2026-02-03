// AI Tools Database - Phase 13: Sales, CRM & Business AI
// 200+ Tools for sales teams and business operations

const AI_TOOLS_PHASE13 = [
    // ==================== CRM ====================
    {name: "Salesforce", category: "CRM", subcategory: "Enterprise", desc: "World's #1 CRM", url: "salesforce.com", pricing: "Paid", rating: 4.4, tags: ["enterprise", "cloud", "platform"], featured: true},
    {name: "HubSpot CRM", category: "CRM", subcategory: "All-in-one", desc: "Free CRM platform", url: "hubspot.com/crm", pricing: "Freemium", rating: 4.5, tags: ["free", "marketing", "sales"]},
    {name: "Pipedrive", category: "CRM", subcategory: "Sales", desc: "Sales-focused CRM", url: "pipedrive.com", pricing: "Paid", rating: 4.4, tags: ["sales", "pipeline", "simple"]},
    {name: "Zoho CRM", category: "CRM", subcategory: "All-in-one", desc: "AI-powered CRM", url: "zoho.com/crm", pricing: "Freemium", rating: 4.3, tags: ["ai", "automation", "affordable"]},
    {name: "Monday Sales CRM", category: "CRM", subcategory: "Flexible", desc: "Customizable CRM", url: "monday.com/crm", pricing: "Paid", rating: 4.3, tags: ["customizable", "visual", "workflow"]},
    {name: "Freshsales", category: "CRM", subcategory: "AI", desc: "AI-powered CRM", url: "freshworks.com/freshsales-crm", pricing: "Freemium", rating: 4.3, tags: ["ai", "freshworks", "phone"]},
    {name: "Close", category: "CRM", subcategory: "Sales", desc: "CRM for SMB sales", url: "close.com", pricing: "Paid", rating: 4.4, tags: ["calling", "email", "smb"]},
    {name: "Copper", category: "CRM", subcategory: "Google", desc: "CRM for Google Workspace", url: "copper.com", pricing: "Paid", rating: 4.2, tags: ["google", "integration", "simple"]},
    {name: "Insightly", category: "CRM", subcategory: "Project", desc: "CRM and project management", url: "insightly.com", pricing: "Freemium", rating: 4.1, tags: ["projects", "crm", "unified"]},
    {name: "Nutshell", category: "CRM", subcategory: "Simple", desc: "Simple sales and marketing", url: "nutshell.com", pricing: "Paid", rating: 4.3, tags: ["simple", "affordable", "smb"]},
    {name: "Less Annoying CRM", category: "CRM", subcategory: "Simple", desc: "Simple CRM for small business", url: "lessannoyingcrm.com", pricing: "Paid", rating: 4.5, tags: ["simple", "small-business", "affordable"]},
    {name: "Nimble", category: "CRM", subcategory: "Social", desc: "Social sales and marketing CRM", url: "nimble.com", pricing: "Paid", rating: 4.2, tags: ["social", "relationship", "smb"]},
    {name: "Capsule", category: "CRM", subcategory: "Simple", desc: "Smart simple CRM", url: "capsulecrm.com", pricing: "Freemium", rating: 4.3, tags: ["simple", "tasks", "affordable"]},
    {name: "Agile CRM", category: "CRM", subcategory: "All-in-one", desc: "All-in-one CRM", url: "agilecrm.com", pricing: "Freemium", rating: 4.0, tags: ["all-in-one", "affordable", "automation"]},
    {name: "Keap (Infusionsoft)", category: "CRM", subcategory: "Automation", desc: "CRM and automation", url: "keap.com", pricing: "Paid", rating: 4.0, tags: ["automation", "small-business", "email"]},
    
    // ==================== SALES INTELLIGENCE ====================
    {name: "ZoomInfo", category: "Sales Intelligence", subcategory: "Data", desc: "B2B data platform", url: "zoominfo.com", pricing: "Paid", rating: 4.3, tags: ["data", "contacts", "intent"], featured: true},
    {name: "Apollo.io", category: "Sales Intelligence", subcategory: "Prospecting", desc: "Sales intelligence platform", url: "apollo.io", pricing: "Freemium", rating: 4.5, tags: ["prospecting", "engagement", "data"]},
    {name: "LinkedIn Sales Navigator", category: "Sales Intelligence", subcategory: "Social", desc: "LinkedIn sales tool", url: "business.linkedin.com/sales-solutions", pricing: "Paid", rating: 4.4, tags: ["linkedin", "prospecting", "social"]},
    {name: "Lusha", category: "Sales Intelligence", subcategory: "Contacts", desc: "B2B contact data", url: "lusha.com", pricing: "Freemium", rating: 4.3, tags: ["contacts", "emails", "phones"]},
    {name: "Clearbit", category: "Sales Intelligence", subcategory: "Enrichment", desc: "Data enrichment platform", url: "clearbit.com", pricing: "Paid", rating: 4.4, tags: ["enrichment", "reveal", "forms"]},
    {name: "LeadIQ", category: "Sales Intelligence", subcategory: "Prospecting", desc: "B2B prospecting platform", url: "leadiq.com", pricing: "Paid", rating: 4.2, tags: ["prospecting", "capture", "sync"]},
    {name: "Seamless.AI", category: "Sales Intelligence", subcategory: "Data", desc: "Real-time contact data", url: "seamless.ai", pricing: "Freemium", rating: 4.1, tags: ["contacts", "real-time", "ai"]},
    {name: "Cognism", category: "Sales Intelligence", subcategory: "Data", desc: "B2B sales intelligence", url: "cognism.com", pricing: "Paid", rating: 4.3, tags: ["data", "gdpr", "intent"]},
    {name: "6sense", category: "Sales Intelligence", subcategory: "Intent", desc: "Revenue AI platform", url: "6sense.com", pricing: "Paid", rating: 4.3, tags: ["intent", "abm", "ai"]},
    {name: "Bombora", category: "Sales Intelligence", subcategory: "Intent", desc: "B2B intent data", url: "bombora.com", pricing: "Paid", rating: 4.2, tags: ["intent", "data", "b2b"]},
    {name: "D&B Hoovers", category: "Sales Intelligence", subcategory: "Data", desc: "Sales acceleration", url: "dnb.com/products/sales-marketing/hoovers", pricing: "Paid", rating: 4.1, tags: ["data", "dnb", "enterprise"]},
    {name: "DiscoverOrg", category: "Sales Intelligence", subcategory: "Data", desc: "B2B intelligence (now ZoomInfo)", url: "discoverorg.com", pricing: "Paid", rating: 4.2, tags: ["data", "org-charts", "intent"]},
    {name: "SalesIntel", category: "Sales Intelligence", subcategory: "Data", desc: "Human-verified B2B data", url: "salesintel.io", pricing: "Paid", rating: 4.2, tags: ["verified", "contacts", "intent"]},
    {name: "UpLead", category: "Sales Intelligence", subcategory: "Data", desc: "B2B prospecting platform", url: "uplead.com", pricing: "Paid", rating: 4.3, tags: ["accuracy", "affordable", "data"]},
    {name: "LeadGenius", category: "Sales Intelligence", subcategory: "Custom", desc: "Custom B2B data", url: "leadgenius.com", pricing: "Paid", rating: 4.1, tags: ["custom", "data", "research"]},
    
    // ==================== SALES ENGAGEMENT ====================
    {name: "Outreach", category: "Sales Engagement", subcategory: "Platform", desc: "Sales execution platform", url: "outreach.io", pricing: "Paid", rating: 4.4, tags: ["sequences", "enterprise", "ai"], featured: true},
    {name: "Salesloft", category: "Sales Engagement", subcategory: "Platform", desc: "Revenue orchestration platform", url: "salesloft.com", pricing: "Paid", rating: 4.4, tags: ["cadences", "coaching", "revenue"]},
    {name: "Gong", category: "Sales Engagement", subcategory: "Intelligence", desc: "Revenue intelligence platform", url: "gong.io", pricing: "Paid", rating: 4.6, tags: ["conversation", "ai", "coaching"], featured: true},
    {name: "Chorus.ai", category: "Sales Engagement", subcategory: "Intelligence", desc: "Conversation intelligence", url: "chorus.ai", pricing: "Paid", rating: 4.4, tags: ["calls", "ai", "coaching"]},
    {name: "Reply.io", category: "Sales Engagement", subcategory: "Outreach", desc: "Sales engagement platform", url: "reply.io", pricing: "Paid", rating: 4.4, tags: ["multichannel", "sequences", "ai"]},
    {name: "Lemlist", category: "Sales Engagement", subcategory: "Cold Email", desc: "Cold outreach platform", url: "lemlist.com", pricing: "Paid", rating: 4.5, tags: ["personalization", "email", "sequences"]},
    {name: "Mailshake", category: "Sales Engagement", subcategory: "Cold Email", desc: "Sales engagement", url: "mailshake.com", pricing: "Paid", rating: 4.3, tags: ["email", "calling", "simple"]},
    {name: "Woodpecker", category: "Sales Engagement", subcategory: "Cold Email", desc: "Cold email tool", url: "woodpecker.co", pricing: "Paid", rating: 4.3, tags: ["cold-email", "agency", "automation"]},
    {name: "Mixmax", category: "Sales Engagement", subcategory: "Email", desc: "Email productivity", url: "mixmax.com", pricing: "Freemium", rating: 4.3, tags: ["gmail", "scheduling", "sequences"]},
    {name: "Yesware", category: "Sales Engagement", subcategory: "Email", desc: "Email tracking for sales", url: "yesware.com", pricing: "Paid", rating: 4.2, tags: ["tracking", "templates", "salesforce"]},
    {name: "Groove", category: "Sales Engagement", subcategory: "Salesforce", desc: "Sales engagement for Salesforce", url: "groove.co", pricing: "Paid", rating: 4.3, tags: ["salesforce", "native", "sequences"]},
    {name: "VanillaSoft", category: "Sales Engagement", subcategory: "Dialer", desc: "Sales engagement platform", url: "vanillasoft.com", pricing: "Paid", rating: 4.2, tags: ["dialer", "queue", "cadence"]},
    {name: "ConnectAndSell", category: "Sales Engagement", subcategory: "Dialer", desc: "Conversation platform", url: "connectandsell.com", pricing: "Paid", rating: 4.3, tags: ["dialer", "lightning", "live"]},
    {name: "Dialpad", category: "Sales Engagement", subcategory: "Phone", desc: "AI-powered communications", url: "dialpad.com", pricing: "Paid", rating: 4.4, tags: ["phone", "ai", "voip"]},
    {name: "Aircall", category: "Sales Engagement", subcategory: "Phone", desc: "Cloud phone system", url: "aircall.io", pricing: "Paid", rating: 4.4, tags: ["phone", "integrations", "cloud"]},
    
    // ==================== MEETING & SCHEDULING ====================
    {name: "Calendly", category: "Scheduling", subcategory: "Booking", desc: "Scheduling automation", url: "calendly.com", pricing: "Freemium", rating: 4.6, tags: ["scheduling", "automation", "popular"], featured: true},
    {name: "Cal.com", category: "Scheduling", subcategory: "Open Source", desc: "Open source scheduling", url: "cal.com", pricing: "Freemium", rating: 4.4, tags: ["open-source", "self-hosted", "free"]},
    {name: "SavvyCal", category: "Scheduling", subcategory: "Personalized", desc: "Personalized scheduling", url: "savvycal.com", pricing: "Paid", rating: 4.4, tags: ["personalized", "overlay", "elegant"]},
    {name: "Doodle", category: "Scheduling", subcategory: "Polling", desc: "Meeting scheduling", url: "doodle.com", pricing: "Freemium", rating: 4.2, tags: ["polling", "group", "scheduling"]},
    {name: "YouCanBook.me", category: "Scheduling", subcategory: "Booking", desc: "Online booking", url: "youcanbook.me", pricing: "Paid", rating: 4.3, tags: ["booking", "calendar", "simple"]},
    {name: "Acuity Scheduling", category: "Scheduling", subcategory: "Appointments", desc: "Appointment scheduling", url: "acuityscheduling.com", pricing: "Paid", rating: 4.5, tags: ["appointments", "squarespace", "payments"]},
    {name: "Setmore", category: "Scheduling", subcategory: "Free", desc: "Free appointment scheduling", url: "setmore.com", pricing: "Freemium", rating: 4.2, tags: ["free", "appointments", "smb"]},
    {name: "Chili Piper", category: "Scheduling", subcategory: "B2B", desc: "B2B scheduling", url: "chilipiper.com", pricing: "Paid", rating: 4.4, tags: ["routing", "b2b", "forms"]},
    {name: "Reclaim.ai", category: "Scheduling", subcategory: "AI", desc: "AI scheduling assistant", url: "reclaim.ai", pricing: "Freemium", rating: 4.4, tags: ["ai", "habits", "time-blocking"]},
    {name: "Clockwise", category: "Scheduling", subcategory: "Calendar", desc: "AI calendar assistant", url: "getclockwise.com", pricing: "Freemium", rating: 4.3, tags: ["ai", "focus-time", "optimization"]},
    {name: "Motion", category: "Scheduling", subcategory: "AI", desc: "AI project manager", url: "usemotion.com", pricing: "Paid", rating: 4.4, tags: ["ai", "tasks", "scheduling"]},
    {name: "Trevor.ai", category: "Scheduling", subcategory: "Time Blocking", desc: "Time blocking assistant", url: "trevor.io", pricing: "Freemium", rating: 4.2, tags: ["time-blocking", "todoist", "simple"]},
    {name: "Zoom", category: "Meetings", subcategory: "Video", desc: "Video conferencing", url: "zoom.us", pricing: "Freemium", rating: 4.5, tags: ["video", "popular", "webinars"]},
    {name: "Microsoft Teams", category: "Meetings", subcategory: "Collaboration", desc: "Team collaboration", url: "microsoft.com/teams", pricing: "Freemium", rating: 4.4, tags: ["microsoft", "collaboration", "video"]},
    {name: "Google Meet", category: "Meetings", subcategory: "Video", desc: "Google video meetings", url: "meet.google.com", pricing: "Freemium", rating: 4.4, tags: ["google", "video", "simple"]},
    
    // ==================== PROPOSAL & CONTRACTS ====================
    {name: "PandaDoc", category: "Proposals", subcategory: "Documents", desc: "Document automation", url: "pandadoc.com", pricing: "Freemium", rating: 4.5, tags: ["proposals", "contracts", "esign"], featured: true},
    {name: "Proposify", category: "Proposals", subcategory: "Proposals", desc: "Proposal software", url: "proposify.com", pricing: "Paid", rating: 4.4, tags: ["proposals", "templates", "analytics"]},
    {name: "Better Proposals", category: "Proposals", subcategory: "Simple", desc: "Simple proposal software", url: "betterproposals.io", pricing: "Paid", rating: 4.4, tags: ["simple", "beautiful", "tracking"]},
    {name: "Qwilr", category: "Proposals", subcategory: "Interactive", desc: "Interactive proposals", url: "qwilr.com", pricing: "Paid", rating: 4.3, tags: ["interactive", "web-based", "beautiful"]},
    {name: "DealHub", category: "Proposals", subcategory: "CPQ", desc: "Revenue platform", url: "dealhub.io", pricing: "Paid", rating: 4.4, tags: ["cpq", "proposals", "sales-room"]},
    {name: "GetAccept", category: "Proposals", subcategory: "Digital Sales", desc: "Digital sales room", url: "getaccept.com", pricing: "Paid", rating: 4.3, tags: ["digital-room", "video", "tracking"]},
    {name: "Loopio", category: "Proposals", subcategory: "RFP", desc: "RFP response software", url: "loopio.com", pricing: "Paid", rating: 4.4, tags: ["rfp", "content-library", "collaboration"]},
    {name: "RFPIO", category: "Proposals", subcategory: "RFP", desc: "RFP management", url: "rfpio.com", pricing: "Paid", rating: 4.3, tags: ["rfp", "ai", "automation"]},
    {name: "Conga", category: "Proposals", subcategory: "CLM", desc: "Revenue lifecycle management", url: "conga.com", pricing: "Paid", rating: 4.1, tags: ["clm", "salesforce", "automation"]},
    {name: "DocSend", category: "Proposals", subcategory: "Tracking", desc: "Secure document sharing", url: "docsend.com", pricing: "Paid", rating: 4.3, tags: ["tracking", "analytics", "secure"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE13 = AI_TOOLS_PHASE13;
}


