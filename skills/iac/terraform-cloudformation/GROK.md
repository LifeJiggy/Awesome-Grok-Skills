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

---

## Advanced Configuration

### Remote State Backend Configuration

Terraform supports multiple remote state backends for collaborative infrastructure management:

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    profile        = "terraform-backend"
  }
}
```

### CloudFormation Drift Configuration

```yaml
DriftDetection:
  Type: AWS::CloudFormation::StackDriftDetection
  Properties:
    StackIds:
      - !Ref ProductionStack
      - !Ref StagingStack
    DetectionThreshold: 10
```

### Multi-Provider Workspace Setup

```python
# Advanced workspace configuration
workspace_config = {
    "default": {
        "backend": "s3",
        "encrypt": True,
        "dynamodb_table": "tf-locks",
    },
    "production": {
        "state_file": "s3://tf-state-prod/terraform.tfstate",
        "lock_table": "tf-locks-prod",
    },
    "staging": {
        "state_file": "s3://tf-state-staging/terraform.tfstate",
        "lock_table": "tf-locks-staging",
    },
}
```

### Module Registry Configuration

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  # ...
}
```

### State Encryption Settings

```python
encryption_config = {
    "algorithm": "AES256",
    "key_arn": "arn:aws:kms:us-east-1:123456789:key/abc-123",
    "encrypt_at_rest": True,
    "encrypt_in_transit": True,
}
```

### Provider Alias Configuration

```hcl
provider "aws" {
  alias  = "us_east"
  region = "us-east-1"
}

provider "aws" {
  alias  = "eu_west"
  region = "eu-west-1"
}
```

## Architecture Patterns

### Hub-and-Spoke Multi-Account Pattern

Use a central networking account (hub) that peers with spoke accounts:

```python
class HubSpokeArchitecture:
    def __init__(self, hub_account, spoke_accounts):
        self.hub_account = hub_account
        self.spoke_accounts = spoke_accounts

    def create_hub_vpc(self):
        return {
            "vpc_cidr": "10.0.0.0/16",
            "subnets": {
                "shared_services": "10.0.1.0/24",
                "transit_gateway": "10.0.2.0/24",
            },
        }

    def create_spoke_peering(self, spoke):
        return {
            "vpc_id": spoke.vpc_id,
            "peer_connection_id": self.hub_account.vpc_id,
            "route_tables": spoke.private_route_tables,
        }
```

### Modular Infrastructure Pattern

```python
# Modular approach - separate concerns
modules = {
    "networking": {"source": "./modules/vpc", "version": "1.0.0"},
    "compute": {"source": "./modules/ecs", "version": "1.0.0"},
    "database": {"source": "./modules/rds", "version": "1.0.0"},
    "monitoring": {"source": "./modules/cloudwatch", "version": "1.0.0"},
}
```

### GitOps Workflow Pattern

```yaml
# .github/workflows/terraform.yml
name: Terraform
on:
  push:
    branches: [main]
    paths: ['infra/**']
jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform plan
      - run: terraform apply
```

### Immutable Infrastructure Pattern

Deploy new infrastructure instead of modifying existing resources:

```python
immutable_config = {
    "strategy": "replace",
    "lifecycle": {
        "create_before_destroy": True,
        "prevent_destroy": False,
        "ignore_changes": ["tags"],
    },
}
```

### Multi-Environment Promotion Pattern

```python
environments = ["dev", "staging", "production"]
promotion_flow = {
    "dev": {"auto_apply": True, "approval": False},
    "staging": {"auto_apply": True, "approval": False},
    "production": {"auto_apply": False, "approval": True},
}
```

## Integration Guide

### CI/CD Pipeline Integration

```yaml
# Jenkins pipeline integration
pipeline {
    agent any
    stages {
        stage('Terraform Init') {
            steps { sh 'terraform init' }
        }
        stage('Terraform Plan') {
            steps { sh 'terraform plan -out=tfplan' }
        }
        stage('Approval') {
            steps {
                input message: 'Approve plan?'
            }
        }
        stage('Terraform Apply') {
            steps { sh 'terraform apply tfplan' }
        }
    }
}
```

### Slack Notification Integration

```python
def notify_slack(plan_result, webhook_url):
    import requests
    payload = {
        "text": f"Terraform Plan: {plan_result.added} added, "
                f"{plan_result.changed} changed, "
                f"{plan_result.destroyed} destroyed",
        "color": "warning" if plan_result.has_changes else "good",
    }
    requests.post(webhook_url, json=payload)
```

### Ansible Integration

```yaml
- name: Terraform provisioning
  hosts: localhost
  tasks:
    - name: Run Terraform
      community.general.terraform:
        project_path: ./infra/terraform
        state: present
```

### Kubernetes Provider Integration

```hcl
provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_ca)
  token                  = data.aws_eks_cluster_auth.main.token
}
```

### Vault Integration for Secrets

```hcl
data "vault_generic_secret" "db_credentials" {
  path = "secret/data/production/database"
}

resource "aws_db_instance" "main" {
  password = data.vault_generic_secret.db_credentials.data["password"]
}
```

### Monitoring Stack Integration

```python
monitoring_integration = {
    "cloudwatch": {"namespace": "Terraform", "metrics": ["drift_count"]},
    "datadog": {"api_key": "xxx", "tags": ["env:production"]},
    "pagerduty": {"service_key": "xxx", "severity": "warning"},
}
```

## Performance Optimization

### Parallel Execution

```bash
# Increase parallelism for large infrastructures
terraform apply -parallelism=20
```

### State File Optimization

```python
# Split large state files into smaller modules
state_optimization = {
    "split_strategy": "by_service",
    "max_resources_per_state": 500,
    "use_remote_state_data_sources": True,
}
```

### Plan Caching

```bash
# Cache plans for repeated applies
terraform plan -out=tfplan
terraform apply tfplan  # Reuse cached plan
```

### Targeted Operations

```bash
# Only apply changes to specific resources
terraform apply -target=module.vpc
terraform plan -target=aws_instance.web[0]
```

### Resource Tainting Strategy

```bash
# Force recreation of specific resources
terraform taint aws_instance.web
terraform untaint aws_instance.web
```

### Refresh Interval Management

```python
refresh_config = {
    "auto_refresh": False,
    "refresh_interval": "30m",
    "target_refresh_interval": "5m",
}
```

### Large State File Handling

```python
large_state_config = {
    "use_backend_config": True,
    "state_splitting": True,
    "max_concurrent_ops": 10,
    "retry_count": 3,
    "retry_delay": "5s",
}
```

## Security Considerations

### State File Encryption

Always encrypt state files at rest and in transit:

```python
security_config = {
    "encrypt_at_rest": True,
    "encrypt_in_transit": True,
    "kms_key_id": "arn:aws:kms:us-east-1:123456789:key/abc-123",
    "state_encryption": "AES256",
}
```

### Secrets Management

```hcl
# Use variables for sensitive values
variable "db_password" {
  type      = string
  sensitive = true
}

# Reference external secret stores
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/database/password"
}
```

### IAM Least Privilege

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:*",
        "s3:ListBucket",
        "s3:GetObject"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "us-east-1"
        }
      }
    }
  ]
}
```

### State Locking

```hcl
terraform {
  backend "s3" {
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### Sensitive Data in Logs

```python
# Suppress sensitive output
import logging
logging.getLogger("terraform").setLevel(logging.WARNING)

# Use sensitive markers
sensitive_vars = {
    "db_password": "sensitive",
    "api_key": "sensitive",
    "cert_private_key": "sensitive",
}
```

### Compliance Guardrails

```python
compliance_policies = {
    "encryption_required": True,
    "tagging_required": True,
    "allowed_regions": ["us-east-1", "eu-west-1"],
    "max_instance_size": "xlarge",
}
```

### Network Security

```hcl
resource "aws_security_group" "restricted" {
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| State lock timeout | Another process holds the lock | `terraform force-unlock LOCK_ID` |
| Provider version conflict | Incompatible provider versions | Pin provider versions in `required_providers` |
| Resource already exists | Resource created outside Terraform | Import resource: `terraform import` |
| Drift detection failure | Backend connectivity issues | Check backend credentials and connectivity |
| Module not found | Source path or registry error | Verify module source and version |
| Plan error: invalid HCL | Syntax error in configuration | Run `terraform validate` to find issues |
| Apply failed | Resource creation error | Check CloudTrail/console for detailed errors |
| State corruption | Interrupted apply or manual edit | Restore from backup; use state migration |

### Debug Mode

```bash
# Enable detailed logging
export TF_LOG=DEBUG
export TF_LOG_PATH=/tmp/terraform.log
terraform apply
```

### State Recovery

```bash
# List state backups
ls terraform.tfstate.backup

# Recover state
cp terraform.tfstate.backup terraform.tfstate

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0
```

### Performance Issues

```bash
# Check plan generation time
time terraform plan

# Optimize provider plugins
terraform init -upgrade
```

## API Reference

### TerraformManager

```python
class TerraformManager:
    def __init__(self, work_dir: str, backend: str = "s3"):
        """Initialize Terraform manager."""

    def init(self, upgrade: bool = False) -> InitResult:
        """Initialize working directory."""

    def plan(self, var_file: str = None) -> PlanResult:
        """Generate execution plan."""

    def apply(self, auto_approve: bool = False) -> ApplyResult:
        """Apply changes to infrastructure."""

    def destroy(self, target: str = None) -> DestroyResult:
        """Destroy infrastructure resources."""

    def state_list(self) -> List[Resource]:
        """List resources in state."""

    def import_resource(self, address: str, id: str) -> ImportResult:
        """Import existing resource."""

    def validate(self) -> ValidationResult:
        """Validate configuration syntax."""
```

### CloudFormationGenerator

```python
class CloudFormationGenerator:
    def __init__(self, template_name: str, description: str = ""):
        """Initialize generator."""

    def add_resource(self, resource: Resource) -> None:
        """Add resource to template."""

    def add_output(self, output: Output) -> None:
        """Add output to template."""

    def add_parameter(self, parameter: Parameter) -> None:
        """Add parameter to template."""

    def generate(self) -> dict:
        """Generate CloudFormation template."""

    def validate(self) -> ValidationResult:
        """Validate template against CloudFormation schema."""

    def deploy(self, stack_name: str) -> DeployResult:
        """Deploy template as CloudFormation stack."""
```

### PlanResult

```python
@dataclass
class PlanResult:
    added: int
    changed: int
    destroyed: int
    has_changes: bool
    cost_estimate: CostEstimate
    resource_changes: List[ResourceChange]
    execution_time: float
```

### Module

```python
@dataclass
class Module:
    name: str
    source: str
    version: str
    variables: Dict[str, Any]
    depends_on: List[str] = field(default_factory=list)
```

### Provider

```python
@dataclass
class Provider:
    name: str
    version: str
    config: Dict[str, Any]
    alias: Optional[str] = None
```

## Data Models

### Resource State

```python
@dataclass
class ResourceState:
    address: str
    resource_type: str
    name: str
    provider_name: str
    values: Dict[str, Any]
    depends_on: List[str]
    created_at: datetime
    updated_at: datetime
```

### Module Output

```python
@dataclass
class ModuleOutput:
    name: str
    value: Any
    sensitive: bool
    description: str
```

### Drift Event

```python
@dataclass
class DriftEvent:
    resource_address: str
    drift_type: DriftType
    severity: str
    changes: List[AttributeChange]
    detected_at: datetime
    remediation_status: str
```

### Cost Estimate

```python
@dataclass
class CostEstimate:
    monthly_cost: float
    currency: str
    resources: List[ResourceCost]
    confidence: float
```

### Stack Configuration

```python
@dataclass
class StackConfiguration:
    name: str
    backend: str
    state_file: str
    lock_table: str
    encryption_key: str
    regions: List[str]
```

## Deployment Guide

### Environment Setup

```bash
# Development
terraform init -backend-config="env=dev"

# Staging
terraform init -backend-config="env=staging"

# Production
terraform init -backend-config="env=production"
```

### Blue-Green Deployment

```python
blue_green_config = {
    "blue": {"environment": "prod-blue", "weight": 100},
    "green": {"environment": "prod-green", "weight": 0},
    "switch_strategy": "gradual",
    "switch_interval": "5m",
}
```

### Rollback Procedures

```bash
# Quick rollback via state backup
cp terraform.tfstate.backup terraform.tfstate
terraform apply

# Targeted rollback
terraform apply -target=module.vpc
```

### Deployment Checklist

- [ ] Run `terraform validate`
- [ ] Run `terraform plan` and review changes
- [ ] Check cost estimate
- [ ] Verify state lock is acquired
- [ ] Apply with approval gate
- [ ] Verify resources are healthy
- [ ] Update documentation

### Multi-Region Deployment

```python
regions = ["us-east-1", "eu-west-1", "ap-southeast-1"]
for region in regions:
    deploy_to_region(region, config)
```

## Monitoring & Observability

### CloudWatch Integration

```python
cloudwatch_config = {
    "namespace": "Terraform/Infrastructure",
    "metrics": [
        {"name": "ResourceCount", "unit": "Count"},
        {"name": "DriftEvents", "unit": "Count"},
        {"name": "ApplyDuration", "unit": "Seconds"},
    ],
    "alarms": [
        {"name": "HighDriftRate", "threshold": 10, "period": 3600},
    ],
}
```

### Logging Configuration

```python
logging_config = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": ["file", "cloudwatch", "slack"],
    "sensitive_fields": ["password", "token", "key"],
}
```

### Health Checks

```python
health_checks = [
    {"name": "state_backend", "type": "connectivity", "timeout": 10},
    {"name": "provider_auth", "type": "authentication", "timeout": 30},
    {"name": "resource_health", "type": "api_call", "timeout": 60},
]
```

### Alerting Rules

```python
alerting_rules = [
    {
        "name": "drift_detected",
        "condition": "drift_count > 0",
        "severity": "warning",
        "channels": ["slack", "email"],
    },
    {
        "name": "apply_failed",
        "condition": "apply_status == 'failed'",
        "severity": "critical",
        "channels": ["slack", "pagerduty"],
    },
]
```

### Dashboard Configuration

```python
dashboard_config = {
    "title": "Infrastructure Health",
    "widgets": [
        "resource_count_chart",
        "drift_events_table",
        "cost_trend_line",
        "apply_history_bar",
    ],
    "refresh_interval": "5m",
}
```

## Testing Strategy

### Terraform Validate

```bash
# Syntax validation
terraform validate

# Format checking
terraform fmt -check
```

### Plan Testing

```python
def test_plan():
    plan = terraform.plan()
    assert plan.added >= 0
    assert plan.destroyed == 0  # No unintended destruction
```

### Integration Testing

```python
class TestInfrastructure:
    def test_vpc_exists(self):
        assert describe_vpc(vpc_id) is not None

    def test_security_groups(self):
        sgs = describe_security_groups()
        assert len(sgs) >= 2

    def test_tags_compliance(self):
        resources = list_all_resources()
        for r in resources:
            assert "Environment" in r.tags
```

### Compliance Testing

```python
def test_compliance():
    resources = terraform.state_list()
    for resource in resources:
        assert has_required_tags(resource)
        assert has_encryption_enabled(resource)
```

### Cost Testing

```python
def test_cost_budget():
    plan = terraform.plan()
    assert plan.cost_estimate.monthly_cost < 1000
```

## Versioning & Migration

### Semantic Versioning

```python
version_config = {
    "strategy": "semver",
    "major": "breaking changes",
    "minor": "new features",
    "patch": "bug fixes",
}
```

### State Migration

```bash
# Migrate state to new backend
terraform state pull > terraform.tfstate
# Update backend configuration
terraform init -migrate-state
```

### Provider Version Pinning

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

### Module Versioning

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"  # Pin to specific version
}
```

## Glossary

| Term | Definition |
|------|------------|
| **State** | A file tracking the mapping of real resources to configuration |
| **Plan** | A preview of changes Terraform will make |
| **Drift** | Deviation of actual infrastructure from desired state |
| **Module** | A container for multiple resources used together |
| **Provider** | A plugin that interacts with cloud APIs |
| **Backend** | Where Terraform state is stored |
| **Stack** | A CloudFormation collection of resources |
| **Template** | A JSON/YAML file defining CloudFormation resources |
| **Terraform Cloud** | HashiCorp's managed service for Terraform |
| **HCL** | HashiCorp Configuration Language |
| **TFState** | Terraform state file format |
| **Workspaces** | Named configurations for managing multiple environments |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with multi-provider support |
| 1.5.0 | 2024-11-01 | Added cost estimation features |
| 1.4.0 | 2024-09-15 | CloudFormation template generation |
| 1.3.0 | 2024-07-20 | Drift detection integration |
| 1.2.0 | 2024-05-10 | Module versioning support |
| 1.1.0 | 2024-03-01 | State locking improvements |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request with detailed description
6. Follow the code style guide
7. Update documentation for new features
8. Add changelog entries

## License

MIT License. See LICENSE file for full terms.
