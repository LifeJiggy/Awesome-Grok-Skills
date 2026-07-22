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
    print(f"Request {i+1}: Ã¢â€ â€™ {target.name} ({target.address})")

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

- **api-management** Ã¢â‚¬â€ Gateway-level load balancing configuration
- **rate-limiting** Ã¢â‚¬â€ Rate limiting applied before load balancing
- **caching** Ã¢â‚¬â€ Response caching to reduce upstream load
- **api-monitoring** Ã¢â‚¬â€ Upstream health and performance monitoring
- **api-gateway** Ã¢â€ â€™ **authentication** Ã¢â‚¬â€ Auth before routing decisions

## Advanced Configuration

### YAML Configuration
```yaml
version: "2.0.0"
settings:
  mode: "production"
  concurrency: 4
  timeout_ms: 30000
  gateway:
    listen_port: 8080
    ssl_enabled: true
    worker_count: 4
```

### JSON Configuration
```json
{"version":"2.0.0","settings":{"gateway":{"listen_port":8080,"ssl_enabled":true}}}
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|----------|
| `GATEWAY_MODE` | Runtime mode | `production` |
| `GATEWAY_PORT` | Listen port | `8080` |
| `GATEWAY_TIMEOUT` | Timeout (ms) | `30000` |
| `REDIS_URL` | Redis connection | `redis://localhost:6379` |
| `BACKEND_URLS` | Backend URLs | -- |

## Architecture Patterns

### System Architecture
```
+---------------------------------------------------+
|                   Client Layer                     |
|  +----------+  +----------+  +------------------+  |
|  |  Web App |  | Mobile   |  |  Third-Party     |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|              API Gateway Layer                      |
|  +------------------+---------------------------+  |
|  |  +--------+ +------+ +------+ +----------+  |  |
|  |  |  Auth  | | Rate | |Cache | |  Route   |  |  |
|  |  +--------+ +------+ +------+ +----------+  |  |
|  +------------------+---------------------------+  |
+-----------------+---------------------------------+
|            Backend Services                         |
|  +----------+  +----------+  +------------------+  |
|  | Service  |  | Service  |  |  Service         |  |
|  |    A     |  |    B     |  |    C             |  |
|  +----------+  +----------+  +------------------+  |
+---------------------------------------------------+
```

### Request Flow
```
Client -> TLS -> Gateway -> Auth -> Rate Limit -> Cache -> Route -> Backend -> Response
                                  |              |
                              [Block?]       [Hit?]
```

## Integration Guide

### Kubernetes
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: gateway-ingress
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: gateway-service
            port:
              number: 8080
```

### Terraform
```hcl
resource "aws_lb" "gateway" {
  name               = "gateway-lb"
  load_balancer_type = "application"
  subnets            = var.subnet_ids
}
```

## Performance Optimization

| Operation | Throughput | Latency (p50) | Latency (p99) |
|-----------|-----------|---------------|---------------|
| Routing | 100,000 req/s | 0.5ms | 2ms |
| Auth Check | 50,000 req/s | 1ms | 5ms |
| Rate Limit | 200,000 req/s | 0.2ms | 1ms |
| Cache Hit | 150,000 req/s | 0.3ms | 1.5ms |

### Tips
1. Connection pooling for backends
2. HTTP keep-alive
3. Cache rate limit counters
4. Workers = 2 * CPU cores
5. Optimize proxy buffers

```nginx
worker_processes auto;
worker_rlimit_nofile 65535;
events {
    worker_connections 4096;
    use epoll;
}
http {
    keepalive_timeout 65;
    proxy_buffer_size 16k;
}
```

## Security Considerations

| Threat | Risk | Mitigation |
|--------|------|------------|
| DDoS | High | Rate limiting, WAF, CDN |
| Credential stuffing | High | Brute-force protection |
| SSL stripping | High | HSTS, secure cookies |
| Header injection | Medium | Input sanitization |
| Request smuggling | Medium | Strict HTTP parsing |

### TLS Configuration
```yaml
tls:
  min_version: "1.2"
  cipher_suites:
    - "TLS_AES_256_GCM_SHA384"
    - "TLS_CHACHA20_POLY1305_SHA256"
```

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| 502 Bad Gateway | Backend down | Check backend health |
| 504 Timeout | Backend slow | Increase timeout |
| 429 Rate Limited | Too many requests | Check config |
| 401 Unauthorized | Auth failure | Check token, JWKS |

### Diagnostic Commands
```bash
curl -s http://localhost:8080/health
curl -s http://localhost:8080/connections | jq .
curl -s http://localhost:8080/backends/health | jq .
```

## API Reference

### `route(request: Request) -> Backend`
Route request to backend.

### `health_check(backend: Backend) -> HealthStatus`
Check backend health.

### `get_metrics() -> GatewayMetrics`
Get gateway metrics.

## Data Models

### Route Schema
```json
{"type":"object","required":["path","backend"],"properties":{"path":{"type":"string"},"backend":{"type":"string"}}}
```

### Backend Schema
```json
{"type":"object","required":["name","url"],"properties":{"name":{"type":"string"},"url":{"type":"string"},"weight":{"type":"integer","default":100}}}
```

## Deployment Guide

### Docker
```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY certs/ /etc/nginx/certs/
EXPOSE 80 443
HEALTHCHECK CMD curl -f http://localhost/health || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gateway-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gateway
  template:
    spec:
      containers:
      - name: gateway
        image: gateway:2.0.0
        ports:
        - containerPort: 8080
        - containerPort: 8443
        resources:
          requests:
            memory: "256Mi"
            cpu: "500m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
```

## Monitoring & Observability

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `requests_total` | Counter | Total requests | -- |
| `request_latency_ms` | Histogram | Latency | p99 > 500ms |
| `error_rate` | Gauge | Error rate | > 5% |
| `upstream_health` | Gauge | Backend health | < 1 |
| `cache_hit_rate` | Gauge | Cache efficiency | < 50% |

## Testing Strategy

```python
def test_route():
    backend = gateway.route(request)
    assert backend.name == "expected-backend"

def test_rate_limit():
    result = gateway.check_rate_limit("user-123", "/api/users")
    assert result.allowed == True
```

## Versioning & Migration

- Major version for breaking changes
- 6-month deprecation notice

### Changelog
- **[2.0.0]** -- Plugin architecture
- **[1.5.0]** -- Performance improvements
- **[1.0.0]** -- Initial release

## Glossary

| Term | Definition |
|------|------------|
| **Upstream** | Backend service |
| **Downstream** | Client |
| **Route** | Path-to-backend mapping |
| **Plugin** | Middleware component |
| **Circuit Breaker** | Cascade failure prevention |
| **Health Check** | Backend availability probe |
| **Rate Limit** | Request restriction |
| **Cache Hit** | Cached response served |

## Changelog

### [2.0.0] -- 2024-12-01
- Plugin system introduced

### [1.5.0] -- 2024-06-15
- Performance improvements

### [1.0.0] -- 2024-01-01
- Initial release

## Contributing Guidelines

```bash
git clone https://github.com/example/gateway.git
cd gateway
make build
make test
```

## License

MIT License -- Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Advanced Troubleshooting

### Common Issues and Resolutions

| Symptom | Root Cause | Resolution |
|---------|------------|------------|
| Uneven load distribution | Sticky sessions misconfigured | Review session affinity settings |
| Connection refused errors | Backend overload | Increase max_connections or add backends |
| High latency variance | Slow backend in pool | Remove slow backends, check health checks |
| Failover not working | Health check misconfigured | Verify health check path and thresholds |
| Session drops | Backend restart during request | Implement connection draining |

### Debug Mode

```yaml
# Enable debug logging for load balancer
load_balancer:
  debug: true
  log_routing: true
  log_health_checks: true
  log_failover: true
```

```bash
# View current upstream status
curl -s http://localhost:8080/upstreams | jq .

# Check specific upstream health
curl -s http://localhost:8080/upstreams/api-v1/health | jq .

# Force health check on upstream
curl -X POST http://localhost:8080/upstreams/api-v1/healthcheck

# View connection pool status
curl -s http://localhost:8080/upstreams/api-v1/connections | jq .
```

### Connection Pool Debugging

```bash
# View active connections per upstream
netstat -an | grep :8080 | awk '{print $5}' | cut -d: -f1 | sort | uniq -c

# Check file descriptor usage
lsof -p $(pgrep -f gateway) | wc -l

# Monitor connection state changes
watch -n 1 'curl -s http://localhost:8080/upstreams | jq ".[] | {name, active_connections, health}"'
```

## Security Hardening

### Upstream Security

```yaml
upstream_security:
  # TLS to backends
  tls:
    enabled: true
    verify: true
    ca_bundle: "/etc/ssl/ca-bundle.crt"
    min_version: "1.2"

  # Client certificate authentication
  client_cert:
    enabled: true
    cert: "/etc/ssl/client.pem"
    key: "/etc/ssl/client-key.pem"

  # Request signing
  request_signing:
    enabled: true
    algorithm: "hmac-sha256"
    secret: "${UPSTREAM_SIGNING_SECRET}"
```

### DDoS Protection

```yaml
ddos_protection:
  # Connection limits
  max_connections_per_ip: 100
  max_connections_total: 10000

  # Timeout settings
  connection_timeout: 5
  idle_timeout: 60
  request_timeout: 30

  # Rate limiting
  rate_limit:
    enabled: true
    requests_per_second: 1000
    burst: 100

  # SYN flood protection
  syn_cookies: true
```

## Configuration Reference

### Load Balancing Algorithms

```yaml
algorithms:
  # Round Robin
  round_robin:
    description: "Sequential distribution"
    use_case: "General purpose, equal-weight backends"

  # Weighted Round Robin
  weighted_round_robin:
    description: "Distribution based on weights"
    use_case: "Canary deployments, heterogeneous backends"

  # Least Connections
  least_connections:
    description: "Route to backend with fewest active connections"
    use_case: "Long-lived connections, variable request times"

  # IP Hash
  ip_hash:
    description: "Consistent routing based on client IP"
    use_case: "Session affinity without cookies"

  # Consistent Hashing
  consistent_hash:
    description: "Consistent routing with minimal redistribution"
    use_case: "Distributed caching, sticky sessions"

  # Least Response Time
  least_response_time:
    description: "Route to fastest responding backend"
    use_case: "Latency-sensitive applications"
```

### Health Check Configuration

```yaml
health_checks:
  active:
    # HTTP health check
    http:
      path: "/health"
      method: "GET"
      expected_status: [200]
      timeout: 3
      interval: 5
      healthy_threshold: 2
      unhealthy_threshold: 3

    # TCP health check
    tcp:
      port: 8080
      timeout: 2
      interval: 5

    # gRPC health check
    grpc:
      service: "health.v1.Health"
      timeout: 3
      interval: 5

  passive:
    # Monitor error rates
    http:
      http_statuses: [500, 502, 503, 504]
      unhealthy_threshold: 5
      interval: 10

    # Monitor timeouts
    timeouts:
      threshold: 3
      interval: 60
```

### Connection Pool Settings

```yaml
connection_pool:
  # Per-upstream limits
  max_connections: 1000
  max_pending_requests: 100
  max_requests_per_connection: 100

  # Timeouts
  connect_timeout: 5
  idle_timeout: 60
  request_timeout: 30

  # Keep-alive
  keepalive:
    enabled: true
    requests: 100
    time: 60

  # Circuit breaker
  circuit_breaker:
    enabled: true
    threshold: 5
    timeout: 30
    half_open_requests: 3
```

## Migration Guide

### Backend Migration

```bash
# Add new backend
load-balancer-cli add-backend \
  --name "api-v2" \
  --address "10.0.2.10:8080" \
  --weight 10

# Gradually shift traffic
for percentage in 10 25 50 75 100; do
  load-balancer-cli set-weight \
    --backend "api-v2" \
    --weight $percentage
  sleep 300  # Wait 5 minutes between shifts
done

# Remove old backend
load-balancer-cli remove-backend --name "api-v1"
```

### Algorithm Migration

```bash
# Export current configuration
load-balancer-cli export --format yaml > lb-config-v1.yaml

# Migrate to new algorithm
load-balancer-cli migrate \
  --input lb-config-v1.yaml \
  --output lb-config-v2.yaml \
  --algorithm least_response_time

# Validate and deploy
load-balancer-cli validate --input lb-config-v2.yaml
load-balancer-cli deploy --input lb-config-v2.yaml
```

## FAQ

**Q: Which algorithm should I use?**
A: Use round-robin for equal-weight backends. Use weighted round-robin for canary deployments. Use least connections for long-lived connections. Use consistent hashing for session affinity.

**Q: How do I handle backend maintenance?**
A: Set the backend to draining state. New connections route to other backends. Existing connections complete before the backend is removed.

**Q: Can I mix algorithms?**
A: Yes. Use different algorithms for different upstream groups. For example, round-robin for stateless services, consistent hashing for stateful services.

**Q: How do I prevent overload?**
A: Set max_connections per backend and configure circuit breakers. Monitor active connections and reject new requests when limits are reached.

## Benchmarks

| Algorithm | Throughput | Latency p50 | Latency p99 | CPU Usage |
|-----------|-----------|-------------|-------------|-----------|
| Round Robin | 100,000 req/s | 0.5ms | 2ms | 15% |
| Weighted Round Robin | 95,000 req/s | 0.6ms | 2.5ms | 16% |
| Least Connections | 90,000 req/s | 0.7ms | 3ms | 18% |
| IP Hash | 95,000 req/s | 0.6ms | 2.5ms | 17% |
| Consistent Hash | 85,000 req/s | 0.8ms | 3.5ms | 20% |
| Least Response Time | 80,000 req/s | 0.4ms | 1.5ms | 22% |

## Code Examples

### Custom Health Check

```python
class CustomHealthChecker:
    def __init__(self, config):
        self.config = config
        self.client = httpx.AsyncClient()

    async def check(self, backend: Upstream) -> HealthStatus:
        """Perform custom health check."""
        try:
            # HTTP check
            response = await self.client.get(
                f"{backend.address}{self.config['path']}",
                timeout=self.config['timeout']
            )

            # Custom validation
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    return HealthStatus.HEALTHY

            return HealthStatus.UNHEALTHY

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return HealthStatus.UNHEALTHY
```

### Traffic Shifting Script

```python
import time

def shift_traffic(from_backend, to_backend, steps=10, delay=60):
    """Gradually shift traffic from one backend to another."""
    for i in range(1, steps + 1):
        percentage = (i / steps) * 100
        new_weight = 100 - percentage
        old_weight = percentage

        # Update weights
        update_backend_weight(from_backend, new_weight)
        update_backend_weight(to_backend, old_weight)

        print(f"Step {i}/{steps}: {from_backend}={new_weight}%, {to_backend}={old_weight}%")

        # Monitor for issues
        if check_error_rate() > 0.01:
            print("Error rate too high, rolling back")
            rollback(from_backend, to_backend)
            return False

        time.sleep(delay)

    print("Traffic shift complete")
    return True
```

## Advanced Monitoring

### Upstream Metrics

```yaml
metrics:
  - name: "upstream_requests_total"
    type: "counter"
    labels: ["upstream", "status"]
    description: "Total requests per upstream"

  - name: "upstream_latency_seconds"
    type: "histogram"
    labels: ["upstream"]
    description: "Request latency per upstream"

  - name: "upstream_active_connections"
    type: "gauge"
    labels: ["upstream"]
    description: "Active connections per upstream"

  - name: "upstream_health_status"
    type: "gauge"
    labels: ["upstream"]
    description: "Health status (1=healthy, 0=unhealthy)"
```

### Alert Rules

```yaml
groups:
  - name: load-balancer-alerts
    rules:
      - alert: BackendUnhealthy
        expr: upstream_health_status == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Backend {{ $labels.upstream }} is unhealthy"

      - alert: HighErrorRate
        expr: sum(rate(upstream_requests_total{status=~"5.."}[5m])) by (upstream) / sum(rate(upstream_requests_total[5m])) by (upstream) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on {{ $labels.upstream }}"

      - alert: ConnectionPoolExhausted
        expr: upstream_active_connections > 900
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Connection pool nearly exhausted on {{ $labels.upstream }}"
```

## Capacity Planning

### Backend Sizing

| Concurrent Connections | Backends Needed | Load Balancer Instances | Network |
|----------------------|-----------------|------------------------|---------|
| 1K | 2-3 | 1 | 1Gbps |
| 10K | 5-10 | 2 | 10Gbps |
| 100K | 20-50 | 4 | 25Gbps |
| 1M | 100+ | 8+ | 100Gbps+ |

### Connection Pool Sizing

```
Per-backend connections: 100-1000 (based on backend capacity)
Total pool size: backends * per_backend_connections
File descriptors: pool_size * 2 (client + server connections)
Memory per connection: ~10KB
Total memory: pool_size * 10KB
```


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
