// AI Tools Database - Phase 32: Additional Specialized Tools
// 150+ More specialized AI tools

const AI_TOOLS_PHASE32 = [
    // ==================== SPEECH & VOICE ====================
    {name: "Whisper", category: "Speech", subcategory: "Transcription", desc: "OpenAI speech recognition", url: "openai.com/whisper", pricing: "Free", rating: 4.7, tags: ["transcription", "openai", "multilingual"], featured: true},
    {name: "Deepgram", category: "Speech", subcategory: "API", desc: "Speech recognition API", url: "deepgram.com", pricing: "Freemium", rating: 4.5, tags: ["api", "real-time", "accurate"]},
    {name: "AssemblyAI", category: "Speech", subcategory: "API", desc: "Speech-to-text API", url: "assemblyai.com", pricing: "Freemium", rating: 4.5, tags: ["api", "transcription", "understanding"]},
    {name: "Rev.ai", category: "Speech", subcategory: "Transcription", desc: "Speech recognition", url: "rev.ai", pricing: "Pay-per-use", rating: 4.3, tags: ["transcription", "api", "accurate"]},
    {name: "Speechmatics", category: "Speech", subcategory: "API", desc: "Speech recognition API", url: "speechmatics.com", pricing: "Paid", rating: 4.3, tags: ["api", "multilingual", "enterprise"]},
    {name: "AWS Transcribe", category: "Speech", subcategory: "AWS", desc: "AWS speech-to-text", url: "aws.amazon.com/transcribe", pricing: "Pay-per-use", rating: 4.3, tags: ["aws", "transcription", "real-time"]},
    {name: "Google Speech-to-Text", category: "Speech", subcategory: "Google", desc: "Google transcription", url: "cloud.google.com/speech-to-text", pricing: "Pay-per-use", rating: 4.4, tags: ["google", "transcription", "accurate"]},
    {name: "Azure Speech", category: "Speech", subcategory: "Azure", desc: "Microsoft speech services", url: "azure.microsoft.com/speech", pricing: "Pay-per-use", rating: 4.3, tags: ["azure", "speech", "translation"]},
    {name: "Picovoice", category: "Speech", subcategory: "On-device", desc: "On-device voice AI", url: "picovoice.ai", pricing: "Freemium", rating: 4.3, tags: ["on-device", "privacy", "wake-word"]},
    {name: "Coqui TTS", category: "Speech", subcategory: "TTS", desc: "Open source TTS", url: "coqui.ai", pricing: "Free", rating: 4.3, tags: ["tts", "open-source", "cloning"]},
    {name: "Tortoise TTS", category: "Speech", subcategory: "TTS", desc: "Quality TTS model", url: "github.com/neonbjb/tortoise-tts", pricing: "Free", rating: 4.4, tags: ["tts", "quality", "open-source"]},
    {name: "Bark", category: "Speech", subcategory: "TTS", desc: "Text-to-audio model", url: "github.com/suno-ai/bark", pricing: "Free", rating: 4.4, tags: ["tts", "music", "effects"]},
    {name: "Parler TTS", category: "Speech", subcategory: "TTS", desc: "Controllable TTS", url: "huggingface.co/parler-tts", pricing: "Free", rating: 4.2, tags: ["tts", "controllable", "open-source"]},
    {name: "Piper TTS", category: "Speech", subcategory: "TTS", desc: "Fast local TTS", url: "github.com/rhasspy/piper", pricing: "Free", rating: 4.3, tags: ["tts", "fast", "local"]},
    {name: "Vosk", category: "Speech", subcategory: "Offline", desc: "Offline speech recognition", url: "alphacephei.com/vosk", pricing: "Free", rating: 4.2, tags: ["offline", "lightweight", "multilingual"]},
    
    // ==================== ROBOTICS & EDGE AI ====================
    {name: "NVIDIA Isaac", category: "Robotics", subcategory: "Platform", desc: "Robotics development", url: "developer.nvidia.com/isaac", pricing: "Freemium", rating: 4.4, tags: ["robotics", "nvidia", "simulation"]},
    {name: "ROS", category: "Robotics", subcategory: "Framework", desc: "Robot Operating System", url: "ros.org", pricing: "Free", rating: 4.5, tags: ["open-source", "robotics", "middleware"]},
    {name: "ROS 2", category: "Robotics", subcategory: "Framework", desc: "Next-gen ROS", url: "ros.org", pricing: "Free", rating: 4.4, tags: ["robotics", "real-time", "modern"]},
    {name: "Gazebo", category: "Robotics", subcategory: "Simulation", desc: "Robot simulation", url: "gazebosim.org", pricing: "Free", rating: 4.3, tags: ["simulation", "physics", "open-source"]},
    {name: "MuJoCo", category: "Robotics", subcategory: "Physics", desc: "Physics engine", url: "mujoco.org", pricing: "Free", rating: 4.5, tags: ["physics", "simulation", "deepmind"]},
    {name: "IsaacGym", category: "Robotics", subcategory: "Training", desc: "GPU robot training", url: "developer.nvidia.com/isaac-gym", pricing: "Free", rating: 4.4, tags: ["training", "gpu", "rl"]},
    {name: "Edge Impulse", category: "Edge AI", subcategory: "Platform", desc: "Edge ML platform", url: "edgeimpulse.com", pricing: "Freemium", rating: 4.5, tags: ["edge", "embedded", "tinyml"]},
    {name: "TensorFlow Lite", category: "Edge AI", subcategory: "Framework", desc: "Mobile ML framework", url: "tensorflow.org/lite", pricing: "Free", rating: 4.4, tags: ["mobile", "edge", "lightweight"]},
    {name: "ONNX Runtime", category: "Edge AI", subcategory: "Runtime", desc: "Cross-platform ML", url: "onnxruntime.ai", pricing: "Free", rating: 4.5, tags: ["runtime", "cross-platform", "performance"]},
    {name: "TensorRT", category: "Edge AI", subcategory: "Inference", desc: "NVIDIA inference", url: "developer.nvidia.com/tensorrt", pricing: "Free", rating: 4.5, tags: ["inference", "nvidia", "optimization"]},
    {name: "OpenVINO", category: "Edge AI", subcategory: "Toolkit", desc: "Intel edge AI", url: "intel.com/openvino", pricing: "Free", rating: 4.3, tags: ["intel", "inference", "optimization"]},
    {name: "Apache TVM", category: "Edge AI", subcategory: "Compiler", desc: "ML compiler", url: "tvm.apache.org", pricing: "Free", rating: 4.2, tags: ["compiler", "optimization", "hardware"]},
    {name: "MNN", category: "Edge AI", subcategory: "Framework", desc: "Mobile neural network", url: "github.com/alibaba/MNN", pricing: "Free", rating: 4.1, tags: ["mobile", "alibaba", "lightweight"]},
    {name: "NCNN", category: "Edge AI", subcategory: "Framework", desc: "Mobile inference", url: "github.com/Tencent/ncnn", pricing: "Free", rating: 4.2, tags: ["mobile", "tencent", "optimized"]},
    {name: "MediaPipe", category: "Edge AI", subcategory: "Solutions", desc: "Google ML solutions", url: "mediapipe.dev", pricing: "Free", rating: 4.5, tags: ["solutions", "google", "real-time"]},
    
    // ==================== SIMULATION & SYNTHETIC DATA ====================
    {name: "NVIDIA Omniverse", category: "Simulation", subcategory: "Platform", desc: "3D simulation platform", url: "nvidia.com/omniverse", pricing: "Freemium", rating: 4.5, tags: ["3d", "simulation", "nvidia"]},
    {name: "Unity Simulation", category: "Simulation", subcategory: "Engine", desc: "Unity ML simulation", url: "unity.com/solutions/simulation", pricing: "Paid", rating: 4.3, tags: ["simulation", "unity", "training"]},
    {name: "Parallel Domain", category: "Simulation", subcategory: "Synthetic", desc: "Synthetic data for AV", url: "paralleldomain.com", pricing: "Paid", rating: 4.2, tags: ["synthetic", "autonomous", "data"]},
    {name: "Rendered.ai", category: "Simulation", subcategory: "Synthetic", desc: "Synthetic data platform", url: "rendered.ai", pricing: "Paid", rating: 4.1, tags: ["synthetic", "data", "generation"]},
    {name: "AI.Reverie", category: "Simulation", subcategory: "Synthetic", desc: "Synthetic data", url: "aireverie.com", pricing: "Paid", rating: 4.1, tags: ["synthetic", "computer-vision", "training"]},
    {name: "Datagen", category: "Simulation", subcategory: "Synthetic", desc: "Synthetic people data", url: "datagen.tech", pricing: "Paid", rating: 4.2, tags: ["synthetic", "people", "faces"]},
    {name: "Synthesis AI", category: "Simulation", subcategory: "Synthetic", desc: "Synthetic data for vision", url: "synthesis.ai", pricing: "Paid", rating: 4.2, tags: ["synthetic", "faces", "vision"]},
    {name: "Gretel.ai", category: "Simulation", subcategory: "Synthetic", desc: "Synthetic data platform", url: "gretel.ai", pricing: "Freemium", rating: 4.3, tags: ["synthetic", "privacy", "tabular"]},
    {name: "Mostly AI", category: "Simulation", subcategory: "Synthetic", desc: "Synthetic tabular data", url: "mostly.ai", pricing: "Freemium", rating: 4.2, tags: ["synthetic", "tabular", "privacy"]},
    {name: "Hazy", category: "Simulation", subcategory: "Synthetic", desc: "Synthetic data for enterprise", url: "hazy.com", pricing: "Paid", rating: 4.1, tags: ["synthetic", "enterprise", "privacy"]},
    
    // ==================== AI ETHICS & GOVERNANCE ====================
    {name: "AI Fairness 360", category: "AI Ethics", subcategory: "Toolkit", desc: "IBM fairness toolkit", url: "aif360.mybluemix.net", pricing: "Free", rating: 4.3, tags: ["fairness", "ibm", "open-source"]},
    {name: "Fairlearn", category: "AI Ethics", subcategory: "Library", desc: "Fairness assessment", url: "fairlearn.org", pricing: "Free", rating: 4.3, tags: ["fairness", "microsoft", "python"]},
    {name: "What-If Tool", category: "AI Ethics", subcategory: "Visualization", desc: "Google ML probing", url: "pair-code.github.io/what-if-tool", pricing: "Free", rating: 4.2, tags: ["visualization", "google", "probing"]},
    {name: "Alibi", category: "AI Ethics", subcategory: "Explainability", desc: "ML explanations", url: "docs.seldon.io/projects/alibi", pricing: "Free", rating: 4.2, tags: ["explainability", "interpretability", "open-source"]},
    {name: "SHAP", category: "AI Ethics", subcategory: "Explainability", desc: "Model explanations", url: "shap.readthedocs.io", pricing: "Free", rating: 4.5, tags: ["explainability", "shapley", "popular"]},
    {name: "LIME", category: "AI Ethics", subcategory: "Explainability", desc: "Local interpretable explanations", url: "github.com/marcotcr/lime", pricing: "Free", rating: 4.3, tags: ["explainability", "local", "interpretable"]},
    {name: "InterpretML", category: "AI Ethics", subcategory: "Explainability", desc: "Microsoft interpretability", url: "interpret.ml", pricing: "Free", rating: 4.3, tags: ["explainability", "microsoft", "glassbox"]},
    {name: "Captum", category: "AI Ethics", subcategory: "Explainability", desc: "PyTorch interpretability", url: "captum.ai", pricing: "Free", rating: 4.2, tags: ["pytorch", "attribution", "interpretability"]},
    {name: "TruEra", category: "AI Ethics", subcategory: "Quality", desc: "AI quality management", url: "truera.com", pricing: "Paid", rating: 4.2, tags: ["quality", "monitoring", "explainability"]},
    {name: "Credo AI", category: "AI Ethics", subcategory: "Governance", desc: "AI governance platform", url: "credo.ai", pricing: "Paid", rating: 4.1, tags: ["governance", "risk", "compliance"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE32 = AI_TOOLS_PHASE32;
}


