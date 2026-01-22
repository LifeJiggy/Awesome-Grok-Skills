from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class AzureServiceType(Enum):
    COMPUTE = "compute"
    STORAGE = "storage"
    DATABASE = "database"
    NETWORK = "network"
    CONTAINER = "container"
    COGNITIVE = "cognitive"
    ANALYTICS = "analytics"
    IDENTITY = "identity"


@dataclass
class VirtualMachine:
    vm_id: str
    name: str
    size: str
    os: str
    admin_username: str
    public_ip: Optional[str]
    private_ip: str
    status: str
    resource_group: str


@dataclass
class AzureSQLDatabase:
    server_name: str
    database_name: str
    edition: str
    service_level: str
    max_size_gb: int
    status: str
    connection_string: str


@dataclass
class AppService:
    app_id: str
    name: string
    kind: str
    runtime: str
    plan: str
    custom_domain: List[str]
    ssl_enabled: bool
    status: str


class AzureServicesManager:
    """Manage Azure resources and services"""
    
    def __init__(self):
        self.resources = []
    
    def create_virtual_machine(self,
                               name: str,
                               size: str = "Standard_B2s",
                               os: str = "UbuntuLTS",
                               admin_username: str = "azureuser") -> VirtualMachine:
        """Create Azure Virtual Machine"""
        return VirtualMachine(
            vm_id=f"/subscriptions/123/resourceGroups/rg-{name}/providers/Microsoft.Compute/virtualMachines/{name}",
            name=name,
            size=size,
            os=os,
            admin_username=admin_username,
            public_ip=None,
            private_ip="10.0.1.4",
            status="Creating",
            resource_group=f"rg-{name}"
        )
    
    def create_azure_sql(self,
                         server_name: str,
                         database_name: str,
                         edition: str = "GeneralPurpose",
                         service_level: str = "GP_Gen5_2") -> AzureSQLDatabase:
        """Create Azure SQL Database"""
        return AzureSQLDatabase(
            server_name=server_name,
            database_name=database_name,
            edition=edition,
            service_level=service_level,
            max_size_gb=32,
            status="Creating",
            connection_string=f"Server=tcp:{server_name}.database.windows.net,1433;Database={database_name};User ID=admin;Password=pass;Encrypt=true;"
        )
    
    def create_app_service(self,
                           name: str,
                           kind: str = "webapp",
                           runtime: str = "python:3.9",
                           plan_tier: str = "S1") -> AppService:
        """Create Azure App Service"""
        return AppService(
            app_id=f"/subscriptions/123/resourceGroups/rg-{name}/providers/Microsoft.Web/sites/{name}",
            name=name,
            kind=kind,
            runtime=runtime,
            plan=f"appserviceplan-{name}",
            custom_domain=[f"{name}.azurewebsites.net"],
            ssl_enabled=True,
            status="Creating"
        )
    
    def create_storage_account(self,
                               name: str,
                               account_type: str = "Standard_LRS") -> Dict:
        """Create Azure Storage Account"""
        return {
            'id': f"/subscriptions/123/resourceGroups/rg-storage/providers/Microsoft.Storage/storageAccounts/{name}",
            'name': name,
            'type': account_type,
            'location': 'eastus',
            'primary_endpoints': {
                'blob': f"https://{name}.blob.core.windows.net/",
                'queue': f"https://{name}.queue.core.windows.net/",
                'table': f"https://{name}.table.core.windows.net/",
                'file': f"https://{name}.file.core.windows.net/"
            },
            'access_tier': 'Hot',
            'encryption': {'services': {'blob': {'enabled': True}, 'file': {'enabled': True}}},
            'allow_blob_public_access': False
        }
    
    def create_aks_cluster(self,
                           name: str,
                           node_count: int = 3,
                           vm_size: str = "Standard_D2s_v3") -> Dict:
        """Create Azure Kubernetes Service cluster"""
        return {
            'id': f"/subscriptions/123/resourceGroups/rg-{name}/providers/Microsoft.ContainerService/managedClusters/{name}",
            'name': name,
            'location': 'eastus',
            'kubernetes_version': '1.27',
            'dns_prefix': name,
            'agent_pool_profiles': [{
                'name': 'agentpool',
                'count': node_count,
                'vm_size': vm_size,
                'os_type': 'Linux'
            }],
            'service_principal_profile': {'client_id': 'app-id', 'secret': '****'},
            'addon_profiles': {
                'azurepolicy': {'enabled': True},
                'omsagent': {'enabled': True}
            },
            'network_profile': {
                'network_plugin': 'azure',
                'load_balancer_sku': 'standard',
                'service_cidr': '10.0.0.0/16',
                'dns_service_ip': '10.0.0.10'
            },
            'status': 'Creating'
        }
    
    def create_cosmos_db(self,
                         name: str,
                         api: str = "sql",
                         consistency_level: str = "Session") -> Dict:
        """Create Azure Cosmos DB"""
        return {
            'id': f"/subscriptions/123/resourceGroups/rg-{name}/providers/Microsoft.DocumentDB/databaseAccounts/{name}",
            'name': name,
            'api': api,
            'consistency_policy': {'default_consistency_level': consistency_level, 'max_interval_in_seconds': 5, 'max_staleness_prefix': 100},
            'locations': [
                {'location_name': 'eastus', 'failover_priority': 0, 'is_zone_redundant': False},
                {'location_name': 'westus', 'failover_priority': 1, 'is_zone_redundant': False}
            ],
            'capabilities': [{'name': 'EnableServerless'}],
            'enable_free_tier': False,
            'status': 'Online'
        }
    
    def create_load_balancer(self,
                             name: str,
                             frontend_ips: List[Dict] = None) -> Dict:
        """Create Azure Load Balancer"""
        return {
            'id': f"/subscriptions/123/resourceGroups/rg-{name}/providers/Microsoft.Network/loadBalancers/{name}",
            'name': name,
            'location': 'eastus',
            'sku': 'Standard',
            'frontend_ip_configurations': frontend_ips or [{'name': 'fe1', 'public_ip_address': {'id': '/subscriptions/123/providers/Microsoft.Network/publicIPAddresses/ip-001'}}],
            'backend_address_pools': [{'name': 'be-pool-1'}],
            'load_balancing_rules': [
                {'name': 'lb-rule-1', 'frontend_port': 80, 'backend_port': 80, 'protocol': 'Tcp', 'enable_floating_ip': False}
            ],
            'probes': [{'name': 'http-probe', 'protocol': 'Http', 'port': 80, 'path': '/'}],
            'inbound_nat_rules': []
        }
    
    def create_virtual_network(self,
                               name: str,
                               address_space: str = "10.0.0.0/16") -> Dict:
        """Create Azure Virtual Network"""
        return {
            'id': f"/subscriptions/123/resourceGroups/rg-{name}/providers/Microsoft.Network/virtualNetworks/{name}",
            'name': name,
            'location': 'eastus',
            'address_space': {'address_prefixes': [address_space]},
            'subnets': [
                {'name': 'Subnet1', 'address_prefix': '10.0.1.0/24', 'service_endpoints': [{'service': 'Microsoft.Storage'}]},
                {'name': 'Subnet2', 'address_prefix': '10.0.2.0/24', 'service_endpoints': [{'service': 'Microsoft.Sql'}]}
            ],
            'ddos_protection_mode': 'VirtualNetworkInherited',
            'dns_servers': ['168.63.129.16']
        }


class AzureDevOpsManager:
    """Manage Azure DevOps resources"""
    
    def __init__(self):
        self.projects = []
    
    def create_project(self,
                       name: str,
                       description: str = "") -> Dict:
        """Create Azure DevOps project"""
        return {
            'id': f"{name.lower().replace(' ', '-')}-001",
            'name': name,
            'description': description,
            'visibility': 'private',
            'process_template': 'Agile',
            'version_control': 'Git',
            'url': f"https://dev.azure.com/organization/{name}"
        }
    
    def create_pipeline(self,
                        name: str,
                        yaml_content: str) -> Dict:
        """Create Azure Pipeline"""
        return {
            'id': f"pipelines/{name}",
            'name': name,
            'folder': '\\\\',
            'configuration': {'type': 'yaml', 'path': 'azure-pipelines.yml'},
            'queue_status': 'enabled',
            'latest_build': {'id': 123, 'status': 'succeeded'}
        }
    
    def create_azure_function(self,
                              name: str,
                              runtime: str = "python",
                              version: str = "3") -> Dict:
        """Create Azure Function App"""
        return {
            'id': f"/subscriptions/123/resourceGroups/rg-{name}/providers/Microsoft.Web/sites/{name}",
            'name': name,
            'kind': 'functionapp',
            'runtime': runtime,
            'runtime_version': version,
            'app_settings': {
                'FUNCTIONS_WORKER_RUNTIME': runtime,
                'AzureWebJobsStorage': 'DefaultEndpointsProtocol=https;AccountName=storage;AccountKey=key'
            },
            'https_only': True,
            'status': 'Running'
        }


if __name__ == "__main__":
    azure = AzureServicesManager()
    
    vm = azure.create_virtual_machine("webvm")
    print(f"VM created: {vm.name}")
    
    sql = azure.create_azure_sql("sql-server", "mydb")
    print(f"SQL Database: {sql.database_name}")
    
    app = azure.create_app_service("mywebapp")
    print(f"App Service: {app.name}")
    
    storage = azure.create_storage_account("mystorageaccount")
    print(f"Storage Account: {storage['name']}")
    
    aks = azure.create_aks_cluster("myaks")
    print(f"AKS Cluster: {aks['name']}")
    
    cosmos = azure.create_cosmos_db("mycosmos")
    print(f"Cosmos DB: {cosmos['name']}")
    
    devops = AzureDevOpsManager()
    project = devops.create_project("MyProject")
    print(f"DevOps Project: {project['name']}")
