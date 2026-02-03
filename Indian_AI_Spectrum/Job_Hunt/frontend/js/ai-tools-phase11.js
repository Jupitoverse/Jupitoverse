// AI Tools Database - Phase 11: Coding, Development & DevOps AI
// 200+ Tools for developers

const AI_TOOLS_PHASE11 = [
    // ==================== AI CODING ASSISTANTS ====================
    {name: "GitHub Copilot", category: "Coding", subcategory: "AI Assistant", desc: "AI pair programmer by GitHub", url: "github.com/features/copilot", pricing: "Paid", rating: 4.7, tags: ["autocomplete", "github", "vscode"], featured: true},
    {name: "Cursor", category: "Coding", subcategory: "IDE", desc: "AI-first code editor", url: "cursor.sh", pricing: "Freemium", rating: 4.7, tags: ["ide", "ai", "chat"], featured: true},
    {name: "Codeium", category: "Coding", subcategory: "AI Assistant", desc: "Free AI code completion", url: "codeium.com", pricing: "Free", rating: 4.5, tags: ["free", "autocomplete", "multi-ide"]},
    {name: "Amazon CodeWhisperer", category: "Coding", subcategory: "AI Assistant", desc: "AWS AI coding companion", url: "aws.amazon.com/codewhisperer", pricing: "Freemium", rating: 4.3, tags: ["aws", "security", "autocomplete"]},
    {name: "Tabnine", category: "Coding", subcategory: "AI Assistant", desc: "AI code completion", url: "tabnine.com", pricing: "Freemium", rating: 4.4, tags: ["privacy", "local", "teams"]},
    {name: "Sourcegraph Cody", category: "Coding", subcategory: "AI Assistant", desc: "AI coding assistant", url: "sourcegraph.com/cody", pricing: "Freemium", rating: 4.4, tags: ["context", "codebase", "chat"]},
    {name: "Replit AI", category: "Coding", subcategory: "IDE", desc: "AI in browser IDE", url: "replit.com/ai", pricing: "Freemium", rating: 4.4, tags: ["browser", "collaborative", "deployment"]},
    {name: "Blackbox AI", category: "Coding", subcategory: "AI Assistant", desc: "AI code assistant", url: "blackbox.ai", pricing: "Freemium", rating: 4.2, tags: ["autocomplete", "chat", "search"]},
    {name: "Codium AI", category: "Coding", subcategory: "Testing", desc: "AI test generation", url: "codium.ai", pricing: "Freemium", rating: 4.3, tags: ["testing", "generation", "coverage"]},
    {name: "Continue", category: "Coding", subcategory: "AI Assistant", desc: "Open source AI assistant", url: "continue.dev", pricing: "Free", rating: 4.3, tags: ["open-source", "vscode", "jetbrains"]},
    {name: "Aider", category: "Coding", subcategory: "CLI", desc: "AI pair programming in terminal", url: "aider.chat", pricing: "Free", rating: 4.4, tags: ["cli", "git", "open-source"]},
    {name: "Mentat", category: "Coding", subcategory: "CLI", desc: "AI coding in terminal", url: "mentat.ai", pricing: "Free", rating: 4.2, tags: ["cli", "context", "open-source"]},
    {name: "Pieces", category: "Coding", subcategory: "Snippets", desc: "AI code snippets manager", url: "pieces.app", pricing: "Free", rating: 4.3, tags: ["snippets", "context", "offline"]},
    {name: "AskCodi", category: "Coding", subcategory: "AI Assistant", desc: "AI coding assistant", url: "askcodi.com", pricing: "Freemium", rating: 4.1, tags: ["chat", "generation", "docs"]},
    {name: "CodeGPT", category: "Coding", subcategory: "Extension", desc: "GPT in your IDE", url: "codegpt.co", pricing: "Freemium", rating: 4.2, tags: ["vscode", "multiple-llms", "chat"]},
    
    // ==================== CODE REVIEW & QUALITY ====================
    {name: "CodeRabbit", category: "Code Review", subcategory: "AI Review", desc: "AI code reviews", url: "coderabbit.ai", pricing: "Freemium", rating: 4.5, tags: ["pr-review", "github", "ai"], featured: true},
    {name: "Codacy", category: "Code Review", subcategory: "Quality", desc: "Automated code review", url: "codacy.com", pricing: "Freemium", rating: 4.3, tags: ["quality", "security", "coverage"]},
    {name: "SonarQube", category: "Code Review", subcategory: "Quality", desc: "Code quality platform", url: "sonarqube.org", pricing: "Freemium", rating: 4.5, tags: ["quality", "security", "enterprise"]},
    {name: "CodeClimate", category: "Code Review", subcategory: "Quality", desc: "Code quality automation", url: "codeclimate.com", pricing: "Freemium", rating: 4.2, tags: ["quality", "maintainability", "ci"]},
    {name: "DeepSource", category: "Code Review", subcategory: "Analysis", desc: "AI code analysis", url: "deepsource.io", pricing: "Freemium", rating: 4.3, tags: ["analysis", "autofix", "security"]},
    {name: "Snyk", category: "Security", subcategory: "Security", desc: "Developer security platform", url: "snyk.io", pricing: "Freemium", rating: 4.5, tags: ["security", "dependencies", "containers"]},
    {name: "Semgrep", category: "Security", subcategory: "SAST", desc: "Static analysis at scale", url: "semgrep.dev", pricing: "Freemium", rating: 4.4, tags: ["sast", "rules", "fast"]},
    {name: "Checkmarx", category: "Security", subcategory: "AppSec", desc: "Application security", url: "checkmarx.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "sast", "dast"]},
    {name: "Veracode", category: "Security", subcategory: "AppSec", desc: "Application security testing", url: "veracode.com", pricing: "Paid", rating: 4.1, tags: ["enterprise", "sast", "sca"]},
    {name: "GitGuardian", category: "Security", subcategory: "Secrets", desc: "Secrets detection", url: "gitguardian.com", pricing: "Freemium", rating: 4.4, tags: ["secrets", "scanning", "monitoring"]},
    
    // ==================== DEVOPS & INFRASTRUCTURE ====================
    {name: "Pulumi", category: "DevOps", subcategory: "IaC", desc: "Infrastructure as code", url: "pulumi.com", pricing: "Freemium", rating: 4.5, tags: ["iac", "multi-cloud", "programming"], featured: true},
    {name: "Terraform", category: "DevOps", subcategory: "IaC", desc: "Infrastructure as code by HashiCorp", url: "terraform.io", pricing: "Freemium", rating: 4.6, tags: ["iac", "multi-cloud", "declarative"]},
    {name: "Ansible", category: "DevOps", subcategory: "Automation", desc: "IT automation platform", url: "ansible.com", pricing: "Freemium", rating: 4.5, tags: ["automation", "config", "redhat"]},
    {name: "Docker", category: "DevOps", subcategory: "Containers", desc: "Container platform", url: "docker.com", pricing: "Freemium", rating: 4.7, tags: ["containers", "images", "compose"]},
    {name: "Kubernetes", category: "DevOps", subcategory: "Orchestration", desc: "Container orchestration", url: "kubernetes.io", pricing: "Free", rating: 4.6, tags: ["orchestration", "containers", "cncf"]},
    {name: "GitHub Actions", category: "DevOps", subcategory: "CI/CD", desc: "CI/CD by GitHub", url: "github.com/features/actions", pricing: "Freemium", rating: 4.6, tags: ["ci-cd", "automation", "github"]},
    {name: "GitLab CI", category: "DevOps", subcategory: "CI/CD", desc: "CI/CD in GitLab", url: "gitlab.com", pricing: "Freemium", rating: 4.5, tags: ["ci-cd", "devops", "platform"]},
    {name: "CircleCI", category: "DevOps", subcategory: "CI/CD", desc: "Continuous integration", url: "circleci.com", pricing: "Freemium", rating: 4.4, tags: ["ci-cd", "fast", "docker"]},
    {name: "Jenkins", category: "DevOps", subcategory: "CI/CD", desc: "Open source automation", url: "jenkins.io", pricing: "Free", rating: 4.3, tags: ["ci-cd", "plugins", "self-hosted"]},
    {name: "ArgoCD", category: "DevOps", subcategory: "GitOps", desc: "GitOps for Kubernetes", url: "argoproj.github.io/cd", pricing: "Free", rating: 4.5, tags: ["gitops", "kubernetes", "declarative"]},
    {name: "Datadog", category: "DevOps", subcategory: "Monitoring", desc: "Monitoring and observability", url: "datadoghq.com", pricing: "Paid", rating: 4.5, tags: ["monitoring", "apm", "logs"]},
    {name: "New Relic", category: "DevOps", subcategory: "Monitoring", desc: "Observability platform", url: "newrelic.com", pricing: "Freemium", rating: 4.4, tags: ["observability", "apm", "full-stack"]},
    {name: "Grafana", category: "DevOps", subcategory: "Visualization", desc: "Metrics visualization", url: "grafana.com", pricing: "Freemium", rating: 4.6, tags: ["dashboards", "prometheus", "open-source"]},
    {name: "Prometheus", category: "DevOps", subcategory: "Monitoring", desc: "Metrics and alerting", url: "prometheus.io", pricing: "Free", rating: 4.5, tags: ["metrics", "alerting", "cncf"]},
    {name: "PagerDuty", category: "DevOps", subcategory: "Incident", desc: "Incident management", url: "pagerduty.com", pricing: "Paid", rating: 4.4, tags: ["incident", "alerting", "on-call"]},
    
    // ==================== API & BACKEND ====================
    {name: "Postman", category: "API", subcategory: "Testing", desc: "API platform", url: "postman.com", pricing: "Freemium", rating: 4.6, tags: ["api", "testing", "collaboration"], featured: true},
    {name: "Insomnia", category: "API", subcategory: "Testing", desc: "API client", url: "insomnia.rest", pricing: "Freemium", rating: 4.4, tags: ["api", "graphql", "grpc"]},
    {name: "Swagger", category: "API", subcategory: "Documentation", desc: "API documentation", url: "swagger.io", pricing: "Freemium", rating: 4.5, tags: ["docs", "openapi", "design"]},
    {name: "RapidAPI", category: "API", subcategory: "Marketplace", desc: "API marketplace", url: "rapidapi.com", pricing: "Freemium", rating: 4.3, tags: ["marketplace", "hub", "testing"]},
    {name: "Kong", category: "API", subcategory: "Gateway", desc: "API gateway platform", url: "konghq.com", pricing: "Freemium", rating: 4.4, tags: ["gateway", "microservices", "enterprise"]},
    {name: "Apigee", category: "API", subcategory: "Gateway", desc: "Google Cloud API management", url: "cloud.google.com/apigee", pricing: "Paid", rating: 4.3, tags: ["gateway", "google", "enterprise"]},
    {name: "Hasura", category: "Backend", subcategory: "GraphQL", desc: "Instant GraphQL APIs", url: "hasura.io", pricing: "Freemium", rating: 4.5, tags: ["graphql", "instant", "postgres"]},
    {name: "Supabase", category: "Backend", subcategory: "BaaS", desc: "Open source Firebase alternative", url: "supabase.com", pricing: "Freemium", rating: 4.6, tags: ["postgres", "auth", "realtime"]},
    {name: "Firebase", category: "Backend", subcategory: "BaaS", desc: "Google's app development platform", url: "firebase.google.com", pricing: "Freemium", rating: 4.5, tags: ["baas", "google", "mobile"]},
    {name: "Appwrite", category: "Backend", subcategory: "BaaS", desc: "Open source backend server", url: "appwrite.io", pricing: "Free", rating: 4.4, tags: ["open-source", "self-hosted", "baas"]},
    {name: "PocketBase", category: "Backend", subcategory: "BaaS", desc: "Open source backend in Go", url: "pocketbase.io", pricing: "Free", rating: 4.4, tags: ["sqlite", "single-file", "simple"]},
    {name: "Nhost", category: "Backend", subcategory: "BaaS", desc: "GraphQL backend platform", url: "nhost.io", pricing: "Freemium", rating: 4.3, tags: ["hasura", "auth", "storage"]},
    {name: "Convex", category: "Backend", subcategory: "BaaS", desc: "Reactive backend platform", url: "convex.dev", pricing: "Freemium", rating: 4.4, tags: ["reactive", "typescript", "real-time"]},
    {name: "Railway", category: "Backend", subcategory: "Deployment", desc: "Infrastructure platform", url: "railway.app", pricing: "Freemium", rating: 4.5, tags: ["deployment", "postgres", "easy"]},
    {name: "Render", category: "Backend", subcategory: "Deployment", desc: "Cloud platform", url: "render.com", pricing: "Freemium", rating: 4.5, tags: ["deployment", "static", "databases"]},
    
    // ==================== DATABASE ====================
    {name: "PlanetScale", category: "Database", subcategory: "MySQL", desc: "Serverless MySQL", url: "planetscale.com", pricing: "Freemium", rating: 4.6, tags: ["mysql", "serverless", "branching"], featured: true},
    {name: "Neon", category: "Database", subcategory: "Postgres", desc: "Serverless Postgres", url: "neon.tech", pricing: "Freemium", rating: 4.5, tags: ["postgres", "serverless", "branching"]},
    {name: "CockroachDB", category: "Database", subcategory: "Distributed", desc: "Distributed SQL database", url: "cockroachlabs.com", pricing: "Freemium", rating: 4.4, tags: ["distributed", "sql", "resilient"]},
    {name: "MongoDB Atlas", category: "Database", subcategory: "NoSQL", desc: "Cloud MongoDB", url: "mongodb.com/atlas", pricing: "Freemium", rating: 4.5, tags: ["nosql", "document", "cloud"]},
    {name: "Redis Cloud", category: "Database", subcategory: "Cache", desc: "Cloud Redis", url: "redis.com/cloud", pricing: "Freemium", rating: 4.5, tags: ["cache", "in-memory", "fast"]},
    {name: "Upstash", category: "Database", subcategory: "Serverless", desc: "Serverless data platform", url: "upstash.com", pricing: "Freemium", rating: 4.4, tags: ["serverless", "redis", "kafka"]},
    {name: "Fauna", category: "Database", subcategory: "Distributed", desc: "Distributed document database", url: "fauna.com", pricing: "Freemium", rating: 4.2, tags: ["distributed", "graphql", "serverless"]},
    {name: "Turso", category: "Database", subcategory: "SQLite", desc: "Edge SQLite database", url: "turso.tech", pricing: "Freemium", rating: 4.3, tags: ["sqlite", "edge", "libsql"]},
    {name: "DynamoDB", category: "Database", subcategory: "NoSQL", desc: "AWS NoSQL database", url: "aws.amazon.com/dynamodb", pricing: "Pay-per-use", rating: 4.4, tags: ["aws", "nosql", "serverless"]},
    {name: "Prisma", category: "Database", subcategory: "ORM", desc: "Next-gen ORM", url: "prisma.io", pricing: "Freemium", rating: 4.6, tags: ["orm", "typescript", "migrations"]},
    
    // ==================== FRONTEND & FRAMEWORKS ====================
    {name: "Vercel", category: "Frontend", subcategory: "Deployment", desc: "Frontend cloud platform", url: "vercel.com", pricing: "Freemium", rating: 4.7, tags: ["nextjs", "edge", "deployment"], featured: true},
    {name: "Netlify", category: "Frontend", subcategory: "Deployment", desc: "Web development platform", url: "netlify.com", pricing: "Freemium", rating: 4.6, tags: ["jamstack", "functions", "forms"]},
    {name: "Cloudflare Pages", category: "Frontend", subcategory: "Deployment", desc: "JAMstack platform", url: "pages.cloudflare.com", pricing: "Freemium", rating: 4.5, tags: ["jamstack", "edge", "fast"]},
    {name: "v0.dev", category: "Frontend", subcategory: "AI UI", desc: "AI UI generation by Vercel", url: "v0.dev", pricing: "Freemium", rating: 4.5, tags: ["ui", "react", "ai"]},
    {name: "Framer", category: "Frontend", subcategory: "Website Builder", desc: "AI website builder", url: "framer.com", pricing: "Freemium", rating: 4.5, tags: ["design", "animation", "ai"]},
    {name: "Webflow", category: "Frontend", subcategory: "Website Builder", desc: "Visual web development", url: "webflow.com", pricing: "Freemium", rating: 4.5, tags: ["visual", "cms", "nocode"]},
    {name: "Builder.io", category: "Frontend", subcategory: "Visual Dev", desc: "Visual development platform", url: "builder.io", pricing: "Freemium", rating: 4.3, tags: ["visual", "cms", "figma"]},
    {name: "Plasmic", category: "Frontend", subcategory: "Visual Dev", desc: "Visual builder for code", url: "plasmic.app", pricing: "Freemium", rating: 4.2, tags: ["visual", "react", "headless"]},
    {name: "TeleportHQ", category: "Frontend", subcategory: "Code Gen", desc: "AI code generation", url: "teleporthq.io", pricing: "Freemium", rating: 4.1, tags: ["code-gen", "design-to-code", "ai"]},
    {name: "Locofy", category: "Frontend", subcategory: "Design to Code", desc: "Figma to code with AI", url: "locofy.ai", pricing: "Freemium", rating: 4.2, tags: ["figma", "code-gen", "responsive"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE11 = AI_TOOLS_PHASE11;
}


