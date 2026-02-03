// AI Tools Database - Phase 18: 3D, Gaming, AR/VR & Metaverse AI
// 200+ Tools for 3D, gaming, and immersive technologies

const AI_TOOLS_PHASE18 = [
    // ==================== 3D MODELING & DESIGN ====================
    {name: "Blender", category: "3D", subcategory: "Modeling", desc: "Free 3D creation suite", url: "blender.org", pricing: "Free", rating: 4.8, tags: ["open-source", "modeling", "animation"], featured: true},
    {name: "Maya", category: "3D", subcategory: "Professional", desc: "Professional 3D software", url: "autodesk.com/maya", pricing: "Paid", rating: 4.6, tags: ["autodesk", "animation", "vfx"]},
    {name: "3ds Max", category: "3D", subcategory: "Professional", desc: "3D modeling and rendering", url: "autodesk.com/3ds-max", pricing: "Paid", rating: 4.5, tags: ["autodesk", "arch-viz", "modeling"]},
    {name: "Cinema 4D", category: "3D", subcategory: "Motion", desc: "3D for motion graphics", url: "maxon.net/cinema-4d", pricing: "Paid", rating: 4.6, tags: ["motion", "easy", "mograph"]},
    {name: "Houdini", category: "3D", subcategory: "VFX", desc: "Procedural 3D and VFX", url: "sidefx.com", pricing: "Freemium", rating: 4.7, tags: ["procedural", "vfx", "simulations"]},
    {name: "ZBrush", category: "3D", subcategory: "Sculpting", desc: "Digital sculpting", url: "zbrush.com", pricing: "Paid", rating: 4.7, tags: ["sculpting", "characters", "detail"]},
    {name: "Substance 3D", category: "3D", subcategory: "Texturing", desc: "3D texturing suite", url: "adobe.com/products/substance3d", pricing: "Paid", rating: 4.6, tags: ["texturing", "materials", "adobe"]},
    {name: "KeyShot", category: "3D", subcategory: "Rendering", desc: "Real-time rendering", url: "keyshot.com", pricing: "Paid", rating: 4.6, tags: ["rendering", "easy", "product"]},
    {name: "Modo", category: "3D", subcategory: "Modeling", desc: "3D modeling software", url: "foundry.com/modo", pricing: "Paid", rating: 4.4, tags: ["modeling", "sculpting", "rendering"]},
    {name: "Marvelous Designer", category: "3D", subcategory: "Clothing", desc: "3D clothing design", url: "marvelousdesigner.com", pricing: "Paid", rating: 4.5, tags: ["clothing", "fashion", "simulation"]},
    {name: "Gravity Sketch", category: "3D", subcategory: "VR Design", desc: "VR 3D design", url: "gravitysketch.com", pricing: "Freemium", rating: 4.4, tags: ["vr", "design", "intuitive"]},
    {name: "Spline", category: "3D", subcategory: "Web", desc: "3D design for web", url: "spline.design", pricing: "Freemium", rating: 4.5, tags: ["web", "interactive", "easy"]},
    {name: "Vectary", category: "3D", subcategory: "Web", desc: "Web-based 3D design", url: "vectary.com", pricing: "Freemium", rating: 4.3, tags: ["web", "ar", "collaboration"]},
    {name: "Womp", category: "3D", subcategory: "Easy", desc: "Easy 3D for everyone", url: "womp.com", pricing: "Freemium", rating: 4.2, tags: ["easy", "web", "beginner"]},
    {name: "SketchUp", category: "3D", subcategory: "Architecture", desc: "3D modeling software", url: "sketchup.com", pricing: "Freemium", rating: 4.5, tags: ["architecture", "easy", "popular"]},
    
    // ==================== AI 3D GENERATION ====================
    {name: "Meshy", category: "AI 3D", subcategory: "Generation", desc: "AI 3D model generator", url: "meshy.ai", pricing: "Freemium", rating: 4.4, tags: ["text-to-3d", "image-to-3d", "ai"], featured: true},
    {name: "Kaedim", category: "AI 3D", subcategory: "Generation", desc: "Image to 3D model", url: "kaedim3d.com", pricing: "Paid", rating: 4.3, tags: ["image-to-3d", "game-ready", "ai"]},
    {name: "Luma AI", category: "AI 3D", subcategory: "Capture", desc: "3D capture with AI", url: "lumalabs.ai", pricing: "Freemium", rating: 4.5, tags: ["nerf", "capture", "realistic"]},
    {name: "Masterpiece X", category: "AI 3D", subcategory: "Generation", desc: "Generate 3D from text", url: "masterpiecex.com", pricing: "Freemium", rating: 4.2, tags: ["text-to-3d", "creative", "ai"]},
    {name: "3DFY.ai", category: "AI 3D", subcategory: "Generation", desc: "AI 3D asset generation", url: "3dfy.ai", pricing: "Paid", rating: 4.2, tags: ["text-to-3d", "scalable", "ai"]},
    {name: "Ponzu", category: "AI 3D", subcategory: "Texturing", desc: "AI 3D texturing", url: "ponzu.gg", pricing: "Freemium", rating: 4.2, tags: ["texturing", "stylize", "ai"]},
    {name: "Polycam", category: "AI 3D", subcategory: "Scanning", desc: "3D scanning app", url: "poly.cam", pricing: "Freemium", rating: 4.5, tags: ["scanning", "lidar", "photogrammetry"]},
    {name: "RealityCapture", category: "AI 3D", subcategory: "Photogrammetry", desc: "Photogrammetry software", url: "capturingreality.com", pricing: "Paid", rating: 4.6, tags: ["photogrammetry", "fast", "accurate"]},
    {name: "Meshroom", category: "AI 3D", subcategory: "Photogrammetry", desc: "Open source photogrammetry", url: "alicevision.org/meshroom", pricing: "Free", rating: 4.2, tags: ["photogrammetry", "open-source", "free"]},
    {name: "Wonder Studio", category: "AI 3D", subcategory: "VFX", desc: "AI VFX tool", url: "wonderdynamics.com", pricing: "Paid", rating: 4.5, tags: ["vfx", "cg-characters", "automatic"]},
    {name: "Move.ai", category: "AI 3D", subcategory: "Motion Capture", desc: "AI motion capture", url: "move.ai", pricing: "Paid", rating: 4.4, tags: ["mocap", "markerless", "ai"]},
    {name: "DeepMotion", category: "AI 3D", subcategory: "Animation", desc: "AI motion capture and animation", url: "deepmotion.com", pricing: "Freemium", rating: 4.3, tags: ["mocap", "animation", "web"]},
    {name: "Rokoko", category: "AI 3D", subcategory: "Motion Capture", desc: "Motion capture tools", url: "rokoko.com", pricing: "Paid", rating: 4.4, tags: ["mocap", "hardware", "ai"]},
    {name: "Mixamo", category: "AI 3D", subcategory: "Animation", desc: "3D characters and animations", url: "mixamo.com", pricing: "Free", rating: 4.5, tags: ["animation", "characters", "free"]},
    {name: "Cascadeur", category: "AI 3D", subcategory: "Animation", desc: "AI-assisted animation", url: "cascadeur.com", pricing: "Freemium", rating: 4.3, tags: ["animation", "physics", "ai"]},
    
    // ==================== GAME DEVELOPMENT ====================
    {name: "Unity", category: "Game Dev", subcategory: "Engine", desc: "Game development platform", url: "unity.com", pricing: "Freemium", rating: 4.6, tags: ["engine", "cross-platform", "popular"], featured: true},
    {name: "Unreal Engine", category: "Game Dev", subcategory: "Engine", desc: "Epic's game engine", url: "unrealengine.com", pricing: "Freemium", rating: 4.7, tags: ["engine", "aaa", "graphics"], featured: true},
    {name: "Godot", category: "Game Dev", subcategory: "Open Source", desc: "Open source game engine", url: "godotengine.org", pricing: "Free", rating: 4.5, tags: ["open-source", "free", "2d-3d"]},
    {name: "GameMaker", category: "Game Dev", subcategory: "2D", desc: "2D game development", url: "gamemaker.io", pricing: "Freemium", rating: 4.4, tags: ["2d", "beginner", "drag-drop"]},
    {name: "RPG Maker", category: "Game Dev", subcategory: "RPG", desc: "RPG creation tool", url: "rpgmakerweb.com", pricing: "Paid", rating: 4.2, tags: ["rpg", "no-code", "classic"]},
    {name: "Construct", category: "Game Dev", subcategory: "No-Code", desc: "No-code game development", url: "construct.net", pricing: "Freemium", rating: 4.3, tags: ["no-code", "html5", "2d"]},
    {name: "Buildbox", category: "Game Dev", subcategory: "No-Code", desc: "No-code game maker", url: "buildbox.com", pricing: "Freemium", rating: 4.1, tags: ["no-code", "mobile", "easy"]},
    {name: "Phaser", category: "Game Dev", subcategory: "HTML5", desc: "HTML5 game framework", url: "phaser.io", pricing: "Free", rating: 4.4, tags: ["html5", "javascript", "framework"]},
    {name: "PlayCanvas", category: "Game Dev", subcategory: "WebGL", desc: "WebGL game engine", url: "playcanvas.com", pricing: "Freemium", rating: 4.3, tags: ["webgl", "collaborative", "browser"]},
    {name: "Roblox Studio", category: "Game Dev", subcategory: "Roblox", desc: "Create for Roblox", url: "create.roblox.com", pricing: "Free", rating: 4.4, tags: ["roblox", "lua", "monetize"]},
    {name: "Core", category: "Game Dev", subcategory: "Platform", desc: "Game creation platform", url: "coregames.com", pricing: "Free", rating: 4.1, tags: ["platform", "unreal", "publish"]},
    {name: "Defold", category: "Game Dev", subcategory: "2D/3D", desc: "Cross-platform game engine", url: "defold.com", pricing: "Free", rating: 4.3, tags: ["cross-platform", "free", "lua"]},
    {name: "CryEngine", category: "Game Dev", subcategory: "AAA", desc: "AAA game engine", url: "cryengine.com", pricing: "Royalty", rating: 4.2, tags: ["aaa", "graphics", "sandbox"]},
    {name: "Cocos", category: "Game Dev", subcategory: "Mobile", desc: "Mobile game engine", url: "cocos.com", pricing: "Free", rating: 4.2, tags: ["mobile", "2d", "china"]},
    {name: "Stride", category: "Game Dev", subcategory: "Open Source", desc: "Open source C# engine", url: "stride3d.net", pricing: "Free", rating: 4.1, tags: ["open-source", "c-sharp", "modern"]},
    
    // ==================== AR/VR DEVELOPMENT ====================
    {name: "Meta Quest", category: "AR/VR", subcategory: "Platform", desc: "VR development platform", url: "developer.oculus.com", pricing: "Free", rating: 4.4, tags: ["vr", "meta", "quest"], featured: true},
    {name: "Apple visionOS", category: "AR/VR", subcategory: "Platform", desc: "Apple spatial computing", url: "developer.apple.com/visionos", pricing: "Free", rating: 4.5, tags: ["ar", "apple", "spatial"]},
    {name: "ARCore", category: "AR/VR", subcategory: "AR", desc: "Google AR SDK", url: "developers.google.com/ar", pricing: "Free", rating: 4.3, tags: ["ar", "android", "google"]},
    {name: "ARKit", category: "AR/VR", subcategory: "AR", desc: "Apple AR framework", url: "developer.apple.com/arkit", pricing: "Free", rating: 4.5, tags: ["ar", "ios", "apple"]},
    {name: "Niantic Lightship", category: "AR/VR", subcategory: "AR", desc: "AR development platform", url: "lightship.dev", pricing: "Freemium", rating: 4.2, tags: ["ar", "location", "niantic"]},
    {name: "Snap AR", category: "AR/VR", subcategory: "AR", desc: "Snapchat AR development", url: "ar.snap.com", pricing: "Free", rating: 4.3, tags: ["ar", "lenses", "snapchat"]},
    {name: "Meta Spark", category: "AR/VR", subcategory: "AR", desc: "Meta AR creation", url: "spark.meta.com", pricing: "Free", rating: 4.3, tags: ["ar", "instagram", "facebook"]},
    {name: "8th Wall", category: "AR/VR", subcategory: "WebAR", desc: "WebAR development", url: "8thwall.com", pricing: "Paid", rating: 4.4, tags: ["webar", "browser", "markerless"]},
    {name: "Zappar", category: "AR/VR", subcategory: "AR", desc: "AR creation platform", url: "zappar.com", pricing: "Freemium", rating: 4.2, tags: ["ar", "studio", "training"]},
    {name: "Vuforia", category: "AR/VR", subcategory: "AR", desc: "Enterprise AR platform", url: "ptc.com/vuforia", pricing: "Paid", rating: 4.2, tags: ["enterprise", "ar", "ptc"]},
    {name: "MRTK", category: "AR/VR", subcategory: "MR", desc: "Microsoft Mixed Reality Toolkit", url: "github.com/microsoft/MixedRealityToolkit", pricing: "Free", rating: 4.3, tags: ["mixed-reality", "hololens", "unity"]},
    {name: "Spatial", category: "AR/VR", subcategory: "Metaverse", desc: "Metaverse platform", url: "spatial.io", pricing: "Freemium", rating: 4.2, tags: ["metaverse", "nft", "social"]},
    {name: "VRChat", category: "AR/VR", subcategory: "Social VR", desc: "Social VR platform", url: "vrchat.com", pricing: "Free", rating: 4.4, tags: ["social", "avatars", "worlds"]},
    {name: "Rec Room", category: "AR/VR", subcategory: "Social VR", desc: "Social gaming VR", url: "recroom.com", pricing: "Free", rating: 4.3, tags: ["social", "gaming", "creation"]},
    {name: "Horizon Worlds", category: "AR/VR", subcategory: "Metaverse", desc: "Meta's metaverse", url: "horizon.meta.com", pricing: "Free", rating: 3.8, tags: ["metaverse", "meta", "social"]},
    
    // ==================== GAME AI & TOOLS ====================
    {name: "Inworld AI", category: "Game AI", subcategory: "NPCs", desc: "AI-powered NPCs", url: "inworld.ai", pricing: "Freemium", rating: 4.4, tags: ["npcs", "characters", "dialogue"], featured: true},
    {name: "Convai", category: "Game AI", subcategory: "NPCs", desc: "AI characters for games", url: "convai.com", pricing: "Freemium", rating: 4.3, tags: ["characters", "voice", "ai"]},
    {name: "Charisma.ai", category: "Game AI", subcategory: "Interactive", desc: "Interactive storytelling", url: "charisma.ai", pricing: "Freemium", rating: 4.2, tags: ["storytelling", "characters", "narrative"]},
    {name: "Scenario", category: "Game AI", subcategory: "Assets", desc: "AI game asset generation", url: "scenario.com", pricing: "Freemium", rating: 4.4, tags: ["assets", "art", "ai"]},
    {name: "Leonardo.ai", category: "Game AI", subcategory: "Assets", desc: "AI game assets", url: "leonardo.ai", pricing: "Freemium", rating: 4.6, tags: ["assets", "textures", "art"]},
    {name: "Promethean AI", category: "Game AI", subcategory: "Level Design", desc: "AI-assisted level design", url: "prometheanai.com", pricing: "Paid", rating: 4.3, tags: ["level-design", "environment", "ai"]},
    {name: "Rosebud AI", category: "Game AI", subcategory: "Characters", desc: "AI-generated characters", url: "rosebud.ai", pricing: "Freemium", rating: 4.2, tags: ["characters", "photos", "ai"]},
    {name: "Ready Player Me", category: "Game AI", subcategory: "Avatars", desc: "Cross-game avatars", url: "readyplayer.me", pricing: "Freemium", rating: 4.4, tags: ["avatars", "metaverse", "integration"]},
    {name: "Wolf3D", category: "Game AI", subcategory: "Avatars", desc: "Avatar SDK", url: "wolf3d.io", pricing: "Freemium", rating: 4.3, tags: ["avatars", "sdk", "3d"]},
    {name: "Synthesia (Games)", category: "Game AI", subcategory: "Characters", desc: "AI video for games", url: "synthesia.io", pricing: "Paid", rating: 4.5, tags: ["video", "npc", "cutscenes"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE18 = AI_TOOLS_PHASE18;
}


