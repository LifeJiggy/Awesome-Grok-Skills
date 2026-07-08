# API Gateway Agent

> Enterprise API gateway with routing, authentication, rate limiting, caching, circuit breaking, load balancing, transformation, and analytics.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Configuration](#configuration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

---

## Overview

The API Gateway Agent provides an enterprise-grade API gateway in a single Python module. It handles the complete request lifecycle — from client authentication through upstream routing, response transformation, and analytics — with built-in resilience patterns (circuit breakers, retries, rate limiting) and security hardening (JWT validation, CORS, TLS configuration, IP filtering).

### What It Does

- **Routing**: Dynamic path matching with wildcards, parameterized paths, and method validation
- **Authentication**: API key, JWT, OAuth2, Basic Auth, and mTLS support
- **Rate Limiting**: Token Bucket, Sliding Window, Fixed Window, and Leaky Bucket algorithms
- **Load Balancing**: Round Robin, Weighted, Least Connections, IP Hash, Consistent Hash, Random
- **Resilience**: Per-upstream circuit breakers, configurable timeouts, retry with backoff
- **Transformation**: Request/response body transforms (JSON↔XML, field ops, base64, masking)
- **Caching**: In-memory TTL cache with pattern invalidation and stale-while-revalidate
- **Analytics**: Per-endpoint, per-status, per-auth-type metrics; cache hit ratio; latency tracking
- **Plugins**: Extensible hook system (on_request, on_response, on_error)
- **Security**: CORS, security headers, IP whitelist/blacklist, request size limits

---

## Features

| Feature | Description |
|---------|-------------|
| Dynamic Routing | Wildcards, parameterized paths, method validation |
| Multi-Auth | API key, JWT, OAuth2, Basic Auth, mTLS |
| 4 Rate Limiters | Token Bucket, Sliding Window, Fixed Window, Leaky Bucket |
| 6 LB Strategies | Round Robin, Weighted, Least Connections, IP Hash, Consistent Hash, Random |
| Circuit Breakers | Per-upstream CLOSED → OPEN → HALF_OPEN state machine |
| Request Transform | Field rename/add/remove, value mapping, base64, masking |
| Response Transform | JSON↔XML, header injection, body redaction |
| In-Memory Cache | LRU-inspired with TTL, pattern invalidation, stale-while-revalidate |
| Structured Logging | Request IDs, latency, upstream, auth type — sensitive headers excluded |
| Plugin System | Sequential hook chain: on_request → route → upstream → on_response → on_error |
| Security Headers | HSTS, X-Frame-Options, CSP, Referrer-Policy, Permissions-Policy |
| Config Import/Export | JSON-serializable state for backup and disaster recovery |

---

## Quick Start

```python
from agents.api_gateway.agent import (
    APIGatewayAgent, GatewayConfig, EndpointConfig,
    HTTPMethod, AuthType, GatewayEnvironment
)

config = GatewayConfig(
    name="production-gateway",
    environment=GatewayEnvironment.PRODUCTION,
    endpoint_configs=[
        EndpointConfig(
            path="/api/v1/users",
            methods=[HTTPMethod.GET, HTTPMethod.POST],
            upstream_url="http://user-service:8080",
            auth_type=AuthType.JWT,
            rate_limit=100,
        ),
    ],
)
agent = APIGatewayAgent(config)
agent.configure_gateway(config)
agent.start()

result = agent.simulate_request("GET", "/api/v1/users", headers={"authorization": "Bearer <jwt>"})
print(result)
```

### Run the Agent

```bash
python agents/api-gateway/agent.py
```

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

### Optional Dependencies

```bash
pip install cryptography pyjwt redis prometheus-client
```

---

## Usage

### Complete Gateway Setup

```python
from agents.api_gateway.agent import (
    APIGatewayAgent, GatewayConfig, EndpointConfig,
    HTTPMethod, AuthType, RateLimitAlgorithm,
    LoadBalancingStrategy, GatewayEnvironment
)

# 1. Configure the gateway
config = GatewayConfig(
    name="my-gateway",
    environment=GatewayEnvironment.PRODUCTION,
    host="0.0.0.0",
    port=8080,
    endpoint_configs=[
        EndpointConfig(
            path="/api/v1/users/*",
            methods=[HTTPMethod.GET, HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.DELETE],
            upstream_url="http://user-service:8080",
            auth_type=AuthType.JWT,
            rate_limit=100,
            rate_limit_window=60,
            caching_enabled=True,
            cache_ttl_seconds=300,
            cors_enabled=True,
            cors_origins=["https://app.example.com"],
        ),
        EndpointConfig(
            path="/api/v1/products/*",
            methods=[HTTPMethod.GET],
            upstream_url="http://product-service:8080",
            auth_type=AuthType.API_KEY,
            rate_limit=500,
            caching_enabled=True,
            cache_ttl_seconds=60,
        ),
    ],
    auth_config=AuthConfig(jwt_secret="super-secret", jwt_expiry_hours=24),
    rate_limit_config=RateLimitConfig(
        default_requests_per_window=1000,
        ip_whitelist=["10.0.0.0/8"],
        ip_blacklist=["192.168.1.100"],
    ),
)

# 2. Start the gateway
agent = APIGatewayAgent(config)
agent.configure_gateway(config)
agent.start()

# 3. Simulate requests
result = agent.simulate_request("GET", "/api/v1/users/123", headers={"authorization": "Bearer <jwt>"})
print(f"Status: {result['status']}, Latency: {result['latency_ms']}ms")
```

### Load Balancing

```python
# Create a pool with 3 backend servers
agent.create_upstream_pool("payment-service", LoadBalancingStrategy.LEAST_CONNECTIONS)
for i in range(3):
    agent.add_upstream_server(
        "/api/v1/payments",
        UpstreamServer(url=f"http://payment-{i}:8080", weight=100)
    )

# Mark a server unhealthy
agent.update_upstream_health("http://payment-0:8080", is_healthy=False)

# Check pool status
stats = agent.get_statistics()
print(stats["upstream_pools"]["payment-service"])
```

### Rate Limiting

```python
# Token Bucket for search (burst-friendly)
agent.configure_rate_limit("/api/v1/search", 30, algorithm=RateLimitAlgorithm.TOKEN_BUCKET)

# Sliding Window for reads (smooth)
agent.configure_rate_limit("/api/v1/products", 200, algorithm=RateLimitAlgorithm.SLIDING_WINDOW)

# Leaky Bucket for writes (constant rate)
agent.configure_rate_limit("/api/v1/orders", 10, algorithm=RateLimitAlgorithm.LEAKY_BUCKET)
```

### Caching

```python
# Check cache stats
stats = agent.get_cache_stats()
print(f"Hit ratio: {stats['hit_ratio']:.1%}")
print(f"Entries: {stats['total_entries']}, Memory: {stats['memory_bytes'] / 1024:.0f}KB")

# Invalidate by pattern
agent.invalidate_cache("/api/v1/products/*")

# Full cache clear
agent.clear_cache()
```

### Plugin System

```python
from agents.api_gateway.agent import Plugin, RequestContext, ResponseContext

class LoggingPlugin(Plugin):
    def on_request(self, request):
        print(f"[REQ] {request.method} {request.path}")
        return request

    def on_response(self, request, response):
        print(f"[RES] {request.path} → {response.status_code} ({response.latency_ms}ms)")
        return response

    def on_error(self, request, error):
        print(f"[ERR] {request.path} → {error}")
        return ResponseContext(status_code=500, body={"error": str(error)})

agent.register_plugin(LoggingPlugin())
```

### API Keys

```python
# Register a key
key = agent.register_api_key(
    owner="frontend-app",
    scopes=["read", "write"],
    rate_limit_override=5000,
    expires_in_days=90
)
print(f"API Key: {key.key_value}")

# Pass in X-API-Key header
result = agent.simulate_request("GET", "/api/v1/users", headers={"X-API-Key": key.key_value})

# Revoke
agent._auth_middleware.revoke_api_key(key.key_value)
```

### Analytics & Monitoring

```python
# Period analytics
analytics = agent.get_analytics(period="1h")
print(f"Requests: {analytics['requests_total']}")
print(f"Error rate: {analytics['error_rate']:.1%}")
print(f"p99 latency: {analytics['latency_p99']}ms")

# Health check
health = agent.health_check()
for component, status in health.items():
    print(f"  {component}: {status}")

# Export config for backup
state = agent.export_config()
agent.import_config(state)  # Restore elsewhere
```

---

## API Reference

### Configuration

```python
config = GatewayConfig(
    name="production-gateway",
    environment=GatewayEnvironment.PRODUCTION,
    host="0.0.0.0",
    port=8080,
    endpoint_configs=[...],
    rate_limit_config=RateLimitConfig(...),
    auth_config=AuthConfig(...),
    circuit_breaker_config=CircuitBreakerConfig(...),
    cache_config=CacheConfig(...),
    logging_config=LoggingConfig(...),
    tls_config=TLSConfig(...),
)
agent.configure_gateway(config)
```

### Endpoint Registration

```python
endpoint = EndpointConfig(
    path="/api/v1/users",
    methods=[HTTPMethod.GET, HTTPMethod.POST],
    upstream_url="http://user-service:8080",
    auth_type=AuthType.JWT,
    rate_limit=100,
    caching_enabled=True,
    cors_enabled=True,
)
agent.register_endpoint(endpoint)
```

### Upstream Management

```python
agent.create_upstream_pool("user-pool", LoadBalancingStrategy.LEAST_CONNECTIONS)
agent.add_upstream_server("/api/v1/users", UpstreamServer(url="http://svc-1:8080", weight=100))
agent.update_upstream_health("http://svc-1:8080", is_healthy=False)
```

### Rate Limiting

```python
agent.configure_rate_limit("/api/v1/expensive", 50, algorithm=RateLimitAlgorithm.TOKEN_BUCKET)
```

### Caching

```python
agent.get_cache_stats()
agent.invalidate_cache("/api/v1/products*")
agent.clear_cache()
```

### Request Simulation

```python
result = agent.simulate_request(
    method="GET",
    path="/api/v1/users",
    headers={"authorization": "Bearer <jwt>"},
    client_ip="10.0.0.1",
)
# Returns: {request_id, status, body, latency_ms, cached, upstream, auth_type, rate_limit_remaining}
```

### Analytics & Reporting

```python
agent.get_analytics()              # per-period report
agent.get_status()                 # gateway + cache + analytics summary
agent.get_statistics()             # detailed breakdown including upstreams, circuit breakers
agent.health_check()               # composite health
agent.export_config()              # JSON-serializable state
agent.import_config(config_dict)   # hydrate gateway from exported state
```

### Plugins

```python
class LoggingPlugin(Plugin):
    def on_request(self, request): logger.info(f"{request.request_id} {request.method} {request.path}"); return request
    def on_response(self, request, response): return response
    def on_error(self, request, error): return ResponseContext(status_code=500, body={"error": str(error)})

agent.register_plugin(LoggingPlugin())
```

### API Keys

```python
key = agent.register_api_key(owner="alice", scopes=["read", "write"])
# Pass key.key_value in X-API-Key header
agent._auth_middleware.revoke_api_key(key.key_value)
```

---

## Examples

### Multi-Version API Gateway

```python
config = GatewayConfig(
    name="versioned-gateway",
    endpoint_configs=[
        EndpointConfig(
            path="/api/v1/users/*",
            upstream_url="http://user-v1:8080",
            auth_type=AuthType.JWT,
        ),
        EndpointConfig(
            path="/api/v2/users/*",
            upstream_url="http://user-v2:8080",
            auth_type=AuthType.JWT,
        ),
    ],
)
```

### OAuth2-Protected Internal API

```python
auth_config = AuthConfig(
    oauth2_client_id="gateway-service",
    oauth2_client_secret="service-secret",
    oauth2_token_url="https://auth.internal/oauth/token",
)
config = GatewayConfig(auth_config=auth_config)
```

### Circuit Breaker Protection

```python
# Aggressive circuit breaker for critical payment service
config = GatewayConfig(
    circuit_breaker_config=CircuitBreakerConfig(
        failure_threshold=3,        # Open after 3 failures
        success_threshold=2,        # Close after 2 successes
        timeout_seconds=15,         # Wait 15s before probing
        half_open_max_probes=5,     # Max 5 probes in half-open
    ),
)
```

---

## Configuration

### GatewayConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | — | Gateway identifier |
| `environment` | GatewayEnvironment | PRODUCTION | Target environment |
| `host` | str | "0.0.0.0" | Bind address |
| `port` | int | 8080 | Bind port |
| `endpoint_configs` | List[EndpointConfig] | [] | Initial endpoints |
| `rate_limit_config` | RateLimitConfig | defaults | Global rate limits |
| `auth_config` | AuthConfig | defaults | Auth configuration |
| `circuit_breaker_config` | CircuitBreakerConfig | defaults | CB settings |
| `cache_config` | CacheConfig | defaults | Cache settings |
| `tls_config` | TLSConfig | defaults | TLS settings |

### RateLimitConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_requests_per_window` | int | 1000 | Default limit per window |
| `default_window_seconds` | int | 60 | Window duration |
| `ip_whitelist` | List[str] | [] | CIDR prefixes to exempt |
| `ip_blacklist` | List[str] | [] | CIDR prefixes to block |

### CacheConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | bool | True | Enable caching |
| `max_size_bytes` | int | 104857600 | Max cache memory (100MB) |
| `default_ttl_seconds` | int | 300 | Default TTL |
| `stale_while_revalidate` | bool | False | Serve stale while refreshing |
| `eviction_policy` | str | "lru" | Eviction strategy |

---

## Data Models

| Class | Description |
|-------|-------------|
| `EndpointConfig` | Per-endpoint routing and policy |
| `UpstreamServer` | Backend instance with health state |
| `RateLimitConfig` | Global and per-resource rate limits |
| `AuthConfig` | JWT, OAuth2, API key config |
| `CircuitBreakerConfig` | LLB failure thresholds and timeout |
| `CacheConfig` | In-memory cache tuning (TTL, max size, eviction) |
| `LoggingConfig` | Structured log format, rotation, sensitive headers |
| `TLSConfig` | TLS termination, cipher suites, mTLS |
| `GatewayConfig` | Top-level gateway configuration |
| `RequestContext` | Runtime request envelope with auth and upstream data |
| `ResponseContext` | Runtime response with cache and latency data |
| `APIKey` | API key with owner, scopes, expiry, and IP restrictions |
| `JWTPayload` | Decoded JWT claims |
| `Plugin` | Abstract base class with hook methods |

---

## Security & Privacy

- No credentials logged; API keys stored in-memory only
- JWT validated with signature, expiration, issuer, audience checks
- Sensitive headers (Authorization, X-API-Key, Cookie) excluded from logs
- CORS origins restricted by configurable allow-list
- Request body size enforced per endpoint
- Security headers auto-injected (HSTS, X-Frame-Options, X-Content-Type-Options, CSP)
- TLS 1.2+ minimum with configurable cipher suites
- IP whitelist/blacklist with CIDR prefix matching

---

## Performance

| Operation | Target |
|-----------|--------|
| Route match | O(n) linear scan (small endpoint count) |
| Token bucket check | O(1) with lock |
| Sliding window | O(k) where k = valid entries per identifier |
| Circuit breaker check | O(1) with lock |
| Cache hit | O(1) dict lookup |
| Cache eviction | O(m) where m = keys sorted by age |
| Plugin chain | O(p) where p = registered plugins |

---

## State Management

```python
state = agent.export_config()
agent.import_config(state)   # Restore gateway state
```

Cache is not persisted across restarts; rebuild from scratch after import.

---

## Constraints

- Single-process, single-node gateway
- Basic Auth demo credentials are illustrative; use LDAP/OAuth2 in production
- TLS termination is configured but not performed; use NGINX, Envoy, or cloud load balancer
- Consistent hash is a deterministic approximation; true consistent hashing requires a ring implementation
- Plugin execution is sequential; parallel plugin execution requires custom threading

---

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| 429 on all requests | Rate limit too tight or IP blacklisted | Increase `default_requests_per_window` or inspect blacklist |
| 503 on all requests | No healthy upstreams | Check upstream health paths; verify services |
| 401 on valid requests | JWT secret/expiry mismatch | Verify secret, exp, iss, aud |
| Cache stale | TTL too long | Reduce `cache_ttl_seconds` or use `invalidate_cache()` |
| CB trips frequently | Upstream unstable | Increase `failure_threshold`, reduce `timeout_seconds` |
| CORS preflight fails | Origin not in allowlist | Add origin to `cors_origins` |
| Slow response | Lock contention or GC | Review limiter state keys; consider distributed cache |
| 502 from upstream | Service down | Check upstream health; verify service is running |
| Memory growing | Cache not evicting | Set `max_size_bytes`; check eviction policy |

---

## Advanced Usage

### Multi-Region Gateway

```python
# Region A
config_a = GatewayConfig(
    name="gateway-us-east",
    environment=GatewayEnvironment.PRODUCTION,
    host="0.0.0.0",
    port=8080,
    endpoint_configs=[
        EndpointConfig(
            path="/api/*",
            upstream_url="http://us-east-backend:8080",
            auth_type=AuthType.JWT,
        ),
    ],
)

# Region B
config_b = GatewayConfig(
    name="gateway-eu-west",
    environment=GatewayEnvironment.PRODUCTION,
    host="0.0.0.0",
    port=8081,
    endpoint_configs=[
        EndpointConfig(
            path="/api/*",
            upstream_url="http://eu-west-backend:8080",
            auth_type=AuthType.JWT,
        ),
    ],
)
```

### Canary Deployment via Routing

```python
# 90% traffic to v1, 10% to v2
config = GatewayConfig(
    endpoint_configs=[
        EndpointConfig(
            path="/api/v1/*",
            upstream_url="http://user-service-v1:8080",
            auth_type=AuthType.JWT,
            rate_limit=1000,
        ),
        EndpointConfig(
            path="/api/v2/*",
            upstream_url="http://user-service-v2:8080",
            auth_type=AuthType.JWT,
            rate_limit=100,
        ),
    ],
)
```

### Webhook Validation

```python
# Validate incoming webhook signatures
endpoint = EndpointConfig(
    path="/webhooks/stripe",
    methods=[HTTPMethod.POST],
    upstream_url="http://payment-processor:8080",
    auth_type=AuthType.WEBHOOK_SIGNATURE,
    webhook_secret="whsec_xxx",
    webhook_header="Stripe-Signature",
)
```

### Custom Error Responses

```python
class CustomErrorPlugin(Plugin):
    def on_error(self, request, error):
        return ResponseContext(
            status_code=503,
            body={
                "error": {
                    "code": "SERVICE_UNAVAILABLE",
                    "message": "The service is temporarily unavailable",
                    "request_id": request.request_id,
                    "retry_after": 30,
                }
            },
            headers={"Retry-After": "30"},
        )

agent.register_plugin(CustomErrorPlugin())
```

### Request Logging for Audit

```python
class AuditPlugin(Plugin):
    def on_request(self, request):
        audit_log.info(json.dumps({
            "request_id": request.request_id,
            "method": request.method,
            "path": request.path,
            "client_ip": request.client_ip,
            "auth_type": request.auth_type,
            "timestamp": datetime.utcnow().isoformat(),
        }))
        return request

    def on_response(self, request, response):
        audit_log.info(json.dumps({
            "request_id": request.request_id,
            "status": response.status_code,
            "latency_ms": response.latency_ms,
            "upstream": response.upstream,
        }))
        return response
```

### Rate Limit Override per Client

```python
# Different rate limits per API key tier
key_free = agent.register_api_key(owner="free-user", scopes=["read"], rate_limit_override=100)
key_pro = agent.register_api_key(owner="pro-user", scopes=["read", "write"], rate_limit_override=5000)
key_enterprise = agent.register_api_key(owner="enterprise", scopes=["read", "write", "admin"], rate_limit_override=50000)
```

### Circuit Breaker Dashboard

```python
stats = agent.get_statistics()
circuit_breakers = stats.get("circuit_breakers", {})
for upstream, cb in circuit_breakers.items():
    print(f"{upstream}: {cb['state']} (failures: {cb['failure_count']}/{cb['failure_threshold']})")
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `RATE_LIMITED` | 429 | Rate limit exceeded |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Authenticated but not authorized |
| `NOT_FOUND` | 404 | No matching route |
| `METHOD_NOT_ALLOWED` | 405 | HTTP method not in allowed list |
| `REQUEST_TOO_LARGE` | 413 | Request body exceeds size limit |
| `UPSTREAM_UNAVAILABLE` | 502 | All upstreams unhealthy |
| `CIRCUIT_OPEN` | 503 | Circuit breaker is OPEN |
| `TIMEOUT` | 504 | Upstream did not respond in time |
| `INTERNAL_ERROR` | 500 | Gateway internal error |

---

## Integration Patterns

### With Prometheus/Grafana

```python
# Export metrics for Prometheus scraping
analytics = agent.get_analytics(period="1m")
# Map to Prometheus metrics:
#   gateway_requests_total{method, path, status}
#   gateway_request_duration_seconds{method, path}
#   gateway_rate_limit_hits_total{path}
#   gateway_circuit_breaker_trips_total{upstream}
#   gateway_cache_hits_total / gateway_cache_misses_total
```

### With OpenTelemetry

```python
# Inject trace context into upstream requests
class TracingPlugin(Plugin):
    def on_request(self, request):
        trace_id = request.headers.get("traceparent", str(uuid.uuid4()))
        request.headers["X-Trace-ID"] = trace_id
        request.metadata["trace_id"] = trace_id
        return request

    def on_response(self, request, response):
        trace_id = request.metadata.get("trace_id", "unknown")
        span_end(trace_id, response.status_code)
        return response
```

### With Redis (Distributed Rate Limiting)

```python
# For multi-node deployments, share rate limit state via Redis
config = GatewayConfig(
    rate_limit_config=RateLimitConfig(
        backend="redis",
        redis_url="redis://redis-cluster:6379",
        redis_key_prefix="gw:ratelimit:",
    ),
)
```

### With NGINX (TLS Termination)

```nginx
# NGINX config for TLS termination in front of gateway
server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/ssl/certs/api.example.com.pem;
    ssl_certificate_key /etc/ssl/private/api.example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
    }
}
```

---

## Metrics Reference

| Metric | Type | Description |
|--------|------|-------------|
| `gateway_requests_total` | Counter | Total requests processed |
| `gateway_request_duration_seconds` | Histogram | Request latency |
| `gateway_errors_total` | Counter | Total errors by status code |
| `gateway_rate_limit_hits_total` | Counter | Rate limit rejections |
| `gateway_circuit_breaker_trips_total` | Counter | Circuit breaker state changes |
| `gateway_cache_hits_total` | Counter | Cache hits |
| `gateway_cache_misses_total` | Counter | Cache misses |
| `gateway_auth_failures_total` | Counter | Authentication failures |
| `gateway_upstream_requests_total` | Counter | Requests to each upstream |
| `gateway_upstream_errors_total` | Counter | Upstream errors |

---

## Files

- `agent.py` — Main implementation (~1100 lines)
- `ARCHITECTURE.md` — Deep system design and data flow
- `GROK.md` — Agent identity, capabilities, and usage patterns
- `README.md` — This file

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*API Gateway Agent v2.0 — Part of the Awesome Grok Skills collection.*
