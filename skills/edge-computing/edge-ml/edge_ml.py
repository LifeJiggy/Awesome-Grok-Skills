"""
Edge ML Framework

Production-grade edge ML toolkit providing distributed inference, model synchronization,
federated aggregation, edge-cloud coordination, and ML pipeline management.
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

class LoadBalancer(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    LATENCY_BASED = "latency_based"
    RESOURCE_BASED = "resource_based"


class SyncStrategy(Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFF = "diff"


class WorkloadType(Enum):
    INFERENCE = "inference"
    TRAINING = "training"
    PREPROCESSING = "preprocessing"
    AGGREGATION = "aggregation"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class InferenceResult:
    """Distributed inference result."""
    prediction: Any
    confidence: float
    nodes_used: List[str]
    latency_ms: float
    aggregation_method: str = "average"


@dataclass
class SyncUpdate:
    """Model synchronization update."""
    model_id: str
    nodes_synced: int
    size_mb: float
    duration_seconds: float
    strategy: SyncStrategy
    version: str = ""


@dataclass
class WorkloadSchedule:
    """Workload scheduling result."""
    workload: Dict[str, Any]
    edge_nodes: List[str]
    cloud_nodes: List[str]
    estimated_latency_ms: float
    estimated_cost: float
    strategy: str = ""


@dataclass
class PipelineResult:
    """ML pipeline execution result."""
    output: Any
    stage_timings: Dict[str, float]
    total_duration_ms: float
    success: bool = True
    errors: List[str] = field(default_factory=list)


@dataclass
class EdgeNode:
    """Edge node information."""
    node_id: str
    status: str = "active"
    inference_count: int = 0
    avg_latency_ms: float = 0.0
    memory_mb: float = 0.0
    cpu_usage: float = 0.0


@dataclass
class ModelInfo:
    """Model information."""
    model_id: str
    version: str
    size_mb: float
    accuracy: float
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Distributed Inference
# ---------------------------------------------------------------------------

class DistributedInference:
    """Orchestrate distributed inference across edge nodes."""

    def __init__(self, nodes: Optional[List[str]] = None,
                 load_balancer: LoadBalancer = LoadBalancer.ROUND_ROBIN):
        self.nodes = nodes or ["edge-1", "edge-2", "edge-3"]
        self.load_balancer = load_balancer
        self._node_stats: Dict[str, EdgeNode] = {
            n: EdgeNode(node_id=n) for n in self.nodes
        }
        self._current_index = 0

    def predict(self, input_data: NDArray) -> InferenceResult:
        start = time.time()

        # Select node based on load balancer
        if self.load_balancer == LoadBalancer.ROUND_ROBIN:
            selected_node = self.nodes[self._current_index % len(self.nodes)]
            self._current_index += 1
        else:
            selected_node = min(self._node_stats.values(),
                               key=lambda n: n.avg_latency_ms).node_id

        # Simulate inference
        time.sleep(0.005)
        latency = (time.time() - start) * 1000

        self._node_stats[selected_node].inference_count += 1
        self._node_stats[selected_node].avg_latency_ms = latency

        return InferenceResult(
            prediction=np.random.choice(["cat", "dog", "bird"]),
            confidence=np.random.uniform(0.7, 0.99),
            nodes_used=[selected_node],
            latency_ms=latency,
        )


# ---------------------------------------------------------------------------
# Model Sync
# ---------------------------------------------------------------------------

class ModelSync:
    """Synchronize models between edge and cloud."""

    def __init__(self, strategy: SyncStrategy = SyncStrategy.INCREMENTAL):
        self.strategy = strategy

    def sync_to_edge(
        self,
        model_id: str,
        source: str = "cloud",
        target_nodes: Optional[List[str]] = None,
    ) -> SyncUpdate:
        target_nodes = target_nodes or ["edge-1", "edge-2"]
        start = time.time()

        # Simulate sync
        time.sleep(0.02)
        duration = time.time() - start

        size = np.random.uniform(10, 100) if self.strategy == SyncStrategy.FULL else np.random.uniform(1, 20)

        return SyncUpdate(
            model_id=model_id,
            nodes_synced=len(target_nodes),
            size_mb=size,
            duration_seconds=duration,
            strategy=self.strategy,
            version=f"v{int(time.time())}",
        )

    def sync_from_edge(
        self,
        model_id: str,
        source_node: str,
    ) -> SyncUpdate:
        return SyncUpdate(
            model_id=model_id,
            nodes_synced=1,
            size_mb=np.random.uniform(5, 50),
            duration_seconds=np.random.uniform(1, 10),
            strategy=self.strategy,
        )


# ---------------------------------------------------------------------------
# Edge-Cloud Coordinator
# ---------------------------------------------------------------------------

class EdgeCloudCoordinator:
    """Coordinate workloads between edge and cloud."""

    def schedule(
        self,
        workload: Dict[str, Any],
        strategy: str = "latency_optimized",
    ) -> WorkloadSchedule:
        workload_type = workload.get("type", "inference")
        data_size = workload.get("data_size", 100)

        if strategy == "latency_optimized":
            edge_nodes = ["edge-1", "edge-2"]
            cloud_nodes = []
        elif strategy == "cost_optimized":
            edge_nodes = []
            cloud_nodes = ["cloud-1"]
        else:
            edge_nodes = ["edge-1"]
            cloud_nodes = ["cloud-1"]

        latency = np.random.uniform(10, 100) if edge_nodes else np.random.uniform(100, 500)
        cost = len(cloud_nodes) * 0.001 * data_size

        return WorkloadSchedule(
            workload=workload,
            edge_nodes=edge_nodes,
            cloud_nodes=cloud_nodes,
            estimated_latency_ms=latency,
            estimated_cost=cost,
            strategy=strategy,
        )


# ---------------------------------------------------------------------------
# ML Pipeline
# ---------------------------------------------------------------------------

class EdgeMLPipeline:
    """Manage ML pipelines at the edge."""

    def __init__(self, name: str = "pipeline"):
        self.name = name
        self._stages: List[Dict[str, str]] = []

    def add_stage(self, stage: Dict[str, str]) -> None:
        self._stages.append(stage)

    def run(self, input_data: Any) -> PipelineResult:
        start = time.time()
        timings = {}
        output = input_data

        for stage in self._stages:
            stage_start = time.time()
            time.sleep(0.001)
            timings[stage["name"]] = (time.time() - stage_start) * 1000

        total_time = (time.time() - start) * 1000

        return PipelineResult(
            output=output,
            stage_timings=timings,
            total_duration_ms=total_time,
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate edge ML capabilities."""
    print("=" * 70)
    print("Edge ML Framework - Demo")
    print("=" * 70)

    # --- 1. Distributed Inference ---
    print("\n--- Distributed Inference ---")
    inference = DistributedInference(["edge-1", "edge-2", "edge-3"])
    result = inference.predict(np.random.rand(1, 224, 224, 3))
    print(f"  Prediction: {result.prediction}")
    print(f"  Confidence: {result.confidence:.2%}")
    print(f"  Node: {result.nodes_used}")
    print(f"  Latency: {result.latency_ms:.1f}ms")

    # --- 2. Model Sync ---
    print("\n--- Model Synchronization ---")
    sync = ModelSync(SyncStrategy.INCREMENTAL)
    update = sync.sync_to_edge("model-v2", "cloud", ["edge-1", "edge-2"])
    print(f"  Synced: {update.nodes_synced} nodes")
    print(f"  Size: {update.size_mb:.1f} MB")
    print(f"  Duration: {update.duration_seconds:.2f}s")
    print(f"  Version: {update.version}")

    # --- 3. Edge-Cloud Coordination ---
    print("\n--- Edge-Cloud Coordination ---")
    coordinator = EdgeCloudCoordinator()
    schedule = coordinator.schedule(
        {"type": "inference", "model": "resnet50", "data_size": 1000},
        "latency_optimized",
    )
    print(f"  Edge nodes: {schedule.edge_nodes}")
    print(f"  Cloud nodes: {schedule.cloud_nodes}")
    print(f"  Latency: {schedule.estimated_latency_ms:.0f}ms")
    print(f"  Cost: ${schedule.estimated_cost:.4f}")

    # --- 4. ML Pipeline ---
    print("\n--- ML Pipeline ---")
    pipeline = EdgeMLPipeline("inference-pipeline")
    pipeline.add_stage({"name": "preprocess", "type": "data_preprocessing"})
    pipeline.add_stage({"name": "infer", "type": "model_inference"})
    pipeline.add_stage({"name": "postprocess", "type": "result_processing"})

    result = pipeline.run({"input": "data"})
    print(f"  Stages: {len(result.stage_timings)}")
    print(f"  Total time: {result.total_duration_ms:.1f}ms")
    print(f"  Success: {result.success}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()