// Additional Git Repositories Database - Part 4
// Mega collection with trending and niche projects

const GIT_REPOS_DATABASE_4 = {
    // ==================== AI AGENTS & ORCHESTRATION ====================
    ai_agents: [
        {name: "MetaGPT", org: "geekan", desc: "Multi-agent framework for software company simulation", url: "https://github.com/geekan/MetaGPT", stars: "38K+", language: "Python", topics: ["agents", "multi-agent", "software-dev"], difficulty: "Advanced", featured: true},
        {name: "AgentGPT", org: "reworkd", desc: "Autonomous AI Agent in browser", url: "https://github.com/reworkd/AgentGPT", stars: "29K+", language: "TypeScript", topics: ["agents", "web", "autonomous"], difficulty: "Intermediate", featured: true},
        {name: "BabyAGI", org: "yoheinakajima", desc: "AI-powered task management", url: "https://github.com/yoheinakajima/babyagi", stars: "19K+", language: "Python", topics: ["agents", "task-management", "autonomous"], difficulty: "Intermediate", featured: true},
        {name: "SuperAGI", org: "TransformerOptimus", desc: "Open-source AGI framework", url: "https://github.com/TransformerOptimus/SuperAGI", stars: "14K+", language: "Python", topics: ["agents", "framework", "tools"], difficulty: "Advanced", featured: true},
        {name: "AgentScope", org: "modelscope", desc: "Multi-agent collaboration platform", url: "https://github.com/modelscope/agentscope", stars: "3K+", language: "Python", topics: ["multi-agent", "research"], difficulty: "Advanced", featured: false},
        {name: "Semantic Kernel", org: "microsoft", desc: "AI orchestration SDK", url: "https://github.com/microsoft/semantic-kernel", stars: "18K+", language: "C#", topics: ["llm", "orchestration", "plugins"], difficulty: "Intermediate", featured: true},
        {name: "AutoGen", org: "microsoft", desc: "Multi-agent conversation framework", url: "https://github.com/microsoft/autogen", stars: "25K+", language: "Python", topics: ["agents", "conversation", "llm"], difficulty: "Intermediate", featured: true},
        {name: "TaskWeaver", org: "microsoft", desc: "Code-first agent framework", url: "https://github.com/microsoft/TaskWeaver", stars: "5K+", language: "Python", topics: ["agents", "code-generation"], difficulty: "Intermediate", featured: false},
        {name: "Phidata", org: "phidatahq", desc: "Build AI Assistants with memory", url: "https://github.com/phidatahq/phidata", stars: "8K+", language: "Python", topics: ["agents", "memory", "assistants"], difficulty: "Beginner", featured: true},
        {name: "Composio", org: "ComposioHQ", desc: "Integration platform for AI agents", url: "https://github.com/ComposioHQ/composio", stars: "5K+", language: "Python", topics: ["agents", "integrations", "tools"], difficulty: "Beginner", featured: false},
    ],

    // ==================== NLP & TEXT PROCESSING ====================
    nlp: [
        {name: "spaCy", org: "explosion", desc: "Industrial-strength NLP", url: "https://github.com/explosion/spaCy", stars: "28K+", language: "Python", topics: ["nlp", "ner", "pos-tagging"], difficulty: "Intermediate", featured: true},
        {name: "NLTK", org: "nltk", desc: "Natural Language Toolkit", url: "https://github.com/nltk/nltk", stars: "13K+", language: "Python", topics: ["nlp", "tokenization", "linguistics"], difficulty: "Beginner", featured: true},
        {name: "Gensim", org: "piskvorky", desc: "Topic modelling for humans", url: "https://github.com/piskvorky/gensim", stars: "15K+", language: "Python", topics: ["nlp", "word2vec", "topic-modelling"], difficulty: "Intermediate", featured: false},
        {name: "TextBlob", org: "sloria", desc: "Simple text processing", url: "https://github.com/sloria/TextBlob", stars: "9K+", language: "Python", topics: ["nlp", "sentiment", "beginner"], difficulty: "Beginner", featured: false},
        {name: "Sentence Transformers", org: "UKPLab", desc: "State-of-art text embeddings", url: "https://github.com/UKPLab/sentence-transformers", stars: "13K+", language: "Python", topics: ["embeddings", "similarity", "search"], difficulty: "Intermediate", featured: true},
        {name: "Instructor", org: "jxnl", desc: "Structured outputs from LLMs", url: "https://github.com/jxnl/instructor", stars: "5K+", language: "Python", topics: ["llm", "structured-output", "pydantic"], difficulty: "Intermediate", featured: true},
        {name: "Outlines", org: "outlines-dev", desc: "Structured text generation", url: "https://github.com/outlines-dev/outlines", stars: "6K+", language: "Python", topics: ["llm", "json-output", "grammar"], difficulty: "Intermediate", featured: true},
        {name: "DSPy", org: "stanfordnlp", desc: "Programming with foundation models", url: "https://github.com/stanfordnlp/dspy", stars: "11K+", language: "Python", topics: ["llm", "prompting", "optimization"], difficulty: "Advanced", featured: true},
        {name: "Marvin", org: "PrefectHQ", desc: "Build AI interfaces that spark joy", url: "https://github.com/PrefectHQ/marvin", stars: "5K+", language: "Python", topics: ["llm", "ai-interface", "tools"], difficulty: "Beginner", featured: false},
        {name: "Presidio", org: "microsoft", desc: "Data protection and PII anonymization", url: "https://github.com/microsoft/presidio", stars: "3K+", language: "Python", topics: ["pii", "privacy", "anonymization"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== STATE MANAGEMENT ====================
    state_management: [
        {name: "Redux", org: "reduxjs", desc: "Predictable state container for JS", url: "https://github.com/reduxjs/redux", stars: "60K+", language: "TypeScript", topics: ["state", "react", "flux"], difficulty: "Intermediate", featured: true},
        {name: "Zustand", org: "pmndrs", desc: "Bear necessities state management", url: "https://github.com/pmndrs/zustand", stars: "42K+", language: "TypeScript", topics: ["state", "react", "simple"], difficulty: "Beginner", featured: true},
        {name: "Jotai", org: "pmndrs", desc: "Primitive and flexible state", url: "https://github.com/pmndrs/jotai", stars: "17K+", language: "TypeScript", topics: ["state", "atoms", "react"], difficulty: "Beginner", featured: true},
        {name: "Recoil", org: "facebookexperimental", desc: "Experimental state management", url: "https://github.com/facebookexperimental/Recoil", stars: "19K+", language: "TypeScript", topics: ["state", "react", "atoms"], difficulty: "Intermediate", featured: false},
        {name: "MobX", org: "mobxjs", desc: "Simple, scalable state management", url: "https://github.com/mobxjs/mobx", stars: "27K+", language: "TypeScript", topics: ["state", "reactive", "observable"], difficulty: "Intermediate", featured: false},
        {name: "Valtio", org: "pmndrs", desc: "Proxy-state made simple", url: "https://github.com/pmndrs/valtio", stars: "8K+", language: "TypeScript", topics: ["state", "proxy", "react"], difficulty: "Beginner", featured: false},
        {name: "XState", org: "statelyai", desc: "State machines and statecharts", url: "https://github.com/statelyai/xstate", stars: "26K+", language: "TypeScript", topics: ["state-machines", "statecharts"], difficulty: "Advanced", featured: true},
        {name: "Pinia", org: "vuejs", desc: "Vue Store", url: "https://github.com/vuejs/pinia", stars: "12K+", language: "TypeScript", topics: ["vue", "state", "store"], difficulty: "Beginner", featured: true},
        {name: "Signals", org: "preactjs", desc: "Reactive primitives", url: "https://github.com/preactjs/signals", stars: "3K+", language: "TypeScript", topics: ["reactive", "signals", "state"], difficulty: "Beginner", featured: false},
        {name: "Legend State", org: "LegendApp", desc: "Super fast state for React", url: "https://github.com/LegendApp/legend-state", stars: "2K+", language: "TypeScript", topics: ["state", "fast", "sync"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== FORM HANDLING ====================
    forms: [
        {name: "React Hook Form", org: "react-hook-form", desc: "Performant form validation", url: "https://github.com/react-hook-form/react-hook-form", stars: "39K+", language: "TypeScript", topics: ["forms", "validation", "react"], difficulty: "Beginner", featured: true},
        {name: "Formik", org: "jaredpalmer", desc: "Build forms in React", url: "https://github.com/jaredpalmer/formik", stars: "33K+", language: "TypeScript", topics: ["forms", "react", "validation"], difficulty: "Beginner", featured: true},
        {name: "Zod", org: "colinhacks", desc: "TypeScript-first schema validation", url: "https://github.com/colinhacks/zod", stars: "30K+", language: "TypeScript", topics: ["validation", "schema", "typescript"], difficulty: "Beginner", featured: true},
        {name: "Yup", org: "jquense", desc: "Schema builder for validation", url: "https://github.com/jquense/yup", stars: "22K+", language: "TypeScript", topics: ["validation", "schema"], difficulty: "Beginner", featured: false},
        {name: "Vee-Validate", org: "logaretm", desc: "Form validation for Vue", url: "https://github.com/logaretm/vee-validate", stars: "10K+", language: "TypeScript", topics: ["vue", "forms", "validation"], difficulty: "Beginner", featured: false},
        {name: "Final Form", org: "final-form", desc: "Framework agnostic form state", url: "https://github.com/final-form/final-form", stars: "3K+", language: "JavaScript", topics: ["forms", "state"], difficulty: "Intermediate", featured: false},
        {name: "Vest", org: "ealush", desc: "Declarative validations framework", url: "https://github.com/ealush/vest", stars: "2K+", language: "TypeScript", topics: ["validation", "unit-test-like"], difficulty: "Beginner", featured: false},
        {name: "TypeBox", org: "sinclairzx81", desc: "JSON Schema Type Builder", url: "https://github.com/sinclairzx81/typebox", stars: "4K+", language: "TypeScript", topics: ["json-schema", "validation"], difficulty: "Intermediate", featured: false},
        {name: "Valibot", org: "fabian-hiller", desc: "Modular schema library", url: "https://github.com/fabian-hiller/valibot", stars: "5K+", language: "TypeScript", topics: ["validation", "modular", "small"], difficulty: "Beginner", featured: true},
        {name: "ArkType", org: "arktypeio", desc: "TypeScript's 1:1 validator", url: "https://github.com/arktypeio/arktype", stars: "3K+", language: "TypeScript", topics: ["validation", "typescript"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== CODE EDITORS & IDEs ====================
    code_editors: [
        {name: "Monaco Editor", org: "microsoft", desc: "VS Code's code editor", url: "https://github.com/microsoft/monaco-editor", stars: "38K+", language: "TypeScript", topics: ["editor", "vscode", "web"], difficulty: "Intermediate", featured: true},
        {name: "CodeMirror", org: "codemirror", desc: "In-browser code editor", url: "https://github.com/codemirror/dev", stars: "5K+", language: "TypeScript", topics: ["editor", "browser", "extensible"], difficulty: "Intermediate", featured: true},
        {name: "Ace Editor", org: "ajaxorg", desc: "Standalone code editor", url: "https://github.com/ajaxorg/ace", stars: "26K+", language: "JavaScript", topics: ["editor", "syntax-highlighting"], difficulty: "Intermediate", featured: false},
        {name: "Prism", org: "PrismJS", desc: "Lightweight syntax highlighter", url: "https://github.com/PrismJS/prism", stars: "12K+", language: "JavaScript", topics: ["syntax-highlighting", "code"], difficulty: "Beginner", featured: false},
        {name: "Highlight.js", org: "highlightjs", desc: "Syntax highlighting for the web", url: "https://github.com/highlightjs/highlight.js", stars: "23K+", language: "JavaScript", topics: ["syntax-highlighting", "code"], difficulty: "Beginner", featured: true},
        {name: "Shiki", org: "shikijs", desc: "Beautiful syntax highlighter", url: "https://github.com/shikijs/shiki", stars: "8K+", language: "TypeScript", topics: ["syntax-highlighting", "textmate"], difficulty: "Beginner", featured: true},
        {name: "Sandpack", org: "codesandbox", desc: "Component toolkit for code editing", url: "https://github.com/codesandbox/sandpack", stars: "4K+", language: "TypeScript", topics: ["sandbox", "react", "playground"], difficulty: "Intermediate", featured: true},
        {name: "StackBlitz SDK", org: "stackblitz", desc: "Web-based IDE SDK", url: "https://github.com/stackblitz/sdk", stars: "800+", language: "TypeScript", topics: ["ide", "web", "embedding"], difficulty: "Beginner", featured: false},
    ],

    // ==================== E-COMMERCE ====================
    ecommerce: [
        {name: "Medusa", org: "medusajs", desc: "Open source Shopify alternative", url: "https://github.com/medusajs/medusa", stars: "22K+", language: "TypeScript", topics: ["ecommerce", "headless", "commerce"], difficulty: "Intermediate", featured: true},
        {name: "Saleor", org: "saleor", desc: "GraphQL-first e-commerce platform", url: "https://github.com/saleor/saleor", stars: "20K+", language: "Python", topics: ["ecommerce", "graphql", "django"], difficulty: "Intermediate", featured: true},
        {name: "Vendure", org: "vendure-ecommerce", desc: "Headless commerce framework", url: "https://github.com/vendure-ecommerce/vendure", stars: "5K+", language: "TypeScript", topics: ["ecommerce", "graphql", "nestjs"], difficulty: "Intermediate", featured: true},
        {name: "Solidus", org: "solidusio", desc: "Rails e-commerce platform", url: "https://github.com/solidusio/solidus", stars: "5K+", language: "Ruby", topics: ["ecommerce", "rails"], difficulty: "Intermediate", featured: false},
        {name: "Sylius", org: "Sylius", desc: "Open source e-commerce PHP", url: "https://github.com/Sylius/Sylius", stars: "7K+", language: "PHP", topics: ["ecommerce", "symfony"], difficulty: "Intermediate", featured: false},
        {name: "Spree", org: "spree", desc: "Open source e-commerce for Ruby", url: "https://github.com/spree/spree", stars: "13K+", language: "Ruby", topics: ["ecommerce", "rails", "api"], difficulty: "Intermediate", featured: false},
        {name: "PrestaShop", org: "PrestaShop", desc: "E-commerce solution", url: "https://github.com/PrestaShop/PrestaShop", stars: "8K+", language: "PHP", topics: ["ecommerce", "php"], difficulty: "Intermediate", featured: false},
        {name: "Commerce.js", org: "chec", desc: "Headless commerce SDK", url: "https://github.com/chec/commerce.js", stars: "700+", language: "JavaScript", topics: ["ecommerce", "sdk", "headless"], difficulty: "Beginner", featured: false},
    ],

    // ==================== PDF & DOCUMENT GENERATION ====================
    pdf_docs: [
        {name: "PDF.js", org: "mozilla", desc: "PDF reader in JavaScript", url: "https://github.com/mozilla/pdf.js", stars: "46K+", language: "JavaScript", topics: ["pdf", "viewer", "rendering"], difficulty: "Intermediate", featured: true},
        {name: "jsPDF", org: "parallax", desc: "Generate PDFs in JavaScript", url: "https://github.com/parallax/jspdf", stars: "28K+", language: "JavaScript", topics: ["pdf", "generation", "client-side"], difficulty: "Beginner", featured: true},
        {name: "React-PDF", org: "diegomura", desc: "Create PDFs with React", url: "https://github.com/diegomura/react-pdf", stars: "14K+", language: "JavaScript", topics: ["pdf", "react", "generation"], difficulty: "Beginner", featured: true},
        {name: "PDFKit", org: "foliojs", desc: "PDF generation library for Node", url: "https://github.com/foliojs/pdfkit", stars: "9K+", language: "JavaScript", topics: ["pdf", "node", "generation"], difficulty: "Intermediate", featured: false},
        {name: "Puppeteer PDF", org: "puppeteer", desc: "Chrome PDF generation", url: "https://github.com/puppeteer/puppeteer", stars: "86K+", language: "TypeScript", topics: ["pdf", "headless", "chrome"], difficulty: "Intermediate", featured: true},
        {name: "WeasyPrint", org: "Kozea", desc: "PDF generation from HTML+CSS", url: "https://github.com/Kozea/WeasyPrint", stars: "6K+", language: "Python", topics: ["pdf", "html", "css"], difficulty: "Intermediate", featured: false},
        {name: "Docxtemplater", org: "open-xml-templating", desc: "Generate docx/pptx from templates", url: "https://github.com/open-xml-templating/docxtemplater", stars: "3K+", language: "JavaScript", topics: ["docx", "templates"], difficulty: "Intermediate", featured: false},
        {name: "Gotenberg", org: "gotenberg", desc: "Docker-powered PDF generation", url: "https://github.com/gotenberg/gotenberg", stars: "6K+", language: "Go", topics: ["pdf", "docker", "api"], difficulty: "Intermediate", featured: true},
        {name: "Typst", org: "typst", desc: "New markup-based typesetting system", url: "https://github.com/typst/typst", stars: "28K+", language: "Rust", topics: ["typesetting", "latex-alternative", "pdf"], difficulty: "Beginner", featured: true},
    ],

    // ==================== EMAIL ====================
    email: [
        {name: "Nodemailer", org: "nodemailer", desc: "Send emails from Node.js", url: "https://github.com/nodemailer/nodemailer", stars: "16K+", language: "JavaScript", topics: ["email", "smtp", "node"], difficulty: "Beginner", featured: true},
        {name: "React Email", org: "resend", desc: "Build emails using React", url: "https://github.com/resend/react-email", stars: "12K+", language: "TypeScript", topics: ["email", "react", "templates"], difficulty: "Beginner", featured: true},
        {name: "MJML", org: "mjmlio", desc: "Responsive email framework", url: "https://github.com/mjmlio/mjml", stars: "16K+", language: "JavaScript", topics: ["email", "responsive", "markup"], difficulty: "Beginner", featured: true},
        {name: "Mailtrain", org: "Mailtrain-org", desc: "Self-hosted newsletter app", url: "https://github.com/Mailtrain-org/mailtrain", stars: "5K+", language: "JavaScript", topics: ["email", "newsletter", "self-hosted"], difficulty: "Intermediate", featured: false},
        {name: "Mailcow", org: "mailcow", desc: "Docker mail server", url: "https://github.com/mailcow/mailcow-dockerized", stars: "7K+", language: "PHP", topics: ["email", "server", "docker"], difficulty: "Advanced", featured: false},
        {name: "Postal", org: "postalserver", desc: "Mail server for developers", url: "https://github.com/postalserver/postal", stars: "14K+", language: "Ruby", topics: ["email", "smtp", "server"], difficulty: "Advanced", featured: false},
        {name: "Mautic", org: "mautic", desc: "Open source marketing automation", url: "https://github.com/mautic/mautic", stars: "6K+", language: "PHP", topics: ["email", "marketing", "automation"], difficulty: "Intermediate", featured: false},
        {name: "Listmonk", org: "knadh", desc: "Self-hosted newsletter manager", url: "https://github.com/knadh/listmonk", stars: "13K+", language: "Go", topics: ["email", "newsletter", "mailing-list"], difficulty: "Beginner", featured: true},
    ],

    // ==================== SCHEDULING & CALENDARS ====================
    scheduling: [
        {name: "Cal.com", org: "calcom", desc: "Open source Calendly alternative", url: "https://github.com/calcom/cal.com", stars: "28K+", language: "TypeScript", topics: ["scheduling", "calendar", "booking"], difficulty: "Intermediate", featured: true},
        {name: "FullCalendar", org: "fullcalendar", desc: "Full-featured calendar library", url: "https://github.com/fullcalendar/fullcalendar", stars: "17K+", language: "TypeScript", topics: ["calendar", "events", "ui"], difficulty: "Beginner", featured: true},
        {name: "Day.js", org: "iamkun", desc: "Fast 2kB date library", url: "https://github.com/iamkun/dayjs", stars: "45K+", language: "JavaScript", topics: ["date", "time", "lightweight"], difficulty: "Beginner", featured: true},
        {name: "date-fns", org: "date-fns", desc: "Modern date utility library", url: "https://github.com/date-fns/date-fns", stars: "33K+", language: "TypeScript", topics: ["date", "time", "modular"], difficulty: "Beginner", featured: true},
        {name: "Luxon", org: "moment", desc: "Modern date time library", url: "https://github.com/moment/luxon", stars: "15K+", language: "JavaScript", topics: ["date", "time", "timezone"], difficulty: "Beginner", featured: false},
        {name: "Cron Parser", org: "harrisiirak", desc: "Node.js cron expression parser", url: "https://github.com/harrisiirak/cron-parser", stars: "2K+", language: "JavaScript", topics: ["cron", "scheduling"], difficulty: "Beginner", featured: false},
        {name: "Node Schedule", org: "node-schedule", desc: "Job scheduler for Node.js", url: "https://github.com/node-schedule/node-schedule", stars: "9K+", language: "JavaScript", topics: ["scheduling", "cron", "jobs"], difficulty: "Beginner", featured: false},
        {name: "Agenda", org: "agenda", desc: "Lightweight job scheduling", url: "https://github.com/agenda/agenda", stars: "9K+", language: "JavaScript", topics: ["jobs", "scheduling", "mongodb"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== PAYMENTS ====================
    payments: [
        {name: "Stripe Node", org: "stripe", desc: "Stripe API library for Node", url: "https://github.com/stripe/stripe-node", stars: "3K+", language: "TypeScript", topics: ["payments", "stripe", "api"], difficulty: "Beginner", featured: true},
        {name: "Stripe React", org: "stripe", desc: "React components for Stripe", url: "https://github.com/stripe/react-stripe-js", stars: "1K+", language: "TypeScript", topics: ["payments", "stripe", "react"], difficulty: "Beginner", featured: false},
        {name: "Paddle Node", org: "paddle", desc: "Paddle API client", url: "https://github.com/paddle-billing/paddle-node-sdk", stars: "100+", language: "TypeScript", topics: ["payments", "billing", "saas"], difficulty: "Beginner", featured: false},
        {name: "LemonSqueezy.js", org: "lmsqueezy", desc: "LemonSqueezy JavaScript SDK", url: "https://github.com/lmsqueezy/lemonsqueezy.js", stars: "200+", language: "TypeScript", topics: ["payments", "saas", "billing"], difficulty: "Beginner", featured: false},
        {name: "Kill Bill", org: "killbill", desc: "Open source billing platform", url: "https://github.com/killbill/killbill", stars: "4K+", language: "Java", topics: ["billing", "subscriptions"], difficulty: "Advanced", featured: false},
        {name: "Lago", org: "getlago", desc: "Open source metering & billing", url: "https://github.com/getlago/lago", stars: "6K+", language: "Ruby", topics: ["billing", "metering", "usage-based"], difficulty: "Intermediate", featured: true},
        {name: "Hyperswitch", org: "juspay", desc: "Open source payments switch", url: "https://github.com/juspay/hyperswitch", stars: "10K+", language: "Rust", topics: ["payments", "gateway", "orchestration"], difficulty: "Advanced", featured: true},
    ],

    // ==================== MAPS & GEOLOCATION ====================
    maps_geo: [
        {name: "Leaflet", org: "Leaflet", desc: "Mobile-friendly interactive maps", url: "https://github.com/Leaflet/Leaflet", stars: "39K+", language: "JavaScript", topics: ["maps", "interactive", "mobile"], difficulty: "Beginner", featured: true},
        {name: "MapLibre GL", org: "maplibre", desc: "Open source map rendering", url: "https://github.com/maplibre/maplibre-gl-js", stars: "6K+", language: "TypeScript", topics: ["maps", "webgl", "vector"], difficulty: "Intermediate", featured: true},
        {name: "Deck.gl", org: "visgl", desc: "Large-scale data visualization", url: "https://github.com/visgl/deck.gl", stars: "11K+", language: "JavaScript", topics: ["visualization", "webgl", "geospatial"], difficulty: "Advanced", featured: true},
        {name: "Turf.js", org: "Turfjs", desc: "Geospatial analysis library", url: "https://github.com/Turfjs/turf", stars: "8K+", language: "JavaScript", topics: ["geospatial", "analysis", "gis"], difficulty: "Intermediate", featured: false},
        {name: "OpenLayers", org: "openlayers", desc: "High-performance web mapping", url: "https://github.com/openlayers/openlayers", stars: "11K+", language: "JavaScript", topics: ["maps", "gis", "wms"], difficulty: "Intermediate", featured: false},
        {name: "H3", org: "uber", desc: "Hexagonal hierarchical geospatial", url: "https://github.com/uber/h3", stars: "4K+", language: "C", topics: ["geospatial", "hexagonal", "indexing"], difficulty: "Advanced", featured: false},
        {name: "GeoJSON", org: "mapbox", desc: "GeoJSON utilities", url: "https://github.com/mapbox/geojson.io", stars: "2K+", language: "JavaScript", topics: ["geojson", "maps", "editor"], difficulty: "Beginner", featured: false},
        {name: "React Map GL", org: "visgl", desc: "React wrapper for Mapbox", url: "https://github.com/visgl/react-map-gl", stars: "7K+", language: "TypeScript", topics: ["maps", "react", "mapbox"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== NOTIFICATION & ALERTS ====================
    notifications: [
        {name: "Novu", org: "novuhq", desc: "Open source notification infrastructure", url: "https://github.com/novuhq/novu", stars: "33K+", language: "TypeScript", topics: ["notifications", "email", "sms", "push"], difficulty: "Intermediate", featured: true},
        {name: "React Toastify", org: "fkhadra", desc: "Toast notifications for React", url: "https://github.com/fkhadra/react-toastify", stars: "12K+", language: "TypeScript", topics: ["notifications", "toast", "react"], difficulty: "Beginner", featured: true},
        {name: "Sonner", org: "emilkowalski", desc: "Opinionated toast component", url: "https://github.com/emilkowalski/sonner", stars: "7K+", language: "TypeScript", topics: ["toast", "notifications", "react"], difficulty: "Beginner", featured: true},
        {name: "Notistack", org: "iamhosseindhv", desc: "Highly customizable notification snackbars", url: "https://github.com/iamhosseindhv/notistack", stars: "4K+", language: "TypeScript", topics: ["notifications", "mui", "snackbar"], difficulty: "Beginner", featured: false},
        {name: "Apprise", org: "caronc", desc: "Push notification library", url: "https://github.com/caronc/apprise", stars: "10K+", language: "Python", topics: ["notifications", "multi-platform"], difficulty: "Beginner", featured: true},
        {name: "Ntfy", org: "binwiederhier", desc: "Simple HTTP-based pub-sub", url: "https://github.com/binwiederhier/ntfy", stars: "16K+", language: "Go", topics: ["notifications", "pub-sub", "self-hosted"], difficulty: "Beginner", featured: true},
        {name: "Gotify", org: "gotify", desc: "Self-hosted push notification server", url: "https://github.com/gotify/server", stars: "10K+", language: "Go", topics: ["notifications", "push", "self-hosted"], difficulty: "Intermediate", featured: false},
        {name: "Pushover", org: "pushover", desc: "Simple push notification API", url: "https://pushover.net/", stars: "N/A", language: "API", topics: ["notifications", "push", "mobile"], difficulty: "Beginner", featured: false},
    ],

    // ==================== INTERNATIONALIZATION ====================
    i18n: [
        {name: "i18next", org: "i18next", desc: "Internationalization framework", url: "https://github.com/i18next/i18next", stars: "7K+", language: "JavaScript", topics: ["i18n", "localization", "translation"], difficulty: "Beginner", featured: true},
        {name: "React-Intl", org: "formatjs", desc: "Internationalize React apps", url: "https://github.com/formatjs/formatjs", stars: "14K+", language: "TypeScript", topics: ["i18n", "react", "intl"], difficulty: "Intermediate", featured: true},
        {name: "Lingui", org: "lingui", desc: "Seamless internationalization", url: "https://github.com/lingui/js-lingui", stars: "4K+", language: "TypeScript", topics: ["i18n", "react", "cli"], difficulty: "Intermediate", featured: false},
        {name: "Vue I18n", org: "intlify", desc: "Internationalization for Vue", url: "https://github.com/intlify/vue-i18n-next", stars: "2K+", language: "TypeScript", topics: ["i18n", "vue", "composition-api"], difficulty: "Beginner", featured: false},
        {name: "Polyglot.js", org: "airbnb", desc: "Tiny I18n library", url: "https://github.com/airbnb/polyglot.js", stars: "4K+", language: "JavaScript", topics: ["i18n", "lightweight"], difficulty: "Beginner", featured: false},
        {name: "Tolgee", org: "tolgee", desc: "Open source localization platform", url: "https://github.com/tolgee/tolgee-platform", stars: "1K+", language: "Kotlin", topics: ["i18n", "platform", "translation"], difficulty: "Intermediate", featured: true},
        {name: "Crowdin", org: "crowdin", desc: "Localization management platform", url: "https://github.com/crowdin/crowdin-api-client-js", stars: "100+", language: "TypeScript", topics: ["i18n", "api", "management"], difficulty: "Beginner", featured: false},
    ],

    // ==================== UTILITIES & HELPERS ====================
    utilities: [
        {name: "Lodash", org: "lodash", desc: "Modern JavaScript utility library", url: "https://github.com/lodash/lodash", stars: "59K+", language: "JavaScript", topics: ["utilities", "functional", "helpers"], difficulty: "Beginner", featured: true},
        {name: "Ramda", org: "ramda", desc: "Practical functional library", url: "https://github.com/ramda/ramda", stars: "23K+", language: "JavaScript", topics: ["functional", "fp", "utilities"], difficulty: "Intermediate", featured: false},
        {name: "Underscore", org: "jashkenas", desc: "JavaScript's utility belt", url: "https://github.com/jashkenas/underscore", stars: "27K+", language: "JavaScript", topics: ["utilities", "functional"], difficulty: "Beginner", featured: false},
        {name: "Radash", org: "rayepps", desc: "Lodash replacement for TypeScript", url: "https://github.com/rayepps/radash", stars: "3K+", language: "TypeScript", topics: ["utilities", "typescript"], difficulty: "Beginner", featured: true},
        {name: "ts-belt", org: "mobily", desc: "Fast, modern TypeScript utilities", url: "https://github.com/mobily/ts-belt", stars: "3K+", language: "TypeScript", topics: ["utilities", "fp", "typescript"], difficulty: "Intermediate", featured: false},
        {name: "Remeda", org: "remeda", desc: "First utility library designed for TypeScript", url: "https://github.com/remeda/remeda", stars: "3K+", language: "TypeScript", topics: ["utilities", "typescript", "fp"], difficulty: "Beginner", featured: false},
        {name: "just", org: "angus-c", desc: "Dependency-free utilities", url: "https://github.com/angus-c/just", stars: "6K+", language: "JavaScript", topics: ["utilities", "modular", "zero-dep"], difficulty: "Beginner", featured: false},
        {name: "change-case", org: "blakeembrey", desc: "Transform strings between cases", url: "https://github.com/blakeembrey/change-case", stars: "2K+", language: "TypeScript", topics: ["string", "utilities"], difficulty: "Beginner", featured: false},
        {name: "nanoid", org: "ai", desc: "Tiny unique ID generator", url: "https://github.com/ai/nanoid", stars: "23K+", language: "JavaScript", topics: ["id", "uuid", "tiny"], difficulty: "Beginner", featured: true},
        {name: "uuid", org: "uuidjs", desc: "RFC4122 UUIDs generator", url: "https://github.com/uuidjs/uuid", stars: "14K+", language: "JavaScript", topics: ["uuid", "id", "standard"], difficulty: "Beginner", featured: false},
    ]
};

// Merge with existing database
if (typeof window !== 'undefined') {
    window.GIT_REPOS_DATABASE_4 = GIT_REPOS_DATABASE_4;
}


