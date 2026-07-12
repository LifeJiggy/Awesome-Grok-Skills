"""
Load Balancing Module — Multiple algorithms, health checking, weighted canary deployments,
session affinity, connection draining, and circuit breaking for API gateways.
"""

from __future__ import annotations

import hashlib
import random
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Algorithm(Enum):
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    IP_HASH = "ip_hash"
    CONSISTENT_HASH = "consistent_hash"
    LEAST_RESPONSE_TIME = "least_response_time"
    RANDOM = "random"


class HealthCheckType(Enum):
    HTTP = "http"
    TCP = "tcp"
    GRPC = "grpc"
    PASSIVE = "passive"


class HealthState(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    DRAINING = "draining"


class SessionAffinity(Enum):
    NONE = "none"
    COOKIE = "cookie"
    HEADER = "header"
    IP = "ip"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class HealthCheck:
    """Health check configuration."""
    type: HealthCheckType = HealthCheckType.HTTP
    path: str = "/health"
    interval_s: float = 5.0
    timeout_s: float = 2.0
    healthy_threshold: int = 2
    unhealthy_threshold: int = 3
    expected_status: int = 200

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "path": self.path,
            "interval_s": self.interval_s,
        }


@dataclass
class Upstream:
    """An upstream target."""
    name: str
    address: str
    weight: int = 100
    max_connections: int = 1000
    current_connections: int = 0
    health_state: HealthState = HealthState.HEALTHY
    health_check: Optional[HealthCheck] = None
    zone: str = "default"
    tags: List[str] = field(default_factory=list)

    @property
    def available_connections(self) -> int:
        return max(0, self.max_connections - self.current_connections)

    @property
    def is_available(self) -> bool:
        return self.health_state in (HealthState.HEALTHY, HealthState.DEGRADED) and self.available_connections > 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "address": self.address,
            "weight": self.weight,
            "health": self.health_state.value,
            "connections": f"{self.current_connections}/{self.max_connections}",
        }


@dataclass
class UpstreamMetrics:
    """Metrics for an upstream."""
    total_requests: int = 0
    active_connections: int = 0
    avg_latency_ms: float = 0.0
    error_rate: float = 0.0
    last_health_check: str = ""
    consecutive_failures: int = 0
    health_status: str = "healthy"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "active_connections": self.active_connections,
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "error_rate": round(self.error_rate, 4),
            "health": self.health_status,
        }


@dataclass
class LoadBalancingResult:
    """Result of load balancing decision."""
    target: Upstream
    algorithm: Algorithm
    reason: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target": self.target.name,
            "address": self.target.address,
            "algorithm": self.algorithm.value,
            "reason": self.reason,
        }


@dataclass
class SessionEntry:
    """A sticky session entry."""
    session_id: str
    target_name: str
    created_at: float = field(default_factory=time.time)
    ttl_s: float = 3600

    @property
    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl_s


@dataclass
class CircuitBreakerState:
    """Circuit breaker for an upstream."""
    failures: int = 0
    successes: int = 0
    state: str = "closed"  # closed, open, half_open
    last_failure_time: float = 0
    threshold: int = 5
    recovery_timeout_s: float = 30

    @property
    def should_reject(self) -> bool:
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout_s:
                self.state = "half_open"
                return False
            return True
        return False

    def record_success(self) -> None:
        if self.state == "half_open":
            self.successes += 1
            if self.successes >= 3:
                self.state = "closed"
                self.failures = 0
        self.failures = max(0, self.failures - 1)

    def record_failure(self) -> None:
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.threshold:
            self.state = "open"


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class LoadBalancer:
    """Main load balancer with multiple algorithms and health checking."""

    def __init__(self, algorithm: Algorithm = Algorithm.ROUND_ROBIN):
        self.algorithm = algorithm
        self._targets: Dict[str, Upstream] = {}
        self._metrics: Dict[str, UpstreamMetrics] = {}
        self._round_robin_index: int = 0
        self._sessions: Dict[str, SessionEntry] = {}
        self._circuit_breakers: Dict[str, CircuitBreakerState] = {}
        self._session_affinity: SessionAffinity = SessionAffinity.NONE
        self._consistent_hash_ring: Dict[int, str] = {}

    def add_target(self, target: Upstream) -> None:
        self._targets[target.name] = target
        self._metrics[target.name] = UpstreamMetrics()
        self._circuit_breakers[target.name] = CircuitBreakerState()
        self._rebuild_hash_ring()

    def remove_target(self, name: str, drain: bool = True) -> None:
        if name in self._targets:
            if drain:
                self._targets[name].health_state = HealthState.DRAINING
            else:
                del self._targets[name]
                self._metrics.pop(name, None)
                self._circuit_breakers.pop(name, None)

    def set_health_check(self, target: Upstream) -> None:
        if target.name in self._targets:
            self._targets[target.name].health_check = target.health_check

    def set_session_affinity(self, affinity: SessionAffinity) -> None:
        self._session_affinity = affinity

    def route(self, client_ip: str = "", path: str = "", headers: Optional[Dict[str, str]] = None) -> Optional[Upstream]:
        """Route a request to an upstream target."""
        available = [t for t in self._targets.values() if t.is_available]
        if not available:
            return None

        # Check session affinity
        if self._session_affinity != SessionAffinity.NONE:
            session_target = self._check_session(client_ip, headers)
            if session_target and session_target in self._targets and self._targets[session_target].is_available:
                return self._targets[session_target]

        # Apply circuit breaker filter
        cb_filtered = [t for t in available if not self._circuit_breakers.get(t.name, CircuitBreakerState()).should_reject]
        if not cb_filtered:
            cb_filtered = available

        if self.algorithm == Algorithm.ROUND_ROBIN:
            target = self._round_robin(cb_filtered)
        elif self.algorithm == Algorithm.WEIGHTED_ROUND_ROBIN:
            target = self._weighted_round_robin(cb_filtered)
        elif self.algorithm == Algorithm.LEAST_CONNECTIONS:
            target = self._least_connections(cb_filtered)
        elif self.algorithm == Algorithm.IP_HASH:
            target = self._ip_hash(cb_filtered, client_ip)
        elif self.algorithm == Algorithm.CONSISTENT_HASH:
            target = self._consistent_hash(cb_filtered, path or client_ip)
        elif self.algorithm == Algorithm.LEAST_RESPONSE_TIME:
            target = self._least_response_time(cb_filtered)
        else:
            target = random.choice(cb_filtered)

        if target:
            target.current_connections += 1
            self._metrics[target.name].active_connections = target.current_connections
            self._metrics[target.name].total_requests += 1

        return target

    def release_connection(self, target_name: str) -> None:
        if target_name in self._targets:
            self._targets[target_name].current_connections = max(0, self._targets[target_name].current_connections - 1)
            self._metrics[target_name].active_connections = self._targets[target_name].current_connections

    def _round_robin(self, targets: List[Upstream]) -> Upstream:
        target = targets[self._round_robin_index % len(targets)]
        self._round_robin_index += 1
        return target

    def _weighted_round_robin(self, targets: List[Upstream]) -> Upstream:
        total_weight = sum(t.weight for t in targets)
        if total_weight == 0:
            return random.choice(targets)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for t in targets:
            cumulative += t.weight
            if r <= cumulative:
                return t
        return targets[-1]

    def _least_connections(self, targets: List[Upstream]) -> Upstream:
        return min(targets, key=lambda t: t.current_connections)

    def _ip_hash(self, targets: List[Upstream], client_ip: str) -> Upstream:
        hash_val = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        return targets[hash_val % len(targets)]

    def _consistent_hash(self, targets: List[Upstream], key: str) -> Upstream:
        if not self._consistent_hash_ring:
            self._rebuild_hash_ring()
        key_hash = int(hashlib.md5(key.encode()).hexdigest(), 16)
        ring_keys = sorted(self._consistent_hash_ring.keys())
        for ring_key in ring_keys:
            if ring_key >= key_hash:
                target_name = self._consistent_hash_ring[ring_key]
                if target_name in [t.name for t in targets]:
                    return [t for t in targets if t.name == target_name][0]
        target_name = self._consistent_hash_ring[ring_keys[0]] if ring_keys else targets[0].name
        return [t for t in targets if t.name == target_name][0] if target_name in [t.name for t in targets] else targets[0]

    def _least_response_time(self, targets: List[Upstream]) -> Upstream:
        return min(targets, key=lambda t: self._metrics.get(t.name, UpstreamMetrics()).avg_latency_ms)

    def _rebuild_hash_ring(self) -> None:
        self._consistent_hash_ring = {}
        for name, target in self._targets.items():
            for i in range(150):
                key = hashlib.md5(f"{target.address}:{i}".encode()).hexdigest()
                self._consistent_hash_ring[int(key, 16)] = name

    def _check_session(self, client_ip: str, headers: Optional[Dict[str, str]]) -> Optional[str]:
        session_id = None
        if self._session_affinity == SessionAffinity.COOKIE and headers:
            cookie = headers.get("Cookie", "")
            for part in cookie.split(";"):
                if "lb_session" in part:
                    session_id = part.split("=")[-1].strip()
        elif self._session_affinity == SessionAffinity.IP:
            session_id = client_ip
        elif self._session_affinity == SessionAffinity.HEADER and headers:
            session_id = headers.get("X-Session-ID")

        if session_id:
            session = self._sessions.get(session_id)
            if session and not session.is_expired:
                return session.target_name
        return None

    def create_session(self, session_id: str, target_name: str) -> None:
        self._sessions[session_id] = SessionEntry(session_id=session_id, target_name=target_name)

    def get_target_metrics(self, name: str) -> Dict[str, Any]:
        metrics = self._metrics.get(name, UpstreamMetrics())
        return metrics.to_dict()

    def get_all_targets(self) -> List[Upstream]:
        return list(self._targets.values())

    def run_health_check(self, name: str) -> bool:
        target = self._targets.get(name)
        cb = self._circuit_breakers.get(name)
        if not target:
            return False

        # Simulate health check
        is_healthy = random.random() > 0.1
        if is_healthy:
            target.health_state = HealthState.HEALTHY
            if cb:
                cb.record_success()
        else:
            target.health_state = HealthState.UNHEALTHY
            if cb:
                cb.record_failure()

        self._metrics[name].last_health_check = datetime.now(timezone.utc).isoformat()
        self._metrics[name].health_status = target.health_state.value
        return is_healthy

    def get_summary(self) -> Dict[str, Any]:
        healthy = sum(1 for t in self._targets.values() if t.health_state == HealthState.HEALTHY)
        total_conn = sum(t.current_connections for t in self._targets.values())
        total_req = sum(m.total_requests for m in self._metrics.values())
        return {
            "targets": len(self._targets),
            "healthy": healthy,
            "total_connections": total_conn,
            "total_requests": total_req,
            "algorithm": self.algorithm.value,
        }


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the load balancing toolkit."""
    print("Load Balancing Toolkit")
    print("=" * 60)

    lb = LoadBalancer(algorithm=Algorithm.WEIGHTED_ROUND_ROBIN)

    lb.add_target(Upstream(name="api-v1", address="10.0.1.10:8080", weight=90, max_connections=500))
    lb.add_target(Upstream(name="api-v2", address="10.0.1.20:8080", weight=10, max_connections=100))

    # Route requests
    print("\n--- Weighted Routing (20 requests) ---")
    distribution = defaultdict(int)
    for i in range(20):
        target = lb.route(client_ip=f"192.168.1.{i}")
        if target:
            distribution[target.name] += 1
    for name, count in distribution.items():
        print(f"  {name}: {count}/{20} ({count/20*100:.0f}%)")

    # Health checks
    print("\n--- Health Checks ---")
    for target in lb.get_all_targets():
        healthy = lb.run_health_check(target.name)
        print(f"  {target.name}: {'healthy' if healthy else 'unhealthy'}")

    # Circuit breaker
    print("\n--- Circuit Breakers ---")
    for name, cb in lb._circuit_breakers.items():
        print(f"  {name}: state={cb.state}, failures={cb.failures}")

    # Summary
    summary = lb.get_summary()
    print(f"\nSummary: {summary['healthy']}/{summary['targets']} targets healthy, {summary['total_requests']} total requests")


if __name__ == "__main__":
    main()
