// AI Tools Database - Phase 27: More Coding & Development Tools
// 200+ Additional developer tools

const AI_TOOLS_PHASE27 = [
    // ==================== LOW-CODE / NO-CODE ====================
    {name: "Bubble", category: "No-Code", subcategory: "App Builder", desc: "Visual web app builder", url: "bubble.io", pricing: "Freemium", rating: 4.5, tags: ["no-code", "apps", "visual"], featured: true},
    {name: "Webflow", category: "No-Code", subcategory: "Website", desc: "Visual website builder", url: "webflow.com", pricing: "Freemium", rating: 4.6, tags: ["website", "cms", "visual"]},
    {name: "Framer", category: "No-Code", subcategory: "Website", desc: "AI website builder", url: "framer.com", pricing: "Freemium", rating: 4.5, tags: ["website", "ai", "design"]},
    {name: "Glide", category: "No-Code", subcategory: "Apps", desc: "Apps from spreadsheets", url: "glideapps.com", pricing: "Freemium", rating: 4.4, tags: ["apps", "spreadsheet", "mobile"]},
    {name: "Adalo", category: "No-Code", subcategory: "Mobile", desc: "No-code mobile apps", url: "adalo.com", pricing: "Freemium", rating: 4.2, tags: ["mobile", "no-code", "native"]},
    {name: "Thunkable", category: "No-Code", subcategory: "Mobile", desc: "Mobile app builder", url: "thunkable.com", pricing: "Freemium", rating: 4.2, tags: ["mobile", "drag-drop", "cross-platform"]},
    {name: "Draftbit", category: "No-Code", subcategory: "Mobile", desc: "Native mobile apps", url: "draftbit.com", pricing: "Paid", rating: 4.2, tags: ["mobile", "react-native", "export"]},
    {name: "FlutterFlow", category: "No-Code", subcategory: "Flutter", desc: "Visual Flutter builder", url: "flutterflow.io", pricing: "Freemium", rating: 4.4, tags: ["flutter", "visual", "export"]},
    {name: "Appgyver", category: "No-Code", subcategory: "Apps", desc: "No-code app platform", url: "appgyver.com", pricing: "Free", rating: 4.3, tags: ["free", "sap", "enterprise"]},
    {name: "Softr", category: "No-Code", subcategory: "Airtable", desc: "Apps from Airtable", url: "softr.io", pricing: "Freemium", rating: 4.4, tags: ["airtable", "portals", "apps"]},
    {name: "Stacker", category: "No-Code", subcategory: "Airtable", desc: "Business apps from data", url: "stacker.app", pricing: "Paid", rating: 4.3, tags: ["airtable", "sheets", "portals"]},
    {name: "Pory", category: "No-Code", subcategory: "Airtable", desc: "Websites from Airtable", url: "pory.io", pricing: "Freemium", rating: 4.2, tags: ["airtable", "notion", "websites"]},
    {name: "Carrd", category: "No-Code", subcategory: "Landing", desc: "Simple landing pages", url: "carrd.co", pricing: "Freemium", rating: 4.5, tags: ["landing", "simple", "affordable"]},
    {name: "Typedream", category: "No-Code", subcategory: "Website", desc: "Notion-like websites", url: "typedream.com", pricing: "Freemium", rating: 4.3, tags: ["notion", "simple", "ai"]},
    {name: "Super", category: "No-Code", subcategory: "Notion", desc: "Websites from Notion", url: "super.so", pricing: "Paid", rating: 4.4, tags: ["notion", "website", "fast"]},
    
    // ==================== AUTOMATION ====================
    {name: "Zapier", category: "Automation", subcategory: "Integration", desc: "App integration platform", url: "zapier.com", pricing: "Freemium", rating: 4.6, tags: ["integration", "automation", "popular"], featured: true},
    {name: "Make (Integromat)", category: "Automation", subcategory: "Workflows", desc: "Visual automation", url: "make.com", pricing: "Freemium", rating: 4.5, tags: ["visual", "powerful", "scenarios"]},
    {name: "n8n", category: "Automation", subcategory: "Open Source", desc: "Open source automation", url: "n8n.io", pricing: "Freemium", rating: 4.5, tags: ["open-source", "self-hosted", "nodes"]},
    {name: "Pipedream", category: "Automation", subcategory: "Developer", desc: "Developer automation", url: "pipedream.com", pricing: "Freemium", rating: 4.5, tags: ["developer", "code", "serverless"]},
    {name: "Tray.io", category: "Automation", subcategory: "Enterprise", desc: "Enterprise automation", url: "tray.io", pricing: "Paid", rating: 4.3, tags: ["enterprise", "api", "integration"]},
    {name: "Workato", category: "Automation", subcategory: "Enterprise", desc: "Enterprise automation", url: "workato.com", pricing: "Paid", rating: 4.4, tags: ["enterprise", "recipes", "ai"]},
    {name: "Microsoft Power Automate", category: "Automation", subcategory: "Microsoft", desc: "Microsoft automation", url: "powerautomate.microsoft.com", pricing: "Freemium", rating: 4.3, tags: ["microsoft", "office", "rpa"]},
    {name: "IFTTT", category: "Automation", subcategory: "Simple", desc: "Simple automation", url: "ifttt.com", pricing: "Freemium", rating: 4.2, tags: ["simple", "applets", "consumer"]},
    {name: "Parabola", category: "Automation", subcategory: "Data", desc: "Data workflow automation", url: "parabola.io", pricing: "Freemium", rating: 4.3, tags: ["data", "drag-drop", "analysis"]},
    {name: "Bardeen", category: "Automation", subcategory: "AI", desc: "AI automation", url: "bardeen.ai", pricing: "Freemium", rating: 4.3, tags: ["ai", "browser", "scraping"]},
    {name: "Axiom", category: "Automation", subcategory: "Browser", desc: "Browser automation", url: "axiom.ai", pricing: "Freemium", rating: 4.2, tags: ["browser", "no-code", "bots"]},
    {name: "Browse AI", category: "Automation", subcategory: "Scraping", desc: "Web scraping robots", url: "browse.ai", pricing: "Freemium", rating: 4.3, tags: ["scraping", "robots", "monitoring"]},
    {name: "Octoparse", category: "Automation", subcategory: "Scraping", desc: "Web scraping tool", url: "octoparse.com", pricing: "Freemium", rating: 4.2, tags: ["scraping", "data", "visual"]},
    {name: "Apify", category: "Automation", subcategory: "Scraping", desc: "Web scraping platform", url: "apify.com", pricing: "Freemium", rating: 4.4, tags: ["scraping", "actors", "api"]},
    {name: "PhantomBuster", category: "Automation", subcategory: "Growth", desc: "Growth automation", url: "phantombuster.com", pricing: "Paid", rating: 4.1, tags: ["linkedin", "growth", "automation"]},
    
    // ==================== TESTING ====================
    {name: "Playwright", category: "Testing", subcategory: "E2E", desc: "End-to-end testing", url: "playwright.dev", pricing: "Free", rating: 4.7, tags: ["e2e", "microsoft", "cross-browser"], featured: true},
    {name: "Cypress", category: "Testing", subcategory: "E2E", desc: "JavaScript testing", url: "cypress.io", pricing: "Freemium", rating: 4.6, tags: ["e2e", "javascript", "component"]},
    {name: "Selenium", category: "Testing", subcategory: "E2E", desc: "Browser automation", url: "selenium.dev", pricing: "Free", rating: 4.3, tags: ["automation", "browser", "legacy"]},
    {name: "Puppeteer", category: "Testing", subcategory: "Headless", desc: "Headless Chrome API", url: "pptr.dev", pricing: "Free", rating: 4.5, tags: ["headless", "chrome", "node"]},
    {name: "TestCafe", category: "Testing", subcategory: "E2E", desc: "E2E testing framework", url: "testcafe.io", pricing: "Freemium", rating: 4.3, tags: ["e2e", "no-webdriver", "cross-browser"]},
    {name: "Jest", category: "Testing", subcategory: "Unit", desc: "JavaScript testing", url: "jestjs.io", pricing: "Free", rating: 4.6, tags: ["unit", "javascript", "facebook"]},
    {name: "Vitest", category: "Testing", subcategory: "Unit", desc: "Vite-native testing", url: "vitest.dev", pricing: "Free", rating: 4.5, tags: ["unit", "vite", "fast"]},
    {name: "Mocha", category: "Testing", subcategory: "Unit", desc: "JavaScript test framework", url: "mochajs.org", pricing: "Free", rating: 4.3, tags: ["unit", "flexible", "node"]},
    {name: "BrowserStack", category: "Testing", subcategory: "Cloud", desc: "Cross-browser testing", url: "browserstack.com", pricing: "Paid", rating: 4.4, tags: ["cloud", "browsers", "devices"]},
    {name: "Sauce Labs", category: "Testing", subcategory: "Cloud", desc: "Testing cloud", url: "saucelabs.com", pricing: "Paid", rating: 4.3, tags: ["cloud", "automation", "enterprise"]},
    {name: "LambdaTest", category: "Testing", subcategory: "Cloud", desc: "Cross-browser cloud", url: "lambdatest.com", pricing: "Freemium", rating: 4.3, tags: ["cloud", "browsers", "affordable"]},
    {name: "Applitools", category: "Testing", subcategory: "Visual", desc: "AI visual testing", url: "applitools.com", pricing: "Freemium", rating: 4.4, tags: ["visual", "ai", "eyes"]},
    {name: "Percy", category: "Testing", subcategory: "Visual", desc: "Visual testing by BrowserStack", url: "percy.io", pricing: "Freemium", rating: 4.3, tags: ["visual", "snapshots", "browserstack"]},
    {name: "Chromatic", category: "Testing", subcategory: "Storybook", desc: "Visual testing for Storybook", url: "chromatic.com", pricing: "Freemium", rating: 4.4, tags: ["storybook", "visual", "ui"]},
    {name: "Meticulous", category: "Testing", subcategory: "AI", desc: "AI frontend testing", url: "meticulous.ai", pricing: "Paid", rating: 4.2, tags: ["ai", "frontend", "automated"]},
    
    // ==================== DOCUMENTATION ====================
    {name: "Mintlify", category: "Docs", subcategory: "Developer", desc: "Beautiful developer docs", url: "mintlify.com", pricing: "Freemium", rating: 4.5, tags: ["docs", "beautiful", "modern"]},
    {name: "GitBook", category: "Docs", subcategory: "Knowledge", desc: "Knowledge management", url: "gitbook.com", pricing: "Freemium", rating: 4.4, tags: ["docs", "knowledge", "collaboration"]},
    {name: "ReadMe", category: "Docs", subcategory: "API", desc: "API documentation", url: "readme.com", pricing: "Freemium", rating: 4.4, tags: ["api", "docs", "developer"]},
    {name: "Docusaurus", category: "Docs", subcategory: "Open Source", desc: "Open source docs", url: "docusaurus.io", pricing: "Free", rating: 4.5, tags: ["open-source", "react", "meta"]},
    {name: "MkDocs", category: "Docs", subcategory: "Markdown", desc: "Markdown documentation", url: "mkdocs.org", pricing: "Free", rating: 4.3, tags: ["markdown", "python", "static"]},
    {name: "Sphinx", category: "Docs", subcategory: "Python", desc: "Python documentation", url: "sphinx-doc.org", pricing: "Free", rating: 4.2, tags: ["python", "rst", "technical"]},
    {name: "VuePress", category: "Docs", subcategory: "Vue", desc: "Vue-powered static site", url: "vuepress.vuejs.org", pricing: "Free", rating: 4.3, tags: ["vue", "static", "docs"]},
    {name: "Nextra", category: "Docs", subcategory: "Next.js", desc: "Next.js documentation", url: "nextra.site", pricing: "Free", rating: 4.3, tags: ["nextjs", "mdx", "modern"]},
    {name: "Starlight", category: "Docs", subcategory: "Astro", desc: "Astro documentation theme", url: "starlight.astro.build", pricing: "Free", rating: 4.3, tags: ["astro", "docs", "fast"]},
    {name: "Redocly", category: "Docs", subcategory: "API", desc: "API docs platform", url: "redocly.com", pricing: "Freemium", rating: 4.3, tags: ["api", "openapi", "enterprise"]},
    {name: "Stoplight", category: "Docs", subcategory: "API", desc: "API design platform", url: "stoplight.io", pricing: "Freemium", rating: 4.3, tags: ["api", "design", "docs"]},
    {name: "Scalar", category: "Docs", subcategory: "API", desc: "Beautiful API docs", url: "scalar.com", pricing: "Freemium", rating: 4.2, tags: ["api", "openapi", "modern"]},
    {name: "Bump.sh", category: "Docs", subcategory: "API", desc: "API documentation", url: "bump.sh", pricing: "Freemium", rating: 4.2, tags: ["api", "changelog", "hub"]},
    {name: "Theneo", category: "Docs", subcategory: "AI", desc: "AI API documentation", url: "theneo.io", pricing: "Freemium", rating: 4.2, tags: ["ai", "api", "docs"]},
    {name: "Fern", category: "Docs", subcategory: "SDK", desc: "API docs and SDKs", url: "buildwithfern.com", pricing: "Freemium", rating: 4.2, tags: ["sdk", "api", "generation"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE27 = AI_TOOLS_PHASE27;
}


