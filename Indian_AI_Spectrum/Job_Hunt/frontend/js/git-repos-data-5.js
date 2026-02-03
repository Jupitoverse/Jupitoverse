// Additional Git Repositories Database - Part 5
// Final collection with specialized and emerging projects

const GIT_REPOS_DATABASE_5 = {
    // ==================== ROBOTICS & HARDWARE ====================
    robotics: [
        {name: "ROS 2", org: "ros2", desc: "Robot Operating System", url: "https://github.com/ros2/ros2", stars: "3K+", language: "Python", topics: ["robotics", "middleware", "autonomous"], difficulty: "Advanced", featured: true},
        {name: "PX4 Autopilot", org: "PX4", desc: "Flight control for drones", url: "https://github.com/PX4/PX4-Autopilot", stars: "7K+", language: "C++", topics: ["drones", "autopilot", "flight"], difficulty: "Advanced", featured: true},
        {name: "OpenCV Contrib", org: "opencv", desc: "Extra OpenCV modules", url: "https://github.com/opencv/opencv_contrib", stars: "9K+", language: "C++", topics: ["computer-vision", "robotics"], difficulty: "Advanced", featured: false},
        {name: "Isaac ROS", org: "NVIDIA-ISAAC-ROS", desc: "NVIDIA robotics packages", url: "https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common", stars: "800+", language: "C++", topics: ["nvidia", "robotics", "gpu"], difficulty: "Advanced", featured: true},
        {name: "Open3D", org: "isl-org", desc: "3D data processing library", url: "https://github.com/isl-org/Open3D", stars: "10K+", language: "C++", topics: ["3d", "point-cloud", "reconstruction"], difficulty: "Advanced", featured: true},
        {name: "Drake", org: "RobotLocomotion", desc: "Planning and control for robots", url: "https://github.com/RobotLocomotion/drake", stars: "3K+", language: "C++", topics: ["robotics", "simulation", "control"], difficulty: "Advanced", featured: false},
        {name: "PyBullet", org: "bulletphysics", desc: "Physics simulation for robotics", url: "https://github.com/bulletphysics/bullet3", stars: "12K+", language: "C++", topics: ["physics", "simulation", "robotics"], difficulty: "Advanced", featured: false},
        {name: "CARLA", org: "carla-simulator", desc: "Autonomous driving simulator", url: "https://github.com/carla-simulator/carla", stars: "10K+", language: "C++", topics: ["autonomous-driving", "simulation"], difficulty: "Advanced", featured: true},
    ],

    // ==================== SCIENCE & RESEARCH ====================
    science: [
        {name: "NumPy", org: "numpy", desc: "Fundamental package for scientific computing", url: "https://github.com/numpy/numpy", stars: "26K+", language: "Python", topics: ["scientific", "arrays", "math"], difficulty: "Beginner", featured: true},
        {name: "SciPy", org: "scipy", desc: "Scientific computing library", url: "https://github.com/scipy/scipy", stars: "12K+", language: "Python", topics: ["scientific", "optimization", "signal"], difficulty: "Intermediate", featured: true},
        {name: "Matplotlib", org: "matplotlib", desc: "Plotting library for Python", url: "https://github.com/matplotlib/matplotlib", stars: "19K+", language: "Python", topics: ["visualization", "plotting", "charts"], difficulty: "Beginner", featured: true},
        {name: "Pandas", org: "pandas-dev", desc: "Data analysis library", url: "https://github.com/pandas-dev/pandas", stars: "42K+", language: "Python", topics: ["data-analysis", "dataframe", "tabular"], difficulty: "Beginner", featured: true},
        {name: "Jupyter", org: "jupyter", desc: "Interactive computing notebooks", url: "https://github.com/jupyter/jupyter", stars: "15K+", language: "Python", topics: ["notebooks", "interactive", "research"], difficulty: "Beginner", featured: true},
        {name: "SymPy", org: "sympy", desc: "Symbolic mathematics library", url: "https://github.com/sympy/sympy", stars: "12K+", language: "Python", topics: ["symbolic-math", "algebra", "calculus"], difficulty: "Intermediate", featured: false},
        {name: "Seaborn", org: "mwaskom", desc: "Statistical data visualization", url: "https://github.com/mwaskom/seaborn", stars: "12K+", language: "Python", topics: ["visualization", "statistics", "plots"], difficulty: "Beginner", featured: false},
        {name: "Plotly", org: "plotly", desc: "Interactive graphing library", url: "https://github.com/plotly/plotly.py", stars: "15K+", language: "Python", topics: ["visualization", "interactive", "3d"], difficulty: "Beginner", featured: true},
        {name: "Altair", org: "altair-viz", desc: "Declarative statistical visualization", url: "https://github.com/altair-viz/altair", stars: "9K+", language: "Python", topics: ["visualization", "vega", "declarative"], difficulty: "Beginner", featured: false},
        {name: "Bokeh", org: "bokeh", desc: "Interactive visualization library", url: "https://github.com/bokeh/bokeh", stars: "19K+", language: "Python", topics: ["visualization", "interactive", "web"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== 3D & GRAPHICS PROGRAMMING ====================
    graphics_3d: [
        {name: "Blender", org: "blender", desc: "3D creation suite", url: "https://github.com/blender/blender", stars: "12K+", language: "C/C++", topics: ["3d", "modeling", "animation"], difficulty: "Advanced", featured: true},
        {name: "FreeCAD", org: "FreeCAD", desc: "3D parametric modeler", url: "https://github.com/FreeCAD/FreeCAD", stars: "17K+", language: "C++", topics: ["cad", "3d", "parametric"], difficulty: "Advanced", featured: true},
        {name: "OpenSCAD", org: "openscad", desc: "Programmable CAD modeller", url: "https://github.com/openscad/openscad", stars: "6K+", language: "C++", topics: ["cad", "programming", "3d-printing"], difficulty: "Intermediate", featured: false},
        {name: "Filament", org: "google", desc: "Real-time physically based renderer", url: "https://github.com/google/filament", stars: "17K+", language: "C++", topics: ["rendering", "pbr", "3d"], difficulty: "Advanced", featured: true},
        {name: "BGFX", org: "bkaradzic", desc: "Cross-platform rendering library", url: "https://github.com/bkaradzic/bgfx", stars: "14K+", language: "C++", topics: ["rendering", "cross-platform", "gpu"], difficulty: "Advanced", featured: false},
        {name: "WGPU", org: "gfx-rs", desc: "Rust implementation of WebGPU", url: "https://github.com/gfx-rs/wgpu", stars: "11K+", language: "Rust", topics: ["webgpu", "graphics", "rust"], difficulty: "Advanced", featured: true},
        {name: "Skia", org: "ArtifexSoftware", desc: "2D graphics library", url: "https://skia.org/", stars: "N/A", language: "C++", topics: ["2d", "graphics", "chrome"], difficulty: "Advanced", featured: false},
        {name: "Rerun", org: "rerun-io", desc: "Visualize multimodal data", url: "https://github.com/rerun-io/rerun", stars: "5K+", language: "Rust", topics: ["visualization", "3d", "robotics"], difficulty: "Intermediate", featured: true},
    ],

    // ==================== VIDEO & STREAMING ====================
    video_streaming: [
        {name: "OBS Studio", org: "obsproject", desc: "Video recording and streaming", url: "https://github.com/obsproject/obs-studio", stars: "55K+", language: "C", topics: ["streaming", "recording", "broadcast"], difficulty: "Intermediate", featured: true},
        {name: "Jellyfin", org: "jellyfin", desc: "Media system for streaming", url: "https://github.com/jellyfin/jellyfin", stars: "30K+", language: "C#", topics: ["media", "streaming", "self-hosted"], difficulty: "Intermediate", featured: true},
        {name: "Video.js", org: "videojs", desc: "Web video player", url: "https://github.com/videojs/video.js", stars: "37K+", language: "JavaScript", topics: ["video", "player", "hls"], difficulty: "Beginner", featured: true},
        {name: "HLS.js", org: "video-dev", desc: "JavaScript HLS client", url: "https://github.com/video-dev/hls.js", stars: "14K+", language: "TypeScript", topics: ["hls", "streaming", "player"], difficulty: "Intermediate", featured: false},
        {name: "Shaka Player", org: "shaka-project", desc: "JavaScript DASH & HLS player", url: "https://github.com/shaka-project/shaka-player", stars: "7K+", language: "JavaScript", topics: ["dash", "hls", "drm"], difficulty: "Intermediate", featured: false},
        {name: "MediaMTX", org: "bluenviron", desc: "Media server for live streaming", url: "https://github.com/bluenviron/mediamtx", stars: "10K+", language: "Go", topics: ["rtsp", "rtmp", "streaming"], difficulty: "Intermediate", featured: true},
        {name: "SRS", org: "ossrs", desc: "Simple realtime media server", url: "https://github.com/ossrs/srs", stars: "24K+", language: "C++", topics: ["rtmp", "webrtc", "streaming"], difficulty: "Advanced", featured: false},
        {name: "Remotion", org: "remotion-dev", desc: "Make videos programmatically", url: "https://github.com/remotion-dev/remotion", stars: "19K+", language: "TypeScript", topics: ["video", "react", "programmatic"], difficulty: "Intermediate", featured: true},
        {name: "Mux", org: "muxinc", desc: "Video infrastructure API", url: "https://github.com/muxinc/mux-player-react", stars: "500+", language: "TypeScript", topics: ["video", "api", "streaming"], difficulty: "Beginner", featured: false},
    ],

    // ==================== TERMINAL & SHELL ====================
    terminal_shell: [
        {name: "Fish Shell", org: "fish-shell", desc: "Smart and user-friendly shell", url: "https://github.com/fish-shell/fish-shell", stars: "24K+", language: "Rust", topics: ["shell", "terminal", "cli"], difficulty: "Beginner", featured: true},
        {name: "Nushell", org: "nushell", desc: "New type of shell", url: "https://github.com/nushell/nushell", stars: "30K+", language: "Rust", topics: ["shell", "data-driven", "modern"], difficulty: "Intermediate", featured: true},
        {name: "Zsh", org: "zsh-users", desc: "Z shell", url: "https://github.com/zsh-users/zsh", stars: "4K+", language: "C", topics: ["shell", "terminal"], difficulty: "Intermediate", featured: false},
        {name: "Alacritty", org: "alacritty", desc: "GPU-accelerated terminal", url: "https://github.com/alacritty/alacritty", stars: "52K+", language: "Rust", topics: ["terminal", "gpu", "fast"], difficulty: "Beginner", featured: true},
        {name: "Kitty", org: "kovidgoyal", desc: "GPU-based terminal emulator", url: "https://github.com/kovidgoyal/kitty", stars: "22K+", language: "C/Python", topics: ["terminal", "gpu", "feature-rich"], difficulty: "Intermediate", featured: true},
        {name: "WezTerm", org: "wez", desc: "GPU-accelerated terminal", url: "https://github.com/wez/wezterm", stars: "14K+", language: "Rust", topics: ["terminal", "multiplexer", "lua"], difficulty: "Intermediate", featured: false},
        {name: "Hyper", org: "vercel", desc: "Electron-based terminal", url: "https://github.com/vercel/hyper", stars: "43K+", language: "TypeScript", topics: ["terminal", "electron", "plugins"], difficulty: "Beginner", featured: false},
        {name: "Tabby", org: "Eugeny", desc: "Terminal for the modern age", url: "https://github.com/Eugeny/tabby", stars: "55K+", language: "TypeScript", topics: ["terminal", "ssh", "serial"], difficulty: "Beginner", featured: true},
        {name: "Atuin", org: "atuinsh", desc: "Magical shell history", url: "https://github.com/atuinsh/atuin", stars: "18K+", language: "Rust", topics: ["shell", "history", "sync"], difficulty: "Beginner", featured: true},
        {name: "Zellij", org: "zellij-org", desc: "Terminal workspace", url: "https://github.com/zellij-org/zellij", stars: "18K+", language: "Rust", topics: ["terminal", "multiplexer", "layout"], difficulty: "Intermediate", featured: true},
    ],

    // ==================== BROWSER EXTENSIONS ====================
    browser_ext: [
        {name: "uBlock Origin", org: "gorhill", desc: "Efficient blocker for browsers", url: "https://github.com/gorhill/uBlock", stars: "43K+", language: "JavaScript", topics: ["ad-blocking", "privacy", "extension"], difficulty: "Intermediate", featured: true},
        {name: "Vimium", org: "philc", desc: "Vim keyboard shortcuts for browser", url: "https://github.com/philc/vimium", stars: "22K+", language: "JavaScript", topics: ["vim", "keyboard", "productivity"], difficulty: "Beginner", featured: true},
        {name: "Refined GitHub", org: "refined-github", desc: "Browser extension for GitHub", url: "https://github.com/refined-github/refined-github", stars: "23K+", language: "TypeScript", topics: ["github", "enhancement", "extension"], difficulty: "Beginner", featured: true},
        {name: "Octotree", org: "ArtifexSoftware", desc: "GitHub code tree extension", url: "https://github.com/ArtifexSoftware/octotree", stars: "N/A", language: "JavaScript", topics: ["github", "tree", "navigation"], difficulty: "Beginner", featured: false},
        {name: "Wappalyzer", org: "wappalyzer", desc: "Identify web technologies", url: "https://github.com/wappalyzer/wappalyzer", stars: "10K+", language: "JavaScript", topics: ["technology", "detection", "analysis"], difficulty: "Beginner", featured: false},
        {name: "React DevTools", org: "facebook", desc: "Debugging React apps", url: "https://github.com/facebook/react/tree/main/packages/react-devtools", stars: "N/A", language: "JavaScript", topics: ["react", "debugging", "devtools"], difficulty: "Beginner", featured: true},
        {name: "Redux DevTools", org: "reduxjs", desc: "Debugging Redux state", url: "https://github.com/reduxjs/redux-devtools", stars: "14K+", language: "TypeScript", topics: ["redux", "debugging", "devtools"], difficulty: "Beginner", featured: false},
        {name: "Vue DevTools", org: "vuejs", desc: "Debugging Vue.js apps", url: "https://github.com/vuejs/devtools", stars: "24K+", language: "TypeScript", topics: ["vue", "debugging", "devtools"], difficulty: "Beginner", featured: false},
        {name: "Plasmo", org: "ArtifexSoftware", desc: "Browser extension framework", url: "https://github.com/ArtifexSoftware/plasmo", stars: "N/A", language: "TypeScript", topics: ["extension", "framework", "react"], difficulty: "Intermediate", featured: true},
        {name: "WXT", org: "wxt-dev", desc: "Next-gen web extension framework", url: "https://github.com/wxt-dev/wxt", stars: "3K+", language: "TypeScript", topics: ["extension", "framework", "vite"], difficulty: "Intermediate", featured: true},
    ],

    // ==================== API CLIENTS & HTTP ====================
    http_clients: [
        {name: "Axios", org: "axios", desc: "Promise based HTTP client", url: "https://github.com/axios/axios", stars: "104K+", language: "JavaScript", topics: ["http", "client", "promise"], difficulty: "Beginner", featured: true},
        {name: "ky", org: "sindresorhus", desc: "Tiny HTTP client based on fetch", url: "https://github.com/sindresorhus/ky", stars: "11K+", language: "TypeScript", topics: ["http", "fetch", "tiny"], difficulty: "Beginner", featured: true},
        {name: "got", org: "sindresorhus", desc: "Human-friendly HTTP requests", url: "https://github.com/sindresorhus/got", stars: "14K+", language: "TypeScript", topics: ["http", "node", "request"], difficulty: "Beginner", featured: false},
        {name: "ofetch", org: "unjs", desc: "Better fetch API", url: "https://github.com/unjs/ofetch", stars: "3K+", language: "TypeScript", topics: ["fetch", "universal", "http"], difficulty: "Beginner", featured: true},
        {name: "Wretch", org: "elbywan", desc: "Tiny wrapper around fetch", url: "https://github.com/elbywan/wretch", stars: "4K+", language: "TypeScript", topics: ["fetch", "wrapper", "fluent"], difficulty: "Beginner", featured: false},
        {name: "HTTPX", org: "encode", desc: "Async HTTP client for Python", url: "https://github.com/encode/httpx", stars: "12K+", language: "Python", topics: ["http", "async", "python"], difficulty: "Beginner", featured: true},
        {name: "aiohttp", org: "aio-libs", desc: "Async HTTP client/server", url: "https://github.com/aio-libs/aiohttp", stars: "14K+", language: "Python", topics: ["http", "async", "server"], difficulty: "Intermediate", featured: false},
        {name: "Requests", org: "psf", desc: "HTTP for Humans", url: "https://github.com/psf/requests", stars: "51K+", language: "Python", topics: ["http", "python", "simple"], difficulty: "Beginner", featured: true},
        {name: "Hoppscotch", org: "hoppscotch", desc: "Open source API dev ecosystem", url: "https://github.com/hoppscotch/hoppscotch", stars: "60K+", language: "TypeScript", topics: ["api", "testing", "postman-alt"], difficulty: "Beginner", featured: true},
        {name: "Insomnia", org: "Kong", desc: "API client and design platform", url: "https://github.com/Kong/insomnia", stars: "33K+", language: "TypeScript", topics: ["api", "rest", "graphql"], difficulty: "Beginner", featured: true},
    ],

    // ==================== SERVERLESS & EDGE ====================
    serverless_edge: [
        {name: "Vercel", org: "vercel", desc: "Frontend cloud platform", url: "https://github.com/vercel/vercel", stars: "12K+", language: "TypeScript", topics: ["serverless", "frontend", "deployment"], difficulty: "Beginner", featured: true},
        {name: "Serverless Framework", org: "serverless", desc: "Build serverless applications", url: "https://github.com/serverless/serverless", stars: "46K+", language: "JavaScript", topics: ["serverless", "aws", "azure"], difficulty: "Intermediate", featured: true},
        {name: "SST", org: "sst", desc: "Build modern full-stack apps", url: "https://github.com/sst/sst", stars: "20K+", language: "TypeScript", topics: ["serverless", "aws", "infrastructure"], difficulty: "Intermediate", featured: true},
        {name: "Architect", org: "architect", desc: "Serverless framework", url: "https://github.com/architect/architect", stars: "2K+", language: "JavaScript", topics: ["serverless", "aws", "arc"], difficulty: "Intermediate", featured: false},
        {name: "OpenFaaS", org: "openfaas", desc: "Serverless functions on Kubernetes", url: "https://github.com/openfaas/faas", stars: "24K+", language: "Go", topics: ["faas", "kubernetes", "functions"], difficulty: "Intermediate", featured: true},
        {name: "Knative", org: "knative", desc: "Kubernetes-based serverless", url: "https://github.com/knative/serving", stars: "5K+", language: "Go", topics: ["serverless", "kubernetes", "serving"], difficulty: "Advanced", featured: false},
        {name: "Deno Deploy", org: "denoland", desc: "Deploy JavaScript globally", url: "https://github.com/denoland/deno", stars: "93K+", language: "Rust", topics: ["javascript", "runtime", "edge"], difficulty: "Intermediate", featured: true},
        {name: "Cloudflare Workers", org: "cloudflare", desc: "Serverless execution environment", url: "https://github.com/cloudflare/workers-sdk", stars: "2K+", language: "TypeScript", topics: ["edge", "serverless", "workers"], difficulty: "Intermediate", featured: true},
        {name: "Bun", org: "oven-sh", desc: "Fast JavaScript runtime", url: "https://github.com/oven-sh/bun", stars: "70K+", language: "Zig", topics: ["javascript", "runtime", "fast"], difficulty: "Beginner", featured: true},
    ],

    // ==================== COMPILERS & LANGUAGE TOOLS ====================
    compilers: [
        {name: "LLVM", org: "llvm", desc: "Compiler infrastructure", url: "https://github.com/llvm/llvm-project", stars: "26K+", language: "C++", topics: ["compiler", "llvm", "toolchain"], difficulty: "Advanced", featured: true},
        {name: "GCC", org: "gcc-mirror", desc: "GNU Compiler Collection", url: "https://github.com/gcc-mirror/gcc", stars: "6K+", language: "C", topics: ["compiler", "gnu", "c"], difficulty: "Advanced", featured: true},
        {name: "SWC", org: "swc-project", desc: "Super-fast TypeScript compiler", url: "https://github.com/swc-project/swc", stars: "30K+", language: "Rust", topics: ["compiler", "typescript", "fast"], difficulty: "Intermediate", featured: true},
        {name: "esbuild", org: "evanw", desc: "Extremely fast bundler", url: "https://github.com/evanw/esbuild", stars: "37K+", language: "Go", topics: ["bundler", "minifier", "fast"], difficulty: "Beginner", featured: true},
        {name: "Vite", org: "vitejs", desc: "Next generation frontend tooling", url: "https://github.com/vitejs/vite", stars: "64K+", language: "TypeScript", topics: ["bundler", "dev-server", "esm"], difficulty: "Beginner", featured: true},
        {name: "Rollup", org: "rollup", desc: "JavaScript module bundler", url: "https://github.com/rollup/rollup", stars: "25K+", language: "JavaScript", topics: ["bundler", "esm", "tree-shaking"], difficulty: "Intermediate", featured: false},
        {name: "Parcel", org: "parcel-bundler", desc: "Zero config bundler", url: "https://github.com/parcel-bundler/parcel", stars: "43K+", language: "JavaScript", topics: ["bundler", "zero-config"], difficulty: "Beginner", featured: false},
        {name: "Turbopack", org: "vercel", desc: "Rust-powered bundler for Webpack", url: "https://github.com/vercel/turbo", stars: "25K+", language: "Rust", topics: ["bundler", "fast", "webpack"], difficulty: "Intermediate", featured: true},
        {name: "Oxc", org: "oxc-project", desc: "Oxidation Compiler", url: "https://github.com/oxc-project/oxc", stars: "9K+", language: "Rust", topics: ["compiler", "linter", "fast"], difficulty: "Intermediate", featured: true},
        {name: "Biome", org: "biomejs", desc: "Toolchain for web projects", url: "https://github.com/biomejs/biome", stars: "11K+", language: "Rust", topics: ["formatter", "linter", "fast"], difficulty: "Beginner", featured: true},
    ],

    // ==================== OPERATING SYSTEMS ====================
    operating_systems: [
        {name: "Linux Kernel", org: "torvalds", desc: "The Linux kernel", url: "https://github.com/torvalds/linux", stars: "170K+", language: "C", topics: ["kernel", "operating-system", "linux"], difficulty: "Advanced", featured: true},
        {name: "Redox OS", org: "redox-os", desc: "Unix-like OS in Rust", url: "https://github.com/redox-os/redox", stars: "15K+", language: "Rust", topics: ["os", "rust", "unix"], difficulty: "Advanced", featured: true},
        {name: "SerenityOS", org: "SerenityOS", desc: "Graphical Unix-like OS", url: "https://github.com/SerenityOS/serenity", stars: "29K+", language: "C++", topics: ["os", "gui", "unix-like"], difficulty: "Advanced", featured: true},
        {name: "Haiku", org: "haiku", desc: "BeOS-inspired OS", url: "https://github.com/haiku/haiku", stars: "2K+", language: "C++", topics: ["os", "beos", "desktop"], difficulty: "Advanced", featured: false},
        {name: "ReactOS", org: "reactos", desc: "Windows-compatible OS", url: "https://github.com/reactos/reactos", stars: "14K+", language: "C", topics: ["os", "windows", "compatibility"], difficulty: "Advanced", featured: false},
        {name: "Bottlerocket", org: "bottlerocket-os", desc: "Linux for containers", url: "https://github.com/bottlerocket-os/bottlerocket", stars: "8K+", language: "Rust", topics: ["os", "containers", "aws"], difficulty: "Advanced", featured: false},
        {name: "Talos Linux", org: "siderolabs", desc: "Kubernetes-focused OS", url: "https://github.com/siderolabs/talos", stars: "5K+", language: "Go", topics: ["os", "kubernetes", "immutable"], difficulty: "Advanced", featured: true},
        {name: "Asahi Linux", org: "AsahiLinux", desc: "Linux for Apple Silicon", url: "https://github.com/AsahiLinux/docs", stars: "800+", language: "Multiple", topics: ["linux", "apple", "m1"], difficulty: "Advanced", featured: true},
    ],

    // ==================== NETWORKING ====================
    networking: [
        {name: "WireGuard", org: "WireGuard", desc: "Fast, modern VPN", url: "https://github.com/WireGuard/wireguard-linux", stars: "600+", language: "C", topics: ["vpn", "networking", "security"], difficulty: "Intermediate", featured: true},
        {name: "Tailscale", org: "tailscale", desc: "Zero config VPN", url: "https://github.com/tailscale/tailscale", stars: "17K+", language: "Go", topics: ["vpn", "wireguard", "mesh"], difficulty: "Beginner", featured: true},
        {name: "Netbird", org: "netbirdio", desc: "Connect devices securely", url: "https://github.com/netbirdio/netbird", stars: "9K+", language: "Go", topics: ["vpn", "p2p", "zero-trust"], difficulty: "Intermediate", featured: true},
        {name: "Headscale", org: "juanfont", desc: "Self-hosted Tailscale control", url: "https://github.com/juanfont/headscale", stars: "20K+", language: "Go", topics: ["tailscale", "self-hosted", "vpn"], difficulty: "Intermediate", featured: true},
        {name: "Zeek", org: "zeek", desc: "Network security monitor", url: "https://github.com/zeek/zeek", stars: "6K+", language: "C++", topics: ["security", "monitoring", "ids"], difficulty: "Advanced", featured: false},
        {name: "Suricata", org: "OISF", desc: "Network threat detection", url: "https://github.com/OISF/suricata", stars: "4K+", language: "C", topics: ["ids", "ips", "security"], difficulty: "Advanced", featured: false},
        {name: "mitmproxy", org: "mitmproxy", desc: "Interactive HTTPS proxy", url: "https://github.com/mitmproxy/mitmproxy", stars: "34K+", language: "Python", topics: ["proxy", "https", "debugging"], difficulty: "Intermediate", featured: true},
        {name: "Charles Proxy Alternative", org: "ArtifexSoftware", desc: "Proxyman for macOS", url: "https://proxyman.io/", stars: "N/A", language: "Swift", topics: ["proxy", "debugging", "macos"], difficulty: "Beginner", featured: false},
    ]
};

// Merge with existing database
if (typeof window !== 'undefined') {
    window.GIT_REPOS_DATABASE_5 = GIT_REPOS_DATABASE_5;
}


