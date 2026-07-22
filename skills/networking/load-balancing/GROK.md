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

## Advanced Configuration

### Load Balancer Settings

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `health_check_interval` | 30s | 5 - 300s | Active health check frequency |
| `health_check_timeout` | 5s | 1 - 30s | Health check response timeout |
| `unhealthy_threshold` | 3 | 1 - 10 | Failures before marking unhealthy |
| `healthy_threshold` | 2 | 1 - 10 | Successes before marking healthy |
| `connection_timeout` | 30s | 5 - 300s | Backend connection timeout |
| `max_connections` | 10000 | 100 - 100000 | Maximum concurrent connections |
| `retry_count` | 3 | 0 - 5 | Retry attempts on failure |

### Advanced Load Balancer Configuration

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class LbAlgorithm(Enum):
    ROUND_ROBIN = "round_robin"
    WEIGHTED_RR = "weighted_round_robin"
    LEAST_CONN = "least_connections"
    IP_HASH = "ip_hash"
    CONSISTENT_HASH = "consistent_hash"
    LEAST_RESPONSE = "least_response_time"
    RANDOM = "random"

@dataclass
class LbConfig:
    algorithm: LbAlgorithm = LbAlgorithm.LEAST_CONN
    health_check_interval: int = 30
    health_check_timeout: int = 5
    unhealthy_threshold: int = 3
    healthy_threshold: int = 2
    connection_timeout: int = 30
    max_connections: int = 10000
    retry_count: int = 3
    ssl_termination: bool = True
    sticky_sessions: bool = False
    session_cookie: str = "LBSESSION"
    drain_timeout: int = 30
    max_request_size: int = 10 * 1024 * 1024

    @classmethod
    def for_high_traffic(cls) -> 'LbConfig':
        return cls(max_connections=50000, health_check_interval=10, retry_count=5)

    @classmethod
    def for_microservices(cls) -> 'LbConfig':
        return cls(algorithm=LbAlgorithm.LEAST_CONN, health_check_interval=5, connection_timeout=10)

class SslCertificate:
    def __init__(self, cert_path: str, key_path: str, chain_path: str = None):
        self.cert_path = cert_path
        self.key_path = key_path
        self.chain_path = chain_path
        self._loaded = False

    def load(self):
        with open(self.cert_path, 'r') as f:
            self.cert = f.read()
        with open(self.key_path, 'r') as f:
            self.key = f.read()
        if self.chain_path:
            with open(self.chain_path, 'r') as f:
                self.chain = f.read()
        self._loaded = True

    def is_valid(self) -> bool:
        return self._loaded and self.cert and self.key

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, List[float]] = {}

    def is_allowed(self, client_ip: str) -> bool:
        import time
        now = time.time()
        if client_ip not in self._requests:
            self._requests[client_ip] = []
        self._requests[client_ip] = [
            t for t in self._requests[client_ip] if now - t < self.window_seconds
        ]
        if len(self._requests[client_ip]) >= self.max_requests:
            return False
        self._requests[client_ip].append(now)
        return True

    def get_usage(self, client_ip: str) -> int:
        import time
        now = time.time()
        if client_ip not in self._requests:
            return 0
        return len([t for t in self._requests[client_ip] if now - t < self.window_seconds])
```

### Advanced Health Checking

```python
import time
import urllib.request
from typing import Callable

class AdvancedHealthChecker:
    def __init__(self, config: LbConfig = None):
        self.config = config or LbConfig()
        self._health_history: Dict[str, List[bool]] = {}

    def check_tcp(self, host: str, port: int) -> bool:
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.config.health_check_timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def check_http(self, url: str, expected_status: int = 200) -> bool:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=self.config.health_check_timeout) as resp:
                return resp.status == expected_status
        except Exception:
            return False

    def check_https(self, url: str, expected_status: int = 200) -> bool:
        return self.check_http(url, expected_status)

    def record_health(self, address: str, healthy: bool):
        if address not in self._health_history:
            self._health_history[address] = []
        self._health_history[address].append(healthy)
        if len(self._health_history[address]) > 100:
            self._health_history[address] = self._health_history[address][-100:]

    def is_truly_healthy(self, address: str) -> bool:
        history = self._health_history.get(address, [])
        if len(history) < self.config.healthy_threshold:
            return True
        recent = history[-self.config.healthy_threshold:]
        return all(recent)

    def should_mark_unhealthy(self, address: str) -> bool:
        history = self._health_history.get(address, [])
        if len(history) < self.config.unhealthy_threshold:
            return False
        recent = history[-self.config.unhealthy_threshold:]
        return not any(recent)
```

### Connection Pool Management

```python
from collections import deque
import threading

class ConnectionPool:
    def __init__(self, max_size: int = 100, timeout: float = 30):
        self.max_size = max_size
        self.timeout = timeout
        self._pool: deque = deque()
        self._lock = threading.Lock()
        self._active = 0

    def acquire(self) -> Optional[object]:
        with self._lock:
            if self._pool:
                return self._pool.popleft()
            if self._active < self.max_size:
                self._active += 1
                return self._create_connection()
        return None

    def release(self, conn):
        with self._lock:
            if len(self._pool) < self.max_size:
                self._pool.append(conn)
            else:
                self._active -= 1
                self._close_connection(conn)

    def _create_connection(self):
        return {"status": "connected", "created_at": time.time()}

    def _close_connection(self, conn):
        conn["status"] = "closed"

    def get_stats(self) -> dict:
        with self._lock:
            return {
                "pool_size": len(self._pool),
                "active": self._active,
                "max_size": self.max_size,
            }
```

## Architecture Patterns

### High Availability Architecture

```
                    ┌─────────────────┐
                    │   DNS / VIP     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        ┌─────┴─────┐ ┌─────┴─────┐ ┌─────┴─────┐
        │   LB-1    │ │   LB-2    │ │   LB-3    │
        │  (Active) │ │ (Standby) │ │ (Standby) │
        └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
              │              │              │
    ┌─────────┼─────────┐   │              │
    │         │         │   │              │
┌───┴───┐ ┌───┴───┐ ┌───┴───┐            │
│App-1  │ │App-2  │ │App-3  │            │
└───────┘ └───────┘ └───────┘            │
                                          │
                              ┌───────────┤
                              │           │
                          ┌───┴───┐ ┌───┴───┐
                          │App-4  │ │App-5  │
                          └───────┘ └───────┘
```

### Session Persistence Patterns

```python
class SessionPersistence:
    def __init__(self, method: str = "cookie"):
        self.method = method
        self._sessions: Dict[str, str] = {}

    def get_upstream(self, client_ip: str, cookies: Dict = None) -> str:
        if self.method == "ip_hash":
            return self._ip_hash(client_ip)
        elif self.method == "cookie":
            return self._cookie_based(cookies)
        elif self.method == "consistent_hash":
            return self._consistent_hash(client_ip)
        return client_ip

    def _ip_hash(self, client_ip: str) -> str:
        import hashlib
        h = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        upstreams = ["10.0.0.1:8080", "10.0.0.2:8080", "10.0.0.3:8080"]
        return upstreams[h % len(upstreams)]

    def _cookie_based(self, cookies: Dict = None) -> str:
        if cookies and "LBSESSION" in cookies:
            return self._sessions.get(cookies["LBSESSION"], "10.0.0.1:8080")
        import uuid
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = "10.0.0.1:8080"
        return "10.0.0.1:8080"

    def _consistent_hash(self, key: str) -> str:
        import hashlib
        ring = {}
        upstreams = ["10.0.0.1:8080", "10.0.0.2:8080", "10.0.0.3:8080"]
        for u in upstreams:
            for i in range(150):
                h = hashlib.md5(f"{u}:{i}".encode()).hexdigest()
                ring[h] = u
        key_hash = hashlib.md5(key.encode()).hexdigest()
        sorted_keys = sorted(ring.keys())
        for k in sorted_keys:
            if k >= key_hash:
                return ring[k]
        return ring[sorted_keys[0]]
```

### SSL Termination Architecture

```python
class SslTerminator:
    def __init__(self, cert_path: str, key_path: str):
        self.cert_path = cert_path
        self.key_path = key_path
        self._certificates: Dict[str, SslCertificate] = {}

    def add_certificate(self, domain: str, cert: SslCertificate):
        self._certificates[domain] = cert

    def get_certificate(self, sni: str) -> Optional[SslCertificate]:
        return self._certificates.get(sni)

    def terminate_ssl(self, client_hello: dict) -> dict:
        sni = client_hello.get("server_name", "")
        cert = self.get_certificate(sni)
        if cert and cert.is_valid():
            return {"status": "ok", "cert": cert.cert}
        return {"status": "error", "message": "No certificate found"}
```

## Integration Guide

### Kubernetes Integration

```python
class K8sLoadBalancer:
    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
        self._services: Dict[str, dict] = {}

    def register_service(self, name: str, port: int, target_port: int):
        self._services[name] = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": name, "namespace": self.namespace},
            "spec": {
                "type": "LoadBalancer",
                "ports": [{"port": port, "targetPort": target_port}],
                "selector": {"app": name},
            },
        }

    def get_service_yaml(self, name: str) -> str:
        import yaml
        return yaml.dump(self._services.get(name, {}))
```

### Prometheus Metrics Export

```python
class LbMetricsExporter:
    def __init__(self):
        self._metrics: Dict[str, float] = {}

    def record_request(self, upstream: str, latency_ms: float, status: int):
        self._metrics[f'lb_requests_total{{upstream="{upstream}",status="{status}"}}'] = \
            self._metrics.get(f'lb_requests_total{{upstream="{upstream}",status="{status}"}}', 0) + 1
        self._metrics[f'lb_request_duration_ms{{upstream="{upstream}"}}'] = latency_ms

    def export_prometheus(self) -> str:
        lines = ["# HELP lb_requests_total Total requests per upstream"]
        lines.append("# TYPE lb_requests_total counter")
        for key, value in self._metrics.items():
            if "total" in key:
                lines.append(f"{key} {value}")
        lines.append("# HELP lb_request_duration_ms Request latency")
        lines.append("# TYPE lb_request_duration_ms gauge")
        for key, value in self._metrics.items():
            if "duration" in key:
                lines.append(f"{key} {value}")
        return "\n".join(lines)
```

## Performance Optimization

### Performance Metrics

| Metric | Target | Strategy |
|--------|--------|----------|
| Connection setup | < 5ms | Connection pooling |
| Request forwarding | < 1ms | Efficient buffer management |
| Health check overhead | < 1% CPU | Async checks, batching |
| SSL handshake | < 10ms | Session resumption, OCSP stapling |
| Memory per connection | < 10KB | Efficient data structures |
| Throughput | 100K+ RPS | epoll/kqueue, zero-copy |

### Connection Draining

```python
class ConnectionDrainer:
    def __init__(self, drain_timeout: int = 30):
        self.drain_timeout = drain_timeout
        self._draining: Dict[str, float] = {}

    def start_drain(self, upstream: str):
        import time
        self._draining[upstream] = time.time()

    def is_draining(self, upstream: str) -> bool:
        import time
        if upstream not in self._draining:
            return False
        elapsed = time.time() - self._draining[upstream]
        if elapsed > self.drain_timeout:
            del self._draining[upstream]
            return False
        return True

    def get_drain_progress(self, upstream: str) -> float:
        import time
        if upstream not in self._draining:
            return 1.0
        elapsed = time.time() - self._draining[upstream]
        return min(1.0, elapsed / self.drain_timeout)
```

## Security Considerations

### DDoS Protection

```python
class DdosProtection:
    def __init__(self, max_requests_per_second: int = 1000, burst_size: int = 2000):
        self.max_rps = max_requests_per_second
        self.burst_size = burst_size
        self._token_buckets: Dict[str, float] = {}

    def is_allowed(self, client_ip: str) -> bool:
        import time
        now = time.time()
        if client_ip not in self._token_buckets:
            self._token_buckets[client_ip] = self.burst_size
        tokens = self._token_buckets[client_ip]
        elapsed = now - self._last_update.get(client_ip, now)
        tokens = min(self.burst_size, tokens + elapsed * self.max_rps)
        if tokens < 1:
            return False
        self._token_buckets[client_ip] = tokens - 1
        self._last_update[client_ip] = now
        return True

    _last_update: Dict[str, float] = {}
```

### IP Whitelisting

```python
class IpWhitelist:
    def __init__(self):
        self._whitelisted: set = set()
        self._blacklisted: set = set()

    def add_whitelist(self, ip: str):
        self._whitelisted.add(ip)

    def add_blacklist(self, ip: str):
        self._blacklisted.add(ip)

    def is_allowed(self, ip: str) -> bool:
        if ip in self._blacklisted:
            return False
        if self._whitelisted and ip not in self._whitelisted:
            return False
        return True
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| uneven distribution | Some backends overloaded | Switch to least-connections algorithm |
| Session drops | Users logged out unexpectedly | Enable sticky sessions |
| SSL errors | HTTPS connection failures | Verify certificate chain, check SNI |
| High latency | Slow response times | Check connection pool size, backend health |
| Cascade failure | Multiple backends failing | Enable circuit breaker, adjust thresholds |
| DNS resolution failure | Can't reach load balancer | Check DNS configuration, use IP fallback |

### Debugging

```python
def debug_load_balancer(lb: LoadBalancer):
    stats = lb.get_stats()
    print("=== Load Balancer Status ===")
    print(f"Algorithm: {stats['algorithm']}")
    print(f"Total upstreams: {stats['total_upstreams']}")
    print(f"Healthy upstreams: {stats['healthy_upstreams']}")
    print(f"Total requests: {stats['total_requests']}")
    for u in stats['upstreams']:
        print(f"  {u['address']}: {u['connections']} conn, "
              f"{u['total_requests']} req, healthy={u['is_healthy']}, "
              f"circuit={u['circuit_state']}")
```

## API Reference

### Core Classes

| Class | Constructor | Key Methods |
|-------|-------------|-------------|
| `LoadBalancer(algorithm)` | `LbAlgorithm` | `add_upstream()`, `remove_upstream()`, `get_upstream()`, `get_stats()` |
| `Upstream(host, port, weight)` | `str, int, int` | `address`, `active_ratio` |
| `CircuitBreaker(threshold, timeout)` | `int, float` | `record_success()`, `record_failure()`, `can_attempt()` |
| `AdvancedHealthChecker(config)` | `LbConfig` | `check_tcp()`, `check_http()`, `is_truly_healthy()` |
| `RateLimiter(max_requests, window)` | `int, int` | `is_allowed()`, `get_usage()` |
| `ConnectionPool(max_size, timeout)` | `int, float` | `acquire()`, `release()`, `get_stats()` |
| `SessionPersistence(method)` | `str` | `get_upstream()` |
| `SslTerminator(cert, key)` | `str, str` | `add_certificate()`, `terminate_ssl()` |
| `DdosProtection(max_rps, burst)` | `int, int` | `is_allowed()` |

## Data Models

### Upstream Schema

```json
{
  "upstream": {
    "host": "string",
    "port": "int",
    "weight": "int",
    "max_connections": "int",
    "current_connections": "int",
    "total_requests": "int",
    "failure_count": "int",
    "is_healthy": "bool"
  }
}
```

### Health Check Result

```json
{
  "health_check": {
    "upstream": "string",
    "status": "healthy|unhealthy",
    "response_time_ms": "float",
    "last_check": "timestamp",
    "consecutive_failures": "int"
  }
}
```

## Deployment Guide

### Nginx Configuration

```nginx
upstream backend {
    least_conn;
    server 10.0.0.1:8080 weight=5;
    server 10.0.0.2:8080 weight=3;
    server 10.0.0.3:8080 backup;

    keepalive 32;
}

server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_connect_timeout 30s;
        proxy_read_timeout 30s;
    }
}
```

### Docker Deployment

```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY ssl/ /etc/ssl/
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
```

## Monitoring and Observability

### Metrics Dashboard

```python
@dataclass
class LbDashboard:
    total_requests: int = 0
    active_connections: int = 0
    healthy_upstreams: int = 0
    avg_latency_ms: float = 0.0
    error_rate: float = 0.0

    def get_dashboard(self) -> dict:
        return {
            "total_requests": self.total_requests,
            "active_connections": self.active_connections,
            "healthy_upstreams": self.healthy_upstreams,
            "avg_latency_ms": f"{self.avg_latency_ms:.1f}",
            "error_rate": f"{self.error_rate:.2%}",
        }
```

## Testing Strategy

### Load Testing

```python
class LoadTest:
    def __init__(self, target_url: str, concurrent: int = 100):
        self.target_url = target_url
        self.concurrent = concurrent
        self._results: List[dict] = []

    def run(self, duration_seconds: int = 60):
        import time
        import threading

        def worker():
            end_time = time.time() + duration_seconds
            while time.time() < end_time:
                start = time.time()
                try:
                    # Simulate request
                    latency = (time.time() - start) * 1000
                    self._results.append({"status": 200, "latency_ms": latency})
                except Exception as e:
                    self._results.append({"status": 500, "error": str(e)})

        threads = [threading.Thread(target=worker) for _ in range(self.concurrent)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def get_report(self) -> dict:
        if not self._results:
            return {}
        latencies = [r["latency_ms"] for r in self._results]
        return {
            "total_requests": len(self._results),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)],
            "error_rate": sum(1 for r in self._results if r.get("status", 200) != 200) / len(self._results),
        }
```

## Versioning and Migration

| Version | Changes |
|---------|---------|
| 2.0.0 | Circuit breaker, rate limiting, SSL termination, DDoS protection |
| 1.5.0 | Health checking, session persistence |
| 1.0.0 | Initial release with basic algorithms |

## Glossary

| Term | Definition |
|------|-----------|
| **Round Robin** | Sequential distribution across upstreams |
| **Least Connections** | Route to backend with fewest active connections |
| **Consistent Hash** | Hash-based routing with minimal redistribution |
| **Circuit Breaker** | Pattern to prevent cascade failures |
| **Health Check** | Periodic verification of backend availability |
| **SSL Termination** | TLS decryption at load balancer |
| **Session Persistence** | Sticky sessions via IP/cookie |
| **Connection Pool** | Reuse of backend connections |
| **Draining** | Graceful shutdown of connections |
| **DDoS** | Distributed Denial of Service attack |

## Changelog

- **2.0.0** - Circuit breaker, rate limiting, SSL, DDoS protection
- **1.5.0** - Health checking, session persistence
- **1.2.0** - Added connection pooling
- **1.1.0** - Enhanced metrics export
- **1.0.0** - Initial release

## Contributing Guidelines

1. Test with realistic load patterns
2. Verify health check accuracy
3. Benchmark algorithm performance
4. Document failover behavior

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills
