// AI Tools Database - Phase 63: More Marketing & Analytics AI
// 150+ Additional marketing and analytics tools

const AI_TOOLS_PHASE63 = [
    // ==================== SEO TOOLS ====================
    {name: "Ahrefs", category: "Marketing", subcategory: "SEO", desc: "SEO toolset", url: "ahrefs.com", pricing: "Paid", rating: 4.7, tags: ["seo", "backlinks", "research"], featured: true},
    {name: "SEMrush", category: "Marketing", subcategory: "SEO", desc: "Marketing toolkit", url: "semrush.com", pricing: "Paid", rating: 4.6, tags: ["seo", "ppc", "content"]},
    {name: "Moz", category: "Marketing", subcategory: "SEO", desc: "SEO software", url: "moz.com", pricing: "Paid", rating: 4.4, tags: ["seo", "da", "keywords"]},
    {name: "Ubersuggest", category: "Marketing", subcategory: "SEO", desc: "SEO tool by Neil Patel", url: "neilpatel.com/ubersuggest", pricing: "Freemium", rating: 4.2, tags: ["seo", "keywords", "free"]},
    {name: "Mangools", category: "Marketing", subcategory: "SEO", desc: "SEO tools bundle", url: "mangools.com", pricing: "Paid", rating: 4.3, tags: ["seo", "kwfinder", "affordable"]},
    {name: "SE Ranking", category: "Marketing", subcategory: "SEO", desc: "SEO platform", url: "seranking.com", pricing: "Paid", rating: 4.3, tags: ["seo", "ranking", "affordable"]},
    {name: "Serpstat", category: "Marketing", subcategory: "SEO", desc: "SEO platform", url: "serpstat.com", pricing: "Paid", rating: 4.2, tags: ["seo", "ppc", "content"]},
    {name: "SpyFu", category: "Marketing", subcategory: "SEO", desc: "Competitor research", url: "spyfu.com", pricing: "Paid", rating: 4.2, tags: ["competitor", "ppc", "seo"]},
    {name: "Majestic", category: "Marketing", subcategory: "Backlinks", desc: "Backlink checker", url: "majestic.com", pricing: "Paid", rating: 4.3, tags: ["backlinks", "trust-flow", "seo"]},
    {name: "Screaming Frog", category: "Marketing", subcategory: "Technical SEO", desc: "SEO spider", url: "screamingfrog.co.uk", pricing: "Freemium", rating: 4.5, tags: ["technical", "crawl", "audit"]},
    {name: "Sitebulb", category: "Marketing", subcategory: "Technical SEO", desc: "Website auditing", url: "sitebulb.com", pricing: "Paid", rating: 4.4, tags: ["audit", "technical", "desktop"]},
    {name: "DeepCrawl (Lumar)", category: "Marketing", subcategory: "Technical SEO", desc: "Website intelligence", url: "lumar.io", pricing: "Paid", rating: 4.3, tags: ["crawl", "enterprise", "technical"]},
    {name: "Botify", category: "Marketing", subcategory: "Enterprise SEO", desc: "Enterprise SEO", url: "botify.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "crawl", "technical"]},
    {name: "BrightEdge", category: "Marketing", subcategory: "Enterprise SEO", desc: "Enterprise SEO", url: "brightedge.com", pricing: "Paid", rating: 4.1, tags: ["enterprise", "content", "seo"]},
    {name: "Conductor", category: "Marketing", subcategory: "Enterprise SEO", desc: "Enterprise organic", url: "conductor.com", pricing: "Paid", rating: 4.1, tags: ["enterprise", "organic", "content"]},
    
    // ==================== PPC & ADS ====================
    {name: "Google Ads", category: "Marketing", subcategory: "PPC", desc: "Google advertising", url: "ads.google.com", pricing: "Pay-per-click", rating: 4.5, tags: ["ppc", "google", "search"], featured: true},
    {name: "Facebook Ads", category: "Marketing", subcategory: "Social Ads", desc: "Meta advertising", url: "facebook.com/business/ads", pricing: "Pay-per-click", rating: 4.4, tags: ["social", "meta", "targeting"]},
    {name: "LinkedIn Ads", category: "Marketing", subcategory: "B2B Ads", desc: "LinkedIn advertising", url: "business.linkedin.com/marketing-solutions/ads", pricing: "Pay-per-click", rating: 4.2, tags: ["b2b", "linkedin", "professional"]},
    {name: "Microsoft Advertising", category: "Marketing", subcategory: "PPC", desc: "Bing ads", url: "ads.microsoft.com", pricing: "Pay-per-click", rating: 4.1, tags: ["ppc", "bing", "search"]},
    {name: "TikTok Ads", category: "Marketing", subcategory: "Social Ads", desc: "TikTok advertising", url: "ads.tiktok.com", pricing: "Pay-per-click", rating: 4.2, tags: ["social", "video", "gen-z"]},
    {name: "Optmyzr", category: "Marketing", subcategory: "PPC Management", desc: "PPC management", url: "optmyzr.com", pricing: "Paid", rating: 4.4, tags: ["ppc", "automation", "scripts"]},
    {name: "WordStream", category: "Marketing", subcategory: "PPC", desc: "PPC tools", url: "wordstream.com", pricing: "Freemium", rating: 4.2, tags: ["ppc", "grader", "tools"]},
    {name: "Adalysis", category: "Marketing", subcategory: "PPC", desc: "PPC optimization", url: "adalysis.com", pricing: "Paid", rating: 4.3, tags: ["ppc", "alerts", "automation"]},
    {name: "PPCexpo", category: "Marketing", subcategory: "PPC", desc: "PPC reporting", url: "ppcexpo.com", pricing: "Paid", rating: 4.1, tags: ["ppc", "reporting", "analysis"]},
    {name: "AdEspresso", category: "Marketing", subcategory: "Social Ads", desc: "Facebook ads tool", url: "adespresso.com", pricing: "Paid", rating: 4.2, tags: ["facebook", "management", "testing"]},
    
    // ==================== ANALYTICS ====================
    {name: "Google Analytics 4", category: "Marketing", subcategory: "Analytics", desc: "Web analytics", url: "analytics.google.com", pricing: "Free", rating: 4.5, tags: ["analytics", "google", "free"], featured: true},
    {name: "Adobe Analytics", category: "Marketing", subcategory: "Analytics", desc: "Enterprise analytics", url: "adobe.com/analytics", pricing: "Paid", rating: 4.4, tags: ["enterprise", "adobe", "advanced"]},
    {name: "Mixpanel", category: "Marketing", subcategory: "Product Analytics", desc: "Product analytics", url: "mixpanel.com", pricing: "Freemium", rating: 4.5, tags: ["product", "events", "funnels"]},
    {name: "Amplitude", category: "Marketing", subcategory: "Product Analytics", desc: "Digital analytics", url: "amplitude.com", pricing: "Freemium", rating: 4.5, tags: ["product", "behavioral", "experimentation"]},
    {name: "Heap", category: "Marketing", subcategory: "Product Analytics", desc: "Autocapture analytics", url: "heap.io", pricing: "Paid", rating: 4.3, tags: ["autocapture", "product", "insights"]},
    {name: "Kissmetrics", category: "Marketing", subcategory: "Analytics", desc: "Behavioral analytics", url: "kissmetrics.io", pricing: "Paid", rating: 4.1, tags: ["behavioral", "saas", "ecommerce"]},
    {name: "Hotjar", category: "Marketing", subcategory: "Behavior", desc: "Behavior analytics", url: "hotjar.com", pricing: "Freemium", rating: 4.5, tags: ["heatmaps", "recordings", "feedback"]},
    {name: "Crazy Egg", category: "Marketing", subcategory: "Behavior", desc: "Heatmaps & testing", url: "crazyegg.com", pricing: "Paid", rating: 4.3, tags: ["heatmaps", "a-b-testing", "recordings"]},
    {name: "Lucky Orange", category: "Marketing", subcategory: "Behavior", desc: "Conversion optimization", url: "luckyorange.com", pricing: "Paid", rating: 4.2, tags: ["heatmaps", "recordings", "chat"]},
    {name: "FullStory", category: "Marketing", subcategory: "DXI", desc: "Digital experience", url: "fullstory.com", pricing: "Paid", rating: 4.4, tags: ["dxi", "session-replay", "frustration"]},
    
    // ==================== CONVERSION & A/B TESTING ====================
    {name: "Optimizely", category: "Marketing", subcategory: "Experimentation", desc: "Digital experimentation", url: "optimizely.com", pricing: "Paid", rating: 4.4, tags: ["a-b-testing", "experimentation", "enterprise"], featured: true},
    {name: "VWO", category: "Marketing", subcategory: "A/B Testing", desc: "A/B testing platform", url: "vwo.com", pricing: "Paid", rating: 4.3, tags: ["a-b-testing", "cro", "personalization"]},
    {name: "AB Tasty", category: "Marketing", subcategory: "A/B Testing", desc: "Experience optimization", url: "abtasty.com", pricing: "Paid", rating: 4.2, tags: ["a-b-testing", "personalization", "feature-flags"]},
    {name: "Convert", category: "Marketing", subcategory: "A/B Testing", desc: "A/B testing", url: "convert.com", pricing: "Paid", rating: 4.3, tags: ["a-b-testing", "privacy", "enterprise"]},
    {name: "Kameleoon", category: "Marketing", subcategory: "A/B Testing", desc: "A/B testing & personalization", url: "kameleoon.com", pricing: "Paid", rating: 4.1, tags: ["a-b-testing", "ai", "personalization"]},
    {name: "Google Optimize", category: "Marketing", subcategory: "A/B Testing", desc: "Free A/B testing", url: "optimize.google.com", pricing: "Free", rating: 4.0, tags: ["a-b-testing", "google", "free"]},
    {name: "Unbounce", category: "Marketing", subcategory: "Landing Pages", desc: "Landing page builder", url: "unbounce.com", pricing: "Paid", rating: 4.4, tags: ["landing-pages", "a-b-testing", "conversion"]},
    {name: "Instapage", category: "Marketing", subcategory: "Landing Pages", desc: "Landing page platform", url: "instapage.com", pricing: "Paid", rating: 4.3, tags: ["landing-pages", "personalization", "enterprise"]},
    {name: "Leadpages", category: "Marketing", subcategory: "Landing Pages", desc: "Landing page builder", url: "leadpages.com", pricing: "Paid", rating: 4.2, tags: ["landing-pages", "smb", "templates"]},
    {name: "ClickFunnels", category: "Marketing", subcategory: "Funnels", desc: "Sales funnels", url: "clickfunnels.com", pricing: "Paid", rating: 4.1, tags: ["funnels", "sales", "marketing"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE63 = AI_TOOLS_PHASE63;
}


