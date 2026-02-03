// Additional Git Repositories Database - Part 3
// Specialized and trending projects

const GIT_REPOS_DATABASE_3 = {
    // ==================== LLM & GENERATIVE AI ====================
    llm_genai: [
        {name: "llama.cpp", org: "ggerganov", desc: "Port of LLaMA model in C/C++", url: "https://github.com/ggerganov/llama.cpp", stars: "55K+", language: "C++", topics: ["llm", "inference", "local"], difficulty: "Advanced", featured: true},
        {name: "GPT4All", org: "nomic-ai", desc: "Run LLMs locally on consumer hardware", url: "https://github.com/nomic-ai/gpt4all", stars: "62K+", language: "C++", topics: ["llm", "local", "chat"], difficulty: "Beginner", featured: true},
        {name: "text-generation-webui", org: "oobabooga", desc: "Gradio web UI for LLMs", url: "https://github.com/oobabooga/text-generation-webui", stars: "35K+", language: "Python", topics: ["llm", "webui", "inference"], difficulty: "Intermediate", featured: true},
        {name: "vLLM", org: "vllm-project", desc: "High-throughput LLM serving", url: "https://github.com/vllm-project/vllm", stars: "20K+", language: "Python", topics: ["llm", "inference", "serving"], difficulty: "Advanced", featured: true},
        {name: "Open Interpreter", org: "OpenInterpreter", desc: "Natural language interface to computer", url: "https://github.com/OpenInterpreter/open-interpreter", stars: "48K+", language: "Python", topics: ["llm", "code-interpreter", "agents"], difficulty: "Beginner", featured: true},
        {name: "Jan", org: "janhq", desc: "Open source ChatGPT alternative runs locally", url: "https://github.com/janhq/jan", stars: "18K+", language: "TypeScript", topics: ["llm", "local", "desktop"], difficulty: "Beginner", featured: true},
        {name: "Open WebUI", org: "open-webui", desc: "User-friendly WebUI for LLMs", url: "https://github.com/open-webui/open-webui", stars: "25K+", language: "Python", topics: ["llm", "webui", "ollama"], difficulty: "Beginner", featured: true},
        {name: "GPT Engineer", org: "AntonOsika", desc: "Specify what you want, AI builds it", url: "https://github.com/AntonOsika/gpt-engineer", stars: "50K+", language: "Python", topics: ["llm", "code-generation", "agents"], difficulty: "Intermediate", featured: true},
        {name: "Guidance", org: "guidance-ai", desc: "Language for controlling LLMs", url: "https://github.com/guidance-ai/guidance", stars: "17K+", language: "Python", topics: ["llm", "prompting", "control"], difficulty: "Intermediate", featured: false},
        {name: "LitGPT", org: "Lightning-AI", desc: "Pretrain, finetune, deploy LLMs", url: "https://github.com/Lightning-AI/litgpt", stars: "8K+", language: "Python", topics: ["llm", "training", "finetuning"], difficulty: "Advanced", featured: false},
        {name: "LM Studio", org: "lmstudio-ai", desc: "Discover, download, and run local LLMs", url: "https://lmstudio.ai/", stars: "N/A", language: "Desktop", topics: ["llm", "local", "gui"], difficulty: "Beginner", featured: false},
        {name: "ExLlamaV2", org: "turboderp", desc: "Fast inference library for LLMs", url: "https://github.com/turboderp/exllamav2", stars: "3K+", language: "Python", topics: ["llm", "quantization", "fast"], difficulty: "Advanced", featured: false},
        {name: "MLC LLM", org: "mlc-ai", desc: "Native LLM inference on any hardware", url: "https://github.com/mlc-ai/mlc-llm", stars: "17K+", language: "Python", topics: ["llm", "mobile", "deployment"], difficulty: "Advanced", featured: false},
    ],

    // ==================== RAG & VECTOR STORES ====================
    rag_vectors: [
        {name: "Chroma", org: "chroma-core", desc: "AI-native open-source embedding database", url: "https://github.com/chroma-core/chroma", stars: "12K+", language: "Python", topics: ["vector-db", "embeddings", "rag"], difficulty: "Beginner", featured: true},
        {name: "Weaviate", org: "weaviate", desc: "Open-source vector database", url: "https://github.com/weaviate/weaviate", stars: "10K+", language: "Go", topics: ["vector-db", "graphql", "ml"], difficulty: "Intermediate", featured: true},
        {name: "Qdrant", org: "qdrant", desc: "Vector similarity search engine", url: "https://github.com/qdrant/qdrant", stars: "17K+", language: "Rust", topics: ["vector-db", "similarity", "fast"], difficulty: "Intermediate", featured: true},
        {name: "Milvus", org: "milvus-io", desc: "Cloud-native vector database", url: "https://github.com/milvus-io/milvus", stars: "27K+", language: "Go", topics: ["vector-db", "cloud-native", "scalable"], difficulty: "Advanced", featured: true},
        {name: "Pinecone (Python Client)", org: "pinecone-io", desc: "Vector database for ML applications", url: "https://github.com/pinecone-io/pinecone-python-client", stars: "300+", language: "Python", topics: ["vector-db", "managed"], difficulty: "Beginner", featured: false},
        {name: "FAISS", org: "facebookresearch", desc: "Efficient similarity search library", url: "https://github.com/facebookresearch/faiss", stars: "27K+", language: "C++", topics: ["similarity", "embeddings", "clustering"], difficulty: "Advanced", featured: true},
        {name: "pgvector", org: "pgvector", desc: "Vector similarity search for PostgreSQL", url: "https://github.com/pgvector/pgvector", stars: "9K+", language: "C", topics: ["postgres", "vector", "extension"], difficulty: "Intermediate", featured: true},
        {name: "LanceDB", org: "lancedb", desc: "Serverless vector database", url: "https://github.com/lancedb/lancedb", stars: "3K+", language: "Rust", topics: ["vector-db", "serverless", "embedded"], difficulty: "Beginner", featured: false},
        {name: "Unstructured", org: "Unstructured-IO", desc: "Extract data from any document", url: "https://github.com/Unstructured-IO/unstructured", stars: "6K+", language: "Python", topics: ["rag", "document-parsing", "etl"], difficulty: "Intermediate", featured: true},
        {name: "Haystack", org: "deepset-ai", desc: "Framework for building NLP applications", url: "https://github.com/deepset-ai/haystack", stars: "14K+", language: "Python", topics: ["rag", "qa", "search"], difficulty: "Intermediate", featured: true},
    ],

    // ==================== COMPUTER VISION ====================
    computer_vision: [
        {name: "Segment Anything", org: "facebookresearch", desc: "Promptable image segmentation", url: "https://github.com/facebookresearch/segment-anything", stars: "43K+", language: "Python", topics: ["segmentation", "foundation-model"], difficulty: "Intermediate", featured: true},
        {name: "ControlNet", org: "lllyasviel", desc: "Conditional control for Stable Diffusion", url: "https://github.com/lllyasviel/ControlNet", stars: "27K+", language: "Python", topics: ["diffusion", "control", "generation"], difficulty: "Advanced", featured: true},
        {name: "ComfyUI", org: "comfyanonymous", desc: "Powerful Stable Diffusion GUI", url: "https://github.com/comfyanonymous/ComfyUI", stars: "35K+", language: "Python", topics: ["diffusion", "gui", "workflow"], difficulty: "Intermediate", featured: true},
        {name: "Automatic1111", org: "AUTOMATIC1111", desc: "Stable Diffusion web UI", url: "https://github.com/AUTOMATIC1111/stable-diffusion-webui", stars: "125K+", language: "Python", topics: ["diffusion", "webui", "generation"], difficulty: "Intermediate", featured: true},
        {name: "Fooocus", org: "lllyasviel", desc: "Simple image generating software", url: "https://github.com/lllyasviel/Fooocus", stars: "35K+", language: "Python", topics: ["diffusion", "simple", "generation"], difficulty: "Beginner", featured: true},
        {name: "InvokeAI", org: "invoke-ai", desc: "Leading creative engine for Stable Diffusion", url: "https://github.com/invoke-ai/InvokeAI", stars: "21K+", language: "Python", topics: ["diffusion", "creative", "ui"], difficulty: "Intermediate", featured: false},
        {name: "GFPGAN", org: "TencentARC", desc: "Face restoration algorithm", url: "https://github.com/TencentARC/GFPGAN", stars: "34K+", language: "Python", topics: ["face-restoration", "enhancement"], difficulty: "Intermediate", featured: false},
        {name: "Real-ESRGAN", org: "xinntao", desc: "Practical image/video restoration", url: "https://github.com/xinntao/Real-ESRGAN", stars: "26K+", language: "Python", topics: ["upscaling", "enhancement", "super-resolution"], difficulty: "Intermediate", featured: true},
        {name: "Rembg", org: "danielgatis", desc: "Remove image background", url: "https://github.com/danielgatis/rembg", stars: "14K+", language: "Python", topics: ["background-removal", "segmentation"], difficulty: "Beginner", featured: false},
        {name: "InsightFace", org: "deepinsight", desc: "Face analysis project", url: "https://github.com/deepinsight/insightface", stars: "20K+", language: "Python", topics: ["face-recognition", "analysis"], difficulty: "Advanced", featured: false},
    ],

    // ==================== AUDIO & SPEECH ====================
    audio_speech: [
        {name: "Whisper", org: "openai", desc: "Robust speech recognition", url: "https://github.com/openai/whisper", stars: "59K+", language: "Python", topics: ["speech-to-text", "transcription"], difficulty: "Intermediate", featured: true},
        {name: "Coqui TTS", org: "coqui-ai", desc: "Text-to-speech synthesis", url: "https://github.com/coqui-ai/TTS", stars: "30K+", language: "Python", topics: ["text-to-speech", "synthesis"], difficulty: "Intermediate", featured: true},
        {name: "Tortoise TTS", org: "neonbjb", desc: "Multi-voice TTS system", url: "https://github.com/neonbjb/tortoise-tts", stars: "12K+", language: "Python", topics: ["text-to-speech", "voice-cloning"], difficulty: "Advanced", featured: false},
        {name: "Bark", org: "suno-ai", desc: "Transformer-based text-to-audio", url: "https://github.com/suno-ai/bark", stars: "32K+", language: "Python", topics: ["text-to-audio", "generation"], difficulty: "Intermediate", featured: true},
        {name: "AudioCraft", org: "facebookresearch", desc: "Audio generation library", url: "https://github.com/facebookresearch/audiocraft", stars: "19K+", language: "Python", topics: ["music-generation", "audio"], difficulty: "Advanced", featured: true},
        {name: "Demucs", org: "facebookresearch", desc: "Music source separation", url: "https://github.com/facebookresearch/demucs", stars: "7K+", language: "Python", topics: ["source-separation", "music"], difficulty: "Intermediate", featured: false},
        {name: "Faster Whisper", org: "SYSTRAN", desc: "Faster Whisper transcription", url: "https://github.com/SYSTRAN/faster-whisper", stars: "9K+", language: "Python", topics: ["transcription", "optimization"], difficulty: "Intermediate", featured: false},
        {name: "WhisperX", org: "m-bain", desc: "Fast automatic speech recognition", url: "https://github.com/m-bain/whisperX", stars: "9K+", language: "Python", topics: ["speech-recognition", "alignment"], difficulty: "Intermediate", featured: false},
        {name: "Piper", org: "rhasspy", desc: "Fast local neural TTS", url: "https://github.com/rhasspy/piper", stars: "4K+", language: "C++", topics: ["tts", "local", "fast"], difficulty: "Intermediate", featured: false},
        {name: "OpenVoice", org: "myshell-ai", desc: "Instant voice cloning", url: "https://github.com/myshell-ai/OpenVoice", stars: "25K+", language: "Python", topics: ["voice-cloning", "tts"], difficulty: "Intermediate", featured: true},
    ],

    // ==================== LOW CODE / NO CODE ====================
    low_code: [
        {name: "Appsmith", org: "appsmithorg", desc: "Build internal tools fast", url: "https://github.com/appsmithorg/appsmith", stars: "31K+", language: "TypeScript", topics: ["low-code", "internal-tools", "admin"], difficulty: "Beginner", featured: true},
        {name: "Tooljet", org: "ToolJet", desc: "Open-source low-code framework", url: "https://github.com/ToolJet/ToolJet", stars: "26K+", language: "JavaScript", topics: ["low-code", "internal-tools"], difficulty: "Beginner", featured: true},
        {name: "Budibase", org: "Budibase", desc: "Low-code platform for internal tools", url: "https://github.com/Budibase/budibase", stars: "20K+", language: "JavaScript", topics: ["low-code", "admin-panels"], difficulty: "Beginner", featured: true},
        {name: "NocoDB", org: "nocodb", desc: "Open source Airtable alternative", url: "https://github.com/nocodb/nocodb", stars: "42K+", language: "TypeScript", topics: ["no-code", "spreadsheet", "database"], difficulty: "Beginner", featured: true},
        {name: "n8n", org: "n8n-io", desc: "Workflow automation platform", url: "https://github.com/n8n-io/n8n", stars: "40K+", language: "TypeScript", topics: ["automation", "workflow", "integration"], difficulty: "Beginner", featured: true},
        {name: "Windmill", org: "windmill-labs", desc: "Developer platform for scripts", url: "https://github.com/windmill-labs/windmill", stars: "8K+", language: "TypeScript", topics: ["automation", "scripts", "workflows"], difficulty: "Intermediate", featured: false},
        {name: "Refine", org: "refinedev", desc: "React framework for CRUD apps", url: "https://github.com/refinedev/refine", stars: "24K+", language: "TypeScript", topics: ["react", "crud", "admin"], difficulty: "Intermediate", featured: true},
        {name: "Baserow", org: "bram2w", desc: "Open source no-code database tool", url: "https://github.com/bram2w/baserow", stars: "3K+", language: "Python", topics: ["no-code", "database", "airtable"], difficulty: "Beginner", featured: false},
        {name: "Flowise", org: "FlowiseAI", desc: "Drag & drop LLM flow builder", url: "https://github.com/FlowiseAI/Flowise", stars: "25K+", language: "TypeScript", topics: ["llm", "no-code", "langchain"], difficulty: "Beginner", featured: true},
        {name: "Dify", org: "langgenius", desc: "LLM app development platform", url: "https://github.com/langgenius/dify", stars: "30K+", language: "Python", topics: ["llm", "low-code", "agents"], difficulty: "Intermediate", featured: true},
    ],

    // ==================== PRODUCTIVITY & NOTES ====================
    productivity: [
        {name: "Obsidian (API)", org: "obsidianmd", desc: "Knowledge base on local Markdown", url: "https://github.com/obsidianmd/obsidian-api", stars: "1K+", language: "TypeScript", topics: ["notes", "markdown", "knowledge"], difficulty: "Beginner", featured: true},
        {name: "Logseq", org: "logseq", desc: "Privacy-first knowledge base", url: "https://github.com/logseq/logseq", stars: "29K+", language: "Clojure", topics: ["notes", "outliner", "graphs"], difficulty: "Beginner", featured: true},
        {name: "Joplin", org: "laurent22", desc: "Open source note taking app", url: "https://github.com/laurent22/joplin", stars: "43K+", language: "TypeScript", topics: ["notes", "markdown", "sync"], difficulty: "Beginner", featured: true},
        {name: "Trilium Notes", org: "zadam", desc: "Hierarchical note taking", url: "https://github.com/zadam/trilium", stars: "25K+", language: "JavaScript", topics: ["notes", "knowledge-base"], difficulty: "Beginner", featured: false},
        {name: "AppFlowy", org: "AppFlowy-IO", desc: "Open source Notion alternative", url: "https://github.com/AppFlowy-IO/AppFlowy", stars: "48K+", language: "Rust/Dart", topics: ["notes", "notion", "productivity"], difficulty: "Beginner", featured: true},
        {name: "Outline", org: "outline", desc: "Team knowledge base", url: "https://github.com/outline/outline", stars: "24K+", language: "TypeScript", topics: ["wiki", "knowledge-base", "team"], difficulty: "Intermediate", featured: false},
        {name: "AFFiNE", org: "toeverything", desc: "Next-gen knowledge base", url: "https://github.com/toeverything/AFFiNE", stars: "32K+", language: "TypeScript", topics: ["notes", "whiteboard", "docs"], difficulty: "Beginner", featured: true},
        {name: "Focalboard", org: "mattermost", desc: "Open source project management", url: "https://github.com/mattermost/focalboard", stars: "19K+", language: "Go", topics: ["kanban", "project-management"], difficulty: "Beginner", featured: false},
        {name: "Plane", org: "makeplane", desc: "Open source Jira alternative", url: "https://github.com/makeplane/plane", stars: "24K+", language: "TypeScript", topics: ["project-management", "issues"], difficulty: "Beginner", featured: true},
        {name: "Twenty", org: "twentyhq", desc: "Open source CRM", url: "https://github.com/twentyhq/twenty", stars: "12K+", language: "TypeScript", topics: ["crm", "sales", "contacts"], difficulty: "Intermediate", featured: true},
    ],

    // ==================== FINANCE & TRADING ====================
    finance: [
        {name: "Zipline", org: "quantopian", desc: "Algorithmic trading library", url: "https://github.com/quantopian/zipline", stars: "17K+", language: "Python", topics: ["trading", "backtesting", "algo"], difficulty: "Advanced", featured: true},
        {name: "Backtrader", org: "mementum", desc: "Python backtesting library", url: "https://github.com/mementum/backtrader", stars: "12K+", language: "Python", topics: ["trading", "backtesting"], difficulty: "Intermediate", featured: false},
        {name: "FinGPT", org: "AI4Finance-Foundation", desc: "Open-source financial LLMs", url: "https://github.com/AI4Finance-Foundation/FinGPT", stars: "12K+", language: "Python", topics: ["llm", "finance", "nlp"], difficulty: "Advanced", featured: true},
        {name: "FinRL", org: "AI4Finance-Foundation", desc: "Deep RL for quantitative finance", url: "https://github.com/AI4Finance-Foundation/FinRL", stars: "9K+", language: "Python", topics: ["rl", "trading", "finance"], difficulty: "Advanced", featured: false},
        {name: "yfinance", org: "ranaroussi", desc: "Yahoo Finance market data downloader", url: "https://github.com/ranaroussi/yfinance", stars: "12K+", language: "Python", topics: ["finance", "data", "stocks"], difficulty: "Beginner", featured: true},
        {name: "Firefly III", org: "firefly-iii", desc: "Personal finances manager", url: "https://github.com/firefly-iii/firefly-iii", stars: "14K+", language: "PHP", topics: ["personal-finance", "budgeting"], difficulty: "Beginner", featured: true},
        {name: "Maybe", org: "maybe-finance", desc: "Open-source personal finance", url: "https://github.com/maybe-finance/maybe", stars: "27K+", language: "Ruby", topics: ["personal-finance", "wealth"], difficulty: "Beginner", featured: true},
        {name: "Actual", org: "actualbudget", desc: "Local-first personal finance", url: "https://github.com/actualbudget/actual", stars: "11K+", language: "JavaScript", topics: ["budgeting", "finance"], difficulty: "Beginner", featured: false},
        {name: "GnuCash", org: "gnucash", desc: "Personal and small-business finance", url: "https://github.com/gnucash/gnucash", stars: "5K+", language: "C++", topics: ["accounting", "finance"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== EDUCATION & LEARNING ====================
    education: [
        {name: "freeCodeCamp", org: "freeCodeCamp", desc: "Learn to code for free", url: "https://github.com/freeCodeCamp/freeCodeCamp", stars: "387K+", language: "TypeScript", topics: ["learning", "coding", "curriculum"], difficulty: "Beginner", featured: true},
        {name: "The Odin Project", org: "TheOdinProject", desc: "Full stack curriculum", url: "https://github.com/TheOdinProject/curriculum", stars: "8K+", language: "Ruby", topics: ["learning", "fullstack", "curriculum"], difficulty: "Beginner", featured: true},
        {name: "CS50", org: "cs50", desc: "Harvard's CS50 course materials", url: "https://github.com/cs50/lectures", stars: "2K+", language: "Multiple", topics: ["cs", "harvard", "learning"], difficulty: "Beginner", featured: true},
        {name: "Developer Roadmaps", org: "kamranahmedse", desc: "Interactive developer roadmaps", url: "https://github.com/kamranahmedse/developer-roadmap", stars: "275K+", language: "TypeScript", topics: ["roadmaps", "learning", "career"], difficulty: "Beginner", featured: true},
        {name: "Build Your Own X", org: "codecrafters-io", desc: "Build your own tech projects", url: "https://github.com/codecrafters-io/build-your-own-x", stars: "260K+", language: "Markdown", topics: ["learning", "projects", "tutorials"], difficulty: "Intermediate", featured: true},
        {name: "Exercism", org: "exercism", desc: "Code practice and mentorship", url: "https://github.com/exercism/exercism", stars: "1K+", language: "Ruby", topics: ["practice", "mentorship", "learning"], difficulty: "Beginner", featured: false},
        {name: "LeetCode Patterns", org: "seanprashad", desc: "LeetCode pattern solutions", url: "https://github.com/seanprashad/leetcode-patterns", stars: "9K+", language: "Markdown", topics: ["algorithms", "interviews", "patterns"], difficulty: "Intermediate", featured: true},
        {name: "NeetCode", org: "neetcode-gh", desc: "Roadmap for coding interviews", url: "https://github.com/neetcode-gh/leetcode", stars: "5K+", language: "Multiple", topics: ["leetcode", "interviews", "dsa"], difficulty: "Intermediate", featured: true},
        {name: "JavaScript Algorithms", org: "trekhleb", desc: "Algorithms in JavaScript", url: "https://github.com/trekhleb/javascript-algorithms", stars: "181K+", language: "JavaScript", topics: ["algorithms", "data-structures", "learning"], difficulty: "Intermediate", featured: true},
        {name: "Project Based Learning", org: "practical-tutorials", desc: "Curated list of project tutorials", url: "https://github.com/practical-tutorials/project-based-learning", stars: "170K+", language: "Markdown", topics: ["learning", "projects", "tutorials"], difficulty: "Beginner", featured: true},
    ],

    // ==================== API & MICROSERVICES ====================
    api_microservices: [
        {name: "Kong", org: "Kong", desc: "Cloud-native API gateway", url: "https://github.com/Kong/kong", stars: "37K+", language: "Lua", topics: ["api-gateway", "microservices"], difficulty: "Intermediate", featured: true},
        {name: "APISIX", org: "apache", desc: "Cloud-native API gateway", url: "https://github.com/apache/apisix", stars: "13K+", language: "Lua", topics: ["api-gateway", "cloud-native"], difficulty: "Intermediate", featured: false},
        {name: "Envoy", org: "envoyproxy", desc: "Cloud-native edge/service proxy", url: "https://github.com/envoyproxy/envoy", stars: "24K+", language: "C++", topics: ["proxy", "service-mesh", "l7"], difficulty: "Advanced", featured: true},
        {name: "Dapr", org: "dapr", desc: "Portable event-driven runtime", url: "https://github.com/dapr/dapr", stars: "23K+", language: "Go", topics: ["microservices", "sidecar", "event-driven"], difficulty: "Intermediate", featured: true},
        {name: "Temporal", org: "temporalio", desc: "Durable execution system", url: "https://github.com/temporalio/temporal", stars: "10K+", language: "Go", topics: ["workflow", "orchestration", "durable"], difficulty: "Advanced", featured: true},
        {name: "Hasura", org: "hasura", desc: "Instant GraphQL APIs", url: "https://github.com/hasura/graphql-engine", stars: "31K+", language: "Haskell", topics: ["graphql", "realtime", "postgres"], difficulty: "Intermediate", featured: true},
        {name: "PostgREST", org: "PostgREST", desc: "REST API for PostgreSQL", url: "https://github.com/PostgREST/postgrest", stars: "22K+", language: "Haskell", topics: ["rest", "postgres", "auto-api"], difficulty: "Beginner", featured: false},
        {name: "NATS", org: "nats-io", desc: "Cloud native messaging", url: "https://github.com/nats-io/nats-server", stars: "14K+", language: "Go", topics: ["messaging", "pub-sub"], difficulty: "Intermediate", featured: false},
        {name: "Litestar", org: "litestar-org", desc: "Production-ready Python API framework", url: "https://github.com/litestar-org/litestar", stars: "4K+", language: "Python", topics: ["api", "python", "fast"], difficulty: "Intermediate", featured: false},
        {name: "Nitro", org: "unjs", desc: "Universal TypeScript backend", url: "https://github.com/unjs/nitro", stars: "5K+", language: "TypeScript", topics: ["backend", "universal", "edge"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== PRIVACY & SELF-HOSTED ====================
    privacy_selfhosted: [
        {name: "Pi-hole", org: "pi-hole", desc: "Network-wide ad blocking", url: "https://github.com/pi-hole/pi-hole", stars: "46K+", language: "Shell", topics: ["ad-blocking", "dns", "privacy"], difficulty: "Beginner", featured: true},
        {name: "Nextcloud", org: "nextcloud", desc: "Self-hosted cloud platform", url: "https://github.com/nextcloud/server", stars: "25K+", language: "PHP", topics: ["cloud", "files", "self-hosted"], difficulty: "Intermediate", featured: true},
        {name: "Bitwarden", org: "bitwarden", desc: "Open source password manager", url: "https://github.com/bitwarden/clients", stars: "4K+", language: "TypeScript", topics: ["passwords", "security"], difficulty: "Beginner", featured: true},
        {name: "Vaultwarden", org: "dani-garcia", desc: "Unofficial Bitwarden server", url: "https://github.com/dani-garcia/vaultwarden", stars: "33K+", language: "Rust", topics: ["passwords", "self-hosted"], difficulty: "Intermediate", featured: true},
        {name: "Uptime Kuma", org: "louislam", desc: "Self-hosted monitoring tool", url: "https://github.com/louislam/uptime-kuma", stars: "49K+", language: "JavaScript", topics: ["monitoring", "uptime", "self-hosted"], difficulty: "Beginner", featured: true},
        {name: "Immich", org: "immich-app", desc: "Self-hosted photo/video backup", url: "https://github.com/immich-app/immich", stars: "33K+", language: "TypeScript", topics: ["photos", "backup", "google-photos"], difficulty: "Intermediate", featured: true},
        {name: "Paperless-ngx", org: "paperless-ngx", desc: "Document management system", url: "https://github.com/paperless-ngx/paperless-ngx", stars: "16K+", language: "Python", topics: ["documents", "ocr", "self-hosted"], difficulty: "Intermediate", featured: false},
        {name: "Portainer", org: "portainer", desc: "Container management UI", url: "https://github.com/portainer/portainer", stars: "28K+", language: "Go", topics: ["docker", "containers", "ui"], difficulty: "Beginner", featured: true},
        {name: "Gitea", org: "go-gitea", desc: "Self-hosted Git service", url: "https://github.com/go-gitea/gitea", stars: "42K+", language: "Go", topics: ["git", "self-hosted", "forge"], difficulty: "Intermediate", featured: true},
        {name: "Forgejo", org: "forgejo", desc: "Community-driven Gitea fork", url: "https://codeberg.org/forgejo/forgejo", stars: "3K+", language: "Go", topics: ["git", "forge", "community"], difficulty: "Intermediate", featured: false},
    ]
};

// Merge with existing database
if (typeof window !== 'undefined') {
    window.GIT_REPOS_DATABASE_3 = GIT_REPOS_DATABASE_3;
}


