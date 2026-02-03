// AI Tools Database - Phase 35: DevOps & CI/CD Tools
// 150+ DevOps and CI/CD tools

const AI_TOOLS_PHASE35 = [
    // ==================== CI/CD PLATFORMS ====================
    {name: "GitHub Actions", category: "CI/CD", subcategory: "GitHub", desc: "GitHub automation", url: "github.com/features/actions", pricing: "Freemium", rating: 4.6, tags: ["github", "workflows", "automation"], featured: true},
    {name: "GitLab CI", category: "CI/CD", subcategory: "GitLab", desc: "GitLab pipelines", url: "docs.gitlab.com/ee/ci", pricing: "Freemium", rating: 4.5, tags: ["gitlab", "pipelines", "devops"]},
    {name: "Jenkins", category: "CI/CD", subcategory: "Self-Hosted", desc: "Automation server", url: "jenkins.io", pricing: "Free", rating: 4.4, tags: ["self-hosted", "plugins", "extensible"]},
    {name: "CircleCI", category: "CI/CD", subcategory: "Cloud", desc: "CI/CD platform", url: "circleci.com", pricing: "Freemium", rating: 4.4, tags: ["cloud", "fast", "parallelism"]},
    {name: "Travis CI", category: "CI/CD", subcategory: "Cloud", desc: "CI for open source", url: "travis-ci.com", pricing: "Freemium", rating: 4.2, tags: ["open-source", "cloud", "simple"]},
    {name: "Azure DevOps", category: "CI/CD", subcategory: "Microsoft", desc: "Microsoft DevOps", url: "azure.microsoft.com/devops", pricing: "Freemium", rating: 4.3, tags: ["microsoft", "enterprise", "boards"]},
    {name: "Bitbucket Pipelines", category: "CI/CD", subcategory: "Atlassian", desc: "Bitbucket CI/CD", url: "bitbucket.org/product/features/pipelines", pricing: "Freemium", rating: 4.2, tags: ["atlassian", "bitbucket", "jira"]},
    {name: "TeamCity", category: "CI/CD", subcategory: "JetBrains", desc: "JetBrains CI server", url: "jetbrains.com/teamcity", pricing: "Freemium", rating: 4.3, tags: ["jetbrains", "enterprise", "builds"]},
    {name: "Buildkite", category: "CI/CD", subcategory: "Hybrid", desc: "Hybrid CI/CD", url: "buildkite.com", pricing: "Paid", rating: 4.5, tags: ["hybrid", "scalable", "agents"]},
    {name: "Drone", category: "CI/CD", subcategory: "Container", desc: "Container-native CI", url: "drone.io", pricing: "Freemium", rating: 4.3, tags: ["container", "docker", "gitops"]},
    {name: "Semaphore", category: "CI/CD", subcategory: "Cloud", desc: "Fast CI/CD", url: "semaphoreci.com", pricing: "Freemium", rating: 4.3, tags: ["fast", "parallelism", "cloud"]},
    {name: "Codefresh", category: "CI/CD", subcategory: "Kubernetes", desc: "GitOps CI/CD", url: "codefresh.io", pricing: "Freemium", rating: 4.3, tags: ["kubernetes", "gitops", "helm"]},
    {name: "GoCD", category: "CI/CD", subcategory: "Open Source", desc: "Continuous delivery", url: "gocd.org", pricing: "Free", rating: 4.1, tags: ["open-source", "pipelines", "thoughtworks"]},
    {name: "Harness", category: "CI/CD", subcategory: "Enterprise", desc: "Software delivery", url: "harness.io", pricing: "Freemium", rating: 4.4, tags: ["enterprise", "ai", "delivery"]},
    {name: "Tekton", category: "CI/CD", subcategory: "Kubernetes", desc: "K8s native CI/CD", url: "tekton.dev", pricing: "Free", rating: 4.2, tags: ["kubernetes", "cncf", "pipelines"]},
    
    // ==================== INFRASTRUCTURE AS CODE ====================
    {name: "Terraform", category: "IaC", subcategory: "Multi-Cloud", desc: "Infrastructure as code", url: "terraform.io", pricing: "Freemium", rating: 4.7, tags: ["iac", "multi-cloud", "hcl"], featured: true},
    {name: "Pulumi", category: "IaC", subcategory: "Multi-Cloud", desc: "IaC with programming languages", url: "pulumi.com", pricing: "Freemium", rating: 4.5, tags: ["iac", "programming", "typescript"]},
    {name: "AWS CloudFormation", category: "IaC", subcategory: "AWS", desc: "AWS IaC", url: "aws.amazon.com/cloudformation", pricing: "Free", rating: 4.3, tags: ["aws", "yaml", "json"]},
    {name: "AWS CDK", category: "IaC", subcategory: "AWS", desc: "Cloud Development Kit", url: "aws.amazon.com/cdk", pricing: "Free", rating: 4.4, tags: ["aws", "programming", "typescript"]},
    {name: "Ansible", category: "IaC", subcategory: "Configuration", desc: "Automation platform", url: "ansible.com", pricing: "Freemium", rating: 4.5, tags: ["automation", "agentless", "redhat"]},
    {name: "Chef", category: "IaC", subcategory: "Configuration", desc: "Configuration management", url: "chef.io", pricing: "Freemium", rating: 4.1, tags: ["configuration", "ruby", "enterprise"]},
    {name: "Puppet", category: "IaC", subcategory: "Configuration", desc: "IT automation", url: "puppet.com", pricing: "Freemium", rating: 4.0, tags: ["configuration", "enterprise", "dsl"]},
    {name: "SaltStack", category: "IaC", subcategory: "Configuration", desc: "Intelligent automation", url: "saltproject.io", pricing: "Freemium", rating: 4.1, tags: ["automation", "python", "vmware"]},
    {name: "Crossplane", category: "IaC", subcategory: "Kubernetes", desc: "Cloud control plane", url: "crossplane.io", pricing: "Free", rating: 4.3, tags: ["kubernetes", "cncf", "multi-cloud"]},
    {name: "Spacelift", category: "IaC", subcategory: "Management", desc: "IaC management", url: "spacelift.io", pricing: "Paid", rating: 4.3, tags: ["terraform", "pulumi", "gitops"]},
    {name: "Env0", category: "IaC", subcategory: "Management", desc: "IaC automation", url: "env0.com", pricing: "Freemium", rating: 4.2, tags: ["terraform", "automation", "collaboration"]},
    {name: "Scalr", category: "IaC", subcategory: "Management", desc: "Terraform collaboration", url: "scalr.com", pricing: "Paid", rating: 4.1, tags: ["terraform", "enterprise", "governance"]},
    
    // ==================== MONITORING & OBSERVABILITY ====================
    {name: "Datadog", category: "Monitoring", subcategory: "APM", desc: "Monitoring platform", url: "datadoghq.com", pricing: "Paid", rating: 4.6, tags: ["apm", "logs", "metrics"], featured: true},
    {name: "New Relic", category: "Monitoring", subcategory: "APM", desc: "Observability platform", url: "newrelic.com", pricing: "Freemium", rating: 4.5, tags: ["apm", "full-stack", "ai"]},
    {name: "Grafana", category: "Monitoring", subcategory: "Visualization", desc: "Observability stack", url: "grafana.com", pricing: "Freemium", rating: 4.7, tags: ["visualization", "open-source", "dashboards"]},
    {name: "Prometheus", category: "Monitoring", subcategory: "Metrics", desc: "Monitoring system", url: "prometheus.io", pricing: "Free", rating: 4.6, tags: ["metrics", "cncf", "alerting"]},
    {name: "Splunk", category: "Monitoring", subcategory: "Logs", desc: "Data platform", url: "splunk.com", pricing: "Paid", rating: 4.4, tags: ["logs", "security", "enterprise"]},
    {name: "Elastic APM", category: "Monitoring", subcategory: "APM", desc: "Elastic observability", url: "elastic.co/apm", pricing: "Freemium", rating: 4.4, tags: ["apm", "elastic", "logs"]},
    {name: "Dynatrace", category: "Monitoring", subcategory: "APM", desc: "Software intelligence", url: "dynatrace.com", pricing: "Paid", rating: 4.4, tags: ["ai", "apm", "enterprise"]},
    {name: "AppDynamics", category: "Monitoring", subcategory: "APM", desc: "Application performance", url: "appdynamics.com", pricing: "Paid", rating: 4.3, tags: ["apm", "cisco", "enterprise"]},
    {name: "Sentry", category: "Monitoring", subcategory: "Errors", desc: "Error tracking", url: "sentry.io", pricing: "Freemium", rating: 4.6, tags: ["errors", "crashes", "performance"]},
    {name: "Jaeger", category: "Monitoring", subcategory: "Tracing", desc: "Distributed tracing", url: "jaegertracing.io", pricing: "Free", rating: 4.4, tags: ["tracing", "cncf", "opentelemetry"]},
    {name: "Zipkin", category: "Monitoring", subcategory: "Tracing", desc: "Distributed tracing", url: "zipkin.io", pricing: "Free", rating: 4.2, tags: ["tracing", "open-source", "twitter"]},
    {name: "Honeycomb", category: "Monitoring", subcategory: "Observability", desc: "Observability platform", url: "honeycomb.io", pricing: "Freemium", rating: 4.5, tags: ["observability", "high-cardinality", "debugging"]},
    {name: "Lightstep", category: "Monitoring", subcategory: "Observability", desc: "Observability platform", url: "lightstep.com", pricing: "Freemium", rating: 4.3, tags: ["observability", "servicenow", "tracing"]},
    {name: "Chronosphere", category: "Monitoring", subcategory: "Metrics", desc: "Cloud monitoring", url: "chronosphere.io", pricing: "Paid", rating: 4.2, tags: ["metrics", "kubernetes", "scale"]},
    {name: "Axiom", category: "Monitoring", subcategory: "Logs", desc: "Log management", url: "axiom.co", pricing: "Freemium", rating: 4.4, tags: ["logs", "unlimited", "serverless"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE35 = AI_TOOLS_PHASE35;
}


