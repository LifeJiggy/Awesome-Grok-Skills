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
