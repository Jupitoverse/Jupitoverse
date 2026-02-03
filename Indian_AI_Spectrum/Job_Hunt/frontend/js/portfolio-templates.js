/**
 * CareerLaunch - Portfolio Templates Engine
 * Amazing, professional portfolio templates with animations
 */

const PortfolioTemplates = {
    // Template configurations
    templates: {
        'developer-dark': {
            name: 'Developer Dark',
            generator: generateDeveloperDark,
            colorSchemes: {
                'purple-night': { primary: '#6366f1', secondary: '#8b5cf6', bg: '#0f0f23', text: '#ffffff' },
                'cyber-green': { primary: '#10b981', secondary: '#34d399', bg: '#0d1117', text: '#ffffff' },
                'ocean-blue': { primary: '#3b82f6', secondary: '#60a5fa', bg: '#0a0a1a', text: '#ffffff' }
            }
        },
        'minimal-light': {
            name: 'Minimal Light',
            generator: generateMinimalLight,
            colorSchemes: {
                'classic': { primary: '#2563eb', secondary: '#3b82f6', bg: '#ffffff', text: '#1f2937' },
                'warm': { primary: '#d97706', secondary: '#f59e0b', bg: '#fffbeb', text: '#1f2937' }
            }
        },
        'gradient-modern': {
            name: 'Gradient Modern',
            generator: generateGradientModern,
            colorSchemes: {
                'purple-sunset': { primary: '#667eea', secondary: '#764ba2', bg: 'linear-gradient(135deg, #667eea, #764ba2)' },
                'ocean-breeze': { primary: '#4facfe', secondary: '#00f2fe', bg: 'linear-gradient(135deg, #4facfe, #00f2fe)' }
            }
        },
        'terminal-style': {
            name: 'Terminal Style',
            generator: generateTerminalStyle,
            colorSchemes: {
                'matrix': { primary: '#00ff00', secondary: '#00cc00', bg: '#0c0c0c', text: '#00ff00' },
                'amber': { primary: '#ffb000', secondary: '#ff8c00', bg: '#1a1a1a', text: '#ffb000' }
            }
        },
        'glassmorphism': {
            name: 'Glassmorphism',
            generator: generateGlassmorphism,
            colorSchemes: {
                'aurora': { primary: '#a855f7', secondary: '#3b82f6', bg: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)' }
            }
        },
        'creative': {
            name: 'Creative Portfolio',
            generator: generateCreative,
            colorSchemes: {
                'vibrant': { primary: '#ff6b6b', secondary: '#feca57', bg: '#ffffff', accent: '#5f27cd' }
            }
        }
    },

    generate(templateId, profileData, colorScheme = null) {
        const template = this.templates[templateId];
        if (!template) {
            console.error('Template not found:', templateId);
            return '';
        }
        const scheme = colorScheme ? template.colorSchemes[colorScheme] : Object.values(template.colorSchemes)[0];
        return template.generator(profileData, scheme);
    }
};

// ==================== DEVELOPER DARK TEMPLATE ====================
function generateDeveloperDark(profile, colors) {
    const p = profile;
    const fullName = `${p.basic?.firstName || 'Your'} ${p.basic?.lastName || 'Name'}`;
    const initials = (p.basic?.firstName?.charAt(0) || 'U') + (p.basic?.lastName?.charAt(0) || '');
    
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${fullName} - Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: ${colors.primary};
            --secondary: ${colors.secondary};
            --bg: ${colors.bg};
            --text: ${colors.text};
            --card-bg: rgba(255,255,255,0.03);
            --border: rgba(255,255,255,0.1);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
            overflow-x: hidden;
        }
        
        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: -1;
            overflow: hidden;
        }
        
        .bg-animation::before {
            content: '';
            position: absolute;
            width: 150%;
            height: 150%;
            background: radial-gradient(ellipse at 20% 80%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
                        radial-gradient(ellipse at 80% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
                        radial-gradient(ellipse at 50% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
            animation: float 20s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(-10%, -10%) rotate(0deg); }
            33% { transform: translate(0%, -5%) rotate(5deg); }
            66% { transform: translate(-5%, 0%) rotate(-5deg); }
        }
        
        /* Container */
        .container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }
        
        /* Header */
        .header {
            position: fixed;
            top: 0; left: 0; right: 0;
            padding: 20px 0;
            background: rgba(15, 15, 35, 0.8);
            backdrop-filter: blur(20px);
            z-index: 100;
            border-bottom: 1px solid var(--border);
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav { display: flex; gap: 32px; }
        
        .nav a {
            color: rgba(255,255,255,0.7);
            text-decoration: none;
            font-size: 0.95rem;
            transition: all 0.3s;
            position: relative;
        }
        
        .nav a:hover { color: white; }
        
        .nav a::after {
            content: '';
            position: absolute;
            bottom: -4px; left: 0;
            width: 0; height: 2px;
            background: var(--primary);
            transition: width 0.3s;
        }
        
        .nav a:hover::after { width: 100%; }
        
        /* Hero Section */
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            padding-top: 80px;
        }
        
        .hero-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }
        
        .hero-text h1 {
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 16px;
        }
        
        .hero-text h1 span {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero-tagline {
            font-size: 1.3rem;
            color: rgba(255,255,255,0.7);
            margin-bottom: 24px;
        }
        
        .hero-bio {
            color: rgba(255,255,255,0.6);
            margin-bottom: 32px;
            font-size: 1.05rem;
        }
        
        .hero-cta { display: flex; gap: 16px; }
        
        .btn {
            padding: 14px 32px;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            box-shadow: 0 10px 40px rgba(99, 102, 241, 0.4);
        }
        
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 50px rgba(99, 102, 241, 0.5);
        }
        
        .btn-outline {
            border: 2px solid rgba(255,255,255,0.3);
            color: white;
        }
        
        .btn-outline:hover {
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.1);
        }
        
        /* Avatar */
        .hero-visual {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .avatar-container {
            position: relative;
            width: 350px;
            height: 350px;
        }
        
        .avatar-ring {
            position: absolute;
            inset: 0;
            border: 3px solid transparent;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--secondary)) border-box;
            -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            animation: rotate 10s linear infinite;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .avatar {
            position: absolute;
            inset: 15px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 6rem;
            font-weight: 800;
            color: white;
            box-shadow: 0 20px 60px rgba(99, 102, 241, 0.4);
        }
        
        /* Section */
        .section {
            padding: 100px 0;
        }
        
        .section-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 48px;
            position: relative;
            display: inline-block;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            bottom: -12px; left: 0;
            width: 60px; height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 2px;
        }
        
        /* Skills */
        .skills-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }
        
        .skill-tag {
            padding: 10px 24px;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 50px;
            font-size: 0.95rem;
            transition: all 0.3s;
        }
        
        .skill-tag:hover {
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.1);
            transform: translateY(-3px);
        }
        
        /* Experience/Projects Cards */
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 24px;
        }
        
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 32px;
            transition: all 0.4s;
            position: relative;
            overflow: hidden;
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.4s;
        }
        
        .card:hover::before { transform: scaleX(1); }
        
        .card:hover {
            transform: translateY(-8px);
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        
        .card-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .card-subtitle {
            color: var(--primary);
            font-weight: 500;
            margin-bottom: 8px;
        }
        
        .card-meta {
            color: rgba(255,255,255,0.5);
            font-size: 0.9rem;
            margin-bottom: 16px;
        }
        
        .card-desc {
            color: rgba(255,255,255,0.7);
            font-size: 0.95rem;
            line-height: 1.7;
        }
        
        .card-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 20px;
        }
        
        .card-tag {
            padding: 4px 12px;
            background: rgba(99, 102, 241, 0.15);
            border-radius: 20px;
            font-size: 0.8rem;
            color: var(--primary);
        }
        
        /* Social Links */
        .social-links {
            display: flex;
            gap: 16px;
            margin-top: 32px;
        }
        
        .social-link {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--card-bg);
            border: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
            transition: all 0.3s;
        }
        
        .social-link:hover {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-color: transparent;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
        }
        
        /* Footer */
        .footer {
            padding: 40px 0;
            border-top: 1px solid var(--border);
            text-align: center;
            color: rgba(255,255,255,0.5);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero-content { grid-template-columns: 1fr; text-align: center; }
            .hero-text h1 { font-size: 2.5rem; }
            .avatar-container { width: 250px; height: 250px; }
            .avatar { font-size: 4rem; }
            .nav { display: none; }
        }
        
        /* Animations */
        .animate-in {
            opacity: 0;
            transform: translateY(30px);
            animation: animateIn 0.6s ease forwards;
        }
        
        @keyframes animateIn {
            to { opacity: 1; transform: translateY(0); }
        }
        
        .delay-1 { animation-delay: 0.1s; }
        .delay-2 { animation-delay: 0.2s; }
        .delay-3 { animation-delay: 0.3s; }
        .delay-4 { animation-delay: 0.4s; }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo">&lt;${initials}/&gt;</div>
                <nav class="nav">
                    <a href="#about">About</a>
                    <a href="#skills">Skills</a>
                    <a href="#experience">Experience</a>
                    <a href="#projects">Projects</a>
                    <a href="#contact">Contact</a>
                </nav>
            </div>
        </div>
    </header>
    
    <section class="hero" id="about">
        <div class="container">
            <div class="hero-content">
                <div class="hero-text">
                    <h1 class="animate-in">Hi, I'm <span>${fullName}</span></h1>
                    <p class="hero-tagline animate-in delay-1">${p.basic?.headline || 'Software Developer'}</p>
                    <p class="hero-bio animate-in delay-2">${p.basic?.bio || 'Passionate about building amazing software and solving complex problems.'}</p>
                    <div class="hero-cta animate-in delay-3">
                        <a href="#contact" class="btn btn-primary"><i class="fas fa-paper-plane"></i> Get in Touch</a>
                        <a href="#projects" class="btn btn-outline"><i class="fas fa-code"></i> View Work</a>
                    </div>
                    <div class="social-links animate-in delay-4">
                        ${p.social?.linkedin ? `<a href="${p.social.linkedin}" class="social-link" target="_blank"><i class="fab fa-linkedin-in"></i></a>` : ''}
                        ${p.social?.github ? `<a href="${p.social.github}" class="social-link" target="_blank"><i class="fab fa-github"></i></a>` : ''}
                        ${p.social?.twitter ? `<a href="${p.social.twitter}" class="social-link" target="_blank"><i class="fab fa-twitter"></i></a>` : ''}
                        <a href="mailto:${p.basic?.email || ''}" class="social-link"><i class="fas fa-envelope"></i></a>
                    </div>
                </div>
                <div class="hero-visual animate-in delay-2">
                    <div class="avatar-container">
                        <div class="avatar-ring"></div>
                        <div class="avatar">${initials}</div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    ${p.skills?.length > 0 ? `
    <section class="section" id="skills">
        <div class="container">
            <h2 class="section-title">Skills & Technologies</h2>
            <div class="skills-grid">
                ${p.skills.map((skill, i) => `<span class="skill-tag animate-in" style="animation-delay: ${i * 0.05}s">${skill}</span>`).join('')}
            </div>
        </div>
    </section>
    ` : ''}
    
    ${p.experience?.length > 0 ? `
    <section class="section" id="experience">
        <div class="container">
            <h2 class="section-title">Experience</h2>
            <div class="card-grid">
                ${p.experience.map((exp, i) => `
                    <div class="card animate-in" style="animation-delay: ${i * 0.1}s">
                        <h3 class="card-title">${exp.title}</h3>
                        <div class="card-subtitle">${exp.company}</div>
                        <div class="card-meta">${exp.startDate} - ${exp.endDate} ${exp.location ? '• ' + exp.location : ''}</div>
                        <p class="card-desc">${exp.description || ''}</p>
                        ${exp.techStack ? `
                            <div class="card-tags">
                                ${exp.techStack.split(',').map(t => `<span class="card-tag">${t.trim()}</span>`).join('')}
                            </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>
        </div>
    </section>
    ` : ''}
    
    ${p.projects?.length > 0 ? `
    <section class="section" id="projects">
        <div class="container">
            <h2 class="section-title">Projects</h2>
            <div class="card-grid">
                ${p.projects.map((proj, i) => `
                    <div class="card animate-in" style="animation-delay: ${i * 0.1}s">
                        <h3 class="card-title">${proj.name}</h3>
                        <p class="card-desc">${proj.description || ''}</p>
                        ${proj.techStack ? `
                            <div class="card-tags">
                                ${proj.techStack.split(',').map(t => `<span class="card-tag">${t.trim()}</span>`).join('')}
                            </div>
                        ` : ''}
                        <div style="margin-top: 20px; display: flex; gap: 12px;">
                            ${proj.url ? `<a href="${proj.url}" target="_blank" class="btn btn-outline" style="padding: 8px 16px; font-size: 0.85rem;"><i class="fas fa-external-link-alt"></i> Live</a>` : ''}
                            ${proj.github ? `<a href="${proj.github}" target="_blank" class="btn btn-outline" style="padding: 8px 16px; font-size: 0.85rem;"><i class="fab fa-github"></i> Code</a>` : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    </section>
    ` : ''}
    
    <section class="section" id="contact">
        <div class="container" style="text-align: center;">
            <h2 class="section-title" style="display: block; text-align: center;">Let's Connect</h2>
            <p style="color: rgba(255,255,255,0.6); max-width: 600px; margin: 0 auto 32px;">
                I'm always open to discussing new opportunities, collaborations, or just having a chat about technology.
            </p>
            <a href="mailto:${p.basic?.email || ''}" class="btn btn-primary btn-lg">
                <i class="fas fa-envelope"></i> Say Hello
            </a>
        </div>
    </section>
    
    <footer class="footer">
        <div class="container">
            <p>© ${new Date().getFullYear()} ${fullName}. Built with CareerLaunch.</p>
        </div>
    </footer>
    
    <script>
        // Smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
            });
        });
        
        // Animate on scroll
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                }
            });
        }, { threshold: 0.1 });
        
        document.querySelectorAll('.animate-in').forEach(el => {
            el.style.animationPlayState = 'paused';
            observer.observe(el);
        });
    </script>
</body>
</html>`;
}

// ==================== MINIMAL LIGHT TEMPLATE ====================
function generateMinimalLight(profile, colors) {
    const p = profile;
    const fullName = `${p.basic?.firstName || 'Your'} ${p.basic?.lastName || 'Name'}`;
    
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${fullName} - Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: ${colors.primary};
            --bg: ${colors.bg};
            --text: ${colors.text};
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.8;
        }
        
        .container { max-width: 900px; margin: 0 auto; padding: 80px 24px; }
        
        h1, h2, h3 { font-family: 'Playfair Display', serif; font-weight: 600; }
        
        .hero { text-align: center; padding: 60px 0 80px; }
        
        .hero h1 { font-size: 3.5rem; margin-bottom: 16px; letter-spacing: -1px; }
        .hero-tagline { font-size: 1.3rem; color: #6b7280; margin-bottom: 24px; }
        .hero-bio { max-width: 600px; margin: 0 auto 32px; color: #4b5563; }
        
        .social-links { display: flex; justify-content: center; gap: 20px; }
        .social-link {
            color: #9ca3af;
            font-size: 1.5rem;
            transition: all 0.3s;
        }
        .social-link:hover { color: var(--primary); transform: translateY(-3px); }
        
        .section { padding: 60px 0; border-top: 1px solid #e5e7eb; }
        .section-title { font-size: 2rem; margin-bottom: 32px; }
        
        .skills-grid { display: flex; flex-wrap: wrap; gap: 12px; }
        .skill-tag {
            padding: 8px 20px;
            background: #f3f4f6;
            border-radius: 50px;
            font-size: 0.9rem;
            color: #4b5563;
            transition: all 0.3s;
        }
        .skill-tag:hover { background: var(--primary); color: white; }
        
        .timeline { position: relative; padding-left: 30px; }
        .timeline::before {
            content: '';
            position: absolute;
            left: 0; top: 8px; bottom: 8px;
            width: 2px;
            background: #e5e7eb;
        }
        
        .timeline-item {
            position: relative;
            padding-bottom: 40px;
        }
        
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -34px; top: 8px;
            width: 10px; height: 10px;
            background: var(--primary);
            border-radius: 50%;
        }
        
        .timeline-title { font-size: 1.25rem; margin-bottom: 4px; }
        .timeline-subtitle { color: var(--primary); font-weight: 500; margin-bottom: 4px; }
        .timeline-meta { color: #9ca3af; font-size: 0.9rem; margin-bottom: 12px; }
        .timeline-desc { color: #6b7280; }
        
        .project-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 32px; }
        .project-card {
            padding: 24px;
            background: #f9fafb;
            border-radius: 12px;
            transition: all 0.3s;
        }
        .project-card:hover { transform: translateY(-4px); box-shadow: 0 10px 40px rgba(0,0,0,0.08); }
        .project-name { font-size: 1.2rem; margin-bottom: 8px; }
        .project-desc { color: #6b7280; font-size: 0.95rem; margin-bottom: 16px; }
        
        .project-links a {
            color: var(--primary);
            text-decoration: none;
            font-size: 0.9rem;
            margin-right: 16px;
        }
        .project-links a:hover { text-decoration: underline; }
        
        .footer { text-align: center; padding: 40px 0; color: #9ca3af; font-size: 0.9rem; }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.5rem; }
            .project-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <section class="hero">
            <h1>${fullName}</h1>
            <p class="hero-tagline">${p.basic?.headline || 'Software Developer'}</p>
            <p class="hero-bio">${p.basic?.bio || ''}</p>
            <div class="social-links">
                ${p.social?.linkedin ? `<a href="${p.social.linkedin}" class="social-link"><i class="fab fa-linkedin"></i></a>` : ''}
                ${p.social?.github ? `<a href="${p.social.github}" class="social-link"><i class="fab fa-github"></i></a>` : ''}
                ${p.social?.twitter ? `<a href="${p.social.twitter}" class="social-link"><i class="fab fa-twitter"></i></a>` : ''}
                <a href="mailto:${p.basic?.email || ''}" class="social-link"><i class="fas fa-envelope"></i></a>
            </div>
        </section>
        
        ${p.skills?.length > 0 ? `
        <section class="section">
            <h2 class="section-title">Skills</h2>
            <div class="skills-grid">
                ${p.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
            </div>
        </section>
        ` : ''}
        
        ${p.experience?.length > 0 ? `
        <section class="section">
            <h2 class="section-title">Experience</h2>
            <div class="timeline">
                ${p.experience.map(exp => `
                    <div class="timeline-item">
                        <h3 class="timeline-title">${exp.title}</h3>
                        <div class="timeline-subtitle">${exp.company}</div>
                        <div class="timeline-meta">${exp.startDate} - ${exp.endDate}</div>
                        <p class="timeline-desc">${exp.description || ''}</p>
                    </div>
                `).join('')}
            </div>
        </section>
        ` : ''}
        
        ${p.projects?.length > 0 ? `
        <section class="section">
            <h2 class="section-title">Projects</h2>
            <div class="project-grid">
                ${p.projects.map(proj => `
                    <div class="project-card">
                        <h3 class="project-name">${proj.name}</h3>
                        <p class="project-desc">${proj.description || ''}</p>
                        <div class="project-links">
                            ${proj.url ? `<a href="${proj.url}" target="_blank"><i class="fas fa-external-link-alt"></i> Live</a>` : ''}
                            ${proj.github ? `<a href="${proj.github}" target="_blank"><i class="fab fa-github"></i> Code</a>` : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        </section>
        ` : ''}
        
        <footer class="footer">
            <p>© ${new Date().getFullYear()} ${fullName}</p>
        </footer>
    </div>
</body>
</html>`;
}

// ==================== GRADIENT MODERN TEMPLATE ====================
function generateGradientModern(profile, colors) {
    const p = profile;
    const fullName = `${p.basic?.firstName || 'Your'} ${p.basic?.lastName || 'Name'}`;
    const initials = (p.basic?.firstName?.charAt(0) || 'U') + (p.basic?.lastName?.charAt(0) || '');
    
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${fullName} - Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: ${colors.bg};
            min-height: 100vh;
            color: white;
        }
        
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 40px;
            position: relative;
            overflow: hidden;
        }
        
        .hero::before {
            content: '';
            position: absolute;
            width: 500px; height: 500px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            top: -100px; right: -100px;
            animation: pulse 4s ease-in-out infinite;
        }
        
        .hero::after {
            content: '';
            position: absolute;
            width: 300px; height: 300px;
            background: rgba(255,255,255,0.08);
            border-radius: 50%;
            bottom: -50px; left: -50px;
            animation: pulse 4s ease-in-out infinite reverse;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        
        .hero-content { position: relative; z-index: 1; max-width: 800px; }
        
        .avatar {
            width: 180px; height: 180px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            margin: 0 auto 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            font-weight: 800;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }
        
        .hero h1 { font-size: 4rem; font-weight: 800; margin-bottom: 16px; }
        .hero-tagline { font-size: 1.5rem; opacity: 0.9; margin-bottom: 24px; }
        .hero-bio { font-size: 1.1rem; opacity: 0.8; max-width: 600px; margin: 0 auto 40px; }
        
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 16px 40px;
            background: rgba(255,255,255,0.2);
            border: none;
            border-radius: 50px;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            text-decoration: none;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
            margin: 0 8px;
        }
        
        .btn:hover {
            background: white;
            color: ${colors.primary};
            transform: translateY(-3px);
        }
        
        .section {
            padding: 80px 40px;
            max-width: 1100px;
            margin: 0 auto;
        }
        
        .section-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 40px;
            text-align: center;
        }
        
        .skills-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 12px;
        }
        
        .skill-tag {
            padding: 12px 28px;
            background: rgba(255,255,255,0.15);
            border-radius: 50px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }
        
        .skill-tag:hover {
            background: rgba(255,255,255,0.3);
            transform: scale(1.05);
        }
        
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
        }
        
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 32px;
            transition: all 0.3s;
        }
        
        .card:hover {
            transform: translateY(-8px);
            background: rgba(255,255,255,0.15);
        }
        
        .card-title { font-size: 1.3rem; font-weight: 600; margin-bottom: 8px; }
        .card-subtitle { opacity: 0.9; margin-bottom: 12px; }
        .card-desc { opacity: 0.8; font-size: 0.95rem; }
        
        .social-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 32px;
        }
        
        .social-link {
            width: 50px; height: 50px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.3rem;
            transition: all 0.3s;
        }
        
        .social-link:hover {
            background: white;
            color: ${colors.primary};
            transform: translateY(-5px);
        }
        
        .footer {
            text-align: center;
            padding: 40px;
            opacity: 0.7;
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.5rem; }
        }
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-content">
            <div class="avatar">${initials}</div>
            <h1>${fullName}</h1>
            <p class="hero-tagline">${p.basic?.headline || 'Software Developer'}</p>
            <p class="hero-bio">${p.basic?.bio || ''}</p>
            <div>
                <a href="mailto:${p.basic?.email || ''}" class="btn"><i class="fas fa-envelope"></i> Contact Me</a>
                ${p.social?.github ? `<a href="${p.social.github}" class="btn" target="_blank"><i class="fab fa-github"></i> GitHub</a>` : ''}
            </div>
            <div class="social-links">
                ${p.social?.linkedin ? `<a href="${p.social.linkedin}" class="social-link" target="_blank"><i class="fab fa-linkedin-in"></i></a>` : ''}
                ${p.social?.twitter ? `<a href="${p.social.twitter}" class="social-link" target="_blank"><i class="fab fa-twitter"></i></a>` : ''}
            </div>
        </div>
    </section>
    
    ${p.skills?.length > 0 ? `
    <section class="section">
        <h2 class="section-title">Skills</h2>
        <div class="skills-grid">
            ${p.skills.map(s => `<span class="skill-tag">${s}</span>`).join('')}
        </div>
    </section>
    ` : ''}
    
    ${p.experience?.length > 0 ? `
    <section class="section">
        <h2 class="section-title">Experience</h2>
        <div class="card-grid">
            ${p.experience.map(exp => `
                <div class="card">
                    <h3 class="card-title">${exp.title}</h3>
                    <div class="card-subtitle">${exp.company} • ${exp.startDate} - ${exp.endDate}</div>
                    <p class="card-desc">${exp.description || ''}</p>
                </div>
            `).join('')}
        </div>
    </section>
    ` : ''}
    
    ${p.projects?.length > 0 ? `
    <section class="section">
        <h2 class="section-title">Projects</h2>
        <div class="card-grid">
            ${p.projects.map(proj => `
                <div class="card">
                    <h3 class="card-title">${proj.name}</h3>
                    <p class="card-desc">${proj.description || ''}</p>
                </div>
            `).join('')}
        </div>
    </section>
    ` : ''}
    
    <footer class="footer">
        <p>© ${new Date().getFullYear()} ${fullName}</p>
    </footer>
</body>
</html>`;
}

// ==================== TERMINAL STYLE TEMPLATE ====================
function generateTerminalStyle(profile, colors) {
    const p = profile;
    const fullName = `${p.basic?.firstName || 'Your'} ${p.basic?.lastName || 'Name'}`;
    const username = (p.basic?.firstName || 'user').toLowerCase();
    
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${fullName} - Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'JetBrains Mono', monospace;
            background: ${colors.bg};
            color: ${colors.text};
            min-height: 100vh;
            padding: 40px;
            line-height: 1.8;
        }
        
        .terminal {
            max-width: 900px;
            margin: 0 auto;
            background: #1a1a1a;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 20px 80px rgba(0,0,0,0.5);
        }
        
        .terminal-header {
            background: #2d2d2d;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .terminal-btn {
            width: 14px; height: 14px;
            border-radius: 50%;
        }
        
        .terminal-btn.red { background: #ff5f56; }
        .terminal-btn.yellow { background: #ffbd2e; }
        .terminal-btn.green { background: #27ca3f; }
        
        .terminal-title {
            flex: 1;
            text-align: center;
            color: #888;
            font-size: 0.85rem;
        }
        
        .terminal-body {
            padding: 32px;
            font-size: 0.95rem;
        }
        
        .prompt {
            color: ${colors.primary};
        }
        
        .command {
            color: white;
        }
        
        .output {
            color: ${colors.text};
            padding-left: 20px;
            margin: 16px 0;
        }
        
        .output-section {
            margin: 32px 0;
        }
        
        .output-title {
            color: ${colors.secondary};
            margin-bottom: 12px;
        }
        
        .link {
            color: ${colors.primary};
            text-decoration: none;
        }
        
        .link:hover {
            text-decoration: underline;
        }
        
        .cursor {
            display: inline-block;
            width: 10px;
            height: 20px;
            background: ${colors.primary};
            animation: blink 1s infinite;
            margin-left: 4px;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        
        .skills-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding-left: 20px;
        }
        
        .skill-item {
            color: ${colors.secondary};
        }
        
        @media (max-width: 768px) {
            body { padding: 20px; }
            .terminal-body { padding: 20px; font-size: 0.85rem; }
        }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="terminal-header">
            <div class="terminal-btn red"></div>
            <div class="terminal-btn yellow"></div>
            <div class="terminal-btn green"></div>
            <div class="terminal-title">${username}@portfolio ~ bash</div>
        </div>
        <div class="terminal-body">
            <div>
                <span class="prompt">${username}@portfolio:~$</span>
                <span class="command"> whoami</span>
            </div>
            <div class="output">
                <strong style="color: white; font-size: 1.2rem;">${fullName}</strong><br>
                ${p.basic?.headline || 'Software Developer'}<br>
                ${p.basic?.location || ''}
            </div>
            
            <div class="output-section">
                <div class="prompt">${username}@portfolio:~$</div>
                <span class="command"> cat about.txt</span>
                <div class="output">${p.basic?.bio || 'A passionate developer building amazing software.'}</div>
            </div>
            
            ${p.skills?.length > 0 ? `
            <div class="output-section">
                <div class="prompt">${username}@portfolio:~$</div>
                <span class="command"> ls ./skills</span>
                <div class="skills-list">
                    ${p.skills.map(s => `<span class="skill-item">[${s}]</span>`).join(' ')}
                </div>
            </div>
            ` : ''}
            
            ${p.experience?.length > 0 ? `
            <div class="output-section">
                <div class="prompt">${username}@portfolio:~$</div>
                <span class="command"> cat experience.json</span>
                <div class="output">
                    ${p.experience.map(exp => `
                        <div style="margin-bottom: 16px;">
                            <span style="color: ${colors.secondary};">"${exp.title}"</span> @ <span style="color: white;">${exp.company}</span><br>
                            <span style="color: #666;">${exp.startDate} - ${exp.endDate}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
            
            <div class="output-section">
                <div class="prompt">${username}@portfolio:~$</div>
                <span class="command"> cat contact.txt</span>
                <div class="output">
                    ${p.basic?.email ? `📧 <a href="mailto:${p.basic.email}" class="link">${p.basic.email}</a><br>` : ''}
                    ${p.social?.github ? `🐙 <a href="${p.social.github}" class="link" target="_blank">GitHub</a><br>` : ''}
                    ${p.social?.linkedin ? `💼 <a href="${p.social.linkedin}" class="link" target="_blank">LinkedIn</a><br>` : ''}
                </div>
            </div>
            
            <div>
                <span class="prompt">${username}@portfolio:~$</span>
                <span class="cursor"></span>
            </div>
        </div>
    </div>
</body>
</html>`;
}

// ==================== GLASSMORPHISM TEMPLATE ====================
function generateGlassmorphism(profile, colors) {
    const p = profile;
    const fullName = `${p.basic?.firstName || 'Your'} ${p.basic?.lastName || 'Name'}`;
    const initials = (p.basic?.firstName?.charAt(0) || 'U') + (p.basic?.lastName?.charAt(0) || '');
    
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${fullName} - Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: ${colors.bg};
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }
        
        .floating-shapes {
            position: fixed;
            inset: 0;
            z-index: -1;
            overflow: hidden;
        }
        
        .shape {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.6;
        }
        
        .shape-1 {
            width: 600px; height: 600px;
            background: ${colors.primary};
            top: -200px; left: -200px;
            animation: float1 15s infinite;
        }
        
        .shape-2 {
            width: 500px; height: 500px;
            background: ${colors.secondary};
            bottom: -150px; right: -150px;
            animation: float2 18s infinite;
        }
        
        .shape-3 {
            width: 300px; height: 300px;
            background: #f472b6;
            top: 50%; left: 50%;
            animation: float3 12s infinite;
        }
        
        @keyframes float1 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(100px, 100px) scale(1.1); }
        }
        
        @keyframes float2 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(-80px, -80px) scale(1.1); }
        }
        
        @keyframes float3 {
            0%, 100% { transform: translate(-50%, -50%) scale(1); }
            50% { transform: translate(-50%, -50%) scale(0.8); }
        }
        
        .glass {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 24px;
        }
        
        .container { max-width: 1000px; margin: 0 auto; padding: 40px 24px; }
        
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
        }
        
        .hero-card {
            text-align: center;
            padding: 60px 80px;
        }
        
        .avatar {
            width: 150px; height: 150px;
            background: linear-gradient(135deg, ${colors.primary}, ${colors.secondary});
            border-radius: 50%;
            margin: 0 auto 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3.5rem;
            font-weight: 800;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .hero h1 { font-size: 3rem; font-weight: 800; margin-bottom: 12px; }
        .hero-tagline { font-size: 1.2rem; opacity: 0.9; margin-bottom: 20px; }
        .hero-bio { opacity: 0.8; max-width: 500px; margin: 0 auto 32px; }
        
        .social-links { display: flex; justify-content: center; gap: 16px; }
        
        .social-link {
            width: 48px; height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
            transition: all 0.3s;
        }
        
        .social-link:hover { transform: scale(1.15); background: rgba(255,255,255,0.2); }
        
        .section { padding: 60px 0; }
        .section-title { font-size: 2rem; font-weight: 700; margin-bottom: 32px; text-align: center; }
        
        .skills-grid {
            display: flex; flex-wrap: wrap; justify-content: center; gap: 12px;
        }
        
        .skill-tag {
            padding: 10px 24px;
            border-radius: 50px;
            font-size: 0.9rem;
        }
        
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
        }
        
        .card {
            padding: 28px;
            transition: all 0.3s;
        }
        
        .card:hover { transform: translateY(-8px); background: rgba(255,255,255,0.15); }
        
        .card-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 8px; }
        .card-subtitle { color: ${colors.primary}; margin-bottom: 8px; font-weight: 500; }
        .card-desc { opacity: 0.8; font-size: 0.95rem; }
        
        .footer { text-align: center; padding: 40px 0; opacity: 0.7; }
        
        @media (max-width: 768px) {
            .hero-card { padding: 40px 24px; }
            .hero h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
    </div>
    
    <section class="hero">
        <div class="hero-card glass">
            <div class="avatar">${initials}</div>
            <h1>${fullName}</h1>
            <p class="hero-tagline">${p.basic?.headline || 'Software Developer'}</p>
            <p class="hero-bio">${p.basic?.bio || ''}</p>
            <div class="social-links">
                ${p.social?.linkedin ? `<a href="${p.social.linkedin}" class="social-link glass" target="_blank"><i class="fab fa-linkedin-in"></i></a>` : ''}
                ${p.social?.github ? `<a href="${p.social.github}" class="social-link glass" target="_blank"><i class="fab fa-github"></i></a>` : ''}
                ${p.social?.twitter ? `<a href="${p.social.twitter}" class="social-link glass" target="_blank"><i class="fab fa-twitter"></i></a>` : ''}
                <a href="mailto:${p.basic?.email || ''}" class="social-link glass"><i class="fas fa-envelope"></i></a>
            </div>
        </div>
    </section>
    
    <div class="container">
        ${p.skills?.length > 0 ? `
        <section class="section">
            <h2 class="section-title">Skills</h2>
            <div class="skills-grid">
                ${p.skills.map(s => `<span class="skill-tag glass">${s}</span>`).join('')}
            </div>
        </section>
        ` : ''}
        
        ${p.experience?.length > 0 ? `
        <section class="section">
            <h2 class="section-title">Experience</h2>
            <div class="card-grid">
                ${p.experience.map(exp => `
                    <div class="card glass">
                        <h3 class="card-title">${exp.title}</h3>
                        <div class="card-subtitle">${exp.company}</div>
                        <p class="card-desc">${exp.description || ''}</p>
                    </div>
                `).join('')}
            </div>
        </section>
        ` : ''}
        
        ${p.projects?.length > 0 ? `
        <section class="section">
            <h2 class="section-title">Projects</h2>
            <div class="card-grid">
                ${p.projects.map(proj => `
                    <div class="card glass">
                        <h3 class="card-title">${proj.name}</h3>
                        <p class="card-desc">${proj.description || ''}</p>
                    </div>
                `).join('')}
            </div>
        </section>
        ` : ''}
    </div>
    
    <footer class="footer">
        <p>© ${new Date().getFullYear()} ${fullName}</p>
    </footer>
</body>
</html>`;
}

// ==================== CREATIVE PORTFOLIO TEMPLATE ====================
function generateCreative(profile, colors) {
    const p = profile;
    const fullName = `${p.basic?.firstName || 'Your'} ${p.basic?.lastName || 'Name'}`;
    
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${fullName} - Creative Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Space Grotesk', sans-serif;
            background: ${colors.bg};
            color: #1a1a1a;
            overflow-x: hidden;
        }
        
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            padding: 40px;
            position: relative;
        }
        
        .hero-bg {
            position: absolute;
            top: 0; right: 0;
            width: 50%;
            height: 100%;
            background: linear-gradient(135deg, ${colors.primary}, ${colors.secondary});
            clip-path: polygon(20% 0, 100% 0, 100% 100%, 0% 100%);
        }
        
        .hero-content {
            position: relative;
            z-index: 1;
            max-width: 600px;
            padding-left: 10%;
        }
        
        .hero h1 {
            font-size: 4.5rem;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 24px;
        }
        
        .hero h1 span {
            color: ${colors.primary};
        }
        
        .hero-tagline {
            font-size: 1.5rem;
            color: #666;
            margin-bottom: 16px;
        }
        
        .hero-bio {
            font-size: 1.1rem;
            color: #888;
            margin-bottom: 32px;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 16px 36px;
            background: ${colors.primary};
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            transition: all 0.3s;
            margin-right: 12px;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .btn-outline {
            background: transparent;
            color: #1a1a1a;
            border: 2px solid #1a1a1a;
        }
        
        .btn-outline:hover {
            background: #1a1a1a;
            color: white;
        }
        
        .section {
            padding: 100px 10%;
        }
        
        .section-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 60px;
        }
        
        .section-title span {
            color: ${colors.primary};
        }
        
        .skills-section {
            background: #f8f8f8;
        }
        
        .skills-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
        }
        
        .skill-tag {
            padding: 14px 28px;
            background: white;
            border-radius: 50px;
            font-weight: 500;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: all 0.3s;
        }
        
        .skill-tag:hover {
            background: ${colors.primary};
            color: white;
            transform: translateY(-4px);
        }
        
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 40px;
        }
        
        .project-card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }
        
        .project-card:hover {
            transform: translateY(-10px);
        }
        
        .project-image {
            height: 200px;
            background: linear-gradient(135deg, ${colors.primary}, ${colors.secondary});
        }
        
        .project-content {
            padding: 28px;
        }
        
        .project-title {
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 12px;
        }
        
        .project-desc {
            color: #666;
            margin-bottom: 20px;
        }
        
        .project-link {
            color: ${colors.primary};
            font-weight: 600;
            text-decoration: none;
        }
        
        .project-link:hover {
            text-decoration: underline;
        }
        
        .footer {
            background: #1a1a1a;
            color: white;
            padding: 60px 10%;
            text-align: center;
        }
        
        .footer-title {
            font-size: 2.5rem;
            margin-bottom: 24px;
        }
        
        .social-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 32px;
        }
        
        .social-link {
            width: 50px;
            height: 50px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
            transition: all 0.3s;
        }
        
        .social-link:hover {
            background: white;
            color: #1a1a1a;
            border-color: white;
        }
        
        @media (max-width: 768px) {
            .hero-bg { display: none; }
            .hero h1 { font-size: 3rem; }
            .hero-content { padding-left: 0; }
            .projects-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-bg"></div>
        <div class="hero-content">
            <h1>Hi, I'm<br><span>${fullName}</span></h1>
            <p class="hero-tagline">${p.basic?.headline || 'Creative Developer'}</p>
            <p class="hero-bio">${p.basic?.bio || ''}</p>
            <div>
                <a href="mailto:${p.basic?.email || ''}" class="btn"><i class="fas fa-envelope"></i> Say Hello</a>
                <a href="#projects" class="btn btn-outline">View Work</a>
            </div>
        </div>
    </section>
    
    ${p.skills?.length > 0 ? `
    <section class="section skills-section">
        <h2 class="section-title">What I <span>Know</span></h2>
        <div class="skills-grid">
            ${p.skills.map(s => `<span class="skill-tag">${s}</span>`).join('')}
        </div>
    </section>
    ` : ''}
    
    ${p.projects?.length > 0 ? `
    <section class="section" id="projects">
        <h2 class="section-title">My <span>Work</span></h2>
        <div class="projects-grid">
            ${p.projects.map(proj => `
                <div class="project-card">
                    <div class="project-image"></div>
                    <div class="project-content">
                        <h3 class="project-title">${proj.name}</h3>
                        <p class="project-desc">${proj.description || ''}</p>
                        ${proj.url ? `<a href="${proj.url}" class="project-link" target="_blank">View Project →</a>` : ''}
                    </div>
                </div>
            `).join('')}
        </div>
    </section>
    ` : ''}
    
    <footer class="footer">
        <h2 class="footer-title">Let's Work Together</h2>
        <p>${p.basic?.email || ''}</p>
        <div class="social-links">
            ${p.social?.linkedin ? `<a href="${p.social.linkedin}" class="social-link" target="_blank"><i class="fab fa-linkedin-in"></i></a>` : ''}
            ${p.social?.github ? `<a href="${p.social.github}" class="social-link" target="_blank"><i class="fab fa-github"></i></a>` : ''}
            ${p.social?.twitter ? `<a href="${p.social.twitter}" class="social-link" target="_blank"><i class="fab fa-twitter"></i></a>` : ''}
        </div>
    </footer>
</body>
</html>`;
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PortfolioTemplates;
}

window.PortfolioTemplates = PortfolioTemplates;
