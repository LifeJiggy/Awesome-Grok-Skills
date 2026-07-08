# AWS Specialist Agent

Senior cloud engineer and automation agent for designing, provisioning, securing, and operating AWS infrastructure with production-grade rigor.

## What It Does

The AWS Specialist Agent manages the full AWS infrastructure lifecycle through validated, typed, and observable methods. It enforces Well-Architected Framework principles across compute, storage, networking, databases, security, and governance.

### Capabilities at a Glance

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

## Installation & Requirements

- Python 3.9+
- boto3 (for production AWS access; agent works in offline/mock mode by default)
- Standard library only for demo: `dataclasses`, `enum`, `typing`, `json`, `logging`, `uuid`, `datetime`

```bash
# Install AWS SDK (optional, for real AWS access)
pip install boto3
```

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

## Running the Demo

```bash
python agents/aws-specialist/agent.py
```

The demo exercises VPC creation, EC2 provisioning, S3/Lambda, load balancing, auto scaling, RDS, DynamoDB, EKS/KMS, CloudWatch, Route53, SNS/SQS, IAM policies, cost estimation, validation, and state export.

## Core API Reference

### Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `region` | `str` | `us-east-1` | AWS region |
| `default_instance_type` | `str` | `t3.micro` | Default EC2 instance type |
| `auto_scaling` | `bool` | `True` | Enable auto scaling by default |
| `enable_monitoring` | `bool` | `True` | CloudWatch detailed monitoring |
| `enable_logging` | `bool` | `True` | Structured logging |
| `max_instances` | `int` | `10` | Safety limit for EC2 |
| `vpc_cidr` | `str` | `10.0.0.0/16` | VPC CIDR block |
| `environment` | `str` | `development` | Environment label |
| `backup_retention_days` | `int` | `7` | RDS backup retention |
| `multi_az` | `bool` | `False` | Multi-AZ deployments |

### Compute

```python
# EC2
agent.provision_ec2(...)
agent.get_instance(instance_id)
agent.list_instances(state_filter="running")
agent.terminate_instance(instance_id, force=False)
agent.start_instance(instance_id)
agent.stop_instance(instance_id)

# Lambda
agent.deploy_lambda(
    function_name, runtime, handler, memory_mb, timeout_seconds,
    role_arn, code_s3_bucket=None, code_s3_key=None,
    environment_variables=None, layers=None, description="", publish=True
)

# Containers
agent.setup_container_service(
    service_name, cpu="256", memory="512", desired_count=1,
    launch_type="FARGATE", environment_variables=None, secrets=None
)

# EKS
agent.create_eks_cluster(cluster_name, kubernetes_version="1.24", endpoint_public_access=True)
```

### Storage

```python
agent.configure_s3_bucket(
    bucket_name, versioning=False, encryption="AES256",
    lifecycle_rules=None, cors=None, tags=None
)
agent.upload_object_to_s3(bucket_name, key, data, content_type="application/octet-stream")

# KMS
agent.create_kms_key(description="", key_usage="ENCRYPT_DECRYPT", origin="AWS_KMS")
```

### Database

```python
agent.create_rds_instance(
    db_instance_identifier, engine, db_instance_class, master_username,
    master_password, allocated_storage_gb, storage_type="gp3",
    multi_az=False, publicly_accessible=False, db_subnet_group_name="default"
)
agent.create_dynamodb_table(
    table_name, partition_key, partition_key_type="S",
    sort_key=None, billing_mode="PAY_PER_REQUEST"
)
agent.create_db_subnet_group(name, subnet_ids, description="")
```

### Networking

```python
agent.create_vpc(cidr_block, name, tags=None)
agent.add_subnet(vpc_id, cidr_block, availability_zone, public=True, map_public_ip=True)
agent.create_security_group(vpc_id, name, description, ingress_rules=None, egress_rules=None)
agent.authorize_security_group_ingress(security_group_id, ip_protocol, from_port, to_port, cidr_ip, description="")
agent.attach_internet_gateway(vpc_id, gateway_id)
agent.configure_vpc_peering(requester_vpc_id, accepter_vpc_id, tags=None)
agent.setup_route53(zone_name, private=False, vpc_id=None)
agent.create_cloudfront_distribution(origin_domain, origin_path="", enabled=True)
```

### Load Balancing & Scaling

```python
agent.create_load_balancer(
    name, scheme="internet-facing", lb_type="application",
    vpc_id="", subnet_ids=None, security_group_ids=None, listeners=None
)
agent.setup_auto_scaling(
    name, launch_configuration, min_size, max_size, desired_capacity,
    vpc_zone_identifiers=None, target_group_arns=None, health_check_type="EC2"
)
agent.scale_auto_scaling_group(name, new_capacity)
```

### Security & IAM

```python
agent.create_iam_role(role_name, assume_role_policy, policies=None, max_session_duration=3600)
agent.generate_iam_policy(actions, resources, effect="Allow", sid="")
agent.create_cloudwatch_alarm(
    alarm_name, metric_name, namespace, statistic, period,
    evaluation_periods, threshold, comparison_operator
)
agent.add_permissions_boundary(role_arn, permissions_boundary_arn)
```

### IaC & Deployment

```python
agent.deploy_cloudformation_stack(stack_name, template_body, parameters=None)
agent.deploy_infrastructure_as_code(
    infrastructure_code, format_type="terraform", variables=None
)
```

### Messaging & Events

```python
agent.publish_sns_topic(topic_name, display_name="", fifo=False)
agent.create_sns_subscription(topic_arn, protocol, endpoint)
agent.send_sqs_message(queue_url, message_body, delay_seconds=0)
agent.create_cloudwatch_metric_stream(name, output_format="JSON", include_filters=None)
```

### Reporting & Operations

```python
agent.get_status()
agent.get_infrastructure_summary()
agent.get_metrics_report()
agent.validate_configuration()
agent.optimize_cost()
agent.export_state()
agent.import_state(state_json)
```

## Security & Compliance

- **Encryption**: AES256 or KMS for all storage; TLS 1.2+ for all transit.
- **IAM**: No hardcoded credentials; roles with least-privilege policies; MFA enforced.
- **Audit Logging**: CloudTrail for management events; CloudWatch for agent operations.
- **Network Isolation**: Private subnets for databases; security groups with deny lists where required.
- **Secrets**: Never logged or cached; use IAM roles or Secrets Manager.

## Cost Management

- **Estimates**: Hourly and monthly breakdowns by service with currency and region context.
- **Optimization**: Rightsizing, idle-load-balancer removal, and storage-tier transitions.
- **Budgets**: Set alerts at 50%/80%/100% of monthly budget.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Provisioning timeout | Instance type unavailable in AZ | Select different AZ or instance family |
| ThrottlingException | API rate limit exceeded | Implement exponential backoff and retry |
| AccessDenied | IAM policy missing | Add required actions to role policy |
| LimitExceeded | Service quota reached | Request quota increase in AWS Console |
| Drift detected | Resource modified externally | Reconcile via CloudFormation or recreate |

## Operational Runbook

1. **Pre-deployment**: Validate configuration, confirm IaC template, request approvals via change management.
2. **Deployment**: Use blue/green or rolling deployments; monitor CloudWatch alarms during rollout.
3. **Post-deployment**: Run validation suite, verify health endpoints, enable detailed monitoring.
4. **Ongoing**: Weekly cost review, monthly rightsizing, quarterly security audit.

## Architecture Details

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for deep dives on compute, storage, networking, database, security, observability, and disaster recovery patterns.

## Agent Instructions

See [`GROK.md`](GROK.md) for system prompt, method specifications, usage patterns, and operational guidelines.

## File Structure

```
agents/aws-specialist/
  agent.py           # Main implementation (~1500+ lines)
  ARCHITECTURE.md    # System design and component reference
  GROK.md            # Agent prompt and API specifications
  README.md          # Usage guide and quick reference
```

## License

Internal use: Awesome-Grok-Skills project.
