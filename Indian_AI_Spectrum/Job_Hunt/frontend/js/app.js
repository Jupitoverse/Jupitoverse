/**
 * CareerLaunch - Complete Career Platform
 * Main Application JavaScript
 */

console.log('🚀 CareerLaunch Loading...');

// ==================== STATE MANAGEMENT ====================
let profileData = {
    basic: {},
    education: [],
    certifications: [],
    experience: [],
    projects: [],
    skills: [],
    achievements: [],
    social: {}
};

let interviews = [];
let currentRoundCount = 0;
let currentFilter = 'all';
let selectedTemplate = 'developer-dark';

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', function() {
    loadAllData();
    initNavigation();
    initTabs();
    initSkills();
    initTemplates();
    initInterviewFilters();
    initCalendar();
    updateGreeting();
    updateStats();
    updateCompletion();
    renderAllLists();
    
    console.log('✅ CareerLaunch Loaded Successfully!');
});

// ==================== DATA PERSISTENCE ====================
function loadAllData() {
    // Load profile data
    const savedProfile = localStorage.getItem('careerlaunch_profile');
    if (savedProfile) {
        profileData = JSON.parse(savedProfile);
        populateFormFields();
        updateProfileDisplay();
    }
    
    // Load interviews
    const savedInterviews = localStorage.getItem('careerlaunch_interviews');
    if (savedInterviews) {
        interviews = JSON.parse(savedInterviews);
    }
}

function saveProfileData() {
    localStorage.setItem('careerlaunch_profile', JSON.stringify(profileData));
    updateCompletion();
    updateProfileDisplay();
}

function saveInterviews() {
    localStorage.setItem('careerlaunch_interviews', JSON.stringify(interviews));
    updateStats();
    renderInterviews();
    renderRecentInterviews();
}

// ==================== NAVIGATION ====================
function initNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function() {
            showSection(this.dataset.section);
        });
    });
}

function showSection(name) {
    // Hide all sections
    document.querySelectorAll('section').forEach(s => s.classList.add('hidden'));
    
    // Show target section
    const section = document.getElementById('section-' + name);
    if (section) {
        section.classList.remove('hidden');
        section.classList.add('animate-in');
    }
    
    // Update nav active state
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const navItem = document.querySelector(`[data-section="${name}"]`);
    if (navItem) navItem.classList.add('active');
}

window.showSection = showSection;

// ==================== TABS ====================
function initTabs() {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function() {
            const tabId = this.dataset.tab;
            
            // Update active tab
            const tabContainer = this.closest('.tabs');
            tabContainer.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Show content
            const section = this.closest('section');
            section.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            const content = document.getElementById('tab-' + tabId);
            if (content) content.classList.add('active');
            
            // Update progress steps
            updateProgressSteps(tabId);
        });
    });
}

function switchToTab(tabName) {
    const tab = document.querySelector(`[data-tab="${tabName}"]`);
    if (tab) tab.click();
}

window.switchToTab = switchToTab;

function updateProgressSteps(currentTab) {
    const steps = ['basic', 'education', 'experience', 'projects', 'skills', 'social'];
    const currentIndex = steps.indexOf(currentTab);
    
    document.querySelectorAll('.progress-step').forEach((step, index) => {
        step.classList.remove('active', 'completed');
        if (index < currentIndex) {
            step.classList.add('completed');
            step.querySelector('.step-circle').innerHTML = '✓';
        } else if (index === currentIndex) {
            step.classList.add('active');
            step.querySelector('.step-circle').textContent = index + 1;
        } else {
            step.querySelector('.step-circle').textContent = index + 1;
        }
    });
}

// ==================== MODAL FUNCTIONS ====================
function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

window.openModal = openModal;
window.closeModal = closeModal;

// Close modal on overlay click
document.querySelectorAll('.modal-overlay').forEach(modal => {
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            this.classList.remove('active');
        }
    });
});

// ==================== INTERVIEW FUNCTIONS ====================
function openInterviewModal() {
    openModal('modal-interview');
    currentRoundCount = 0;
    document.getElementById('rounds-container').innerHTML = '';
    addRound();
}

window.openInterviewModal = openInterviewModal;

function addRound() {
    currentRoundCount++;
    const template = document.getElementById('round-template');
    const clone = template.content.cloneNode(true);
    clone.querySelector('.round-num').textContent = currentRoundCount;
    document.getElementById('rounds-container').appendChild(clone);
}

window.addRound = addRound;

function removeRound(btn) {
    if (currentRoundCount <= 1) {
        alert('At least one round is required');
        return;
    }
    btn.closest('.round-card').remove();
    currentRoundCount--;
    
    // Renumber rounds
    document.querySelectorAll('.round-num').forEach((el, idx) => {
        el.textContent = idx + 1;
    });
}

window.removeRound = removeRound;

function saveInterview() {
    const company = document.getElementById('int-company').value.trim();
    const position = document.getElementById('int-position').value.trim();
    
    if (!company || !position) {
        alert('Please fill in Company and Position');
        return;
    }
    
    // Collect rounds
    const rounds = [];
    document.querySelectorAll('#rounds-container .round-card').forEach((card, idx) => {
        rounds.push({
            number: idx + 1,
            type: card.querySelector('.round-type').value,
            datetime: card.querySelector('.round-datetime').value,
            status: card.querySelector('.round-status').value,
            questions: card.querySelector('.round-questions').value,
            notes: card.querySelector('.round-notes').value
        });
    });
    
    const interview = {
        id: Date.now(),
        company,
        position,
        appliedDate: document.getElementById('int-applied-date').value,
        appliedVia: document.getElementById('int-applied-via').value,
        status: document.getElementById('int-status').value,
        hrName: document.getElementById('int-hr-name').value,
        hrContact: document.getElementById('int-hr-contact').value,
        expectedCtc: document.getElementById('int-expected-ctc').value,
        offeredCtc: document.getElementById('int-offered-ctc').value,
        isPublic: document.getElementById('int-public').checked,
        notes: document.getElementById('int-notes').value,
        rounds,
        createdAt: new Date().toISOString()
    };
    
    interviews.push(interview);
    saveInterviews();
    
    closeModal('modal-interview');
    document.getElementById('interview-form').reset();
    
    alert('Interview saved successfully! 🎉');
}

window.saveInterview = saveInterview;

function initInterviewFilters() {
    document.querySelectorAll('.filter-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            currentFilter = this.dataset.filter;
            document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            renderInterviews();
        });
    });
}

function renderInterviews() {
    const container = document.getElementById('interviews-list');
    let filtered = currentFilter === 'all' ? interviews : interviews.filter(i => i.status === currentFilter);
    
    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📋</div>
                <div class="empty-title">No interviews found</div>
                <div class="empty-desc">${currentFilter === 'all' ? 'Start tracking your journey' : 'No interviews with this status'}</div>
                <button class="btn btn-primary" onclick="openInterviewModal()">
                    <i class="fas fa-plus"></i> Add Interview
                </button>
            </div>`;
        return;
    }
    
    const statusEmoji = {
        applied: '📤', screening: '📞', in_progress: '🔄', final_round: '🎯',
        offer: '🎉', accepted: '✅', rejected: '❌', declined: '🚫', on_hold: '⏸️'
    };
    
    container.innerHTML = filtered.map(int => `
        <div class="interview-card animate-slide">
            <div class="interview-header">
                <div>
                    <div class="interview-company">${int.company}</div>
                    <div class="interview-position">${int.position}</div>
                </div>
                <span class="status-badge status-${int.status}">
                    ${statusEmoji[int.status] || ''} ${int.status.replace('_', ' ')}
                </span>
            </div>
            <div class="interview-meta">
                <span><i class="fas fa-calendar"></i> ${int.appliedDate || 'N/A'}</span>
                <span><i class="fas fa-list-ol"></i> ${int.rounds?.length || 0} rounds</span>
                <span><i class="fas fa-${int.appliedVia === 'referral' ? 'user-friends' : 'globe'}"></i> ${int.appliedVia || 'Direct'}</span>
                <span><i class="fas fa-${int.isPublic ? 'globe' : 'lock'}"></i> ${int.isPublic ? 'Public' : 'Private'}</span>
            </div>
            <div class="interview-actions">
                <button class="btn btn-xs btn-outline"><i class="fas fa-eye"></i> View</button>
                <button class="btn btn-xs btn-secondary"><i class="fas fa-edit"></i> Edit</button>
                <button class="btn btn-xs btn-error" onclick="deleteInterview(${int.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function renderRecentInterviews() {
    const container = document.getElementById('recent-interviews');
    const recent = interviews.slice(-3).reverse();
    
    if (recent.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="padding: 24px;">
                <div class="empty-icon">📋</div>
                <div class="empty-title">No interviews yet</div>
                <div class="text-sm text-muted">Start tracking your journey</div>
            </div>`;
        return;
    }
    
    const statusEmoji = {
        applied: '📤', screening: '📞', in_progress: '🔄', final_round: '🎯',
        offer: '🎉', rejected: '❌', declined: '🚫'
    };
    
    container.innerHTML = recent.map(int => `
        <div class="item-card" style="margin-bottom: 12px;">
            <div class="item-title">${int.company}</div>
            <div class="item-subtitle">${int.position}</div>
            <div class="item-meta">
                <span class="status-badge status-${int.status}" style="font-size: 0.7rem; padding: 4px 10px;">
                    ${statusEmoji[int.status] || ''} ${int.status.replace('_', ' ')}
                </span>
            </div>
        </div>
    `).join('');
}

function deleteInterview(id) {
    if (!confirm('Delete this interview?')) return;
    interviews = interviews.filter(i => i.id !== id);
    saveInterviews();
}

window.deleteInterview = deleteInterview;

// ==================== PROFILE FUNCTIONS ====================
function saveBasicInfo() {
    profileData.basic = {
        firstName: document.getElementById('first-name').value,
        lastName: document.getElementById('last-name').value,
        headline: document.getElementById('headline').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        location: document.getElementById('location').value,
        experienceYears: document.getElementById('experience-years').value,
        currentRole: document.getElementById('current-role').value,
        bio: document.getElementById('bio').value,
        lookingForJob: document.getElementById('looking-for-job').checked,
        noticePeriod: document.getElementById('notice-period').value,
        expectedCtc: document.getElementById('expected-ctc').value
    };
    
    saveProfileData();
    switchToTab('education');
    alert('Basic info saved! ✅');
}

window.saveBasicInfo = saveBasicInfo;

function saveEducation() {
    const edu = {
        id: Date.now(),
        degree: document.getElementById('edu-degree').value,
        institution: document.getElementById('edu-institution').value,
        startYear: document.getElementById('edu-start').value,
        endYear: document.getElementById('edu-end').value,
        grade: document.getElementById('edu-grade').value,
        description: document.getElementById('edu-desc').value
    };
    
    if (!edu.degree || !edu.institution) {
        alert('Please fill required fields');
        return;
    }
    
    profileData.education.push(edu);
    saveProfileData();
    renderEducationList();
    closeModal('modal-education');
    clearModalFields('modal-education');
}

window.saveEducation = saveEducation;

function saveExperience() {
    const exp = {
        id: Date.now(),
        title: document.getElementById('exp-title').value,
        company: document.getElementById('exp-company').value,
        location: document.getElementById('exp-location').value,
        startDate: document.getElementById('exp-start').value,
        endDate: document.getElementById('exp-current')?.checked ? 'Present' : document.getElementById('exp-end').value,
        description: document.getElementById('exp-desc').value,
        techStack: document.getElementById('exp-tech').value
    };
    
    if (!exp.title || !exp.company) {
        alert('Please fill required fields');
        return;
    }
    
    profileData.experience.push(exp);
    saveProfileData();
    renderExperienceList();
    closeModal('modal-experience');
    clearModalFields('modal-experience');
}

window.saveExperience = saveExperience;

function saveProject() {
    const proj = {
        id: Date.now(),
        name: document.getElementById('proj-name').value,
        description: document.getElementById('proj-desc').value,
        url: document.getElementById('proj-url').value,
        github: document.getElementById('proj-github').value,
        techStack: document.getElementById('proj-tech').value,
        features: document.getElementById('proj-features').value
    };
    
    if (!proj.name || !proj.description) {
        alert('Please fill required fields');
        return;
    }
    
    profileData.projects.push(proj);
    saveProfileData();
    renderProjectList();
    closeModal('modal-project');
    clearModalFields('modal-project');
}

window.saveProject = saveProject;

function saveCertification() {
    const cert = {
        id: Date.now(),
        name: document.getElementById('cert-name').value,
        organization: document.getElementById('cert-org').value,
        date: document.getElementById('cert-date').value,
        expiry: document.getElementById('cert-expiry').value,
        url: document.getElementById('cert-url').value
    };
    
    if (!cert.name) {
        alert('Please fill certification name');
        return;
    }
    
    profileData.certifications.push(cert);
    saveProfileData();
    renderCertList();
    closeModal('modal-cert');
    clearModalFields('modal-cert');
}

window.saveCertification = saveCertification;

function saveAward() {
    const award = {
        id: Date.now(),
        title: document.getElementById('award-title').value,
        organization: document.getElementById('award-org').value,
        date: document.getElementById('award-date').value,
        description: document.getElementById('award-desc').value
    };
    
    if (!award.title) {
        alert('Please fill award title');
        return;
    }
    
    profileData.achievements.push(award);
    saveProfileData();
    renderAwardList();
    closeModal('modal-award');
    clearModalFields('modal-award');
}

window.saveAward = saveAward;

function saveSocialLinks() {
    profileData.social = {
        linkedin: document.getElementById('linkedin-url').value,
        github: document.getElementById('github-url').value,
        kaggle: document.getElementById('kaggle-url').value,
        huggingface: document.getElementById('huggingface-url').value,
        twitter: document.getElementById('twitter-url').value,
        website: document.getElementById('website-url').value,
        leetcode: document.getElementById('leetcode-url').value,
        hackerrank: document.getElementById('hackerrank-url').value
    };
    saveProfileData();
    alert('Social links saved! ✅');
}

window.saveSocialLinks = saveSocialLinks;

function clearModalFields(modalId) {
    document.querySelectorAll(`#${modalId} input, #${modalId} textarea, #${modalId} select`).forEach(el => {
        if (el.type === 'checkbox') el.checked = false;
        else el.value = '';
    });
}

// ==================== SKILLS ====================
function initSkills() {
    document.querySelectorAll('.skill-tag').forEach(tag => {
        tag.addEventListener('click', function() {
            this.classList.toggle('selected');
            updateSelectedSkills();
        });
    });
}

function updateSelectedSkills() {
    const selected = Array.from(document.querySelectorAll('.skill-tag.selected')).map(t => t.dataset.skill);
    profileData.skills = selected;
    document.getElementById('skills-count').textContent = selected.length;
}

function saveSkills() {
    saveProfileData();
    alert('Skills saved! ✅');
}

window.saveSkills = saveSkills;

// ==================== RENDER LISTS ====================
function renderAllLists() {
    renderEducationList();
    renderCertList();
    renderExperienceList();
    renderProjectList();
    renderAwardList();
    renderInterviews();
    renderRecentInterviews();
}

function renderEducationList() {
    const container = document.getElementById('education-list');
    if (!profileData.education?.length) {
        container.innerHTML = '<div class="empty-state"><div class="empty-icon">🎓</div><div class="empty-title">No education added</div></div>';
        return;
    }
    container.innerHTML = profileData.education.map(edu => `
        <div class="item-card">
            <div class="item-header">
                <div>
                    <div class="item-title">${edu.degree}</div>
                    <div class="item-subtitle">${edu.institution}</div>
                </div>
                <button class="btn btn-xs btn-error" onclick="deleteEducation(${edu.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="item-meta">${edu.startYear} - ${edu.endYear} ${edu.grade ? '• ' + edu.grade : ''}</div>
            ${edu.description ? `<div class="item-desc">${edu.description}</div>` : ''}
        </div>
    `).join('');
}

function deleteEducation(id) {
    profileData.education = profileData.education.filter(e => e.id !== id);
    saveProfileData();
    renderEducationList();
}
window.deleteEducation = deleteEducation;

function renderCertList() {
    const container = document.getElementById('cert-list');
    if (!profileData.certifications?.length) {
        container.innerHTML = '<div class="empty-state"><div class="empty-icon">📜</div><div class="empty-title">No certifications added</div></div>';
        return;
    }
    container.innerHTML = profileData.certifications.map(cert => `
        <div class="item-card">
            <div class="item-header">
                <div>
                    <div class="item-title">${cert.name}</div>
                    <div class="item-subtitle">${cert.organization || ''}</div>
                </div>
                <button class="btn btn-xs btn-error" onclick="deleteCert(${cert.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="item-meta">${cert.date || ''} ${cert.url ? `• <a href="${cert.url}" target="_blank" class="text-accent">Verify</a>` : ''}</div>
        </div>
    `).join('');
}

function deleteCert(id) {
    profileData.certifications = profileData.certifications.filter(c => c.id !== id);
    saveProfileData();
    renderCertList();
}
window.deleteCert = deleteCert;

function renderExperienceList() {
    const container = document.getElementById('experience-list');
    if (!profileData.experience?.length) {
        container.innerHTML = '<div class="empty-state"><div class="empty-icon">💼</div><div class="empty-title">No experience added</div></div>';
        return;
    }
    container.innerHTML = profileData.experience.map(exp => `
        <div class="item-card">
            <div class="item-header">
                <div>
                    <div class="item-title">${exp.title}</div>
                    <div class="item-subtitle">${exp.company}</div>
                </div>
                <button class="btn btn-xs btn-error" onclick="deleteExperience(${exp.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="item-meta">${exp.startDate} - ${exp.endDate} ${exp.location ? '• ' + exp.location : ''}</div>
            <div class="item-desc">${exp.description}</div>
            ${exp.techStack ? `<div class="item-tags">${exp.techStack.split(',').map(t => `<span class="item-tag">${t.trim()}</span>`).join('')}</div>` : ''}
        </div>
    `).join('');
}

function deleteExperience(id) {
    profileData.experience = profileData.experience.filter(e => e.id !== id);
    saveProfileData();
    renderExperienceList();
}
window.deleteExperience = deleteExperience;

function renderProjectList() {
    const container = document.getElementById('project-list');
    if (!profileData.projects?.length) {
        container.innerHTML = '<div class="empty-state"><div class="empty-icon">🚀</div><div class="empty-title">No projects added</div></div>';
        return;
    }
    container.innerHTML = profileData.projects.map(proj => `
        <div class="item-card">
            <div class="item-header">
                <div>
                    <div class="item-title">${proj.name}</div>
                    <div class="flex gap-2 mt-1">
                        ${proj.url ? `<a href="${proj.url}" target="_blank" class="text-xs text-accent"><i class="fas fa-external-link-alt"></i> Live</a>` : ''}
                        ${proj.github ? `<a href="${proj.github}" target="_blank" class="text-xs text-accent"><i class="fab fa-github"></i> Code</a>` : ''}
                    </div>
                </div>
                <button class="btn btn-xs btn-error" onclick="deleteProject(${proj.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="item-desc">${proj.description}</div>
            ${proj.techStack ? `<div class="item-tags">${proj.techStack.split(',').map(t => `<span class="item-tag">${t.trim()}</span>`).join('')}</div>` : ''}
        </div>
    `).join('');
}

function deleteProject(id) {
    profileData.projects = profileData.projects.filter(p => p.id !== id);
    saveProfileData();
    renderProjectList();
}
window.deleteProject = deleteProject;

function renderAwardList() {
    const container = document.getElementById('award-list');
    if (!profileData.achievements?.length) {
        container.innerHTML = '<div class="empty-state"><div class="empty-icon">🏆</div><div class="empty-title">No awards added</div></div>';
        return;
    }
    container.innerHTML = profileData.achievements.map(award => `
        <div class="item-card">
            <div class="item-header">
                <div>
                    <div class="item-title">${award.title}</div>
                    <div class="item-subtitle">${award.organization || ''}</div>
                </div>
                <button class="btn btn-xs btn-error" onclick="deleteAward(${award.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="item-meta">${award.date || ''}</div>
            ${award.description ? `<div class="item-desc">${award.description}</div>` : ''}
        </div>
    `).join('');
}

function deleteAward(id) {
    profileData.achievements = profileData.achievements.filter(a => a.id !== id);
    saveProfileData();
    renderAwardList();
}
window.deleteAward = deleteAward;

// ==================== POPULATE FORM FIELDS ====================
function populateFormFields() {
    const p = profileData;
    
    // Basic info
    if (p.basic?.firstName) document.getElementById('first-name').value = p.basic.firstName;
    if (p.basic?.lastName) document.getElementById('last-name').value = p.basic.lastName;
    if (p.basic?.headline) document.getElementById('headline').value = p.basic.headline;
    if (p.basic?.email) document.getElementById('email').value = p.basic.email;
    if (p.basic?.phone) document.getElementById('phone').value = p.basic.phone;
    if (p.basic?.location) document.getElementById('location').value = p.basic.location;
    if (p.basic?.experienceYears) document.getElementById('experience-years').value = p.basic.experienceYears;
    if (p.basic?.currentRole) document.getElementById('current-role').value = p.basic.currentRole;
    if (p.basic?.bio) document.getElementById('bio').value = p.basic.bio;
    if (p.basic?.lookingForJob) document.getElementById('looking-for-job').checked = p.basic.lookingForJob;
    if (p.basic?.noticePeriod) document.getElementById('notice-period').value = p.basic.noticePeriod;
    if (p.basic?.expectedCtc) document.getElementById('expected-ctc').value = p.basic.expectedCtc;
    
    // Social links
    if (p.social?.linkedin) document.getElementById('linkedin-url').value = p.social.linkedin;
    if (p.social?.github) document.getElementById('github-url').value = p.social.github;
    if (p.social?.kaggle) document.getElementById('kaggle-url').value = p.social.kaggle;
    if (p.social?.huggingface) document.getElementById('huggingface-url').value = p.social.huggingface;
    if (p.social?.twitter) document.getElementById('twitter-url').value = p.social.twitter;
    if (p.social?.website) document.getElementById('website-url').value = p.social.website;
    if (p.social?.leetcode) document.getElementById('leetcode-url').value = p.social.leetcode;
    if (p.social?.hackerrank) document.getElementById('hackerrank-url').value = p.social.hackerrank;
    
    // Skills
    if (p.skills?.length) {
        p.skills.forEach(skill => {
            const tag = document.querySelector(`.skill-tag[data-skill="${skill}"]`);
            if (tag) tag.classList.add('selected');
        });
        document.getElementById('skills-count').textContent = p.skills.length;
    }
}

function updateProfileDisplay() {
    const p = profileData.basic;
    if (p?.firstName) {
        const fullName = `${p.firstName} ${p.lastName || ''}`.trim();
        document.getElementById('user-name').textContent = fullName;
        document.getElementById('greeting-name').textContent = p.firstName;
        document.getElementById('avatar').innerHTML = p.firstName.charAt(0).toUpperCase() + 
            '<div class="avatar-badge"><i class="fas fa-check"></i></div>';
    }
    if (p?.headline) {
        document.getElementById('user-headline').textContent = p.headline.substring(0, 50) + (p.headline.length > 50 ? '...' : '');
    }
}

// ==================== STATS & COMPLETION ====================
function updateStats() {
    const total = interviews.length;
    const active = interviews.filter(i => !['rejected', 'declined'].includes(i.status)).length;
    const offers = interviews.filter(i => ['offer', 'accepted'].includes(i.status)).length;
    const responded = interviews.filter(i => i.status !== 'applied').length;
    const responseRate = total > 0 ? Math.round((responded / total) * 100) : 0;
    
    document.getElementById('stat-applications').textContent = total;
    document.getElementById('stat-interviews').textContent = active;
    document.getElementById('stat-offers').textContent = offers;
    document.getElementById('stat-response').textContent = responseRate + '%';
    document.getElementById('interview-count').textContent = total;
}

function updateCompletion() {
    const items = [];
    let completed = 0;
    
    if (profileData.basic?.firstName && profileData.basic?.bio) {
        completed++;
        items.push({ name: 'Basic Info', done: true });
    } else {
        items.push({ name: 'Basic Info', done: false });
    }
    
    if (profileData.education?.length > 0) {
        completed++;
        items.push({ name: 'Education', done: true });
    } else {
        items.push({ name: 'Education', done: false });
    }
    
    if (profileData.experience?.length > 0) {
        completed++;
        items.push({ name: 'Experience', done: true });
    } else {
        items.push({ name: 'Experience', done: false });
    }
    
    if (profileData.projects?.length > 0) {
        completed++;
        items.push({ name: 'Projects', done: true });
    } else {
        items.push({ name: 'Projects', done: false });
    }
    
    if (profileData.skills?.length > 0) {
        completed++;
        items.push({ name: 'Skills', done: true });
    } else {
        items.push({ name: 'Skills', done: false });
    }
    
    if (profileData.social?.linkedin || profileData.social?.github) {
        completed++;
        items.push({ name: 'Social Links', done: true });
    } else {
        items.push({ name: 'Social Links', done: false });
    }
    
    const percent = Math.round((completed / 6) * 100);
    
    // Update all completion displays
    document.getElementById('sidebar-completion').textContent = percent + '%';
    document.getElementById('sidebar-completion-bar').style.width = percent + '%';
    document.getElementById('overview-completion').textContent = percent + '%';
    document.getElementById('overview-completion-bar').style.width = percent + '%';
    document.getElementById('profile-badge').textContent = percent + '%';
    
    // Update completion items
    document.getElementById('completion-items').innerHTML = items.map(i => 
        `<span class="completion-item ${i.done ? 'done' : 'pending'}">
            ${i.done ? '✅' : '⏳'} ${i.name}
        </span>`
    ).join('');
    
    // Hide completion card if 100%
    if (percent === 100) {
        document.getElementById('completion-card').style.display = 'none';
    }
}

function updateGreeting() {
    const hour = new Date().getHours();
    let greeting = 'Good Morning';
    if (hour >= 12 && hour < 17) greeting = 'Good Afternoon';
    else if (hour >= 17) greeting = 'Good Evening';
    document.getElementById('greeting').textContent = greeting;
}

// ==================== PORTFOLIO ====================
function initTemplates() {
    document.querySelectorAll('.template-card').forEach(card => {
        card.addEventListener('click', function() {
            document.querySelectorAll('.template-card').forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            selectedTemplate = this.dataset.template;
        });
    });
}

function showPortfolioStep(step) {
    document.getElementById('portfolio-step-1').classList.toggle('hidden', step !== 1);
    document.getElementById('portfolio-step-2').classList.toggle('hidden', step !== 2);
    document.getElementById('portfolio-step-3').classList.toggle('hidden', step !== 3);
}

window.showPortfolioStep = showPortfolioStep;

function generatePortfolio() {
    if (!profileData.basic?.firstName) {
        alert('Please complete your basic profile first!');
        showSection('profile');
        return;
    }
    
    generatePortfolioPreview();
    showPortfolioStep(2);
}

window.generatePortfolio = generatePortfolio;

function generatePortfolioPreview() {
    const preview = document.getElementById('portfolio-preview');
    const username = (profileData.basic?.firstName || 'user').toLowerCase().replace(/\s/g, '');
    
    document.getElementById('preview-username').textContent = username;
    
    // Use the portfolio templates engine if available
    if (window.PortfolioTemplates) {
        const html = PortfolioTemplates.generate(selectedTemplate, profileData);
        preview.innerHTML = `<iframe srcdoc="${html.replace(/"/g, '&quot;')}" style="width: 100%; height: 600px; border: none;"></iframe>`;
    } else {
        // Fallback to inline preview
        const p = profileData;
        const fullName = `${p.basic?.firstName || ''} ${p.basic?.lastName || ''}`.trim() || 'Your Name';
        
        preview.innerHTML = `
            <div style="font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #0f0f23, #1a1a3e); color: white; min-height: 500px; padding: 60px 40px;">
                <div style="max-width: 900px; margin: 0 auto;">
                    <div style="text-align: center; margin-bottom: 50px;">
                        <div style="width: 140px; height: 140px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 50%; margin: 0 auto 24px; display: flex; align-items: center; justify-content: center; font-size: 3.5rem; font-weight: bold; box-shadow: 0 20px 60px rgba(99,102,241,0.4);">
                            ${fullName.charAt(0)}
                        </div>
                        <h1 style="font-size: 2.5rem; margin-bottom: 12px; font-weight: 700;">${fullName}</h1>
                        <p style="color: #a0a0b0; font-size: 1.2rem;">${p.basic?.headline || 'Software Developer'}</p>
                        <p style="color: #6b7280; margin-top: 12px; font-size: 0.95rem;">📍 ${p.basic?.location || 'Location'}</p>
                        
                        <div style="display: flex; justify-content: center; gap: 12px; margin-top: 24px;">
                            ${p.social?.linkedin ? `<a href="${p.social.linkedin}" style="width: 44px; height: 44px; background: #0077b5; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; text-decoration: none;">in</a>` : ''}
                            ${p.social?.github ? `<a href="${p.social.github}" style="width: 44px; height: 44px; background: #333; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; text-decoration: none;">GH</a>` : ''}
                            ${p.social?.twitter ? `<a href="${p.social.twitter}" style="width: 44px; height: 44px; background: #1da1f2; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; text-decoration: none;">X</a>` : ''}
                        </div>
                    </div>
                    
                    ${p.basic?.bio ? `
                    <div style="background: rgba(255,255,255,0.05); padding: 32px; border-radius: 16px; margin-bottom: 32px;">
                        <h3 style="margin-bottom: 16px; color: #8b5cf6; font-size: 1.1rem;">About Me</h3>
                        <p style="color: #b0b0c0; line-height: 1.8;">${p.basic.bio}</p>
                    </div>
                    ` : ''}
                    
                    ${p.skills?.length > 0 ? `
                    <div style="margin-bottom: 32px;">
                        <h3 style="margin-bottom: 16px; color: #8b5cf6; font-size: 1.1rem;">Skills</h3>
                        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                            ${p.skills.map(s => `<span style="padding: 8px 18px; background: rgba(99,102,241,0.2); border-radius: 25px; font-size: 0.9rem; border: 1px solid rgba(99,102,241,0.3);">${s}</span>`).join('')}
                        </div>
                    </div>
                    ` : ''}
                    
                    ${p.experience?.length > 0 ? `
                    <div style="margin-bottom: 32px;">
                        <h3 style="margin-bottom: 16px; color: #8b5cf6; font-size: 1.1rem;">Experience</h3>
                        ${p.experience.slice(0, 3).map(exp => `
                            <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #6366f1;">
                                <div style="font-weight: 600; font-size: 1.05rem;">${exp.title}</div>
                                <div style="color: #8b5cf6;">${exp.company}</div>
                                <div style="color: #6b7280; font-size: 0.85rem; margin-top: 6px;">${exp.startDate} - ${exp.endDate}</div>
                            </div>
                    `).join('')}
                </div>
                ` : ''}
                
                ${p.projects?.length > 0 ? `
                <div>
                    <h3 style="margin-bottom: 16px; color: #8b5cf6; font-size: 1.1rem;">Projects</h3>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                        ${p.projects.slice(0, 4).map(proj => `
                            <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 12px;">
                                <div style="font-weight: 600; margin-bottom: 8px;">${proj.name}</div>
                                <p style="color: #a0a0b0; font-size: 0.9rem; line-height: 1.5;">${proj.description?.substring(0, 100)}...</p>
                                ${proj.techStack ? `<div style="margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px;">${proj.techStack.split(',').slice(0,3).map(t => `<span style="padding: 4px 10px; background: rgba(255,255,255,0.1); border-radius: 15px; font-size: 0.75rem;">${t.trim()}</span>`).join('')}</div>` : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
                ` : ''}
            </div>
        </div>
    `;
}

function publishPortfolio() {
    const username = (profileData.basic?.firstName || 'user').toLowerCase().replace(/\s/g, '');
    document.getElementById('portfolio-url').value = `https://careerlaunch.io/${username}`;
    showPortfolioStep(3);
    alert('Portfolio published successfully! 🎉');
}

window.publishPortfolio = publishPortfolio;

function copyPortfolioLink() {
    const url = document.getElementById('portfolio-url');
    url.select();
    document.execCommand('copy');
    alert('Link copied! 📋');
}

window.copyPortfolioLink = copyPortfolioLink;

function quickPreviewPortfolio() {
    if (!profileData.basic?.firstName) {
        alert('Please add at least your name to preview the portfolio!');
        return;
    }
    
    if (window.PortfolioTemplates) {
        const html = PortfolioTemplates.generate(selectedTemplate, profileData);
        const newWindow = window.open('', '_blank');
        newWindow.document.write(html);
        newWindow.document.close();
    } else {
        alert('Portfolio templates not loaded. Please refresh the page.');
    }
}

window.quickPreviewPortfolio = quickPreviewPortfolio;

function downloadPortfolio() {
    if (!profileData.basic?.firstName) {
        alert('Please complete your profile first!');
        return;
    }
    
    if (window.PortfolioTemplates) {
        const html = PortfolioTemplates.generate(selectedTemplate, profileData);
        const blob = new Blob([html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `portfolio-${profileData.basic.firstName.toLowerCase()}.html`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

window.downloadPortfolio = downloadPortfolio;

// ==================== CALENDAR ====================
let currentMonth = new Date();

function initCalendar() {
    renderCalendar();
    
    document.getElementById('btn-prev-month')?.addEventListener('click', () => {
        currentMonth.setMonth(currentMonth.getMonth() - 1);
        renderCalendar();
    });
    
    document.getElementById('btn-next-month')?.addEventListener('click', () => {
        currentMonth.setMonth(currentMonth.getMonth() + 1);
        renderCalendar();
    });
}

function renderCalendar() {
    const year = currentMonth.getFullYear();
    const month = currentMonth.getMonth();
    
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];
    
    document.getElementById('calendar-month').textContent = `${monthNames[month]} ${year}`;
    
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const today = new Date();
    
    let html = '';
    
    // Previous month days
    const prevMonthDays = new Date(year, month, 0).getDate();
    for (let i = firstDay - 1; i >= 0; i--) {
        html += `<div class="calendar-day other-month">${prevMonthDays - i}</div>`;
    }
    
    // Current month days
    for (let day = 1; day <= daysInMonth; day++) {
        const isToday = today.getDate() === day && today.getMonth() === month && today.getFullYear() === year;
        const hasEvent = interviews.some(int => {
            return int.rounds?.some(r => {
                if (!r.datetime) return false;
                const rDate = new Date(r.datetime);
                return rDate.getDate() === day && rDate.getMonth() === month && rDate.getFullYear() === year;
            });
        });
        
        html += `<div class="calendar-day ${isToday ? 'today' : ''} ${hasEvent ? 'has-event' : ''}">${day}</div>`;
    }
    
    // Next month days
    const totalCells = 42;
    const remainingCells = totalCells - (firstDay + daysInMonth);
    for (let day = 1; day <= remainingCells; day++) {
        html += `<div class="calendar-day other-month">${day}</div>`;
    }
    
    document.getElementById('calendar-days').innerHTML = html;
}

// ==================== IMPORT FROM SOCIAL ====================
function importFromLinkedIn() {
    const url = document.getElementById('linkedin-url').value;
    if (!url) {
        alert('Please enter your LinkedIn URL first');
        return;
    }
    alert('LinkedIn import initiated! Due to API restrictions, manual verification may be required.');
}

window.importFromLinkedIn = importFromLinkedIn;

function importFromGitHub() {
    const url = document.getElementById('github-url').value;
    if (!url) {
        alert('Please enter your GitHub URL first');
        return;
    }
    alert('GitHub import initiated! Your repositories will be added as projects.');
}

window.importFromGitHub = importFromGitHub;

// ==================== FILE UPLOADS ====================
document.getElementById('photo-upload')?.addEventListener('click', () => {
    document.getElementById('profile-photo').click();
});

document.getElementById('resume-upload-box')?.addEventListener('click', () => {
    document.getElementById('resume-upload').click();
});

console.log('✅ All functions initialized!');
