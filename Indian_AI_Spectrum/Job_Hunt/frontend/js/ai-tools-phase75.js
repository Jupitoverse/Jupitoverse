// AI Tools Database - Phase 75: More Security & Privacy AI
// 100+ Additional security and privacy AI tools

const AI_TOOLS_PHASE75 = [
    // ==================== CYBERSECURITY ====================
    {name: "CrowdStrike", category: "Security", subcategory: "Endpoint", desc: "Endpoint protection", url: "crowdstrike.com", pricing: "Enterprise", rating: 4.6, tags: ["endpoint", "edr", "cloud"], featured: true},
    {name: "SentinelOne", category: "Security", subcategory: "Endpoint", desc: "AI security platform", url: "sentinelone.com", pricing: "Enterprise", rating: 4.5, tags: ["endpoint", "ai", "autonomous"]},
    {name: "Darktrace", category: "Security", subcategory: "Threat Detection", desc: "AI cyber defense", url: "darktrace.com", pricing: "Enterprise", rating: 4.4, tags: ["ai", "threat-detection", "self-learning"]},
    {name: "Palo Alto Networks", category: "Security", subcategory: "Firewall", desc: "Network security", url: "paloaltonetworks.com", pricing: "Enterprise", rating: 4.5, tags: ["firewall", "ngfw", "cloud"]},
    {name: "Fortinet", category: "Security", subcategory: "Network", desc: "Network security", url: "fortinet.com", pricing: "Enterprise", rating: 4.4, tags: ["firewall", "utm", "sd-wan"]},
    {name: "Zscaler", category: "Security", subcategory: "Cloud Security", desc: "Cloud security", url: "zscaler.com", pricing: "Enterprise", rating: 4.4, tags: ["cloud", "sase", "zero-trust"]},
    {name: "Cloudflare", category: "Security", subcategory: "Web Security", desc: "Web security & CDN", url: "cloudflare.com", pricing: "Freemium", rating: 4.6, tags: ["cdn", "ddos", "waf"]},
    {name: "Okta", category: "Security", subcategory: "Identity", desc: "Identity management", url: "okta.com", pricing: "Enterprise", rating: 4.5, tags: ["identity", "sso", "iam"]},
    {name: "Auth0", category: "Security", subcategory: "Identity", desc: "Identity platform", url: "auth0.com", pricing: "Freemium", rating: 4.5, tags: ["identity", "authentication", "developers"]},
    {name: "Duo Security", category: "Security", subcategory: "MFA", desc: "Multi-factor auth", url: "duo.com", pricing: "Freemium", rating: 4.4, tags: ["mfa", "cisco", "access"]},
    {name: "Ping Identity", category: "Security", subcategory: "Identity", desc: "Identity security", url: "pingidentity.com", pricing: "Enterprise", rating: 4.2, tags: ["identity", "sso", "enterprise"]},
    
    // ==================== VULNERABILITY & THREAT ====================
    {name: "Tenable", category: "Security", subcategory: "Vulnerability", desc: "Vulnerability management", url: "tenable.com", pricing: "Paid", rating: 4.4, tags: ["vulnerability", "nessus", "exposure"], featured: true},
    {name: "Qualys", category: "Security", subcategory: "Vulnerability", desc: "Cloud security", url: "qualys.com", pricing: "Enterprise", rating: 4.3, tags: ["vulnerability", "cloud", "compliance"]},
    {name: "Rapid7", category: "Security", subcategory: "Vulnerability", desc: "Security analytics", url: "rapid7.com", pricing: "Enterprise", rating: 4.3, tags: ["vulnerability", "siem", "detection"]},
    {name: "Snyk", category: "Security", subcategory: "DevSecOps", desc: "Developer security", url: "snyk.io", pricing: "Freemium", rating: 4.5, tags: ["devsecops", "code", "containers"]},
    {name: "Checkmarx", category: "Security", subcategory: "SAST", desc: "Application security", url: "checkmarx.com", pricing: "Enterprise", rating: 4.2, tags: ["sast", "code-scanning", "appsec"]},
    {name: "Veracode", category: "Security", subcategory: "AppSec", desc: "Application security", url: "veracode.com", pricing: "Enterprise", rating: 4.2, tags: ["appsec", "sast", "dast"]},
    {name: "Burp Suite", category: "Security", subcategory: "Pentesting", desc: "Web security testing", url: "portswigger.net", pricing: "Freemium", rating: 4.6, tags: ["pentesting", "web", "proxy"]},
    {name: "Nmap", category: "Security", subcategory: "Scanning", desc: "Network scanner", url: "nmap.org", pricing: "Free", rating: 4.7, tags: ["scanning", "open-source", "network"]},
    {name: "Metasploit", category: "Security", subcategory: "Pentesting", desc: "Penetration testing", url: "metasploit.com", pricing: "Freemium", rating: 4.5, tags: ["pentesting", "exploit", "framework"]},
    
    // ==================== SIEM & MONITORING ====================
    {name: "Splunk", category: "Security", subcategory: "SIEM", desc: "Security analytics", url: "splunk.com", pricing: "Enterprise", rating: 4.5, tags: ["siem", "analytics", "observability"], featured: true},
    {name: "Elastic Security", category: "Security", subcategory: "SIEM", desc: "SIEM & XDR", url: "elastic.co/security", pricing: "Freemium", rating: 4.4, tags: ["siem", "elastic", "xdr"]},
    {name: "IBM QRadar", category: "Security", subcategory: "SIEM", desc: "Security intelligence", url: "ibm.com/qradar", pricing: "Enterprise", rating: 4.2, tags: ["siem", "ibm", "analytics"]},
    {name: "Microsoft Sentinel", category: "Security", subcategory: "SIEM", desc: "Cloud SIEM", url: "azure.microsoft.com/sentinel", pricing: "Pay-per-use", rating: 4.3, tags: ["siem", "azure", "cloud"]},
    {name: "Sumo Logic", category: "Security", subcategory: "SIEM", desc: "Cloud monitoring", url: "sumologic.com", pricing: "Freemium", rating: 4.2, tags: ["siem", "cloud", "observability"]},
    {name: "LogRhythm", category: "Security", subcategory: "SIEM", desc: "SIEM platform", url: "logrhythm.com", pricing: "Enterprise", rating: 4.1, tags: ["siem", "analytics", "compliance"]},
    {name: "Datadog Security", category: "Security", subcategory: "Monitoring", desc: "Cloud security", url: "datadoghq.com/security", pricing: "Paid", rating: 4.4, tags: ["monitoring", "cloud", "observability"]},
    
    // ==================== PRIVACY & COMPLIANCE ====================
    {name: "OneTrust", category: "Security", subcategory: "Privacy", desc: "Privacy management", url: "onetrust.com", pricing: "Enterprise", rating: 4.3, tags: ["privacy", "gdpr", "compliance"], featured: true},
    {name: "TrustArc", category: "Security", subcategory: "Privacy", desc: "Privacy platform", url: "trustarc.com", pricing: "Enterprise", rating: 4.1, tags: ["privacy", "compliance", "gdpr"]},
    {name: "BigID", category: "Security", subcategory: "Privacy", desc: "Data intelligence", url: "bigid.com", pricing: "Enterprise", rating: 4.2, tags: ["privacy", "data-discovery", "ai"]},
    {name: "Privitar", category: "Security", subcategory: "Data Privacy", desc: "Data privacy", url: "privitar.com", pricing: "Enterprise", rating: 4.1, tags: ["privacy", "anonymization", "data"]},
    {name: "Cookiebot", category: "Security", subcategory: "Consent", desc: "Cookie consent", url: "cookiebot.com", pricing: "Freemium", rating: 4.2, tags: ["consent", "cookies", "gdpr"]},
    {name: "Osano", category: "Security", subcategory: "Privacy", desc: "Data privacy platform", url: "osano.com", pricing: "Freemium", rating: 4.1, tags: ["privacy", "consent", "compliance"]},
    {name: "Termly", category: "Security", subcategory: "Compliance", desc: "Privacy policies", url: "termly.io", pricing: "Freemium", rating: 4.2, tags: ["privacy-policy", "gdpr", "generator"]},
    
    // ==================== PASSWORD & SECRETS ====================
    {name: "1Password", category: "Security", subcategory: "Password", desc: "Password manager", url: "1password.com", pricing: "Paid", rating: 4.7, tags: ["password", "team", "enterprise"], featured: true},
    {name: "LastPass", category: "Security", subcategory: "Password", desc: "Password manager", url: "lastpass.com", pricing: "Freemium", rating: 4.2, tags: ["password", "free", "business"]},
    {name: "Dashlane", category: "Security", subcategory: "Password", desc: "Password manager", url: "dashlane.com", pricing: "Freemium", rating: 4.4, tags: ["password", "vpn", "dark-web"]},
    {name: "Bitwarden", category: "Security", subcategory: "Password", desc: "Open-source password", url: "bitwarden.com", pricing: "Freemium", rating: 4.6, tags: ["password", "open-source", "free"]},
    {name: "Keeper", category: "Security", subcategory: "Password", desc: "Password security", url: "keepersecurity.com", pricing: "Paid", rating: 4.4, tags: ["password", "enterprise", "secrets"]},
    {name: "HashiCorp Vault", category: "Security", subcategory: "Secrets", desc: "Secrets management", url: "vaultproject.io", pricing: "Freemium", rating: 4.5, tags: ["secrets", "hashicorp", "enterprise"]},
    {name: "AWS Secrets Manager", category: "Security", subcategory: "Secrets", desc: "AWS secrets", url: "aws.amazon.com/secrets-manager", pricing: "Pay-per-use", rating: 4.3, tags: ["secrets", "aws", "rotation"]},
    {name: "Doppler", category: "Security", subcategory: "Secrets", desc: "Secrets platform", url: "doppler.com", pricing: "Freemium", rating: 4.4, tags: ["secrets", "env-vars", "syncing"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE75 = AI_TOOLS_PHASE75;
}


