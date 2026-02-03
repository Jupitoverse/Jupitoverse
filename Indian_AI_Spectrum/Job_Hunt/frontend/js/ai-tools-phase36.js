// AI Tools Database - Phase 36: Security & Authentication Tools
// 150+ Security and auth tools

const AI_TOOLS_PHASE36 = [
    // ==================== AUTHENTICATION ====================
    {name: "Auth0", category: "Authentication", subcategory: "Identity", desc: "Identity platform", url: "auth0.com", pricing: "Freemium", rating: 4.6, tags: ["identity", "sso", "enterprise"], featured: true},
    {name: "Okta", category: "Authentication", subcategory: "Enterprise", desc: "Identity management", url: "okta.com", pricing: "Paid", rating: 4.5, tags: ["enterprise", "sso", "workforce"]},
    {name: "Firebase Auth", category: "Authentication", subcategory: "Google", desc: "Google authentication", url: "firebase.google.com/auth", pricing: "Freemium", rating: 4.5, tags: ["firebase", "mobile", "social"]},
    {name: "AWS Cognito", category: "Authentication", subcategory: "AWS", desc: "AWS identity", url: "aws.amazon.com/cognito", pricing: "Freemium", rating: 4.3, tags: ["aws", "user-pools", "federated"]},
    {name: "Clerk", category: "Authentication", subcategory: "Modern", desc: "User management", url: "clerk.com", pricing: "Freemium", rating: 4.5, tags: ["modern", "react", "components"]},
    {name: "Supabase Auth", category: "Authentication", subcategory: "Open Source", desc: "Supabase auth", url: "supabase.com/auth", pricing: "Freemium", rating: 4.4, tags: ["open-source", "postgres", "row-level"]},
    {name: "Stytch", category: "Authentication", subcategory: "Passwordless", desc: "Passwordless auth", url: "stytch.com", pricing: "Freemium", rating: 4.3, tags: ["passwordless", "api", "modern"]},
    {name: "Magic", category: "Authentication", subcategory: "Passwordless", desc: "Passwordless login", url: "magic.link", pricing: "Freemium", rating: 4.2, tags: ["passwordless", "web3", "blockchain"]},
    {name: "Descope", category: "Authentication", subcategory: "No-Code", desc: "Drag-drop auth flows", url: "descope.com", pricing: "Freemium", rating: 4.2, tags: ["no-code", "flows", "visual"]},
    {name: "WorkOS", category: "Authentication", subcategory: "Enterprise", desc: "Enterprise-ready auth", url: "workos.com", pricing: "Freemium", rating: 4.4, tags: ["enterprise", "sso", "directory-sync"]},
    {name: "OneLogin", category: "Authentication", subcategory: "Enterprise", desc: "IAM platform", url: "onelogin.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "sso", "iam"]},
    {name: "Ping Identity", category: "Authentication", subcategory: "Enterprise", desc: "Enterprise identity", url: "pingidentity.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "iam", "federation"]},
    {name: "FusionAuth", category: "Authentication", subcategory: "Self-Hosted", desc: "Auth for developers", url: "fusionauth.io", pricing: "Freemium", rating: 4.3, tags: ["self-hosted", "api", "flexible"]},
    {name: "Keycloak", category: "Authentication", subcategory: "Open Source", desc: "Open source IAM", url: "keycloak.org", pricing: "Free", rating: 4.4, tags: ["open-source", "redhat", "sso"]},
    {name: "Ory", category: "Authentication", subcategory: "Open Source", desc: "Identity infrastructure", url: "ory.sh", pricing: "Freemium", rating: 4.3, tags: ["open-source", "cloud-native", "zero-trust"]},
    
    // ==================== SECURITY TOOLS ====================
    {name: "Snyk", category: "Security", subcategory: "DevSecOps", desc: "Developer security", url: "snyk.io", pricing: "Freemium", rating: 4.6, tags: ["devsecops", "vulnerabilities", "scanning"], featured: true},
    {name: "SonarQube", category: "Security", subcategory: "Code Analysis", desc: "Code quality & security", url: "sonarqube.org", pricing: "Freemium", rating: 4.5, tags: ["code-quality", "sast", "analysis"]},
    {name: "Veracode", category: "Security", subcategory: "AppSec", desc: "Application security", url: "veracode.com", pricing: "Paid", rating: 4.3, tags: ["appsec", "enterprise", "sast-dast"]},
    {name: "Checkmarx", category: "Security", subcategory: "AppSec", desc: "Application security", url: "checkmarx.com", pricing: "Paid", rating: 4.2, tags: ["appsec", "enterprise", "sast"]},
    {name: "Dependabot", category: "Security", subcategory: "Dependencies", desc: "Dependency updates", url: "github.com/dependabot", pricing: "Free", rating: 4.5, tags: ["dependencies", "github", "automated"]},
    {name: "Renovate", category: "Security", subcategory: "Dependencies", desc: "Dependency updates", url: "renovatebot.com", pricing: "Free", rating: 4.5, tags: ["dependencies", "multi-platform", "configurable"]},
    {name: "Trivy", category: "Security", subcategory: "Container", desc: "Container scanner", url: "aquasecurity.github.io/trivy", pricing: "Free", rating: 4.5, tags: ["container", "scanner", "aqua"]},
    {name: "Grype", category: "Security", subcategory: "Container", desc: "Vulnerability scanner", url: "github.com/anchore/grype", pricing: "Free", rating: 4.3, tags: ["vulnerabilities", "sbom", "anchore"]},
    {name: "OWASP ZAP", category: "Security", subcategory: "DAST", desc: "Web app scanner", url: "owasp.org/zap", pricing: "Free", rating: 4.4, tags: ["dast", "owasp", "penetration"]},
    {name: "Burp Suite", category: "Security", subcategory: "Pentest", desc: "Web security testing", url: "portswigger.net/burp", pricing: "Freemium", rating: 4.6, tags: ["pentest", "professional", "security"]},
    {name: "HashiCorp Vault", category: "Security", subcategory: "Secrets", desc: "Secrets management", url: "vaultproject.io", pricing: "Freemium", rating: 4.6, tags: ["secrets", "encryption", "hashicorp"]},
    {name: "AWS Secrets Manager", category: "Security", subcategory: "Secrets", desc: "AWS secrets", url: "aws.amazon.com/secrets-manager", pricing: "Pay-per-use", rating: 4.4, tags: ["aws", "secrets", "rotation"]},
    {name: "Doppler", category: "Security", subcategory: "Secrets", desc: "Secrets management", url: "doppler.com", pricing: "Freemium", rating: 4.4, tags: ["secrets", "sync", "developer"]},
    {name: "Infisical", category: "Security", subcategory: "Secrets", desc: "Open source secrets", url: "infisical.com", pricing: "Freemium", rating: 4.3, tags: ["open-source", "secrets", "sync"]},
    {name: "CrowdStrike", category: "Security", subcategory: "Endpoint", desc: "Endpoint security", url: "crowdstrike.com", pricing: "Paid", rating: 4.5, tags: ["endpoint", "ai", "enterprise"]},
    
    // ==================== NETWORK SECURITY ====================
    {name: "Cloudflare Security", category: "Security", subcategory: "WAF", desc: "Web security", url: "cloudflare.com/security", pricing: "Freemium", rating: 4.6, tags: ["waf", "ddos", "bot"], featured: true},
    {name: "AWS WAF", category: "Security", subcategory: "WAF", desc: "AWS web firewall", url: "aws.amazon.com/waf", pricing: "Pay-per-use", rating: 4.3, tags: ["waf", "aws", "rules"]},
    {name: "Imperva", category: "Security", subcategory: "WAF", desc: "Application security", url: "imperva.com", pricing: "Paid", rating: 4.2, tags: ["waf", "ddos", "enterprise"]},
    {name: "Signal Sciences", category: "Security", subcategory: "WAF", desc: "Next-gen WAF", url: "signalsciences.com", pricing: "Paid", rating: 4.3, tags: ["waf", "fastly", "real-time"]},
    {name: "Tailscale", category: "Security", subcategory: "VPN", desc: "Zero-config VPN", url: "tailscale.com", pricing: "Freemium", rating: 4.7, tags: ["vpn", "wireguard", "zero-config"]},
    {name: "WireGuard", category: "Security", subcategory: "VPN", desc: "Modern VPN protocol", url: "wireguard.com", pricing: "Free", rating: 4.6, tags: ["vpn", "protocol", "fast"]},
    {name: "Twingate", category: "Security", subcategory: "ZTNA", desc: "Zero trust access", url: "twingate.com", pricing: "Freemium", rating: 4.4, tags: ["ztna", "zero-trust", "remote"]},
    {name: "Zscaler", category: "Security", subcategory: "SASE", desc: "Cloud security", url: "zscaler.com", pricing: "Paid", rating: 4.3, tags: ["sase", "zero-trust", "enterprise"]},
    {name: "Netskope", category: "Security", subcategory: "SASE", desc: "SASE platform", url: "netskope.com", pricing: "Paid", rating: 4.2, tags: ["sase", "casb", "dlp"]},
    {name: "Palo Alto Prisma", category: "Security", subcategory: "Cloud", desc: "Cloud security", url: "paloaltonetworks.com/prisma", pricing: "Paid", rating: 4.3, tags: ["cloud", "security", "enterprise"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE36 = AI_TOOLS_PHASE36;
}


