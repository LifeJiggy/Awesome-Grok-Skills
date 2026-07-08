# AWS Specialist Agent

Senior cloud engineer and automation agent for designing, provisioning, securing, and operating AWS infrastructure with production-grade rigor.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Compute](#compute)
  - [Storage](#storage)
  - [Networking](#networking)
  - [Database](#database)
  - [Security & IAM](#security--iam)
  - [Monitoring](#monitoring)
  - [Messaging](#messaging)
  - [IaC & Deployment](#iac--deployment)
  - [Cost Management](#cost-management)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Security & Compliance](#security--compliance)
- [Architecture Details](#architecture-details)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The AWS Specialist Agent manages the full AWS infrastructure lifecycle through validated, typed, and observable methods. It enforces Well-Architected Framework principles across compute, storage, networking, databases, security, and governance.

**Key Benefits:**
- Complete AWS infrastructure lifecycle management
- Well-Architected Framework compliance
- Cost optimization and right-sizing recommendations
- Security-first approach with least-privilege IAM
- Infrastructure as Code support (CloudFormation, Terraform)

**Use Cases:**
- New infrastructure provisioning and setup
- Existing infrastructure optimization
- Security hardening and compliance
- Cost reduction and optimization
- Disaster recovery planning
- CI/CD pipeline infrastructure

## Features

| Domain | Key Capabilities |
|--------|------------------|
| **Compute** | EC2 provisioning/management, Lambda deployment, ECS/EKS container services, Batch computing |
| **Storage** | S3 lifecycle and versioning, EBS volumes and snapshots, KMS encryption |
| **Networking** | VPC design, subnet planning, security groups, load balancers, Route53, CloudFront |
| **Databases** | RDS/Aurora, DynamoDB, ElastiCache, DB subnet groups |
| **Security** | IAM roles/policies, KMS key management, GuardDuty, Config rules, audit logging |
| **Monitoring** | CloudWatch alarms, metric streams, cost estimation, optimization recommendations |
| **IaC** | CloudFormation, Terraform, CDK, Pulumi deployment workflows |
| **Messaging** | SNS topics/subscriptions, SQS queuing, EventBridge patterns |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         AWSSpecialistAgent                                       │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────────────────────┤
│   Compute   │   Storage   │  Networking │  Database   │      Security           │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────────────────┤
│ EC2         │ S3          │ VPC         │ RDS         │ IAM                     │
│ Lambda      │ EBS         │ Subnets     │ DynamoDB    │ KMS                     │
│ ECS/EKS     │ KMS         │ SecurityGrp │ ElastiCache │ Secrets Manager         │
│ Batch       │             │ LoadBalancer│ DB SubnetGrp│ GuardDuty               │
├─────────────┴─────────────┴─────────────┴─────────────┴─────────────────────────┤
│                         Monitoring & Observability                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│ CloudWatch │ Cost Explorer │ Config Rules │ Health Dashboard │ Trusted Advisor  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                         Messaging & Events                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│ SNS Topics │ SQS Queues │ EventBridge │ Step Functions │ AppSync               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                         IaC & Deployment                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│ CloudFormation │ Terraform │ CDK │ CodePipeline │ CodeDeploy                   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for deep dives on compute, storage, networking, database, security, observability, and disaster recovery patterns.

## Quick Start

```python
from agents.aws_specialist.agent import AWSSpecialistAgent, Config

config = Config(
    region="us-east-1",
    environment="production",
    tags={"Team": "platform", "CostCenter": "engineering"}
)

agent = AWSSpecialistAgent(config=config)

# Provision a VPC with public and private subnets
vpc = agent.create_vpc("10.0.0.0/16", "main-vpc")
public_subnet = agent.add_subnet(vpc.id, "10.0.1.0/24", "us-east-1a", public=True)
private_subnet = agent.add_subnet(vpc.id, "10.0.2.0/24", "us-east-1a", public=False)

# Create security group permitting HTTPS
from agents.aws_specialist.agent import SecurityGroupRule
web_sg = agent.create_security_group(
    vpc.id, "web-sg", "Web tier",
    ingress_rules=[SecurityGroupRule("tcp", 443, 443, "0.0.0.0/0", "HTTPS")]
)

# Launch EC2 instance
instance = agent.provision_ec2(
    name="web-server-1",
    instance_type="t3.micro",
    ami_id="ami-0abcdef1234567890",
    security_group_ids=[web_sg.id],
    tags={"Role": "frontend"}
)
print(instance.id, instance.state)
```

Run the demo:

```bash
python agents/aws-specialist/agent.py
```

## Installation

### Requirements

- Python 3.9+
- boto3 (optional, for real AWS access; agent works in offline/mock mode by default)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills

# Install dependencies (optional)
pip install boto3

# Install in development mode
pip install -e .
```

## Usage

### Compute

```python
# EC2 Instance Management
instance = agent.provision_ec2(
    name="web-server-1",
    instance_type="t3.micro",
    ami_id="ami-0abcdef1234567890",
    security_group_ids=[web_sg.id],
    subnet_id=public_subnet.id,
    tags={"Role": "frontend", "Environment": "production"}
)

# Get instance details
details = agent.get_instance(instance.id)
# {"id": "i-abc123", "state": "running", "public_ip": "203.0.113.42", ...}

# List instances
running = agent.list_instances(state_filter="running")
# [Instance(...), Instance(...), ...]

# Instance lifecycle
agent.start_instance(instance.id)
agent.stop_instance(instance.id)
agent.terminate_instance(instance.id, force=False)

# Lambda Functions
function = agent.deploy_lambda(
    function_name="process-uploads",
    runtime="python3.11",
    handler="index.handler",
    memory_mb=256,
    timeout_seconds=30,
    role_arn="arn:aws:iam::123456789012:role/lambda-role",
    environment_variables={"BUCKET": "my-uploads"},
    code_s3_bucket="my-deployments",
    code_s3_key="lambda/process-uploads.zip"
)

# ECS/EKS Container Services
service = agent.setup_container_service(
    service_name="api-service",
    cpu="256",
    memory="512",
    desired_count=2,
    launch_type="FARGATE",
    environment_variables={"DB_HOST": "mydb.cluster.us-east-1.rds.amazonaws.com"},
    secrets={"DB_PASSWORD": "arn:aws:secretsmanager:us-east-1:123456789012:secret:db-password"}
)

# EKS Cluster
cluster = agent.create_eks_cluster(
    cluster_name="production-cluster",
    kubernetes_version="1.28",
    endpoint_public_access=True
)
```

### Storage

```python
# S3 Bucket Configuration
bucket = agent.configure_s3_bucket(
    bucket_name="my-app-assets",
    versioning=True,
    encryption="aws:kms",
    lifecycle_rules=[
        {"id": "archive-old-logs", "prefix": "logs/", "transition_days": 90, "storage_class": "GLACIER"}
    ],
    cors=[
        {"allowed_origins": ["https://myapp.com"], "allowed_methods": ["GET", "HEAD"]}
    ],
    tags={"Environment": "production", "Team": "platform"}
)

# Upload object
agent.upload_object_to_s3(
    bucket_name="my-app-assets",
    key="images/logo.png",
    data=open("logo.png", "rb").read(),
    content_type="image/png"
)

# KMS Key Management
key = agent.create_kms_key(
    description="Encryption key for application data",
    key_usage="ENCRYPT_DECRYPT",
    origin="AWS_KMS"
)
# key.id = "key-abc123"
# key.arn = "arn:aws:kms:us-east-1:123456789012:key/key-abc123"
```

### Networking

```python
# VPC Creation
vpc = agent.create_vpc("10.0.0.0/16", "production-vpc")
# vpc.id = "vpc-abc123"

# Subnets
public_subnet = agent.add_subnet(
    vpc.id, "10.0.1.0/24", "us-east-1a",
    public=True, map_public_ip=True
)
private_subnet = agent.add_subnet(
    vpc.id, "10.0.2.0/24", "us-east-1a",
    public=False
)

# Security Groups
web_sg = agent.create_security_group(
    vpc.id, "web-sg", "Web tier security group",
    ingress_rules=[
        SecurityGroupRule("tcp", 443, 443, "0.0.0.0/0", "HTTPS"),
        SecurityGroupRule("tcp", 80, 80, "0.0.0.0/0", "HTTP")
    ],
    egress_rules=[
        SecurityGroupRule("tcp", 443, 443, "0.0.0.0/0", "HTTPS outbound")
    ]
)

# Additional ingress rules
agent.authorize_security_group_ingress(
    web_sg.id, "tcp", 8080, 8080, "10.0.0.0/16", "Internal API"
)

# Internet Gateway
igw = agent.attach_internet_gateway(vpc.id)

# VPC Peering
peering = agent.configure_vpc_peering(
    requester_vpc_id="vpc-abc123",
    accepter_vpc_id="vpc-def456"
)

# Route53 DNS
zone = agent.setup_route53("example.com", private=False)

# CloudFront CDN
distribution = agent.create_cloudfront_distribution(
    origin_domain="myapp-assets.s3.amazonaws.com",
    origin_path="/static",
    enabled=True
)
```

### Database

```python
# RDS Instance
db = agent.create_rds_instance(
    db_instance_identifier="production-db",
    engine="postgres",
    db_instance_class="db.r6g.large",
    master_username="admin",
    master_password="secure-password-here",
    allocated_storage_gb=100,
    storage_type="gp3",
    multi_az=True,
    publicly_accessible=False,
    db_subnet_group_name="production-subnet-group",
    backup_retention_days=14,
    DeletionProtection=True
)

# DynamoDB Table
table = agent.create_dynamodb_table(
    table_name="user-sessions",
    partition_key="session_id",
    partition_key_type="S",
    sort_key="user_id",
    billing_mode="PAY_PER_REQUEST",
    tags={"Environment": "production"}
)

# DB Subnet Group
subnet_group = agent.create_db_subnet_group(
    name="production-subnet-group",
    subnet_ids=["subnet-abc", "subnet-def"],
    description="Subnet group for production databases"
)
```

### Security & IAM

```python
# IAM Role
role = agent.create_iam_role(
    role_name="ec2-s3-role",
    assume_role_policy={
        "Version": "2012-10-17",
        "Statement": [
            {"Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"}, "Action": "sts:AssumeRole"}
        ]
    },
    policies=[
        agent.generate_iam_policy(
            actions=["s3:GetObject", "s3:PutObject"],
            resources=["arn:aws:s3:::my-bucket/*"]
        )
    ]
)

# CloudWatch Alarm
alarm = agent.create_cloudwatch_alarm(
    alarm_name="high-cpu-utilization",
    metric_name="CPUUtilization",
    namespace="AWS/EC2",
    statistic="Average",
    period=300,
    evaluation_periods=3,
    threshold=80.0,
    comparison_operator="GreaterThanThreshold",
    dimensions={"InstanceId": "i-abc123"}
)

# Permissions Boundary
agent.add_permissions_boundary(role.arn, "arn:aws:iam::123456789012:policy/BoundaryPolicy")
```

### Monitoring

```python
# Get infrastructure status
status = agent.get_status()
# {
#   "vpcs": 2,
#   "instances": 15,
#   "load_balancers": 3,
#   "rds_instances": 4,
#   "s3_buckets": 12
# }

# Infrastructure summary
summary = agent.get_infrastructure_summary()
# {
#   "compute": {"ec2": 15, "lambda": 8, "ecs_services": 3},
#   "storage": {"s3_buckets": 12, "ebs_volumes": 20},
#   "networking": {"vpcs": 2, "subnets": 8, "security_groups": 15},
#   "databases": {"rds": 4, "dynamodb": 6, "elasticache": 2}
# }

# Metrics report
metrics = agent.get_metrics_report()
# {
#   "period": "last_30_days",
#   "cost_estimate": {"total": 12500.00, "by_service": {...}},
#   "utilization": {"ec2_avg": 45.0, "rds_avg": 62.0},
#   "recommendations": [
#     {"type": "rightsize", "resource": "i-abc123", "suggestion": "Downsize to t3.small"}
#   ]
# }

# Validation
validation = agent.validate_configuration()
# {"valid": True, "warnings": [], "errors": []}

# Cost optimization
optimization = agent.optimize_cost()
# {
#   "total_savings_potential": 3500.00,
#   "recommendations": [
#     {"type": "reserved_instances", "savings": 2000.00, "confidence": "high"},
#     {"type": "rightsize", "savings": 1000.00, "confidence": "medium"},
#     {"type": "delete_idle", "savings": 500.00, "confidence": "high"}
#   ]
# }
```

### Messaging

```python
# SNS Topic
topic = agent.publish_sns_topic("alerts", display_name="Infrastructure Alerts")

# SNS Subscription
subscription = agent.create_sns_subscription(
    topic_arn=topic.arn,
    protocol="email",
    endpoint="ops-team@company.com"
)

# SQS Queue
queue = agent.send_sqs_message(
    queue_url="https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",
    message_body='{"event": "deployment_complete", "service": "api"}',
    delay_seconds=0
)

# CloudWatch Metric Stream
stream = agent.create_cloudwatch_metric_stream(
    name="cost-metrics-stream",
    output_format="JSON",
    include_filters=["AWS/Billing*", "AWS/EC2*"]
)
```

### IaC & Deployment

```python
# CloudFormation Stack
stack = agent.deploy_cloudformation_stack(
    stack_name="production-infrastructure",
    template_body=open("template.yaml").read(),
    parameters={"Environment": "production", "VpcCIDR": "10.0.0.0/16"}
)

# Terraform Deployment
agent.deploy_infrastructure_as_code(
    infrastructure_code=open("main.tf").read(),
    format_type="terraform",
    variables={"environment": "production", "region": "us-east-1"}
)
```

### Cost Management

```python
# Get cost breakdown
costs = agent.get_cost_breakdown(
    start_date="2025-01-01",
    end_date="2025-01-31",
    granularity="MONTHLY"
)
# {
#   "total": 12500.00,
#   "by_service": {
#     "EC2": 4500.00,
#     "RDS": 3200.00,
#     "S3": 800.00,
#     "Data Transfer": 1500.00
#   },
#   "by_tag": {
#     "Team:platform": 8000.00,
#     "Team:data": 4500.00
#   }
# }

# Export state
state = agent.export_state()
# Saves current infrastructure state to JSON

# Import state
agent.import_state(state)
```

## API Reference

### Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `region` | `str` | `us-east-1` | AWS region |
| `environment` | `str` | `development` | Environment label |
| `default_instance_type` | `str` | `t3.micro` | Default EC2 type |
| `auto_scaling` | `bool` | `True` | Enable auto scaling |
| `enable_monitoring` | `bool` | `True` | CloudWatch monitoring |
| `max_instances` | `int` | `10` | EC2 safety limit |
| `vpc_cidr` | `str` | `10.0.0.0/16` | VPC CIDR block |
| `backup_retention_days` | `int` | `7` | RDS backup retention |
| `multi_az` | `bool` | `False` | Multi-AZ deployments |

## Configuration

```python
from agents.aws_specialist.agent import AWSSpecialistAgent, Config

# Custom configuration
config = Config(
    region="eu-west-1",
    environment="staging",
    default_instance_type="t3.small",
    max_instances=20,
    tags={
        "Environment": "staging",
        "Team": "platform",
        "CostCenter": "engineering",
        "ManagedBy": "aws-specialist-agent"
    }
)

agent = AWSSpecialistAgent(config=config)
```

## Examples

### Production Web Application Stack

```python
# 1. Create VPC
vpc = agent.create_vpc("10.0.0.0/16", "prod-vpc")

# 2. Create subnets
public_a = agent.add_subnet(vpc.id, "10.0.1.0/24", "us-east-1a", public=True)
public_b = agent.add_subnet(vpc.id, "10.0.2.0/24", "us-east-1b", public=True)
private_a = agent.add_subnet(vpc.id, "10.0.3.0/24", "us-east-1a", public=False)
private_b = agent.add_subnet(vpc.id, "10.0.4.0/24", "us-east-1b", public=False)

# 3. Security groups
web_sg = agent.create_security_group(vpc.id, "web-sg", "Web tier",
    ingress_rules=[SecurityGroupRule("tcp", 443, 443, "0.0.0.0/0")])
app_sg = agent.create_security_group(vpc.id, "app-sg", "App tier",
    ingress_rules=[SecurityGroupRule("tcp", 8080, 8080, "10.0.0.0/16")])
db_sg = agent.create_security_group(vpc.id, "db-sg", "Database tier",
    ingress_rules=[SecurityGroupRule("tcp", 5432, 5432, "10.0.0.0/16")])

# 4. Load balancer
alb = agent.create_load_balancer(
    name="prod-alb",
    scheme="internet-facing",
    vpc_id=vpc.id,
    subnet_ids=[public_a.id, public_b.id],
    security_group_ids=[web_sg.id]
)

# 5. Auto scaling group
asg = agent.setup_auto_scaling(
    name="prod-asg",
    min_size=2,
    max_size=10,
    desired_capacity=3,
    vpc_zone_identifiers=[private_a.id, private_b.id]
)

# 6. Database
db = agent.create_rds_instance(
    db_instance_identifier="prod-db",
    engine="postgres",
    db_instance_class="db.r6g.large",
    multi_az=True,
    allocated_storage_gb=100
)
```

## Best Practices

1. **Tag Everything** - Consistent tagging for cost allocation and management
2. **Least Privilege** - IAM roles with minimal required permissions
3. **Encryption Everywhere** - KMS for data at rest, TLS for data in transit
4. **Multi-AZ for Production** - High availability for critical workloads
5. **Automated Backups** - Enable and test backup restoration
6. **Monitoring & Alerting** - CloudWatch alarms for key metrics
7. **Cost Optimization** - Regular right-sizing and reserved instances
8. **Security Reviews** - Periodic IAM and security group audits

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Provisioning timeout | Instance type unavailable in AZ | Select different AZ or instance family |
| ThrottlingException | API rate limit exceeded | Implement exponential backoff and retry |
| AccessDenied | IAM policy missing | Add required actions to role policy |
| LimitExceeded | Service quota reached | Request quota increase in AWS Console |
| Drift detected | Resource modified externally | Reconcile via CloudFormation or recreate |
| VPC Peering failed | Overlapping CIDR blocks | Use non-overlapping CIDR ranges |
| RDS connection refused | Security group misconfigured | Allow inbound on port from app SG |
| S3 access denied | Bucket policy or IAM issue | Check bucket policy and role permissions |

## Security & Compliance

- **Encryption**: AES256 or KMS for all storage; TLS 1.2+ for all transit
- **IAM**: No hardcoded credentials; roles with least-privilege policies; MFA enforced
- **Audit Logging**: CloudTrail for management events; CloudWatch for agent operations
- **Network Isolation**: Private subnets for databases; security groups with deny lists
- **Secrets**: Never logged or cached; use IAM roles or Secrets Manager
- **Compliance**: Well-Architected Framework pillars enforced

## Architecture Details

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for deep dives on compute, storage, networking, database, security, observability, and disaster recovery patterns.

## Agent Instructions

See [`GROK.md`](GROK.md) for system prompt, method specifications, usage patterns, and operational guidelines.

## Files

```
agents/aws-specialist/
  agent.py           # Main implementation (~1500+ lines)
  ARCHITECTURE.md    # System design and component reference
  GROK.md            # Agent prompt and API specifications
  README.md          # Usage guide and quick reference
```

## Contributing

Contributions are welcome! Please see our contributing guidelines in the main repository.

## License

Internal use: Awesome-Grok-Skills project.

---

*AWS Specialist Agent — Part of the Awesome Grok Skills collection.*
