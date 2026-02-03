"""
Seed Skills Data - Comprehensive skill categories and skills
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models import get_db, SkillCategory, Skill

SKILL_CATEGORIES = [
    {
        "name": "Programming Languages",
        "slug": "programming",
        "description": "Core programming languages",
        "icon": "fas fa-code",
        "color": "#3b82f6",
        "display_order": 1,
        "skills": [
            "JavaScript", "TypeScript", "Python", "Java", "C++", "C#", "Go", "Rust",
            "Ruby", "PHP", "Kotlin", "Swift", "Scala", "R", "MATLAB", "Perl",
            "Haskell", "Clojure", "Elixir", "Dart", "Lua", "Julia", "Assembly",
            "Objective-C", "Visual Basic", "COBOL", "Fortran", "Shell/Bash"
        ]
    },
    {
        "name": "Frontend Development",
        "slug": "frontend",
        "description": "Frontend frameworks, libraries and tools",
        "icon": "fas fa-desktop",
        "color": "#8b5cf6",
        "display_order": 2,
        "skills": [
            "React", "Vue.js", "Angular", "Next.js", "Nuxt.js", "Svelte", "SvelteKit",
            "HTML5", "CSS3", "SASS/SCSS", "Less", "Tailwind CSS", "Bootstrap",
            "Material UI", "Chakra UI", "Ant Design", "Styled Components",
            "Redux", "Zustand", "Recoil", "MobX", "Vuex", "Pinia",
            "React Query", "SWR", "Apollo Client", "GraphQL",
            "Webpack", "Vite", "Rollup", "Parcel", "esbuild",
            "Jest", "Cypress", "Playwright", "Testing Library",
            "Storybook", "Figma", "Framer Motion", "GSAP", "Three.js",
            "WebGL", "D3.js", "Chart.js", "Recharts"
        ]
    },
    {
        "name": "Backend Development",
        "slug": "backend",
        "description": "Backend frameworks and server-side technologies",
        "icon": "fas fa-server",
        "color": "#10b981",
        "display_order": 3,
        "skills": [
            "Node.js", "Express.js", "NestJS", "Fastify", "Koa",
            "Django", "Flask", "FastAPI", "Tornado",
            "Spring Boot", "Spring MVC", "Hibernate",
            ".NET Core", "ASP.NET", "Entity Framework",
            "Ruby on Rails", "Sinatra",
            "Laravel", "Symfony", "CodeIgniter",
            "Gin", "Echo", "Fiber",
            "Phoenix", "Actix", "Rocket",
            "GraphQL", "REST API", "gRPC", "WebSocket",
            "OAuth", "JWT", "Passport.js",
            "Microservices", "Serverless", "API Gateway"
        ]
    },
    {
        "name": "Database",
        "slug": "database",
        "description": "Database management systems",
        "icon": "fas fa-database",
        "color": "#f59e0b",
        "display_order": 4,
        "skills": [
            "PostgreSQL", "MySQL", "MariaDB", "SQLite", "Oracle", "SQL Server",
            "MongoDB", "Cassandra", "DynamoDB", "CouchDB", "Couchbase",
            "Redis", "Memcached", "ElastiCache",
            "Elasticsearch", "Solr", "Algolia",
            "Neo4j", "ArangoDB", "Amazon Neptune",
            "InfluxDB", "TimescaleDB", "Prometheus",
            "Firebase", "Supabase", "PlanetScale",
            "Prisma", "TypeORM", "Sequelize", "SQLAlchemy", "Mongoose"
        ]
    },
    {
        "name": "Cloud & DevOps",
        "slug": "cloud-devops",
        "description": "Cloud platforms and DevOps tools",
        "icon": "fas fa-cloud",
        "color": "#ec4899",
        "display_order": 5,
        "skills": [
            "AWS", "Google Cloud Platform", "Microsoft Azure", "DigitalOcean", "Heroku",
            "AWS EC2", "AWS Lambda", "AWS S3", "AWS RDS", "AWS EKS", "AWS ECS",
            "GCP Compute", "Cloud Functions", "Cloud Run", "BigQuery", "GKE",
            "Azure Functions", "Azure DevOps", "Azure Kubernetes Service",
            "Docker", "Kubernetes", "Docker Compose", "Helm", "Podman",
            "Terraform", "Pulumi", "CloudFormation", "Ansible", "Chef", "Puppet",
            "Jenkins", "GitHub Actions", "GitLab CI", "CircleCI", "Travis CI", "ArgoCD",
            "Prometheus", "Grafana", "Datadog", "New Relic", "Splunk", "ELK Stack",
            "Nginx", "Apache", "HAProxy", "Traefik", "Envoy",
            "Vault", "Consul", "Kong", "Istio"
        ]
    },
    {
        "name": "AI & Machine Learning",
        "slug": "ai-ml",
        "description": "Artificial Intelligence and Machine Learning",
        "icon": "fas fa-brain",
        "color": "#6366f1",
        "display_order": 6,
        "skills": [
            "TensorFlow", "PyTorch", "Keras", "JAX", "MXNet",
            "Scikit-learn", "XGBoost", "LightGBM", "CatBoost",
            "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly",
            "OpenCV", "Pillow", "Albumentations",
            "NLTK", "spaCy", "Gensim", "TextBlob",
            "Hugging Face", "Transformers", "LangChain", "LlamaIndex",
            "OpenAI API", "Anthropic API", "Google AI",
            "Stable Diffusion", "DALL-E", "Midjourney",
            "MLflow", "Weights & Biases", "Neptune.ai",
            "ONNX", "TensorRT", "OpenVINO",
            "Jupyter", "Google Colab", "Kaggle Notebooks",
            "Deep Learning", "Computer Vision", "NLP", "Reinforcement Learning",
            "Time Series Analysis", "Recommendation Systems", "Anomaly Detection"
        ]
    },
    {
        "name": "Mobile Development",
        "slug": "mobile",
        "description": "Mobile app development",
        "icon": "fas fa-mobile-alt",
        "color": "#14b8a6",
        "display_order": 7,
        "skills": [
            "React Native", "Flutter", "Ionic", "Xamarin", "Cordova",
            "iOS Development", "Swift", "SwiftUI", "Objective-C", "UIKit",
            "Android Development", "Kotlin", "Java Android", "Jetpack Compose",
            "Expo", "NativeScript", "Capacitor",
            "Firebase", "AppCenter", "Fastlane",
            "App Store Connect", "Google Play Console",
            "Push Notifications", "In-App Purchases",
            "ARKit", "ARCore", "Core ML", "ML Kit"
        ]
    },
    {
        "name": "Data Engineering",
        "slug": "data-engineering",
        "description": "Data pipelines and processing",
        "icon": "fas fa-cogs",
        "color": "#f97316",
        "display_order": 8,
        "skills": [
            "Apache Spark", "Apache Kafka", "Apache Flink", "Apache Beam",
            "Apache Airflow", "Prefect", "Dagster", "Luigi",
            "dbt", "Great Expectations", "Apache NiFi",
            "Snowflake", "Databricks", "Redshift", "BigQuery",
            "Hive", "Presto", "Trino", "Apache Druid",
            "Apache Hadoop", "HDFS", "MapReduce",
            "Delta Lake", "Apache Iceberg", "Apache Hudi",
            "ETL", "ELT", "Data Warehousing", "Data Lake",
            "Data Modeling", "Star Schema", "Slowly Changing Dimensions",
            "CDC", "Stream Processing", "Batch Processing"
        ]
    },
    {
        "name": "Testing & QA",
        "slug": "testing",
        "description": "Testing frameworks and quality assurance",
        "icon": "fas fa-vial",
        "color": "#84cc16",
        "display_order": 9,
        "skills": [
            "Jest", "Mocha", "Chai", "Jasmine", "Vitest",
            "Pytest", "unittest", "nose", "Robot Framework",
            "JUnit", "TestNG", "Mockito",
            "Selenium", "Cypress", "Playwright", "Puppeteer", "WebdriverIO",
            "Appium", "Detox", "XCTest", "Espresso",
            "Postman", "Rest Assured", "Supertest",
            "k6", "Gatling", "JMeter", "Locust",
            "SonarQube", "CodeClimate", "Codacy",
            "TDD", "BDD", "E2E Testing", "Unit Testing",
            "Integration Testing", "Performance Testing", "Security Testing"
        ]
    },
    {
        "name": "Security",
        "slug": "security",
        "description": "Cybersecurity and application security",
        "icon": "fas fa-shield-alt",
        "color": "#ef4444",
        "display_order": 10,
        "skills": [
            "OWASP", "Penetration Testing", "Vulnerability Assessment",
            "OAuth 2.0", "OpenID Connect", "SAML", "SSO",
            "SSL/TLS", "HTTPS", "PKI", "Certificates",
            "Encryption", "Hashing", "Cryptography",
            "WAF", "DDoS Protection", "Firewall",
            "SIEM", "SOC", "Incident Response",
            "Compliance", "GDPR", "HIPAA", "SOC 2", "PCI DSS",
            "Burp Suite", "Nmap", "Metasploit", "Wireshark",
            "Static Analysis", "Dynamic Analysis", "Secure Code Review"
        ]
    },
    {
        "name": "Tools & Productivity",
        "slug": "tools",
        "description": "Development tools and productivity software",
        "icon": "fas fa-wrench",
        "color": "#64748b",
        "display_order": 11,
        "skills": [
            "Git", "GitHub", "GitLab", "Bitbucket",
            "VS Code", "IntelliJ IDEA", "PyCharm", "WebStorm", "Vim", "Neovim",
            "JIRA", "Confluence", "Trello", "Asana", "Linear", "Notion",
            "Slack", "Discord", "Microsoft Teams",
            "Figma", "Sketch", "Adobe XD", "Canva",
            "Postman", "Insomnia", "curl",
            "Linux", "macOS", "Windows", "WSL",
            "Bash", "Zsh", "PowerShell",
            "npm", "yarn", "pnpm", "pip", "poetry", "cargo", "maven", "gradle"
        ]
    },
    {
        "name": "Soft Skills",
        "slug": "soft-skills",
        "description": "Professional and interpersonal skills",
        "icon": "fas fa-users",
        "color": "#a855f7",
        "display_order": 12,
        "skills": [
            "Communication", "Leadership", "Team Management",
            "Problem Solving", "Critical Thinking", "Decision Making",
            "Project Management", "Agile", "Scrum", "Kanban",
            "Time Management", "Prioritization", "Organization",
            "Presentation", "Public Speaking", "Technical Writing",
            "Mentoring", "Coaching", "Interviewing",
            "Conflict Resolution", "Negotiation", "Collaboration",
            "Adaptability", "Creativity", "Innovation"
        ]
    }
]


def seed_skills():
    """Seed skill categories and skills"""
    db = next(get_db())
    
    try:
        for cat_data in SKILL_CATEGORIES:
            # Check if category exists
            existing_cat = db.query(SkillCategory).filter(
                SkillCategory.slug == cat_data["slug"]
            ).first()
            
            if existing_cat:
                category = existing_cat
                print(f"Category exists: {cat_data['name']}")
            else:
                category = SkillCategory(
                    name=cat_data["name"],
                    slug=cat_data["slug"],
                    description=cat_data["description"],
                    icon=cat_data["icon"],
                    color=cat_data["color"],
                    display_order=cat_data["display_order"]
                )
                db.add(category)
                db.flush()
                print(f"Created category: {cat_data['name']}")
            
            # Add skills
            for skill_name in cat_data["skills"]:
                skill_slug = skill_name.lower().replace(" ", "-").replace("/", "-").replace(".", "-").replace("#", "sharp")
                
                existing_skill = db.query(Skill).filter(
                    Skill.slug == skill_slug
                ).first()
                
                if not existing_skill:
                    skill = Skill(
                        category_id=category.id,
                        name=skill_name,
                        slug=skill_slug,
                        is_popular=skill_name in [
                            "JavaScript", "Python", "React", "Node.js", "AWS",
                            "Docker", "Kubernetes", "PostgreSQL", "MongoDB",
                            "TypeScript", "Java", "Git", "Linux"
                        ]
                    )
                    db.add(skill)
        
        db.commit()
        print("✅ Skills seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding skills: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_skills()
