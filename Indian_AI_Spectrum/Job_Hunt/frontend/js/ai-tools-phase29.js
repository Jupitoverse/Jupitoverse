// AI Tools Database - Phase 29: More Specialized AI Tools
// 150+ Specialized tools across categories

const AI_TOOLS_PHASE29 = [
    // ==================== TRANSLATION & LOCALIZATION ====================
    {name: "DeepL", category: "Translation", subcategory: "AI", desc: "AI translation", url: "deepl.com", pricing: "Freemium", rating: 4.7, tags: ["ai", "accurate", "european"], featured: true},
    {name: "Google Translate", category: "Translation", subcategory: "Free", desc: "Free translation", url: "translate.google.com", pricing: "Free", rating: 4.5, tags: ["free", "many-languages", "google"]},
    {name: "Microsoft Translator", category: "Translation", subcategory: "Enterprise", desc: "Microsoft translation", url: "translator.microsoft.com", pricing: "Freemium", rating: 4.3, tags: ["enterprise", "office", "api"]},
    {name: "Smartling", category: "Localization", subcategory: "Enterprise", desc: "Translation management", url: "smartling.com", pricing: "Paid", rating: 4.3, tags: ["enterprise", "tms", "workflow"]},
    {name: "Lokalise", category: "Localization", subcategory: "Platform", desc: "Localization platform", url: "lokalise.com", pricing: "Paid", rating: 4.5, tags: ["developer", "workflow", "automation"]},
    {name: "Phrase", category: "Localization", subcategory: "Platform", desc: "Localization suite", url: "phrase.com", pricing: "Paid", rating: 4.4, tags: ["tms", "memsource", "enterprise"]},
    {name: "Crowdin", category: "Localization", subcategory: "Crowdsource", desc: "Crowdsourced localization", url: "crowdin.com", pricing: "Freemium", rating: 4.4, tags: ["crowdsource", "agile", "integrations"]},
    {name: "Transifex", category: "Localization", subcategory: "Platform", desc: "Localization platform", url: "transifex.com", pricing: "Paid", rating: 4.2, tags: ["agile", "continuous", "api"]},
    {name: "Weglot", category: "Localization", subcategory: "Website", desc: "Website translation", url: "weglot.com", pricing: "Paid", rating: 4.5, tags: ["website", "no-code", "seo"]},
    {name: "Bablic", category: "Localization", subcategory: "Website", desc: "Website localization", url: "bablic.com", pricing: "Paid", rating: 4.1, tags: ["website", "visual", "simple"]},
    {name: "Trados", category: "Localization", subcategory: "CAT", desc: "CAT tool by SDL", url: "rws.com/trados", pricing: "Paid", rating: 4.2, tags: ["cat", "professional", "legacy"]},
    {name: "memoQ", category: "Localization", subcategory: "CAT", desc: "Translation environment", url: "memoq.com", pricing: "Paid", rating: 4.3, tags: ["cat", "professional", "server"]},
    {name: "Wordfast", category: "Localization", subcategory: "CAT", desc: "CAT tool", url: "wordfast.com", pricing: "Freemium", rating: 4.1, tags: ["cat", "affordable", "freelancer"]},
    {name: "OmegaT", category: "Localization", subcategory: "Open Source", desc: "Free CAT tool", url: "omegat.org", pricing: "Free", rating: 4.0, tags: ["open-source", "free", "cat"]},
    {name: "Lilt", category: "Localization", subcategory: "AI", desc: "AI translation platform", url: "lilt.com", pricing: "Paid", rating: 4.2, tags: ["ai", "adaptive", "enterprise"]},
    
    // ==================== OCR & DOCUMENT AI ====================
    {name: "ABBYY FineReader", category: "OCR", subcategory: "Desktop", desc: "OCR software", url: "abbyy.com/finereader", pricing: "Paid", rating: 4.5, tags: ["ocr", "pdf", "desktop"], featured: true},
    {name: "Adobe Acrobat", category: "OCR", subcategory: "PDF", desc: "PDF editor with OCR", url: "acrobat.adobe.com", pricing: "Paid", rating: 4.4, tags: ["pdf", "ocr", "editing"]},
    {name: "Google Document AI", category: "OCR", subcategory: "Cloud", desc: "Google's document AI", url: "cloud.google.com/document-ai", pricing: "Pay-per-use", rating: 4.4, tags: ["google", "cloud", "processing"]},
    {name: "Amazon Textract", category: "OCR", subcategory: "AWS", desc: "AWS document extraction", url: "aws.amazon.com/textract", pricing: "Pay-per-use", rating: 4.3, tags: ["aws", "extraction", "forms"]},
    {name: "Azure Form Recognizer", category: "OCR", subcategory: "Azure", desc: "Microsoft document AI", url: "azure.microsoft.com/form-recognizer", pricing: "Pay-per-use", rating: 4.3, tags: ["azure", "forms", "custom"]},
    {name: "Tesseract", category: "OCR", subcategory: "Open Source", desc: "Open source OCR", url: "tesseract-ocr.github.io", pricing: "Free", rating: 4.3, tags: ["open-source", "free", "ocr"]},
    {name: "Nanonets", category: "OCR", subcategory: "AI", desc: "AI OCR platform", url: "nanonets.com", pricing: "Freemium", rating: 4.3, tags: ["ai", "automation", "custom"]},
    {name: "Docparser", category: "OCR", subcategory: "Automation", desc: "Document data extraction", url: "docparser.com", pricing: "Paid", rating: 4.2, tags: ["extraction", "automation", "rules"]},
    {name: "Parseur", category: "OCR", subcategory: "Email", desc: "Email and PDF parsing", url: "parseur.com", pricing: "Freemium", rating: 4.2, tags: ["email", "pdf", "extraction"]},
    {name: "Rossum", category: "OCR", subcategory: "AI", desc: "AI document understanding", url: "rossum.ai", pricing: "Paid", rating: 4.3, tags: ["ai", "invoices", "enterprise"]},
    {name: "Hyperscience", category: "OCR", subcategory: "Enterprise", desc: "Enterprise document AI", url: "hyperscience.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "automation", "ml"]},
    {name: "Kofax", category: "OCR", subcategory: "Enterprise", desc: "Intelligent automation", url: "kofax.com", pricing: "Paid", rating: 4.1, tags: ["enterprise", "capture", "rpa"]},
    {name: "DocuWare", category: "OCR", subcategory: "DMS", desc: "Document management", url: "docuware.com", pricing: "Paid", rating: 4.2, tags: ["dms", "workflow", "cloud"]},
    {name: "M-Files", category: "OCR", subcategory: "DMS", desc: "Intelligent information management", url: "m-files.com", pricing: "Paid", rating: 4.2, tags: ["dms", "metadata", "ai"]},
    {name: "PandaDoc", category: "OCR", subcategory: "Documents", desc: "Document automation", url: "pandadoc.com", pricing: "Freemium", rating: 4.5, tags: ["proposals", "contracts", "esign"]},
    
    // ==================== ACCESSIBILITY ====================
    {name: "axe DevTools", category: "Accessibility", subcategory: "Testing", desc: "Accessibility testing", url: "deque.com/axe", pricing: "Freemium", rating: 4.5, tags: ["testing", "browser", "wcag"]},
    {name: "WAVE", category: "Accessibility", subcategory: "Testing", desc: "Web accessibility evaluation", url: "wave.webaim.org", pricing: "Free", rating: 4.4, tags: ["free", "testing", "webaim"]},
    {name: "Lighthouse", category: "Accessibility", subcategory: "Audit", desc: "Web audit tool", url: "developer.chrome.com/lighthouse", pricing: "Free", rating: 4.5, tags: ["audit", "performance", "chrome"]},
    {name: "UserWay", category: "Accessibility", subcategory: "Widget", desc: "Accessibility widget", url: "userway.org", pricing: "Freemium", rating: 4.2, tags: ["widget", "overlay", "ai"]},
    {name: "accessiBe", category: "Accessibility", subcategory: "AI", desc: "AI accessibility", url: "accessibe.com", pricing: "Paid", rating: 3.8, tags: ["ai", "overlay", "automated"]},
    {name: "AudioEye", category: "Accessibility", subcategory: "Platform", desc: "Digital accessibility", url: "audioeye.com", pricing: "Paid", rating: 4.0, tags: ["platform", "remediation", "monitoring"]},
    {name: "EqualWeb", category: "Accessibility", subcategory: "Widget", desc: "Accessibility widget", url: "equalweb.com", pricing: "Paid", rating: 4.0, tags: ["widget", "ai", "compliance"]},
    {name: "Siteimprove", category: "Accessibility", subcategory: "Platform", desc: "Digital presence platform", url: "siteimprove.com", pricing: "Paid", rating: 4.3, tags: ["accessibility", "seo", "analytics"]},
    {name: "Level Access", category: "Accessibility", subcategory: "Enterprise", desc: "Enterprise accessibility", url: "levelaccess.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "audit", "training"]},
    {name: "Pope Tech", category: "Accessibility", subcategory: "Monitoring", desc: "Accessibility monitoring", url: "pope.tech", pricing: "Paid", rating: 4.3, tags: ["monitoring", "wave", "affordable"]},
    
    // ==================== RESEARCH & ACADEMIA ====================
    {name: "Semantic Scholar", category: "Research", subcategory: "Search", desc: "AI-powered research", url: "semanticscholar.org", pricing: "Free", rating: 4.5, tags: ["papers", "ai", "citations"], featured: true},
    {name: "Google Scholar", category: "Research", subcategory: "Search", desc: "Scholarly literature search", url: "scholar.google.com", pricing: "Free", rating: 4.6, tags: ["search", "citations", "google"]},
    {name: "ResearchGate", category: "Research", subcategory: "Network", desc: "Research network", url: "researchgate.net", pricing: "Free", rating: 4.3, tags: ["network", "papers", "collaboration"]},
    {name: "Academia.edu", category: "Research", subcategory: "Network", desc: "Academic platform", url: "academia.edu", pricing: "Freemium", rating: 4.0, tags: ["network", "papers", "sharing"]},
    {name: "Elicit", category: "Research", subcategory: "AI", desc: "AI research assistant", url: "elicit.org", pricing: "Freemium", rating: 4.4, tags: ["ai", "papers", "analysis"]},
    {name: "Consensus", category: "Research", subcategory: "AI", desc: "AI research search", url: "consensus.app", pricing: "Freemium", rating: 4.3, tags: ["ai", "evidence", "search"]},
    {name: "Scite", category: "Research", subcategory: "Citations", desc: "Smart citations", url: "scite.ai", pricing: "Freemium", rating: 4.3, tags: ["citations", "context", "ai"]},
    {name: "Connected Papers", category: "Research", subcategory: "Visualization", desc: "Paper connections", url: "connectedpapers.com", pricing: "Freemium", rating: 4.4, tags: ["visualization", "connections", "discovery"]},
    {name: "Zotero", category: "Research", subcategory: "Reference", desc: "Reference manager", url: "zotero.org", pricing: "Free", rating: 4.6, tags: ["reference", "free", "open-source"]},
    {name: "Mendeley", category: "Research", subcategory: "Reference", desc: "Reference manager", url: "mendeley.com", pricing: "Freemium", rating: 4.3, tags: ["reference", "elsevier", "network"]},
    {name: "EndNote", category: "Research", subcategory: "Reference", desc: "Reference software", url: "endnote.com", pricing: "Paid", rating: 4.1, tags: ["reference", "enterprise", "legacy"]},
    {name: "Paperpile", category: "Research", subcategory: "Reference", desc: "Modern reference manager", url: "paperpile.com", pricing: "Paid", rating: 4.4, tags: ["reference", "google-docs", "modern"]},
    {name: "RefWorks", category: "Research", subcategory: "Reference", desc: "Reference management", url: "refworks.proquest.com", pricing: "Paid", rating: 4.0, tags: ["reference", "institution", "proquest"]},
    {name: "Overleaf", category: "Research", subcategory: "LaTeX", desc: "Online LaTeX editor", url: "overleaf.com", pricing: "Freemium", rating: 4.6, tags: ["latex", "collaborative", "academic"]},
    {name: "Authorea", category: "Research", subcategory: "Writing", desc: "Collaborative research writing", url: "authorea.com", pricing: "Freemium", rating: 4.2, tags: ["writing", "collaborative", "publishing"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE29 = AI_TOOLS_PHASE29;
}


