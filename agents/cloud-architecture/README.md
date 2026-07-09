# Cloud Architecture Agent

Enterprise-grade cloud design, multi-cloud management, and infrastructure automation across AWS, Azure, and GCP.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [Examples](#examples)
- [Cloud Provider Support](#cloud-provider-support)
- [Best Practices](#best-practices)
- [Security](#security)
- [Scalability](#scalability)
- [Design Patterns](#design-patterns)
- [Troubleshooting](#troubleshooting)
- [Architecture Details](#architecture-details)
- [File Structure](#file-structure)
- [License](#license)

## Overview

The Cloud Architecture Agent is a comprehensive infrastructure design system that helps architects and engineers plan, design, cost, secure, and migrate cloud workloads across AWS, Azure, and GCP. It combines the AWS Well-Architected Framework (and equivalent cloud-native frameworks) with automated design generation, cost optimization, and compliance validation.

The agent produces production-ready reference architectures with ASCII diagrams, data-flow maps, cost breakdowns, and IaC templates (Terraform, CloudFormation, ARM).

## Architecture

```
Cloud Architecture Agent
├── Architecture Designer (Reference Library + Pattern Generator)
├── Cost Estimator (Pricing DB + TCO Calculator + Optimization)
├── Migration Manager (6R Strategy + Wave Builder + Dependency Mapper)
├── Security Architect (Threat Model + Encryption + Zero-Trust)
├── Multi-Cloud Manager (Provider Abstraction + Drift Detection)
├── Compliance & Governance (Framework Registry + Policy Engine + Audit)
└── Shared Data Layer (Templates + Cost Models + Control Maps)
```

### Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Requirements│────▶│  Design     │────▶│  Validation │
│ Gathering   │     │  Engine     │     │  & Checks   │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
              ┌─────▼──────┐          ┌───────▼───────┐          ┌───────▼──────┐
              │    Cost    │          │  Compliance   │          │   Security   │
              │  Estimate  │          │   Check       │          │   Design     │
              └─────┬──────┘          └───────┬───────┘          └───────┬──────┘
                    │                          │                          │
                    └──────────────────────────┼──────────────────────────┘
                                               │
                                        ┌──────▼──────┐
                                        │   Output    │
                                        │  (Terraform,│
                                        │   CFN, ARM) │
                                        └─────────────┘
```

## Features

| Feature | Description |
|---------|-------------|
| **Multi-Cloud Design** | Reference architectures across AWS, Azure, and GCP |
| **Cost Estimation** | Detailed monthly/annual cost projections with optimization recommendations |
| **Migration Planning** | 6R strategy classification, wave planning, and dependency mapping |
| **Security Architecture** | Defense-in-depth design, zero-trust networking, encryption strategy |
| **Compliance Validation** | SOC2, HIPAA, PCI-DSS, GDPR, ISO 27001, FedRAMP framework checks |
| **Network Design** | VPC/subnet planning, Transit Gateway, VPN, peering, DNS |
| **Container Orchestration** | EKS/AKS/GKE cluster design, service mesh, node groups |
| **Serverless Architecture** | Lambda/Functions design, event-driven patterns, Step Functions |
| **Disaster Recovery** | Multi-region DR strategies with RPO/RTO calculations |
| **Data Architecture** | Database selection matrix, storage tiering, data flow patterns |
| **Landing Zone** | Multi-account strategy, governance, tagging, budget alerts |
| **IaC Generation** | Terraform, CloudFormation, ARM template output |

## Quick Start

```python
from agents.cloud_architecture.agent import CloudArchitectureAgent, CloudProvider

agent = CloudArchitectureAgent()

# Design a scalable e-commerce platform
architecture = agent.create_architecture(
    name="E-Commerce Platform",
    description="Scalable, highly-available e-commerce platform on AWS",
    provider=CloudProvider.AWS,
    scale="large",
    compliance=["SOC2", "PCI-DSS"]
)

# Generate cost estimate
cost = agent.estimate_cost(architecture)
print(f"Estimated monthly cost: ${cost['monthly_total']:,}")

# Generate Terraform template
template = agent.generate_terraform(architecture)
```

Run the demo directly:

```bash
python agents/cloud-architecture/agent.py
```

## Installation

**Requirements:**
- Python 3.9+
- No external dependencies for demo/offline mode

```bash
# Optional: Install cloud SDKs for real provider access
pip install boto3                    # AWS
pip install azure-identity azure-mgmt-*  # Azure
pip install google-cloud-*           # GCP
pip install python-hcl2              # Terraform HCL parsing
```

## Usage

### Architecture Design

Create multi-tier architectures with provider-specific service recommendations:

```python
from agents.cloud_architecture.agent import CloudArchitectureAgent, CloudProvider

agent = CloudArchitectureAgent()

# Design a three-tier web application
arch = agent.create_architecture(
    name="Web Application",
    description="Standard three-tier web app with auto-scaling",
    provider=CloudProvider.AWS,
    scale="medium",
    compliance=["SOC2"],
    requirements={
        "availability": "99.95%",
        "max_latency_ms": 200,
        "concurrent_users": 10000,
        "data_sensitivity": "confidential"
    }
)

# Get recommended services
services = agent.get_recommended_services(arch)
# {
#   "compute": ["ECS Fargate", "Lambda"],
#   "database": ["Aurora PostgreSQL", "ElastiCache"],
#   "storage": ["S3"],
#   "networking": ["ALB", "CloudFront", "Route53"],
#   "security": ["WAF", "GuardDuty", "KMS"]
# }
```

### Cost Estimation

Generate detailed cost projections with optimization recommendations:

```python
# Full cost estimate
cost_report = agent.estimate_cost(arch)
print(cost_report)
# {
#   "monthly_total": 4200,
#   "annual_total": 50400,
#   "breakdown": {
#     "compute": 2400,
#     "storage": 800,
#     "database": 1200,
#     "network": 400,
#     "management": 300
#   },
#   "optimization_savings": 1260,
#   "recommendations": [
#     "Use Reserved Instances for baseline compute: save $720/month",
#     "Enable S3 Intelligent-Tiering: save $180/month",
#     "Right-size RDS instance: save $360/month"
#   ]
# }

# Compare across providers
comparison = agent.compare_costs(arch, providers=[CloudProvider.AWS, CloudProvider.AZURE])
```

### Migration Planning

Classify workloads using the 6R strategy and generate migration wave plans:

```python
# Assess current environment
assessment = agent.assess_migration(
    applications=[
        {"name": "Legacy CRM", "type": "monolith", "database": "Oracle", "users": 500},
        {"name": "Web Portal", "type": "web-app", "database": "MySQL", "users": 5000},
        {"name": "Batch Processor", "type": "batch", "database": "PostgreSQL", "users": 0}
    ],
    target_provider=CloudProvider.AWS
)

# 6R classification
for app in assessment["applications"]:
    print(f"{app['name']}: {app['strategy']} (timeline: {app['timeline']})")
# Legacy CRM: Replatform (6-10 weeks)
# Web Portal: Refactor (12-20 weeks)
# Batch Processor: Rehost (4-8 weeks)

# Generate migration waves
waves = agent.generate_migration_waves(assessment)
```

### Security Architecture

Design defense-in-depth security across all layers:

```python
# Generate security architecture
security = agent.design_security(
    architecture=arch,
    compliance=["SOC2", "PCI-DSS"],
    data_classification="confidential"
)

print(security["layers"])
# {
#   "identity": {"mfa": true, "sso": "SAML/OIDC", "least_privilege": true},
#   "network": {"waf": true, "ddos_protection": true, "private_subnets": true},
#   "data": {"encryption_at_rest": "KMS-CMK", "encryption_in_transit": "TLS-1.3"},
#   "application": {"sast": true, "dast": true, "container_scanning": true},
#   "monitoring": {"cloudtrail": true, "guardduty": true, "siem": true}
# }
```

### Compliance Checking

Validate architecture against compliance frameworks:

```python
# Check SOC2 compliance
result = agent.check_compliance(arch, framework="SOC2")
print(f"Score: {result['score']}% ({result['status']})")
# Score: 87% (Partial)

for control in result["gaps"]:
    print(f"  - {control['id']}: {control['description']}")
#   - CC6.1: Enable VPC Flow Logs
#   - CC7.1: Configure GuardDuty in all regions
```

### Network Design

Design VPC/subnet architecture with security controls:

```python
# Design VPC
vpc = agent.design_network(
    name="Production VPC",
    cidr="10.0.0.0/16",
    availability_zones=3,
    tiers=["public", "private", "data"],
    connectivity="hybrid"
)

print(vpc["subnets"])
# {
#   "public":  ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"],
#   "private": ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"],
#   "data":    ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]
# }
```

### Disaster Recovery

Design DR strategy with RPO/RTO targets:

```python
# Design DR
dr = agent.design_dr(
    architecture=arch,
    rpo_hours=1,
    rto_hours=2,
    budget_constraint="medium"
)

print(dr["strategy"])
# "warm_standby"
print(dr["details"])
# {"primary_region": "us-east-1", "secondary_region": "us-west-2",
#  "replication": "async", "failover": "automatic", "cost_overhead": "40%"}
```

## API Reference

### CloudArchitectureAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_architecture(name, description, provider, scale, compliance, requirements?)` | name: str, description: str, provider: CloudProvider, scale: str, compliance: List[str], requirements?: Dict | Architecture |
| `estimate_cost(architecture)` | architecture: Architecture | CostReport |
| `compare_costs(architecture, providers)` | architecture: Architecture, providers: List[CloudProvider] | CostComparison |
| `design_security(architecture, compliance, data_classification)` | architecture: Architecture, compliance: List[str], data_classification: str | SecurityArchitecture |
| `check_compliance(architecture, framework)` | architecture: Architecture, framework: str | ComplianceResult |
| `assess_migration(applications, target_provider)` | applications: List[Dict], target_provider: CloudProvider | MigrationAssessment |
| `generate_migration_waves(assessment)` | assessment: MigrationAssessment | List[MigrationWave] |
| `design_network(name, cidr, availability_zones, tiers, connectivity)` | name: str, cidr: str, availability_zones: int, tiers: List[str], connectivity: str | NetworkDesign |
| `design_dr(architecture, rpo_hours, rto_hours, budget_constraint)` | architecture: Architecture, rpo_hours: float, rto_hours: float, budget_constraint: str | DRDesign |
| `generate_terraform(architecture)` | architecture: Architecture | str |
| `generate_cloudformation(architecture)` | architecture: Architecture | Dict |
| `generate_arm_template(architecture)` | architecture: Architecture | Dict |

### CloudProvider Enum

| Value | Description |
|-------|-------------|
| `CloudProvider.AWS` | Amazon Web Services |
| `CloudProvider.AZURE` | Microsoft Azure |
| `CloudProvider.GCP` | Google Cloud Platform |

### Scale Options

| Scale | Description | Typical Components |
|-------|-------------|-------------------|
| `small` | Prototype or MVP | 2-3 services, single AZ |
| `medium` | Standard production | 5-10 services, multi-AZ |
| `large` | Enterprise | 15+ services, multi-AZ, DR |
| `global` | Global scale | Multi-region, active-active |

## Data Models

### Architecture

```python
@dataclass
class Architecture:
    arch_id: str                    # Unique identifier
    name: str                       # Architecture name
    description: str                # Description
    provider: CloudProvider         # AWS, AZURE, GCP
    scale: str                      # small, medium, large, global
    compliance: List[str]           # Compliance frameworks
    requirements: Dict              # Availability, latency, etc.
    services: Dict[str, List[str]]  # Recommended services by category
    created_at: datetime            # Creation timestamp
```

### CostReport

```python
@dataclass
class CostReport:
    monthly_total: float            # Total monthly cost
    annual_total: float             # Total annual cost
    breakdown: Dict[str, float]     # Cost by category
    optimization_savings: float     # Potential savings
    recommendations: List[str]      # Optimization recommendations
```

### MigrationWave

```python
@dataclass
class MigrationWave:
    number: int                     # Wave sequence number
    applications: List[str]         # Application names
    timeline: str                   # Estimated duration
    dependencies: List[str]         # Wave dependencies
    risk_level: str                 # low, medium, high
```

## Configuration

```python
# Agent configuration
agent = CloudArchitectureAgent(
    default_provider=CloudProvider.AWS,
    default_region="us-east-1",
    cost_model="standard",          # standard | detailed | custom
    compliance_strict=False,        # True = fail on any gap
    output_format="markdown",       # markdown | json | yaml
    enable_iac_generation=True,     # Generate Terraform/CFN/ARM
    enable_cost_optimization=True,  # Include optimization recommendations
)
```

### Environment Variables

```bash
# Cloud credentials (for real provider access)
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-east-1"

export AZURE_SUBSCRIPTION_ID="..."
export AZURE_TENANT_ID="..."

export GOOGLE_PROJECT_ID="..."
export GOOGLE_APPLICATION_CREDENTIALS="..."
```

## Examples

### Example 1: E-Commerce Platform on AWS

```python
agent = CloudArchitectureAgent()

arch = agent.create_architecture(
    name="ShopFast E-Commerce",
    description="High-availability e-commerce with PCI-DSS compliance",
    provider=CloudProvider.AWS,
    scale="large",
    compliance=["PCI-DSS", "SOC2"]
)

# Cost estimate
cost = agent.estimate_cost(arch)
print(f"Monthly: ${cost['monthly_total']:,}, Annual: ${cost['annual_total']:,}")

# Generate Terraform
tf_code = agent.generate_terraform(arch)
with open("main.tf", "w") as f:
    f.write(tf_code)
```

### Example 2: Multi-Cloud DR Assessment

```python
# Assess DR options
dr_options = agent.assess_dr_options(
    current_provider=CloudProvider.AWS,
    secondary_provider=CloudProvider.AZURE,
    workload_type="database",
    rpo_hours=1,
    rto_hours=4
)

for option in dr_options:
    print(f"{option['strategy']}: ${option['monthly_cost']:,}/month, RPO={option['rpo']}")
```

### Example 3: Migration Wave Planning

```python
assessment = agent.assess_migration(
    applications=[
        {"name": "App-A", "type": "web", "size": "medium"},
        {"name": "App-B", "type": "api", "size": "large"},
        {"name": "App-C", "type": "batch", "size": "small"},
    ],
    target_provider=CloudProvider.AWS
)

waves = agent.generate_migration_waves(assessment)
for wave in waves:
    print(f"Wave {wave['number']}: {wave['apps']} ({wave['timeline']})")
```

## Cloud Provider Support

| Capability | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| Compute | EC2, Lambda, ECS, EKS | VMs, Functions, AKS | Compute Engine, Cloud Run, GKE |
| Storage | S3, EBS, EFS, Glacier | Blob, Managed Disks | Cloud Storage, Persistent Disk |
| Database | RDS, Aurora, DynamoDB, Redshift | SQL DB, CosmosDB, Synapse | Cloud SQL, Firestore, BigQuery |
| Networking | VPC, ALB, NLB, CloudFront | VNet, LB, Front Door | VPC, Cloud LB, CDN |
| Security | IAM, KMS, GuardDuty | Entra ID, Key Vault, Defender | IAM, Cloud KMS, SCC |
| Messaging | SQS, SNS, EventBridge | Service Bus, Event Grid | Pub/Sub, Cloud Tasks |
| Monitoring | CloudWatch, X-Ray | Monitor, App Insights | Cloud Monitoring, Trace |
| IaC | CloudFormation, CDK | ARM, Bicep | Deployment Manager |

## Best Practices

1. **Always Start with Requirements** — Profile workload before selecting services.
2. **Design for Failure** — Assume components will fail; build redundancy.
3. **Multi-AZ for Production** — Never run production on a single AZ.
4. **Encrypt Everything** — KMS at rest, TLS in transit, no exceptions.
5. **Tag All Resources** — Environment, Owner, CostCenter, Application at minimum.
6. **Use Managed Services** — Reduce operational burden where possible.
7. **Implement Auto-Scaling** — Never statically provision for peak.
8. **Budget Alerts** — Set alerts at 50%, 80%, and 100% thresholds.
9. **Test DR Quarterly** — Runbook drills, not just documentation.
10. **Review Costs Monthly** — Rightsizing, reserved instances, spot utilization.

## Security

### Security Layers

```
┌─────────────────────────────────────────┐
│ Identity & Access Management            │
│ MFA, SSO, Least Privilege, PIM          │
├─────────────────────────────────────────┤
│ Network Security                        │
│ WAF, DDoS, Private Subnets, NACLs      │
├─────────────────────────────────────────┤
│ Data Protection                         │
│ Encryption at Rest/In Transit, KMS      │
├─────────────────────────────────────────┤
│ Application Security                    │
│ SAST, DAST, Container Scanning          │
├─────────────────────────────────────────┤
│ Monitoring & Detection                  │
│ CloudTrail, GuardDuty, SIEM Integration │
└─────────────────────────────────────────┘
```

## Scalability

### Performance Targets

| Operation | Latency | Throughput |
|-----------|---------|------------|
| Architecture creation | < 1s | 100/sec |
| Cost estimation | < 2s | 50/sec |
| Compliance check | < 3s | 30/sec |
| IaC generation | < 5s | 20/sec |

### Scaling Strategy

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Single    │────▶│  Cached     │────▶│  Distributed│
│   Instance  │     │  Results    │     │  Worker     │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Design Patterns

### Strategy Pattern — Provider Abstraction

```python
class CloudProviderStrategy:
    def get_services(self, category: str) -> List[str]:
        raise NotImplementedError

class AWSStrategy(CloudProviderStrategy):
    def get_services(self, category):
        return AWS_SERVICE_MAP[category]
```

### Builder Pattern — Architecture Construction

```python
builder = ArchitectureBuilder()
arch = (builder
    .set_name("My App")
    .set_provider(CloudProvider.AWS)
    .set_scale("large")
    .add_compliance(["SOC2"])
    .build())
```

### Template Method — IaC Generation

```python
class IaCGenerator:
    def generate(self, architecture):
        template = self._create_template(architecture)
        self._add_resources(template, architecture)
        self._add_outputs(template, architecture)
        return self._serialize(template)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Cost estimate seems high | Check if right-sizing recommendations are applied; verify instance types |
| Compliance score low | Review gap list; implement missing controls; re-assess |
| Migration plan unrealistic | Verify application inventory is complete; adjust wave sizes |
| Network design has overlap | Check CIDR blocks across VPCs; use non-overlapping ranges |
| DR RTO not achievable | Consider active-active instead of pilot light; optimize failover |
| Terraform generation fails | Ensure architecture has all required fields; check provider compatibility |

## Architecture Details

See [ARCHITECTURE.md](ARCHITECTURE.md) for deep dives on:
- System component design with ASCII diagrams
- Multi-cloud provider mapping
- Landing zone architecture
- VPC/subnet design patterns
- Cost estimation model
- Security defense-in-depth layers
- Migration framework (6R strategy)
- Compliance framework mappings
- Serverless and container patterns
- Disaster recovery architecture
- Performance engineering patterns

## Agent Instructions

See [GROK.md](GROK.md) for the agent system prompt, identity, principles, detailed capabilities with code examples, method signatures, data models, and operational checklists.

## File Structure

```
agents/cloud-architecture/
├── agent.py           # Main implementation (~1,100+ lines)
├── ARCHITECTURE.md    # System architecture and design patterns
├── GROK.md            # Agent prompt, capabilities, and API specs
└── README.md          # This file — usage guide and quick reference
```

## Additional Examples

### Example 4: Landing Zone Design

```python
# Design a multi-account landing zone
landing_zone = agent.design_landing_zone(
    name="Enterprise Landing Zone",
    provider=CloudProvider.AWS,
    accounts=[
        {"name": "Management", "purpose": "billing, identity, security"},
        {"name": "SharedServices", "purpose": "CI/CD, monitoring, DNS"},
        {"name": "Production", "purpose": "production workloads"},
        {"name": "Staging", "purpose": "pre-production testing"},
        {"name": "Development", "purpose": "developer sandboxes"},
    ],
    compliance=["SOC2", "HIPAA"]
)

print(f"Total accounts: {len(landing_zone['accounts'])}")
print(f"Monthly cost: ${landing_zone['monthly_cost']:,}")
```

### Example 5: Kubernetes Cluster Design

```python
# Design EKS cluster
cluster = agent.design_kubernetes(
    name="Production EKS",
    provider=CloudProvider.AWS,
    node_groups=[
        {"name": "general", "instance_type": "m5.xlarge", "min": 3, "max": 10},
        {"name": "memory", "instance_type": "r5.xlarge", "min": 2, "max": 6},
    ],
    networking={"mode": "aws-cni", "network_policy": "calico"},
    monitoring={"prometheus": True, "grafana": True}
)

print(f"Cluster endpoint: {cluster['endpoint']}")
print(f"Estimated monthly: ${cluster['monthly_cost']:,}")
```

### Example 6: Serverless Architecture

```python
# Design serverless API
serverless = agent.design_serverless(
    name="Order Processing API",
    provider=CloudProvider.AWS,
    components=[
        {"type": "api_gateway", "protocol": "REST"},
        {"type": "lambda", "runtime": "python3.11", "memory_mb": 1024},
        {"type": "dynamodb", "table": "orders", "billing": "on-demand"},
        {"type": "s3", "bucket": "order-attachments"},
        {"type": "sqs", "queue": "order-processing"},
    ],
    compliance=["SOC2"]
)

print(f"Architecture: {serverless['name']}")
for comp in serverless["components"]:
    print(f"  {comp['type']}: {comp['service']}")
```

## Deployment Checklist

- [ ] Review architecture against requirements
- [ ] Validate cost estimate fits budget
- [ ] Check compliance score meets threshold
- [ ] Verify DR strategy meets RPO/RTO targets
- [ ] Test Terraform/CFN/ARM generation
- [ ] Validate network CIDR ranges don't overlap
- [ ] Review security controls for data classification
- [ ] Confirm tagging strategy is complete
- [ ] Set up budget alerts at 50%, 80%, 100%
- [ ] Schedule DR testing quarterly

## Operational Runbook

### Cost Optimization Checklist

- [ ] Right-size underutilized instances
- [ ] Enable Reserved Instances for baseline
- [ ] Use Spot/Preemptible for non-critical
- [ ] Enable auto-scaling for variable loads
- [ ] Review storage lifecycle policies
- [ ] Delete unattached volumes and IPs
- [ ] Check for idle load balancers
- [ ] Review data transfer costs

### Security Audit Checklist

- [ ] Enable MFA for all administrative access
- [ ] Rotate access keys every 90 days
- [ ] Review IAM policies quarterly
- [ ] Enable CloudTrail/Azure Activity Log
- [ ] Configure GuardDuty/Defender
- [ ] Review NSG/firewall rules
- [ ] Enable encryption at rest and in transit
- [ ] Set up SIEM integration

### Disaster Recovery Testing

```
Quarterly DR Test Procedure:
1. Announce maintenance window
2. Trigger failover to secondary region
3. Verify application connectivity
4. Run smoke tests
5. Measure RTO (actual vs target)
6. Trigger failback
7. Verify primary region recovery
8. Document results and gaps
9. Update runbook if needed
```

## Reference Architecture Templates

### Three-Tier Web Application (AWS)

```
┌─────────────────────────────────────────────────────────────────┐
│                        VPC (10.0.0.0/16)                        │
├─────────────────────────────────────────────────────────────────┤
│  Public Subnets                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                        │
│  │   ALB   │  │   ALB   │  │   ALB   │                        │
│  │  (AZ1)  │  │  (AZ2)  │  │  (AZ3)  │                        │
│  └────┬────┘  └────┬────┘  └────┬────┘                        │
├───────┼─────────────┼─────────────┼─────────────────────────────┤
│  Private Subnets (App Tier)                                     │
│  ┌────┴────┐  ┌────┴────┐  ┌────┴────┐                        │
│  │   ECS   │  │   ECS   │  │   ECS   │                        │
│  │  Tasks  │  │  Tasks  │  │  Tasks  │                        │
│  └────┬────┘  └────┬────┘  └────┬────┘                        │
├───────┼─────────────┼─────────────┼─────────────────────────────┤
│  Private Subnets (Data Tier)                                    │
│  ┌────┴────┐  ┌────┴────┐  ┌────┴────┐                        │
│  │ Aurora  │  │ Aurora  │  │ ElastiC │                        │
│  │ Primary │  │ Replica │  │  Cache   │                        │
│  └─────────┘  └─────────┘  └─────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

### Serverless Architecture (AWS)

```
┌─────────────────────────────────────────────────────────────────┐
│                         CloudFront                              │
│                    (CDN + SSL termination)                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                       API Gateway                               │
│                  (REST + custom domains)                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼───────┐  ┌───────▼───────┐  ┌───────▼───────┐
│    Lambda     │  │    Lambda     │  │    Lambda     │
│   (Users)    │  │   (Orders)   │  │  (Products)  │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                   │
        └──────────────────┼───────────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      ┌─────▼─────┐  ┌────▼────┐  ┌─────▼─────┐
      │ DynamoDB  │  │   S3    │  │   SQS     │
      │  (Data)   │  │ (Files) │  │ (Queue)   │
      └───────────┘  └─────────┘  └───────────┘
```

### Multi-Region Active-Active (Azure)

```
┌──────────────────────┐     ┌──────────────────────┐
│     East US          │     │     West US          │
├──────────────────────┤     ├──────────────────────┤
│ ┌──────────────────┐ │     │ ┌──────────────────┐ │
│ │   Front Door     │◄├─────├►│   Front Door     │ │
│ └────────┬─────────┘ │     │ └────────┬─────────┘ │
│          │           │     │          │           │
│ ┌────────▼─────────┐ │     │ ┌────────▼─────────┐ │
│ │   App Service    │ │     │ │   App Service    │ │
│ └────────┬─────────┘ │     │ └────────┬─────────┘ │
│          │           │     │          │           │
│ ┌────────▼─────────┐ │     │ ┌────────▼─────────┐ │
│ │   SQL Database   │◄├─────├►│   SQL Database   │ │
│ │  (Read Replica)  │ │     │ │  (Read Replica)  │ │
│ └──────────────────┘ │     │ └──────────────────┘ │
└──────────────────────┘     └──────────────────────┘
         │                            │
         └──────────────┬─────────────┘
                        │
              ┌─────────▼─────────┐
              │    Cosmos DB      │
              │  (Multi-Region)   │
              └───────────────────┘
```

### GCP Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GKE Cluster                              │
├─────────────────────────────────────────────────────────────────┤
│  Node Pool: General                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                        │
│  │  Pod    │  │  Pod    │  │  Pod    │                        │
│  │ (API)  │  │ (API)  │  │ (API)  │                        │
│  └────┬────┘  └────┬────┘  └────┬────┘                        │
├───────┼─────────────┼─────────────┼─────────────────────────────┤
│  Node Pool: Memory-Optimized                                    │
│  ┌────┴────┐  ┌────┴────┐                                      │
│  │  Pod    │  │  Pod    │                                      │
│  │ (Worker)│  │ (Worker)│                                      │
│  └────┬────┘  └────┬────┘                                      │
├───────┼─────────────┼───────────────────────────────────────────┤
│  Services                                                       │
│  ┌────┴────┐  ┌────┴────┐  ┌─────────────┐                    │
│  │  Cloud  │  │  Cloud  │  │   Cloud     │                    │
│  │   SQL   │  │  Memorystore│ │  Storage   │                    │
│  └─────────┘  └─────────┘  └─────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

## Glossary

| Term | Definition |
|------|------------|
| VPC | Virtual Private Cloud — isolated network environment |
| Subnet | Subdivision of a VIP for resource placement |
| AZ | Availability Zone — physically separate datacenter |
| Region | Geographic area containing multiple AZs |
| CIDR | Classless Inter-Domain Routing — IP address block notation |
| LB | Load Balancer — distributes traffic across targets |
| NAT | Network Address Translation — outbound internet for private subnets |
| VPN | Virtual Private Network — encrypted tunnel |
| ExpressRoute | Azure private dedicated connection |
| Direct Connect | AWS private dedicated connection |
| Interconnect | GCP private dedicated connection |
| WAF | Web Application Firewall — HTTP request filtering |
| DDoS | Distributed Denial of Service attack |
| IAM | Identity and Access Management |
| RBAC | Role-Based Access Control |
| KMS | Key Management Service — encryption key management |
| IaC | Infrastructure as Code — declarative resource definitions |
| TPL | Terraform — infrastructure as code tool |
| CFN | CloudFormation — AWS IaC tool |
| ARM | Azure Resource Manager — Azure IaC template |
| RPO | Recovery Point Objective — maximum data loss tolerance |
| RTO | Recovery Time Objective — maximum downtime tolerance |
| MTTD | Mean Time to Detect — average detection time |
| MTTR | Mean Time to Recover — average recovery time |
| SLA | Service Level Agreement — uptime guarantee |
| SLO | Service Level Objective — internal reliability target |
| SLI | Service Level Indicator — measured reliability metric |
| ToR | Top of Rack — network switch at rack top |
| BGP | Border Gateway Protocol — dynamic routing protocol |
| Anycast | Single IP announced from multiple locations |

## License

Internal use: Awesome-Grok-Skills project. MIT License — see [LICENSE](../../LICENSE) for details.
