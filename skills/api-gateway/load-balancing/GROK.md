---
name: "load-balancing"
category: "api-gateway"
version: "2.0.0"
tags: ["load-balancing", "upstream", "round-robin", "weighted", "health-check", "sticky-session"]
---

# Load Balancing

## Overview

Gateway load balancing platform implementing multiple algorithms (round-robin, least connections, weighted round-robin, IP hash, consistent hashing, least response time) with health checking, weighted traffic splitting for canary deployments, sticky sessions, connection draining, and upstream health visualization. Supports both L4 (TCP) and L7 (HTTP) load balancing with configurable session affinity and graceful shutdown handling.

## Core Capabilities

- **Multiple Algorithms**: Round-robin, weighted round-robin, least connections, IP hash, consistent hashing, least response time
- **Health Checking**: Active (HTTP/TCP probes) and passive (error rate monitoring) health checks with configurable thresholds
- **Canary Deployments**: Weighted traffic splitting between upstream versions (90/10, 80/20, etc.)
- **Session Affinity**: Sticky sessions via cookie, header, or IP-based routing
- **Connection Draining**: Graceful connection draining during upstream removal or deployment
- **Failover**: Automatic failover to backup upstreams when primary is unhealthy
- **Circuit Breaking**: Per-upstream circuit breakers with configurable thresholds
- **Metrics**: Per-upstream latency, connection count, error rate, and throughput metrics

## Usage

```python
from load_balancing import (
    LoadBalancer, Algorithm, Upstream, HealthCheck, WeightedTarget
)

# Create load balancer
lb = LoadBalancer(algorithm=Algorithm.WEIGHTED_ROUND_ROBIN)

# Add upstream targets
lb.add_target(Upstream(
    name="api-v1-stable",
    address="10.0.1.10:8080",
    weight=90,
    max_connections=1000,
))
lb.add_target(Upstream(
    name="api-v2-canary",
    address="10.0.1.20:8080",
    weight=10,
    max_connections=200,
))

# Configure health checks
lb.set_health_check(Upstream(
    name="api-v1-stable",
    health_check=HealthCheck(
        type="http",
        path="/health",
        interval_s=5,
        timeout_s=2,
        healthy_threshold=2,
        unhealthy_threshold=3,
    ),
))

# Route a request
for i in range(20):
    target = lb.route(client_ip="192.168.1.100")
    print(f"Request {i+1}: → {target.name} ({target.address})")

# Get upstream metrics
for target in lb.get_all_targets():
    metrics = lb.get_target_metrics(target.name)
    print(f"\n{target.name}:")
    print(f"  Connections: {metrics['active_connections']}")
    print(f"  Requests: {metrics['total_requests']}")
    print(f"  Avg latency: {metrics['avg_latency_ms']:.1f}ms")
    print(f"  Health: {metrics['health_status']}")
```

## Best Practices

- Use weighted round-robin for canary deployments with gradual traffic shifting
- Implement aggressive health checks (5-second intervals) for latency-sensitive services
- Set connection limits per upstream to prevent resource exhaustion
- Use consistent hashing for stateful services requiring session affinity
- Implement connection draining (30-60 seconds) before removing upstreams
- Monitor per-upstream metrics to detect uneven load distribution
- Use circuit breakers alongside health checks for defense in depth
- Configure failover upstreams for critical services
- Set max connections based on upstream capacity to prevent overload
- Test load balancer behavior under upstream failure scenarios

## Related Modules

- **api-management** — Gateway-level load balancing configuration
- **rate-limiting** — Rate limiting applied before load balancing
- **caching** — Response caching to reduce upstream load
- **api-monitoring** — Upstream health and performance monitoring
- **api-gateway** → **authentication** — Auth before routing decisions
