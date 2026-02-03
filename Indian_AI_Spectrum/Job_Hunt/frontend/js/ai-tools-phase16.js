// AI Tools Database - Phase 16: Customer Support & Chatbots AI
// 200+ Tools for customer support and chatbot development

const AI_TOOLS_PHASE16 = [
    // ==================== HELPDESK & TICKETING ====================
    {name: "Zendesk", category: "Support", subcategory: "Helpdesk", desc: "Customer service platform", url: "zendesk.com", pricing: "Paid", rating: 4.4, tags: ["helpdesk", "ticketing", "enterprise"], featured: true},
    {name: "Freshdesk", category: "Support", subcategory: "Helpdesk", desc: "Customer support software", url: "freshworks.com/freshdesk", pricing: "Freemium", rating: 4.4, tags: ["helpdesk", "ticketing", "affordable"]},
    {name: "Intercom", category: "Support", subcategory: "Messaging", desc: "Customer messaging platform", url: "intercom.com", pricing: "Paid", rating: 4.4, tags: ["messaging", "chatbot", "support"]},
    {name: "Help Scout", category: "Support", subcategory: "Email", desc: "Customer support software", url: "helpscout.com", pricing: "Paid", rating: 4.5, tags: ["email", "docs", "simple"]},
    {name: "Front", category: "Support", subcategory: "Inbox", desc: "Shared inbox for teams", url: "front.com", pricing: "Paid", rating: 4.5, tags: ["inbox", "email", "collaborative"]},
    {name: "Gorgias", category: "Support", subcategory: "E-commerce", desc: "E-commerce helpdesk", url: "gorgias.com", pricing: "Paid", rating: 4.5, tags: ["ecommerce", "shopify", "automation"]},
    {name: "Gladly", category: "Support", subcategory: "Customer-centric", desc: "Customer service platform", url: "gladly.com", pricing: "Paid", rating: 4.4, tags: ["customer-centric", "omnichannel", "modern"]},
    {name: "Kustomer", category: "Support", subcategory: "CRM", desc: "Customer service CRM", url: "kustomer.com", pricing: "Paid", rating: 4.3, tags: ["crm", "timeline", "facebook"]},
    {name: "Zoho Desk", category: "Support", subcategory: "Helpdesk", desc: "Context-aware helpdesk", url: "zoho.com/desk", pricing: "Freemium", rating: 4.3, tags: ["zoho", "helpdesk", "ai"]},
    {name: "Kayako", category: "Support", subcategory: "Helpdesk", desc: "Customer service software", url: "kayako.com", pricing: "Paid", rating: 4.1, tags: ["helpdesk", "unified", "journeys"]},
    {name: "HappyFox", category: "Support", subcategory: "Helpdesk", desc: "Help desk software", url: "happyfox.com", pricing: "Paid", rating: 4.3, tags: ["helpdesk", "ticketing", "automation"]},
    {name: "TeamSupport", category: "Support", subcategory: "B2B", desc: "B2B customer support", url: "teamsupport.com", pricing: "Paid", rating: 4.2, tags: ["b2b", "enterprise", "customer-success"]},
    {name: "ServiceNow", category: "Support", subcategory: "ITSM", desc: "IT service management", url: "servicenow.com", pricing: "Paid", rating: 4.3, tags: ["itsm", "enterprise", "workflow"]},
    {name: "Jira Service Management", category: "Support", subcategory: "ITSM", desc: "IT service management", url: "atlassian.com/software/jira/service-management", pricing: "Freemium", rating: 4.3, tags: ["itsm", "atlassian", "devops"]},
    {name: "Salesforce Service Cloud", category: "Support", subcategory: "Enterprise", desc: "Enterprise service platform", url: "salesforce.com/service-cloud", pricing: "Paid", rating: 4.2, tags: ["enterprise", "salesforce", "ai"]},
    
    // ==================== LIVE CHAT ====================
    {name: "LiveChat", category: "Live Chat", subcategory: "Chat", desc: "Customer service platform", url: "livechat.com", pricing: "Paid", rating: 4.5, tags: ["chat", "ticketing", "chatbot"]},
    {name: "Tawk.to", category: "Live Chat", subcategory: "Free", desc: "Free live chat", url: "tawk.to", pricing: "Free", rating: 4.4, tags: ["free", "chat", "widget"]},
    {name: "Tidio", category: "Live Chat", subcategory: "Chatbot", desc: "Live chat and chatbots", url: "tidio.com", pricing: "Freemium", rating: 4.5, tags: ["chat", "chatbot", "affordable"]},
    {name: "Crisp", category: "Live Chat", subcategory: "Multi-channel", desc: "Customer messaging platform", url: "crisp.chat", pricing: "Freemium", rating: 4.4, tags: ["chat", "multi-channel", "affordable"]},
    {name: "Olark", category: "Live Chat", subcategory: "Simple", desc: "Simple live chat", url: "olark.com", pricing: "Paid", rating: 4.2, tags: ["simple", "chat", "data"]},
    {name: "Chatra", category: "Live Chat", subcategory: "SMB", desc: "Live chat for SMB", url: "chatra.com", pricing: "Freemium", rating: 4.3, tags: ["smb", "simple", "affordable"]},
    {name: "Acquire", category: "Live Chat", subcategory: "Video", desc: "Customer engagement platform", url: "acquire.io", pricing: "Paid", rating: 4.2, tags: ["video", "co-browse", "enterprise"]},
    {name: "Userlike", category: "Live Chat", subcategory: "Unified", desc: "Unified messaging", url: "userlike.com", pricing: "Freemium", rating: 4.3, tags: ["unified", "whatsapp", "european"]},
    {name: "Chaport", category: "Live Chat", subcategory: "Simple", desc: "Modern live chat", url: "chaport.com", pricing: "Freemium", rating: 4.3, tags: ["simple", "mobile", "group-chats"]},
    {name: "JivoChat", category: "Live Chat", subcategory: "Multi-channel", desc: "Omnichannel messaging", url: "jivochat.com", pricing: "Freemium", rating: 4.2, tags: ["omnichannel", "calls", "affordable"]},
    
    // ==================== AI CHATBOTS ====================
    {name: "ChatGPT", category: "AI Chatbot", subcategory: "General", desc: "OpenAI's conversational AI", url: "chat.openai.com", pricing: "Freemium", rating: 4.8, tags: ["gpt", "openai", "conversational"], featured: true},
    {name: "Claude", category: "AI Chatbot", subcategory: "General", desc: "Anthropic's AI assistant", url: "claude.ai", pricing: "Freemium", rating: 4.7, tags: ["anthropic", "safe", "helpful"], featured: true},
    {name: "Gemini", category: "AI Chatbot", subcategory: "Google", desc: "Google's AI assistant", url: "gemini.google.com", pricing: "Freemium", rating: 4.5, tags: ["google", "multimodal", "search"]},
    {name: "Copilot", category: "AI Chatbot", subcategory: "Microsoft", desc: "Microsoft's AI companion", url: "copilot.microsoft.com", pricing: "Freemium", rating: 4.4, tags: ["microsoft", "bing", "integration"]},
    {name: "Perplexity", category: "AI Chatbot", subcategory: "Search", desc: "AI-powered search", url: "perplexity.ai", pricing: "Freemium", rating: 4.6, tags: ["search", "citations", "research"]},
    {name: "Poe", category: "AI Chatbot", subcategory: "Multi-bot", desc: "Access multiple AI bots", url: "poe.com", pricing: "Freemium", rating: 4.4, tags: ["multi-bot", "quora", "variety"]},
    {name: "Character.ai", category: "AI Chatbot", subcategory: "Characters", desc: "Chat with AI characters", url: "character.ai", pricing: "Freemium", rating: 4.5, tags: ["characters", "roleplay", "creative"]},
    {name: "Replika", category: "AI Chatbot", subcategory: "Companion", desc: "AI companion", url: "replika.ai", pricing: "Freemium", rating: 4.1, tags: ["companion", "emotional", "personal"]},
    {name: "Pi", category: "AI Chatbot", subcategory: "Companion", desc: "Personal AI by Inflection", url: "pi.ai", pricing: "Free", rating: 4.3, tags: ["personal", "conversational", "empathetic"]},
    {name: "Jasper Chat", category: "AI Chatbot", subcategory: "Marketing", desc: "AI chat for marketing", url: "jasper.ai/chat", pricing: "Paid", rating: 4.2, tags: ["marketing", "brand", "teams"]},
    {name: "You.com", category: "AI Chatbot", subcategory: "Search", desc: "AI search engine", url: "you.com", pricing: "Freemium", rating: 4.2, tags: ["search", "chat", "privacy"]},
    {name: "Phind", category: "AI Chatbot", subcategory: "Developer", desc: "AI search for developers", url: "phind.com", pricing: "Free", rating: 4.4, tags: ["developer", "coding", "search"]},
    {name: "Khanmigo", category: "AI Chatbot", subcategory: "Education", desc: "Khan Academy AI tutor", url: "khanacademy.org/khan-labs", pricing: "Paid", rating: 4.5, tags: ["education", "tutor", "learning"]},
    {name: "Wix ADI", category: "AI Chatbot", subcategory: "Website", desc: "AI website builder", url: "wix.com/adi", pricing: "Freemium", rating: 4.2, tags: ["website", "builder", "design"]},
    {name: "Hugging Chat", category: "AI Chatbot", subcategory: "Open", desc: "Open source chat", url: "huggingface.co/chat", pricing: "Free", rating: 4.2, tags: ["open-source", "free", "huggingface"]},
    
    // ==================== CHATBOT BUILDERS ====================
    {name: "Botpress", category: "Chatbot Builder", subcategory: "Open Source", desc: "Open source chatbot builder", url: "botpress.com", pricing: "Freemium", rating: 4.4, tags: ["open-source", "nlu", "visual"], featured: true},
    {name: "Dialogflow", category: "Chatbot Builder", subcategory: "Google", desc: "Google's chatbot platform", url: "cloud.google.com/dialogflow", pricing: "Freemium", rating: 4.3, tags: ["google", "nlu", "enterprise"]},
    {name: "Amazon Lex", category: "Chatbot Builder", subcategory: "AWS", desc: "AWS chatbot service", url: "aws.amazon.com/lex", pricing: "Pay-per-use", rating: 4.2, tags: ["aws", "alexa", "enterprise"]},
    {name: "Microsoft Bot Framework", category: "Chatbot Builder", subcategory: "Microsoft", desc: "Microsoft's bot platform", url: "dev.botframework.com", pricing: "Pay-per-use", rating: 4.2, tags: ["microsoft", "azure", "enterprise"]},
    {name: "Rasa", category: "Chatbot Builder", subcategory: "Open Source", desc: "Open source ML chatbot", url: "rasa.com", pricing: "Freemium", rating: 4.3, tags: ["open-source", "ml", "on-premise"]},
    {name: "Landbot", category: "Chatbot Builder", subcategory: "No-Code", desc: "No-code chatbot builder", url: "landbot.io", pricing: "Freemium", rating: 4.4, tags: ["no-code", "visual", "conversational"]},
    {name: "ManyChat", category: "Chatbot Builder", subcategory: "Messenger", desc: "Messenger marketing", url: "manychat.com", pricing: "Freemium", rating: 4.4, tags: ["messenger", "instagram", "marketing"]},
    {name: "Chatfuel", category: "Chatbot Builder", subcategory: "No-Code", desc: "No-code chatbots", url: "chatfuel.com", pricing: "Freemium", rating: 4.2, tags: ["messenger", "no-code", "marketing"]},
    {name: "MobileMonkey", category: "Chatbot Builder", subcategory: "Omnichannel", desc: "Omnichannel chatbot", url: "mobilemonkey.com", pricing: "Freemium", rating: 4.1, tags: ["omnichannel", "marketing", "instagram"]},
    {name: "Drift", category: "Chatbot Builder", subcategory: "Revenue", desc: "Conversational marketing", url: "drift.com", pricing: "Paid", rating: 4.2, tags: ["sales", "marketing", "conversational"]},
    {name: "Ada", category: "Chatbot Builder", subcategory: "Enterprise", desc: "AI customer service", url: "ada.cx", pricing: "Paid", rating: 4.3, tags: ["enterprise", "automation", "ai"]},
    {name: "Kommunicate", category: "Chatbot Builder", subcategory: "Support", desc: "Customer support automation", url: "kommunicate.io", pricing: "Freemium", rating: 4.3, tags: ["support", "hybrid", "affordable"]},
    {name: "Flow XO", category: "Chatbot Builder", subcategory: "Multi-platform", desc: "Multi-platform chatbots", url: "flowxo.com", pricing: "Freemium", rating: 4.1, tags: ["multi-platform", "integration", "visual"]},
    {name: "Botsify", category: "Chatbot Builder", subcategory: "No-Code", desc: "No-code AI chatbots", url: "botsify.com", pricing: "Paid", rating: 4.0, tags: ["no-code", "education", "affordable"]},
    {name: "Tars", category: "Chatbot Builder", subcategory: "Conversational", desc: "Conversational landing pages", url: "hellotars.com", pricing: "Paid", rating: 4.2, tags: ["landing-pages", "conversational", "lead-gen"]},
    
    // ==================== VOICE ASSISTANTS ====================
    {name: "Amazon Alexa", category: "Voice", subcategory: "Assistant", desc: "Amazon's voice assistant", url: "developer.amazon.com/alexa", pricing: "Free", rating: 4.3, tags: ["smart-home", "skills", "amazon"]},
    {name: "Google Assistant", category: "Voice", subcategory: "Assistant", desc: "Google's voice assistant", url: "assistant.google.com", pricing: "Free", rating: 4.4, tags: ["smart-home", "google", "actions"]},
    {name: "Siri", category: "Voice", subcategory: "Assistant", desc: "Apple's voice assistant", url: "apple.com/siri", pricing: "Free", rating: 4.2, tags: ["apple", "ios", "shortcuts"]},
    {name: "Cortana", category: "Voice", subcategory: "Assistant", desc: "Microsoft's assistant", url: "microsoft.com/cortana", pricing: "Free", rating: 3.8, tags: ["microsoft", "productivity", "enterprise"]},
    {name: "Voiceflow", category: "Voice", subcategory: "Builder", desc: "Voice app design platform", url: "voiceflow.com", pricing: "Freemium", rating: 4.4, tags: ["design", "alexa", "google"]},
    {name: "Jovo", category: "Voice", subcategory: "Framework", desc: "Voice app framework", url: "jovo.tech", pricing: "Free", rating: 4.2, tags: ["framework", "cross-platform", "open-source"]},
    {name: "Speechly", category: "Voice", subcategory: "API", desc: "Voice input API", url: "speechly.com", pricing: "Freemium", rating: 4.2, tags: ["api", "real-time", "voice-ui"]},
    {name: "Picovoice", category: "Voice", subcategory: "On-device", desc: "On-device voice AI", url: "picovoice.ai", pricing: "Freemium", rating: 4.3, tags: ["on-device", "privacy", "wake-word"]},
    {name: "AssemblyAI", category: "Voice", subcategory: "Transcription", desc: "AI speech-to-text", url: "assemblyai.com", pricing: "Freemium", rating: 4.5, tags: ["transcription", "api", "accurate"]},
    {name: "Deepgram", category: "Voice", subcategory: "Transcription", desc: "Speech recognition API", url: "deepgram.com", pricing: "Freemium", rating: 4.5, tags: ["transcription", "real-time", "enterprise"]},
    
    // ==================== KNOWLEDGE BASE ====================
    {name: "Zendesk Guide", category: "Knowledge Base", subcategory: "Help Center", desc: "Self-service help center", url: "zendesk.com/service/guide", pricing: "Paid", rating: 4.3, tags: ["help-center", "zendesk", "ai"]},
    {name: "Helpjuice", category: "Knowledge Base", subcategory: "Internal", desc: "Knowledge base software", url: "helpjuice.com", pricing: "Paid", rating: 4.4, tags: ["internal", "analytics", "customization"]},
    {name: "Document360", category: "Knowledge Base", subcategory: "Technical", desc: "Knowledge base for SaaS", url: "document360.com", pricing: "Paid", rating: 4.5, tags: ["saas", "technical", "ai"]},
    {name: "HelpDocs", category: "Knowledge Base", subcategory: "Simple", desc: "Simple knowledge base", url: "helpdocs.io", pricing: "Paid", rating: 4.4, tags: ["simple", "beautiful", "fast"]},
    {name: "Intercom Articles", category: "Knowledge Base", subcategory: "Integrated", desc: "Integrated help center", url: "intercom.com/articles", pricing: "Paid", rating: 4.3, tags: ["intercom", "integrated", "suggestions"]},
    {name: "Notion", category: "Knowledge Base", subcategory: "Wiki", desc: "Team wiki and docs", url: "notion.so", pricing: "Freemium", rating: 4.7, tags: ["wiki", "flexible", "popular"]},
    {name: "Confluence", category: "Knowledge Base", subcategory: "Enterprise", desc: "Team workspace", url: "atlassian.com/software/confluence", pricing: "Freemium", rating: 4.2, tags: ["atlassian", "enterprise", "wiki"]},
    {name: "Slite", category: "Knowledge Base", subcategory: "Team", desc: "Team knowledge base", url: "slite.com", pricing: "Freemium", rating: 4.4, tags: ["team", "ai", "search"]},
    {name: "Guru", category: "Knowledge Base", subcategory: "Browser", desc: "Knowledge in browser", url: "getguru.com", pricing: "Freemium", rating: 4.4, tags: ["browser", "verification", "slack"]},
    {name: "Stonly", category: "Knowledge Base", subcategory: "Interactive", desc: "Interactive guides", url: "stonly.com", pricing: "Paid", rating: 4.3, tags: ["interactive", "guides", "support"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE16 = AI_TOOLS_PHASE16;
}


