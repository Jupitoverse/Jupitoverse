// AI Tools Database - Phase 10: Image, Video & Audio Generation AI
// 200+ Tools for multimedia creation

const AI_TOOLS_PHASE10 = [
    // ==================== IMAGE GENERATION ====================
    {name: "Midjourney", category: "Image Generation", subcategory: "Art", desc: "AI art generation via Discord", url: "midjourney.com", pricing: "Paid", rating: 4.8, tags: ["art", "discord", "quality"], featured: true},
    {name: "DALL-E 3", category: "Image Generation", subcategory: "OpenAI", desc: "OpenAI's image generation", url: "openai.com/dall-e-3", pricing: "Paid", rating: 4.7, tags: ["openai", "chatgpt", "realistic"]},
    {name: "Stable Diffusion", category: "Image Generation", subcategory: "Open Source", desc: "Open-source image generation", url: "stability.ai", pricing: "Freemium", rating: 4.6, tags: ["open-source", "local", "customizable"], featured: true},
    {name: "Leonardo.ai", category: "Image Generation", subcategory: "Art", desc: "AI image generation platform", url: "leonardo.ai", pricing: "Freemium", rating: 4.6, tags: ["gaming", "assets", "control"]},
    {name: "Firefly", category: "Image Generation", subcategory: "Adobe", desc: "Adobe's generative AI", url: "adobe.com/firefly", pricing: "Freemium", rating: 4.5, tags: ["adobe", "commercial", "safe"]},
    {name: "Ideogram", category: "Image Generation", subcategory: "Text", desc: "AI image with text generation", url: "ideogram.ai", pricing: "Freemium", rating: 4.5, tags: ["text", "logos", "typography"]},
    {name: "Playground AI", category: "Image Generation", subcategory: "Free", desc: "Free AI image creation", url: "playgroundai.com", pricing: "Freemium", rating: 4.4, tags: ["free", "easy", "community"]},
    {name: "NightCafe", category: "Image Generation", subcategory: "Art", desc: "AI art generator", url: "nightcafe.studio", pricing: "Freemium", rating: 4.3, tags: ["art", "community", "styles"]},
    {name: "Lexica", category: "Image Generation", subcategory: "Search", desc: "Stable Diffusion search engine", url: "lexica.art", pricing: "Freemium", rating: 4.3, tags: ["search", "prompts", "stable-diffusion"]},
    {name: "DreamStudio", category: "Image Generation", subcategory: "Stability", desc: "Stability AI's official app", url: "dreamstudio.ai", pricing: "Paid", rating: 4.4, tags: ["stability", "official", "api"]},
    {name: "Craiyon", category: "Image Generation", subcategory: "Free", desc: "Free AI image generator (DALL-E mini)", url: "craiyon.com", pricing: "Free", rating: 3.8, tags: ["free", "dalle-mini", "fun"]},
    {name: "Deep Dream Generator", category: "Image Generation", subcategory: "Art", desc: "Neural network art", url: "deepdreamgenerator.com", pricing: "Freemium", rating: 4.0, tags: ["neural", "psychedelic", "art"]},
    {name: "Artbreeder", category: "Image Generation", subcategory: "Breeding", desc: "Collaborative image breeding", url: "artbreeder.com", pricing: "Freemium", rating: 4.2, tags: ["collaborative", "portraits", "mixing"]},
    {name: "StarryAI", category: "Image Generation", subcategory: "Mobile", desc: "AI art generator app", url: "starryai.com", pricing: "Freemium", rating: 4.1, tags: ["mobile", "nft", "ownership"]},
    {name: "Genmo", category: "Image Generation", subcategory: "Creative", desc: "Creative AI platform", url: "genmo.ai", pricing: "Freemium", rating: 4.2, tags: ["video", "creative", "experimental"]},
    {name: "BlueWillow", category: "Image Generation", subcategory: "Free", desc: "Free AI image generation", url: "bluewillow.ai", pricing: "Free", rating: 4.0, tags: ["free", "discord", "alternative"]},
    {name: "Mage.space", category: "Image Generation", subcategory: "Free", desc: "Free stable diffusion", url: "mage.space", pricing: "Freemium", rating: 4.1, tags: ["free", "fast", "unfiltered"]},
    {name: "Dezgo", category: "Image Generation", subcategory: "Free", desc: "Free text-to-image AI", url: "dezgo.com", pricing: "Free", rating: 4.0, tags: ["free", "fast", "simple"]},
    {name: "Photosonic", category: "Image Generation", subcategory: "Writesonic", desc: "AI image by Writesonic", url: "writesonic.com/photosonic", pricing: "Freemium", rating: 4.0, tags: ["writesonic", "fast", "integration"]},
    {name: "Pixlr AI", category: "Image Generation", subcategory: "Editor", desc: "AI-powered image editing", url: "pixlr.com", pricing: "Freemium", rating: 4.2, tags: ["editor", "effects", "browser"]},
    
    // ==================== IMAGE EDITING & ENHANCEMENT ====================
    {name: "Remove.bg", category: "Image Editing", subcategory: "Background", desc: "AI background removal", url: "remove.bg", pricing: "Freemium", rating: 4.7, tags: ["background", "removal", "fast"], featured: true},
    {name: "Cleanup.pictures", category: "Image Editing", subcategory: "Cleanup", desc: "Remove objects from images", url: "cleanup.pictures", pricing: "Freemium", rating: 4.5, tags: ["cleanup", "remove", "inpainting"]},
    {name: "Clipdrop", category: "Image Editing", subcategory: "Suite", desc: "AI image tools by Stability", url: "clipdrop.co", pricing: "Freemium", rating: 4.5, tags: ["stability", "suite", "tools"]},
    {name: "Photoroom", category: "Image Editing", subcategory: "Background", desc: "AI photo editor", url: "photoroom.com", pricing: "Freemium", rating: 4.6, tags: ["background", "product", "mobile"]},
    {name: "Topaz Labs", category: "Image Editing", subcategory: "Enhancement", desc: "AI image enhancement suite", url: "topazlabs.com", pricing: "Paid", rating: 4.6, tags: ["enhancement", "upscaling", "professional"]},
    {name: "Let's Enhance", category: "Image Editing", subcategory: "Upscaling", desc: "AI image upscaler", url: "letsenhance.io", pricing: "Freemium", rating: 4.4, tags: ["upscaling", "enhancement", "quality"]},
    {name: "Gigapixel AI", category: "Image Editing", subcategory: "Upscaling", desc: "AI upscaling by Topaz", url: "topazlabs.com/gigapixel", pricing: "Paid", rating: 4.6, tags: ["upscaling", "topaz", "detail"]},
    {name: "Remini", category: "Image Editing", subcategory: "Enhancement", desc: "AI photo enhancer", url: "remini.ai", pricing: "Freemium", rating: 4.4, tags: ["enhancement", "mobile", "restoration"]},
    {name: "Luminar Neo", category: "Image Editing", subcategory: "Editor", desc: "AI photo editor by Skylum", url: "skylum.com/luminar", pricing: "Paid", rating: 4.4, tags: ["editor", "professional", "plugins"]},
    {name: "ON1 Photo RAW", category: "Image Editing", subcategory: "Editor", desc: "AI photo editing software", url: "on1.com", pricing: "Paid", rating: 4.3, tags: ["raw", "editing", "ai"]},
    {name: "Perfectly Clear", category: "Image Editing", subcategory: "Correction", desc: "AI photo correction", url: "eyeq.photos", pricing: "Paid", rating: 4.2, tags: ["correction", "automatic", "batch"]},
    {name: "VanceAI", category: "Image Editing", subcategory: "Suite", desc: "AI image processing tools", url: "vanceai.com", pricing: "Freemium", rating: 4.2, tags: ["suite", "processing", "tools"]},
    {name: "Deep Image", category: "Image Editing", subcategory: "Upscaling", desc: "AI image upscaler", url: "deep-image.ai", pricing: "Freemium", rating: 4.1, tags: ["upscaling", "api", "batch"]},
    {name: "Pixelcut", category: "Image Editing", subcategory: "Product", desc: "AI product photo editor", url: "pixelcut.ai", pricing: "Freemium", rating: 4.3, tags: ["product", "ecommerce", "mobile"]},
    {name: "Fotor AI", category: "Image Editing", subcategory: "Editor", desc: "AI photo editor", url: "fotor.com", pricing: "Freemium", rating: 4.2, tags: ["editor", "effects", "collage"]},
    
    // ==================== VIDEO GENERATION ====================
    {name: "Runway Gen-2", category: "Video Generation", subcategory: "Text-to-Video", desc: "AI video generation", url: "runwayml.com", pricing: "Freemium", rating: 4.6, tags: ["video", "text-to-video", "professional"], featured: true},
    {name: "Pika Labs", category: "Video Generation", subcategory: "Text-to-Video", desc: "AI video creation", url: "pika.art", pricing: "Freemium", rating: 4.5, tags: ["video", "animation", "creative"]},
    {name: "Sora", category: "Video Generation", subcategory: "OpenAI", desc: "OpenAI's video generation", url: "openai.com/sora", pricing: "Paid", rating: 4.8, tags: ["openai", "realistic", "long-form"], featured: true},
    {name: "Synthesia", category: "Video Generation", subcategory: "Avatar", desc: "AI avatar video creation", url: "synthesia.io", pricing: "Paid", rating: 4.5, tags: ["avatar", "training", "corporate"]},
    {name: "HeyGen", category: "Video Generation", subcategory: "Avatar", desc: "AI video avatars", url: "heygen.com", pricing: "Freemium", rating: 4.5, tags: ["avatar", "spokesperson", "translation"]},
    {name: "D-ID", category: "Video Generation", subcategory: "Avatar", desc: "AI video platform", url: "d-id.com", pricing: "Freemium", rating: 4.4, tags: ["avatar", "talking-head", "api"]},
    {name: "Colossyan", category: "Video Generation", subcategory: "Corporate", desc: "AI video for learning", url: "colossyan.com", pricing: "Paid", rating: 4.4, tags: ["learning", "corporate", "multilingual"]},
    {name: "Elai.io", category: "Video Generation", subcategory: "Avatar", desc: "AI video generation platform", url: "elai.io", pricing: "Paid", rating: 4.3, tags: ["avatar", "presenter", "ppt"]},
    {name: "Hour One", category: "Video Generation", subcategory: "Avatar", desc: "AI virtual human videos", url: "hourone.ai", pricing: "Paid", rating: 4.3, tags: ["avatar", "enterprise", "characters"]},
    {name: "Fliki", category: "Video Generation", subcategory: "Text-to-Video", desc: "Text to video with AI", url: "fliki.ai", pricing: "Freemium", rating: 4.4, tags: ["text-to-video", "voiceover", "easy"]},
    {name: "InVideo AI", category: "Video Generation", subcategory: "Text-to-Video", desc: "AI video creation", url: "invideo.io/ai", pricing: "Freemium", rating: 4.3, tags: ["text-to-video", "templates", "social"]},
    {name: "Pictory", category: "Video Generation", subcategory: "Text-to-Video", desc: "AI video from text", url: "pictory.ai", pricing: "Paid", rating: 4.3, tags: ["blog-to-video", "repurposing", "editing"]},
    {name: "Lumen5", category: "Video Generation", subcategory: "Marketing", desc: "AI video for marketing", url: "lumen5.com", pricing: "Freemium", rating: 4.3, tags: ["marketing", "social", "blog-to-video"]},
    {name: "Vidnoz", category: "Video Generation", subcategory: "Avatar", desc: "Free AI video generator", url: "vidnoz.com", pricing: "Freemium", rating: 4.2, tags: ["free", "avatar", "tools"]},
    {name: "Deepbrain AI", category: "Video Generation", subcategory: "Avatar", desc: "AI avatar video platform", url: "deepbrain.io", pricing: "Paid", rating: 4.3, tags: ["avatar", "realistic", "studio"]},
    
    // ==================== VIDEO EDITING ====================
    {name: "Runway", category: "Video Editing", subcategory: "AI Editing", desc: "AI video editing tools", url: "runwayml.com", pricing: "Freemium", rating: 4.6, tags: ["editing", "ai", "professional"], featured: true},
    {name: "Descript", category: "Video Editing", subcategory: "Text-Based", desc: "Edit video like a doc", url: "descript.com", pricing: "Freemium", rating: 4.6, tags: ["text-based", "transcription", "podcasts"]},
    {name: "Kapwing", category: "Video Editing", subcategory: "Browser", desc: "Online video editor", url: "kapwing.com", pricing: "Freemium", rating: 4.4, tags: ["browser", "collaborative", "subtitles"]},
    {name: "Opus Clip", category: "Video Editing", subcategory: "Clips", desc: "AI short video generator", url: "opus.pro", pricing: "Freemium", rating: 4.5, tags: ["clips", "shorts", "repurposing"]},
    {name: "Captions", category: "Video Editing", subcategory: "Captions", desc: "AI video captions and editing", url: "captions.ai", pricing: "Freemium", rating: 4.5, tags: ["captions", "subtitles", "mobile"]},
    {name: "VEED.io", category: "Video Editing", subcategory: "Browser", desc: "Online video editing", url: "veed.io", pricing: "Freemium", rating: 4.4, tags: ["browser", "subtitles", "easy"]},
    {name: "Wondershare Filmora", category: "Video Editing", subcategory: "Desktop", desc: "AI video editing software", url: "filmora.wondershare.com", pricing: "Freemium", rating: 4.4, tags: ["desktop", "effects", "beginner"]},
    {name: "CapCut", category: "Video Editing", subcategory: "Mobile", desc: "Free video editor by ByteDance", url: "capcut.com", pricing: "Freemium", rating: 4.5, tags: ["free", "mobile", "tiktok"]},
    {name: "Magisto", category: "Video Editing", subcategory: "Automated", desc: "AI video editing", url: "magisto.com", pricing: "Paid", rating: 4.0, tags: ["automated", "business", "vimeo"]},
    {name: "Wisecut", category: "Video Editing", subcategory: "Automated", desc: "AI video editor", url: "wisecut.video", pricing: "Freemium", rating: 4.2, tags: ["automated", "jump-cuts", "music"]},
    {name: "Topaz Video AI", category: "Video Editing", subcategory: "Enhancement", desc: "AI video upscaling", url: "topazlabs.com/topaz-video-ai", pricing: "Paid", rating: 4.6, tags: ["upscaling", "enhancement", "frame"]},
    {name: "Gling", category: "Video Editing", subcategory: "YouTube", desc: "AI editing for YouTubers", url: "gling.ai", pricing: "Paid", rating: 4.3, tags: ["youtube", "cuts", "silence-removal"]},
    {name: "AutoPod", category: "Video Editing", subcategory: "Podcast", desc: "AI podcast editing for Premiere", url: "autopod.fm", pricing: "Paid", rating: 4.4, tags: ["podcast", "premiere", "multi-cam"]},
    {name: "Vizard", category: "Video Editing", subcategory: "Clips", desc: "AI video clips and repurposing", url: "vizard.ai", pricing: "Freemium", rating: 4.3, tags: ["clips", "repurposing", "social"]},
    {name: "Munch", category: "Video Editing", subcategory: "Clips", desc: "AI content repurposing", url: "getmunch.com", pricing: "Paid", rating: 4.2, tags: ["clips", "social", "analytics"]},
    
    // ==================== AUDIO GENERATION ====================
    {name: "ElevenLabs", category: "Audio", subcategory: "Voice Synthesis", desc: "AI voice synthesis", url: "elevenlabs.io", pricing: "Freemium", rating: 4.7, tags: ["voice", "realistic", "cloning"], featured: true},
    {name: "Murf AI", category: "Audio", subcategory: "Voice", desc: "AI voice generator", url: "murf.ai", pricing: "Freemium", rating: 4.5, tags: ["voiceover", "studio", "commercial"]},
    {name: "Play.ht", category: "Audio", subcategory: "Voice", desc: "AI text-to-speech", url: "play.ht", pricing: "Freemium", rating: 4.4, tags: ["tts", "voices", "podcasts"]},
    {name: "Resemble AI", category: "Audio", subcategory: "Voice Cloning", desc: "AI voice cloning", url: "resemble.ai", pricing: "Paid", rating: 4.4, tags: ["cloning", "api", "enterprise"]},
    {name: "Speechify", category: "Audio", subcategory: "TTS", desc: "Text-to-speech app", url: "speechify.com", pricing: "Freemium", rating: 4.5, tags: ["tts", "reading", "accessibility"]},
    {name: "Descript Overdub", category: "Audio", subcategory: "Voice Cloning", desc: "AI voice for editing", url: "descript.com/overdub", pricing: "Paid", rating: 4.4, tags: ["editing", "cloning", "podcast"]},
    {name: "Wellsaid Labs", category: "Audio", subcategory: "Voice", desc: "AI voice for enterprise", url: "wellsaidlabs.com", pricing: "Paid", rating: 4.4, tags: ["enterprise", "studio", "commercial"]},
    {name: "Listnr", category: "Audio", subcategory: "TTS", desc: "AI text-to-speech", url: "listnr.tech", pricing: "Freemium", rating: 4.2, tags: ["tts", "podcasts", "voices"]},
    {name: "Voicemod", category: "Audio", subcategory: "Voice Changer", desc: "Real-time voice changer", url: "voicemod.net", pricing: "Freemium", rating: 4.3, tags: ["voice-changer", "gaming", "streaming"]},
    {name: "FakeYou", category: "Audio", subcategory: "Voice", desc: "Deep fake voice generator", url: "fakeyou.com", pricing: "Freemium", rating: 4.0, tags: ["celebrities", "characters", "fun"]},
    
    // ==================== MUSIC & SOUND ====================
    {name: "Suno AI", category: "Music", subcategory: "Generation", desc: "AI music generation", url: "suno.ai", pricing: "Freemium", rating: 4.6, tags: ["music", "songs", "vocals"], featured: true},
    {name: "Udio", category: "Music", subcategory: "Generation", desc: "AI music creation", url: "udio.com", pricing: "Freemium", rating: 4.5, tags: ["music", "realistic", "genres"]},
    {name: "AIVA", category: "Music", subcategory: "Composition", desc: "AI music composer", url: "aiva.ai", pricing: "Freemium", rating: 4.4, tags: ["composition", "classical", "orchestral"]},
    {name: "Soundraw", category: "Music", subcategory: "Generation", desc: "AI music for creators", url: "soundraw.io", pricing: "Paid", rating: 4.4, tags: ["royalty-free", "customizable", "youtube"]},
    {name: "Mubert", category: "Music", subcategory: "Generation", desc: "AI generative music", url: "mubert.com", pricing: "Freemium", rating: 4.2, tags: ["generative", "ambient", "streams"]},
    {name: "Boomy", category: "Music", subcategory: "Creation", desc: "Create music with AI", url: "boomy.com", pricing: "Freemium", rating: 4.1, tags: ["creation", "release", "easy"]},
    {name: "Amper Music", category: "Music", subcategory: "Composition", desc: "AI music composition", url: "ampermusic.com", pricing: "Paid", rating: 4.2, tags: ["composition", "shutterstock", "enterprise"]},
    {name: "Beatoven.ai", category: "Music", subcategory: "Background", desc: "AI music for video", url: "beatoven.ai", pricing: "Freemium", rating: 4.2, tags: ["background", "video", "mood"]},
    {name: "Epidemic Sound", category: "Music", subcategory: "Library", desc: "Music library with AI", url: "epidemicsound.com", pricing: "Paid", rating: 4.5, tags: ["library", "royalty-free", "youtube"]},
    {name: "Artlist", category: "Music", subcategory: "Library", desc: "Music and SFX library", url: "artlist.io", pricing: "Paid", rating: 4.5, tags: ["library", "sfx", "unlimited"]},
    {name: "AudioJungle", category: "Music", subcategory: "Marketplace", desc: "Royalty-free music", url: "audiojungle.net", pricing: "Per-Item", rating: 4.2, tags: ["marketplace", "envato", "variety"]},
    {name: "Splice", category: "Music", subcategory: "Samples", desc: "Music samples and loops", url: "splice.com", pricing: "Paid", rating: 4.5, tags: ["samples", "loops", "production"]},
    {name: "Landr", category: "Music", subcategory: "Mastering", desc: "AI music mastering", url: "landr.com", pricing: "Paid", rating: 4.2, tags: ["mastering", "distribution", "ai"]},
    {name: "iZotope", category: "Music", subcategory: "Production", desc: "AI audio production tools", url: "izotope.com", pricing: "Paid", rating: 4.6, tags: ["production", "mixing", "mastering"]},
    {name: "Accusonus", category: "Music", subcategory: "Audio Repair", desc: "AI audio repair tools", url: "accusonus.com", pricing: "Paid", rating: 4.3, tags: ["repair", "cleanup", "plugins"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE10 = AI_TOOLS_PHASE10;
}


