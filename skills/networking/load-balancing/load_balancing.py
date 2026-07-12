"""
Load Balancing Module
Part of the networking skill domain.

Production-grade load balancing: distribution algorithms, health checks,
circuit breaking, session persistence, and traffic management.
"""

from __future__ import annotations

import hashlib
import random
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple


class LBAlgorithm(Enum):
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    LEAST_RESPONSE_TIME = "least_response_time"
    IP_HASH = "ip_hash"
    CONSISTENT_HASH = "consistent_hash"
    RANDOM = "random"
    POWER_OF_TWO = "power_of_two_choices"


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class HealthStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


@dataclass
class Upstream:
    host: str
    port: int
    weight: int = 1
    max_connections: int = 1000
    current_connections: int = 0
    total_requests: int = 0
    total_failures: int = 0
    success_count: int = 0
    failure_count: int = 0
    last_failure_time: float = 0.0
    last_health_check: float = 0.0
    avg_response_time_ms: float = 0.0
    is_healthy: bool = True
    tags: Dict[str, str] = field(default_factory=dict)

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"

    @property
    def failure_rate(self) -> float:
        total = self.total_requests
        return self.total_failures / total if total > 0 else 0.0

    @property
    def active_ratio(self) -> float:
        return self.current_connections / self.max_connections if self.max_connections > 0 else 1.0

    def update_avg_response_time(self, new_time_ms: float, alpha: float = 0.1):
        self.avg_response_time_ms = (1 - alpha) * self.avg_response_time_ms + alpha * new_time_ms


@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    success_threshold: int = 3
    recovery_timeout: float = 30.0
    half_open_max_calls: int = 3
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: float = 0.0
    half_open_calls: int = 0
    total_rejections: int = 0

    def record_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self._reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = max(0, self.failure_count - 1)

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def can_execute(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                self.success_count = 0
                return True
            self.total_rejections += 1
            return False
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls < self.half_open_max_calls:
                self.half_open_calls += 1
                return True
            return False
        return False

    def _reset(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.half_open_calls = 0


@dataclass
class HealthCheckConfig:
    interval: float = 10.0
    timeout: float = 5.0
    unhealthy_threshold: int = 3
    healthy_threshold: int = 2
    check_path: str = "/health"
    method: str = "GET"


@dataclass
class RateLimitConfig:
    requests_per_second: float = 100.0
    burst_size: int = 200
    window_size: float = 1.0


class TokenBucketRateLimiter:
    def __init__(self, rate: float, burst: int):
        self.rate = rate
        self.burst = burst
        self.tokens = float(burst)
        self.last_refill = time.time()

    def allow(self) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        self.last_refill = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: deque = deque()

    def allow(self) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds
        while self._requests and self._requests[0] < cutoff:
            self._requests.popleft()
        if len(self._requests) < self.max_requests:
            self._requests.append(now)
            return True
        return False


class LoadBalancer:
    def __init__(self, algorithm: LBAlgorithm = LBAlgorithm.ROUND_ROBIN):
        self.algorithm = algorithm
        self.upstreams: List[Upstream] = []
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._rr_index = 0
        self._request_log: deque = deque(maxlen=50000)
        self._consistent_hash_ring: Dict[str, Upstream] = {}
        self._hash_ring_built = False

    def add_upstream(self, host: str, port: int, weight: int = 1,
                     tags: Optional[Dict[str, str]] = None) -> Upstream:
        upstream = Upstream(host=host, port=port, weight=weight, tags=tags or {})
        self.upstreams.append(upstream)
        self.circuit_breakers[upstream.address] = CircuitBreaker()
        self._hash_ring_built = False
        return upstream

    def remove_upstream(self, address: str):
        self.upstreams = [u for u in self.upstreams if u.address != address]
        self.circuit_breakers.pop(address, None)
        self._hash_ring_built = False

    def get_upstream(self, client_ip: str = "", key: str = "",
                     tags_filter: Optional[Dict[str, str]] = None) -> Optional[Upstream]:
        candidates = self._get_available_upstreams(tags_filter)
        if not candidates:
            return None

        if self.algorithm == LBAlgorithm.ROUND_ROBIN:
            return self._select_round_robin(candidates)
        elif self.algorithm == LBAlgorithm.WEIGHTED_ROUND_ROBIN:
            return self._select_weighted_round_robin(candidates)
        elif self.algorithm == LBAlgorithm.LEAST_CONNECTIONS:
            return self._select_least_connections(candidates)
        elif self.algorithm == LBAlgorithm.LEAST_RESPONSE_TIME:
            return self._select_least_response_time(candidates)
        elif self.algorithm == LBAlgorithm.IP_HASH:
            return self._select_ip_hash(candidates, client_ip or key)
        elif self.algorithm == LBAlgorithm.CONSISTENT_HASH:
            return self._select_consistent_hash(candidates, key or client_ip)
        elif self.algorithm == LBAlgorithm.POWER_OF_TWO:
            return self._select_power_of_two(candidates)
        else:
            return random.choice(candidates)

    def _get_available_upstreams(self, tags_filter: Optional[Dict[str, str]] = None) -> List[Upstream]:
        result = []
        for u in self.upstreams:
            if not u.is_healthy:
                continue
            cb = self.circuit_breakers.get(u.address)
            if cb and not cb.can_execute():
                continue
            if tags_filter and not all(u.tags.get(k) == v for k, v in tags_filter.items()):
                continue
            result.append(u)
        return result

    def _select_round_robin(self, upstreams: List[Upstream]) -> Upstream:
        idx = self._rr_index % len(upstreams)
        self._rr_index = (self._rr_index + 1) % len(upstreams)
        return upstreams[idx]

    def _select_weighted_round_robin(self, upstreams: List[Upstream]) -> Upstream:
        total = sum(u.weight for u in upstreams)
        r = random.uniform(0, total)
        cumulative = 0
        for u in upstreams:
            cumulative += u.weight
            if r <= cumulative:
                return u
        return upstreams[-1]

    def _select_least_connections(self, upstreams: List[Upstream]) -> Upstream:
        return min(upstreams, key=lambda u: u.current_connections)

    def _select_least_response_time(self, upstreams: List[Upstream]) -> Upstream:
        return min(upstreams, key=lambda u: u.avg_response_time_ms)

    def _select_ip_hash(self, upstreams: List[Upstream], client_ip: str) -> Upstream:
        h = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        return upstreams[h % len(upstreams)]

    def _select_consistent_hash(self, upstreams: List[Upstream], key: str) -> Upstream:
        if not self._hash_ring_built or len(self._consistent_hash_ring) != len(upstreams) * 150:
            self._build_hash_ring(upstreams)
        if not self._consistent_hash_ring:
            return upstreams[0]

        sorted_keys = sorted(self._consistent_hash_ring.keys())
        hash_key = hashlib.md5(key.encode()).hexdigest()
        for k in sorted_keys:
            if k >= hash_key:
                return self._consistent_hash_ring[k]
        return self._consistent_hash_ring[sorted_keys[0]]

    def _build_hash_ring(self, upstreams: List[Upstream]):
        self._consistent_hash_ring.clear()
        for u in upstreams:
            for i in range(150):
                h = hashlib.md5(f"{u.address}:{i}".encode()).hexdigest()
                self._consistent_hash_ring[h] = u
        self._hash_ring_built = True

    def _select_power_of_two(self, upstreams: List[Upstream]) -> Upstream:
        a = random.choice(upstreams)
        b = random.choice(upstreams)
        return a if a.current_connections <= b.current_connections else b

    def record_request(self, upstream: Upstream, success: bool, latency_ms: float):
        upstream.total_requests += 1
        if not success:
            upstream.total_failures += 1
        upstream.update_avg_response_time(latency_ms)

        cb = self.circuit_breakers.get(upstream.address)
        if cb:
            if success:
                cb.record_success()
            else:
                cb.record_failure()

        self._request_log.append({
            "upstream": upstream.address,
            "success": success,
            "latency_ms": latency_ms,
            "timestamp": time.time(),
        })

    def get_upstream_by_address(self, address: str) -> Optional[Upstream]:
        for u in self.upstreams:
            if u.address == address:
                return u
        return None

    def drain_upstream(self, address: str, timeout: float = 30.0):
        upstream = self.get_upstream_by_address(address)
        if upstream:
            upstream.is_healthy = False
            upstream.max_connections = 0

    def get_stats(self) -> Dict[str, Any]:
        total_requests = sum(u.total_requests for u in self.upstreams)
        total_failures = sum(u.total_failures for u in self.upstreams)

        recent = [r for r in self._request_log if time.time() - r["timestamp"] < 60]
        avg_latency = sum(r["latency_ms"] for r in recent) / len(recent) if recent else 0

        return {
            "algorithm": self.algorithm.value,
            "total_upstreams": len(self.upstreams),
            "healthy_upstreams": sum(1 for u in self.upstreams if u.is_healthy),
            "total_requests": total_requests,
            "total_failures": total_failures,
            "failure_rate": total_failures / total_requests if total_requests > 0 else 0,
            "recent_avg_latency_ms": round(avg_latency, 2),
            "upstreams": [{
                "address": u.address,
                "weight": u.weight,
                "connections": u.current_connections,
                "requests": u.total_requests,
                "failures": u.total_failures,
                "avg_response_ms": round(u.avg_response_time_ms, 2),
                "healthy": u.is_healthy,
                "circuit": self.circuit_breakers.get(u.address, CircuitBreaker()).state.value,
            } for u in self.upstreams],
        }


class HealthChecker:
    def __init__(self, config: Optional[HealthCheckConfig] = None):
        self.config = config or HealthCheckConfig()
        self._failure_counts: Dict[str, int] = {}
        self._success_counts: Dict[str, int] = {}

    def check(self, upstream: Upstream, is_healthy_fn: Optional[Callable[[Upstream], bool]] = None) -> HealthStatus:
        if is_healthy_fn:
            healthy = is_healthy_fn(upstream)
        else:
            healthy = self._default_check(upstream)

        addr = upstream.address
        if healthy:
            self._failure_counts[addr] = 0
            self._success_counts[addr] = self._success_counts.get(addr, 0) + 1
            if self._success_counts[addr] >= self.config.healthy_threshold:
                upstream.is_healthy = True
                return HealthStatus.HEALTHY
            return HealthStatus.DEGRADED
        else:
            self._success_counts[addr] = 0
            self._failure_counts[addr] = self._failure_counts.get(addr, 0) + 1
            if self._failure_counts[addr] >= self.config.unhealthy_threshold:
                upstream.is_healthy = False
                return HealthStatus.UNHEALTHY
            return HealthStatus.DEGRADED

    def _default_check(self, upstream: Upstream) -> bool:
        return upstream.is_healthy and upstream.failure_rate < 0.5

    def check_all(self, upstreams: List[Upstream],
                  is_healthy_fn: Optional[Callable[[Upstream], bool]] = None) -> Dict[str, HealthStatus]:
        results: Dict[str, HealthStatus] = {}
        for u in upstreams:
            results[u.address] = self.check(u, is_healthy_fn)
        return results


def main():
    print("=== Load Balancing Module ===")

    lb = LoadBalancer(LBAlgorithm.LEAST_CONNECTIONS)

    upstreams = [
        ("10.0.1.1", 8080, 5),
        ("10.0.1.2", 8080, 3),
        ("10.0.1.3", 8080, 1),
        ("10.0.1.4", 8080, 2),
    ]

    print("\n=== Adding Upstreams ===")
    for host, port, weight in upstreams:
        u = lb.add_upstream(host, port, weight)
        print(f"  Added {u.address} (weight={weight})")

    print("\n=== Load Distribution (100 requests) ===")
    distribution: Dict[str, int] = {}
    for i in range(100):
        ip = f"client_{i % 20}"
        u = lb.get_upstream(client_ip=ip)
        if u:
            distribution[u.address] = distribution.get(u.address, 0) + 1
            lb.record_request(u, success=random.random() > 0.05, latency_ms=random.uniform(5, 100))

    for addr, count in sorted(distribution.items()):
        print(f"  {addr}: {count} requests")

    print("\n=== Circuit Breaker ===")
    cb = lb.circuit_breakers["10.0.1.1:8080"]
    for _ in range(6):
        cb.record_failure()
    print(f"  State after 6 failures: {cb.state.value}")
    print(f"  Can execute: {cb.can_execute()}")
    print(f"  Rejections: {cb.total_rejections}")

    print("\n=== Rate Limiting ===")
    token_bucket = TokenBucketRateLimiter(rate=10, burst=20)
    allowed = sum(1 for _ in range(30) if token_bucket.allow())
    print(f"  Token bucket: {allowed}/30 allowed")

    sliding = SlidingWindowRateLimiter(max_requests=5, window_seconds=1.0)
    allowed = sum(1 for _ in range(10) if sliding.allow())
    print(f"  Sliding window: {allowed}/10 allowed")

    print("\n=== Health Check ===")
    checker = HealthChecker(HealthCheckConfig(unhealthy_threshold=2))
    statuses = checker.check_all(lb.upstreams)
    for addr, status in statuses.items():
        print(f"  {addr}: {status.value}")

    print("\n=== Stats ===")
    stats = lb.get_stats()
    print(f"  Algorithm: {stats['algorithm']}")
    print(f"  Upstreams: {stats['total_upstreams']}")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Failure rate: {stats['failure_rate']:.2%}")
    print(f"  Avg latency: {stats['recent_avg_latency_ms']:.1f}ms")

    print("\nDone.")


if __name__ == "__main__":
    main()
