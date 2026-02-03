// Comprehensive Git Repositories Database
// Top Open Source Projects across domains

const GIT_REPOS_DATABASE = {
    // ==================== AI / MACHINE LEARNING ====================
    ai_ml: [
        {name: "TensorFlow", org: "tensorflow", desc: "End-to-end open source ML platform by Google", url: "https://github.com/tensorflow/tensorflow", stars: "180K+", language: "C++/Python", topics: ["deep-learning", "ml", "neural-networks"], difficulty: "Advanced", featured: true},
        {name: "PyTorch", org: "pytorch", desc: "Tensors and dynamic neural networks with GPU acceleration", url: "https://github.com/pytorch/pytorch", stars: "75K+", language: "Python/C++", topics: ["deep-learning", "ml", "neural-networks"], difficulty: "Advanced", featured: true},
        {name: "Transformers", org: "huggingface", desc: "State-of-the-art NLP library with pretrained models", url: "https://github.com/huggingface/transformers", stars: "120K+", language: "Python", topics: ["nlp", "bert", "gpt", "llm"], difficulty: "Intermediate", featured: true},
        {name: "LangChain", org: "langchain-ai", desc: "Building LLM-powered applications", url: "https://github.com/langchain-ai/langchain", stars: "75K+", language: "Python", topics: ["llm", "rag", "agents", "chatbots"], difficulty: "Intermediate", featured: true},
        {name: "LlamaIndex", org: "run-llama", desc: "Data framework for LLM applications", url: "https://github.com/run-llama/llama_index", stars: "30K+", language: "Python", topics: ["llm", "rag", "embeddings"], difficulty: "Intermediate", featured: true},
        {name: "Scikit-learn", org: "scikit-learn", desc: "Machine learning in Python", url: "https://github.com/scikit-learn/scikit-learn", stars: "58K+", language: "Python", topics: ["ml", "classification", "regression"], difficulty: "Beginner", featured: true},
        {name: "Keras", org: "keras-team", desc: "Deep learning API running on TensorFlow", url: "https://github.com/keras-team/keras", stars: "60K+", language: "Python", topics: ["deep-learning", "neural-networks"], difficulty: "Intermediate", featured: false},
        {name: "FastAI", org: "fastai", desc: "Making deep learning accessible", url: "https://github.com/fastai/fastai", stars: "25K+", language: "Python", topics: ["deep-learning", "education"], difficulty: "Beginner", featured: false},
        {name: "OpenCV", org: "opencv", desc: "Open source computer vision library", url: "https://github.com/opencv/opencv", stars: "74K+", language: "C++", topics: ["computer-vision", "image-processing"], difficulty: "Intermediate", featured: true},
        {name: "Stable Diffusion", org: "CompVis", desc: "Latent text-to-image diffusion model", url: "https://github.com/CompVis/stable-diffusion", stars: "65K+", language: "Python", topics: ["generative-ai", "image-generation"], difficulty: "Advanced", featured: true},
        {name: "YOLO", org: "ultralytics", desc: "Real-time object detection", url: "https://github.com/ultralytics/ultralytics", stars: "20K+", language: "Python", topics: ["object-detection", "computer-vision"], difficulty: "Intermediate", featured: false},
        {name: "Detectron2", org: "facebookresearch", desc: "Facebook's object detection platform", url: "https://github.com/facebookresearch/detectron2", stars: "28K+", language: "Python", topics: ["object-detection", "segmentation"], difficulty: "Advanced", featured: false},
        {name: "MLflow", org: "mlflow", desc: "ML lifecycle management platform", url: "https://github.com/mlflow/mlflow", stars: "17K+", language: "Python", topics: ["mlops", "experiment-tracking"], difficulty: "Intermediate", featured: false},
        {name: "Ray", org: "ray-project", desc: "Unified framework for scaling AI", url: "https://github.com/ray-project/ray", stars: "30K+", language: "Python", topics: ["distributed", "scaling", "ml"], difficulty: "Advanced", featured: false},
        {name: "JAX", org: "google", desc: "Composable transformations of NumPy programs", url: "https://github.com/google/jax", stars: "27K+", language: "Python", topics: ["ml", "autograd", "xla"], difficulty: "Advanced", featured: false},
        {name: "Diffusers", org: "huggingface", desc: "State-of-the-art diffusion models", url: "https://github.com/huggingface/diffusers", stars: "22K+", language: "Python", topics: ["diffusion", "generative-ai"], difficulty: "Intermediate", featured: true},
        {name: "AutoGPT", org: "Significant-Gravitas", desc: "Autonomous GPT-4 agent", url: "https://github.com/Significant-Gravitas/AutoGPT", stars: "160K+", language: "Python", topics: ["agents", "autonomous", "llm"], difficulty: "Advanced", featured: true},
        {name: "CrewAI", org: "joaomdmoura", desc: "Framework for orchestrating AI agents", url: "https://github.com/joaomdmoura/crewAI", stars: "15K+", language: "Python", topics: ["agents", "multi-agent"], difficulty: "Intermediate", featured: true},
        {name: "Ollama", org: "ollama", desc: "Run LLMs locally", url: "https://github.com/ollama/ollama", stars: "55K+", language: "Go", topics: ["llm", "local", "inference"], difficulty: "Beginner", featured: true},
        {name: "LocalAI", org: "mudler", desc: "Free local OpenAI alternative", url: "https://github.com/mudler/LocalAI", stars: "20K+", language: "Go", topics: ["llm", "local", "api"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== WEB DEVELOPMENT ====================
    web_dev: [
        {name: "React", org: "facebook", desc: "JavaScript library for building user interfaces", url: "https://github.com/facebook/react", stars: "220K+", language: "JavaScript", topics: ["frontend", "ui", "components"], difficulty: "Intermediate", featured: true},
        {name: "Vue.js", org: "vuejs", desc: "Progressive JavaScript framework", url: "https://github.com/vuejs/vue", stars: "206K+", language: "JavaScript", topics: ["frontend", "framework"], difficulty: "Beginner", featured: true},
        {name: "Angular", org: "angular", desc: "Platform for building web applications", url: "https://github.com/angular/angular", stars: "94K+", language: "TypeScript", topics: ["frontend", "framework", "enterprise"], difficulty: "Advanced", featured: true},
        {name: "Next.js", org: "vercel", desc: "React framework for production", url: "https://github.com/vercel/next.js", stars: "120K+", language: "JavaScript", topics: ["react", "ssr", "fullstack"], difficulty: "Intermediate", featured: true},
        {name: "Svelte", org: "sveltejs", desc: "Cybernetically enhanced web apps", url: "https://github.com/sveltejs/svelte", stars: "76K+", language: "JavaScript", topics: ["frontend", "compiler"], difficulty: "Beginner", featured: true},
        {name: "Tailwind CSS", org: "tailwindlabs", desc: "Utility-first CSS framework", url: "https://github.com/tailwindlabs/tailwindcss", stars: "77K+", language: "CSS", topics: ["css", "utility", "styling"], difficulty: "Beginner", featured: true},
        {name: "Bootstrap", org: "twbs", desc: "Most popular CSS framework", url: "https://github.com/twbs/bootstrap", stars: "167K+", language: "CSS/JS", topics: ["css", "components", "responsive"], difficulty: "Beginner", featured: false},
        {name: "Astro", org: "withastro", desc: "Content-driven website framework", url: "https://github.com/withastro/astro", stars: "40K+", language: "TypeScript", topics: ["static-site", "performance"], difficulty: "Intermediate", featured: true},
        {name: "Remix", org: "remix-run", desc: "Full stack web framework", url: "https://github.com/remix-run/remix", stars: "27K+", language: "TypeScript", topics: ["fullstack", "react", "ssr"], difficulty: "Intermediate", featured: false},
        {name: "SolidJS", org: "solidjs", desc: "Declarative, efficient reactive UI library", url: "https://github.com/solidjs/solid", stars: "30K+", language: "TypeScript", topics: ["frontend", "reactive"], difficulty: "Intermediate", featured: false},
        {name: "htmx", org: "bigskysoftware", desc: "High power tools for HTML", url: "https://github.com/bigskysoftware/htmx", stars: "32K+", language: "JavaScript", topics: ["hypermedia", "html"], difficulty: "Beginner", featured: true},
        {name: "Alpine.js", org: "alpinejs", desc: "Rugged, minimal tool for composing behavior", url: "https://github.com/alpinejs/alpine", stars: "26K+", language: "JavaScript", topics: ["lightweight", "vanilla"], difficulty: "Beginner", featured: false},
        {name: "Three.js", org: "mrdoob", desc: "3D library for JavaScript", url: "https://github.com/mrdoob/three.js", stars: "98K+", language: "JavaScript", topics: ["3d", "webgl", "graphics"], difficulty: "Intermediate", featured: true},
        {name: "D3.js", org: "d3", desc: "Data-driven documents visualization", url: "https://github.com/d3/d3", stars: "107K+", language: "JavaScript", topics: ["visualization", "charts", "data"], difficulty: "Advanced", featured: false},
        {name: "Chart.js", org: "chartjs", desc: "Simple yet flexible charting", url: "https://github.com/chartjs/Chart.js", stars: "63K+", language: "JavaScript", topics: ["charts", "visualization"], difficulty: "Beginner", featured: false},
        {name: "Framer Motion", org: "framer", desc: "Production-ready motion library for React", url: "https://github.com/framer/motion", stars: "22K+", language: "TypeScript", topics: ["animation", "react"], difficulty: "Intermediate", featured: false},
        {name: "Shadcn/ui", org: "shadcn-ui", desc: "Beautifully designed components", url: "https://github.com/shadcn-ui/ui", stars: "55K+", language: "TypeScript", topics: ["components", "radix", "tailwind"], difficulty: "Intermediate", featured: true},
        {name: "Radix UI", org: "radix-ui", desc: "Unstyled, accessible UI primitives", url: "https://github.com/radix-ui/primitives", stars: "14K+", language: "TypeScript", topics: ["a11y", "headless"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== BACKEND & APIs ====================
    backend: [
        {name: "Node.js", org: "nodejs", desc: "JavaScript runtime built on V8", url: "https://github.com/nodejs/node", stars: "102K+", language: "C++/JS", topics: ["runtime", "server", "javascript"], difficulty: "Intermediate", featured: true},
        {name: "Express.js", org: "expressjs", desc: "Fast, unopinionated web framework for Node", url: "https://github.com/expressjs/express", stars: "63K+", language: "JavaScript", topics: ["api", "web-framework"], difficulty: "Beginner", featured: true},
        {name: "FastAPI", org: "tiangolo", desc: "Modern, fast Python web framework", url: "https://github.com/tiangolo/fastapi", stars: "70K+", language: "Python", topics: ["api", "async", "openapi"], difficulty: "Intermediate", featured: true},
        {name: "Django", org: "django", desc: "High-level Python web framework", url: "https://github.com/django/django", stars: "76K+", language: "Python", topics: ["web-framework", "orm", "admin"], difficulty: "Intermediate", featured: true},
        {name: "Flask", org: "pallets", desc: "Lightweight WSGI web application framework", url: "https://github.com/pallets/flask", stars: "66K+", language: "Python", topics: ["web-framework", "microframework"], difficulty: "Beginner", featured: true},
        {name: "Spring Boot", org: "spring-projects", desc: "Java-based framework for microservices", url: "https://github.com/spring-projects/spring-boot", stars: "72K+", language: "Java", topics: ["java", "enterprise", "microservices"], difficulty: "Advanced", featured: true},
        {name: "NestJS", org: "nestjs", desc: "Progressive Node.js framework", url: "https://github.com/nestjs/nest", stars: "63K+", language: "TypeScript", topics: ["node", "enterprise", "typescript"], difficulty: "Intermediate", featured: true},
        {name: "Go Fiber", org: "gofiber", desc: "Express-inspired Go web framework", url: "https://github.com/gofiber/fiber", stars: "31K+", language: "Go", topics: ["go", "fast", "api"], difficulty: "Intermediate", featured: false},
        {name: "Gin", org: "gin-gonic", desc: "HTTP web framework written in Go", url: "https://github.com/gin-gonic/gin", stars: "74K+", language: "Go", topics: ["go", "api", "performance"], difficulty: "Intermediate", featured: true},
        {name: "Echo", org: "labstack", desc: "High performance Go web framework", url: "https://github.com/labstack/echo", stars: "28K+", language: "Go", topics: ["go", "api"], difficulty: "Intermediate", featured: false},
        {name: "Actix Web", org: "actix", desc: "Powerful Rust web framework", url: "https://github.com/actix/actix-web", stars: "20K+", language: "Rust", topics: ["rust", "async", "fast"], difficulty: "Advanced", featured: false},
        {name: "Rocket", org: "SergioBenitez", desc: "Web framework for Rust", url: "https://github.com/SergioBenitez/Rocket", stars: "23K+", language: "Rust", topics: ["rust", "web"], difficulty: "Advanced", featured: false},
        {name: "Rails", org: "rails", desc: "Ruby on Rails web framework", url: "https://github.com/rails/rails", stars: "54K+", language: "Ruby", topics: ["ruby", "mvc", "convention"], difficulty: "Intermediate", featured: true},
        {name: "Laravel", org: "laravel", desc: "PHP framework for web artisans", url: "https://github.com/laravel/laravel", stars: "76K+", language: "PHP", topics: ["php", "mvc", "eloquent"], difficulty: "Intermediate", featured: true},
        {name: "Phoenix", org: "phoenixframework", desc: "Elixir web framework", url: "https://github.com/phoenixframework/phoenix", stars: "20K+", language: "Elixir", topics: ["elixir", "realtime", "liveview"], difficulty: "Advanced", featured: false},
        {name: "Hono", org: "honojs", desc: "Ultrafast web framework for the Edge", url: "https://github.com/honojs/hono", stars: "14K+", language: "TypeScript", topics: ["edge", "cloudflare", "fast"], difficulty: "Intermediate", featured: true},
        {name: "tRPC", org: "trpc", desc: "End-to-end typesafe APIs", url: "https://github.com/trpc/trpc", stars: "32K+", language: "TypeScript", topics: ["typescript", "rpc", "fullstack"], difficulty: "Intermediate", featured: true},
        {name: "GraphQL", org: "graphql", desc: "Query language for APIs", url: "https://github.com/graphql/graphql-js", stars: "20K+", language: "TypeScript", topics: ["api", "query", "specification"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== DATABASES ====================
    databases: [
        {name: "PostgreSQL", org: "postgres", desc: "World's most advanced open source database", url: "https://github.com/postgres/postgres", stars: "14K+", language: "C", topics: ["sql", "relational", "enterprise"], difficulty: "Intermediate", featured: true},
        {name: "MongoDB", org: "mongodb", desc: "Document-oriented NoSQL database", url: "https://github.com/mongodb/mongo", stars: "25K+", language: "C++", topics: ["nosql", "document", "scalable"], difficulty: "Intermediate", featured: true},
        {name: "Redis", org: "redis", desc: "In-memory data structure store", url: "https://github.com/redis/redis", stars: "64K+", language: "C", topics: ["cache", "key-value", "fast"], difficulty: "Beginner", featured: true},
        {name: "SQLite", org: "sqlite", desc: "Embedded SQL database engine", url: "https://github.com/sqlite/sqlite", stars: "5K+", language: "C", topics: ["embedded", "sql", "lightweight"], difficulty: "Beginner", featured: true},
        {name: "MySQL", org: "mysql", desc: "Popular open source SQL database", url: "https://github.com/mysql/mysql-server", stars: "10K+", language: "C++", topics: ["sql", "relational"], difficulty: "Intermediate", featured: false},
        {name: "Supabase", org: "supabase", desc: "Open source Firebase alternative", url: "https://github.com/supabase/supabase", stars: "65K+", language: "TypeScript", topics: ["postgres", "realtime", "auth"], difficulty: "Beginner", featured: true},
        {name: "PocketBase", org: "pocketbase", desc: "Backend in a single Go file", url: "https://github.com/pocketbase/pocketbase", stars: "33K+", language: "Go", topics: ["backend", "sqlite", "realtime"], difficulty: "Beginner", featured: true},
        {name: "Prisma", org: "prisma", desc: "Next-generation ORM for Node.js", url: "https://github.com/prisma/prisma", stars: "36K+", language: "TypeScript", topics: ["orm", "typescript", "database"], difficulty: "Intermediate", featured: true},
        {name: "Drizzle ORM", org: "drizzle-team", desc: "TypeScript ORM with SQL-like syntax", url: "https://github.com/drizzle-team/drizzle-orm", stars: "20K+", language: "TypeScript", topics: ["orm", "typescript", "sql"], difficulty: "Intermediate", featured: true},
        {name: "ClickHouse", org: "ClickHouse", desc: "OLAP database for analytics", url: "https://github.com/ClickHouse/ClickHouse", stars: "33K+", language: "C++", topics: ["analytics", "columnar", "fast"], difficulty: "Advanced", featured: false},
        {name: "CockroachDB", org: "cockroachdb", desc: "Distributed SQL database", url: "https://github.com/cockroachdb/cockroach", stars: "29K+", language: "Go", topics: ["distributed", "sql", "scalable"], difficulty: "Advanced", featured: false},
        {name: "TiDB", org: "pingcap", desc: "Distributed NewSQL database", url: "https://github.com/pingcap/tidb", stars: "36K+", language: "Go", topics: ["distributed", "mysql-compatible"], difficulty: "Advanced", featured: false},
        {name: "Vitess", org: "vitessio", desc: "Database clustering for MySQL", url: "https://github.com/vitessio/vitess", stars: "17K+", language: "Go", topics: ["mysql", "sharding", "kubernetes"], difficulty: "Advanced", featured: false},
        {name: "DuckDB", org: "duckdb", desc: "In-process analytical database", url: "https://github.com/duckdb/duckdb", stars: "17K+", language: "C++", topics: ["analytics", "embedded", "olap"], difficulty: "Intermediate", featured: true},
    ],

    // ==================== DEVOPS & INFRASTRUCTURE ====================
    devops: [
        {name: "Kubernetes", org: "kubernetes", desc: "Container orchestration platform", url: "https://github.com/kubernetes/kubernetes", stars: "106K+", language: "Go", topics: ["containers", "orchestration", "cloud-native"], difficulty: "Advanced", featured: true},
        {name: "Docker", org: "moby", desc: "Container runtime (Moby project)", url: "https://github.com/moby/moby", stars: "67K+", language: "Go", topics: ["containers", "virtualization"], difficulty: "Intermediate", featured: true},
        {name: "Terraform", org: "hashicorp", desc: "Infrastructure as Code tool", url: "https://github.com/hashicorp/terraform", stars: "41K+", language: "Go", topics: ["iac", "cloud", "provisioning"], difficulty: "Intermediate", featured: true},
        {name: "Ansible", org: "ansible", desc: "IT automation platform", url: "https://github.com/ansible/ansible", stars: "60K+", language: "Python", topics: ["automation", "configuration", "devops"], difficulty: "Intermediate", featured: true},
        {name: "Prometheus", org: "prometheus", desc: "Monitoring and alerting toolkit", url: "https://github.com/prometheus/prometheus", stars: "52K+", language: "Go", topics: ["monitoring", "metrics", "alerting"], difficulty: "Intermediate", featured: true},
        {name: "Grafana", org: "grafana", desc: "Observability and data visualization", url: "https://github.com/grafana/grafana", stars: "60K+", language: "TypeScript/Go", topics: ["visualization", "dashboards", "monitoring"], difficulty: "Intermediate", featured: true},
        {name: "Helm", org: "helm", desc: "Package manager for Kubernetes", url: "https://github.com/helm/helm", stars: "26K+", language: "Go", topics: ["kubernetes", "package-manager"], difficulty: "Intermediate", featured: false},
        {name: "ArgoCD", org: "argoproj", desc: "GitOps continuous delivery", url: "https://github.com/argoproj/argo-cd", stars: "16K+", language: "Go", topics: ["gitops", "kubernetes", "cd"], difficulty: "Intermediate", featured: true},
        {name: "Jenkins", org: "jenkinsci", desc: "Automation server for CI/CD", url: "https://github.com/jenkinsci/jenkins", stars: "22K+", language: "Java", topics: ["ci", "cd", "automation"], difficulty: "Intermediate", featured: false},
        {name: "GitHub Actions", org: "actions", desc: "Automate workflows", url: "https://github.com/actions/runner", stars: "4K+", language: "C#", topics: ["ci", "cd", "automation"], difficulty: "Beginner", featured: true},
        {name: "Nginx", org: "nginx", desc: "Web server and reverse proxy", url: "https://github.com/nginx/nginx", stars: "20K+", language: "C", topics: ["web-server", "proxy", "load-balancer"], difficulty: "Intermediate", featured: true},
        {name: "Traefik", org: "traefik", desc: "Cloud-native edge router", url: "https://github.com/traefik/traefik", stars: "47K+", language: "Go", topics: ["reverse-proxy", "kubernetes", "edge"], difficulty: "Intermediate", featured: false},
        {name: "Caddy", org: "caddyserver", desc: "Fast web server with automatic HTTPS", url: "https://github.com/caddyserver/caddy", stars: "53K+", language: "Go", topics: ["web-server", "https", "simple"], difficulty: "Beginner", featured: true},
        {name: "Vault", org: "hashicorp", desc: "Secrets management", url: "https://github.com/hashicorp/vault", stars: "29K+", language: "Go", topics: ["secrets", "security", "encryption"], difficulty: "Advanced", featured: false},
        {name: "Consul", org: "hashicorp", desc: "Service mesh and discovery", url: "https://github.com/hashicorp/consul", stars: "27K+", language: "Go", topics: ["service-mesh", "discovery"], difficulty: "Advanced", featured: false},
        {name: "Istio", org: "istio", desc: "Service mesh for Kubernetes", url: "https://github.com/istio/istio", stars: "35K+", language: "Go", topics: ["service-mesh", "kubernetes", "networking"], difficulty: "Advanced", featured: false},
    ],

    // ==================== MOBILE DEVELOPMENT ====================
    mobile: [
        {name: "React Native", org: "facebook", desc: "Build mobile apps using React", url: "https://github.com/facebook/react-native", stars: "115K+", language: "JavaScript", topics: ["mobile", "cross-platform", "react"], difficulty: "Intermediate", featured: true},
        {name: "Flutter", org: "flutter", desc: "Google's UI toolkit for mobile/web/desktop", url: "https://github.com/flutter/flutter", stars: "160K+", language: "Dart", topics: ["mobile", "cross-platform", "ui"], difficulty: "Intermediate", featured: true},
        {name: "Expo", org: "expo", desc: "Universal React Native applications", url: "https://github.com/expo/expo", stars: "28K+", language: "TypeScript", topics: ["react-native", "mobile", "tools"], difficulty: "Beginner", featured: true},
        {name: "Swift", org: "apple", desc: "Apple's programming language", url: "https://github.com/apple/swift", stars: "65K+", language: "Swift", topics: ["ios", "macos", "apple"], difficulty: "Intermediate", featured: true},
        {name: "Kotlin", org: "JetBrains", desc: "Modern JVM language", url: "https://github.com/JetBrains/kotlin", stars: "47K+", language: "Kotlin", topics: ["android", "jvm", "multiplatform"], difficulty: "Intermediate", featured: true},
        {name: "Jetpack Compose", org: "androidx", desc: "Android's modern UI toolkit", url: "https://github.com/androidx/androidx", stars: "5K+", language: "Kotlin", topics: ["android", "ui", "declarative"], difficulty: "Intermediate", featured: false},
        {name: "SwiftUI", org: "apple", desc: "Declarative UI framework for Apple", url: "https://developer.apple.com/xcode/swiftui/", stars: "N/A", language: "Swift", topics: ["ios", "macos", "declarative"], difficulty: "Intermediate", featured: false},
        {name: "Capacitor", org: "ionic-team", desc: "Cross-platform native runtime", url: "https://github.com/ionic-team/capacitor", stars: "11K+", language: "TypeScript", topics: ["hybrid", "pwa", "native"], difficulty: "Beginner", featured: false},
        {name: "Tauri", org: "tauri-apps", desc: "Build desktop apps with web tech", url: "https://github.com/tauri-apps/tauri", stars: "77K+", language: "Rust", topics: ["desktop", "lightweight", "secure"], difficulty: "Intermediate", featured: true},
        {name: "Electron", org: "electron", desc: "Build cross-platform desktop apps", url: "https://github.com/electron/electron", stars: "111K+", language: "C++/JS", topics: ["desktop", "cross-platform"], difficulty: "Intermediate", featured: true},
    ],

    // ==================== SECURITY ====================
    security: [
        {name: "OWASP ZAP", org: "zaproxy", desc: "Web application security scanner", url: "https://github.com/zaproxy/zaproxy", stars: "12K+", language: "Java", topics: ["security", "scanning", "pentest"], difficulty: "Intermediate", featured: true},
        {name: "Metasploit", org: "rapid7", desc: "Penetration testing framework", url: "https://github.com/rapid7/metasploit-framework", stars: "32K+", language: "Ruby", topics: ["pentest", "exploitation", "security"], difficulty: "Advanced", featured: true},
        {name: "Nmap", org: "nmap", desc: "Network discovery and security auditing", url: "https://github.com/nmap/nmap", stars: "9K+", language: "C", topics: ["networking", "scanning", "security"], difficulty: "Intermediate", featured: true},
        {name: "Burp Suite (Community)", org: "portswigger", desc: "Web security testing", url: "https://portswigger.net/burp/communitydownload", stars: "N/A", language: "Java", topics: ["web-security", "proxy"], difficulty: "Intermediate", featured: false},
        {name: "Nuclei", org: "projectdiscovery", desc: "Fast vulnerability scanner", url: "https://github.com/projectdiscovery/nuclei", stars: "17K+", language: "Go", topics: ["vulnerability", "scanning", "templates"], difficulty: "Intermediate", featured: true},
        {name: "Trivy", org: "aquasecurity", desc: "Comprehensive vulnerability scanner", url: "https://github.com/aquasecurity/trivy", stars: "21K+", language: "Go", topics: ["container-security", "iac", "sbom"], difficulty: "Beginner", featured: true},
        {name: "Snyk", org: "snyk", desc: "Developer security platform", url: "https://github.com/snyk/cli", stars: "5K+", language: "TypeScript", topics: ["devsecops", "dependencies"], difficulty: "Beginner", featured: false},
        {name: "Semgrep", org: "semgrep", desc: "Static analysis tool", url: "https://github.com/semgrep/semgrep", stars: "9K+", language: "OCaml", topics: ["sast", "code-analysis"], difficulty: "Intermediate", featured: false},
        {name: "Falco", org: "falcosecurity", desc: "Cloud-native runtime security", url: "https://github.com/falcosecurity/falco", stars: "6K+", language: "C++", topics: ["kubernetes", "runtime-security"], difficulty: "Advanced", featured: false},
        {name: "HashiCorp Vault", org: "hashicorp", desc: "Secrets management", url: "https://github.com/hashicorp/vault", stars: "29K+", language: "Go", topics: ["secrets", "encryption", "iam"], difficulty: "Advanced", featured: true},
    ],

    // ==================== DATA ENGINEERING ====================
    data_engineering: [
        {name: "Apache Spark", org: "apache", desc: "Unified analytics engine for big data", url: "https://github.com/apache/spark", stars: "38K+", language: "Scala", topics: ["big-data", "analytics", "distributed"], difficulty: "Advanced", featured: true},
        {name: "Apache Kafka", org: "apache", desc: "Distributed event streaming platform", url: "https://github.com/apache/kafka", stars: "27K+", language: "Java/Scala", topics: ["streaming", "messaging", "event-driven"], difficulty: "Advanced", featured: true},
        {name: "Apache Airflow", org: "apache", desc: "Workflow orchestration platform", url: "https://github.com/apache/airflow", stars: "34K+", language: "Python", topics: ["workflow", "scheduling", "etl"], difficulty: "Intermediate", featured: true},
        {name: "dbt", org: "dbt-labs", desc: "Data transformation tool", url: "https://github.com/dbt-labs/dbt-core", stars: "8K+", language: "Python", topics: ["analytics", "transformation", "sql"], difficulty: "Intermediate", featured: true},
        {name: "Apache Flink", org: "apache", desc: "Stream processing framework", url: "https://github.com/apache/flink", stars: "23K+", language: "Java", topics: ["streaming", "real-time", "stateful"], difficulty: "Advanced", featured: false},
        {name: "Dagster", org: "dagster-io", desc: "Data orchestration platform", url: "https://github.com/dagster-io/dagster", stars: "10K+", language: "Python", topics: ["orchestration", "data-pipeline"], difficulty: "Intermediate", featured: false},
        {name: "Prefect", org: "PrefectHQ", desc: "Modern workflow orchestration", url: "https://github.com/PrefectHQ/prefect", stars: "14K+", language: "Python", topics: ["workflow", "orchestration"], difficulty: "Intermediate", featured: false},
        {name: "Great Expectations", org: "great-expectations", desc: "Data quality and testing", url: "https://github.com/great-expectations/great_expectations", stars: "9K+", language: "Python", topics: ["data-quality", "testing", "validation"], difficulty: "Intermediate", featured: false},
        {name: "Delta Lake", org: "delta-io", desc: "Storage layer for data lakes", url: "https://github.com/delta-io/delta", stars: "7K+", language: "Scala", topics: ["data-lake", "acid", "spark"], difficulty: "Advanced", featured: false},
        {name: "Trino", org: "trinodb", desc: "Distributed SQL query engine", url: "https://github.com/trinodb/trino", stars: "9K+", language: "Java", topics: ["sql", "distributed", "analytics"], difficulty: "Advanced", featured: false},
        {name: "Mage", org: "mage-ai", desc: "Modern data pipeline tool", url: "https://github.com/mage-ai/mage-ai", stars: "7K+", language: "Python", topics: ["etl", "pipeline", "ml"], difficulty: "Beginner", featured: true},
        {name: "Polars", org: "pola-rs", desc: "Fast DataFrame library", url: "https://github.com/pola-rs/polars", stars: "26K+", language: "Rust", topics: ["dataframe", "fast", "analytics"], difficulty: "Intermediate", featured: true},
    ],

    // ==================== BLOCKCHAIN & WEB3 ====================
    blockchain: [
        {name: "Bitcoin", org: "bitcoin", desc: "Bitcoin core implementation", url: "https://github.com/bitcoin/bitcoin", stars: "75K+", language: "C++", topics: ["cryptocurrency", "blockchain", "p2p"], difficulty: "Advanced", featured: true},
        {name: "Ethereum (go-ethereum)", org: "ethereum", desc: "Go implementation of Ethereum", url: "https://github.com/ethereum/go-ethereum", stars: "46K+", language: "Go", topics: ["ethereum", "smart-contracts", "evm"], difficulty: "Advanced", featured: true},
        {name: "Solidity", org: "ethereum", desc: "Smart contract language", url: "https://github.com/ethereum/solidity", stars: "22K+", language: "C++", topics: ["smart-contracts", "ethereum"], difficulty: "Intermediate", featured: true},
        {name: "Hardhat", org: "NomicFoundation", desc: "Ethereum development environment", url: "https://github.com/NomicFoundation/hardhat", stars: "6K+", language: "TypeScript", topics: ["ethereum", "development", "testing"], difficulty: "Intermediate", featured: true},
        {name: "Foundry", org: "foundry-rs", desc: "Blazing fast Ethereum toolkit", url: "https://github.com/foundry-rs/foundry", stars: "7K+", language: "Rust", topics: ["ethereum", "testing", "fast"], difficulty: "Intermediate", featured: true},
        {name: "OpenZeppelin Contracts", org: "OpenZeppelin", desc: "Secure smart contract library", url: "https://github.com/OpenZeppelin/openzeppelin-contracts", stars: "24K+", language: "Solidity", topics: ["security", "standards", "erc20"], difficulty: "Intermediate", featured: true},
        {name: "Web3.js", org: "web3", desc: "Ethereum JavaScript API", url: "https://github.com/web3/web3.js", stars: "18K+", language: "TypeScript", topics: ["ethereum", "javascript", "api"], difficulty: "Intermediate", featured: false},
        {name: "Ethers.js", org: "ethers-io", desc: "Complete Ethereum library", url: "https://github.com/ethers-io/ethers.js", stars: "7K+", language: "TypeScript", topics: ["ethereum", "wallet", "api"], difficulty: "Intermediate", featured: true},
        {name: "Viem", org: "wagmi-dev", desc: "TypeScript interface for Ethereum", url: "https://github.com/wagmi-dev/viem", stars: "2K+", language: "TypeScript", topics: ["ethereum", "typescript"], difficulty: "Intermediate", featured: false},
        {name: "Wagmi", org: "wagmi-dev", desc: "React hooks for Ethereum", url: "https://github.com/wagmi-dev/wagmi", stars: "5K+", language: "TypeScript", topics: ["react", "ethereum", "hooks"], difficulty: "Intermediate", featured: false},
        {name: "Anchor", org: "coral-xyz", desc: "Solana smart contract framework", url: "https://github.com/coral-xyz/anchor", stars: "3K+", language: "Rust", topics: ["solana", "smart-contracts"], difficulty: "Advanced", featured: false},
    ],

    // ==================== TESTING ====================
    testing: [
        {name: "Jest", org: "jestjs", desc: "JavaScript testing framework", url: "https://github.com/jestjs/jest", stars: "43K+", language: "TypeScript", topics: ["testing", "javascript", "unit-tests"], difficulty: "Beginner", featured: true},
        {name: "Playwright", org: "microsoft", desc: "Cross-browser end-to-end testing", url: "https://github.com/microsoft/playwright", stars: "61K+", language: "TypeScript", topics: ["e2e", "browser", "automation"], difficulty: "Intermediate", featured: true},
        {name: "Cypress", org: "cypress-io", desc: "JavaScript end-to-end testing", url: "https://github.com/cypress-io/cypress", stars: "46K+", language: "JavaScript", topics: ["e2e", "testing", "browser"], difficulty: "Beginner", featured: true},
        {name: "Selenium", org: "SeleniumHQ", desc: "Browser automation framework", url: "https://github.com/SeleniumHQ/selenium", stars: "29K+", language: "Java", topics: ["automation", "browser", "testing"], difficulty: "Intermediate", featured: true},
        {name: "Pytest", org: "pytest-dev", desc: "Python testing framework", url: "https://github.com/pytest-dev/pytest", stars: "11K+", language: "Python", topics: ["testing", "python", "fixtures"], difficulty: "Beginner", featured: true},
        {name: "Vitest", org: "vitest-dev", desc: "Blazing fast Vite-native testing", url: "https://github.com/vitest-dev/vitest", stars: "11K+", language: "TypeScript", topics: ["testing", "vite", "fast"], difficulty: "Beginner", featured: true},
        {name: "Testing Library", org: "testing-library", desc: "Simple testing utilities", url: "https://github.com/testing-library/react-testing-library", stars: "18K+", language: "JavaScript", topics: ["react", "dom", "accessibility"], difficulty: "Beginner", featured: false},
        {name: "Puppeteer", org: "puppeteer", desc: "Headless Chrome automation", url: "https://github.com/puppeteer/puppeteer", stars: "86K+", language: "TypeScript", topics: ["automation", "chrome", "scraping"], difficulty: "Intermediate", featured: false},
        {name: "k6", org: "grafana", desc: "Modern load testing tool", url: "https://github.com/grafana/k6", stars: "23K+", language: "Go", topics: ["load-testing", "performance"], difficulty: "Intermediate", featured: false},
        {name: "Locust", org: "locustio", desc: "Python load testing tool", url: "https://github.com/locustio/locust", stars: "23K+", language: "Python", topics: ["load-testing", "python"], difficulty: "Intermediate", featured: false},
    ],

    // ==================== DEVELOPER TOOLS ====================
    dev_tools: [
        {name: "VS Code", org: "microsoft", desc: "Open source code editor", url: "https://github.com/microsoft/vscode", stars: "157K+", language: "TypeScript", topics: ["editor", "ide", "extensions"], difficulty: "Beginner", featured: true},
        {name: "Neovim", org: "neovim", desc: "Vim-fork focused on extensibility", url: "https://github.com/neovim/neovim", stars: "76K+", language: "C/Lua", topics: ["editor", "vim", "terminal"], difficulty: "Advanced", featured: true},
        {name: "Git", org: "git", desc: "Distributed version control system", url: "https://github.com/git/git", stars: "49K+", language: "C", topics: ["version-control", "distributed"], difficulty: "Intermediate", featured: true},
        {name: "GitHub CLI", org: "cli", desc: "GitHub's official command line tool", url: "https://github.com/cli/cli", stars: "35K+", language: "Go", topics: ["cli", "github", "productivity"], difficulty: "Beginner", featured: false},
        {name: "Lazygit", org: "jesseduffield", desc: "Terminal UI for git commands", url: "https://github.com/jesseduffield/lazygit", stars: "45K+", language: "Go", topics: ["git", "terminal", "ui"], difficulty: "Beginner", featured: true},
        {name: "Oh My Zsh", org: "ohmyzsh", desc: "Zsh configuration manager", url: "https://github.com/ohmyzsh/ohmyzsh", stars: "168K+", language: "Shell", topics: ["shell", "zsh", "productivity"], difficulty: "Beginner", featured: true},
        {name: "Starship", org: "starship", desc: "Minimal, fast shell prompt", url: "https://github.com/starship/starship", stars: "40K+", language: "Rust", topics: ["shell", "prompt", "customization"], difficulty: "Beginner", featured: false},
        {name: "fzf", org: "junegunn", desc: "Command-line fuzzy finder", url: "https://github.com/junegunn/fzf", stars: "59K+", language: "Go", topics: ["cli", "fuzzy-finder", "productivity"], difficulty: "Beginner", featured: true},
        {name: "ripgrep", org: "BurntSushi", desc: "Fast text search tool", url: "https://github.com/BurntSushi/ripgrep", stars: "44K+", language: "Rust", topics: ["search", "grep", "fast"], difficulty: "Beginner", featured: false},
        {name: "tmux", org: "tmux", desc: "Terminal multiplexer", url: "https://github.com/tmux/tmux", stars: "32K+", language: "C", topics: ["terminal", "multiplexer"], difficulty: "Intermediate", featured: false},
        {name: "Zed", org: "zed-industries", desc: "High-performance code editor", url: "https://github.com/zed-industries/zed", stars: "35K+", language: "Rust", topics: ["editor", "fast", "collaborative"], difficulty: "Beginner", featured: true},
        {name: "Warp", org: "warpdotdev", desc: "Modern, Rust-based terminal", url: "https://github.com/warpdotdev/Warp", stars: "18K+", language: "Rust", topics: ["terminal", "modern", "ai"], difficulty: "Beginner", featured: false},
    ]
};

// Export
if (typeof window !== 'undefined') {
    window.GIT_REPOS_DATABASE = GIT_REPOS_DATABASE;
}


