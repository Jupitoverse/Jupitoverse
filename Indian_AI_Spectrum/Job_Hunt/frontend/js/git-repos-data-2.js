// Additional Git Repositories Database - Part 2
// More specialized domains

const GIT_REPOS_DATABASE_2 = {
    // ==================== GAMING & GRAPHICS ====================
    gaming: [
        {name: "Godot Engine", org: "godotengine", desc: "Multi-platform 2D/3D game engine", url: "https://github.com/godotengine/godot", stars: "83K+", language: "C++", topics: ["game-engine", "2d", "3d", "gdscript"], difficulty: "Intermediate", featured: true},
        {name: "Bevy", org: "bevyengine", desc: "Refreshingly simple ECS game engine in Rust", url: "https://github.com/bevyengine/bevy", stars: "32K+", language: "Rust", topics: ["game-engine", "ecs", "rust"], difficulty: "Intermediate", featured: true},
        {name: "Phaser", org: "photonstorm", desc: "HTML5 game framework", url: "https://github.com/photonstorm/phaser", stars: "36K+", language: "JavaScript", topics: ["html5", "2d", "game-framework"], difficulty: "Beginner", featured: true},
        {name: "PixiJS", org: "pixijs", desc: "HTML5 2D rendering engine", url: "https://github.com/pixijs/pixijs", stars: "42K+", language: "TypeScript", topics: ["2d", "webgl", "rendering"], difficulty: "Intermediate", featured: false},
        {name: "Raylib", org: "raysan5", desc: "Simple library to enjoy videogames programming", url: "https://github.com/raysan5/raylib", stars: "18K+", language: "C", topics: ["game-dev", "simple", "learning"], difficulty: "Beginner", featured: true},
        {name: "LÖVE", org: "love2d", desc: "Lua 2D game framework", url: "https://github.com/love2d/love", stars: "4K+", language: "C++/Lua", topics: ["2d", "lua", "game-framework"], difficulty: "Beginner", featured: false},
        {name: "Babylon.js", org: "BabylonJS", desc: "Powerful 3D game and rendering engine", url: "https://github.com/BabylonJS/Babylon.js", stars: "22K+", language: "TypeScript", topics: ["3d", "webgl", "webxr"], difficulty: "Intermediate", featured: false},
        {name: "PlayCanvas", org: "playcanvas", desc: "WebGL game engine", url: "https://github.com/playcanvas/engine", stars: "9K+", language: "JavaScript", topics: ["3d", "webgl", "game-engine"], difficulty: "Intermediate", featured: false},
        {name: "Amethyst (Rust)", org: "amethyst", desc: "Data-driven game engine in Rust", url: "https://github.com/amethyst/amethyst", stars: "8K+", language: "Rust", topics: ["ecs", "game-engine", "rust"], difficulty: "Advanced", featured: false},
        {name: "SDL", org: "libsdl-org", desc: "Cross-platform development library", url: "https://github.com/libsdl-org/SDL", stars: "7K+", language: "C", topics: ["multimedia", "cross-platform"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== CLI & AUTOMATION ====================
    cli_automation: [
        {name: "Typer", org: "tiangolo", desc: "Build CLI apps with Python type hints", url: "https://github.com/tiangolo/typer", stars: "14K+", language: "Python", topics: ["cli", "python", "type-hints"], difficulty: "Beginner", featured: true},
        {name: "Click", org: "pallets", desc: "Python package for creating CLIs", url: "https://github.com/pallets/click", stars: "15K+", language: "Python", topics: ["cli", "python", "commands"], difficulty: "Beginner", featured: true},
        {name: "Cobra", org: "spf13", desc: "CLI library for Go", url: "https://github.com/spf13/cobra", stars: "35K+", language: "Go", topics: ["cli", "go", "commands"], difficulty: "Beginner", featured: true},
        {name: "Charm", org: "charmbracelet", desc: "Beautiful CLI tools collection", url: "https://github.com/charmbracelet/bubbletea", stars: "24K+", language: "Go", topics: ["tui", "cli", "terminal"], difficulty: "Intermediate", featured: true},
        {name: "Rich", org: "Textualize", desc: "Python library for rich text in terminal", url: "https://github.com/Textualize/rich", stars: "47K+", language: "Python", topics: ["terminal", "formatting", "python"], difficulty: "Beginner", featured: true},
        {name: "Textual", org: "Textualize", desc: "TUI framework for Python", url: "https://github.com/Textualize/textual", stars: "23K+", language: "Python", topics: ["tui", "python", "terminal"], difficulty: "Intermediate", featured: true},
        {name: "Ink", org: "vadimdemedes", desc: "React for interactive CLIs", url: "https://github.com/vadimdemedes/ink", stars: "26K+", language: "TypeScript", topics: ["cli", "react", "interactive"], difficulty: "Intermediate", featured: false},
        {name: "Inquirer.js", org: "SBoudrias", desc: "Interactive CLI prompts", url: "https://github.com/SBoudrias/Inquirer.js", stars: "19K+", language: "JavaScript", topics: ["cli", "prompts", "interactive"], difficulty: "Beginner", featured: false},
        {name: "Commander.js", org: "tj", desc: "Node.js CLI framework", url: "https://github.com/tj/commander.js", stars: "26K+", language: "JavaScript", topics: ["cli", "node", "commands"], difficulty: "Beginner", featured: false},
        {name: "Clap", org: "clap-rs", desc: "Rust command line argument parser", url: "https://github.com/clap-rs/clap", stars: "13K+", language: "Rust", topics: ["cli", "rust", "parsing"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== IOT & EMBEDDED ====================
    iot_embedded: [
        {name: "Arduino", org: "arduino", desc: "Arduino IDE and libraries", url: "https://github.com/arduino/Arduino", stars: "14K+", language: "C++", topics: ["iot", "embedded", "hardware"], difficulty: "Beginner", featured: true},
        {name: "PlatformIO", org: "platformio", desc: "Professional embedded development platform", url: "https://github.com/platformio/platformio-core", stars: "7K+", language: "Python", topics: ["embedded", "iot", "cross-platform"], difficulty: "Intermediate", featured: true},
        {name: "ESP-IDF", org: "espressif", desc: "Espressif IoT Development Framework", url: "https://github.com/espressif/esp-idf", stars: "12K+", language: "C", topics: ["esp32", "iot", "wifi"], difficulty: "Intermediate", featured: true},
        {name: "MicroPython", org: "micropython", desc: "Python for microcontrollers", url: "https://github.com/micropython/micropython", stars: "18K+", language: "C", topics: ["python", "embedded", "iot"], difficulty: "Beginner", featured: true},
        {name: "CircuitPython", org: "adafruit", desc: "Easy coding for microcontrollers", url: "https://github.com/adafruit/circuitpython", stars: "4K+", language: "C", topics: ["python", "education", "iot"], difficulty: "Beginner", featured: false},
        {name: "Zephyr", org: "zephyrproject-rtos", desc: "Scalable real-time OS", url: "https://github.com/zephyrproject-rtos/zephyr", stars: "9K+", language: "C", topics: ["rtos", "embedded", "iot"], difficulty: "Advanced", featured: false},
        {name: "FreeRTOS", org: "FreeRTOS", desc: "Real-time operating system kernel", url: "https://github.com/FreeRTOS/FreeRTOS", stars: "4K+", language: "C", topics: ["rtos", "embedded", "realtime"], difficulty: "Advanced", featured: true},
        {name: "Home Assistant Core", org: "home-assistant", desc: "Open source home automation", url: "https://github.com/home-assistant/core", stars: "68K+", language: "Python", topics: ["smart-home", "automation", "iot"], difficulty: "Intermediate", featured: true},
        {name: "ESPHome", org: "esphome", desc: "ESP8266/ESP32 configuration system", url: "https://github.com/esphome/esphome", stars: "7K+", language: "C++", topics: ["esp", "yaml", "home-automation"], difficulty: "Beginner", featured: false},
        {name: "Tasmota", org: "arendst", desc: "Alternative firmware for ESP devices", url: "https://github.com/arendst/Tasmota", stars: "21K+", language: "C", topics: ["esp", "firmware", "iot"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== DOCUMENTATION ====================
    documentation: [
        {name: "Docusaurus", org: "facebook", desc: "Easy to maintain documentation sites", url: "https://github.com/facebook/docusaurus", stars: "52K+", language: "TypeScript", topics: ["docs", "static-site", "react"], difficulty: "Beginner", featured: true},
        {name: "MkDocs", org: "mkdocs", desc: "Project documentation with Markdown", url: "https://github.com/mkdocs/mkdocs", stars: "18K+", language: "Python", topics: ["docs", "markdown", "static-site"], difficulty: "Beginner", featured: true},
        {name: "Sphinx", org: "sphinx-doc", desc: "Python documentation generator", url: "https://github.com/sphinx-doc/sphinx", stars: "6K+", language: "Python", topics: ["docs", "python", "rst"], difficulty: "Intermediate", featured: false},
        {name: "Storybook", org: "storybookjs", desc: "UI component explorer", url: "https://github.com/storybookjs/storybook", stars: "82K+", language: "TypeScript", topics: ["ui", "components", "documentation"], difficulty: "Intermediate", featured: true},
        {name: "VitePress", org: "vuejs", desc: "Vite & Vue powered static site generator", url: "https://github.com/vuejs/vitepress", stars: "11K+", language: "TypeScript", topics: ["docs", "vue", "vite"], difficulty: "Beginner", featured: true},
        {name: "Mintlify", org: "mintlify", desc: "Beautiful documentation for your products", url: "https://github.com/mintlify/mint", stars: "2K+", language: "TypeScript", topics: ["docs", "mdx", "beautiful"], difficulty: "Beginner", featured: false},
        {name: "Nextra", org: "shuding", desc: "Next.js static site generator", url: "https://github.com/shuding/nextra", stars: "10K+", language: "TypeScript", topics: ["docs", "next.js", "mdx"], difficulty: "Beginner", featured: false},
        {name: "Swagger UI", org: "swagger-api", desc: "API documentation UI", url: "https://github.com/swagger-api/swagger-ui", stars: "25K+", language: "JavaScript", topics: ["api", "openapi", "documentation"], difficulty: "Beginner", featured: true},
        {name: "Readme.so", org: "octokatherine", desc: "README generator", url: "https://github.com/octokatherine/readme.so", stars: "4K+", language: "TypeScript", topics: ["readme", "generator", "markdown"], difficulty: "Beginner", featured: false},
    ],

    // ==================== SYSTEM DESIGN & ARCHITECTURE ====================
    system_design: [
        {name: "System Design Primer", org: "donnemartin", desc: "Learn system design for tech interviews", url: "https://github.com/donnemartin/system-design-primer", stars: "250K+", language: "Python", topics: ["learning", "interviews", "architecture"], difficulty: "Intermediate", featured: true},
        {name: "Awesome Scalability", org: "binhnguyennus", desc: "Scalability patterns and best practices", url: "https://github.com/binhnguyennus/awesome-scalability", stars: "52K+", language: "Markdown", topics: ["scalability", "architecture"], difficulty: "Intermediate", featured: true},
        {name: "Tech Interview Handbook", org: "yangshun", desc: "Materials for technical interviews", url: "https://github.com/yangshun/tech-interview-handbook", stars: "108K+", language: "TypeScript", topics: ["interviews", "algorithms", "career"], difficulty: "Intermediate", featured: true},
        {name: "Coding Interview University", org: "jwasham", desc: "Complete study plan for SE interviews", url: "https://github.com/jwasham/coding-interview-university", stars: "290K+", language: "Markdown", topics: ["learning", "interviews", "cs"], difficulty: "Intermediate", featured: true},
        {name: "Clean Code JavaScript", org: "ryanmcdermott", desc: "Clean Code concepts for JavaScript", url: "https://github.com/ryanmcdermott/clean-code-javascript", stars: "89K+", language: "JavaScript", topics: ["clean-code", "best-practices"], difficulty: "Beginner", featured: false},
        {name: "Design Patterns", org: "refactoring-guru", desc: "Design patterns in various languages", url: "https://github.com/RefactoringGuru/design-patterns-examples", stars: "1K+", language: "Multiple", topics: ["patterns", "oop", "learning"], difficulty: "Intermediate", featured: false},
        {name: "Patterns.dev", org: "patterns-dev", desc: "Modern web app design patterns", url: "https://github.com/lydiahallie/javascript-questions", stars: "59K+", language: "JavaScript", topics: ["patterns", "react", "learning"], difficulty: "Intermediate", featured: false},
        {name: "Awesome Architecture", org: "mehdihadeli", desc: "Software architecture resources", url: "https://github.com/mehdihadeli/awesome-software-architecture", stars: "6K+", language: "Markdown", topics: ["architecture", "ddd", "microservices"], difficulty: "Advanced", featured: false},
    ],

    // ==================== AUTHENTICATION & IDENTITY ====================
    auth_identity: [
        {name: "Auth.js (NextAuth)", org: "nextauthjs", desc: "Authentication for Next.js", url: "https://github.com/nextauthjs/next-auth", stars: "22K+", language: "TypeScript", topics: ["auth", "next.js", "oauth"], difficulty: "Intermediate", featured: true},
        {name: "Clerk", org: "clerk", desc: "Complete user management", url: "https://github.com/clerk/javascript", stars: "2K+", language: "TypeScript", topics: ["auth", "user-management"], difficulty: "Beginner", featured: true},
        {name: "Lucia", org: "lucia-auth", desc: "Simple and flexible authentication", url: "https://github.com/lucia-auth/lucia", stars: "7K+", language: "TypeScript", topics: ["auth", "sessions", "simple"], difficulty: "Intermediate", featured: true},
        {name: "Keycloak", org: "keycloak", desc: "Open source identity and access management", url: "https://github.com/keycloak/keycloak", stars: "20K+", language: "Java", topics: ["iam", "sso", "oauth"], difficulty: "Advanced", featured: true},
        {name: "Ory Hydra", org: "ory", desc: "OAuth 2.0 and OpenID Connect server", url: "https://github.com/ory/hydra", stars: "15K+", language: "Go", topics: ["oauth", "oidc", "identity"], difficulty: "Advanced", featured: false},
        {name: "Ory Kratos", org: "ory", desc: "Cloud-native identity & user management", url: "https://github.com/ory/kratos", stars: "10K+", language: "Go", topics: ["identity", "user-management"], difficulty: "Advanced", featured: false},
        {name: "Passport.js", org: "jaredhanson", desc: "Simple authentication for Node.js", url: "https://github.com/jaredhanson/passport", stars: "22K+", language: "JavaScript", topics: ["auth", "node", "strategies"], difficulty: "Intermediate", featured: false},
        {name: "jose", org: "panva", desc: "JWS, JWE, JWT, JWK library", url: "https://github.com/panva/jose", stars: "4K+", language: "TypeScript", topics: ["jwt", "jwe", "cryptography"], difficulty: "Intermediate", featured: false},
        {name: "Authelia", org: "authelia", desc: "Single sign-on multi-factor portal", url: "https://github.com/authelia/authelia", stars: "19K+", language: "Go", topics: ["sso", "mfa", "security"], difficulty: "Intermediate", featured: false},
        {name: "SuperTokens", org: "supertokens", desc: "Open source authentication", url: "https://github.com/supertokens/supertokens-core", stars: "11K+", language: "Java", topics: ["auth", "self-hosted"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== CMS & CONTENT ====================
    cms_content: [
        {name: "Strapi", org: "strapi", desc: "Leading open source headless CMS", url: "https://github.com/strapi/strapi", stars: "60K+", language: "JavaScript", topics: ["cms", "headless", "api"], difficulty: "Intermediate", featured: true},
        {name: "Payload CMS", org: "payloadcms", desc: "Code-first headless CMS", url: "https://github.com/payloadcms/payload", stars: "19K+", language: "TypeScript", topics: ["cms", "next.js", "code-first"], difficulty: "Intermediate", featured: true},
        {name: "Sanity", org: "sanity-io", desc: "Content platform", url: "https://github.com/sanity-io/sanity", stars: "5K+", language: "TypeScript", topics: ["cms", "structured-content"], difficulty: "Intermediate", featured: true},
        {name: "Ghost", org: "TryGhost", desc: "Professional publishing platform", url: "https://github.com/TryGhost/Ghost", stars: "45K+", language: "JavaScript", topics: ["cms", "blogging", "publishing"], difficulty: "Intermediate", featured: true},
        {name: "KeystoneJS", org: "keystonejs", desc: "CMS and GraphQL API", url: "https://github.com/keystonejs/keystone", stars: "8K+", language: "TypeScript", topics: ["cms", "graphql", "admin"], difficulty: "Intermediate", featured: false},
        {name: "Directus", org: "directus", desc: "Instant REST + GraphQL API", url: "https://github.com/directus/directus", stars: "25K+", language: "TypeScript", topics: ["cms", "api", "database"], difficulty: "Intermediate", featured: true},
        {name: "WordPress", org: "WordPress", desc: "World's most popular CMS", url: "https://github.com/WordPress/WordPress", stars: "18K+", language: "PHP", topics: ["cms", "blogging", "php"], difficulty: "Beginner", featured: true},
        {name: "Tina CMS", org: "tinacms", desc: "Git-backed headless CMS", url: "https://github.com/tinacms/tinacms", stars: "11K+", language: "TypeScript", topics: ["cms", "git-based", "visual"], difficulty: "Intermediate", featured: false},
        {name: "Netlify CMS", org: "netlify", desc: "Git-based content management", url: "https://github.com/netlify/netlify-cms", stars: "17K+", language: "JavaScript", topics: ["cms", "git", "static"], difficulty: "Beginner", featured: false},
    ],

    // ==================== MESSAGING & REALTIME ====================
    messaging_realtime: [
        {name: "Socket.io", org: "socketio", desc: "Realtime bidirectional event-based communication", url: "https://github.com/socketio/socket.io", stars: "60K+", language: "TypeScript", topics: ["websockets", "realtime", "events"], difficulty: "Intermediate", featured: true},
        {name: "RabbitMQ", org: "rabbitmq", desc: "Open source message broker", url: "https://github.com/rabbitmq/rabbitmq-server", stars: "11K+", language: "Erlang", topics: ["messaging", "queue", "amqp"], difficulty: "Intermediate", featured: true},
        {name: "NATS", org: "nats-io", desc: "Cloud-native messaging system", url: "https://github.com/nats-io/nats-server", stars: "14K+", language: "Go", topics: ["messaging", "pub-sub", "cloud-native"], difficulty: "Intermediate", featured: true},
        {name: "BullMQ", org: "taskforcesh", desc: "Node.js queue based on Redis", url: "https://github.com/taskforcesh/bullmq", stars: "5K+", language: "TypeScript", topics: ["queue", "redis", "jobs"], difficulty: "Intermediate", featured: true},
        {name: "Celery", org: "celery", desc: "Distributed task queue for Python", url: "https://github.com/celery/celery", stars: "23K+", language: "Python", topics: ["task-queue", "async", "distributed"], difficulty: "Intermediate", featured: true},
        {name: "Ably", org: "ably", desc: "Realtime messaging platform", url: "https://github.com/ably/ably-js", stars: "300+", language: "TypeScript", topics: ["realtime", "pub-sub"], difficulty: "Beginner", featured: false},
        {name: "Pusher", org: "pusher", desc: "Realtime messaging APIs", url: "https://github.com/pusher/pusher-js", stars: "2K+", language: "TypeScript", topics: ["realtime", "websockets"], difficulty: "Beginner", featured: false},
        {name: "Centrifugo", org: "centrifugal", desc: "Scalable realtime messaging server", url: "https://github.com/centrifugal/centrifugo", stars: "7K+", language: "Go", topics: ["realtime", "websockets", "scalable"], difficulty: "Intermediate", featured: false},
        {name: "LiveKit", org: "livekit", desc: "Realtime video and audio", url: "https://github.com/livekit/livekit", stars: "7K+", language: "Go", topics: ["webrtc", "video", "audio"], difficulty: "Intermediate", featured: true},
        {name: "Partykit", org: "partykit", desc: "Everything multiplayer", url: "https://github.com/partykit/partykit", stars: "4K+", language: "TypeScript", topics: ["multiplayer", "realtime", "edge"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== SEARCH ENGINES ====================
    search: [
        {name: "Elasticsearch", org: "elastic", desc: "Distributed RESTful search engine", url: "https://github.com/elastic/elasticsearch", stars: "67K+", language: "Java", topics: ["search", "analytics", "distributed"], difficulty: "Advanced", featured: true},
        {name: "Meilisearch", org: "meilisearch", desc: "Lightning-fast search engine", url: "https://github.com/meilisearch/meilisearch", stars: "43K+", language: "Rust", topics: ["search", "typo-tolerant", "fast"], difficulty: "Beginner", featured: true},
        {name: "Typesense", org: "typesense", desc: "Fast, typo-tolerant search", url: "https://github.com/typesense/typesense", stars: "17K+", language: "C++", topics: ["search", "typo-tolerant", "open-source"], difficulty: "Intermediate", featured: true},
        {name: "OpenSearch", org: "opensearch-project", desc: "Community-driven fork of Elasticsearch", url: "https://github.com/opensearch-project/OpenSearch", stars: "8K+", language: "Java", topics: ["search", "analytics", "aws"], difficulty: "Advanced", featured: false},
        {name: "Sonic", org: "valeriansaliou", desc: "Fast, lightweight search backend", url: "https://github.com/valeriansaliou/sonic", stars: "19K+", language: "Rust", topics: ["search", "fast", "lightweight"], difficulty: "Intermediate", featured: false},
        {name: "Algolia (InstantSearch)", org: "algolia", desc: "Frontend search library", url: "https://github.com/algolia/instantsearch", stars: "3K+", language: "TypeScript", topics: ["search", "ui", "frontend"], difficulty: "Beginner", featured: false},
        {name: "Tantivy", org: "quickwit-oss", desc: "Full-text search engine in Rust", url: "https://github.com/quickwit-oss/tantivy", stars: "10K+", language: "Rust", topics: ["search", "rust", "full-text"], difficulty: "Advanced", featured: false},
        {name: "Lunr.js", org: "olivernn", desc: "Client-side full-text search", url: "https://github.com/olivernn/lunr.js", stars: "8K+", language: "JavaScript", topics: ["search", "client-side", "lightweight"], difficulty: "Beginner", featured: false},
    ],

    // ==================== MEDIA & FILE PROCESSING ====================
    media_files: [
        {name: "FFmpeg", org: "FFmpeg", desc: "Complete solution for media processing", url: "https://github.com/FFmpeg/FFmpeg", stars: "42K+", language: "C", topics: ["video", "audio", "conversion"], difficulty: "Advanced", featured: true},
        {name: "ImageMagick", org: "ImageMagick", desc: "Image manipulation tools", url: "https://github.com/ImageMagick/ImageMagick", stars: "10K+", language: "C", topics: ["image", "processing", "conversion"], difficulty: "Intermediate", featured: true},
        {name: "Sharp", org: "lovell", desc: "High performance Node.js image processing", url: "https://github.com/lovell/sharp", stars: "27K+", language: "C++/JS", topics: ["image", "node", "fast"], difficulty: "Beginner", featured: true},
        {name: "Pillow", org: "python-pillow", desc: "Python Imaging Library fork", url: "https://github.com/python-pillow/Pillow", stars: "11K+", language: "Python", topics: ["image", "python", "processing"], difficulty: "Beginner", featured: true},
        {name: "Uppy", org: "transloadit", desc: "File uploader for web browsers", url: "https://github.com/transloadit/uppy", stars: "28K+", language: "JavaScript", topics: ["upload", "file", "ui"], difficulty: "Beginner", featured: true},
        {name: "Filepond", org: "pqina", desc: "Flexible file upload library", url: "https://github.com/pqina/filepond", stars: "14K+", language: "JavaScript", topics: ["upload", "file", "modern"], difficulty: "Beginner", featured: false},
        {name: "yt-dlp", org: "yt-dlp", desc: "YouTube-DL fork with additional features", url: "https://github.com/yt-dlp/yt-dlp", stars: "72K+", language: "Python", topics: ["video", "download", "youtube"], difficulty: "Beginner", featured: true},
        {name: "Cloudinary SDK", org: "cloudinary", desc: "Image and video management", url: "https://github.com/cloudinary/cloudinary_js", stars: "500+", language: "JavaScript", topics: ["media", "cloud", "transformation"], difficulty: "Beginner", featured: false},
        {name: "Lottie", org: "airbnb", desc: "Render After Effects animations", url: "https://github.com/airbnb/lottie-web", stars: "29K+", language: "JavaScript", topics: ["animation", "motion", "vector"], difficulty: "Beginner", featured: true},
    ],

    // ==================== MONITORING & LOGGING ====================
    monitoring_logging: [
        {name: "Sentry", org: "getsentry", desc: "Application monitoring platform", url: "https://github.com/getsentry/sentry", stars: "36K+", language: "Python", topics: ["monitoring", "errors", "performance"], difficulty: "Intermediate", featured: true},
        {name: "Jaeger", org: "jaegertracing", desc: "Distributed tracing platform", url: "https://github.com/jaegertracing/jaeger", stars: "19K+", language: "Go", topics: ["tracing", "observability", "distributed"], difficulty: "Advanced", featured: true},
        {name: "Zipkin", org: "openzipkin", desc: "Distributed tracing system", url: "https://github.com/openzipkin/zipkin", stars: "16K+", language: "Java", topics: ["tracing", "distributed", "latency"], difficulty: "Advanced", featured: false},
        {name: "Loki", org: "grafana", desc: "Log aggregation system", url: "https://github.com/grafana/loki", stars: "22K+", language: "Go", topics: ["logging", "prometheus", "grafana"], difficulty: "Intermediate", featured: true},
        {name: "Fluentd", org: "fluent", desc: "Unified logging layer", url: "https://github.com/fluent/fluentd", stars: "12K+", language: "Ruby", topics: ["logging", "data-collection"], difficulty: "Intermediate", featured: false},
        {name: "Vector", org: "vectordotdev", desc: "High-performance observability pipeline", url: "https://github.com/vectordotdev/vector", stars: "16K+", language: "Rust", topics: ["logging", "metrics", "pipeline"], difficulty: "Intermediate", featured: false},
        {name: "OpenTelemetry", org: "open-telemetry", desc: "Observability framework", url: "https://github.com/open-telemetry/opentelemetry-js", stars: "2K+", language: "TypeScript", topics: ["observability", "tracing", "metrics"], difficulty: "Intermediate", featured: true},
        {name: "Pino", org: "pinojs", desc: "Super fast Node.js logger", url: "https://github.com/pinojs/pino", stars: "13K+", language: "JavaScript", topics: ["logging", "node", "fast"], difficulty: "Beginner", featured: false},
        {name: "Winston", org: "winstonjs", desc: "Universal logging library", url: "https://github.com/winstonjs/winston", stars: "22K+", language: "JavaScript", topics: ["logging", "node", "transports"], difficulty: "Beginner", featured: false},
    ]
};

// Merge with existing database
if (typeof window !== 'undefined') {
    window.GIT_REPOS_DATABASE_2 = GIT_REPOS_DATABASE_2;
}


