# Azure Specialist Agent

Senior cloud engineer agent for designing, provisioning, securing, and operating Microsoft Azure infrastructure with production-grade rigor.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Security](#security)
- [Cost Management](#cost-management)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [License](#license)

## Overview

The Azure Specialist Agent is a production-grade automation framework for Microsoft Azure cloud services. It provisions and manages compute, networking, storage, databases, security, and application platform resources while enforcing Azure Well-Architected Framework principles.

Whether you're setting up a new Azure environment, migrating workloads to the cloud, hardening security posture, or optimizing costs, the Azure Specialist Agent provides the tools to manage your Azure infrastructure efficiently and securely.

## Features

### Compute
- Virtual Machines (B/D/E/F/G/L/N/M series)
- Availability Sets and Zones
- App Service Plans and Functions
- Azure Kubernetes Service (AKS)
- VM Scale Sets

### Storage
- Storage Accounts (LRS/GRS/ZRS)
- Blob Containers with lifecycle management
- Managed Disks (Standard/Premium/Ultra)
- Key Vault for secrets and keys

### Networking
- Virtual Networks with subnets
- Network Security Groups (NSG)
- Load Balancers (Basic/Standard)
- Public IP Addresses
- VPN Gateways

### Databases
- Azure SQL Database
- Cosmos DB (Multi-model)
- Cache for Redis
- PostgreSQL/MySQL/MariaDB

### Security
- Managed Identities
- RBAC (Role-Based Access Control)
- Key Vault integration
- NSG validation
- Azure Policy

### Cost Management
- Cost estimation
- Optimization recommendations
- Budget alerts
- Tag-based allocation

## Quick Start

### Installation

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Basic Usage

```python
from agents.azure_specialist.agent import AzureSpecialistAgent, Config

config = Config(
    subscription_id="00000000-0000-0000-0000-000000000000",
    resource_group="prod-rg",
    location="eastus",
    environment="production",
    tags={"Team": "platform", "CostCenter": "engineering"}
)

agent = AzureSpecialistAgent(config=config)

# Create VNet with subnet and NSG
vnet = agent.create_virtual_network("prod-vnet", ["10.0.0.0/16"])
subnet = agent.add_subnet(vnet.id, "web-subnet", "10.0.1.0/24")
nsg = agent.create_network_security_group("web-nsg")
agent.add_nsg_security_rule(nsg.id, "AllowHTTPS", 100, "Inbound", "Allow", "Tcp", "*", "*", "*", "443")

# Provision VM in availability set
avset = agent.create_availability_set("web-avset")
vm = agent.create_vm(
    name="web-vm",
    size="Standard_B2s",
    admin_username="azureuser",
    admin_password="P@ssw0rd!",
    availability_set_id=avset.id,
    tags={"Role": "frontend"}
)
print(vm.id, vm.status)
```

### Run the Demo

```bash
python agents/azure-specialist/agent.py
```

Exercises networking, VM management, App Service/Functions, AKS, storage, databases, Key Vault, security validation, cost estimation, and state export.

## Usage

### Networking

```python
# Create VNet
vnet = agent.create_virtual_network("prod-vnet", ["10.0.0.0/16"])

# Add subnet with NSG
subnet = agent.add_subnet(vnet.id, "web-subnet", "10.0.1.0/24", network_security_group_id=nsg.id)

# Create NSG with rules
nsg = agent.create_network_security_group("web-nsg")
agent.add_nsg_security_rule(nsg.id, "AllowHTTPS", 100, "Inbound", "Allow", "Tcp", "*", "*", "*", "443")
agent.add_nsg_security_rule(nsg.id, "DenyAll", 65500, "Inbound", "Deny", "*", "*", "*", "*", "*")

# Create load balancer
lb = agent.create_load_balancer("web-lb", sku="Standard")
```

### Compute

```python
# Create VM
vm = agent.create_vm(
    name="web-vm",
    size="Standard_B2s",
    admin_username="azureuser",
    admin_password="P@ssw0rd!",
    os_type="Linux",
    tags={"Role": "frontend"}
)

# Manage VM
agent.start_vm(vm.id)
agent.stop_vm(vm.id)
agent.restart_vm(vm.id)

# Create App Service Plan and Function App
plan = agent.create_app_service_plan("api-plan", sku_name="P1v2")
func_app = agent.deploy_function_app("api-functions", runtime_stack="python", runtime_version="3.11")
```

### Storage & Secrets

```python
# Create storage account
storage = agent.create_storage_account("prodstorage", sku="Standard_GRS")

# Create blob container
container = agent.create_blob_container(storage.name, "backups", public_access="None")

# Create Key Vault
vault = agent.create_key_vault("appvault", sku="premium", enable_purge_protection=True)
```

### Databases

```python
# Create SQL Database
sql_srv = agent.create_sql_server("dbsrv", "admin", "S3cureP@ss!")
sql_db = agent.create_sql_database("appdb", sql_srv.id, sku_name="S1")

# Create Redis Cache
redis = agent.create_redis_cache("appcache", sku="Standard", capacity=1)

# Create Cosmos DB
cosmos = agent.create_cosmos_db_account("appcosmos", kind="GlobalDocumentDB")
```

### Security

```python
# Create managed identity
identity = agent.create_system_assigned_identity("app-identity")

# Validate NSG rules
issues = agent.validate_nsg_rules(nsg.id)

# Configure CI/CD
agent.configure_cicd(project="myapp", organization="myorg", repository="myrepo")
```

### Reporting & Cost Management

```python
# Get status
status = agent.get_status()

# Estimate costs
costs = agent.estimate_cost([{"type": "vm", "size": "Standard_B2s", "hours": 730}])

# Optimize costs
optimization = agent.optimize_costs()

# Get billing summary
billing = agent.get_account_billing_summary()

# Export state
state_json = agent.export_state()
```

## API Reference

### Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `subscription_id` | `str` | `""` | Azure subscription ID |
| `tenant_id` | `str` | `""` | Azure AD tenant ID |
| `resource_group` | `str` | `"default"` | Default resource group |
| `location` | `str` | `"eastus"` | Default Azure region |
| `default_vm_size` | `str` | `"Standard_B1s"` | Default VM size |
| `default_os_type` | `str` | `"Linux"` | Default OS |
| `enable_monitoring` | `bool` | `True` | Enable metrics |
| `enable_backup` | `bool` | `True` | Enable backup |
| `backup_retention_days` | `int` | `30` | Backup retention |
| `max_vms` | `int` | `50` | VM safety limit |
| `environment` | `str` | `"development"` | Environment label |

### Network

```python
agent.create_virtual_network(name, address_space, location=None, dns_servers=None)
agent.add_subnet(vnet_id, name, address_prefix, network_security_group_id=None)
agent.create_network_security_group(name, location=None)
agent.add_nsg_security_rule(nsg_id, name, priority, direction, access, protocol, source_prefix, source_port, dest_prefix, dest_port)
agent.create_public_ip_address(name, sku="Standard", allocation_method="Static")
agent.create_network_interface(name, subnet_id, private_ip_address, public_ip_address_id=None)
agent.create_load_balancer(name, sku="Standard")
agent.configure_vpn_gateway(name, vnet_id, gateway_type="Vpn", sku="VpnGw1")
```

### Compute

```python
agent.create_vm(name, size, admin_username, admin_password=None, ssh_key_data=None, os_type="Linux")
agent.get_vm(vm_id)
agent.list_vms(status_filter=None, resource_group_filter=None)
agent.start_vm(vm_id)
agent.stop_vm(vm_id, deallocate=True)
agent.deallocate_vm(vm_id)
agent.restart_vm(vm_id)
agent.create_availability_set(name, fault_domain_count=2, update_domain_count=5)
agent.create_managed_disk(name, disk_size_gb, sku="Standard_LRS", os_type="Linux")
agent.create_app_service_plan(name, sku_name="B1", capacity=1, os_type="Linux")
agent.deploy_function_app(name, runtime_stack="python", runtime_version="3.11")
agent.create_function(function_app_name, function_name, trigger_type="HTTP")
agent.setup_aks(cluster_name, kubernetes_version="1.27", node_count=3, vm_size="Standard_D2s_v3")
```

### Storage & Secrets

```python
agent.create_storage_account(name, sku="Standard_LRS", kind="StorageV2", access_tier="Hot")
agent.create_blob_container(storage_account_name, container_name, public_access="None")
agent.create_key_vault(name, sku="standard", enable_purge_protection=False)
```

### Database

```python
agent.create_sql_server(server_name, administrator_login, administrator_password)
agent.create_sql_database(name, server_id, sku_name="S0", max_size_bytes=268435456000)
agent.create_redis_cache(name, sku="Standard", capacity=1)
agent.create_cosmos_db_account(account_name, kind="GlobalDocumentDB", consistency_policy="Session")
```

### Security

```python
agent.create_system_assigned_identity(name)
agent.create_key_vault(name, sku="standard", enable_purge_protection=True)
agent.add_nsg_security_rule(nsg_id, name, priority, direction, access, protocol, source, source_port, dest, dest_port)
agent.validate_nsg_rules(nsg_id)
agent.configure_vpn_gateway(name, vnet_id)
```

### CI/CD

```python
agent.configure_cicd(project="myapp", organization="myorg", repository="myrepo", branch="main")
```

### Reporting

```python
agent.get_status()
agent.get_metrics_report()
agent.get_account_billing_summary(billing_period="current")
agent.validate_configuration()
agent.optimize_costs()
agent.export_state()
agent.import_state(state_json)
```

## Examples

### Production Web Application

```python
from agents.azure_specialist.agent import AzureSpecialistAgent, Config

config = Config(
    subscription_id="00000000-0000-0000-0000-000000000000",
    resource_group="prod-web-rg",
    location="eastus",
    environment="production",
)

agent = AzureSpecialistAgent(config=config)

# Networking
vnet = agent.create_virtual_network("prod-vnet", ["10.0.0.0/16"])
web_subnet = agent.add_subnet(vnet.id, "web-subnet", "10.0.1.0/24")
app_subnet = agent.add_subnet(vnet.id, "app-subnet", "10.0.2.0/24")
db_subnet = agent.add_subnet(vnet.id, "db-subnet", "10.0.3.0/24")

# Web tier
web_nsg = agent.create_network_security_group("web-nsg")
agent.add_nsg_security_rule(web_nsg.id, "AllowHTTPS", 100, "Inbound", "Allow", "Tcp", "*", "*", "*", "443")
web_avset = agent.create_availability_set("web-avset")
web_vm = agent.create_vm("web-vm-1", "Standard_B2s", "azureuser", "P@ssw0rd!", availability_set_id=web_avset.id)

# App tier
app_nsg = agent.create_network_security_group("app-nsg")
app_avset = agent.create_availability_set("app-avset")
app_vm = agent.create_vm("app-vm-1", "Standard_D2s_v3", "azureuser", "P@ssw0rd!", availability_set_id=app_avset.id)

# Data tier
sql_srv = agent.create_sql_server("proddbsrv", "sqladmin", "S3cureP@ss!")
sql_db = agent.create_sql_database("proddb", sql_srv.id, sku_name="P1")

# Storage
storage = agent.create_storage_account("prodstorage", sku="Standard_GRS")
vault = agent.create_key_vault("prodvault", sku="premium", enable_purge_protection=True)

# Monitoring
status = agent.get_status()
print(f"Resources: {status['total_resources']}")
```

### AKS Cluster with Monitoring

```python
# Create AKS cluster
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

# Create managed identity for AKS
identity = agent.create_system_assigned_identity("aks-identity")

# Create container registry
# (via Azure CLI or ARM template)

# Configure monitoring
status = agent.get_status()
print(f"AKS Cluster: {aks.cluster_name}")
```

### Cost-Optimized Development Environment

```python
config = Config(
    subscription_id="00000000-0000-0000-0000-000000000000",
    resource_group="dev-rg",
    location="eastus",
    environment="development",
)

agent = AzureSpecialistAgent(config=config)

# Use small VMs
vm = agent.create_vm("dev-vm", "Standard_B1s", "devuser", "DevP@ss123!")

# Use basic storage
storage = agent.create_storage_account("devstorage", sku="Standard_LRS")

# Use basic SQL
sql_srv = agent.create_sql_server("devdbsrv", "sqladmin", "DevP@ss123!")
sql_db = agent.create_sql_database("devdb", sql_srv.id, sku_name="Basic")

# Estimate costs
costs = agent.estimate_cost([
    {"type": "vm", "size": "Standard_B1s", "hours": 730},
    {"type": "storage", "sku": "Standard_LRS", "gb": 50},
    {"type": "sql", "tier": "Basic"},
])
print(f"Estimated monthly cost: ${costs['total_monthly']}")
```

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

## Architecture

For detailed architecture documentation, see [ARCHITECTURE.md](./ARCHITECTURE.md).

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Azure Specialist Agent                      │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│   Compute   │   Storage   │  Network    │    Database      │
│   Manager   │   Manager   │  Manager    │    Manager       │
├─────────────┼─────────────┼─────────────┼──────────────────┤
│ - VM        │ - Storage   │ - VNet      │ - SQL DB         │
│ - AKS       │ - Blob      │ - NSG       │ - Cosmos DB      │
│ - Functions │ - Disk      │ - LB        │ - Redis          │
│ - App Svc   │ - Key Vault │ - VPN       │ - PostgreSQL     │
├─────────────┴─────────────┴─────────────┴──────────────────┤
│                  Security & Identity Layer                  │
│  - Managed Identities  - RBAC  - Azure Policy  - Key Vault │
├─────────────────────────────────────────────────────────────┤
│                  Observability Layer                         │
│  - Azure Monitor  - Log Analytics  - App Insights          │
├─────────────────────────────────────────────────────────────┤
│                  Cost Management Layer                       │
│  - Estimation  - Optimization  - Budgets  - Tags            │
└─────────────────────────────────────────────────────────────┘
```

## Security

- **Managed Identities**: Eliminate credentials for Azure services
- **NSG Hardening**: Deny rules for RDP/SSH from internet by default
- **Key Vault**: Soft delete and purge protection for secrets durability
- **Encryption**: Platform-managed encryption by default; use Key Vault keys for compliance
- **RBAC**: Least privilege; use built-in roles over custom where possible
- **Azure Policy**: Enforce compliance at scale
- **Audit Logging**: All operations logged

## Cost Management

- `estimate_cost(services)` returns hourly/monthly estimates for known SKUs
- `optimize_costs()` identifies stopped VMs, oversize instances, and free-tier missed opportunities
- `get_account_billing_summary()` estimates monthly spend by resource category
- Tag all resources with `Environment`, `Team`, `Project`, and `ManagedBy` for cost allocation

### Cost Optimization Strategies

| Strategy | Description | Savings |
|----------|-------------|---------|
| Reserved Instances | 1-3 year commitment | 30-60% |
| Dev/Test Pricing | Non-production | 50-75% |
| Auto-Shutdown | Stop non-prod VMs | 100% (off-hours) |
| Right-Sizing | Match VM to workload | 20-50% |
| Storage Tiering | Hot → Cool → Archive | 50-80% |

## Best Practices

### Security
1. Use managed identities instead of service principals
2. Enable soft delete and purge protection for Key Vault
3. Enforce NSG rules with least privilege
4. Encrypt data at rest and in transit
5. Enable Azure AD authentication for SQL

### Reliability
6. Deploy VMs in availability sets (2+ fault domains)
7. Use zone-redundant storage for production
8. Implement health probes and load balancer rules
9. Enable auto-backup for VMs
10. Use geo-redundant storage for critical data

### Performance
11. Select VM sizes based on workload
12. Use Premium SSD for I/O-intensive databases
13. Enable accelerated networking
14. Use Azure Cache for Redis to offload reads

### Cost
15. Use dev/test pricing where possible
16. Implement auto-shutdown for non-production
17. Use reserved instances for steady-state workloads
18. Configure lifecycle management for blob storage
19. Right-size underutilized VMs

### Operations
20. Use ARM templates or Terraform for IaC
21. Tag all resources for cost allocation
22. Implement CI/CD pipelines
23. Use deployment slots for zero-downtime deployments
24. Document runbooks for common operations

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| VM creation fails | Quota exceeded | Request quota increase or choose different size/region |
| Key Vault soft delete missing | Not enabled at creation | Recreate with enable_soft_delete=True |
| AKS provisioning fails | Insufficient subnet IPs | Increase subnet CIDR, free IPs |
| SQL firewall block | Client IP not in rules | Add firewall rule or enable Azure services |
| Storage account name collision | Globally unique name taken | Pick another 3-24 char lowercase name |
| NSG rule not working | Priority conflict | Check rule priority and order |
| Load balancer backend unhealthy | Health probe failing | Verify backend VM health |
| Function app cold start | Consumption plan | Use Premium plan for no cold start |

## FAQ

**Q: How does the agent handle Azure authentication?**
A: The agent supports managed identities, service principals, and Azure CLI credentials. Managed identities are recommended for production workloads.

**Q: Can I use the agent with multiple subscriptions?**
A: Yes. Configure the subscription_id per agent instance or use the import_state/export_state features to manage multiple environments.

**Q: How does cost estimation work?**
A: The agent uses Azure retail pricing APIs to calculate hourly and monthly costs based on SKU, region, and usage patterns.

**Q: What happens if a provisioning operation fails?**
A: The agent logs the error, updates state, and returns error details. You can retry the operation or use export_state to recover.

**Q: Can I customize NSG rules?**
A: Yes. The agent supports custom NSG rules with configurable priority, direction, access, protocol, and address prefixes.

**Q: How do I migrate existing Azure resources?**
A: Use the export_state feature to capture existing resource state, then manage them through the agent going forward.

## License

MIT License - see LICENSE file for details.
