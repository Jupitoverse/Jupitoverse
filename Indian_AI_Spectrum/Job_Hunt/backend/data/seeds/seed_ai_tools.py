"""
Seed AI Tools Data - Comprehensive AI tools directory
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models import get_db, AITool, AIToolCategory, PricingModel

AI_TOOLS = [
    # ==================== TEXT GENERATION / LLMs ====================
    {
        "name": "ChatGPT",
        "slug": "chatgpt",
        "tagline": "AI-powered conversational assistant",
        "description": "ChatGPT is an AI chatbot developed by OpenAI that uses large language models to generate human-like text responses. It can answer questions, write content, code, and assist with various tasks.",
        "category": AIToolCategory.CHATBOT,
        "tags": ["chatbot", "gpt", "nlp", "writing", "coding"],
        "website_url": "https://chat.openai.com",
        "api_url": "https://platform.openai.com/docs/api-reference",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
        "pricing_model": PricingModel.FREEMIUM,
        "free_tier_limits": "GPT-3.5 free, GPT-4 with Plus subscription",
        "starting_price": "$20/month for Plus",
        "features": ["Multi-turn conversations", "Code generation", "Image understanding", "Web browsing", "Plugins"],
        "use_cases": ["Content writing", "Coding assistance", "Research", "Learning", "Customer support"],
        "api_available": True,
        "company_name": "OpenAI",
        "user_count": "100M+",
        "is_featured": True
    },
    {
        "name": "Claude",
        "slug": "claude",
        "tagline": "AI assistant by Anthropic focused on safety",
        "description": "Claude is an AI assistant created by Anthropic designed to be helpful, harmless, and honest. Known for longer context windows and nuanced responses.",
        "category": AIToolCategory.CHATBOT,
        "tags": ["chatbot", "anthropic", "safe-ai", "writing"],
        "website_url": "https://claude.ai",
        "api_url": "https://docs.anthropic.com",
        "pricing_model": PricingModel.FREEMIUM,
        "starting_price": "$20/month for Pro",
        "features": ["200K context window", "Document analysis", "Code generation", "Safe responses"],
        "use_cases": ["Long document analysis", "Research", "Writing", "Coding"],
        "api_available": True,
        "company_name": "Anthropic",
        "is_featured": True
    },
    {
        "name": "Google Gemini",
        "slug": "google-gemini",
        "tagline": "Google's most capable AI model",
        "description": "Gemini is Google's largest and most capable AI model, designed to be multimodal from the ground up. It can process text, code, images, audio, and video.",
        "category": AIToolCategory.CHATBOT,
        "tags": ["google", "multimodal", "chatbot"],
        "website_url": "https://gemini.google.com",
        "api_url": "https://ai.google.dev",
        "pricing_model": PricingModel.FREEMIUM,
        "features": ["Multimodal understanding", "Google integration", "Code generation"],
        "api_available": True,
        "company_name": "Google",
        "is_featured": True
    },
    {
        "name": "Perplexity AI",
        "slug": "perplexity-ai",
        "tagline": "AI-powered answer engine with citations",
        "description": "Perplexity AI is an AI-powered search engine that provides direct answers to questions with source citations. Great for research and fact-checking.",
        "category": AIToolCategory.RESEARCH,
        "tags": ["search", "research", "citations", "facts"],
        "website_url": "https://perplexity.ai",
        "pricing_model": PricingModel.FREEMIUM,
        "starting_price": "$20/month for Pro",
        "features": ["Source citations", "Real-time search", "Follow-up questions", "File analysis"],
        "use_cases": ["Research", "Fact-checking", "Learning", "News"],
        "company_name": "Perplexity AI",
        "is_featured": True
    },
    
    # ==================== CODE ASSISTANTS ====================
    {
        "name": "GitHub Copilot",
        "slug": "github-copilot",
        "tagline": "Your AI pair programmer",
        "description": "GitHub Copilot is an AI coding assistant that helps you write code faster. It suggests whole lines or entire functions based on context.",
        "category": AIToolCategory.CODE_ASSISTANT,
        "tags": ["coding", "ide", "autocomplete", "github"],
        "website_url": "https://github.com/features/copilot",
        "documentation_url": "https://docs.github.com/en/copilot",
        "pricing_model": PricingModel.PAID,
        "starting_price": "$10/month",
        "features": ["Code completion", "Multi-language support", "IDE integration", "Chat interface"],
        "use_cases": ["Code writing", "Learning", "Documentation", "Testing"],
        "integrations": ["VS Code", "JetBrains", "Neovim", "GitHub"],
        "company_name": "GitHub (Microsoft)",
        "is_featured": True
    },
    {
        "name": "Cursor",
        "slug": "cursor",
        "tagline": "The AI-first code editor",
        "description": "Cursor is an AI-powered code editor built for pair programming with AI. Fork of VS Code with native AI integration.",
        "category": AIToolCategory.CODE_ASSISTANT,
        "tags": ["ide", "coding", "editor", "ai-native"],
        "website_url": "https://cursor.sh",
        "pricing_model": PricingModel.FREEMIUM,
        "starting_price": "$20/month for Pro",
        "features": ["AI chat", "Codebase understanding", "Multi-file editing", "VS Code compatible"],
        "use_cases": ["Coding", "Refactoring", "Learning", "Documentation"],
        "platforms": ["desktop"],
        "company_name": "Anysphere",
        "is_featured": True
    },
    {
        "name": "Tabnine",
        "slug": "tabnine",
        "tagline": "AI code completion for all languages",
        "description": "Tabnine is an AI assistant for software developers that speeds up coding with whole-line and full-function code completions.",
        "category": AIToolCategory.CODE_ASSISTANT,
        "tags": ["coding", "autocomplete", "privacy"],
        "website_url": "https://tabnine.com",
        "pricing_model": PricingModel.FREEMIUM,
        "starting_price": "$12/month",
        "features": ["Privacy-focused", "On-premise option", "All major languages", "Team training"],
        "integrations": ["VS Code", "JetBrains", "Vim", "Sublime"],
        "company_name": "Tabnine",
        "is_featured": False
    },
    {
        "name": "Codeium",
        "slug": "codeium",
        "tagline": "Free AI code completion",
        "description": "Codeium is a free AI-powered code completion tool supporting 70+ languages. Great alternative to GitHub Copilot.",
        "category": AIToolCategory.CODE_ASSISTANT,
        "tags": ["coding", "free", "autocomplete"],
        "website_url": "https://codeium.com",
        "pricing_model": PricingModel.FREE,
        "features": ["Free for individuals", "70+ languages", "Chat interface", "Fast completions"],
        "integrations": ["VS Code", "JetBrains", "Vim", "Chrome"],
        "company_name": "Exafunction",
        "is_featured": True
    },
    {
        "name": "Replit AI",
        "slug": "replit-ai",
        "tagline": "AI-powered coding in the browser",
        "description": "Replit's AI features include code generation, explanation, and transformation directly in their online IDE.",
        "category": AIToolCategory.CODE_ASSISTANT,
        "tags": ["coding", "browser", "learning"],
        "website_url": "https://replit.com",
        "pricing_model": PricingModel.FREEMIUM,
        "features": ["Browser-based IDE", "AI code generation", "Collaboration", "Deployment"],
        "platforms": ["web"],
        "company_name": "Replit",
        "is_featured": False
    },
    
    # ==================== IMAGE GENERATION ====================
    {
        "name": "Midjourney",
        "slug": "midjourney",
        "tagline": "AI art generator with stunning quality",
        "description": "Midjourney is an AI art generator known for creating highly artistic and stylized images. Works through Discord.",
        "category": AIToolCategory.IMAGE_GENERATION,
        "tags": ["art", "images", "creative", "discord"],
        "website_url": "https://midjourney.com",
        "pricing_model": PricingModel.PAID,
        "starting_price": "$10/month",
        "features": ["High-quality art", "Style control", "Variations", "Upscaling"],
        "use_cases": ["Art creation", "Concept design", "Marketing", "Social media"],
        "platforms": ["discord"],
        "company_name": "Midjourney",
        "is_featured": True
    },
    {
        "name": "DALL-E 3",
        "slug": "dall-e-3",
        "tagline": "OpenAI's advanced image generation",
        "description": "DALL-E 3 by OpenAI generates highly detailed images from text descriptions with improved accuracy and safety features.",
        "category": AIToolCategory.IMAGE_GENERATION,
        "tags": ["openai", "images", "text-to-image"],
        "website_url": "https://openai.com/dall-e-3",
        "api_url": "https://platform.openai.com/docs/guides/images",
        "pricing_model": PricingModel.PAID,
        "features": ["High fidelity", "Text rendering", "ChatGPT integration", "API access"],
        "api_available": True,
        "company_name": "OpenAI",
        "is_featured": True
    },
    {
        "name": "Stable Diffusion",
        "slug": "stable-diffusion",
        "tagline": "Open-source image generation",
        "description": "Stable Diffusion is an open-source AI model for generating images. Can be run locally or via various hosted services.",
        "category": AIToolCategory.IMAGE_GENERATION,
        "tags": ["open-source", "images", "local"],
        "website_url": "https://stability.ai",
        "github_url": "https://github.com/Stability-AI/stablediffusion",
        "pricing_model": PricingModel.OPEN_SOURCE,
        "features": ["Open source", "Local running", "Fine-tuning", "ControlNet"],
        "open_source": True,
        "self_hosted": True,
        "company_name": "Stability AI",
        "is_featured": True
    },
    {
        "name": "Leonardo AI",
        "slug": "leonardo-ai",
        "tagline": "AI image generation for game assets",
        "description": "Leonardo AI specializes in generating game assets, concept art, and consistent character designs.",
        "category": AIToolCategory.IMAGE_GENERATION,
        "tags": ["gaming", "assets", "art", "characters"],
        "website_url": "https://leonardo.ai",
        "pricing_model": PricingModel.FREEMIUM,
        "features": ["Game assets", "Character consistency", "Fine-tuning", "API"],
        "use_cases": ["Game development", "Concept art", "Marketing"],
        "company_name": "Leonardo AI",
        "is_featured": False
    },
    {
        "name": "Canva AI",
        "slug": "canva-ai",
        "tagline": "AI-powered design tools",
        "description": "Canva's Magic Studio includes AI tools for image generation, editing, writing, and design automation.",
        "category": AIToolCategory.DESIGN,
        "tags": ["design", "marketing", "social-media"],
        "website_url": "https://canva.com",
        "pricing_model": PricingModel.FREEMIUM,
        "features": ["Magic Write", "Magic Design", "Background removal", "Text to image"],
        "use_cases": ["Social media", "Marketing", "Presentations"],
        "company_name": "Canva",
        "is_featured": True
    },
    
    # ==================== VIDEO GENERATION ====================
    {
        "name": "Runway",
        "slug": "runway",
        "tagline": "AI-powered video generation and editing",
        "description": "Runway offers Gen-2 for text-to-video generation and various AI tools for video editing and effects.",
        "category": AIToolCategory.VIDEO_GENERATION,
        "tags": ["video", "editing", "generation"],
        "website_url": "https://runwayml.com",
        "pricing_model": PricingModel.FREEMIUM,
        "starting_price": "$12/month",
        "features": ["Text to video", "Image to video", "Video editing", "Green screen"],
        "use_cases": ["Content creation", "Film", "Marketing"],
        "company_name": "Runway",
        "is_featured": True
    },
    {
        "name": "Synthesia",
        "slug": "synthesia",
        "tagline": "AI video generation with avatars",
        "description": "Synthesia creates AI videos with realistic avatars. Great for training videos, marketing, and corporate communications.",
        "category": AIToolCategory.VIDEO_GENERATION,
        "tags": ["avatars", "corporate", "training"],
        "website_url": "https://synthesia.io",
        "pricing_model": PricingModel.PAID,
        "starting_price": "$22/month",
        "features": ["140+ avatars", "120+ languages", "Custom avatars", "Templates"],
        "use_cases": ["Training videos", "Marketing", "Sales"],
        "company_name": "Synthesia",
        "is_featured": False
    },
    {
        "name": "Pika",
        "slug": "pika",
        "tagline": "Create and edit videos with AI",
        "description": "Pika allows you to create and edit videos using AI, turning ideas into visual content with simple prompts.",
        "category": AIToolCategory.VIDEO_GENERATION,
        "tags": ["video", "creative", "editing"],
        "website_url": "https://pika.art",
        "pricing_model": PricingModel.FREEMIUM,
        "features": ["Text to video", "Image to video", "Video editing"],
        "company_name": "Pika Labs",
        "is_featured": False
    },
    
    # ==================== AUDIO & MUSIC ====================
    {
        "name": "ElevenLabs",
        "slug": "elevenlabs",
        "tagline": "AI voice generation and cloning",
        "description": "ElevenLabs offers high-quality AI voice generation, voice cloning, and text-to-speech in multiple languages.",
        "category": AIToolCategory.AUDIO_MUSIC,
        "tags": ["voice", "tts", "cloning"],
        "website_url": "https://elevenlabs.io",
        "api_url": "https://elevenlabs.io/docs",
        "pricing_model": PricingModel.FREEMIUM,
        "starting_price": "$5/month",
        "features": ["Voice cloning", "29 languages", "Emotional control", "API"],
        "use_cases": ["Audiobooks", "Podcasts", "Content creation"],
        "api_available": True,
        "company_name": "ElevenLabs",
        "is_featured": True
    },
    {
        "name": "Suno AI",
        "slug": "suno-ai",
        "tagline": "Create music with AI",
        "description": "Suno AI generates complete songs with vocals, instruments, and lyrics from text prompts.",
        "category": AIToolCategory.AUDIO_MUSIC,
        "tags": ["music", "songs", "creative"],
        "website_url": "https://suno.ai",
        "pricing_model": PricingModel.FREEMIUM,
        "features": ["Full songs", "Lyrics generation", "Multiple genres", "High quality"],
        "use_cases": ["Music creation", "Content", "Fun"],
        "company_name": "Suno",
        "is_featured": True
    },
    {
        "name": "Murf AI",
        "slug": "murf-ai",
        "tagline": "AI voiceover generator",
        "description": "Murf AI creates studio-quality voiceovers with AI. 120+ voices across 20 languages.",
        "category": AIToolCategory.AUDIO_MUSIC,
        "tags": ["voiceover", "tts", "professional"],
        "website_url": "https://murf.ai",
        "pricing_model": PricingModel.FREEMIUM,
        "starting_price": "$19/month",
        "features": ["120+ voices", "Pitch control", "Video sync", "API"],
        "use_cases": ["E-learning", "Marketing", "YouTube"],
        "company_name": "Murf AI",
        "is_featured": False
    },
    
    # ==================== WRITING & CONTENT ====================
    {
        "name": "Jasper AI",
        "slug": "jasper-ai",
        "tagline": "AI content platform for marketing",
        "description": "Jasper is an AI writing assistant designed for marketing teams. Creates blog posts, ads, social content, and more.",
        "category": AIToolCategory.WRITING,
        "tags": ["marketing", "content", "copywriting"],
        "website_url": "https://jasper.ai",
        "pricing_model": PricingModel.PAID,
        "starting_price": "$39/month",
        "features": ["Brand voice", "Templates", "SEO optimization", "Team collaboration"],
        "use_cases": ["Marketing", "Blog writing", "Social media", "Ads"],
        "company_name": "Jasper",
        "is_featured": True
    },
    {
        "name": "Copy.ai",
        "slug": "copy-ai",
        "tagline": "AI copywriting made simple",
        "description": "Copy.ai generates marketing copy, social media posts, and various content types with AI.",
        "category": AIToolCategory.WRITING,
        "tags": ["copywriting", "marketing", "social"],
        "website_url": "https://copy.ai",
        "pricing_model": PricingModel.FREEMIUM,
        "features": ["90+ templates", "Multiple languages", "Brand voices"],
        "use_cases": ["Marketing copy", "Social media", "Emails"],
        "company_name": "Copy.ai",
        "is_featured": False
    },
    {
        "name": "Grammarly",
        "slug": "grammarly",
        "tagline": "AI writing assistant for grammar and style",
        "description": "Grammarly helps improve your writing with grammar checking, style suggestions, and AI-powered rewrites.",
        "category": AIToolCategory.WRITING,
        "tags": ["grammar", "editing", "writing"],
        "website_url": "https://grammarly.com",
        "pricing_model": PricingModel.FREEMIUM,
        "starting_price": "$12/month",
        "features": ["Grammar check", "Tone detection", "Plagiarism check", "AI rewrite"],
        "integrations": ["Chrome", "Word", "Gmail", "Slack"],
        "company_name": "Grammarly",
        "is_featured": True
    },
    {
        "name": "Notion AI",
        "slug": "notion-ai",
        "tagline": "AI assistant in your workspace",
        "description": "Notion AI helps with writing, summarizing, brainstorming, and organizing within your Notion workspace.",
        "category": AIToolCategory.PRODUCTIVITY,
        "tags": ["productivity", "writing", "notes"],
        "website_url": "https://notion.so/product/ai",
        "pricing_model": PricingModel.PAID,
        "starting_price": "$10/month per member",
        "features": ["Summarization", "Writing assistance", "Translation", "Action items"],
        "integrations": ["Notion"],
        "company_name": "Notion",
        "is_featured": True
    },
    
    # ==================== PRODUCTIVITY ====================
    {
        "name": "Otter.ai",
        "slug": "otter-ai",
        "tagline": "AI meeting transcription",
        "description": "Otter.ai provides real-time transcription for meetings, interviews, and conversations with AI-powered summaries.",
        "category": AIToolCategory.PRODUCTIVITY,
        "tags": ["transcription", "meetings", "notes"],
        "website_url": "https://otter.ai",
        "pricing_model": PricingModel.FREEMIUM,
        "starting_price": "$8.33/month",
        "features": ["Real-time transcription", "Meeting summaries", "Speaker identification", "Integrations"],
        "integrations": ["Zoom", "Google Meet", "Teams"],
        "company_name": "Otter.ai",
        "is_featured": False
    },
    {
        "name": "Zapier AI",
        "slug": "zapier-ai",
        "tagline": "AI-powered automation",
        "description": "Zapier's AI features help create automations using natural language and add AI capabilities to workflows.",
        "category": AIToolCategory.AUTOMATION,
        "tags": ["automation", "workflows", "integration"],
        "website_url": "https://zapier.com",
        "pricing_model": PricingModel.FREEMIUM,
        "features": ["Natural language automation", "AI actions", "6000+ app integrations"],
        "use_cases": ["Workflow automation", "Data processing", "Marketing"],
        "company_name": "Zapier",
        "is_featured": False
    },
    
    # ==================== DATA & ANALYTICS ====================
    {
        "name": "Julius AI",
        "slug": "julius-ai",
        "tagline": "AI data analyst",
        "description": "Julius AI analyzes your data, creates visualizations, and answers questions about your datasets using natural language.",
        "category": AIToolCategory.DATA_ANALYSIS,
        "tags": ["data", "analytics", "visualization"],
        "website_url": "https://julius.ai",
        "pricing_model": PricingModel.FREEMIUM,
        "features": ["Data analysis", "Visualizations", "Python execution", "Excel/CSV support"],
        "use_cases": ["Data analysis", "Reporting", "Research"],
        "company_name": "Julius AI",
        "is_featured": False
    },
    
    # ==================== OPEN SOURCE / SELF-HOSTED ====================
    {
        "name": "Ollama",
        "slug": "ollama",
        "tagline": "Run LLMs locally",
        "description": "Ollama makes it easy to run large language models locally on your machine. Supports Llama, Mistral, and more.",
        "category": AIToolCategory.TEXT_GENERATION,
        "tags": ["local", "open-source", "llm", "privacy"],
        "website_url": "https://ollama.ai",
        "github_url": "https://github.com/ollama/ollama",
        "pricing_model": PricingModel.OPEN_SOURCE,
        "features": ["Local LLMs", "Privacy", "Multiple models", "API compatible"],
        "open_source": True,
        "self_hosted": True,
        "company_name": "Ollama",
        "is_featured": True
    },
    {
        "name": "LM Studio",
        "slug": "lm-studio",
        "tagline": "Discover and run local LLMs",
        "description": "LM Studio provides a desktop app for discovering, downloading, and running local LLMs with a ChatGPT-like interface.",
        "category": AIToolCategory.TEXT_GENERATION,
        "tags": ["local", "desktop", "llm"],
        "website_url": "https://lmstudio.ai",
        "pricing_model": PricingModel.FREE,
        "features": ["Model discovery", "Local inference", "Chat UI", "API server"],
        "platforms": ["desktop"],
        "self_hosted": True,
        "is_featured": False
    },
    {
        "name": "Hugging Face",
        "slug": "hugging-face",
        "tagline": "The AI community's home",
        "description": "Hugging Face is the leading platform for sharing and collaborating on machine learning models, datasets, and spaces.",
        "category": AIToolCategory.RESEARCH,
        "tags": ["models", "datasets", "community", "ml"],
        "website_url": "https://huggingface.co",
        "github_url": "https://github.com/huggingface",
        "pricing_model": PricingModel.FREEMIUM,
        "features": ["Model hub", "Datasets", "Spaces", "Inference API", "Training"],
        "use_cases": ["ML development", "Model hosting", "Research"],
        "api_available": True,
        "open_source": True,
        "company_name": "Hugging Face",
        "is_featured": True
    },
    {
        "name": "LangChain",
        "slug": "langchain",
        "tagline": "Build LLM-powered applications",
        "description": "LangChain is a framework for developing applications powered by language models, enabling chains of AI components.",
        "category": AIToolCategory.CODE_ASSISTANT,
        "tags": ["framework", "llm", "development", "python"],
        "website_url": "https://langchain.com",
        "github_url": "https://github.com/langchain-ai/langchain",
        "documentation_url": "https://python.langchain.com",
        "pricing_model": PricingModel.OPEN_SOURCE,
        "features": ["Chains", "Agents", "RAG", "Memory", "Tools"],
        "open_source": True,
        "supported_languages": ["Python", "JavaScript"],
        "company_name": "LangChain",
        "is_featured": True
    }
]


def seed_ai_tools():
    """Seed AI tools data"""
    db = next(get_db())
    
    try:
        count = 0
        for tool_data in AI_TOOLS:
            existing = db.query(AITool).filter(AITool.slug == tool_data["slug"]).first()
            
            if existing:
                print(f"Tool exists: {tool_data['name']}")
                continue
            
            tool = AITool(
                name=tool_data["name"],
                slug=tool_data["slug"],
                tagline=tool_data.get("tagline"),
                description=tool_data.get("description"),
                category=tool_data.get("category", AIToolCategory.OTHER),
                tags=tool_data.get("tags"),
                website_url=tool_data.get("website_url"),
                api_url=tool_data.get("api_url"),
                github_url=tool_data.get("github_url"),
                documentation_url=tool_data.get("documentation_url"),
                logo_url=tool_data.get("logo_url"),
                pricing_model=tool_data.get("pricing_model", PricingModel.FREEMIUM),
                free_tier_limits=tool_data.get("free_tier_limits"),
                starting_price=tool_data.get("starting_price"),
                features=tool_data.get("features"),
                use_cases=tool_data.get("use_cases"),
                integrations=tool_data.get("integrations"),
                api_available=tool_data.get("api_available", False),
                open_source=tool_data.get("open_source", False),
                self_hosted=tool_data.get("self_hosted", False),
                supported_languages=tool_data.get("supported_languages"),
                platforms=tool_data.get("platforms"),
                company_name=tool_data.get("company_name"),
                user_count=tool_data.get("user_count"),
                is_featured=tool_data.get("is_featured", False)
            )
            db.add(tool)
            count += 1
            print(f"Created tool: {tool_data['name']}")
        
        db.commit()
        print(f"✅ {count} AI tools seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding AI tools: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_ai_tools()
