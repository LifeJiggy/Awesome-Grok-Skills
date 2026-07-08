# Cloud Architecture Agent

Enterprise-grade cloud design, multi-cloud management, and infrastructure automation across AWS, Azure, and GCP.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Architecture Design](#architecture-design)
  - [Cost Estimation](#cost-estimation)
  - [Migration Planning](#migration-planning)
  - [Security Architecture](#security-architecture)
  - [Compliance Checking](#compliance-checking)
  - [Network Design](#network-design)
  - [Disaster Recovery](#disaster-recovery)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Cloud Provider Support](#cloud-provider-support)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Architecture Details](#architecture-details)
- [File Structure](#file-structure)
- [License](#license)

## Overview

The Cloud Architecture Agent is a comprehensive infrastructure design system that helps architects and engineers plan, design, cost, secure, and migrate cloud workloads across AWS, Azure, and GCP. It combines the AWS Well-Architected Framework (and equivalent cloud-native frameworks) with automated design generation, cost optimization, and compliance validation.

The agent produces production-ready reference architectures with ASCII diagrams, data-flow maps, cost breakdowns, and IaC templates (Terraform, CloudFormation, ARM).

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

See [ARCHITECTURE.md](ARCHITECTURE.md) for full system design, ASCII diagrams, and component deep dives.

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

## License

Internal use: Awesome-Grok-Skills project. MIT License — see [LICENSE](../../LICENSE) for details.
