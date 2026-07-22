---
name: "multi-cloud"
category: "cloud"
version: "2.0.0"
tags: ["cloud", "multi-cloud", "hybrid", "portability", "orchestration"]
---

# Multi-Cloud

## Overview

The Multi-Cloud module provides strategies and tools for architecting across multiple cloud providers (AWS, Azure, GCP, and others). It covers workload placement, data synchronization, identity federation, networking interconnect, cost arbitrage, vendor lock-in avoidance, and unified management plane design. The module emphasizes cloud-agnostic patterns and portable architectures.

This skill is essential for enterprise architects, platform engineers, and organizations adopting multi-cloud strategies for resilience, best-of-breed services, or regulatory requirements.

## Core Capabilities

- **Workload Placement**: Decision frameworks for which cloud to run which workload based on cost, performance, compliance, and data locality
- **Cloud-Agnostic Design**: Terraform multi-provider patterns, Kubernetes portability, and abstraction layers
- **Identity Federation**: Cross-cloud identity management using OIDC, SAML, and workload identity federation
- **Networking**: Cross-cloud VPN, dedicated interconnects (Direct Connect, ExpressRoute, Cloud Interconnect), and SD-WAN
- **Data Synchronization**: Multi-cloud data replication, conflict resolution, and consistency models
- **Cost Management**: Cross-cloud cost comparison, unified billing, and spend optimization
- **Security**: Unified policy enforcement, cross-cloud SIEM, and compliance across providers
- **Orchestration**: Kubernetes federation, service mesh across clouds, and unified CI/CD

## Usage Examples

```python
from multi_cloud import (
    WorkloadPlacer,
    CloudAgnosticArchitect,
    CostComparator,
    NetworkDesigner,
    IdentityFederator,
)

# --- Workload Placement ---
placer = WorkloadPlacer()
placement = placer.recommend(
    workloads=[
        {"name": "ml-training", "gpu_required": True, "data_location": "us"},
        {"name": "web-api", "latency_sensitive": True, "regions": ["us", "eu"]},
        {"name": "batch-processing", "cost_sensitive": True},
    ],
    providers=["aws", "azure", "gcp"],
)
for w in placement:
    print(f"  {w['workload']}: {w['provider']} ({w['service']})")

# --- Cost Comparison ---
comparator = CostComparator()
comparison = comparator.compare(
    workload="kubernetes",
    specs={"cpu": 8, "memory_gb": 32, "nodes": 3},
    providers=["aws", "azure", "gcp"],
)
for provider, cost in comparison.items():
    print(f"  {provider}: ${cost:.0f}/month")

# --- Network Design ---
net = NetworkDesigner()
design = net.design_interconnect(
    cloud_a={"provider": "aws", "region": "us-east-1"},
    cloud_b={"provider": "azure", "region": "eastus"},
    bandwidth_gbps=10,
    latency_target_ms=5,
)
print(f"Interconnect: {design.type}")
print(f"Est cost: ${design.monthly_cost:.0f}/month")

# --- Identity Federation ---
idp = IdentityFederator()
federation = idp.federate(
    primary_provider="aws",
    secondary_providers=["azure", "gcp"],
    protocol="oidc",
)
print(f"Federation established across {len(federation.providers)} providers")

# --- Cloud-Agnostic Architecture ---
architect = CloudAgnosticArchitect()
arch = architect.design(
    components=["api", "database", "cache", "queue", "storage"],
    target_portability="high",
)
print(f"Technologies: {arch.technologies}")
```

## Best Practices

- Use Kubernetes as the compute abstraction layer for maximum portability across clouds
- Prefer managed services with open standards (PostgreSQL, Redis, Kafka) over proprietary alternatives
- Implement identity federation — one identity across all clouds, not separate accounts
- Use Terraform with multi-provider modules for consistent infrastructure-as-code
- Deploy service mesh (Istio/Linkerd) for consistent networking and observability across clouds
- Centralize secrets management with a cloud-agnostic tool (HashiCorp Vault)
- Implement unified logging and monitoring across all cloud providers
- Use CDN providers with multi-cloud origins (Cloudflare, Fastly) for edge consistency
- Maintain cloud-agnostic data formats (Parquet, Avro) for portability
- Design for graceful degradation — what happens when one cloud provider has an outage?

## Related Modules

- **aws-architecture**: AWS-specific architecture patterns
- **azure-services**: Azure-specific architecture patterns
- **gcp-platform**: GCP-specific architecture patterns
- **serverless**: Serverless patterns that work across clouds

## Advanced Configuration

### Multi-Cloud Provider Configuration

```yaml
providers:
  aws:
    region: "us-east-1"
    profile: "production"
    credentials_source: "vault"
  azure:
    subscription: "sub-production"
    tenant: "tenant-id"
    credentials_source: "vault"
  gcp:
    project: "project-prod"
    zone: "us-central1-a"
    credentials_source: "vault"
```

### Terraform Multi-Provider Configuration

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  alias  = "us_east"
  region = "us-east-1"
}

provider "azurerm" {
  features {}
  alias = "east_us"
}

provider "google" {
  project = "my-project"
  region  = "us-central1"
  alias   = "us_central"
}
```

### Kubernetes Federation Configuration

```yaml
# kubefed-config.yaml
apiVersion: core.kubefed.io/v1beta1
kind: KubeFedCluster
metadata:
  name: aws-cluster
  namespace: kube-federation-system
spec:
  apiEndpoint: https://aws-k8s.example.com
  secretRef:
    name: aws-cluster-secret
---
apiVersion: core.kubefed.io/v1beta1
kind: KubeFedCluster
metadata:
  name: gcp-cluster
  namespace: kube-federation-system
spec:
  apiEndpoint: https://gcp-k8s.example.com
  secretRef:
    name: gcp-cluster-secret
```

## Architecture Patterns

### Multi-Cloud Architecture

```
Multi-Cloud Strategy:
├── Workload Placement
│   ├── AWS — Compute-heavy, ML workloads
│   ├── Azure — Enterprise integration, .NET
│   ├── GCP — Data analytics, AI/ML
│   └── On-prem — Compliance, legacy
├── Networking
│   ├── Cloud Interconnect (dedicated)
│   ├── VPN (encrypted tunnels)
│   ├── SD-WAN (software-defined)
│   └── Service Mesh (Istio/Linkerd)
├── Identity
│   ├── Federated identity (OIDC)
│   ├── Workload identity federation
│   └── Cross-cloud SSO
├── Data
│   ├── Multi-cloud replication
│   ├── Conflict resolution
│   └── Consistency models
└── Management
    ├── Unified control plane
    ├── Cost management
    └── Compliance monitoring
```

### Identity Federation Architecture

```
Identity Federation:
├── Primary Identity Provider
│   ├── Azure AD/Entra ID
│   ├── Okta
│   └── Auth0
├── Federation
│   ├── OIDC tokens
│   ├── SAML assertions
│   └── Workload identity
├── Cross-Cloud Access
│   ├── AWS AssumeRole
│   ├── Azure Managed Identity
│   └── GCP Workload Identity
└── Audit
    ├── Centralized logging
    ├── Compliance tracking
    └── Access reviews
```

### Data Synchronization Architecture

```
Data Sync Patterns:
├── Active-Active
│   ├── Multi-master replication
│   ├── Conflict resolution (last-write-wins)
│   └── High availability
├── Active-Passive
│   ├── Primary-replica
│   ├── Failover capability
│   └── Cost efficient
├── Event-Driven
│   ├── Event sourcing
│   ├── CQRS pattern
│   └── Eventually consistent
└── Batch Sync
    ├── Scheduled replication
    ├── ETL pipelines
    └── Data lake integration
```

## Integration Guide

### Terraform Multi-Cloud

```hcl
# AWS resource
resource "aws_instance" "web" {
  provider = aws.us_east
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
}

# Azure resource
resource "azurerm_virtual_machine" "web" {
  provider = azurerm.east_us
  name                = "web-vm"
  location            = "East US"
  resource_group_name = azurerm_resource_group.example.name
}

# GCP resource
resource "google_compute_instance" "web" {
  provider = google.us_central
  name         = "web-instance"
  machine_type = "e2-micro"
  zone         = "us-central1-a"
}
```

### Cross-Cloud Kubernetes

```yaml
# federated-deployment.yaml
apiVersion: types.kubefed.io/v1beta1
kind: FederatedDeployment
metadata:
  name: web-app
spec:
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: nginx:latest
  placement:
    clusters:
    - name: aws-cluster
    - name: gcp-cluster
  overrides:
  - clusterName: aws-cluster
    clusterOverrides:
    - path: "/spec/replicas"
      value: 3
  - clusterName: gcp-cluster
    clusterOverrides:
    - path: "/spec/replicas"
      value: 2
```

### HashiCorp Vault Integration

```python
import hvac

# Connect to Vault
client = hvac.Client(
    url='https://vault.example.com',
    token='my-token'
)

# Read secrets
secret = client.secrets.kv.v2.read_secret_version(
    path='multi-cloud/credentials',
    mount_point='secret',
)
print(f"AWS Key: {secret['data']['data']['aws_key'][:8]}...")
print(f"GCP Key: {secret['data']['data']['gcp_key'][:8]}...")
```

## Performance Optimization

### Cross-Cloud Latency

| Path | Typical Latency | Optimization |
|------|-----------------|--------------|
| AWS to Azure | 5-20ms | Direct Connect + ExpressRoute |
| AWS to GCP | 5-20ms | Direct Connect + Cloud Interconnect |
| Azure to GCP | 5-20ms | ExpressRoute + Cloud Interconnect |
| Any to On-prem | 10-50ms | Dedicated interconnect |

### Cost Optimization

```
Multi-Cloud Cost Strategies:
├── Spot/Preemptible instances (60-90% savings)
├── Reserved/Committed use (30-60% savings)
├── Right-sizing across providers
├── Cross-cloud arbitrage
├── Shared services consolidation
└── Unified cost management
```

### Data Transfer Optimization

```
Data Transfer Strategies:
├── Minimize cross-cloud transfers
├── Use compression
├── Batch transfers during off-peak
├── Cache frequently accessed data
├── Use CDN for static content
└── Optimize serialization format
```

## Security Considerations

### Multi-Cloud Security

| Control | Description | Implementation |
|---------|-------------|----------------|
| Identity Federation | Single identity across clouds | OIDC, SAML |
| Unified Policy | Consistent security policies | Open Policy Agent |
| Centralized Logging | Single pane of glass | SIEM integration |
| Secret Management | Cross-cloud secrets | HashiCorp Vault |
| Compliance | Unified compliance monitoring | Cloud Security Posture Management |

### Zero Trust Architecture

```
Zero Trust Principles:
├── Verify explicitly
├── Use least privilege access
├── Assume breach
├── Micro-segmentation
├── Encrypt everything
└── Continuous monitoring
```

### Secret Management

```
Cross-Cloud Secrets:
├── HashiCorp Vault (centralized)
├── AWS Secrets Manager
├── Azure Key Vault
├── GCP Secret Manager
└── Synchronization between providers
```

## Troubleshooting Guide

### Common Multi-Cloud Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Latency | Slow cross-cloud calls | Use dedicated interconnects |
| IAM Confusion | Access denied across clouds | Federate identity |
| Cost Overrun | Untracked spending | Unified cost management |
| Data Inconsistency | Conflicting data | Implement conflict resolution |
| Compliance Gap | Audit failures | Unified compliance monitoring |

### Debugging Cross-Cloud Issues

```bash
# Test cross-cloud connectivity
aws ec2 describe-vpc-peering-connections
az network vnet peering list
gcloud compute networks peerings list

# Check identity federation
aws sts get-caller-identity
az account show
gcloud auth list

# Verify secret access
vault kv get -field=aws_key secret/multi-cloud/credentials
```

## API Reference

### WorkloadPlacer

```python
class WorkloadPlacer:
    def recommend(
        workloads: list[dict],
        providers: list[str],
    ) -> list[Placement]:
        """Recommend workload placement across clouds."""

class Placement:
    workload: str
    provider: str
    service: str
    estimated_cost: float
    latency_ms: float
    compliance_status: str
```

### CostComparator

```python
class CostComparator:
    def compare(
        workload: str,
        specs: dict,
        providers: list[str],
    ) -> dict:
        """Compare costs across providers."""
```

### IdentityFederator

```python
class IdentityFederator:
    def federate(
        primary_provider: str,
        secondary_providers: list[str],
        protocol: str,
    ) -> FederationResult:
        """Establish identity federation across clouds."""

class FederationResult:
    providers: list[str]
    protocol: str
    trust_established: bool
    audit_enabled: bool
```

## Data Models

### CloudProvider

```
CloudProvider:
  name: str
  regions: list[str]
  services_used: list[str]
  monthly_cost: float
  compliance_status: str
  last_synced: datetime
```

### WorkloadPlacement

```
WorkloadPlacement:
  workload_id: str
  cloud_provider: str
  service: str
  region: str
  instance_type: str
  monthly_cost: float
  performance_score: float
  compliance_score: float
```

### CrossCloudMetric

```
CrossCloudMetric:
  metric_name: str
  source_cloud: str
  target_cloud: str
  latency_ms: float
  bandwidth_mbps: float
  cost_per_gb: float
  availability_pct: float
```

## Deployment Guide

### Multi-Cloud Setup

```
1. Planning
   ├── Define workload placement strategy
   ├── Select providers
   ├── Design networking
   └── Plan identity federation

2. Infrastructure
   ├── Deploy networking (interconnects)
   ├── Set up identity federation
   ├── Configure secret management
   └── Deploy monitoring

3. Deployment
   ├── Deploy workloads to each cloud
   ├── Configure cross-cloud communication
   ├── Set up data replication
   └── Enable failover

4. Operations
   ├── Unified monitoring
   ├── Cost management
   ├── Compliance monitoring
   └── Incident response
```

## Monitoring & Observability

### Multi-Cloud Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Cross-Cloud Latency | Latency between clouds | <20ms |
| Data Transfer Cost | Cost of cross-cloud data | Within budget |
| Availability | Cross-cloud availability | >99.9% |
| Compliance Score | Security posture | >90% |
| Cost Variance | Budget vs actual | <10% |

### Unified Dashboard

```
Multi-Cloud Dashboard:
├── Cost summary by provider
├── Performance comparison
├── Security posture
├── Compliance status
├── Resource utilization
├── Cross-cloud connectivity
└── Alert summary
```

## Testing Strategy

### Multi-Cloud Testing

```
1. Connectivity Tests
   ├── Cross-cloud latency
   ├── Bandwidth testing
   ├── Failover testing
   └── VPN stability

2. Identity Tests
   ├── Federation validation
   ├── Cross-cloud access
   ├── Role propagation
   └── Token exchange

3. Data Tests
   ├── Replication accuracy
   ├── Conflict resolution
   ├── Consistency checks
   └── Backup/restore
```

## Versioning & Migration

### Multi-Cloud Versioning

```
Major: Provider change
├── Example: Migrate from AWS to GCP
├── Requires: Full testing, rollback plan
└── Risk: High

Minor: Service additions
├── Example: Add Azure for specific workload
├── Requires: Testing, documentation
└── Risk: Medium

Patch: Configuration changes
├── Example: Update instance types
├── Requires: Basic testing
└── Risk: Low
```

## Glossary

| Term | Definition |
|------|-----------|
| Cloud Interconnect | Dedicated private connection between clouds |
| Federation | Single identity across multiple providers |
| Multi-Cloud | Using multiple cloud providers |
| SD-WAN | Software-defined wide area network |
| Service Mesh | Infrastructure layer for service communication |
| Zero Trust | Security model requiring verification for every access |
| CQRS | Command Query Responsibility Segregation |
| Event Sourcing | Storing state changes as a sequence of events |
| Workload Identity | Mapping workload to cloud IAM identity |
| Conflict Resolution | Handling data conflicts in multi-master replication |

## Changelog

### 2.0.0 (2024-12-01)
- Added Kubernetes federation
- Added cross-cloud data sync
- Improved cost optimization
- Added unified monitoring

### 1.2.0 (2024-08-15)
- Added identity federation
- Added cross-cloud networking
- Improved security

### 1.1.0 (2024-05-20)
- Added workload placement
- Added cost comparison
- Improved documentation

### 1.0.0 (2024-02-01)
- Initial release with basic patterns
- Simple provider configuration
- Basic networking

## Contributing Guidelines

### Adding New Patterns

1. Document the pattern
2. Include multi-provider examples
3. Provide cost estimates
4. Add security considerations
5. Submit PR with review

## License

MIT License

Copyright (c) 2024 Multi-Cloud Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
