---
name: "caching"
category: "api-gateway"
version: "2.0.0"
tags: ["caching", "cdn", "redis", "cache-invalidation", "response-cache", "ttl", "edge-cache"]
---

# Gateway Caching

## Overview

Gateway-level response caching platform for reducing upstream load and improving API response times. This module implements in-memory, Redis-backed, and CDN edge caching with configurable TTLs, cache key strategies, ETag-based conditional requests, cache invalidation (manual, TTL, event-driven), and cache warming. Supports per-endpoint cache policies, vary headers, cache-busting, and stale-while-revalidate patterns.

## Core Capabilities

- **Multi-Layer Caching**: In-memory (L1), Redis (L2), and CDN edge (L3) caching hierarchy
- **Cache Key Strategies**: URL-based, header-based, query-param-based, and custom cache key functions
- **Conditional Requests**: ETag and Last-Modified headers for 304 Not Modified responses
- **Cache Invalidation**: TTL-based, manual purge, event-driven, and pattern-based invalidation
- **Stale-While-Revalidate**: Serve stale responses while refreshing in background
- **Vary Headers**: Cache different variants based on Accept, Accept-Language, or custom headers
- **Cache Warming**: Pre-populate cache for critical endpoints on startup or schedule
- **Metrics**: Cache hit rate, miss rate, size, eviction count, and per-endpoint statistics

## Usage

```python
from caching import (
    CacheManager, CacheLayer, CachePolicy, CacheKey, ETagHandler
)

# Initialize cache manager
cache = CacheManager(
    l1_size_mb=256,
    l2_redis_url="redis://localhost:6379",
    default_ttl_seconds=300,
)

# Configure per-endpoint policies
cache.add_policy(CachePolicy(
    endpoint="GET /api/products",
    ttl_seconds=600,
    vary_headers=["Accept-Language"],
    cache_key=CacheKey(
        include_path=True,
        include_query=True,
        include_headers=["Authorization"],
        exclude_query_params=["timestamp"],
    ),
    stale_while_revalidate_s=60,
    stale_if_error_s=3600,
))

cache.add_policy(CachePolicy(
    endpoint="GET /api/config",
    ttl_seconds=3600,
    vary_headers=[],
    tags=["config"],
))

# Check cache
result = cache.get(
    key="GET /api/products?category=electronics",
    headers={"Accept-Language": "en"},
)
if result.hit:
    print(f"Cache HIT: {result.data}")
    print(f"Age: {result.age_seconds}s, TTL: {result.ttl_seconds}s")
else:
    # Fetch from upstream and cache
    data = fetch_from_upstream()
    cache.set(key=result.key, value=data, ttl=300, tags=["products"])

# ETag handling
etag_handler = ETagHandler()
etag = etag_handler.generate(data)
if etag_handler.check_match(request_headers, etag):
    return Response(status=304)

# Cache invalidation
cache.invalidate_pattern("/api/products/*")
cache.invalidate_tag("products")

# Metrics
metrics = cache.get_metrics()
print(f"Hit rate: {metrics['hit_rate']:.1%}")
print(f"Total hits: {metrics['hits']}, misses: {metrics['misses']}")
print(f"Memory used: {metrics['l1_size_mb']:.1f} MB")
```

## Best Practices

- Cache at the gateway level to reduce load on all backend services
- Use appropriate TTLs: short (1-5 min) for dynamic data, long (1hr+) for static
- Implement cache warming for critical endpoints to avoid cold-start misses
- Use ETag-based conditional requests to reduce bandwidth and improve freshness
- Implement stale-while-revalidate for high-traffic endpoints to serve stale data during refresh
- Use cache tags for efficient bulk invalidation when related data changes
- Monitor cache hit rates per endpoint — below 50% suggests misconfigured policies
- Set appropriate cache size limits to prevent memory exhaustion
- Use Vary headers correctly to cache personalized responses without over-caching
- Test cache behavior under load to verify eviction and refresh patterns

## Related Modules

- **api-management** — Gateway-level caching plugin configuration
- **load-balancing** — Cache-aware load balancing decisions
- **rate-limiting** — Cached rate limit counters for performance
- **api-monitoring** — Cache metrics and hit rate monitoring
- **api** → **api-design** — Cache-friendly API design patterns

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
| Low hit rate | Cache key mismatch | Review cache key generation logic |
| Stale data served | TTL too long | Reduce TTL, implement invalidation |
| Cache stampede | Thundering herd on expiry | Implement stale-while-revalidate |
| Memory exhaustion | No eviction policy | Set max memory limits, LRU eviction |
| Cache inconsistency | Multiple cache layers | Use distributed cache invalidation |

### Debug Mode

```yaml
# Enable debug logging for cache
cache:
  debug: true
  log_hits: true
  log_misses: true
  log_invalidations: true
  trace_headers: true
```

```bash
# Check cache status
curl -s http://localhost:8080/cache/status | jq .

# View cache statistics
curl -s http://localhost:8080/cache/stats | jq .

# Manually invalidate cache
curl -X POST http://localhost:8080/cache/invalidate \
  -H "Content-Type: application/json" \
  -d '{"pattern": "/api/products/*"}'

# Warm cache for endpoint
curl -X POST http://localhost:8080/cache/warm \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "GET /api/products"}'
```

### Cache Debugging

```python
# Debug cache key generation
def debug_cache_key(request):
    key_parts = []
    key_parts.append(f"method:{request.method}")
    key_parts.append(f"path:{request.path}")
    key_parts.append(f"query:{sorted(request.query_params.items())}")

    if request.headers.get("Accept-Language"):
        key_parts.append(f"lang:{request.headers['Accept-Language']}")

    cache_key = ":".join(key_parts)
    print(f"Cache key: {cache_key}")
    print(f"Key hash: {hash(cache_key)}")

    return cache_key
```

## Security Hardening

### Cache Security

```yaml
cache_security:
  # Never cache sensitive data
  exclude_paths:
    - "/api/auth/*"
    - "/api/user/profile"
    - "/api/payments/*"

  # Exclude sensitive headers from cache key
  exclude_headers:
    - "Authorization"
    - "Cookie"
    - "X-API-Key"

  # Cache encryption
  encryption:
    enabled: false  # Enable for sensitive cached data
    algorithm: "aes-256-gcm"
    key: "${CACHE_ENCRYPTION_KEY}"

  # Access control
  access_control:
    enabled: true
    allowed_origins:
      - "https://app.example.com"
```

### Cache Poisoning Prevention

```yaml
cache_poisoning_prevention:
  # Validate cache keys
  validate_keys: true
  max_key_length: 256

  # Rate limit cache operations
  rate_limit:
    enabled: true
    max_sets_per_minute: 1000
    max_gets_per_minute: 10000

  # Audit cache changes
  audit:
    enabled: true
    log_all_invalidations: true
```

## Configuration Reference

### Cache Key Strategies

```yaml
cache_keys:
  # URL-based
  url_based:
    include_path: true
    include_query: true
    sort_query_params: true
    exclude_params: ["timestamp", "nocache"]

  # Header-based
  header_based:
    include:
      - "Accept"
      - "Accept-Language"
    exclude:
      - "Authorization"
      - "Cookie"

  # Custom functions
  custom:
    - name: "user_cache"
      function: "generate_user_cache_key"
      config:
        include_user_id: true
        include_tenant: true
```

### TTL Configuration

```yaml
ttl_config:
  # Default TTLs by content type
  defaults:
    static: 86400      # 24 hours
    dynamic: 300       # 5 minutes
    api: 60            # 1 minute
    user_specific: 0   # No caching

  # Per-endpoint overrides
  endpoints:
    "GET /api/products":
      ttl: 600
      stale_while_revalidate: 60
      stale_if_error: 3600
    "GET /api/config":
      ttl: 3600
      stale_while_revalidate: 300
    "GET /api/user/{id}":
      ttl: 0  # Don't cache user-specific data
```

### Cache Invalidation

```yaml
invalidation:
  # TTL-based
  ttl:
    enabled: true

  # Manual purge
  manual:
    enabled: true
    api_endpoint: "/cache/invalidate"

  # Event-driven
  events:
    enabled: true
    channels:
      - "product:updated"
      - "config:changed"

  # Pattern-based
  patterns:
    enabled: true
    support_wildcards: true

  # Tag-based
  tags:
    enabled: true
    max_tags_per_entry: 10
```

## Migration Guide

### Cache Backend Migration

```bash
# Export current cache config
cache-cli export --format yaml > cache-config-v1.yaml

# Migrate from in-memory to Redis
cache-cli migrate \
  --input cache-config-v1.yaml \
  --output cache-config-v2.yaml \
  --target redis://new-redis:6379

# Warm cache after migration
cache-cli warm --config cache-config-v2.yaml --endpoints all

# Validate migration
cache-cli validate --config cache-config-v2.yaml
```

### CDN Migration

```bash
# Purge old CDN cache
curl -X PURGE https://cdn.example.com/*

# Update CDN configuration
cache-cli cdn configure \
  --provider "new-cdn" \
  --api-key "${CDN_API_KEY}"

# Test CDN caching
curl -I https://api.example.com/api/products | grep -i "cache"
```

## FAQ

**Q: What's the ideal cache hit rate?**
A: Aim for 80%+ for static content, 50%+ for dynamic API responses. Below 50% suggests misconfigured policies.

**Q: How do I handle cache stampede?**
A: Implement stale-while-revalidate. Serve stale content while refreshing in background. Use distributed locks for cache warming.

**Q: Can I cache POST requests?**
A: Generally no, but you can cache responses to idempotent POST requests if the response is deterministic. Use POST body hash as part of cache key.

**Q: How do I handle cache invalidation?**
A: Use tag-based invalidation for related data. Implement event-driven invalidation for real-time updates. Fall back to TTL for eventual consistency.

## Benchmarks

| Operation | Throughput | Latency p50 | Latency p99 | Memory/Entry |
|-----------|-----------|-------------|-------------|--------------|
| L1 (in-memory) | 500,000 req/s | 0.05ms | 0.2ms | 256 bytes |
| L2 (Redis) | 150,000 req/s | 0.3ms | 1.5ms | 512 bytes |
| L3 (CDN) | 1,000,000 req/s | 0.01ms | 0.1ms | N/A |
| Cache invalidation | 50,000 ops/s | 0.5ms | 2ms | N/A |
| Cache warming | 10,000 keys/s | 1ms | 5ms | N/A |

## Code Examples

### Custom Cache Store

```python
class CustomCacheStore:
    def __init__(self, config):
        self.config = config
        self.redis = redis.Redis.from_url(config["redis_url"])
        self.local_cache = {}

    async def get(self, key: str) -> Optional[CacheEntry]:
        """Get from cache with L1/L2 fallback."""
        # Check L1 (local)
        if key in self.local_cache:
            entry = self.local_cache[key]
            if not entry.is_expired():
                return entry
            del self.local_cache[key]

        # Check L2 (Redis)
        data = await self.redis.get(key)
        if data:
            entry = CacheEntry.from_json(data)
            if not entry.is_expired():
                # Populate L1
                self.local_cache[key] = entry
                return entry

        return None

    async def set(self, key: str, value: Any, ttl: int, tags: List[str] = None):
        """Set in both L1 and L2."""
        entry = CacheEntry(value=value, ttl=ttl, tags=tags or [])

        # Set in L2 (Redis)
        await self.redis.setex(key, ttl, entry.to_json())

        # Set in L1 (local)
        self.local_cache[key] = entry
```

### Cache Warming Script

```python
import asyncio
import httpx

async def warm_cache(endpoints: List[str], concurrency: int = 10):
    """Warm cache for specified endpoints."""
    semaphore = asyncio.Semaphore(concurrency)
    client = httpx.AsyncClient()

    async def warm_endpoint(endpoint: str):
        async with semaphore:
            response = await client.get(f"http://localhost:8080{endpoint}")
            print(f"Warmed {endpoint}: {response.status_code}")

    tasks = [warm_endpoint(ep) for ep in endpoints]
    await asyncio.gather(*tasks)
    await client.aclose()

# Usage
endpoints = [
    "/api/products",
    "/api/categories",
    "/api/config",
]
asyncio.run(warm_cache(endpoints))
```

## Advanced Monitoring

### Cache Metrics

```yaml
metrics:
  - name: "cache_hits_total"
    type: "counter"
    labels: ["layer", "endpoint"]
    description: "Total cache hits"

  - name: "cache_misses_total"
    type: "counter"
    labels: ["layer", "endpoint"]
    description: "Total cache misses"

  - name: "cache_size_bytes"
    type: "gauge"
    labels: ["layer"]
    description: "Current cache size"

  - name: "cache_evictions_total"
    type: "counter"
    labels: ["layer", "reason"]
    description: "Total cache evictions"

  - name: "cache_latency_seconds"
    type: "histogram"
    labels: ["layer", "operation"]
    description: "Cache operation latency"
```

### Alert Rules

```yaml
groups:
  - name: cache-alerts
    rules:
      - alert: LowHitRate
        expr: sum(rate(cache_hits_total[5m])) / (sum(rate(cache_hits_total[5m])) + sum(rate(cache_misses_total[5m]))) < 0.5
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Cache hit rate below 50%"

      - alert: HighEvictionRate
        expr: rate(cache_evictions_total[5m]) > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High cache eviction rate"

      - alert: CacheMemoryHigh
        expr: cache_size_bytes / 1024 / 1024 > 1024
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Cache memory usage > 1GB"
```

## Capacity Planning

### Cache Sizing

| Daily Requests | Hit Rate | Cache Size | Redis Memory | Eviction Rate |
|---------------|----------|------------|--------------|---------------|
| 1M | 80% | 100MB | 200MB | Low |
| 10M | 70% | 500MB | 1GB | Medium |
| 100M | 60% | 2GB | 4GB | High |
| 1B | 50% | 10GB | 20GB | Very High |

### Cache Key Sizing

```
Average key size: 100 bytes
Average value size: 2KB
Entries per endpoint: 10,000
Total endpoints: 100
Total cache entries: 1M
Total cache size: 2GB + 100MB keys = 2.1GB
```
