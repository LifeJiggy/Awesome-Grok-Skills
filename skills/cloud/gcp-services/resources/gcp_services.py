from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class GCPServiceType(Enum):
    COMPUTE = "compute"
    STORAGE = "storage"
    DATABASE = "database"
    NETWORKING = "networking"
    CONTAINER = "container"
    AI_ML = "ai_ml"
    ANALYTICS = "analytics"
    API = "api"


@dataclass
class GCEInstance:
    instance_id: str
    name: string
    machine_type: str
    zone: str
    status: str
    internal_ip: str
    external_ip: Optional[str]
    disks: List[str]
    network_interfaces: List[Dict]


@dataclass
class GKECluster:
    cluster_id: str
    name: str
    location: str
    node_count: int
    machine_type: str
    status: str
    kubernetes_version: str


@dataclass
class CloudSQLInstance:
    instance_id: str
    name: str
    database_version: str
    tier: str
    region: str
    Multi_AZ: bool
    status: str
    connection_name: str


class GCPServicesManager:
    """Manage Google Cloud Platform services"""
    
    def __init__(self):
        self.resources = []
    
    def create_compute_engine(self,
                              name: str,
                              machine_type: str = "e2-medium",
                              zone: str = "us-central1-a") -> GCEInstance:
        """Create GCE Instance"""
        return GCEInstance(
            instance_id=f"projects/my-project/zones/{zone}/instances/{name}",
            name=name,
            machine_type=f"zones/{zone}/machineTypes/{machine_type}",
            zone=zone,
            status="PROVISIONING",
            internal_ip="10.0.1.4",
            external_ip=None,
            disks=["projects/my-project/zones/{zone}/disks/boot-disk".format(zone=zone)],
            network_interfaces=[{
                'network': 'projects/my-project/global/networks/default',
                'subnetwork': f"projects/my-project/regions/us-central1/subnetworks/default",
                'access_configs': [{'name': 'external-nat', 'type': 'ONE_TO_ONE_NAT'}]
            }]
        )
    
    def create_gke_cluster(self,
                           name: str,
                           node_count: int = 3,
                           location: str = "us-central1") -> GKECluster:
        """Create GKE Cluster"""
        return GKECluster(
            cluster_id=f"projects/my-project/locations/{location}/clusters/{name}",
            name=name,
            location=location,
            node_count=node_count,
            machine_type="e2-medium",
            status="PROVISIONING",
            kubernetes_version="1.27.3-gke.100"
        )
    
    def create_cloud_sql(self,
                         name: str,
                         database_version: str = "POSTGRES_15",
                         tier: str = "db-custom-2-7680",
                         region: str = "us-central1") -> CloudSQLInstance:
        """Create Cloud SQL instance"""
        return CloudSQLInstance(
            instance_id=f"projects/my-project/instances/{name}",
            name=name,
            database_version=database_version,
            tier=tier,
            region=region,
            Multi_AZ=True,
            status="RUNNABLE",
            connection_name=f"my-project:{region}:{name}"
        )
    
    def create_cloud_storage_bucket(self,
                                    name: str,
                                    location: str = "US") -> Dict:
        """Create Cloud Storage bucket"""
        return {
            'name': name,
            'location': location,
            'storage_class': 'STANDARD',
            'id': f"{name}.appspot.com",
            'time_created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            'encryption': {'default_kms_key': f"projects/my-project/keyRings/kr/cryptoKeys/key-1"},
            'versioning': {'enabled': False},
            'lifecycle': {'rules': []},
            'public_access_prevention': 'enforced',
            'uniform_bucket_level_access': True
        }
    
    def create_cloud_function(self,
                              name: str,
                              runtime: str = "python311",
                              entry_point: str = "hello_world") -> Dict:
        """Create Cloud Function"""
        return {
            'name': f"projects/my-project/locations/us-central1/functions/{name}",
            'runtime': runtime,
            'entry_point': entry_point,
            'event_trigger': {'event_type': 'google.cloud.storage.object.v1.finalized', 'resource': f"projects/_/buckets/{name}-bucket"},
            'service_account_email': f"{name}@my-project.iam.gserviceaccount.com",
            'available_memory_mb': 256,
            'timeout_seconds': 60,
            'max_instances': 10,
            'status': 'ACTIVE'
        }
    
    def create_cloud_run_service(self,
                                 name: str,
                                 image: str = "gcr.io/my-project/image:latest") -> Dict:
        """Create Cloud Run service"""
        return {
            'name': f"namespaces/default/services/{name}",
            'location': "us-central1",
            'image': image,
            'port': 8080,
            'memory': "256Mi",
            'cpu': "1",
            'autoscaling': {'min_instances': 0, 'max_instances': 10},
            'concurrency': 80,
            'authentication': {'allow_unauthenticated': False},
            'revision': f"{name}-00001-abc",
            'url': f"https://{name}-abcde-uc.a.run.app"
        }
    
    def create_vpc_network(self,
                           name: str,
                           subnet_mode: str = "custom") -> Dict:
        """Create VPC network"""
        return {
            'id': f"projects/my-project/global/networks/{name}",
            'name': name,
            'auto_create_subnetworks': False,
            'subnet_mode': subnet_mode,
            'routing_mode': 'REGIONAL',
            'mtu': 1460,
            'firewall_rules': [
                {'name': 'allow-internal', 'direction': 'INGRESS', 'allowed': [{'IPProtocol': 'tcp', 'ports': ['0-65535']}, {'IPProtocol': 'udp', 'ports': ['0-65535']}]},
                {'name': 'allow-ssh', 'direction': 'INGRESS', 'allowed': [{'IPProtocol': 'tcp', 'ports': ['22']}], 'source_ranges': ['0.0.0.0/0']}
            ],
            'peerings': []
        }
    
    def create_bigquery_dataset(self,
                                dataset_id: str,
                                location: str = "US") -> Dict:
        """Create BigQuery dataset"""
        return {
            'dataset_id': dataset_id,
            'location': location,
            'default_table_expiration_ms': None,
            'default_partition_expiration_ms': None,
            'labels': {'env': 'production'},
            'access': [
                {'role': 'OWNER', 'specialGroup': 'projectOwners'},
                {'role': 'READER', 'specialGroup': 'projectReaders'}
            ],
            'friendly_name': dataset_id.title()
        }
    
    def create_vertex_ai_model(self,
                               name: str,
                               display_name: str) -> Dict:
        """Create Vertex AI Model"""
        return {
            'name': f"projects/my-project/locations/us-central1/models/{name}",
            'display_name': display_name,
            'container_spec': {
                'image_uri': 'gcr.io/my-project/model:v1',
                'command': [],
                'args': [],
                'ports': [{'containerPort': 8080}]
            },
            'predict_schemata': {
                'instance_schema_uri': 'gs://my-project/schema.yaml',
                'parameters_schema_uri': 'gs://my-project/parameters.yaml',
                'prediction_schema_uri': 'gs://my-project/prediction.yaml'
            },
            'version': 1,
            'create_time': datetime.now().isoformat(),
            'etag': 'abc123'
        }


class GCPResourceManager:
    """Manage GCP resources and projects"""
    
    def __init__(self):
        self.projects = []
    
    def create_project(self,
                       name: str,
                       project_id: str,
                       organization_id: str = None) -> Dict:
        """Create GCP project"""
        return {
            'name': name,
            'project_id': project_id,
            'project_number': f"{hash(project_id) % 10**9}",
            'lifecycle_state': 'ACTIVE',
            'parent': {'type': 'organization', 'id': organization_id} if organization_id else None,
            'labels': {'env': 'production'},
            'create_time': datetime.now().isoformat()
        }
    
    def enable_service(self,
                       project_id: str,
                       service: str) -> Dict:
        """Enable GCP service"""
        return {
            'name': f"projects/{project_id}/services/{service}",
            'config': {
                'name': service,
                'title': service.title(),
                'display_name': service.title()
            },
            'state': 'ENABLED'
        }
    
    def set_iam_policy(self,
                       resource: str,
                       bindings: List[Dict]) -> Dict:
        """Set IAM policy"""
        return {
            'version': 1,
            'etag': 'ACAB',
            'bindings': bindings + [
                {'role': 'roles/owner', 'members': ['user:admin@example.com']},
                {'role': 'roles/editor', 'members': ['user:developer@example.com']}
            ]
        }


class GCPCostManagement:
    """GCP cost optimization"""
    
    def analyze_costs(self,
                      billing_account: str) -> Dict:
        """Analyze GCP costs"""
        return {
            'billing_account': billing_account,
            'cost_this_month': 2450.75,
            'forecasted': 2800.00,
            'by_service': {
                'Compute Engine': 850.00,
                'Cloud Storage': 120.00,
                'BigQuery': 340.00,
                'Cloud Run': 180.00,
                'Other': 960.75
            },
            'by_location': {
                'us-central1': 1800.00,
                'us-east1': 450.00,
                'europe-west1': 200.75
            },
            'recommendations': [
                {'action': 'Compress Cloud Storage objects', 'savings': 45.00},
                {'action': 'Use committed use discounts for persistent disks', 'savings': 120.00},
                {'action': 'Right-size GCE instances', 'savings': 200.00}
            ]
        }


if __name__ == "__main__":
    gcp = GCPServicesManager()
    
    instance = gcp.create_compute_engine("my-instance")
    print(f"GCE Instance: {instance.name}")
    
    gke = gcp.create_gke_cluster("my-cluster")
    print(f"GKE Cluster: {gke.name}")
    
    cloudsql = gcp.create_cloud_sql("my-db")
    print(f"Cloud SQL: {cloudsql.name}")
    
    bucket = gcp.create_cloud_storage_bucket("my-bucket")
    print(f"GCS Bucket: {bucket['name']}")
    
    function = gcp.create_cloud_function("my-function")
    print(f"Cloud Function: {function['name']}")
    
    cloudrun = gcp.create_cloud_run_service("my-service")
    print(f"Cloud Run: {cloudrun['url']}")
    
    bigquery = gcp.create_bigquery_dataset("my_dataset")
    print(f"BigQuery Dataset: {bigquery['dataset_id']}")
    
    cost = GCPCostManagement()
    analysis = cost.analyze_costs("billing-123")
    print(f"Monthly Cost: ${analysis['cost_this_month']}")
