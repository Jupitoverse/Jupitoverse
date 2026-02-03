// AI Tools Database - Phase 78: More IoT, Robotics & Hardware AI
// 80+ Additional IoT, robotics and hardware tools

const AI_TOOLS_PHASE78 = [
    // ==================== IOT PLATFORMS ====================
    {name: "AWS IoT", category: "IoT", subcategory: "Platform", desc: "AWS IoT services", url: "aws.amazon.com/iot", pricing: "Pay-per-use", rating: 4.5, tags: ["cloud", "aws", "enterprise"], featured: true},
    {name: "Azure IoT Hub", category: "IoT", subcategory: "Platform", desc: "Microsoft IoT", url: "azure.microsoft.com/iot-hub", pricing: "Pay-per-use", rating: 4.4, tags: ["cloud", "azure", "enterprise"]},
    {name: "Google Cloud IoT", category: "IoT", subcategory: "Platform", desc: "Google IoT", url: "cloud.google.com/iot", pricing: "Pay-per-use", rating: 4.3, tags: ["cloud", "google", "ai"]},
    {name: "Particle", category: "IoT", subcategory: "Platform", desc: "IoT development", url: "particle.io", pricing: "Freemium", rating: 4.4, tags: ["hardware", "development", "enterprise"]},
    {name: "Losant", category: "IoT", subcategory: "Platform", desc: "Enterprise IoT", url: "losant.com", pricing: "Freemium", rating: 4.2, tags: ["enterprise", "platform", "visualization"]},
    {name: "ThingSpeak", category: "IoT", subcategory: "Platform", desc: "IoT analytics", url: "thingspeak.com", pricing: "Freemium", rating: 4.1, tags: ["mathworks", "matlab", "analytics"]},
    {name: "Blynk", category: "IoT", subcategory: "Platform", desc: "IoT app builder", url: "blynk.io", pricing: "Freemium", rating: 4.3, tags: ["mobile", "no-code", "easy"]},
    {name: "Ubidots", category: "IoT", subcategory: "Platform", desc: "IoT platform", url: "ubidots.com", pricing: "Freemium", rating: 4.2, tags: ["dashboards", "analytics", "industrial"]},
    {name: "ThingsBoard", category: "IoT", subcategory: "Platform", desc: "Open-source IoT", url: "thingsboard.io", pricing: "Freemium", rating: 4.3, tags: ["open-source", "platform", "visualization"]},
    {name: "Node-RED", category: "IoT", subcategory: "Flow", desc: "Flow-based IoT", url: "nodered.org", pricing: "Free", rating: 4.4, tags: ["flow", "open-source", "visual"]},
    
    // ==================== EDGE AI ====================
    {name: "NVIDIA Jetson", category: "IoT", subcategory: "Edge AI", desc: "Edge AI computing", url: "nvidia.com/jetson", pricing: "Paid", rating: 4.6, tags: ["edge", "nvidia", "gpu"], featured: true},
    {name: "Intel Neural Compute Stick", category: "IoT", subcategory: "Edge AI", desc: "Edge inference", url: "intel.com/neural-compute-stick", pricing: "Paid", rating: 4.2, tags: ["edge", "intel", "inference"]},
    {name: "Google Coral", category: "IoT", subcategory: "Edge AI", desc: "Edge TPU", url: "coral.ai", pricing: "Paid", rating: 4.3, tags: ["edge", "tpu", "google"]},
    {name: "Edge Impulse", category: "IoT", subcategory: "TinyML", desc: "Embedded ML", url: "edgeimpulse.com", pricing: "Freemium", rating: 4.4, tags: ["tinyml", "embedded", "ml"]},
    {name: "TensorFlow Lite", category: "IoT", subcategory: "Mobile ML", desc: "Mobile ML framework", url: "tensorflow.org/lite", pricing: "Free", rating: 4.5, tags: ["mobile", "edge", "tensorflow"]},
    {name: "ONNX Runtime", category: "IoT", subcategory: "Inference", desc: "Cross-platform ML", url: "onnxruntime.ai", pricing: "Free", rating: 4.4, tags: ["inference", "cross-platform", "optimization"]},
    {name: "OpenVINO", category: "IoT", subcategory: "Inference", desc: "Intel inference", url: "docs.openvino.ai", pricing: "Free", rating: 4.3, tags: ["inference", "intel", "optimization"]},
    {name: "Qualcomm AI Engine", category: "IoT", subcategory: "Mobile AI", desc: "Mobile AI platform", url: "qualcomm.com/ai", pricing: "Paid", rating: 4.2, tags: ["mobile", "snapdragon", "edge"]},
    
    // ==================== ROBOTICS ====================
    {name: "ROS (Robot OS)", category: "Robotics", subcategory: "Framework", desc: "Robot operating system", url: "ros.org", pricing: "Free", rating: 4.6, tags: ["framework", "open-source", "robotics"], featured: true},
    {name: "ROS 2", category: "Robotics", subcategory: "Framework", desc: "Next-gen ROS", url: "docs.ros.org/ros2", pricing: "Free", rating: 4.5, tags: ["framework", "open-source", "modern"]},
    {name: "Gazebo", category: "Robotics", subcategory: "Simulation", desc: "Robot simulation", url: "gazebosim.org", pricing: "Free", rating: 4.4, tags: ["simulation", "open-source", "3d"]},
    {name: "NVIDIA Isaac", category: "Robotics", subcategory: "Simulation", desc: "Robot simulation", url: "developer.nvidia.com/isaac-sim", pricing: "Free", rating: 4.5, tags: ["simulation", "nvidia", "ai"]},
    {name: "MoveIt", category: "Robotics", subcategory: "Motion Planning", desc: "Motion planning", url: "moveit.ros.org", pricing: "Free", rating: 4.4, tags: ["motion", "ros", "manipulation"]},
    {name: "OpenCV", category: "Robotics", subcategory: "Vision", desc: "Computer vision", url: "opencv.org", pricing: "Free", rating: 4.7, tags: ["vision", "open-source", "library"]},
    {name: "Boston Dynamics", category: "Robotics", subcategory: "Robots", desc: "Advanced robots", url: "bostondynamics.com", pricing: "Enterprise", rating: 4.6, tags: ["robots", "spot", "atlas"]},
    {name: "Universal Robots", category: "Robotics", subcategory: "Cobots", desc: "Collaborative robots", url: "universal-robots.com", pricing: "Paid", rating: 4.5, tags: ["cobots", "industrial", "arm"]},
    {name: "ABB Robotics", category: "Robotics", subcategory: "Industrial", desc: "Industrial robots", url: "abb.com/robotics", pricing: "Enterprise", rating: 4.4, tags: ["industrial", "automation", "arm"]},
    {name: "Fetch Robotics", category: "Robotics", subcategory: "Warehouse", desc: "Warehouse robots", url: "fetchrobotics.com", pricing: "Enterprise", rating: 4.2, tags: ["warehouse", "amr", "logistics"]},
    
    // ==================== SMART HOME ====================
    {name: "Home Assistant", category: "IoT", subcategory: "Smart Home", desc: "Open home automation", url: "home-assistant.io", pricing: "Free", rating: 4.7, tags: ["smart-home", "open-source", "local"], featured: true},
    {name: "SmartThings", category: "IoT", subcategory: "Smart Home", desc: "Samsung smart home", url: "smartthings.com", pricing: "Free", rating: 4.3, tags: ["smart-home", "samsung", "hub"]},
    {name: "Apple HomeKit", category: "IoT", subcategory: "Smart Home", desc: "Apple home", url: "apple.com/homekit", pricing: "Free", rating: 4.4, tags: ["smart-home", "apple", "siri"]},
    {name: "Google Home", category: "IoT", subcategory: "Smart Home", desc: "Google smart home", url: "home.google.com", pricing: "Free", rating: 4.4, tags: ["smart-home", "google", "assistant"]},
    {name: "Amazon Alexa", category: "IoT", subcategory: "Smart Home", desc: "Amazon smart home", url: "alexa.amazon.com", pricing: "Free", rating: 4.4, tags: ["smart-home", "amazon", "voice"]},
    {name: "Hubitat", category: "IoT", subcategory: "Smart Home", desc: "Local automation", url: "hubitat.com", pricing: "Paid", rating: 4.3, tags: ["smart-home", "local", "hub"]},
    {name: "Homey", category: "IoT", subcategory: "Smart Home", desc: "Smart home hub", url: "homey.app", pricing: "Paid", rating: 4.2, tags: ["smart-home", "hub", "flow"]},
    
    // ==================== HARDWARE DESIGN ====================
    {name: "Arduino", category: "IoT", subcategory: "Hardware", desc: "Open-source electronics", url: "arduino.cc", pricing: "Paid", rating: 4.7, tags: ["hardware", "open-source", "maker"], featured: true},
    {name: "Raspberry Pi", category: "IoT", subcategory: "Hardware", desc: "Single-board computer", url: "raspberrypi.org", pricing: "Paid", rating: 4.8, tags: ["sbc", "linux", "maker"]},
    {name: "ESP32", category: "IoT", subcategory: "Hardware", desc: "WiFi/BT microcontroller", url: "espressif.com/esp32", pricing: "Paid", rating: 4.6, tags: ["wifi", "bluetooth", "low-cost"]},
    {name: "Adafruit", category: "IoT", subcategory: "Hardware", desc: "Electronics & tutorials", url: "adafruit.com", pricing: "Paid", rating: 4.6, tags: ["electronics", "tutorials", "maker"]},
    {name: "SparkFun", category: "IoT", subcategory: "Hardware", desc: "Electronics components", url: "sparkfun.com", pricing: "Paid", rating: 4.5, tags: ["electronics", "tutorials", "maker"]},
    {name: "Seeed Studio", category: "IoT", subcategory: "Hardware", desc: "IoT hardware", url: "seeedstudio.com", pricing: "Paid", rating: 4.3, tags: ["hardware", "grove", "iot"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE78 = AI_TOOLS_PHASE78;
}


