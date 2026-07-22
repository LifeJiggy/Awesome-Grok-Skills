---
name: "Container Orchestration"
version: "2.0.0"
description: "Comprehensive container orchestration toolkit with Kubernetes management, deployment automation, scaling, networking, and security for production container workloads"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["devops", "kubernetes", "containers", "orchestration", "scaling", "deployment"]
category: "devops"
personality: "container-engineer"
use_cases: ["Kubernetes management", "deployment automation", "auto-scaling", "networking", "security"]
---

# Container Orchestration

> Production-grade container orchestration framework providing Kubernetes management, deployment automation, auto-scaling, networking configuration, and security policies for production container workloads.

## Overview

The Container Orchestration module provides a complete toolkit for managing containerized applications. It implements Kubernetes resource management, deployment strategies, Horizontal Pod Autoscaler configuration, NetworkPolicy management, RBAC setup, and Helm chart operations. Every operation includes health monitoring, rollback capability, and audit logging.

## Core Capabilities

### 1. Kubernetes Resource Management
- Deployment, Service, ConfigMap, Secret management
- Pod lifecycle management
- Namespace management
- Resource quota enforcement
- Label and annotation management

### 2. Deployment Automation
- Rolling update configuration
- Blue-green and canary deployments
- Rollback procedures
- Deployment history tracking
- Health check configuration

### 3. Auto-Scaling
- Horizontal Pod Autoscaler (HPA)
- Vertical Pod Autoscaler (VPA)
- Cluster Autoscaler integration
- Custom metrics scaling
- Scaling policies

### 4. Networking
- Service mesh configuration
- Ingress management
- NetworkPolicy creation
- DNS configuration
- Load balancing

### 5. Security
- RBAC configuration
- Pod Security Policies
- Network Policies
- Secret management
- Image scanning integration

### 6. Helm Operations
- Chart installation and upgrade
- Release management
- Value overrides
- Chart repository management
- Chart testing

## Usage Examples

### Kubernetes Deployment

```python
from container_orchestration import KubernetesManager, Deployment

manager = KubernetesManager(namespace="production")

# Create deployment
deployment = Deployment(
    name="api-service",
    image="app:v2.1.0",
    replicas=3,
    ports=[8080],
    env={"DATABASE_URL": "secret:db-url"},
    resources={"cpu": "500m", "memory": "512Mi"},
    health_check="/health",
)

result = manager.deploy(deployment)
print(f"Deployment: {result.name}")
print(f"Status: {result.status}")
print(f"Replicas ready: {result.ready_replicas}")
```

### Auto-Scaling

```python
from container_orchestration import AutoScaler

scaler = AutoScaler()

# Configure HPA
hpa = scaler.create_hpa(
    deployment="api-service",
    min_replicas=2,
    max_replicas=10,
    cpu_target=70,
    memory_target=80,
)

print(f"HPA created: {hpa.name}")
print(f"Min/Max: {hpa.min_replicas}/{hpa.max_replicas}")
print(f"Targets: CPU={hpa.cpu_target}%, Memory={hpa.memory_target}%")
```

### Network Policies

```python
from container_orchestration import NetworkPolicyManager

netpol = NetworkPolicyManager()

# Create network policy
policy = netpol.create_policy(
    name="allow-frontend-to-backend",
    namespace="production",
    ingress_rules=[
        {"from": {"podSelector": {"app": "frontend"}}, "ports": [{"port": 8080}]}
    ],
)

print(f"Network policy: {policy.name}")
print(f"Rules: {len(policy.ingress_rules)} ingress rules")
```

## Best Practices

### Deployments
- Use rolling updates with maxUnavailable=25% and maxSurge=25%
- Always set resource requests and limits
- Configure liveness and readiness probes
- Use PodDisruptionBudgets for critical services

### Scaling
- Start with HPA based on CPU/memory
- Tune scaling thresholds based on workload patterns
- Set appropriate cooldown periods
- Monitor scaling events for anomalies

### Networking
- Implement NetworkPolicies to restrict traffic
- Use namespaces for environment isolation
- Configure Ingress with TLS termination
- Monitor network latency between services

### Security
- Run containers as non-root
- Use read-only root filesystem
- Apply Pod Security Standards
- Scan images for vulnerabilities

## Related Modules

- **ci-cd-pipelines**: Pipeline integration for deployments
- **infrastructure-as-code**: Infrastructure management
- **monitoring**: Kubernetes monitoring and alerting
- **site-reliability**: SRE practices for container workloads

---

## Advanced Configuration

### Advanced Kubernetes Deployment

```python
from container_orchestration import KubernetesManager, Deployment, Container

manager = KubernetesManager(namespace="production")

# Advanced deployment configuration
deployment = Deployment(
    name="api-service",
    replicas=3,
    containers=[
        Container(
            name="api",
            image="app:v2.1.0",
            ports=[8080],
            env={"DATABASE_URL": "secret:db-url"},
            resources={"cpu": "500m-1000m", "memory": "512Mi-1Gi"},
            health_check="/health",
            readiness_check="/ready",
            startup_check="/startup",
            security_context={
                "run_as_non_root": True,
                "read_only_root_filesystem": True,
                "capabilities": {"drop": ["ALL"]},
            },
        ),
        Container(
            name="sidecar",
            image="envoy:latest",
            ports=[9901],
            resources={"cpu": "100m", "memory": "128Mi"},
        ),
    ],
    strategy={
        "type": "RollingUpdate",
        "rolling_update": {
            "max_surge": "25%",
            "max_unavailable": "25%",
        },
    },
    affinity={
        "pod_anti_affinity": {
            "preferred_during_scheduling": {
                "weight": 100,
                "pod_affinity_term": {
                    "topology_key": "kubernetes.io/hostname",
                },
            },
        },
    },
    tolerations=[
        {"key": "dedicated", "operator": "Equal", "value": "api", "effect": "NoSchedule"},
    ],
)

result = manager.deploy(deployment)
print(f"Deployment: {result.name}")
print(f"Status: {result.status}")
print(f"Replicas ready: {result.ready_replicas}")
```

### Advanced Auto-Scaling

```python
from container_orchestration import AutoScaler, ScalingPolicy

scaler = AutoScaler()

# Advanced HPA configuration
hpa = scaler.create_hpa(
    deployment="api-service",
    min_replicas=2,
    max_replicas=20,
    metrics=[
        {"type": "Resource", "resource": "cpu", "target": 70},
        {"type": "Resource", "resource": "memory", "target": 80},
        {"type": "Pods", "pod": {"metric": "requests_per_second", "target": 1000}},
        {"type": "Object", "object": {"metric": "queue_length", "target": 100, "api": "custom.metrics.k8s.io"}},
    ],
    behavior={
        "scale_up": {
            "stabilization_window_seconds": 60,
            "select_policy": "Max",
            "policies": [
                {"type": "Percent", "value": 100, "period_seconds": 60},
                {"type": "Pods", "value": 4, "period_seconds": 60},
            ],
        },
        "scale_down": {
            "stabilization_window_seconds": 300,
            "select_policy": "Min",
            "policies": [
                {"type": "Percent", "value": 10, "period_seconds": 60},
            ],
        },
    },
)

# Create PDB
pdb = scaler.create_pdb(
    name="api-service-pdb",
    min_available=2,
    selector={"app": "api-service"},
)

print(f"HPA created: {hpa.name}")
print(f"PDB created: {pdb.name}")
```

### Advanced Network Policies

```python
from container_orchestration import NetworkPolicyManager

netpol = NetworkPolicyManager()

# Create comprehensive network policy
policy = netpol.create_policy(
    name="api-service-network-policy",
    namespace="production",
    pod_selector={"app": "api-service"},
    ingress_rules=[
        {
            "from": [
                {"namespace_selector": {"match_labels": {"environment": "production"}}},
                {"pod_selector": {"match_labels": {"app": "frontend"}}},
            ],
            "ports": [{"port": 8080, "protocol": "TCP"}],
        },
    ],
    egress_rules=[
        {
            "to": [
                {"namespace_selector": {"match_labels": {"environment": "production"}}},
            ],
            "ports": [
                {"port": 5432, "protocol": "TCP"},  # PostgreSQL
                {"port": 6379, "protocol": "TCP"},  # Redis
            ],
        },
        {
            "to": [
                {"ip_block": {"cidr": "0.0.0.0/0", "except": ["10.0.0.0/8"]}},
            ],
            "ports": [{"port": 443, "protocol": "TCP"}],
        },
    ],
)

print(f"Network policy: {policy.name}")
print(f"Ingress rules: {len(policy.ingress_rules)}")
print(f"Egress rules: {len(policy.egress_rules)}")
```

## Architecture Patterns

### Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Kubernetes Architecture                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Control Plane                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  API Server │  │  Scheduler  │  │  Controller  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Worker Nodes                            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Node 1     │  │  Node 2     │  │  Node 3     │ │   │
│  │  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │ │   │
│  │  │  │ Pods  │  │  │  │ Pods  │  │  │  │ Pods  │  │ │   │
│  │  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Helm Integration

```python
from container_orchestration import HelmManager

helm = HelmManager()

# Install chart with values
result = helm.install(
    release="api-service",
    chart="bitnami/nginx",
    namespace="production",
    values={
        "replicaCount": 3,
        "image": {"repository": "app", "tag": "v2.1.0"},
        "service": {"type": "ClusterIP", "port": 8080},
        "ingress": {"enabled": True, "hosts": ["api.example.com"]},
    },
)

print(f"Release: {result.release}")
print(f"Status: {result.status}")
print(f"Revision: {result.revision}")
```

## Performance Optimization

### Kubernetes Performance

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Pod startup time | < 30s | 30-60s | > 60s |
| Deployment rollout | < 5min | 5-10min | > 10min |
| HPA scale-up time | < 2min | 2-5min | > 5min |
| Node utilization | 60-80% | 80-90% | > 90% |

## Security Considerations

### Pod Security

```python
from container_orchestration import SecurityPolicy

security = SecurityPolicy()

# Create Pod Security Policy
psp = security.create_psp(
    name="restricted",
    privileged=False,
    allow_privilege_escalation=False,
    required_drop_capabilities=["ALL"],
    run_as_user={"rule": "MustRunAsNonRoot"},
    seccomp_profile={"type": "RuntimeDefault"},
)

print(f"PSP: {psp.name}")
print(f"Privileged: {psp.privileged}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Pod not starting | CrashLoopBackOff | Check logs, resource limits |
| Service unreachable | Connection refused | Check endpoints, network policies |
| HPA not scaling | Metrics not available | Verify metrics server |
| Node pressure | Pods evicted | Add nodes, adjust resource requests |

## API Reference

### KubernetesManager

```python
class KubernetesManager:
    def __init__(self, namespace: str = "default")
    def deploy(self, deployment: Deployment) -> DeploymentResult
    def scale(self, name: str, replicas: int) -> ScaleResult
    def rollback(self, name: str) -> RollbackResult
    def get_status(self, name: str) -> DeploymentStatus
    def get_pods(self, selector: dict = None) -> list[Pod]
    def get_events(self, **kwargs) -> list[Event]
```

### AutoScaler

```python
class AutoScaler:
    def __init__(self)
    def create_hpa(self, **kwargs) -> HPA
    def create_vpa(self, **kwargs) -> VPA
    def create_pdb(self, **kwargs) -> PDB
    def get_metrics(self, deployment: str) -> ScalingMetrics
    def get_recommendations(self, deployment: str) -> list[ScalingRecommendation]
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class PodPhase(Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    UNKNOWN = "Unknown"

@dataclass
class Pod:
    name: str
    namespace: str
    phase: PodPhase
    node: str
    ip: str
    restart_count: int
    containers: List['ContainerStatus']

@dataclass
class DeploymentResult:
    name: str
    status: str
    ready_replicas: int
    available_replicas: int
    conditions: List['Condition']
```

## Deployment Guide

### Installation

```bash
pip install container-orchestration
```

## Monitoring & Observability

### Metrics Collection

```python
from container_orchestration import MetricsCollector

collector = MetricsCollector()

# Collect Kubernetes metrics
collector.gauge("k8s.pod.count", count, tags={"deployment": deployment})
collector.gauge("k8s.node.utilization", utilization)
collector.counter("k8s.deployment.total", count, tags={"status": status})
collector.histogram("k8s.pod.restart.count", count)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from container_orchestration import KubernetesManager, AutoScaler

@pytest.fixture
def manager():
    return KubernetesManager(namespace="test")

def test_deploy(manager):
    deployment = Deployment(name="test", image="nginx:latest", replicas=1)
    result = manager.deploy(deployment)
    assert result.status == "success"
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Kubernetes | 1.24 | 1.28+ |
| Helm | 3.0 | 3.13+ |

## Glossary

| Term | Definition |
|------|------------|
| **Pod** | Smallest deployable unit |
| **Deployment** | Manages pod replicas |
| **Service** | Network endpoint for pods |
| **HPA** | Horizontal Pod Autoscaler |
| **PDB** | Pod Disruption Budget |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added advanced HPA configuration
- New network policy manager
- Improved security policies
- Added Helm integration

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/container-orchestration.git
cd container-orchestration
pip install -e ".[dev]"
pytest
```

## Advanced Topics

### StatefulSet Management

```python
from container_orchestration import StatefulSetManager

manager = StatefulSetManager(namespace="production")

# Create StatefulSet for database cluster
statefulset = manager.create(
    name="postgres-cluster",
    image="postgres:16",
    replicas=3,
    volume_claim_templates=[
        {
            "name": "data",
            "storage": "100Gi",
            "storage_class": "fast-ssd",
            "access_modes": ["ReadWriteOnce"],
        }
    ],
    service_name="postgres-headless",
    pod_management_policy="OrderedReady",
    update_strategy={"type": "RollingUpdate"},
)

print(f"StatefulSet: {statefulset.name}")
print(f"Replicas: {statefulset.current_replicas}/{statefulset.desired_replicas}")
print(f"Volume claims: {len(statefulset.volume_claims)}")
```

### DaemonSet Operations

```python
from container_orchestration import DaemonSetManager

dsm = DaemonSetManager()

# Deploy monitoring agent across all nodes
daemonset = dsm.deploy(
    name="fluentd-logging",
    image="fluentd:v1.16",
    namespace="monitoring",
    node_selector={"node-type": "worker"},
    tolerations=[
        {"key": "node-role.kubernetes.io/control-plane", "operator": "Exists", "effect": "NoSchedule"}
    ],
    update_strategy={"type": "RollingUpdate", "max_unavailable": 1},
    resources={"cpu": "100m", "memory": "256Mi"},
)

print(f"DaemonSet: {daemonset.name}")
print(f"Nodes running: {daemonset.current_nodes}/{daemonset.desired_nodes}")
print(f"Ready: {daemonset.ready_nodes}")
```

### Service Mesh Configuration

| Feature | Istio | Linkerd | Consul Connect |
|---------|-------|---------|----------------|
| mTLS | Automatic | Automatic | Optional |
| Traffic management | Advanced | Basic | Moderate |
| Observability | Rich | Moderate | Rich |
| Sidecar proxy | Envoy | Linkerd-proxy | Envoy |
| Resource overhead | High | Low | Moderate |
| Learning curve | Steep | Moderate | Moderate |

```python
from container_orchestration import ServiceMesh

mesh = ServiceMesh(provider="istio")

# Configure traffic splitting for canary deployment
mesh.configure_traffic(
    service="api-service",
    rules=[
        {"match": {"headers": {"x-canary": {"exact": "true"}}}, "route": {"weight": 100}},
        {"match": {}, "route": {"routes": [{"destination": "api-service-v1", "weight": 90}, {"destination": "api-service-v2", "weight": 10}]}},
    ],
)

# Enable mutual TLS
mesh.enable_mtls(namespace="production")

print(f"mTLS enabled: {mesh.mtls_status}")
print(f"Traffic rules: {mesh.rule_count}")
```

### Multi-Cluster Management

```python
from container_orchestration import MultiClusterManager

mcm = MultiClusterManager()

# Register clusters
mcm.register_cluster(name="us-east", endpoint="https://us-east.k8s.example.com")
mcm.register_cluster(name="eu-west", endpoint="https://eu-west.k8s.example.com")

# Federate services across clusters
federation = mcm.federate_service(
    name="global-api",
    clusters=["us-east", "eu-west"],
    load_balancing="geo-aware",
    failover="automatic",
)

print(f"Federated service: {federation.name}")
print(f"Clusters: {len(federation.clusters)}")
print(f"Load balancing: {federation.load_balancing}")
```

### Custom Resource Definitions

```python
from container_orchestration import CRDManager

crd_mgr = CRDManager()

# Define custom resource for application config
crd = crd_mgr.create_crd(
    name="appconfig",
    group="platform.example.com",
    version="v1alpha1",
    scope="Namespaced",
    names={"plural": "appconfigs", "singular": "appconfig", "kind": "AppConfig"},
    validation={
        "openAPIV3Schema": {
            "type": "object",
            "properties": {
                "spec": {"type": "object", "properties": {
                    "replicas": {"type": "integer", "minimum": 1},
                    "image": {"type": "string"},
                    "env": {"type": "object"},
                }, "required": ["replicas", "image"]},
            },
        },
    },
)

print(f"CRD: {crd.name}")
print(f"Group: {crd.group}")
print(f"Version: {crd.version}")
```

### Pod Disruption Budget Strategy

| Scenario | minAvailable | maxUnavailable | Use Case |
|----------|-------------|----------------|----------|
| Critical service | 2 | - | Payment processing |
| Standard service | 1 | 25% | API servers |
| Batch workload | 0 | 100% | Data processing |
| HA database | 2 | 1 | Database cluster |

```python
from container_orchestration import PDBManager

pdb_mgr = PDBManager()

# Create PDB for critical service
pdb = pdb_mgr.create(
    name="api-service-pdb",
    namespace="production",
    selector={"app": "api-service"},
    min_available=2,
)

# Create PDB with maxUnavailable
pdb2 = pdb_mgr.create(
    name="worker-pdb",
    namespace="production",
    selector={"app": "worker"},
    max_unavailable="25%",
)

print(f"PDB 1: {pdb.name}, minAvailable: {pdb.min_available}")
print(f"PDB 2: {pdb2.name}, maxUnavailable: {pdb2.max_unavailable}")
```

### Namespace Resource Quotas

```python
from container_orchestration import ResourceQuotaManager

quota_mgr = ResourceQuotaManager()

# Set resource quotas for namespace
quota = quota_mgr.create(
    name="production-quota",
    namespace="production",
    hard={
        "requests.cpu": "20",
        "requests.memory": "40Gi",
        "limits.cpu": "40",
        "limits.memory": "80Gi",
        "pods": "50",
        "services": "20",
        "persistentvolumeclaims": "10",
        "configmaps": "50",
        "secrets": "50",
    },
)

print(f"Quota: {quota.name}")
print(f"CPU request: {quota.used['requests.cpu']}/{quota.hard['requests.cpu']}")
print(f"Memory request: {quota.used['requests.memory']}/{quota.hard['requests.memory']}")
```

## Production Runbooks

### Pod CrashLoopBackOff Recovery

| Step | Action | Command |
|------|--------|---------|
| 1 | Check pod logs | `kubectl logs <pod> --previous` |
| 2 | Describe pod events | `kubectl describe pod <pod>` |
| 3 | Check resource limits | `kubectl top pod <pod>` |
| 4 | Verify image exists | `kubectl get events` |
| 5 | Check node health | `kubectl describe node <node>` |
| 6 | Restart if needed | `kubectl delete pod <pod>` |

### Cluster Node Scaling Runbook

```bash
# Check current node status
kubectl get nodes -o wide

# Drain node before removal
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data

# Remove node from cluster
kubectl delete node <node>

# Scale up node group (AWS EKS example)
aws eks update-nodegroup-config --cluster-name prod --nodegroup-name workers --scaling-config minSize=3,maxSize=10,desiredSize=5
```

## Performance Benchmarks

### Pod Lifecycle Timing

| Phase | Target | Typical | Max Acceptable |
|-------|--------|---------|----------------|
| Pending → Running | < 10s | 5s | 30s |
| Container creation | < 5s | 2s | 15s |
| Readiness probe pass | < 10s | 3s | 30s |
| Graceful shutdown | < 30s | 10s | 60s |

### Network Performance

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Pod-to-pod latency | < 1ms | 1-5ms | > 5ms |
| Service latency (P99) | < 50ms | 50-200ms | > 200ms |
| DNS resolution | < 5ms | 5-20ms | > 20ms |
| Ingress latency (P95) | < 100ms | 100-500ms | > 500ms |

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills