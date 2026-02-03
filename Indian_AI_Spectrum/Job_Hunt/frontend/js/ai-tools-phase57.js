// AI Tools Database - Phase 57: Architecture & Construction AI
// 100+ Architecture and construction AI tools

const AI_TOOLS_PHASE57 = [
    // ==================== BIM & DESIGN ====================
    {name: "Autodesk Revit", category: "Architecture AI", subcategory: "BIM", desc: "BIM software", url: "autodesk.com/revit", pricing: "Paid", rating: 4.5, tags: ["bim", "autodesk", "design"], featured: true},
    {name: "ArchiCAD", category: "Architecture AI", subcategory: "BIM", desc: "Graphisoft BIM", url: "graphisoft.com/archicad", pricing: "Paid", rating: 4.4, tags: ["bim", "graphisoft", "design"]},
    {name: "SketchUp", category: "Architecture AI", subcategory: "3D Modeling", desc: "3D modeling software", url: "sketchup.com", pricing: "Freemium", rating: 4.5, tags: ["3d", "modeling", "easy"]},
    {name: "Rhino", category: "Architecture AI", subcategory: "3D Modeling", desc: "3D NURBS modeling", url: "rhino3d.com", pricing: "Paid", rating: 4.5, tags: ["3d", "nurbs", "parametric"]},
    {name: "Grasshopper", category: "Architecture AI", subcategory: "Parametric", desc: "Parametric design", url: "grasshopper3d.com", pricing: "Free", rating: 4.5, tags: ["parametric", "rhino", "visual-programming"]},
    {name: "Blender", category: "Architecture AI", subcategory: "3D", desc: "Open source 3D", url: "blender.org", pricing: "Free", rating: 4.7, tags: ["3d", "open-source", "rendering"]},
    {name: "AutoCAD", category: "Architecture AI", subcategory: "CAD", desc: "CAD software", url: "autodesk.com/autocad", pricing: "Paid", rating: 4.4, tags: ["cad", "autodesk", "drafting"]},
    {name: "Vectorworks", category: "Architecture AI", subcategory: "BIM", desc: "Design software", url: "vectorworks.net", pricing: "Paid", rating: 4.2, tags: ["bim", "design", "entertainment"]},
    {name: "Chief Architect", category: "Architecture AI", subcategory: "Residential", desc: "Residential design", url: "chiefarchitect.com", pricing: "Paid", rating: 4.3, tags: ["residential", "home-design", "3d"]},
    {name: "Planner 5D", category: "Architecture AI", subcategory: "Home Design", desc: "Home design tool", url: "planner5d.com", pricing: "Freemium", rating: 4.2, tags: ["home", "design", "easy"]},
    
    // ==================== AI DESIGN TOOLS ====================
    {name: "Midjourney Architecture", category: "Architecture AI", subcategory: "AI Design", desc: "AI architectural viz", url: "midjourney.com", pricing: "Paid", rating: 4.6, tags: ["ai", "visualization", "concept"], featured: true},
    {name: "Spacemaker (Autodesk)", category: "Architecture AI", subcategory: "AI Design", desc: "AI urban design", url: "spacemakerai.com", pricing: "Paid", rating: 4.3, tags: ["ai", "urban", "generative"]},
    {name: "TestFit", category: "Architecture AI", subcategory: "Feasibility", desc: "Building configurator", url: "testfit.io", pricing: "Paid", rating: 4.2, tags: ["feasibility", "generative", "configurator"]},
    {name: "Finch3D", category: "Architecture AI", subcategory: "AI Design", desc: "AI floor plan", url: "finch3d.com", pricing: "Paid", rating: 4.1, tags: ["ai", "floor-plan", "optimization"]},
    {name: "Hypar", category: "Architecture AI", subcategory: "Generative", desc: "Generative design", url: "hypar.io", pricing: "Freemium", rating: 4.2, tags: ["generative", "computational", "cloud"]},
    {name: "Delve (Google)", category: "Architecture AI", subcategory: "AI Design", desc: "Google urban design", url: "sidewalklabs.com/products/delve", pricing: "Paid", rating: 4.0, tags: ["ai", "urban", "google"]},
    {name: "Cove.tool", category: "Architecture AI", subcategory: "Analysis", desc: "Building performance", url: "cove.tools", pricing: "Paid", rating: 4.3, tags: ["performance", "analysis", "sustainability"]},
    {name: "Ladybug Tools", category: "Architecture AI", subcategory: "Analysis", desc: "Environmental analysis", url: "ladybug.tools", pricing: "Free", rating: 4.4, tags: ["analysis", "environmental", "grasshopper"]},
    {name: "IES VE", category: "Architecture AI", subcategory: "Simulation", desc: "Building simulation", url: "iesve.com", pricing: "Paid", rating: 4.2, tags: ["simulation", "energy", "daylighting"]},
    {name: "Sefaira", category: "Architecture AI", subcategory: "Analysis", desc: "Building performance", url: "sefaira.com", pricing: "Paid", rating: 4.0, tags: ["performance", "trimble", "sustainability"]},
    
    // ==================== CONSTRUCTION TECH ====================
    {name: "Procore", category: "Architecture AI", subcategory: "Construction", desc: "Construction management", url: "procore.com", pricing: "Paid", rating: 4.5, tags: ["construction", "management", "platform"], featured: true},
    {name: "Autodesk Construction Cloud", category: "Architecture AI", subcategory: "Construction", desc: "Construction platform", url: "construction.autodesk.com", pricing: "Paid", rating: 4.3, tags: ["construction", "autodesk", "bim"]},
    {name: "PlanGrid", category: "Architecture AI", subcategory: "Field", desc: "Field productivity", url: "plangrid.com", pricing: "Paid", rating: 4.3, tags: ["field", "autodesk", "blueprints"]},
    {name: "Fieldwire", category: "Architecture AI", subcategory: "Field", desc: "Field management", url: "fieldwire.com", pricing: "Freemium", rating: 4.4, tags: ["field", "tasks", "mobile"]},
    {name: "OpenSpace", category: "Architecture AI", subcategory: "Reality Capture", desc: "360 documentation", url: "openspace.ai", pricing: "Paid", rating: 4.4, tags: ["360", "documentation", "ai"]},
    {name: "Matterport Construction", category: "Architecture AI", subcategory: "Reality Capture", desc: "3D capture", url: "matterport.com", pricing: "Paid", rating: 4.5, tags: ["3d", "capture", "twins"]},
    {name: "DroneDeploy", category: "Architecture AI", subcategory: "Drone", desc: "Drone mapping", url: "dronedeploy.com", pricing: "Paid", rating: 4.4, tags: ["drone", "mapping", "progress"]},
    {name: "Buildots", category: "Architecture AI", subcategory: "AI Construction", desc: "AI construction tracking", url: "buildots.com", pricing: "Paid", rating: 4.2, tags: ["ai", "tracking", "progress"]},
    {name: "Disperse", category: "Architecture AI", subcategory: "AI Construction", desc: "Construction AI", url: "disperse.io", pricing: "Paid", rating: 4.1, tags: ["ai", "analytics", "progress"]},
    {name: "Reconstruct", category: "Architecture AI", subcategory: "Reality Capture", desc: "Visual project intel", url: "reconstructinc.com", pricing: "Paid", rating: 4.0, tags: ["visual", "ai", "progress"]},
    
    // ==================== RENDERING & VIZ ====================
    {name: "Enscape", category: "Architecture AI", subcategory: "Rendering", desc: "Real-time rendering", url: "enscape3d.com", pricing: "Paid", rating: 4.6, tags: ["rendering", "real-time", "vr"], featured: true},
    {name: "Lumion", category: "Architecture AI", subcategory: "Rendering", desc: "Architectural viz", url: "lumion.com", pricing: "Paid", rating: 4.5, tags: ["rendering", "visualization", "real-time"]},
    {name: "Twinmotion", category: "Architecture AI", subcategory: "Rendering", desc: "Real-time viz", url: "unrealengine.com/twinmotion", pricing: "Freemium", rating: 4.4, tags: ["rendering", "epic", "real-time"]},
    {name: "V-Ray", category: "Architecture AI", subcategory: "Rendering", desc: "Ray tracing renderer", url: "chaos.com/vray", pricing: "Paid", rating: 4.6, tags: ["rendering", "ray-tracing", "chaos"]},
    {name: "Corona Renderer", category: "Architecture AI", subcategory: "Rendering", desc: "Rendering engine", url: "corona-renderer.com", pricing: "Paid", rating: 4.5, tags: ["rendering", "chaos", "realistic"]},
    {name: "KeyShot", category: "Architecture AI", subcategory: "Rendering", desc: "3D rendering", url: "keyshot.com", pricing: "Paid", rating: 4.5, tags: ["rendering", "product", "fast"]},
    {name: "D5 Render", category: "Architecture AI", subcategory: "Rendering", desc: "Real-time ray tracing", url: "d5render.com", pricing: "Freemium", rating: 4.4, tags: ["rendering", "ray-tracing", "rtx"]},
    {name: "Veras", category: "Architecture AI", subcategory: "AI Rendering", desc: "AI visualization", url: "evolvelab.io/veras", pricing: "Paid", rating: 4.2, tags: ["ai", "visualization", "concept"]},
    {name: "Arkoai", category: "Architecture AI", subcategory: "AI Rendering", desc: "AI arch rendering", url: "arkoai.com", pricing: "Paid", rating: 4.1, tags: ["ai", "rendering", "architecture"]},
    {name: "Kaedim", category: "Architecture AI", subcategory: "AI 3D", desc: "2D to 3D AI", url: "kaedim3d.com", pricing: "Paid", rating: 4.0, tags: ["ai", "3d", "generation"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE57 = AI_TOOLS_PHASE57;
}


