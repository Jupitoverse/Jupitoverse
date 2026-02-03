// AI Tools Database - Phase 33: More Business Intelligence & Analytics
// 150+ BI and analytics tools

const AI_TOOLS_PHASE33 = [
    // ==================== BUSINESS INTELLIGENCE ====================
    {name: "Tableau", category: "BI", subcategory: "Visualization", desc: "Visual analytics platform", url: "tableau.com", pricing: "Paid", rating: 4.6, tags: ["visualization", "dashboards", "enterprise"], featured: true},
    {name: "Power BI", category: "BI", subcategory: "Microsoft", desc: "Microsoft BI tool", url: "powerbi.microsoft.com", pricing: "Freemium", rating: 4.5, tags: ["microsoft", "dashboards", "integration"]},
    {name: "Looker", category: "BI", subcategory: "Google", desc: "Google BI platform", url: "cloud.google.com/looker", pricing: "Paid", rating: 4.4, tags: ["google", "modeling", "enterprise"]},
    {name: "Qlik Sense", category: "BI", subcategory: "Associative", desc: "Associative analytics", url: "qlik.com", pricing: "Paid", rating: 4.3, tags: ["associative", "dashboards", "enterprise"]},
    {name: "Sisense", category: "BI", subcategory: "Embedded", desc: "Embedded analytics", url: "sisense.com", pricing: "Paid", rating: 4.3, tags: ["embedded", "api", "customizable"]},
    {name: "Domo", category: "BI", subcategory: "Cloud", desc: "Cloud BI platform", url: "domo.com", pricing: "Paid", rating: 4.2, tags: ["cloud", "mobile", "connectors"]},
    {name: "ThoughtSpot", category: "BI", subcategory: "Search", desc: "Search-driven analytics", url: "thoughtspot.com", pricing: "Paid", rating: 4.3, tags: ["search", "ai", "natural-language"]},
    {name: "Mode", category: "BI", subcategory: "Collaborative", desc: "Collaborative analytics", url: "mode.com", pricing: "Freemium", rating: 4.3, tags: ["collaborative", "sql", "python"]},
    {name: "Metabase", category: "BI", subcategory: "Open Source", desc: "Open source BI", url: "metabase.com", pricing: "Freemium", rating: 4.5, tags: ["open-source", "simple", "self-hosted"]},
    {name: "Redash", category: "BI", subcategory: "Open Source", desc: "Query and visualize", url: "redash.io", pricing: "Free", rating: 4.2, tags: ["open-source", "sql", "dashboards"]},
    {name: "Apache Superset", category: "BI", subcategory: "Open Source", desc: "Open source exploration", url: "superset.apache.org", pricing: "Free", rating: 4.3, tags: ["open-source", "apache", "exploration"]},
    {name: "Preset", category: "BI", subcategory: "Cloud", desc: "Cloud Superset", url: "preset.io", pricing: "Freemium", rating: 4.2, tags: ["superset", "cloud", "managed"]},
    {name: "Lightdash", category: "BI", subcategory: "dbt", desc: "BI for dbt", url: "lightdash.com", pricing: "Freemium", rating: 4.3, tags: ["dbt", "metrics", "open-source"]},
    {name: "GoodData", category: "BI", subcategory: "Embedded", desc: "Analytics platform", url: "gooddata.com", pricing: "Paid", rating: 4.1, tags: ["embedded", "enterprise", "white-label"]},
    {name: "Klipfolio", category: "BI", subcategory: "Dashboards", desc: "Dashboard software", url: "klipfolio.com", pricing: "Paid", rating: 4.2, tags: ["dashboards", "real-time", "smb"]},
    
    // ==================== DATA VISUALIZATION ====================
    {name: "D3.js", category: "Visualization", subcategory: "Library", desc: "JavaScript visualization", url: "d3js.org", pricing: "Free", rating: 4.6, tags: ["javascript", "custom", "web"], featured: true},
    {name: "Chart.js", category: "Visualization", subcategory: "Library", desc: "Simple JS charts", url: "chartjs.org", pricing: "Free", rating: 4.5, tags: ["javascript", "simple", "responsive"]},
    {name: "Plotly", category: "Visualization", subcategory: "Library", desc: "Interactive graphing", url: "plotly.com", pricing: "Freemium", rating: 4.5, tags: ["interactive", "python", "javascript"]},
    {name: "Highcharts", category: "Visualization", subcategory: "Library", desc: "Interactive charts", url: "highcharts.com", pricing: "Freemium", rating: 4.4, tags: ["interactive", "commercial", "maps"]},
    {name: "ECharts", category: "Visualization", subcategory: "Library", desc: "Apache charts library", url: "echarts.apache.org", pricing: "Free", rating: 4.4, tags: ["apache", "interactive", "baidu"]},
    {name: "Vega", category: "Visualization", subcategory: "Grammar", desc: "Visualization grammar", url: "vega.github.io", pricing: "Free", rating: 4.3, tags: ["grammar", "declarative", "academic"]},
    {name: "Observable", category: "Visualization", subcategory: "Notebooks", desc: "Data exploration", url: "observablehq.com", pricing: "Freemium", rating: 4.4, tags: ["notebooks", "reactive", "d3"]},
    {name: "RAWGraphs", category: "Visualization", subcategory: "Tool", desc: "Open data visualization", url: "rawgraphs.io", pricing: "Free", rating: 4.2, tags: ["open-source", "no-code", "export"]},
    {name: "Flourish", category: "Visualization", subcategory: "Tool", desc: "Data storytelling", url: "flourish.studio", pricing: "Freemium", rating: 4.4, tags: ["storytelling", "animated", "templates"]},
    {name: "Datawrapper", category: "Visualization", subcategory: "Tool", desc: "Charts for news", url: "datawrapper.de", pricing: "Freemium", rating: 4.5, tags: ["journalism", "responsive", "embeddable"]},
    {name: "Infogram", category: "Visualization", subcategory: "Tool", desc: "Infographics maker", url: "infogram.com", pricing: "Freemium", rating: 4.2, tags: ["infographics", "maps", "reports"]},
    {name: "Canva Charts", category: "Visualization", subcategory: "Tool", desc: "Canva data viz", url: "canva.com", pricing: "Freemium", rating: 4.3, tags: ["canva", "easy", "design"]},
    {name: "Google Charts", category: "Visualization", subcategory: "Library", desc: "Google charting", url: "developers.google.com/chart", pricing: "Free", rating: 4.2, tags: ["google", "free", "web"]},
    {name: "ApexCharts", category: "Visualization", subcategory: "Library", desc: "Modern charts", url: "apexcharts.com", pricing: "Free", rating: 4.3, tags: ["modern", "interactive", "react"]},
    {name: "Recharts", category: "Visualization", subcategory: "React", desc: "React charts", url: "recharts.org", pricing: "Free", rating: 4.3, tags: ["react", "composable", "d3-based"]},
    
    // ==================== PRODUCT ANALYTICS ====================
    {name: "Mixpanel", category: "Analytics", subcategory: "Product", desc: "Product analytics", url: "mixpanel.com", pricing: "Freemium", rating: 4.5, tags: ["product", "events", "funnels"], featured: true},
    {name: "Amplitude", category: "Analytics", subcategory: "Product", desc: "Digital analytics", url: "amplitude.com", pricing: "Freemium", rating: 4.5, tags: ["product", "behavioral", "experimentation"]},
    {name: "Heap", category: "Analytics", subcategory: "Product", desc: "Autocapture analytics", url: "heap.io", pricing: "Paid", rating: 4.3, tags: ["autocapture", "retroactive", "insights"]},
    {name: "PostHog", category: "Analytics", subcategory: "Open Source", desc: "Open source analytics", url: "posthog.com", pricing: "Freemium", rating: 4.4, tags: ["open-source", "feature-flags", "session-replay"]},
    {name: "Pendo", category: "Analytics", subcategory: "Product", desc: "Product experience", url: "pendo.io", pricing: "Paid", rating: 4.3, tags: ["product", "guides", "feedback"]},
    {name: "LogRocket", category: "Analytics", subcategory: "Session", desc: "Session replay", url: "logrocket.com", pricing: "Freemium", rating: 4.4, tags: ["session-replay", "errors", "frontend"]},
    {name: "FullStory", category: "Analytics", subcategory: "DXI", desc: "Digital experience", url: "fullstory.com", pricing: "Paid", rating: 4.4, tags: ["dxi", "session-replay", "frustration"]},
    {name: "Smartlook", category: "Analytics", subcategory: "Session", desc: "Qualitative analytics", url: "smartlook.com", pricing: "Freemium", rating: 4.2, tags: ["session-replay", "events", "heatmaps"]},
    {name: "UXCam", category: "Analytics", subcategory: "Mobile", desc: "Mobile app analytics", url: "uxcam.com", pricing: "Freemium", rating: 4.3, tags: ["mobile", "session-replay", "heatmaps"]},
    {name: "Indicative", category: "Analytics", subcategory: "Product", desc: "Customer journey analytics", url: "indicative.com", pricing: "Paid", rating: 4.1, tags: ["journey", "product", "mparticle"]},
    
    // ==================== WEB ANALYTICS ====================
    {name: "Google Analytics", category: "Analytics", subcategory: "Web", desc: "Web analytics by Google", url: "analytics.google.com", pricing: "Free", rating: 4.6, tags: ["web", "free", "standard"]},
    {name: "Plausible", category: "Analytics", subcategory: "Privacy", desc: "Privacy-first analytics", url: "plausible.io", pricing: "Paid", rating: 4.5, tags: ["privacy", "lightweight", "simple"]},
    {name: "Fathom", category: "Analytics", subcategory: "Privacy", desc: "Privacy-focused analytics", url: "usefathom.com", pricing: "Paid", rating: 4.5, tags: ["privacy", "simple", "fast"]},
    {name: "Simple Analytics", category: "Analytics", subcategory: "Privacy", desc: "Simple privacy analytics", url: "simpleanalytics.com", pricing: "Paid", rating: 4.4, tags: ["privacy", "simple", "gdpr"]},
    {name: "Umami", category: "Analytics", subcategory: "Open Source", desc: "Open source analytics", url: "umami.is", pricing: "Free", rating: 4.4, tags: ["open-source", "privacy", "self-hosted"]},
    {name: "Matomo", category: "Analytics", subcategory: "Self-Hosted", desc: "Web analytics platform", url: "matomo.org", pricing: "Freemium", rating: 4.3, tags: ["self-hosted", "privacy", "comprehensive"]},
    {name: "Clicky", category: "Analytics", subcategory: "Real-time", desc: "Real-time web analytics", url: "clicky.com", pricing: "Freemium", rating: 4.1, tags: ["real-time", "heatmaps", "uptime"]},
    {name: "Pirsch", category: "Analytics", subcategory: "Privacy", desc: "Cookie-free analytics", url: "pirsch.io", pricing: "Paid", rating: 4.2, tags: ["privacy", "cookie-free", "simple"]},
    {name: "GoatCounter", category: "Analytics", subcategory: "Open Source", desc: "Easy open source analytics", url: "goatcounter.com", pricing: "Freemium", rating: 4.2, tags: ["open-source", "simple", "free"]},
    {name: "Countly", category: "Analytics", subcategory: "Mobile", desc: "Mobile analytics", url: "count.ly", pricing: "Freemium", rating: 4.1, tags: ["mobile", "push", "crashes"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE33 = AI_TOOLS_PHASE33;
}


