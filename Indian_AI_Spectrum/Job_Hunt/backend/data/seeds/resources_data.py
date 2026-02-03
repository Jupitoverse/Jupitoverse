"""
Learning Resources and Roadmaps Data
Comprehensive collection of courses, YouTube channels, books, and roadmaps
"""
import sys
import os
import json
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import SessionLocal, init_db
from app.models.resource import Resource, Roadmap, RoadmapStep, ResourceType, ResourcePricing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RESOURCES = [
    # DSA & Interview Prep
    {"title": "LeetCode", "resource_type": ResourceType.WEBSITE, "platform": "LeetCode", "url": "https://leetcode.com", "description": "Best platform for coding interview preparation. 2500+ problems.", "pricing": ResourcePricing.FREE, "difficulty_level": "all", "skills_covered": json.dumps(["DSA", "Interview", "Coding"])},
    {"title": "NeetCode.io", "resource_type": ResourceType.WEBSITE, "platform": "NeetCode", "url": "https://neetcode.io", "description": "Curated 150 LeetCode problems with video explanations.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["DSA", "Interview", "FAANG"])},
    {"title": "AlgoExpert", "resource_type": ResourceType.COURSE, "platform": "AlgoExpert", "url": "https://algoexpert.io", "description": "Curated 200+ interview questions with video solutions.", "pricing": ResourcePricing.PAID, "difficulty_level": "intermediate", "skills_covered": json.dumps(["DSA", "Interview"])},
    {"title": "Striver's A2Z DSA Sheet", "resource_type": ResourceType.COURSE, "platform": "TakeUForward", "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2", "description": "Complete DSA course with 450+ problems. Very popular in India.", "pricing": ResourcePricing.FREE, "difficulty_level": "all", "skills_covered": json.dumps(["DSA", "Interview", "Indian"]), "is_indian_creator": True, "is_india_focused": True},
    {"title": "Cracking the Coding Interview", "resource_type": ResourceType.BOOK, "platform": "Amazon", "url": "https://www.crackingthecodinginterview.com", "description": "The bible of coding interviews. 189 questions and solutions.", "pricing": ResourcePricing.PAID, "difficulty_level": "intermediate", "skills_covered": json.dumps(["DSA", "Interview", "Book"])},
    
    # System Design
    {"title": "System Design Primer", "resource_type": ResourceType.GITHUB_REPO, "platform": "GitHub", "url": "https://github.com/donnemartin/system-design-primer", "description": "Comprehensive system design resource. 200k+ stars on GitHub.", "pricing": ResourcePricing.FREE, "difficulty_level": "advanced", "skills_covered": json.dumps(["System Design", "Architecture"])},
    {"title": "Gaurav Sen - System Design", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@gaborvision", "description": "Popular YouTube channel for system design concepts.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["System Design", "YouTube", "Indian"]), "is_indian_creator": True},
    {"title": "ByteByteGo", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@ByteByteGo", "description": "System design concepts with amazing visualizations.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["System Design", "Architecture"])},
    {"title": "Designing Data-Intensive Applications", "resource_type": ResourceType.BOOK, "platform": "O'Reilly", "url": "https://dataintensive.net", "description": "The DDIA book. Must-read for distributed systems.", "pricing": ResourcePricing.PAID, "difficulty_level": "advanced", "skills_covered": json.dumps(["System Design", "Distributed Systems"])},
    {"title": "Grokking System Design Interview", "resource_type": ResourceType.COURSE, "platform": "Educative", "url": "https://educative.io/courses/grokking-the-system-design-interview", "description": "Popular interactive course for system design interviews.", "pricing": ResourcePricing.PAID, "difficulty_level": "intermediate", "skills_covered": json.dumps(["System Design", "Interview"])},
    
    # Web Development
    {"title": "freeCodeCamp", "resource_type": ResourceType.WEBSITE, "platform": "freeCodeCamp", "url": "https://freecodecamp.org", "description": "Free coding bootcamp. Full-stack web development curriculum.", "pricing": ResourcePricing.FREE, "difficulty_level": "beginner", "skills_covered": json.dumps(["Web Dev", "JavaScript", "React"])},
    {"title": "The Odin Project", "resource_type": ResourceType.WEBSITE, "platform": "Odin Project", "url": "https://theodinproject.com", "description": "Full-stack curriculum. Project-based learning.", "pricing": ResourcePricing.FREE, "difficulty_level": "beginner", "skills_covered": json.dumps(["Web Dev", "Full Stack"])},
    {"title": "MDN Web Docs", "resource_type": ResourceType.DOCUMENTATION, "platform": "Mozilla", "url": "https://developer.mozilla.org", "description": "Official web documentation. Best reference for HTML, CSS, JS.", "pricing": ResourcePricing.FREE, "difficulty_level": "all", "skills_covered": json.dumps(["Web Dev", "Reference"])},
    {"title": "JavaScript.info", "resource_type": ResourceType.WEBSITE, "platform": "JavaScript.info", "url": "https://javascript.info", "description": "Modern JavaScript tutorial. From basics to advanced.", "pricing": ResourcePricing.FREE, "difficulty_level": "all", "skills_covered": json.dumps(["JavaScript", "Web Dev"])},
    {"title": "React Official Docs", "resource_type": ResourceType.DOCUMENTATION, "platform": "React", "url": "https://react.dev", "description": "Official React documentation with interactive examples.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["React", "Frontend"])},
    {"title": "Fireship", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@Fireship", "description": "Quick, entertaining web dev tutorials and tech news.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Web Dev", "YouTube"])},
    {"title": "Traversy Media", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@TraversyMedia", "description": "Practical web development tutorials.", "pricing": ResourcePricing.FREE, "difficulty_level": "beginner", "skills_covered": json.dumps(["Web Dev", "YouTube"])},
    
    # Python & Backend
    {"title": "Python Official Tutorial", "resource_type": ResourceType.DOCUMENTATION, "platform": "Python.org", "url": "https://docs.python.org/3/tutorial", "description": "Official Python tutorial for beginners.", "pricing": ResourcePricing.FREE, "difficulty_level": "beginner", "skills_covered": json.dumps(["Python", "Backend"])},
    {"title": "Real Python", "resource_type": ResourceType.WEBSITE, "platform": "Real Python", "url": "https://realpython.com", "description": "Python tutorials for all levels.", "pricing": ResourcePricing.FREEMIUM, "difficulty_level": "all", "skills_covered": json.dumps(["Python", "Backend"])},
    {"title": "Corey Schafer Python", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@coreyms", "description": "Excellent Python tutorials on YouTube.", "pricing": ResourcePricing.FREE, "difficulty_level": "beginner", "skills_covered": json.dumps(["Python", "YouTube"])},
    {"title": "FastAPI Documentation", "resource_type": ResourceType.DOCUMENTATION, "platform": "FastAPI", "url": "https://fastapi.tiangolo.com", "description": "Official FastAPI docs. Learn modern Python APIs.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Python", "FastAPI", "Backend"])},
    {"title": "Django Documentation", "resource_type": ResourceType.DOCUMENTATION, "platform": "Django", "url": "https://docs.djangoproject.com", "description": "Official Django framework documentation.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Python", "Django", "Backend"])},
    
    # Data Science & ML
    {"title": "Andrew Ng Machine Learning", "resource_type": ResourceType.COURSE, "platform": "Coursera", "url": "https://coursera.org/specializations/machine-learning-introduction", "description": "The classic ML course by Andrew Ng. Stanford quality.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Machine Learning", "AI"])},
    {"title": "Fast.ai", "resource_type": ResourceType.COURSE, "platform": "Fast.ai", "url": "https://fast.ai", "description": "Practical deep learning for coders. Top-down approach.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Deep Learning", "AI"])},
    {"title": "Kaggle Learn", "resource_type": ResourceType.WEBSITE, "platform": "Kaggle", "url": "https://kaggle.com/learn", "description": "Free micro-courses on data science and ML.", "pricing": ResourcePricing.FREE, "difficulty_level": "beginner", "skills_covered": json.dumps(["Data Science", "ML"])},
    {"title": "StatQuest", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@statquest", "description": "Statistics and ML concepts explained simply.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Statistics", "ML", "YouTube"])},
    {"title": "3Blue1Brown", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@3blue1brown", "description": "Beautiful math visualizations for deep learning concepts.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Math", "Deep Learning", "YouTube"])},
    {"title": "Hands-On Machine Learning", "resource_type": ResourceType.BOOK, "platform": "O'Reilly", "url": "https://oreilly.com/library/view/hands-on-machine-learning/9781492032632", "description": "Practical ML with Scikit-Learn, Keras, TensorFlow.", "pricing": ResourcePricing.PAID, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Machine Learning", "Python"])},
    
    # DevOps & Cloud
    {"title": "AWS Training", "resource_type": ResourceType.WEBSITE, "platform": "AWS", "url": "https://aws.amazon.com/training", "description": "Official AWS training and certification paths.", "pricing": ResourcePricing.FREE, "difficulty_level": "all", "skills_covered": json.dumps(["AWS", "Cloud"])},
    {"title": "Google Cloud Skills Boost", "resource_type": ResourceType.WEBSITE, "platform": "Google Cloud", "url": "https://cloudskillsboost.google", "description": "GCP training with hands-on labs.", "pricing": ResourcePricing.FREE, "difficulty_level": "all", "skills_covered": json.dumps(["GCP", "Cloud"])},
    {"title": "Docker Official Docs", "resource_type": ResourceType.DOCUMENTATION, "platform": "Docker", "url": "https://docs.docker.com/get-started", "description": "Learn Docker containerization.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Docker", "DevOps"])},
    {"title": "Kubernetes Documentation", "resource_type": ResourceType.DOCUMENTATION, "platform": "Kubernetes", "url": "https://kubernetes.io/docs/tutorials", "description": "Official Kubernetes tutorials.", "pricing": ResourcePricing.FREE, "difficulty_level": "advanced", "skills_covered": json.dumps(["Kubernetes", "DevOps"])},
    {"title": "TechWorld with Nana", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@TechWorldwithNana", "description": "DevOps tutorials - Docker, Kubernetes, CI/CD.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["DevOps", "YouTube"])},
    {"title": "KodeKloud", "resource_type": ResourceType.COURSE, "platform": "KodeKloud", "url": "https://kodekloud.com", "description": "DevOps courses with hands-on labs. Very practical.", "pricing": ResourcePricing.PAID, "difficulty_level": "intermediate", "skills_covered": json.dumps(["DevOps", "Kubernetes", "Terraform"])},
    
    # Indian YouTube Channels
    {"title": "Striver (TakeUForward)", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@takeUforward", "description": "Best DSA content for Indian placements. Very detailed.", "pricing": ResourcePricing.FREE, "difficulty_level": "all", "skills_covered": json.dumps(["DSA", "Indian", "YouTube"]), "is_indian_creator": True, "is_india_focused": True},
    {"title": "Love Babbar", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@LoveBabbar", "description": "DSA and placement preparation. Hindi content.", "pricing": ResourcePricing.FREE, "difficulty_level": "all", "skills_covered": json.dumps(["DSA", "Indian", "YouTube", "Hindi"]), "is_indian_creator": True, "is_india_focused": True, "language": "Hindi"},
    {"title": "Apna College", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@ApnaCollegeOfficial", "description": "Complete programming courses in Hindi.", "pricing": ResourcePricing.FREE, "difficulty_level": "beginner", "skills_covered": json.dumps(["Programming", "Indian", "YouTube", "Hindi"]), "is_indian_creator": True, "is_india_focused": True, "language": "Hindi"},
    {"title": "Code with Harry", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@CodeWithHarry", "description": "Programming tutorials in Hindi/English.", "pricing": ResourcePricing.FREE, "difficulty_level": "beginner", "skills_covered": json.dumps(["Programming", "Indian", "YouTube", "Hindi"]), "is_indian_creator": True, "is_india_focused": True, "language": "Hindi"},
    {"title": "CodeHelp by Babbar", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@CodeHelp", "description": "Complete DSA course by Love Babbar.", "pricing": ResourcePricing.FREE, "difficulty_level": "all", "skills_covered": json.dumps(["DSA", "Indian", "YouTube"]), "is_indian_creator": True, "is_india_focused": True},
    {"title": "Pepcoding", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@Pepcoding", "description": "DSA and competitive programming.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["DSA", "CP", "Indian", "YouTube"]), "is_indian_creator": True},
    {"title": "Hitesh Choudhary", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@HiteshChoudharydotcom", "description": "Web development and programming tutorials.", "pricing": ResourcePricing.FREE, "difficulty_level": "all", "skills_covered": json.dumps(["Web Dev", "Indian", "YouTube"]), "is_indian_creator": True},
    {"title": "Akshay Saini", "resource_type": ResourceType.YOUTUBE_CHANNEL, "platform": "YouTube", "url": "https://youtube.com/@akshaymarch7", "description": "Namaste JavaScript - Deep JS concepts.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["JavaScript", "Indian", "YouTube"]), "is_indian_creator": True, "is_india_focused": True},
    
    # Competitive Programming
    {"title": "Codeforces", "resource_type": ResourceType.WEBSITE, "platform": "Codeforces", "url": "https://codeforces.com", "description": "Competitive programming contests and practice.", "pricing": ResourcePricing.FREE, "difficulty_level": "advanced", "skills_covered": json.dumps(["CP", "Contests"])},
    {"title": "AtCoder", "resource_type": ResourceType.WEBSITE, "platform": "AtCoder", "url": "https://atcoder.jp", "description": "Japanese competitive programming platform.", "pricing": ResourcePricing.FREE, "difficulty_level": "advanced", "skills_covered": json.dumps(["CP", "Contests"])},
    {"title": "CSES Problem Set", "resource_type": ResourceType.WEBSITE, "platform": "CSES", "url": "https://cses.fi/problemset", "description": "Curated 300 competitive programming problems.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["CP", "DSA"])},
    {"title": "USACO Guide", "resource_type": ResourceType.WEBSITE, "platform": "USACO", "url": "https://usaco.guide", "description": "Free competitive programming curriculum.", "pricing": ResourcePricing.FREE, "difficulty_level": "advanced", "skills_covered": json.dumps(["CP", "Algorithms"])},
    
    # Interview Preparation Platforms
    {"title": "InterviewBit", "resource_type": ResourceType.WEBSITE, "platform": "InterviewBit", "url": "https://interviewbit.com", "description": "Structured interview preparation platform.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Interview", "DSA"])},
    {"title": "Pramp", "resource_type": ResourceType.WEBSITE, "platform": "Pramp", "url": "https://pramp.com", "description": "Free peer-to-peer mock interviews.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Interview", "Mock"])},
    {"title": "Interviewing.io", "resource_type": ResourceType.WEBSITE, "platform": "Interviewing.io", "url": "https://interviewing.io", "description": "Anonymous mock interviews with engineers.", "pricing": ResourcePricing.FREE, "difficulty_level": "intermediate", "skills_covered": json.dumps(["Interview", "Mock"])},
]


def seed_resources():
    """Seed learning resources"""
    logger.info("📚 Seeding Learning Resources...")
    init_db()
    db = SessionLocal()
    
    added = 0
    updated = 0
    
    try:
        for resource_data in RESOURCES:
            title = resource_data.get("title")
            existing = db.query(Resource).filter(Resource.title == title).first()
            
            if existing:
                for key, value in resource_data.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                resource = Resource(**resource_data)
                db.add(resource)
                added += 1
        
        db.commit()
        logger.info(f"✅ Resources: Added {added}, Updated {updated}")
        
        total = db.query(Resource).count()
        logger.info(f"📊 Total resources: {total}")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_resources()

