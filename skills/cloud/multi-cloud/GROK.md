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
