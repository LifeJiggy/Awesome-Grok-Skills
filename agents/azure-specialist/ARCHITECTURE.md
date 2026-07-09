# Azure Specialist Agent - System Architecture

## 1. Overview

The Azure Specialist Agent is a production-grade automation framework for Microsoft Azure cloud services. It provisions and manages compute, networking, storage, databases, security, and application platform resources while enforcing Azure Well-Architected Framework principles.

## 2. Design Principles

- **Azure Well-Architected Framework**: Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency.
- **Infrastructure as Code**: Declarative resource definitions with state tracking and export/import.
- **Zero Trust Security**: Identity-based access, network isolation, encryption everywhere.
- **Observability**: Structured logging, metrics, and operational reporting.
- **High Availability**: Availability sets, zone-redundant storage, auto-scaling.

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Azure Specialist Agent                               │
├─────────────┬─────────────┬─────────────┬─────────────┬───────────────────┤
│  Compute    │  Storage    │  Network     │  Database   │  Application      │
│  Manager    │  Manager    │  Manager     │  Manager    │  Platform         │
├─────────────┼─────────────┼─────────────┼─────────────┼───────────────────┤
│  - VM       │  - Storage  │  - VNet      │  - SQL DB   │  - App Service    │
│  - AKS      │    Account  │  - Subnet    │  - Cosmos   │  - Functions      │
│  - Func App │  - Blob     │  - NSG/NACL  │  - Redis    │  - ACR            │
│  - AV Set   │  - Disk     │  - LB        │  - MySQL    │  - Logic Apps     │
│  - VMSS     │  - KMS/     │  - VPN/      │  - MariaDB  │  - Event Grid     │
│             │    KeyVault │    ExpressRoute│  - PostgreSQL│                  │
└─────────────┴─────────────┴─────────────┴─────────────┴───────────────────┘
         │           │           │           │           │
         └───────────┴───────────┴───────────┴───────────┘
                     │
              ┌──────────────┐
              │  Observability│
              ├──────────────┤
              │  - Azure     │
              │    Monitor   │
              │  - Log       │
              │    Analytics │
              │  - App       │
              │    Insights  │
              └──────────────┘
                     │
              ┌──────────────┐
              │  Identity &  │
              │  Access      │
              ├──────────────┤
              │  - Azure AD  │
              │  - RBAC      │
              │  - Managed   │
              │    Identity  │
              │  - Role      │
              │    Assignments│
              └──────────────┘
```

### Resource Provisioning Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Request    │────▶│  Validation │────▶│  Resource   │
│  Received   │     │  & Planning │     │  Group      │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
              ┌─────▼──────┐          ┌───────▼───────┐          ┌───────▼──────┐
              │  Network   │          │   Compute     │          │   Storage    │
              │  Provision │          │   Provision   │          │   Provision  │
              └─────┬──────┘          └───────┬───────┘          └───────┬──────┘
                    │                          │                          │
                    └──────────────────────────┼──────────────────────────┘
                                               │
                                        ┌──────▼──────┐
                                        │  Configure  │
                                        │  Security   │
                                        │  (NSG,RBAC) │
                                        └──────┬──────┘
                                               │
                                        ┌──────▼──────┐
                                        │  Register   │
                                        │  & Report   │
                                        └─────────────┘
```

## 4. Component Deep Dive

### 4.1 Compute Manager

#### Virtual Machines (IaaS)
- **Size families**: B-series (burstable), D-series (general), E-series (memory-optimized), F-series (compute-optimized), G-series (memory), L-series (storage), N-series (GPU), M-series (memory-intensive).
- **OS support**: Windows Server and Linux (Canonical, RedHat, SUSE, Ubuntu).
- **Availability Sets**: Fault domains (physical rack separation) and update domains (rolling updates).
- **Deployment models**: Single-instance, scale sets, spot/low-priority VMs.
- **Extensions**: Custom script, DSC, run command, guest diagnostics.

#### Availability Sets & Zone-Redundant VMs
- Fault domain count: 2-3 (per region).
- Update domain count: 5 (default).
- Availability Zones: Physically separate datacenters within a region.
- VM Scale Sets (planned): Stateless compute tier with auto-scaling.

#### App Service & Functions (PaaS)
- **App Service Plans**: Basic, Standard, Premium tiers with Linux/Windows OS.
- **Functions**: Serverless with Python, Node.js, .NET, Java, PowerShell triggers.
- **Scaling**: Manual, scheduled, or automatic based on metrics.

#### Container Services (AKS)
- Kubernetes version management (1.24-1.27+).
- Networking plugins: Azure CNI or Kubenet.
- Network policies: Calico or Azure Network Policy.
- Managed identities for Azure AD integration.
- Auto-scaling cluster autoscaler for node pools.

### 4.2 Storage Manager

#### Storage Accounts
- **Performance**: Standard (HDD) vs Premium (SSD).
- **Replication**: LRS, GRS, RAGRS, ZRS, GZRS, RA-GZRS.
- **Access tiers**: Hot, Cool, Archive.
- **Encryption**: Microsoft-managed keys by default; customer-managed with Key Vault.
- **Firewalls and virtual networks**: Restrict access to specific VNets or IP ranges.

#### Blob Storage
- Containers with anonymous blob access disabled by default.
- Soft delete for blobs, snapshots, and versions.
- Immutable storage (WORM) for compliance.
- Lifecycle management for tier transitions.

#### Managed Disks
- Ultra Disk (v2): Low latency, high throughput (requires managed disks with availability zone).
- Premium SSD: Production workloads.
- Standard SSD/HDD: Dev/test and archival.
- Shared disks: For clustered applications (SAP, SQL FCIs).

#### Key Vault
- Secrets: Key-value pairs stored encrypted.
- Keys: RSA and elliptic curve keys with HSM protection (Premium tier).
- Certificates: Import or create with trusted CA.
- Access policies and RBAC authorization.
- Soft delete and purge protection for compliance.

### 4.3 Network Manager

#### Virtual Networks (VNet)
- Address space: RFC 1918 private ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16).
- Subnet delegation for PaaS services (Microsoft.Web, Microsoft.Sql, etc.).
- Service endpoints for direct VNet integration to Azure services.
- VNet peering (global or regional) with gateway transit.

#### Network Security Groups (NSG)
- Stateful packet filtering at subnet or NIC level.
- Priority-based rules (100-4096, lower number = higher priority).
- Default rules: AllowVNetInbound, AllowAzureLoadBalancerInbound.
- Application Security Groups: Tag-based rule targeting.

#### Public IP Addresses
- Static (reserved) vs Dynamic allocation.
- SKUs: Basic (no SLA, all ports) vs Standard (zone-redundant, load-balanced by default).
- Domain name labels for DNS resolution.

#### Load Balancer
- SKUs: Basic vs Standard (zone-redundant, backend pools by NSG).
- Types: Public (internet-facing) or Internal (private VNet only).
- Rules: 5-tuple hash-based distribution.
- Probes: TCP or HTTP health checks.
- Inbound NAT rules for direct RDP/SSH.

#### VPN Gateway
- SKUs: VpnGw1 (low throughput) to VpnGw5 (10+ Gbps).
- Policy-based vs Route-based.
- BGP for dynamic routing.

### 4.4 Database Manager

#### Azure SQL Database
- **Deployment options**: Single database, elastic pool, managed instance.
- **Service tiers**: Basic, Standard (S0-S3), Premium (P1-P15), vCore-based.
- **Features**: Transparent data encryption (TDE), dynamic data masking, row-level security.
- **Performance**: DTU or vCore model with auto-scaling.
- **High availability**: Zone-redundant HA, auto-failover groups.

#### Cosmos DB
- **APIs**: SQL (Core), MongoDB, Cassandra, Gremlin, Table.
- **Consistency levels**: Strong, Bounded staleness, Session, Consistent prefix, Eventual.
- **Partitioning**: Partition key selection for even distribution.
- **Throughput**: Manual (RU/s) or autoscale with max RU/s.
- **Multi-region writes**: Active geo-replication with automatic failover.

#### Cache for Redis
- Tiers: Basic, Standard, Premium.
- Clustering for larger datasets.
- Data persistence: RDB/AOF.
- SSL and authentication enforced.

#### Key Vault
- Soft delete: 90-day retention (optional purge protection).
- RBAC vs access policies for authorization.

### 4.5 Application Platform

#### App Service (Web Apps)
- Runtime stacks: .NET, Java, Node.js, Python, PHP.
- Deployment slots (staging/production) with swap.
- Hybrid connections, VNet integration, private endpoints.
- Built-in load balancing and autoscaling.

#### Azure Functions
- Consumption plan (serverless), Premium (no cold start), Dedicated.
- Trigger types: HTTP, Timer, Blob, Queue, Event Hub, Service Bus, Cosmos DB.
- Durable Functions for orchestration.

### 4.6 Security & Identity

#### Azure Active Directory (Entra ID)
- Tenants, users, groups, service principals.
- Conditional Access policies.
- Privileged Identity Management (PIM) for just-in-time access.
- Identity Protection for risk-based policies.

#### Managed Identities
- System-assigned (tied to resource lifecycle).
- User-assigned (independent, can be shared).

#### Role-Based Access Control (RBAC)
- Built-in roles: Owner, Contributor, Reader, User Access Administrator.
- Custom role definitions with specific actions.
- Scope: Subscription, Resource Group, Resource.

#### Azure Policy & Blueprints
- Policy definitions and assignments for compliance.
- Blueprints for environment templates (dev/test/prod).

## 5. State Management

- In-memory registry with JSON export/import for disaster recovery.
- Tracks resource IDs, names, tags, and relationships.
- State validation for drift detection.
- Support for multi-resource groups and subscriptions (planned).

## 6. Observability

### 6.1 Structured Logging
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "agent": "AzureSpecialistAgent",
  "operation": "compute.vm.create",
  "vm_id": "vm-abc123",
  "vm_name": "web-vm-1",
  "size": "Standard_B2s",
  "os": "Linux",
  "duration_ms": 450,
  "status": "success"
}
```

### 6.2 Metrics
- `azure_operation_total`: Counter by operation type and status.
- `provision_latency_ms`: Provisioning duration per operation.
- `resource_count`: Gauge by resource type.
- `subscription_cost_estimate_usd`: Estimated hourly/monthly spend.

### 6.3 Reporting
- get_status(): Agent overview.
- get_metrics_report(): Operational metrics and success rates.
- get_account_billing_summary(): Cost estimates by subscription.
- validate_configuration(): Pre-deployment checks.
- export_state(): Full state snapshot for backups.

## 7. Security Architecture

### 7.1 Threat Model
- **Insider Threat**: RBAC with least privilege, PIM, access reviews.
- **Data Exfiltration**: NSG rules, private endpoints, VNet service endpoints.
- **Credential Leakage**: No admin passwords in code; Key Vault with RBAC and soft delete.
- **Man-in-the-Middle**: TLS 1.2+, certificate validation, HTTPS-only.

### 7.2 Compliance Frameworks
- **ISO 27001**: Audit log retention, encryption, access control.
- **SOC 2**: Azure AD identity protection, Azure Policy enforcement.
- **HIPAA**: Private endpoints, encryption at rest, audit logging.
- **PCI DSS**: Network segmentation, NSG/WAF rules, monitoring.

### 7.3 Secrets Management
- Azure Key Vault for secrets, keys, and certificates.
- Managed identities eliminate need for secrets in application code.
- Key rotation enforced by policy.
- No secrets in IaC templates; use references or key vault integration.

## 8. Cost Management

### 8.1 Billing Visibility
- Subscription-level cost estimates with resource breakdown.
- Tag-based cost allocation.
- Reservation and savings plan recommendations.

### 8.2 Optimization
- Rightsizing VMs and databases based on utilization.
- Idle resource detection (unattached disks, stopped VMs, empty load balancers).
- Storage tier transitions (Hot → Cool → Archive).
- Dev/Test pricing with Azure Hybrid Benefit for Windows Server and SQL.

### 8.3 Budgets & Alerts
- Budget thresholds at 50%, 80%, 100%.
- Action groups for notifications (email, SMS, webhook).

## 9. Disaster Recovery

### 9.1 Backup Strategy
- **VM Backup**: Azure Backup for VMs; daily, weekly, monthly retention.
- **SQL Database**: Long-term retention (LTR) backups.
- **Storage**: Soft delete, blob versioning, geo-redundant replication.
- **AKS**: Velero or Azure Backup for CSI snapshots.

### 9.2 Recovery Objectives
- RPO < 15 minutes for SQL with full recovery model.
- RTO < 30 minutes for VM restore from backup.
- Cross-region replication for Cosmos DB and RAID-GRS.

### 9.3 Runbooks
- Automated failover for availability zones.
- Point-in-time restore for SQL and Cosmos.
- Geo-restore for storage accounts.

## 10. Integration Patterns

### 10.1 CI/CD with Azure DevOps
- YAML pipelines with stages: Build → Test → Deploy.
- Service connections for Azure subscriptions.
- Deployment slots with swap for zero-downtime releases.

### 10.2 Event-Driven Architecture
- Event Grid for event routing (storage, custom topics).
- Event Hubs for ingestion (telemetry, logs).
- Service Bus for reliable messaging (queues and topics).

### 10.3 API Gateway
- Azure API Management (APIM) with policies and rate limits.
- Functions Proxies for lightweight routing.

## 11. Configuration Reference

```yaml
subscription_id: "00000000-0000-0000-0000-000000000000"
tenant_id: "00000000-0000-0000-0000-000000000000"
resource_group: default
location: eastus
default_vm_size: Standard_B1s
default_os_type: Linux
enable_monitoring: true
enable_backup: true
backup_retention_days: 30
max_vms: 50
environment: development
location_secondary: westus2
tags:
  ManagedBy: AzureSpecialistAgent
  CostCenter: Engineering
```

## 12. Performance Considerations

### 12.1 VM Placement
- Proximity placement groups for low-latency workloads.
- Spread across fault domains for HA.
- Accelerated networking for high-throughput VMs.

### 12.2 Storage Performance
- Premium SSD for IO-intensive workloads.
- Ultra Disk for sub-millisecond latency.
- Application consistent snapshots for databases.

### 12.3 Network Performance
- Accelerated networking (SR-IOV) on supported VM sizes.
- ExpressRoute for private, deterministic connectivity.
- Standard SKU LB with zone-redundant frontends.

## 13. Testing Strategy

### 13.1 Unit Tests
- Mock Azure SDK responses.
- Validate parameter ranges and formats.
- Test business logic and state transitions.

### 13.2 Integration Tests
- Sandbox Azure subscription per test run.
- Resource group teardown after test.
- Health check validation post-provisioning.

### 13.3 Contract Tests
- Validate Azure REST API contract compliance.
- Ensure backward compatibility with ARM templates.

## 14. Future Roadmap

- **Phase 1**: VM, VNet, NSG, LB, Storage, SQL, Cosmos, Key Vault, AKS, Functions. *(Current)*
- **Phase 2**: ExpressRoute, Bastion, Firewall, Front Door, CDN, Event Hubs, Service Bus.
- **Phase 3**: ARM/Bicep/Terraform native deployment, multi-subscription, landing zones.
- **Phase 4**: AI-assisted cost optimization with Azure Cost Management.

## 15. Operational Runbook

### 15.1 Startup
1. Validate Azure SDK configuration and credentials.
2. Verify subscription access via `az account show` equivalent.
3. Initialize state registries and start metric collection.
4. Configure logging with Application Insights (optional).

### 15.2 Shutdown
1. Flush pending metrics and state snapshots.
2. Export state to Azure Blob Storage backup.
3. Close HTTP sessions.

### 15.3 Troubleshooting
- **QuotaExceeded**: Check subscription limits; request increase via Azure portal.
- **AuthorizationFailed**: Review role assignments and Azure Policy denials.
- **SKUNotAvailable**: Verify SKU availability in target region; consider alternative.
- **DeploymentFailed**: Check activity log in Azure portal for detailed error.
- **NetworkPeeringFailed**: Verify address space non-overlap and subscription permissions.
- **KeyVaultAccessDenied**: Check access policy or RBAC role assignment.

---

## 16. Azure Resource Naming Conventions

### Naming Pattern

```
<resource_type>-<project>-<environment>-<region>-<instance>

Examples:
  vm-webapp-prod-eastus-01
  vnet-shared-prod-eastus-01
  sql-db-app-prod-eastus-01
  stwebappprodeastus01
```

### Resource Type Abbreviations

| Resource | Abbreviation | Example |
|----------|--------------|---------|
| Virtual Machine | vm | vm-web-prod-eastus-01 |
| Virtual Network | vnet | vnet-shared-prod-eastus-01 |
| Subnet | snet | snet-web-prod-eastus-01 |
| Network Security Group | nsg | nsg-web-prod-eastus-01 |
| Storage Account | st | stwebappprodeastus01 |
| SQL Database | sql | sql-app-prod-eastus-01 |
| App Service Plan | asp | asp-web-prod-eastus-01 |
| Key Vault | kv | kv-shared-prod-eastus-01 |
| Load Balancer | lb | lb-web-prod-eastus-01 |
| Public IP | pip | pip-web-prod-eastus-01 |

---

## 17. Azure Policy Examples

### Require Tags

```json
{
  "if": {
    "field": "tags['Environment']",
    "exists": "false"
  },
  "then": {
    "effect": "deny"
  }
}
```

### Restrict VM Sizes

```json
{
  "if": {
    "allOf": [
      {
        "field": "type",
        "equals": "Microsoft.Compute/virtualMachines"
      },
      {
        "field": "Microsoft.Compute/virtualMachines/vmSize",
        "notIn": ["Standard_B1s", "Standard_B2s", "Standard_D2s_v3"]
      }
    ]
  },
  "then": {
    "effect": "deny"
  }
}
```

### Require Encryption

```json
{
  "if": {
    "allOf": [
      {
        "field": "type",
        "equals": "Microsoft.Storage/storageAccounts"
      },
      {
        "field": "Microsoft.Storage/storageAccounts/encryption.services.blob.enabled",
        "equals": "false"
      }
    ]
  },
  "then": {
    "effect": "deny"
  }
}
```

---

## 18. NSG Rule Priority Matrix

### Common Web Application Rules

| Priority | Name | Direction | Action | Protocol | Port | Source | Destination |
|----------|------|-----------|--------|----------|------|--------|-------------|
| 100 | AllowHTTPS | Inbound | Allow | TCP | 443 | Internet | * |
| 110 | AllowHTTP | Inbound | Allow | TCP | 80 | Internet | * |
| 200 | AllowSSH | Inbound | Allow | TCP | 22 | AdminIP | * |
| 300 | AllowRDP | Inbound | Allow | TCP | 3389 | AdminIP | * |
| 400 | AllowVNet | Inbound | Allow | * | * | VNet | VNet |
| 500 | AllowLB | Inbound | Allow | * | * | AzureLoadBalancer | * |
| 600 | DenyAll | Inbound | Deny | * | * | * | * |
| 100 | AllowOutbound | Outbound | Allow | * | * | * | Internet |

### Application Security Groups

```python
# Define ASGs
web_asg = ApplicationSecurityGroup(name="asg-web")
db_asg = ApplicationSecurityGroup(name="asg-db")

# NSG rules using ASGs
nsg_rules = [
    NSGRule(
        name="AllowWebToDB",
        priority=100,
        direction="Inbound",
        access="Allow",
        protocol="TCP",
        destination_port_range="1433",
        source_application_security_group=web_asg,
        destination_application_security_group=db_asg,
    )
]
```

---

## 19. VNet Peering Configuration

### Regional Peering

```python
# VNet A (10.0.0.0/16) peered with VNet B (10.1.0.0/16)
peering_config = VNetPeering(
    name="peer-a-to-b",
    remote_vnet_id="/subscriptions/.../virtualNetworks/vnet-b",
    allow_virtual_network_access=True,
    allow_forwarded_traffic=True,
    allow_gateway_transit=False,
    use_remote_gateways=False,
)
```

### Global Peering

```python
# VNet in East US peered with VNet in West US
global_peering = VNetPeering(
    name="peer-east-to-west",
    remote_vnet_id="/subscriptions/.../virtualNetworks/vnet-west",
    allow_virtual_network_access=True,
    allow_forwarded_traffic=True,
    allow_gateway_transit=True,
    use_remote_gateways=False,
)
```

---

## 20. Azure Backup Configuration

### VM Backup Policy

```python
backup_policy = BackupPolicy(
    name="DailyBackup",
    frequency="Daily",
    time="02:00",
    retention_daily=7,
    retention_weekly=4,
    retention_monthly=12,
    retention_yearly=3,
)
```

### SQL Database Backup

```python
sql_backup = SQLBackupConfig(
    backup_storage_redundancy="Geo",  # LRS, ZRS, Geo, GeoZRS
    short_term_retention_days=7,
    long_term_retention_weekly=4,
    long_term_retention_monthly=12,
    long_term_retention_yearly=3,
    geo_backup_enabled=True,
)
```

---

## 21. Cost Estimation Examples

### VM Cost Breakdown

```
VM: Standard_D2s_v3 (2 vCPU, 8 GB RAM)
  Compute: $0.096/hour × 730 hours = $70.08/month
  OS Disk: 127 GB Premium SSD = $19.05/month
  Data Disk: 256 GB Premium SSD = $38.40/month
  Public IP: Static = $4.00/month
  Bandwidth: 100 GB outbound = $8.70/month
  ─────────────────────────────────────────────
  Total: $140.23/month
```

### SQL Database Cost Breakdown

```
Azure SQL Database: Standard S3 (100 DTUs)
  Database: $120.00/month
  Storage: 250 GB included = $0.00
  Backup LRS: 250 GB = $5.00/month
  Threat Detection: $15.00/month
  ─────────────────────────────────────────────
  Total: $140.00/month
```

### Storage Account Cost Breakdown

```
Storage Account: Standard (LRS, Hot)
  Data: 1 TB = $20.48/month
  Write Operations: 100,000 = $0.05
  Read Operations: 1,000,000 = $0.04
  Data Retrieval: 0 GB = $0.00
  ─────────────────────────────────────────────
  Total: $20.57/month
```

---

## 22. Azure Monitor Alert Rules

### VM CPU Alert

```python
alert_rule = AlertRule(
    name="HighCPUAlert",
    resource_id="/subscriptions/.../virtualMachines/vm-001",
    metric_name="Percentage CPU",
    operator="GreaterThan",
    threshold=80,
    time_aggregation="Average",
    window_size="PT5M",
    evaluation_frequency="PT1M",
    severity=2,
    action_groups=["email-ops-team"],
)
```

### SQL DTU Alert

```python
sql_alert = AlertRule(
    name="HighDTUAlert",
    resource_id="/subscriptions/.../databases/mydb",
    metric_name="dtu_consumption_percent",
    operator="GreaterThan",
    threshold=90,
    time_aggregation="Average",
    window_size="PT10M",
    severity=1,
    action_groups=["email-ops-team", "slack-alerts"],
)
```

---

## 23. Azure RBAC Role Assignments

### Built-in Roles

| Role | Scope | Description |
|------|-------|-------------|
| Owner | Subscription | Full access including RBAC |
| Contributor | Subscription | Full access except RBAC |
| Reader | Subscription | Read-only access |
| User Access Administrator | Subscription | Manage RBAC only |
| Virtual Machine Contributor | Subscription | Manage VMs, disks, NICs |
| Network Contributor | Subscription | Manage networks |
| Storage Blob Data Reader | Storage Account | Read blob data |

### Custom Role Example

```python
custom_role = CustomRole(
    name="AppDeployer",
    description="Deploy apps but not modify infrastructure",
    actions=[
        "Microsoft.Web/sites/write",
        "Microsoft.Web/sites/read",
        "Microsoft.Web/sites/start",
        "Microsoft.Web/sites/stop",
        "Microsoft.Insights/components/read",
    ],
    not_actions=[
        "Microsoft.Authorization/*/write",
        "Microsoft.Authorization/*/delete",
    ],
    assignable_scopes=[
        "/subscriptions/00000000-0000-0000-0000-000000000000"
    ],
)
```

---

## 24. Azure App Service Configuration

### App Service Plan Tiers

| Tier | vCPUs | RAM | Storage | Features |
|------|-------|-----|---------|----------|
| Basic B1 | 1 | 1.75 GB | 10 GB | Custom domains, manual scale |
| Standard S1 | 1 | 1.75 GB | 50 GB | Auto-scale, slots, backups |
| Premium P1v3 | 2 | 8 GB | 250 GB | Enhanced performance, more slots |
| Isolated I1 | 2 | 8 GB | 200 GB | VNet integration, dedicated |

### Deployment Slots

```python
# Production and Staging slots
slots = [
    DeploymentSlot(name="production", traffic_percentage=100),
    DeploymentSlot(name="staging", traffic_percentage=0),
]

# Slot swap with preview
swap_preview = SwapOperation(
    source_slot="staging",
    target_slot="production",
    swap_with_preview=True,  # Preview before full swap
)
```

---

## 25. Azure Functions Configuration

### Function App Plans

| Plan | Use Case | Cold Start | Scaling |
|------|----------|------------|---------|
| Consumption | Event-driven, sporadic | Yes | Automatic (0-200) |
| Premium | High-performance, VNet | No | Automatic (1-100) |
| Dedicated | Predictable, always-on | No | Manual/auto |

### Trigger Types

```python
# HTTP Trigger
http_trigger = HttpTrigger(
    auth_level="function",  # anonymous, function, admin
    methods=["GET", "POST"],
)

# Timer Trigger
timer_trigger = TimerTrigger(
    schedule="0 0 */6 * * *",  # Every 6 hours
    run_on_startup=False,
)

# Blob Trigger
blob_trigger = BlobTrigger(
    path="uploads/{name}",
    connection="AzureWebJobsStorage",
)

# Queue Trigger
queue_trigger = QueueTrigger(
    queue_name="process-items",
    connection="AzureWebJobsStorage",
    batch_size=16,
)
```

---

## 26. Azure Cosmos DB Configuration

### Consistency Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| Strong | Linearizable reads | Financial transactions |
| Bounded Staleness | Reads lag by K versions or T seconds | Gaming leaderboards |
| Session | Consistent within session | Most web apps |
| Consistent Prefix | Monotonic reads | Social media feeds |
| Eventual | Eventually consistent | High-throughput analytics |

### Partition Key Strategy

```python
# Good partition key choices
partition_keys = {
    "/userId": "User profiles (even distribution)",
    "/orderId": "Orders (unique per record)",
    "/tenantId": "Multi-tenant (tenant isolation)",
    "/region": "Geographic distribution",
}

# Avoid hot partitions
# Bad: /status (most documents = "active")
# Bad: /timestamp (all recent docs in same partition)
```

### Throughput Configuration

```python
# Manual provisioned throughput
throughput = ContainerThroughput(
    manual_ru=4000,  # Request Units per second
)

# Autoscale throughput
autoscale = ContainerThroughput(
    autoscale_max_ru=10000,  # Max RU/s
    autoscale_min_ru=400,    # Min RU/s (baseline)
)
```

---

## 27. Azure Monitor Queries

### Kusto Query Language (KQL) Examples

```kusto
// VM CPU usage over last hour
Heartbeat
| where TimeGenerated > ago(1h)
| where ComputerName == "vm-web-001"
| summarize avg(ComputerCPUPercentage) by bin(TimeGenerated, 5m)
| render timechart

// Failed sign-ins
SigninLogs
| where ResultType != 0
| summarize count() by UserPrincipalName, ResultDescription
| order by count_ desc

// Storage account operations
StorageBlobLogs
| where TimeGenerated > ago(24h)
| summarize operationCount=count() by OperationName
| render piechart
```

### Workbooks

```json
{
  "version": "Notebook/1.0",
  "items": [
    {
      "type": 1,
      "content": {
        "json": "## Azure Resource Health"
      }
    },
    {
      "type": 3,
      "content": {
        "query": "resources | summarize count() by type",
        "visualization": "piechart"
      }
    }
  ]
}
```

---

## 28. Azure Resource Locks

### Management Group Locks

```python
# Prevent deletion of critical resources
resource_lock = ResourceLock(
    name="CanNotDelete",
    level="CanNotDelete",  # CanNotDelete or ReadOnly
    notes="Production resources - do not delete",
    resource_id="/subscriptions/.../resourceGroups/rg-prod",
)
```

### Lock Hierarchy

```
Management Group (CanNotDelete)
  └── Subscription (CanNotDelete)
        └── Resource Group (CanNotDelete)
              └── Storage Account (ReadOnly)
              └── SQL Database (CanNotDelete)
```

---

## 29. Azure Data Factory Integration

### Pipeline Configuration

```python
pipeline = DataFactoryPipeline(
    name="ETL-Pipeline",
    activities=[
        CopyActivity(
            name="CopyFromSource",
            source=AzureBlobSource(path="input/{yyyy}/{MM}/{dd}"),
            sink=AzureSqlSink(table="staging_data"),
        ),
        StoredProcedureActivity(
            name="TransformData",
            procedure_name="sp_transform",
            parameters={"date": "@pipeline().parameters.runDate"},
        ),
    ],
    parameters={
        "runDate": "2026-07-06"
    }
)
```

### Trigger Types

| Type | Description | Use Case |
|------|-------------|----------|
| Schedule | Cron-based | Daily ETL |
| Tumbling Window | Fixed-size windows | Hourly processing |
| Event | Blob/events trigger | Real-time ingestion |

---

## 30. Azure API Management

### API Configuration

```python
api_config = APIMApi(
    name="Order API",
    path="orders",
    protocols=["https"],
    products=["starter", "premium"],
    policies=[
        RateLimitPolicy(requests=100, renewal_period=60),
        QuotaPolicy(calls=1000, period="day"),
        CORSPolicy(origins=["https://app.example.com"]),
    ],
)
```

### Developer Portal

```
┌─────────────────────────────────────────┐
│ API Management Developer Portal         │
├─────────────────────────────────────────┤
│ • API Documentation                     │
│ • Try-it Console                        │
│ • Subscription Management               │
│ • Usage Analytics                       │
│ • API Key Management                    │
└─────────────────────────────────────────┘
```
