---
name: "terraform-cloudformation"
category: "iac"
version: "2.0.0"
tags: ["iac", "terraform", "cloudformation", "aws", "infrastructure-as-code"]
description: "Infrastructure as Code management with Terraform and AWS CloudFormation"
---

# Terraform & CloudFormation

## Overview

This module provides comprehensive infrastructure as code (IaC) capabilities using Terraform and AWS CloudFormation. It enables automated provisioning, management, and versioning of cloud infrastructure across multiple providers. The module supports state management, module composition, plan/apply workflows, drift detection, and cost estimation, making it suitable for teams managing complex multi-cloud environments at scale.

## Core Capabilities

- **Multi-Provider Support**: Manage infrastructure across AWS, Azure, GCP, and custom providers
- **State Management**: Remote state with locking, versioning, and encryption
- **Module System**: Reusable infrastructure components with versioned registries
- **Plan/Apply Workflow**: Preview changes before applying with approval gates
- **CloudFormation Templates**: Generate and manage AWS CloudFormation templates
- **Stack Management**: Create, update, and delete CloudFormation stacks with rollback support
- **Cost Estimation**: Estimate infrastructure costs before deployment
- **Import & Drift Detection**: Import existing resources and detect configuration drift

## Usage Examples

### Terraform Configuration

```python
from terraform_cloudformation import TerraformManager, Provider, Module

manager = TerraformManager(work_dir="/infra/terraform")

# Define providers
manager.add_provider(Provider(
    name="aws",
    version="~> 5.0",
    config={"region": "us-east-1", "profile": "production"}
))

# Add modules
manager.add_module(Module(
    name="vpc",
    source = "terraform-aws-modules/vpc/aws",
    version="5.0.0",
    variables={
        "cidr": "10.0.0.0/16",
        "azs": ["us-east-1a", "us-east-1b"],
        "private_subnets": ["10.0.1.0/24", "10.0.2.0/24"],
        "public_subnets": ["10.0.101.0/24", "10.0.102.0/24"],
    }
))

# Generate configuration
config = manager.generate()
print(config)
```

### CloudFormation Template Generation

```python
from terraform_cloudformation import CloudFormationGenerator, Resource

generator = CloudFormationGenerator(
    template_name="production-stack",
    description="Production infrastructure"
)

# Add resources
generator.add_resource(Resource(
    type="AWS::EC2::VPC",
    logical_id="ProductionVPC",
    properties={
        "CidrBlock": "10.0.0.0/16",
        "EnableDnsHostnames": True,
        "EnableDnsSupport": True,
        "Tags": [{"Key": "Environment", "Value": "production"}],
    }
))

generator.add_resource(Resource(
    type="AWS::EC2::Subnet",
    logical_id="PublicSubnet1",
    properties={
        "VpcId": {"Ref": "ProductionVPC"},
        "CidrBlock": "10.0.1.0/24",
        "AvailabilityZone": "us-east-1a",
    }
))

# Generate template
template = generator.generate()
print(template)
```

### Plan and Apply Workflow

```python
from terraform_cloudformation import TerraformWorkflow, ApprovalGate

workflow = TerraformWorkflow(work_dir="/infra/terraform")

# Run plan
plan_result = workflow.plan(
    var_file="production.tfvars",
    parallelism=10,
)

print(f"Plan Summary:")
print(f"  Added: {plan_result.added}")
print(f"  Changed: {plan_result.changed}")
print(f"  Destroyed: {plan_result.destroyed}")
print(f"  Cost Estimate: {plan_result.cost_estimate}")

# Apply with approval gate
if plan_result.has_changes:
    gate = ApprovalGate(
        approvers=["lead-devops", "security-team"],
        timeout_hours=24,
    )
    if gate.request_approval(plan_result):
        apply_result = workflow.apply(auto_approve=False)
        print(f"Apply complete: {apply_result.resources_created} resources created")
```

## Best Practices

- **Remote State**: Always use remote state backends with state locking
- **State Encryption**: Enable encryption for sensitive state files
- **Module Versioning**: Pin module versions to avoid unexpected changes
- **Plan Review**: Always review plans before applying changes
- **Least Privilege**: Use minimal IAM permissions for Terraform execution
- **Secrets Management**: Never commit secrets to state files; use external secret stores
- **Workspace Isolation**: Use separate workspaces for different environments
- **Tagging Standards**: Enforce consistent tagging across all resources

## Related Modules

- **cloud-deployment**: Deployment orchestration for cloud resources
- **drift-detection**: Detect infrastructure configuration drift
- **ansible-playbooks**: Configuration management integration
