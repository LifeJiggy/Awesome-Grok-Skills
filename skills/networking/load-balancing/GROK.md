---
name: load-balancing
category: networking
version: 2.0.0
tags: [networking, load-balancing, reverse-proxy, ha, traffic-distribution]
---

# Load Balancing

## Overview

Production-grade load balancing and traffic distribution toolkit covering algorithm implementation, health checking, session persistence, circuit breaking, and dynamic upstream management. This skill provides software load balancer implementations, reverse proxy configurations, and distributed traffic management strategies for high-availability systems.

## Core Capabilities

- **Distribution Algorithms**: Round-robin, weighted round-robin, least connections, IP hash, consistent hashing, and random
- **Health Checks**: Active and passive health monitoring with configurable thresholds and intervals
- **Session Persistence**: Sticky sessions via IP hash, cookie injection, and consistent hashing
- **Circuit Breaking**: Failure detection with half-open, closed, and open states
- **SSL Termination**: TLS offloading, SNI routing, and certificate management
- **Rate Limiting**: Token bucket, sliding window, and fixed-window rate limiting per upstream
- **Dynamic Configuration**: Runtime upstream addition/removal without restarts
- **Metrics and Observability**: Latency tracking, error rates, connection pooling stats

## Usage Examples

```python
import time
import random
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum
from collections import deque

class LoadBalancingAlgorithm(Enum):
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    IP_HASH = "ip_hash"
    CONSISTENT_HASH = "consistent_hash"
    RANDOM = "random"

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class Upstream:
    host: str
    port: int
    weight: int = 1
    max_connections: int = 1000
    current_connections: int = 0
    total_requests: int = 0
    failure_count: int = 0
    last_failure: float = 0.0
    is_healthy: bool = True

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"

    @property
    def active_ratio(self) -> float:
        return self.current_connections / self.max_connections if self.max_connections > 0 else 1.0

@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    half_open_max: int = 3
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: float = 0.0
    half_open_attempts: int = 0

    def record_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_max:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        elif self.state == CircuitState.CLOSED:
            self.failure_count = max(0, self.failure_count - 1)

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def can_attempt(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_attempts = 0
                return True
            return False
        if self.state == CircuitState.HALF_OPEN:
            return self.half_open_attempts < self.half_open_max
        return False

class LoadBalancer:
    def __init__(self, algorithm: LoadBalancingAlgorithm = LoadBalancingAlgorithm.ROUND_ROBIN):
        self.algorithm = algorithm
        self.upstreams: List[Upstream] = []
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._round_robin_index = 0
        self._request_log: deque = deque(maxlen=10000)

    def add_upstream(self, host: str, port: int, weight: int = 1) -> Upstream:
        upstream = Upstream(host=host, port=port, weight=weight)
        self.upstreams.append(upstream)
        self.circuit_breakers[upstream.address] = CircuitBreaker()
        return upstream

    def remove_upstream(self, address: str):
        self.upstreams = [u for u in self.upstreams if u.address != address]
        self.circuit_breakers.pop(address, None)

    def get_upstream(self, client_ip: str = "", path: str = "") -> Optional[Upstream]:
        available = [u for u in self.upstreams if u.is_healthy and
                     self.circuit_breakers.get(u.address, CircuitBreaker()).can_attempt()]
        if not available:
            return None

        if self.algorithm == LoadBalancingAlgorithm.ROUND_ROBIN:
            return self._round_robin(available)
        elif self.algorithm == LoadBalancingAlgorithm.WEIGHTED_ROUND_ROBIN:
            return self._weighted_round_robin(available)
        elif self.algorithm == LoadBalancingAlgorithm.LEAST_CONNECTIONS:
            return self._least_connections(available)
        elif self.algorithm == LoadBalancingAlgorithm.IP_HASH:
            return self._ip_hash(available, client_ip)
        elif self.algorithm == LoadBalancingAlgorithm.CONSISTENT_HASH:
            return self._consistent_hash(available, client_ip)
        else:
            return random.choice(available)

    def _round_robin(self, upstreams: List[Upstream]) -> Upstream:
        idx = self._round_robin_index % len(upstreams)
        self._round_robin_index += 1
        return upstreams[idx]

    def _weighted_round_robin(self, upstreams: List[Upstream]) -> Upstream:
        total_weight = sum(u.weight for u in upstreams)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for u in upstreams:
            cumulative += u.weight
            if r <= cumulative:
                return u
        return upstreams[-1]

    def _least_connections(self, upstreams: List[Upstream]) -> Upstream:
        return min(upstreams, key=lambda u: u.current_connections)

    def _ip_hash(self, upstreams: List[Upstream], client_ip: str) -> Upstream:
        hash_val = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        return upstreams[hash_val % len(upstreams)]

    def _consistent_hash(self, upstreams: List[Upstream], key: str) -> Upstream:
        ring = {}
        for u in upstreams:
            for i in range(150):
                h = hashlib.md5(f"{u.address}:{i}".encode()).hexdigest()
                ring[h] = u
        hash_key = hashlib.md5(key.encode()).hexdigest()
        sorted_keys = sorted(ring.keys())
        for k in sorted_keys:
            if k >= hash_key:
                return ring[k]
        return ring[sorted_keys[0]] if sorted_keys else upstreams[0]

    def record_request(self, upstream: Upstream, success: bool, latency_ms: float):
        upstream.total_requests += 1
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

    def get_stats(self) -> Dict:
        return {
            "total_upstreams": len(self.upstreams),
            "healthy_upstreams": sum(1 for u in self.upstreams if u.is_healthy),
            "total_requests": sum(u.total_requests for u in self.upstreams),
            "algorithm": self.algorithm.value,
            "upstreams": [{
                "address": u.address,
                "weight": u.weight,
                "connections": u.current_connections,
                "total_requests": u.total_requests,
                "is_healthy": u.is_healthy,
                "circuit_state": self.circuit_breakers.get(u.address, CircuitBreaker()).state.value,
            } for u in self.upstreams],
        }
```

## Best Practices

- Use least-connections for request-heavy workloads with variable response times
- Use consistent hashing for cache-friendly load balancing
- Implement circuit breakers to prevent cascade failures
- Always configure active health checks with appropriate intervals
- Monitor upstream connection pools to prevent resource exhaustion
- Use weighted round-robin when backends have heterogeneous capacity
- Log request distribution for capacity planning and anomaly detection
- Implement graceful drain when removing upstreams
- Set reasonable connection timeouts per upstream
- Use SSL termination at the load balancer to reduce backend overhead

## Related Modules

- `network-engineering` - Network infrastructure and routing
- `traffic-analysis` - Traffic pattern analysis and optimization
- `dns-management` - DNS-based load balancing and failover
- `sdn` - Software-defined networking patterns
