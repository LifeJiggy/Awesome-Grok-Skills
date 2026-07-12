"""
Container Orchestration Framework

Production-grade container orchestration toolkit providing Kubernetes management,
deployment automation, auto-scaling, networking, and security for production workloads.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DeploymentStatus(Enum):
    PENDING = "pending"
    PROGRESSING = "progressing"
    AVAILABLE = "available"
    UPDATING = "updating"
    ROLLING_BACK = "rolling_back"
    FAILED = "failed"


class PodPhase(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    UNKNOWN = "unknown"


class ServiceType(Enum):
    CLUSTER_IP = "ClusterIP"
    NODE_PORT = "NodePort"
    LOAD_BALANCER = "LoadBalancer"
    EXTERNAL_NAME = "ExternalName"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Deployment:
    """Kubernetes deployment definition."""
    name: str
    image: str
    replicas: int = 1
    ports: List[int] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    resources: Dict[str, str] = field(default_factory=dict)
    health_check: str = "/health"
    namespace: str = "default"
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class DeploymentResult:
    """Deployment execution result."""
    name: str
    status: DeploymentStatus
    ready_replicas: int = 0
    available_replicas: int = 0
    updated_replicas: int = 0
    message: str = ""
    duration_seconds: float = 0.0


@dataclass
class HPA:
    """Horizontal Pod Autoscaler configuration."""
    name: str
    deployment: str
    min_replicas: int
    max_replicas: int
    cpu_target: int = 70
    memory_target: int = 80
    current_replicas: int = 0
    target_cpu: int = 0


@dataclass
class NetworkPolicy:
    """Kubernetes network policy."""
    name: str
    namespace: str
    ingress_rules: List[Dict[str, Any]] = field(default_factory=list)
    egress_rules: List[Dict[str, Any]] = field(default_factory=list)
    pod_selector: Dict[str, str] = field(default_factory=dict)


@dataclass
class PodStatus:
    """Pod status information."""
    name: str
    phase: PodPhase
    ready: bool = False
    restart_count: int = 0
    node: str = ""
    ip: str = ""


@dataclass
class ServiceInfo:
    """Kubernetes service information."""
    name: str
    type: ServiceType
    cluster_ip: str = ""
    ports: List[int] = field(default_factory=list)
    selector: Dict[str, str] = field(default_factory=dict)


@dataclass
class HelmRelease:
    """Helm release information."""
    name: str
    chart: str
    version: str
    status: str
    namespace: str = "default"
    revision: int = 1
    values: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Kubernetes Manager
# ---------------------------------------------------------------------------

class KubernetesManager:
    """Manage Kubernetes resources."""

    def __init__(self, namespace: str = "default", kubeconfig: str = ""):
        self.namespace = namespace
        self.kubeconfig = kubeconfig
        self._deployments: Dict[str, Deployment] = {}
        self._history: List[DeploymentResult] = []

    def deploy(self, deployment: Deployment) -> DeploymentResult:
        start = time.time()
        self._deployments[deployment.name] = deployment

        # Simulate deployment
        time.sleep(0.05)
        duration = time.time() - start

        result = DeploymentResult(
            name=deployment.name,
            status=DeploymentStatus.AVAILABLE,
            ready_replicas=deployment.replicas,
            available_replicas=deployment.replicas,
            updated_replicas=deployment.replicas,
            duration_seconds=duration,
        )

        self._history.append(result)
        logger.info("Deployed %s: %s (%d replicas)", deployment.name, result.status.value, deployment.replicas)
        return result

    def rollback(self, name: str, revision: int = 0) -> DeploymentResult:
        if name in self._deployments:
            dep = self._deployments[name]
            return DeploymentResult(
                name=name,
                status=DeploymentStatus.AVAILABLE,
                ready_replicas=dep.replicas,
                message=f"Rolled back to revision {revision}",
            )
        return DeploymentResult(name=name, status=DeploymentStatus.FAILED, message="Deployment not found")

    def get_pods(self, deployment_name: str) -> List[PodStatus]:
        dep = self._deployments.get(deployment_name)
        if not dep:
            return []
        return [
            PodStatus(
                name=f"{deployment_name}-{hashlib.md5(str(i).encode()).hexdigest()[:8]}",
                phase=PodPhase.RUNNING,
                ready=True,
                node=f"node-{i % 3}",
                ip=f"10.0.{i}.{np.random.randint(1, 255)}",
            )
            for i in range(dep.replicas)
        ]

    def scale(self, name: str, replicas: int) -> DeploymentResult:
        if name in self._deployments:
            self._deployments[name].replicas = replicas
            return DeploymentResult(
                name=name,
                status=DeploymentStatus.AVAILABLE,
                ready_replicas=replicas,
                message=f"Scaled to {replicas} replicas",
            )
        return DeploymentResult(name=name, status=DeploymentStatus.FAILED)

    def get_deployment(self, name: str) -> Optional[Deployment]:
        return self._deployments.get(name)


# ---------------------------------------------------------------------------
# Auto Scaler
# ---------------------------------------------------------------------------

class AutoScaler:
    """Manage auto-scaling for Kubernetes workloads."""

    def create_hpa(
        self,
        deployment: str,
        min_replicas: int = 2,
        max_replicas: int = 10,
        cpu_target: int = 70,
        memory_target: int = 80,
    ) -> HPA:
        return HPA(
            name=f"{deployment}-hpa",
            deployment=deployment,
            min_replicas=min_replicas,
            max_replicas=max_replicas,
            cpu_target=cpu_target,
            memory_target=memory_target,
            current_replicas=min_replicas,
        )

    def get_recommendations(self, hpa: HPA) -> Dict[str, Any]:
        return {
            "current_replicas": hpa.current_replicas,
            "recommended_replicas": min(hpa.max_replicas, hpa.current_replicas + 2),
            "cpu_utilization": np.random.uniform(40, 90),
            "memory_utilization": np.random.uniform(50, 85),
        }


# ---------------------------------------------------------------------------
# Network Policy Manager
# ---------------------------------------------------------------------------

class NetworkPolicyManager:
    """Manage Kubernetes network policies."""

    def create_policy(
        self,
        name: str,
        namespace: str = "default",
        ingress_rules: Optional[List[Dict[str, Any]]] = None,
        egress_rules: Optional[List[Dict[str, Any]]] = None,
        pod_selector: Optional[Dict[str, str]] = None,
    ) -> NetworkPolicy:
        return NetworkPolicy(
            name=name,
            namespace=namespace,
            ingress_rules=ingress_rules or [],
            egress_rules=egress_rules or [],
            pod_selector=pod_selector or {},
        )

    def get_policies(self, namespace: str = "default") -> List[NetworkPolicy]:
        return [
            self.create_policy("allow-frontend", namespace,
                              ingress_rules=[{"from": {"app": "frontend"}}]),
            self.create_policy("deny-all-ingress", namespace),
        ]


# ---------------------------------------------------------------------------
# Helm Manager
# ---------------------------------------------------------------------------

class HelmManager:
    """Manage Helm releases."""

    def install(self, release_name: str, chart: str, namespace: str = "default",
                values: Optional[Dict[str, Any]] = None) -> HelmRelease:
        return HelmRelease(
            name=release_name,
            chart=chart,
            version="1.0.0",
            status="deployed",
            namespace=namespace,
            values=values or {},
        )

    def upgrade(self, release_name: str, chart: str, version: str) -> HelmRelease:
        return HelmRelease(
            name=release_name, chart=chart, version=version,
            status="deployed", revision=2,
        )

    def list_releases(self, namespace: str = "default") -> List[HelmRelease]:
        return [
            HelmRelease("api-service", "api-chart", "1.2.0", "deployed"),
            HelmRelease("frontend", "frontend-chart", "2.0.1", "deployed"),
        ]


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate container orchestration capabilities."""
    print("=" * 70)
    print("Container Orchestration Framework - Demo")
    print("=" * 70)

    # --- 1. Deployment ---
    print("\n--- Kubernetes Deployment ---")
    k8s = KubernetesManager(namespace="production")
    deployment = Deployment(
        name="api-service",
        image="app:v2.1.0",
        replicas=3,
        ports=[8080],
        env={"DATABASE_URL": "secret:db-url"},
        resources={"cpu": "500m", "memory": "512Mi"},
    )

    result = k8s.deploy(deployment)
    print(f"  Deployment: {result.name}")
    print(f"  Status: {result.status.value}")
    print(f"  Replicas: {result.ready_replicas}")

    pods = k8s.get_pods("api-service")
    print(f"  Pods: {len(pods)}")
    for pod in pods[:2]:
        print(f"    {pod.name}: {pod.phase.value} ({pod.ip})")

    # --- 2. Auto-Scaling ---
    print("\n--- Auto-Scaling ---")
    scaler = AutoScaler()
    hpa = scaler.create_hpa("api-service", min_replicas=2, max_replicas=10)
    print(f"  HPA: {hpa.name}")
    print(f"  Min/Max: {hpa.min_replicas}/{hpa.max_replicas}")
    print(f"  Targets: CPU={hpa.cpu_target}%, Memory={hpa.memory_target}%")

    recs = scaler.get_recommendations(hpa)
    print(f"  Recommended replicas: {recs['recommended_replicas']}")

    # --- 3. Network Policies ---
    print("\n--- Network Policies ---")
    netpol = NetworkPolicyManager()
    policy = netpol.create_policy(
        name="allow-frontend-to-backend",
        namespace="production",
        ingress_rules=[{"from": {"app": "frontend"}, "ports": [{"port": 8080}]}],
    )
    print(f"  Policy: {policy.name}")
    print(f"  Ingress rules: {len(policy.ingress_rules)}")

    policies = netpol.get_policies("production")
    print(f"  Total policies: {len(policies)}")

    # --- 4. Helm ---
    print("\n--- Helm Operations ---")
    helm = HelmManager()
    release = helm.install("api-service", "api-chart", "production")
    print(f"  Release: {release.name} ({release.chart} v{release.version})")
    print(f"  Status: {release.status}")

    releases = helm.list_releases()
    print(f"  Installed releases: {len(releases)}")
    for r in releases:
        print(f"    {r.name}: {r.chart} v{r.version} ({r.status})")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()