// AI Tools Mega Database - Part 3: Specialized Categories

const AI_TOOLS_DATABASE_3 = {
    // ==================== RESEARCH & ANALYSIS ====================
    research: [
        {name: "Elicit", category: "Research", sub: "Academic", desc: "AI research assistant", url: "https://elicit.org", pricing: "Freemium", rating: 4.6, users: "500K+", tags: ["research"], featured: true, icon: "🔬"},
        {name: "Consensus", category: "Research", sub: "Science", desc: "AI for scientific papers", url: "https://consensus.app", pricing: "Freemium", rating: 4.5, users: "300K+", tags: ["science"], featured: true, icon: "🧪"},
        {name: "ChatPDF", category: "Research", sub: "Documents", desc: "Chat with PDFs", url: "https://chatpdf.com", pricing: "Freemium", rating: 4.5, users: "1M+", tags: ["pdf"], featured: false, icon: "📄"},
        {name: "Scholarcy", category: "Research", sub: "Summary", desc: "AI paper summarization", url: "https://scholarcy.com", pricing: "Freemium", rating: 4.3, users: "200K+", tags: ["summary"], featured: false, icon: "📚"},
        {name: "Semantic Scholar", category: "Research", sub: "Search", desc: "AI academic search", url: "https://semanticscholar.org", pricing: "Free", rating: 4.6, users: "1M+", tags: ["search"], featured: false, icon: "🔍"},
        {name: "Scite", category: "Research", sub: "Citations", desc: "AI citation analysis", url: "https://scite.ai", pricing: "Freemium", rating: 4.4, users: "100K+", tags: ["citations"], featured: false, icon: "📊"},
        {name: "ResearchRabbit", category: "Research", sub: "Discovery", desc: "AI research discovery", url: "https://researchrabbit.ai", pricing: "Free", rating: 4.4, users: "200K+", tags: ["discovery"], featured: false, icon: "🐰"},
        {name: "Iris.ai", category: "Research", sub: "Workspace", desc: "AI research workspace", url: "https://iris.ai", pricing: "Paid", rating: 4.2, users: "50K+", tags: ["workspace"], featured: false, icon: "👁️"},
        {name: "Litmaps", category: "Research", sub: "Mapping", desc: "Literature mapping", url: "https://litmaps.com", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["mapping"], featured: false, icon: "🗺️"},
        {name: "Connected Papers", category: "Research", sub: "Graph", desc: "Paper connections graph", url: "https://connectedpapers.com", pricing: "Freemium", rating: 4.4, users: "500K+", tags: ["graph"], featured: false, icon: "🔗"},
        {name: "Explainpaper", category: "Research", sub: "Explain", desc: "AI paper explanation", url: "https://explainpaper.com", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["explain"], featured: false, icon: "💡"},
        {name: "SciSpace", category: "Research", sub: "Copilot", desc: "Research copilot", url: "https://typeset.io", pricing: "Freemium", rating: 4.3, users: "200K+", tags: ["copilot"], featured: false, icon: "🚀"},
        {name: "Jenni AI", category: "Research", sub: "Writing", desc: "AI research writing", url: "https://jenni.ai", pricing: "Freemium", rating: 4.3, users: "500K+", tags: ["writing"], featured: false, icon: "✍️"},
        {name: "Paperpal", category: "Research", sub: "Editing", desc: "AI academic editing", url: "https://paperpal.com", pricing: "Freemium", rating: 4.2, users: "100K+", tags: ["editing"], featured: false, icon: "📝"},
        {name: "Writefull", category: "Research", sub: "Academic", desc: "AI academic writing", url: "https://writefull.com", pricing: "Freemium", rating: 4.3, users: "200K+", tags: ["academic"], featured: false, icon: "✏️"},
    ],

    // ==================== DATA & ANALYTICS ====================
    data: [
        {name: "Julius AI", category: "Data", sub: "Analysis", desc: "AI data analyst", url: "https://julius.ai", pricing: "Freemium", rating: 4.5, users: "500K+", tags: ["analysis"], featured: true, icon: "📊"},
        {name: "Obviously AI", category: "Data", sub: "ML", desc: "No-code ML", url: "https://obviously.ai", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["ml"], featured: false, icon: "🤖"},
        {name: "Akkio", category: "Data", sub: "ML", desc: "No-code AI analytics", url: "https://akkio.com", pricing: "Paid", rating: 4.2, users: "30K+", tags: ["analytics"], featured: false, icon: "📈"},
        {name: "MonkeyLearn", category: "Data", sub: "Text", desc: "Text analytics AI", url: "https://monkeylearn.com", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["text"], featured: false, icon: "🐒"},
        {name: "DataRobot", category: "Data", sub: "Enterprise ML", desc: "Enterprise AI platform", url: "https://datarobot.com", pricing: "Paid", rating: 4.4, users: "10K+", tags: ["enterprise"], featured: false, icon: "🤖"},
        {name: "H2O.ai", category: "Data", sub: "ML Platform", desc: "ML platform", url: "https://h2o.ai", pricing: "Freemium", rating: 4.4, users: "50K+", tags: ["platform"], featured: false, icon: "💧"},
        {name: "Dataiku", category: "Data", sub: "Platform", desc: "AI/ML platform", url: "https://dataiku.com", pricing: "Paid", rating: 4.4, users: "20K+", tags: ["platform"], featured: false, icon: "📊"},
        {name: "Alteryx", category: "Data", sub: "Analytics", desc: "AI analytics automation", url: "https://alteryx.com", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["automation"], featured: false, icon: "⚡"},
        {name: "RapidMiner", category: "Data", sub: "ML", desc: "Data science platform", url: "https://rapidminer.com", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["data-science"], featured: false, icon: "⛏️"},
        {name: "KNIME", category: "Data", sub: "Analytics", desc: "Open source analytics", url: "https://knime.com", pricing: "Free", rating: 4.3, users: "100K+", tags: ["open-source"], featured: false, icon: "🔧"},
        {name: "Tableau AI", category: "Data", sub: "Visualization", desc: "AI-powered BI", url: "https://tableau.com", pricing: "Paid", rating: 4.5, users: "200K+", tags: ["visualization"], featured: false, icon: "📈"},
        {name: "Power BI Copilot", category: "Data", sub: "BI", desc: "AI in Power BI", url: "https://powerbi.microsoft.com", pricing: "Paid", rating: 4.4, users: "500K+", tags: ["bi"], featured: false, icon: "📊"},
        {name: "ThoughtSpot", category: "Data", sub: "Search", desc: "AI-powered analytics", url: "https://thoughtspot.com", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["search"], featured: false, icon: "💭"},
        {name: "Sisense", category: "Data", sub: "BI", desc: "AI analytics platform", url: "https://sisense.com", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["bi"], featured: false, icon: "📊"},
        {name: "Qlik Sense", category: "Data", sub: "BI", desc: "AI-assisted analytics", url: "https://qlik.com", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["bi"], featured: false, icon: "📈"},
    ],

    // ==================== EDUCATION ====================
    education: [
        {name: "Khan Academy Khanmigo", category: "Education", sub: "Tutor", desc: "AI tutor by Khan Academy", url: "https://khanacademy.org/khan-labs", pricing: "Freemium", rating: 4.6, users: "1M+", tags: ["tutoring"], featured: true, icon: "🎓"},
        {name: "Duolingo Max", category: "Education", sub: "Language", desc: "AI language learning", url: "https://duolingo.com", pricing: "Paid", rating: 4.7, users: "50M+", tags: ["language"], featured: true, icon: "🦉"},
        {name: "Photomath", category: "Education", sub: "Math", desc: "AI math solver", url: "https://photomath.com", pricing: "Freemium", rating: 4.6, users: "30M+", tags: ["math"], featured: true, icon: "🔢"},
        {name: "Quizlet Q-Chat", category: "Education", sub: "Study", desc: "AI study assistant", url: "https://quizlet.com", pricing: "Freemium", rating: 4.4, users: "60M+", tags: ["study"], featured: false, icon: "📚"},
        {name: "Socratic by Google", category: "Education", sub: "Homework", desc: "AI homework help", url: "https://socratic.org", pricing: "Free", rating: 4.5, users: "10M+", tags: ["homework"], featured: false, icon: "🎓"},
        {name: "Coursera AI", category: "Education", sub: "Courses", desc: "AI course recommendations", url: "https://coursera.org", pricing: "Freemium", rating: 4.4, users: "100M+", tags: ["courses"], featured: false, icon: "📖"},
        {name: "Brainly", category: "Education", sub: "Q&A", desc: "AI homework Q&A", url: "https://brainly.com", pricing: "Freemium", rating: 4.3, users: "50M+", tags: ["qa"], featured: false, icon: "🧠"},
        {name: "Chegg AI", category: "Education", sub: "Study", desc: "AI study help", url: "https://chegg.com", pricing: "Paid", rating: 4.2, users: "10M+", tags: ["study"], featured: false, icon: "📘"},
        {name: "Mathway", category: "Education", sub: "Math", desc: "AI math problem solver", url: "https://mathway.com", pricing: "Freemium", rating: 4.4, users: "10M+", tags: ["math"], featured: false, icon: "🔢"},
        {name: "Wolfram Alpha", category: "Education", sub: "Computation", desc: "AI computational knowledge", url: "https://wolframalpha.com", pricing: "Freemium", rating: 4.5, users: "10M+", tags: ["computation"], featured: false, icon: "🐺"},
        {name: "Synthesis", category: "Education", sub: "Kids", desc: "AI learning for kids", url: "https://synthesis.is", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["kids"], featured: false, icon: "👶"},
        {name: "Carnegie Learning", category: "Education", sub: "Math", desc: "AI math curriculum", url: "https://carnegielearning.com", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["curriculum"], featured: false, icon: "📐"},
        {name: "Century Tech", category: "Education", sub: "Platform", desc: "AI learning platform", url: "https://century.tech", pricing: "Paid", rating: 4.2, users: "50K+", tags: ["platform"], featured: false, icon: "🏛️"},
        {name: "Querium", category: "Education", sub: "STEM", desc: "AI STEM tutoring", url: "https://querium.com", pricing: "Paid", rating: 4.2, users: "20K+", tags: ["stem"], featured: false, icon: "🔬"},
        {name: "Cognii", category: "Education", sub: "Assessment", desc: "AI assessment", url: "https://cognii.com", pricing: "Paid", rating: 4.1, users: "10K+", tags: ["assessment"], featured: false, icon: "📝"},
    ],

    // ==================== HR & RECRUITING ====================
    hr: [
        {name: "HireVue", category: "HR", sub: "Interviewing", desc: "AI video interviews", url: "https://hirevue.com", pricing: "Paid", rating: 4.2, users: "1K+", tags: ["interviewing"], featured: false, icon: "🎥"},
        {name: "Eightfold AI", category: "HR", sub: "Talent", desc: "AI talent intelligence", url: "https://eightfold.ai", pricing: "Paid", rating: 4.4, users: "500+", tags: ["talent"], featured: true, icon: "8️⃣"},
        {name: "Pymetrics", category: "HR", sub: "Assessment", desc: "AI talent matching", url: "https://pymetrics.ai", pricing: "Paid", rating: 4.1, users: "500+", tags: ["assessment"], featured: false, icon: "🧩"},
        {name: "Textio", category: "HR", sub: "Writing", desc: "AI job descriptions", url: "https://textio.com", pricing: "Paid", rating: 4.3, users: "1K+", tags: ["writing"], featured: false, icon: "✍️"},
        {name: "Phenom", category: "HR", sub: "Talent", desc: "AI talent experience", url: "https://phenom.com", pricing: "Paid", rating: 4.3, users: "5K+", tags: ["experience"], featured: false, icon: "⭐"},
        {name: "Paradox", category: "HR", sub: "Assistant", desc: "AI recruiting assistant", url: "https://paradox.ai", pricing: "Paid", rating: 4.4, users: "5K+", tags: ["assistant"], featured: false, icon: "🤖"},
        {name: "Beamery", category: "HR", sub: "Talent", desc: "AI talent lifecycle", url: "https://beamery.com", pricing: "Paid", rating: 4.2, users: "2K+", tags: ["lifecycle"], featured: false, icon: "✨"},
        {name: "Greenhouse AI", category: "HR", sub: "ATS", desc: "AI recruiting ATS", url: "https://greenhouse.io", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["ats"], featured: false, icon: "🌿"},
        {name: "Lever", category: "HR", sub: "ATS", desc: "AI talent acquisition", url: "https://lever.co", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["ats"], featured: false, icon: "🎯"},
        {name: "Workday AI", category: "HR", sub: "HCM", desc: "AI HR management", url: "https://workday.com", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["hcm"], featured: false, icon: "📊"},
        {name: "SeekOut", category: "HR", sub: "Sourcing", desc: "AI talent sourcing", url: "https://seekout.com", pricing: "Paid", rating: 4.3, users: "5K+", tags: ["sourcing"], featured: false, icon: "🔍"},
        {name: "Fetcher", category: "HR", sub: "Sourcing", desc: "AI recruiting automation", url: "https://fetcher.ai", pricing: "Paid", rating: 4.2, users: "5K+", tags: ["automation"], featured: false, icon: "🤖"},
        {name: "Humanly", category: "HR", sub: "Screening", desc: "AI candidate screening", url: "https://humanly.io", pricing: "Paid", rating: 4.2, users: "2K+", tags: ["screening"], featured: false, icon: "👤"},
        {name: "Ideal", category: "HR", sub: "Screening", desc: "AI talent screening", url: "https://ideal.com", pricing: "Paid", rating: 4.2, users: "2K+", tags: ["screening"], featured: false, icon: "✨"},
        {name: "Entelo", category: "HR", sub: "Sourcing", desc: "AI recruiting platform", url: "https://entelo.com", pricing: "Paid", rating: 4.1, users: "2K+", tags: ["sourcing"], featured: false, icon: "🎯"},
    ],

    // ==================== LEGAL ====================
    legal: [
        {name: "Harvey AI", category: "Legal", sub: "Assistant", desc: "AI legal assistant", url: "https://harvey.ai", pricing: "Enterprise", rating: 4.5, users: "500+", tags: ["assistant"], featured: true, icon: "⚖️"},
        {name: "Casetext", category: "Legal", sub: "Research", desc: "AI legal research", url: "https://casetext.com", pricing: "Paid", rating: 4.6, users: "10K+", tags: ["research"], featured: true, icon: "📚"},
        {name: "DoNotPay", category: "Legal", sub: "Consumer", desc: "AI consumer legal help", url: "https://donotpay.com", pricing: "Paid", rating: 4.0, users: "200K+", tags: ["consumer"], featured: false, icon: "🤖"},
        {name: "Kira Systems", category: "Legal", sub: "Contract", desc: "AI contract analysis", url: "https://kirasystems.com", pricing: "Paid", rating: 4.3, users: "2K+", tags: ["contract"], featured: false, icon: "📄"},
        {name: "Luminance", category: "Legal", sub: "AI Platform", desc: "AI legal platform", url: "https://luminance.com", pricing: "Paid", rating: 4.3, users: "1K+", tags: ["platform"], featured: false, icon: "💡"},
        {name: "LawGeex", category: "Legal", sub: "Contract", desc: "AI contract review", url: "https://lawgeex.com", pricing: "Paid", rating: 4.2, users: "2K+", tags: ["contract"], featured: false, icon: "📋"},
        {name: "Ironclad", category: "Legal", sub: "CLM", desc: "AI contract lifecycle", url: "https://ironcladapp.com", pricing: "Paid", rating: 4.4, users: "5K+", tags: ["clm"], featured: false, icon: "🔒"},
        {name: "Juro", category: "Legal", sub: "Contract", desc: "AI contract automation", url: "https://juro.com", pricing: "Paid", rating: 4.3, users: "3K+", tags: ["automation"], featured: false, icon: "📝"},
        {name: "Lexion", category: "Legal", sub: "CLM", desc: "AI contract management", url: "https://lexion.ai", pricing: "Paid", rating: 4.2, users: "2K+", tags: ["management"], featured: false, icon: "📋"},
        {name: "Evisort", category: "Legal", sub: "Contract", desc: "AI contract intelligence", url: "https://evisort.com", pricing: "Paid", rating: 4.2, users: "2K+", tags: ["intelligence"], featured: false, icon: "👁️"},
        {name: "Spellbook", category: "Legal", sub: "Drafting", desc: "AI contract drafting", url: "https://spellbook.legal", pricing: "Paid", rating: 4.3, users: "5K+", tags: ["drafting"], featured: false, icon: "📖"},
        {name: "Legal Robot", category: "Legal", sub: "Analysis", desc: "AI legal analysis", url: "https://legalrobot.com", pricing: "Paid", rating: 4.0, users: "10K+", tags: ["analysis"], featured: false, icon: "🤖"},
    ],

    // ==================== 3D & GAMING ====================
    threeDGaming: [
        {name: "Meshy", category: "3D", sub: "Generation", desc: "AI 3D model generator", url: "https://meshy.ai", pricing: "Freemium", rating: 4.4, users: "500K+", tags: ["3d"], featured: true, icon: "🎲"},
        {name: "Scenario", category: "3D", sub: "Gaming", desc: "AI game assets", url: "https://scenario.com", pricing: "Freemium", rating: 4.4, users: "100K+", tags: ["gaming"], featured: true, icon: "🎮"},
        {name: "Inworld AI", category: "3D", sub: "NPCs", desc: "AI NPCs for games", url: "https://inworld.ai", pricing: "Freemium", rating: 4.3, users: "50K+", tags: ["npcs"], featured: false, icon: "🤖"},
        {name: "Kaedim", category: "3D", sub: "Generation", desc: "2D to 3D with AI", url: "https://kaedim3d.com", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["3d"], featured: false, icon: "🎯"},
        {name: "Luma AI", category: "3D", sub: "Capture", desc: "AI 3D capture", url: "https://lumalabs.ai", pricing: "Freemium", rating: 4.4, users: "200K+", tags: ["capture"], featured: false, icon: "💫"},
        {name: "Spline AI", category: "3D", sub: "Design", desc: "AI 3D design tool", url: "https://spline.design", pricing: "Freemium", rating: 4.3, users: "500K+", tags: ["design"], featured: false, icon: "🎨"},
        {name: "CSM.ai", category: "3D", sub: "Generation", desc: "AI 3D from images", url: "https://csm.ai", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["generation"], featured: false, icon: "📷"},
        {name: "Masterpiece Studio", category: "3D", sub: "VR", desc: "AI 3D in VR", url: "https://masterpiecestudio.com", pricing: "Paid", rating: 4.2, users: "20K+", tags: ["vr"], featured: false, icon: "🥽"},
        {name: "Sloyd", category: "3D", sub: "Gaming", desc: "AI 3D for games", url: "https://sloyd.ai", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["gaming"], featured: false, icon: "🎮"},
        {name: "Poly.AI", category: "3D", sub: "Voice", desc: "AI voice for games", url: "https://poly.ai", pricing: "Paid", rating: 4.3, users: "20K+", tags: ["voice"], featured: false, icon: "🎤"},
        {name: "Convai", category: "3D", sub: "Characters", desc: "AI game characters", url: "https://convai.com", pricing: "Freemium", rating: 4.2, users: "30K+", tags: ["characters"], featured: false, icon: "👤"},
        {name: "Promethean AI", category: "3D", sub: "Environments", desc: "AI game environments", url: "https://prometheanai.com", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["environments"], featured: false, icon: "🌍"},
    ],

    // ==================== AUTOMATION ====================
    automation: [
        {name: "Zapier AI", category: "Automation", sub: "Workflows", desc: "AI workflow automation", url: "https://zapier.com/ai", pricing: "Freemium", rating: 4.6, users: "2M+", tags: ["workflows"], featured: true, icon: "⚡"},
        {name: "Make (Integromat)", category: "Automation", sub: "Visual", desc: "Visual automation", url: "https://make.com", pricing: "Freemium", rating: 4.5, users: "500K+", tags: ["visual"], featured: true, icon: "🔧"},
        {name: "Bardeen", category: "Automation", sub: "Browser", desc: "AI browser automation", url: "https://bardeen.ai", pricing: "Freemium", rating: 4.4, users: "200K+", tags: ["browser"], featured: false, icon: "🌐"},
        {name: "Browse AI", category: "Automation", sub: "Scraping", desc: "AI web scraping", url: "https://browse.ai", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["scraping"], featured: false, icon: "🔍"},
        {name: "Axiom.ai", category: "Automation", sub: "Browser", desc: "Browser automation", url: "https://axiom.ai", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["browser"], featured: false, icon: "🤖"},
        {name: "Tray.io", category: "Automation", sub: "Enterprise", desc: "Enterprise automation", url: "https://tray.io", pricing: "Paid", rating: 4.3, users: "20K+", tags: ["enterprise"], featured: false, icon: "📊"},
        {name: "Workato", category: "Automation", sub: "Enterprise", desc: "Enterprise integration", url: "https://workato.com", pricing: "Paid", rating: 4.4, users: "20K+", tags: ["integration"], featured: false, icon: "🔗"},
        {name: "n8n", category: "Automation", sub: "Open Source", desc: "Open source automation", url: "https://n8n.io", pricing: "Freemium", rating: 4.4, users: "200K+", tags: ["open-source"], featured: false, icon: "🔧"},
        {name: "Pipedream", category: "Automation", sub: "Developer", desc: "Developer automation", url: "https://pipedream.com", pricing: "Freemium", rating: 4.4, users: "100K+", tags: ["developer"], featured: false, icon: "💻"},
        {name: "Automate.io", category: "Automation", sub: "Simple", desc: "Simple automation", url: "https://automate.io", pricing: "Freemium", rating: 4.2, users: "100K+", tags: ["simple"], featured: false, icon: "🤖"},
        {name: "Activepieces", category: "Automation", sub: "Open Source", desc: "Open source Zapier", url: "https://activepieces.com", pricing: "Freemium", rating: 4.3, users: "50K+", tags: ["open-source"], featured: false, icon: "🧩"},
        {name: "Robocorp", category: "Automation", sub: "RPA", desc: "AI-powered RPA", url: "https://robocorp.com", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["rpa"], featured: false, icon: "🤖"},
    ],

    // ==================== AI AGENTS ====================
    agents: [
        {name: "AutoGPT", category: "Agents", sub: "Autonomous", desc: "Open source AI agent", url: "https://github.com/Significant-Gravitas/AutoGPT", pricing: "Free", rating: 4.3, users: "150K+", tags: ["autonomous"], featured: true, icon: "🤖"},
        {name: "AgentGPT", category: "Agents", sub: "Browser", desc: "AI agents in browser", url: "https://agentgpt.reworkd.ai", pricing: "Freemium", rating: 4.2, users: "100K+", tags: ["browser"], featured: false, icon: "🕵️"},
        {name: "CrewAI", category: "Agents", sub: "Multi-agent", desc: "Multi-agent orchestration", url: "https://crewai.com", pricing: "Free", rating: 4.4, users: "50K+", tags: ["multi-agent"], featured: true, icon: "👥"},
        {name: "BabyAGI", category: "Agents", sub: "Autonomous", desc: "Task-driven AI agent", url: "https://github.com/yoheinakajima/babyagi", pricing: "Free", rating: 4.1, users: "50K+", tags: ["autonomous"], featured: false, icon: "👶"},
        {name: "SuperAGI", category: "Agents", sub: "Framework", desc: "AI agent framework", url: "https://superagi.com", pricing: "Freemium", rating: 4.2, users: "30K+", tags: ["framework"], featured: false, icon: "🦸"},
        {name: "Langchain Agents", category: "Agents", sub: "Framework", desc: "Agent framework", url: "https://langchain.com", pricing: "Free", rating: 4.5, users: "200K+", tags: ["framework"], featured: false, icon: "🔗"},
        {name: "Fixie.ai", category: "Agents", sub: "Platform", desc: "AI agent platform", url: "https://fixie.ai", pricing: "Freemium", rating: 4.2, users: "20K+", tags: ["platform"], featured: false, icon: "🔧"},
        {name: "Sweep", category: "Agents", sub: "Coding", desc: "AI coding agent", url: "https://sweep.dev", pricing: "Freemium", rating: 4.3, users: "50K+", tags: ["coding"], featured: false, icon: "🧹"},
        {name: "GPT Pilot", category: "Agents", sub: "Coding", desc: "AI dev agent", url: "https://github.com/Pythagora-io/gpt-pilot", pricing: "Free", rating: 4.3, users: "30K+", tags: ["coding"], featured: false, icon: "✈️"},
        {name: "Devin", category: "Agents", sub: "Coding", desc: "AI software engineer", url: "https://cognition-labs.com", pricing: "Waitlist", rating: 4.5, users: "0", tags: ["coding"], featured: true, icon: "👨‍💻"},
        {name: "MultiOn", category: "Agents", sub: "Browser", desc: "AI browser agent", url: "https://multion.ai", pricing: "Freemium", rating: 4.2, users: "30K+", tags: ["browser"], featured: false, icon: "🌐"},
        {name: "Adept AI", category: "Agents", sub: "General", desc: "General AI agent", url: "https://adept.ai", pricing: "Waitlist", rating: 4.3, users: "0", tags: ["general"], featured: false, icon: "🎯"},
    ],

    // ==================== API & INFRASTRUCTURE ====================
    api: [
        {name: "OpenAI API", category: "API", sub: "LLM", desc: "GPT-4, DALL-E, Whisper", url: "https://platform.openai.com", pricing: "Pay-per-use", rating: 4.8, users: "2M+", tags: ["llm"], featured: true, icon: "🔌"},
        {name: "Anthropic Claude API", category: "API", sub: "LLM", desc: "Claude models API", url: "https://anthropic.com/api", pricing: "Pay-per-use", rating: 4.7, users: "500K+", tags: ["llm"], featured: true, icon: "🤖"},
        {name: "Hugging Face", category: "API", sub: "Platform", desc: "ML model hub", url: "https://huggingface.co", pricing: "Freemium", rating: 4.8, users: "500K+", tags: ["models"], featured: true, icon: "🤗"},
        {name: "Replicate", category: "API", sub: "Models", desc: "Run ML models via API", url: "https://replicate.com", pricing: "Pay-per-use", rating: 4.5, users: "200K+", tags: ["api"], featured: false, icon: "🔄"},
        {name: "Together AI", category: "API", sub: "LLM", desc: "Open source LLM API", url: "https://together.ai", pricing: "Pay-per-use", rating: 4.4, users: "100K+", tags: ["llm"], featured: false, icon: "🤝"},
        {name: "Groq", category: "API", sub: "Fast Inference", desc: "Ultra-fast LLM inference", url: "https://groq.com", pricing: "Freemium", rating: 4.6, users: "200K+", tags: ["fast"], featured: true, icon: "⚡"},
        {name: "Fireworks AI", category: "API", sub: "Inference", desc: "Fast model inference", url: "https://fireworks.ai", pricing: "Pay-per-use", rating: 4.4, users: "50K+", tags: ["inference"], featured: false, icon: "🎆"},
        {name: "Anyscale", category: "API", sub: "LLM", desc: "LLM platform", url: "https://anyscale.com", pricing: "Pay-per-use", rating: 4.3, users: "50K+", tags: ["platform"], featured: false, icon: "📊"},
        {name: "Modal", category: "API", sub: "Infrastructure", desc: "ML infrastructure", url: "https://modal.com", pricing: "Pay-per-use", rating: 4.4, users: "50K+", tags: ["infra"], featured: false, icon: "🖥️"},
        {name: "Banana.dev", category: "API", sub: "Inference", desc: "ML model deployment", url: "https://banana.dev", pricing: "Pay-per-use", rating: 4.2, users: "30K+", tags: ["deployment"], featured: false, icon: "🍌"},
        {name: "RunPod", category: "API", sub: "GPU", desc: "GPU cloud for AI", url: "https://runpod.io", pricing: "Pay-per-use", rating: 4.4, users: "100K+", tags: ["gpu"], featured: false, icon: "🚀"},
        {name: "Lambda Labs", category: "API", sub: "GPU", desc: "GPU cloud", url: "https://lambdalabs.com", pricing: "Pay-per-use", rating: 4.3, users: "50K+", tags: ["gpu"], featured: false, icon: "λ"},
        {name: "Paperspace", category: "API", sub: "GPU", desc: "ML cloud platform", url: "https://paperspace.com", pricing: "Pay-per-use", rating: 4.3, users: "100K+", tags: ["cloud"], featured: false, icon: "📄"},
        {name: "Cohere", category: "API", sub: "LLM", desc: "Enterprise LLM API", url: "https://cohere.com", pricing: "Pay-per-use", rating: 4.4, users: "50K+", tags: ["enterprise"], featured: false, icon: "🔮"},
        {name: "AI21 Labs", category: "API", sub: "LLM", desc: "Jurassic models API", url: "https://ai21.com", pricing: "Pay-per-use", rating: 4.3, users: "30K+", tags: ["llm"], featured: false, icon: "🦕"},
    ]
};

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_DATABASE_3 = AI_TOOLS_DATABASE_3;
}


