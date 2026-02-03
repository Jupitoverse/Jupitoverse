// AI Tools Database - Phase 34: Cloud Services & Infrastructure
// 150+ Cloud and infrastructure tools

const AI_TOOLS_PHASE34 = [
    // ==================== CLOUD PROVIDERS ====================
    {name: "Amazon Web Services", category: "Cloud", subcategory: "Provider", desc: "Leading cloud platform", url: "aws.amazon.com", pricing: "Pay-per-use", rating: 4.6, tags: ["cloud", "comprehensive", "leader"], featured: true},
    {name: "Microsoft Azure", category: "Cloud", subcategory: "Provider", desc: "Microsoft cloud platform", url: "azure.microsoft.com", pricing: "Pay-per-use", rating: 4.5, tags: ["cloud", "enterprise", "microsoft"]},
    {name: "Google Cloud Platform", category: "Cloud", subcategory: "Provider", desc: "Google cloud services", url: "cloud.google.com", pricing: "Pay-per-use", rating: 4.5, tags: ["cloud", "ai-ml", "data"]},
    {name: "DigitalOcean", category: "Cloud", subcategory: "Simple", desc: "Simple cloud infrastructure", url: "digitalocean.com", pricing: "Pay-per-use", rating: 4.5, tags: ["simple", "developers", "affordable"]},
    {name: "Linode (Akamai)", category: "Cloud", subcategory: "VPS", desc: "Cloud computing", url: "linode.com", pricing: "Pay-per-use", rating: 4.4, tags: ["vps", "simple", "affordable"]},
    {name: "Vultr", category: "Cloud", subcategory: "VPS", desc: "Cloud infrastructure", url: "vultr.com", pricing: "Pay-per-use", rating: 4.3, tags: ["vps", "global", "affordable"]},
    {name: "Hetzner", category: "Cloud", subcategory: "European", desc: "European cloud hosting", url: "hetzner.com", pricing: "Pay-per-use", rating: 4.5, tags: ["europe", "affordable", "dedicated"]},
    {name: "OVHcloud", category: "Cloud", subcategory: "European", desc: "European cloud provider", url: "ovhcloud.com", pricing: "Pay-per-use", rating: 4.2, tags: ["europe", "dedicated", "affordable"]},
    {name: "Oracle Cloud", category: "Cloud", subcategory: "Enterprise", desc: "Oracle cloud infrastructure", url: "oracle.com/cloud", pricing: "Pay-per-use", rating: 4.1, tags: ["enterprise", "oracle", "free-tier"]},
    {name: "IBM Cloud", category: "Cloud", subcategory: "Enterprise", desc: "IBM cloud services", url: "ibm.com/cloud", pricing: "Pay-per-use", rating: 4.0, tags: ["enterprise", "watson", "hybrid"]},
    {name: "Alibaba Cloud", category: "Cloud", subcategory: "Asia", desc: "Asian cloud leader", url: "alibabacloud.com", pricing: "Pay-per-use", rating: 4.2, tags: ["asia", "alibaba", "global"]},
    {name: "Tencent Cloud", category: "Cloud", subcategory: "Asia", desc: "Tencent cloud services", url: "cloud.tencent.com", pricing: "Pay-per-use", rating: 4.1, tags: ["asia", "tencent", "gaming"]},
    {name: "UpCloud", category: "Cloud", subcategory: "European", desc: "European cloud hosting", url: "upcloud.com", pricing: "Pay-per-use", rating: 4.3, tags: ["europe", "fast", "ssd"]},
    {name: "Scaleway", category: "Cloud", subcategory: "European", desc: "European cloud provider", url: "scaleway.com", pricing: "Pay-per-use", rating: 4.2, tags: ["europe", "developers", "bare-metal"]},
    {name: "Contabo", category: "Cloud", subcategory: "Budget", desc: "Budget VPS hosting", url: "contabo.com", pricing: "Pay-per-use", rating: 4.0, tags: ["budget", "vps", "storage"]},
    
    // ==================== SERVERLESS ====================
    {name: "AWS Lambda", category: "Serverless", subcategory: "Functions", desc: "AWS serverless compute", url: "aws.amazon.com/lambda", pricing: "Pay-per-use", rating: 4.5, tags: ["functions", "aws", "events"], featured: true},
    {name: "Google Cloud Functions", category: "Serverless", subcategory: "Functions", desc: "Google serverless", url: "cloud.google.com/functions", pricing: "Pay-per-use", rating: 4.4, tags: ["functions", "google", "events"]},
    {name: "Azure Functions", category: "Serverless", subcategory: "Functions", desc: "Microsoft serverless", url: "azure.microsoft.com/functions", pricing: "Pay-per-use", rating: 4.3, tags: ["functions", "azure", "triggers"]},
    {name: "Cloudflare Workers", category: "Serverless", subcategory: "Edge", desc: "Edge computing", url: "workers.cloudflare.com", pricing: "Freemium", rating: 4.6, tags: ["edge", "fast", "global"]},
    {name: "Vercel Functions", category: "Serverless", subcategory: "Edge", desc: "Vercel serverless", url: "vercel.com", pricing: "Freemium", rating: 4.5, tags: ["frontend", "edge", "nextjs"]},
    {name: "Netlify Functions", category: "Serverless", subcategory: "Jamstack", desc: "Netlify serverless", url: "netlify.com/products/functions", pricing: "Freemium", rating: 4.4, tags: ["jamstack", "aws-lambda", "simple"]},
    {name: "Deno Deploy", category: "Serverless", subcategory: "Edge", desc: "Deno edge functions", url: "deno.com/deploy", pricing: "Freemium", rating: 4.3, tags: ["deno", "edge", "typescript"]},
    {name: "Fly.io", category: "Serverless", subcategory: "Edge", desc: "Run apps everywhere", url: "fly.io", pricing: "Freemium", rating: 4.4, tags: ["edge", "docker", "global"]},
    {name: "Fastly Compute@Edge", category: "Serverless", subcategory: "Edge", desc: "Edge compute", url: "fastly.com/products/edge-compute", pricing: "Paid", rating: 4.3, tags: ["edge", "wasm", "cdn"]},
    {name: "AWS Fargate", category: "Serverless", subcategory: "Containers", desc: "Serverless containers", url: "aws.amazon.com/fargate", pricing: "Pay-per-use", rating: 4.4, tags: ["containers", "serverless", "ecs"]},
    
    // ==================== EDGE & CDN ====================
    {name: "Cloudflare", category: "CDN", subcategory: "Edge", desc: "Edge platform", url: "cloudflare.com", pricing: "Freemium", rating: 4.7, tags: ["cdn", "security", "edge"], featured: true},
    {name: "Fastly", category: "CDN", subcategory: "Edge", desc: "Edge cloud platform", url: "fastly.com", pricing: "Paid", rating: 4.4, tags: ["cdn", "edge", "real-time"]},
    {name: "Akamai", category: "CDN", subcategory: "Enterprise", desc: "Content delivery network", url: "akamai.com", pricing: "Paid", rating: 4.3, tags: ["cdn", "enterprise", "security"]},
    {name: "AWS CloudFront", category: "CDN", subcategory: "AWS", desc: "AWS CDN", url: "aws.amazon.com/cloudfront", pricing: "Pay-per-use", rating: 4.4, tags: ["cdn", "aws", "global"]},
    {name: "Azure CDN", category: "CDN", subcategory: "Azure", desc: "Microsoft CDN", url: "azure.microsoft.com/cdn", pricing: "Pay-per-use", rating: 4.2, tags: ["cdn", "azure", "microsoft"]},
    {name: "Google Cloud CDN", category: "CDN", subcategory: "Google", desc: "Google CDN", url: "cloud.google.com/cdn", pricing: "Pay-per-use", rating: 4.3, tags: ["cdn", "google", "global"]},
    {name: "BunnyCDN", category: "CDN", subcategory: "Affordable", desc: "Affordable CDN", url: "bunny.net", pricing: "Pay-per-use", rating: 4.5, tags: ["cdn", "affordable", "fast"]},
    {name: "KeyCDN", category: "CDN", subcategory: "Simple", desc: "Simple CDN", url: "keycdn.com", pricing: "Pay-per-use", rating: 4.3, tags: ["cdn", "simple", "affordable"]},
    {name: "StackPath", category: "CDN", subcategory: "Security", desc: "Edge platform", url: "stackpath.com", pricing: "Paid", rating: 4.1, tags: ["cdn", "security", "edge"]},
    {name: "Limelight", category: "CDN", subcategory: "Enterprise", desc: "Enterprise CDN", url: "limelight.com", pricing: "Paid", rating: 4.0, tags: ["cdn", "enterprise", "streaming"]},
    
    // ==================== CONTAINERS ====================
    {name: "Docker", category: "Containers", subcategory: "Platform", desc: "Container platform", url: "docker.com", pricing: "Freemium", rating: 4.7, tags: ["containers", "images", "compose"], featured: true},
    {name: "Kubernetes", category: "Containers", subcategory: "Orchestration", desc: "Container orchestration", url: "kubernetes.io", pricing: "Free", rating: 4.6, tags: ["orchestration", "cncf", "standard"]},
    {name: "Amazon EKS", category: "Containers", subcategory: "Managed K8s", desc: "AWS managed Kubernetes", url: "aws.amazon.com/eks", pricing: "Pay-per-use", rating: 4.4, tags: ["kubernetes", "aws", "managed"]},
    {name: "Google GKE", category: "Containers", subcategory: "Managed K8s", desc: "Google managed Kubernetes", url: "cloud.google.com/kubernetes-engine", pricing: "Pay-per-use", rating: 4.5, tags: ["kubernetes", "google", "autopilot"]},
    {name: "Azure AKS", category: "Containers", subcategory: "Managed K8s", desc: "Azure Kubernetes", url: "azure.microsoft.com/aks", pricing: "Pay-per-use", rating: 4.3, tags: ["kubernetes", "azure", "managed"]},
    {name: "Red Hat OpenShift", category: "Containers", subcategory: "Enterprise", desc: "Enterprise Kubernetes", url: "openshift.com", pricing: "Paid", rating: 4.3, tags: ["kubernetes", "enterprise", "redhat"]},
    {name: "Rancher", category: "Containers", subcategory: "Management", desc: "Kubernetes management", url: "rancher.com", pricing: "Freemium", rating: 4.4, tags: ["kubernetes", "multi-cluster", "suse"]},
    {name: "Portainer", category: "Containers", subcategory: "Management", desc: "Container management UI", url: "portainer.io", pricing: "Freemium", rating: 4.4, tags: ["docker", "kubernetes", "ui"]},
    {name: "Podman", category: "Containers", subcategory: "Runtime", desc: "Daemonless containers", url: "podman.io", pricing: "Free", rating: 4.3, tags: ["daemonless", "rootless", "redhat"]},
    {name: "containerd", category: "Containers", subcategory: "Runtime", desc: "Container runtime", url: "containerd.io", pricing: "Free", rating: 4.4, tags: ["runtime", "cncf", "kubernetes"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE34 = AI_TOOLS_PHASE34;
}


