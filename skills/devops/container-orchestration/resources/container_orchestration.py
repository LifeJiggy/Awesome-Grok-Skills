from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class ResourceType(Enum):
    POD = "pod"
    DEPLOYMENT = "deployment"
    SERVICE = "service"
    INGRESS = "ingress"
    CONFIGMAP = "configmap"
    SECRET = "secret"
    PERSISTENTVOLUME = "persistentvolume"
    NAMESPACE = "namespace"


@dataclass
class Pod:
    name: str
    namespace: str
    image: str
    replicas: int
    status: str
    ready_replicas: int
    cpu_request: str
    memory_request: str


class KubernetesManager:
    """Manage Kubernetes clusters and workloads"""
    
    def __init__(self):
        self.clusters = []
    
    def create_deployment(self,
                          name: str,
                          image: str,
                          replicas: int = 3,
                          namespace: str = "default") -> Dict:
        """Create Kubernetes deployment"""
        return {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {'name': name, 'namespace': namespace},
            'spec': {
                'replicas': replicas,
                'selector': {'matchLabels': {'app': name}},
                'template': {
                    'metadata': {'labels': {'app': name}},
                    'spec': {
                        'containers': [{
                            'name': name,
                            'image': image,
                            'ports': [{'containerPort': 8080}],
                            'resources': {
                                'requests': {'cpu': '100m', 'memory': '128Mi'},
                                'limits': {'cpu': '500m', 'memory': '512Mi'}
                            },
                            'livenessProbe': {
                                'httpGet': {'path': '/health', 'port': 8080},
                                'initialDelaySeconds': 30,
                                'periodSeconds': 10
                            },
                            'readinessProbe': {
                                'httpGet': {'path': '/ready', 'port': 8080},
                                'initialDelaySeconds': 5,
                                'periodSeconds': 5
                            }
                        }]
                    }
                }
            }
        }
    
    def create_service(self,
                       name: str,
                       port: int = 80,
                       target_port: int = 8080,
                       namespace: str = "default") -> Dict:
        """Create Kubernetes service"""
        return {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {'name': name, 'namespace': namespace},
            'spec': {
                'type': 'ClusterIP',
                'selector': {'app': name},
                'ports': [
                    {'protocol': 'TCP', 'port': port, 'targetPort': target_port}
                ]
            }
        }
    
    def create_ingress(self,
                       name: str,
                       host: str,
                       service_name: str,
                       service_port: int = 80,
                       namespace: str = "default") -> Dict:
        """Create Kubernetes ingress"""
        return {
            'apiVersion': 'networking.k8s.io/v1',
            'kind': 'Ingress',
            'metadata': {'name': name, 'namespace': namespace},
            'spec': {
                'rules': [{
                    'host': host,
                    'http': {
                        'paths': [{
                            'path': '/',
                            'pathType': 'Prefix',
                            'backend': {
                                'service': {
                                    'name': service_name,
                                    'port': {'number': service_port}
                                }
                            }
                        }]
                    }
                }]
            }
        }
    
    def create_configmap(self,
                         name: str,
                         data: Dict,
                         namespace: str = "default") -> Dict:
        """Create Kubernetes configmap"""
        return {
            'apiVersion': 'v1',
            'kind': 'ConfigMap',
            'metadata': {'name': name, 'namespace': namespace},
            'data': data
        }
    
    def create_secret(self,
                      name: str,
                      data: Dict,
                      secret_type: str = "Opaque",
                      namespace: str = "default") -> Dict:
        """Create Kubernetes secret"""
        return {
            'apiVersion': 'v1',
            'kind': 'Secret',
            'metadata': {'name': name, 'namespace': namespace},
            'type': secret_type,
            'data': {k: v for k, v in data.items()}
        }
    
    def create_statefulset(self,
                           name: str,
                           image: str,
                           replicas: int = 3,
                           volume_claim_template: str = None) -> Dict:
        """Create Kubernetes statefulset"""
        spec = {
            'serviceName': name,
            'replicas': replicas,
            'selector': {'matchLabels': {'app': name}},
            'template': {
                'metadata': {'labels': {'app': name}},
                'spec': {
                    'containers': [{
                        'name': name,
                        'image': image,
                        'ports': [{'containerPort': 27017}],
                        'volumeMounts': [{'name': 'data', 'mountPath': '/data/db'}]
                    }]
                }
            },
            'volumeClaimTemplates': []
        }
        
        if volume_claim_template:
            spec['volumeClaimTemplates'] = [{
                'metadata': {'name': 'data'},
                'spec': {
                    'accessModes': ['ReadWriteOnce'],
                    'resources': {'requests': {'storage': '10Gi'}}
                }
            }]
        
        return {
            'apiVersion': 'apps/v1',
            'kind': 'StatefulSet',
            'metadata': {'name': name},
            'spec': spec
        }
    
    def create_hpa(self,
                   name: str,
                   min_replicas: int = 2,
                   max_replicas: int = 10,
                   cpu_threshold: int = 70) -> Dict:
        """Create horizontal pod autoscaler"""
        return {
            'apiVersion': 'autoscaling/v2',
            'kind': 'HorizontalPodAutoscaler',
            'metadata': {'name': name},
            'spec': {
                'scaleTargetRef': {
                    'apiVersion': 'apps/v1',
                    'kind': 'Deployment',
                    'name': name
                },
                'minReplicas': min_replicas,
                'maxReplicas': max_replicas,
                'metrics': [{
                    'type': 'Resource',
                    'resource': {
                        'name': 'cpu',
                        'target': {
                            'type': 'Utilization',
                            'averageUtilization': cpu_threshold
                        }
                    }
                }]
            }
        }


class HelmManager:
    """Manage Helm charts and releases"""
    
    def __init__(self):
        self.releases = []
    
    def create_helm_chart(self,
                          name: str,
                          version: str = "0.1.0",
                          dependencies: List[str] = None) -> Dict:
        """Create Helm chart structure"""
        return {
            'name': name,
            'version': version,
            'chart_yaml': {
                'apiVersion': 'v2',
                'name': name,
                'version': version,
                'dependencies': [{'name': dep, 'version': '1.0.0'} for dep in (dependencies or [])]
            },
            'values_yaml': {
                'replicaCount': 3,
                'image': {'repository': name, 'tag': 'latest'},
                'service': {'type': 'ClusterIP', 'port': 80},
                'ingress': {'enabled': False},
                'resources': {
                    'requests': {'cpu': '100m', 'memory': '128Mi'},
                    'limits': {'cpu': '500m', 'memory': '512Mi'}
                }
            },
            'templates': ['deployment.yaml', 'service.yaml', 'ingress.yaml', ' NOTES.txt']
        }
    
    def install_release(self,
                        name: str,
                        chart: str,
                        namespace: str = "default",
                        values: Dict = None) -> Dict:
        """Install Helm release"""
        return {
            'name': name,
            'namespace': namespace,
            'chart': chart,
            'version': 1,
            'status': 'deployed',
            'values': values or {},
            'resources': ['deployment', 'service', 'configmap'],
            'installed_at': datetime.now().isoformat()
        }
    
    def upgrade_release(self,
                        name: str,
                        chart: str,
                        version: int = 2) -> Dict:
        """Upgrade Helm release"""
        return {
            'name': name,
            'version': version,
            'chart': chart,
            'status': 'deployed',
            'diff': {
                'changed': ['image.tag', 'replicaCount'],
                'added': ['resources.limits'],
                'removed': []
            }
        }
    
    def rollback_release(self,
                         name: str,
                         revision: int = 1) -> Dict:
        """Rollback Helm release"""
        return {
            'name': name,
            'rollback_to': revision,
            'status': 'deployed',
            'message': f'Rolled back to revision {revision}'
        }


class K8sSecurityManager:
    """Manage Kubernetes security"""
    
    def __init__(self):
        self.policies = []
    
    def create_network_policy(self,
                              name: str,
                              namespace: str,
                              pod_selector: Dict,
                              ingress_rules: List[Dict] = None,
                              egress_rules: List[Dict] = None) -> Dict:
        """Create network policy"""
        return {
            'apiVersion': 'networking.k8s.io/v1',
            'kind': 'NetworkPolicy',
            'metadata': {'name': name, 'namespace': namespace},
            'spec': {
                'podSelector': pod_selector,
                'policyTypes': ['Ingress', 'Egress'],
                'ingress': ingress_rules or [{'from': [{'podSelector': {}}]}],
                'egress': egress_rules or []
            }
        }
    
    def create_rbac_policy(self,
                           name: str,
                           role_type: str = "Role",
                           resources: List[str] = None,
                           verbs: List[str] = None) -> Dict:
        """Create RBAC policy"""
        return {
            'apiVersion': 'rbac.authorization.k8s.io/v1',
            'kind': role_type,
            'metadata': {'name': name},
            'rules': [{
                'apiGroups': [''],
                'resources': resources or ['pods', 'services'],
                'verbs': verbs or ['get', 'list', 'watch']
            }]
        }
    
    def create_pod_security_policy(self,
                                   name: str,
                                   privileged: bool = False) -> Dict:
        """Create pod security policy"""
        return {
            'apiVersion': 'policy/v1beta1',
            'kind': 'PodSecurityPolicy',
            'metadata': {'name': name},
            'spec': {
                'privileged': privileged,
                'allowPrivilegeEscalation': False,
                'requiredDropCapabilities': ['ALL'],
                'volumes': ['configMap', 'emptyDir', 'secret', 'downwardAPI'],
                'hostNetwork': False,
                'hostPID': False,
                'hostIPC': False,
                'runAsUser': {'rule': 'MustRunAsNonRoot'},
                'seLinux': {'rule': 'RunAsAny'},
                'supplementalGroups': {'rule': 'MustRunAs', 'ranges': [{'min': 10000, 'max': 10000}]}
            }
        }


class ClusterManager:
    """Manage Kubernetes cluster operations"""
    
    def __init__(self):
        self.nodes = []
    
    def get_cluster_health(self) -> Dict:
        """Check cluster health"""
        return {
            'timestamp': datetime.now().isoformat(),
            'control_plane': {'status': 'healthy', 'components': ['etcd', 'scheduler', 'controller-manager']},
            'nodes': {
                'total': 6,
                'ready': 5,
                'not_ready': 1,
                'cpu_utilization': 0.65,
                'memory_utilization': 0.72
            },
            'components': {
                'kube-proxy': 'Healthy',
                'coredns': 'Healthy',
                'metrics-server': 'Healthy'
            },
            'events': [
                {'type': 'Warning', 'reason': 'NodeNotReady', 'message': 'Node memory pressure'}
            ]
        }
    
    def scale_deployment(self,
                         name: str,
                         replicas: int,
                         namespace: str = "default") -> Dict:
        """Scale deployment"""
        return {
            'deployment': name,
            'namespace': namespace,
            'previous_replicas': 3,
            'new_replicas': replicas,
            'scaling_time': datetime.now().isoformat(),
            'status': 'completed'
        }
    
    def drain_node(self,
                   node_name: str,
                   delete_pods: bool = True,
                   timeout: int = 600) -> Dict:
        """Drain node for maintenance"""
        return {
            'node': node_name,
            'delete_pods': delete_pods,
            'timeout_seconds': timeout,
            'evicted_pods': ['pod-1', 'pod-2'],
            'status': 'completed',
            'drain_time': datetime.now().isoformat()
        }
    
    def rolling_update(self,
                       name: str,
                       image: str,
                       max_surge: str = "25%",
                       max_unavailable: str = "25%") -> Dict:
        """Perform rolling update"""
        return {
            'deployment': name,
            'new_image': image,
            'strategy': 'RollingUpdate',
            'max_surge': max_surge,
            'max_unavailable': max_unavailable,
            'updated_replicas': 2,
            'ready_replicas': 1,
            'available_replicas': 1,
            'unavailable_replicas': 1,
            'status': 'in_progress'
        }
    
    def backup_etcd(self,
                    backup_path: str) -> Dict:
        """Backup etcd cluster"""
        return {
            'backup_path': backup_path,
            'snapshot_size_mb': 150,
            'created_at': datetime.now().isoformat(),
            'retention': '30 days',
            'status': 'completed'
        }


if __name__ == "__main__":
    k8s = KubernetesManager()
    
    deployment = k8s.create_deployment("webapp", "nginx:latest", replicas=3)
    print(f"Deployment: {deployment['metadata']['name']}")
    
    service = k8s.create_service("webapp-service", port=80, target_port=8080)
    print(f"Service: {service['metadata']['name']}")
    
    ingress = k8s.create_ingress("webapp-ingress", "app.example.com", "webapp-service")
    print(f"Ingress: {ingress['metadata']['name']}")
    
    configmap = k8s.create_configmap("app-config", {"database.url": "postgres://db:5432"})
    print(f"ConfigMap: {configmap['metadata']['name']}")
    
    hpa = k8s.create_hpa("webapp", min_replicas=2, max_replicas=10)
    print(f"HPA: {hpa['metadata']['name']}")
    
    helm = HelmManager()
    chart = helm.create_helm_chart("my-app", version="1.0.0")
    print(f"Chart: {chart['name']} v{chart['version']}")
    
    release = helm.install_release("my-app", "my-chart", namespace="production")
    print(f"Release: {release['name']} v{release['version']}")
    
    security = K8sSecurityManager()
    network_policy = security.create_network_policy(
        "default-deny",
        namespace="production",
        pod_selector={'app': 'webapp'}
    )
    print(f"NetworkPolicy: {network_policy['metadata']['name']}")
    
    cluster = ClusterManager()
    health = cluster.get_cluster_health()
    print(f"Cluster ready nodes: {health['nodes']['ready']}/{health['nodes']['total']}")
