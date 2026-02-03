// AI Tools Mega Database - Part 2: Business & Productivity Categories

const AI_TOOLS_DATABASE_2 = {
    // ==================== PRODUCTIVITY ====================
    productivity: [
        {name: "Otter.ai", category: "Productivity", sub: "Transcription", desc: "AI meeting transcription", url: "https://otter.ai", pricing: "Freemium", rating: 4.6, users: "10M+", tags: ["meetings"], featured: true, icon: "🦦"},
        {name: "Fireflies.ai", category: "Productivity", sub: "Meetings", desc: "AI meeting assistant", url: "https://fireflies.ai", pricing: "Freemium", rating: 4.5, users: "300K+", tags: ["meetings"], featured: true, icon: "🔥"},
        {name: "Motion", category: "Productivity", sub: "Calendar", desc: "AI calendar scheduling", url: "https://usemotion.com", pricing: "Paid", rating: 4.5, users: "100K+", tags: ["calendar"], featured: false, icon: "📅"},
        {name: "Taskade", category: "Productivity", sub: "Tasks", desc: "AI workspace for teams", url: "https://taskade.com", pricing: "Freemium", rating: 4.4, users: "500K+", tags: ["tasks"], featured: false, icon: "✅"},
        {name: "Reclaim.ai", category: "Productivity", sub: "Calendar", desc: "AI calendar management", url: "https://reclaim.ai", pricing: "Freemium", rating: 4.4, users: "200K+", tags: ["calendar"], featured: false, icon: "🗓️"},
        {name: "tl;dv", category: "Productivity", sub: "Meetings", desc: "AI meeting recorder", url: "https://tldv.io", pricing: "Freemium", rating: 4.4, users: "200K+", tags: ["recording"], featured: false, icon: "📹"},
        {name: "Mem", category: "Productivity", sub: "Notes", desc: "AI-powered note taking", url: "https://mem.ai", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["notes"], featured: false, icon: "📝"},
        {name: "Reflect", category: "Productivity", sub: "Notes", desc: "AI note-taking with backlinks", url: "https://reflect.app", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["notes", "pkm"], featured: false, icon: "🪞"},
        {name: "Fathom", category: "Productivity", sub: "Meetings", desc: "Free AI meeting notes", url: "https://fathom.video", pricing: "Free", rating: 4.5, users: "500K+", tags: ["free", "meetings"], featured: false, icon: "📊"},
        {name: "Grain", category: "Productivity", sub: "Meetings", desc: "AI video highlights", url: "https://grain.com", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["highlights"], featured: false, icon: "🌾"},
        {name: "Krisp", category: "Productivity", sub: "Audio", desc: "AI noise cancellation", url: "https://krisp.ai", pricing: "Freemium", rating: 4.6, users: "3M+", tags: ["noise"], featured: false, icon: "🔇"},
        {name: "Clockwise", category: "Productivity", sub: "Calendar", desc: "AI calendar optimization", url: "https://clockwise.com", pricing: "Freemium", rating: 4.3, users: "200K+", tags: ["calendar"], featured: false, icon: "⏰"},
        {name: "Fellow", category: "Productivity", sub: "Meetings", desc: "AI meeting management", url: "https://fellow.app", pricing: "Freemium", rating: 4.4, users: "100K+", tags: ["meetings"], featured: false, icon: "👥"},
        {name: "Supernormal", category: "Productivity", sub: "Meetings", desc: "AI meeting notes", url: "https://supernormal.com", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["notes"], featured: false, icon: "✨"},
        {name: "Sembly AI", category: "Productivity", sub: "Meetings", desc: "AI meeting assistant", url: "https://sembly.ai", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["meetings"], featured: false, icon: "🤖"},
        {name: "Read AI", category: "Productivity", sub: "Meetings", desc: "Meeting analytics AI", url: "https://read.ai", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["analytics"], featured: false, icon: "📖"},
        {name: "Hive", category: "Productivity", sub: "Project Mgmt", desc: "AI project management", url: "https://hive.com", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["projects"], featured: false, icon: "🐝"},
        {name: "ClickUp AI", category: "Productivity", sub: "Project Mgmt", desc: "AI in ClickUp workspace", url: "https://clickup.com/ai", pricing: "Paid", rating: 4.4, users: "500K+", tags: ["projects"], featured: false, icon: "📋"},
        {name: "Monday AI", category: "Productivity", sub: "Project Mgmt", desc: "AI in Monday.com", url: "https://monday.com/lp/ai", pricing: "Paid", rating: 4.3, users: "200K+", tags: ["projects"], featured: false, icon: "📊"},
        {name: "Asana Intelligence", category: "Productivity", sub: "Project Mgmt", desc: "AI in Asana", url: "https://asana.com/product/ai", pricing: "Paid", rating: 4.3, users: "200K+", tags: ["projects"], featured: false, icon: "🎯"},
    ],

    // ==================== DESIGN ====================
    design: [
        {name: "Figma AI", category: "Design", sub: "UI/UX", desc: "AI features in Figma", url: "https://figma.com/ai", pricing: "Freemium", rating: 4.5, users: "4M+", tags: ["ui", "design"], featured: true, icon: "🎨"},
        {name: "Framer AI", category: "Design", sub: "Web", desc: "AI website builder", url: "https://framer.com/ai", pricing: "Freemium", rating: 4.6, users: "1M+", tags: ["websites"], featured: true, icon: "🌐"},
        {name: "Remove.bg", category: "Design", sub: "Background", desc: "AI background remover", url: "https://remove.bg", pricing: "Freemium", rating: 4.7, users: "30M+", tags: ["background"], featured: true, icon: "🖼️"},
        {name: "Photoroom", category: "Design", sub: "Product", desc: "AI product photos", url: "https://photoroom.com", pricing: "Freemium", rating: 4.6, users: "10M+", tags: ["product"], featured: false, icon: "📸"},
        {name: "Looka", category: "Design", sub: "Logo", desc: "AI logo maker", url: "https://looka.com", pricing: "Paid", rating: 4.4, users: "1M+", tags: ["logos"], featured: false, icon: "🏷️"},
        {name: "Brandmark", category: "Design", sub: "Logo", desc: "AI logo generator", url: "https://brandmark.io", pricing: "Paid", rating: 4.3, users: "500K+", tags: ["logos"], featured: false, icon: "✨"},
        {name: "Designs.ai", category: "Design", sub: "Suite", desc: "AI design toolkit", url: "https://designs.ai", pricing: "Paid", rating: 4.2, users: "500K+", tags: ["suite"], featured: false, icon: "🎨"},
        {name: "Uizard", category: "Design", sub: "Prototyping", desc: "AI UI design tool", url: "https://uizard.io", pricing: "Freemium", rating: 4.3, users: "500K+", tags: ["prototyping"], featured: false, icon: "📱"},
        {name: "Khroma", category: "Design", sub: "Colors", desc: "AI color palette", url: "https://khroma.co", pricing: "Free", rating: 4.2, users: "500K+", tags: ["colors"], featured: false, icon: "🎨"},
        {name: "Cleanup.pictures", category: "Design", sub: "Editing", desc: "Remove objects from photos", url: "https://cleanup.pictures", pricing: "Freemium", rating: 4.5, users: "5M+", tags: ["editing"], featured: false, icon: "🧹"},
        {name: "Let's Enhance", category: "Design", sub: "Upscaling", desc: "AI image upscaling", url: "https://letsenhance.io", pricing: "Freemium", rating: 4.4, users: "1M+", tags: ["upscaling"], featured: false, icon: "📈"},
        {name: "Vectorizer.ai", category: "Design", sub: "Vectors", desc: "AI image to vector", url: "https://vectorizer.ai", pricing: "Freemium", rating: 4.4, users: "500K+", tags: ["vectors"], featured: false, icon: "📐"},
        {name: "Clipdrop", category: "Design", sub: "Suite", desc: "AI image editing suite", url: "https://clipdrop.co", pricing: "Freemium", rating: 4.5, users: "2M+", tags: ["editing"], featured: false, icon: "✂️"},
        {name: "Picsart AI", category: "Design", sub: "Editing", desc: "AI photo editing", url: "https://picsart.com", pricing: "Freemium", rating: 4.4, users: "50M+", tags: ["editing", "mobile"], featured: false, icon: "🖼️"},
        {name: "Pixlr AI", category: "Design", sub: "Editing", desc: "AI photo editor", url: "https://pixlr.com", pricing: "Freemium", rating: 4.3, users: "10M+", tags: ["editing"], featured: false, icon: "🎨"},
        {name: "Fotor AI", category: "Design", sub: "Editing", desc: "AI image editing", url: "https://fotor.com", pricing: "Freemium", rating: 4.3, users: "5M+", tags: ["editing"], featured: false, icon: "📷"},
        {name: "Hotpot.ai", category: "Design", sub: "Tools", desc: "AI design tools", url: "https://hotpot.ai", pricing: "Freemium", rating: 4.2, users: "2M+", tags: ["tools"], featured: false, icon: "🍲"},
        {name: "Autodesigner", category: "Design", sub: "Presentations", desc: "AI presentation design", url: "https://autodesigner.ai", pricing: "Paid", rating: 4.1, users: "50K+", tags: ["presentations"], featured: false, icon: "📊"},
        {name: "Visme AI", category: "Design", sub: "Graphics", desc: "AI visual content", url: "https://visme.co", pricing: "Freemium", rating: 4.3, users: "500K+", tags: ["graphics"], featured: false, icon: "📈"},
        {name: "Gamma", category: "Design", sub: "Presentations", desc: "AI presentations", url: "https://gamma.app", pricing: "Freemium", rating: 4.5, users: "1M+", tags: ["presentations"], featured: true, icon: "📊"},
    ],

    // ==================== MARKETING & SEO ====================
    marketing: [
        {name: "Surfer SEO", category: "Marketing", sub: "SEO", desc: "AI SEO optimization", url: "https://surferseo.com", pricing: "Paid", rating: 4.6, users: "100K+", tags: ["seo"], featured: true, icon: "🏄"},
        {name: "Clearscope", category: "Marketing", sub: "SEO", desc: "AI content optimization", url: "https://clearscope.io", pricing: "Paid", rating: 4.5, users: "50K+", tags: ["seo"], featured: false, icon: "🎯"},
        {name: "MarketMuse", category: "Marketing", sub: "Content", desc: "AI content strategy", url: "https://marketmuse.com", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["content"], featured: false, icon: "📚"},
        {name: "Semrush AI", category: "Marketing", sub: "SEO Suite", desc: "AI marketing toolkit", url: "https://semrush.com", pricing: "Paid", rating: 4.5, users: "200K+", tags: ["seo", "suite"], featured: true, icon: "📊"},
        {name: "Ahrefs AI", category: "Marketing", sub: "SEO", desc: "AI SEO tools", url: "https://ahrefs.com", pricing: "Paid", rating: 4.6, users: "100K+", tags: ["seo"], featured: false, icon: "🔗"},
        {name: "Frase", category: "Marketing", sub: "Content", desc: "AI content creation", url: "https://frase.io", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["content"], featured: false, icon: "📝"},
        {name: "NeuronWriter", category: "Marketing", sub: "SEO", desc: "AI SEO writing", url: "https://neuronwriter.com", pricing: "Paid", rating: 4.3, users: "30K+", tags: ["seo", "writing"], featured: false, icon: "🧠"},
        {name: "Scalenut", category: "Marketing", sub: "Content", desc: "AI content marketing", url: "https://scalenut.com", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["content"], featured: false, icon: "🥜"},
        {name: "SE Ranking AI", category: "Marketing", sub: "SEO", desc: "AI SEO platform", url: "https://seranking.com", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["seo"], featured: false, icon: "📈"},
        {name: "Lately", category: "Marketing", sub: "Social", desc: "AI social media", url: "https://lately.ai", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["social"], featured: false, icon: "📱"},
        {name: "Hootsuite AI", category: "Marketing", sub: "Social", desc: "AI social management", url: "https://hootsuite.com", pricing: "Paid", rating: 4.4, users: "200K+", tags: ["social"], featured: false, icon: "🦉"},
        {name: "Buffer AI", category: "Marketing", sub: "Social", desc: "AI social scheduling", url: "https://buffer.com", pricing: "Freemium", rating: 4.3, users: "500K+", tags: ["social"], featured: false, icon: "📊"},
        {name: "Sprout Social AI", category: "Marketing", sub: "Social", desc: "AI social analytics", url: "https://sproutsocial.com", pricing: "Paid", rating: 4.4, users: "100K+", tags: ["social"], featured: false, icon: "🌱"},
        {name: "Phrasee", category: "Marketing", sub: "Email", desc: "AI email copy", url: "https://phrasee.co", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["email"], featured: false, icon: "✉️"},
        {name: "Seventh Sense", category: "Marketing", sub: "Email", desc: "AI email timing", url: "https://theseventhsense.com", pricing: "Paid", rating: 4.2, users: "20K+", tags: ["email"], featured: false, icon: "⏰"},
        {name: "Albert AI", category: "Marketing", sub: "Advertising", desc: "AI ad optimization", url: "https://albert.ai", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["ads"], featured: false, icon: "🤖"},
        {name: "Adcreative.ai", category: "Marketing", sub: "Ads", desc: "AI ad creative", url: "https://adcreative.ai", pricing: "Paid", rating: 4.4, users: "100K+", tags: ["ads"], featured: false, icon: "🎨"},
        {name: "Persado", category: "Marketing", sub: "Copy", desc: "AI marketing language", url: "https://persado.com", pricing: "Enterprise", rating: 4.3, users: "1K+", tags: ["enterprise"], featured: false, icon: "💬"},
        {name: "Mutiny", category: "Marketing", sub: "Personalization", desc: "AI website personalization", url: "https://mutinyhq.com", pricing: "Paid", rating: 4.4, users: "10K+", tags: ["personalization"], featured: false, icon: "🎯"},
        {name: "PathFactory", category: "Marketing", sub: "Content", desc: "AI content intelligence", url: "https://pathfactory.com", pricing: "Paid", rating: 4.2, users: "10K+", tags: ["content"], featured: false, icon: "🛤️"},
    ],

    // ==================== SALES ====================
    sales: [
        {name: "Gong", category: "Sales", sub: "Intelligence", desc: "AI sales call analysis", url: "https://gong.io", pricing: "Paid", rating: 4.7, users: "4K+", tags: ["calls"], featured: true, icon: "🔔"},
        {name: "Chorus.ai", category: "Sales", sub: "Intelligence", desc: "Conversation intelligence", url: "https://chorus.ai", pricing: "Paid", rating: 4.5, users: "3K+", tags: ["calls"], featured: false, icon: "🎤"},
        {name: "Apollo.io", category: "Sales", sub: "Prospecting", desc: "AI B2B prospecting", url: "https://apollo.io", pricing: "Freemium", rating: 4.5, users: "500K+", tags: ["prospecting"], featured: true, icon: "🚀"},
        {name: "Clari", category: "Sales", sub: "Revenue", desc: "AI revenue intelligence", url: "https://clari.com", pricing: "Paid", rating: 4.4, users: "5K+", tags: ["revenue"], featured: false, icon: "📊"},
        {name: "Outreach", category: "Sales", sub: "Engagement", desc: "AI sales engagement", url: "https://outreach.io", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["engagement"], featured: false, icon: "📤"},
        {name: "Salesloft", category: "Sales", sub: "Engagement", desc: "AI sales platform", url: "https://salesloft.com", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["platform"], featured: false, icon: "🎯"},
        {name: "ZoomInfo", category: "Sales", sub: "Data", desc: "AI B2B data", url: "https://zoominfo.com", pricing: "Paid", rating: 4.4, users: "100K+", tags: ["data"], featured: false, icon: "📊"},
        {name: "Lusha", category: "Sales", sub: "Data", desc: "AI contact data", url: "https://lusha.com", pricing: "Freemium", rating: 4.3, users: "200K+", tags: ["data"], featured: false, icon: "📇"},
        {name: "Seamless.AI", category: "Sales", sub: "Data", desc: "AI lead data", url: "https://seamless.ai", pricing: "Freemium", rating: 4.2, users: "100K+", tags: ["leads"], featured: false, icon: "🎯"},
        {name: "Clearbit", category: "Sales", sub: "Enrichment", desc: "AI data enrichment", url: "https://clearbit.com", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["enrichment"], featured: false, icon: "✨"},
        {name: "People.ai", category: "Sales", sub: "Revenue", desc: "AI revenue intelligence", url: "https://people.ai", pricing: "Paid", rating: 4.3, users: "5K+", tags: ["revenue"], featured: false, icon: "👥"},
        {name: "Drift", category: "Sales", sub: "Chat", desc: "AI sales chat", url: "https://drift.com", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["chat"], featured: false, icon: "💬"},
        {name: "Qualified", category: "Sales", sub: "Chat", desc: "AI pipeline generation", url: "https://qualified.com", pricing: "Paid", rating: 4.4, users: "10K+", tags: ["chat"], featured: false, icon: "🎯"},
        {name: "6sense", category: "Sales", sub: "ABM", desc: "AI account-based marketing", url: "https://6sense.com", pricing: "Paid", rating: 4.4, users: "5K+", tags: ["abm"], featured: false, icon: "6️⃣"},
        {name: "Demandbase", category: "Sales", sub: "ABM", desc: "AI B2B go-to-market", url: "https://demandbase.com", pricing: "Paid", rating: 4.3, users: "5K+", tags: ["abm"], featured: false, icon: "📊"},
        {name: "Cognism", category: "Sales", sub: "Data", desc: "AI sales intelligence", url: "https://cognism.com", pricing: "Paid", rating: 4.3, users: "30K+", tags: ["data"], featured: false, icon: "🧠"},
        {name: "LeadIQ", category: "Sales", sub: "Prospecting", desc: "AI prospecting", url: "https://leadiq.com", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["prospecting"], featured: false, icon: "🎯"},
        {name: "Lavender", category: "Sales", sub: "Email", desc: "AI email coaching", url: "https://lavender.ai", pricing: "Freemium", rating: 4.4, users: "50K+", tags: ["email"], featured: false, icon: "💜"},
        {name: "Regie.ai", category: "Sales", sub: "Content", desc: "AI sales content", url: "https://regie.ai", pricing: "Paid", rating: 4.2, users: "10K+", tags: ["content"], featured: false, icon: "📝"},
        {name: "Crystal", category: "Sales", sub: "Personality", desc: "AI personality insights", url: "https://crystalknows.com", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["personality"], featured: false, icon: "💎"},
    ],

    // ==================== CUSTOMER SERVICE ====================
    customerService: [
        {name: "Intercom Fin", category: "Support", sub: "Chatbot", desc: "AI customer service bot", url: "https://intercom.com/fin", pricing: "Paid", rating: 4.5, users: "25K+", tags: ["chatbot"], featured: true, icon: "💬"},
        {name: "Zendesk AI", category: "Support", sub: "Platform", desc: "AI support platform", url: "https://zendesk.com", pricing: "Paid", rating: 4.4, users: "100K+", tags: ["platform"], featured: true, icon: "💚"},
        {name: "Freshdesk Freddy", category: "Support", sub: "Chatbot", desc: "AI support assistant", url: "https://freshworks.com/freddy-ai", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["chatbot"], featured: false, icon: "🤖"},
        {name: "Ada", category: "Support", sub: "Automation", desc: "AI support automation", url: "https://ada.cx", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["automation"], featured: false, icon: "🤖"},
        {name: "Tidio", category: "Support", sub: "Chat", desc: "AI live chat", url: "https://tidio.com", pricing: "Freemium", rating: 4.5, users: "300K+", tags: ["chat"], featured: false, icon: "🤝"},
        {name: "Kommunicate", category: "Support", sub: "Chatbot", desc: "AI chatbot builder", url: "https://kommunicate.io", pricing: "Freemium", rating: 4.3, users: "50K+", tags: ["chatbot"], featured: false, icon: "💬"},
        {name: "Forethought", category: "Support", sub: "AI Agent", desc: "AI support agent", url: "https://forethought.ai", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["agent"], featured: false, icon: "🧠"},
        {name: "Ultimate.ai", category: "Support", sub: "Automation", desc: "AI CS automation", url: "https://ultimate.ai", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["automation"], featured: false, icon: "🎯"},
        {name: "Kustomer", category: "Support", sub: "CRM", desc: "AI customer service CRM", url: "https://kustomer.com", pricing: "Paid", rating: 4.3, users: "20K+", tags: ["crm"], featured: false, icon: "👤"},
        {name: "Dixa", category: "Support", sub: "Platform", desc: "AI CS platform", url: "https://dixa.com", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["platform"], featured: false, icon: "📞"},
        {name: "Helpshift", category: "Support", sub: "Mobile", desc: "AI mobile support", url: "https://helpshift.com", pricing: "Paid", rating: 4.2, users: "10K+", tags: ["mobile"], featured: false, icon: "📱"},
        {name: "Capacity", category: "Support", sub: "Knowledge", desc: "AI knowledge management", url: "https://capacity.com", pricing: "Paid", rating: 4.2, users: "5K+", tags: ["knowledge"], featured: false, icon: "📚"},
        {name: "Thankful", category: "Support", sub: "Automation", desc: "AI ticket automation", url: "https://thankful.ai", pricing: "Paid", rating: 4.2, users: "5K+", tags: ["automation"], featured: false, icon: "🙏"},
        {name: "Cognigy", category: "Support", sub: "Conversational", desc: "AI conversational platform", url: "https://cognigy.com", pricing: "Paid", rating: 4.3, users: "5K+", tags: ["conversational"], featured: false, icon: "🗣️"},
        {name: "Boost.ai", category: "Support", sub: "Virtual Agent", desc: "AI virtual agents", url: "https://boost.ai", pricing: "Paid", rating: 4.3, users: "5K+", tags: ["virtual-agent"], featured: false, icon: "🚀"},
        {name: "Haptik", category: "Support", sub: "Chatbot", desc: "Conversational AI", url: "https://haptik.ai", pricing: "Paid", rating: 4.2, users: "10K+", tags: ["chatbot"], featured: false, icon: "💬"},
        {name: "Yellow.ai", category: "Support", sub: "Enterprise", desc: "Enterprise AI automation", url: "https://yellow.ai", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["enterprise"], featured: false, icon: "💛"},
        {name: "LivePerson", category: "Support", sub: "Messaging", desc: "AI messaging platform", url: "https://liveperson.com", pricing: "Paid", rating: 4.2, users: "20K+", tags: ["messaging"], featured: false, icon: "💬"},
        {name: "Sprinklr AI", category: "Support", sub: "CX", desc: "AI customer experience", url: "https://sprinklr.com", pricing: "Paid", rating: 4.3, users: "10K+", tags: ["cx"], featured: false, icon: "💧"},
        {name: "Netomi", category: "Support", sub: "Resolution", desc: "AI ticket resolution", url: "https://netomi.com", pricing: "Paid", rating: 4.2, users: "5K+", tags: ["resolution"], featured: false, icon: "🎯"},
    ]
};

// Merge with main database
if (typeof window !== 'undefined') {
    window.AI_TOOLS_DATABASE_2 = AI_TOOLS_DATABASE_2;
}


