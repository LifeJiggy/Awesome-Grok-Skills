---
name: "Infrastructure as Code"
version: "2.0.0"
description: "Comprehensive infrastructure as code toolkit with Terraform management, cloud resource provisioning, configuration management, drift detection, and cost optimization for cloud infrastructure"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["devops", "infrastructure", "terraform", "cloud", "provisioning", "configuration"]
category: "devops"
personality: "infrastructure-engineer"
use_cases: ["Terraform management", "cloud provisioning", "configuration management", "drift detection", "cost optimization"]
---

# Infrastructure as Code

> Production-grade infrastructure as code framework providing Terraform management, cloud resource provisioning, configuration management, drift detection, and cost optimization for reliable cloud infrastructure.

## Overview

The Infrastructure as Code module provides tools for managing cloud infrastructure programmatically. It implements Terraform configuration management, multi-cloud resource provisioning, configuration drift detection, cost estimation and optimization, security compliance checking, and infrastructure documentation generation. Every operation includes state management, rollback capability, and audit logging.

## Core Capabilities

### 1. Terraform Management
- Configuration validation and formatting
- Plan generation and analysis
- Apply with approval workflows
- State management and locking
- Module registry integration

### 2. Cloud Resource Provisioning
- Multi-cloud support (AWS, GCP, Azure)
- Resource dependency management
- Parallel provisioning
- Tag and label management
- Resource group organization

### 3. Configuration Management
- Ansible playbook management
- Chef/Puppet configuration
- Salt state management
- Configuration drift detection
- Compliance enforcement

### 4. Drift Detection
- Continuous drift monitoring
- Drift severity assessment
- Auto-remediation policies
- Drift impact analysis
- Historical drift tracking

### 5. Cost Optimization
- Resource cost estimation
- Unused resource detection
- Right-sizing recommendations
- Reserved instance planning
- Cost allocation tracking

### 6. Security and Compliance
- Security group auditing
- IAM policy analysis
- Compliance rule enforcement
- Vulnerability scanning
- Encryption verification

## Usage Examples

### Terraform Management

```python
from infrastructure_as_code import TerraformManager

tf = TerraformManager(directory="/infra/terraform")

# Validate configuration
validation = tf.validate()
print(f"Valid: {validation.is_valid}")
print(f"Errors: {validation.errors}")

# Generate plan
plan = tf.plan()
print(f"Changes: {plan.additions} additions, {plan.changes} changes, {plan.deletions} deletions")
print(f"Cost estimate: ${plan.cost_estimate:.2f}/month")

# Apply with approval
if plan.approved:
    result = tf.apply()
    print(f"Applied: {result.success}")
    print(f"Resources: {result.resources_modified}")
```

### Cloud Provisioning

```python
from infrastructure_as_code import CloudProvisioner

provisioner = CloudProvisioner(provider="aws")

# Provision infrastructure
infra = provisioner.provision(
    template="vpc",
    parameters={
        "cidr_block": "10.0.0.0/16",
        "availability_zones": ["us-east-1a", "us-east-1b", "us-east-1c"],
        "enable_nat_gateway": True,
    },
    tags={"Environment": "production", "Team": "platform"},
)

print(f"VPC: {infra.vpc_id}")
print(f"Subnets: {len(infra.subnets)}")
print(f"NAT Gateway: {infra.nat_gateway_id}")
```

### Drift Detection

```python
from infrastructure_as_code import DriftDetector

detector = DriftDetector()

# Check for drift
drift = detector.check(environment="production")
print(f"Drift detected: {drift.detected}")
print(f"Resources with drift: {len(drift.resources)}")

for resource in drift.resources:
    print(f"  {resource.type}:{resource.name}")
    print(f"    Expected: {resource.expected}")
    print(f"    Actual: {resource.actual}")
    print(f"    Severity: {resource.severity}")
```

### Cost Optimization

```python
from infrastructure_as_code import CostOptimizer

optimizer = CostOptimizer()

# Analyze costs
analysis = optimizer.analyze(environment="production")
print(f"Monthly cost: ${analysis.total_cost:.2f}")
print(f"Waste: ${analysis.waste_cost:.2f}")

print("\nOptimization recommendations:")
for rec in analysis.recommendations:
    print(f"  {rec.description}: save ${rec.savings:.2f}/month")
```

## Best Practices

### Terraform
- Use remote state with locking
- Version control all configurations
- Use modules for reusable components
- Plan before apply always

### Cloud Provisioning
- Tag all resources for cost allocation
- Use least-privilege IAM policies
- Enable encryption at rest and in transit
- Monitor resource utilization

### Configuration Management
- Use idempotent configurations
- Test configurations in staging
- Version control playbooks and roles
- Monitor configuration drift

### Cost Optimization
- Review costs weekly
- Use reserved instances for predictable workloads
- Right-size underutilized resources
- Set up billing alerts

## Related Modules

- **ci-cd-pipelines**: Pipeline integration for infrastructure changes
- **container-orchestration**: Kubernetes infrastructure management
- **monitoring**: Infrastructure monitoring and alerting
- **security-hardening**: Security configuration management