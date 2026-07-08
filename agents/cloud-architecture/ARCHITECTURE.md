# Cloud Architecture Agent — System Architecture

## 1. Overview

The Cloud Architecture Agent is an enterprise-grade design system for multi-cloud infrastructure. It automates architecture design, cost estimation, migration planning, security review, and compliance checking across AWS, Azure, and GCP. The agent follows the Well-Architected Framework and produces production-ready reference architectures with ASCII diagrams, data-flow maps, and cost breakdowns.

## 2. Design Principles

- **Well-Architected First** — Every design is evaluated against the five pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization.
- **Cloud-Native by Default** — Managed services preferred; serverless where appropriate.
- **Infrastructure as Code** — All designs produce Terraform, CloudFormation, or ARM templates.
- **Security-Defense-in-Depth** — Encryption at rest and transit, least-privilege IAM, zero-trust networking.
- **Multi-Cloud Portability** — Abstract provider-specific details behind a unified model.
- **Cost-Aware Design** — Every architecture includes cost projections and optimization levers.

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         Cloud Architecture Agent                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌───────────────────┐  ┌───────────────────┐  ┌──────────────────────────────────┐ │
│  │  Architecture     │  │  Cost Estimator   │  │  Migration Manager               │ │
│  │  Designer         │  │                   │  │                                  │ │
│  │  ┌─────────────┐  │  │  ┌─────────────┐  │  │  ┌────────────┐ ┌────────────┐  │ │
│  │  │ Reference   │  │  │  │ Pricing DB  │  │  │  │ 6R Strategy│ │ Wave Plan  │  │ │
│  │  │ Library     │  │  │  │             │  │  │  │ Engine     │ │ Builder    │  │ │
│  │  └─────────────┘  │  │  └─────────────┘  │  │  └────────────┘ └────────────┘  │ │
│  │  ┌─────────────┐  │  │  ┌─────────────┐  │  │  ┌────────────┐ ┌────────────┐  │ │
│  │  │ Pattern     │  │  │  │ TCO Calc    │  │  │  │ Dependency │ │ Rollback   │  │ │
│  │  │ Generator   │  │  │  │ Engine      │  │  │  │ Mapper     │ │ Planner    │  │ │
│  │  └─────────────┘  │  │  └─────────────┘  │  │  └────────────┘ └────────────┘  │ │
│  └───────────────────┘  └───────────────────┘  └──────────────────────────────────┘ │
│                                                                                      │
│  ┌───────────────────┐  ┌───────────────────┐  ┌──────────────────────────────────┐ │
│  │  Security         │  │  Multi-Cloud      │  │  Compliance &                    │ │
│  │  Architect        │  │  Manager          │  │  Governance                      │ │
│  │  ┌─────────────┐  │  │  ┌─────────────┐  │  │  ┌────────────┐ ┌────────────┐  │ │
│  │  │ Threat      │  │  │  │ Provider    │  │  │  │ Framework  │ │ Policy     │  │ │
│  │  │ Model       │  │  │  │ Abstraction │  │  │  │ Registry   │ │ Engine     │  │ │
│  │  └─────────────┘  │  │  └─────────────┘  │  │  └────────────┘ └────────────┘  │ │
│  │  ┌─────────────┐  │  │  ┌─────────────┐  │  │  ┌────────────┐ ┌────────────┐  │ │
│  │  │ Encryption  │  │  │  │ Drift       │  │  │  │ Audit Log  │ │ Report Gen │  │ │
│  │  │ & Key Mgmt  │  │  │  │ Detector    │  │  │  │ Tracker    │ │            │  │ │
│  │  └─────────────┘  │  │  └─────────────┘  │  │  └────────────┘ └────────────┘  │ │
│  └───────────────────┘  └───────────────────┘  └──────────────────────────────────┘ │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐│
│  │                            Shared Data Layer                                     ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐││
│  │  │ Architecture │  │ Cost Model   │  │ Compliance   │  │ Provider Catalog     │││
│  │  │ Templates    │  │ Registry     │  │ Control Map  │  │ (AWS/Azure/GCP)      │││
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────────┘││
│  └─────────────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## 4. Architecture Design Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           Design Workflow                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Requirements │───▶│ Architecture │───▶│ Cost         │───▶│ Security     │       │
│  │ Analysis     │    │ Design       │    │ Estimation   │    │ Review       │       │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘       │
│        │                   │                   │                    │                 │
│        ▼                   ▼                   ▼                    ▼                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Workload     │    │ Reference    │    │ Optimization │    │ Compliance   │       │
│  │ Profiling    │    │ Architecture │    │ Report       │    │ Validation   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘       │
│        │                   │                   │                    │                 │
│        ▼                   ▼                   ▼                    ▼                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Dependency   │    │ IaC Template │    │ Budget       │    │ Documentation│       │
│  │ Mapping      │    │ Generation   │    │ Alerts       │    │ Generation   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Requirements Analysis Phase

The agent ingests business requirements and translates them into technical constraints:

```
Input Requirements:
├── Business Context
│   ├── Application type (web, API, data platform, ML)
│   ├── Expected user load (concurrent, daily active)
│   ├── Revenue impact of downtime
│   └── Growth projections (1yr, 3yr, 5yr)
├── Technical Constraints
│   ├── Existing technology stack
│   ├── Data residency requirements
│   ├── Latency requirements (p50, p99)
│   └── Integration points (APIs, databases, third-party)
├── Compliance Requirements
│   ├── Regulatory frameworks (SOC2, HIPAA, PCI, GDPR)
│   ├── Data classification levels
│   └── Audit retention periods
└── Budget Constraints
    ├── Monthly spend ceiling
    ├── Capital vs operational preference
    └── Reserved/spot instance willingness
```

### 4.2 Architecture Design Phase

The design engine selects from a library of proven patterns:

```yaml
pattern_selection:
  input:
    workload_type: "web-application"
    scale: "large"
    compliance: ["SOC2", "PCI-DSS"]
    availability_target: "99.99%"

  matching:
    tier_architecture: "three-tier"
    compute_pattern: "auto-scaling-containers"
    data_pattern: "multi-database"
    network_pattern: "multi-az-with-edge"

  output:
    architecture_id: "ARCH-2025-0042"
    provider: "aws"
    components: [...]
    estimated_monthly_cost: "$4,200"
```

## 5. Multi-Cloud Support

### 5.1 Cloud Provider Mapping

| Component          | AWS                            | Azure                           | GCP                           |
|-------------------|--------------------------------|--------------------------------|-------------------------------|
| Compute           | EC2, Lambda, ECS, EKS          | VMs, Functions, AKS            | Compute Engine, Cloud Run, GKE|
| Storage           | S3, EBS, EFS, Glacier          | Blob, Managed Disks, Files     | Cloud Storage, Persistent Disk|
| Database          | RDS, DynamoDB, Aurora, Redshift| SQL DB, CosmosDB, Synapse      | Cloud SQL, Firestore, BigQuery|
| Networking        | VPC, ALB, NLB, CloudFront      | VNet, LB, Front Door           | VPC, Cloud Load Balancer, CDN |
| Security          | IAM, KMS, GuardDuty            | Entra ID, Key Vault, Defender  | IAM, Cloud KMS, SCC          |
| Messaging         | SQS, SNS, EventBridge          | Service Bus, Event Grid        | Pub/Sub, Cloud Tasks          |
| Analytics         | EMR, Athena, Kinesis           | Data Factory, Event Hubs       | Dataflow, Pub/Sub, BigQuery   |
| Monitoring        | CloudWatch, X-Ray              | Monitor, App Insights          | Cloud Monitoring, Trace       |

### 5.2 Provider Abstraction Layer

```python
# Provider-agnostic resource definition
class CloudResource:
    """Unified resource model across clouds."""
    name: str
    resource_type: str  # compute, storage, database, network
    provider: CloudProvider  # AWS, AZURE, GCP
    properties: Dict[str, Any]
    tags: Dict[str, str]
    dependencies: List[str]  # resource IDs this depends on

    def to_terraform(self) -> str:
        """Generate HCL for this resource."""
        ...

    def to_cloudformation(self) -> Dict:
        """Generate CFN resource block."""
        ...

    def to_arm(self) -> Dict:
        """Generate ARM template resource."""
        ...
```

### 5.3 Cross-Cloud Networking

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    Multi-Cloud Network Topology                                   │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  ┌──────────────────────┐         ┌──────────────────────┐                       │
│  │      AWS VPC         │         │     Azure VNet       │                       │
│  │   10.0.0.0/16        │◀───────▶│   10.1.0.0/16        │                       │
│  │                      │  VPN/   │                      │                       │
│  │  ┌────────────────┐  │  Peering│  ┌────────────────┐  │                       │
│  │  │ Public Subnet  │  │         │  │ Public Subnet  │  │                       │
│  │  │ 10.0.1.0/24    │  │         │  │ 10.0.1.0/24    │  │                       │
│  │  └────────────────┘  │         │  └────────────────┘  │                       │
│  │  ┌────────────────┐  │         │  ┌────────────────┐  │                       │
│  │  │ Private Subnet │  │         │  │ Private Subnet │  │                       │
│  │  │ 10.0.11.0/24   │  │         │  │ 10.0.11.0/24   │  │                       │
│  │  └────────────────┘  │         │  └────────────────┘  │                       │
│  │  ┌────────────────┐  │         │  ┌────────────────┐  │                       │
│  │  │ Data Subnet    │  │         │  │ Data Subnet    │  │                       │
│  │  │ 10.0.21.0/24   │  │         │  │ 10.0.21.0/24   │  │                       │
│  │  └────────────────┘  │         │  └────────────────┘  │                       │
│  └──────────────────────┘         └──────────────────────┘                       │
│            │                                │                                     │
│            └──────────┐    ┌────────────────┘                                     │
│                       ▼    ▼                                                      │
│              ┌──────────────────────┐                                             │
│              │      GCP VPC         │                                             │
│              │   10.2.0.0/16        │                                             │
│              │  (Shared Services)   │                                             │
│              └──────────────────────┘                                             │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## 6. Landing Zone Architecture

### 6.1 Multi-Account Strategy

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    Multi-Account / Subscription Layout                            │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                     Management Account / Root                              │  │
│  │  ├── Organization Policy (SCP)                                            │  │
│  │  ├── Billing Consolidation                                                │  │
│  │  └── Identity Provider (SSO / Entra ID)                                  │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│       │                                                                           │
│       ├── Security OU                                                            │
│       │   ├── Log Archive Account        (CloudTrail, Config, VPC Flow Logs)     │
│       │   ├── Security Tooling Account   (GuardDuty, Security Hub, SIEM)         │
│       │   └── Audit Account              (Read-only, cross-account access)       │
│       │                                                                           │
│       ├── Infrastructure OU                                                       │
│       │   ├── Network Account           (VPC, Transit Gateway, VPN)              │
│       │   ├── Shared Services Account   (DNS, Directory, Artifacts)              │
│       │   └── DNS Account               (Route53 / Private DNS)                 │
│       │                                                                           │
│       ├── Workloads OU                                                            │
│       │   ├── Production Account        (prod workloads only)                    │
│       │   ├── Staging Account           (pre-production testing)                 │
│       │   ├── Development Account       (active development)                     │
│       │   └── Sandbox Account           (experimentation, no prod data)          │
│       │                                                                           │
│       └── Policy Staging OU                                                       │
│           └── Policy Staging Account     (test SCPs before applying)             │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Landing Zone Components

```yaml
landing_zone:
  networking:
    hub_spoke_topology: true
    transit_gateway:
      route_tables:
        - shared_services
        - production
        - staging
        - development
    dns:
      private_zone: "*.internal.example.com"
      resolver_inbound: true
    vpn:
      site_to_site: true
      point_to_site: true

  security:
    guardrails:
      - deny_public_s3
      - deny_unencrypted_ebs
      - enforce_mfa
      - require_tags
      - restrict_regions
    logging:
      cloudtrail: true
      vpc_flow_logs: true
      config: true
      access_logs: true

  identity:
    sso_provider: "Entra ID"
    mfa_required: true
    role_mapping:
      admin: "OrganizationAdministrator"
      dev: "DeveloperAccess"
      readonly: "ReadOnlyAccess"

  governance:
    tagging_standard:
      required:
        - Environment
        - Owner
        - CostCenter
        - Application
        - DataClassification
      optional:
        - Project
        - Team
        - Version
    budget_alerts:
      - threshold: 50
        notify: ["finance@example.com"]
      - threshold: 80
        notify: ["finance@example.com", "cto@example.com"]
      - threshold: 100
        notify: ["all-stakeholders"]
        action: "sns-alert"
```

## 7. Network Architecture

### 7.1 VPC Design Patterns

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         Three-Tier VPC Architecture                               │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│                              ┌─────────────────┐                                 │
│                              │   Internet      │                                 │
│                              │   Gateway       │                                 │
│                              └────────┬────────┘                                 │
│                                       │                                          │
│                          ┌────────────┼────────────┐                            │
│                          │            │            │                             │
│                          ▼            ▼            ▼                             │
│                  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│                  │  Public      │ │  Public      │ │  Public      │             │
│                  │  Subnet AZ1 │ │  Subnet AZ2 │ │  Subnet AZ3 │             │
│                  │ 10.0.1.0/24 │ │ 10.0.2.0/24 │ │ 10.0.3.0/24 │             │
│                  │             │ │             │ │             │              │
│                  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │             │
│                  │ │ ALB     │ │ │ │ ALB     │ │ │ │ ALB     │ │             │
│                  │ │ NAT GW  │ │ │ │ NAT GW  │ │ │ │ NAT GW  │ │             │
│                  │ │ Bastion │ │ │ │ Bastion │ │ │ │ Bastion │ │             │
│                  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │             │
│                  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘             │
│                         │               │               │                      │
│                         ▼               ▼               ▼                      │
│                  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│                  │  Private     │ │  Private     │ │  Private     │             │
│                  │  Subnet AZ1 │ │  Subnet AZ2 │ │  Subnet AZ3 │             │
│                  │ 10.0.11.0/24│ │ 10.0.12.0/24│ │ 10.0.13.0/24│             │
│                  │             │ │             │ │             │              │
│                  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │             │
│                  │ │ ECS/EKS │ │ │ │ ECS/EKS │ │ │ │ ECS/EKS │ │             │
│                  │ │ Lambda  │ │ │ │ Lambda  │ │ │ │ Lambda  │ │             │
│                  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │             │
│                  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘             │
│                         │               │               │                      │
│                         ▼               ▼               ▼                      │
│                  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│                  │  Data        │ │  Data        │ │  Data        │             │
│                  │  Subnet AZ1 │ │  Subnet AZ2 │ │  Subnet AZ3 │             │
│                  │ 10.0.21.0/24│ │ 10.0.22.0/24│ │ 10.0.23.0/24│             │
│                  │             │ │             │ │             │              │
│                  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │             │
│                  │ │ RDS     │ │ │ │ RDS     │ │ │ │ RDS     │ │             │
│                  │ │ Redis   │ │ │ │ Redis   │ │ │ │ Redis   │ │             │
│                  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │             │
│                  └─────────────┘ └─────────────┘ └─────────────┘             │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Transit Gateway Topology

```yaml
transit_gateway:
  description: "Hub-and-spoke for multi-VPC connectivity"
  route_tables:
    shared_services:
      attachments:
        - shared_services_vpc
      routes:
        - destination: "10.0.0.0/8"
          target: "blackhole"  # default deny
        - destination: "10.0.100.0/24"
          target: "shared_services_vpc"
    spoke_production:
      attachments:
        - prod_vpc
      routes:
        - destination: "10.0.100.0/24"
          target: "tgw"
        - destination: "0.0.0.0/0"
          target: "prod_nat_gateway"
    spoke_staging:
      attachments:
        - staging_vpc
      routes:
        - destination: "10.0.100.0/24"
          target: "tgw"
```

## 8. Cost Estimation Model

### 8.1 Pricing Factors

```
Monthly Cost = Compute + Storage + Database + Network + Serverless + Management

Where:
  Compute     = Σ(instance_hours × hourly_rate)
  Storage     = Σ(storage_gb × gb_rate) + IOPS costs + snapshots
  Database    = Σ(instance_hours × rate) + storage + backup + I/O
  Network     = Data transfer + inter-region + CDN + NAT Gateway hours
  Serverless  = Requests × $0.20/million + GB-seconds × $0.0000166667
  Management  = Monitoring + Security tools + Support plan
```

### 8.2 Cost Optimization Strategies

```yaml
optimization_strategies:
  reserved_instances:
    description: "Commit to steady-state workloads"
    savings: "30-60%"
    when_to_use:
      - Production databases
      - Always-on application servers
      - Baseline compute capacity
    considerations:
      - 1-year vs 3-year commitment
      - Convertible vs standard
      - Regional vs zonal

  spot_instances:
    description: "Use unused capacity for fault-tolerant workloads"
    savings: "60-90%"
    when_to_use:
      - Batch processing
      - CI/CD pipelines
      - Stateless web servers
      - Container workloads (EKS/Fargate Spot)
    considerations:
      - 2-minute interruption notice
      - Checkpoint frequently
      - Diversify instance types

  right_sizing:
    description: "Match instance types to actual usage"
    savings: "15-30%"
    process:
      - "Analyze 14-day CloudWatch metrics"
      - "Identify CPU/memory underutilization (<30%)"
      - "Test downgrade on staging first"
      - "Monitor performance for 7 days"

  storage_lifecycle:
    description: "Move data to cheaper tiers automatically"
    savings: "20-40%"
    tiers:
      - Standard → Standard-IA (30 days)
      - Standard-IA → Glacier Instant (90 days)
      - Glacier Instant → Glacier Flexible (180 days)
      - Glacier Flexible → Glacier Deep Archive (365 days)

  auto_scaling:
    description: "Match capacity to demand"
    savings: "10-25%"
    strategies:
      - scheduled_scaling: "Predictable traffic patterns"
      - target_tracking: "Maintain target metric value"
      - step_scaling: "React to CloudWatch alarms"
```

### 8.3 Cost Dashboard

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      Monthly Cost Breakdown                                       │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  Compute (EC2/Lambda/ECS)     ████████████████████░░░░░░  $2,400  (40%)         │
│  Storage (S3/EBS)             ████████████░░░░░░░░░░░░░░  $1,200  (20%)         │
│  Database (RDS/DynamoDB)      ██████████████░░░░░░░░░░░░  $1,500  (25%)         │
│  Network (Data Transfer)      ████░░░░░░░░░░░░░░░░░░░░░░  $400   (7%)          │
│  Monitoring & Security        ███░░░░░░░░░░░░░░░░░░░░░░░  $300   (5%)          │
│  Other (Support, DNS, etc)    ██░░░░░░░░░░░░░░░░░░░░░░░░  $200   (3%)          │
│                                                                                   │
│  Total: $6,000/month  |  Projected Annual: $72,000                              │
│  Optimization Potential: -$1,800/month (30%)                                     │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## 9. Security Architecture

### 9.1 Defense-in-Depth Layers

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                        Security Layers                                             │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  Layer 1: Identity & Access Management                                           │
│  ├── IAM Policies & Roles (least privilege)                                     │
│  ├── Multi-Factor Authentication (MFA enforced)                                 │
│  ├── Service Control Policies (SCP guardrails)                                  │
│  ├── Identity Federation (SSO via SAML/OIDC)                                   │
│  └── Privileged Access Management (PAM)                                         │
│                                                                                   │
│  Layer 2: Perimeter Security                                                     │
│  ├── Web Application Firewall (WAF)                                             │
│  ├── DDoS Protection (Shield / Azure DDoS / Cloud Armor)                       │
│  ├── API Gateway Rate Limiting                                                   │
│  ├── Geographic Restrictions                                                     │
│  └── Bot Management                                                             │
│                                                                                   │
│  Layer 3: Network Security                                                       │
│  ├── VPC with Private Subnets (no public IPs on workloads)                     │
│  ├── Security Groups (stateful, instance-level)                                 │
│  ├── NACLs (stateful, subnet-level)                                             │
│  ├── VPC Endpoints (private connectivity to cloud services)                     │
│  ├── Network Segmentation (micro-segmentation)                                  │
│  └── TLS 1.3 for all in-transit traffic                                        │
│                                                                                   │
│  Layer 4: Data Protection                                                        │
│  ├── Encryption at Rest (KMS / CMK with automatic rotation)                    │
│  ├── Encryption in Transit (TLS 1.3 / mTLS)                                    │
│  ├── Data Classification & DLP                                                   │
│  ├── Key Management (HSM-backed for sensitive data)                             │
│  └── Data Masking & Tokenization                                                │
│                                                                                   │
│  Layer 5: Application Security                                                   │
│  ├── SAST/DAST in CI/CD pipeline                                                │
│  ├── Container Image Scanning                                                   │
│  ├── Dependency Vulnerability Scanning                                          │
│  ├── Secrets Management (Secrets Manager / Key Vault)                          │
│  └── Runtime Application Self-Protection (RASP)                                │
│                                                                                   │
│  Layer 6: Monitoring & Response                                                  │
│  ├── CloudTrail / Activity Logs                                                 │
│  ├── SIEM Integration (Splunk, Sentinel, Chronicle)                            │
│  ├── Threat Detection (GuardDuty / Defender for Cloud)                         │
│  ├── Incident Response Playbooks                                                │
│  └── Forensic Evidence Preservation                                            │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Zero-Trust Network Model

```yaml
zero_trust:
  principles:
    - "Never trust, always verify"
    - "Assume breach"
    - "Verify explicitly"
    - "Use least privilege access"

  implementation:
    identity:
      - "Strong authentication (MFA for all humans)"
      - "Service-to-service mTLS"
      - "Short-lived credentials (STS tokens)"
      - "Just-in-time access (PIM)"

    device:
      - "Device health attestation"
      - "Endpoint detection and response"
      - "Patch compliance verification"

    network:
      - "Micro-segmentation with security groups"
      - "Software-defined perimeter"
      - "Encrypted overlay networks"
      - "No implicit trust based on network location"

    application:
      - "Application-level authorization"
      - "API gateway with token validation"
      - "Input validation and output encoding"

    data:
      - "Data classification and labeling"
      - "Encryption everywhere"
      - "Data Loss Prevention (DLP)"
      - "Access logging and audit trails"
```

## 10. Migration Framework

### 10.1 The 6 Rs Migration Strategy

| Strategy    | Description              | Timeline     | Risk    | Cost Impact | Use Case                          |
|------------|--------------------------|-------------|---------|-------------|-----------------------------------|
| Rehost     | Lift and shift           | 4-8 weeks   | Low     | Minimal     | Time pressure, legacy apps        |
| Replatform | Minor cloud optimization | 6-10 weeks  | Medium  | Moderate    | Database to managed service       |
| Refactor   | Re-architect             | 12-20 weeks | High    | Significant | Long-term scale, cloud-native     |
| Repurchase | SaaS replacement         | 2-6 weeks   | Medium  | Ongoing     | Standard functionality            |
| Retire     | Decommission             | 2-4 weeks   | Low     | Savings     | Legacy systems, unused apps       |
| Retain     | Keep on-premises         | N/A         | N/A     | Ongoing     | Regulatory, latency constraints   |

### 10.2 Migration Phases

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         Migration Timeline                                        │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  Phase 1: Discovery & Assessment (Weeks 1-4)                                    │
│  ├── Application inventory and dependency mapping                                │
│  ├── Performance baseline (CPU, memory, I/O, network)                           │
│  ├── TCO calculation (current vs. cloud)                                         │
│  ├── Risk assessment and compliance requirements                                │
│  └── 6R classification per application                                          │
│                                                                                   │
│  Phase 2: Foundation & Landing Zone (Weeks 5-8)                                  │
│  ├── Multi-account setup (org, OUs, SCPs)                                       │
│  ├── VPC design and connectivity (hub-spoke, Transit GW)                       │
│  ├── Identity and access (SSO, IAM roles, service accounts)                    │
│  ├── Logging and monitoring (CloudTrail, Config, GuardDuty)                    │
│  └── Security baseline (WAF, encryption, secrets)                              │
│                                                                                   │
│  Phase 3: Pilot Migration (Weeks 9-12)                                          │
│  ├── Select 2-3 low-risk applications                                           │
│  ├── Execute migration (rehost or replatform)                                   │
│  ├── Validate performance and functionality                                     │
│  ├── Test disaster recovery procedures                                         │
│  └── Document lessons learned and refine playbook                              │
│                                                                                   │
│  Phase 4: Wave Migration (Weeks 13-28)                                          │
│  ├── Group applications by dependency and risk                                  │
│  ├── Migrate in waves (4-6 waves, 2-3 weeks each)                              │
│  ├── Parallel run for critical applications                                     │
│  ├── Data migration (DMS, storage gateway, snapshots)                          │
│  └── Cutover and go-live per wave                                               │
│                                                                                   │
│  Phase 5: Optimization (Weeks 29-32)                                            │
│  ├── Right-size based on actual utilization                                     │
│  ├── Implement reserved instances for steady workloads                         │
│  ├── Enable auto-scaling and spot instances                                    │
│  ├── Decommission legacy infrastructure                                        │
│  └── Knowledge transfer and runbook updates                                    │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 10.3 Migration Tooling

```yaml
migration_tools:
  discovery:
    - AWS Migration Hub
    - Azure Migrate
    - Cloudamize
    - Flexera

  data_migration:
    - AWS DMS (Database Migration Service)
    - Azure Database Migration Service
    - AWS Snowball (large data transfers)
    - Storage Gateway (hybrid storage)

  server_migration:
    - AWS Application Migration Service (MGN)
    - Azure Site Recovery
    - CloudEndure

  container_migration:
    - AWS App2Container
    - Azure Migrate Containers
    - Moby BuildKit
```

## 11. Compliance Frameworks

### 11.1 Supported Frameworks

| Framework  | Key Controls                     | Industry        | Audit Frequency |
|-----------|----------------------------------|-----------------|-----------------|
| SOC 2     | Security, Availability, Privacy  | SaaS, Cloud     | Annual          |
| ISO 27001 | Information Security Management  | Enterprise      | Annual          |
| PCI DSS   | Cardholder Data Protection       | E-commerce      | Quarterly       |
| HIPAA     | PHI Protection                   | Healthcare      | Annual          |
| GDPR      | Data Privacy (EU)                | EU Companies    | Ongoing         |
| FedRAMP   | Government Security              | Public Sector   | Annual          |
| NIST 800-53| Security Controls               | Federal/DoD     | Annual          |
| CCPA      | Consumer Privacy (California)    | CA Companies    | Ongoing         |

### 11.2 Compliance-as-Code

```yaml
compliance_as_code:
  aws_config_rules:
    - s3-bucket-public-read-prohibited
    - ec2-instances-in-vpc
    - encrypted-volumes
    - rds-storage-encrypted
    - iam-user-mfa-enabled
    - root-account-mfa-enabled
    - cloudtrail-enabled
    - vpc-flow-logs-enabled

  azure_policies:
    - StorageAccountsShouldUseHTTPS
    - VMSShouldUseManagedDisks
    - NetworkSecurityGroupsShouldBeDenied
    - SQLServersShouldUseAzureADOnlyAuthentication
    - KeyVaultsShouldHavePurgeProtection

  gcp_policies:
    - compute-vm-require-os-login
    - iam-require-mfa
    - storage-bucket-enable-customer-managed-encryption
    - sql-require-ssl
    - logging-enable-audit
```

## 12. Serverless Architecture Patterns

### 12.1 Event-Driven Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    Serverless Event-Driven Pattern                                │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  ┌─────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐      │
│  │ Client  │───▶│ API Gateway │───▶│ Lambda       │───▶│ DynamoDB        │      │
│  │         │    │ (REST/HTTP) │    │ (Function)   │    │ (NoSQL)         │      │
│  └─────────┘    └─────────────┘    └──────┬───────┘    └─────────────────┘      │
│                                           │                                      │
│                                           ▼                                      │
│                                    ┌──────────────┐    ┌─────────────────┐      │
│                                    │ SNS / SQS    │───▶│ Lambda          │      │
│                                    │ (Messaging)  │    │ (Consumer)      │      │
│                                    └──────────────┘    └────────┬────────┘      │
│                                                                 │               │
│                                           ┌─────────────────────┘               │
│                                           ▼                                      │
│                                    ┌──────────────┐    ┌─────────────────┐      │
│                                    │ EventBridge  │───▶│ Step Functions  │      │
│                                    │ (Router)     │    │ (Orchestration)│      │
│                                    └──────────────┘    └─────────────────┘      │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 12.2 Serverless Decision Matrix

```yaml
serverless_decision:
  use_serverless_when:
    - "Event-driven or scheduled workloads"
    - "Variable or unpredictable traffic"
    - "Short-lived execution (<15 minutes)"
    - "No persistent connections required"
    - "Rapid prototyping needed"

  avoid_serverless_when:
    - "Long-running processes (>15 minutes)"
    - "Persistent WebSocket connections"
    - "Consistent high-throughput (24/7)"
    - "Specialized hardware (GPU) required"
    - "VPC-native with fixed IP needed"
```

## 13. Container Orchestration Architecture

### 13.1 Kubernetes Cluster Design

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster Architecture                                │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  ┌──────────────────────────────────────────────────────────────────────────┐    │
│  │                     Control Plane                                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐               │    │
│  │  │ API      │  │ etcd     │  │ Scheduler│  │ Controller│              │    │
│  │  │ Server   │  │ Store    │  │          │  │ Manager  │               │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘               │    │
│  └──────────────────────────────────────────────────────────────────────────┘    │
│                              │                                                   │
│  ┌──────────────────────────┼───────────────────────────────────────────────┐   │
│  │                     Worker Nodes                                         │   │
│  │                                                                          │   │
│  │  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────┐ │   │
│  │  │    Node Group 1     │  │    Node Group 2     │  │  Spot/Fargate   │ │   │
│  │  │  (General Purpose)  │  │  (Memory Optimized) │  │  (Batch)        │ │   │
│  │  │                     │  │                     │  │                 │ │   │
│  │  │ ┌─────┐ ┌─────┐   │  │ ┌─────┐ ┌─────┐   │  │ ┌─────┐        │ │   │
│  │  │ │Pod 1│ │Pod 2│   │  │ │Pod 3│ │Pod 4│   │  │ │Pod 5│        │ │   │
│  │  │ └─────┘ └─────┘   │  │ └─────┘ └─────┘   │  │ └─────┘        │ │   │
│  │  └─────────────────────┘  └─────────────────────┘  └─────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│                                                                                   │
│  ┌──────────────────────────────────────────────────────────────────────────┐    │
│  │                     Service Mesh (Istio / Linkerd)                        │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐               │    │
│  │  │ mTLS     │  │ Traffic  │  │ Observ-  │  │ Policy   │               │    │
│  │  │          │  │ Mgmt     │  │ ability  │  │ Enforce  │               │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘               │    │
│  └──────────────────────────────────────────────────────────────────────────┘    │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 13.2 Container Platform Selection

| Feature               | ECS Fargate         | EKS                  | AKS                  | GKE Autopilot       |
|-----------------------|--------------------|-----------------------|----------------------|---------------------|
| Control Plane Mgmt   | Fully managed      | Managed (user nodes) | Managed              | Fully managed       |
| Node Management      | None (serverless)  | User-managed         | User/node auto       | None (serverless)   |
| Kubernetes API       | No                 | Yes                   | Yes                  | Yes                 |
| Complexity           | Low                | High                  | Medium               | Low                 |
| Best For             | Simple containers  | Complex K8s workloads | Azure-native K8s    | Simple K8s workloads|
| Cost Model           | Per-task           | Per-node + per-task  | Per-node             | Per-pod             |

## 14. Disaster Recovery Architecture

### 14.1 DR Strategies

```yaml
disaster_recovery:
  backup_and_restore:
    rpo: "24 hours"
    rto: "4-8 hours"
    description: "Restore from backups to new infrastructure"
    cost: "Low"
    use_case: "Non-critical workloads"

  pilot_light:
    rpo: "1 hour"
    rto: "1-2 hours"
    description: "Minimal running infrastructure, scale up on failover"
    cost: "Medium"
    use_case: "Standard business applications"

  warm_standby:
    rpo: "5 minutes"
    rto: "15-30 minutes"
    description: "Scaled-down replica, scale up on failover"
    cost: "High"
    use_case: "Business-critical applications"

  multi_site_active_active:
    rpo: "0 (real-time sync)"
    rto: "< 5 minutes"
    description: "Full production in multiple regions"
    cost: "Very High"
    use_case: "Mission-critical, global applications"
```

### 14.2 DR Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    Multi-Region DR Architecture                                   │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  Primary Region (us-east-1)        Secondary Region (us-west-2)                 │
│  ┌─────────────────────────┐       ┌─────────────────────────┐                  │
│  │ ┌─────────────────────┐ │       │ ┌─────────────────────┐ │                  │
│  │ │     ALB / WAF       │ │       │ │     ALB / WAF       │ │                  │
│  │ └─────────┬───────────┘ │       │ └─────────┬───────────┘ │                  │
│  │           │             │       │           │             │                   │
│  │ ┌─────────▼───────────┐ │       │ ┌─────────▼───────────┐ │                  │
│  │ │   ECS / EKS         │ │       │ │   ECS / EKS         │ │                  │
│  │ │   (Auto Scaling)    │ │       │ │   (Auto Scaling)    │ │                  │
│  │ └─────────┬───────────┘ │       │ └─────────┬───────────┘ │                  │
│  │           │             │       │           │             │                   │
│  │ ┌─────────▼───────────┐ │       │ ┌─────────▼───────────┐ │                  │
│  │ │   RDS Aurora        │◀├───────├▶│   RDS Aurora        │ │                  │
│  │ │   (Multi-AZ + Read  │ │  Cross│ │   (Read Replica)    │ │                  │
│  │ │    Replicas)        │ │Region │ └─────────────────────┘ │                  │
│  │ └─────────────────────┘ │  Repl  │                       │                   │
│  │                         │       │                       │                   │
│  │ ┌─────────────────────┐ │       │ ┌─────────────────────┐ │                  │
│  │ │   S3 Bucket         │◀├───────├▶│   S3 Bucket         │ │                  │
│  │ │   (Primary)         │ │  CRR  │ │   (Replica)         │ │                  │
│  │ └─────────────────────┘ │       │ └─────────────────────┘ │                  │
│  └─────────────────────────┘       └─────────────────────────┘                  │
│                                                                                   │
│  Route53 / Traffic Manager                                                       │
│  ├── Health checks (30s interval)                                               │
│  ├── Failover routing policy                                                    │
│  └── Automatic failover on health check failure                                │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## 15. Performance Engineering

### 15.1 Performance Patterns

```yaml
performance_patterns:
  caching:
    edge_cdn:
      provider: "CloudFront / Azure CDN / Cloud CDN"
      use_case: "Static assets, API responses"
      ttl: "5 minutes - 24 hours"

    application_cache:
      provider: "ElastiCache / Azure Cache for Redis"
      use_case: "Session data, frequent queries"
      strategy: "Cache-aside (Lazy Loading)"
      eviction: "LRU with TTL"

    database_cache:
      provider: "Aurora Read Replicas / Cosmos DB"
      use_case: "Read-heavy workloads"
      strategy: "Read replica + connection pooling"

  async_processing:
    patterns:
      - "Event-driven: SNS → SQS → Lambda"
      - "Message queue: SQS + ECS workers"
      - "Stream processing: Kinesis + Lambda"
      - "Orchestration: Step Functions / Durable Functions"

  auto_scaling:
    triggers:
      cpu_utilization: "> 70%"
      memory_utilization: "> 80%"
      request_count: "> 1000/min"
      queue_depth: "> 100 messages"
      response_time: "> 2 seconds p99"
```

### 15.2 Latency Optimization

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    Latency Optimization Stack                                     │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  Client                                                       Origin Server      │
│    │                                                                 │           │
│    ▼                                                                 ▲           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Browser  │  │ CDN Edge │  │ API GW   │  │ App      │  │ Database │          │
│  │ Cache    │  │ (PoP)    │  │ Cache    │  │ Cache    │  │ Replica  │          │
│  │ (10ms)   │  │ (20ms)   │  │ (5ms)    │  │ (2ms)    │  │ (5ms)    │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
│                                                                                   │
│  Total latency path: Client → CDN → API GW → App → DB                          │
│  With caching: 10ms + 20ms + 5ms + 2ms = 37ms                                  │
│  Without caching: 10ms + 20ms + 5ms + 2ms + 50ms = 87ms                        │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## 16. Data Architecture Patterns

### 16.1 Data Storage Selection

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    Database Selection Matrix                                      │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  Use Case              │ AWS              │ Azure             │ GCP               │
│  ─────────────────────┼─────────────────┼──────────────────┼───────────────────│
│  Relational (OLTP)     │ Aurora/Postgres  │ Azure SQL         │ Cloud SQL         │
│  Document              │ DynamoDB         │ Cosmos DB         │ Firestore         │
│  Key-Value             │ ElastiCache/Redis│ Cache for Redis   │ Memorystore       │
│  Time-Series           │ Timestream       │ Data Explorer     │ Bigtable          │
│  Graph                 │ Neptune          │ Cosmos DB (Gremlin)│ Firestore        │
│  Analytics (OLAP)      │ Redshift         │ Synapse           │ BigQuery          │
│  Search                │ OpenSearch       │ Cognitive Search  │ Cloud Search      │
│  Object Storage        │ S3               │ Blob Storage      │ Cloud Storage     │
│  File Storage          │ EFS/FSx          │ Files/NetApp      │ Filestore         │
│  Ledger                │ QLDB             │ —                 │ —                 │
│  In-Memory             │ ElastiCache      │ Cache for Redis   │ Memorystore       │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 16.2 Data Flow Pattern

```
Data Ingestion → Data Processing → Data Storage → Data Serving → Data Governance

  Kinesis/Event Hubs    Lambda/Functions     S3/Blob           API Gateway        Classification
  Pub/Sub               EMR/Databricks       DynamoDB/Cosmos   CDN                Encryption
  MSK/Event Hubs        Dataflow             Redshift/Synapse  BI Tools           Retention
  Direct Connect        Step Functions       BigQuery           Caching            Compliance
```

## 17. Integration Points

### 17.1 Cloud Provider API Integration

```python
# AWS Integration
import boto3

aws_session = boto3.Session(region_name='us-east-1')
ec2_client = aws_session.client('ec2')
instances = ec2_client.describe_instances(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
)

# Azure Integration
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

credential = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)
vms = compute_client.virtual_machines.list_all()

# GCP Integration
from google.cloud import compute_v1

gcp_client = compute_v1.InstancesClient()
instances = gcp_client.list(project=project_id, zone=zone)
```

### 17.2 Terraform Integration

```hcl
# Multi-cloud module example
module "cloud_architecture" {
  source = "./modules/architecture"

  providers = {
    aws    = aws.primary
    azure  = azurerm.secondary
    google = google.shared_services
  }

  architecture_name = var.architecture_name
  environment       = var.environment
  compliance        = var.compliance_requirements
  cost_optimization = true
  dr_strategy       = "pilot_light"
}

# Networking
module "networking" {
  source = "./modules/networking"

  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  enable_transit_gw  = true
}

# Security
module "security" {
  source = "./modules/security"

  enable_waf          = true
  enable_guardduty    = true
  enable_config       = true
  encryption_level    = "customer_managed"
}
```

## 18. Tech Stack

| Layer            | Technology                                        |
|-----------------|---------------------------------------------------|
| Language         | Python 3.10+, TypeScript                          |
| Type System      | dataclasses, Enum, TypedDict, Pydantic            |
| CLI              | Click / Typer                                     |
| IaC              | Terraform, CloudFormation, ARM, Pulumi            |
| Testing          | pytest, moto (AWS mock), localstack              |
| Documentation    | Markdown, Mermaid diagrams                        |
| State Storage    | JSON snapshots, DynamoDB/Cosmos for persistence  |
| Logging          | Python logging, structured JSON                   |
| Hashing          | hashlib, secrets                                  |
| Pattern Matching | re (regex)                                        |
| ID Generation    | uuid4, nanoid                                     |

## 19. Extension Points

| Extension              | How to Extend                                            |
|------------------------|----------------------------------------------------------|
| New cloud provider     | Add provider enum, implement provider-specific methods  |
| New compliance framework | Add to FRAMEWORKS dict with control mappings          |
| New architecture pattern | Add to patterns library with template and cost model  |
| Custom cost model      | Override cost estimation methods with provider API      |
| Custom IaC output      | Implement new template generator (Pulumi, CDK)         |
| Integration webhook    | Add event hooks for external system notifications      |

## 20. Performance Characteristics

| Metric                        | Target                          |
|-------------------------------|--------------------------------|
| Architecture design time      | 5-15 minutes                   |
| Cost estimation accuracy      | ±10%                           |
| Compliance check time         | 2-5 minutes                    |
| Migration plan generation     | 10-30 minutes                  |
| IaC template generation       | < 30 seconds                   |
| Architecture document render  | < 60 seconds                   |
| Concurrent designs            | 10 per agent instance          |

## 21. Best Practices

1. **Design for Failure** — Assume every component will fail; build redundancy and graceful degradation.
2. **Implement Auto-Scaling** — Match capacity to demand; never over-provision permanently.
3. **Use Managed Services** — Reduce operational overhead; let the cloud provider handle undifferentiated heavy lifting.
4. **Enable Comprehensive Logging** — You cannot manage what you cannot see; log everything, alert on anomalies.
5. **Automate Everything** — Infrastructure as Code is mandatory; no click-ops in production.
6. **Regular Security Reviews** — Continuous compliance scanning; quarterly penetration tests.
7. **Cost Visibility** — Tag all resources; implement budgets and alerts; review monthly.
8. **Disaster Recovery Testing** — Run DR drills quarterly; document and refine playbooks.
9. **Living Documentation** — Architecture decisions recorded (ADRs); diagrams stay current.
10. **Team Training** — Continuous skill development; cloud certifications; game days.
