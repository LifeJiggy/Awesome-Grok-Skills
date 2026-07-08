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
