---
name: "Azure Specialist Agent"
version: "2.0.0"
description: "Senior cloud engineer agent for designing, provisioning, securing, and operating Microsoft Azure infrastructure with production-grade rigor"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["azure", "cloud", "infrastructure", "devops", "security", "kubernetes", "serverless", "databases"]
category: "cloud"
personality: "cloud-architect"
use_cases: ["infrastructure-provisioning", "cloud-migration", "security-hardening", "cost-optimization", "disaster-recovery", "container-orchestration"]
complexity: "advanced"
dependencies: ["python>=3.8"]
---

# Azure Specialist Agent

> Design, provision, secure, and operate Microsoft Azure infrastructure with production-grade rigor.

The Azure Specialist Agent is a production-grade automation framework for Microsoft Azure cloud services. It provisions and manages compute, networking, storage, databases, security, and application platform resources while enforcing Azure Well-Architected Framework principles.

---

## Core Principles

1. **Azure Well-Architected Framework**: Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency.
2. **Infrastructure as Code**: Declarative resource definitions with state tracking and export/import.
3. **Zero Trust Security**: Identity-based access, network isolation, encryption everywhere.
4. **Observability**: Structured logging, metrics, and operational reporting.
5. **High Availability**: Availability sets, zone-redundant storage, auto-scaling.

---

## Capabilities

### 1. Compute Management

Provision and manage virtual machines, container services, and serverless compute.

```python
from agents.azure_specialist.agent import AzureSpecialistAgent, Config

config = Config(
    subscription_id="00000000-0000-0000-0000-000000000000",
    resource_group="prod-rg",
    location="eastus",
    environment="production",
)

agent = AzureSpecialistAgent(config=config)

# Create VM
vm = agent.create_vm(
    name="web-vm",
    size="Standard_B2s",
    admin_username="azureuser",
    admin_password="P@ssw0rd!",
    os_type="Linux",
    availability_set_id=avset.id,
    tags={"Role": "frontend", "Env": "prod"},
)
print(f"VM: {vm.id}, Status: {vm.status}")
# → VM: /subscriptions/.../vm/web-vm, Status: running

# Create availability set
avset = agent.create_availability_set("web-avset", fault_domain_count=2)

# Create App Service Plan
plan = agent.create_app_service_plan("api-plan", sku_name="P1v2", os_type="Linux")

# Deploy Function App
func_app = agent.deploy_function_app(
    "api-functions",
    runtime_stack="python",
    runtime_version="3.11",
    app_service_plan_id=plan.id,
)

# Setup AKS
aks = agent.setup_aks(
    "prod-aks",
    kubernetes_version="1.27",
    node_count=3,
    vm_size="Standard_D2s_v3",
    enable_rbac=True,
    enable_auto_scaling=True,
    min_count=2,
    max_count=10,
)
```

**VM Size Families:**

| Family | Use Case | Examples |
|--------|----------|----------|
| B-series | Burstable, dev/test | B1s, B2s, B2ms |
| D-series | General purpose | D2s_v3, D4s_v3, D8s_v3 |
| E-series | Memory optimized | E2s_v3, E4s_v3, E8s_v3 |
| F-series | Compute optimized | F2s_v2, F4s_v2, F8s_v2 |
| G-series | Memory intensive | G1, G2, G3 |
| L-series | Storage optimized | L4s, L8s, L16s |
| N-series | GPU | NC6, ND6, NV6 |

**VM States:**

| State | Description | Actions |
|-------|-------------|---------|
| Running | VM is operational | stop, restart, deallocate |
| Stopped | VM is stopped (still allocated) | start, deallocate |
| Deallocated | VM is stopped and deallocated | start, delete |
| Failed | VM is in error state | restart, delete |

---

### 2. Storage Management

Create and manage storage accounts, blob containers, and managed disks.

```python
# Create storage account
storage = agent.create_storage_account(
    name="prodstorageacct",
    sku="Standard_GRS",
    kind="StorageV2",
    access_tier="Hot",
    enable_https=True,
    allow_blob_public_access=False,
    tags={"Env": "prod"},
)

# Create blob container
container = agent.create_blob_container(
    storage.name,
    "backups",
    public_access="None",
)

# Create managed disk
disk = agent.create_managed_disk(
    "web-disk",
    disk_size_gb=128,
    sku="Premium_LRS",
    os_type="Linux",
)
```

**Storage Replication Options:**

| Replication | Description | Use Case |
|-------------|-------------|----------|
| LRS | Locally redundant | Dev/test |
| GRS | Geo-redundant | Production |
| RAGRS | Read-access geo-redundant | High availability |
| ZRS | Zone-redundant | Zone-redundant apps |
| GZRS | Geo-zone-redundant | Critical production |
| RA-GZRS | Read-access geo-zone | Maximum availability |

**Storage Access Tiers:**

| Tier | Access Frequency | Cost | Use Case |
|------|------------------|------|----------|
| Hot | Frequent | Higher | Active data |
| Cool | Infrequent | Lower | Archival data |
| Archive | Rare | Lowest | Long-term retention |

---

### 3. Network Management

Configure virtual networks, security groups, load balancers, and VPN gateways.

```python
# Create VNet
vnet = agent.create_virtual_network(
    "prod-vnet",
    ["10.0.0.0/16"],
    dns_servers=["10.0.0.4", "10.0.0.5"],
)

# Add subnet
subnet = agent.add_subnet(
    vnet.id,
    "web-subnet",
    "10.0.1.0/24",
    network_security_group_id=nsg.id,
)

# Create NSG
nsg = agent.create_network_security_group("web-nsg")

# Add NSG rule
agent.add_nsg_security_rule(
    nsg.id,
    "AllowHTTPS",
    priority=100,
    direction="Inbound",
    access="Allow",
    protocol="Tcp",
    source_address_prefix="*",
    source_port_range="*",
    destination_address_prefix="*",
    destination_port_range="443",
)

# Create load balancer
lb = agent.create_load_balancer("web-lb", sku="Standard")

# Create public IP
pip = agent.create_public_ip_address("web-pip", sku="Standard")

# Configure VPN Gateway
vpn = agent.configure_vpn_gateway(
    "hub-vpn",
    vnet.id,
    gateway_type="Vpn",
    sku="VpnGw1",
)
```

**NSG Rule Priorities:**

| Priority | Rule | Description |
|----------|------|-------------|
| 65500 | AllowVNetInbound | Default allow VNet |
| 65000 | AllowAzureLoadBalancer | Default allow LB |
| 65501 | DenyAllInbound | Default deny all |
| 100-4096 | Custom rules | User-defined |

**Load Balancer SKUs:**

| SKU | Features | Use Case |
|-----|----------|----------|
| Basic | Limited rules, no SLA | Dev/test |
| Standard | Zone-redundant, full rules | Production |

---

### 4. Database Management

Provision SQL databases, Cosmos DB, Redis cache, and managed databases.

```python
# Create SQL Server
sql_srv = agent.create_sql_server(
    "dbsrv",
    "sqladmin",
    "S3cureP@ss!",
)

# Create SQL Database
sql_db = agent.create_sql_database(
    "appdb",
    sql_srv.id,
    sku_name="S1",
    max_size_bytes=268435456000,
    zone_redundant=True,
)

# Create Redis Cache
redis = agent.create_redis_cache(
    "appcache",
    sku="Standard",
    capacity=1,
)

# Create Cosmos DB
cosmos = agent.create_cosmos_db_account(
    "appcosmos",
    kind="GlobalDocumentDB",
    consistency_policy="Session",
    enable_auto_failover=True,
)
```

**SQL Database Tiers:**

| Tier | Use Case | Price |
|------|----------|-------|
| Basic | Light workloads | Low |
| Standard | Production | Medium |
| Premium | High performance | High |
| General Purpose | Balanced | Variable |
| Business Critical | Mission critical | High |
| Hyperscale | Large databases | Variable |

**Cosmos DB Consistency Levels:**

| Level | Description | Use Case |
|-------|-------------|----------|
| Strong | Linearizable | Financial |
| Bounded Staleness | Prefix with lag | Leaderboards |
| Session | Client session | Most apps |
| Consistent Prefix | Prefix guaranteed | Social |
| Eventual | No ordering | Counters |

---

### 5. Security & Identity

Configure Azure AD, managed identities, RBAC, and Key Vault.

```python
# Create managed identity
identity = agent.create_system_assigned_identity("app-identity")

# Create Key Vault
vault = agent.create_key_vault(
    "appvault",
    sku="premium",
    enable_purge_protection=True,
)

# Validate NSG rules
issues = agent.validate_nsg_rules(nsg.id)
```

**RBAC Built-in Roles:**

| Role | Permissions | Use Case |
|------|-------------|----------|
| Owner | Full access | Break-glass only |
| Contributor | Create/manage | Operators |
| Reader | Read-only | Monitoring |
| User Access Admin | Manage access | Admins |

**Security Controls:**

| Control | Description | Implementation |
|---------|-------------|----------------|
| Managed Identity | Passwordless auth | System or user-assigned |
| Key Vault | Secrets management | Soft delete, RBAC |
| NSG | Network filtering | Priority-based rules |
| Encryption | Data protection | Platform or customer keys |
| Azure Policy | Compliance | Built-in or custom |

---

### 6. Cost Management

Estimate, optimize, and report on Azure spending.

```python
# Estimate costs
costs = agent.estimate_cost([
    {"type": "vm", "size": "Standard_B2s", "hours": 730},
    {"type": "storage", "sku": "Standard_LRS", "gb": 100},
    {"type": "sql", "tier": "S1"},
])

# Optimize costs
optimization = agent.optimize_costs()
print(f"Potential savings: ${optimization['total_monthly_savings']}")

# Get billing summary
billing = agent.get_account_billing_summary()
```

**Cost Optimization Strategies:**

| Strategy | Description | Savings |
|----------|-------------|---------|
| Reserved Instances | 1-3 year commitment | 30-60% |
| Dev/Test Pricing | Non-production | 50-75% |
| Auto-Shutdown | Stop non-prod VMs | 100% (off-hours) |
| Right-Sizing | Match VM to workload | 20-50% |
| Storage Tiering | Hot → Cool → Archive | 50-80% |

---

## Method Signatures

### Network Management
- `create_virtual_network(name, address_space, location=None, dns_servers=None, tags=None) -> VirtualNetwork`
- `add_subnet(vnet_id, name, address_prefix, network_security_group_id=None, route_table_id=None, service_endpoints=None, delegations=None) -> Subnet`
- `create_network_security_group(name, location=None, tags=None) -> NetworkSecurityGroup`
- `add_nsg_security_rule(nsg_id, name, priority, direction, access, protocol, source_address_prefix, source_port_range, destination_address_prefix, destination_port_range, description="") -> Dict`
- `create_public_ip_address(name, sku="Standard", allocation_method="Static", location=None, tags=None) -> PublicIPAddress`
- `create_network_interface(name, subnet_id, private_ip_address, public_ip_address_id=None, network_security_group_id=None, enable_accelerated_networking=False, location=None, tags=None) -> NetworkInterface`
- `configure_vpn_gateway(name, vnet_id, gateway_type="Vpn", sku="VpnGw1", location=None) -> Dict`
- `create_load_balancer(name, sku="Standard", location=None, tags=None) -> LoadBalancer`

### Compute Management
- `create_vm(name, size, admin_username, admin_password=None, ssh_key_data=None, os_type="Linux", image_reference=None, network_interface_ids=None, availability_set_id=None, disk_ids=None, zones=None, tags=None, enable_boot_diagnostics=True, encryption_at_host=True) -> AzureVM`
- `get_vm(vm_id: str) -> AzureVM`
- `list_vms(status_filter=None, resource_group_filter=None) -> List[AzureVM]`
- `start_vm(vm_id) -> Dict`
- `stop_vm(vm_id, deallocate=True) -> Dict`
- `deallocate_vm(vm_id) -> Dict`
- `restart_vm(vm_id) -> Dict`
- `create_availability_set(name, location=None, fault_domain_count=2, update_domain_count=5, tags=None) -> AvailabilitySet`
- `create_managed_disk(name, disk_size_gb, sku="Standard_LRS", location=None, os_type="Linux", tags=None) -> Disk`
- `create_app_service_plan(name, sku_name="B1", capacity=1, location=None, os_type="Linux", tags=None) -> AppServicePlan`
- `deploy_function_app(name, runtime_stack="python", runtime_version="3.11", app_service_plan_id=None, storage_account_name="", app_settings=None, connection_strings=None) -> FunctionApp`
- `create_function(function_app_name, function_name, trigger_type="HTTP", script="", bindings=None) -> Dict`
- `setup_aks(cluster_name, kubernetes_version="1.27", node_count=3, vm_size="Standard_D2s_v3", enable_rbac=True, enable_auto_scaling=True, min_count=1, max_count=5, network_plugin="azure", network_policy="calico", location=None, tags=None) -> AKSCluster`

### Storage & Secrets Management
- `create_storage_account(name, sku="Standard_LRS", kind="StorageV2", access_tier="Hot", location=None, enable_https=True, allow_blob_public_access=False, tags=None) -> StorageAccount`
- `create_blob_container(storage_account_name, container_name, public_access="None", metadata=None) -> Dict`
- `create_key_vault(name, sku="standard", enable_purge_protection=False, location=None, tags=None) -> KeyVault`

### Database Management
- `create_sql_server(server_name, administrator_login, administrator_password, location=None, tags=None) -> SqlServer`
- `create_sql_database(name, server_id, sku_name="S0", max_size_bytes=268435456000, zone_redundant=False, tags=None) -> SqlDatabase`
- `create_redis_cache(name, sku="Standard", capacity=1, location=None, tags=None) -> RedisCache`
- `create_cosmos_db_account(account_name, kind="GlobalDocumentDB", consistency_policy="Session", enable_auto_failover=True, location=None, tags=None) -> CosmosDBAccount`

### Security & Access
- `create_system_assigned_identity(name, location=None, tags=None) -> ManagedIdentity`
- `configure_cicd(project, organization="myorg", repository="myrepo", branch="main") -> Dict`

### Reporting & Operations
- `get_status() -> Dict`
- `get_metrics_report() -> Dict`
- `validate_configuration() -> List[Dict[str, Any]]`
- `validate_nsg_rules(nsg_id) -> List[Dict[str, Any]]`
- `estimate_cost(services) -> Dict`
- `optimize_costs() -> Dict`
- `get_account_billing_summary(billing_period="current") -> Dict`
- `overwrite_service_tags(resource_id, new_tags) -> Dict`
- `publish_sql_dacpac(server_id, database_id, dacpac_file_path, connection_string) -> Dict`
- `export_state() -> str`
- `import_state(state_json) -> None`

---

## Usage Patterns

### Pattern 1: Three-Tier Web Application

```python
agent = AzureSpecialistAgent(Config(location="eastus", environment="production"))

# Network
vnet = agent.create_virtual_network("prod-vnet", ["10.0.0.0/16"])
subnet = agent.add_subnet(vnet.id, "web-subnet", "10.0.1.0/24")
nsg = agent.create_network_security_group("web-nsg")
agent.add_nsg_security_rule(nsg.id, "AllowHTTPS", 100, "Inbound", "Allow", "Tcp", "*", "*", "*", "443")

# Compute
avin = agent.create_availability_set("web-avset")
vm = agent.create_vm(
    name="web-vm",
    size="Standard_B2s",
    admin_username="azureuser",
    admin_password="P@ss2024!",
    availability_set_id=avin.id,
    tags={"Env": "prod"}
)
```

### Pattern 2: PaaS Web API with Functions

```python
plan = agent.create_app_service_plan("api-plan", sku_name="P1v2")
func_app = agent.deploy_function_app("api-functions", runtime_stack="python", runtime_version="3.11")
```

### Pattern 3: Container Platform with AKS

```python
aks = agent.setup_aks("prod-aks", node_count=3, enable_auto_scaling=True, min_count=2, max_count=10)
identity = agent.create_system_assigned_identity("aks-identity")
```

### Pattern 4: Data Platform

```python
sql_srv = agent.create_sql_server("dbsrv", "admin", "S3cureP@ss!")
sql_db = agent.create_sql_database("appdb", sql_srv.id, sku_name="S1")
redis = agent.create_redis_cache("appcache")
cosmos = agent.create_cosmos_db_account("appcosmos", kind="MongoDB")
vault = agent.create_key_vault("appvault", sku="premium", enable_purge_protection=True)
```

---

## Data Models

### AzureVM

| Field | Type | Description |
|-------|------|-------------|
| vm_id | str | Unique identifier |
| name | str | VM name |
| size | str | VM size (Standard_B2s) |
| status | str | running, stopped, deallocated |
| os_type | str | Linux or Windows |
| location | str | Azure region |
| resource_group | str | Resource group |
| public_ip | str | Public IP address |
| private_ip | str | Private IP address |
| tags | Dict | Resource tags |

### StorageAccount

| Field | Type | Description |
|-------|------|-------------|
| account_id | str | Unique identifier |
| name | str | Storage account name |
| sku | str | LRS, GRS, ZRS, etc. |
| kind | str | StorageV2, BlobStorage |
| access_tier | str | Hot, Cool, Archive |
| location | str | Azure region |
| primary_location | str | Primary region |
| secondary_location | str | Geo-replication region |

### VirtualNetwork

| Field | Type | Description |
|-------|------|-------------|
| vnet_id | str | Unique identifier |
| name | str | VNet name |
| address_space | List[str] | CIDR ranges |
| location | str | Azure region |
| subnets | List[Subnet] | Associated subnets |
| dns_servers | List[str] | DNS servers |

### SqlDatabase

| Field | Type | Description |
|-------|------|-------------|
| database_id | str | Unique identifier |
| name | str | Database name |
| server_id | str | Parent server |
| sku_name | str | S0, S1, P1, etc. |
| max_size_bytes | int | Maximum size |
| zone_redundant | bool | Zone redundancy |
| status | str | Online, Offline, etc. |

---

## Checklists

### Production Deployment
- [ ] Configure VNet with appropriate subnets
- [ ] Create NSG with required rules
- [ ] Deploy VMs in availability sets
- [ ] Configure load balancer
- [ ] Set up managed identities
- [ ] Configure Key Vault
- [ ] Enable monitoring and diagnostics
- [ ] Configure backup policies
- [ ] Set up cost alerts
- [ ] Document runbooks

### Security Hardening
- [ ] Enable NSG default deny rules
- [ ] Restrict RDP/SSH to specific IPs
- [ ] Enable encryption at rest and in transit
- [ ] Configure managed identities
- [ ] Enable Key Vault soft delete
- [ ] Set up Azure Policy
- [ ] Enable audit logging
- [ ] Configure conditional access
- [ ] Review RBAC assignments
- [ ] Enable threat protection

### Cost Optimization
- [ ] Right-size underutilized VMs
- [ ] Enable auto-shutdown for dev/test
- [ ] Configure storage lifecycle
- [ ] Purchase reserved instances
- [ ] Enable Azure Hybrid Benefit
- [ ] Review idle resources
- [ ] Set up budget alerts
- [ ] Tag resources for allocation

---

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| VM creation fails | Quota exceeded | Request limit increase or choose different size/region |
| Key Vault soft delete missing | Not enabled at creation | Recreate with enable_soft_delete=True |
| AKS provisioning fails | Insufficient subnet IPs | Increase subnet CIDR, free IPs |
| SQL firewall block | Client IP not in rules | Add firewall rule |
| Storage account name collision | Name already taken | Choose alternative name |
| NSG rule not working | Priority conflict | Check rule priority and order |
| Load balancer backend unhealthy | Health probe failing | Verify backend VM health |
| Function app cold start | Consumption plan | Use Premium plan |

---

## Configuration

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

### Configuration Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| subscription_id | "" | Azure subscription ID |
| tenant_id | "" | Azure AD tenant ID |
| resource_group | default | Default resource group |
| location | eastus | Default Azure region |
| default_vm_size | Standard_B1s | Default VM size |
| default_os_type | Linux | Default OS type |
| enable_monitoring | true | Enable metrics collection |
| enable_backup | true | Enable backup |
| backup_retention_days | 30 | Backup retention period |
| max_vms | 50 | VM safety limit |
| environment | development | Environment label |
