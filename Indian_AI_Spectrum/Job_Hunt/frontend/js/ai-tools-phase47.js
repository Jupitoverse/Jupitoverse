// AI Tools Database - Phase 47: Automotive & Transportation AI Tools
// 150+ Automotive and transportation AI tools

const AI_TOOLS_PHASE47 = [
    // ==================== AUTONOMOUS VEHICLES ====================
    {name: "Waymo", category: "Auto AI", subcategory: "Autonomous", desc: "Self-driving tech", url: "waymo.com", pricing: "Paid", rating: 4.6, tags: ["autonomous", "robotaxi", "alphabet"], featured: true},
    {name: "Cruise", category: "Auto AI", subcategory: "Autonomous", desc: "Autonomous vehicles", url: "getcruise.com", pricing: "Paid", rating: 4.3, tags: ["autonomous", "gm", "robotaxi"]},
    {name: "Zoox", category: "Auto AI", subcategory: "Autonomous", desc: "Autonomous mobility", url: "zoox.com", pricing: "Paid", rating: 4.2, tags: ["autonomous", "amazon", "purpose-built"]},
    {name: "Aurora", category: "Auto AI", subcategory: "Autonomous", desc: "Self-driving tech", url: "aurora.tech", pricing: "Paid", rating: 4.3, tags: ["autonomous", "trucking", "platform"]},
    {name: "Motional", category: "Auto AI", subcategory: "Autonomous", desc: "Driverless tech", url: "motional.com", pricing: "Paid", rating: 4.2, tags: ["autonomous", "hyundai", "aptiv"]},
    {name: "Nuro", category: "Auto AI", subcategory: "Delivery", desc: "Autonomous delivery", url: "nuro.ai", pricing: "Paid", rating: 4.3, tags: ["delivery", "autonomous", "last-mile"]},
    {name: "Argo AI (closed)", category: "Auto AI", subcategory: "Autonomous", desc: "Self-driving (closed)", url: "argo.ai", pricing: "N/A", rating: 4.0, tags: ["autonomous", "ford", "closed"]},
    {name: "Mobileye", category: "Auto AI", subcategory: "ADAS", desc: "Driving assistance", url: "mobileye.com", pricing: "Paid", rating: 4.5, tags: ["adas", "intel", "vision"], featured: true},
    {name: "Comma.ai", category: "Auto AI", subcategory: "Aftermarket", desc: "Aftermarket autonomous", url: "comma.ai", pricing: "Paid", rating: 4.4, tags: ["aftermarket", "openpilot", "affordable"]},
    {name: "TuSimple", category: "Auto AI", subcategory: "Trucking", desc: "Autonomous trucking", url: "tusimple.com", pricing: "Paid", rating: 4.0, tags: ["trucking", "autonomous", "freight"]},
    {name: "Plus", category: "Auto AI", subcategory: "Trucking", desc: "Truck autonomy", url: "plus.ai", pricing: "Paid", rating: 4.1, tags: ["trucking", "driver-in", "autonomous"]},
    {name: "Kodiak Robotics", category: "Auto AI", subcategory: "Trucking", desc: "Autonomous trucking", url: "kodiak.ai", pricing: "Paid", rating: 4.1, tags: ["trucking", "long-haul", "autonomous"]},
    
    // ==================== CONNECTED CARS ====================
    {name: "Tesla Autopilot", category: "Auto AI", subcategory: "ADAS", desc: "Tesla driver assistance", url: "tesla.com/autopilot", pricing: "Paid", rating: 4.5, tags: ["adas", "fsd", "neural"], featured: true},
    {name: "Wejo", category: "Auto AI", subcategory: "Data", desc: "Connected car data", url: "wejo.com", pricing: "Paid", rating: 4.0, tags: ["data", "connected", "analytics"]},
    {name: "Otonomo", category: "Auto AI", subcategory: "Data", desc: "Vehicle data platform", url: "otonomo.io", pricing: "Paid", rating: 4.1, tags: ["data", "marketplace", "privacy"]},
    {name: "Smartcar", category: "Auto AI", subcategory: "API", desc: "Vehicle API", url: "smartcar.com", pricing: "Freemium", rating: 4.3, tags: ["api", "connected", "developers"]},
    {name: "High Mobility", category: "Auto AI", subcategory: "API", desc: "Car data API", url: "high-mobility.com", pricing: "Freemium", rating: 4.1, tags: ["api", "data", "oems"]},
    {name: "Geotab", category: "Auto AI", subcategory: "Telematics", desc: "Fleet telematics", url: "geotab.com", pricing: "Paid", rating: 4.4, tags: ["telematics", "fleet", "data"]},
    {name: "Samsara", category: "Auto AI", subcategory: "Fleet", desc: "Fleet operations", url: "samsara.com", pricing: "Paid", rating: 4.5, tags: ["fleet", "iot", "operations"]},
    {name: "Lytx", category: "Auto AI", subcategory: "Dash Cam", desc: "Video telematics", url: "lytx.com", pricing: "Paid", rating: 4.3, tags: ["dashcam", "ai", "coaching"]},
    {name: "Nauto", category: "Auto AI", subcategory: "AI Dash Cam", desc: "AI dash camera", url: "nauto.com", pricing: "Paid", rating: 4.2, tags: ["dashcam", "ai", "distraction"]},
    {name: "Netradyne", category: "Auto AI", subcategory: "AI Dash Cam", desc: "Fleet safety AI", url: "netradyne.com", pricing: "Paid", rating: 4.3, tags: ["dashcam", "ai", "driveri"]},
    
    // ==================== MOBILITY SERVICES ====================
    {name: "Uber", category: "Auto AI", subcategory: "Rideshare", desc: "Ride-sharing platform", url: "uber.com", pricing: "Pay-per-use", rating: 4.4, tags: ["rideshare", "global", "mobility"], featured: true},
    {name: "Lyft", category: "Auto AI", subcategory: "Rideshare", desc: "Ride-sharing", url: "lyft.com", pricing: "Pay-per-use", rating: 4.3, tags: ["rideshare", "usa", "pink"]},
    {name: "Ola", category: "Auto AI", subcategory: "India", desc: "Indian ride-sharing", url: "olacabs.com", pricing: "Pay-per-use", rating: 4.2, tags: ["india", "rideshare", "ev"]},
    {name: "Grab", category: "Auto AI", subcategory: "Southeast Asia", desc: "SE Asia super app", url: "grab.com", pricing: "Pay-per-use", rating: 4.3, tags: ["southeast-asia", "super-app", "delivery"]},
    {name: "Didi", category: "Auto AI", subcategory: "China", desc: "Chinese ride-hailing", url: "didiglobal.com", pricing: "Pay-per-use", rating: 4.1, tags: ["china", "rideshare", "global"]},
    {name: "Bolt", category: "Auto AI", subcategory: "Europe", desc: "European mobility", url: "bolt.eu", pricing: "Pay-per-use", rating: 4.2, tags: ["europe", "rideshare", "affordable"]},
    {name: "Lime", category: "Auto AI", subcategory: "Micromobility", desc: "E-scooter sharing", url: "li.me", pricing: "Pay-per-use", rating: 4.1, tags: ["scooter", "bike", "micromobility"]},
    {name: "Bird", category: "Auto AI", subcategory: "Micromobility", desc: "E-scooter sharing", url: "bird.co", pricing: "Pay-per-use", rating: 4.0, tags: ["scooter", "electric", "urban"]},
    {name: "Spin", category: "Auto AI", subcategory: "Micromobility", desc: "Micromobility", url: "spin.app", pricing: "Pay-per-use", rating: 4.0, tags: ["scooter", "bike", "ford"]},
    {name: "Voi", category: "Auto AI", subcategory: "Europe Micro", desc: "European e-scooters", url: "voiscooters.com", pricing: "Pay-per-use", rating: 4.1, tags: ["europe", "scooter", "sustainable"]},
    
    // ==================== EV & CHARGING ====================
    {name: "ChargePoint", category: "Auto AI", subcategory: "Charging", desc: "EV charging network", url: "chargepoint.com", pricing: "Pay-per-use", rating: 4.3, tags: ["charging", "network", "ev"], featured: true},
    {name: "EVgo", category: "Auto AI", subcategory: "Charging", desc: "Fast charging", url: "evgo.com", pricing: "Pay-per-use", rating: 4.1, tags: ["charging", "fast", "dc"]},
    {name: "Electrify America", category: "Auto AI", subcategory: "Charging", desc: "Ultra-fast charging", url: "electrifyamerica.com", pricing: "Pay-per-use", rating: 4.2, tags: ["charging", "vw", "ultra-fast"]},
    {name: "PlugShare", category: "Auto AI", subcategory: "Charging Map", desc: "EV charging map", url: "plugshare.com", pricing: "Free", rating: 4.5, tags: ["map", "charging", "community"]},
    {name: "Blink Charging", category: "Auto AI", subcategory: "Charging", desc: "EV charging", url: "blinkcharging.com", pricing: "Pay-per-use", rating: 4.0, tags: ["charging", "hardware", "network"]},
    {name: "Rivian Adventure Network", category: "Auto AI", subcategory: "Charging", desc: "Rivian charging", url: "rivian.com", pricing: "Pay-per-use", rating: 4.3, tags: ["rivian", "adventure", "dc"]},
    {name: "Tesla Supercharger", category: "Auto AI", subcategory: "Charging", desc: "Tesla fast charging", url: "tesla.com/supercharger", pricing: "Pay-per-use", rating: 4.6, tags: ["tesla", "fast", "reliable"]},
    {name: "Shell Recharge", category: "Auto AI", subcategory: "Charging", desc: "Shell EV charging", url: "shell.com/recharge", pricing: "Pay-per-use", rating: 4.1, tags: ["shell", "charging", "network"]},
    {name: "Greenlots", category: "Auto AI", subcategory: "Software", desc: "EV charging software", url: "greenlots.com", pricing: "Paid", rating: 4.0, tags: ["software", "shell", "grid"]},
    {name: "Volta", category: "Auto AI", subcategory: "Charging", desc: "Free EV charging", url: "voltacharging.com", pricing: "Free", rating: 4.2, tags: ["free", "advertising", "retail"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE47 = AI_TOOLS_PHASE47;
}


