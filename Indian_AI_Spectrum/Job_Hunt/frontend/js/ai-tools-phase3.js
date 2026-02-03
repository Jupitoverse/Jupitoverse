// AI Tools Database - Phase 3: Coding, Development & Automation
// 200+ Tools for developers and technical professionals

const AI_TOOLS_PHASE3 = [
    // ==================== CODE ASSISTANTS ====================
    {name: "GitHub Copilot", category: "Coding", subcategory: "Code Assistant", desc: "AI pair programmer by GitHub/OpenAI", url: "github.com/features/copilot", pricing: "Paid", rating: 4.9, tags: ["coding", "autocomplete", "ide"], featured: true},
    {name: "Cursor", category: "Coding", subcategory: "AI IDE", desc: "AI-first code editor built for pair programming", url: "cursor.sh", pricing: "Freemium", rating: 4.8, tags: ["ide", "chat", "refactor"], featured: true},
    {name: "Codeium", category: "Coding", subcategory: "Code Assistant", desc: "Free AI code completion and chat", url: "codeium.com", pricing: "Free", rating: 4.7, tags: ["free", "autocomplete", "ide"], featured: true},
    {name: "Tabnine", category: "Coding", subcategory: "Code Assistant", desc: "AI code completion for teams", url: "tabnine.com", pricing: "Freemium", rating: 4.6, tags: ["teams", "autocomplete", "private"]},
    {name: "Amazon CodeWhisperer", category: "Coding", subcategory: "Code Assistant", desc: "AWS AI coding companion", url: "aws.amazon.com/codewhisperer", pricing: "Freemium", rating: 4.5, tags: ["aws", "security", "coding"]},
    {name: "Replit AI", category: "Coding", subcategory: "Code Assistant", desc: "AI coding assistant in Replit", url: "replit.com/ai", pricing: "Freemium", rating: 4.6, tags: ["browser", "collaborative", "learning"]},
    {name: "Sourcegraph Cody", category: "Coding", subcategory: "Code Assistant", desc: "AI coding assistant with codebase context", url: "sourcegraph.com/cody", pricing: "Freemium", rating: 4.5, tags: ["context", "enterprise", "search"]},
    {name: "Continue", category: "Coding", subcategory: "Code Assistant", desc: "Open-source AI code assistant", url: "continue.dev", pricing: "Free", rating: 4.4, tags: ["open-source", "customizable", "local"]},
    {name: "Aider", category: "Coding", subcategory: "Code Assistant", desc: "AI pair programming in terminal", url: "aider.chat", pricing: "Free", rating: 4.5, tags: ["terminal", "git", "open-source"]},
    {name: "Codex (OpenAI)", category: "Coding", subcategory: "Code Generation", desc: "OpenAI's code generation model", url: "openai.com/blog/openai-codex", pricing: "Paid", rating: 4.7, tags: ["api", "generation", "openai"]},
    {name: "StarCoder", category: "Coding", subcategory: "Open Source", desc: "Open-source code LLM by BigCode", url: "huggingface.co/bigcode", pricing: "Free", rating: 4.4, tags: ["open-source", "research", "llm"]},
    {name: "Code Llama", category: "Coding", subcategory: "Open Source", desc: "Meta's open-source code LLM", url: "ai.meta.com/code-llama", pricing: "Free", rating: 4.6, tags: ["open-source", "meta", "llm"]},
    {name: "Phind", category: "Coding", subcategory: "Code Search", desc: "AI search engine for developers", url: "phind.com", pricing: "Freemium", rating: 4.6, tags: ["search", "coding", "answers"]},
    {name: "Blackbox AI", category: "Coding", subcategory: "Code Assistant", desc: "AI code autocomplete and chat", url: "blackbox.ai", pricing: "Freemium", rating: 4.3, tags: ["autocomplete", "chat", "snippets"]},
    {name: "Codium AI", category: "Coding", subcategory: "Testing", desc: "AI-powered test generation", url: "codium.ai", pricing: "Freemium", rating: 4.5, tags: ["testing", "coverage", "quality"]},
    {name: "Pieces", category: "Coding", subcategory: "Code Snippets", desc: "AI-powered code snippet manager", url: "pieces.app", pricing: "Freemium", rating: 4.4, tags: ["snippets", "organization", "context"]},
    {name: "MutableAI", category: "Coding", subcategory: "Code Generation", desc: "AI for rapid software development", url: "mutable.ai", pricing: "Freemium", rating: 4.2, tags: ["generation", "prototyping", "speed"]},
    {name: "Safurai", category: "Coding", subcategory: "Code Assistant", desc: "AI coding assistant for VSCode", url: "safurai.com", pricing: "Free", rating: 4.2, tags: ["vscode", "free", "assistant"]},
    {name: "AskCodi", category: "Coding", subcategory: "Code Assistant", desc: "AI code assistant and generator", url: "askcodi.com", pricing: "Freemium", rating: 4.1, tags: ["generation", "explanation", "documentation"]},
    {name: "Whisperer", category: "Coding", subcategory: "Code Assistant", desc: "AI coding assistant for multiple IDEs", url: "whisperer.ai", pricing: "Freemium", rating: 4.0, tags: ["ide", "multi-platform", "assistant"]},
    
    // ==================== WEB DEVELOPMENT ====================
    {name: "v0.dev", category: "Web Dev", subcategory: "UI Generation", desc: "Generate React UI components with AI", url: "v0.dev", pricing: "Freemium", rating: 4.7, tags: ["react", "ui", "components"], featured: true},
    {name: "Vercel AI", category: "Web Dev", subcategory: "AI SDK", desc: "SDK for building AI applications", url: "sdk.vercel.ai", pricing: "Free", rating: 4.6, tags: ["sdk", "streaming", "react"]},
    {name: "Builder.io", category: "Web Dev", subcategory: "Visual Builder", desc: "AI-powered visual development", url: "builder.io", pricing: "Freemium", rating: 4.5, tags: ["visual", "cms", "components"]},
    {name: "Framer AI", category: "Web Dev", subcategory: "Website Builder", desc: "AI website generation and design", url: "framer.com", pricing: "Freemium", rating: 4.6, tags: ["website", "design", "no-code"]},
    {name: "Webflow", category: "Web Dev", subcategory: "Website Builder", desc: "Visual web development with AI features", url: "webflow.com", pricing: "Freemium", rating: 4.6, tags: ["visual", "design", "professional"]},
    {name: "Wix ADI", category: "Web Dev", subcategory: "Website Builder", desc: "AI website creation by Wix", url: "wix.com/adi", pricing: "Freemium", rating: 4.3, tags: ["website", "easy", "templates"]},
    {name: "Durable AI", category: "Web Dev", subcategory: "Website Builder", desc: "AI website builder in 30 seconds", url: "durable.co", pricing: "Paid", rating: 4.4, tags: ["fast", "business", "simple"]},
    {name: "10Web", category: "Web Dev", subcategory: "WordPress", desc: "AI WordPress website builder", url: "10web.io", pricing: "Paid", rating: 4.3, tags: ["wordpress", "hosting", "ai"]},
    {name: "Hostinger AI", category: "Web Dev", subcategory: "Website Builder", desc: "AI website builder by Hostinger", url: "hostinger.com/ai-website-builder", pricing: "Paid", rating: 4.3, tags: ["hosting", "website", "affordable"]},
    {name: "Zyro", category: "Web Dev", subcategory: "Website Builder", desc: "AI website builder with templates", url: "zyro.com", pricing: "Paid", rating: 4.2, tags: ["templates", "ecommerce", "easy"]},
    {name: "Teleporthq", category: "Web Dev", subcategory: "Code Generation", desc: "Generate code from designs", url: "teleporthq.io", pricing: "Freemium", rating: 4.3, tags: ["design-to-code", "react", "vue"]},
    {name: "Anima", category: "Web Dev", subcategory: "Design to Code", desc: "Convert Figma to code with AI", url: "animaapp.com", pricing: "Freemium", rating: 4.4, tags: ["figma", "react", "html"]},
    {name: "Locofy", category: "Web Dev", subcategory: "Design to Code", desc: "Turn designs into production code", url: "locofy.ai", pricing: "Freemium", rating: 4.5, tags: ["figma", "xd", "production"]},
    {name: "Windsurf", category: "Web Dev", subcategory: "AI IDE", desc: "AI-powered web development IDE", url: "codeium.com/windsurf", pricing: "Free", rating: 4.5, tags: ["ide", "flow", "agentic"]},
    {name: "bolt.new", category: "Web Dev", subcategory: "AI Development", desc: "Full-stack web apps in browser", url: "bolt.new", pricing: "Freemium", rating: 4.6, tags: ["full-stack", "browser", "instant"]},
    
    // ==================== MOBILE DEVELOPMENT ====================
    {name: "FlutterFlow", category: "Mobile Dev", subcategory: "App Builder", desc: "Visual app builder with AI features", url: "flutterflow.io", pricing: "Freemium", rating: 4.5, tags: ["flutter", "visual", "no-code"]},
    {name: "Bravo Studio", category: "Mobile Dev", subcategory: "App Builder", desc: "Convert Figma to mobile apps", url: "bravostudio.app", pricing: "Freemium", rating: 4.3, tags: ["figma", "no-code", "native"]},
    {name: "Adalo", category: "Mobile Dev", subcategory: "App Builder", desc: "No-code app builder with AI", url: "adalo.com", pricing: "Freemium", rating: 4.2, tags: ["no-code", "apps", "database"]},
    {name: "Thunkable", category: "Mobile Dev", subcategory: "App Builder", desc: "Cross-platform app development", url: "thunkable.com", pricing: "Freemium", rating: 4.2, tags: ["cross-platform", "visual", "education"]},
    {name: "Glide", category: "Mobile Dev", subcategory: "App Builder", desc: "Build apps from spreadsheets", url: "glideapps.com", pricing: "Freemium", rating: 4.4, tags: ["spreadsheet", "no-code", "fast"]},
    {name: "AppGyver", category: "Mobile Dev", subcategory: "App Builder", desc: "No-code platform by SAP", url: "appgyver.com", pricing: "Free", rating: 4.3, tags: ["sap", "professional", "free"]},
    {name: "BuildFire", category: "Mobile Dev", subcategory: "App Builder", desc: "Mobile app development platform", url: "buildfire.com", pricing: "Paid", rating: 4.1, tags: ["enterprise", "plugins", "custom"]},
    {name: "Draftbit", category: "Mobile Dev", subcategory: "App Builder", desc: "Build React Native apps visually", url: "draftbit.com", pricing: "Paid", rating: 4.2, tags: ["react-native", "visual", "export"]},
    {name: "Appmaker", category: "Mobile Dev", subcategory: "Shopify Apps", desc: "Mobile apps for Shopify stores", url: "appmaker.xyz", pricing: "Paid", rating: 4.1, tags: ["shopify", "ecommerce", "mobile"]},
    {name: "GoodBarber", category: "Mobile Dev", subcategory: "App Builder", desc: "No-code iOS and Android apps", url: "goodbarber.com", pricing: "Paid", rating: 4.0, tags: ["ios", "android", "pwa"]},
    
    // ==================== DATABASE & BACKEND ====================
    {name: "Supabase", category: "Backend", subcategory: "BaaS", desc: "Open-source Firebase alternative with AI", url: "supabase.com", pricing: "Freemium", rating: 4.7, tags: ["postgres", "auth", "realtime"], featured: true},
    {name: "Firebase", category: "Backend", subcategory: "BaaS", desc: "Google's app development platform", url: "firebase.google.com", pricing: "Freemium", rating: 4.6, tags: ["google", "realtime", "hosting"]},
    {name: "PlanetScale", category: "Backend", subcategory: "Database", desc: "Serverless MySQL with AI features", url: "planetscale.com", pricing: "Freemium", rating: 4.6, tags: ["mysql", "serverless", "branching"]},
    {name: "Neon", category: "Backend", subcategory: "Database", desc: "Serverless Postgres with AI", url: "neon.tech", pricing: "Freemium", rating: 4.5, tags: ["postgres", "serverless", "branching"]},
    {name: "Xata", category: "Backend", subcategory: "Database", desc: "Serverless database with search and AI", url: "xata.io", pricing: "Freemium", rating: 4.4, tags: ["search", "ai", "serverless"]},
    {name: "Railway", category: "Backend", subcategory: "Deployment", desc: "Deploy apps and databases easily", url: "railway.app", pricing: "Freemium", rating: 4.5, tags: ["deployment", "easy", "databases"]},
    {name: "Render", category: "Backend", subcategory: "Deployment", desc: "Cloud platform for apps and services", url: "render.com", pricing: "Freemium", rating: 4.5, tags: ["deployment", "simple", "auto-scaling"]},
    {name: "Fly.io", category: "Backend", subcategory: "Deployment", desc: "Deploy apps close to users globally", url: "fly.io", pricing: "Freemium", rating: 4.5, tags: ["edge", "global", "containers"]},
    {name: "Appwrite", category: "Backend", subcategory: "BaaS", desc: "Open-source backend server", url: "appwrite.io", pricing: "Freemium", rating: 4.5, tags: ["open-source", "self-hosted", "functions"]},
    {name: "Hasura", category: "Backend", subcategory: "GraphQL", desc: "Instant GraphQL APIs on databases", url: "hasura.io", pricing: "Freemium", rating: 4.5, tags: ["graphql", "instant", "postgres"]},
    
    // ==================== API & INTEGRATION ====================
    {name: "Postman", category: "API", subcategory: "API Testing", desc: "API platform with AI features", url: "postman.com", pricing: "Freemium", rating: 4.7, tags: ["testing", "collaboration", "documentation"], featured: true},
    {name: "Insomnia", category: "API", subcategory: "API Testing", desc: "API client for REST and GraphQL", url: "insomnia.rest", pricing: "Freemium", rating: 4.5, tags: ["rest", "graphql", "open-source"]},
    {name: "RapidAPI", category: "API", subcategory: "API Marketplace", desc: "Marketplace for APIs", url: "rapidapi.com", pricing: "Freemium", rating: 4.4, tags: ["marketplace", "apis", "hub"]},
    {name: "Zapier", category: "API", subcategory: "Automation", desc: "Connect apps and automate workflows", url: "zapier.com", pricing: "Freemium", rating: 4.7, tags: ["automation", "integration", "no-code"], featured: true},
    {name: "Make (Integromat)", category: "API", subcategory: "Automation", desc: "Visual automation platform", url: "make.com", pricing: "Freemium", rating: 4.6, tags: ["automation", "visual", "powerful"]},
    {name: "n8n", category: "API", subcategory: "Automation", desc: "Open-source workflow automation", url: "n8n.io", pricing: "Freemium", rating: 4.5, tags: ["open-source", "self-hosted", "automation"]},
    {name: "Pipedream", category: "API", subcategory: "Automation", desc: "Connect APIs with code and no-code", url: "pipedream.com", pricing: "Freemium", rating: 4.4, tags: ["developer", "serverless", "events"]},
    {name: "Tray.io", category: "API", subcategory: "Enterprise Automation", desc: "Enterprise automation platform", url: "tray.io", pricing: "Paid", rating: 4.4, tags: ["enterprise", "integration", "automation"]},
    {name: "Workato", category: "API", subcategory: "Enterprise Automation", desc: "Enterprise integration platform", url: "workato.com", pricing: "Paid", rating: 4.5, tags: ["enterprise", "ai", "integration"]},
    {name: "Activepieces", category: "API", subcategory: "Automation", desc: "Open-source Zapier alternative", url: "activepieces.com", pricing: "Freemium", rating: 4.3, tags: ["open-source", "automation", "self-hosted"]},
    
    // ==================== DEVOPS & INFRASTRUCTURE ====================
    {name: "Docker", category: "DevOps", subcategory: "Containers", desc: "Container platform for developers", url: "docker.com", pricing: "Freemium", rating: 4.8, tags: ["containers", "virtualization", "deployment"], featured: true},
    {name: "Kubernetes", category: "DevOps", subcategory: "Orchestration", desc: "Container orchestration platform", url: "kubernetes.io", pricing: "Free", rating: 4.7, tags: ["orchestration", "scaling", "containers"]},
    {name: "Terraform", category: "DevOps", subcategory: "IaC", desc: "Infrastructure as Code tool", url: "terraform.io", pricing: "Freemium", rating: 4.7, tags: ["iac", "cloud", "automation"]},
    {name: "Pulumi", category: "DevOps", subcategory: "IaC", desc: "Modern Infrastructure as Code", url: "pulumi.com", pricing: "Freemium", rating: 4.5, tags: ["iac", "programming", "multi-cloud"]},
    {name: "Ansible", category: "DevOps", subcategory: "Configuration", desc: "IT automation platform", url: "ansible.com", pricing: "Freemium", rating: 4.6, tags: ["automation", "configuration", "agentless"]},
    {name: "GitHub Actions", category: "DevOps", subcategory: "CI/CD", desc: "Automate workflows in GitHub", url: "github.com/features/actions", pricing: "Freemium", rating: 4.7, tags: ["ci-cd", "automation", "github"]},
    {name: "GitLab CI", category: "DevOps", subcategory: "CI/CD", desc: "Complete DevOps platform", url: "gitlab.com", pricing: "Freemium", rating: 4.6, tags: ["ci-cd", "devops", "complete"]},
    {name: "CircleCI", category: "DevOps", subcategory: "CI/CD", desc: "Continuous integration platform", url: "circleci.com", pricing: "Freemium", rating: 4.5, tags: ["ci-cd", "automation", "fast"]},
    {name: "Jenkins", category: "DevOps", subcategory: "CI/CD", desc: "Open-source automation server", url: "jenkins.io", pricing: "Free", rating: 4.4, tags: ["open-source", "ci-cd", "plugins"]},
    {name: "ArgoCD", category: "DevOps", subcategory: "GitOps", desc: "GitOps continuous delivery", url: "argoproj.github.io/cd", pricing: "Free", rating: 4.5, tags: ["gitops", "kubernetes", "declarative"]},
    {name: "Harness", category: "DevOps", subcategory: "CI/CD", desc: "AI-powered software delivery", url: "harness.io", pricing: "Freemium", rating: 4.4, tags: ["ai", "delivery", "enterprise"]},
    {name: "Spacelift", category: "DevOps", subcategory: "IaC", desc: "Infrastructure management platform", url: "spacelift.io", pricing: "Paid", rating: 4.3, tags: ["terraform", "pulumi", "management"]},
    
    // ==================== TESTING & QA ====================
    {name: "Playwright", category: "Testing", subcategory: "E2E Testing", desc: "End-to-end testing framework", url: "playwright.dev", pricing: "Free", rating: 4.7, tags: ["e2e", "browser", "microsoft"], featured: true},
    {name: "Cypress", category: "Testing", subcategory: "E2E Testing", desc: "JavaScript testing framework", url: "cypress.io", pricing: "Freemium", rating: 4.6, tags: ["e2e", "javascript", "fast"]},
    {name: "Selenium", category: "Testing", subcategory: "Browser Automation", desc: "Browser automation framework", url: "selenium.dev", pricing: "Free", rating: 4.5, tags: ["automation", "browser", "open-source"]},
    {name: "TestCafe", category: "Testing", subcategory: "E2E Testing", desc: "Cross-browser testing tool", url: "testcafe.io", pricing: "Free", rating: 4.3, tags: ["cross-browser", "node", "no-webdriver"]},
    {name: "Puppeteer", category: "Testing", subcategory: "Browser Automation", desc: "Node library for Chrome automation", url: "pptr.dev", pricing: "Free", rating: 4.5, tags: ["chrome", "headless", "scraping"]},
    {name: "Jest", category: "Testing", subcategory: "Unit Testing", desc: "JavaScript testing framework", url: "jestjs.io", pricing: "Free", rating: 4.7, tags: ["javascript", "unit", "snapshot"]},
    {name: "Vitest", category: "Testing", subcategory: "Unit Testing", desc: "Vite-powered testing framework", url: "vitest.dev", pricing: "Free", rating: 4.6, tags: ["vite", "fast", "modern"]},
    {name: "Testim", category: "Testing", subcategory: "AI Testing", desc: "AI-powered test automation", url: "testim.io", pricing: "Paid", rating: 4.4, tags: ["ai", "automation", "self-healing"]},
    {name: "Mabl", category: "Testing", subcategory: "AI Testing", desc: "Intelligent test automation", url: "mabl.com", pricing: "Paid", rating: 4.4, tags: ["ai", "low-code", "ci-cd"]},
    {name: "Applitools", category: "Testing", subcategory: "Visual Testing", desc: "AI visual testing platform", url: "applitools.com", pricing: "Freemium", rating: 4.5, tags: ["visual", "ai", "cross-browser"]},
    {name: "Percy", category: "Testing", subcategory: "Visual Testing", desc: "Visual review platform", url: "percy.io", pricing: "Freemium", rating: 4.4, tags: ["visual", "snapshots", "review"]},
    {name: "Sauce Labs", category: "Testing", subcategory: "Cloud Testing", desc: "Cloud testing platform", url: "saucelabs.com", pricing: "Paid", rating: 4.3, tags: ["cloud", "devices", "browsers"]},
    {name: "BrowserStack", category: "Testing", subcategory: "Cloud Testing", desc: "Cross-browser testing cloud", url: "browserstack.com", pricing: "Paid", rating: 4.5, tags: ["cloud", "real-devices", "browsers"]},
    {name: "LambdaTest", category: "Testing", subcategory: "Cloud Testing", desc: "Cloud testing platform", url: "lambdatest.com", pricing: "Freemium", rating: 4.3, tags: ["cloud", "affordable", "selenium"]},
    
    // ==================== SECURITY ====================
    {name: "Snyk", category: "Security", subcategory: "Vulnerability Scanning", desc: "Developer security platform", url: "snyk.io", pricing: "Freemium", rating: 4.7, tags: ["vulnerabilities", "dependencies", "containers"], featured: true},
    {name: "SonarQube", category: "Security", subcategory: "Code Quality", desc: "Code quality and security platform", url: "sonarqube.org", pricing: "Freemium", rating: 4.6, tags: ["quality", "security", "static-analysis"]},
    {name: "Dependabot", category: "Security", subcategory: "Dependency Updates", desc: "Automated dependency updates", url: "github.com/dependabot", pricing: "Free", rating: 4.5, tags: ["dependencies", "github", "automated"]},
    {name: "CodeQL", category: "Security", subcategory: "Code Analysis", desc: "Semantic code analysis engine", url: "github.com/github/codeql", pricing: "Free", rating: 4.5, tags: ["analysis", "vulnerabilities", "github"]},
    {name: "Semgrep", category: "Security", subcategory: "Static Analysis", desc: "Fast static analysis tool", url: "semgrep.dev", pricing: "Freemium", rating: 4.5, tags: ["sast", "fast", "patterns"]},
    {name: "Trivy", category: "Security", subcategory: "Container Security", desc: "Container vulnerability scanner", url: "trivy.dev", pricing: "Free", rating: 4.5, tags: ["containers", "vulnerabilities", "open-source"]},
    {name: "Checkov", category: "Security", subcategory: "IaC Security", desc: "Policy-as-code for cloud security", url: "checkov.io", pricing: "Freemium", rating: 4.4, tags: ["iac", "terraform", "policy"]},
    {name: "OWASP ZAP", category: "Security", subcategory: "Penetration Testing", desc: "Web app security scanner", url: "owasp.org/www-project-zap", pricing: "Free", rating: 4.4, tags: ["penetration", "web-security", "open-source"]},
    {name: "Burp Suite", category: "Security", subcategory: "Penetration Testing", desc: "Web security testing toolkit", url: "portswigger.net/burp", pricing: "Freemium", rating: 4.6, tags: ["pentesting", "professional", "comprehensive"]},
    {name: "GitGuardian", category: "Security", subcategory: "Secrets Detection", desc: "Detect secrets in code", url: "gitguardian.com", pricing: "Freemium", rating: 4.5, tags: ["secrets", "detection", "git"]},
    
    // ==================== DOCUMENTATION ====================
    {name: "Notion AI", category: "Documentation", subcategory: "Knowledge Base", desc: "AI-powered workspace", url: "notion.so", pricing: "Freemium", rating: 4.8, tags: ["workspace", "docs", "ai"], featured: true},
    {name: "Gitbook", category: "Documentation", subcategory: "Documentation", desc: "Modern documentation platform", url: "gitbook.com", pricing: "Freemium", rating: 4.5, tags: ["docs", "collaboration", "git"]},
    {name: "ReadMe", category: "Documentation", subcategory: "API Docs", desc: "API documentation platform", url: "readme.com", pricing: "Freemium", rating: 4.5, tags: ["api", "developer", "interactive"]},
    {name: "Docusaurus", category: "Documentation", subcategory: "Static Docs", desc: "Documentation site generator", url: "docusaurus.io", pricing: "Free", rating: 4.5, tags: ["static", "react", "meta"]},
    {name: "Mintlify", category: "Documentation", subcategory: "Documentation", desc: "Beautiful documentation with AI", url: "mintlify.com", pricing: "Freemium", rating: 4.6, tags: ["beautiful", "ai", "modern"]},
    {name: "Swagger", category: "Documentation", subcategory: "API Docs", desc: "API documentation tools", url: "swagger.io", pricing: "Freemium", rating: 4.5, tags: ["api", "openapi", "standard"]},
    {name: "Stoplight", category: "Documentation", subcategory: "API Design", desc: "API design and documentation", url: "stoplight.io", pricing: "Freemium", rating: 4.4, tags: ["api", "design", "mock"]},
    {name: "Swimm", category: "Documentation", subcategory: "Code Docs", desc: "AI-powered code documentation", url: "swimm.io", pricing: "Freemium", rating: 4.4, tags: ["code", "ai", "sync"]},
    {name: "Scribe", category: "Documentation", subcategory: "How-to Guides", desc: "Auto-generate how-to guides", url: "scribehow.com", pricing: "Freemium", rating: 4.5, tags: ["guides", "automatic", "screenshots"]},
    {name: "Tango", category: "Documentation", subcategory: "How-to Guides", desc: "Create how-to guides automatically", url: "tango.us", pricing: "Freemium", rating: 4.4, tags: ["guides", "training", "workflows"]},
    
    // ==================== LOW-CODE / NO-CODE ====================
    {name: "Bubble", category: "No-Code", subcategory: "Web Apps", desc: "Visual web app builder", url: "bubble.io", pricing: "Freemium", rating: 4.6, tags: ["web-apps", "visual", "powerful"], featured: true},
    {name: "Airtable", category: "No-Code", subcategory: "Database", desc: "Spreadsheet-database hybrid with AI", url: "airtable.com", pricing: "Freemium", rating: 4.6, tags: ["database", "spreadsheet", "collaboration"]},
    {name: "Retool", category: "No-Code", subcategory: "Internal Tools", desc: "Build internal tools quickly", url: "retool.com", pricing: "Freemium", rating: 4.6, tags: ["internal", "dashboard", "database"]},
    {name: "Appsmith", category: "No-Code", subcategory: "Internal Tools", desc: "Open-source internal tool builder", url: "appsmith.com", pricing: "Freemium", rating: 4.5, tags: ["open-source", "internal", "dashboard"]},
    {name: "Softr", category: "No-Code", subcategory: "Web Apps", desc: "Build apps from Airtable", url: "softr.io", pricing: "Freemium", rating: 4.4, tags: ["airtable", "portals", "websites"]},
    {name: "Stacker", category: "No-Code", subcategory: "Portals", desc: "Build apps from spreadsheets", url: "stackerhq.com", pricing: "Freemium", rating: 4.3, tags: ["portals", "spreadsheet", "business"]},
    {name: "Directual", category: "No-Code", subcategory: "Backend", desc: "No-code backend platform", url: "directual.com", pricing: "Freemium", rating: 4.2, tags: ["backend", "logic", "api"]},
    {name: "Xano", category: "No-Code", subcategory: "Backend", desc: "No-code backend builder", url: "xano.com", pricing: "Paid", rating: 4.4, tags: ["backend", "api", "scalable"]},
    {name: "Noodl", category: "No-Code", subcategory: "Full-Stack", desc: "Full-stack low-code platform", url: "noodl.net", pricing: "Free", rating: 4.2, tags: ["full-stack", "visual", "open-source"]},
    {name: "WeWeb", category: "No-Code", subcategory: "Frontend", desc: "No-code frontend builder", url: "weweb.io", pricing: "Freemium", rating: 4.3, tags: ["frontend", "visual", "export"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE3 = AI_TOOLS_PHASE3;
}


