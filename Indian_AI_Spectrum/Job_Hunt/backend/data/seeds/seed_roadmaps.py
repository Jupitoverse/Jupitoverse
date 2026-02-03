"""
Seed Career Roadmaps Data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models import get_db, CareerRoadmap
import json

ROADMAPS = [
    {
        "title": "Frontend Developer",
        "slug": "frontend-developer",
        "description": "Complete roadmap to become a modern frontend developer. Learn HTML, CSS, JavaScript, React/Vue, and more.",
        "short_description": "Master modern frontend development from basics to advanced",
        "role": "Frontend Developer",
        "experience_level": "beginner",
        "icon": "fas fa-laptop-code",
        "color": "#3b82f6",
        "duration_weeks": 24,
        "overview": "Frontend development is one of the most in-demand skills. This roadmap will take you from zero to job-ready.",
        "prerequisites": ["Basic computer knowledge", "Willingness to learn"],
        "steps": [
            {
                "id": 1, "title": "HTML Fundamentals", "duration": "2 weeks",
                "topics": ["HTML5 basics", "Semantic HTML", "Forms", "Accessibility"],
                "resources": ["MDN Web Docs", "freeCodeCamp HTML course"]
            },
            {
                "id": 2, "title": "CSS Mastery", "duration": "3 weeks",
                "topics": ["CSS basics", "Flexbox", "Grid", "Responsive design", "CSS animations"],
                "resources": ["CSS-Tricks", "Kevin Powell YouTube"]
            },
            {
                "id": 3, "title": "JavaScript Fundamentals", "duration": "4 weeks",
                "topics": ["Variables", "Functions", "DOM manipulation", "Events", "ES6+", "Async JS"],
                "resources": ["JavaScript.info", "Eloquent JavaScript"]
            },
            {
                "id": 4, "title": "React.js", "duration": "4 weeks",
                "topics": ["Components", "State", "Props", "Hooks", "React Router", "Context API"],
                "resources": ["React docs", "Scrimba React course"]
            },
            {
                "id": 5, "title": "State Management", "duration": "2 weeks",
                "topics": ["Redux", "Zustand", "React Query"],
                "resources": ["Redux docs", "Academind"]
            },
            {
                "id": 6, "title": "Build Tools & Deployment", "duration": "2 weeks",
                "topics": ["Webpack/Vite", "npm/yarn", "CI/CD", "Vercel/Netlify"],
                "resources": ["Vite docs", "Vercel tutorials"]
            },
            {
                "id": 7, "title": "Testing", "duration": "2 weeks",
                "topics": ["Jest", "React Testing Library", "E2E with Cypress"],
                "resources": ["Testing Library docs", "Kent C. Dodds blog"]
            },
            {
                "id": 8, "title": "Projects & Portfolio", "duration": "5 weeks",
                "topics": ["Build 3+ projects", "Portfolio website", "GitHub profile"],
                "resources": ["Frontend Mentor", "Real-world projects"]
            }
        ],
        "is_featured": True,
        "display_order": 1
    },
    {
        "title": "Backend Developer",
        "slug": "backend-developer",
        "description": "Learn server-side development with Node.js, Python, databases, and APIs.",
        "short_description": "Build robust server-side applications and APIs",
        "role": "Backend Developer",
        "experience_level": "beginner",
        "icon": "fas fa-server",
        "color": "#10b981",
        "duration_weeks": 26,
        "overview": "Backend development powers the web. Learn to build APIs, work with databases, and deploy applications.",
        "prerequisites": ["Basic programming knowledge", "Understanding of HTTP"],
        "steps": [
            {
                "id": 1, "title": "Programming Fundamentals", "duration": "3 weeks",
                "topics": ["Python/Node.js basics", "Data structures", "Algorithms"],
                "resources": ["Python docs", "Node.js docs"]
            },
            {
                "id": 2, "title": "Databases", "duration": "4 weeks",
                "topics": ["SQL basics", "PostgreSQL", "MongoDB", "Redis"],
                "resources": ["PostgreSQL tutorial", "MongoDB University"]
            },
            {
                "id": 3, "title": "API Development", "duration": "4 weeks",
                "topics": ["REST API design", "FastAPI/Express", "Authentication", "GraphQL basics"],
                "resources": ["FastAPI docs", "Express docs"]
            },
            {
                "id": 4, "title": "Authentication & Security", "duration": "2 weeks",
                "topics": ["JWT", "OAuth", "Security best practices", "OWASP"],
                "resources": ["OWASP guidelines", "Auth0 tutorials"]
            },
            {
                "id": 5, "title": "DevOps Basics", "duration": "3 weeks",
                "topics": ["Docker", "CI/CD", "AWS/GCP basics", "Nginx"],
                "resources": ["Docker docs", "AWS tutorials"]
            },
            {
                "id": 6, "title": "Testing & Best Practices", "duration": "2 weeks",
                "topics": ["Unit testing", "Integration testing", "TDD"],
                "resources": ["pytest docs", "Jest docs"]
            },
            {
                "id": 7, "title": "Projects", "duration": "8 weeks",
                "topics": ["Build REST API", "Real-time app", "Microservices"],
                "resources": ["Build real projects"]
            }
        ],
        "is_featured": True,
        "display_order": 2
    },
    {
        "title": "Full Stack Developer",
        "slug": "fullstack-developer",
        "description": "Become a complete full-stack developer with frontend, backend, and DevOps skills.",
        "short_description": "Master both frontend and backend development",
        "role": "Full Stack Developer",
        "experience_level": "intermediate",
        "icon": "fas fa-layer-group",
        "color": "#8b5cf6",
        "duration_weeks": 36,
        "overview": "Full-stack developers are highly valued. This roadmap combines frontend and backend skills.",
        "prerequisites": ["Basic HTML/CSS", "Some programming experience"],
        "steps": [
            {"id": 1, "title": "Frontend Fundamentals", "duration": "6 weeks", "topics": ["HTML/CSS", "JavaScript", "React"]},
            {"id": 2, "title": "Backend Fundamentals", "duration": "6 weeks", "topics": ["Node.js/Python", "APIs", "Databases"]},
            {"id": 3, "title": "Full Stack Integration", "duration": "4 weeks", "topics": ["Connect frontend to backend", "Authentication flow"]},
            {"id": 4, "title": "DevOps & Deployment", "duration": "4 weeks", "topics": ["Docker", "CI/CD", "Cloud deployment"]},
            {"id": 5, "title": "Advanced Topics", "duration": "6 weeks", "topics": ["Microservices", "GraphQL", "Performance"]},
            {"id": 6, "title": "Portfolio Projects", "duration": "10 weeks", "topics": ["Build 3 full-stack projects"]}
        ],
        "is_featured": True,
        "display_order": 3
    },
    {
        "title": "Data Scientist",
        "slug": "data-scientist",
        "description": "Learn data science with Python, statistics, machine learning, and deep learning.",
        "short_description": "Analyze data and build ML models",
        "role": "Data Scientist",
        "experience_level": "intermediate",
        "icon": "fas fa-chart-bar",
        "color": "#f59e0b",
        "duration_weeks": 32,
        "overview": "Data science combines statistics, programming, and domain expertise to extract insights from data.",
        "prerequisites": ["Basic Python", "High school math"],
        "steps": [
            {"id": 1, "title": "Python for Data Science", "duration": "3 weeks", "topics": ["NumPy", "Pandas", "Matplotlib"]},
            {"id": 2, "title": "Statistics & Probability", "duration": "4 weeks", "topics": ["Descriptive stats", "Probability", "Hypothesis testing"]},
            {"id": 3, "title": "Machine Learning", "duration": "8 weeks", "topics": ["Scikit-learn", "Supervised learning", "Unsupervised learning"]},
            {"id": 4, "title": "Deep Learning", "duration": "6 weeks", "topics": ["TensorFlow/PyTorch", "Neural networks", "CNNs", "RNNs"]},
            {"id": 5, "title": "Data Engineering", "duration": "4 weeks", "topics": ["SQL", "ETL", "Data pipelines"]},
            {"id": 6, "title": "Projects & Kaggle", "duration": "7 weeks", "topics": ["Kaggle competitions", "End-to-end projects"]}
        ],
        "is_featured": True,
        "display_order": 4
    },
    {
        "title": "DevOps Engineer",
        "slug": "devops-engineer",
        "description": "Master CI/CD, containers, Kubernetes, cloud platforms, and infrastructure as code.",
        "short_description": "Automate and streamline software delivery",
        "role": "DevOps Engineer",
        "experience_level": "intermediate",
        "icon": "fas fa-cogs",
        "color": "#ec4899",
        "duration_weeks": 28,
        "overview": "DevOps bridges development and operations. Learn to automate, monitor, and scale infrastructure.",
        "prerequisites": ["Linux basics", "Basic scripting", "Networking fundamentals"],
        "steps": [
            {"id": 1, "title": "Linux & Scripting", "duration": "3 weeks", "topics": ["Linux commands", "Bash scripting", "Python automation"]},
            {"id": 2, "title": "Docker & Containers", "duration": "4 weeks", "topics": ["Docker basics", "Docker Compose", "Container best practices"]},
            {"id": 3, "title": "Kubernetes", "duration": "5 weeks", "topics": ["K8s architecture", "Deployments", "Services", "Helm"]},
            {"id": 4, "title": "CI/CD", "duration": "3 weeks", "topics": ["GitHub Actions", "Jenkins", "ArgoCD"]},
            {"id": 5, "title": "Cloud Platforms", "duration": "6 weeks", "topics": ["AWS", "GCP", "Terraform"]},
            {"id": 6, "title": "Monitoring & Security", "duration": "4 weeks", "topics": ["Prometheus", "Grafana", "Security scanning"]},
            {"id": 7, "title": "Projects", "duration": "3 weeks", "topics": ["Build complete CI/CD pipeline"]}
        ],
        "is_featured": True,
        "display_order": 5
    },
    {
        "title": "Machine Learning Engineer",
        "slug": "ml-engineer",
        "description": "Go beyond data science to productionize ML models at scale.",
        "short_description": "Deploy and scale ML models in production",
        "role": "ML Engineer",
        "experience_level": "advanced",
        "icon": "fas fa-brain",
        "color": "#6366f1",
        "duration_weeks": 30,
        "overview": "ML Engineers bridge the gap between data science and production systems.",
        "prerequisites": ["Python proficiency", "ML fundamentals", "Basic DevOps"],
        "steps": [
            {"id": 1, "title": "Advanced ML", "duration": "4 weeks", "topics": ["Feature engineering", "Model optimization", "Experiment tracking"]},
            {"id": 2, "title": "MLOps", "duration": "6 weeks", "topics": ["MLflow", "Kubeflow", "Model versioning"]},
            {"id": 3, "title": "Model Deployment", "duration": "4 weeks", "topics": ["FastAPI", "TensorFlow Serving", "Triton"]},
            {"id": 4, "title": "Scaling & Monitoring", "duration": "4 weeks", "topics": ["Model monitoring", "A/B testing", "Feature stores"]},
            {"id": 5, "title": "LLMs & Generative AI", "duration": "6 weeks", "topics": ["Transformers", "LangChain", "Fine-tuning"]},
            {"id": 6, "title": "Projects", "duration": "6 weeks", "topics": ["End-to-end ML system"]}
        ],
        "is_featured": True,
        "display_order": 6
    },
    {
        "title": "System Design",
        "slug": "system-design",
        "description": "Learn to design scalable, distributed systems for technical interviews and real-world applications.",
        "short_description": "Design scalable distributed systems",
        "role": "Senior Software Engineer",
        "experience_level": "advanced",
        "icon": "fas fa-project-diagram",
        "color": "#14b8a6",
        "duration_weeks": 12,
        "overview": "System design is essential for senior engineering roles and building large-scale systems.",
        "prerequisites": ["3+ years development experience", "Backend knowledge"],
        "steps": [
            {"id": 1, "title": "Fundamentals", "duration": "2 weeks", "topics": ["Scalability", "Load balancing", "Caching", "CAP theorem"]},
            {"id": 2, "title": "Databases", "duration": "2 weeks", "topics": ["SQL vs NoSQL", "Sharding", "Replication", "Indexing"]},
            {"id": 3, "title": "Distributed Systems", "duration": "3 weeks", "topics": ["Consistency", "Consensus", "Message queues"]},
            {"id": 4, "title": "Design Patterns", "duration": "2 weeks", "topics": ["Microservices", "Event-driven", "CQRS"]},
            {"id": 5, "title": "Case Studies", "duration": "3 weeks", "topics": ["Design URL shortener", "Design Twitter", "Design Netflix"]}
        ],
        "is_featured": False,
        "display_order": 7
    },
    {
        "title": "DSA for Interviews",
        "slug": "dsa-interviews",
        "description": "Master data structures and algorithms for coding interviews at top tech companies.",
        "short_description": "Crack coding interviews at FAANG+",
        "role": "Software Engineer",
        "experience_level": "intermediate",
        "icon": "fas fa-code",
        "color": "#ef4444",
        "duration_weeks": 16,
        "overview": "A structured approach to mastering DSA for technical interviews.",
        "prerequisites": ["Basic programming", "One language proficiency"],
        "steps": [
            {"id": 1, "title": "Arrays & Strings", "duration": "2 weeks", "topics": ["Two pointers", "Sliding window", "Prefix sum"]},
            {"id": 2, "title": "Linked Lists", "duration": "1 week", "topics": ["Reversal", "Fast/slow pointers", "Merge"]},
            {"id": 3, "title": "Trees & Graphs", "duration": "4 weeks", "topics": ["BFS", "DFS", "Binary trees", "BST"]},
            {"id": 4, "title": "Dynamic Programming", "duration": "4 weeks", "topics": ["1D DP", "2D DP", "State machine DP"]},
            {"id": 5, "title": "Advanced Topics", "duration": "3 weeks", "topics": ["Heap", "Trie", "Union Find", "Segment tree"]},
            {"id": 6, "title": "Mock Interviews", "duration": "2 weeks", "topics": ["Practice interviews", "Time management"]}
        ],
        "is_featured": True,
        "display_order": 8
    }
]


def seed_roadmaps():
    """Seed career roadmaps"""
    db = next(get_db())
    
    try:
        for roadmap_data in ROADMAPS:
            existing = db.query(CareerRoadmap).filter(
                CareerRoadmap.slug == roadmap_data["slug"]
            ).first()
            
            if existing:
                print(f"Roadmap exists: {roadmap_data['title']}")
                continue
            
            roadmap = CareerRoadmap(
                title=roadmap_data["title"],
                slug=roadmap_data["slug"],
                description=roadmap_data["description"],
                short_description=roadmap_data.get("short_description"),
                role=roadmap_data.get("role"),
                experience_level=roadmap_data.get("experience_level"),
                icon=roadmap_data.get("icon"),
                color=roadmap_data.get("color"),
                duration_weeks=roadmap_data.get("duration_weeks"),
                overview=roadmap_data.get("overview"),
                prerequisites=roadmap_data.get("prerequisites"),
                steps=roadmap_data.get("steps"),
                is_featured=roadmap_data.get("is_featured", False),
                display_order=roadmap_data.get("display_order", 0)
            )
            db.add(roadmap)
            print(f"Created roadmap: {roadmap_data['title']}")
        
        db.commit()
        print("✅ Career roadmaps seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding roadmaps: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_roadmaps()
