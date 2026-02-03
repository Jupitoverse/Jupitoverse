"""
Seed Git Repositories Data - Popular repos for learning and reference
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models import get_db, GitRepository

GIT_REPOSITORIES = [
    # ==================== LEARNING & ROADMAPS ====================
    {
        "name": "developer-roadmap",
        "full_name": "kamranahmedse/developer-roadmap",
        "description": "Interactive roadmaps, guides and educational content to help developers grow in their careers",
        "owner_name": "kamranahmedse",
        "html_url": "https://github.com/kamranahmedse/developer-roadmap",
        "homepage": "https://roadmap.sh",
        "stars": 280000,
        "language": "TypeScript",
        "topics": ["roadmap", "learning", "career", "frontend", "backend", "devops"],
        "category": "learning",
        "skill_level": "beginner",
        "is_featured": True
    },
    {
        "name": "free-programming-books",
        "full_name": "EbookFoundation/free-programming-books",
        "description": "Freely available programming books and resources",
        "owner_name": "EbookFoundation",
        "html_url": "https://github.com/EbookFoundation/free-programming-books",
        "stars": 320000,
        "language": None,
        "topics": ["books", "learning", "resources", "free"],
        "category": "learning",
        "skill_level": "beginner",
        "is_featured": True
    },
    {
        "name": "coding-interview-university",
        "full_name": "jwasham/coding-interview-university",
        "description": "A complete computer science study plan to become a software engineer",
        "owner_name": "jwasham",
        "html_url": "https://github.com/jwasham/coding-interview-university",
        "stars": 290000,
        "language": None,
        "topics": ["interview", "dsa", "computer-science", "career"],
        "category": "learning",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "system-design-primer",
        "full_name": "donnemartin/system-design-primer",
        "description": "Learn how to design large-scale systems for tech interviews",
        "owner_name": "donnemartin",
        "html_url": "https://github.com/donnemartin/system-design-primer",
        "stars": 260000,
        "language": "Python",
        "topics": ["system-design", "interview", "architecture", "scalability"],
        "category": "learning",
        "skill_level": "advanced",
        "is_featured": True
    },
    {
        "name": "tech-interview-handbook",
        "full_name": "yangshun/tech-interview-handbook",
        "description": "Curated coding interview preparation materials for busy software engineers",
        "owner_name": "yangshun",
        "html_url": "https://github.com/yangshun/tech-interview-handbook",
        "homepage": "https://techinterviewhandbook.org",
        "stars": 110000,
        "language": "TypeScript",
        "topics": ["interview", "preparation", "career"],
        "category": "learning",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "project-based-learning",
        "full_name": "practical-tutorials/project-based-learning",
        "description": "Curated list of project-based tutorials",
        "owner_name": "practical-tutorials",
        "html_url": "https://github.com/practical-tutorials/project-based-learning",
        "stars": 160000,
        "language": None,
        "topics": ["projects", "learning", "tutorials"],
        "category": "learning",
        "skill_level": "beginner",
        "is_featured": True
    },
    {
        "name": "build-your-own-x",
        "full_name": "codecrafters-io/build-your-own-x",
        "description": "Master programming by recreating your favorite technologies from scratch",
        "owner_name": "codecrafters-io",
        "html_url": "https://github.com/codecrafters-io/build-your-own-x",
        "stars": 280000,
        "language": None,
        "topics": ["learning", "projects", "diy"],
        "category": "learning",
        "skill_level": "intermediate",
        "is_featured": True
    },
    
    # ==================== JAVASCRIPT/TYPESCRIPT ====================
    {
        "name": "react",
        "full_name": "facebook/react",
        "description": "The library for web and native user interfaces",
        "owner_name": "facebook",
        "html_url": "https://github.com/facebook/react",
        "homepage": "https://react.dev",
        "stars": 220000,
        "language": "JavaScript",
        "topics": ["react", "frontend", "ui", "javascript"],
        "category": "frameworks",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "next.js",
        "full_name": "vercel/next.js",
        "description": "The React Framework for the Web",
        "owner_name": "vercel",
        "html_url": "https://github.com/vercel/next.js",
        "homepage": "https://nextjs.org",
        "stars": 120000,
        "language": "JavaScript",
        "topics": ["nextjs", "react", "ssr", "framework"],
        "category": "frameworks",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "vue",
        "full_name": "vuejs/vue",
        "description": "Vue.js is a progressive JavaScript framework for building user interfaces",
        "owner_name": "vuejs",
        "html_url": "https://github.com/vuejs/vue",
        "homepage": "https://vuejs.org",
        "stars": 207000,
        "language": "TypeScript",
        "topics": ["vue", "frontend", "framework"],
        "category": "frameworks",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "node",
        "full_name": "nodejs/node",
        "description": "Node.js JavaScript runtime",
        "owner_name": "nodejs",
        "html_url": "https://github.com/nodejs/node",
        "homepage": "https://nodejs.org",
        "stars": 105000,
        "language": "JavaScript",
        "topics": ["nodejs", "javascript", "runtime", "backend"],
        "category": "runtime",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "javascript-algorithms",
        "full_name": "trekhleb/javascript-algorithms",
        "description": "Algorithms and data structures implemented in JavaScript",
        "owner_name": "trekhleb",
        "html_url": "https://github.com/trekhleb/javascript-algorithms",
        "stars": 185000,
        "language": "JavaScript",
        "topics": ["algorithms", "data-structures", "javascript"],
        "category": "learning",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "30-seconds-of-code",
        "full_name": "Chalarangelo/30-seconds-of-code",
        "description": "Short code snippets for all your development needs",
        "owner_name": "Chalarangelo",
        "html_url": "https://github.com/Chalarangelo/30-seconds-of-code",
        "homepage": "https://30secondsofcode.org",
        "stars": 120000,
        "language": "JavaScript",
        "topics": ["snippets", "javascript", "reference"],
        "category": "learning",
        "skill_level": "beginner",
        "is_featured": False
    },
    
    # ==================== PYTHON ====================
    {
        "name": "Python",
        "full_name": "TheAlgorithms/Python",
        "description": "All Algorithms implemented in Python",
        "owner_name": "TheAlgorithms",
        "html_url": "https://github.com/TheAlgorithms/Python",
        "stars": 180000,
        "language": "Python",
        "topics": ["algorithms", "data-structures", "python"],
        "category": "learning",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "fastapi",
        "full_name": "tiangolo/fastapi",
        "description": "FastAPI framework, high performance, easy to learn, fast to code, ready for production",
        "owner_name": "tiangolo",
        "html_url": "https://github.com/tiangolo/fastapi",
        "homepage": "https://fastapi.tiangolo.com",
        "stars": 72000,
        "language": "Python",
        "topics": ["fastapi", "api", "python", "backend"],
        "category": "frameworks",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "django",
        "full_name": "django/django",
        "description": "The Web framework for perfectionists with deadlines",
        "owner_name": "django",
        "html_url": "https://github.com/django/django",
        "homepage": "https://www.djangoproject.com/",
        "stars": 77000,
        "language": "Python",
        "topics": ["django", "python", "web-framework", "backend"],
        "category": "frameworks",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "flask",
        "full_name": "pallets/flask",
        "description": "The Python micro framework for building web applications",
        "owner_name": "pallets",
        "html_url": "https://github.com/pallets/flask",
        "homepage": "https://flask.palletsprojects.com",
        "stars": 66000,
        "language": "Python",
        "topics": ["flask", "python", "microframework", "backend"],
        "category": "frameworks",
        "skill_level": "beginner",
        "is_featured": False
    },
    
    # ==================== AI/ML ====================
    {
        "name": "transformers",
        "full_name": "huggingface/transformers",
        "description": "State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX",
        "owner_name": "huggingface",
        "html_url": "https://github.com/huggingface/transformers",
        "homepage": "https://huggingface.co/transformers",
        "stars": 125000,
        "language": "Python",
        "topics": ["machine-learning", "nlp", "transformers", "pytorch"],
        "category": "ai-ml",
        "skill_level": "advanced",
        "is_featured": True
    },
    {
        "name": "langchain",
        "full_name": "langchain-ai/langchain",
        "description": "Build context-aware reasoning applications",
        "owner_name": "langchain-ai",
        "html_url": "https://github.com/langchain-ai/langchain",
        "homepage": "https://python.langchain.com",
        "stars": 85000,
        "language": "Python",
        "topics": ["llm", "ai", "langchain", "rag"],
        "category": "ai-ml",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "stable-diffusion-webui",
        "full_name": "AUTOMATIC1111/stable-diffusion-webui",
        "description": "Stable Diffusion web UI",
        "owner_name": "AUTOMATIC1111",
        "html_url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
        "stars": 130000,
        "language": "Python",
        "topics": ["stable-diffusion", "ai", "image-generation"],
        "category": "ai-ml",
        "skill_level": "intermediate",
        "is_featured": True
    },
    {
        "name": "llama",
        "full_name": "meta-llama/llama",
        "description": "Inference code for Llama models",
        "owner_name": "meta-llama",
        "html_url": "https://github.com/meta-llama/llama",
        "stars": 55000,
        "language": "Python",
        "topics": ["llm", "ai", "meta", "open-source"],
        "category": "ai-ml",
        "skill_level": "advanced",
        "is_featured": True
    },
    {
        "name": "ollama",
        "full_name": "ollama/ollama",
        "description": "Get up and running with Llama 3, Mistral, and other large language models",
        "owner_name": "ollama",
        "html_url": "https://github.com/ollama/ollama",
        "homepage": "https://ollama.ai",
        "stars": 70000,
        "language": "Go",
        "topics": ["llm", "local", "ai"],
        "category": "ai-ml",
        "skill_level": "beginner",
        "is_featured": True
    },
    
    # ==================== DEVOPS & TOOLS ====================
    {
        "name": "kubernetes",
        "full_name": "kubernetes/kubernetes",
        "description": "Production-Grade Container Scheduling and Management",
        "owner_name": "kubernetes",
        "html_url": "https://github.com/kubernetes/kubernetes",
        "homepage": "https://kubernetes.io",
        "stars": 108000,
        "language": "Go",
        "topics": ["kubernetes", "containers", "devops", "cloud"],
        "category": "devops",
        "skill_level": "advanced",
        "is_featured": True
    },
    {
        "name": "docker-compose",
        "full_name": "docker/compose",
        "description": "Define and run multi-container applications with Docker",
        "owner_name": "docker",
        "html_url": "https://github.com/docker/compose",
        "homepage": "https://docs.docker.com/compose/",
        "stars": 33000,
        "language": "Go",
        "topics": ["docker", "containers", "devops"],
        "category": "devops",
        "skill_level": "intermediate",
        "is_featured": False
    },
    {
        "name": "terraform",
        "full_name": "hashicorp/terraform",
        "description": "Terraform enables you to safely and predictably create, change, and improve infrastructure",
        "owner_name": "hashicorp",
        "html_url": "https://github.com/hashicorp/terraform",
        "homepage": "https://www.terraform.io/",
        "stars": 41000,
        "language": "Go",
        "topics": ["terraform", "infrastructure", "iac", "devops"],
        "category": "devops",
        "skill_level": "intermediate",
        "is_featured": True
    },
    
    # ==================== AWESOME LISTS ====================
    {
        "name": "awesome",
        "full_name": "sindresorhus/awesome",
        "description": "Awesome lists about all kinds of interesting topics",
        "owner_name": "sindresorhus",
        "html_url": "https://github.com/sindresorhus/awesome",
        "stars": 310000,
        "language": None,
        "topics": ["awesome", "lists", "resources"],
        "category": "learning",
        "skill_level": "beginner",
        "is_featured": True
    },
    {
        "name": "awesome-python",
        "full_name": "vinta/awesome-python",
        "description": "A curated list of awesome Python frameworks, libraries and software",
        "owner_name": "vinta",
        "html_url": "https://github.com/vinta/awesome-python",
        "homepage": "https://awesome-python.com/",
        "stars": 210000,
        "language": "Python",
        "topics": ["python", "awesome", "resources"],
        "category": "learning",
        "skill_level": "beginner",
        "is_featured": False
    },
    {
        "name": "awesome-react",
        "full_name": "enaqx/awesome-react",
        "description": "A collection of awesome things regarding React ecosystem",
        "owner_name": "enaqx",
        "html_url": "https://github.com/enaqx/awesome-react",
        "stars": 63000,
        "language": None,
        "topics": ["react", "awesome", "resources"],
        "category": "learning",
        "skill_level": "beginner",
        "is_featured": False
    },
    
    # ==================== TOOLS & UTILITIES ====================
    {
        "name": "vscode",
        "full_name": "microsoft/vscode",
        "description": "Visual Studio Code - Open Source",
        "owner_name": "microsoft",
        "html_url": "https://github.com/microsoft/vscode",
        "homepage": "https://code.visualstudio.com",
        "stars": 160000,
        "language": "TypeScript",
        "topics": ["vscode", "editor", "ide", "development"],
        "category": "tools",
        "skill_level": "beginner",
        "is_featured": True
    },
    {
        "name": "ohmyzsh",
        "full_name": "ohmyzsh/ohmyzsh",
        "description": "A delightful community-driven framework for managing your zsh configuration",
        "owner_name": "ohmyzsh",
        "html_url": "https://github.com/ohmyzsh/ohmyzsh",
        "homepage": "https://ohmyz.sh/",
        "stars": 170000,
        "language": "Shell",
        "topics": ["terminal", "shell", "zsh", "productivity"],
        "category": "tools",
        "skill_level": "beginner",
        "is_featured": False
    },
    {
        "name": "public-apis",
        "full_name": "public-apis/public-apis",
        "description": "A collective list of free APIs for use in software and web development",
        "owner_name": "public-apis",
        "html_url": "https://github.com/public-apis/public-apis",
        "stars": 300000,
        "language": "Python",
        "topics": ["api", "resources", "development"],
        "category": "learning",
        "skill_level": "beginner",
        "is_featured": True
    }
]


def seed_git_repos():
    """Seed Git repositories data"""
    db = next(get_db())
    
    try:
        count = 0
        for repo_data in GIT_REPOSITORIES:
            existing = db.query(GitRepository).filter(
                GitRepository.full_name == repo_data["full_name"]
            ).first()
            
            if existing:
                print(f"Repo exists: {repo_data['full_name']}")
                continue
            
            repo = GitRepository(
                name=repo_data["name"],
                full_name=repo_data["full_name"],
                description=repo_data.get("description"),
                owner_name=repo_data.get("owner_name"),
                html_url=repo_data["html_url"],
                homepage=repo_data.get("homepage"),
                stars=repo_data.get("stars", 0),
                language=repo_data.get("language"),
                topics=repo_data.get("topics"),
                category=repo_data.get("category"),
                skill_level=repo_data.get("skill_level"),
                is_featured=repo_data.get("is_featured", False)
            )
            db.add(repo)
            count += 1
            print(f"Created repo: {repo_data['full_name']}")
        
        db.commit()
        print(f"✅ {count} Git repositories seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding Git repos: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_git_repos()
