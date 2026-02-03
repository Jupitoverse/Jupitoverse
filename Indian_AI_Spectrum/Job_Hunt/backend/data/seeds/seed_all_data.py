"""
Master Seed Script - Seeds all data in the correct order
Run this to populate the entire database with initial data
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import init_db, get_database_info

def run_all_seeds():
    """Run all seed scripts in the correct order"""
    print("=" * 60)
    print("🚀 CareerLaunch Database Seeding")
    print("=" * 60)
    
    # 1. Initialize database tables
    print("\n📦 Step 1: Initializing database tables...")
    init_db()
    
    # Show database info
    db_info = get_database_info()
    print(f"   Database type: {db_info['type']}")
    print(f"   Database URL: {db_info['url']}")
    
    # 2. Seed master data (no dependencies)
    print("\n📊 Step 2: Seeding master data...")
    
    # Skills
    print("\n   🔧 Seeding skills...")
    try:
        from seed_skills import seed_skills
        seed_skills()
    except Exception as e:
        print(f"   ⚠️ Skills seeding error: {e}")
    
    # Portfolio templates
    print("\n   🎨 Seeding portfolio templates...")
    try:
        from seed_portfolio_templates import seed_portfolio_templates
        seed_portfolio_templates()
    except Exception as e:
        print(f"   ⚠️ Portfolio templates seeding error: {e}")
    
    # Career roadmaps
    print("\n   🗺️ Seeding career roadmaps...")
    try:
        from seed_roadmaps import seed_roadmaps
        seed_roadmaps()
    except Exception as e:
        print(f"   ⚠️ Roadmaps seeding error: {e}")
    
    # 3. Seed content data
    print("\n📚 Step 3: Seeding content data...")
    
    # AI Tools
    print("\n   🤖 Seeding AI tools...")
    try:
        from seed_ai_tools import seed_ai_tools
        seed_ai_tools()
    except Exception as e:
        print(f"   ⚠️ AI tools seeding error: {e}")
    
    # Git repositories
    print("\n   📂 Seeding Git repositories...")
    try:
        from seed_git_repos import seed_git_repos
        seed_git_repos()
    except Exception as e:
        print(f"   ⚠️ Git repos seeding error: {e}")
    
    # 4. Seed company data
    print("\n🏢 Step 4: Seeding company data...")
    try:
        from seed_data import seed_database
        seed_database()
    except Exception as e:
        print(f"   ⚠️ Company data seeding error: {e}")
    
    # 5. Seed additional companies
    print("\n🏢 Step 5: Seeding more companies...")
    try:
        from more_companies import seed_more_companies
        seed_more_companies()
    except Exception as e:
        print(f"   ⚠️ More companies seeding error: {e}")
    
    # 6. Seed resources
    print("\n📖 Step 6: Seeding resources...")
    try:
        from resources_data import seed_resources
        seed_resources()
    except Exception as e:
        print(f"   ⚠️ Resources seeding error: {e}")
    
    # 7. Seed countries
    print("\n🌍 Step 7: Seeding countries...")
    try:
        from country_details import seed_countries
        seed_countries()
    except Exception as e:
        print(f"   ⚠️ Countries seeding error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Database seeding complete!")
    print("=" * 60)
    
    # Print summary
    print_summary()


def print_summary():
    """Print database summary"""
    from app.models import get_db
    from sqlalchemy import text
    
    db = next(get_db())
    
    print("\n📊 Database Summary:")
    print("-" * 40)
    
    tables = [
        ("skill_categories", "Skill Categories"),
        ("skills", "Skills"),
        ("portfolio_templates", "Portfolio Templates"),
        ("career_roadmaps", "Career Roadmaps"),
        ("ai_tools", "AI Tools"),
        ("git_repositories", "Git Repositories"),
        ("companies", "Companies"),
        ("resources", "Resources"),
        ("countries", "Countries"),
    ]
    
    for table_name, display_name in tables:
        try:
            result = db.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            print(f"   {display_name}: {count}")
        except:
            print(f"   {display_name}: (table not found)")
    
    db.close()


if __name__ == "__main__":
    # Change to seeds directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_all_seeds()
