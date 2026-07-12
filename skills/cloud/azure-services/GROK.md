---
name: "azure-services"
category: "cloud"
version: "2.0.0"
tags: ["cloud", "Azure", "architecture", "services", "enterprise"]
---

# Azure Services

## Overview

The Azure Services module provides comprehensive guidance for designing and managing Microsoft Azure cloud architectures. It covers Azure compute, networking, storage, databases, AI/ML services, and enterprise integration patterns. The module follows the Azure Well-Architected Framework and cloud adoption framework for enterprise deployments.

This skill is essential for Azure architects, cloud engineers, and enterprise teams building workloads on Microsoft Azure.

## Core Capabilities

- **Compute**: Virtual Machines, Azure Functions, AKS, Container Apps, and App Service selection and optimization
- **Networking**: VNet design, Azure Front Door, ExpressRoute, Private Link, and hybrid connectivity
- **Storage**: Blob Storage tiers, Managed Disks, Azure Files, and data lake architecture
- **Databases**: Azure SQL, Cosmos DB, PostgreSQL, and database service selection
- **Identity**: Azure AD/Entra ID, Managed Identity, Conditional Access, and zero-trust patterns
- **Security**: Microsoft Defender for Cloud, Key Vault, Sentinel, and security posture management
- **DevOps**: Azure DevOps, GitHub Actions, ARM/Bicep templates, and CI/CD pipelines
- **Cost Management**: Azure Cost Management, reservations, savings plans, and optimization

## Usage Examples

```python
from azure_services import (
    AzureWellArchitected,
    ComputeSelector,
    NetworkDesigner,
    SecurityReviewer,
    CostOptimizer,
)

# --- Well-Architected Review ---
review = AzureWellArchitected(workload="e-commerce-api")
review.assess(
    pillar="reliability",
    findings=["Single region deployment", "No health probes configured"],
    severity="high",
)

# --- Compute Selection ---
selector = ComputeSelector()
rec = selector.recommend(
    workload="web-api",
    requests_per_sec=500,
    memory_mb=1024,
    gpu_required=False,
)
print(f"Service: {rec.service}, Tier: {rec.tier}")

# --- VNet Design ---
designer = NetworkDesigner()
vnet = designer.design_vnet(
    name="production-vnet",
    address_space="10.0.0.0/16",
    subnets=[
        {"name": "web", "cidr": "10.0.1.0/24"},
        {"name": "app", "cidr": "10.0.2.0/24"},
        {"name": "data", "cidr": "10.0.3.0/24"},
    ],
    peerings=[{"vnet": "hub-vnet", "allow_forwarded": True}],
)
print(f"VNet: {vnet.name}, Subnets: {len(vnet.subnets)}")

# --- Security Review ---
security = SecurityReviewer()
findings = security.review_subscription(subscription_id="sub-001")
for f in findings:
    print(f"  [{f.severity}] {f.finding}")
```

## Best Practices

- Use Azure Entra ID (AAD) for all identity management — avoid local accounts
- Implement Private Endpoints for all PaaS services to avoid public exposure
- Use Azure Policy for governance guardrails at scale
- Enable Microsoft Defender for Cloud across all subscriptions
- Use Bicep templates for infrastructure-as-code — preferred over ARM JSON
- Implement hub-spoke network topology for enterprise environments
- Use Azure Front Door for global load balancing and WAF protection
- Enable diagnostic logging for all services and centralize in Log Analytics
- Use Azure Cost Management with budgets and alerts for spend governance
- Apply Azure Blueprints for consistent environment provisioning

## Related Modules

- **aws-architecture**: AWS cloud architecture patterns
- **gcp-platform**: GCP cloud architecture patterns
- **multi-cloud**: Cross-cloud strategies and portability
- **serverless**: Serverless-first patterns on Azure
