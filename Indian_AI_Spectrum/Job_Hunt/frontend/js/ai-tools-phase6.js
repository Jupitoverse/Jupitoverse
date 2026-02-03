// AI Tools Database - Phase 6: Research, Education & Productivity AI
// 200+ Tools for researchers, students, and professionals

const AI_TOOLS_PHASE6 = [
    // ==================== RESEARCH & ACADEMIC ====================
    {name: "Semantic Scholar", category: "Research", subcategory: "Academic Search", desc: "AI-powered academic search engine", url: "semanticscholar.org", pricing: "Free", rating: 4.7, tags: ["academic", "papers", "ai"], featured: true},
    {name: "Elicit", category: "Research", subcategory: "Research Assistant", desc: "AI research assistant for papers", url: "elicit.org", pricing: "Freemium", rating: 4.6, tags: ["papers", "literature-review", "ai"], featured: true},
    {name: "Consensus", category: "Research", subcategory: "Academic Search", desc: "AI search engine for research papers", url: "consensus.app", pricing: "Freemium", rating: 4.5, tags: ["evidence", "papers", "claims"]},
    {name: "Scite.ai", category: "Research", subcategory: "Citation Analysis", desc: "Smart citations for research", url: "scite.ai", pricing: "Freemium", rating: 4.5, tags: ["citations", "supporting", "contrasting"]},
    {name: "Connected Papers", category: "Research", subcategory: "Literature Review", desc: "Visual literature exploration", url: "connectedpapers.com", pricing: "Freemium", rating: 4.5, tags: ["visualization", "graph", "related"]},
    {name: "Research Rabbit", category: "Research", subcategory: "Literature Discovery", desc: "AI for discovering research papers", url: "researchrabbit.ai", pricing: "Free", rating: 4.5, tags: ["discovery", "recommendations", "free"]},
    {name: "Litmaps", category: "Research", subcategory: "Literature Mapping", desc: "Visual citation network exploration", url: "litmaps.com", pricing: "Freemium", rating: 4.4, tags: ["visualization", "citations", "mapping"]},
    {name: "Inciteful", category: "Research", subcategory: "Paper Discovery", desc: "Citation network analysis", url: "inciteful.xyz", pricing: "Free", rating: 4.3, tags: ["network", "free", "discovery"]},
    {name: "Paperpal", category: "Research", subcategory: "Academic Writing", desc: "AI writing assistant for researchers", url: "paperpal.com", pricing: "Freemium", rating: 4.4, tags: ["writing", "academic", "grammar"]},
    {name: "Trinka", category: "Research", subcategory: "Academic Writing", desc: "AI grammar checker for academic writing", url: "trinka.ai", pricing: "Freemium", rating: 4.3, tags: ["grammar", "academic", "technical"]},
    {name: "Writefull", category: "Research", subcategory: "Academic Writing", desc: "AI for academic writing feedback", url: "writefull.com", pricing: "Freemium", rating: 4.4, tags: ["feedback", "academic", "language"]},
    {name: "Jenni AI", category: "Research", subcategory: "Academic Writing", desc: "AI writing assistant for research", url: "jenni.ai", pricing: "Freemium", rating: 4.3, tags: ["writing", "citations", "research"]},
    {name: "SciSpace (Typeset)", category: "Research", subcategory: "Research Platform", desc: "AI-powered research platform", url: "typeset.io", pricing: "Freemium", rating: 4.4, tags: ["copilot", "papers", "explanation"]},
    {name: "Explainpaper", category: "Research", subcategory: "Paper Understanding", desc: "AI to explain research papers", url: "explainpaper.com", pricing: "Freemium", rating: 4.4, tags: ["explanation", "highlight", "simple"]},
    {name: "ChatPaper", category: "Research", subcategory: "Paper Analysis", desc: "Chat with academic papers", url: "chatpaper.org", pricing: "Free", rating: 4.2, tags: ["chat", "papers", "analysis"]},
    {name: "Mendeley", category: "Research", subcategory: "Reference Manager", desc: "Reference manager and academic network", url: "mendeley.com", pricing: "Free", rating: 4.3, tags: ["references", "collaboration", "elsevier"]},
    {name: "Zotero", category: "Research", subcategory: "Reference Manager", desc: "Free reference management tool", url: "zotero.org", pricing: "Free", rating: 4.6, tags: ["open-source", "free", "references"]},
    {name: "EndNote", category: "Research", subcategory: "Reference Manager", desc: "Professional reference management", url: "endnote.com", pricing: "Paid", rating: 4.2, tags: ["professional", "references", "clarivate"]},
    {name: "Paperpile", category: "Research", subcategory: "Reference Manager", desc: "Reference manager for Google Docs", url: "paperpile.com", pricing: "Paid", rating: 4.4, tags: ["google-docs", "pdf", "modern"]},
    {name: "ReadCube Papers", category: "Research", subcategory: "Reference Manager", desc: "Reference manager with AI features", url: "papersapp.com", pricing: "Freemium", rating: 4.3, tags: ["ai", "recommendations", "reading"]},
    
    // ==================== EDUCATION & LEARNING ====================
    {name: "Khan Academy Khanmigo", category: "Education", subcategory: "AI Tutor", desc: "AI tutor powered by GPT-4", url: "khanacademy.org", pricing: "Freemium", rating: 4.7, tags: ["tutor", "personalized", "k-12"], featured: true},
    {name: "Duolingo Max", category: "Education", subcategory: "Language Learning", desc: "AI-powered language learning", url: "duolingo.com", pricing: "Freemium", rating: 4.6, tags: ["languages", "gamified", "ai"], featured: true},
    {name: "Quizlet", category: "Education", subcategory: "Flashcards", desc: "AI-enhanced flashcard learning", url: "quizlet.com", pricing: "Freemium", rating: 4.5, tags: ["flashcards", "study", "ai"]},
    {name: "Anki", category: "Education", subcategory: "Flashcards", desc: "Spaced repetition flashcard app", url: "apps.ankiweb.net", pricing: "Free", rating: 4.6, tags: ["spaced-repetition", "free", "customizable"]},
    {name: "Brainscape", category: "Education", subcategory: "Flashcards", desc: "Adaptive flashcard learning", url: "brainscape.com", pricing: "Freemium", rating: 4.3, tags: ["adaptive", "flashcards", "science"]},
    {name: "Coursera", category: "Education", subcategory: "Online Courses", desc: "Online courses with AI features", url: "coursera.org", pricing: "Freemium", rating: 4.5, tags: ["courses", "universities", "certificates"]},
    {name: "Udemy", category: "Education", subcategory: "Online Courses", desc: "Marketplace for online courses", url: "udemy.com", pricing: "Marketplace", rating: 4.3, tags: ["courses", "marketplace", "skills"]},
    {name: "edX", category: "Education", subcategory: "Online Courses", desc: "University courses online", url: "edx.org", pricing: "Freemium", rating: 4.4, tags: ["universities", "degrees", "certificates"]},
    {name: "Skillshare", category: "Education", subcategory: "Creative Learning", desc: "Online classes for creatives", url: "skillshare.com", pricing: "Paid", rating: 4.3, tags: ["creative", "skills", "projects"]},
    {name: "Brilliant", category: "Education", subcategory: "STEM Learning", desc: "Interactive STEM learning", url: "brilliant.org", pricing: "Freemium", rating: 4.6, tags: ["stem", "interactive", "problem-solving"]},
    {name: "Socratic by Google", category: "Education", subcategory: "Homework Help", desc: "AI homework helper", url: "socratic.org", pricing: "Free", rating: 4.4, tags: ["homework", "google", "free"]},
    {name: "Photomath", category: "Education", subcategory: "Math Solver", desc: "AI math problem solver", url: "photomath.com", pricing: "Freemium", rating: 4.5, tags: ["math", "camera", "step-by-step"]},
    {name: "Mathway", category: "Education", subcategory: "Math Solver", desc: "AI math problem solver", url: "mathway.com", pricing: "Freemium", rating: 4.4, tags: ["math", "solver", "explanations"]},
    {name: "Wolfram Alpha", category: "Education", subcategory: "Computational", desc: "Computational knowledge engine", url: "wolframalpha.com", pricing: "Freemium", rating: 4.6, tags: ["math", "science", "knowledge"]},
    {name: "Symbolab", category: "Education", subcategory: "Math Solver", desc: "AI-powered math calculator", url: "symbolab.com", pricing: "Freemium", rating: 4.4, tags: ["math", "calculator", "step-by-step"]},
    {name: "Chegg", category: "Education", subcategory: "Homework Help", desc: "Homework help and tutoring", url: "chegg.com", pricing: "Paid", rating: 4.1, tags: ["homework", "tutoring", "textbooks"]},
    {name: "Bartleby", category: "Education", subcategory: "Homework Help", desc: "Homework solutions and help", url: "bartleby.com", pricing: "Paid", rating: 4.0, tags: ["homework", "solutions", "textbooks"]},
    {name: "Kahoot!", category: "Education", subcategory: "Quizzes", desc: "Game-based learning platform", url: "kahoot.com", pricing: "Freemium", rating: 4.5, tags: ["games", "quizzes", "engagement"]},
    {name: "Quizizz", category: "Education", subcategory: "Quizzes", desc: "Interactive quiz platform", url: "quizizz.com", pricing: "Freemium", rating: 4.4, tags: ["quizzes", "interactive", "fun"]},
    {name: "Edpuzzle", category: "Education", subcategory: "Video Learning", desc: "Interactive video lessons", url: "edpuzzle.com", pricing: "Freemium", rating: 4.4, tags: ["video", "interactive", "assessment"]},
    
    // ==================== NOTE-TAKING & KNOWLEDGE ====================
    {name: "Notion", category: "Productivity", subcategory: "All-in-One", desc: "All-in-one workspace with AI", url: "notion.so", pricing: "Freemium", rating: 4.8, tags: ["workspace", "docs", "database"], featured: true},
    {name: "Obsidian", category: "Productivity", subcategory: "Knowledge Base", desc: "Knowledge base and note-taking", url: "obsidian.md", pricing: "Freemium", rating: 4.7, tags: ["markdown", "linking", "local"], featured: true},
    {name: "Roam Research", category: "Productivity", subcategory: "Knowledge Base", desc: "Note-taking for networked thought", url: "roamresearch.com", pricing: "Paid", rating: 4.5, tags: ["linking", "graph", "research"]},
    {name: "Logseq", category: "Productivity", subcategory: "Knowledge Base", desc: "Open-source knowledge base", url: "logseq.com", pricing: "Free", rating: 4.5, tags: ["open-source", "privacy", "outliner"]},
    {name: "Mem", category: "Productivity", subcategory: "AI Notes", desc: "AI-powered note-taking", url: "mem.ai", pricing: "Freemium", rating: 4.4, tags: ["ai", "auto-organize", "search"]},
    {name: "Reflect", category: "Productivity", subcategory: "AI Notes", desc: "AI-powered personal notes", url: "reflect.app", pricing: "Paid", rating: 4.4, tags: ["ai", "backlinks", "personal"]},
    {name: "Tana", category: "Productivity", subcategory: "Knowledge Base", desc: "Supertag-based workspace", url: "tana.inc", pricing: "Freemium", rating: 4.3, tags: ["supertags", "flexible", "ai"]},
    {name: "Capacities", category: "Productivity", subcategory: "Knowledge Base", desc: "Object-based note-taking", url: "capacities.io", pricing: "Freemium", rating: 4.3, tags: ["objects", "studio", "personal"]},
    {name: "Craft", category: "Productivity", subcategory: "Documents", desc: "Beautiful document creation", url: "craft.do", pricing: "Freemium", rating: 4.5, tags: ["beautiful", "apple", "collaboration"]},
    {name: "Coda", category: "Productivity", subcategory: "Docs", desc: "Doc that brings it all together", url: "coda.io", pricing: "Freemium", rating: 4.4, tags: ["docs", "apps", "automation"]},
    {name: "Bear", category: "Productivity", subcategory: "Notes", desc: "Beautiful markdown notes for Apple", url: "bear.app", pricing: "Freemium", rating: 4.5, tags: ["apple", "markdown", "beautiful"]},
    {name: "Ulysses", category: "Productivity", subcategory: "Writing", desc: "Writing app for Apple devices", url: "ulysses.app", pricing: "Paid", rating: 4.5, tags: ["apple", "writing", "distraction-free"]},
    {name: "iA Writer", category: "Productivity", subcategory: "Writing", desc: "Focused writing app", url: "ia.net/writer", pricing: "Paid", rating: 4.5, tags: ["focus", "markdown", "minimal"]},
    {name: "Typora", category: "Productivity", subcategory: "Markdown", desc: "Seamless markdown editor", url: "typora.io", pricing: "Paid", rating: 4.4, tags: ["markdown", "wysiwyg", "beautiful"]},
    {name: "Nota", category: "Productivity", subcategory: "Markdown", desc: "Modern markdown editor", url: "nota.md", pricing: "Freemium", rating: 4.2, tags: ["markdown", "modern", "pro"]},
    
    // ==================== PERSONAL AI ASSISTANTS ====================
    {name: "Apple Intelligence", category: "AI Assistant", subcategory: "Device AI", desc: "AI integrated into Apple devices", url: "apple.com", pricing: "Included", rating: 4.5, tags: ["apple", "siri", "private"], featured: true},
    {name: "Google Assistant", category: "AI Assistant", subcategory: "Device AI", desc: "Google's AI assistant", url: "assistant.google.com", pricing: "Free", rating: 4.5, tags: ["google", "smart-home", "search"]},
    {name: "Amazon Alexa", category: "AI Assistant", subcategory: "Device AI", desc: "Amazon's voice AI assistant", url: "alexa.amazon.com", pricing: "Free", rating: 4.3, tags: ["amazon", "smart-home", "voice"]},
    {name: "Rabbit R1", category: "AI Assistant", subcategory: "Hardware", desc: "AI pocket companion device", url: "rabbit.tech", pricing: "Paid", rating: 4.0, tags: ["hardware", "lam", "agent"]},
    {name: "Humane AI Pin", category: "AI Assistant", subcategory: "Hardware", desc: "Wearable AI assistant", url: "humane.com", pricing: "Paid", rating: 3.5, tags: ["wearable", "screenless", "ambient"]},
    {name: "Tab AI", category: "AI Assistant", subcategory: "Wearable", desc: "AI wearable for memory", url: "mytab.ai", pricing: "Paid", rating: 4.0, tags: ["wearable", "memory", "context"]},
    {name: "Rewind AI", category: "AI Assistant", subcategory: "Memory", desc: "AI that remembers everything", url: "rewind.ai", pricing: "Freemium", rating: 4.4, tags: ["memory", "search", "mac"]},
    {name: "Recall AI", category: "AI Assistant", subcategory: "Memory", desc: "AI meeting memory assistant", url: "recall.ai", pricing: "Freemium", rating: 4.2, tags: ["meetings", "memory", "api"]},
    {name: "Personal AI", category: "AI Assistant", subcategory: "Personal", desc: "Train your personal AI", url: "personal.ai", pricing: "Freemium", rating: 4.1, tags: ["personal", "training", "memory"]},
    {name: "Embra", category: "AI Assistant", subcategory: "Mac AI", desc: "AI assistant for Mac", url: "embra.app", pricing: "Paid", rating: 4.2, tags: ["mac", "contextual", "assistant"]},
    
    // ==================== CALENDAR & SCHEDULING ====================
    {name: "Calendly", category: "Scheduling", subcategory: "Booking", desc: "Appointment scheduling software", url: "calendly.com", pricing: "Freemium", rating: 4.6, tags: ["booking", "scheduling", "meetings"], featured: true},
    {name: "Cal.com", category: "Scheduling", subcategory: "Booking", desc: "Open-source scheduling", url: "cal.com", pricing: "Freemium", rating: 4.5, tags: ["open-source", "scheduling", "booking"]},
    {name: "Reclaim.ai", category: "Scheduling", subcategory: "Smart Calendar", desc: "AI calendar management", url: "reclaim.ai", pricing: "Freemium", rating: 4.5, tags: ["ai", "time-blocking", "habits"]},
    {name: "Clockwise", category: "Scheduling", subcategory: "Smart Calendar", desc: "AI calendar optimization", url: "getclockwise.com", pricing: "Freemium", rating: 4.4, tags: ["ai", "focus-time", "optimization"]},
    {name: "Motion", category: "Scheduling", subcategory: "AI Planner", desc: "AI-powered daily planner", url: "usemotion.com", pricing: "Paid", rating: 4.5, tags: ["ai", "planning", "tasks"]},
    {name: "SavvyCal", category: "Scheduling", subcategory: "Booking", desc: "Scheduling that recipients love", url: "savvycal.com", pricing: "Paid", rating: 4.4, tags: ["scheduling", "overlay", "friendly"]},
    {name: "Doodle", category: "Scheduling", subcategory: "Group Scheduling", desc: "Group scheduling made easy", url: "doodle.com", pricing: "Freemium", rating: 4.3, tags: ["polling", "group", "meetings"]},
    {name: "When2meet", category: "Scheduling", subcategory: "Group Scheduling", desc: "Simple group scheduling", url: "when2meet.com", pricing: "Free", rating: 4.2, tags: ["free", "simple", "group"]},
    {name: "Fantastical", category: "Scheduling", subcategory: "Calendar App", desc: "Calendar app for Apple", url: "flexibits.com/fantastical", pricing: "Paid", rating: 4.6, tags: ["apple", "natural-language", "beautiful"]},
    {name: "Amie", category: "Scheduling", subcategory: "Calendar App", desc: "Beautiful calendar and tasks", url: "amie.so", pricing: "Freemium", rating: 4.4, tags: ["beautiful", "tasks", "scheduling"]},
    
    // ==================== MEETING & COLLABORATION ====================
    {name: "Zoom", category: "Meetings", subcategory: "Video Conferencing", desc: "Video conferencing platform", url: "zoom.us", pricing: "Freemium", rating: 4.5, tags: ["video", "conferencing", "webinars"], featured: true},
    {name: "Microsoft Teams", category: "Meetings", subcategory: "Collaboration", desc: "Team collaboration with AI", url: "microsoft.com/teams", pricing: "Freemium", rating: 4.4, tags: ["microsoft", "collaboration", "chat"]},
    {name: "Google Meet", category: "Meetings", subcategory: "Video Conferencing", desc: "Google's video meeting solution", url: "meet.google.com", pricing: "Freemium", rating: 4.4, tags: ["google", "simple", "free"]},
    {name: "Slack", category: "Meetings", subcategory: "Team Chat", desc: "Team communication with AI", url: "slack.com", pricing: "Freemium", rating: 4.5, tags: ["chat", "channels", "integrations"]},
    {name: "Discord", category: "Meetings", subcategory: "Community", desc: "Community platform for chat", url: "discord.com", pricing: "Freemium", rating: 4.5, tags: ["community", "voice", "gaming"]},
    {name: "Krisp", category: "Meetings", subcategory: "Noise Cancellation", desc: "AI noise cancellation for calls", url: "krisp.ai", pricing: "Freemium", rating: 4.6, tags: ["noise", "cancellation", "calls"]},
    {name: "Fathom", category: "Meetings", subcategory: "Meeting Notes", desc: "AI meeting assistant", url: "fathom.video", pricing: "Freemium", rating: 4.5, tags: ["notes", "transcription", "free"]},
    {name: "Fireflies.ai", category: "Meetings", subcategory: "Meeting Notes", desc: "AI meeting transcription", url: "fireflies.ai", pricing: "Freemium", rating: 4.5, tags: ["transcription", "notes", "search"]},
    {name: "Otter.ai", category: "Meetings", subcategory: "Transcription", desc: "AI meeting notes and transcription", url: "otter.ai", pricing: "Freemium", rating: 4.6, tags: ["transcription", "live", "search"]},
    {name: "Grain", category: "Meetings", subcategory: "Meeting Clips", desc: "Record and share meeting highlights", url: "grain.com", pricing: "Freemium", rating: 4.4, tags: ["highlights", "clips", "sharing"]},
    {name: "tl;dv", category: "Meetings", subcategory: "Meeting Recording", desc: "AI meeting recorder", url: "tldv.io", pricing: "Freemium", rating: 4.4, tags: ["recording", "highlights", "free"]},
    {name: "Read.ai", category: "Meetings", subcategory: "Meeting Analytics", desc: "AI meeting analytics and coaching", url: "read.ai", pricing: "Freemium", rating: 4.3, tags: ["analytics", "coaching", "engagement"]},
    {name: "Avoma", category: "Meetings", subcategory: "Revenue Intelligence", desc: "AI meeting assistant for sales", url: "avoma.com", pricing: "Paid", rating: 4.3, tags: ["sales", "intelligence", "coaching"]},
    {name: "Vowel", category: "Meetings", subcategory: "Video Meetings", desc: "AI-powered video meetings", url: "vowel.com", pricing: "Freemium", rating: 4.2, tags: ["video", "ai", "transcription"]},
    {name: "Around", category: "Meetings", subcategory: "Video Meetings", desc: "Distraction-free video calls", url: "around.co", pricing: "Free", rating: 4.2, tags: ["floating", "minimal", "focus"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE6 = AI_TOOLS_PHASE6;
}


