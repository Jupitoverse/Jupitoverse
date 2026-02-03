// AI Tools Mega Database - Part 1: Core Categories
// Total: 500+ AI Tools across 30+ categories

const AI_TOOLS_DATABASE = {
    // ==================== CHATBOTS & ASSISTANTS ====================
    chatbots: [
        {name: "ChatGPT", category: "Chatbot", sub: "General", desc: "OpenAI's flagship AI chatbot for conversations, writing, coding", url: "https://chat.openai.com", pricing: "Freemium", rating: 4.9, users: "200M+", tags: ["chatbot", "writing", "coding"], featured: true, icon: "💬"},
        {name: "Claude", category: "Chatbot", sub: "General", desc: "Anthropic's helpful, harmless, honest AI assistant", url: "https://claude.ai", pricing: "Freemium", rating: 4.8, users: "50M+", tags: ["chatbot", "writing", "analysis"], featured: true, icon: "🤖"},
        {name: "Gemini", category: "Chatbot", sub: "Multimodal", desc: "Google's multimodal AI for text, images, and code", url: "https://gemini.google.com", pricing: "Freemium", rating: 4.7, users: "100M+", tags: ["multimodal", "google"], featured: true, icon: "✨"},
        {name: "Microsoft Copilot", category: "Chatbot", sub: "Assistant", desc: "AI assistant in Windows, Edge, and Office", url: "https://copilot.microsoft.com", pricing: "Freemium", rating: 4.5, users: "50M+", tags: ["microsoft", "office"], featured: true, icon: "🪟"},
        {name: "Perplexity AI", category: "Search", sub: "AI Search", desc: "AI search engine with cited sources", url: "https://perplexity.ai", pricing: "Freemium", rating: 4.8, users: "30M+", tags: ["search", "research"], featured: true, icon: "🔍"},
        {name: "You.com", category: "Search", sub: "AI Search", desc: "AI search with chat and app integration", url: "https://you.com", pricing: "Freemium", rating: 4.4, users: "5M+", tags: ["search", "apps"], featured: false, icon: "🔎"},
        {name: "Phind", category: "Search", sub: "Developer", desc: "AI search engine for developers", url: "https://phind.com", pricing: "Free", rating: 4.5, users: "2M+", tags: ["coding", "search"], featured: false, icon: "👨‍💻"},
        {name: "Kagi", category: "Search", sub: "Premium", desc: "Premium ad-free search with AI", url: "https://kagi.com", pricing: "Paid", rating: 4.6, users: "500K+", tags: ["search", "privacy"], featured: false, icon: "🔐"},
        {name: "Character.AI", category: "Chatbot", sub: "Characters", desc: "Chat with AI characters and personalities", url: "https://character.ai", pricing: "Freemium", rating: 4.5, users: "20M+", tags: ["characters", "roleplay"], featured: false, icon: "🎭"},
        {name: "Pi", category: "Chatbot", sub: "Personal", desc: "Personal AI by Inflection - empathetic conversations", url: "https://pi.ai", pricing: "Free", rating: 4.4, users: "5M+", tags: ["personal", "empathy"], featured: false, icon: "💜"},
        {name: "Poe", category: "Chatbot", sub: "Multi-model", desc: "Access multiple AI models in one place", url: "https://poe.com", pricing: "Freemium", rating: 4.5, users: "10M+", tags: ["multi-model", "quora"], featured: false, icon: "🎯"},
        {name: "HuggingChat", category: "Chatbot", sub: "Open Source", desc: "Open source AI chat by Hugging Face", url: "https://huggingface.co/chat", pricing: "Free", rating: 4.3, users: "2M+", tags: ["open-source", "free"], featured: false, icon: "🤗"},
        {name: "Llama 2 Chat", category: "Chatbot", sub: "Open Source", desc: "Meta's open source chat model", url: "https://llama.meta.com", pricing: "Free", rating: 4.4, users: "5M+", tags: ["open-source", "meta"], featured: false, icon: "🦙"},
        {name: "Mistral Chat", category: "Chatbot", sub: "Open Source", desc: "Mistral AI's powerful chat assistant", url: "https://chat.mistral.ai", pricing: "Freemium", rating: 4.5, users: "2M+", tags: ["open-source", "efficient"], featured: false, icon: "🌪️"},
    ],

    // ==================== WRITING & CONTENT ====================
    writing: [
        {name: "Jasper", category: "Writing", sub: "Marketing", desc: "AI marketing copy and content creation", url: "https://jasper.ai", pricing: "Paid", rating: 4.6, users: "100K+", tags: ["marketing", "copy"], featured: true, icon: "✍️"},
        {name: "Copy.ai", category: "Writing", sub: "Copywriting", desc: "AI copywriting for social, blogs, sales", url: "https://copy.ai", pricing: "Freemium", rating: 4.5, users: "200K+", tags: ["copywriting"], featured: false, icon: "📝"},
        {name: "Grammarly", category: "Writing", sub: "Grammar", desc: "AI writing assistant for grammar and clarity", url: "https://grammarly.com", pricing: "Freemium", rating: 4.7, users: "30M+", tags: ["grammar"], featured: true, icon: "📖"},
        {name: "Notion AI", category: "Writing", sub: "Productivity", desc: "AI in Notion for writing and brainstorming", url: "https://notion.so/ai", pricing: "Paid", rating: 4.6, users: "10M+", tags: ["notes", "productivity"], featured: true, icon: "📓"},
        {name: "QuillBot", category: "Writing", sub: "Paraphrasing", desc: "AI paraphrasing and summarizing", url: "https://quillbot.com", pricing: "Freemium", rating: 4.5, users: "20M+", tags: ["paraphrasing"], featured: false, icon: "🪶"},
        {name: "Writesonic", category: "Writing", sub: "Content", desc: "AI writer for articles and blogs", url: "https://writesonic.com", pricing: "Freemium", rating: 4.4, users: "150K+", tags: ["articles", "seo"], featured: false, icon: "📰"},
        {name: "Rytr", category: "Writing", sub: "Content", desc: "AI writing in 30+ languages", url: "https://rytr.me", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["multilingual"], featured: false, icon: "🌐"},
        {name: "Wordtune", category: "Writing", sub: "Rewriting", desc: "AI-powered rewriting and editing", url: "https://wordtune.com", pricing: "Freemium", rating: 4.4, users: "5M+", tags: ["rewriting"], featured: false, icon: "🎵"},
        {name: "Sudowrite", category: "Writing", sub: "Fiction", desc: "AI writing partner for fiction", url: "https://sudowrite.com", pricing: "Paid", rating: 4.5, users: "100K+", tags: ["fiction", "creative"], featured: false, icon: "📚"},
        {name: "NovelAI", category: "Writing", sub: "Stories", desc: "AI-assisted storytelling", url: "https://novelai.net", pricing: "Paid", rating: 4.4, users: "500K+", tags: ["stories", "fiction"], featured: false, icon: "📖"},
        {name: "Anyword", category: "Writing", sub: "Marketing", desc: "AI copywriting with performance prediction", url: "https://anyword.com", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["marketing", "analytics"], featured: false, icon: "📊"},
        {name: "Copysmith", category: "Writing", sub: "eCommerce", desc: "AI content for eCommerce", url: "https://copysmith.ai", pricing: "Paid", rating: 4.3, users: "30K+", tags: ["ecommerce", "product"], featured: false, icon: "🛒"},
        {name: "Peppertype", category: "Writing", sub: "Content", desc: "AI content generation platform", url: "https://peppertype.ai", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["content"], featured: false, icon: "🌶️"},
        {name: "Simplified", category: "Writing", sub: "All-in-one", desc: "AI writing, design, video in one", url: "https://simplified.com", pricing: "Freemium", rating: 4.3, users: "200K+", tags: ["design", "video"], featured: false, icon: "✨"},
        {name: "Ink", category: "Writing", sub: "SEO", desc: "AI writing with SEO optimization", url: "https://inkforall.com", pricing: "Freemium", rating: 4.2, users: "100K+", tags: ["seo", "optimization"], featured: false, icon: "🖋️"},
        {name: "Copymatic", category: "Writing", sub: "Content", desc: "AI content and copy generator", url: "https://copymatic.ai", pricing: "Paid", rating: 4.1, users: "50K+", tags: ["content", "copy"], featured: false, icon: "📄"},
        {name: "Hyperwrite", category: "Writing", sub: "Assistant", desc: "Personal AI writing assistant", url: "https://hyperwriteai.com", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["assistant", "personal"], featured: false, icon: "⚡"},
        {name: "Lex", category: "Writing", sub: "Documents", desc: "AI-powered word processor", url: "https://lex.page", pricing: "Freemium", rating: 4.4, users: "200K+", tags: ["documents", "writing"], featured: false, icon: "📄"},
        {name: "Creaitor", category: "Writing", sub: "Marketing", desc: "AI marketing content platform", url: "https://creaitor.ai", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["marketing"], featured: false, icon: "🎨"},
        {name: "ContentBot", category: "Writing", sub: "Blogs", desc: "AI blog and article writer", url: "https://contentbot.ai", pricing: "Paid", rating: 4.1, users: "30K+", tags: ["blogs", "articles"], featured: false, icon: "📝"},
    ],

    // ==================== IMAGE GENERATION ====================
    imageGeneration: [
        {name: "Midjourney", category: "Image", sub: "Art", desc: "Leading AI art generator", url: "https://midjourney.com", pricing: "Paid", rating: 4.9, users: "15M+", tags: ["art", "creative"], featured: true, icon: "🎨"},
        {name: "DALL-E 3", category: "Image", sub: "General", desc: "OpenAI's image generator", url: "https://openai.com/dall-e-3", pricing: "Paid", rating: 4.8, users: "20M+", tags: ["images", "openai"], featured: true, icon: "🖼️"},
        {name: "Stable Diffusion", category: "Image", sub: "Open Source", desc: "Open-source image generation", url: "https://stability.ai", pricing: "Free", rating: 4.7, users: "10M+", tags: ["open-source"], featured: true, icon: "🌀"},
        {name: "Leonardo AI", category: "Image", sub: "Gaming", desc: "AI for game assets", url: "https://leonardo.ai", pricing: "Freemium", rating: 4.6, users: "5M+", tags: ["gaming", "assets"], featured: true, icon: "🎮"},
        {name: "Adobe Firefly", category: "Image", sub: "Creative", desc: "Adobe's generative AI", url: "https://firefly.adobe.com", pricing: "Freemium", rating: 4.6, users: "10M+", tags: ["adobe", "creative"], featured: true, icon: "🔥"},
        {name: "Ideogram", category: "Image", sub: "Text", desc: "AI images with accurate text", url: "https://ideogram.ai", pricing: "Freemium", rating: 4.5, users: "3M+", tags: ["text", "logos"], featured: false, icon: "💡"},
        {name: "Playground AI", category: "Image", sub: "Free", desc: "Free AI image generator", url: "https://playground.ai", pricing: "Freemium", rating: 4.4, users: "2M+", tags: ["free"], featured: false, icon: "🎪"},
        {name: "Canva AI", category: "Image", sub: "Design", desc: "AI in Canva for design", url: "https://canva.com", pricing: "Freemium", rating: 4.5, users: "50M+", tags: ["design"], featured: false, icon: "🎯"},
        {name: "Bing Image Creator", category: "Image", sub: "Free", desc: "Free DALL-E powered images", url: "https://bing.com/create", pricing: "Free", rating: 4.4, users: "20M+", tags: ["free", "microsoft"], featured: false, icon: "🔷"},
        {name: "NightCafe", category: "Image", sub: "Art", desc: "AI art community platform", url: "https://nightcafe.studio", pricing: "Freemium", rating: 4.3, users: "2M+", tags: ["art", "community"], featured: false, icon: "🌙"},
        {name: "Lexica", category: "Image", sub: "Search", desc: "Search and generate AI images", url: "https://lexica.art", pricing: "Freemium", rating: 4.3, users: "1M+", tags: ["search", "gallery"], featured: false, icon: "🔍"},
        {name: "DreamStudio", category: "Image", sub: "Stable Diffusion", desc: "Official Stable Diffusion interface", url: "https://dreamstudio.ai", pricing: "Paid", rating: 4.4, users: "2M+", tags: ["stable-diffusion"], featured: false, icon: "💭"},
        {name: "Craiyon", category: "Image", sub: "Free", desc: "Free AI image generation", url: "https://craiyon.com", pricing: "Free", rating: 4.0, users: "10M+", tags: ["free", "simple"], featured: false, icon: "🖍️"},
        {name: "Artbreeder", category: "Image", sub: "Mixing", desc: "Blend and evolve images", url: "https://artbreeder.com", pricing: "Freemium", rating: 4.2, users: "3M+", tags: ["mixing", "portraits"], featured: false, icon: "🧬"},
        {name: "Blue Willow", category: "Image", sub: "Art", desc: "Free AI art on Discord", url: "https://bluewillow.ai", pricing: "Free", rating: 4.1, users: "1M+", tags: ["free", "discord"], featured: false, icon: "🌿"},
        {name: "Dreamlike", category: "Image", sub: "Art", desc: "High-quality AI art", url: "https://dreamlike.art", pricing: "Freemium", rating: 4.2, users: "500K+", tags: ["art", "quality"], featured: false, icon: "✨"},
        {name: "PhotoSonic", category: "Image", sub: "Realistic", desc: "Photorealistic AI images", url: "https://writesonic.com/photosonic-ai-art-generator", pricing: "Freemium", rating: 4.1, users: "500K+", tags: ["photorealistic"], featured: false, icon: "📷"},
        {name: "Imagine by Meta", category: "Image", sub: "Free", desc: "Meta's free image generator", url: "https://imagine.meta.com", pricing: "Free", rating: 4.3, users: "5M+", tags: ["meta", "free"], featured: false, icon: "🔵"},
        {name: "Tensor Art", category: "Image", sub: "Community", desc: "AI art with model sharing", url: "https://tensor.art", pricing: "Freemium", rating: 4.3, users: "1M+", tags: ["community", "models"], featured: false, icon: "🎨"},
        {name: "Civitai", category: "Image", sub: "Models", desc: "AI model sharing platform", url: "https://civitai.com", pricing: "Free", rating: 4.4, users: "2M+", tags: ["models", "community"], featured: false, icon: "🤖"},
        {name: "Krea AI", category: "Image", sub: "Real-time", desc: "Real-time AI image generation", url: "https://krea.ai", pricing: "Freemium", rating: 4.4, users: "500K+", tags: ["real-time", "fast"], featured: false, icon: "⚡"},
        {name: "Seaart", category: "Image", sub: "Art", desc: "AI art generation platform", url: "https://seaart.ai", pricing: "Freemium", rating: 4.2, users: "1M+", tags: ["art"], featured: false, icon: "🌊"},
        {name: "PicSo", category: "Image", sub: "Art", desc: "Text to image AI art", url: "https://picso.ai", pricing: "Freemium", rating: 4.1, users: "500K+", tags: ["art", "text-to-image"], featured: false, icon: "🎭"},
        {name: "Gencraft", category: "Image", sub: "Mobile", desc: "AI art on mobile", url: "https://gencraft.com", pricing: "Freemium", rating: 4.2, users: "2M+", tags: ["mobile", "app"], featured: false, icon: "📱"},
    ],

    // ==================== VIDEO ====================
    video: [
        {name: "Runway", category: "Video", sub: "Generation", desc: "AI video generation and editing", url: "https://runway.ml", pricing: "Freemium", rating: 4.7, users: "5M+", tags: ["video", "editing"], featured: true, icon: "🎬"},
        {name: "Pika Labs", category: "Video", sub: "Generation", desc: "Text-to-video AI", url: "https://pika.art", pricing: "Freemium", rating: 4.5, users: "2M+", tags: ["video", "animation"], featured: true, icon: "📹"},
        {name: "Synthesia", category: "Video", sub: "Avatars", desc: "AI avatar videos", url: "https://synthesia.io", pricing: "Paid", rating: 4.6, users: "50K+", tags: ["avatars", "training"], featured: true, icon: "👤"},
        {name: "HeyGen", category: "Video", sub: "Avatars", desc: "AI videos with avatars", url: "https://heygen.com", pricing: "Freemium", rating: 4.5, users: "100K+", tags: ["avatars", "voice"], featured: true, icon: "🗣️"},
        {name: "Descript", category: "Video", sub: "Editing", desc: "AI video/podcast editing", url: "https://descript.com", pricing: "Freemium", rating: 4.7, users: "3M+", tags: ["editing", "podcast"], featured: true, icon: "✂️"},
        {name: "CapCut", category: "Video", sub: "Editing", desc: "Free video editor with AI", url: "https://capcut.com", pricing: "Free", rating: 4.6, users: "200M+", tags: ["editing", "free"], featured: true, icon: "📱"},
        {name: "Opus Clip", category: "Video", sub: "Clips", desc: "Turn long videos into clips", url: "https://opus.pro", pricing: "Freemium", rating: 4.5, users: "500K+", tags: ["clips", "shorts"], featured: false, icon: "🎞️"},
        {name: "Lumen5", category: "Video", sub: "Marketing", desc: "Blog to video AI", url: "https://lumen5.com", pricing: "Freemium", rating: 4.3, users: "500K+", tags: ["marketing", "blog"], featured: false, icon: "💡"},
        {name: "InVideo", category: "Video", sub: "Templates", desc: "AI video maker", url: "https://invideo.io", pricing: "Freemium", rating: 4.4, users: "2M+", tags: ["templates"], featured: false, icon: "🎥"},
        {name: "Pictory", category: "Video", sub: "Content", desc: "AI video from scripts", url: "https://pictory.ai", pricing: "Paid", rating: 4.3, users: "200K+", tags: ["scripts", "content"], featured: false, icon: "📽️"},
        {name: "D-ID", category: "Video", sub: "Avatars", desc: "AI talking avatars", url: "https://d-id.com", pricing: "Freemium", rating: 4.4, users: "500K+", tags: ["avatars", "talking"], featured: false, icon: "🎭"},
        {name: "Colossyan", category: "Video", sub: "Training", desc: "AI videos for L&D", url: "https://colossyan.com", pricing: "Paid", rating: 4.3, users: "50K+", tags: ["training", "enterprise"], featured: false, icon: "🎓"},
        {name: "Elai.io", category: "Video", sub: "Avatars", desc: "AI video from text", url: "https://elai.io", pricing: "Paid", rating: 4.2, users: "100K+", tags: ["avatars", "text"], featured: false, icon: "🤖"},
        {name: "Fliki", category: "Video", sub: "Content", desc: "Text to video with AI voice", url: "https://fliki.ai", pricing: "Freemium", rating: 4.3, users: "300K+", tags: ["voice", "video"], featured: false, icon: "🎤"},
        {name: "Steve AI", category: "Video", sub: "Animation", desc: "AI animated videos", url: "https://steve.ai", pricing: "Freemium", rating: 4.2, users: "200K+", tags: ["animation"], featured: false, icon: "🎬"},
        {name: "Veed.io", category: "Video", sub: "Editing", desc: "Online video editor with AI", url: "https://veed.io", pricing: "Freemium", rating: 4.4, users: "1M+", tags: ["editing", "online"], featured: false, icon: "🎞️"},
        {name: "Kapwing", category: "Video", sub: "Editing", desc: "AI video editing platform", url: "https://kapwing.com", pricing: "Freemium", rating: 4.3, users: "1M+", tags: ["editing", "collaboration"], featured: false, icon: "✨"},
        {name: "Wondershare Filmora", category: "Video", sub: "Editing", desc: "Desktop video editor with AI", url: "https://filmora.wondershare.com", pricing: "Paid", rating: 4.4, users: "5M+", tags: ["desktop", "editing"], featured: false, icon: "🎬"},
        {name: "Captions", category: "Video", sub: "Captions", desc: "AI auto-captions for videos", url: "https://captions.ai", pricing: "Freemium", rating: 4.5, users: "2M+", tags: ["captions", "accessibility"], featured: false, icon: "💬"},
        {name: "Sora (OpenAI)", category: "Video", sub: "Generation", desc: "OpenAI's video generation model", url: "https://openai.com/sora", pricing: "Coming Soon", rating: 5.0, users: "0", tags: ["upcoming", "openai"], featured: true, icon: "🌟"},
    ],

    // ==================== AUDIO & MUSIC ====================
    audio: [
        {name: "ElevenLabs", category: "Audio", sub: "Voice", desc: "Most realistic AI voice generation", url: "https://elevenlabs.io", pricing: "Freemium", rating: 4.9, users: "5M+", tags: ["voice", "tts"], featured: true, icon: "🎙️"},
        {name: "Suno AI", category: "Audio", sub: "Music", desc: "Create full songs with AI", url: "https://suno.ai", pricing: "Freemium", rating: 4.7, users: "3M+", tags: ["music", "songs"], featured: true, icon: "🎵"},
        {name: "Udio", category: "Audio", sub: "Music", desc: "AI music with vocals", url: "https://udio.com", pricing: "Freemium", rating: 4.6, users: "2M+", tags: ["music"], featured: true, icon: "🎶"},
        {name: "Murf AI", category: "Audio", sub: "Voiceover", desc: "AI voiceover generator", url: "https://murf.ai", pricing: "Freemium", rating: 4.5, users: "500K+", tags: ["voiceover"], featured: false, icon: "🔊"},
        {name: "AIVA", category: "Audio", sub: "Composition", desc: "AI music composer", url: "https://aiva.ai", pricing: "Freemium", rating: 4.4, users: "500K+", tags: ["composition"], featured: false, icon: "🎼"},
        {name: "Krisp", category: "Audio", sub: "Noise Cancel", desc: "AI noise cancellation", url: "https://krisp.ai", pricing: "Freemium", rating: 4.6, users: "3M+", tags: ["noise"], featured: false, icon: "🔇"},
        {name: "Soundraw", category: "Audio", sub: "Music", desc: "AI royalty-free music", url: "https://soundraw.io", pricing: "Paid", rating: 4.3, users: "200K+", tags: ["royalty-free"], featured: false, icon: "🎹"},
        {name: "Beatoven.ai", category: "Audio", sub: "Music", desc: "AI background music", url: "https://beatoven.ai", pricing: "Freemium", rating: 4.2, users: "100K+", tags: ["background"], featured: false, icon: "🎧"},
        {name: "Podcastle", category: "Audio", sub: "Podcast", desc: "AI podcast creation", url: "https://podcastle.ai", pricing: "Freemium", rating: 4.4, users: "500K+", tags: ["podcast"], featured: false, icon: "🎙️"},
        {name: "Resemble AI", category: "Audio", sub: "Voice Clone", desc: "AI voice cloning", url: "https://resemble.ai", pricing: "Paid", rating: 4.4, users: "100K+", tags: ["cloning"], featured: false, icon: "👥"},
        {name: "Play.ht", category: "Audio", sub: "TTS", desc: "AI text to speech", url: "https://play.ht", pricing: "Freemium", rating: 4.4, users: "300K+", tags: ["tts"], featured: false, icon: "▶️"},
        {name: "Speechify", category: "Audio", sub: "TTS", desc: "Text to speech reader", url: "https://speechify.com", pricing: "Freemium", rating: 4.5, users: "5M+", tags: ["reader", "tts"], featured: false, icon: "📖"},
        {name: "Descript Overdub", category: "Audio", sub: "Voice Clone", desc: "Clone your voice", url: "https://descript.com/overdub", pricing: "Paid", rating: 4.5, users: "500K+", tags: ["cloning"], featured: false, icon: "🎤"},
        {name: "Voicemod", category: "Audio", sub: "Voice Changer", desc: "Real-time voice changer", url: "https://voicemod.net", pricing: "Freemium", rating: 4.3, users: "2M+", tags: ["voice-changer"], featured: false, icon: "🎭"},
        {name: "Adobe Podcast", category: "Audio", sub: "Enhancement", desc: "AI audio enhancement", url: "https://podcast.adobe.com", pricing: "Free", rating: 4.5, users: "1M+", tags: ["enhancement", "free"], featured: false, icon: "🎚️"},
        {name: "Lalal.ai", category: "Audio", sub: "Separation", desc: "AI vocal/music separation", url: "https://lalal.ai", pricing: "Freemium", rating: 4.5, users: "500K+", tags: ["separation"], featured: false, icon: "🔀"},
        {name: "Cleanvoice", category: "Audio", sub: "Editing", desc: "AI podcast editing", url: "https://cleanvoice.ai", pricing: "Paid", rating: 4.3, users: "100K+", tags: ["editing", "podcast"], featured: false, icon: "🧹"},
        {name: "Riffusion", category: "Audio", sub: "Music", desc: "AI music from images", url: "https://riffusion.com", pricing: "Free", rating: 4.2, users: "500K+", tags: ["experimental"], featured: false, icon: "🌊"},
        {name: "Boomy", category: "Audio", sub: "Music", desc: "Create and release AI music", url: "https://boomy.com", pricing: "Freemium", rating: 4.1, users: "1M+", tags: ["music", "release"], featured: false, icon: "💥"},
        {name: "Soundful", category: "Audio", sub: "Music", desc: "AI background music", url: "https://soundful.com", pricing: "Freemium", rating: 4.2, users: "200K+", tags: ["background"], featured: false, icon: "🎹"},
    ],

    // ==================== CODING & DEVELOPMENT ====================
    coding: [
        {name: "GitHub Copilot", category: "Coding", sub: "Assistant", desc: "AI pair programmer", url: "https://github.com/features/copilot", pricing: "Paid", rating: 4.8, users: "1.5M+", tags: ["coding"], featured: true, icon: "🐙"},
        {name: "Cursor", category: "Coding", sub: "IDE", desc: "AI-first code editor", url: "https://cursor.sh", pricing: "Freemium", rating: 4.7, users: "500K+", tags: ["ide"], featured: true, icon: "⌨️"},
        {name: "Replit AI", category: "Coding", sub: "IDE", desc: "Browser-based AI coding", url: "https://replit.com/ai", pricing: "Freemium", rating: 4.5, users: "20M+", tags: ["browser"], featured: true, icon: "💻"},
        {name: "Codeium", category: "Coding", sub: "Autocomplete", desc: "Free AI code completion", url: "https://codeium.com", pricing: "Free", rating: 4.5, users: "500K+", tags: ["free"], featured: true, icon: "🆓"},
        {name: "Tabnine", category: "Coding", sub: "Autocomplete", desc: "AI code completion", url: "https://tabnine.com", pricing: "Freemium", rating: 4.4, users: "1M+", tags: ["autocomplete"], featured: false, icon: "⌘"},
        {name: "v0 by Vercel", category: "Coding", sub: "UI", desc: "Generate React UI", url: "https://v0.dev", pricing: "Freemium", rating: 4.6, users: "500K+", tags: ["ui", "react"], featured: true, icon: "🎨"},
        {name: "bolt.new", category: "Coding", sub: "Full Stack", desc: "Generate full-stack apps", url: "https://bolt.new", pricing: "Freemium", rating: 4.5, users: "200K+", tags: ["fullstack"], featured: true, icon: "⚡"},
        {name: "Amazon CodeWhisperer", category: "Coding", sub: "AWS", desc: "AWS AI coding companion", url: "https://aws.amazon.com/codewhisperer", pricing: "Freemium", rating: 4.3, users: "500K+", tags: ["aws"], featured: false, icon: "☁️"},
        {name: "Sourcegraph Cody", category: "Coding", sub: "Search", desc: "AI code search and chat", url: "https://sourcegraph.com/cody", pricing: "Freemium", rating: 4.4, users: "200K+", tags: ["search"], featured: false, icon: "🔍"},
        {name: "Pieces", category: "Coding", sub: "Snippets", desc: "AI code snippet manager", url: "https://pieces.app", pricing: "Free", rating: 4.3, users: "200K+", tags: ["snippets"], featured: false, icon: "🧩"},
        {name: "Continue", category: "Coding", sub: "Open Source", desc: "Open source AI coding", url: "https://continue.dev", pricing: "Free", rating: 4.4, users: "100K+", tags: ["open-source"], featured: false, icon: "🔄"},
        {name: "Aider", category: "Coding", sub: "Terminal", desc: "AI pair programming in terminal", url: "https://aider.chat", pricing: "Free", rating: 4.5, users: "50K+", tags: ["terminal", "open-source"], featured: false, icon: "💻"},
        {name: "Codium AI", category: "Coding", sub: "Testing", desc: "AI test generation", url: "https://codium.ai", pricing: "Freemium", rating: 4.3, users: "100K+", tags: ["testing"], featured: false, icon: "🧪"},
        {name: "Mintlify", category: "Coding", sub: "Docs", desc: "AI documentation generator", url: "https://mintlify.com", pricing: "Freemium", rating: 4.4, users: "50K+", tags: ["docs"], featured: false, icon: "📄"},
        {name: "Swimm", category: "Coding", sub: "Docs", desc: "AI code documentation", url: "https://swimm.io", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["docs"], featured: false, icon: "🏊"},
        {name: "Bito", category: "Coding", sub: "Assistant", desc: "AI coding assistant", url: "https://bito.ai", pricing: "Freemium", rating: 4.2, users: "100K+", tags: ["assistant"], featured: false, icon: "🤖"},
        {name: "Blackbox AI", category: "Coding", sub: "Search", desc: "AI code search", url: "https://blackbox.ai", pricing: "Freemium", rating: 4.1, users: "500K+", tags: ["search"], featured: false, icon: "⬛"},
        {name: "CodeGPT", category: "Coding", sub: "VSCode", desc: "GPT in VS Code", url: "https://codegpt.co", pricing: "Freemium", rating: 4.2, users: "200K+", tags: ["vscode"], featured: false, icon: "💬"},
        {name: "Cody (Sourcegraph)", category: "Coding", sub: "Enterprise", desc: "Enterprise AI coding", url: "https://sourcegraph.com/cody", pricing: "Paid", rating: 4.4, users: "50K+", tags: ["enterprise"], featured: false, icon: "🏢"},
        {name: "Refact.ai", category: "Coding", sub: "Self-hosted", desc: "Self-hosted AI coding", url: "https://refact.ai", pricing: "Freemium", rating: 4.2, users: "50K+", tags: ["self-hosted"], featured: false, icon: "🏠"},
    ]
};

// Export for use
if (typeof window !== 'undefined') {
    window.AI_TOOLS_DATABASE = AI_TOOLS_DATABASE;
}


