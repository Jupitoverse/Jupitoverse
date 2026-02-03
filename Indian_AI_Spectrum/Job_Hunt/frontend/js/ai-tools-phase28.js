// AI Tools Database - Phase 28: More Business & Enterprise AI Tools
// 200+ Additional business tools

const AI_TOOLS_PHASE28 = [
    // ==================== SPREADSHEETS & DATA ====================
    {name: "Google Sheets", category: "Spreadsheet", subcategory: "Cloud", desc: "Cloud spreadsheet", url: "sheets.google.com", pricing: "Free", rating: 4.6, tags: ["cloud", "collaboration", "google"], featured: true},
    {name: "Microsoft Excel", category: "Spreadsheet", subcategory: "Desktop", desc: "Spreadsheet software", url: "microsoft.com/excel", pricing: "Paid", rating: 4.6, tags: ["desktop", "powerful", "enterprise"]},
    {name: "Airtable", category: "Spreadsheet", subcategory: "Database", desc: "Spreadsheet-database hybrid", url: "airtable.com", pricing: "Freemium", rating: 4.5, tags: ["database", "flexible", "views"]},
    {name: "Rows", category: "Spreadsheet", subcategory: "Modern", desc: "Modern spreadsheet", url: "rows.com", pricing: "Freemium", rating: 4.3, tags: ["modern", "integrations", "ai"]},
    {name: "Grist", category: "Spreadsheet", subcategory: "Open Source", desc: "Open source spreadsheet", url: "getgrist.com", pricing: "Freemium", rating: 4.2, tags: ["open-source", "database", "self-host"]},
    {name: "Stackby", category: "Spreadsheet", subcategory: "Database", desc: "Spreadsheet-database", url: "stackby.com", pricing: "Freemium", rating: 4.1, tags: ["database", "api", "affordable"]},
    {name: "SeaTable", category: "Spreadsheet", subcategory: "Database", desc: "Spreadsheet with database", url: "seatable.io", pricing: "Freemium", rating: 4.1, tags: ["database", "self-host", "plugins"]},
    {name: "NocoDB", category: "Spreadsheet", subcategory: "Open Source", desc: "Open source Airtable", url: "nocodb.com", pricing: "Free", rating: 4.3, tags: ["open-source", "airtable-alt", "sql"]},
    {name: "Baserow", category: "Spreadsheet", subcategory: "Open Source", desc: "No-code database", url: "baserow.io", pricing: "Freemium", rating: 4.2, tags: ["open-source", "no-code", "api"]},
    {name: "Smartsheet", category: "Spreadsheet", subcategory: "Work", desc: "Work management", url: "smartsheet.com", pricing: "Paid", rating: 4.3, tags: ["enterprise", "projects", "collaboration"]},
    {name: "Excel AI (Copilot)", category: "Spreadsheet", subcategory: "AI", desc: "AI in Excel", url: "microsoft.com/excel", pricing: "Paid", rating: 4.3, tags: ["ai", "copilot", "formulas"]},
    {name: "Sheet+", category: "Spreadsheet", subcategory: "AI", desc: "AI for spreadsheets", url: "sheetplus.ai", pricing: "Freemium", rating: 4.2, tags: ["ai", "formulas", "explanations"]},
    {name: "Formulabot", category: "Spreadsheet", subcategory: "AI", desc: "AI formula generator", url: "formulabot.com", pricing: "Freemium", rating: 4.2, tags: ["ai", "formulas", "explain"]},
    {name: "Akkio", category: "Spreadsheet", subcategory: "AI", desc: "AI for spreadsheet data", url: "akkio.com", pricing: "Freemium", rating: 4.2, tags: ["ai", "predictions", "no-code"]},
    {name: "Obviously AI", category: "Spreadsheet", subcategory: "ML", desc: "No-code ML", url: "obviously.ai", pricing: "Paid", rating: 4.1, tags: ["ml", "no-code", "predictions"]},
    
    // ==================== PRESENTATION ====================
    {name: "Google Slides", category: "Presentation", subcategory: "Cloud", desc: "Cloud presentations", url: "slides.google.com", pricing: "Free", rating: 4.4, tags: ["cloud", "collaboration", "google"]},
    {name: "Microsoft PowerPoint", category: "Presentation", subcategory: "Desktop", desc: "Presentation software", url: "microsoft.com/powerpoint", pricing: "Paid", rating: 4.5, tags: ["desktop", "enterprise", "powerful"]},
    {name: "Keynote", category: "Presentation", subcategory: "Apple", desc: "Apple presentations", url: "apple.com/keynote", pricing: "Free", rating: 4.6, tags: ["apple", "beautiful", "animation"]},
    {name: "Canva", category: "Presentation", subcategory: "Design", desc: "Design presentations", url: "canva.com", pricing: "Freemium", rating: 4.6, tags: ["design", "templates", "easy"]},
    {name: "Pitch", category: "Presentation", subcategory: "Collaborative", desc: "Collaborative presentations", url: "pitch.com", pricing: "Freemium", rating: 4.4, tags: ["collaborative", "modern", "beautiful"]},
    {name: "Beautiful.ai", category: "Presentation", subcategory: "AI", desc: "AI presentations", url: "beautiful.ai", pricing: "Paid", rating: 4.4, tags: ["ai", "design", "smart"]},
    {name: "Tome", category: "Presentation", subcategory: "AI", desc: "AI storytelling", url: "tome.app", pricing: "Freemium", rating: 4.4, tags: ["ai", "storytelling", "generation"]},
    {name: "Gamma", category: "Presentation", subcategory: "AI", desc: "AI presentation maker", url: "gamma.app", pricing: "Freemium", rating: 4.5, tags: ["ai", "docs", "websites"]},
    {name: "Slides.ai", category: "Presentation", subcategory: "AI", desc: "AI slides from text", url: "slides.ai", pricing: "Freemium", rating: 4.2, tags: ["ai", "text-to-slides", "google"]},
    {name: "Slidesgo", category: "Presentation", subcategory: "Templates", desc: "Free slide templates", url: "slidesgo.com", pricing: "Freemium", rating: 4.4, tags: ["templates", "free", "canva"]},
    {name: "Slidebean", category: "Presentation", subcategory: "Startup", desc: "Pitch deck creator", url: "slidebean.com", pricing: "Paid", rating: 4.2, tags: ["pitch-deck", "startup", "ai"]},
    {name: "Visme", category: "Presentation", subcategory: "Visual", desc: "Visual content creation", url: "visme.co", pricing: "Freemium", rating: 4.3, tags: ["visual", "infographics", "presentations"]},
    {name: "Prezi", category: "Presentation", subcategory: "Dynamic", desc: "Dynamic presentations", url: "prezi.com", pricing: "Freemium", rating: 4.2, tags: ["dynamic", "zoom", "nonlinear"]},
    {name: "Powtoon", category: "Presentation", subcategory: "Animated", desc: "Animated presentations", url: "powtoon.com", pricing: "Freemium", rating: 4.2, tags: ["animated", "video", "explainer"]},
    {name: "Genially", category: "Presentation", subcategory: "Interactive", desc: "Interactive content", url: "genial.ly", pricing: "Freemium", rating: 4.3, tags: ["interactive", "infographics", "gamification"]},
    
    // ==================== FORMS & SURVEYS ====================
    {name: "Typeform", category: "Forms", subcategory: "Conversational", desc: "Conversational forms", url: "typeform.com", pricing: "Freemium", rating: 4.5, tags: ["conversational", "beautiful", "experience"], featured: true},
    {name: "Google Forms", category: "Forms", subcategory: "Free", desc: "Free form builder", url: "forms.google.com", pricing: "Free", rating: 4.4, tags: ["free", "google", "simple"]},
    {name: "Microsoft Forms", category: "Forms", subcategory: "Microsoft", desc: "Forms by Microsoft", url: "forms.microsoft.com", pricing: "Free", rating: 4.2, tags: ["microsoft", "office", "enterprise"]},
    {name: "JotForm", category: "Forms", subcategory: "Feature-rich", desc: "Form builder", url: "jotform.com", pricing: "Freemium", rating: 4.4, tags: ["forms", "templates", "apps"]},
    {name: "Tally", category: "Forms", subcategory: "Simple", desc: "Simple free forms", url: "tally.so", pricing: "Freemium", rating: 4.5, tags: ["simple", "free", "notion-like"]},
    {name: "Paperform", category: "Forms", subcategory: "Beautiful", desc: "Beautiful forms", url: "paperform.co", pricing: "Paid", rating: 4.4, tags: ["beautiful", "payments", "conditional"]},
    {name: "Fillout", category: "Forms", subcategory: "Modern", desc: "Modern form builder", url: "fillout.com", pricing: "Freemium", rating: 4.3, tags: ["modern", "integrations", "affordable"]},
    {name: "Formspark", category: "Forms", subcategory: "Backend", desc: "Form backend", url: "formspark.io", pricing: "Freemium", rating: 4.2, tags: ["backend", "static", "simple"]},
    {name: "Formspree", category: "Forms", subcategory: "Backend", desc: "Form backend", url: "formspree.io", pricing: "Freemium", rating: 4.3, tags: ["backend", "developers", "simple"]},
    {name: "SurveyMonkey", category: "Surveys", subcategory: "Enterprise", desc: "Survey platform", url: "surveymonkey.com", pricing: "Freemium", rating: 4.3, tags: ["surveys", "enterprise", "analysis"]},
    {name: "Qualtrics", category: "Surveys", subcategory: "Enterprise", desc: "Experience management", url: "qualtrics.com", pricing: "Paid", rating: 4.3, tags: ["enterprise", "experience", "research"]},
    {name: "Alchemer", category: "Surveys", subcategory: "Enterprise", desc: "Enterprise surveys", url: "alchemer.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "feedback", "surveys"]},
    {name: "SurveyLegend", category: "Surveys", subcategory: "Visual", desc: "Visual surveys", url: "surveylegend.com", pricing: "Freemium", rating: 4.2, tags: ["visual", "mobile", "beautiful"]},
    {name: "Survicate", category: "Surveys", subcategory: "Product", desc: "Product surveys", url: "survicate.com", pricing: "Freemium", rating: 4.3, tags: ["product", "nps", "in-app"]},
    {name: "Delighted", category: "Surveys", subcategory: "NPS", desc: "NPS surveys", url: "delighted.com", pricing: "Freemium", rating: 4.4, tags: ["nps", "csat", "ces"]},
    
    // ==================== MEETINGS & VIDEO ====================
    {name: "Zoom", category: "Video", subcategory: "Meetings", desc: "Video conferencing", url: "zoom.us", pricing: "Freemium", rating: 4.5, tags: ["meetings", "webinars", "popular"]},
    {name: "Google Meet", category: "Video", subcategory: "Meetings", desc: "Google video meetings", url: "meet.google.com", pricing: "Freemium", rating: 4.4, tags: ["google", "simple", "integrated"]},
    {name: "Microsoft Teams", category: "Video", subcategory: "Collaboration", desc: "Team collaboration", url: "teams.microsoft.com", pricing: "Freemium", rating: 4.4, tags: ["microsoft", "enterprise", "chat"]},
    {name: "Whereby", category: "Video", subcategory: "Simple", desc: "Simple video meetings", url: "whereby.com", pricing: "Freemium", rating: 4.3, tags: ["simple", "browser", "embed"]},
    {name: "Around", category: "Video", subcategory: "Collaborative", desc: "Collaborative meetings", url: "around.co", pricing: "Freemium", rating: 4.2, tags: ["collaborative", "floating", "modern"]},
    {name: "Loom", category: "Video", subcategory: "Async", desc: "Async video messaging", url: "loom.com", pricing: "Freemium", rating: 4.6, tags: ["async", "recording", "sharing"]},
    {name: "Vidyard", category: "Video", subcategory: "Sales", desc: "Video for sales", url: "vidyard.com", pricing: "Freemium", rating: 4.3, tags: ["sales", "hosting", "analytics"]},
    {name: "Wistia", category: "Video", subcategory: "Marketing", desc: "Video for marketing", url: "wistia.com", pricing: "Freemium", rating: 4.4, tags: ["marketing", "hosting", "analytics"]},
    {name: "Vimeo", category: "Video", subcategory: "Hosting", desc: "Video hosting", url: "vimeo.com", pricing: "Freemium", rating: 4.4, tags: ["hosting", "professional", "privacy"]},
    {name: "StreamYard", category: "Video", subcategory: "Streaming", desc: "Live streaming studio", url: "streamyard.com", pricing: "Freemium", rating: 4.5, tags: ["streaming", "browser", "multistream"]},
    {name: "Restream", category: "Video", subcategory: "Multistream", desc: "Multistream platform", url: "restream.io", pricing: "Freemium", rating: 4.4, tags: ["multistream", "studio", "chat"]},
    {name: "OBS Studio", category: "Video", subcategory: "Open Source", desc: "Open source streaming", url: "obsproject.com", pricing: "Free", rating: 4.6, tags: ["open-source", "streaming", "recording"]},
    {name: "Krisp", category: "Video", subcategory: "Noise", desc: "AI noise cancellation", url: "krisp.ai", pricing: "Freemium", rating: 4.5, tags: ["noise", "ai", "calls"]},
    {name: "Grain", category: "Video", subcategory: "Recording", desc: "Meeting recording AI", url: "grain.com", pricing: "Freemium", rating: 4.3, tags: ["recording", "highlights", "sharing"]},
    {name: "Fathom", category: "Video", subcategory: "Notes", desc: "AI meeting notes", url: "fathom.video", pricing: "Free", rating: 4.5, tags: ["notes", "ai", "free"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE28 = AI_TOOLS_PHASE28;
}


