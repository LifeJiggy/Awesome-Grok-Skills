"""
Service Mesh Module
Service mesh configuration for traffic management and security
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MTLSMode(Enum):
    DISABLED = "DISABLED"
    PERMISSIVE = "PERMISSIVE"
    STRICT = "STRICT"

class TrafficAction(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"

@dataclass
class TrafficRule:
    source: str = ""
    destination: str = ""
    match: Dict[str, str] = field(default_factory=dict)
    weight: int = 100
    timeout_ms: int = 30000
    retries: int = 0
    id: str = field(default_factory=lambda: f"tr-{str(uuid.uuid4())[:8]}")

@dataclass
class MTLSConfig:
    mode: MTLSMode = MTLSMode.STRICT

@dataclass
class SecurityPolicy:
    name: str = ""
    namespace: str = "default"
    mtls: MTLSConfig = field(default_factory=MTLSConfig)
    authorization_rules: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ObservabilityConfig:
    tracing: bool = True
    sampling_rate: float = 0.1
    metrics: bool = True
    access_logging: bool = True

@dataclass
class CircuitBreaker:
    consecutive_errors: int = 5
    interval_seconds: int = 30
    timeout_seconds: int = 60

@dataclass
class ResilienceConfig:
    circuit_breaker: Optional[CircuitBreaker] = None
    retry_policy: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ServiceMesh:
    name: str = ""
    platform: str = "istio"
    _traffic_rules: List[TrafficRule] = field(default_factory=list)
    _security_policies: List[SecurityPolicy] = field(default_factory=list)

    def add_traffic_rule(self, rule: TrafficRule) -> None:
        self._traffic_rules.append(rule)

    @property
    def rule_count(self) -> int:
        return len(self._traffic_rules)

    def apply_security_policy(self, policy: SecurityPolicy) -> None:
        self._security_policies.append(policy)

    def configure_observability(self, config: ObservabilityConfig) -> None:
        logger.info("Configured observability: tracing=%s, metrics=%s", config.tracing, config.metrics)

    def configure_resilience(self, config: ResilienceConfig) -> None:
        logger.info("Configured resilience: circuit_breaker=%s", config.circuit_breaker is not None)

def main() -> None:
    print("=" * 60)
    print("  Service Mesh Module — Demo")
    print("=" * 60)

    mesh = ServiceMesh(name="production-mesh", platform="istio")
    mesh.add_traffic_rule(TrafficRule(source="gateway", destination="order-service", weight=90))
    mesh.add_traffic_rule(TrafficRule(source="gateway", destination="order-service-v2", weight=10))
    print(f"\n[+] Mesh: {mesh.name} ({mesh.rule_count} traffic rules)")

    policy = SecurityPolicy(name="strict-mtls", mtls=MTLSConfig(mode=MTLSMode.STRICT))
    mesh.apply_security_policy(policy)
    print(f"[+] Security: {len(mesh._security_policies)} policies")

    mesh.configure_observability(ObservabilityConfig(tracing=True, sampling_rate=0.1))
    mesh.configure_resilience(ResilienceConfig(circuit_breaker=CircuitBreaker()))
    print(f"[+] Configured: observability + resilience")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
