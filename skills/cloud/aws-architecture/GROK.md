---
name: "aws-architecture"
category: "cloud"
version: "2.0.0"
tags: ["cloud", "AWS", "architecture", "Well-Architected", "infrastructure"]
---

# AWS Architecture

## Overview

The AWS Architecture module provides comprehensive guidance for designing, deploying, and managing cloud architectures on Amazon Web Services following the Well-Architected Framework. It covers compute, storage, networking, database, and application services with architecture patterns for high availability, cost optimization, security, and operational excellence.

This skill is essential for cloud architects, DevOps engineers, and solutions architects building production workloads on AWS.

## Core Capabilities

- **Well-Architected Review**: Assessment across 6 pillars — operational excellence, security, reliability, performance efficiency, cost optimization, sustainability
- **Compute Patterns**: EC2, Lambda, ECS/EKS, Fargate selection criteria and deployment architectures
- **Storage Patterns**: S3, EBS, EFS, and storage class optimization for different access patterns
- **Networking**: VPC design, Transit Gateway, Direct Connect, and hybrid connectivity patterns
- **Database**: RDS, DynamoDB, Aurora, ElastiCache, and database selection frameworks
- **High Availability**: Multi-AZ, multi-region, disaster recovery strategies (backup/restore, pilot light, warm standby, multi-site)
- **Security**: IAM, KMS, Secrets Manager, GuardDuty, Security Hub, and zero-trust patterns
- **Cost Optimization**: Reserved Instances, Savings Plans, Spot Instances, right-sizing, and cost monitoring

## Usage Examples

```python
from aws_architecture import (
    WellArchitectedReview,
    ComputeSelector,
    NetworkDesigner,
    DRStrategist,
    CostOptimizer,
)

# --- Well-Architected Review ---
review = WellArchitectedReview(workload="payment-api")
review.add_finding(
    pillar="security",
    finding="No encryption at rest for DynamoDB tables",
    risk="high",
    recommendation="Enable AWS-managed encryption",
)
review.add_finding(
    pillar="cost",
    finding="Over-provisioned EC2 instances",
    risk="medium",
    recommendation="Right-size to t3.large",
)
print(f"Risk score: {review.risk_score:.1f}")
print(f"Findings: {review.total_findings}")

# --- Compute Selection ---
selector = ComputeSelector()
recommendation = selector.recommend(
    workload_type="api",
    peak_rps=1000,
    avg_rps=100,
    memory_mb=512,
    cold_start_tolerance_ms=100,
)
print(f"Recommended: {recommendation.service}")
print(f"Instance type: {recommendation.instance_type}")
print(f"Est monthly cost: ${recommendation.estimated_cost:.0f}")

# --- VPC Design ---
designer = NetworkDesigner()
vpc = designer.design_vpc(
    name="production",
    cidr="10.0.0.0/16",
    availability_zones=3,
    public_subnets=True,
    private_subnets=True,
    nat_gateways=3,
    vpc_endpoints=["s3", "dynamodb", "secretsmanager"],
)
print(f"VPC: {vpc.cidr}")
print(f"Subnets: {vpc.total_subnets}")
print(f"NAT Gateways: {vpc.nat_gateways}")

# --- Disaster Recovery ---
dr = DRStrategist()
strategy = dr.recommend(
    rpo_hours=1,
    rto_hours=4,
    budget="medium",
    data_size_tb=1,
)
print(f"Strategy: {strategy.strategy}")
print(f"RPO: {strategy.rpo_hours}h  RTO: {strategy.rto_hours}h")
print(f"Est cost: ${strategy.monthly_cost:.0f}/month")

# --- Cost Optimization ---
optimizer = CostOptimizer()
report = optimizer.analyze(
    monthly_spend=15000,
    ec2_hours=5000,
    s3_tb=10,
    data_transfer_gb=500,
)
print(f"Potential savings: ${report.potential_savings:.0f}/month")
for rec in report.recommendations:
    print(f"  - {rec}")
```

## Best Practices

- Design for failure — every component should be treated as replaceable
- Use Auto Scaling for all stateless workloads to handle traffic variability
- Implement multi-AZ by default; use multi-region only for DR or global latency
- Apply defense-in-depth: WAF, Shield, Security Groups, NACLs, IAM policies
- Use S3 Intelligent-Tiering for unpredictable access patterns
- Enable CloudTrail in all regions and guardrails via AWS Organizations SCPs
- Tag all resources for cost allocation: environment, team, project, cost-center
- Use SSM Parameter Store or Secrets Manager — never hardcode secrets
- Implement health checks at every layer with proper thresholds
- Review AWS Well-Architected Framework bi-annually for every production workload

## Related Modules

- **azure-services**: Azure cloud architecture patterns
- **gcp-platform**: GCP cloud architecture patterns
- **multi-cloud**: Cross-cloud architecture strategies
- **serverless**: Serverless-first architecture patterns

## Advanced Configuration

### AWS CLI Configuration

```bash
# Configure AWS CLI
aws configure
# Access Key ID: ${AWS_ACCESS_KEY_ID}
# Secret Access Key: ${AWS_SECRET_ACCESS_KEY}
# Region: us-east-1
# Output format: json

# Configure profiles
aws configure --profile production
aws configure --profile staging
```

### Terraform Provider Configuration

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
```

### Well-Architected Configuration

```yaml
well_architected:
  pillars:
    - name: "operational_excellence"
      weight: 0.15
    - name: "security"
      weight: 0.25
    - name: "reliability"
      weight: 0.25
    - name: "performance_efficiency"
      weight: 0.15
    - name: "cost_optimization"
      weight: 0.15
    - name: "sustainability"
      weight: 0.05
  review_frequency: "quarterly"
  automated_assessment: true
```

## Architecture Patterns

### High Availability Architecture

```
Multi-AZ Deployment:
├── Application Tier
│   ├── ALB (Application Load Balancer)
│   ├── Auto Scaling Group
│   ├── EC2 instances (2+ AZs)
│   └── Target Groups
├── Database Tier
│   ├── RDS Multi-AZ
│   ├── Read Replicas
│   └── ElastiCache
├── Storage Tier
│   ├── S3 (Cross-Region Replication)
│   └── EBS (Multi-Attach)
└── DNS
    ├── Route 53 (health checks)
    └── Latency-based routing
```

### Disaster Recovery Strategies

| Strategy | RPO | RTO | Cost | Complexity |
|----------|-----|-----|------|------------|
| Backup & Restore | Hours | Hours | Low | Low |
| Pilot Light | Minutes | 10s of min | Medium | Medium |
| Warm Standby | Seconds | Minutes | High | Medium |
| Multi-Site | Near zero | Near zero | Very High | High |

### Serverless Architecture

```
Event-Driven Architecture:
├── API Gateway → Lambda → DynamoDB
├── S3 Events → Lambda → SQS
├── DynamoDB Streams → Lambda → Elasticsearch
├── SNS → Lambda → Multiple targets
├── EventBridge → Step Functions → Multiple services
└── Kinesis → Lambda → S3/Redshift
```

### Data Lake Architecture

```
Data Lake Layers:
├── Raw Zone (S3)
│   ├── Original format
│   └── Immutable
├── Cleansed Zone (S3)
│   ├── Validated
│   └── Schema applied
├── Processed Zone (S3)
│   ├── Transformed
│   └── Enriched
├── Consumption Zone (S3)
│   ├── Analytics-ready
│   └── ML-ready
└── Governance
    ├── AWS Glue Catalog
    ├── Lake Formation
    └── Data Lineage
```

## Integration Guide

### AWS CDK Integration

```typescript
// lib/stack.ts
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';

export class MyStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'Vpc', {
      maxAzs: 3,
      natGateways: 1,
    });

    const database = new rds.DatabaseInstance(this, 'Database', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_15_3,
      }),
      vpc,
      multiAz: true,
      backupRetention: cdk.Duration.days(7),
    });
  }
}
```

### AWS SDK Integration

```python
import boto3

# EC2 client
ec2 = boto3.client('ec2')
instances = ec2.describe_instances()

# S3 client
s3 = boto3.client('s3')
s3.upload_file('local_file.txt', 'bucket-name', 'remote_key.txt')

# Lambda client
lambda_client = boto3.client('lambda')
response = lambda_client.invoke(
    FunctionName='my-function',
    Payload=b'{"key": "value"}',
)
```

### CloudFormation Integration

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'My Application Stack'

Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-unique-bucket-name
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: TransitionToIA
            Status: Enabled
            Transitions:
              - StorageClass: STANDARD_IA
                TransitionInDays: 90
```

## Performance Optimization

### Compute Optimization

| Instance Type | Use Case | vCPU | Memory | Network |
|---------------|----------|------|--------|---------|
| t3.medium | Burstable workloads | 2 | 4 GB | Up to 5 Gbps |
| m5.large | General purpose | 2 | 8 GB | Up to 10 Gbps |
| c5.xlarge | Compute intensive | 4 | 8 GB | Up to 10 Gbps |
| r5.large | Memory intensive | 2 | 16 GB | Up to 10 Gbps |
| p3.2xlarge | ML training | 8 | 61 GB | 10 Gbps |

### Storage Optimization

```
S3 Storage Classes:
├── S3 Standard — Frequent access
├── S3 Intelligent-Tiering — Unknown patterns
├── S3 Standard-IA — Infrequent access (30d min)
├── S3 One Zone-IA — Non-critical, re-creatable
├── S3 Glacier Instant Retrieval — Archive (ms access)
├── S3 Glacier Flexible Retrieval — Archive (min-hours)
└── S3 Glacier Deep Archive — Long-term archive (12h)

EBS Volume Types:
├── gp3 — General SSD (3000 IOPS baseline)
├── io2 — High-performance SSD (64K IOPS)
├── st1 — Throughput-optimized HDD
└── sc1 — Cold HDD (infrequent access)
```

### Network Optimization

```
Performance Techniques:
├── CloudFront caching (edge locations)
├── Global Accelerator (anycast IP)
├── VPC endpoints (S3, DynamoDB)
├── Direct Connect (dedicated bandwidth)
└── Enhanced networking (ENA)
```

## Security Considerations

### Security Best Practices

| Practice | Implementation | Priority |
|----------|---------------|----------|
| MFA | IAM policies with MFA | Critical |
| Encryption | KMS for at-rest, TLS for transit | Critical |
| Least Privilege | IAM roles with minimal permissions | Critical |
| VPC Security | Security groups, NACLs | High |
| Logging | CloudTrail, VPC Flow Logs | High |
| Monitoring | GuardDuty, Security Hub | High |

### IAM Policy Examples

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-bucket"
    }
  ]
}
```

### VPC Security

```
Security Layers:
├── Security Groups (stateful, instance-level)
├── NACLs (stateless, subnet-level)
├── VPC Endpoints (private connectivity)
├── Flow Logs (traffic monitoring)
├── Network Firewall (traffic inspection)
└── WAF (application layer protection)
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Access Denied | IAM policy error | Check permissions, resource ARNs |
| Throttling | Request limit exceeded | Request increase, implement backoff |
| Connection Timeout | Cannot reach endpoint | Check VPC, security groups, routes |
| Performance | Slow response times | Check instance type, caching, CDN |
| Cost Overrun | High bill | Check usage, right-size, set budgets |

### Debugging Commands

```bash
# Check IAM permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789:role/my-role \
  --action-names s3:GetObject

# Check VPC connectivity
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-123
aws ec2 describe-security-groups --filters Name=vpc-id,Values=vpc-123

# Check CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average \
  --dimensions Name=InstanceId,Values=i-1234567890abcdef0
```

## API Reference

### EC2

```python
import boto3

ec2 = boto3.resource('ec2')

# Create instance
instance = ec2.create_instances(
    ImageId='ami-0c55b159cbfafe1f0',
    InstanceType='t3.micro',
    MinCount=1,
    MaxCount=1,
    KeyName='my-key-pair',
    SecurityGroupIds=['sg-12345678'],
    SubnetId='subnet-12345678',
)

# Describe instances
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
)
```

### S3

```python
s3 = boto3.resource('s3')

# Create bucket
bucket = s3.create_bucket(
    Bucket='my-unique-bucket',
    CreateBucketConfiguration={'LocationConstraint': 'us-west-2'},
)

# Upload object
bucket.Object('key.txt').upload_file('local.txt')

# List objects
for obj in bucket.objects.all():
    print(obj.key, obj.last_modified)
```

### Lambda

```python
lambda_client = boto3.client('lambda')

# Create function
function = lambda_client.create_function(
    FunctionName='my-function',
    Runtime='python3.11',
    Role='arn:aws:iam::123456789:role/lambda-role',
    Handler='index.handler',
    Code={'ZipFile': b'file_bytes'},
)

# Invoke function
response = lambda_client.invoke(
    FunctionName='my-function',
    InvocationType='RequestResponse',
    Payload=b'{"key": "value"}',
)
```

## Data Models

### EC2 Instance

```
EC2Instance:
  instance_id: str
  instance_type: str
  state: str
  private_ip: str
  public_ip: str
  vpc_id: str
  subnet_id: str
  security_groups: list[str]
  tags: dict
  launch_time: datetime
```

### S3 Bucket

```
S3Bucket:
  name: str
  region: str
  creation_date: datetime
  versioning: bool
  encryption: str
  lifecycle_rules: list[dict]
  policy: dict
  tags: dict
```

### Lambda Function

```
LambdaFunction:
  function_name: str
  runtime: str
  handler: str
  role: str
  memory_size: int
  timeout: int
  vpc_config: dict
  environment: dict
  last_modified: datetime
  code_size: int
```

## Deployment Guide

### Infrastructure Deployment

```
1. Prerequisites
   ├── AWS account with admin access
   ├── AWS CLI configured
   ├── Terraform/CDK installed
   └── State backend configured

2. Deployment Steps
   ├── Initialize Terraform/CDK
   ├── Plan infrastructure changes
   ├── Apply infrastructure
   ├── Verify deployment
   └── Update documentation

3. Post-Deployment
   ├── Configure monitoring
   ├── Set up alerts
   ├── Enable backup
   └── Document procedures
```

### CI/CD Pipeline

```yaml
# buildspec.yml
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.11
  pre_build:
    commands:
      - pip install -r requirements.txt
      - python -m pytest tests/
  build:
    commands:
      - aws cloudformation package template.yaml --s3-bucket my-bucket
  post_build:
    commands:
      - aws cloudformation deploy --template-file packaged.yaml --stack-name my-stack
```

## Monitoring & Observability

### Key Metrics

| Metric | Service | Target |
|--------|---------|--------|
| CPU Utilization | EC2 | <70% average |
| Memory Usage | EC2 | <80% average |
| 5XX Error Rate | ALB | <0.1% |
| Latency P99 | ALB | <500ms |
| DynamoDB Read Capacity | DynamoDB | <80% provisioned |
| S3 Request Rate | S3 | Within limits |

### CloudWatch Dashboards

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Put metric data
cloudwatch.put_metric_data(
    Namespace='MyApp',
    MetricData=[
        {
            'MetricName': 'RequestCount',
            'Dimensions': [
                {'Name': 'Environment', 'Value': 'production'},
            ],
            'Value': 100,
            'Unit': 'Count',
        },
    ],
)
```

## Testing Strategy

### Testing Approach

```
1. Unit Tests
   ├── Lambda function logic
   ├── Data transformation
   └── API integration

2. Integration Tests
   ├── End-to-end workflows
   ├── Service interactions
   └── Error handling

3. Performance Tests
   ├── Load testing (Locust)
   ├── Stress testing
   └── Endurance testing

4. Security Tests
   ├── Penetration testing
   ├── IAM policy review
   └── Vulnerability scanning
```

## Versioning & Migration

### Infrastructure Versioning

```
Major: New architecture pattern
├── Example: Migrate from EC2 to Lambda
├── Requires: Full testing, rollback plan
└── Risk: High

Minor: Service additions
├── Example: Add ElastiCache cluster
├── Requires: Testing, documentation
└── Risk: Low

Patch: Configuration changes
├── Example: Update instance type
├── Requires: Basic testing
└── Risk: Very low
```

## Glossary

| Term | Definition |
|------|-----------|
| ALB | Application Load Balancer |
| Auto Scaling | Automatic capacity adjustment |
| CloudFormation | Infrastructure as Code service |
| EC2 | Elastic Compute Cloud |
| EBS | Elastic Block Store |
| ELB | Elastic Load Balancing |
| IAM | Identity and Access Management |
| KMS | Key Management Service |
| Lambda | Function-as-a-Service |
| RDS | Relational Database Service |
| S3 | Simple Storage Service |
| VPC | Virtual Private Cloud |

## Changelog

### 2.0.0 (2024-12-01)
- Added Well-Architected review automation
- Added CDK patterns
- Improved cost optimization
- Added sustainability pillar

### 1.2.0 (2024-08-15)
- Added multi-AZ patterns
- Added disaster recovery strategies
- Improved security hardening

### 1.1.0 (2024-05-20)
- Added serverless patterns
- Added data lake architecture
- Improved networking

### 1.0.0 (2024-02-01)
- Initial release with basic compute patterns
- Simple storage guidance
- Basic networking

## Contributing Guidelines

### Adding New Patterns

1. Document the pattern
2. Include architecture diagram
3. Provide working code examples
4. Add cost estimates
5. Submit PR with review

### Code Quality

- All examples must be runnable
- Include IAM permissions
- Document costs
- Test in multiple regions

## License

MIT License

Copyright (c) 2024 AWS Architecture Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
