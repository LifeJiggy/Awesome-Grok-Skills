"""Azure Specialist Agent - Microsoft Cloud Services and Architecture."""

from __future__ import annotations

import logging
import time
import json
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union, Tuple
from enum import Enum
from datetime import datetime, timedelta
import uuid
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("azure-specialist-agent")


class VMSize(Enum):
    B1S = "Standard_B1s"
    B2S = "Standard_B2s"
    D2S_V3 = "Standard_D2s_v3"
    D4S_V3 = "Standard_D4s_v3"
    E2S_V3 = "Standard_E2s_v3"
    F4S_V2 = "Standard_F4s_v2"
    G1S = "Standard_G1s"
    L4S = "Standard_L4s"
    NC6 = "Standard_NC6"
    NC12 = "Standard_NC12"


class VMStatus(Enum):
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    DEALLOCATED = "deallocated"
    FAILED = "failed"


class OSType(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"


class StorageSKU(Enum):
    STANDARD_LRS = "Standard_LRS"
    STANDARD_GRS = "Standard_GRS"
    STANDARD_RAGRS = "Standard_RAGRS"
    STANDARD_ZRS = "Standard_ZRS"
    PREMIUM_LRS = "Premium_LRS"
    PREMIUM_ZRS = "Premium_ZRS"


class BackupFrequency(Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"


class BackupRetention(Enum):
    SHORT = 7
    MEDIUM = 30
    LONG = 365


class NetworkingTier(Enum):
    BASIC = "Basic"
    STANDARD = "Standard"


class LoadBalancerSku(Enum):
    BASIC = "Basic"
    STANDARD = "Standard"


class SKUName(Enum):
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM = "Premium"


class MetricUnit(Enum):
    COUNT = "Count"
    PERCENT = "Percent"
    BYTES = "Bytes"
    SECONDS = "Seconds"
    MILLISECONDS = "Milliseconds"


class AggregationType(Enum):
    AVERAGE = "Average"
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    TOTAL = "Total"
    COUNT = "Count"


class AlertSeverity(Enum):
    SEV0 = 0
    SEV1 = 1
    SEV2 = 2
    SEV3 = 3
    SEV4 = 4


class PricingTier(Enum):
    FREE = "Free"
    STANDARD = "Standard"
    PREMIUM = "Premium"


class DatabaseSKU(Enum):
    BASIC = "Basic"
    S0 = "S0"
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    P1 = "P1"
    P2 = "P2"
    P4 = "P4"
    P6 = "P6"
    P11 = "P11"
    P15 = "P15"
    GP_GEN5_2 = "GP_Gen5_2"
    GP_GEN5_4 = "GP_Gen5_4"
    BC_GEN5_2 = "BC_Gen5_2"
    M_GEN5_2 = "M_Gen5_2"


class CacheSKU(Enum):
    BASIC_C = "Basic_C"
    STANDARD_C = "Standard_C"
    PREMIUM_C = "Premium_C"
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM = "Premium"


class KeyVaultSKU(Enum):
    STANDARD = "standard"
    PREMIUM = "premium"


class KubernetesVersion(Enum):
    V1_24 = "1.24"
    V1_25 = "1.25"
    V1_26 = "1.26"
    V1_27 = "1.27"


class managedIdentityType(Enum):
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"


class RoleType(Enum):
    CONTRIBUTOR = "Contributor"
    READER = "Reader"
    OWNER = "Owner"
    VIRTUAL_MACHINE_ADMINISTRATOR_LOGIN = "Virtual Machine Administrator Login"


@dataclass
class Metric:
    name: str
    value: Any
    unit: str = "count"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    dimensions: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    def __init__(self) -> None:
        self._metrics: List[Metric] = []

    def record(self, name: str, value: Any, unit: str = "count", **dimensions: str) -> None:
        metric = Metric(name=name, value=value, unit=unit, dimensions=dimensions)
        self._metrics.append(metric)
        logger.info(f"Metric recorded: {name}={value} {unit}")

    def get_metrics(self, name: Optional[str] = None) -> List[Metric]:
        if name:
            return [m for m in self._metrics if m.name == name]
        return list(self._metrics)

    def clear(self) -> None:
        self._metrics.clear()


@dataclass
class Config:
    subscription_id: str = ""
    tenant_id: str = ""
    resource_group: str = "default"
    location: str = "eastus"
    default_vm_size: str = "Standard_B1s"
    default_os_type: str = "Linux"
    enable_monitoring: bool = True
    enable_backup: bool = True
    backup_retention_days: int = 30
    tags: Dict[str, str] = field(default_factory=dict)
    max_vms: int = 50
    environment: str = "development"
    encryption_key_id: Optional[str] = None
    location_secondary: str = "westus2"


@dataclass
class Subnet:
    id: str
    name: str
    address_prefix: str
    vnet_id: str
    network_security_group_id: Optional[str] = None
    route_table_id: Optional[str] = None
    service_endpoints: List[str] = field(default_factory=list)
    delegations: List[str] = field(default_factory=list)


@dataclass
class NetworkSecurityGroup:
    id: str
    name: str
    location: str
    security_rules: List[Dict[str, Any]] = field(default_factory=list)
    default_security_rules: List[Dict[str, Any]] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class PublicIPAddress:
    id: str
    name: str
    ip_address: str
    location: str
    sku: str = "Standard"
    allocation_method: str = "Static"
    domain_name_label: str = ""


@dataclass
class NetworkInterface:
    id: str
    name: str
    subnet_id: str
    private_ip_address: str
    public_ip_address_id: Optional[str] = None
    network_security_group_id: Optional[str] = None
    ip_configurations: List[Dict[str, Any]] = field(default_factory=list)
    enable_accelerated_networking: bool = False
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class VirtualNetwork:
    id: str
    name: str
    address_space: List[str]
    location: str
    subnets: List[Subnet] = field(default_factory=list)
    dns_servers: List[str] = field(default_factory=list)
    enable_ddos_protection: bool = False
    enable_vm_protection: bool = False
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AzureVM:
    id: str
    name: str
    size: str
    os_type: str
    status: str
    location: str
    resource_group: str
    admin_username: str = "azureuser"
    vm_id: str = ""
    private_ip_address: Optional[str] = None
    public_ip_address: Optional[str] = None
    network_interface_ids: List[str] = field(default_factory=list)
    disk_ids: List[str] = field(default_factory=list)
    image_reference: Dict[str, str] = field(default_factory=dict)
    availability_set_id: Optional[str] = None
    proximity_placement_group_id: Optional[str] = None
    host_group_id: Optional[str] = None
    zones: List[str] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    plan: Optional[Dict[str, str]] = None
    encryption_at_host: bool = True
    user_data: Optional[str] = None
    boot_diagnostics_enabled: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Disk:
    id: str
    name: str
    disk_size_gb: int
    sku: str
    location: str
    resource_group: str
    managed: bool = True
    os_type: str = "Linux"
    creation_data: Dict[str, str] = field(default_factory=dict)
    disk_iops_read_write: int = 0
    disk_mbps_read_write: int = 0
    encryption_type: str = "EncryptionAtRestWithPlatformKey"
    max_shares: int = 1
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class LoadBalancer:
    id: str
    name: str
    location: str
    resource_group: str
    sku: str
    backend_address_pools: List[str] = field(default_factory=list)
    frontend_ip_configurations: List[Dict[str, Any]] = field(default_factory=list)
    load_balancing_rules: List[Dict[str, Any]] = field(default_factory=list)
    inbound_nat_pools: List[Dict[str, Any]] = field(default_factory=list)
    probes: List[Dict[str, Any]] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AvailabilitySet:
    id: str
    name: str
    location: str
    resource_group: str
    platform_fault_domain_count: int = 2
    platform_update_domain_count: int = 5
    proximity_placement_group_id: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class AKSCluster:
    id: str
    name: str
    location: str
    resource_group: str
    kubernetes_version: str
    dns_prefix: str
    fqdn: str
    node_resource_group: str
    enable_rbac: bool = True
    enable_auto_scaling: bool = False
    min_count: int = 1
    max_count: int = 5
    network_plugin: str = "azure"
    network_policy: str = "calico"
    managed_identity: Dict[str, Any] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class FunctionApp:
    id: str
    name: str
    location: str
    resource_group: str
    runtime_stack: str
    runtime_version: str
    default_host_name: str
    outbound_ip_addresses: List[str] = field(default_factory=list)
    https_only: bool = True
    functions: List[str] = field(default_factory=list)
    app_settings: Dict[str, str] = field(default_factory=dict)
    connection_strings: List[Dict[str, str]] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class StorageAccount:
    id: str
    name: str
    location: str
    resource_group: str
    sku: str
    kind: str
    access_tier: str
    enable_https_traffic_only: bool = True
    allow_blob_public_access: bool = False
    enable_encryption: bool = True
    encryption_key_source: str = "Microsoft.Storage"
    network_rule_set: Dict[str, Any] = field(default_factory=dict)
    containers: List[str] = field(default_factory=list)
    queues: List[str] = field(default_factory=list)
    file_shares: List[str] = field(default_factory=list)
    tables: List[str] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class KeyVault:
    id: str
    name: str
    location: str
    resource_group: str
    vault_uri: str
    tenant_id: str
    sku: str
    enable_soft_delete: bool = True
    enable_purge_protection: bool = False
    enable_rbac_authorization: bool = True
    access_policies: List[Dict[str, Any]] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    keys: List[str] = field(default_factory=list)
    certificates: List[str] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CosmosDBAccount:
    id: str
    name: str
    location: str
    resource_group: str
    kind: str
    consistency_policy: str = "Session"
    enable_automatic_failover: bool = True
    enable_multiple_write_locations: bool = False
    databases: List[str] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SqlServer:
    id: str
    name: str
    location: str
    resource_group: str
    administrator_login: str
    fully_qualified_domain_name: str
    version: str = "12.0"
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SqlDatabase:
    id: str
    name: str
    server_id: str
    location: str
    resource_group: str
    sku_name: str
    max_size_bytes: int = 268435456000
    collation: str = "SQL_Latin1_General_CP1_CI_AS"
    zone_redundant: bool = False
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class RedisCache:
    id: str
    name: str
    location: str
    resource_group: str
    sku: str
    capacity: int
    enable_non_ssl_port: bool = False
    enable_authentication: bool = True
    redis_version: str = "6.0"
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ManagedIdentity:
    id: str
    name: str
    principal_id: str
    tenant_id: str
    type: str
    location: str = "eastus"
    client_id: str = ""
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class AppServicePlan:
    id: str
    name: str
    location: str
    resource_group: str
    sku_name: str
    capacity: int = 1
    os_type: str = "Linux"
    per_site_scaling: bool = False
    tags: Dict[str, str] = field(default_factory=dict)


class ValidationError(Exception):
    pass


class ResourceConflictError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


class AzureServiceError(Exception):
    pass


class AzureSpecialistAgent:
    """Agent for Microsoft Azure cloud services with comprehensive management."""

    def __init__(self, config: Optional[Config] = None, metrics_collector: Optional[MetricsCollector] = None) -> None:
        self._config = config or Config()
        self._metrics = metrics_collector or MetricsCollector()
        self._vms: Dict[str, AzureVM] = {}
        self._vnets: Dict[str, VirtualNetwork] = {}
        self._subnets: Dict[str, Subnet] = {}
        self._nsgs: Dict[str, NetworkSecurityGroup] = {}
        self._public_ips: Dict[str, PublicIPAddress] = {}
        self._network_interfaces: Dict[str, NetworkInterface] = {}
        self._disks: Dict[str, Disk] = {}
        self._load_balancers: Dict[str, LoadBalancer] = {}
        self._availability_sets: Dict[str, AvailabilitySet] = {}
        self._aks_clusters: Dict[str, AKSCluster] = {}
        self._function_apps: Dict[str, FunctionApp] = {}
        self._storage_accounts: Dict[str, StorageAccount] = {}
        self._key_vaults: Dict[str, KeyVault] = {}
        self._cosmos_db_accounts: Dict[str, CosmosDBAccount] = {}
        self._sql_servers: Dict[str, SqlServer] = {}
        self._sql_databases: Dict[str, SqlDatabase] = {}
        self._redis_caches: Dict[str, RedisCache] = {}
        self._managed_identities: Dict[str, ManagedIdentity] = {}
        self._app_service_plans: Dict[str, AppServicePlan] = {}
        self._role_assignments: Dict[str, Dict[str, Any]] = {}
        self._operation_history: List[Dict[str, Any]] = []
        self._start_time = datetime.utcnow()

        logger.info(f"Initialized AzureSpecialistAgent in subscription={self._config.subscription_id}, location={self._config.location}")

    def _log_operation(self, operation: str, details: Dict[str, Any], status: str = "success") -> None:
        entry = {
            "operation": operation,
            "details": details,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._operation_history.append(entry)
        self._metrics.record("azure_operation", 1, operation=operation, status=status)

    def _generate_id(self, prefix: str) -> str:
        return f"{prefix}-{uuid.uuid4().hex[:12]}"

    def _validate_location(self, location: str) -> str:
        valid_locations = [
            "eastus", "eastus2", "westus", "westus2", "westus3",
            "centralus", "northcentralus", "southcentralus",
            "northeurope", "westeurope", "uksouth", "ukwest",
            "francecentral", "germanywestcentral", "switzerlandnorth",
            "norwayeast", "eastasia", "southeastasia", "japaneast", "australiaeast", "australiasoutheast"
        ]
        if location not in valid_locations:
            raise ValidationError(f"Invalid Azure region: {location}. Valid: {valid_locations}")
        return location

    def _validate_vm_size(self, size: str) -> str:
        valid_sizes = [s.value for s in VMSize]
        if size not in valid_sizes:
            raise ValidationError(f"Invalid VM size: {size}. Valid: {valid_sizes}")
        return size

    def _validate_dns_name(self, name: str) -> str:
        pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$"
        if not re.match(pattern, name):
            raise ValidationError(f"Invalid DNS name: {name}. Must be alphanumeric and hyphens, start/end with alphanumeric.")
        if len(name) < 2 or len(name) > 63:
            raise ValidationError(f"DNS name must be 2-63 characters: {name}")
        return name.lower()

    def _validate_storage_account_name(self, name: str) -> str:
        pattern = r"^[a-z0-9]{3,24}$"
        if not re.match(pattern, name):
            raise ValidationError(f"Invalid storage account name: {name}. Must be 3-24 lowercase alphanumeric.")
        return name.lower()

    def create_virtual_network(self, name: str, address_space: List[str], location: Optional[str] = None,
                                dns_servers: Optional[List[str]] = None, tags: Optional[Dict[str, str]] = None) -> VirtualNetwork:
        location = location or self._config.location
        self._validate_location(location)
        vnet = VirtualNetwork(
            id=self._generate_id("vnet"),
            name=name,
            address_space=address_space,
            location=location,
            dns_servers=dns_servers or [],
            tags={**self._config.tags, **(tags or {})}
        )
        self._vnets[vnet.id] = vnet
        logger.info(f"Created virtual network: {vnet.id} ({name})")
        self._log_operation("network.vnet.create", {"vnet_id": vnet.id, "name": name})
        return vnet

    def add_subnet(self, vnet_id: str, name: str, address_prefix: str,
                   network_security_group_id: Optional[str] = None,
                   route_table_id: Optional[str] = None,
                   service_endpoints: Optional[List[str]] = None,
                   delegations: Optional[List[str]] = None) -> Subnet:
        vnet = self._vnets.get(vnet_id)
        if not vnet:
            raise ResourceNotFoundError(f"Virtual network not found: {vnet_id}")
        subnet = Subnet(
            id=self._generate_id("subnet"),
            name=name,
            address_prefix=address_prefix,
            vnet_id=vnet_id,
            network_security_group_id=network_security_group_id,
            route_table_id=route_table_id,
            service_endpoints=service_endpoints or [],
            delegations=delegations or []
        )
        self._subnets[subnet.id] = subnet
        vnet.subnets.append(subnet)
        logger.info(f"Added subnet {subnet.id} ({name}) to VNet {vnet_id}")
        self._log_operation("network.subnet.create", {"subnet_id": subnet.id, "vnet_id": vnet_id})
        return subnet

    def create_network_security_group(self, name: str, location: Optional[str] = None,
                                      tags: Optional[Dict[str, str]] = None) -> NetworkSecurityGroup:
        location = location or self._config.location
        self._validate_location(location)
        nsg = NetworkSecurityGroup(
            id=self._generate_id("nsg"),
            name=name,
            location=location,
            security_rules=[],
            tags={**self._config.tags, **(tags or {})}
        )
        self._nsgs[nsg.id] = nsg
        logger.info(f"Created network security group: {nsg.id} ({name})")
        self._log_operation("network.nsg.create", {"nsg_id": nsg.id, "name": name})
        return nsg

    def add_nsg_security_rule(self, nsg_id: str, name: str, priority: int, direction: str,
                              access: str, protocol: str, source_address_prefix: str,
                              source_port_range: str, destination_address_prefix: str,
                              destination_port_range: str, description: str = "") -> Dict[str, Any]:
        nsg = self._nsgs.get(nsg_id)
        if not nsg:
            raise ResourceNotFoundError(f"NSG not found: {nsg_id}")
        if priority < 100 or priority > 4096:
            raise ValidationError(f"Priority must be 100-4096: {priority}")
        if direction not in ["Inbound", "Outbound"]:
            raise ValidationError(f"Direction must be 'Inbound' or 'Outbound': {direction}")
        if access not in ["Allow", "Deny"]:
            raise ValidationError(f"Access must be 'Allow' or 'Deny': {access}")
        rule = {
            "name": name,
            "priority": priority,
            "direction": direction,
            "access": access,
            "protocol": protocol,
            "source_address_prefix": source_address_prefix,
            "source_port_range": source_port_range,
            "destination_address_prefix": destination_address_prefix,
            "destination_port_range": destination_port_range,
            "description": description
        }
        nsg.security_rules.append(rule)
        logger.info(f"Added NSG rule '{name}' (priority {priority}) to {nsg_id}")
        self._log_operation("network.nsg.add_rule", {"nsg_id": nsg_id, "rule_name": name, "priority": priority})
        return {"nsg_id": nsg_id, "rule": rule}

    def create_public_ip_address(self, name: str, sku: str = "Standard",
                                 allocation_method: str = "Static",
                                 location: Optional[str] = None,
                                 tags: Optional[Dict[str, str]] = None) -> PublicIPAddress:
        location = location or self._config.location
        self._validate_location(location)
        self._validate_dns_name(name)
        pip = PublicIPAddress(
            id=self._generate_id("pip"),
            name=name,
            ip_address="",
            location=location,
            sku=sku,
            allocation_method=allocation_method,
            domain_name_label=f"{name.lower()}-{uuid.uuid4().hex[:6]}"
        )
        self._public_ips[pip.id] = pip
        logger.info(f"Created public IP: {pip.id} ({name})")
        self._log_operation("network.pip.create", {"pip_id": pip.id, "name": name})
        return pip

    def create_network_interface(self, name: str, subnet_id: str, private_ip_address: str,
                                  public_ip_address_id: Optional[str] = None,
                                  network_security_group_id: Optional[str] = None,
                                  enable_accelerated_networking: bool = False,
                                  location: Optional[str] = None,
                                  tags: Optional[Dict[str, str]] = None) -> NetworkInterface:
        location = location or self._config.location
        subnet = self._subnets.get(subnet_id)
        if not subnet:
            raise ResourceNotFoundError(f"Subnet not found: {subnet_id}")
        nic = NetworkInterface(
            id=self._generate_id("nic"),
            name=name,
            subnet_id=subnet_id,
            private_ip_address=private_ip_address,
            public_ip_address_id=public_ip_address_id,
            network_security_group_id=network_security_group_id,
            enable_accelerated_networking=enable_accelerated_networking,
            tags={**self._config.tags, **(tags or {})}
        )
        self._network_interfaces[nic.id] = nic
        logger.info(f"Created network interface: {nic.id} ({name})")
        self._log_operation("network.nic.create", {"nic_id": nic.id, "name": name})
        return nic

    def create_vm(self, name: str, size: str, admin_username: str = "azureuser",
                  admin_password: Optional[str] = None, ssh_key_data: Optional[str] = None,
                  os_type: str = "Linux", image_reference: Optional[Dict[str, str]] = None,
                  network_interface_ids: Optional[List[str]] = None,
                  availability_set_id: Optional[str] = None,
                  disk_ids: Optional[List[str]] = None,
                  zones: Optional[List[str]] = None,
                  tags: Optional[Dict[str, str]] = None,
                  enable_boot_diagnostics: bool = True,
                  encryption_at_host: bool = True) -> AzureVM:
        start = time.time()
        try:
            if len(self._vms) >= self._config.max_vms:
                raise ResourceConflictError(f"Maximum VM limit reached: {self._config.max_vms}")
            size = self._validate_vm_size(size)
            self._validate_location(self._config.location)
            if not admin_password and not ssh_key_data:
                raise ValidationError("Either admin_password or ssh_key_data must be provided")
            vm = AzureVM(
                id=self._generate_id("vm"),
                name=name,
                size=size,
                os_type=os_type,
                status=VMStatus.DEALLOCATED.value,
                location=self._config.location,
                resource_group=self._config.resource_group,
                admin_username=admin_username,
                network_interface_ids=network_interface_ids or [],
                disk_ids=disk_ids or [],
                image_reference=image_reference or {"publisher": "Canonical", "offer": "UbuntuServer", "sku": "18.04-LTS", "version": "latest"},
                availability_set_id=availability_set_id,
                zones=zones or [],
                tags={**self._config.tags, **(tags or {})},
                boot_diagnostics_enabled=enable_boot_diagnostics,
                encryption_at_host=encryption_at_host
            )
            self._vms[vm.id] = vm
            logger.info(f"Created VM {vm.id} ({name}) size={size} os={os_type}")
            self._log_operation("compute.vm.create", {"vm_id": vm.id, "name": name, "size": size, "os": os_type})
            latency = (time.time() - start) * 1000
            self._metrics.record("provision_latency_ms", round(latency, 2), operation="compute.vm.create")
            return vm
        except ValidationError:
            raise
        except ResourceNotFoundError:
            raise
        except Exception as e:
            self._log_operation("compute.vm.create", {"name": name}, status="error")
            logger.error(f"Failed to create VM: {e}")
            raise AzureServiceError(f"VM creation failed: {e}")

    def get_vm(self, vm_id: str) -> AzureVM:
        if vm_id not in self._vms:
            raise ResourceNotFoundError(f"VM not found: {vm_id}")
        return self._vms[vm_id]

    def list_vms(self, status_filter: Optional[str] = None, resource_group_filter: Optional[str] = None) -> List[AzureVM]:
        vms = list(self._vms.values())
        if status_filter:
            vms = [v for v in vms if v.status == status_filter]
        if resource_group_filter:
            vms = [v for v in vms if v.resource_group == resource_group_filter]
        return vms

    def start_vm(self, vm_id: str) -> Dict[str, Any]:
        start = time.time()
        try:
            vm = self.get_vm(vm_id)
            if vm.status not in [VMStatus.STOPPED.value, VMStatus.DEALLOCATED.value]:
                raise ValidationError(f"Cannot start VM in state: {vm.status}")
            vm.status = VMStatus.STARTING.value
            logger.info(f"Starting VM {vm_id}")
            self._log_operation("compute.vm.start", {"vm_id": vm_id})
            return {"vm_id": vm_id, "status": vm.status}
        except ResourceNotFoundError:
            raise
        except ValidationError:
            raise
        except Exception as e:
            self._log_operation("compute.vm.start", {"vm_id": vm_id}, status="error")
            logger.error(f"Failed to start VM: {e}")
            raise AzureServiceError(f"VM start failed: {e}")

    def stop_vm(self, vm_id: str, deallocate: bool = True) -> Dict[str, Any]:
        start = time.time()
        try:
            vm = self.get_vm(vm_id)
            if vm.status not in [VMStatus.RUNNING.value, VMStatus.STARTING.value]:
                raise ValidationError(f"Cannot stop VM in state: {vm.status}")
            vm.status = VMStatus.STOPPING.value
            logger.info(f"Stopping VM {vm_id} (deallocate={deallocate})")
            self._log_operation("compute.vm.stop", {"vm_id": vm_id, "deallocate": deallocate})
            return {"vm_id": vm_id, "status": vm.status, "deallocate": deallocate}
        except ResourceNotFoundError:
            raise
        except ValidationError:
            raise
        except Exception as e:
            self._log_operation("compute.vm.stop", {"vm_id": vm_id}, status="error")
            logger.error(f"Failed to stop VM: {e}")
            raise AzureServiceError(f"VM stop failed: {e}")

    def deallocate_vm(self, vm_id: str) -> Dict[str, Any]:
        vm = self.get_vm(vm_id)
        vm.status = VMStatus.DEALLOCATED.value
        logger.info(f"Deallocated VM {vm_id}")
        self._log_operation("compute.vm.deallocate", {"vm_id": vm_id})
        return {"vm_id": vm_id, "status": vm.status}

    def restart_vm(self, vm_id: str) -> Dict[str, Any]:
        vm = self.get_vm(vm_id)
        vm.status = VMStatus.STARTING.value
        logger.info(f"Restarting VM {vm_id}")
        self._log_operation("compute.vm.restart", {"vm_id": vm_id})
        return {"vm_id": vm_id, "status": vm.status}

    def create_availability_set(self, name: str, location: Optional[str] = None,
                                fault_domain_count: int = 2, update_domain_count: int = 5,
                                tags: Optional[Dict[str, str]] = None) -> AvailabilitySet:
        location = location or self._config.location
        self._validate_location(location)
        aset = AvailabilitySet(
            id=self._generate_id("avset"),
            name=name,
            location=location,
            resource_group=self._config.resource_group,
            platform_fault_domain_count=fault_domain_count,
            platform_update_domain_count=update_domain_count,
            tags={**self._config.tags, **(tags or {})}
        )
        self._availability_sets[aset.id] = aset
        logger.info(f"Created availability set: {aset.id} ({name})")
        self._log_operation("compute.avset.create", {"avset_id": aset.id, "name": name})
        return aset

    def create_managed_disk(self, name: str, disk_size_gb: int, sku: str = "Standard_LRS",
                            location: Optional[str] = None, os_type: str = "Linux",
                            tags: Optional[Dict[str, str]] = None) -> Disk:
        location = location or self._config.location
        if disk_size_gb < 4 or disk_size_gb > 32768:
            raise ValidationError(f"Disk size must be 4-32768 GB: {disk_size_gb}")
        disk = Disk(
            id=self._generate_id("disk"),
            name=name,
            disk_size_gb=disk_size_gb,
            sku=sku,
            location=location,
            resource_group=self._config.resource_group,
            os_type=os_type,
            tags={**self._config.tags, **(tags or {})}
        )
        self._disks[disk.id] = disk
        logger.info(f"Created managed disk: {disk.id} ({name}) size={disk_size_gb}GB sku={sku}")
        self._log_operation("compute.disk.create", {"disk_id": disk.id, "disk_size_gb": disk_size_gb, "sku": sku})
        return disk

    def create_app_service_plan(self, name: str, sku_name: str = "B1", capacity: int = 1,
                                location: Optional[str] = None, os_type: str = "Linux",
                                tags: Optional[Dict[str, str]] = None) -> AppServicePlan:
        location = location or self._config.location
        plan = AppServicePlan(
            id=self._generate_id("plan"),
            name=name,
            location=location,
            resource_group=self._config.resource_group,
            sku_name=sku_name,
            capacity=capacity,
            os_type=os_type,
            tags={**self._config.tags, **(tags or {})}
        )
        self._app_service_plans[plan.id] = plan
        logger.info(f"Created App Service plan: {plan.id} ({name}) sku={sku_name}")
        self._log_operation("compute.appservice.create_plan", {"plan_id": plan.id, "name": name, "sku": sku_name})
        return plan

    def deploy_function_app(self, name: str, runtime_stack: str = "python", runtime_version: str = "3.11",
                            app_service_plan_id: Optional[str] = None, storage_account_name: str = "",
                            app_settings: Optional[Dict[str, str]] = None,
                            connection_strings: Optional[List[Dict[str, str]]] = None) -> FunctionApp:
        host_name = f"{name}.azurewebsites.net"
        func = FunctionApp(
            id=self._generate_id("funcapp"),
            name=name,
            location=self._config.location,
            resource_group=self._config.resource_group,
            runtime_stack=runtime_stack,
            runtime_version=runtime_version,
            default_host_name=host_name,
            outbound_ip_addresses=[f"20.0.0.{uuid.uuid4().hex[:2]}"],
            https_only=True,
            app_settings=app_settings or {"FUNCTIONS_WORKER_RUNTIME": runtime_stack, "WEBSITE_RUN_FROM_PACKAGE": "1"},
            connection_strings=connection_strings or [],
            tags=self._config.tags.copy()
        )
        self._function_apps[name] = func
        logger.info(f"Deployed Function App: {name}")
        self._log_operation("compute.functionapp.create", {"name": name, "runtime": f"{runtime_stack} {runtime_version}"})
        return func

    def create_function(self, function_app_name: str, function_name: str, trigger_type: str = "HTTP",
                        script: str = "", bindings: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        func_app = self._function_apps.get(function_app_name)
        if not func_app:
            raise ResourceNotFoundError(f"Function app not found: {function_app_name}")
        if function_name in func_app.functions:
            raise ResourceConflictError(f"Function already exists: {function_name}")
        func_app.functions.append(function_name)
        logger.info(f"Created function: {function_name} in app {function_app_name} trigger={trigger_type}")
        self._log_operation("compute.function.create", {"app": function_app_name, "function": function_name, "trigger": trigger_type})
        return {
            "function_app_name": function_app_name,
            "function_name": function_name,
            "trigger_type": trigger_type,
            "script": script,
            "bindings": bindings or [],
            "invoke_url_template": f"https://{func_app.default_host_name}/api/{function_name}"
        }

    def setup_aks(self, cluster_name: str, kubernetes_version: str = "1.27",
                  node_count: int = 3, vm_size: str = "Standard_D2s_v3",
                  enable_rbac: bool = True, enable_auto_scaling: bool = True,
                  min_count: int = 1, max_count: int = 5,
                  network_plugin: str = "azure", network_policy: str = "calico",
                  location: Optional[str] = None,
                  tags: Optional[Dict[str, str]] = None) -> AKSCluster:
        location = location or self._config.location
        self._validate_location(location)
        self._validate_vm_size(vm_size)
        dns_prefix = f"{cluster_name}-dns"
        fqdn = f"{cluster_name}.{location}.azmk8s.io"
        cluster = AKSCluster(
            id=self._generate_id("aks"),
            name=cluster_name,
            location=location,
            resource_group=self._config.resource_group,
            kubernetes_version=kubernetes_version,
            dns_prefix=dns_prefix,
            fqdn=fqdn,
            node_resource_group=f"MC_{self._config.resource_group}_{cluster_name}_{location}",
            enable_rbac=enable_rbac,
            enable_auto_scaling=enable_auto_scaling,
            min_count=min_count,
            max_count=max_count,
            network_plugin=network_plugin,
            network_policy=network_policy,
            tags={**self._config.tags, **(tags or {})}
        )
        self._aks_clusters[cluster.id] = cluster
        logger.info(f"Created AKS cluster: {cluster.id} ({cluster_name}) version={kubernetes_version}")
        self._log_operation("compute.aks.create", {"cluster_id": cluster.id, "name": cluster_name, "version": kubernetes_version})
        return cluster

    def create_storage_account(self, name: str, sku: str = "Standard_LRS", kind: str = "StorageV2",
                               access_tier: str = "Hot", location: Optional[str] = None,
                               enable_https: bool = True, allow_blob_public_access: bool = False,
                               tags: Optional[Dict[str, str]] = None) -> StorageAccount:
        location = location or self._config.location
        self._validate_storage_account_name(name)
        self._validate_location(location)
        valid_skus = [s.value for s in StorageSKU]
        if sku not in valid_skus:
            raise ValidationError(f"Invalid storage SKU: {sku}. Valid: {valid_skus}")
        account = StorageAccount(
            id=self._generate_id("stor"),
            name=name,
            location=location,
            resource_group=self._config.resource_group,
            sku=sku,
            kind=kind,
            access_tier=access_tier,
            enable_https_traffic_only=enable_https,
            allow_blob_public_access=allow_blob_public_access,
            tags={**self._config.tags, **(tags or {})}
        )
        self._storage_accounts[name] = account
        logger.info(f"Created storage account: {name} sku={sku} kind={kind}")
        self._log_operation("storage.account.create", {"account_name": name, "sku": sku, "kind": kind})
        return account

    def create_blob_container(self, storage_account_name: str, container_name: str,
                               public_access: str = "None",
                               metadata: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        account = self._storage_accounts.get(storage_account_name)
        if not account:
            raise ResourceNotFoundError(f"Storage account not found: {storage_account_name}")
        account.containers.append(container_name)
        logger.info(f"Created blob container: {container_name} in account {storage_account_name}")
        self._log_operation("storage.container.create", {"account": storage_account_name, "container": container_name})
        return {
            "storage_account": storage_account_name,
            "container_name": container_name,
            "public_access": public_access,
            "metadata": metadata or {},
            "uri": f"https://{storage_account_name}.blob.core.windows.net/{container_name}"
        }

    def create_key_vault(self, name: str, sku: str = "standard", enable_purge_protection: bool = False,
                         location: Optional[str] = None, tags: Optional[Dict[str, str]] = None) -> KeyVault:
        location = location or self._config.location
        name = self._validate_dns_name(name)
        self._validate_location(location)
        vault_uri = f"https://{name}.vault.azure.net/"
        vault = KeyVault(
            id=self._generate_id("vault"),
            name=name,
            location=location,
            resource_group=self._config.resource_group,
            vault_uri=vault_uri,
            tenant_id=self._config.tenant_id or "00000000-0000-0000-0000-000000000000",
            sku=sku,
            enable_soft_delete=True,
            enable_purge_protection=enable_purge_protection,
            tags={**self._config.tags, **(tags or {})}
        )
        self._key_vaults[name] = vault
        logger.info(f"Created Key Vault: {name}")
        self._log_operation("security.vault.create", {"vault_name": name, "sku": sku})
        return vault

    def create_sql_server(self, server_name: str, administrator_login: str, administrator_password: str,
                          location: Optional[str] = None, tags: Optional[Dict[str, str]] = None) -> SqlServer:
        location = location or self._config.location
        self._validate_dns_name(server_name)
        fqdn = f"{server_name}.database.windows.net"
        server = SqlServer(
            id=self._generate_id("sqlserver"),
            name=server_name,
            location=location,
            resource_group=self._config.resource_group,
            administrator_login=administrator_login,
            fully_qualified_domain_name=fqdn,
            tags={**self._config.tags, **(tags or {})}
        )
        self._sql_servers[server.id] = server
        logger.info(f"Created SQL server: {server_name}")
        self._log_operation("database.sql.create_server", {"server_id": server.id, "name": server_name})
        return server

    def create_sql_database(self, name: str, server_id: str, sku_name: str = "S0",
                            max_size_bytes: int = 268435456000,
                            zone_redundant: bool = False,
                            tags: Optional[Dict[str, str]] = None) -> SqlDatabase:
        server = self._sql_servers.get(server_id)
        if not server:
            raise ResourceNotFoundError(f"SQL server not found: {server_id}")
        db = SqlDatabase(
            id=self._generate_id("sqldb"),
            name=name,
            server_id=server_id,
            location=server.location,
            resource_group=self._config.resource_group,
            sku_name=sku_name,
            max_size_bytes=max_size_bytes,
            zone_redundant=zone_redundant,
            tags={**self._config.tags, **(tags or {})}
        )
        self._sql_databases[db.id] = db
        logger.info(f"Created SQL database: {name} in server {server.name}")
        self._log_operation("database.sql.create_database", {"db_id": db.id, "name": name, "sku": sku_name})
        return db

    def create_redis_cache(self, name: str, sku: str = "Standard", capacity: int = 1,
                           location: Optional[str] = None,
                           tags: Optional[Dict[str, str]] = None) -> RedisCache:
        location = location or self._config.location
        cache = RedisCache(
            id=self._generate_id("redis"),
            name=name,
            location=location,
            resource_group=self._config.resource_group,
            sku=sku,
            capacity=capacity,
            tags={**self._config.tags, **(tags or {})}
        )
        self._redis_caches[cache.id] = cache
        logger.info(f"Created Redis cache: {name} sku={sku} capacity={capacity}")
        self._log_operation("cache.redis.create", {"cache_id": cache.id, "name": name, "sku": sku})
        return cache

    def create_cosmos_db_account(self, account_name: str, kind: str = "GlobalDocumentDB",
                                  consistency_policy: str = "Session",
                                  enable_auto_failover: bool = True,
                                  location: Optional[str] = None,
                                  tags: Optional[Dict[str, str]] = None) -> CosmosDBAccount:
        account = CosmosDBAccount(
            id=self._generate_id("cosmos"),
            name=account_name,
            location=location or self._config.location,
            resource_group=self._config.resource_group,
            kind=kind,
            consistency_policy=consistency_policy,
            enable_automatic_failover=enable_auto_failover,
            tags={**self._config.tags, **(tags or {})}
        )
        self._cosmos_db_accounts[account.id] = account
        logger.info(f"Created Cosmos DB account: {account_name}")
        self._log_operation("database.cosmos.create", {"account_id": account.id, "name": account_name, "kind": kind})
        return account

    def create_system_assigned_identity(self, name: str, location: Optional[str] = None,
                                         tags: Optional[Dict[str, str]] = None) -> ManagedIdentity:
        location = location or self._config.location
        identity = ManagedIdentity(
            id=self._generate_id("identity"),
            name=name,
            principal_id=f"00000000-0000-0000-0000-{uuid.uuid4().hex[:12]}",
            tenant_id=self._config.tenant_id or "00000000-0000-0000-0000-000000000000",
            type=managedIdentityType.SYSTEM_ASSIGNED.value,
            location=location,
            client_id=f"00000000-0000-0000-0000-{uuid.uuid4().hex[:12]}",
            tags={**self._config.tags, **(tags or {})}
        )
        self._managed_identities[identity.id] = identity
        logger.info(f"Created managed identity: {name}")
        self._log_operation("security.identity.create", {"identity_id": identity.id, "name": name})
        return identity

    def configure_cicd(self, project: str, organization: str = "myorg",
                       repository: str = "myrepo", branch: str = "main") -> Dict[str, Any]:
        project_id = self._generate_id("project")
        pipeline_id = self._generate_id("pipeline")
        logger.info(f"Configured Azure DevOps CI/CD for project {project}")
        self._log_operation("devops.cicd.configure", {"project": project, "repo": repository, "branch": branch})
        return {
            "organization": organization,
            "project": project,
            "project_id": project_id,
            "repository": repository,
            "default_branch": branch,
            "pipeline_id": pipeline_id,
            "service_connection_id": self._generate_id("sc"),
            "stages": ["build", "test", "deploy"],
            "status": "active"
        }

    def estimate_cost(self, services: List[str]) -> Dict[str, Any]:
        pricing = {
            "Standard_B1s": 0.012, "Standard_B2s": 0.0256, "Standard_D2s_v3": 0.096,
            "Standard_E2s_v3": 0.144, "Standard_F4s_v2": 0.199, "Standard_G1s": 0.076,
            "Standard_L4s": 0.478, "Standard_NC6": 0.576,
            "Standard_LRS": 0.0184, "Standard_GRS": 0.0368,
            "Basic_C": 0.004, "Standard_C": 0.016, "Premium_C": 0.096,
            "Basic": 4.99, "Standard": 30.00, "Premium": 200.00
        }
        total = 0.0
        details = {}
        for svc in services:
            if svc in pricing:
                cost = pricing[svc]
                details[svc] = {"hourly": cost, "monthly": round(cost * 730, 2)}
                total += cost
            else:
                details[svc] = {"hourly": "varies", "monthly": "varies"}
        logger.info(f"Estimated Azure cost for {len(services)} services")
        self._log_operation("cost_estimate", {"services": services})
        return {
            "currency": "USD",
            "region": self._config.location,
            "subscription_id": self._config.subscription_id[-8:] if self._config.subscription_id else "unknown",
            "total_hourly": round(total, 4),
            "total_monthly": round(total * 730, 2),
            "details": details
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "AzureSpecialistAgent",
            "subscription_id": self._config.subscription_id,
            "resource_group": self._config.resource_group,
            "location": self._config.location,
            "environment": self._config.environment,
            "vms_managed": len(self._vms),
            "vnets_managed": len(self._vnets),
            "subnets_managed": len(self._subnets),
            "nsgs_managed": len(self._nsgs),
            "availability_sets": len(self._availability_sets),
            "aks_clusters": len(self._aks_clusters),
            "function_apps": len(self._function_apps),
            "storage_accounts": len(self._storage_accounts),
            "key_vaults": len(self._key_vaults),
            "sql_servers": len(self._sql_servers),
            "sql_databases": len(self._sql_databases),
            "redis_caches": len(self._redis_caches),
            "managed_identities": len(self._managed_identities),
            "operations_performed": len(self._operation_history),
            "uptime_seconds": (datetime.utcnow() - self._start_time).total_seconds()
        }

    def get_metrics_report(self) -> Dict[str, Any]:
        return {
            "total_metric_points": len(self._metrics.get_metrics()),
            "operations_logged": len(self._operation_history),
            "success_rate": self._calculate_success_rate(),
            "entities": {
                "vm": len(self._vms),
                "vnet": len(self._vnets),
                "subnet": len(self._subnets),
                "nsg": len(self._nsgs),
                "public_ip": len(self._public_ips),
                "network_interface": len(self._network_interfaces),
                "disk": len(self._disks),
                "load_balancer": len(self._load_balancers),
                "availability_set": len(self._availability_sets),
                "aks": len(self._aks_clusters),
                "function_app": len(self._function_apps),
                "storage_account": len(self._storage_accounts),
                "key_vault": len(self._key_vaults),
                "cosmos": len(self._cosmos_db_accounts),
                "sql_server": len(self._sql_servers),
                "sql_database": len(self._sql_databases),
                "redis": len(self._redis_caches),
                "managed_identity": len(self._managed_identities),
                "app_service_plan": len(self._app_service_plans)
            }
        }

    def _calculate_success_rate(self) -> float:
        if not self._operation_history:
            return 0.0
        success = sum(1 for op in self._operation_history if op.get("status") == "success")
        return round(success / len(self._operation_history), 4)

    def export_state(self) -> str:
        state = {
            "region": self._config.location,
            "resource_group": self._config.resource_group,
            "vnets": list(self._vnets.keys()),
            "subnets": list(self._subnets.keys()),
            "nsgs": list(self._nsgs.keys()),
            "public_ips": list(self._public_ips.keys()),
            "nicks": list(self._network_interfaces.keys()),
            "vms": [v.name for v in self._vms.values()],
            "disks": list(self._disks.keys()),
            "load_balancers": [lb.name for lb in self._load_balancers.values()],
            "av_sets": list(self._availability_sets.keys()),
            "aks_clusters": [a.name for a in self._aks_clusters.values()],
            "function_apps": list(self._function_apps.keys()),
            "storage_accounts": list(self._storage_accounts.keys()),
            "key_vaults": list(self._key_vaults.keys()),
            "cosmos": list(self._cosmos_db_accounts.keys()),
            "sql_servers": [s.name for s in self._sql_servers.values()],
            "sql_databases": [d.name for d in self._sql_databases.values()],
            "redis": list(self._redis_caches.keys()),
            "managed_identities": list(self._managed_identities.keys()),
            "app_service_plans": list(self._app_service_plans.keys())
        }
        return json.dumps(state, indent=2, default=str)

    def import_state(self, state_json: str) -> None:
        state = json.loads(state_json)
        logger.info(f"Importing Azure state with {len(state)} top-level keys")
        self._log_operation("state.import", {"state_keys": list(state.keys())})

    def validate_configuration(self) -> List[Dict[str, Any]]:
        issues = []
        for vm_id, vm in self._vms.items():
            if vm.status == VMStatus.RUNNING.value and not vm.network_interface_ids:
                issues.append({"severity": "medium", "type": "network", "resource_id": vm_id, "message": "Running VM has no NICs"})
            if vm.status == VMStatus.RUNNING.value and not vm.availability_set_id:
                issues.append({"severity": "low", "type": "reliability", "resource_id": vm_id, "message": "Running VM not in availability set"})
        for pip_id, pip in self._public_ips.items():
            if pip.allocation_method == "Static" and not pip.ip_address:
                issues.append({"severity": "info", "type": "resource", "resource_id": pip_id, "message": "Static PIP not allocated"})
        logger.info(f"Configuration validation found {len(issues)} issues")
        return issues

    def validate_nsg_rules(self, nsg_id: str) -> List[Dict[str, Any]]:
        nsg = self._nsgs.get(nsg_id)
        if not nsg:
            raise ResourceNotFoundError(f"NSG not found: {nsg_id}")
        issues = []
        for rule in nsg.security_rules:
            if rule.get("destination_port_range") == "22" and rule.get("source_address_prefix") == "*":
                issues.append({"rule": rule["name"], "issue": "SSH open to internet", "severity": "high"})
            if rule.get("destination_port_range") == "3389" and rule.get("source_address_prefix") == "*":
                issues.append({"rule": rule["name"], "issue": "RDP open to internet", "severity": "critical"})
            if rule.get("priority", 0) < 100:
                issues.append({"rule": rule["name"], "issue": "Priority too low (reserved for default rules)", "severity": "warning"})
        return issues

    def optimize_costs(self) -> Dict[str, Any]:
        savings = 0.0
        recommendations = []
        for vm_id, vm in self._vms.items():
            if vm.status in [VMStatus.STOPPED.value, VMStatus.DEALLOCATED.value]:
                recommendations.append({"resource": vm_id, "type": vm.name, "action": "deallocate_stopped_vm", "estimated_monthly_savings": 15.0})
                savings += 15.0
            elif vm.size in [VMSize.NC12.value, VMSize.G1S.value]:
                recommendations.append({"resource": vm_id, "type": vm.name, "action": "rightsizing", "current_size": vm.size, "suggested_size": "Standard_D2s_v3", "estimated_monthly_savings": 75.0})
                savings += 75.0
        for disk_id, disk in self._disks.items():
            if disk.sku == StorageSKU.PREMIUM_LRS.value and disk.disk_iops_read_write == 0 and disk.disk_mbps_read_write == 0:
                recommendations.append({"resource": disk_id, "action": "downgrade_to_standard", "estimated_monthly_savings": 5.0})
                savings += 5.0
        logger.info(f"Cost optimization: ${round(savings, 2)}/month potential")
        self._log_operation("optimize.costs", {"monthly_savings": round(savings, 2)})
        return {"potential_savings_monthly": round(savings, 2), "recommendations": recommendations}

    def configure_vpn_gateway(self, name: str, vnet_id: str, gateway_type: str = "Vpn",
                               sku: str = "VpnGw1", location: Optional[str] = None) -> Dict[str, Any]:
        vnet = self._vnets.get(vnet_id)
        if not vnet:
            raise ResourceNotFoundError(f"VNet not found: {vnet_id}")
        gateway_id = self._generate_id("vgw")
        logger.info(f"Created VPN gateway: {name}")
        self._log_operation("network.vpngw.create", {"gateway_id": gateway_id, "name": name, "vnet_id": vnet_id})
        return {
            "id": gateway_id,
            "name": name,
            "vnet_id": vnet_id,
            "gateway_type": gateway_type,
            "sku": sku,
            "location": location or self._config.location,
            "bgp_peering_address": "10.0.255.254",
            "status": "ProvisioningSucceeded"
        }

    def create_load_balancer(self, name: str, sku: str = "Standard", location: Optional[str] = None,
                              tags: Optional[Dict[str, str]] = None) -> LoadBalancer:
        location = location or self._config.location
        self._validate_dns_name(name)
        lb = LoadBalancer(
            id=self._generate_id("lb"),
            name=name,
            location=location,
            resource_group=self._config.resource_group,
            sku=sku,
            tags={**self._config.tags, **(tags or {})}
        )
        self._load_balancers[lb.id] = lb
        logger.info(f"Created load balancer: {lb.id} ({name}) sku={sku}")
        self._log_operation("network.lb.create", {"lb_id": lb.id, "name": name, "sku": sku})
        return lb

    def publish_sql_dacpac(self, server_id: str, database_id: str, dacpac_file_path: str,
                           connection_string: str) -> Dict[str, Any]:
        server = self._sql_servers.get(server_id)
        db = self._sql_databases.get(database_id)
        if not server or not db:
            raise ResourceNotFoundError("SQL server or database not found")
        logger.info(f"Published DACPAC to {server.name}.{db.name}")
        self._log_operation("database.sql.deploy_dacpac", {"server_id": server_id, "db_id": database_id, "dacpac": dacpac_file_path})
        return {
            "server": server.fully_qualified_domain_name,
            "database": db.name,
            "dacpac": dacpac_file_path,
            "deployment_status": "Success",
            "details": "Post-deployment script ran successfully."
        }

    def overwrite_service_tags(self, resource_id: str, new_tags: Dict[str, str]) -> Dict[str, Any]:
        logger.info(f"Overwriting tags for resource: {resource_id}")
        self._log_operation("resource.tags.overwrite", {"resource_id": resource_id, "new_tag_count": len(new_tags)})
        return {
            "resource_id": resource_id,
            "tags": new_tags,
            "status": "updated",
            "updated_at": datetime.utcnow().isoformat()
        }

    def get_account_billing_summary(self, billing_period: str = "current") -> Dict[str, Any]:
        logger.info(f"Retrieved Azure billing summary for period={billing_period}")
        self._log_operation("billing.summary", {"period": billing_period})
        return {
            "billing_period": billing_period,
            "subscription_id": self._config.subscription_id[-8:] if self._config.subscription_id else "unknown",
            "estimated_cost_usd": round(len(self._vms) * 15.0 + len(self._sql_databases) * 25.0 + len(self._storage_accounts) * 2.5, 2),
            "currency": "USD",
            "resources": {
                "vms": len(self._vms),
                "sql_databases": len(self._sql_databases),
                "storage_accounts": len(self._storage_accounts)
            }
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "AzureSpecialistAgent",
            "subscription_id": self._config.subscription_id,
            "resource_group": self._config.resource_group,
            "location": self._config.location,
            "environment": self._config.environment,
            "vms_managed": len(self._vms),
            "vnets_managed": len(self._vnets),
            "subnets_managed": len(self._subnets),
            "nsgs_managed": len(self._nsgs),
            "availability_sets": len(self._availability_sets),
            "aks_clusters": len(self._aks_clusters),
            "function_apps": len(self._function_apps),
            "storage_accounts": len(self._storage_accounts),
            "key_vaults": len(self._key_vaults),
            "sql_servers": len(self._sql_servers),
            "sql_databases": len(self._sql_databases),
            "redis_caches": len(self._redis_caches),
            "managed_identities": len(self._managed_identities),
            "app_service_plans": len(self._app_service_plans),
            "operations_performed": len(self._operation_history),
            "uptime_seconds": (datetime.utcnow() - self._start_time).total_seconds(),
            "success_rate": self._calculate_success_rate()
        }


def demonstrate_networking(agent: AzureSpecialistAgent) -> None:
    print("\n=== Networking ===")
    vnet = agent.create_virtual_network(name="prod-vnet", address_space=["10.0.0.0/16"])
    print(f"VNet: {vnet.name} | ID: {vnet.id} | Address Space: {vnet.address_space}")
    subnet = agent.add_subnet(vnet.id, "frontend-subnet", "10.0.1.0/24", service_endpoints=["Microsoft.Storage"])
    print(f"Subnet: {subnet.name} | CIDR: {subnet.address_prefix}")
    nsg = agent.create_network_security_group(name="web-nsg")
    agent.add_nsg_security_rule(nsg.id, "AllowHTTPS", 100, "Inbound", "Allow", "Tcp", "*", "*", "*", "443")
    agent.add_nsg_security_rule(nsg.id, "DenyAll", 65500, "Inbound", "Deny", "*", "*", "*", "*", "*")
    print(f"NSG: {nsg.name} | Rules: {len(nsg.security_rules)}")
    pip = agent.create_public_ip_address(name="web-pip")
    print(f"Public IP: {pip.name} | SKU: {pip.sku} | Allocation: {pip.allocation_method}")
    nic = agent.create_network_interface("web-nic", subnet.id, "10.0.1.4", public_ip_address_id=pip.id, network_security_group_id=nsg.id)
    print(f"NIC: {nic.name} | Private IP: {nic.private_ip_address} | AcceleratedNetworking: {nic.enable_accelerated_networking}")


def demonstrate_vm_management(agent: AzureSpecialistAgent) -> None:
    print("\n=== VM Management ===")
    avset = agent.create_availability_set(name="web-avset", fault_domain_count=2, update_domain_count=5)
    print(f"Availability Set: {avset.name} | FD: {avset.platform_fault_domain_count}")
    disk = agent.create_managed_disk(name="web-disk-os", disk_size_gb=128, sku="Standard_LRS", os_type="Linux")
    print(f"Disk: {disk.name} | Size: {disk.disk_size_gb}GB | SKU: {disk.sku}")
    vm = agent.create_vm(
        name="web-vm-1",
        size="Standard_B2s",
        admin_username="azureuser",
        admin_password="P@ssw0rd2024!",
        os_type="Linux",
        availability_set_id=avset.id,
        disk_ids=[disk.id],
        tags={"Environment": "production", "Team": "platform"}
    )
    print(f"VM: {vm.id} | Name: {vm.name} | Size: {vm.size} | OS: {vm.os_type} | Status: {vm.status}")
    agent.start_vm(vm.id)
    vm.status = "running"
    print(f"VM started: {vm.name} | Status: {vm.status}")


def demonstrate_app_services(agent: AzureSpecialistAgent) -> None:
    print("\n=== App Services ===")
    plan = agent.create_app_service_plan(name="api-plan", sku_name="P1v2", capacity=2)
    print(f"App Service Plan: {plan.name} | SKU: {plan.sku_name} | Capacity: {plan.capacity}")
    func_app = agent.deploy_function_app(name="order-processor", runtime_stack="python", runtime_version="3.11")
    print(f"Function App: {func_app.name} | Runtime: {func_app.runtime_stack} {func_app.runtime_version} | URL: {func_app.default_host_name}")
    func = agent.create_function("order-processor", "process-order", trigger_type="HTTP",
                                  script="import json\ndef main(req): return {'status': 'ok'}")
    print(f"Function: {func['function_name']} | Trigger: {func['trigger_type']} | URL: {func['invoke_url_template']}")


def demonstrate_containers(agent: AzureSpecialistAgent) -> None:
    print("\n=== AKS & Managed Identity ===")
    aks = agent.setup_aks(cluster_name="prod-aks", kubernetes_version="1.27", node_count=3, vm_size="Standard_D2s_v3",
                          enable_rbac=True, enable_auto_scaling=True, min_count=2, max_count=10)
    print(f"AKS: {aks.name} | Version: {aks.kubernetes_version} | FQDN: {aks.fqdn}")
    identity = agent.create_system_assigned_identity(name="akspodidentity")
    print(f"Managed Identity: {identity.name} | Principal: {identity.principal_id} | Type: {identity.type}")


def demonstrate_storage_db(agent: AzureSpecialistAgent) -> None:
    print("\n=== Storage & Database ===")
    storage = agent.create_storage_account(name="appstorageprod", sku="Standard_LRS", kind="StorageV2", access_tier="Hot")
    print(f"Storage: {storage.id} | SKU: {storage.sku} | Kind: {storage.kind}")
    container = agent.create_blob_container("appstorageprod", "documents")
    print(f"Blob Container: {container['container_name']} | URI: {container['uri']}")
    server = agent.create_sql_server("prod-sql-srv", "sqladmin", "SqlP@ssw0rd!2024")
    print(f"SQL Server: {server.name} | FQDN: {server.fully_qualified_domain_name}")
    db = agent.create_sql_database("appdb", server.id, sku_name="S1")
    print(f"SQL Database: {db.name} | SKU: {db.sku_name} | MaxSize: {db.max_size_bytes} bytes")
    cosmos = agent.create_cosmos_db_account("appcosmos", kind="MongoDB", consistency_policy="BoundedStaleness")
    print(f"Cosmos DB: {cosmos.name} | Kind: {cosmos.kind} | Consistency: {cosmos.consistency_policy}")
    redis = agent.create_redis_cache("appcache", sku="Standard", capacity=1)
    print(f"Redis: {redis.name} | SKU: {redis.sku} | Capacity: {redis.capacity}")
    vault = agent.create_key_vault("appvaultprod", sku="premium", enable_purge_protection=True)
    print(f"Key Vault: {vault.name} | URI: {vault.vault_uri} | SKU: {vault.sku}")


def demonstrate_security_compliance(agent: AzureSpecialistAgent) -> None:
    print("\n=== Security & Compliance ===")
    identity = agent.create_system_assigned_identity(name="secure-identity")
    print(f"Managed Identity: {identity.name} | Type: {identity.type}")
    vault = agent.create_key_vault("secure-vault")
    print(f"Key Vault: {vault.name} | Soft Delete: {vault.enable_soft_delete} | Purge Protected: {vault.enable_purge_protection}")
    nsg = agent.create_network_security_group(name="secure-nsg")
    agent.add_nsg_security_rule(nsg.id, "DenyRDP", 4000, "Inbound", "Deny", "*", "*", "*", "*", "3389")
    issues = agent.validate_nsg_rules(nsg.id)
    print(f"NSG Validation: {len(issues)} issues found: {[i['issue'] for i in issues]}")


def demonstrate_monitoring_cicd(agent: AzureSpecialistAgent) -> None:
    print("\n=== CI/CD & Monitoring ===")
    cicd = agent.configure_cicd(project="myapp", organization="azureorg", repository="myapp-repo", branch="main")
    print(f"Azure DevOps Project: {cicd['project']} | Pipeline: {cicd['pipeline_id']} | Stages: {cicd['stages']}")


def demonstrate_reporting(agent: AzureSpecialistAgent) -> None:
    print("\n=== Reporting ===")
    summary = agent.get_status()
    print("=== Status ===")
    for k, v in summary.items():
        if k != "agent":
            print(f"  {k}: {v}")
    metrics = agent.get_metrics_report()
    print(f"\nMetrics: {metrics['operations_logged']} ops, {metrics['success_rate']:.2%} success rate")
    billing = agent.get_account_billing_summary()
    print(f"\nBilled estimate: ${billing['estimated_cost_usd']}/mo")
    issues = agent.validate_configuration()
    print(f"\nValidation issues: {len(issues)}")
    state = agent.export_state()
    print(f"Exported state ({len(state)} chars)")


def main() -> None:
    print("Azure Specialist Agent Demo")
    print("=" * 50)
    config = Config(
        subscription_id="00000000-0000-0000-0000-000000000000",
        resource_group="demo-rg",
        location="eastus",
        environment="development",
        tags={"ManagedBy": "AzureSpecialistAgent", "Project": "Demo"}
    )
    agent = AzureSpecialistAgent(config=config)
    print(agent.get_status())
    demonstrate_networking(agent)
    demonstrate_vm_management(agent)
    demonstrate_app_services(agent)
    demonstrate_containers(agent)
    demonstrate_storage_db(agent)
    demonstrate_security_compliance(agent)
    demonstrate_monitoring_cicd(agent)
    demonstrate_reporting(agent)
    print("\n" + "=" * 50)
    print("Demo completed.")


if __name__ == "__main__":
    main()
