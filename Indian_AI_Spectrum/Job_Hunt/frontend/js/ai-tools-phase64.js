// AI Tools Database - Phase 64: More Developer & Coding AI
// 150+ Additional developer and coding tools

const AI_TOOLS_PHASE64 = [
    // ==================== AI CODE ASSISTANTS ====================
    {name: "GitHub Copilot", category: "Coding", subcategory: "AI Assistant", desc: "AI pair programmer", url: "github.com/features/copilot", pricing: "Paid", rating: 4.7, tags: ["ai", "autocomplete", "github"], featured: true},
    {name: "Cursor", category: "Coding", subcategory: "AI IDE", desc: "AI-first code editor", url: "cursor.sh", pricing: "Freemium", rating: 4.6, tags: ["ai", "editor", "ide"]},
    {name: "Codeium", category: "Coding", subcategory: "AI Assistant", desc: "Free AI coding", url: "codeium.com", pricing: "Freemium", rating: 4.5, tags: ["ai", "free", "autocomplete"]},
    {name: "Tabnine", category: "Coding", subcategory: "AI Assistant", desc: "AI code completion", url: "tabnine.com", pricing: "Freemium", rating: 4.4, tags: ["ai", "autocomplete", "private"]},
    {name: "Amazon CodeWhisperer", category: "Coding", subcategory: "AI Assistant", desc: "AWS AI coding", url: "aws.amazon.com/codewhisperer", pricing: "Freemium", rating: 4.3, tags: ["aws", "ai", "security"]},
    {name: "Sourcegraph Cody", category: "Coding", subcategory: "AI Assistant", desc: "AI coding assistant", url: "sourcegraph.com/cody", pricing: "Freemium", rating: 4.3, tags: ["ai", "context", "codebase"]},
    {name: "Replit AI", category: "Coding", subcategory: "AI IDE", desc: "Replit with AI", url: "replit.com/ai", pricing: "Freemium", rating: 4.4, tags: ["ai", "browser", "collaborative"]},
    {name: "Codiga", category: "Coding", subcategory: "Code Analysis", desc: "Code analysis AI", url: "codiga.io", pricing: "Freemium", rating: 4.2, tags: ["analysis", "snippets", "security"]},
    {name: "Codex (OpenAI)", category: "Coding", subcategory: "AI Model", desc: "Code generation model", url: "openai.com/codex", pricing: "Paid", rating: 4.5, tags: ["model", "openai", "api"]},
    {name: "Phind", category: "Coding", subcategory: "AI Search", desc: "Developer search", url: "phind.com", pricing: "Freemium", rating: 4.4, tags: ["search", "ai", "developer"]},
    {name: "BlackBox AI", category: "Coding", subcategory: "AI Code", desc: "AI code generation", url: "blackbox.ai", pricing: "Freemium", rating: 4.1, tags: ["code", "generation", "search"]},
    {name: "Bito", category: "Coding", subcategory: "AI Assistant", desc: "AI code assistant", url: "bito.ai", pricing: "Freemium", rating: 4.2, tags: ["assistant", "ide", "productivity"]},
    {name: "AskCodi", category: "Coding", subcategory: "AI Assistant", desc: "AI coding helper", url: "askcodi.com", pricing: "Freemium", rating: 4.0, tags: ["assistant", "generation", "explanation"]},
    {name: "Codium AI", category: "Coding", subcategory: "Testing", desc: "AI test generation", url: "codium.ai", pricing: "Freemium", rating: 4.3, tags: ["testing", "ai", "quality"]},
    {name: "Mintlify", category: "Coding", subcategory: "Documentation", desc: "AI documentation", url: "mintlify.com", pricing: "Freemium", rating: 4.4, tags: ["documentation", "ai", "beautiful"]},
    
    // ==================== IDES & EDITORS ====================
    {name: "VS Code", category: "Coding", subcategory: "IDE", desc: "Microsoft code editor", url: "code.visualstudio.com", pricing: "Free", rating: 4.8, tags: ["editor", "microsoft", "extensions"], featured: true},
    {name: "JetBrains IDEs", category: "Coding", subcategory: "IDE", desc: "Professional IDEs", url: "jetbrains.com", pricing: "Paid", rating: 4.7, tags: ["ide", "professional", "refactoring"]},
    {name: "IntelliJ IDEA", category: "Coding", subcategory: "IDE", desc: "Java IDE", url: "jetbrains.com/idea", pricing: "Freemium", rating: 4.7, tags: ["java", "kotlin", "enterprise"]},
    {name: "PyCharm", category: "Coding", subcategory: "IDE", desc: "Python IDE", url: "jetbrains.com/pycharm", pricing: "Freemium", rating: 4.6, tags: ["python", "django", "scientific"]},
    {name: "WebStorm", category: "Coding", subcategory: "IDE", desc: "JavaScript IDE", url: "jetbrains.com/webstorm", pricing: "Paid", rating: 4.5, tags: ["javascript", "typescript", "web"]},
    {name: "Sublime Text", category: "Coding", subcategory: "Editor", desc: "Text editor", url: "sublimetext.com", pricing: "Paid", rating: 4.4, tags: ["editor", "fast", "lightweight"]},
    {name: "Vim/Neovim", category: "Coding", subcategory: "Editor", desc: "Modal text editor", url: "neovim.io", pricing: "Free", rating: 4.6, tags: ["modal", "terminal", "customizable"]},
    {name: "Emacs", category: "Coding", subcategory: "Editor", desc: "Extensible editor", url: "gnu.org/emacs", pricing: "Free", rating: 4.4, tags: ["extensible", "lisp", "org-mode"]},
    {name: "Zed", category: "Coding", subcategory: "Editor", desc: "High-performance editor", url: "zed.dev", pricing: "Free", rating: 4.3, tags: ["performance", "rust", "collaborative"]},
    {name: "Fleet", category: "Coding", subcategory: "IDE", desc: "JetBrains lightweight", url: "jetbrains.com/fleet", pricing: "Free", rating: 4.1, tags: ["lightweight", "jetbrains", "polyglot"]},
    
    // ==================== VERSION CONTROL ====================
    {name: "GitHub", category: "Coding", subcategory: "Version Control", desc: "Code hosting", url: "github.com", pricing: "Freemium", rating: 4.8, tags: ["git", "hosting", "collaboration"], featured: true},
    {name: "GitLab", category: "Coding", subcategory: "DevOps", desc: "DevOps platform", url: "gitlab.com", pricing: "Freemium", rating: 4.5, tags: ["git", "devops", "ci-cd"]},
    {name: "Bitbucket", category: "Coding", subcategory: "Version Control", desc: "Atlassian git", url: "bitbucket.org", pricing: "Freemium", rating: 4.2, tags: ["git", "atlassian", "jira"]},
    {name: "Azure DevOps", category: "Coding", subcategory: "DevOps", desc: "Microsoft DevOps", url: "dev.azure.com", pricing: "Freemium", rating: 4.3, tags: ["devops", "microsoft", "boards"]},
    {name: "SourceForge", category: "Coding", subcategory: "Hosting", desc: "Open source hosting", url: "sourceforge.net", pricing: "Free", rating: 3.8, tags: ["open-source", "hosting", "download"]},
    {name: "Gitea", category: "Coding", subcategory: "Self-Hosted", desc: "Self-hosted git", url: "gitea.io", pricing: "Free", rating: 4.3, tags: ["self-hosted", "lightweight", "go"]},
    {name: "Gogs", category: "Coding", subcategory: "Self-Hosted", desc: "Painless git service", url: "gogs.io", pricing: "Free", rating: 4.2, tags: ["self-hosted", "lightweight", "go"]},
    {name: "GitKraken", category: "Coding", subcategory: "Git Client", desc: "Git GUI client", url: "gitkraken.com", pricing: "Freemium", rating: 4.4, tags: ["gui", "cross-platform", "visual"]},
    {name: "Sourcetree", category: "Coding", subcategory: "Git Client", desc: "Free git client", url: "sourcetreeapp.com", pricing: "Free", rating: 4.2, tags: ["gui", "atlassian", "free"]},
    {name: "Fork", category: "Coding", subcategory: "Git Client", desc: "Fast git client", url: "git-fork.com", pricing: "Paid", rating: 4.4, tags: ["gui", "fast", "native"]},
    
    // ==================== API DEVELOPMENT ====================
    {name: "Postman", category: "Coding", subcategory: "API", desc: "API platform", url: "postman.com", pricing: "Freemium", rating: 4.6, tags: ["api", "testing", "documentation"], featured: true},
    {name: "Insomnia", category: "Coding", subcategory: "API", desc: "API client", url: "insomnia.rest", pricing: "Freemium", rating: 4.4, tags: ["api", "rest", "graphql"]},
    {name: "Hoppscotch", category: "Coding", subcategory: "API", desc: "Open source API", url: "hoppscotch.io", pricing: "Free", rating: 4.4, tags: ["api", "open-source", "fast"]},
    {name: "Thunder Client", category: "Coding", subcategory: "API", desc: "VS Code API client", url: "thunderclient.com", pricing: "Freemium", rating: 4.3, tags: ["api", "vscode", "lightweight"]},
    {name: "Bruno", category: "Coding", subcategory: "API", desc: "Git-based API client", url: "usebruno.com", pricing: "Free", rating: 4.3, tags: ["api", "git", "offline"]},
    {name: "RapidAPI", category: "Coding", subcategory: "API Marketplace", desc: "API marketplace", url: "rapidapi.com", pricing: "Freemium", rating: 4.2, tags: ["marketplace", "apis", "hub"]},
    {name: "Swagger", category: "Coding", subcategory: "API Docs", desc: "API documentation", url: "swagger.io", pricing: "Freemium", rating: 4.4, tags: ["documentation", "openapi", "spec"]},
    {name: "Readme.io", category: "Coding", subcategory: "API Docs", desc: "Developer hubs", url: "readme.com", pricing: "Paid", rating: 4.4, tags: ["documentation", "developer-hub", "api"]},
    {name: "Stoplight", category: "Coding", subcategory: "API Design", desc: "API design platform", url: "stoplight.io", pricing: "Freemium", rating: 4.3, tags: ["design", "openapi", "documentation"]},
    {name: "Kong", category: "Coding", subcategory: "API Gateway", desc: "API gateway", url: "konghq.com", pricing: "Freemium", rating: 4.3, tags: ["gateway", "microservices", "enterprise"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE64 = AI_TOOLS_PHASE64;
}


