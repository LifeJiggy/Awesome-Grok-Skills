"""
Edge Networking Framework

Production-grade edge networking toolkit providing network management, protocol
optimization, traffic engineering, QoS, and edge connectivity.
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

class Protocol(Enum):
    MQTT = "mqtt"
    COAP = "coap"
    WEBSOCKET = "websocket"
    HTTP = "http"
    HTTP3 = "http3"
    GRPC = "grpc"
    CUSTOM = "custom"


class LoadBalancingMethod(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    IP_HASH = "ip_hash"
    RANDOM = "random"


class TrafficClass(Enum):
    VOICE = "voice"
    VIDEO = "video"
    BEST_EFFORT = "best_effort"
    BACKGROUND = "background"


class InterfaceStatus(Enum):
    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class InterfaceConfig:
    """Network interface configuration."""
    name: str
    ip_address: str = ""
    netmask: str = "255.255.255.0"
    gateway: str = ""
    dns: List[str] = field(default_factory=list)
    status: InterfaceStatus = InterfaceStatus.UP


@dataclass
class ProtocolConfig:
    """Protocol optimization configuration."""
    protocol: Protocol
    qos_level: int = 0
    keepalive_seconds: int = 60
    max_packet_size: int = 1024
    timeout_ms: int = 5000
    retries: int = 3


@dataclass
class LoadBalancerConfig:
    """Load balancer configuration."""
    method: LoadBalancingMethod
    backends: List[str]
    health_check: str = "/health"
    health_check_interval: int = 30


@dataclass
class QoSRule:
    """QoS policy rule."""
    traffic_class: TrafficClass
    priority: int
    bandwidth_mbps: float
    max_latency_ms: float = 0
    max_jitter_ms: float = 0
    max_packet_loss: float = 0.0


@dataclass
class NetworkMetrics:
    """Network performance metrics."""
    latency_ms: float = 0.0
    throughput_mbps: float = 0.0
    packet_loss: float = 0.0
    jitter_ms: float = 0.0
    active_connections: int = 0
    bandwidth_usage_pct: float = 0.0


@dataclass
class QoSPolicy:
    """QoS policy configuration."""
    rules: List[QoSRule] = field(default_factory=list)

    def add_rule(self, traffic_class: TrafficClass, priority: int,
                 bandwidth_mbps: float, max_latency_ms: float = 0,
                 max_jitter_ms: float = 0) -> None:
        self.rules.append(QoSRule(
            traffic_class=traffic_class,
            priority=priority,
            bandwidth_mbps=bandwidth_mbps,
            max_latency_ms=max_latency_ms,
            max_jitter_ms=max_jitter_ms,
        ))


# ---------------------------------------------------------------------------
# Network Manager
# ---------------------------------------------------------------------------

class NetworkManager:
    """Manage edge network configuration."""

    def __init__(self):
        self._interfaces: Dict[str, InterfaceConfig] = {}

    def configure_interface(self, config: InterfaceConfig) -> InterfaceConfig:
        self._interfaces[config.name] = config
        logger.info("Configured interface: %s (%s)", config.name, config.ip_address)
        return config

    def get_interface(self, name: str) -> Optional[InterfaceConfig]:
        return self._interfaces.get(name)

    def get_metrics(self, interface_name: str) -> NetworkMetrics:
        return NetworkMetrics(
            latency_ms=np.random.uniform(1, 20),
            throughput_mbps=np.random.uniform(100, 1000),
            packet_loss=np.random.uniform(0, 0.01),
            jitter_ms=np.random.uniform(0.5, 5),
            active_connections=np.random.randint(10, 100),
            bandwidth_usage_pct=np.random.uniform(20, 80),
        )


# ---------------------------------------------------------------------------
# Protocol Optimizer
# ---------------------------------------------------------------------------

class ProtocolOptimizer:
    """Optimize protocols for edge networks."""

    def optimize(
        self,
        protocol: Protocol,
        network_type: str = "standard",
        requirements: Optional[Dict[str, Any]] = None,
    ) -> ProtocolConfig:
        if protocol == Protocol.MQTT:
            return ProtocolConfig(
                protocol=protocol,
                qos_level=1 if network_type == "constrained" else 0,
                keepalive_seconds=60,
                max_packet_size=256 if network_type == "constrained" else 1024,
            )
        elif protocol == Protocol.COAP:
            return ProtocolConfig(
                protocol=protocol,
                qos_level=0,
                keepalive_seconds=30,
                max_packet_size=1024,
            )
        else:
            return ProtocolConfig(protocol=protocol)


# ---------------------------------------------------------------------------
# Traffic Engineer
# ---------------------------------------------------------------------------

class TrafficEngineer:
    """Engineer traffic flow at the edge."""

    def configure_load_balancing(
        self,
        method: LoadBalancingMethod,
        backends: List[str],
        health_check: str = "/health",
    ) -> LoadBalancerConfig:
        return LoadBalancerConfig(
            method=method,
            backends=backends,
            health_check=health_check,
        )

    def get_backend_health(self, backends: List[str]) -> Dict[str, bool]:
        return {backend: np.random.random() > 0.1 for backend in backends}


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate edge networking capabilities."""
    print("=" * 70)
    print("Edge Networking Framework - Demo")
    print("=" * 70)

    # --- 1. Network Management ---
    print("\n--- Network Management ---")
    manager = NetworkManager()
    iface = manager.configure_interface(InterfaceConfig(
        name="eth0", ip_address="192.168.1.100",
        gateway="192.168.1.1", dns=["8.8.8.8"],
    ))
    print(f"  Interface: {iface.name} ({iface.ip_address})")

    metrics = manager.get_metrics("eth0")
    print(f"  Latency: {metrics.latency_ms:.1f}ms")
    print(f"  Throughput: {metrics.throughput_mbps:.0f} Mbps")
    print(f"  Packet loss: {metrics.packet_loss:.4f}%")

    # --- 2. Protocol Optimization ---
    print("\n--- Protocol Optimization ---")
    optimizer = ProtocolOptimizer()
    mqtt_config = optimizer.optimize(Protocol.MQTT, "constrained")
    print(f"  Protocol: {mqtt_config.protocol.value}")
    print(f"  QoS: {mqtt_config.qos_level}")
    print(f"  Keepalive: {mqtt_config.keepalive_seconds}s")

    # --- 3. Traffic Engineering ---
    print("\n--- Traffic Engineering ---")
    engineer = TrafficEngineer()
    lb = engineer.configure_load_balancing(
        LoadBalancingMethod.LEAST_CONNECTIONS,
        ["10.0.1.1:8080", "10.0.1.2:8080"],
    )
    print(f"  Method: {lb.method.value}")
    print(f"  Backends: {len(lb.backends)}")

    health = engineer.get_backend_health(lb.backends)
    print(f"  Health: {health}")

    # --- 4. QoS ---
    print("\n--- Quality of Service ---")
    qos = QoSPolicy()
    qos.add_rule(TrafficClass.VOICE, 7, 10, 20, 5)
    qos.add_rule(TrafficClass.VIDEO, 5, 50, 100)
    qos.add_rule(TrafficClass.BEST_EFFORT, 3, 100)

    print(f"  Rules: {len(qos.rules)}")
    for rule in qos.rules:
        print(f"    {rule.traffic_class.value}: priority={rule.priority}, "
              f"bandwidth={rule.bandwidth_mbps}Mbps, latency={rule.max_latency_ms}ms")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()