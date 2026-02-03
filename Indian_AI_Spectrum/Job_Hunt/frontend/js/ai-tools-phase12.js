// AI Tools Database - Phase 12: Marketing, Advertising & SEO AI
// 200+ Tools for marketers

const AI_TOOLS_PHASE12 = [
    // ==================== SOCIAL MEDIA ====================
    {name: "Buffer", category: "Social Media", subcategory: "Scheduling", desc: "Social media scheduling", url: "buffer.com", pricing: "Freemium", rating: 4.5, tags: ["scheduling", "analytics", "engagement"], featured: true},
    {name: "Hootsuite", category: "Social Media", subcategory: "Management", desc: "Social media management", url: "hootsuite.com", pricing: "Paid", rating: 4.3, tags: ["management", "enterprise", "analytics"]},
    {name: "Sprout Social", category: "Social Media", subcategory: "Management", desc: "Social management platform", url: "sproutsocial.com", pricing: "Paid", rating: 4.4, tags: ["management", "analytics", "listening"]},
    {name: "Later", category: "Social Media", subcategory: "Visual", desc: "Visual social media planner", url: "later.com", pricing: "Freemium", rating: 4.4, tags: ["instagram", "visual", "scheduling"]},
    {name: "Planoly", category: "Social Media", subcategory: "Instagram", desc: "Instagram planner", url: "planoly.com", pricing: "Freemium", rating: 4.3, tags: ["instagram", "visual", "planning"]},
    {name: "SocialBee", category: "Social Media", subcategory: "Automation", desc: "Social media automation", url: "socialbee.io", pricing: "Paid", rating: 4.4, tags: ["automation", "categories", "recycling"]},
    {name: "MeetEdgar", category: "Social Media", subcategory: "Automation", desc: "Social media automation", url: "meetedgar.com", pricing: "Paid", rating: 4.2, tags: ["automation", "library", "recycling"]},
    {name: "Tailwind", category: "Social Media", subcategory: "Pinterest", desc: "Pinterest and Instagram tool", url: "tailwindapp.com", pricing: "Paid", rating: 4.3, tags: ["pinterest", "instagram", "scheduling"]},
    {name: "Publer", category: "Social Media", subcategory: "Scheduling", desc: "Social media scheduler", url: "publer.io", pricing: "Freemium", rating: 4.3, tags: ["scheduling", "analytics", "collaboration"]},
    {name: "Sendible", category: "Social Media", subcategory: "Agency", desc: "Social media for agencies", url: "sendible.com", pricing: "Paid", rating: 4.2, tags: ["agency", "management", "white-label"]},
    {name: "Agorapulse", category: "Social Media", subcategory: "Management", desc: "Social media management", url: "agorapulse.com", pricing: "Paid", rating: 4.4, tags: ["inbox", "reporting", "management"]},
    {name: "Loomly", category: "Social Media", subcategory: "Collaboration", desc: "Brand success platform", url: "loomly.com", pricing: "Paid", rating: 4.3, tags: ["collaboration", "approval", "calendar"]},
    {name: "Brandwatch", category: "Social Media", subcategory: "Listening", desc: "Social intelligence", url: "brandwatch.com", pricing: "Paid", rating: 4.3, tags: ["listening", "analytics", "enterprise"]},
    {name: "Sprinklr", category: "Social Media", subcategory: "Enterprise", desc: "Unified CXM platform", url: "sprinklr.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "cxm", "unified"]},
    {name: "Khoros", category: "Social Media", subcategory: "Enterprise", desc: "Customer engagement platform", url: "khoros.com", pricing: "Paid", rating: 4.1, tags: ["enterprise", "community", "care"]},
    
    // ==================== CONTENT MARKETING ====================
    {name: "HubSpot", category: "Marketing", subcategory: "Platform", desc: "Marketing automation platform", url: "hubspot.com", pricing: "Freemium", rating: 4.5, tags: ["crm", "automation", "inbound"], featured: true},
    {name: "Marketo", category: "Marketing", subcategory: "Automation", desc: "Marketing automation by Adobe", url: "marketo.com", pricing: "Paid", rating: 4.2, tags: ["automation", "adobe", "enterprise"]},
    {name: "Mailchimp", category: "Marketing", subcategory: "Email", desc: "Email marketing platform", url: "mailchimp.com", pricing: "Freemium", rating: 4.4, tags: ["email", "automation", "smb"]},
    {name: "ActiveCampaign", category: "Marketing", subcategory: "Automation", desc: "Customer experience automation", url: "activecampaign.com", pricing: "Paid", rating: 4.5, tags: ["automation", "crm", "email"]},
    {name: "ConvertKit", category: "Marketing", subcategory: "Creators", desc: "Creator marketing platform", url: "convertkit.com", pricing: "Freemium", rating: 4.4, tags: ["creators", "email", "landing"]},
    {name: "Klaviyo", category: "Marketing", subcategory: "E-commerce", desc: "E-commerce marketing", url: "klaviyo.com", pricing: "Freemium", rating: 4.5, tags: ["ecommerce", "email", "sms"]},
    {name: "Drip", category: "Marketing", subcategory: "E-commerce", desc: "ECRM for growing brands", url: "drip.com", pricing: "Paid", rating: 4.3, tags: ["ecommerce", "automation", "email"]},
    {name: "Brevo (Sendinblue)", category: "Marketing", subcategory: "Email", desc: "Marketing platform", url: "brevo.com", pricing: "Freemium", rating: 4.3, tags: ["email", "sms", "chat"]},
    {name: "Constant Contact", category: "Marketing", subcategory: "Email", desc: "Email marketing", url: "constantcontact.com", pricing: "Paid", rating: 4.1, tags: ["email", "smb", "templates"]},
    {name: "GetResponse", category: "Marketing", subcategory: "Automation", desc: "Marketing automation", url: "getresponse.com", pricing: "Paid", rating: 4.2, tags: ["email", "webinars", "automation"]},
    {name: "Omnisend", category: "Marketing", subcategory: "E-commerce", desc: "E-commerce marketing", url: "omnisend.com", pricing: "Freemium", rating: 4.4, tags: ["ecommerce", "omnichannel", "automation"]},
    {name: "Moosend", category: "Marketing", subcategory: "Email", desc: "Email marketing platform", url: "moosend.com", pricing: "Paid", rating: 4.3, tags: ["email", "automation", "affordable"]},
    {name: "Customer.io", category: "Marketing", subcategory: "Messaging", desc: "Automated messaging", url: "customer.io", pricing: "Paid", rating: 4.4, tags: ["messaging", "automation", "data"]},
    {name: "Intercom", category: "Marketing", subcategory: "Engagement", desc: "Customer messaging platform", url: "intercom.com", pricing: "Paid", rating: 4.4, tags: ["chat", "support", "engagement"]},
    {name: "Drift", category: "Marketing", subcategory: "Conversational", desc: "Conversational marketing", url: "drift.com", pricing: "Paid", rating: 4.2, tags: ["chat", "bot", "sales"]},
    
    // ==================== SEO TOOLS ====================
    {name: "Ahrefs", category: "SEO", subcategory: "All-in-one", desc: "SEO toolset", url: "ahrefs.com", pricing: "Paid", rating: 4.7, tags: ["backlinks", "keywords", "audit"], featured: true},
    {name: "SEMrush", category: "SEO", subcategory: "All-in-one", desc: "Marketing toolkit", url: "semrush.com", pricing: "Paid", rating: 4.6, tags: ["seo", "ppc", "content"], featured: true},
    {name: "Moz Pro", category: "SEO", subcategory: "All-in-one", desc: "SEO software", url: "moz.com", pricing: "Paid", rating: 4.4, tags: ["seo", "da", "keywords"]},
    {name: "Ubersuggest", category: "SEO", subcategory: "Keywords", desc: "Keyword research tool", url: "neilpatel.com/ubersuggest", pricing: "Freemium", rating: 4.2, tags: ["keywords", "affordable", "neilpatel"]},
    {name: "Mangools", category: "SEO", subcategory: "Suite", desc: "SEO tools suite", url: "mangools.com", pricing: "Paid", rating: 4.4, tags: ["keywords", "serp", "affordable"]},
    {name: "SE Ranking", category: "SEO", subcategory: "All-in-one", desc: "SEO platform", url: "seranking.com", pricing: "Paid", rating: 4.4, tags: ["rank-tracking", "audit", "keywords"]},
    {name: "Serpstat", category: "SEO", subcategory: "All-in-one", desc: "Growth hacking tool", url: "serpstat.com", pricing: "Paid", rating: 4.2, tags: ["seo", "ppc", "analytics"]},
    {name: "Screaming Frog", category: "SEO", subcategory: "Crawler", desc: "SEO spider crawler", url: "screamingfrog.co.uk", pricing: "Freemium", rating: 4.6, tags: ["crawler", "technical", "audit"]},
    {name: "Surfer SEO", category: "SEO", subcategory: "Content", desc: "Content optimization", url: "surferseo.com", pricing: "Paid", rating: 4.5, tags: ["content", "optimization", "nlp"]},
    {name: "Clearscope", category: "SEO", subcategory: "Content", desc: "Content optimization platform", url: "clearscope.io", pricing: "Paid", rating: 4.5, tags: ["content", "optimization", "keywords"]},
    {name: "Frase", category: "SEO", subcategory: "Content", desc: "AI content optimization", url: "frase.io", pricing: "Paid", rating: 4.4, tags: ["ai", "content", "research"]},
    {name: "MarketMuse", category: "SEO", subcategory: "Content", desc: "Content strategy platform", url: "marketmuse.com", pricing: "Paid", rating: 4.3, tags: ["content", "strategy", "ai"]},
    {name: "NeuronWriter", category: "SEO", subcategory: "Content", desc: "NLP content optimization", url: "neuronwriter.com", pricing: "Paid", rating: 4.3, tags: ["nlp", "content", "affordable"]},
    {name: "Linkody", category: "SEO", subcategory: "Backlinks", desc: "Backlink monitoring", url: "linkody.com", pricing: "Paid", rating: 4.1, tags: ["backlinks", "monitoring", "alerts"]},
    {name: "Majestic", category: "SEO", subcategory: "Backlinks", desc: "Link intelligence", url: "majestic.com", pricing: "Paid", rating: 4.3, tags: ["backlinks", "trust-flow", "index"]},
    
    // ==================== ADVERTISING ====================
    {name: "Google Ads", category: "Advertising", subcategory: "Search", desc: "Google advertising platform", url: "ads.google.com", pricing: "Pay-per-click", rating: 4.6, tags: ["ppc", "search", "display"], featured: true},
    {name: "Facebook Ads", category: "Advertising", subcategory: "Social", desc: "Meta advertising", url: "facebook.com/business/ads", pricing: "Pay-per-click", rating: 4.4, tags: ["social", "targeting", "meta"]},
    {name: "LinkedIn Ads", category: "Advertising", subcategory: "B2B", desc: "LinkedIn advertising", url: "business.linkedin.com/marketing-solutions/ads", pricing: "Pay-per-click", rating: 4.2, tags: ["b2b", "professional", "targeting"]},
    {name: "TikTok Ads", category: "Advertising", subcategory: "Social", desc: "TikTok advertising", url: "ads.tiktok.com", pricing: "Pay-per-click", rating: 4.2, tags: ["social", "video", "gen-z"]},
    {name: "AdRoll", category: "Advertising", subcategory: "Retargeting", desc: "Growth marketing platform", url: "adroll.com", pricing: "Paid", rating: 4.1, tags: ["retargeting", "display", "email"]},
    {name: "Criteo", category: "Advertising", subcategory: "Retargeting", desc: "Commerce media platform", url: "criteo.com", pricing: "Paid", rating: 4.0, tags: ["retargeting", "commerce", "display"]},
    {name: "Taboola", category: "Advertising", subcategory: "Native", desc: "Native advertising", url: "taboola.com", pricing: "Pay-per-click", rating: 3.9, tags: ["native", "content", "discovery"]},
    {name: "Outbrain", category: "Advertising", subcategory: "Native", desc: "Content discovery platform", url: "outbrain.com", pricing: "Pay-per-click", rating: 3.9, tags: ["native", "content", "recommendation"]},
    {name: "Wordstream", category: "Advertising", subcategory: "PPC", desc: "PPC management software", url: "wordstream.com", pricing: "Paid", rating: 4.2, tags: ["ppc", "management", "smb"]},
    {name: "Optmyzr", category: "Advertising", subcategory: "PPC", desc: "PPC optimization tool", url: "optmyzr.com", pricing: "Paid", rating: 4.4, tags: ["ppc", "automation", "scripts"]},
    {name: "Adalysis", category: "Advertising", subcategory: "PPC", desc: "PPC analysis tool", url: "adalysis.com", pricing: "Paid", rating: 4.3, tags: ["analysis", "automation", "alerts"]},
    {name: "AdEspresso", category: "Advertising", subcategory: "Social", desc: "Facebook ad optimization", url: "adespresso.com", pricing: "Paid", rating: 4.2, tags: ["facebook", "testing", "optimization"]},
    {name: "Madgicx", category: "Advertising", subcategory: "Meta", desc: "Meta ads optimization", url: "madgicx.com", pricing: "Paid", rating: 4.3, tags: ["meta", "ai", "automation"]},
    {name: "Revealbot", category: "Advertising", subcategory: "Automation", desc: "Ad automation platform", url: "revealbot.com", pricing: "Paid", rating: 4.3, tags: ["automation", "rules", "reporting"]},
    {name: "Triple Whale", category: "Advertising", subcategory: "Analytics", desc: "E-commerce analytics", url: "triplewhale.com", pricing: "Paid", rating: 4.4, tags: ["ecommerce", "attribution", "analytics"]},
    
    // ==================== ANALYTICS ====================
    {name: "Google Analytics", category: "Analytics", subcategory: "Web", desc: "Web analytics by Google", url: "analytics.google.com", pricing: "Free", rating: 4.6, tags: ["web", "free", "google"], featured: true},
    {name: "Mixpanel", category: "Analytics", subcategory: "Product", desc: "Product analytics", url: "mixpanel.com", pricing: "Freemium", rating: 4.5, tags: ["product", "events", "funnels"]},
    {name: "Amplitude", category: "Analytics", subcategory: "Product", desc: "Digital analytics platform", url: "amplitude.com", pricing: "Freemium", rating: 4.5, tags: ["product", "behavioral", "experimentation"]},
    {name: "Heap", category: "Analytics", subcategory: "Product", desc: "Digital insights platform", url: "heap.io", pricing: "Paid", rating: 4.3, tags: ["autocapture", "product", "session"]},
    {name: "Hotjar", category: "Analytics", subcategory: "Behavior", desc: "Heatmaps and recordings", url: "hotjar.com", pricing: "Freemium", rating: 4.5, tags: ["heatmaps", "recordings", "feedback"]},
    {name: "FullStory", category: "Analytics", subcategory: "Experience", desc: "Digital experience intelligence", url: "fullstory.com", pricing: "Paid", rating: 4.4, tags: ["session", "frustration", "dxi"]},
    {name: "Crazy Egg", category: "Analytics", subcategory: "Behavior", desc: "Heatmaps and A/B testing", url: "crazyegg.com", pricing: "Paid", rating: 4.2, tags: ["heatmaps", "scrollmaps", "testing"]},
    {name: "Lucky Orange", category: "Analytics", subcategory: "Behavior", desc: "Conversion optimization", url: "luckyorange.com", pricing: "Paid", rating: 4.3, tags: ["heatmaps", "recordings", "chat"]},
    {name: "Mouseflow", category: "Analytics", subcategory: "Behavior", desc: "Session replay and heatmaps", url: "mouseflow.com", pricing: "Freemium", rating: 4.2, tags: ["replay", "heatmaps", "forms"]},
    {name: "Plausible", category: "Analytics", subcategory: "Privacy", desc: "Privacy-focused analytics", url: "plausible.io", pricing: "Paid", rating: 4.5, tags: ["privacy", "simple", "lightweight"]},
    {name: "Fathom", category: "Analytics", subcategory: "Privacy", desc: "Privacy-first analytics", url: "usefathom.com", pricing: "Paid", rating: 4.5, tags: ["privacy", "simple", "gdpr"]},
    {name: "Matomo", category: "Analytics", subcategory: "Self-hosted", desc: "Open source analytics", url: "matomo.org", pricing: "Freemium", rating: 4.3, tags: ["open-source", "self-hosted", "privacy"]},
    {name: "PostHog", category: "Analytics", subcategory: "Product", desc: "Product analytics suite", url: "posthog.com", pricing: "Freemium", rating: 4.4, tags: ["open-source", "feature-flags", "experiments"]},
    {name: "Segment", category: "Analytics", subcategory: "CDP", desc: "Customer data platform", url: "segment.com", pricing: "Freemium", rating: 4.4, tags: ["cdp", "integration", "twilio"]},
    {name: "mParticle", category: "Analytics", subcategory: "CDP", desc: "Customer data infrastructure", url: "mparticle.com", pricing: "Paid", rating: 4.3, tags: ["cdp", "mobile", "enterprise"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE12 = AI_TOOLS_PHASE12;
}


