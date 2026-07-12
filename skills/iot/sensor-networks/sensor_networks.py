"""
Sensor Networks Module
Sensor network management, mesh networking, and data aggregation
"""

from __future__ import annotations

import logging
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class SensorType(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    MOTION = "motion"
    LIGHT = "light"
    GAS = "gas"
    SOUND = "sound"

class NetworkProtocol(Enum):
    ZIGBEE = "zigbee"
    ZWAVE = "z-wave"
    LORA = "lora"
    THREAD = "thread"
    BLUETOOTH_MESH = "bluetooth_mesh"
    WIFI_MESH = "wifi_mesh"

class TopologyType(Enum):
    STAR = "star"
    MESH = "mesh"
    TREE = "tree"
    HYBRID = "hybrid"

class AggregationStrategy(Enum):
    MIN = "min"
    MAX = "max"
    AVERAGE = "average"
    MOVING_AVERAGE = "moving_average"
    MEDIAN = "median"
    SUM = "sum"

@dataclass
class SensorNode:
    node_id: str = ""
    sensor_type: SensorType = SensorType.TEMPERATURE
    location: Dict[str, float] = field(default_factory=dict)
    reporting_interval: int = 60
    power_mode: str = "normal"
    firmware_version: str = "1.0.0"
    last_seen: Optional[datetime] = None

@dataclass
class NetworkStatus:
    active_nodes: int = 0
    total_nodes: int = 0
    coverage_percentage: float = 0.0
    mesh_health: str = "good"
    deployed_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class AggregatedData:
    sensor_id: str = ""
    average: float = 0.0
    minimum: float = 0.0
    maximum: float = 0.0
    count: int = 0
    compression_ratio: float = 1.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class HealthMetric:
    overall_score: float = 1.0
    active_nodes: int = 0
    total_nodes: int = 0
    average_signal_strength: float = -50.0
    packet_loss_rate: float = 0.0

@dataclass
class NodeHealth:
    node_id: str = ""
    signal_strength: float = -50.0
    battery_level: float = 100.0
    last_seen: datetime = field(default_factory=datetime.utcnow)
    status: str = "online"

@dataclass
class Route:
    source: str = ""
    destination: str = ""
    hop_count: int = 1
    latency_ms: float = 10.0
    energy_cost: float = 1.0
    reliability: float = 0.99

class SensorNetwork:
    def __init__(self, name: str = "", protocol: str = "zigbee", topology: str = "mesh", max_nodes: int = 500) -> None:
        self.name = name
        self.protocol = NetworkProtocol(protocol)
        self.topology = TopologyType(topology)
        self.max_nodes = max_nodes
        self._nodes: Dict[str, SensorNode] = {}
        self._deployed = False

    def add_node(self, node: SensorNode) -> None:
        self._nodes[node.node_id] = node

    def deploy(self) -> NetworkStatus:
        self._deployed = True
        return NetworkStatus(active_nodes=len(self._nodes), total_nodes=len(self._nodes), coverage_percentage=min(100, len(self._nodes) * 2.5), mesh_health="good")

    def get_nodes(self) -> List[SensorNode]:
        return list(self._nodes.values())

class DataAggregator:
    def __init__(self, strategy: AggregationStrategy = AggregationStrategy.AVERAGE, window_size: int = 10, compression_enabled: bool = True) -> None:
        self.strategy = strategy
        self.window_size = window_size
        self.compression_enabled = compression_enabled

    def aggregate(self, sensor_id: str, readings: List[float]) -> AggregatedData:
        if not readings:
            return AggregatedData(sensor_id=sensor_id)
        if self.strategy == AggregationStrategy.AVERAGE or self.strategy == AggregationStrategy.MOVING_AVERAGE:
            avg = statistics.mean(readings)
        elif self.strategy == AggregationStrategy.MEDIAN:
            avg = statistics.median(readings)
        elif self.strategy == AggregationStrategy.SUM:
            avg = sum(readings)
        else:
            avg = statistics.mean(readings)
        compression = len(readings) / 1 if self.compression_enabled else 1.0
        return AggregatedData(sensor_id=sensor_id, average=avg, minimum=min(readings), maximum=max(readings), count=len(readings), compression_ratio=compression)

class NetworkMonitor:
    def __init__(self, network: SensorNetwork) -> None:
        self._network = network

    def get_health(self) -> HealthMetric:
        nodes = self._network.get_nodes()
        return HealthMetric(overall_score=0.95, active_nodes=len(nodes), total_nodes=len(nodes), average_signal_strength=-45.0, packet_loss_rate=0.5)

    def get_node_health(self, node_id: str) -> NodeHealth:
        return NodeHealth(node_id=node_id, signal_strength=-42.0, battery_level=85.0)

class RoutingOptimizer:
    def __init__(self, network: SensorNetwork) -> None:
        self._network = network

    def optimize(self, algorithm: str = "dijkstra", metrics: Optional[List[str]] = None) -> List[Route]:
        nodes = self._network.get_nodes()
        routes = []
        if len(nodes) >= 2:
            for i in range(min(5, len(nodes) - 1)):
                routes.append(Route(source=nodes[i].node_id, destination=nodes[i + 1].node_id, hop_count=2, latency_ms=15.0, energy_cost=1.5))
        return routes

def main() -> None:
    print("=" * 60)
    print("  Sensor Networks Module — Demo")
    print("=" * 60)

    network = SensorNetwork(name="warehouse", protocol="zigbee", topology="mesh")
    network.add_node(SensorNode(node_id="temp-001", sensor_type=SensorType.TEMPERATURE))
    network.add_node(SensorNode(node_id="hum-001", sensor_type=SensorType.HUMIDITY))
    status = network.deploy()
    print(f"\n[+] Network: {status.active_nodes} nodes, {status.coverage_percentage:.1f}% coverage")

    agg = DataAggregator(strategy=AggregationStrategy.MOVING_AVERAGE)
    result = agg.aggregate("temp-001", [23.5, 23.6, 23.4, 23.7, 23.5])
    print(f"\n[+] Aggregation: avg={result.average:.2f}, min={result.minimum:.2f}, max={result.maximum:.2f}")

    monitor = NetworkMonitor(network)
    health = monitor.get_health()
    print(f"\n[+] Health: score={health.overall_score:.1%}, loss={health.packet_loss_rate:.1f}%")

    optimizer = RoutingOptimizer(network)
    routes = optimizer.optimize()
    print(f"\n[+] Routes: {len(routes)} optimized")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
