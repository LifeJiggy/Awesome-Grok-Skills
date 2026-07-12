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
