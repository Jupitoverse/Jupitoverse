# CareerLaunch Database Setup Guide

## Recommended: PostgreSQL

### Why PostgreSQL?
- **JSONB Support**: Store flexible data (skills, roadmap steps) with indexing
- **Full-Text Search**: Built-in search for jobs, companies, questions
- **Relationships**: Proper foreign keys and joins for user → experiences → projects
- **Scalability**: Handles millions of users, concurrent connections
- **Industry Standard**: Used by Naukri, LinkedIn, most job portals

---

## Quick Setup Options

### Option 1: Local PostgreSQL (Development)
```bash
# Windows - Download installer from https://www.postgresql.org/download/windows/
# Or use Chocolatey:
choco install postgresql

# Create database
psql -U postgres
CREATE DATABASE careerlaunch;
CREATE USER careerlaunch_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE careerlaunch TO careerlaunch_user;
```

### Option 2: Docker (Recommended for Development)
```bash
docker run --name careerlaunch-db \
  -e POSTGRES_DB=careerlaunch \
  -e POSTGRES_USER=careerlaunch_user \
  -e POSTGRES_PASSWORD=your_secure_password \
  -p 5432:5432 \
  -d postgres:15
```

### Option 3: Cloud (Production)
- **Supabase** (Free tier, PostgreSQL) - https://supabase.com
- **Railway** (Easy deployment) - https://railway.app
- **Neon** (Serverless PostgreSQL) - https://neon.tech
- **AWS RDS** / **Google Cloud SQL** (Enterprise)

---

## Database Schema Overview

### Core Tables
```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS & AUTH                            │
├─────────────────────────────────────────────────────────────────┤
│ users              - Authentication, basic info                 │
│ user_profiles      - Extended profile, preferences              │
│ subscriptions      - Payment/subscription records               │
│ referral_rewards   - Referral tracking                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       PROFILE DATA                              │
├─────────────────────────────────────────────────────────────────┤
│ educations         - User education history                     │
│ experiences        - Work experience                           │
│ projects           - Personal/work projects                     │
│ certifications     - Professional certifications                │
│ awards             - Awards & achievements                      │
│ user_skills        - User's skills with levels                 │
│ social_links       - LinkedIn, GitHub, etc.                    │
│ resumes            - Uploaded resumes                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     INTERVIEW TRACKING                          │
├─────────────────────────────────────────────────────────────────┤
│ interview_trackers - Track interview progress                   │
│ interview_questions- Community shared questions                 │
│ study_tasks        - Preparation tasks                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      COMPANIES & JOBS                           │
├─────────────────────────────────────────────────────────────────┤
│ companies          - Company database                          │
│ jobs               - Job listings                              │
│ job_applications   - User applications                         │
│ saved_jobs         - Bookmarked jobs                           │
│ hr_contacts        - HR contact database                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      MASTER DATA                                │
├─────────────────────────────────────────────────────────────────┤
│ skill_categories   - Programming, Frontend, Backend, etc.      │
│ skills             - Master skill list (400+)                  │
│ portfolio_templates- Portfolio design templates                 │
│ career_roadmaps    - Learning roadmaps                         │
│ resources          - Learning resources                        │
│ countries          - Abroad job destinations                   │
│ agencies           - Recruitment agencies                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     PORTFOLIO & CONTENT                         │
├─────────────────────────────────────────────────────────────────┤
│ user_portfolios    - Generated portfolios                      │
│ portfolio_analytics- View tracking                             │
│ user_roadmap_progress - Learning progress                      │
│ community_posts    - User discussions                          │
│ community_comments - Post comments                             │
│ reviews            - Company reviews                           │
│ referrals          - Referral requests                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     SCRAPED DATA                                │
├─────────────────────────────────────────────────────────────────┤
│ ai_tools           - AI tools directory                        │
│ git_repositories   - Popular GitHub repos                      │
│ youtube_channels   - Tech YouTube channels                     │
│ online_courses     - Course aggregation                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Environment Configuration

Create `.env` file in backend directory:
```env
# Database
DATABASE_URL=postgresql://careerlaunch_user:your_secure_password@localhost:5432/careerlaunch

# For development (SQLite fallback)
# DATABASE_URL=sqlite:///./job_hunt.db

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs (optional)
GITHUB_TOKEN=your_github_token
LINKEDIN_API_KEY=your_linkedin_key
```

---

## Migration Commands

```bash
# Initialize database
cd backend
python -c "from app.models.database import init_db; init_db()"

# Seed master data
python data/seeds/seed_skills.py
python data/seeds/seed_portfolio_templates.py
python data/seeds/seed_roadmaps.py
python data/seeds/seed_companies.py
python data/seeds/seed_ai_tools.py
python data/seeds/seed_git_repos.py

# Or seed everything at once
python data/seeds/seed_all_data.py
```

---

## Data Statistics (After Full Seeding)

| Table | Records | Description |
|-------|---------|-------------|
| companies | 500+ | Indian IT companies |
| skills | 400+ | Technical & soft skills |
| skill_categories | 12 | Skill groupings |
| career_roadmaps | 8 | Learning paths |
| portfolio_templates | 10 | Design templates |
| ai_tools | 100+ | AI tools directory |
| git_repositories | 50+ | Popular repos |
| resources | 200+ | Learning resources |
| countries | 20+ | Abroad destinations |
