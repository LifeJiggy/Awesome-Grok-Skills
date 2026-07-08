# Azure Specialist Agent

Senior cloud engineer agent for designing, provisioning, securing, and operating Microsoft Azure infrastructure with production-grade rigor.

## Quick Start

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

## Running the Demo

```bash
python agents/azure-specialist/agent.py
```

Exercises networking, VM management, App Service/Functions, AKS, storage, databases, Key Vault, security validation, cost estimation, and state export.

## Capabilities

| Domain | Key Capabilities |
|--------|------------------|
| **Compute** | VMs (B/D/E/F/G/L/N/M), Availability Sets, App Service Plans, Functions, AKS |
| **Storage** | Storage Accounts (LRS/GRS/ZRS), Blob Containers, Managed Disks, Key Vault |
| **Networking** | VNet/Subnet, NSG, Public IP, NIC, Load Balancer, VPN Gateway |
| **Databases** | SQL Database, Cosmos DB, Redis Cache |
| **Security** | Managed Identities, RBAC, NSG validation, Key Vault encryption |
| **DevOps** | Azure DevOps CI/CD configuration, resource tagging |
| **Monitoring** | Metrics collection, operation history, cost estimation, optimization |

## Core API Reference

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

## Security & Compliance

- **Managed Identities**: Eliminate credentials for Azure services.
- **NSG Hardening**: Deny rules for RDP/SSH from internet by default.
- **Key Vault**: Soft delete and purge protection for secrets durability.
- **Encryption**: Platform-managed encryption by default; use Key Vault keys for compliance.
- **RBAC**: Least privilege; use built-in roles over custom where possible.

## Cost Management

- `estimate_cost(services)` returns hourly/monthly estimates for known SKUs.
- `optimize_costs()` identifies stopped VMs, oversize instances, and free-tier missed opportunities.
- `get_account_billing_summary()` estimates monthly spend by resource category.
- Tag all resources with `Environment`, `Team`, `Project`, and `ManagedBy` for cost allocation.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| `QuotaExceeded` | Subscription VM quota reached | Request quota increase or scale down |
| `SKUNotAvailable` | VM size unavailable in region | Choose alternative size or location |
| `Storage account name collision` | Globally unique name taken | Pick another 3-24 char lowercase name |
| `AKS provisioning fails` | Insufficient subnet IPs | Enlarge subnet or clean up IPs |
| `Key Vault firewall block` | Network rules restrict access | Allow trusted Azure services or specific IPs |

## State Management

```python
state_json = agent.export_state()
with open("azure-state.json", "w") as f:
    f.write(state_json)

# Later or in another session
with open("azure-state.json") as f:
    agent.import_state(f.read())
```

## File Structure

```
agents/azure-specialist/
  agent.py           # Main implementation (~1500+ lines)
  ARCHITECTURE.md    # System design reference
  GROK.md            # Agent prompt and API docs
  README.md          # Usage guide and quick reference
```

## License

Internal use: Awesome-Grok-Skills project.
