# Kubernetes

## Overview

Kubernetes is the de facto standard for container orchestration, automating the deployment, scaling, and management of containerized applications. This skill covers Kubernetes architecture, resource definitions, networking, storage, and operational tooling. Kubernetes enables declarative infrastructure where desired state is specified and the system automatically works to achieve and maintain it.

## Core Capabilities

Workload resources including Deployments, StatefulSets, DaemonSets, Jobs, and CronJobs manage containerized applications. Services provide stable network endpoints for accessing pods. Ingress controllers expose HTTP/HTTPS routes with TLS termination and path-based routing. ConfigMaps and Secrets decouple configuration from container images.

PersistentVolumeClaims provide durable storage for stateful applications. HorizontalPodAutoscaler automatically adjusts replica counts based on metrics. PodDisruptionBudgets ensure availability during maintenance. NetworkPolicies control traffic flow between pods. RBAC governs user and service account permissions.

## Usage Examples

```python
from kubernetes import Kubernetes

k8s = Kubernetes()

k8s.create_cluster(
    name="production-cluster",
    version="1.28",
    provider="AWS"
)

k8s.add_node(
    node_name="worker-node-1",
    node_type="worker",
    zone="us-east-1a",
    labels={"node-type": "general-purpose"},
    taints=[{"key": "workload", "value": "production", "effect": "NoSchedule"}]
)

k8s.create_namespace(
    namespace_name="production",
    resource_quotas={"cpu": "100", "memory": "200Gi"},
    limit_ranges={"cpu": {"default": "500m", "default_request": "100m"}}
)

deployment = k8s.create_deployment(
    name="api-server",
    namespace="production",
    image="myregistry/api-server:v2.1.0",
    replicas=3,
    labels={"app": "api-server", "version": "v2"}
)

k8s.add_container_port(
    deployment,
    port="main",
    container_port=8080,
    protocol="TCP"
)

k8s.add_resource_limits(
    deployment,
    cpu_limit="1000m",
    memory_limit="1Gi",
    cpu_request="500m",
    memory_request="512Mi"
)

k8s.add_liveness_probe(
    deployment,
    probe_type="httpGet",
    path="/health",
    port=8080
)

k8s.add_readiness_probe(
    deployment,
    probe_type="httpGet",
    path="/ready",
    port=8080
)

service = k8s.create_service(
    name="api-server",
    namespace="production",
    service_type="ClusterIP",
    selector={"app": "api-server"},
    ports=[{"port": 80, "target_port": 8080, "protocol": "TCP"}]
)

configmap = k8s.create_configmap(
    name="api-config",
    namespace="production",
    literals={
        "DATABASE_URL": "postgresql://db:5432/myapp",
        "CACHE_URL": "redis://cache:6379",
        "LOG_LEVEL": "info"
    }
)

secret = k8s.create_secret(
    name="api-secrets",
    namespace="production",
    secret_type="Opaque",
    string_data={
        "DATABASE_PASSWORD": "secret_password",
        "API_KEY": "api_key_value"
    }
)

ingress = k8s.create_ingress(
    name="api-ingress",
    namespace="production"
)

k8s.add_ingress_rule(
    ingress,
    host="api.example.com",
    path="/",
    service_name="api-server",
    service_port=80
)

pvc = k8s.create_persistent_volume_claim(
    name="api-data",
    namespace="production",
    storage_size="10Gi",
    access_modes=["ReadWriteOnce"]
)

statefulset = k8s.create_statefulset(
    name="postgres",
    namespace="production",
    image="postgres:15",
    replicas=1,
    volume_claims=[pvc]
)

daemonset = k8s.create_daemonset(
    name="log-collector",
    namespace="production",
    image="fluent/fluent-bit:2.2",
    labels={"app": "log-collector"}
)

job = k8s.create_job(
    name="database-migration",
    namespace="production",
    image="myregistry/api-server:migration",
    completions=1,
    backoff_limit=3
)

cronjob = k8s.create_cronjob(
    name="daily-backup",
    namespace="production",
    image="myregistry/backup-tool:v1",
    schedule="0 2 * * *",
    concurrency_policy="Forbid"
)

hpa = k8s.create_hpa(
    name="api-server-hpa",
    namespace="production",
    deployment_name="api-server",
    min_replicas=3,
    max_replicas=20,
    cpu_threshold=70
)

network_policy = k8s.create_network_policy(
    name="api-network-policy",
    namespace="production",
    pod_selector={"app": "api-server"},
    ingress_rules=[{
        "from": [{"pod_selector": {"match_labels": {"app": "frontend"}}}],
        "ports": [{"protocol": "TCP", "port": 8080}]
    }],
    egress_rules=[{
        "to": [{"namespace_selector": {"match_labels": {"name": "database"}}}],
        "ports": [{"protocol": "TCP", "port": 5432}]
    }]
)

service_account = k8s.create_service_account(
    name="api-server-sa",
    namespace="production",
    automount_token=True
)

role = k8s.create_rbac_role(
    name="api-server-role",
    namespace="production",
    rules=[{
        "api_groups": [""],
        "resources": ["configmaps", "secrets"],
        "verbs": ["get", "list", "watch"]
    }]
)

cluster_role = k8s.create_rbac_cluster_role(
    name="node-reader",
    rules=[{
        "api_groups": [""],
        "resources": ["nodes"],
        "verbs": ["get", "list", "watch"]
    }]
)

role_binding = k8s.create_role_binding(
    name="api-server-binding",
    namespace="production",
    role_name="api-server-role",
    subjects=[{
        "kind": "ServiceAccount",
        "name": "api-server-sa",
        "namespace": "production"
    }]
)
```

## Best Practices

Use namespaces to organize and isolate resources. Set resource requests and limits for all containers. Implement liveness and readiness probes for reliable deployments. Use labels and annotations to organize and identify resources.

Implement network policies to restrict traffic flow. Use PodDisruptionBudgets for maintenance safety. Automate deployments with GitOps approaches. Monitor cluster and application metrics. Regularly update Kubernetes and add-on components.

## Related Skills

- Docker (container fundamentals)
- Container Orchestration (container management)
- CI/CD Pipelines (automation workflows)
- Cloud Architecture (cloud-native design)

## Use Cases

Microservices orchestration coordinates many independent services with service discovery and load balancing. Batch job processing handles periodic and one-time workloads reliably. Stateful applications like databases run with persistent storage and ordered deployment. Machine learning workloads scale GPU resources for model training and inference. Edge computing extends Kubernetes to distributed locations.
