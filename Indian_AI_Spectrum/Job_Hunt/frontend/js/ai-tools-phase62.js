// AI Tools Database - Phase 62: More Image & Video AI
// 150+ Additional image and video tools

const AI_TOOLS_PHASE62 = [
    // ==================== IMAGE GENERATION ====================
    {name: "Midjourney", category: "Image", subcategory: "Generation", desc: "AI art generation", url: "midjourney.com", pricing: "Paid", rating: 4.8, tags: ["art", "generation", "discord"], featured: true},
    {name: "DALL-E 3", category: "Image", subcategory: "Generation", desc: "OpenAI image generation", url: "openai.com/dall-e-3", pricing: "Paid", rating: 4.7, tags: ["generation", "openai", "chatgpt"]},
    {name: "Stable Diffusion", category: "Image", subcategory: "Generation", desc: "Open source image AI", url: "stability.ai", pricing: "Freemium", rating: 4.6, tags: ["open-source", "generation", "local"]},
    {name: "Adobe Firefly", category: "Image", subcategory: "Generation", desc: "Adobe AI generation", url: "adobe.com/firefly", pricing: "Freemium", rating: 4.5, tags: ["adobe", "generation", "commercial"]},
    {name: "Ideogram", category: "Image", subcategory: "Generation", desc: "AI image with text", url: "ideogram.ai", pricing: "Freemium", rating: 4.4, tags: ["text", "generation", "typography"]},
    {name: "Playground AI", category: "Image", subcategory: "Generation", desc: "AI image playground", url: "playgroundai.com", pricing: "Freemium", rating: 4.3, tags: ["generation", "editing", "free"]},
    {name: "NightCafe", category: "Image", subcategory: "Generation", desc: "AI art generator", url: "nightcafe.studio", pricing: "Freemium", rating: 4.2, tags: ["art", "community", "credits"]},
    {name: "Artbreeder", category: "Image", subcategory: "Generation", desc: "Collaborative AI art", url: "artbreeder.com", pricing: "Freemium", rating: 4.3, tags: ["collaborative", "faces", "breeding"]},
    {name: "Craiyon", category: "Image", subcategory: "Generation", desc: "Free AI art", url: "craiyon.com", pricing: "Freemium", rating: 4.0, tags: ["free", "generation", "dalle-mini"]},
    {name: "DreamStudio", category: "Image", subcategory: "Generation", desc: "Stability AI studio", url: "dreamstudio.ai", pricing: "Paid", rating: 4.3, tags: ["stability", "studio", "generation"]},
    {name: "Canva AI", category: "Image", subcategory: "Design", desc: "Canva AI features", url: "canva.com", pricing: "Freemium", rating: 4.6, tags: ["design", "templates", "ai"]},
    {name: "Krea AI", category: "Image", subcategory: "Generation", desc: "Real-time AI generation", url: "krea.ai", pricing: "Freemium", rating: 4.3, tags: ["real-time", "generation", "creative"]},
    {name: "Lexica", category: "Image", subcategory: "Search", desc: "AI art search", url: "lexica.art", pricing: "Freemium", rating: 4.2, tags: ["search", "prompts", "generation"]},
    {name: "Mage Space", category: "Image", subcategory: "Generation", desc: "Free AI art", url: "mage.space", pricing: "Freemium", rating: 4.1, tags: ["free", "generation", "unlimited"]},
    {name: "Dezgo", category: "Image", subcategory: "Generation", desc: "AI image generator", url: "dezgo.com", pricing: "Freemium", rating: 4.0, tags: ["generation", "free", "api"]},
    
    // ==================== IMAGE EDITING ====================
    {name: "PhotoRoom", category: "Image", subcategory: "Background", desc: "Background removal", url: "photoroom.com", pricing: "Freemium", rating: 4.6, tags: ["background", "removal", "editing"], featured: true},
    {name: "Remove.bg", category: "Image", subcategory: "Background", desc: "Remove backgrounds", url: "remove.bg", pricing: "Freemium", rating: 4.7, tags: ["background", "removal", "ai"]},
    {name: "Cleanup.pictures", category: "Image", subcategory: "Inpainting", desc: "Remove objects", url: "cleanup.pictures", pricing: "Freemium", rating: 4.5, tags: ["cleanup", "inpainting", "removal"]},
    {name: "Magic Eraser", category: "Image", subcategory: "Inpainting", desc: "Remove unwanted objects", url: "magiceraser.io", pricing: "Freemium", rating: 4.3, tags: ["eraser", "removal", "cleanup"]},
    {name: "Pixlr", category: "Image", subcategory: "Editor", desc: "Online photo editor", url: "pixlr.com", pricing: "Freemium", rating: 4.3, tags: ["editor", "online", "free"]},
    {name: "Photopea", category: "Image", subcategory: "Editor", desc: "Free Photoshop alternative", url: "photopea.com", pricing: "Free", rating: 4.5, tags: ["editor", "free", "photoshop"]},
    {name: "Fotor", category: "Image", subcategory: "Editor", desc: "Online photo editor", url: "fotor.com", pricing: "Freemium", rating: 4.2, tags: ["editor", "online", "effects"]},
    {name: "BeFunky", category: "Image", subcategory: "Editor", desc: "Photo editor & design", url: "befunky.com", pricing: "Freemium", rating: 4.1, tags: ["editor", "collage", "design"]},
    {name: "PicMonkey", category: "Image", subcategory: "Editor", desc: "Photo editing", url: "picmonkey.com", pricing: "Paid", rating: 4.1, tags: ["editing", "design", "templates"]},
    {name: "Luminar Neo", category: "Image", subcategory: "Editor", desc: "AI photo editor", url: "skylum.com/luminar", pricing: "Paid", rating: 4.4, tags: ["ai", "editor", "desktop"]},
    {name: "Topaz Labs", category: "Image", subcategory: "Enhancement", desc: "AI photo enhancement", url: "topazlabs.com", pricing: "Paid", rating: 4.5, tags: ["enhancement", "upscaling", "denoise"]},
    {name: "Gigapixel AI", category: "Image", subcategory: "Upscaling", desc: "AI image upscaling", url: "topazlabs.com/gigapixel", pricing: "Paid", rating: 4.5, tags: ["upscaling", "topaz", "quality"]},
    {name: "Let's Enhance", category: "Image", subcategory: "Upscaling", desc: "AI image upscaling", url: "letsenhance.io", pricing: "Freemium", rating: 4.3, tags: ["upscaling", "enhancement", "online"]},
    {name: "Bigjpg", category: "Image", subcategory: "Upscaling", desc: "Anime upscaling", url: "bigjpg.com", pricing: "Freemium", rating: 4.2, tags: ["upscaling", "anime", "free"]},
    {name: "Upscayl", category: "Image", subcategory: "Upscaling", desc: "Free upscaling", url: "upscayl.org", pricing: "Free", rating: 4.4, tags: ["upscaling", "open-source", "desktop"]},
    
    // ==================== VIDEO EDITING ====================
    {name: "Runway ML", category: "Video", subcategory: "AI Video", desc: "AI video editing", url: "runwayml.com", pricing: "Freemium", rating: 4.6, tags: ["ai", "video", "creative"], featured: true},
    {name: "Pika Labs", category: "Video", subcategory: "Generation", desc: "AI video generation", url: "pika.art", pricing: "Freemium", rating: 4.5, tags: ["generation", "text-to-video", "ai"]},
    {name: "Sora (OpenAI)", category: "Video", subcategory: "Generation", desc: "OpenAI video generation", url: "openai.com/sora", pricing: "Waitlist", rating: 4.8, tags: ["generation", "openai", "text-to-video"]},
    {name: "HeyGen", category: "Video", subcategory: "AI Avatar", desc: "AI video avatars", url: "heygen.com", pricing: "Freemium", rating: 4.5, tags: ["avatar", "spokesperson", "ai"]},
    {name: "D-ID", category: "Video", subcategory: "AI Avatar", desc: "AI video creation", url: "d-id.com", pricing: "Freemium", rating: 4.4, tags: ["avatar", "talking-head", "ai"]},
    {name: "Colossyan", category: "Video", subcategory: "AI Avatar", desc: "AI video platform", url: "colossyan.com", pricing: "Paid", rating: 4.3, tags: ["avatar", "training", "learning"]},
    {name: "Elai.io", category: "Video", subcategory: "AI Avatar", desc: "AI video generation", url: "elai.io", pricing: "Freemium", rating: 4.2, tags: ["avatar", "video", "ai"]},
    {name: "Hour One", category: "Video", subcategory: "AI Avatar", desc: "AI video presenters", url: "hourone.ai", pricing: "Paid", rating: 4.1, tags: ["avatar", "virtual-human", "enterprise"]},
    {name: "Rephrase.ai", category: "Video", subcategory: "AI Avatar", desc: "AI video personalization", url: "rephrase.ai", pricing: "Paid", rating: 4.2, tags: ["personalization", "avatar", "enterprise"]},
    {name: "FlexClip", category: "Video", subcategory: "Editor", desc: "Online video maker", url: "flexclip.com", pricing: "Freemium", rating: 4.2, tags: ["editor", "online", "templates"]},
    {name: "Animoto", category: "Video", subcategory: "Editor", desc: "Video maker", url: "animoto.com", pricing: "Paid", rating: 4.1, tags: ["video", "slideshow", "templates"]},
    {name: "Biteable", category: "Video", subcategory: "Editor", desc: "Video maker", url: "biteable.com", pricing: "Paid", rating: 4.1, tags: ["video", "animated", "templates"]},
    {name: "Promo", category: "Video", subcategory: "Marketing", desc: "Video marketing", url: "promo.com", pricing: "Paid", rating: 4.0, tags: ["marketing", "video", "templates"]},
    {name: "Wave.video", category: "Video", subcategory: "Editor", desc: "Video marketing platform", url: "wave.video", pricing: "Freemium", rating: 4.2, tags: ["marketing", "editing", "streaming"]},
    {name: "Fliki", category: "Video", subcategory: "Text-to-Video", desc: "Text to video AI", url: "fliki.ai", pricing: "Freemium", rating: 4.3, tags: ["text-to-video", "voice", "ai"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE62 = AI_TOOLS_PHASE62;
}


