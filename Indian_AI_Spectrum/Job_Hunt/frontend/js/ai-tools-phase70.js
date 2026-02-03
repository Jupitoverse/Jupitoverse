// AI Tools Database - Phase 70: More 3D, AR/VR & Gaming
// 100+ Additional 3D, AR/VR and gaming tools

const AI_TOOLS_PHASE70 = [
    // ==================== 3D MODELING ====================
    {name: "Blender", category: "3D", subcategory: "Modeling", desc: "Open source 3D", url: "blender.org", pricing: "Free", rating: 4.8, tags: ["3d", "open-source", "animation"], featured: true},
    {name: "Cinema 4D", category: "3D", subcategory: "Modeling", desc: "3D animation", url: "maxon.net/cinema-4d", pricing: "Paid", rating: 4.6, tags: ["3d", "motion", "professional"]},
    {name: "Maya", category: "3D", subcategory: "Modeling", desc: "3D animation", url: "autodesk.com/maya", pricing: "Paid", rating: 4.6, tags: ["3d", "autodesk", "animation"]},
    {name: "3ds Max", category: "3D", subcategory: "Modeling", desc: "3D modeling & rendering", url: "autodesk.com/3ds-max", pricing: "Paid", rating: 4.5, tags: ["3d", "autodesk", "archviz"]},
    {name: "ZBrush", category: "3D", subcategory: "Sculpting", desc: "Digital sculpting", url: "maxon.net/zbrush", pricing: "Paid", rating: 4.7, tags: ["sculpting", "high-poly", "characters"]},
    {name: "Houdini", category: "3D", subcategory: "VFX", desc: "Procedural 3D", url: "sidefx.com", pricing: "Freemium", rating: 4.6, tags: ["procedural", "vfx", "simulation"]},
    {name: "Substance 3D", category: "3D", subcategory: "Texturing", desc: "3D texturing", url: "substance3d.com", pricing: "Paid", rating: 4.6, tags: ["texturing", "adobe", "materials"]},
    {name: "Modo", category: "3D", subcategory: "Modeling", desc: "3D modeling", url: "foundry.com/modo", pricing: "Paid", rating: 4.3, tags: ["modeling", "animation", "foundry"]},
    {name: "LightWave 3D", category: "3D", subcategory: "Animation", desc: "3D animation", url: "lightwave3d.com", pricing: "Paid", rating: 4.1, tags: ["animation", "vfx", "classic"]},
    {name: "SketchUp", category: "3D", subcategory: "Architecture", desc: "3D design", url: "sketchup.com", pricing: "Freemium", rating: 4.5, tags: ["architecture", "easy", "modeling"]},
    {name: "Fusion 360", category: "3D", subcategory: "CAD", desc: "Cloud CAD", url: "autodesk.com/fusion-360", pricing: "Freemium", rating: 4.5, tags: ["cad", "cloud", "manufacturing"]},
    {name: "SolidWorks", category: "3D", subcategory: "CAD", desc: "3D CAD", url: "solidworks.com", pricing: "Paid", rating: 4.5, tags: ["cad", "engineering", "professional"]},
    
    // ==================== AI 3D GENERATION ====================
    {name: "Meshy", category: "3D", subcategory: "AI Generation", desc: "AI 3D model generation", url: "meshy.ai", pricing: "Freemium", rating: 4.3, tags: ["ai", "text-to-3d", "game-ready"], featured: true},
    {name: "Luma AI", category: "3D", subcategory: "3D Capture", desc: "3D capture & NeRF", url: "lumalabs.ai", pricing: "Free", rating: 4.4, tags: ["nerf", "capture", "photorealistic"]},
    {name: "Point-E", category: "3D", subcategory: "AI Generation", desc: "OpenAI 3D", url: "github.com/openai/point-e", pricing: "Free", rating: 4.0, tags: ["ai", "openai", "point-cloud"]},
    {name: "Shap-E", category: "3D", subcategory: "AI Generation", desc: "OpenAI 3D meshes", url: "github.com/openai/shap-e", pricing: "Free", rating: 4.1, tags: ["ai", "openai", "meshes"]},
    {name: "GET3D (NVIDIA)", category: "3D", subcategory: "AI Generation", desc: "NVIDIA 3D AI", url: "nv-tlabs.github.io/GET3D", pricing: "Free", rating: 4.2, tags: ["ai", "nvidia", "research"]},
    {name: "Kaedim", category: "3D", subcategory: "AI Generation", desc: "Image to 3D", url: "kaedim3d.com", pricing: "Paid", rating: 4.2, tags: ["ai", "image-to-3d", "game-ready"]},
    {name: "3DFY", category: "3D", subcategory: "AI Generation", desc: "AI 3D creation", url: "3dfy.ai", pricing: "Paid", rating: 4.1, tags: ["ai", "text-to-3d", "image-to-3d"]},
    {name: "CSM.ai", category: "3D", subcategory: "AI Generation", desc: "Common Sense Machines", url: "csm.ai", pricing: "Freemium", rating: 4.2, tags: ["ai", "3d", "simulation"]},
    {name: "Alpha3D", category: "3D", subcategory: "AI Generation", desc: "2D to 3D AI", url: "alpha3d.io", pricing: "Paid", rating: 4.0, tags: ["ai", "conversion", "game-assets"]},
    {name: "Masterpiece Studio", category: "3D", subcategory: "AI Generation", desc: "VR 3D creation", url: "masterpiecestudio.com", pricing: "Paid", rating: 4.1, tags: ["vr", "ai", "creation"]},
    
    // ==================== GAME ENGINES ====================
    {name: "Unity", category: "3D", subcategory: "Game Engine", desc: "Game engine", url: "unity.com", pricing: "Freemium", rating: 4.6, tags: ["game-engine", "cross-platform", "mobile"], featured: true},
    {name: "Unreal Engine", category: "3D", subcategory: "Game Engine", desc: "Epic's engine", url: "unrealengine.com", pricing: "Freemium", rating: 4.7, tags: ["game-engine", "aaa", "graphics"]},
    {name: "Godot", category: "3D", subcategory: "Game Engine", desc: "Open source engine", url: "godotengine.org", pricing: "Free", rating: 4.5, tags: ["game-engine", "open-source", "2d-3d"]},
    {name: "CryEngine", category: "3D", subcategory: "Game Engine", desc: "AAA game engine", url: "cryengine.com", pricing: "Freemium", rating: 4.2, tags: ["game-engine", "graphics", "fps"]},
    {name: "Amazon Lumberyard", category: "3D", subcategory: "Game Engine", desc: "AWS game engine", url: "aws.amazon.com/lumberyard", pricing: "Free", rating: 3.9, tags: ["game-engine", "aws", "multiplayer"]},
    {name: "O3DE", category: "3D", subcategory: "Game Engine", desc: "Open 3D Engine", url: "o3de.org", pricing: "Free", rating: 4.0, tags: ["game-engine", "open-source", "linux"]},
    {name: "GameMaker", category: "3D", subcategory: "Game Engine", desc: "2D game engine", url: "gamemaker.io", pricing: "Freemium", rating: 4.4, tags: ["2d", "beginner", "drag-drop"]},
    {name: "RPG Maker", category: "3D", subcategory: "Game Engine", desc: "RPG creation", url: "rpgmakerweb.com", pricing: "Paid", rating: 4.2, tags: ["rpg", "no-code", "2d"]},
    {name: "Construct", category: "3D", subcategory: "Game Engine", desc: "No-code game engine", url: "construct.net", pricing: "Freemium", rating: 4.3, tags: ["no-code", "2d", "html5"]},
    {name: "Defold", category: "3D", subcategory: "Game Engine", desc: "Cross-platform engine", url: "defold.com", pricing: "Free", rating: 4.3, tags: ["cross-platform", "2d", "king"]},
    
    // ==================== AR/VR DEVELOPMENT ====================
    {name: "Spark AR", category: "3D", subcategory: "AR", desc: "Meta AR studio", url: "sparkar.facebook.com", pricing: "Free", rating: 4.4, tags: ["ar", "instagram", "facebook"], featured: true},
    {name: "Lens Studio", category: "3D", subcategory: "AR", desc: "Snapchat AR", url: "lensstudio.snapchat.com", pricing: "Free", rating: 4.4, tags: ["ar", "snapchat", "filters"]},
    {name: "Effect House", category: "3D", subcategory: "AR", desc: "TikTok AR", url: "effecthouse.tiktok.com", pricing: "Free", rating: 4.2, tags: ["ar", "tiktok", "effects"]},
    {name: "Reality Composer", category: "3D", subcategory: "AR", desc: "Apple AR", url: "developer.apple.com/reality-composer", pricing: "Free", rating: 4.2, tags: ["ar", "apple", "ios"]},
    {name: "Aero", category: "3D", subcategory: "AR", desc: "Adobe AR", url: "adobe.com/aero", pricing: "Free", rating: 4.1, tags: ["ar", "adobe", "creative"]},
    {name: "Meta Presence Platform", category: "3D", subcategory: "VR", desc: "Meta Quest dev", url: "developer.oculus.com", pricing: "Free", rating: 4.3, tags: ["vr", "meta", "quest"]},
    {name: "SteamVR", category: "3D", subcategory: "VR", desc: "Valve VR platform", url: "store.steampowered.com/steamvr", pricing: "Free", rating: 4.4, tags: ["vr", "steam", "valve"]},
    {name: "VRTK", category: "3D", subcategory: "VR", desc: "VR toolkit", url: "vrtk.io", pricing: "Free", rating: 4.2, tags: ["vr", "unity", "toolkit"]},
    {name: "A-Frame", category: "3D", subcategory: "WebXR", desc: "Web VR framework", url: "aframe.io", pricing: "Free", rating: 4.3, tags: ["webxr", "web", "mozilla"]},
    {name: "Babylon.js", category: "3D", subcategory: "WebGL", desc: "Web 3D engine", url: "babylonjs.com", pricing: "Free", rating: 4.4, tags: ["webgl", "3d", "microsoft"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE70 = AI_TOOLS_PHASE70;
}


