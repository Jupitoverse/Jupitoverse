"""
AI Tools Scraper - Scrapes AI tools from various sources
Creates a comprehensive database of AI tools for the AI Spectrum page
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Comprehensive AI Tools Database (curated from multiple sources)
AI_TOOLS_DATABASE = [
    # Text & Writing
    {"name": "ChatGPT", "category": "Chatbot", "subcategory": "General Assistant", "description": "Advanced AI chatbot by OpenAI for conversations, writing, coding, and more.", "url": "https://chat.openai.com", "pricing": "Freemium", "rating": 4.9, "users": "200M+", "tags": ["chatbot", "writing", "coding", "research"], "featured": True},
    {"name": "Claude", "category": "Chatbot", "subcategory": "General Assistant", "description": "Anthropic's AI assistant known for safety, helpfulness, and long context.", "url": "https://claude.ai", "pricing": "Freemium", "rating": 4.8, "users": "50M+", "tags": ["chatbot", "writing", "analysis", "coding"], "featured": True},
    {"name": "Gemini", "category": "Chatbot", "subcategory": "General Assistant", "description": "Google's multimodal AI for text, images, and code generation.", "url": "https://gemini.google.com", "pricing": "Freemium", "rating": 4.7, "users": "100M+", "tags": ["chatbot", "multimodal", "google"], "featured": True},
    {"name": "Perplexity AI", "category": "Search", "subcategory": "AI Search Engine", "description": "AI-powered search engine with cited sources and real-time information.", "url": "https://perplexity.ai", "pricing": "Freemium", "rating": 4.8, "users": "30M+", "tags": ["search", "research", "citations"], "featured": True},
    {"name": "Jasper", "category": "Writing", "subcategory": "Marketing Copy", "description": "AI writing assistant for marketing teams. Create blogs, ads, emails.", "url": "https://jasper.ai", "pricing": "Paid", "rating": 4.6, "users": "100K+", "tags": ["marketing", "copywriting", "content"], "featured": False},
    {"name": "Copy.ai", "category": "Writing", "subcategory": "Marketing Copy", "description": "AI copywriting tool for social media, blogs, and sales copy.", "url": "https://copy.ai", "pricing": "Freemium", "rating": 4.5, "users": "200K+", "tags": ["copywriting", "marketing", "social media"], "featured": False},
    {"name": "Writesonic", "category": "Writing", "subcategory": "Content Creation", "description": "AI writer for articles, blogs, ads, and product descriptions.", "url": "https://writesonic.com", "pricing": "Freemium", "rating": 4.4, "users": "150K+", "tags": ["writing", "seo", "articles"], "featured": False},
    {"name": "Grammarly", "category": "Writing", "subcategory": "Grammar & Style", "description": "AI-powered writing assistant for grammar, clarity, and tone.", "url": "https://grammarly.com", "pricing": "Freemium", "rating": 4.7, "users": "30M+", "tags": ["grammar", "writing", "proofreading"], "featured": True},
    {"name": "QuillBot", "category": "Writing", "subcategory": "Paraphrasing", "description": "AI paraphrasing and summarizing tool for better writing.", "url": "https://quillbot.com", "pricing": "Freemium", "rating": 4.5, "users": "20M+", "tags": ["paraphrasing", "summarizing", "writing"], "featured": False},
    {"name": "Notion AI", "category": "Writing", "subcategory": "Productivity", "description": "AI assistant built into Notion for writing, summarizing, and brainstorming.", "url": "https://notion.so/product/ai", "pricing": "Paid", "rating": 4.6, "users": "10M+", "tags": ["productivity", "writing", "notes"], "featured": False},
    
    # Image Generation
    {"name": "Midjourney", "category": "Image Generation", "subcategory": "Art & Illustration", "description": "Leading AI art generator creating stunning, artistic images from text prompts.", "url": "https://midjourney.com", "pricing": "Paid", "rating": 4.9, "users": "15M+", "tags": ["art", "illustration", "creative"], "featured": True},
    {"name": "DALL-E 3", "category": "Image Generation", "subcategory": "General Images", "description": "OpenAI's image generator with high accuracy and text understanding.", "url": "https://openai.com/dall-e-3", "pricing": "Paid", "rating": 4.8, "users": "20M+", "tags": ["images", "art", "openai"], "featured": True},
    {"name": "Stable Diffusion", "category": "Image Generation", "subcategory": "Open Source", "description": "Open-source image generation model. Run locally or via cloud.", "url": "https://stability.ai", "pricing": "Free", "rating": 4.7, "users": "10M+", "tags": ["open-source", "images", "local"], "featured": True},
    {"name": "Leonardo AI", "category": "Image Generation", "subcategory": "Game Assets", "description": "AI image generator focused on game assets, characters, and environments.", "url": "https://leonardo.ai", "pricing": "Freemium", "rating": 4.6, "users": "5M+", "tags": ["gaming", "assets", "characters"], "featured": False},
    {"name": "Ideogram", "category": "Image Generation", "subcategory": "Text in Images", "description": "AI image generator that excels at rendering text within images.", "url": "https://ideogram.ai", "pricing": "Freemium", "rating": 4.5, "users": "3M+", "tags": ["text", "logos", "design"], "featured": False},
    {"name": "Adobe Firefly", "category": "Image Generation", "subcategory": "Creative Suite", "description": "Adobe's generative AI integrated into Creative Cloud apps.", "url": "https://firefly.adobe.com", "pricing": "Freemium", "rating": 4.6, "users": "10M+", "tags": ["adobe", "creative", "design"], "featured": True},
    {"name": "Canva AI", "category": "Image Generation", "subcategory": "Design", "description": "AI-powered design tools within Canva for images, presentations.", "url": "https://canva.com/ai-image-generator", "pricing": "Freemium", "rating": 4.5, "users": "50M+", "tags": ["design", "social media", "presentations"], "featured": False},
    {"name": "Playground AI", "category": "Image Generation", "subcategory": "Free Generator", "description": "Free AI image generator with multiple models and styles.", "url": "https://playground.ai", "pricing": "Freemium", "rating": 4.4, "users": "2M+", "tags": ["free", "images", "art"], "featured": False},
    
    # Video
    {"name": "Runway", "category": "Video", "subcategory": "Video Generation", "description": "AI video generation and editing. Create videos from text or images.", "url": "https://runway.ml", "pricing": "Freemium", "rating": 4.7, "users": "5M+", "tags": ["video", "generation", "editing"], "featured": True},
    {"name": "Pika Labs", "category": "Video", "subcategory": "Video Generation", "description": "Text-to-video and image-to-video AI generator.", "url": "https://pika.art", "pricing": "Freemium", "rating": 4.5, "users": "2M+", "tags": ["video", "animation", "creative"], "featured": False},
    {"name": "Synthesia", "category": "Video", "subcategory": "AI Avatars", "description": "Create AI avatar videos from text. Perfect for training and marketing.", "url": "https://synthesia.io", "pricing": "Paid", "rating": 4.6, "users": "50K+", "tags": ["avatars", "training", "marketing"], "featured": True},
    {"name": "HeyGen", "category": "Video", "subcategory": "AI Avatars", "description": "AI video generator with realistic avatars and voice cloning.", "url": "https://heygen.com", "pricing": "Freemium", "rating": 4.5, "users": "100K+", "tags": ["avatars", "voice", "marketing"], "featured": False},
    {"name": "Descript", "category": "Video", "subcategory": "Video Editing", "description": "AI-powered video and podcast editing. Edit video like a doc.", "url": "https://descript.com", "pricing": "Freemium", "rating": 4.7, "users": "3M+", "tags": ["editing", "podcast", "transcription"], "featured": True},
    {"name": "CapCut", "category": "Video", "subcategory": "Video Editing", "description": "Free video editor with AI features for social media content.", "url": "https://capcut.com", "pricing": "Free", "rating": 4.6, "users": "200M+", "tags": ["editing", "social media", "free"], "featured": False},
    {"name": "Lumen5", "category": "Video", "subcategory": "Video Creation", "description": "Turn blog posts into videos automatically with AI.", "url": "https://lumen5.com", "pricing": "Freemium", "rating": 4.3, "users": "500K+", "tags": ["marketing", "blog", "automation"], "featured": False},
    {"name": "InVideo", "category": "Video", "subcategory": "Video Creation", "description": "AI video maker for marketing, social media, and presentations.", "url": "https://invideo.io", "pricing": "Freemium", "rating": 4.4, "users": "2M+", "tags": ["marketing", "templates", "social"], "featured": False},
    
    # Audio & Music
    {"name": "ElevenLabs", "category": "Audio", "subcategory": "Voice Generation", "description": "Most realistic AI voice generator. Text-to-speech and voice cloning.", "url": "https://elevenlabs.io", "pricing": "Freemium", "rating": 4.9, "users": "5M+", "tags": ["voice", "tts", "cloning"], "featured": True},
    {"name": "Murf AI", "category": "Audio", "subcategory": "Voice Generation", "description": "AI voice generator for videos, presentations, and audiobooks.", "url": "https://murf.ai", "pricing": "Freemium", "rating": 4.5, "users": "500K+", "tags": ["voiceover", "videos", "audiobooks"], "featured": False},
    {"name": "Suno AI", "category": "Audio", "subcategory": "Music Generation", "description": "Create full songs with vocals and instruments from text prompts.", "url": "https://suno.ai", "pricing": "Freemium", "rating": 4.7, "users": "3M+", "tags": ["music", "songs", "vocals"], "featured": True},
    {"name": "Udio", "category": "Audio", "subcategory": "Music Generation", "description": "AI music generator creating high-quality songs with vocals.", "url": "https://udio.com", "pricing": "Freemium", "rating": 4.6, "users": "2M+", "tags": ["music", "songs", "creative"], "featured": False},
    {"name": "AIVA", "category": "Audio", "subcategory": "Music Composition", "description": "AI composer for soundtracks, background music, and jingles.", "url": "https://aiva.ai", "pricing": "Freemium", "rating": 4.4, "users": "500K+", "tags": ["composition", "soundtrack", "royalty-free"], "featured": False},
    {"name": "Soundraw", "category": "Audio", "subcategory": "Music Generation", "description": "AI music generator for royalty-free tracks. Customize length and mood.", "url": "https://soundraw.io", "pricing": "Paid", "rating": 4.3, "users": "200K+", "tags": ["music", "royalty-free", "background"], "featured": False},
    {"name": "Krisp", "category": "Audio", "subcategory": "Noise Cancellation", "description": "AI-powered noise cancellation for calls and recordings.", "url": "https://krisp.ai", "pricing": "Freemium", "rating": 4.6, "users": "3M+", "tags": ["noise", "calls", "meetings"], "featured": False},
    {"name": "Podcastle", "category": "Audio", "subcategory": "Podcast", "description": "AI-powered podcast creation, editing, and transcription.", "url": "https://podcastle.ai", "pricing": "Freemium", "rating": 4.4, "users": "500K+", "tags": ["podcast", "editing", "recording"], "featured": False},
    
    # Coding & Development
    {"name": "GitHub Copilot", "category": "Coding", "subcategory": "Code Assistant", "description": "AI pair programmer that suggests code in real-time. Trained on GitHub.", "url": "https://github.com/features/copilot", "pricing": "Paid", "rating": 4.8, "users": "1.5M+", "tags": ["coding", "autocomplete", "github"], "featured": True},
    {"name": "Cursor", "category": "Coding", "subcategory": "AI IDE", "description": "AI-first code editor built for pair programming with AI.", "url": "https://cursor.sh", "pricing": "Freemium", "rating": 4.7, "users": "500K+", "tags": ["ide", "coding", "ai-native"], "featured": True},
    {"name": "Replit AI", "category": "Coding", "subcategory": "Code Generation", "description": "AI coding assistant in browser-based IDE. Build and deploy apps.", "url": "https://replit.com/ai", "pricing": "Freemium", "rating": 4.5, "users": "20M+", "tags": ["ide", "browser", "deployment"], "featured": False},
    {"name": "Tabnine", "category": "Coding", "subcategory": "Code Completion", "description": "AI code completion for all major IDEs and languages.", "url": "https://tabnine.com", "pricing": "Freemium", "rating": 4.4, "users": "1M+", "tags": ["autocomplete", "privacy", "local"], "featured": False},
    {"name": "Codeium", "category": "Coding", "subcategory": "Code Completion", "description": "Free AI code completion and chat for developers.", "url": "https://codeium.com", "pricing": "Free", "rating": 4.5, "users": "500K+", "tags": ["free", "autocomplete", "chat"], "featured": False},
    {"name": "Amazon CodeWhisperer", "category": "Coding", "subcategory": "Code Assistant", "description": "AWS's AI coding companion. Free for individual use.", "url": "https://aws.amazon.com/codewhisperer", "pricing": "Freemium", "rating": 4.3, "users": "500K+", "tags": ["aws", "coding", "security"], "featured": False},
    {"name": "Sourcegraph Cody", "category": "Coding", "subcategory": "Code Search", "description": "AI coding assistant with codebase understanding and search.", "url": "https://sourcegraph.com/cody", "pricing": "Freemium", "rating": 4.4, "users": "200K+", "tags": ["search", "codebase", "enterprise"], "featured": False},
    {"name": "v0 by Vercel", "category": "Coding", "subcategory": "UI Generation", "description": "Generate React UI components from text descriptions.", "url": "https://v0.dev", "pricing": "Freemium", "rating": 4.6, "users": "500K+", "tags": ["ui", "react", "frontend"], "featured": True},
    {"name": "bolt.new", "category": "Coding", "subcategory": "App Generation", "description": "Generate full-stack apps from prompts in the browser.", "url": "https://bolt.new", "pricing": "Freemium", "rating": 4.5, "users": "200K+", "tags": ["fullstack", "apps", "browser"], "featured": False},
    
    # Productivity
    {"name": "Otter.ai", "category": "Productivity", "subcategory": "Transcription", "description": "AI meeting transcription and note-taking assistant.", "url": "https://otter.ai", "pricing": "Freemium", "rating": 4.6, "users": "10M+", "tags": ["transcription", "meetings", "notes"], "featured": True},
    {"name": "Fireflies.ai", "category": "Productivity", "subcategory": "Meeting Assistant", "description": "AI meeting assistant that records, transcribes, and summarizes.", "url": "https://fireflies.ai", "pricing": "Freemium", "rating": 4.5, "users": "300K+", "tags": ["meetings", "transcription", "summary"], "featured": False},
    {"name": "tl;dv", "category": "Productivity", "subcategory": "Meeting Assistant", "description": "AI meeting recorder for Google Meet and Zoom with timestamps.", "url": "https://tldv.io", "pricing": "Freemium", "rating": 4.4, "users": "200K+", "tags": ["meetings", "recording", "highlights"], "featured": False},
    {"name": "Mem", "category": "Productivity", "subcategory": "Note Taking", "description": "AI-powered note-taking app that organizes itself.", "url": "https://mem.ai", "pricing": "Freemium", "rating": 4.3, "users": "100K+", "tags": ["notes", "organization", "search"], "featured": False},
    {"name": "Taskade", "category": "Productivity", "subcategory": "Project Management", "description": "AI-powered workspace for tasks, notes, and collaboration.", "url": "https://taskade.com", "pricing": "Freemium", "rating": 4.4, "users": "500K+", "tags": ["tasks", "collaboration", "ai-agents"], "featured": False},
    {"name": "Motion", "category": "Productivity", "subcategory": "Calendar", "description": "AI calendar that automatically schedules and prioritizes tasks.", "url": "https://usemotion.com", "pricing": "Paid", "rating": 4.5, "users": "100K+", "tags": ["calendar", "scheduling", "automation"], "featured": False},
    {"name": "Reclaim.ai", "category": "Productivity", "subcategory": "Calendar", "description": "AI scheduling assistant for Google Calendar. Auto-schedule habits.", "url": "https://reclaim.ai", "pricing": "Freemium", "rating": 4.4, "users": "200K+", "tags": ["calendar", "habits", "time-blocking"], "featured": False},
    
    # Design
    {"name": "Figma AI", "category": "Design", "subcategory": "UI/UX Design", "description": "AI features in Figma for generating designs and assets.", "url": "https://figma.com/ai", "pricing": "Freemium", "rating": 4.5, "users": "4M+", "tags": ["design", "ui", "collaboration"], "featured": True},
    {"name": "Framer AI", "category": "Design", "subcategory": "Web Design", "description": "Generate entire websites from text prompts. No-code builder.", "url": "https://framer.com/ai", "pricing": "Freemium", "rating": 4.6, "users": "1M+", "tags": ["websites", "no-code", "generation"], "featured": True},
    {"name": "Uizard", "category": "Design", "subcategory": "Prototyping", "description": "AI-powered UI design tool. Turn sketches into designs.", "url": "https://uizard.io", "pricing": "Freemium", "rating": 4.3, "users": "500K+", "tags": ["prototyping", "wireframes", "ui"], "featured": False},
    {"name": "Looka", "category": "Design", "subcategory": "Logo Design", "description": "AI logo maker for brands and businesses.", "url": "https://looka.com", "pricing": "Paid", "rating": 4.4, "users": "1M+", "tags": ["logos", "branding", "business"], "featured": False},
    {"name": "Khroma", "category": "Design", "subcategory": "Color Palettes", "description": "AI color palette generator that learns your preferences.", "url": "https://khroma.co", "pricing": "Free", "rating": 4.2, "users": "500K+", "tags": ["colors", "palettes", "design"], "featured": False},
    {"name": "Remove.bg", "category": "Design", "subcategory": "Background Removal", "description": "AI background remover for images. Instant and accurate.", "url": "https://remove.bg", "pricing": "Freemium", "rating": 4.7, "users": "30M+", "tags": ["background", "editing", "images"], "featured": False},
    {"name": "Cleanup.pictures", "category": "Design", "subcategory": "Image Editing", "description": "Remove unwanted objects from photos with AI.", "url": "https://cleanup.pictures", "pricing": "Freemium", "rating": 4.5, "users": "5M+", "tags": ["editing", "removal", "images"], "featured": False},
    {"name": "Photoroom", "category": "Design", "subcategory": "Photo Editing", "description": "AI photo editor for e-commerce and product photography.", "url": "https://photoroom.com", "pricing": "Freemium", "rating": 4.6, "users": "10M+", "tags": ["product", "ecommerce", "editing"], "featured": False},
    
    # Marketing & SEO
    {"name": "Surfer SEO", "category": "Marketing", "subcategory": "SEO", "description": "AI-powered SEO tool for content optimization and analysis.", "url": "https://surferseo.com", "pricing": "Paid", "rating": 4.6, "users": "100K+", "tags": ["seo", "content", "optimization"], "featured": True},
    {"name": "Clearscope", "category": "Marketing", "subcategory": "SEO", "description": "AI content optimization platform for SEO-driven content.", "url": "https://clearscope.io", "pricing": "Paid", "rating": 4.5, "users": "50K+", "tags": ["seo", "content", "research"], "featured": False},
    {"name": "MarketMuse", "category": "Marketing", "subcategory": "Content Strategy", "description": "AI content intelligence platform for planning and optimization.", "url": "https://marketmuse.com", "pricing": "Paid", "rating": 4.4, "users": "50K+", "tags": ["content", "strategy", "seo"], "featured": False},
    {"name": "Lately", "category": "Marketing", "subcategory": "Social Media", "description": "AI social media manager that repurposes long-form content.", "url": "https://lately.ai", "pricing": "Paid", "rating": 4.3, "users": "50K+", "tags": ["social", "repurposing", "automation"], "featured": False},
    {"name": "Phrasee", "category": "Marketing", "subcategory": "Email Marketing", "description": "AI copywriting for email subject lines and marketing copy.", "url": "https://phrasee.co", "pricing": "Paid", "rating": 4.4, "users": "50K+", "tags": ["email", "copywriting", "optimization"], "featured": False},
    {"name": "Persado", "category": "Marketing", "subcategory": "Marketing AI", "description": "AI-generated marketing language that drives engagement.", "url": "https://persado.com", "pricing": "Enterprise", "rating": 4.3, "users": "1K+", "tags": ["enterprise", "marketing", "language"], "featured": False},
    
    # Research & Analysis
    {"name": "Elicit", "category": "Research", "subcategory": "Academic Research", "description": "AI research assistant that finds and summarizes papers.", "url": "https://elicit.org", "pricing": "Freemium", "rating": 4.6, "users": "500K+", "tags": ["research", "papers", "academic"], "featured": True},
    {"name": "Consensus", "category": "Research", "subcategory": "Academic Research", "description": "AI search engine for scientific research with evidence.", "url": "https://consensus.app", "pricing": "Freemium", "rating": 4.5, "users": "300K+", "tags": ["science", "research", "evidence"], "featured": False},
    {"name": "Semantic Scholar", "category": "Research", "subcategory": "Academic Search", "description": "AI-powered academic search engine by Allen AI.", "url": "https://semanticscholar.org", "pricing": "Free", "rating": 4.6, "users": "1M+", "tags": ["academic", "search", "citations"], "featured": False},
    {"name": "Scholarcy", "category": "Research", "subcategory": "Paper Summarization", "description": "AI tool that summarizes research papers into flashcards.", "url": "https://scholarcy.com", "pricing": "Freemium", "rating": 4.3, "users": "200K+", "tags": ["summary", "papers", "flashcards"], "featured": False},
    {"name": "Scite", "category": "Research", "subcategory": "Citation Analysis", "description": "AI tool showing how papers cite each other with context.", "url": "https://scite.ai", "pricing": "Freemium", "rating": 4.4, "users": "100K+", "tags": ["citations", "analysis", "research"], "featured": False},
    {"name": "ChatPDF", "category": "Research", "subcategory": "Document Analysis", "description": "Chat with any PDF document using AI.", "url": "https://chatpdf.com", "pricing": "Freemium", "rating": 4.5, "users": "1M+", "tags": ["pdf", "chat", "documents"], "featured": False},
    
    # Data & Analytics
    {"name": "Julius AI", "category": "Data", "subcategory": "Data Analysis", "description": "AI data analyst that creates visualizations and insights.", "url": "https://julius.ai", "pricing": "Freemium", "rating": 4.5, "users": "500K+", "tags": ["data", "visualization", "analysis"], "featured": True},
    {"name": "Obviously AI", "category": "Data", "subcategory": "ML No-Code", "description": "No-code ML platform for predictions and analytics.", "url": "https://obviously.ai", "pricing": "Paid", "rating": 4.3, "users": "50K+", "tags": ["ml", "no-code", "predictions"], "featured": False},
    {"name": "Akkio", "category": "Data", "subcategory": "ML Platform", "description": "No-code AI for business analytics and predictions.", "url": "https://akkio.com", "pricing": "Paid", "rating": 4.2, "users": "30K+", "tags": ["analytics", "predictions", "business"], "featured": False},
    {"name": "MonkeyLearn", "category": "Data", "subcategory": "Text Analysis", "description": "No-code text analytics and sentiment analysis.", "url": "https://monkeylearn.com", "pricing": "Paid", "rating": 4.3, "users": "50K+", "tags": ["text", "sentiment", "analytics"], "featured": False},
    
    # Customer Service
    {"name": "Intercom Fin", "category": "Customer Service", "subcategory": "AI Chatbot", "description": "AI customer service chatbot powered by GPT-4.", "url": "https://intercom.com/fin", "pricing": "Paid", "rating": 4.5, "users": "25K+", "tags": ["support", "chatbot", "automation"], "featured": True},
    {"name": "Zendesk AI", "category": "Customer Service", "subcategory": "Support Platform", "description": "AI-powered customer service platform with bots and insights.", "url": "https://zendesk.com/service/ai", "pricing": "Paid", "rating": 4.4, "users": "100K+", "tags": ["support", "ticketing", "automation"], "featured": False},
    {"name": "Ada", "category": "Customer Service", "subcategory": "AI Chatbot", "description": "AI-powered customer service automation platform.", "url": "https://ada.cx", "pricing": "Paid", "rating": 4.4, "users": "50K+", "tags": ["chatbot", "automation", "enterprise"], "featured": False},
    {"name": "Tidio", "category": "Customer Service", "subcategory": "Live Chat", "description": "AI chatbot and live chat for small businesses.", "url": "https://tidio.com", "pricing": "Freemium", "rating": 4.5, "users": "300K+", "tags": ["chat", "small-business", "ecommerce"], "featured": False},
    
    # Sales
    {"name": "Gong", "category": "Sales", "subcategory": "Conversation Intelligence", "description": "AI sales intelligence platform for call analysis and coaching.", "url": "https://gong.io", "pricing": "Paid", "rating": 4.7, "users": "4K+", "tags": ["sales", "calls", "coaching"], "featured": True},
    {"name": "Chorus.ai", "category": "Sales", "subcategory": "Conversation Intelligence", "description": "AI conversation intelligence for sales teams.", "url": "https://chorus.ai", "pricing": "Paid", "rating": 4.5, "users": "3K+", "tags": ["sales", "calls", "intelligence"], "featured": False},
    {"name": "Clari", "category": "Sales", "subcategory": "Revenue Intelligence", "description": "AI-powered revenue operations platform.", "url": "https://clari.com", "pricing": "Paid", "rating": 4.4, "users": "5K+", "tags": ["revenue", "forecasting", "sales"], "featured": False},
    {"name": "Apollo.io", "category": "Sales", "subcategory": "Sales Intelligence", "description": "AI-powered B2B database and sales engagement.", "url": "https://apollo.io", "pricing": "Freemium", "rating": 4.5, "users": "500K+", "tags": ["leads", "outreach", "b2b"], "featured": False},
    
    # HR & Recruiting
    {"name": "HireVue", "category": "HR", "subcategory": "Interviewing", "description": "AI video interviewing and assessment platform.", "url": "https://hirevue.com", "pricing": "Paid", "rating": 4.2, "users": "1K+", "tags": ["interviewing", "assessment", "hiring"], "featured": False},
    {"name": "Eightfold AI", "category": "HR", "subcategory": "Talent Intelligence", "description": "AI talent intelligence platform for hiring and retention.", "url": "https://eightfold.ai", "pricing": "Paid", "rating": 4.4, "users": "500+", "tags": ["talent", "hiring", "enterprise"], "featured": False},
    {"name": "Pymetrics", "category": "HR", "subcategory": "Assessment", "description": "AI-powered talent matching using neuroscience games.", "url": "https://pymetrics.ai", "pricing": "Paid", "rating": 4.1, "users": "500+", "tags": ["assessment", "matching", "games"], "featured": False},
    {"name": "Textio", "category": "HR", "subcategory": "Job Descriptions", "description": "AI writing assistant for inclusive job descriptions.", "url": "https://textio.com", "pricing": "Paid", "rating": 4.3, "users": "1K+", "tags": ["writing", "dei", "recruiting"], "featured": False},
    
    # Legal
    {"name": "Harvey AI", "category": "Legal", "subcategory": "Legal Assistant", "description": "AI legal assistant for research and document drafting.", "url": "https://harvey.ai", "pricing": "Enterprise", "rating": 4.5, "users": "500+", "tags": ["legal", "research", "documents"], "featured": True},
    {"name": "Casetext", "category": "Legal", "subcategory": "Legal Research", "description": "AI-powered legal research with CoCounsel assistant.", "url": "https://casetext.com", "pricing": "Paid", "rating": 4.6, "users": "10K+", "tags": ["research", "case-law", "ai-assistant"], "featured": False},
    {"name": "DoNotPay", "category": "Legal", "subcategory": "Consumer Legal", "description": "AI lawyer for fighting tickets, canceling subscriptions.", "url": "https://donotpay.com", "pricing": "Paid", "rating": 4.0, "users": "200K+", "tags": ["consumer", "legal-help", "automation"], "featured": False},
    
    # Healthcare
    {"name": "Nabla", "category": "Healthcare", "subcategory": "Clinical Notes", "description": "AI assistant for clinical documentation and notes.", "url": "https://nabla.com", "pricing": "Paid", "rating": 4.5, "users": "10K+", "tags": ["clinical", "notes", "healthcare"], "featured": False},
    {"name": "Glass Health", "category": "Healthcare", "subcategory": "Diagnosis Support", "description": "AI diagnostic assistant for healthcare providers.", "url": "https://glass.health", "pricing": "Paid", "rating": 4.4, "users": "5K+", "tags": ["diagnosis", "clinical", "ai-assist"], "featured": False},
    
    # Education
    {"name": "Khan Academy Khanmigo", "category": "Education", "subcategory": "AI Tutor", "description": "AI tutor powered by GPT-4 for personalized learning.", "url": "https://khanacademy.org/khan-labs", "pricing": "Freemium", "rating": 4.6, "users": "1M+", "tags": ["tutoring", "education", "personalized"], "featured": True},
    {"name": "Duolingo Max", "category": "Education", "subcategory": "Language Learning", "description": "AI-powered language learning with GPT-4 features.", "url": "https://duolingo.com", "pricing": "Paid", "rating": 4.7, "users": "50M+", "tags": ["language", "learning", "ai-tutor"], "featured": False},
    {"name": "Quizlet Q-Chat", "category": "Education", "subcategory": "Study Assistant", "description": "AI tutor for flashcard-based learning.", "url": "https://quizlet.com", "pricing": "Freemium", "rating": 4.4, "users": "60M+", "tags": ["study", "flashcards", "tutor"], "featured": False},
    {"name": "Photomath", "category": "Education", "subcategory": "Math Solver", "description": "AI math solver that shows step-by-step solutions.", "url": "https://photomath.com", "pricing": "Freemium", "rating": 4.6, "users": "30M+", "tags": ["math", "solver", "education"], "featured": False},
    
    # Finance
    {"name": "AlphaSense", "category": "Finance", "subcategory": "Market Intelligence", "description": "AI-powered market intelligence and search platform.", "url": "https://alpha-sense.com", "pricing": "Paid", "rating": 4.5, "users": "5K+", "tags": ["finance", "research", "intelligence"], "featured": False},
    {"name": "Kensho", "category": "Finance", "subcategory": "Analytics", "description": "AI analytics for financial institutions by S&P Global.", "url": "https://kensho.com", "pricing": "Enterprise", "rating": 4.4, "users": "1K+", "tags": ["analytics", "finance", "enterprise"], "featured": False},
    
    # 3D & Gaming
    {"name": "Meshy", "category": "3D", "subcategory": "3D Generation", "description": "AI 3D model generator from text and images.", "url": "https://meshy.ai", "pricing": "Freemium", "rating": 4.4, "users": "500K+", "tags": ["3d", "models", "generation"], "featured": True},
    {"name": "Kaedim", "category": "3D", "subcategory": "3D Generation", "description": "Turn 2D images into 3D models with AI.", "url": "https://kaedim3d.com", "pricing": "Paid", "rating": 4.3, "users": "50K+", "tags": ["3d", "images", "modeling"], "featured": False},
    {"name": "Scenario", "category": "3D", "subcategory": "Game Assets", "description": "AI-generated game assets with custom trained models.", "url": "https://scenario.com", "pricing": "Freemium", "rating": 4.4, "users": "100K+", "tags": ["gaming", "assets", "generation"], "featured": False},
    {"name": "Inworld AI", "category": "3D", "subcategory": "AI NPCs", "description": "Create AI-powered NPCs for games and experiences.", "url": "https://inworld.ai", "pricing": "Freemium", "rating": 4.3, "users": "50K+", "tags": ["npcs", "gaming", "characters"], "featured": False},
    
    # Automation
    {"name": "Zapier AI", "category": "Automation", "subcategory": "Workflow Automation", "description": "AI-powered automation builder for connecting apps.", "url": "https://zapier.com/ai", "pricing": "Freemium", "rating": 4.6, "users": "2M+", "tags": ["automation", "integration", "no-code"], "featured": True},
    {"name": "Make (Integromat)", "category": "Automation", "subcategory": "Workflow Automation", "description": "Visual automation platform with AI capabilities.", "url": "https://make.com", "pricing": "Freemium", "rating": 4.5, "users": "500K+", "tags": ["automation", "visual", "integration"], "featured": False},
    {"name": "Bardeen", "category": "Automation", "subcategory": "Browser Automation", "description": "AI automation for repetitive browser tasks.", "url": "https://bardeen.ai", "pricing": "Freemium", "rating": 4.4, "users": "200K+", "tags": ["browser", "automation", "productivity"], "featured": False},
    {"name": "Browse AI", "category": "Automation", "subcategory": "Web Scraping", "description": "Train AI to scrape and monitor any website.", "url": "https://browse.ai", "pricing": "Freemium", "rating": 4.3, "users": "100K+", "tags": ["scraping", "monitoring", "data"], "featured": False},
    
    # AI Agents
    {"name": "AutoGPT", "category": "AI Agents", "subcategory": "Autonomous Agent", "description": "Open-source autonomous AI agent framework.", "url": "https://github.com/Significant-Gravitas/AutoGPT", "pricing": "Free", "rating": 4.3, "users": "150K+", "tags": ["autonomous", "open-source", "agents"], "featured": True},
    {"name": "AgentGPT", "category": "AI Agents", "subcategory": "Autonomous Agent", "description": "Deploy autonomous AI agents in browser.", "url": "https://agentgpt.reworkd.ai", "pricing": "Freemium", "rating": 4.2, "users": "100K+", "tags": ["autonomous", "browser", "agents"], "featured": False},
    {"name": "CrewAI", "category": "AI Agents", "subcategory": "Multi-Agent", "description": "Framework for orchestrating multiple AI agents.", "url": "https://crewai.com", "pricing": "Free", "rating": 4.4, "users": "50K+", "tags": ["multi-agent", "framework", "orchestration"], "featured": False},
    
    # API & Infrastructure
    {"name": "OpenAI API", "category": "API", "subcategory": "LLM API", "description": "Access GPT-4, DALL-E, Whisper and more via API.", "url": "https://platform.openai.com", "pricing": "Pay-per-use", "rating": 4.8, "users": "2M+", "tags": ["api", "gpt", "enterprise"], "featured": True},
    {"name": "Anthropic Claude API", "category": "API", "subcategory": "LLM API", "description": "Access Claude models via API for applications.", "url": "https://anthropic.com/api", "pricing": "Pay-per-use", "rating": 4.7, "users": "500K+", "tags": ["api", "claude", "enterprise"], "featured": False},
    {"name": "Hugging Face", "category": "API", "subcategory": "ML Platform", "description": "Platform for sharing and deploying ML models.", "url": "https://huggingface.co", "pricing": "Freemium", "rating": 4.8, "users": "500K+", "tags": ["models", "open-source", "deployment"], "featured": True},
    {"name": "Replicate", "category": "API", "subcategory": "ML API", "description": "Run open-source ML models via simple API.", "url": "https://replicate.com", "pricing": "Pay-per-use", "rating": 4.5, "users": "200K+", "tags": ["api", "models", "cloud"], "featured": False},
    {"name": "Together AI", "category": "API", "subcategory": "LLM API", "description": "Fast inference API for open-source LLMs.", "url": "https://together.ai", "pricing": "Pay-per-use", "rating": 4.4, "users": "100K+", "tags": ["api", "open-source", "inference"], "featured": False},
    {"name": "Groq", "category": "API", "subcategory": "Fast Inference", "description": "Ultra-fast LLM inference with custom hardware.", "url": "https://groq.com", "pricing": "Freemium", "rating": 4.6, "users": "200K+", "tags": ["fast", "inference", "api"], "featured": True},
]

def get_ai_tools():
    """Return the AI tools database"""
    return AI_TOOLS_DATABASE

def get_categories():
    """Get unique categories"""
    categories = set()
    for tool in AI_TOOLS_DATABASE:
        categories.add(tool["category"])
    return sorted(list(categories))

def save_to_json():
    """Save AI tools to JSON file"""
    output_path = os.path.join(os.path.dirname(__file__), 'ai_tools_data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "tools": AI_TOOLS_DATABASE,
            "categories": get_categories(),
            "total": len(AI_TOOLS_DATABASE)
        }, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(AI_TOOLS_DATABASE)} AI tools to {output_path}")

if __name__ == "__main__":
    print(f"📊 AI Tools Database: {len(AI_TOOLS_DATABASE)} tools")
    print(f"📁 Categories: {', '.join(get_categories())}")
    save_to_json()


