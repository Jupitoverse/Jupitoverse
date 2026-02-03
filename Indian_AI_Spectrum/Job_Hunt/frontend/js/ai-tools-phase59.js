// AI Tools Database - Phase 59: Government & Civic Tech
// 100+ Government and civic technology tools

const AI_TOOLS_PHASE59 = [
    // ==================== E-GOVERNMENT ====================
    {name: "Salesforce Government", category: "GovTech", subcategory: "CRM", desc: "Government CRM", url: "salesforce.com/government", pricing: "Paid", rating: 4.3, tags: ["crm", "government", "fedramp"], featured: true},
    {name: "ServiceNow Gov", category: "GovTech", subcategory: "Workflow", desc: "Government workflows", url: "servicenow.com/gov", pricing: "Paid", rating: 4.3, tags: ["workflow", "it", "government"]},
    {name: "Tyler Technologies", category: "GovTech", subcategory: "Software", desc: "Government software", url: "tylertech.com", pricing: "Paid", rating: 4.1, tags: ["local-gov", "courts", "public-safety"]},
    {name: "Accela", category: "GovTech", subcategory: "Permitting", desc: "Civic applications", url: "accela.com", pricing: "Paid", rating: 4.0, tags: ["permitting", "licensing", "civic"]},
    {name: "OpenGov", category: "GovTech", subcategory: "Budgeting", desc: "Government budgeting", url: "opengov.com", pricing: "Paid", rating: 4.2, tags: ["budgeting", "reporting", "transparency"]},
    {name: "Granicus", category: "GovTech", subcategory: "Communications", desc: "Government comms", url: "granicus.com", pricing: "Paid", rating: 4.1, tags: ["communications", "meetings", "digital"]},
    {name: "Socrata", category: "GovTech", subcategory: "Data", desc: "Open data platform", url: "socrata.com", pricing: "Paid", rating: 4.2, tags: ["open-data", "tyler", "analytics"]},
    {name: "CivicPlus", category: "GovTech", subcategory: "Websites", desc: "Government websites", url: "civicplus.com", pricing: "Paid", rating: 4.0, tags: ["websites", "cms", "local-gov"]},
    {name: "Munis (Tyler)", category: "GovTech", subcategory: "ERP", desc: "Government ERP", url: "tylertech.com/munis", pricing: "Paid", rating: 4.0, tags: ["erp", "financials", "local-gov"]},
    {name: "Cityworks", category: "GovTech", subcategory: "Asset", desc: "Asset management", url: "cityworks.com", pricing: "Paid", rating: 4.1, tags: ["assets", "gis", "infrastructure"]},
    
    // ==================== CIVIC ENGAGEMENT ====================
    {name: "SeeClickFix", category: "GovTech", subcategory: "311", desc: "311 platform", url: "seeclickfix.com", pricing: "Paid", rating: 4.3, tags: ["311", "requests", "civic"], featured: true},
    {name: "Bang the Table", category: "GovTech", subcategory: "Engagement", desc: "Community engagement", url: "bangthetable.com", pricing: "Paid", rating: 4.2, tags: ["engagement", "consultation", "granicus"]},
    {name: "Pol.is", category: "GovTech", subcategory: "Engagement", desc: "Opinion gathering", url: "pol.is", pricing: "Freemium", rating: 4.3, tags: ["opinion", "consensus", "ai"]},
    {name: "Decidim", category: "GovTech", subcategory: "Participation", desc: "Participatory platform", url: "decidim.org", pricing: "Free", rating: 4.4, tags: ["participatory", "open-source", "barcelona"]},
    {name: "Consul", category: "GovTech", subcategory: "Participation", desc: "Citizen participation", url: "consulproject.org", pricing: "Free", rating: 4.2, tags: ["participation", "open-source", "madrid"]},
    {name: "Balancing Act", category: "GovTech", subcategory: "Budgeting", desc: "Budget simulations", url: "abalancingact.com", pricing: "Paid", rating: 4.1, tags: ["budget", "simulation", "engagement"]},
    {name: "PublicInput", category: "GovTech", subcategory: "Engagement", desc: "Public input platform", url: "publicinput.com", pricing: "Paid", rating: 4.0, tags: ["input", "meetings", "surveys"]},
    {name: "Cityflag", category: "GovTech", subcategory: "Mobile", desc: "Citizen reporting", url: "cityflag.com", pricing: "Paid", rating: 3.9, tags: ["reporting", "mobile", "issues"]},
    {name: "PublicStuff", category: "GovTech", subcategory: "311", desc: "311 requests", url: "publicstuff.com", pricing: "Paid", rating: 4.0, tags: ["311", "accela", "requests"]},
    {name: "Zencity", category: "GovTech", subcategory: "Analytics", desc: "Community insights", url: "zencity.io", pricing: "Paid", rating: 4.2, tags: ["insights", "ai", "sentiment"]},
    
    // ==================== VOTING & ELECTIONS ====================
    {name: "Democracy Works", category: "GovTech", subcategory: "Voting", desc: "Voting access", url: "democracy.works", pricing: "Freemium", rating: 4.4, tags: ["voting", "access", "registration"], featured: true},
    {name: "Vote.org", category: "GovTech", subcategory: "Voting", desc: "Voter registration", url: "vote.org", pricing: "Free", rating: 4.5, tags: ["registration", "nonpartisan", "access"]},
    {name: "BallotReady", category: "GovTech", subcategory: "Ballot", desc: "Ballot information", url: "ballotready.org", pricing: "Freemium", rating: 4.3, tags: ["ballot", "candidates", "information"]},
    {name: "VoteSmart", category: "GovTech", subcategory: "Research", desc: "Political research", url: "votesmart.org", pricing: "Free", rating: 4.2, tags: ["research", "candidates", "voting-records"]},
    {name: "ElectionGuard", category: "GovTech", subcategory: "Security", desc: "Election security", url: "electionguard.vote", pricing: "Free", rating: 4.3, tags: ["security", "microsoft", "verification"]},
    {name: "Clear Ballot", category: "GovTech", subcategory: "Voting Systems", desc: "Election technology", url: "clearballot.com", pricing: "Paid", rating: 4.1, tags: ["voting-systems", "audit", "transparent"]},
    {name: "Hart InterCivic", category: "GovTech", subcategory: "Voting Systems", desc: "Voting equipment", url: "hartintercivic.com", pricing: "Paid", rating: 4.0, tags: ["voting", "equipment", "elections"]},
    {name: "ES&S", category: "GovTech", subcategory: "Voting Systems", desc: "Election systems", url: "essvote.com", pricing: "Paid", rating: 3.9, tags: ["voting-systems", "hardware", "software"]},
    
    // ==================== PUBLIC SAFETY ====================
    {name: "Axon", category: "GovTech", subcategory: "Public Safety", desc: "Police technology", url: "axon.com", pricing: "Paid", rating: 4.3, tags: ["police", "body-cameras", "tasers"], featured: true},
    {name: "Motorola Solutions", category: "GovTech", subcategory: "Communications", desc: "Public safety comms", url: "motorolasolutions.com", pricing: "Paid", rating: 4.2, tags: ["radio", "911", "command"]},
    {name: "Tyler New World", category: "GovTech", subcategory: "CAD", desc: "CAD/RMS", url: "tylertech.com/new-world", pricing: "Paid", rating: 4.1, tags: ["cad", "rms", "public-safety"]},
    {name: "Mark43", category: "GovTech", subcategory: "RMS", desc: "Modern RMS", url: "mark43.com", pricing: "Paid", rating: 4.2, tags: ["rms", "modern", "cloud"]},
    {name: "RapidSOS", category: "GovTech", subcategory: "911", desc: "911 data platform", url: "rapidsos.com", pricing: "Paid", rating: 4.4, tags: ["911", "data", "location"]},
    {name: "Rave Mobile Safety", category: "GovTech", subcategory: "Alerts", desc: "Mass notification", url: "ravemobilesafety.com", pricing: "Paid", rating: 4.2, tags: ["alerts", "notification", "motorola"]},
    {name: "Everbridge", category: "GovTech", subcategory: "Alerts", desc: "Critical event mgmt", url: "everbridge.com", pricing: "Paid", rating: 4.2, tags: ["alerts", "crisis", "management"]},
    {name: "ShotSpotter", category: "GovTech", subcategory: "Gunshot", desc: "Gunshot detection", url: "shotspotter.com", pricing: "Paid", rating: 3.8, tags: ["gunshot", "detection", "police"]},
    {name: "Flock Safety", category: "GovTech", subcategory: "License Plate", desc: "LPR cameras", url: "flocksafety.com", pricing: "Paid", rating: 4.1, tags: ["lpr", "cameras", "community"]},
    {name: "Ring Neighbors", category: "GovTech", subcategory: "Community", desc: "Community safety", url: "ring.com/neighbors", pricing: "Free", rating: 4.0, tags: ["community", "amazon", "doorbell"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE59 = AI_TOOLS_PHASE59;
}


