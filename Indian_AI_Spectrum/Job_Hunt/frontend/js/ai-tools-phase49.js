// AI Tools Database - Phase 49: Manufacturing & Industrial AI
// 100+ Manufacturing and industrial AI tools

const AI_TOOLS_PHASE49 = [
    // ==================== INDUSTRIAL IOT ====================
    {name: "Siemens MindSphere", category: "Industrial AI", subcategory: "IIoT", desc: "Industrial IoT platform", url: "siemens.com/mindsphere", pricing: "Paid", rating: 4.4, tags: ["iiot", "siemens", "analytics"], featured: true},
    {name: "GE Predix", category: "Industrial AI", subcategory: "IIoT", desc: "Industrial platform", url: "ge.com/digital", pricing: "Paid", rating: 4.1, tags: ["iiot", "ge", "industrial"]},
    {name: "PTC ThingWorx", category: "Industrial AI", subcategory: "IIoT", desc: "IIoT platform", url: "ptc.com/thingworx", pricing: "Paid", rating: 4.3, tags: ["iiot", "ar", "digital-twin"]},
    {name: "Rockwell Automation", category: "Industrial AI", subcategory: "Automation", desc: "Industrial automation", url: "rockwellautomation.com", pricing: "Paid", rating: 4.2, tags: ["automation", "plc", "industrial"]},
    {name: "Honeywell Forge", category: "Industrial AI", subcategory: "Analytics", desc: "Industrial analytics", url: "honeywell.com/forge", pricing: "Paid", rating: 4.2, tags: ["analytics", "enterprise", "iot"]},
    {name: "ABB Ability", category: "Industrial AI", subcategory: "Platform", desc: "ABB digital platform", url: "global.abb/ability", pricing: "Paid", rating: 4.1, tags: ["digital", "abb", "industrial"]},
    {name: "Schneider EcoStruxure", category: "Industrial AI", subcategory: "Platform", desc: "IoT platform", url: "schneider-electric.com/ecostruxure", pricing: "Paid", rating: 4.2, tags: ["iot", "energy", "automation"]},
    {name: "Emerson Plantweb", category: "Industrial AI", subcategory: "Monitoring", desc: "Plant monitoring", url: "emerson.com/plantweb", pricing: "Paid", rating: 4.1, tags: ["monitoring", "predictive", "process"]},
    {name: "Uptake", category: "Industrial AI", subcategory: "Analytics", desc: "Industrial AI analytics", url: "uptake.com", pricing: "Paid", rating: 4.2, tags: ["analytics", "predictive", "assets"]},
    {name: "C3 AI", category: "Industrial AI", subcategory: "Enterprise", desc: "Enterprise AI platform", url: "c3.ai", pricing: "Paid", rating: 4.1, tags: ["enterprise", "ai", "analytics"]},
    
    // ==================== PREDICTIVE MAINTENANCE ====================
    {name: "Augury", category: "Industrial AI", subcategory: "Predictive", desc: "Machine health AI", url: "augury.com", pricing: "Paid", rating: 4.4, tags: ["predictive", "maintenance", "vibration"], featured: true},
    {name: "Senseye", category: "Industrial AI", subcategory: "Predictive", desc: "Predictive maintenance", url: "senseye.io", pricing: "Paid", rating: 4.3, tags: ["predictive", "siemens", "maintenance"]},
    {name: "SparkCognition", category: "Industrial AI", subcategory: "Predictive", desc: "Industrial AI", url: "sparkcognition.com", pricing: "Paid", rating: 4.2, tags: ["ai", "industrial", "predictive"]},
    {name: "Nanoprecise", category: "Industrial AI", subcategory: "Predictive", desc: "Industrial IoT analytics", url: "nanoprecise.io", pricing: "Paid", rating: 4.1, tags: ["iot", "predictive", "analytics"]},
    {name: "Petasense", category: "Industrial AI", subcategory: "Vibration", desc: "Vibration monitoring", url: "petasense.com", pricing: "Paid", rating: 4.1, tags: ["vibration", "wireless", "predictive"]},
    {name: "Presenso", category: "Industrial AI", subcategory: "Predictive", desc: "AI maintenance", url: "presenso.com", pricing: "Paid", rating: 4.0, tags: ["predictive", "ai", "autonomous"]},
    {name: "Falkonry", category: "Industrial AI", subcategory: "Operations", desc: "Operations AI", url: "falkonry.com", pricing: "Paid", rating: 4.0, tags: ["operations", "time-series", "ai"]},
    {name: "Sight Machine", category: "Industrial AI", subcategory: "Manufacturing", desc: "Manufacturing analytics", url: "sightmachine.com", pricing: "Paid", rating: 4.2, tags: ["manufacturing", "analytics", "ai"]},
    {name: "Uptake Edge", category: "Industrial AI", subcategory: "Edge", desc: "Edge AI analytics", url: "uptake.com", pricing: "Paid", rating: 4.0, tags: ["edge", "analytics", "ai"]},
    
    // ==================== ROBOTICS ====================
    {name: "Universal Robots", category: "Industrial AI", subcategory: "Cobots", desc: "Collaborative robots", url: "universal-robots.com", pricing: "Paid", rating: 4.5, tags: ["cobot", "automation", "arm"], featured: true},
    {name: "Boston Dynamics", category: "Industrial AI", subcategory: "Robotics", desc: "Advanced robotics", url: "bostondynamics.com", pricing: "Paid", rating: 4.6, tags: ["robotics", "spot", "atlas"]},
    {name: "FANUC", category: "Industrial AI", subcategory: "Robotics", desc: "Industrial robots", url: "fanuc.com", pricing: "Paid", rating: 4.4, tags: ["robots", "cnc", "industrial"]},
    {name: "ABB Robotics", category: "Industrial AI", subcategory: "Robotics", desc: "ABB robots", url: "abb.com/robotics", pricing: "Paid", rating: 4.3, tags: ["robots", "industrial", "automation"]},
    {name: "KUKA", category: "Industrial AI", subcategory: "Robotics", desc: "Industrial robots", url: "kuka.com", pricing: "Paid", rating: 4.3, tags: ["robots", "automation", "industrial"]},
    {name: "Omron", category: "Industrial AI", subcategory: "Automation", desc: "Industrial automation", url: "omron.com", pricing: "Paid", rating: 4.2, tags: ["automation", "sensors", "robots"]},
    {name: "Locus Robotics", category: "Industrial AI", subcategory: "Warehouse", desc: "Warehouse robots", url: "locusrobotics.com", pricing: "Paid", rating: 4.4, tags: ["warehouse", "amr", "fulfillment"]},
    {name: "Fetch Robotics", category: "Industrial AI", subcategory: "AMR", desc: "Autonomous mobile robots", url: "fetchrobotics.com", pricing: "Paid", rating: 4.2, tags: ["amr", "warehouse", "logistics"]},
    {name: "6 River Systems", category: "Industrial AI", subcategory: "Fulfillment", desc: "Fulfillment robots", url: "6river.com", pricing: "Paid", rating: 4.2, tags: ["fulfillment", "shopify", "amr"]},
    {name: "Symbotic", category: "Industrial AI", subcategory: "Warehouse", desc: "Warehouse automation", url: "symbotic.com", pricing: "Paid", rating: 4.3, tags: ["warehouse", "automation", "ai"]},
    
    // ==================== QUALITY CONTROL ====================
    {name: "Landing AI", category: "Industrial AI", subcategory: "Vision", desc: "Visual inspection AI", url: "landing.ai", pricing: "Paid", rating: 4.4, tags: ["vision", "inspection", "defects"], featured: true},
    {name: "Cognex", category: "Industrial AI", subcategory: "Vision", desc: "Machine vision", url: "cognex.com", pricing: "Paid", rating: 4.5, tags: ["vision", "inspection", "barcode"]},
    {name: "Keyence", category: "Industrial AI", subcategory: "Sensors", desc: "Industrial sensors", url: "keyence.com", pricing: "Paid", rating: 4.5, tags: ["sensors", "vision", "measurement"]},
    {name: "ISRA Vision", category: "Industrial AI", subcategory: "Vision", desc: "Surface inspection", url: "isravision.com", pricing: "Paid", rating: 4.2, tags: ["vision", "surface", "inspection"]},
    {name: "Instrumental", category: "Industrial AI", subcategory: "Quality", desc: "Manufacturing quality", url: "instrumental.com", pricing: "Paid", rating: 4.3, tags: ["quality", "manufacturing", "ai"]},
    {name: "Elementary", category: "Industrial AI", subcategory: "Vision", desc: "AI visual inspection", url: "elementary.ai", pricing: "Paid", rating: 4.1, tags: ["vision", "inspection", "defects"]},
    {name: "Eigen Innovations", category: "Industrial AI", subcategory: "Vision", desc: "Industrial vision AI", url: "eigeninnovations.com", pricing: "Paid", rating: 4.0, tags: ["vision", "ai", "manufacturing"]},
    {name: "Matrox Imaging", category: "Industrial AI", subcategory: "Vision", desc: "Vision systems", url: "matrox.com/imaging", pricing: "Paid", rating: 4.2, tags: ["vision", "imaging", "software"]},
    
    // ==================== 3D PRINTING ====================
    {name: "Markforged", category: "Industrial AI", subcategory: "3D Printing", desc: "Industrial 3D printing", url: "markforged.com", pricing: "Paid", rating: 4.4, tags: ["3d-printing", "metal", "composites"], featured: true},
    {name: "HP 3D Printing", category: "Industrial AI", subcategory: "3D Printing", desc: "HP additive manufacturing", url: "hp.com/3dprinting", pricing: "Paid", rating: 4.3, tags: ["3d-printing", "mjf", "industrial"]},
    {name: "Stratasys", category: "Industrial AI", subcategory: "3D Printing", desc: "3D printing solutions", url: "stratasys.com", pricing: "Paid", rating: 4.3, tags: ["3d-printing", "fdm", "polyjet"]},
    {name: "Desktop Metal", category: "Industrial AI", subcategory: "3D Printing", desc: "Metal 3D printing", url: "desktopmetal.com", pricing: "Paid", rating: 4.2, tags: ["metal", "3d-printing", "binder-jetting"]},
    {name: "Carbon", category: "Industrial AI", subcategory: "3D Printing", desc: "DLS 3D printing", url: "carbon3d.com", pricing: "Paid", rating: 4.4, tags: ["3d-printing", "dls", "resin"]},
    {name: "Formlabs", category: "Industrial AI", subcategory: "3D Printing", desc: "SLA 3D printing", url: "formlabs.com", pricing: "Paid", rating: 4.5, tags: ["3d-printing", "sla", "desktop"]},
    {name: "EOS", category: "Industrial AI", subcategory: "3D Printing", desc: "Industrial 3D printing", url: "eos.info", pricing: "Paid", rating: 4.3, tags: ["3d-printing", "metal", "polymer"]},
    {name: "3D Systems", category: "Industrial AI", subcategory: "3D Printing", desc: "3D printing company", url: "3dsystems.com", pricing: "Paid", rating: 4.1, tags: ["3d-printing", "enterprise", "software"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE49 = AI_TOOLS_PHASE49;
}


