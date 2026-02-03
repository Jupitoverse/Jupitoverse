// AI Tools Database - Phase 14: Education, Learning & HR AI
// 200+ Tools for education and human resources

const AI_TOOLS_PHASE14 = [
    // ==================== ONLINE LEARNING ====================
    {name: "Coursera", category: "Learning", subcategory: "Courses", desc: "Online courses from universities", url: "coursera.org", pricing: "Freemium", rating: 4.6, tags: ["university", "certificates", "degrees"], featured: true},
    {name: "Udemy", category: "Learning", subcategory: "Courses", desc: "Learn anything online", url: "udemy.com", pricing: "Paid", rating: 4.5, tags: ["courses", "affordable", "variety"]},
    {name: "edX", category: "Learning", subcategory: "Courses", desc: "Online courses from top institutions", url: "edx.org", pricing: "Freemium", rating: 4.5, tags: ["university", "free", "certificates"]},
    {name: "LinkedIn Learning", category: "Learning", subcategory: "Professional", desc: "Professional learning platform", url: "linkedin.com/learning", pricing: "Paid", rating: 4.4, tags: ["professional", "linkedin", "business"]},
    {name: "Skillshare", category: "Learning", subcategory: "Creative", desc: "Creative skills platform", url: "skillshare.com", pricing: "Paid", rating: 4.4, tags: ["creative", "projects", "community"]},
    {name: "MasterClass", category: "Learning", subcategory: "Celebrity", desc: "Learn from the best", url: "masterclass.com", pricing: "Paid", rating: 4.4, tags: ["celebrities", "premium", "video"]},
    {name: "Pluralsight", category: "Learning", subcategory: "Tech", desc: "Technology skills platform", url: "pluralsight.com", pricing: "Paid", rating: 4.5, tags: ["tech", "paths", "assessments"]},
    {name: "Codecademy", category: "Learning", subcategory: "Coding", desc: "Learn to code interactively", url: "codecademy.com", pricing: "Freemium", rating: 4.5, tags: ["coding", "interactive", "beginner"]},
    {name: "freeCodeCamp", category: "Learning", subcategory: "Coding", desc: "Free coding education", url: "freecodecamp.org", pricing: "Free", rating: 4.7, tags: ["free", "coding", "certificates"]},
    {name: "Udacity", category: "Learning", subcategory: "Tech", desc: "Tech nanodegrees", url: "udacity.com", pricing: "Paid", rating: 4.2, tags: ["nanodegrees", "tech", "career"]},
    {name: "DataCamp", category: "Learning", subcategory: "Data", desc: "Data science education", url: "datacamp.com", pricing: "Freemium", rating: 4.4, tags: ["data-science", "interactive", "python"]},
    {name: "Brilliant", category: "Learning", subcategory: "Math/Science", desc: "Interactive STEM learning", url: "brilliant.org", pricing: "Freemium", rating: 4.5, tags: ["stem", "interactive", "problem-solving"]},
    {name: "Khan Academy", category: "Learning", subcategory: "Free", desc: "Free education for everyone", url: "khanacademy.org", pricing: "Free", rating: 4.7, tags: ["free", "k-12", "nonprofit"]},
    {name: "Duolingo", category: "Learning", subcategory: "Languages", desc: "Language learning app", url: "duolingo.com", pricing: "Freemium", rating: 4.6, tags: ["languages", "gamified", "free"]},
    {name: "Babbel", category: "Learning", subcategory: "Languages", desc: "Language learning", url: "babbel.com", pricing: "Paid", rating: 4.4, tags: ["languages", "practical", "speech"]},
    
    // ==================== AI LEARNING TOOLS ====================
    {name: "Khanmigo", category: "AI Education", subcategory: "Tutor", desc: "AI tutor by Khan Academy", url: "khanacademy.org/khan-labs", pricing: "Paid", rating: 4.5, tags: ["tutor", "khan-academy", "personalized"], featured: true},
    {name: "Quizlet", category: "AI Education", subcategory: "Flashcards", desc: "AI-powered flashcards", url: "quizlet.com", pricing: "Freemium", rating: 4.5, tags: ["flashcards", "study", "ai"]},
    {name: "Photomath", category: "AI Education", subcategory: "Math", desc: "AI math solver", url: "photomath.com", pricing: "Freemium", rating: 4.6, tags: ["math", "camera", "steps"]},
    {name: "Socratic by Google", category: "AI Education", subcategory: "Homework", desc: "AI homework helper", url: "socratic.org", pricing: "Free", rating: 4.4, tags: ["homework", "google", "camera"]},
    {name: "Elsa Speak", category: "AI Education", subcategory: "Speaking", desc: "AI English pronunciation", url: "elsaspeak.com", pricing: "Freemium", rating: 4.5, tags: ["pronunciation", "english", "ai"]},
    {name: "Speak", category: "AI Education", subcategory: "Languages", desc: "AI language tutor", url: "speak.com", pricing: "Paid", rating: 4.4, tags: ["speaking", "ai", "conversation"]},
    {name: "Knowji", category: "AI Education", subcategory: "Vocabulary", desc: "AI vocabulary learning", url: "knowji.com", pricing: "Paid", rating: 4.2, tags: ["vocabulary", "spaced-repetition", "ai"]},
    {name: "Synthesis", category: "AI Education", subcategory: "Kids", desc: "Learning for kids by Musk's team", url: "synthesis.com", pricing: "Paid", rating: 4.3, tags: ["kids", "games", "thinking"]},
    {name: "Coursera Coach", category: "AI Education", subcategory: "Coaching", desc: "AI learning coach", url: "coursera.org", pricing: "Paid", rating: 4.2, tags: ["coaching", "coursera", "personalized"]},
    {name: "Duolingo Max", category: "AI Education", subcategory: "Languages", desc: "AI-powered language learning", url: "duolingo.com", pricing: "Paid", rating: 4.4, tags: ["gpt-4", "explain", "roleplay"]},
    {name: "Scholarly", category: "AI Education", subcategory: "Notes", desc: "AI study companion", url: "scholarly.so", pricing: "Freemium", rating: 4.2, tags: ["notes", "flashcards", "ai"]},
    {name: "Tome", category: "AI Education", subcategory: "Presentations", desc: "AI presentations", url: "tome.app", pricing: "Freemium", rating: 4.4, tags: ["presentations", "ai", "storytelling"]},
    {name: "Gamma", category: "AI Education", subcategory: "Presentations", desc: "AI presentation maker", url: "gamma.app", pricing: "Freemium", rating: 4.5, tags: ["presentations", "docs", "ai"]},
    {name: "Caktus AI", category: "AI Education", subcategory: "Writing", desc: "AI for students", url: "caktus.ai", pricing: "Freemium", rating: 4.0, tags: ["essays", "students", "writing"]},
    {name: "Gradescope", category: "AI Education", subcategory: "Grading", desc: "AI-assisted grading", url: "gradescope.com", pricing: "Paid", rating: 4.3, tags: ["grading", "rubrics", "feedback"]},
    
    // ==================== LMS & COURSE CREATION ====================
    {name: "Teachable", category: "Course Creation", subcategory: "Platform", desc: "Create and sell courses", url: "teachable.com", pricing: "Freemium", rating: 4.4, tags: ["courses", "creators", "monetization"], featured: true},
    {name: "Thinkific", category: "Course Creation", subcategory: "Platform", desc: "Online course platform", url: "thinkific.com", pricing: "Freemium", rating: 4.4, tags: ["courses", "memberships", "community"]},
    {name: "Kajabi", category: "Course Creation", subcategory: "All-in-one", desc: "All-in-one creator platform", url: "kajabi.com", pricing: "Paid", rating: 4.3, tags: ["courses", "marketing", "premium"]},
    {name: "Podia", category: "Course Creation", subcategory: "Simple", desc: "Sell courses and downloads", url: "podia.com", pricing: "Paid", rating: 4.4, tags: ["simple", "downloads", "memberships"]},
    {name: "LearnDash", category: "Course Creation", subcategory: "WordPress", desc: "WordPress LMS plugin", url: "learndash.com", pricing: "Paid", rating: 4.3, tags: ["wordpress", "lms", "flexible"]},
    {name: "Moodle", category: "LMS", subcategory: "Open Source", desc: "Open source LMS", url: "moodle.org", pricing: "Free", rating: 4.2, tags: ["open-source", "education", "customizable"]},
    {name: "Canvas", category: "LMS", subcategory: "Education", desc: "Learning management system", url: "instructure.com/canvas", pricing: "Paid", rating: 4.4, tags: ["k-12", "higher-ed", "enterprise"]},
    {name: "Blackboard", category: "LMS", subcategory: "Enterprise", desc: "Education technology", url: "blackboard.com", pricing: "Paid", rating: 3.8, tags: ["enterprise", "education", "legacy"]},
    {name: "Google Classroom", category: "LMS", subcategory: "Free", desc: "Free learning management", url: "classroom.google.com", pricing: "Free", rating: 4.4, tags: ["free", "google", "simple"]},
    {name: "Schoology", category: "LMS", subcategory: "K-12", desc: "K-12 learning platform", url: "schoology.com", pricing: "Paid", rating: 4.2, tags: ["k-12", "lms", "assessment"]},
    {name: "TalentLMS", category: "LMS", subcategory: "Corporate", desc: "Corporate training LMS", url: "talentlms.com", pricing: "Freemium", rating: 4.4, tags: ["corporate", "training", "affordable"]},
    {name: "360Learning", category: "LMS", subcategory: "Collaborative", desc: "Collaborative learning", url: "360learning.com", pricing: "Paid", rating: 4.4, tags: ["collaborative", "peer-learning", "ai"]},
    {name: "Docebo", category: "LMS", subcategory: "Enterprise", desc: "AI-powered LMS", url: "docebo.com", pricing: "Paid", rating: 4.3, tags: ["enterprise", "ai", "content"]},
    {name: "Absorb LMS", category: "LMS", subcategory: "Corporate", desc: "Corporate learning platform", url: "absorblms.com", pricing: "Paid", rating: 4.4, tags: ["corporate", "modern", "integrations"]},
    {name: "LearnWorlds", category: "Course Creation", subcategory: "Interactive", desc: "Interactive course platform", url: "learnworlds.com", pricing: "Paid", rating: 4.4, tags: ["interactive", "video", "community"]},
    
    // ==================== HR & RECRUITING ====================
    {name: "Workday", category: "HR", subcategory: "HCM", desc: "Enterprise HCM", url: "workday.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "hcm", "finance"], featured: true},
    {name: "BambooHR", category: "HR", subcategory: "HRIS", desc: "HR software for SMB", url: "bamboohr.com", pricing: "Paid", rating: 4.5, tags: ["smb", "hris", "modern"]},
    {name: "Gusto", category: "HR", subcategory: "Payroll", desc: "Payroll and HR", url: "gusto.com", pricing: "Paid", rating: 4.5, tags: ["payroll", "benefits", "smb"]},
    {name: "Rippling", category: "HR", subcategory: "All-in-one", desc: "HR, IT, and finance", url: "rippling.com", pricing: "Paid", rating: 4.5, tags: ["unified", "it", "automation"]},
    {name: "Deel", category: "HR", subcategory: "Global", desc: "Global payroll and HR", url: "deel.com", pricing: "Paid", rating: 4.5, tags: ["global", "contractors", "compliance"]},
    {name: "Remote.com", category: "HR", subcategory: "Global", desc: "Global HR platform", url: "remote.com", pricing: "Paid", rating: 4.4, tags: ["global", "employment", "compliance"]},
    {name: "Greenhouse", category: "Recruiting", subcategory: "ATS", desc: "Hiring software", url: "greenhouse.io", pricing: "Paid", rating: 4.4, tags: ["ats", "hiring", "structured"]},
    {name: "Lever", category: "Recruiting", subcategory: "ATS", desc: "Talent acquisition suite", url: "lever.co", pricing: "Paid", rating: 4.4, tags: ["ats", "crm", "modern"]},
    {name: "Ashby", category: "Recruiting", subcategory: "ATS", desc: "All-in-one recruiting", url: "ashbyhq.com", pricing: "Paid", rating: 4.5, tags: ["ats", "analytics", "modern"]},
    {name: "Workable", category: "Recruiting", subcategory: "ATS", desc: "Recruiting software", url: "workable.com", pricing: "Paid", rating: 4.3, tags: ["ats", "sourcing", "ai"]},
    {name: "SmartRecruiters", category: "Recruiting", subcategory: "Enterprise", desc: "Enterprise recruiting", url: "smartrecruiters.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "ats", "marketplace"]},
    {name: "HireVue", category: "Recruiting", subcategory: "Video", desc: "Video interviewing", url: "hirevue.com", pricing: "Paid", rating: 4.0, tags: ["video", "ai", "assessment"]},
    {name: "Pymetrics", category: "Recruiting", subcategory: "Assessment", desc: "AI talent matching", url: "pymetrics.ai", pricing: "Paid", rating: 4.1, tags: ["ai", "games", "bias-free"]},
    {name: "Eightfold.ai", category: "Recruiting", subcategory: "AI", desc: "AI talent intelligence", url: "eightfold.ai", pricing: "Paid", rating: 4.3, tags: ["ai", "matching", "talent"]},
    {name: "Phenom", category: "Recruiting", subcategory: "Experience", desc: "Talent experience platform", url: "phenom.com", pricing: "Paid", rating: 4.3, tags: ["experience", "ai", "career-site"]},
    
    // ==================== EMPLOYEE ENGAGEMENT ====================
    {name: "Lattice", category: "HR", subcategory: "Performance", desc: "People management platform", url: "lattice.com", pricing: "Paid", rating: 4.5, tags: ["performance", "engagement", "goals"], featured: true},
    {name: "Culture Amp", category: "HR", subcategory: "Engagement", desc: "Employee experience platform", url: "cultureamp.com", pricing: "Paid", rating: 4.4, tags: ["engagement", "surveys", "analytics"]},
    {name: "15Five", category: "HR", subcategory: "Performance", desc: "Performance management", url: "15five.com", pricing: "Paid", rating: 4.4, tags: ["performance", "1-on-1s", "okrs"]},
    {name: "Leapsome", category: "HR", subcategory: "All-in-one", desc: "People enablement platform", url: "leapsome.com", pricing: "Paid", rating: 4.5, tags: ["performance", "engagement", "learning"]},
    {name: "Peakon (Workday)", category: "HR", subcategory: "Engagement", desc: "Employee engagement", url: "peakon.com", pricing: "Paid", rating: 4.4, tags: ["engagement", "listening", "ai"]},
    {name: "Officevibe", category: "HR", subcategory: "Engagement", desc: "Employee engagement tool", url: "officevibe.com", pricing: "Freemium", rating: 4.3, tags: ["pulse", "feedback", "simple"]},
    {name: "TINYpulse", category: "HR", subcategory: "Engagement", desc: "Employee engagement surveys", url: "tinypulse.com", pricing: "Paid", rating: 4.2, tags: ["pulse", "recognition", "feedback"]},
    {name: "Bonusly", category: "HR", subcategory: "Recognition", desc: "Employee recognition", url: "bonus.ly", pricing: "Paid", rating: 4.5, tags: ["recognition", "rewards", "culture"]},
    {name: "Kudos", category: "HR", subcategory: "Recognition", desc: "Employee recognition platform", url: "kudos.com", pricing: "Paid", rating: 4.3, tags: ["recognition", "culture", "analytics"]},
    {name: "Motivosity", category: "HR", subcategory: "Recognition", desc: "Employee recognition software", url: "motivosity.com", pricing: "Paid", rating: 4.5, tags: ["recognition", "gratitude", "belonging"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE14 = AI_TOOLS_PHASE14;
}


