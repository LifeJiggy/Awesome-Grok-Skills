# AWS Specialist Agent — System Architecture

## 1. Overview

The AWS Specialist Agent is a production-grade automation framework for managing, provisioning, configuring, and monitoring AWS cloud infrastructure. It encapsulates AWS Well-Architected Framework best practices, security hardening, cost optimization, and operational excellence into reusable, typed agent methods. The agent operates in offline/mock mode by default and connects to real AWS via boto3 when credentials are provided.

## 2. Design Principles

- **Infrastructure as Code (IaC)** — Every resource is defined declaratively and tracked in state.
- **Security by Default** — Encryption at rest and in transit, least-privilege IAM, and network isolation.
- **High Availability** — Multi-AZ deployments, auto-scaling, and health checks.
- **Observability** — Structured logging, metrics collection, and CloudWatch integration.
- **Cost Optimization** — Rightsizing recommendations, idle resource detection, and budget alerts.
- **Immutable Infrastructure** — Rebuild rather than patch; replace instances, don't SSH in.
- **Well-Architected Pillars** — Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization.

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         AWS Specialist Agent                                         │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────────────────────────┤
│  Compute    │  Storage    │  Network    │  Database   │  Security / Compliance      │
│  Manager    │  Manager    │  Manager    │  Manager    │  Manager                    │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────────────────────┤
│  EC2        │  S3         │  VPC        │  RDS        │  IAM Roles/Policies         │
│  Lambda     │  EBS        │  Subnets    │  DynamoDB   │  KMS Keys                   │
│  ECS/Fargate│  EFS        │  SG / NACL  │  Aurora     │  CloudTrail                 │
│  EKS        │  Glacier    │  ALB / NLB  │  ElastiCache│  GuardDuty                  │
│  Batch      │  FSx        │  Route 53   │  Neptune    │  Config Rules               │
│  Spot Fleet │  Storage GW │  CloudFront │  Redshift   │  Security Hub               │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────────────────────┘
         │           │           │           │                    │
         └───────────┴───────────┴───────────┴────────────────────┘
                     │
              ┌──────────────────┐
              │  Messaging &     │
              │  Event Engine    │
              ├──────────────────┤
              │  SQS / SNS       │
              │  EventBridge     │
              │  Kinesis         │
              │  Step Functions  │
              └──────────────────┘
                     │
              ┌──────────────────┐
              │  Observability   │
              ├──────────────────┤
              │  CloudWatch      │
              │  X-Ray           │
              │  CloudTrail      │
              │  Cost Explorer   │
              └──────────────────┘
                     │
              ┌──────────────────┐
              │  IaC Engine      │
              ├──────────────────┤
              │  CloudFormation  │
              │  Terraform       │
              │  CDK (Python)    │
              │  Pulumi          │
              └──────────────────┘
```

## 4. Component Deep Dive

### 4.1 Compute Manager

Manages EC2 instance lifecycles, Lambda serverless functions, container orchestration (ECS/EKS), and batch computing.

#### EC2 Provisioning Workflow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       EC2 Provisioning Pipeline                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐      │
│  │ Validate   │───▶│ Allocate   │───▶│ Attach     │───▶│ Bootstrap  │      │
│  │ Instance   │    │ EBS Volume │    │ SG + IAM   │    │ User-Data  │      │
│  │ Type       │    │ (IOPS/Thr) │    │ Profile    │    │            │      │
│  └────────────┘    └────────────┘    └────────────┘    └────────────┘      │
│       │                                   │                  │              │
│       ▼                                   ▼                  ▼              │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐      │
│  │ Check      │    │ Configure  │    │ Enable     │    │ Tag        │      │
│  │ Instance   │    │ Placement  │    │ Detailed   │    │ Resources  │      │
│  │ Limits     │    │ Group      │    │ Monitoring │    │            │      │
│  └────────────┘    └────────────┘    └────────────┘    └────────────┘      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**EC2 Instance Families:**

| Family    | Use Case              | Example Sizes       | vCPU Range | Memory Range |
|-----------|-----------------------|---------------------|-----------|--------------|
| t3/t3a    | General burstable     | t3.micro → t3.2xlarge | 2-8      | 1-32 GB      |
| m5/m6i    | General purpose       | m5.large → m6i.4xlarge | 2-16    | 8-64 GB      |
| c5/c6i    | Compute optimized     | c5.large → c6i.4xlarge | 2-16    | 4-32 GB      |
| r5/r6i    | Memory optimized      | r5.large → r6i.4xlarge | 2-16    | 16-128 GB    |
| i3/i4i    | Storage optimized     | i3.large → i4i.4xlarge | 2-16    | 16-128 GB    |
| p4d/p5    | GPU (ML training)     | p4d.24xlarge         | 96       | 1152 GB      |
| g5/g6     | GPU (inference)       | g5.xlarge            | 4-96     | 16-192 GB     |
| inf2      | ML inference (custom)  | inf2.xlarge          | 4-128    | 32-2048 GB    |
| m7g/r7g   | Graviton3 (ARM)       | m7g.large            | 2-48     | 8-384 GB      |

**EC2 Provisioning Code Pattern:**
```python
def provision_ec2(
    self,
    name: str,
    instance_type: str,
    ami_id: str,
    key_name: Optional[str] = None,
    security_group_ids: Optional[List[str]] = None,
    user_data: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    attach_volume: bool = True,
    volume_size_gb: int = 20
) -> EC2Instance:
    """
    Provision an EC2 instance with full lifecycle management.

    Steps:
    1. Validate instance type against allowed families
    2. Check account limits and availability
    3. Allocate EBS volume with specified IOPS/throughput
    4. Create IAM instance profile if needed
    5. Launch instance with placement, monitoring, metadata options
    6. Attach security groups and configure network interface
    7. Inject user-data for bootstrap configuration
    8. Apply tags for cost allocation and governance
    9. Register in agent state registry
    10. Return EC2Instance dataclass with full metadata
    """
```

#### Lambda Deployment Workflow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       Lambda Deployment Pipeline                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐      │
│  │ Validate   │───▶│ Package    │───▶│ Create /   │───▶│ Configure  │      │
│  │ Runtime &  │    │ Code &     │    │ Update     │    │ Concurrency│      │
│  │ Handler    │    │ Checksum   │    │ Function   │    │ + DLQ      │      │
│  └────────────┘    └────────────┘    └────────────┘    └────────────┘      │
│       │                                   │                  │              │
│       ▼                                   ▼                  ▼              │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐      │
│  │ Validate   │    │ Set Env    │    │ Configure  │    │ Publish    │      │
│  │ IAM Role   │    │ Variables  │    │ VPC Config │    │ Version    │      │
│  └────────────┘    └────────────┘    └────────────┘    └────────────┘      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Lambda Configuration Options:**

```yaml
lambda_config:
  runtime: "python3.11"       # python3.9-3.12, nodejs18.x-20.x, java11-17, go1.x, rust
  memory_mb: 256              # 128 MB - 10,240 MB (in 1 MB increments)
  timeout_seconds: 30         # 1 second - 900 seconds (15 minutes)
  ephemeral_storage_mb: 512   # 512 MB - 10,240 MB
  reserved_concurrency: 100   # -1 = unreserved account limit
  layers:
    - "arn:aws:lambda:us-east-1:123456789:layer:shared-libs:1"
  environment:
    variables:
      TABLE_NAME: "Users"
      STAGE: "production"
  dead_letter_config:
    target_arn: "arn:aws:sqs:us-east-1:123456789:dlq-lambda"
  vpc_config:
    subnet_ids: ["subnet-xxx", "subnet-yyy"]
    security_group_ids: ["sg-xxx"]
  tracing_config:
    mode: "Active"            # Active | PassThrough
```

#### Container Services (ECS/EKS)

**ECS Fargate Task Definition:**

```yaml
ecs_task_definition:
  family: "web-api"
  cpu: "512"
  memory: "1024"
  execution_role_arn: "arn:aws:iam::123:role/ecsTaskExecutionRole"
  task_role_arn: "arn:aws:iam::123:role/ecsTaskRole"
  network_mode: "awsvpc"
  requires_compatibilities: ["FARGATE"]
  containers:
    - name: "api"
      image: "123456789.dkr.ecr.us-east-1.amazonaws.com/api:latest"
      portMappings:
        - containerPort: 8080
          protocol: "tcp"
      environment:
        - name: "DB_HOST"
          valueFrom:
            secrets:
              - name: "arn:aws:secretsmanager:us-east-1:123:secret:db-credentials"
                valueFrom: "host"
      logConfiguration:
        logDriver: "awslogs"
        options:
          awslogs-group: "/ecs/web-api"
          awslogs-region: "us-east-1"
          awslogs-stream-prefix: "ecs"
      healthCheck:
        command: ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
        interval: 30
        timeout: 5
        retries: 3
        startPeriod: 60
```

### 4.2 Storage Manager

#### S3 Bucket Configuration

```yaml
s3_bucket_config:
  bucket_name: "myapp-production-assets"
  versioning: true
  encryption:
    type: "aws:kms"
    kms_key_id: "arn:aws:kms:us-east-1:123:key/xxx"
  block_public_access:
    block_public_acls: true
    block_public_policy: true
    ignore_public_acls: true
    restrict_public_buckets: true
  lifecycle_rules:
    - id: "archive-old-data"
      prefix: "logs/"
      transitions:
        - days: 30
          storage_class: "STANDARD_IA"
        - days: 90
          storage_class: "GLACIER"
        - days: 365
          storage_class: "DEEP_ARCHIVE"
      expiration:
        days: 730
    - id: "intelligent-tiering"
      prefix: "data/"
      intelligent_tiering:
        - access_tier: "ARCHIVE_ACCESS"
          days: 90
        - access_tier: "DEEP_ARCHIVE_ACCESS"
          days: 180
  cors:
    - allowed_headers: ["*"]
      allowed_methods: ["GET", "HEAD"]
      allowed_origins: ["https://app.example.com"]
      max_age_seconds: 3600
  replication:
    destination:
      bucket: "arn:aws:s3:::myapp-dr-backup"
      storage_class: "STANDARD_IA"
      encryption: true
    rules:
      - prefix: ""
        status: "Enabled"
  object_lock:
    enabled: true
    mode: "COMPLIANCE"
    retention_days: 2555  # ~7 years
```

#### EBS Volume Types

| Type     | Max IOPS  | Max Throughput | Use Case                | Cost     |
|----------|-----------|----------------|------------------------|----------|
| gp3      | 16,000    | 1,000 MB/s     | General purpose        | Low      |
| gp2      | 16,000    | 250 MB/s       | Legacy general purpose | Low      |
| io2       | 64,000    | 1,000 MB/s     | Mission-critical DB    | High     |
| io2 Block | 256,000   | 4,000 MB/s     | SAP HANA, Oracle       | Very High|
| st1      | 500       | 500 MB/s       | Throughput-heavy work  | Low      |
| sc1      | 250       | 250 MB/s       | Cold storage           | Lowest   |

### 4.3 Network Manager

#### VPC Design Patterns

```
Pattern 1: Single VPC with Public/Private Subnets
─────────────────────────────────────────────────
  VPC 10.0.0.0/16
  ├── Public Subnet 10.0.1.0/24  (ALB, Bastion)
  ├── Private Subnet 10.0.11.0/24 (App servers)
  └── Data Subnet 10.0.21.0/24   (RDS, ElastiCache)

Pattern 2: Multi-VPC with Peering
──────────────────────────────────
  Dev VPC 10.1.0.0/16 ◄──── peering ────► Staging VPC 10.2.0.0/16
       │                                          │
       └──────────── peering ─────────────────────┘
       │
  Prod VPC 10.3.0.0/16

Pattern 3: Transit Gateway Hub-and-Spoke
─────────────────────────────────────────
         ┌──── Dev VPC
         │
  Transit GW ──── Staging VPC
         │
         └──── Prod VPC
         │
         └──── Shared Services VPC
```

**Subnet Strategy:**

| Subnet Type | Route Target         | Use Case                    | Internet Access |
|------------|----------------------|-----------------------------|-----------------|
| Public     | Internet Gateway     | ALB, Bastion, NAT Gateway   | Inbound + Outbound |
| Private    | NAT Gateway          | App servers, Lambda VPC     | Outbound only   |
| Data       | No internet route    | RDS, ElastiCache, Redshift  | None            |
| Isolated   | No internet route    | Sensitive workloads         | None            |

#### Security Groups vs NACLs

| Feature              | Security Groups              | NACLs                        |
|---------------------|------------------------------|------------------------------|
| Level               | Instance-level               | Subnet-level                 |
| State               | Stateful                     | Stateless                    |
| Rules               | Allow only                   | Allow and Deny               |
| Evaluation          | All rules evaluated          | Rules in number order        |
| Default              | Allow all outbound           | Allow all inbound/outbound   |
| Scope               | Can reference other SGs      | Can reference CIDR only      |
| Performance         | Faster (stateful)            | Slower (stateful tracking)   |
| Use Case            | Primary security mechanism   | Additional defense layer     |

### 4.4 Database Manager

#### RDS Best Practices

```yaml
rds_configuration:
  engine: "postgres"
  engine_version: "15.4"
  instance_class: "db.r6g.large"
  storage:
    type: "gp3"
    allocated_gb: 100
    iops: 3000
    throughput: 125
    encrypted: true
    kms_key: "arn:aws:kms:us-east-1:123:key/xxx"
  high_availability:
    multi_az: true
    auto_failover: true
  backup:
    automated: true
    retention_days: 35
    backup_window: "03:00-04:00"
    maintenance_window: "Mon:04:00-Mon:05:00"
  monitoring:
    performance_insights: true
    enhanced_monitoring: true
    monitoring_interval: 60
    cloudwatch_alarms:
      - cpu_utilization: 80
      - free_storage: 10240  # MB
      - connections: 100
  networking:
    publicly_accessible: false
    db_subnet_group: "prod-subnet-group"
    vpc_security_groups: ["sg-rds-prod"]
    parameter_group: "custom-pg-15"
  parameters:
    shared_preload_libraries: "pg_stat_statements"
    max_connections: "200"
    log_min_duration_statement: "1000"
```

#### DynamoDB Design

```yaml
dynamodb_config:
  table_name: "Users"
  billing_mode: "PAY_PER_REQUEST"  # or PROVISIONED
  partition_key:
    name: "PK"
    type: "S"
  sort_key:
    name: "SK"
    type: "S"
  global_secondary_indexes:
    - index_name: "GSI1"
      partition_key: { name: "GSI1PK", type: "S" }
      sort_key: { name: "GSI1SK", type: "S" }
      projection_type: "ALL"
  local_secondary_indexes:
    - index_name: "LSI1"
      sort_key: { name: "LSI1SK", type: "S" }
      projection_type: "ALL"
  point_in_time_recovery: true
  sse_specification:
    sse_enabled: true
    sse_type: "KMS"
    kms_master_key: "arn:aws:kms:us-east-1:123:key/xxx"
  ttl:
    attribute_name: "expires_at"
    enabled: true
  auto_scaling:
    read:
      min_capacity: 5
      max_capacity: 1000
      target_value: 70
    write:
      min_capacity: 5
      max_capacity: 1000
      target_value: 70
```

### 4.5 Security & Compliance Manager

#### IAM Hardening

```yaml
iam_best_practices:
  root_account:
    - "Enable MFA on root account"
    - "Never use root for daily operations"
    - "Create CloudTrail alarm for root usage"

  iam_users:
    - "Enforce MFA for all human users"
    - "Use roles instead of long-lived access keys"
    - "Rotate access keys every 90 days"
    - "Enable credential reports"

  iam_roles:
    - "Least privilege: only required actions"
    - "Use managed policies over inline"
    - "Set maximum session duration"
    - "Use permission boundaries for delegation"
    - "Tag roles for cost allocation"

  service_control_policies:
    - "Deny leaving the organization"
    - "Deny disabling CloudTrail"
    - "Deny modifying IAM policies"
    - "Restrict regions"
    - "Deny public S3 buckets"

  aws_organizations:
    organizational_units:
      - Security (Log Archive, Security Tooling)
      - Infrastructure (Network, Shared Services)
      - Workloads (Prod, Staging, Dev, Sandbox)
```

#### Encryption Strategy

| Service        | Default Encryption | Key Type        | Rotation |
|---------------|-------------------|-----------------|----------|
| S3            | SSE-S3            | SSE-KMS (CMK)   | Annual   |
| EBS           | Enabled (AES-256) | KMS CMK         | Annual   |
| RDS           | Enabled           | KMS CMK         | Annual   |
| DynamoDB      | Enabled           | KMS CMK         | Annual   |
| ElastiCache   | In-transit        | KMS CMK         | Annual   |
| SQS/SNS       | Enabled           | KMS CMK         | Annual   |
| Kinesis        | Enabled           | KMS CMK         | Annual   |
| Redshift       | Enabled           | KMS CMK         | Annual   |

#### Secrets Management

```yaml
secrets_manager:
  rotation:
    enabled: true
    rotation_lambda: "arn:aws:lambda:us-east-1:123:secret-rotation"
    schedule: "rate(30 days)"
  secrets:
    - name: "prod/database/credentials"
      description: "RDS production credentials"
      kms_key: "arn:aws:kms:us-east-1:123:key/xxx"
      tags:
        Environment: "production"
        Application: "web-api"
    - name: "prod/api-keys/third-party"
      description: "Third-party API keys"
      kms_key: "arn:aws:kms:us-east-1:123:key/xxx"

parameter_store:
  standard:
    - name: "/config/web-api/stage"
      value: "production"
      tier: "Standard"
  secure:
    - name: "/secure/web-api/db-host"
      value: "prod-db.xxx.rds.amazonaws.com"
      tier: "SecureString"
      kms_key: "alias/aws/ssm"
```

### 4.6 Messaging & Events

#### Event-Driven Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    AWS Event-Driven Architecture                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐      │
│  │ API GW   │───▶│ Lambda       │───▶│ SQS          │───▶│ Lambda   │      │
│  │ (REST)   │    │ (Handler)    │    │ (Buffer)     │    │ (Worker) │      │
│  └──────────┘    └──────┬───────┘    └──────────────┘    └──────────┘      │
│                         │                                                   │
│                         ▼                                                   │
│                  ┌──────────────┐    ┌──────────────┐    ┌──────────┐      │
│                  │ DynamoDB     │    │ EventBridge  │───▶│ Lambda   │      │
│                  │ (Write)      │    │ (Rule)       │    │ (React)  │      │
│                  └──────────────┘    └──────────────┘    └──────────┘      │
│                                                                              │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐      │
│  │ S3       │───▶│ EventBridge  │───▶│ Step Func    │───▶│ Multiple │      │
│  │ (Upload) │    │ (Pattern)    │    │ (Orchestrate)│    │ Lambdas  │      │
│  └──────────┘    └──────────────┘    └──────────────┘    └──────────┘      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**SQS Configuration:**

```yaml
sqs_queue:
  queue_name: "web-api-tasks"
  queue_type: "standard"  # or "fifo"
  visibility_timeout: 300
  message_retention: 1209600  # 14 days
  receive_wait_time: 20  # long polling
  dead_letter_queue:
    target_arn: "arn:aws:sqs:us-east-1:123:web-api-tasks-dlq"
    max_receive_count: 3
  kms_master_key: "alias/aws/sqs"
  policy:
    - Effect: "Allow"
      Principal: { Service: "lambda.amazonaws.com" }
      Action: "sqs:SendMessage"
      Resource: "arn:aws:sqs:us-east-1:123:web-api-tasks"
```

**EventBridge Rules:**

```yaml
eventbridge_rules:
  - name: "ec2-state-change"
    event_pattern:
      source: ["aws.ec2"]
      detail_type: ["EC2 Instance State-change Notification"]
      detail:
        state: ["stopped", "terminated"]
    targets:
      - arn: "arn:aws:lambda:us-east-1:123:notify-slack"
      - arn: "arn:aws:sqs:us-east-1:123:ec2-events"

  - name: "rds-backup-complete"
    event_pattern:
      source: ["aws.rds"]
      detail_type: ["RDS DB Instance Event"]
      detail:
        EventCategories: ["backup"]
    targets:
      - arn: "arn:aws:sns:us-east-1:123:backup-notifications"
```

## 5. State Management

### 5.1 State Registry

The agent maintains an in-memory state registry for all provisioned resources:

```python
@dataclass
class ResourceState:
    resource_id: str
    resource_type: str  # ec2, s3, rds, lambda, vpc, etc.
    provider: str       # aws
    region: str
    status: str         # creating, running, stopped, terminated
    properties: Dict[str, Any]
    tags: Dict[str, str]
    created_at: datetime
    updated_at: datetime
    cost_per_hour: float
```

### 5.2 State Export/Import

```python
# Export state
state_json = agent.export_state()
# Produces JSON with all resources, their properties, and metadata

# Import state (for disaster recovery or session continuity)
agent.import_state(state_json)

# Drift detection
drift = agent.detect_drift()
# Returns list of resources modified outside the agent
```

### 5.3 State Versioning

- State snapshots stored in S3 for rollback capability
- Version history maintained (last 10 snapshots)
- Drift detection compares deployed vs. desired state

## 6. Observability

### 6.1 Structured Logging

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "INFO",
  "agent": "AWSSpecialistAgent",
  "operation": "ec2.provision",
  "instance_id": "i-1234567890abcdef0",
  "instance_type": "t3.micro",
  "region": "us-east-1",
  "duration_ms": 245,
  "status": "success",
  "cost_estimate": "$0.0104/hr"
}
```

### 6.2 Metrics

| Metric               | Type      | Description                            |
|---------------------|-----------|----------------------------------------|
| aws_operation_total  | Counter   | Operations by type and status          |
| provision_latency_ms | Histogram | Provisioning latency per resource type |
| resource_count       | Gauge     | Managed resources by type              |
| cost_estimate_usd    | Gauge     | Estimated hourly cost                  |
| drift_detected       | Counter   | Drift events detected                  |

### 6.3 Health Checks

- API health endpoint returning agent status and resource counts
- Dependency checks for AWS service availability (STS, EC2, S3)
- Circuit breaker pattern for transient failures (3 retries, exponential backoff)

## 7. Security Architecture

### 7.1 Threat Model

| Threat              | Mitigation                                    |
|--------------------|-----------------------------------------------|
| Insider Threat     | IAM Access Analyzer + CloudTrail audit         |
| Data Exfiltration  | VPC endpoints + NACLs + S3 block public access |
| Credential Leakage | Secrets Manager + no hardcoded creds          |
| DDoS              | Shield Advanced + WAF + ALB rate limiting      |
| Privilege Escalation| Least privilege + SCP guardrails              |
| Supply Chain       | Dependency scanning + image scanning          |

### 7.2 Compliance Frameworks

```yaml
compliance_controls:
  soc2:
    - CloudTrail enabled in all regions
    - AWS Config rules active
    - Security Hub aggregation
    - GuardDuty enabled
    - VPC Flow Logs enabled

  hipaa:
    - Encryption at rest (all data stores)
    - Encryption in transit (TLS 1.2+)
    - Access logging enabled
    - Audit trails retained 6 years
    - BAA with AWS

  pci_dss:
    - Network segmentation (cardholder data environment)
    - Encryption of cardholder data
    - Vulnerability scanning (monthly)
    - Access control (least privilege)
    - Audit logging (1 year retention)

  gdpr:
    - Data residency controls (region selection)
    - Data deletion capabilities
    - Access logging for PII
    - Encryption of personal data
    - Breach notification process
```

## 8. Cost Management

### 8.1 Cost Estimation Engine

```yaml
pricing_models:
  compute:
    on_demand: "Pay per hour, no commitment"
    reserved_1yr: "Up to 40% savings vs on-demand"
    reserved_3yr: "Up to 60% savings vs on-demand"
    savings_plans_1yr: "Up to 30% savings, flexible"
    savings_plans_3yr: "Up to 50% savings, flexible"
    spot: "Up to 90% savings, interruptible"

  storage:
    standard: "Frequently accessed"
    standard_ia: "Infrequent access, 30-day minimum"
    one_zone_ia: "Single AZ, lowest cost IA"
    glacier: "Archive, retrieval minutes-hours"
    glacier_deep: "Long-term archive, retrieval hours"

  database:
    provisioned: "Predictable workloads, hourly billing"
    serverless: "Variable workloads, per-use billing"
    aurora_serverless_v2: "Auto-scaling, per-ACU billing"
```

### 8.2 Optimization Recommendations

| Category        | Recommendation                          | Savings    |
|----------------|------------------------------------------|-----------|
| Right-sizing   | Downgrade over-provisioned EC2           | 15-30%    |
| Reserved       | Purchase RIs for steady workloads        | 30-60%    |
| Spot           | Use for batch/CI/stateless               | 60-90%    |
| Storage        | Lifecycle to IA/Glacier                  | 20-40%    |
| Idle Resources | Remove unattached EBS/empty LBs          | $50-200/mo|
| NAT Gateway    | Use VPC endpoints for AWS services       | 30-50%    |
| Data Transfer  | Use CloudFront for caching              | 40-60%    |

### 8.3 Tagging Strategy

```yaml
required_tags:
  - key: "Environment"
    values: ["production", "staging", "development"]
    enforced: true
  - key: "Owner"
    values: ["team-name"]
    enforced: true
  - key: "CostCenter"
    values: ["CC-1234"]
    enforced: true
  - key: "Application"
    values: ["app-name"]
    enforced: true
  - key: "DataClassification"
    values: ["public", "internal", "confidential", "restricted"]
    enforced: true

optional_tags:
  - key: "Project"
  - key: "Version"
  - key: "ManagedBy"
  - key: "Backup"
```

## 9. Disaster Recovery

### 9.1 Backup Strategy

| Service     | Backup Method               | RPO           | Retention    |
|------------|----------------------------|---------------|--------------|
| RDS        | Automated daily + txn logs  | 5 minutes     | 35 days      |
| EBS        | Snapshots + lifecycle       | 24 hours      | 30 days      |
| S3         | Cross-region replication    | Real-time     | Indefinite   |
| DynamoDB   | Point-in-time recovery      | 5 minutes     | 35 days      |
| ElastiCache| Snapshots + daily backup    | 24 hours      | 35 days      |
| Redshift   | Automated snapshots         | 24 hours      | 30 days      |

### 9.2 DR Strategies

```yaml
disaster_recovery:
  backup_restore:
    rpo: "24 hours"
    rto: "4-8 hours"
    cost: "Low"
    use_case: "Non-critical workloads"

  pilot_light:
    rpo: "1 hour"
    rto: "1-2 hours"
    cost: "Medium"
    resources:
      - "RDS read replica in secondary region"
      - "S3 cross-region replication"
      - "AMI copy to secondary region"

  warm_standby:
    rpo: "5 minutes"
    rto: "15-30 minutes"
    cost: "High"
    resources:
      - "Scaled-down ECS service in secondary region"
      - "Aurora Global Database"
      - "Route 53 health checks"

  multi_site_active_active:
    rpo: "0"
    rto: "< 5 minutes"
    cost: "Very High"
    resources:
      - "Full ECS/EKS in both regions"
      - "Aurora Global Database with write forwarding"
      - "CloudFront with origin groups"
```

## 10. Integration Patterns

### 10.1 CI/CD Integration

```yaml
cicd_pipeline:
  source:
    provider: "CodeCommit"  # or GitHub, GitLab
    branch: "main"
  build:
    provider: "CodeBuild"
    commands:
      - "pip install -r requirements.txt"
      - "python -m pytest tests/"
      - "cdk synth"
  test:
    provider: "CodeBuild"
    commands:
      - "python -m pytest tests/integration/"
  deploy:
    provider: "CodeDeploy"
    strategy: "blue_green"  # or rolling, canary
    approvals:
      - "manual"  # for production
```

### 10.2 Event-Driven Automation

```
CloudTrail → EventBridge → SNS → Lambda (Alert)
EC2 State Change → EventBridge → Lambda (Notify)
RDS Event → EventBridge → SNS (Backup notification)
Config Rule Violation → EventBridge → Lambda (Remediate)
GuardDuty Finding → EventBridge → Lambda (Investigate)
```

## 11. Configuration Reference

### 11.1 Agent Configuration

```yaml
agent_config:
  region: us-east-1
  default_instance_type: t3.micro
  auto_scaling: true
  enable_monitoring: true
  enable_logging: true
  max_instances: 10
  vpc_cidr: 10.0.0.0/16
  environment: development
  backup_retention_days: 7
  multi_az: false
  tags:
    Project: MyApp
    ManagedBy: AWSSpecialistAgent
    CostCenter: Engineering
```

### 11.2 Resource Limits

| Resource                  | Default Limit | Configurable |
|--------------------------|---------------|--------------|
| EC2 instances per agent  | 100           | Yes          |
| S3 buckets               | 1000          | AWS limit    |
| Lambda functions          | 1000/region   | AWS limit    |
| VPCs per region           | 5             | AWS limit    |
| RDS instances             | 40            | AWS limit    |
| Security groups           | 2500          | AWS limit    |

## 12. Performance Considerations

### 12.1 Scalability

- Stateless agent design allows horizontal scaling
- Connection pooling for AWS SDK clients
- Exponential backoff with jitter for API retries
- Batch operations where API supports it

### 12.2 Latency Targets

| Operation              | Target     |
|-----------------------|------------|
| EC2 provision          | < 30 sec  |
| S3 bucket creation     | < 5 sec   |
| Lambda deploy          | < 15 sec  |
| RDS provision          | < 10 min  |
| VPC creation           | < 60 sec  |
| Security group create  | < 5 sec   |
| State export           | < 5 sec   |

## 13. Testing Strategy

### 13.1 Unit Tests

- Mock boto3 client responses with moto
- Validate input parameters and error handling
- Test state transitions and business logic
- Test IAM policy generation and validation

### 13.2 Integration Tests

- Deploy to isolated AWS test account
- Verify resource creation and configuration
- Test cross-service interactions
- Clean up resources after test execution

### 13.3 Contract Tests

- Validate AWS API contract compliance
- Ensure backward compatibility
- Test error response handling

## 14. Future Roadmap

| Phase | Scope | Status |
|-------|-------|--------|
| Phase 1 | EC2, S3, Lambda, IAM, VPC, RDS, DynamoDB | Current |
| Phase 2 | EKS, ECS, ElastiCache, Neptune, SageMaker | Planned |
| Phase 3 | Multi-account Organizations, Control Tower | Planned |
| Phase 4 | AI-powered anomaly detection and auto-remediation | Planned |
| Phase 5 | Cross-cloud federation (Azure AD integration) | Future |

## 15. Operational Runbook

### 15.1 Startup

1. Load configuration from environment variables or config file
2. Initialize AWS SDK clients with region and credentials
3. Validate connectivity with `sts.get_caller_identity()`
4. Load state from S3 or initialize empty state
5. Start metrics collection and logging

### 15.2 Shutdown

1. Flush pending operations
2. Export current state to S3 backup
3. Close AWS SDK sessions
4. Flush log buffers

### 15.3 Troubleshooting

| Issue               | Likely Cause              | Resolution                              |
|--------------------|---------------------------|-----------------------------------------|
| ThrottlingException| API rate limit            | Exponential backoff with jitter         |
| AccessDenied       | IAM policy missing        | Add required actions to role policy     |
| LimitExceeded      | Service quota reached     | Request quota increase in Console       |
| DriftDetected      | Resource modified outside | Reconcile via CloudFormation or recreate|
| ProvisionTimeout   | AZ capacity issue         | Different AZ or instance type           |
| InvalidAMIID       | AMI not available         | Verify AMI exists in region             |
