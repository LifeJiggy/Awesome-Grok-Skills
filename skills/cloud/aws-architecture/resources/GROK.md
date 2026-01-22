# AWS Architecture Agent

## Overview

The **AWS Architecture Agent** provides comprehensive capabilities for designing, deploying, and managing Amazon Web Services infrastructure. This agent helps architects and developers build scalable, reliable, and cost-effective cloud solutions following AWS best practices and the Well-Architected Framework.

## Core Capabilities

### 1. Compute Services
Provision and manage compute resources:
- **EC2 Instances**: Virtual machines with various sizes
- **Lambda Functions**: Serverless compute
- **ECS/EKS**: Container orchestration
- **Lightsail**: Simplified virtual servers
- **Batch**: Batch computing workloads

### 2. Database Services
Manage relational and NoSQL databases:
- **RDS**: Managed relational databases
- **DynamoDB**: Managed NoSQL database
- **ElastiCache**: In-memory caching
- **Redshift**: Data warehousing
- **DocumentDB**: MongoDB-compatible

### 3. Storage Services
Handle data storage requirements:
- **S3**: Object storage with various tiers
- **EBS**: Block storage for EC2
- **EFS**: Managed file storage
- **FSx**: File systems for specific workloads
- **Glacier**: Archive storage

### 4. Networking
Configure secure and scalable networks:
- **VPC**: Virtual private cloud
- **Subnets**: Public and private network segments
- **Route 53**: DNS service
- **CloudFront**: Content delivery network
- **Load Balancers**: Application and network LB

### 5. Serverless
Build event-driven architectures:
- **Lambda**: Serverless functions
- **API Gateway**: API management
- **Step Functions**: Workflow orchestration
- **EventBridge**: Event bus
- **SQS/SNS**: Message queuing and pub/sub

## Usage Examples

### EC2 Instance Management

```python
from aws_architecture import AWSServicesManager

aws = AWSServicesManager()
instance = aws.create_ec2_instance(
    instance_type="t3.micro",
    ami_id="ami-0c02fb55956c7d316",
    key_name="my-key-pair",
    security_groups=["sg-0123abcd"]
)
print(f"Instance ID: {instance.instance_id}")
print(f"Public IP: {instance.public_ip}")
print(f"Status: {instance.state}")
```

### VPC Creation

```python
vpc = aws.create_vpc(
    cidr_block="10.0.0.0/16",
    availability_zones=["us-east-1a", "us-east-1b", "us-east-1c"]
)
print(f"VPC ID: {vpc.vpc_id}")
for subnet in vpc.subnets:
    print(f"Subnet: {subnet['subnet_id']} - {subnet['cidr']}")
```

### RDS Database

```python
rds = aws.create_rds_instance(
    engine="postgres",
    instance_class="db.t3.medium",
    Multi_AZ=True
)
print(f"Database: {rds.db_identifier}")
print(f"Endpoint: {rds.endpoint}")
print(f"Status: {rds.status}")
```

### S3 Bucket

```python
bucket = aws.create_s3_bucket(
    bucket_name="my-data-bucket",
    region="us-east-1"
)
print(f"Bucket: {bucket['bucket_name']}")
print(f"Encryption: {bucket['encryption']}")
print(f"Versioning: {bucket['versioning']}")
```

### Lambda Function

```python
lambda_func = aws.create_lambda_function(
    function_name="my-function",
    runtime="python3.9",
    memory_size=256,
    timeout=30
)
print(f"Function: {lambda_func['function_name']}")
print(f"Memory: {lambda_func['memory_size']}MB")
```

### Load Balancer

```python
lb = aws.create_load_balancer(
    name="my-alb",
    scheme="internet-facing",
    listener_ports=[80, 443]
)
print(f"DNS: {lb['dns_name']}")
print(f"Type: {lb['type']}")
```

### Auto Scaling

```python
asg = aws.create_autoscaling_group(
    name="my-asg",
    min_size=2,
    max_size=10,
    desired_capacity=4
)
print(f"ASG: {asg['auto_scaling_group_name']}")
print(f"Desired: {asg['desired_capacity']}")
```

### Cost Optimization

```python
from aws_architecture import AWSCostOptimizer

cost = AWSCostOptimizer()
analysis = cost.analyze_cost_by_service({})
print(f"Total Monthly Cost: ${analysis['total_cost']}")
for service, cost_amt in analysis['by_service'].items():
    print(f"  {service}: ${cost_amt}")

ri_rec = cost.get_reserved_instance_recommendation("EC2", 0.75)
print(f"RI Savings: ${ri_rec['monthly_savings']}/month")
```

### Well-Architected Review

```python
from aws_architecture import AWSWellArchitected

review = AWSWellArchitected().review_architecture({})
print(f"Overall Score: {review['overall_score']}%")
for pillar, data in review['pillars'].items():
    print(f"  {pillar}: {data['score']}%")
```

## AWS Well-Architected Framework

### Six Pillars

| Pillar | Focus | Key Questions |
|--------|-------|---------------|
| **Operational Excellence** | Running and monitoring systems | How do you understand system health? |
| **Security** | Protecting data and systems | How do you protect your workload? |
| **Reliability** | Recovering from failures | How does your system recover? |
| **Performance** | Using computing resources efficiently | How do you choose resources? |
| **Cost Optimization** | Getting lowest price | How do you optimize costs? |
| **Sustainability** | Minimizing environmental impact | How do you reduce footprint? |

### Design Principles

1. **Stop guessing capacity needs**
2. **Test systems at production scale**
3. **Automate to make experimentation easier**
4. **Allow for evolutionary architectures**
5. **Drive architectures using data**
6. **Improve through game days**

## Common Architectures

### Web Application

```
Internet → CloudFront → ALB → Auto Scaling Group → EC2
                                     ↓
                              RDS (Multi-AZ)
                                     ↓
                              ElastiCache
```

### Serverless API

```
API Gateway → Lambda → DynamoDB
      ↓                    ↓
EventBridge           S3 (data store)
```

### Microservices

```
Client → API Gateway → Service A → SQS → Service B
                                  ↓
                              RDS
```

## Cost Optimization Strategies

### EC2 Cost Optimization

| Strategy | Savings Potential | Effort |
|----------|------------------|--------|
| Reserved Instances | Up to 72% | Low |
| Spot Instances | Up to 90% | Medium |
| Right-sizing | 20-40% | Low |
| Auto Scaling | 15-30% | Low |

### S3 Cost Optimization

| Storage Class | Use Case | Savings vs Standard |
|---------------|----------|---------------------|
| Intelligent-Tiering | Unknown access patterns | Up to 40% |
| Standard-IA | Infrequent access | 40% |
| Glacier | Archival | 70% |
| Glacier Deep Archive | Long-term archival | 95% |

## Security Best Practices

### Identity and Access Management

1. **Use IAM roles for services** instead of access keys
2. **Apply least privilege** to all policies
3. **Enable MFA** for all users
4. **Use service control policies** for organization boundaries
5. **Regularly audit** permissions

### Network Security

1. **Use VPCs** with proper subnet design
2. **Implement security groups** as firewall
3. **Use NACLs** for subnet-level control
4. **Enable VPC flow logs** for monitoring
5. **Use private endpoints** for AWS services

### Data Protection

1. **Encrypt data at rest** using KMS
2. **Encrypt data in transit** using TLS
3. **Use key rotation** for encryption keys
4. **Implement backup and recovery** strategies
5. **Classify data** and apply controls

## AWS Services by Use Case

### Compute

| Need | Recommended Service |
|------|---------------------|
| Virtual servers | EC2 |
| Containers | ECS or EKS |
| Serverless | Lambda |
| Batch jobs | Batch |

### Database

| Need | Recommended Service |
|------|---------------------|
| Relational | RDS (PostgreSQL, MySQL, etc.) |
| NoSQL (key-value) | DynamoDB |
| NoSQL (document) | DocumentDB |
| Caching | ElastiCache |
| Data Warehouse | Redshift |

### Storage

| Need | Recommended Service |
|------|---------------------|
| Object storage | S3 |
| Block storage | EBS |
| File storage | EFS |
| Archive | S3 Glacier |

## Tools and Resources

### Infrastructure as Code

| Tool | Description | Use Case |
|------|-------------|----------|
| CloudFormation | Native IaC | AWS resources |
| AWS CDK | Programmatic IaC | TypeScript, Python, etc. |
| Terraform | Multi-cloud IaC | Hybrid cloud |
| Pulumi | Modern IaC | Any language |

### Development Tools

| Tool | Purpose |
|------|---------|
| AWS CLI | Command-line access |
| AWS SDKs | Language-specific APIs |
| SAM | Serverless applications |
| Amplify | Frontend development |

## Related Skills

- [Azure Services](./../azure-services/resources/GROK.md) - Microsoft cloud
- [GCP Services](./../gcp-services/resources/GROK.md) - Google cloud
- [CI/CD Pipelines](./../../devops/ci-cd-pipelines/resources/GROK.md) - Deployment automation
- [Infrastructure Automation](./../../devops/infrastructure-automation/resources/GROK.md) - IaC practices

---

**File Path**: `skills/cloud/aws-architecture/resources/aws_architecture.py`
