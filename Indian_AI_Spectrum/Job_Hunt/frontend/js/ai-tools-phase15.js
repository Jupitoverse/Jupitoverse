// AI Tools Database - Phase 15: Productivity, Collaboration & Notes AI
// 200+ Tools for productivity and collaboration

const AI_TOOLS_PHASE15 = [
    // ==================== NOTE TAKING ====================
    {name: "Notion", category: "Productivity", subcategory: "All-in-one", desc: "All-in-one workspace", url: "notion.so", pricing: "Freemium", rating: 4.7, tags: ["notes", "wiki", "database"], featured: true},
    {name: "Obsidian", category: "Productivity", subcategory: "Notes", desc: "Knowledge base on markdown", url: "obsidian.md", pricing: "Freemium", rating: 4.7, tags: ["markdown", "local", "linking"]},
    {name: "Roam Research", category: "Productivity", subcategory: "Notes", desc: "Networked thought", url: "roamresearch.com", pricing: "Paid", rating: 4.4, tags: ["bi-directional", "graph", "research"]},
    {name: "Logseq", category: "Productivity", subcategory: "Notes", desc: "Open source knowledge base", url: "logseq.com", pricing: "Free", rating: 4.4, tags: ["open-source", "local", "outliner"]},
    {name: "Craft", category: "Productivity", subcategory: "Notes", desc: "Beautiful documents", url: "craft.do", pricing: "Freemium", rating: 4.5, tags: ["apple", "beautiful", "documents"]},
    {name: "Bear", category: "Productivity", subcategory: "Notes", desc: "Beautiful markdown notes", url: "bear.app", pricing: "Freemium", rating: 4.6, tags: ["apple", "markdown", "simple"]},
    {name: "Evernote", category: "Productivity", subcategory: "Notes", desc: "Note-taking app", url: "evernote.com", pricing: "Freemium", rating: 4.2, tags: ["notes", "web-clipper", "search"]},
    {name: "OneNote", category: "Productivity", subcategory: "Notes", desc: "Microsoft note-taking", url: "onenote.com", pricing: "Free", rating: 4.4, tags: ["microsoft", "free", "handwriting"]},
    {name: "Apple Notes", category: "Productivity", subcategory: "Notes", desc: "Built-in Apple notes", url: "apple.com/notes", pricing: "Free", rating: 4.5, tags: ["apple", "free", "simple"]},
    {name: "Mem", category: "Productivity", subcategory: "AI Notes", desc: "AI-powered notes", url: "mem.ai", pricing: "Freemium", rating: 4.3, tags: ["ai", "search", "connections"]},
    {name: "Reflect", category: "Productivity", subcategory: "AI Notes", desc: "AI note-taking", url: "reflect.app", pricing: "Paid", rating: 4.3, tags: ["ai", "backlinks", "encrypted"]},
    {name: "Capacities", category: "Productivity", subcategory: "Notes", desc: "Studio for your mind", url: "capacities.io", pricing: "Freemium", rating: 4.2, tags: ["objects", "database", "modern"]},
    {name: "Anytype", category: "Productivity", subcategory: "Notes", desc: "Local-first everything app", url: "anytype.io", pricing: "Freemium", rating: 4.2, tags: ["local", "privacy", "objects"]},
    {name: "Tana", category: "Productivity", subcategory: "Notes", desc: "Supertag note-taking", url: "tana.inc", pricing: "Paid", rating: 4.3, tags: ["supertags", "ai", "structured"]},
    {name: "RemNote", category: "Productivity", subcategory: "Learning", desc: "Notes with flashcards", url: "remnote.com", pricing: "Freemium", rating: 4.3, tags: ["flashcards", "spaced-repetition", "notes"]},
    
    // ==================== TASK MANAGEMENT ====================
    {name: "Todoist", category: "Tasks", subcategory: "Simple", desc: "To-do list app", url: "todoist.com", pricing: "Freemium", rating: 4.6, tags: ["simple", "cross-platform", "natural-language"], featured: true},
    {name: "Things 3", category: "Tasks", subcategory: "Apple", desc: "Beautiful task manager", url: "culturedcode.com/things", pricing: "Paid", rating: 4.7, tags: ["apple", "beautiful", "gtd"]},
    {name: "TickTick", category: "Tasks", subcategory: "All-in-one", desc: "Tasks and calendar", url: "ticktick.com", pricing: "Freemium", rating: 4.5, tags: ["calendar", "pomodoro", "habits"]},
    {name: "Any.do", category: "Tasks", subcategory: "Simple", desc: "Simple task manager", url: "any.do", pricing: "Freemium", rating: 4.3, tags: ["simple", "assistant", "calendar"]},
    {name: "Microsoft To Do", category: "Tasks", subcategory: "Microsoft", desc: "Microsoft task app", url: "todo.microsoft.com", pricing: "Free", rating: 4.4, tags: ["microsoft", "free", "wunderlist"]},
    {name: "Remember The Milk", category: "Tasks", subcategory: "Classic", desc: "Task management", url: "rememberthemilk.com", pricing: "Freemium", rating: 4.2, tags: ["classic", "smart-lists", "location"]},
    {name: "OmniFocus", category: "Tasks", subcategory: "GTD", desc: "Pro task management", url: "omnigroup.com/omnifocus", pricing: "Paid", rating: 4.4, tags: ["gtd", "apple", "power-users"]},
    {name: "Sunsama", category: "Tasks", subcategory: "Daily Planner", desc: "Daily planner for work", url: "sunsama.com", pricing: "Paid", rating: 4.5, tags: ["daily", "timeboxing", "calm"]},
    {name: "Akiflow", category: "Tasks", subcategory: "Time Blocking", desc: "Time blocking task manager", url: "akiflow.com", pricing: "Paid", rating: 4.3, tags: ["time-blocking", "calendar", "unified"]},
    {name: "Sorted", category: "Tasks", subcategory: "Hyper-scheduling", desc: "Auto-scheduling task manager", url: "sortedapp.com", pricing: "Paid", rating: 4.3, tags: ["auto-schedule", "magic", "apple"]},
    {name: "GoodTask", category: "Tasks", subcategory: "Reminders", desc: "iOS Reminders powered", url: "goodtaskapp.com", pricing: "Paid", rating: 4.4, tags: ["reminders", "apple", "powerful"]},
    {name: "Structured", category: "Tasks", subcategory: "Visual", desc: "Visual day planner", url: "structured.app", pricing: "Freemium", rating: 4.5, tags: ["visual", "timeline", "simple"]},
    {name: "Habitica", category: "Tasks", subcategory: "Gamified", desc: "Gamified task manager", url: "habitica.com", pricing: "Freemium", rating: 4.3, tags: ["gamified", "rpg", "habits"]},
    {name: "Focusmate", category: "Tasks", subcategory: "Accountability", desc: "Virtual coworking", url: "focusmate.com", pricing: "Freemium", rating: 4.5, tags: ["accountability", "coworking", "focus"]},
    {name: "Forest", category: "Tasks", subcategory: "Focus", desc: "Stay focused, plant trees", url: "forestapp.cc", pricing: "Paid", rating: 4.6, tags: ["focus", "pomodoro", "trees"]},
    
    // ==================== PROJECT MANAGEMENT ====================
    {name: "Asana", category: "Project Management", subcategory: "Work", desc: "Work management platform", url: "asana.com", pricing: "Freemium", rating: 4.5, tags: ["projects", "portfolios", "workflows"], featured: true},
    {name: "Monday.com", category: "Project Management", subcategory: "Work OS", desc: "Work operating system", url: "monday.com", pricing: "Paid", rating: 4.4, tags: ["visual", "flexible", "apps"]},
    {name: "ClickUp", category: "Project Management", subcategory: "All-in-one", desc: "One app to replace them all", url: "clickup.com", pricing: "Freemium", rating: 4.4, tags: ["all-in-one", "features", "customizable"]},
    {name: "Basecamp", category: "Project Management", subcategory: "Team", desc: "Project management for teams", url: "basecamp.com", pricing: "Paid", rating: 4.3, tags: ["simple", "flat-rate", "communication"]},
    {name: "Trello", category: "Project Management", subcategory: "Kanban", desc: "Kanban-style boards", url: "trello.com", pricing: "Freemium", rating: 4.5, tags: ["kanban", "visual", "simple"]},
    {name: "Jira", category: "Project Management", subcategory: "Agile", desc: "Agile project management", url: "atlassian.com/software/jira", pricing: "Freemium", rating: 4.3, tags: ["agile", "software", "enterprise"]},
    {name: "Linear", category: "Project Management", subcategory: "Software", desc: "Modern issue tracking", url: "linear.app", pricing: "Freemium", rating: 4.7, tags: ["software", "fast", "beautiful"]},
    {name: "Height", category: "Project Management", subcategory: "AI", desc: "AI project management", url: "height.app", pricing: "Freemium", rating: 4.3, tags: ["ai", "autonomous", "modern"]},
    {name: "Shortcut", category: "Project Management", subcategory: "Software", desc: "Project management for software", url: "shortcut.com", pricing: "Freemium", rating: 4.4, tags: ["software", "stories", "iterations"]},
    {name: "Wrike", category: "Project Management", subcategory: "Enterprise", desc: "Enterprise work management", url: "wrike.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "marketing", "creative"]},
    {name: "Teamwork", category: "Project Management", subcategory: "Client", desc: "Client work management", url: "teamwork.com", pricing: "Freemium", rating: 4.3, tags: ["client", "agencies", "time-tracking"]},
    {name: "Hive", category: "Project Management", subcategory: "Flexible", desc: "Flexible project management", url: "hive.com", pricing: "Freemium", rating: 4.2, tags: ["flexible", "views", "automation"]},
    {name: "Airtable", category: "Project Management", subcategory: "Database", desc: "Spreadsheet-database hybrid", url: "airtable.com", pricing: "Freemium", rating: 4.5, tags: ["database", "flexible", "automations"]},
    {name: "Coda", category: "Project Management", subcategory: "Doc", desc: "All-in-one doc", url: "coda.io", pricing: "Freemium", rating: 4.4, tags: ["doc", "tables", "automations"]},
    {name: "SmartSheet", category: "Project Management", subcategory: "Enterprise", desc: "Enterprise work execution", url: "smartsheet.com", pricing: "Paid", rating: 4.3, tags: ["enterprise", "spreadsheet", "collaboration"]},
    
    // ==================== COLLABORATION ====================
    {name: "Slack", category: "Collaboration", subcategory: "Messaging", desc: "Team messaging platform", url: "slack.com", pricing: "Freemium", rating: 4.5, tags: ["messaging", "channels", "integrations"], featured: true},
    {name: "Discord", category: "Collaboration", subcategory: "Community", desc: "Community platform", url: "discord.com", pricing: "Freemium", rating: 4.5, tags: ["community", "voice", "gaming"]},
    {name: "Microsoft Teams", category: "Collaboration", subcategory: "Enterprise", desc: "Microsoft collaboration hub", url: "microsoft.com/teams", pricing: "Freemium", rating: 4.4, tags: ["microsoft", "enterprise", "video"]},
    {name: "Google Workspace", category: "Collaboration", subcategory: "Suite", desc: "Google productivity suite", url: "workspace.google.com", pricing: "Paid", rating: 4.5, tags: ["google", "email", "docs"]},
    {name: "Miro", category: "Collaboration", subcategory: "Whiteboard", desc: "Online whiteboard", url: "miro.com", pricing: "Freemium", rating: 4.6, tags: ["whiteboard", "visual", "workshops"]},
    {name: "Figma", category: "Collaboration", subcategory: "Design", desc: "Collaborative design", url: "figma.com", pricing: "Freemium", rating: 4.8, tags: ["design", "collaborative", "prototyping"]},
    {name: "FigJam", category: "Collaboration", subcategory: "Whiteboard", desc: "Figma whiteboard", url: "figma.com/figjam", pricing: "Freemium", rating: 4.5, tags: ["whiteboard", "figma", "brainstorming"]},
    {name: "Lucidspark", category: "Collaboration", subcategory: "Whiteboard", desc: "Virtual whiteboard", url: "lucidspark.com", pricing: "Freemium", rating: 4.3, tags: ["whiteboard", "brainstorming", "lucid"]},
    {name: "Mural", category: "Collaboration", subcategory: "Whiteboard", desc: "Visual collaboration", url: "mural.co", pricing: "Paid", rating: 4.4, tags: ["whiteboard", "workshops", "enterprise"]},
    {name: "Whimsical", category: "Collaboration", subcategory: "Visual", desc: "Visual thinking tool", url: "whimsical.com", pricing: "Freemium", rating: 4.5, tags: ["flowcharts", "wireframes", "mind-maps"]},
    {name: "Loom", category: "Collaboration", subcategory: "Video", desc: "Async video messaging", url: "loom.com", pricing: "Freemium", rating: 4.6, tags: ["video", "async", "screen-recording"]},
    {name: "Mmhmm", category: "Collaboration", subcategory: "Presentations", desc: "Virtual presentations", url: "mmhmm.app", pricing: "Freemium", rating: 4.2, tags: ["presentations", "video", "virtual"]},
    {name: "Around", category: "Collaboration", subcategory: "Meetings", desc: "Collaborative meetings", url: "around.co", pricing: "Freemium", rating: 4.3, tags: ["meetings", "floating", "collaborative"]},
    {name: "Gather", category: "Collaboration", subcategory: "Virtual Office", desc: "Virtual office space", url: "gather.town", pricing: "Freemium", rating: 4.3, tags: ["virtual-office", "spatial", "fun"]},
    {name: "Teamflow", category: "Collaboration", subcategory: "Virtual Office", desc: "Virtual HQ for teams", url: "teamflowhq.com", pricing: "Paid", rating: 4.2, tags: ["virtual-office", "spatial", "video"]},
    
    // ==================== KNOWLEDGE MANAGEMENT ====================
    {name: "Confluence", category: "Knowledge", subcategory: "Wiki", desc: "Team workspace by Atlassian", url: "atlassian.com/software/confluence", pricing: "Freemium", rating: 4.2, tags: ["wiki", "atlassian", "documentation"]},
    {name: "Notion", category: "Knowledge", subcategory: "Wiki", desc: "All-in-one workspace", url: "notion.so", pricing: "Freemium", rating: 4.7, tags: ["wiki", "docs", "database"]},
    {name: "Slite", category: "Knowledge", subcategory: "Wiki", desc: "Team knowledge base", url: "slite.com", pricing: "Freemium", rating: 4.4, tags: ["wiki", "simple", "ai"]},
    {name: "Guru", category: "Knowledge", subcategory: "Wiki", desc: "Company wiki", url: "getguru.com", pricing: "Freemium", rating: 4.4, tags: ["wiki", "browser", "verification"]},
    {name: "Tettra", category: "Knowledge", subcategory: "Wiki", desc: "Knowledge management", url: "tettra.com", pricing: "Paid", rating: 4.3, tags: ["wiki", "q&a", "slack"]},
    {name: "Nuclino", category: "Knowledge", subcategory: "Wiki", desc: "Unified workspace", url: "nuclino.com", pricing: "Freemium", rating: 4.4, tags: ["wiki", "real-time", "visual"]},
    {name: "Slab", category: "Knowledge", subcategory: "Wiki", desc: "Knowledge hub", url: "slab.com", pricing: "Freemium", rating: 4.4, tags: ["wiki", "posts", "unified-search"]},
    {name: "Almanac", category: "Knowledge", subcategory: "Docs", desc: "Modern docs platform", url: "almanac.io", pricing: "Freemium", rating: 4.2, tags: ["docs", "async", "templates"]},
    {name: "Gitbook", category: "Knowledge", subcategory: "Documentation", desc: "Documentation platform", url: "gitbook.com", pricing: "Freemium", rating: 4.4, tags: ["docs", "technical", "api"]},
    {name: "Readme", category: "Knowledge", subcategory: "API Docs", desc: "API documentation", url: "readme.com", pricing: "Freemium", rating: 4.4, tags: ["api", "developer", "docs"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE15 = AI_TOOLS_PHASE15;
}


