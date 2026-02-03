// Comprehensive Learning Resources Database for AI Spectrum India

const LEARNING_RESOURCES = {
    // ==================== PROGRAMMING LANGUAGES ====================
    programming: [
        // Python
        {name: "Python.org Tutorial", category: "Programming", sub: "Python", level: "Beginner", url: "https://docs.python.org/3/tutorial/", type: "Documentation", free: true, rating: 4.8, desc: "Official Python tutorial - best starting point"},
        {name: "Automate the Boring Stuff", category: "Programming", sub: "Python", level: "Beginner", url: "https://automatetheboringstuff.com/", type: "Book/Course", free: true, rating: 4.9, desc: "Practical Python for automation - free book"},
        {name: "Real Python", category: "Programming", sub: "Python", level: "All", url: "https://realpython.com/", type: "Tutorials", free: false, rating: 4.8, desc: "High-quality Python tutorials and articles"},
        {name: "Python Crash Course", category: "Programming", sub: "Python", level: "Beginner", url: "https://nostarch.com/pythoncrashcourse2e", type: "Book", free: false, rating: 4.7, desc: "Best-selling Python book for beginners"},
        {name: "Corey Schafer Python", category: "Programming", sub: "Python", level: "All", url: "https://youtube.com/@coreyms", type: "Video", free: true, rating: 4.9, desc: "Excellent Python YouTube tutorials"},
        
        // JavaScript
        {name: "JavaScript.info", category: "Programming", sub: "JavaScript", level: "All", url: "https://javascript.info/", type: "Tutorial", free: true, rating: 4.9, desc: "Modern JavaScript tutorial - comprehensive"},
        {name: "FreeCodeCamp JavaScript", category: "Programming", sub: "JavaScript", level: "Beginner", url: "https://freecodecamp.org/learn/javascript-algorithms-and-data-structures/", type: "Course", free: true, rating: 4.8, desc: "Interactive JavaScript course"},
        {name: "Eloquent JavaScript", category: "Programming", sub: "JavaScript", level: "Intermediate", url: "https://eloquentjavascript.net/", type: "Book", free: true, rating: 4.7, desc: "Deep dive into JavaScript"},
        {name: "You Don't Know JS", category: "Programming", sub: "JavaScript", level: "Advanced", url: "https://github.com/getify/You-Dont-Know-JS", type: "Book", free: true, rating: 4.8, desc: "Advanced JavaScript concepts"},
        {name: "Traversy Media JS", category: "Programming", sub: "JavaScript", level: "All", url: "https://youtube.com/@TraversyMedia", type: "Video", free: true, rating: 4.8, desc: "Popular JS YouTube channel"},
        
        // Java
        {name: "Java Programming MOOC", category: "Programming", sub: "Java", level: "Beginner", url: "https://java-programming.mooc.fi/", type: "Course", free: true, rating: 4.8, desc: "University of Helsinki Java course"},
        {name: "Head First Java", category: "Programming", sub: "Java", level: "Beginner", url: "https://oreilly.com/library/view/head-first-java/9781492091646/", type: "Book", free: false, rating: 4.7, desc: "Fun way to learn Java"},
        {name: "Baeldung", category: "Programming", sub: "Java", level: "All", url: "https://baeldung.com/", type: "Tutorials", free: true, rating: 4.7, desc: "Java and Spring tutorials"},
        
        // Go
        {name: "Go by Example", category: "Programming", sub: "Go", level: "Beginner", url: "https://gobyexample.com/", type: "Tutorial", free: true, rating: 4.8, desc: "Learn Go through annotated examples"},
        {name: "Tour of Go", category: "Programming", sub: "Go", level: "Beginner", url: "https://go.dev/tour/", type: "Interactive", free: true, rating: 4.9, desc: "Official interactive Go tutorial"},
        
        // Rust
        {name: "The Rust Book", category: "Programming", sub: "Rust", level: "Beginner", url: "https://doc.rust-lang.org/book/", type: "Book", free: true, rating: 4.9, desc: "Official Rust programming book"},
        {name: "Rustlings", category: "Programming", sub: "Rust", level: "Beginner", url: "https://github.com/rust-lang/rustlings", type: "Exercises", free: true, rating: 4.8, desc: "Small exercises to learn Rust"},
    ],

    // ==================== WEB DEVELOPMENT ====================
    webDev: [
        // Frontend
        {name: "MDN Web Docs", category: "Web Dev", sub: "Frontend", level: "All", url: "https://developer.mozilla.org/", type: "Documentation", free: true, rating: 4.9, desc: "The definitive web dev resource"},
        {name: "The Odin Project", category: "Web Dev", sub: "Full Stack", level: "Beginner", url: "https://theodinproject.com/", type: "Curriculum", free: true, rating: 4.9, desc: "Free full-stack curriculum"},
        {name: "FreeCodeCamp", category: "Web Dev", sub: "Full Stack", level: "Beginner", url: "https://freecodecamp.org/", type: "Course", free: true, rating: 4.8, desc: "Comprehensive web dev courses"},
        {name: "Frontend Masters", category: "Web Dev", sub: "Frontend", level: "All", url: "https://frontendmasters.com/", type: "Video", free: false, rating: 4.8, desc: "Expert-led frontend courses"},
        {name: "CSS Tricks", category: "Web Dev", sub: "CSS", level: "All", url: "https://css-tricks.com/", type: "Tutorials", free: true, rating: 4.7, desc: "CSS tips and techniques"},
        
        // React
        {name: "React Official Docs", category: "Web Dev", sub: "React", level: "All", url: "https://react.dev/", type: "Documentation", free: true, rating: 4.9, desc: "Official React documentation"},
        {name: "Full Stack Open", category: "Web Dev", sub: "React", level: "Intermediate", url: "https://fullstackopen.com/", type: "Course", free: true, rating: 4.9, desc: "University of Helsinki React course"},
        {name: "Epic React", category: "Web Dev", sub: "React", level: "Advanced", url: "https://epicreact.dev/", type: "Course", free: false, rating: 4.9, desc: "Kent C. Dodds React course"},
        
        // Node.js
        {name: "Node.js Docs", category: "Web Dev", sub: "Node.js", level: "All", url: "https://nodejs.org/docs/", type: "Documentation", free: true, rating: 4.7, desc: "Official Node.js documentation"},
        {name: "Node.js Best Practices", category: "Web Dev", sub: "Node.js", level: "Intermediate", url: "https://github.com/goldbergyoni/nodebestpractices", type: "Guide", free: true, rating: 4.8, desc: "Node.js best practices guide"},
    ],

    // ==================== DATA SCIENCE & ML ====================
    dataScience: [
        {name: "Fast.ai", category: "ML/AI", sub: "Deep Learning", level: "Intermediate", url: "https://fast.ai/", type: "Course", free: true, rating: 4.9, desc: "Practical deep learning course"},
        {name: "Kaggle Learn", category: "ML/AI", sub: "Data Science", level: "Beginner", url: "https://kaggle.com/learn", type: "Course", free: true, rating: 4.8, desc: "Hands-on data science courses"},
        {name: "Andrew Ng ML Course", category: "ML/AI", sub: "Machine Learning", level: "Beginner", url: "https://coursera.org/learn/machine-learning", type: "Course", free: true, rating: 4.9, desc: "Classic ML course by Andrew Ng"},
        {name: "Deep Learning Specialization", category: "ML/AI", sub: "Deep Learning", level: "Intermediate", url: "https://coursera.org/specializations/deep-learning", type: "Course", free: false, rating: 4.9, desc: "Comprehensive DL specialization"},
        {name: "StatQuest", category: "ML/AI", sub: "Statistics", level: "All", url: "https://youtube.com/@statquest", type: "Video", free: true, rating: 4.9, desc: "Statistics and ML explained clearly"},
        {name: "3Blue1Brown", category: "ML/AI", sub: "Math", level: "All", url: "https://youtube.com/@3blue1brown", type: "Video", free: true, rating: 5.0, desc: "Beautiful math visualizations"},
        {name: "Hands-On ML Book", category: "ML/AI", sub: "Machine Learning", level: "Intermediate", url: "https://oreilly.com/library/view/hands-on-machine-learning/9781492032632/", type: "Book", free: false, rating: 4.9, desc: "Practical ML with Scikit-Learn"},
        {name: "Hugging Face Course", category: "ML/AI", sub: "NLP", level: "Intermediate", url: "https://huggingface.co/course", type: "Course", free: true, rating: 4.8, desc: "NLP with Transformers"},
        {name: "Made With ML", category: "ML/AI", sub: "MLOps", level: "Intermediate", url: "https://madewithml.com/", type: "Course", free: true, rating: 4.7, desc: "MLOps best practices"},
    ],

    // ==================== SYSTEM DESIGN ====================
    systemDesign: [
        {name: "System Design Primer", category: "System Design", sub: "Fundamentals", level: "Intermediate", url: "https://github.com/donnemartin/system-design-primer", type: "Guide", free: true, rating: 4.9, desc: "Comprehensive system design guide"},
        {name: "Designing Data-Intensive Apps", category: "System Design", sub: "Distributed", level: "Advanced", url: "https://dataintensive.net/", type: "Book", free: false, rating: 5.0, desc: "Must-read for backend engineers"},
        {name: "ByteByteGo", category: "System Design", sub: "All", level: "Intermediate", url: "https://bytebytego.com/", type: "Newsletter", free: false, rating: 4.8, desc: "System design newsletter by Alex Xu"},
        {name: "High Scalability", category: "System Design", sub: "Case Studies", level: "Advanced", url: "http://highscalability.com/", type: "Blog", free: true, rating: 4.7, desc: "Real-world architecture case studies"},
        {name: "Grokking System Design", category: "System Design", sub: "Interview", level: "Intermediate", url: "https://designgurus.org/course/grokking-the-system-design-interview", type: "Course", free: false, rating: 4.7, desc: "System design interview prep"},
    ],

    // ==================== DSA & INTERVIEW PREP ====================
    dsa: [
        {name: "LeetCode", category: "DSA", sub: "Practice", level: "All", url: "https://leetcode.com/", type: "Platform", free: true, rating: 4.9, desc: "Most popular coding practice platform"},
        {name: "NeetCode", category: "DSA", sub: "Roadmap", level: "Intermediate", url: "https://neetcode.io/", type: "Roadmap", free: true, rating: 4.9, desc: "Curated LeetCode roadmap"},
        {name: "Blind 75", category: "DSA", sub: "List", level: "Intermediate", url: "https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions", type: "List", free: true, rating: 4.8, desc: "Essential 75 LeetCode problems"},
        {name: "Strivers A2Z DSA", category: "DSA", sub: "Course", level: "All", url: "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/", type: "Course", free: true, rating: 4.9, desc: "Comprehensive DSA by Striver"},
        {name: "AlgoExpert", category: "DSA", sub: "Interview", level: "Intermediate", url: "https://algoexpert.io/", type: "Course", free: false, rating: 4.7, desc: "Curated coding interview prep"},
        {name: "Codeforces", category: "DSA", sub: "Competitive", level: "Advanced", url: "https://codeforces.com/", type: "Platform", free: true, rating: 4.8, desc: "Competitive programming platform"},
        {name: "CSES Problem Set", category: "DSA", sub: "Practice", level: "All", url: "https://cses.fi/problemset/", type: "Problems", free: true, rating: 4.8, desc: "High-quality problem set"},
    ],

    // ==================== DEVOPS & CLOUD ====================
    devops: [
        {name: "Docker Docs", category: "DevOps", sub: "Docker", level: "Beginner", url: "https://docs.docker.com/", type: "Documentation", free: true, rating: 4.8, desc: "Official Docker documentation"},
        {name: "Kubernetes.io", category: "DevOps", sub: "Kubernetes", level: "Intermediate", url: "https://kubernetes.io/docs/", type: "Documentation", free: true, rating: 4.8, desc: "Official K8s documentation"},
        {name: "DevOps Roadmap", category: "DevOps", sub: "Roadmap", level: "All", url: "https://roadmap.sh/devops", type: "Roadmap", free: true, rating: 4.8, desc: "DevOps learning roadmap"},
        {name: "AWS Free Tier", category: "DevOps", sub: "AWS", level: "Beginner", url: "https://aws.amazon.com/free/", type: "Platform", free: true, rating: 4.7, desc: "AWS free tier for practice"},
        {name: "KodeKloud", category: "DevOps", sub: "All", level: "All", url: "https://kodekloud.com/", type: "Course", free: false, rating: 4.8, desc: "Hands-on DevOps courses"},
        {name: "Terraform Docs", category: "DevOps", sub: "IaC", level: "Intermediate", url: "https://terraform.io/docs", type: "Documentation", free: true, rating: 4.7, desc: "Infrastructure as Code"},
    ],

    // ==================== CERTIFICATIONS ====================
    certifications: [
        {name: "AWS Certified Solutions Architect", category: "Certification", sub: "AWS", level: "Intermediate", url: "https://aws.amazon.com/certification/certified-solutions-architect-associate/", type: "Certification", free: false, rating: 4.8, desc: "Most popular cloud certification"},
        {name: "Google Cloud Certifications", category: "Certification", sub: "GCP", level: "Intermediate", url: "https://cloud.google.com/certification", type: "Certification", free: false, rating: 4.7, desc: "GCP certifications"},
        {name: "Azure Certifications", category: "Certification", sub: "Azure", level: "Intermediate", url: "https://learn.microsoft.com/en-us/certifications/", type: "Certification", free: false, rating: 4.7, desc: "Microsoft Azure certs"},
        {name: "CKA - Kubernetes Admin", category: "Certification", sub: "Kubernetes", level: "Advanced", url: "https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/", type: "Certification", free: false, rating: 4.8, desc: "Kubernetes admin certification"},
        {name: "Terraform Associate", category: "Certification", sub: "IaC", level: "Intermediate", url: "https://hashicorp.com/certification/terraform-associate", type: "Certification", free: false, rating: 4.6, desc: "HashiCorp Terraform cert"},
    ],

    // ==================== SOFT SKILLS ====================
    softSkills: [
        {name: "Tech Interview Handbook", category: "Career", sub: "Interviews", level: "All", url: "https://techinterviewhandbook.org/", type: "Guide", free: true, rating: 4.9, desc: "Complete interview preparation"},
        {name: "Levels.fyi", category: "Career", sub: "Salary", level: "All", url: "https://levels.fyi/", type: "Data", free: true, rating: 4.8, desc: "Tech salary data"},
        {name: "Blind", category: "Career", sub: "Community", level: "All", url: "https://teamblind.com/", type: "Community", free: true, rating: 4.5, desc: "Anonymous tech community"},
        {name: "Gergely Orosz Newsletter", category: "Career", sub: "Growth", level: "All", url: "https://newsletter.pragmaticengineer.com/", type: "Newsletter", free: false, rating: 4.8, desc: "Engineering career insights"},
    ]
};

// Career Roadmaps
const CAREER_ROADMAPS = {
    frontend: {
        title: "Frontend Developer Roadmap",
        description: "Complete path to becoming a frontend developer",
        duration: "6-12 months",
        salary: "₹6-25 LPA",
        steps: [
            {phase: "Foundation", duration: "2 months", skills: ["HTML5", "CSS3", "JavaScript ES6+"], resources: ["MDN Web Docs", "FreeCodeCamp", "JavaScript.info"]},
            {phase: "CSS Mastery", duration: "1 month", skills: ["Flexbox", "Grid", "Responsive Design", "Sass/SCSS", "Tailwind CSS"], resources: ["CSS Tricks", "Tailwind Docs"]},
            {phase: "JavaScript Deep Dive", duration: "2 months", skills: ["DOM Manipulation", "Async/Await", "Fetch API", "TypeScript"], resources: ["You Don't Know JS", "TypeScript Docs"]},
            {phase: "React Ecosystem", duration: "2 months", skills: ["React", "React Router", "State Management", "Hooks"], resources: ["React.dev", "Full Stack Open"]},
            {phase: "Build Tools", duration: "2 weeks", skills: ["Webpack", "Vite", "npm/yarn", "ESLint"], resources: ["Vite Docs", "Webpack Docs"]},
            {phase: "Testing", duration: "2 weeks", skills: ["Jest", "React Testing Library", "Cypress"], resources: ["Testing Library Docs"]},
            {phase: "Advanced", duration: "1 month", skills: ["Next.js", "Performance Optimization", "PWA", "GraphQL"], resources: ["Next.js Docs", "Web.dev"]}
        ]
    },
    backend: {
        title: "Backend Developer Roadmap",
        description: "Complete path to becoming a backend developer",
        duration: "8-12 months",
        salary: "₹8-30 LPA",
        steps: [
            {phase: "Programming Fundamentals", duration: "2 months", skills: ["Python/Node.js/Java/Go", "Data Structures", "Algorithms"], resources: ["Python.org", "Node.js Docs"]},
            {phase: "Databases", duration: "1 month", skills: ["SQL", "PostgreSQL", "MongoDB", "Redis"], resources: ["PostgreSQL Tutorial", "MongoDB University"]},
            {phase: "API Development", duration: "1 month", skills: ["REST APIs", "Express.js/FastAPI/Spring Boot", "Authentication"], resources: ["REST API Tutorial", "JWT.io"]},
            {phase: "DevOps Basics", duration: "1 month", skills: ["Linux", "Docker", "Git", "CI/CD"], resources: ["Docker Docs", "GitHub Actions"]},
            {phase: "System Design", duration: "2 months", skills: ["Microservices", "Message Queues", "Caching", "Load Balancing"], resources: ["System Design Primer", "ByteByteGo"]},
            {phase: "Cloud", duration: "1 month", skills: ["AWS/GCP/Azure", "Serverless", "Kubernetes"], resources: ["AWS Free Tier", "KodeKloud"]},
            {phase: "Security", duration: "2 weeks", skills: ["OWASP", "Encryption", "Security Best Practices"], resources: ["OWASP", "Auth0 Blog"]}
        ]
    },
    fullstack: {
        title: "Full Stack Developer Roadmap",
        description: "Complete path to becoming a full stack developer",
        duration: "12-18 months",
        salary: "₹10-35 LPA",
        steps: [
            {phase: "Web Fundamentals", duration: "2 months", skills: ["HTML", "CSS", "JavaScript"], resources: ["The Odin Project", "FreeCodeCamp"]},
            {phase: "Frontend Framework", duration: "2 months", skills: ["React/Vue/Angular", "State Management"], resources: ["React.dev", "Vue.js Docs"]},
            {phase: "Backend Development", duration: "3 months", skills: ["Node.js/Python", "Express/FastAPI", "REST APIs"], resources: ["Full Stack Open", "Real Python"]},
            {phase: "Databases", duration: "1 month", skills: ["SQL", "PostgreSQL", "MongoDB"], resources: ["PostgreSQL Tutorial", "MongoDB Docs"]},
            {phase: "DevOps", duration: "1 month", skills: ["Docker", "CI/CD", "Deployment"], resources: ["Docker Docs", "Vercel Docs"]},
            {phase: "Full Stack Project", duration: "2 months", skills: ["Complete App", "Authentication", "Deployment"], resources: ["Build projects", "GitHub"]}
        ]
    },
    dataScience: {
        title: "Data Scientist Roadmap",
        description: "Complete path to becoming a data scientist",
        duration: "12-18 months",
        salary: "₹10-40 LPA",
        steps: [
            {phase: "Math & Statistics", duration: "2 months", skills: ["Linear Algebra", "Statistics", "Probability"], resources: ["Khan Academy", "StatQuest"]},
            {phase: "Python for Data", duration: "2 months", skills: ["Python", "NumPy", "Pandas", "Matplotlib"], resources: ["Kaggle Learn", "Real Python"]},
            {phase: "Machine Learning", duration: "3 months", skills: ["Scikit-learn", "ML Algorithms", "Feature Engineering"], resources: ["Andrew Ng Course", "Hands-On ML"]},
            {phase: "Deep Learning", duration: "2 months", skills: ["Neural Networks", "TensorFlow/PyTorch", "CNNs", "RNNs"], resources: ["Fast.ai", "Deep Learning Specialization"]},
            {phase: "Specialization", duration: "2 months", skills: ["NLP/Computer Vision/Time Series"], resources: ["Hugging Face Course", "Coursera"]},
            {phase: "MLOps", duration: "1 month", skills: ["Model Deployment", "MLflow", "Docker"], resources: ["Made With ML", "MLOps Community"]}
        ]
    },
    devops: {
        title: "DevOps Engineer Roadmap",
        description: "Complete path to becoming a DevOps engineer",
        duration: "10-14 months",
        salary: "₹12-40 LPA",
        steps: [
            {phase: "Linux & Scripting", duration: "2 months", skills: ["Linux Administration", "Bash", "Python"], resources: ["Linux Journey", "Python Docs"]},
            {phase: "Version Control", duration: "2 weeks", skills: ["Git", "GitHub", "GitLab"], resources: ["Git Documentation", "GitHub Learning"]},
            {phase: "Containers", duration: "1 month", skills: ["Docker", "Docker Compose", "Container Security"], resources: ["Docker Docs", "KodeKloud"]},
            {phase: "CI/CD", duration: "1 month", skills: ["Jenkins", "GitHub Actions", "GitLab CI"], resources: ["Jenkins Docs", "GitHub Actions Docs"]},
            {phase: "Orchestration", duration: "2 months", skills: ["Kubernetes", "Helm", "Service Mesh"], resources: ["Kubernetes.io", "CKAD Course"]},
            {phase: "Infrastructure as Code", duration: "1 month", skills: ["Terraform", "Ansible", "CloudFormation"], resources: ["Terraform Docs", "Ansible Docs"]},
            {phase: "Cloud Platform", duration: "2 months", skills: ["AWS/GCP/Azure", "Certifications"], resources: ["Cloud Provider Docs", "A Cloud Guru"]},
            {phase: "Monitoring", duration: "1 month", skills: ["Prometheus", "Grafana", "ELK Stack"], resources: ["Prometheus Docs", "Grafana Tutorials"]}
        ]
    },
    ai_ml: {
        title: "AI/ML Engineer Roadmap",
        description: "Complete path to becoming an AI/ML engineer",
        duration: "14-20 months",
        salary: "₹15-50 LPA",
        steps: [
            {phase: "Mathematics", duration: "3 months", skills: ["Linear Algebra", "Calculus", "Statistics", "Optimization"], resources: ["3Blue1Brown", "Khan Academy"]},
            {phase: "Programming", duration: "2 months", skills: ["Python", "NumPy", "Pandas"], resources: ["Python.org", "Real Python"]},
            {phase: "Machine Learning", duration: "3 months", skills: ["Scikit-learn", "ML Algorithms", "Model Evaluation"], resources: ["Andrew Ng Course", "Kaggle"]},
            {phase: "Deep Learning", duration: "3 months", skills: ["PyTorch/TensorFlow", "CNNs", "RNNs", "Transformers"], resources: ["Fast.ai", "PyTorch Tutorials"]},
            {phase: "LLMs & Generative AI", duration: "2 months", skills: ["Transformers", "Fine-tuning", "RAG", "LangChain"], resources: ["Hugging Face", "OpenAI Docs"]},
            {phase: "MLOps", duration: "2 months", skills: ["Model Deployment", "MLflow", "Kubernetes"], resources: ["Made With ML", "MLOps Zoomcamp"]}
        ]
    },
    mobile: {
        title: "Mobile Developer Roadmap",
        description: "Complete path to becoming a mobile developer",
        duration: "8-12 months",
        salary: "₹8-30 LPA",
        steps: [
            {phase: "Programming Basics", duration: "2 months", skills: ["JavaScript/Dart/Kotlin/Swift"], resources: ["Dart.dev", "Swift.org"]},
            {phase: "Cross-platform Framework", duration: "3 months", skills: ["React Native/Flutter"], resources: ["React Native Docs", "Flutter.dev"]},
            {phase: "Native Development", duration: "2 months", skills: ["iOS (Swift)", "Android (Kotlin)"], resources: ["Apple Developer", "Android Developers"]},
            {phase: "State Management", duration: "1 month", skills: ["Redux/Provider/Riverpod"], resources: ["Redux Docs", "Provider Package"]},
            {phase: "Backend Integration", duration: "1 month", skills: ["REST APIs", "Firebase", "Authentication"], resources: ["Firebase Docs", "Supabase"]},
            {phase: "Publishing", duration: "2 weeks", skills: ["App Store", "Play Store", "CI/CD"], resources: ["Store Guidelines", "Fastlane"]}
        ]
    },
    security: {
        title: "Cybersecurity Engineer Roadmap",
        description: "Complete path to becoming a security engineer",
        duration: "12-18 months",
        salary: "₹10-40 LPA",
        steps: [
            {phase: "Networking Fundamentals", duration: "2 months", skills: ["TCP/IP", "DNS", "HTTP/HTTPS", "VPN"], resources: ["Cisco CCNA", "Network+"]},
            {phase: "Linux & Scripting", duration: "2 months", skills: ["Linux", "Bash", "Python"], resources: ["Linux Journey", "OverTheWire"]},
            {phase: "Security Fundamentals", duration: "2 months", skills: ["OWASP Top 10", "Cryptography", "Authentication"], resources: ["OWASP", "Crypto 101"]},
            {phase: "Ethical Hacking", duration: "3 months", skills: ["Penetration Testing", "Burp Suite", "Metasploit"], resources: ["HackTheBox", "TryHackMe"]},
            {phase: "Cloud Security", duration: "2 months", skills: ["AWS Security", "GCP Security", "Azure Security"], resources: ["Cloud Security Alliance", "AWS Security"]},
            {phase: "Certifications", duration: "2 months", skills: ["CEH", "Security+", "OSCP"], resources: ["CompTIA", "Offensive Security"]}
        ]
    },
    blockchain: {
        title: "Blockchain Developer Roadmap",
        description: "Complete path to becoming a blockchain developer",
        duration: "8-12 months",
        salary: "₹12-50 LPA",
        steps: [
            {phase: "Blockchain Basics", duration: "1 month", skills: ["How Blockchain Works", "Consensus", "Cryptography"], resources: ["Bitcoin Whitepaper", "Coursera"]},
            {phase: "Smart Contracts", duration: "2 months", skills: ["Solidity", "Ethereum", "EVM"], resources: ["CryptoZombies", "Solidity Docs"]},
            {phase: "DApp Development", duration: "2 months", skills: ["Web3.js", "Ethers.js", "Hardhat", "Truffle"], resources: ["Hardhat Docs", "Buildspace"]},
            {phase: "Frontend Integration", duration: "1 month", skills: ["React + Web3", "MetaMask", "WalletConnect"], resources: ["RainbowKit", "wagmi"]},
            {phase: "DeFi & NFTs", duration: "2 months", skills: ["DeFi Protocols", "NFT Standards", "IPFS"], resources: ["DeFi Pulse", "OpenZeppelin"]},
            {phase: "Security", duration: "1 month", skills: ["Smart Contract Security", "Auditing"], resources: ["Damn Vulnerable DeFi", "Ethernaut"]}
        ]
    },
    productManager: {
        title: "Product Manager Roadmap",
        description: "Complete path to becoming a product manager",
        duration: "6-12 months",
        salary: "₹15-50 LPA",
        steps: [
            {phase: "PM Fundamentals", duration: "1 month", skills: ["Product Thinking", "User Research", "Market Analysis"], resources: ["Inspired Book", "Product School"]},
            {phase: "User Experience", duration: "1 month", skills: ["UX Research", "Personas", "User Journeys"], resources: ["Nielsen Norman", "UX Design Course"]},
            {phase: "Strategy", duration: "1 month", skills: ["Product Strategy", "Roadmapping", "Prioritization"], resources: ["Product Strategy Book", "Reforge"]},
            {phase: "Analytics", duration: "1 month", skills: ["Metrics", "A/B Testing", "Data Analysis"], resources: ["Amplitude", "Mixpanel Academy"]},
            {phase: "Technical Skills", duration: "2 months", skills: ["SQL", "APIs", "System Design Basics"], resources: ["Mode Analytics", "API Guide"]},
            {phase: "Leadership", duration: "1 month", skills: ["Stakeholder Management", "Communication"], resources: ["Crucial Conversations", "PM Interview Prep"]}
        ]
    }
};

// ==================== REMOTE JOB PORTALS ====================
const REMOTE_JOB_PORTALS = {
    top_remote_first: [
        {name: 'We Work Remotely', url: 'https://weworkremotely.com', desc: 'Largest remote work community'},
        {name: 'FlexJobs', url: 'https://www.flexjobs.com', desc: 'Vetted remote & flexible jobs'},
        {name: 'Remotive', url: 'https://remotive.io', desc: 'Remote job board for developers'},
        {name: 'JustRemote', url: 'https://justremote.co', desc: 'Remote jobs across industries'},
        {name: 'Working Nomads', url: 'https://www.workingnomads.co/jobs', desc: 'Curated remote jobs for digital nomads'},
        {name: 'Jobspresso', url: 'https://jobspresso.co', desc: 'Expertly curated remote jobs'},
        {name: 'Remote OK', url: 'https://remoteok.com', desc: 'Remote jobs aggregator'},
        {name: 'Pangian', url: 'https://pangian.com', desc: 'Remote job community'},
        {name: 'Virtual Vocations', url: 'https://www.virtualvocations.com', desc: 'Telecommute jobs database'},
        {name: 'SkipTheDrive', url: 'https://www.skipthedrive.com', desc: 'Remote and work from home jobs'}
    ],
    india_focused: [
        {name: 'Himalayas', url: 'https://himalayas.app', desc: 'Remote-first global jobs'},
        {name: 'Remote Rocketship', url: 'https://remoterocketship.com', desc: 'Curated remote roles'},
        {name: 'Jooble India', url: 'https://in.jooble.org', desc: 'Job search aggregator'},
        {name: 'Internshala', url: 'https://internshala.com', desc: 'Internships & entry-level roles'},
        {name: 'Apna', url: 'https://apna.co', desc: 'India-focused jobs & remote roles'}
    ],
    tech_focused: [
        {name: 'Outsourcely', url: 'https://www.outsourcely.com', desc: 'Startups hiring remote workers'},
        {name: 'Remote4Me', url: 'https://remote4.me/', desc: 'Remote tech jobs'},
        {name: 'Hubstaff Talent', url: 'https://talent.hubstaff.com', desc: 'Free remote talent platform'},
        {name: 'EuropeRemotely', url: 'https://europeremotely.com', desc: 'Remote jobs in Europe timezone'},
        {name: 'RemoteHub', url: 'https://www.remotehub.com', desc: 'Remote work community'},
        {name: 'RemoteWoman', url: 'https://remotewoman.com', desc: 'Remote jobs for women in tech'},
        {name: 'RemoteBase', url: 'https://remotebase.com', desc: 'Silicon Valley jobs, remotely'},
        {name: 'RemoteTechJobs', url: 'https://remotetechjobs.com', desc: 'Tech-specific remote roles'},
        {name: 'DailyRemote', url: 'https://dailyremote.com', desc: 'Daily updated remote jobs'},
        {name: 'NoDesk', url: 'https://nodesk.co', desc: 'Remote work resources'}
    ],
    startup_focused: [
        {name: 'AngelList / Wellfound', url: 'https://wellfound.com', desc: 'Startup jobs platform'},
        {name: 'PowerToFly', url: 'https://powertofly.com', desc: 'Diverse & inclusive remote jobs'},
        {name: 'Toptal', url: 'https://www.toptal.com', desc: 'Top 3% freelance talent'},
        {name: 'LinkedIn Remote', url: 'https://www.linkedin.com/jobs/remote-jobs/', desc: 'LinkedIn remote filter'},
        {name: 'Indeed Remote', url: 'https://in.indeed.com', desc: 'Indeed with remote filter'}
    ]
};

// ==================== SQL LEARNING RESOURCES ====================
const SQL_RESOURCES = {
    quick_mastery: [
        {name: '50 SQL Questions in 2 Hours', url: 'https://lnkd.in/e8tEXMb9', type: 'Video', desc: 'Ultimate Interview Practice'},
        {name: 'SQL for Data Analysis in 2 Hours', url: 'https://lnkd.in/g-jDN9TV', type: 'Video', desc: 'With dataset + 50 queries'},
        {name: 'Complex SQL Queries Guide', url: 'https://lnkd.in/effnhz6P', type: 'Article', desc: 'Step-by-Step for Real Reports'}
    ],
    portfolio_projects: [
        {name: 'Retail Analytics with Superstore', url: 'https://lnkd.in/ebypRkxz', stack: 'AWS S3, Glue, Athena, QuickSight'},
        {name: 'End-to-End ETL Analytics', url: 'https://lnkd.in/eJy8WNGz', stack: 'SQL, Python'},
        {name: 'Netflix Data Cleaning & ELT', url: 'https://lnkd.in/eiP3SKCn', stack: 'Python, SQL'},
        {name: 'SQL Portfolio Project', url: 'https://lnkd.in/eXn82pEd', stack: 'SQL'},
        {name: 'Yelp Business Review Analysis', url: 'https://lnkd.in/eex2k9aR', stack: 'S3, Python, Snowflake, SQL'},
        {name: 'Food Delivery Insights', url: 'https://lnkd.in/ev4pDVU9', stack: 'Advanced SQL'}
    ],
    playlists: [
        {name: 'SQL Tips and Tricks', url: 'https://lnkd.in/gK_qsy2M'},
        {name: 'SQL Medium-Complex Problems', url: 'https://lnkd.in/gj3pFXcP'},
        {name: 'Leetcode SQL Hard Problems', url: 'https://lnkd.in/gHJdu5Cw'},
        {name: 'Complex SQL Interview Questions', url: 'https://lnkd.in/g_4uyzHT'}
    ]
};

// ==================== DATABRICKS RESOURCES ====================
const DATABRICKS_RESOURCES = [
    {name: 'Delta Lake Internals', url: 'https://lnkd.in/gFzStZM6'},
    {name: 'Cluster Management & Autoscaling', url: 'https://lnkd.in/g6sJvutG'},
    {name: 'Structured Streaming', url: 'https://lnkd.in/gfVM-f2a'},
    {name: 'Performance Tuning & Caching', url: 'https://lnkd.in/g-f2qN3U'},
    {name: 'Unity Catalog & Access Control', url: 'https://lnkd.in/gwja8apn'},
    {name: 'Jobs API & Workflows', url: 'https://lnkd.in/gF6Q67vM'},
    {name: 'Delta Live Tables (DLT)', url: 'https://lnkd.in/gscqV3Qg'},
    {name: 'Photon & Runtime Optimizations', url: 'https://lnkd.in/g6gQqitK'},
    {name: 'Delta Change Data Feed (CDF)', url: 'https://lnkd.in/giBZKUXh'},
    {name: 'Lakehouse ETL Design Patterns', url: 'https://lnkd.in/gmyMpVpT'}
];

// ==================== AZURE DATA ENGINEERING ====================
const AZURE_DATA_ENGINEERING = {
    description: 'End-to-End Azure Data Engineering Project Guide',
    components: [
        {name: 'Data Lake Storage (ADLS Gen2)', desc: 'Central scalable repository using Medallion Architecture (Bronze, Silver, Gold)'},
        {name: 'Azure Data Factory', desc: 'Cloud ETL/ELT service for pipeline orchestration'},
        {name: 'Azure Databricks', desc: 'Apache Spark platform for data processing with PySpark'},
        {name: 'Azure Synapse Analytics', desc: 'Unified analytics for data warehousing and big data'},
        {name: 'Power BI', desc: 'Business Intelligence for dashboards and reports'},
        {name: 'Azure Key Vault', desc: 'Secure storage for credentials and secrets'}
    ],
    steps: [
        {phase: 'Resource Setup', desc: 'Create Resource Group, Storage Account with Bronze/Silver/Gold containers'},
        {phase: 'Data Ingestion', desc: 'Use ADF to copy raw data from sources to Bronze layer'},
        {phase: 'Data Transformation', desc: 'Use Databricks/PySpark to clean data and move to Silver/Gold'},
        {phase: 'Data Warehousing', desc: 'Load Gold layer data into Synapse for optimized querying'},
        {phase: 'Reporting', desc: 'Connect Power BI to Gold layer for dashboards'},
        {phase: 'Automation', desc: 'Set up ADF triggers for scheduled runs'}
    ]
};

// ==================== AI AGENTS GITHUB REPOS ====================
const AI_AGENTS_REPOS = [
    {name: 'Hands-On Large Language Models', url: 'https://lnkd.in/dxaVF86w', desc: 'Complete code notebooks from basics to advanced LLM fine-tuning'},
    {name: 'AI Agents for Beginners', url: 'https://lnkd.in/dHvTmJnv', desc: 'Free 11-part intro course for building AI agents'},
    {name: 'GenAI Agents', url: 'https://lnkd.in/dEt72MEy', desc: 'Tutorials for building generative AI agents'},
    {name: 'Made with ML', url: 'https://lnkd.in/d2dMACMj', desc: 'Design, build, deploy production ML apps'},
    {name: 'Prompt Engineering Guide', url: 'https://lnkd.in/dBUCsVJ8', desc: 'Resources to master writing effective AI prompts'},
    {name: 'Hands-On AI Engineering', url: 'https://lnkd.in/dgQtRyk7', desc: 'Practical LLM-powered apps and agent solutions'},
    {name: 'Awesome Generative AI Guide', url: 'https://lnkd.in/dJ8gxp3a', desc: 'Curated hub for GenAI research and tools'},
    {name: 'Designing ML Systems', url: 'https://lnkd.in/dEx8sQJK', desc: 'Based on Designing ML Systems book'},
    {name: 'ML for Beginners (Microsoft)', url: 'https://lnkd.in/dBj3BAEY', desc: 'Free beginner-friendly ML intro by Microsoft'},
    {name: 'LLM Course', url: 'https://lnkd.in/diZgGACG', desc: 'Hands-on course for designing LLM apps'}
];

// ==================== HIRING AGENCIES ====================
const HIRING_AGENCIES = [
    {name: 'Robert Half', url: 'https://roberthalf.com', global: true},
    {name: 'Adecco', url: 'https://adecco.com', global: true},
    {name: 'Randstad', url: 'https://randstad.com', global: true},
    {name: 'Kelly Services', url: 'https://kellyservices.com', global: true},
    {name: 'ManpowerGroup', url: 'https://manpowergroup.com', global: true},
    {name: 'Aerotek', url: 'https://aerotek.com', global: true},
    {name: 'Korn Ferry', url: 'https://kornferry.com', global: true},
    {name: 'Kforce', url: 'https://kforce.com', global: true},
    {name: 'Michael Page', url: 'https://michaelpage.com', global: true},
    {name: 'Allegis Group', url: 'https://allegisgroup.com', global: true},
    {name: 'TEKsystems', url: 'https://teksystems.com', global: true},
    {name: 'AppleOne', url: 'https://appleone.com', global: true},
    {name: 'Insight Global', url: 'https://insightglobal.com', global: true},
    {name: 'Beacon Hill Staffing', url: 'https://beaconhillstaffing.com', global: true}
];

// Export
if (typeof window !== 'undefined') {
    window.LEARNING_RESOURCES = LEARNING_RESOURCES;
    window.CAREER_ROADMAPS = CAREER_ROADMAPS;
    window.REMOTE_JOB_PORTALS = REMOTE_JOB_PORTALS;
    window.SQL_RESOURCES = SQL_RESOURCES;
    window.DATABRICKS_RESOURCES = DATABRICKS_RESOURCES;
    window.AZURE_DATA_ENGINEERING = AZURE_DATA_ENGINEERING;
    window.AI_AGENTS_REPOS = AI_AGENTS_REPOS;
    window.HIRING_AGENCIES = HIRING_AGENCIES;
}


