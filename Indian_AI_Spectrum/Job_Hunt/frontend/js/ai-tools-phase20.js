// AI Tools Database - Phase 20: Security, Privacy & Compliance AI
// 200+ Tools for cybersecurity and compliance

const AI_TOOLS_PHASE20 = [
    // ==================== CYBERSECURITY ====================
    {name: "CrowdStrike", category: "Security", subcategory: "Endpoint", desc: "Cloud-native endpoint security", url: "crowdstrike.com", pricing: "Paid", rating: 4.6, tags: ["endpoint", "ai", "edr"], featured: true},
    {name: "Palo Alto Networks", category: "Security", subcategory: "Network", desc: "Network security platform", url: "paloaltonetworks.com", pricing: "Paid", rating: 4.5, tags: ["firewall", "network", "ai"]},
    {name: "SentinelOne", category: "Security", subcategory: "Endpoint", desc: "AI-powered endpoint protection", url: "sentinelone.com", pricing: "Paid", rating: 4.5, tags: ["endpoint", "xdr", "ai"]},
    {name: "Darktrace", category: "Security", subcategory: "AI Security", desc: "AI cybersecurity platform", url: "darktrace.com", pricing: "Paid", rating: 4.4, tags: ["ai", "threat-detection", "autonomous"]},
    {name: "Cylance", category: "Security", subcategory: "AI Antivirus", desc: "AI-based antivirus", url: "blackberry.com/us/en/products/cylance", pricing: "Paid", rating: 4.2, tags: ["ai", "antivirus", "blackberry"]},
    {name: "Fortinet", category: "Security", subcategory: "Network", desc: "Network security solutions", url: "fortinet.com", pricing: "Paid", rating: 4.4, tags: ["firewall", "sd-wan", "sase"]},
    {name: "Cisco Security", category: "Security", subcategory: "Network", desc: "Cisco security solutions", url: "cisco.com/security", pricing: "Paid", rating: 4.3, tags: ["network", "enterprise", "cisco"]},
    {name: "Splunk", category: "Security", subcategory: "SIEM", desc: "Security monitoring platform", url: "splunk.com", pricing: "Paid", rating: 4.4, tags: ["siem", "analytics", "observability"]},
    {name: "Elastic Security", category: "Security", subcategory: "SIEM", desc: "Open security platform", url: "elastic.co/security", pricing: "Freemium", rating: 4.4, tags: ["siem", "open-source", "elastic"]},
    {name: "IBM Security", category: "Security", subcategory: "Enterprise", desc: "IBM security solutions", url: "ibm.com/security", pricing: "Paid", rating: 4.2, tags: ["enterprise", "watson", "qradar"]},
    {name: "Microsoft Defender", category: "Security", subcategory: "Endpoint", desc: "Microsoft security suite", url: "microsoft.com/security", pricing: "Freemium", rating: 4.4, tags: ["microsoft", "endpoint", "cloud"]},
    {name: "Rapid7", category: "Security", subcategory: "Vulnerability", desc: "Security analytics", url: "rapid7.com", pricing: "Paid", rating: 4.3, tags: ["vulnerability", "detection", "response"]},
    {name: "Qualys", category: "Security", subcategory: "Vulnerability", desc: "Cloud security platform", url: "qualys.com", pricing: "Paid", rating: 4.3, tags: ["vulnerability", "cloud", "compliance"]},
    {name: "Tenable", category: "Security", subcategory: "Vulnerability", desc: "Exposure management", url: "tenable.com", pricing: "Paid", rating: 4.3, tags: ["vulnerability", "nessus", "exposure"]},
    {name: "Vectra AI", category: "Security", subcategory: "Detection", desc: "AI threat detection", url: "vectra.ai", pricing: "Paid", rating: 4.4, tags: ["ai", "ndr", "threat-detection"]},
    
    // ==================== IDENTITY & ACCESS ====================
    {name: "Okta", category: "Identity", subcategory: "IAM", desc: "Identity management", url: "okta.com", pricing: "Paid", rating: 4.5, tags: ["iam", "sso", "mfa"], featured: true},
    {name: "Auth0", category: "Identity", subcategory: "Authentication", desc: "Authentication platform", url: "auth0.com", pricing: "Freemium", rating: 4.6, tags: ["auth", "okta", "developer"]},
    {name: "Ping Identity", category: "Identity", subcategory: "IAM", desc: "Intelligent identity", url: "pingidentity.com", pricing: "Paid", rating: 4.3, tags: ["iam", "sso", "enterprise"]},
    {name: "OneLogin", category: "Identity", subcategory: "IAM", desc: "Cloud identity platform", url: "onelogin.com", pricing: "Paid", rating: 4.2, tags: ["iam", "sso", "directory"]},
    {name: "JumpCloud", category: "Identity", subcategory: "Directory", desc: "Cloud directory platform", url: "jumpcloud.com", pricing: "Freemium", rating: 4.3, tags: ["directory", "mdm", "ldap"]},
    {name: "CyberArk", category: "Identity", subcategory: "PAM", desc: "Privileged access management", url: "cyberark.com", pricing: "Paid", rating: 4.3, tags: ["pam", "secrets", "enterprise"]},
    {name: "1Password", category: "Identity", subcategory: "Passwords", desc: "Password manager", url: "1password.com", pricing: "Paid", rating: 4.7, tags: ["passwords", "teams", "secure"]},
    {name: "Bitwarden", category: "Identity", subcategory: "Passwords", desc: "Open source password manager", url: "bitwarden.com", pricing: "Freemium", rating: 4.6, tags: ["passwords", "open-source", "self-host"]},
    {name: "LastPass", category: "Identity", subcategory: "Passwords", desc: "Password manager", url: "lastpass.com", pricing: "Freemium", rating: 4.1, tags: ["passwords", "enterprise", "legacy"]},
    {name: "Dashlane", category: "Identity", subcategory: "Passwords", desc: "Password manager", url: "dashlane.com", pricing: "Freemium", rating: 4.3, tags: ["passwords", "vpn", "business"]},
    {name: "Keeper", category: "Identity", subcategory: "Passwords", desc: "Password security", url: "keepersecurity.com", pricing: "Paid", rating: 4.4, tags: ["passwords", "enterprise", "secrets"]},
    {name: "Stytch", category: "Identity", subcategory: "Auth API", desc: "Authentication infrastructure", url: "stytch.com", pricing: "Freemium", rating: 4.4, tags: ["auth", "api", "passwordless"]},
    {name: "Clerk", category: "Identity", subcategory: "Auth API", desc: "Complete user management", url: "clerk.com", pricing: "Freemium", rating: 4.6, tags: ["auth", "react", "developer"]},
    {name: "Descope", category: "Identity", subcategory: "Auth", desc: "Drag-and-drop authentication", url: "descope.com", pricing: "Freemium", rating: 4.3, tags: ["auth", "no-code", "flows"]},
    {name: "WorkOS", category: "Identity", subcategory: "Enterprise", desc: "Enterprise-ready auth", url: "workos.com", pricing: "Freemium", rating: 4.5, tags: ["sso", "directory-sync", "enterprise"]},
    
    // ==================== PRIVACY & COMPLIANCE ====================
    {name: "OneTrust", category: "Privacy", subcategory: "Privacy", desc: "Privacy management platform", url: "onetrust.com", pricing: "Paid", rating: 4.3, tags: ["privacy", "gdpr", "consent"], featured: true},
    {name: "TrustArc", category: "Privacy", subcategory: "Privacy", desc: "Privacy compliance platform", url: "trustarc.com", pricing: "Paid", rating: 4.2, tags: ["privacy", "compliance", "consent"]},
    {name: "BigID", category: "Privacy", subcategory: "Data Discovery", desc: "Data intelligence platform", url: "bigid.com", pricing: "Paid", rating: 4.3, tags: ["data-discovery", "privacy", "ai"]},
    {name: "Transcend", category: "Privacy", subcategory: "Privacy", desc: "Data privacy infrastructure", url: "transcend.io", pricing: "Paid", rating: 4.4, tags: ["privacy", "requests", "developer"]},
    {name: "Ethyca", category: "Privacy", subcategory: "Data Privacy", desc: "Privacy engineering platform", url: "ethyca.com", pricing: "Freemium", rating: 4.3, tags: ["privacy", "fides", "open-source"]},
    {name: "Cookiebot", category: "Privacy", subcategory: "Consent", desc: "Cookie consent solution", url: "cookiebot.com", pricing: "Freemium", rating: 4.2, tags: ["cookies", "consent", "gdpr"]},
    {name: "Termly", category: "Privacy", subcategory: "Compliance", desc: "Privacy policy generator", url: "termly.io", pricing: "Freemium", rating: 4.2, tags: ["policies", "consent", "generator"]},
    {name: "Iubenda", category: "Privacy", subcategory: "Compliance", desc: "Privacy and compliance", url: "iubenda.com", pricing: "Freemium", rating: 4.3, tags: ["policies", "consent", "gdpr"]},
    {name: "Osano", category: "Privacy", subcategory: "Consent", desc: "Data privacy platform", url: "osano.com", pricing: "Freemium", rating: 4.2, tags: ["consent", "vendor-risk", "privacy"]},
    {name: "Privy", category: "Privacy", subcategory: "Consent", desc: "Privacy consent management", url: "privy.com", pricing: "Freemium", rating: 4.0, tags: ["consent", "marketing", "popups"]},
    {name: "Vanta", category: "Compliance", subcategory: "SOC 2", desc: "Security compliance automation", url: "vanta.com", pricing: "Paid", rating: 4.5, tags: ["soc2", "compliance", "automation"], featured: true},
    {name: "Drata", category: "Compliance", subcategory: "SOC 2", desc: "Compliance automation", url: "drata.com", pricing: "Paid", rating: 4.5, tags: ["soc2", "iso", "automation"]},
    {name: "Secureframe", category: "Compliance", subcategory: "SOC 2", desc: "Security compliance platform", url: "secureframe.com", pricing: "Paid", rating: 4.4, tags: ["soc2", "hipaa", "automation"]},
    {name: "Laika", category: "Compliance", subcategory: "SOC 2", desc: "Compliance automation", url: "heylaika.com", pricing: "Paid", rating: 4.3, tags: ["soc2", "compliance", "workflow"]},
    {name: "Sprinto", category: "Compliance", subcategory: "SOC 2", desc: "Compliance automation", url: "sprinto.com", pricing: "Paid", rating: 4.4, tags: ["soc2", "iso", "automation"]},
    
    // ==================== AI SECURITY ====================
    {name: "HiddenLayer", category: "AI Security", subcategory: "ML Security", desc: "AI security platform", url: "hiddenlayer.com", pricing: "Paid", rating: 4.3, tags: ["ml-security", "adversarial", "protection"]},
    {name: "Robust Intelligence", category: "AI Security", subcategory: "ML Testing", desc: "ML risk management", url: "robustintelligence.com", pricing: "Paid", rating: 4.3, tags: ["ml-testing", "risk", "validation"]},
    {name: "Protect AI", category: "AI Security", subcategory: "ML Security", desc: "AI security platform", url: "protectai.com", pricing: "Paid", rating: 4.2, tags: ["ml-security", "supply-chain", "scanning"]},
    {name: "CalypsoAI", category: "AI Security", subcategory: "LLM Security", desc: "LLM security platform", url: "calypsoai.com", pricing: "Paid", rating: 4.2, tags: ["llm", "security", "governance"]},
    {name: "LakeraGuard", category: "AI Security", subcategory: "LLM Security", desc: "LLM security guard", url: "lakera.ai", pricing: "Freemium", rating: 4.3, tags: ["llm", "prompt-injection", "security"]},
    {name: "Rebuff", category: "AI Security", subcategory: "Prompt Security", desc: "Prompt injection detection", url: "rebuff.ai", pricing: "Free", rating: 4.1, tags: ["prompt-injection", "open-source", "detection"]},
    {name: "Arthur AI", category: "AI Security", subcategory: "Monitoring", desc: "AI performance monitoring", url: "arthur.ai", pricing: "Paid", rating: 4.3, tags: ["monitoring", "fairness", "explainability"]},
    {name: "Fiddler AI", category: "AI Security", subcategory: "Monitoring", desc: "ML monitoring and explainability", url: "fiddler.ai", pricing: "Paid", rating: 4.2, tags: ["monitoring", "explainability", "drift"]},
    {name: "Arize AI", category: "AI Security", subcategory: "Observability", desc: "ML observability platform", url: "arize.com", pricing: "Freemium", rating: 4.4, tags: ["observability", "monitoring", "troubleshooting"]},
    {name: "WhyLabs", category: "AI Security", subcategory: "Monitoring", desc: "AI observability platform", url: "whylabs.ai", pricing: "Freemium", rating: 4.3, tags: ["observability", "profiling", "monitoring"]},
    
    // ==================== VPN & ENCRYPTION ====================
    {name: "NordVPN", category: "VPN", subcategory: "Consumer", desc: "VPN service", url: "nordvpn.com", pricing: "Paid", rating: 4.5, tags: ["vpn", "privacy", "security"]},
    {name: "ExpressVPN", category: "VPN", subcategory: "Consumer", desc: "Fast VPN service", url: "expressvpn.com", pricing: "Paid", rating: 4.5, tags: ["vpn", "fast", "streaming"]},
    {name: "Surfshark", category: "VPN", subcategory: "Consumer", desc: "Affordable VPN", url: "surfshark.com", pricing: "Paid", rating: 4.4, tags: ["vpn", "affordable", "unlimited"]},
    {name: "ProtonVPN", category: "VPN", subcategory: "Privacy", desc: "Privacy-focused VPN", url: "protonvpn.com", pricing: "Freemium", rating: 4.5, tags: ["vpn", "privacy", "swiss"]},
    {name: "Mullvad", category: "VPN", subcategory: "Privacy", desc: "Anonymous VPN", url: "mullvad.net", pricing: "Paid", rating: 4.6, tags: ["vpn", "anonymous", "privacy"]},
    {name: "Tailscale", category: "VPN", subcategory: "Mesh", desc: "Mesh VPN", url: "tailscale.com", pricing: "Freemium", rating: 4.7, tags: ["mesh", "wireguard", "simple"]},
    {name: "Cloudflare WARP", category: "VPN", subcategory: "Free", desc: "Free VPN by Cloudflare", url: "1.1.1.1", pricing: "Freemium", rating: 4.3, tags: ["free", "cloudflare", "fast"]},
    {name: "Perimeter 81", category: "VPN", subcategory: "Business", desc: "Business VPN", url: "perimeter81.com", pricing: "Paid", rating: 4.2, tags: ["business", "sase", "zero-trust"]},
    {name: "Zscaler", category: "VPN", subcategory: "Enterprise", desc: "Zero trust exchange", url: "zscaler.com", pricing: "Paid", rating: 4.3, tags: ["zero-trust", "enterprise", "sase"]},
    {name: "Signal", category: "Encryption", subcategory: "Messaging", desc: "Encrypted messaging", url: "signal.org", pricing: "Free", rating: 4.7, tags: ["messaging", "encrypted", "privacy"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE20 = AI_TOOLS_PHASE20;
}


