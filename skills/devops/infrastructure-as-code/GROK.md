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

---

## Advanced Configuration

### Advanced Terraform Management

```python
from infrastructure_as_code import TerraformManager, TerraformConfig

tf = TerraformManager(
    directory="/infra/terraform",
    config=TerraformConfig(
        backend="s3",
        backend_config={
            "bucket": "terraform-state-prod",
            "key": "infra/terraform.tfstate",
            "region": "us-east-1",
            "dynamodb_table": "terraform-locks",
            "encrypt": True,
        },
        parallelism=10,
        lock=True,
        input=False,
    ),
)

# Comprehensive plan
plan = tf.plan_detailed(
    target=["module.vpc", "module.eks"],
    var_files=["production.tfvars"],
    out="plan.out",
)

print(f"Plan summary:")
print(f"  Additions: {plan.additions}")
print(f"  Changes: {plan.changes}")
print(f"  Deletions: {plan.deletions}")
print(f"  Cost estimate: ${plan.cost_estimate:.2f}/month")
print(f"  Execution time: {plan.execution_time_seconds:.0f}s")

# Apply with auto-approval
result = tf.apply(
    plan_file="plan.out",
    auto_approve=False,
    parallelism=10,
)

print(f"Apply result: {result.success}")
print(f"Resources modified: {result.resources_modified}")
print(f"Duration: {result.duration_seconds:.0f}s")
```

### Advanced Cloud Provisioning

```python
from infrastructure_as_code import CloudProvisioner, ProvisioningConfig

provisioner = CloudProvisioner(
    provider="aws",
    config=ProvisioningConfig(
        region="us-east-1",
        profile="production",
        assume_role="arn:aws:iam::123456789012:role/terraform",
    ),
)

# Provision comprehensive infrastructure
infra = provisioner.provision_comprehensive(
    template="eks-cluster",
    parameters={
        "cluster_name": "production",
        "kubernetes_version": "1.28",
        "vpc_cidr": "10.0.0.0/16",
        "availability_zones": ["us-east-1a", "us-east-1b", "us-east-1c"],
        "node_groups": [
            {"name": "general", "instance_type": "m5.large", "min_size": 3, "max_size": 10},
            {"name": "spot", "instance_type": "m5.large", "min_size": 0, "max_size": 20, "spot": True},
        ],
        "enable_irsa": True,
        "enable_cluster_autoscaler": True,
        "enable_metrics_server": True,
    },
    tags={"Environment": "production", "Team": "platform", "ManagedBy": "terraform"},
)

print(f"EKS Cluster: {infra.cluster_name}")
print(f"Endpoint: {infra.endpoint}")
print(f"Node groups: {len(infra.node_groups)}")
print(f"VPC: {infra.vpc_id}")
```

### Advanced Drift Detection

```python
from infrastructure_as_code import DriftDetector, DriftConfig

detector = DriftDetector(
    config=DriftConfig(
        continuous_monitoring=True,
        check_interval_minutes=15,
        auto_remediate=False,
        notify_on_drift=True,
        severity_threshold="medium",
    ),
)

# Comprehensive drift check
drift = detector.check_comprehensive(
    environment="production",
    resources=["all"],
    include_cost_impact=True,
)

print(f"Drift detected: {drift.detected}")
print(f"Resources with drift: {len(drift.resources)}")
print(f"Cost impact: ${drift.cost_impact:.2f}/month")

for resource in drift.resources:
    print(f"\n  {resource.type}:{resource.name}")
    print(f"    Severity: {resource.severity}")
    print(f"    Expected: {resource.expected}")
    print(f"    Actual: {resource.actual}")
    print(f"    Drift type: {resource.drift_type}")
    if resource.auto_remediable:
        print(f"    Auto-remediation available")
```

### Advanced Cost Optimization

```python
from infrastructure_as_code import CostOptimizer, OptimizationConfig

optimizer = OptimizationConfig(
    analyze_unused=True,
    right_size=True,
    reserved_instances=True,
    spot_instances=True,
    savings_plans=True,
)

# Comprehensive cost analysis
analysis = optimizer.analyze_comprehensive(
    environment="production",
    time_range_days=30,
    include_forecasting=True,
)

print(f"Current monthly cost: ${analysis.current_cost:.2f}")
print(f"Waste: ${analysis.waste_cost:.2f}")
print(f"Potential savings: ${analysis.potential_savings:.2f}")

print("\nOptimization recommendations:")
for rec in analysis.recommendations:
    print(f"  [{rec.priority}] {rec.description}")
    print(f"    Savings: ${rec.savings:.2f}/month")
    print(f"    Implementation: {rec.implementation}")
    print(f"    Effort: {rec.effort_hours:.1f} hours")
```

## Architecture Patterns

### IaC Architecture

```
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š                Infrastructure as Code Architecture          Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¤
Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š              Source Control                          Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€š  Terraform  Ã¢â€â€š  Ã¢â€â€š  Ansible    Ã¢â€â€š  Ã¢â€â€š  Helm       Ã¢â€â€š Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€š  Configs    Ã¢â€â€š  Ã¢â€â€š  Playbooks  Ã¢â€â€š  Ã¢â€â€š  Charts     Ã¢â€â€š Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ   Ã¢â€â€š
Ã¢â€â€š                           Ã¢â€â€š                                 Ã¢â€â€š
Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â´Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š              CI/CD Pipeline                          Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€š  Validate   Ã¢â€â€š  Ã¢â€â€š  Plan       Ã¢â€â€š  Ã¢â€â€š  Apply      Ã¢â€â€š Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ   Ã¢â€â€š
Ã¢â€â€š                           Ã¢â€â€š                                 Ã¢â€â€š
Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â´Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š              Cloud Providers                         Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€š  AWS        Ã¢â€â€š  Ã¢â€â€š  GCP        Ã¢â€â€š  Ã¢â€â€š  Azure      Ã¢â€â€š Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ   Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

## Integration Guide

### GitHub Actions Integration

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
    paths: ['terraform/**']
  pull_request:
    branches: [main]
    paths: ['terraform/**']

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
      
      - name: Terraform Init
        run: terraform init
      
      - name: Terraform Plan
        run: terraform plan -out=plan.out
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply plan.out
```

## Performance Optimization

### Infrastructure Performance

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Plan time | < 2min | 2-5min | > 5min |
| Apply time | < 10min | 10-30min | > 30min |
| Drift detection | < 5min | 5-15min | > 15min |
| Cost accuracy | > 95% | 85-95% | < 85% |

## Security Considerations

### Infrastructure Security

```python
from infrastructure_as_code import SecurityScanner

scanner = SecurityScanner()

# Scan infrastructure for security issues
security = scanner.scan("/infra/terraform")
print(f"Security score: {security.score:.1f}/100")
print(f"Issues: {len(security.issues)}")

for issue in security.issues:
    print(f"  [{issue.severity}] {issue.description}")
    print(f"    Resource: {issue.resource}")
    print(f"    Fix: {issue.fix_suggestion}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| State lock | Cannot acquire lock | Check for stuck operations |
| Drift | Resources modified manually | Apply or import changes |
| Cost overrun | Unexpected charges | Review unused resources |
| Plan failure | Invalid configuration | Validate syntax |

## API Reference

### TerraformManager

```python
class TerraformManager:
    def __init__(self, directory: str, config: TerraformConfig = None)
    def init(self) -> InitResult
    def validate(self) -> ValidationResult
    def plan(self, **kwargs) -> PlanResult
    def plan_detailed(self, **kwargs) -> DetailedPlanResult
    def apply(self, **kwargs) -> ApplyResult
    def destroy(self, **kwargs) -> DestroyResult
    def state_list(self) -> list[str]
    def import_resource(self, address: str, id: str) -> ImportResult
```

### CloudProvisioner

```python
class CloudProvisioner:
    def __init__(self, provider: str, config: ProvisioningConfig = None)
    def provision(self, template: str, **kwargs) -> ProvisionResult
    def provision_comprehensive(self, template: str, **kwargs) -> ComprehensiveResult
    def list_resources(self) -> list[Resource]
    def get_cost_estimate(self) -> CostEstimate
    def validate_template(self, template: str) -> ValidationResult
```

### DriftDetector

```python
class DriftDetector:
    def __init__(self, config: DriftConfig = None)
    def check(self, environment: str, **kwargs) -> DriftResult
    def check_comprehensive(self, environment: str, **kwargs) -> ComprehensiveResult
    def get_history(self) -> list[DriftEvent]
    def auto_remediate(self, resource: str) -> RemediationResult
    def get_severity_counts(self) -> dict[str, int]
```

### CostOptimizer

```python
class CostOptimizer:
    def __init__(self, config: OptimizationConfig = None)
    def analyze(self, environment: str, **kwargs) -> CostAnalysis
    def analyze_comprehensive(self, environment: str, **kwargs) -> ComprehensiveResult
    def get_recommendations(self) -> list[CostRecommendation]
    def get_forecast(self, days: int = 30) -> CostForecast
    def get_rightsizing(self) -> list[RightsizingRecommendation]
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class DriftSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Resource:
    type: str
    name: str
    provider: str
    region: str
    tags: Dict[str, str]
    cost_monthly: float

@dataclass
class DriftResource:
    type: str
    name: str
    severity: DriftSeverity
    expected: str
    actual: str
    drift_type: str
    auto_remediable: bool

@dataclass
class CostRecommendation:
    priority: str
    description: str
    savings: float
    implementation: str
    effort_hours: float
```

## Deployment Guide

### Installation

```bash
pip install infrastructure-as-code
```

## Monitoring & Observability

### Metrics Collection

```python
from infrastructure_as_code import MetricsCollector

collector = MetricsCollector()

# Collect infrastructure metrics
collector.gauge("infra.cost.monthly", cost, tags={"environment": environment})
collector.counter("infra.drift.detected", count, tags={"severity": severity})
collector.histogram("infra.apply.duration.seconds", duration)
collector.gauge("infra.resources.total", count, tags={"provider": provider})
```

## Testing Strategy

### Unit Tests

```python
import pytest
from infrastructure_as_code import TerraformManager, DriftDetector

@pytest.fixture
def tf():
    return TerraformManager(directory="test/terraform")

def test_validate(tf):
    result = tf.validate()
    assert result.is_valid
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Terraform | 1.0 | 1.6+ |
| AWS CLI | 2.0 | 2.15+ |

## Glossary

| Term | Definition |
|------|------------|
| **IaC** | Infrastructure as Code |
| **Drift** | Manual changes to infrastructure |
| **State** | Terraform's view of infrastructure |
| **Module** | Reusable Terraform component |
| **Plan** | Preview of infrastructure changes |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added comprehensive cost optimization
- New drift detection engine
- Improved multi-cloud support
- Added security scanning

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/infrastructure-as-code.git
cd infrastructure-as-code
pip install -e ".[dev]"
pytest
```

## Advanced Topics

### Pulumi Integration

```python
from infrastructure_as_code import PulumiManager

pulumi = PulumiManager()

# Define infrastructure with Pulumi
stack = pulumi.create_stack(
    name="production-vpc",
    project="platform",
    runtime="python",
    config={
        "vpc:cidr": "10.0.0.0/16",
        "vpc:azs": ["us-east-1a", "us-east-1b", "us-east-1c"],
        "vpc:enable_nat_gateway": True,
    },
)

# Preview changes
preview = pulumi.preview(stack)
print(f"Resources to add: {preview.additions}")
print(f"Resources to change: {preview.changes}")
print(f"Resources to delete: {preview.deletions}")

# Deploy
result = pulumi.up(stack)
print(f"Stack: {result.stack_name}")
print(f"Resources created: {result.resource_count}")
print(f"Outputs: {result.outputs}")
```

### AWS CDK Patterns

```python
from infrastructure_as_code import CDKManager

cdk = CDKManager()

# Synthesize CDK application
synth = cdk.synthesize("/path/to/cdk/app")
print(f"Stacks: {len(synth.stacks)}")
print(f"Total resources: {synth.total_resources}")

for stack in synth.stacks:
    print(f"\n  Stack: {stack.name}")
    print(f"    Resources: {stack.resource_count}")
    print(f"    Parameters: {len(stack.parameters)}")
    print(f"    Outputs: {len(stack.outputs)}")

# Diff against deployed state
diff = cdk.diff(stack_name="Production")
print(f"\nChanges: {diff.additions} add, {diff.changes} change, {diff.deletions} delete")
```

### GitOps Workflow Patterns

| Tool | Sync Method | Multi-Cluster | UI | Best For |
|------|-------------|---------------|-----|----------|
| ArgoCD | Git Ã¢â€ â€™ Cluster | Yes | Rich | Kubernetes-native |
| Flux | Git Ã¢â€ â€™ Cluster | Yes | CLI | Lightweight, composable |
| Crossplane | K8s Ã¢â€ â€™ Cloud | Yes | None | Multi-cloud provisioning |
| Spacelift | Git Ã¢â€ â€™ Terraform | Yes | Rich | Terraform-native GitOps |

### Secret Management

```python
from infrastructure_as_code import SecretManager

sm = SecretManager(provider="vault")

# Store secret
secret = sm.store(
    name="database-credentials",
    path="secret/prod/database",
    data={
        "username": "admin",
        "password": "s3cr3t",
        "host": "db.example.com",
        "port": 5432,
    },
    ttl="90d",
    rotation_policy="monthly",
)

print(f"Secret: {secret.name}")
print(f"Version: {secret.version}")
print(f"Next rotation: {secret.next_rotation}")

# Retrieve secret
retrieved = sm.retrieve("secret/prod/database")
print(f"Retrieved keys: {list(retrieved.data.keys())}")
```

### Terraform Workspace Strategy

```python
from infrastructure_as_code import WorkspaceManager

wm = WorkspaceManager(directory="/infra/terraform")

# List workspaces
workspaces = wm.list_workspaces()
print(f"Workspaces: {len(workspaces)}")
for ws in workspaces:
    print(f"  {ws.name}: {ws.resource_count} resources, ${ws.cost_monthly:.2f}/mo")

# Create new workspace
new_ws = wm.create_workspace(
    name="staging",
    variables={"environment": "staging", "region": "us-west-2"},
)

print(f"Created workspace: {new_ws.name}")
```

### Infrastructure Testing

```python
from infrastructure_as_code import InfraTestRunner

runner = InfraTestRunner()

# Run infrastructure tests
results = runner.run(
    test_types=["terraform_validate", "terraform_plan", "security_scan", "cost_check"],
    directory="/infra/terraform",
)

print(f"Tests: {results.total}")
print(f"Passed: {results.passed}")
print(f"Failed: {results.failed}")

for test in results.details:
    status = "PASS" if test.passed else "FAIL"
    print(f"  [{status}] {test.name}: {test.description}")
    if not test.passed:
        print(f"    Error: {test.error}")
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
