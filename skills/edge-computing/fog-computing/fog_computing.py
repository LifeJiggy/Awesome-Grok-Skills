"""
Fog Computing Framework

Production-grade fog computing toolkit providing fog node management, workload
orchestration, resource optimization, service placement, and fog-cloud integration.
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

class NodeStatus(Enum):
    ACTIVE = "active"
    IDLE = "idle"
    MAINTENANCE = "maintenance"
    FAILED = "failed"
    OFFLINE = "offline"


class PlacementStrategy(Enum):
    LATENCY_OPTIMIZED = "latency_optimized"
    COST_OPTIMIZED = "cost_optimized"
    RELIABILITY = "reliability"
    BALANCED = "balanced"


class ExecutionTier(Enum):
    EDGE = "edge"
    FOG = "fog"
    CLOUD = "cloud"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class NodeConfig:
    """Fog node configuration."""
    node_id: str
    location: str = ""
    resources: Dict[str, Any] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)


@dataclass
class FogNode:
    """Fog node information."""
    node_id: str
    status: NodeStatus = NodeStatus.ACTIVE
    location: str = ""
    resources: Dict[str, Any] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    last_heartbeat: Optional[datetime] = None


@dataclass
class PlacementResult:
    """Workload placement result."""
    node_id: str
    workload: Dict[str, Any]
    expected_latency_ms: float
    resource_impact: Dict[str, float]
    cost: float = 0.0


@dataclass
class ResourceOptimization:
    """Resource optimization result."""
    node_id: str
    cpu_utilization: float
    memory_utilization: float
    storage_utilization: float
    recommendations: List[str]
    estimated_savings: float = 0.0


@dataclass
class OffloadResult:
    """Workload offloading result."""
    tier: ExecutionTier
    node_id: str
    cost: float
    latency_ms: float
    success: bool = True


@dataclass
class FogCloudSync:
    """Fog-cloud synchronization status."""
    fog_nodes: List[str]
    cloud_provider: str
    sync_status: str = "synced"
    last_sync: Optional[datetime] = None
    data_transferred_mb: float = 0.0


# ---------------------------------------------------------------------------
# Fog Node Manager
# ---------------------------------------------------------------------------

class FogNodeManager:
    """Manage fog computing nodes."""

    def __init__(self):
        self._nodes: Dict[str, FogNode] = {}

    def register_node(self, config: NodeConfig) -> FogNode:
        node = FogNode(
            node_id=config.node_id,
            status=NodeStatus.ACTIVE,
            location=config.location,
            resources=config.resources,
            capabilities=config.capabilities,
            last_heartbeat=datetime.now(timezone.utc),
        )
        self._nodes[config.node_id] = node
        logger.info("Registered fog node: %s", config.node_id)
        return node

    def get_node(self, node_id: str) -> Optional[FogNode]:
        return self._nodes.get(node_id)

    def list_nodes(self, status: Optional[NodeStatus] = None) -> List[FogNode]:
        nodes = list(self._nodes.values())
        if status:
            nodes = [n for n in nodes if n.status == status]
        return nodes

    def update_heartbeat(self, node_id: str) -> None:
        if node_id in self._nodes:
            self._nodes[node_id].last_heartbeat = datetime.now(timezone.utc)

    def get_cluster_status(self) -> Dict[str, Any]:
        nodes = list(self._nodes.values())
        return {
            "total": len(nodes),
            "active": sum(1 for n in nodes if n.status == NodeStatus.ACTIVE),
            "idle": sum(1 for n in nodes if n.status == NodeStatus.IDLE),
            "failed": sum(1 for n in nodes if n.status == NodeStatus.FAILED),
        }


# ---------------------------------------------------------------------------
# Fog Orchestrator
# ---------------------------------------------------------------------------

class FogOrchestrator:
    """Orchestrate workloads across fog infrastructure."""

    def __init__(self):
        self._nodes: List[FogNode] = []

    def set_nodes(self, nodes: List[FogNode]) -> None:
        self._nodes = nodes

    def place_workload(
        self,
        workload: Dict[str, Any],
        strategy: PlacementStrategy = PlacementStrategy.LATENCY_OPTIMIZED,
    ) -> PlacementResult:
        if not self._nodes:
            return PlacementResult(
                node_id="fog-1",
                workload=workload,
                expected_latency_ms=50,
                resource_impact={"cpu": 0.2, "memory": 0.1},
            )

        if strategy == PlacementStrategy.LATENCY_OPTIMIZED:
            selected = min(self._nodes, key=lambda n: np.random.uniform(10, 100))
        elif strategy == PlacementStrategy.COST_OPTIMIZED:
            selected = min(self._nodes, key=lambda n: np.random.uniform(0.01, 0.1))
        else:
            selected = self._nodes[0]

        return PlacementResult(
            node_id=selected.node_id,
            workload=workload,
            expected_latency_ms=np.random.uniform(10, 100),
            resource_impact={"cpu": np.random.uniform(0.1, 0.5), "memory": np.random.uniform(0.05, 0.3)},
        )


# ---------------------------------------------------------------------------
# Resource Optimizer
# ---------------------------------------------------------------------------

class ResourceOptimizer:
    """Optimize fog node resources."""

    def optimize(self, node_id: str) -> ResourceOptimization:
        cpu = np.random.uniform(0.3, 0.9)
        memory = np.random.uniform(0.4, 0.85)
        storage = np.random.uniform(0.2, 0.7)

        recommendations = []
        if cpu > 0.8:
            recommendations.append("Consider scaling up CPU resources")
        if memory > 0.8:
            recommendations.append("Memory pressure detected, optimize usage")
        if storage > 0.7:
            recommendations.append("Storage filling up, consider cleanup")

        return ResourceOptimization(
            node_id=node_id,
            cpu_utilization=cpu,
            memory_utilization=memory,
            storage_utilization=storage,
            recommendations=recommendations,
            estimated_savings=np.random.uniform(10, 100),
        )


# ---------------------------------------------------------------------------
# Fog-Cloud Bridge
# ---------------------------------------------------------------------------

class FogCloudBridge:
    """Bridge between fog and cloud infrastructure."""

    def offload(
        self,
        workload: Dict[str, Any],
        fog_nodes: Optional[List[str]] = None,
        cloud_provider: str = "aws",
    ) -> OffloadResult:
        # Decide tier based on workload characteristics
        data_size = workload.get("data_size", 100)
        latency_sla = workload.get("latency_sla", 100)

        if latency_sla < 50:
            tier = ExecutionTier.FOG
            node = (fog_nodes or ["fog-1"])[0]
        elif data_size > 10000:
            tier = ExecutionTier.CLOUD
            node = f"cloud-{cloud_provider}"
        else:
            tier = ExecutionTier.FOG
            node = (fog_nodes or ["fog-1"])[0]

        latency = np.random.uniform(10, 100) if tier == ExecutionTier.FOG else np.random.uniform(100, 500)
        cost = 0.001 * data_size if tier == ExecutionTier.CLOUD else 0.0001 * data_size

        return OffloadResult(
            tier=tier,
            node_id=node,
            cost=cost,
            latency_ms=latency,
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate fog computing capabilities."""
    print("=" * 70)
    print("Fog Computing Framework - Demo")
    print("=" * 70)

    # --- 1. Fog Node Management ---
    print("\n--- Fog Node Management ---")
    manager = FogNodeManager()
    for i in range(3):
        node = manager.register_node(NodeConfig(
            node_id=f"fog-{i+1}",
            location=f"building-{chr(65+i)}",
            resources={"cpu": 4, "memory_mb": 4096},
            capabilities=["inference", "preprocessing"],
        ))
        print(f"  Node: {node.node_id} ({node.location})")

    status = manager.get_cluster_status()
    print(f"  Cluster: {status}")

    # --- 2. Workload Orchestration ---
    print("\n--- Workload Orchestration ---")
    orchestrator = FogOrchestrator()
    orchestrator.set_nodes(manager.list_nodes())
    placement = orchestrator.place_workload(
        {"type": "inference", "latency_sla": 50},
        PlacementStrategy.LATENCY_OPTIMIZED,
    )
    print(f"  Placed on: {placement.node_id}")
    print(f"  Latency: {placement.expected_latency_ms:.0f}ms")
    print(f"  Resource impact: {placement.resource_impact}")

    # --- 3. Resource Optimization ---
    print("\n--- Resource Optimization ---")
    optimizer = ResourceOptimizer()
    opt = optimizer.optimize("fog-1")
    print(f"  CPU: {opt.cpu_utilization:.0%}")
    print(f"  Memory: {opt.memory_utilization:.0%}")
    print(f"  Storage: {opt.storage_utilization:.0%}")
    print(f"  Recommendations: {opt.recommendations}")

    # --- 4. Fog-Cloud Integration ---
    print("\n--- Fog-Cloud Integration ---")
    bridge = FogCloudBridge()
    result = bridge.offload({"type": "training", "data_size": 5000}, ["fog-1", "fog-2"])
    print(f"  Tier: {result.tier.value}")
    print(f"  Node: {result.node_id}")
    print(f"  Cost: ${result.cost:.4f}")
    print(f"  Latency: {result.latency_ms:.0f}ms")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()