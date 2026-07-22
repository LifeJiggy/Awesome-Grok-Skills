---
name: "rate-limiting"
category: "api-gateway"
version: "2.0.0"
tags: ["rate-limiting", "throttling", "token-bucket", "sliding-window", "ddos", "backpressure"]
---

# Rate Limiting

## Overview

Distributed rate limiting platform for API gateways implementing multiple algorithms (token bucket, sliding window, fixed window, leaky bucket), per-user/per-endpoint/per-IP limiting, distributed counter synchronization via Redis, graceful degradation under load, and DDoS protection. Supports both API-level and consumer-level rate limits with burst allowances, priority queues, and automatic retry-after headers.

## Core Capabilities

- **Multiple Algorithms**: Token bucket, sliding window log, sliding window counter, fixed window, and leaky bucket
- **Granular Limits**: Per-IP, per-user, per-API-key, per-endpoint, per-method, and global rate limits
- **Distributed Counters**: Redis-backed distributed rate limit counters with atomic operations
- **Burst Handling**: Configurable burst allowances for short traffic spikes
- **Priority Queues**: Tiered rate limits (free/pro/enterprise) with priority-based request handling
- **Graceful Degradation**: Load shedding and backpressure when approaching limits
- **Retry-After Headers**: RFC 7231 compliant retry-after and rate limit headers
- **Analytics**: Real-time rate limit metrics, blocked request tracking, and abuse detection

## Usage

```python
from rate_limiting import (
    RateLimiter, Algorithm, RateLimit, ConsumerTier, SlidingWindow
)

# Configure rate limiter
limiter = RateLimiter(
    algorithm=Algorithm.SLIDING_WINDOW,
    storage="redis://localhost:6379",
    default_limit=1000,
    default_window_seconds=60,
)

# Add tiered limits
limiter.add_tier(ConsumerTier(
    name="free",
    requests_per_minute=60,
    requests_per_hour=1000,
    burst_allowance=10,
))
limiter.add_tier(ConsumerTier(
    name="pro",
    requests_per_minute=600,
    requests_per_hour=10000,
    burst_allowance=50,
))
limiter.add_tier(ConsumerTier(
    name="enterprise",
    requests_per_minute=6000,
    requests_per_hour=100000,
    burst_allowance=200,
))

# Add endpoint-specific limits
limiter.add_limit(RateLimit(
    endpoint="POST /api/auth/login",
    limit=5,
    window_seconds=60,
    key="ip",
    block_duration_seconds=900,  # 15 min lockout
))
limiter.add_limit(RateLimit(
    endpoint="GET /api/search",
    limit=30,
    window_seconds=60,
    key="user",
))

# Check rate limit
result = limiter.check(
    key="user-123",
    endpoint="GET /api/users",
    tier="pro",
)
print(f"Allowed: {result.allowed}")
print(f"Remaining: {result.remaining}/{result.limit}")
print(f"Reset: {result.reset_at}")
print(f"Headers: {result.headers}")
```

## Best Practices

- Apply rate limits at the gateway level to reject excessive requests before they reach services
- Use sliding window algorithms for smoother rate limiting without boundary spikes
- Set per-endpoint limits based on the resource cost of each endpoint
- Implement progressive rate limiting: warn Ã¢â€ â€™ throttle Ã¢â€ â€™ block
- Use token bucket for bursty traffic patterns where short bursts are acceptable
- Always return Retry-After headers so clients can implement proper backoff
- Monitor blocked requests to detect abuse patterns and adjust limits
- Implement circuit breakers alongside rate limits for defense in depth
- Use different keys (IP, user, API key) for different rate limiting dimensions
- Test rate limiting under realistic load to verify distributed counter accuracy

## Related Modules

- **api-management** Ã¢â‚¬â€ Gateway-level rate limiting integration
- **authentication** Ã¢â‚¬â€ Rate limiting tied to authenticated consumers
- **load-balancing** Ã¢â‚¬â€ Distribute rate-limited traffic across backends
- **api-security** Ã¢â‚¬â€ DDoS protection and abuse prevention
- **api-monitoring** Ã¢â‚¬â€ Rate limit metrics and alerting

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
| Rate limits not enforced | Redis connection failure | Check Redis connectivity, implement fallback |
| Counter drift | Clock skew between nodes | Use NTP sync, implement sliding window |
| False positives | Aggressive limits | Adjust limits based on actual traffic patterns |
| High Redis latency | Network congestion | Use Redis Cluster, optimize key design |
| Memory exhaustion | Too many unique keys | Implement key expiry, use bloom filters |

### Debug Mode

```yaml
# Enable debug logging for rate limiter
rate_limiter:
  debug: true
  log_blocked: true
  log_allowed: false
  metrics_enabled: true
```

```bash
# Check current rate limit status for a key
curl -s http://localhost:8080/rate-limits/status \
  -H "X-Key: user-123" | jq .

# View rate limit configuration
curl -s http://localhost:8080/rate-limits/config | jq .

# Manually reset a rate limit
curl -X POST http://localhost:8080/rate-limits/reset \
  -H "X-Key: user-123" \
  -H "X-Endpoint: /api/users"
```

### Redis Monitoring

```bash
# Check Redis rate limit keys
redis-cli KEYS "rate_limit:*" | head -20

# Monitor Redis operations in real-time
redis-cli MONITOR | grep rate_limit

# Check Redis memory usage
redis-cli INFO memory | grep used_memory_human

# View rate limit counters
redis-cli HGETALL "rate_limit:user-123:GET:/api/users"
```

## Security Hardening

### DDoS Protection Layers

| Layer | Protection | Configuration |
|-------|-----------|---------------|
| L3/L4 | Network rate limiting | Firewall rules, SYN cookies |
| L7 | HTTP rate limiting | Per-IP, per-user limits |
| Application | Business logic limits | Per-endpoint, per-tier limits |
| Global | Aggregate limits | Total request caps |

### Anti-Abuse Patterns

```yaml
# Progressive rate limiting for auth endpoints
auth_rate_limits:
  - endpoint: "POST /api/auth/login"
    rules:
      - limit: 5
        window: 60
        action: "block"
        duration: 300
      - limit: 10
        window: 300
        action: "block"
        duration: 900
      - limit: 20
        window: 3600
        action: "block"
        duration: 3600

# IP reputation-based limits
ip_reputation:
  enabled: true
  blocklist:
    - "203.0.113.0/24"
  throttle_threshold: 100  # requests per minute
  throttle_duration: 600
```

### Bot Detection

```yaml
bot_detection:
  enabled: true
  rules:
    - pattern: "python-requests"
      action: "throttle"
      limit: 10
      window: 60
    - pattern: "curl"
      action: "throttle"
      limit: 20
      window: 60
    - pattern: ".*bot.*"
      action: "captcha"
```

## Configuration Reference

### Token Bucket Algorithm

```yaml
token_bucket:
  enabled: true
  default_capacity: 100
  default_refill_rate: 10  # tokens per second
  refill_interval: 1       # seconds

  # Per-tier configuration
  tiers:
    free:
      capacity: 50
      refill_rate: 5
    pro:
      capacity: 500
      refill_rate: 50
    enterprise:
      capacity: 5000
      refill_rate: 500
```

### Sliding Window Algorithm

```yaml
sliding_window:
  enabled: true
  type: "counter"  # or "log"
  window_size: 60  # seconds

  # Precise counting with Redis
  precision: 10  # sub-windows for accuracy

  # Configuration
  storage: "redis"
  redis_url: "redis://localhost:6379"
  key_prefix: "rl:"
  key_expiry: 120  # seconds
```

### Fixed Window Algorithm

```yaml
fixed_window:
  enabled: true
  window_size: 60  # seconds
  max_requests: 1000

  # Alignment
  align_to_clock: true  # Align to clock boundaries
  reset_on_overflow: false  # Don't reset counter early
```

### Distributed Counter Configuration

```yaml
distributed_counters:
  storage: "redis"
  redis_url: "redis://localhost:6379"
  
  # Redis Cluster support
  cluster:
    enabled: false
    nodes:
      - "redis-1:6379"
      - "redis-2:6379"
      - "redis-3:6379"
  
  # Atomic operations
  atomic: true
  
  # Fallback behavior when Redis is down
  fallback:
    enabled: true
    mode: "local"  # Use local in-memory counters
    log_warning: true
```

## Migration Guide

### Algorithm Migration

```bash
# Export current rate limit config
rate-limiter-cli export --format yaml > config-v1.yaml

# Migrate from fixed window to sliding window
rate-limiter-cli migrate \
  --input config-v1.yaml \
  --output config-v2.yaml \
  --target-algorithm sliding_window

# Validate configuration
rate-limiter-cli validate --input config-v2.yaml

# Deploy with gradual rollout
rate-limiter-cli deploy \
  --input config-v2.yaml \
  --percentage 10 \
  --monitor-metrics
```

### Redis Migration

```bash
# Export rate limit data from Redis
redis-cli --scan --pattern "rate_limit:*" | \
  while read key; do
    redis-cli DUMP "$key" > "backup/$key.dump"
  done

# Import to new Redis cluster
for file in backup/*.dump; do
  key=$(basename "$file" .dump)
  redis-cli -h new-redis RESTORE "$key" 0 "$(cat "$file")"
done
```

## FAQ

**Q: How accurate are distributed rate limits?**
A: With Redis Cluster and atomic operations, accuracy is >99.9%. Occasional over-admission (<0.1%) may occur during network partitions.

**Q: What happens if Redis goes down?**
A: The system falls back to local in-memory counters. Rate limiting continues but may not be perfectly distributed across gateway instances.

**Q: Can I have different limits for different endpoints?**
A: Yes. Configure per-endpoint limits with different keys (IP, user, API key) and different algorithms.

**Q: How do I handle burst traffic?**
A: Use token bucket with burst allowance. Set `burst_capacity` higher than normal capacity for short spikes.

## Benchmarks

| Algorithm | Throughput | Latency p50 | Latency p99 | Memory/Key |
|-----------|-----------|-------------|-------------|------------|
| Token Bucket | 200,000 req/s | 0.2ms | 1ms | 64 bytes |
| Sliding Window (counter) | 180,000 req/s | 0.3ms | 1.5ms | 128 bytes |
| Sliding Window (log) | 150,000 req/s | 0.4ms | 2ms | 256 bytes |
| Fixed Window | 220,000 req/s | 0.1ms | 0.5ms | 32 bytes |
| Leaky Bucket | 190,000 req/s | 0.25ms | 1.2ms | 96 bytes |

## Code Examples

### Custom Rate Limit Key Generator

```python
class RateLimitKeyGenerator:
    def __init__(self, config):
        self.config = config

    def generate(self, request):
        """Generate rate limit key based on configuration."""
        parts = []

        # Add endpoint
        if self.config.get("include_endpoint"):
            parts.append(f"{request.method}:{request.path}")

        # Add identifier
        identifier_type = self.config.get("identifier", "ip")
        if identifier_type == "ip":
            parts.append(f"ip:{request.client_ip}")
        elif identifier_type == "user":
            parts.append(f"user:{request.user_id}")
        elif identifier_type == "api_key":
            parts.append(f"key:{request.api_key}")

        # Add tier
        if hasattr(request, "tier"):
            parts.append(f"tier:{request.tier}")

        return ":".join(parts)
```

### Rate Limit Middleware

```python
from functools import wraps

def rate_limit(endpoint, limit, window):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = generate_key(request)
            result = rate_limiter.check(key, endpoint, limit, window)

            if not result.allowed:
                return Response(
                    status=429,
                    headers={
                        "X-RateLimit-Limit": str(limit),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(result.reset_at),
                        "Retry-After": str(result.retry_after),
                    }
                )

            response = f(*args, **kwargs)
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = str(result.remaining)
            response.headers["X-RateLimit-Reset"] = str(result.reset_at)
            return response
        return wrapper
    return decorator

# Usage
@app.route("/api/users", methods=["GET"])
@rate_limit("GET /api/users", limit=100, window=60)
def get_users():
    return jsonify(users)
```

### Analytics Dashboard Query

```sql
-- Top rate-limited endpoints
SELECT
    endpoint,
    COUNT(*) as blocked_count,
    COUNT(DISTINCT client_key) as unique_clients
FROM rate_limit_events
WHERE action = 'blocked'
  AND timestamp > NOW() - INTERVAL '1 hour'
GROUP BY endpoint
ORDER BY blocked_count DESC
LIMIT 10;

-- Rate limit trends
SELECT
    DATE_TRUNC('minute', timestamp) as minute,
    COUNT(*) as total_requests,
    SUM(CASE WHEN action = 'blocked' THEN 1 ELSE 0 END) as blocked,
    ROUND(SUM(CASE WHEN action = 'blocked' THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100, 2) as block_rate
FROM rate_limit_events
WHERE timestamp > NOW() - INTERVAL '24 hours'
GROUP BY minute
ORDER BY minute;
```

## Advanced Monitoring

### Prometheus Metrics

```yaml
# Rate limit specific metrics
metrics:
  - name: "rate_limit_requests_total"
    type: "counter"
    labels: ["endpoint", "action", "tier"]
    description: "Total rate limit decisions"

  - name: "rate_limit_latency_seconds"
    type: "histogram"
    labels: ["endpoint"]
    description: "Rate limit check latency"

  - name: "rate_limit_redis_operations_total"
    type: "counter"
    labels: ["operation", "status"]
    description: "Redis operations for rate limiting"
```

### Alert Rules

```yaml
groups:
  - name: rate-limit-alerts
    rules:
      - alert: HighBlockRate
        expr: sum(rate(rate_limit_requests_total{action="blocked"}[5m])) / sum(rate(rate_limit_requests_total[5m])) > 0.3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High rate limit block rate (>30%)"

      - alert: RateLimitLatencyHigh
        expr: histogram_quantile(0.99, rate(rate_limit_latency_seconds_bucket[5m])) > 0.01
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Rate limit check latency >10ms"

      - alert: RedisDown
        expr: rate_limit_redis_operations_total{status="error"} > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Redis rate limit operations failing"
```

## Capacity Planning

### Rate Limit Resource Requirements

| Concurrent Users | Redis Memory | Redis Operations/sec | Gateway Instances |
|-----------------|--------------|---------------------|-------------------|
| 1K | 50MB | 1K | 1 |
| 10K | 200MB | 10K | 2 |
| 100K | 1GB | 100K | 4 |
| 1M | 8GB | 500K | 8 |

### Key Sizing

```
Key format: {prefix}:{endpoint}:{identifier}:{window}
Example: rl:GET:/api/users:user-123:1704067200

Average key size: 50 bytes
Keys per user per hour: ~10 (different endpoints)
Total keys for 100K users: 1M keys = 50MB Redis memory
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
