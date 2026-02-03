// AI Tools Database - Phase 60: Miscellaneous & Emerging AI Tools
// 100+ Miscellaneous and emerging AI tools

const AI_TOOLS_PHASE60 = [
    // ==================== SPATIAL COMPUTING ====================
    {name: "Apple Vision Pro", category: "Spatial", subcategory: "Headset", desc: "Spatial computer", url: "apple.com/apple-vision-pro", pricing: "Paid", rating: 4.5, tags: ["spatial", "ar", "vr", "apple"], featured: true},
    {name: "Meta Quest", category: "Spatial", subcategory: "VR", desc: "VR headset", url: "meta.com/quest", pricing: "Paid", rating: 4.4, tags: ["vr", "meta", "gaming"]},
    {name: "Niantic Lightship", category: "Spatial", subcategory: "AR Platform", desc: "AR development", url: "lightship.dev", pricing: "Freemium", rating: 4.2, tags: ["ar", "niantic", "development"]},
    {name: "8th Wall", category: "Spatial", subcategory: "WebAR", desc: "Web-based AR", url: "8thwall.com", pricing: "Paid", rating: 4.3, tags: ["webar", "development", "niantic"]},
    {name: "Zappar", category: "Spatial", subcategory: "AR", desc: "AR platform", url: "zappar.com", pricing: "Paid", rating: 4.1, tags: ["ar", "development", "creative"]},
    {name: "Vuforia", category: "Spatial", subcategory: "AR SDK", desc: "AR development", url: "ptc.com/vuforia", pricing: "Freemium", rating: 4.2, tags: ["ar", "sdk", "enterprise"]},
    {name: "ARKit", category: "Spatial", subcategory: "SDK", desc: "Apple AR framework", url: "developer.apple.com/arkit", pricing: "Free", rating: 4.5, tags: ["ar", "apple", "ios"]},
    {name: "ARCore", category: "Spatial", subcategory: "SDK", desc: "Google AR platform", url: "developers.google.com/ar", pricing: "Free", rating: 4.4, tags: ["ar", "google", "android"]},
    {name: "Spatial", category: "Spatial", subcategory: "Metaverse", desc: "Metaverse platform", url: "spatial.io", pricing: "Freemium", rating: 4.2, tags: ["metaverse", "collaboration", "3d"]},
    {name: "Gather", category: "Spatial", subcategory: "Virtual Space", desc: "Virtual spaces", url: "gather.town", pricing: "Freemium", rating: 4.4, tags: ["virtual", "office", "events"]},
    
    // ==================== QUANTUM COMPUTING ====================
    {name: "IBM Quantum", category: "Quantum", subcategory: "Platform", desc: "Quantum computing", url: "quantum.ibm.com", pricing: "Freemium", rating: 4.4, tags: ["quantum", "ibm", "cloud"], featured: true},
    {name: "Amazon Braket", category: "Quantum", subcategory: "Cloud", desc: "AWS quantum", url: "aws.amazon.com/braket", pricing: "Pay-per-use", rating: 4.2, tags: ["quantum", "aws", "cloud"]},
    {name: "Azure Quantum", category: "Quantum", subcategory: "Cloud", desc: "Microsoft quantum", url: "azure.microsoft.com/quantum", pricing: "Pay-per-use", rating: 4.1, tags: ["quantum", "azure", "cloud"]},
    {name: "Google Quantum AI", category: "Quantum", subcategory: "Research", desc: "Google quantum", url: "quantumai.google", pricing: "Research", rating: 4.3, tags: ["quantum", "google", "research"]},
    {name: "IonQ", category: "Quantum", subcategory: "Hardware", desc: "Trapped ion quantum", url: "ionq.com", pricing: "Paid", rating: 4.2, tags: ["quantum", "hardware", "trapped-ion"]},
    {name: "Rigetti", category: "Quantum", subcategory: "Platform", desc: "Quantum cloud", url: "rigetti.com", pricing: "Pay-per-use", rating: 4.0, tags: ["quantum", "cloud", "superconducting"]},
    {name: "D-Wave", category: "Quantum", subcategory: "Annealing", desc: "Quantum annealing", url: "dwavesys.com", pricing: "Pay-per-use", rating: 4.1, tags: ["quantum", "annealing", "optimization"]},
    {name: "Qiskit", category: "Quantum", subcategory: "SDK", desc: "Quantum SDK", url: "qiskit.org", pricing: "Free", rating: 4.4, tags: ["quantum", "ibm", "python"]},
    {name: "Cirq", category: "Quantum", subcategory: "SDK", desc: "Google quantum SDK", url: "quantumai.google/cirq", pricing: "Free", rating: 4.2, tags: ["quantum", "google", "python"]},
    {name: "PennyLane", category: "Quantum", subcategory: "ML", desc: "Quantum ML", url: "pennylane.ai", pricing: "Free", rating: 4.3, tags: ["quantum-ml", "xanadu", "python"]},
    
    // ==================== BLOCKCHAIN & WEB3 ====================
    {name: "Ethereum", category: "Web3", subcategory: "Blockchain", desc: "Smart contracts", url: "ethereum.org", pricing: "Pay-per-use", rating: 4.6, tags: ["blockchain", "smart-contracts", "defi"], featured: true},
    {name: "Solana", category: "Web3", subcategory: "Blockchain", desc: "Fast blockchain", url: "solana.com", pricing: "Pay-per-use", rating: 4.4, tags: ["blockchain", "fast", "nft"]},
    {name: "Polygon", category: "Web3", subcategory: "Layer 2", desc: "Ethereum scaling", url: "polygon.technology", pricing: "Pay-per-use", rating: 4.4, tags: ["layer2", "scaling", "ethereum"]},
    {name: "Alchemy", category: "Web3", subcategory: "Infrastructure", desc: "Web3 infrastructure", url: "alchemy.com", pricing: "Freemium", rating: 4.5, tags: ["infrastructure", "api", "development"]},
    {name: "Infura", category: "Web3", subcategory: "Infrastructure", desc: "Ethereum API", url: "infura.io", pricing: "Freemium", rating: 4.3, tags: ["api", "ethereum", "consensys"]},
    {name: "Thirdweb", category: "Web3", subcategory: "Development", desc: "Web3 development", url: "thirdweb.com", pricing: "Freemium", rating: 4.4, tags: ["development", "sdk", "nft"]},
    {name: "Moralis", category: "Web3", subcategory: "Development", desc: "Web3 development", url: "moralis.io", pricing: "Freemium", rating: 4.2, tags: ["development", "api", "cross-chain"]},
    {name: "OpenZeppelin", category: "Web3", subcategory: "Security", desc: "Smart contract security", url: "openzeppelin.com", pricing: "Freemium", rating: 4.5, tags: ["security", "contracts", "audit"]},
    {name: "Chainlink", category: "Web3", subcategory: "Oracle", desc: "Blockchain oracle", url: "chain.link", pricing: "Pay-per-use", rating: 4.5, tags: ["oracle", "data", "defi"]},
    {name: "The Graph", category: "Web3", subcategory: "Indexing", desc: "Blockchain indexing", url: "thegraph.com", pricing: "Pay-per-use", rating: 4.3, tags: ["indexing", "query", "graphql"]},
    
    // ==================== ROBOTICS ====================
    {name: "ROS", category: "Robotics", subcategory: "Framework", desc: "Robot Operating System", url: "ros.org", pricing: "Free", rating: 4.6, tags: ["robotics", "open-source", "framework"], featured: true},
    {name: "Isaac Sim", category: "Robotics", subcategory: "Simulation", desc: "NVIDIA robotics sim", url: "developer.nvidia.com/isaac-sim", pricing: "Free", rating: 4.4, tags: ["simulation", "nvidia", "ai"]},
    {name: "Gazebo", category: "Robotics", subcategory: "Simulation", desc: "Robot simulator", url: "gazebosim.org", pricing: "Free", rating: 4.4, tags: ["simulation", "open-source", "ros"]},
    {name: "MuJoCo", category: "Robotics", subcategory: "Physics", desc: "Physics engine", url: "mujoco.org", pricing: "Free", rating: 4.5, tags: ["physics", "deepmind", "simulation"]},
    {name: "PyBullet", category: "Robotics", subcategory: "Simulation", desc: "Python robotics", url: "pybullet.org", pricing: "Free", rating: 4.3, tags: ["simulation", "python", "ai"]},
    {name: "OpenAI Gym", category: "Robotics", subcategory: "RL", desc: "RL environment", url: "gym.openai.com", pricing: "Free", rating: 4.5, tags: ["rl", "environment", "research"]},
    {name: "Gymnasium", category: "Robotics", subcategory: "RL", desc: "RL toolkit", url: "gymnasium.farama.org", pricing: "Free", rating: 4.4, tags: ["rl", "farama", "maintained"]},
    {name: "Hello Robot", category: "Robotics", subcategory: "Hardware", desc: "Mobile manipulator", url: "hello-robot.com", pricing: "Paid", rating: 4.2, tags: ["robot", "mobile", "research"]},
    {name: "Clearpath Robotics", category: "Robotics", subcategory: "Hardware", desc: "Research robots", url: "clearpathrobotics.com", pricing: "Paid", rating: 4.3, tags: ["robots", "research", "outdoor"]},
    {name: "Unitree", category: "Robotics", subcategory: "Quadruped", desc: "Robot dogs", url: "unitree.com", pricing: "Paid", rating: 4.2, tags: ["quadruped", "china", "affordable"]},
    
    // ==================== BIOTECH AI ====================
    {name: "DeepMind AlphaFold", category: "BioTech AI", subcategory: "Protein", desc: "Protein prediction", url: "alphafold.ebi.ac.uk", pricing: "Free", rating: 4.9, tags: ["protein", "deepmind", "breakthrough"], featured: true},
    {name: "Isomorphic Labs", category: "BioTech AI", subcategory: "Drug", desc: "AI drug discovery", url: "isomorphiclabs.com", pricing: "Research", rating: 4.5, tags: ["drug-discovery", "deepmind", "ai"]},
    {name: "Ginkgo Bioworks", category: "BioTech AI", subcategory: "Synth Bio", desc: "Cell programming", url: "ginkgobioworks.com", pricing: "Paid", rating: 4.3, tags: ["synthetic-biology", "cells", "foundry"]},
    {name: "Zymergen", category: "BioTech AI", subcategory: "Materials", desc: "Bio-based materials", url: "zymergen.com", pricing: "Paid", rating: 3.8, tags: ["materials", "fermentation", "bio"]},
    {name: "Inscripta", category: "BioTech AI", subcategory: "Gene Editing", desc: "Gene editing", url: "inscripta.com", pricing: "Paid", rating: 4.1, tags: ["gene-editing", "crispr", "automation"]},
    {name: "Benchling", category: "BioTech AI", subcategory: "R&D", desc: "Life science R&D", url: "benchling.com", pricing: "Paid", rating: 4.5, tags: ["r&d", "cloud", "collaboration"]},
    {name: "Illumina", category: "BioTech AI", subcategory: "Sequencing", desc: "DNA sequencing", url: "illumina.com", pricing: "Paid", rating: 4.6, tags: ["sequencing", "genomics", "leader"]},
    {name: "10x Genomics", category: "BioTech AI", subcategory: "Single Cell", desc: "Single cell analysis", url: "10xgenomics.com", pricing: "Paid", rating: 4.5, tags: ["single-cell", "genomics", "spatial"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE60 = AI_TOOLS_PHASE60;
}


