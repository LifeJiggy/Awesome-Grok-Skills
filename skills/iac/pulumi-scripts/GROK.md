---
name: "pulumi-scripts"
category: "iac"
version: "2.0.0"
tags: ["iac", "pulumi", "infrastructure", "programming-languages", "cloud"]
description: "Infrastructure as Code using Pulumi with general-purpose programming languages"
---

# Pulumi Scripts

## Overview

The Pulumi Scripts module provides infrastructure as code capabilities using Pulumi, which allows defining cloud infrastructure using general-purpose programming languages like Python, TypeScript, Go, and C#. Unlike template-based IaC tools, Pulumi leverages the full power of programming languages including loops, conditionals, functions, classes, and package management. This module supports multi-cloud provisioning, component creation, stack configuration, and state management with backend options.

## Core Capabilities

- **Multi-Language Support**: Define infrastructure in Python, TypeScript, Go, or C#
- **Native Programming Constructs**: Use loops, conditionals, and functions for dynamic infrastructure
- **Component Resources**: Create reusable infrastructure components as custom resources
- **Stack References**: Share outputs between stacks for modular architectures
- **Policy as Code**: Define and enforce compliance policies using CrossGuard
- **Secrets Management**: Built-in encryption for sensitive configuration values
- **State Management**: Multiple backend options including Pulumi Cloud, S3, and local
- **Drift Detection**: Detect and remediate infrastructure configuration drift

## Usage Examples

### Basic Infrastructure Definition

```python
from pulumi import Config, Output
import pulumi_aws as aws

# Configuration
config = Config()
vpc_cidr = config.get("vpc_cidr") or "10.0.0.0/16"

# Create VPC
vpc = aws.ec2.Vpc("main-vpc",
    cidr_block=vpc_cidr,
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": "main-vpc", "Environment": "production"},
)

# Create subnets
public_subnet = aws.ec2.Subnet("public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",
    map_public_ip_on_launch=True,
    tags={"Name": "public-subnet"},
)

# Create internet gateway
igw = aws.ec2.InternetGateway("main-igw",
    vpc_id=vpc.id,
    tags={"Name": "main-igw"},
)

# Export outputs
export("vpc_id", vpc.id)
export("public_subnet_id", public_subnet.id)
```

### Component Resources

```python
from pulumi import ComponentResource, ResourceOptions
import pulumi_aws as aws

class WebServer(ComponentResource):
    def __init__(self, name: str, opts: ResourceOptions = None):
        super().__init__("custom:infrastructure:WebServer", name, {}, opts)

        # Create security group
        self.sg = aws.ec2.SecurityGroup(f"{name}-sg",
            description="Web server security group",
            vpc_id=opts.vpc_id if opts else "",
            ingress=[
                {"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]},
                {"protocol": "tcp", "from_port": 443, "to_port": 443, "cidr_blocks": ["0.0.0.0/0"]},
            ],
            egress=[{"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}],
            parent=self,
        )

        # Create EC2 instance
        self.instance = aws.ec2.Instance(f"{name}-instance",
            instance_type="t3.micro",
            ami="ami-0c55b159cbfafe1f0",
            vpc_security_group_ids=[self.sg.id],
            tags={"Name": name},
            parent=self,
        )

        self.register_outputs({
            "public_ip": self.instance.public_ip,
            "instance_id": self.instance.id,
        })
```

### Stack References

```python
from pulumi import stack_reference, export

# Reference another stack
network_stack = stack_reference("organization/network/production")

# Use outputs from the network stack
vpc_id = network_stack.get_output("vpc_id")
subnet_ids = network_stack.get_output("subnet_ids")

# Create resources using referenced values
app_server = aws.ec2.Instance("app-server",
    instance_type="t3.medium",
    ami="ami-0c55b159cbfafe1f0",
    subnet_id=subnet_ids[0],
    vpc_security_group_ids=[network_stack.get_output("app_sg_id")],
)

export("app_server_ip", app_server.public_ip)
```

### Policy as Code

```python
from pulumi_policy import EnforcementLevel, ResourceValidationPolicy

# Define policy
no_public_s3 = ResourceValidationPolicy(
    name="no-public-s3",
    description="S3 buckets should not be publicly accessible",
    enforcement_level=EnforcementLevel.ADVISORY,
    validate_resource=lambda args, report_violation: [
        report_violation("S3 buckets should not have public ACL")
        if args.get("acl") == "public-read"
        else None
    ],
)

# Apply policy
policies = [no_public_s3]
```

## Best Practices

- **Use Component Resources**: Abstract common patterns into reusable components
- **Leverage Programming Constructs**: Use loops and conditionals for dynamic infrastructure
- **Manage Secrets Properly**: Use Pulumi's secret management for sensitive values
- **Stack Separation**: Separate infrastructure into logical stacks (network, compute, database)
- **Policy Enforcement**: Define and enforce compliance policies early
- **Testing**: Write unit tests for infrastructure code using Pulumi's testing framework
- **Version Control**: Treat infrastructure code like application code with proper versioning
- **Documentation**: Document stack inputs, outputs, and dependencies

## Related Modules

- **terraform-cloudformation**: Alternative IaC tools for comparison
- **cloud-deployment**: Deployment orchestration for Pulumi-managed infrastructure
- **drift-detection**: Verify Pulumi-managed infrastructure state

---

## Advanced Configuration

### Backend Configuration

```python
# Pulumi.yaml
name: my-infrastructure
runtime: python
description: Cloud infrastructure using Pulumi

config:
  aws:region: us-east-1
  aws:profile: production
```

### Secrets Configuration

```python
from pulumi import Config

config = Config()
db_password = config.require_secret("db_password")
api_key = config.require_secret("api_key")
```

### Stack References for Cross-Stack Dependencies

```python
from pulumi import stack_reference

network_stack = stack_reference("organization/network/production")
vpc_id = network_stack.get_output("vpc_id")
subnet_ids = network_stack.get_output("subnet_ids")
```

### Dynamic Providers

```python
from pulumi.dynamic import ResourceProvider, CreateResult

class MyProvider(ResourceProvider):
    def create(self, inputs):
        # Custom resource creation logic
        return CreateResult(id_=inputs["name"], outs={**inputs})
```

### Resource Options Configuration

```python
from pulumi import ResourceOptions

opts = ResourceOptions(
    depends_on=[other_resource],
    protect=True,
    ignore_changes=["tags"],
    delete_before_replace=True,
    custom_timeout_seconds=300,
)
```

### Policy Enforcement

```python
from pulumi_policy import (
    EnforcementLevel,
    ResourceValidationPolicy,
    StackValidationPolicy,
)

require_encryption = ResourceValidationPolicy(
    name="require-encryption",
    description="All storage must be encrypted",
    enforcement_level=EnforcementLevel.MANDATORY,
    validate_resource=lambda args, report_violation: [
        report_violation("Storage must have encryption enabled")
        if not args.get("encrypted")
        else None
    ],
)
```

### Workspace Configuration

```python
# Multiple environments
environments = {
    "dev": {"replicas": 1, "instance_type": "t3.micro"},
    "staging": {"replicas": 2, "instance_type": "t3.small"},
    "production": {"replicas": 3, "instance_type": "t3.medium"},
}
```

## Architecture Patterns

### Multi-Stack Architecture

```python
# network/Pulumi.main.py
# compute/Pulumi.main.py
# database/Pulumi.main.py
# monitoring/Pulumi.main.py
```

### Component-Based Architecture

```python
from pulumi import ComponentResource

class MicroserviceStack(ComponentResource):
    def __init__(self, name, opts=None):
        super().__init__("custom:app:MicroserviceStack", name, {}, opts)

        self.vpc = self._create_vpc(name)
        self.cluster = self._create_cluster(name)
        self.database = self._create_database(name)
```

### GitOps Pattern

```yaml
# .github/workflows/pulumi.yml
name: Pulumi Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pulumi/actions@v3
        with:
          command: up
          stack-name: production
```

### Environment Promotion Pattern

```python
def promote_environment(source_env, target_env):
    # Copy configuration from source to target
    config = pulumi.Config()
    for key in config.keys():
        if key.startswith(f"{source_env}:"):
            target_key = key.replace(source_env, target_env)
            config.set(target_key, config.get(key))
```

### Service Catalog Pattern

```python
service_catalog = {
    "web-service": {
        "replicas": 3,
        "cpu": "500m",
        "memory": "512Mi",
        "port": 80,
    },
    "api-service": {
        "replicas": 5,
        "cpu": "1000m",
        "memory": "1Gi",
        "port": 8080,
    },
}
```

## Integration Guide

### CI/CD Integration

```yaml
# GitHub Actions
- name: Pulumi Up
  uses: pulumi/actions@v3
  with:
    command: up
    stack-name: ${{ github.ref_name }}
  env:
    PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
```

### Terraform State Import

```python
# Import existing Terraform resources
import pulumi_terraform as tf

existing_resource = tf.Resource(
    "existing-vpc",
    urn="urn:pulumi:prod::vpc::aws:ec2/vpc:Vpc::main",
    id="vpc-12345678",
)
```

### Kubernetes Integration

```python
import pulumi_kubernetes as k8s

# Deploy to Kubernetes
namespace = k8s.core.v1.Namespace("app-namespace")

deployment = k8s.apps.v1.Deployment(
    "app-deployment",
    metadata={"namespace": namespace.metadata.name},
    spec={
        "replicas": 3,
        "selector": {"matchLabels": {"app": "myapp"}},
        "template": {
            "metadata": {"labels": {"app": "myapp"}},
            "spec": {
                "containers": [{
                    "name": "myapp",
                    "image": "myapp:latest",
                    "ports": [{"containerPort": 80}],
                }],
            },
        },
    },
)
```

### AWS Lambda Integration

```python
import pulumi_aws as aws

lambda_role = aws.iam.Role("lambda-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
        }],
    }),
)

lambda_fn = aws.lambda_.Function("my-function",
    runtime="python3.11",
    handler="index.handler",
    role=lambda_role.arn,
    code=".",
)
```

### Azure Integration

```python
import pulumi_azure as azure

resource_group = azure.core.ResourceGroup("app-rg")

app_service = azure.appservice.Plan("app-plan",
    resource_group_name=resource_group.name,
    kind="Linux",
    reserved=True,
)
```

### GCP Integration

```python
import pulumi_gcp as gcp

network = gcp.compute.Network("app-network")

instance = gcp.compute.Instance("app-instance",
    machine_type="e2-medium",
    zone="us-central1-a",
    boot_disk={"initialize_params": {"image": "debian-cloud/debian-11"}},
    network_interfaces=[{"network": network.id}],
)
```

## Performance Optimization

### Parallel Resource Creation

```bash
# Pulumi automatically creates resources in parallel
pulumi up --parallel=20
```

### State Backend Optimization

```python
# Use fast state backend
config = {
    "backend": "s3",
    "bucket": "pulumi-state",
    "region": "us-east-1",
    "encrypt": True,
    "dynamodb_table": "pulumi-locks",
}
```

### Resource Caching

```python
from pulumi import Output

# Cache outputs to reduce API calls
cached_output = output.apply(lambda x: cache.get(x) or compute(x))
```

### Batch Operations

```python
# Create multiple resources in batch
for i in range(100):
    instance = aws.ec2.Instance(f"instance-{i}",
        instance_type="t3.micro",
        ami="ami-0c55b159cbfafe1f0",
    )
```

### Refresh Optimization

```bash
# Skip refresh for faster updates
pulumi up --refresh=false

# Selective refresh
pulumi refresh --target=urn:pulumi:prod::vpc::aws:ec2/vpc:Vpc::main
```

### Concurrent Stack Operations

```bash
# Deploy multiple stacks in parallel
pulumi up --stack dev &
pulumi up --stack staging &
wait
```

## Security Considerations

### Secrets Management

```python
from pulumi import Config

config = Config()

# Secret values are encrypted at rest
db_password = config.require_secret("db_password")
api_key = config.require_secret("api_key")

# Reference secrets from external stores
aws_secret = aws.secretsmanager.SecretVersion.get(
    "db-secret",
    secret_id="prod/database",
)
```

### IAM Best Practices

```python
# Least privilege IAM
role = aws.iam.Role("app-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
        }],
    }),
)

policy = aws.iam.RolePolicy("app-policy",
    role=role.id,
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["s3:GetObject"],
            "Resource": "arn:aws:s3:::my-bucket/*",
        }],
    }),
)
```

### Network Security

```python
security_group = aws.ec2.SecurityGroup("app-sg",
    vpc_id=vpc.id,
    ingress=[{
        "protocol": "tcp",
        "from_port": 443,
        "to_port": 443,
        "cidr_blocks": ["10.0.0.0/8"],
    }],
    egress=[{
        "protocol": "-1",
        "from_port": 0,
        "to_port": 0,
        "cidr_blocks": ["0.0.0.0/0"],
    }],
)
```

### Encryption at Rest

```python
bucket = aws.s3.Bucket("secure-bucket",
    server_side_encryption_configuration={
        "rule": {
            "apply_server_side_encryption_by_default": {
                "sse_algorithm": "AES256",
            },
        },
    },
)
```

### State File Security

```python
# Encrypt state file
pulumi_config = {
    "encrypt_secrets": True,
    "encryption_provider": "aws-kms",
    "kms_key_arn": "arn:aws:kms:us-east-1:123456789:key/abc-123",
}
```

### Compliance Policies

```python
from pulumi_policy import ResourceValidationPolicy

require_tags = ResourceValidationPolicy(
    name="require-tags",
    description="All resources must have required tags",
    enforcement_level=EnforcementLevel.MANDATORY,
    validate_resource=lambda args, report_violation: [
        report_violation(f"Missing required tag: {tag}")
        for tag in ["Environment", "Team", "CostCenter"]
        if tag not in args.get("tags", {})
    ],
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| State lock conflict | Another operation in progress | `pulumi state unlock` |
| Resource already exists | Created outside Pulumi | `pulumi import` resource |
| Plugin not found | Missing provider plugin | `pulumi plugin install` |
| Refresh timeout | Slow API responses | Increase timeout or use `--refresh=false` |
| Duplicate resource name | Naming conflict | Use unique names or stacks |
| Secret decryption failed | Wrong encryption key | Verify KMS key permissions |
| Stack reference not found | Wrong stack name or project | Verify stack path |

### Debug Mode

```bash
# Enable verbose logging
PULUMI_LOG_LEVEL=debug pulumi up

# Capture debug output
PULUMI_LOG_LEVEL=debug pulumi up 2>&1 | tee pulumi-debug.log
```

### State Recovery

```bash
# List state history
pulumi state history

# Restore previous state
pulumi state restore <deployment-id>
```

### Import Existing Resources

```bash
# Import by URN
pulumi import aws:ec2/vpc:Vpc main vpc-12345678

# Import from Terraform
pulumi import --from terraform aws:ec2/vpc:Vpc main vpc-12345678
```

### Resource Tainting

```bash
# Force replacement of resource
pulumi state tag --force-replace urn:pulumi:prod::vpc::aws:ec2/vpc:Vpc::main

# Repair corrupted state
pulumi state repair
```

## API Reference

### PulumiManager

```python
class PulumiManager:
    def __init__(self, project: str, stack: str):
        """Initialize Pulumi manager."""

    def up(self, parallel: int = 10) -> UpResult:
        """Deploy infrastructure."""

    def destroy(self) -> DestroyResult:
        """Destroy all resources."""

    def refresh(self) -> RefreshResult:
        """Refresh state from cloud."""

    def preview(self) -> PreviewResult:
        """Preview changes without applying."""

    def import_resource(self, urn: str, id: str) -> ImportResult:
        """Import existing resource."""
```

### ComponentResource

```python
class ComponentResource:
    def __init__(self, name: str, opts: ResourceOptions = None):
        """Initialize component resource."""

    def register_outputs(self, outputs: dict) -> None:
        """Register component outputs."""

    def add_child(self, name: str, resource) -> None:
        """Add child resource."""
```

### UpResult

```python
@dataclass
class UpResult:
    stdout: str
    stderr: str
    outputs: Dict[str, Output]
    summary: Summary
    resources_created: int
    resources_updated: int
    resources_deleted: int
```

### Summary

```python
@dataclass
class Summary:
    version: str
    plugin_versions: Dict[str, str]
    operations: int
    duration: float
    resource_count: int
```

### Output

```python
@dataclass
class Output:
    name: str
    value: Any
    secret: bool
    type: str
```

## Data Models

### Stack Configuration

```python
@dataclass
class StackConfig:
    name: str
    project: str
    config: Dict[str, Any]
    secrets: Dict[str, str]
    backend: str
```

### Resource State

```python
@dataclass
class ResourceState:
    urn: str
    type: str
    name: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    created: datetime
    modified: datetime
    deleted: datetime = None
```

### Deployment

```python
@dataclass
class Deployment:
    id: str
    stack: str
    project: str
    resources: List[ResourceState]
    created_at: datetime
    duration: float
    status: str
```

### Policy

```python
@dataclass
class Policy:
    name: str
    description: str
    enforcement_level: EnforcementLevel
    validate_resource: Callable
    validate_stack: Callable = None
```

### Config

```python
@dataclass
class Config:
    key: str
    value: Any
    secret: bool = False
    encrypted: bool = False
```

## Deployment Guide

### Stack Initialization

```bash
# Create new stack
pulumi stack init dev

# Set configuration
pulumi config set aws:region us-east-1
pulumi config set replicas 3

# Deploy
pulumi up
```

### Multi-Environment Deployment

```python
# Deploy to dev
pulumi stack select dev
pulumi up

# Deploy to production
pulumi stack select production
pulumi up
```

### Rollback Procedures

```bash
# View deployment history
pulumi deployment history

# Rollback to previous deployment
pulumi deployment rollback <deployment-id>
```

### Deployment Checklist

- [ ] Run `pulumi preview` to review changes
- [ ] Check for policy violations
- [ ] Verify secrets are encrypted
- [ ] Review cost estimates
- [ ] Test in non-production first
- [ ] Monitor deployment progress

## Monitoring & Observability

### CloudWatch Integration

```python
import pulumi_aws as cloudwatch

# Create dashboard
dashboard = cloudwatch.Dashboard("app-dashboard",
    dashboard_name="InfrastructureHealth",
    dashboard_body=json.dumps({
        "widgets": [
            {
                "type": "metric",
                "properties": {
                    "metrics": [["AWS/EC2", "CPUUtilization"]],
                    "title": "CPU Usage",
                },
            },
        ],
    }),
)
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pulumi.log"),
        logging.StreamHandler(),
    ],
)
```

### Alerting

```python
alarm = cloudwatch.MetricAlarm("high-cpu",
    comparison_operator="GreaterThanThreshold",
    evaluation_periods=2,
    metric_name="CPUUtilization",
    namespace="AWS/EC2",
    period=120,
    statistic="Average",
    threshold=80,
    alarm_actions=[sns_topic.arn],
)
```

### Dashboard Metrics

```python
metrics_config = {
    "widgets": [
        "resource_count",
        "deployment_duration",
        "error_rate",
        "cost_trend",
    ],
    "refresh_interval": "5m",
}
```

## Testing Strategy

### Unit Testing

```python
import pulumi
from pulumi.testing import assert_equal

def test_vpc_cidr():
    vpc = aws.ec2.Vpc("test-vpc",
        cidr_block="10.0.0.0/16",
    )
    assert_equal(vpc.cidr_block, "10.0.0.0/16")
```

### Integration Testing

```python
def test_full_stack():
    # Deploy stack
    result = pulumi.up()
    assert result.resources_created > 0

    # Verify resources
    vpc = get_vpc(result.outputs["vpc_id"])
    assert vpc is not None

    # Cleanup
    pulumi.destroy()
```

### Policy Testing

```python
def test_policy_enforcement():
    # Test that policy catches violations
    with pytest.raises(PolicyViolationError):
        # Try to create non-compliant resource
        create_public_bucket()
```

### Snapshot Testing

```python
def test_stack_snapshot():
    result = pulumi.preview()
    snapshot.assert_match(result.plan, "stack-snapshot.json")
```

## Versioning & Migration

### Pulumi Version Management

```bash
# Check current version
pulumi version

# Update Pulumi
curl -fsSL https://get.pulumi.com | sh

# Update provider plugins
pulumi plugin install aws
```

### State Migration

```bash
# Migrate between backends
pulumi state migrate --new-backend=s3://my-state-bucket

# Export state
pulumi stack export --file=state.json

# Import state
pulumi stack import --file=state.json
```

### Breaking Changes

```python
# Version compatibility matrix
compatibility = {
    "pulumi-aws": {
        "5.0.0": {"breaking": ["vpc.cidr_block type change"]},
        "6.0.0": {"breaking": ["removed deprecated resources"]},
    },
}
```

## Glossary

| Term | Definition |
|------|------------|
| **Stack** | A deployment of Pulumi programs |
| **Resource** | Infrastructure component managed by Pulumi |
| **Output** | A value produced by a resource |
| **URN** | Unique Resource Name identifier |
| **Component Resource** | Reusable infrastructure building block |
| **Policy** | Compliance rule enforced during deployment |
| **Backend** | Where Pulumi state is stored |
| **Config** | Configuration values for a stack |
| **Secret** | Encrypted configuration value |
| **Plugin** | Provider plugin for cloud APIs |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with multi-cloud support |
| 1.5.0 | 2024-11-01 | Added policy enforcement |
| 1.4.0 | 2024-09-15 | Component resource improvements |
| 1.3.0 | 2024-07-20 | Secrets management enhancements |
| 1.2.0 | 2024-05-10 | Stack reference support |
| 1.1.0 | 2024-03-01 | Performance optimizations |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow Pulumi coding standards
2. Write unit tests for new components
3. Document all outputs and inputs
4. Include examples in README
5. Test with multiple providers
6. Update changelog for changes

## License

MIT License. See LICENSE file for full terms.
