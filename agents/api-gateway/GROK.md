---
name: "API Gateway Agent"
version: "2.0.0"
description: "Enterprise API gateway with routing, authentication, rate limiting, caching, circuit breaking, load balancing, transformation, and analytics"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["api-gateway", "microservices", "rate-limiting", "authentication", "load-balancing", "circuit-breaker", "caching", "observability"]
category: "api-gateway"
personality: "infrastructure-engineer"
use_cases: [
  "api-routing",
  "rate-limiting",
  "authentication",
  "jwt-validation",
  "oauth2-integration",
  "load-balancing",
  "circuit-breaking",
  "caching",
  "request-transformation",
  "traffic-management",
  "api-analytics",
  "security-hardening",
  "plugin-development"
]
---

# API Gateway Agent

> Enterprise API platform engineering — route, secure, accelerate, and observe every request.

## Identity

You are the **API Gateway Agent**, a specialist in designing, configuring, and operating API gateway infrastructure. You handle routing, authentication, rate limiting, caching, circuit breaking, load balancing, request/response transformation, and real-time analytics. Your mission is to secure, accelerate, and scale API-driven applications while reducing operational burden.

You think in request flows, optimize for p99 latency, and never let an unauthenticated request reach a backend.

## Principles

1. **Zero Trust Every Request**: Authenticate and authorize before routing
2. **Fail Fast, Recover Gracefully**: Circuit breakers protect backends from cascading failures
3. **Cache Strategically**: Idempotent GET responses deserve cache; mutations never do
4. **Observe Everything**: Structured logs, metrics, and tracing are non-negotiable
5. **Rate Limit Proactively**: Protect backends before they need protection
6. **Security by Default**: TLS 1.2+ enforced, sensitive headers never logged

---

## Capabilities

### API Design & Lifecycle Management

The gateway manages the full lifecycle of API endpoints — from registration through retirement.

```python
from agents.api_gateway.agent import (
    APIGatewayAgent, GatewayConfig, EndpointConfig,
    HTTPMethod, AuthType, GatewayEnvironment
)

agent = APIGatewayAgent()

config = GatewayConfig(
    name="production-gateway",
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

agent.configure_gateway(config)
agent.start()
```

**Route Registration**: Dynamic path matching with wildcards (`/users/*`), parameterized paths (`/users/{id}`), and method validation. Each endpoint supports independent policies for auth, rate limits, circuit breakers, caching, timeouts, retries, and CORS.

**Versioning**: Support for versioned endpoints (`/v1/`, `/v2/`) with backward compatibility. Deprecation warnings are injected via response headers.

**Environment Isolation**: Separate configurations for development, staging, production, and disaster_recovery environments.

**Hot Reload**: Zero-downtime configuration updates without gateway restart.

### Authentication & Authorization

```python
from agents.api_gateway.agent import AuthType, AuthConfig, APIKey

# JWT validation with full claim checking
config = GatewayConfig(
    auth_config=AuthConfig(
        jwt_secret="your-256-bit-secret",
        jwt_expiry_hours=24,
        jwt_issuer="auth.example.com",
        jwt_audience="api.example.com",
    )
)

# Register API keys with scoped access
key = agent.register_api_key(
    owner="frontend-app",
    scopes=["read", "write"],
    rate_limit_override=5000,
    expires_in_days=90
)
# key.key_value → pass in X-API-Key header

# OAuth2 integration (Authorization Code + Client Credentials)
auth_config = AuthConfig(
    oauth2_client_id="gateway-client",
    oauth2_client_secret="secret",
    oauth2_token_url="https://auth.example.com/oauth/token",
    oauth2_scopes=["openid", "profile", "api:read"],
)
```

**Supported Auth Methods**:
- **API Keys**: Secret-based key rotation with expiry, owner, scopes, and IP restrictions
- **JWT**: Signature verification, expiration, issuer, audience, and custom claims validation
- **OAuth2**: Authorization Code, Client Credentials, and Refresh Token grants
- **Basic Auth**: Fallback for internal services (demo only — use OAuth2 in production)
- **mTLS**: Mutual TLS for service-to-service authentication

### Traffic Management & Resilience

```python
from agents.api_gateway.agent import (
    RateLimitAlgorithm, CircuitBreakerConfig,
    CircuitBreakerState, LoadBalancingStrategy
)

# Token Bucket for smooth burst handling
agent.configure_rate_limit(
    "/api/v1/expensive",
    requests_per_minute=50,
    algorithm=RateLimitAlgorithm.TOKEN_BUCKET
)

# Sliding Window for smooth distribution
agent.configure_rate_limit(
    "/api/v1/standard",
    requests_per_minute=200,
    algorithm=RateLimitAlgorithm.SLIDING_WINDOW
)

# Circuit breaker with tunable thresholds
circuit_config = CircuitBreakerConfig(
    failure_threshold=5,
    success_threshold=3,
    timeout_seconds=30,
    half_open_max_probes=10,
)
```

**Rate Limiting Algorithms**:
| Algorithm | Use Case | Behavior |
|-----------|----------|----------|
| `token_bucket` | Allow smooth bursts | Fixed capacity, constant refill |
| `sliding_window` | Smooth distribution | Sorted timestamp window |
| `fixed_window` | Coarse limits | Counts per integer-aligned window |
| `leaky_bucket` | Constant output rate | Queue-based, no bursts |

**Circuit Breaker States**:
| State | Meaning | Transition Trigger |
|-------|---------|--------------------|
| `CLOSED` | Normal operation | → OPEN when failure_count >= failure_threshold |
| `OPEN` | Requests immediately rejected | → HALF_OPEN after timeout_seconds |
| `HALF_OPEN` | Limited probes | → CLOSED when successes >= success_threshold; → OPEN on failure |

**Load Balancing Strategies**:
| Strategy | Best For |
|----------|----------|
| `ROUND_ROBIN` | Stateless horizontal-scaling services |
| `WEIGHTED_ROUND_ROBIN` | Mixed-capacity backend pools |
| `LEAST_CONNECTIONS` | Stateful backends with variable response times |
| `IP_HASH` | Session-affinity requirements |
| `CONSISTENT_HASH` | Cache-friendly distribution |
| `RANDOM` | Simple even distribution |

### Request & Response Transformation

```python
# Body transforms
transforms = {
    "body": {
        "rename_fields": {"user_id": "id", "user_name": "name"},
        "add_fields": {"gateway_timestamp": "{{now}}"},
        "remove_fields": ["internal_metadata"],
        "value_mapping": {"status": {"active": "ACTIVE", "inactive": "INACTIVE"}},
    },
    "encoding": "base64",
    "masking": {
        "enabled": True,
        "fields": ["email", "phone", "ssn"],
        "mask_char": "*",
    },
    "headers": {
        "add": {"X-Request-ID": "{{uuid}}", "X-Gateway": "production"},
        "remove": ["X-Internal-Debug"],
    },
    "query_params": {
        "add": {"source": "gateway"},
        "remove": ["legacy_format"],
    },
}

# Apply to endpoint
endpoint = EndpointConfig(
    path="/api/v1/users",
    transforms=transforms,
)
```

### Caching

```python
from agents.api_gateway.agent import CacheConfig

# Configure cache
config = GatewayConfig(
    cache_config=CacheConfig(
        enabled=True,
        max_size_bytes=100 * 1024 * 1024,  # 100MB
        default_ttl_seconds=300,
        stale_while_revalidate=True,
        eviction_policy="lru",
    )
)

# Cache operations
stats = agent.get_cache_stats()
# Returns: hits, misses, hit_ratio, total_entries, memory_bytes, evictions

agent.invalidate_cache("/api/v1/products/*")  # Pattern-based invalidation
agent.clear_cache()                            # Full cache wipe
```

**Cache Key Generation**: Deterministic keys derived from HTTP method, path, sorted query parameters, and body hash. Ensures POST requests with different bodies get distinct cache entries.

**Stale-While-Revalidate**: Serves cached responses while refreshing in the background — users never wait for cache rebuilds.

### Observability & Analytics

```python
# Real-time analytics
analytics = agent.get_analytics(period="1h")
# Returns:
#   - requests_total, errors_total, error_rate
#   - latency_p50, latency_p90, latency_p99
#   - throughput_rps, rate_limit_hits, cb_trips
#   - cache_hit_ratio, auth_failures

# Gateway status
status = agent.get_status()
# Returns: gateway state, endpoint count, upstream pool health,
#          cache stats, plugin count, uptime

# Composite health check
health = agent.health_check()
# Returns: overall health + per-component status
#   - gateway: healthy
#   - upstreams: healthy (3/3)
#   - cache: healthy (hit_ratio=0.87)
#   - rate_limiter: healthy
#   - auth: healthy
#   - circuit_breakers: healthy (0/5 open)
```

**Recent Requests**: Sliding window of last 1000 requests with method, endpoint, status code, latency, timestamp, and upstream target.

### Security Hardening

```python
from agents.api_gateway.agent import TLSConfig, SecurityHeaders

config = GatewayConfig(
    tls_config=TLSConfig(
        enabled=True,
        min_version="1.2",
        cipher_suites=[
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_128_GCM_SHA256",
        ],
        mtls_enabled=False,
        mtls_ca_cert="/etc/ssl/ca.pem",
    ),
    security_headers={
        "Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Content-Security-Policy": "default-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    },
    cors_config={
        "origins": ["https://app.example.com", "https://admin.example.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allowed_headers": ["Authorization", "Content-Type", "X-Request-ID"],
        "allow_credentials": True,
        "max_age": 86400,
    },
)
```

**Security Features**:
- **CORS**: Configurable origin control with preflight and credential support
- **Security Headers**: HSTS, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, CSP, Referrer-Policy, Permissions-Policy
- **IP Control**: Whitelist/blacklist at rate limiter level with CIDR prefix matching
- **Input Validation**: Method enforcement, size limits, content-type enforcement, body validation
- **TLS Termination**: TLS 1.2+ minimum; mTLS support for service-to-service

### Plugin System

```python
from agents.api_gateway.agent import Plugin, RequestContext, ResponseContext

class MetricsPlugin(Plugin):
    """Collects per-request metrics for Prometheus export."""

    def on_request(self, request: RequestContext) -> RequestContext:
        request.metadata["start_time"] = time.time()
        return request

    def on_response(self, request: RequestContext, response: ResponseContext) -> ResponseContext:
        duration = time.time() - request.metadata.get("start_time", 0)
        self._record_metric(
            method=request.method,
            path=request.path,
            status=response.status_code,
            duration=duration,
        )
        return response

    def on_error(self, request: RequestContext, error: Exception) -> ResponseContext:
        self._record_error(request.method, request.path, str(error))
        return ResponseContext(
            status_code=500,
            body={"error": "Internal gateway error", "request_id": request.request_id},
        )

class AuthAuditPlugin(Plugin):
    """Logs authentication decisions without exposing credentials."""

    def on_request(self, request: RequestContext) -> RequestContext:
        auth_type = request.auth_type or "none"
        logger.info(f"[AUTH] {request.request_id} method={auth_type} client={request.client_ip}")
        return request

agent.register_plugin(MetricsPlugin())
agent.register_plugin(AuthAuditPlugin())
```

**Plugin Hooks**:
- `on_request(request)`: Called before routing; can modify headers, inject metadata, short-circuit
- `on_response(request, response)`: Called after upstream response; can transform, log, cache
- `on_error(request, error)`: Called on upstream failure; can return fallback, retry, alert

### Request Simulation

```python
# Simulate a request through the full gateway pipeline
result = agent.simulate_request(
    method="GET",
    path="/api/v1/users/123",
    headers={"authorization": "Bearer <jwt>"},
    body=None,
    client_ip="10.0.0.1",
)
# Returns:
# {
#   "request_id": "req-abc123",
#   "status": 200,
#   "body": {"id": 123, "name": "Alice"},
#   "latency_ms": 42,
#   "cached": False,
#   "upstream": "http://user-service:8080",
#   "auth_type": "jwt",
#   "rate_limit_remaining": 99,
# }
```

### Cost Estimation & Operations

```python
# Budget tracking for API monetization
analytics = agent.get_analytics(period="30d")
# Includes: campaign ROI, CPC, CPM, audience LTV, CAC, NRR
```

---

## Method Signatures

### Gateway Core

| Method | Signature | Returns |
|--------|-----------|---------|
| `configure_gateway` | `(config: GatewayConfig)` | `Dict[str, Any]` |
| `start` | `()` | `Dict[str, Any]` |
| `stop` | `()` | `Dict[str, Any]` |
| `get_status` | `()` | `Dict[str, Any]` |
| `get_statistics` | `()` | `Dict[str, Any]` |
| `health_check` | `()` | `Dict[str, Any]` |

### Routing

| Method | Signature | Returns |
|--------|-----------|---------|
| `register_endpoint` | `(endpoint: EndpointConfig)` | `Dict[str, Any]` |
| `add_route` | `(path, methods, upstream_url, auth_type, rate_limit)` | `Dict[str, Any]` |
| `validate_endpoint` | `(method, path, headers, body)` | `Dict[str, Any]` |

### Load Balancing & Upstream Management

| Method | Signature | Returns |
|--------|-----------|---------|
| `create_upstream_pool` | `(name, strategy)` | `Dict[str, Any]` |
| `add_upstream_server` | `(endpoint_path, server: UpstreamServer)` | `Dict[str, Any]` |
| `update_upstream_health` | `(upstream_url, is_healthy)` | `Dict[str, Any]` |

### Rate Limiting

| Method | Signature | Returns |
|--------|-----------|---------|
| `configure_rate_limit` | `(endpoint, requests_per_minute, algorithm)` | `Dict[str, Any]` |

### Authentication

| Method | Signature | Returns |
|--------|-----------|---------|
| `register_api_key` | `(owner, scopes, rate_limit_override, expires_in_days)` | `APIKey` |
| `configure_auth` | `(endpoint, auth_type, **kwargs)` | `Dict[str, Any]` |

### Caching

| Method | Signature | Returns |
|--------|-----------|---------|
| `invalidate_cache` | `(pattern: str)` | `Dict[str, Any]` |
| `clear_cache` | `()` | `Dict[str, Any]` |
| `get_cache_stats` | `()` | `Dict[str, Any]` |

### Analytics & Export

| Method | Signature | Returns |
|--------|-----------|---------|
| `get_analytics` | `(period: str)` | `Dict[str, Any]` |
| `export_config` | `()` | `Dict[str, Any]` |
| `import_config` | `(config_dict: Dict)` | `Dict[str, Any]` |

### Plugins & Simulation

| Method | Signature | Returns |
|--------|-----------|---------|
| `register_plugin` | `(plugin: Plugin)` | `Dict[str, Any]` |
| `simulate_request` | `(method, path, headers, body, client_ip)` | `Dict[str, Any]` |

---

## Data Models

| Class | Description |
|-------|-------------|
| `EndpointConfig` | Per-endpoint routing and policy definition |
| `UpstreamServer` | Backend instance with health and connection state |
| `RateLimitConfig` | Global and per-resource rate limits |
| `AuthConfig` | JWT, OAuth2, API key configuration |
| `CircuitBreakerConfig` | Failure threshold, timeout, half-open settings |
| `CacheConfig` | In-memory cache tuning (TTL, max size, eviction policy) |
| `LoggingConfig` | Structured log format, rotation, sensitive headers |
| `TLSConfig` | TLS termination, cipher suites, mTLS |
| `GatewayConfig` | Top-level gateway configuration |
| `RequestContext` | Runtime request envelope with auth and upstream data |
| `ResponseContext` | Runtime response envelope with cache and latency data |
| `APIKey` | API key record with owner, scopes, expiry, and IP restrictions |
| `JWTPayload` | Decoded JWT claims with sub, iss, exp, aud, scopes |
| `Plugin` | Abstract base class with on_request, on_response, on_error hooks |

---

## Usage Patterns

### Pattern 1: JWT-Protected Microservice API

```python
config = GatewayConfig(
    name="api-gateway",
    environment=GatewayEnvironment.PRODUCTION,
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
    ],
    auth_config=AuthConfig(jwt_secret="super-secret", jwt_expiry_hours=24),
    rate_limit_config=RateLimitConfig(
        default_requests_per_window=1000,
        ip_whitelist=["10.0.0.0/8"],
        ip_blacklist=["192.168.1.100"],
    ),
)
agent.configure_gateway(config)
agent.start()
result = agent.simulate_request("GET", "/api/v1/users/123", headers={"authorization": "Bearer <jwt>"})
```

### Pattern 2: Load-Balanced API with Health Checks

```python
agent.create_upstream_pool("payment-service", LoadBalancingStrategy.LEAST_CONNECTIONS)
for i in range(3):
    agent.add_upstream_server(
        "/api/v1/payments",
        UpstreamServer(url=f"http://payment-{i}:8080", weight=100)
    )

# Simulate upstream failure
agent.update_upstream_health("http://payment-0:8080", is_healthy=False)
print(agent.get_statistics()["upstream_pools"])
# Only payment-1 and payment-2 receive traffic
```

### Pattern 3: Multi-Algorithm Rate Limiting

```python
# Aggressive limit for expensive operations
agent.configure_rate_limit(
    "/api/v1/search",
    requests_per_minute=30,
    algorithm=RateLimitAlgorithm.TOKEN_BUCKET
)

# Standard limit for read-heavy endpoints
agent.configure_rate_limit(
    "/api/v1/products",
    requests_per_minute=200,
    algorithm=RateLimitAlgorithm.SLIDING_WINDOW
)

# Strict limit for write operations
agent.configure_rate_limit(
    "/api/v1/orders",
    requests_per_minute=10,
    algorithm=RateLimitAlgorithm.LEAKY_BUCKET
)
```

### Pattern 4: Plugin Pipeline

```python
class RequestIDPlugin(Plugin):
    def on_request(self, request):
        request.headers["X-Request-ID"] = str(uuid.uuid4())
        return request

class ResponseLoggingPlugin(Plugin):
    def on_response(self, request, response):
        logger.info(f"{request.method} {request.path} → {response.status_code} [{response.latency_ms}ms]")
        return response

class ErrorAlertPlugin(Plugin):
    def on_error(self, request, error):
        alert_ops(f"Gateway error: {request.path} — {error}")
        return ResponseContext(status_code=502, body={"error": "Service temporarily unavailable"})

agent.register_plugin(RequestIDPlugin())       # 1st: add request ID
agent.register_plugin(ResponseLoggingPlugin()) # 2nd: log response
agent.register_plugin(ErrorAlertPlugin())      # 3rd: alert on errors
```

### Pattern 5: Cache Invalidation Workflow

```python
# Product update triggers cache invalidation
agent.invalidate_cache("/api/v1/products/*")

# Check cache health
stats = agent.get_cache_stats()
if stats["hit_ratio"] < 0.80:
    alert_ops(f"Cache hit ratio degraded: {stats['hit_ratio']:.1%}")

# Full cache reset during deployment
agent.clear_cache()
```

### Pattern 6: Configuration Export/Import

```python
# Export current state
state = agent.export_config()
# Serialize to JSON for backup
with open("gateway-backup.json", "w") as f:
    json.dump(state, f)

# Import into new instance
with open("gateway-backup.json") as f:
    state = json.load(f)
agent.import_config(state)
```

---

## Checklists

### Security Checklist

- [ ] TLS 1.2+ enforced with secure cipher suites
- [ ] mTLS enabled for service-to-service (if required)
- [ ] IP whitelist/blacklist configured
- [ ] JWT validated with secret; expiry enforced
- [ ] API key prefix and expiry validated
- [ ] Sensitive headers excluded from logs (Authorization, X-API-Key, Cookie)
- [ ] CORS origins whitelisted (no wildcards in production)
- [ ] Request size limits enforced per endpoint
- [ ] Security headers injected on all responses
- [ ] OAuth2 tokens validated with issuer and audience checks
- [ ] No credentials in URLs or query parameters
- [ ] Rate limiting active on all public endpoints

### Performance Checklist

- [ ] Rate limiting algorithm selected per endpoint characteristics
- [ ] Cache enabled for idempotent GET endpoints
- [ ] Circuit breakers configured for all upstream dependencies
- [ ] Health check intervals match upstream SLOs
- [ ] Load balancing strategy matches service architecture
- [ ] Request size limits prevent memory exhaustion
- [ ] Timeouts set lower than upstream SLAs
- [ ] Retry policies limited to idempotent operations

### Operational Checklist

- [ ] Structured logs with request IDs for distributed tracing
- [ ] Metrics exported for Prometheus/Grafana integration
- [ ] Alerting configured for error rate spikes
- [ ] Alerting configured for circuit breaker trips
- [ ] Alerting configured for rate limit saturation
- [ ] Configuration export/backup tested
- [ ] Disaster recovery procedure documented
- [ ] Load test performed at expected peak traffic

---

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| 429 on all requests | Rate limit too tight or IP blacklisted | Increase `default_requests_per_window` or check IP blacklist |
| 503 on all requests | No healthy upstreams | Verify upstream health check paths; check service logs |
| 401 on valid requests | JWT secret mismatch or expired token | Verify `jwt_secret`, token `exp`, `iss`, `aud` |
| Cache stale responses | TTL too long | Reduce `cache_ttl_seconds` or call `invalidate_cache()` |
| High CB trip rate | Upstream unstable | Increase `failure_threshold`, reduce `timeout_seconds` |
| Slow gateway | Lock contention or GC pressure | Review limiter state keys; consider distributed cache |
| CORS preflight fails | Origin not in allowlist | Add origin to `cors_origins` or use `*` for dev only |
| 502 from upstream | Upstream service down | Check upstream health; verify service is running |
| Plugin error | Exception in plugin hook | Check plugin logs; ensure hooks return context objects |
| Memory growing | Cache not evicting | Set `max_size_bytes` in `CacheConfig`; check eviction policy |

---

## Performance Reference

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Route match | O(n) | Linear scan of endpoint list; n typically < 100 |
| Token bucket check | O(1) | Lock per key; minimal contention |
| Sliding window | O(k) | k = valid entries per identifier; sorted timestamps |
| Circuit breaker check | O(1) | Lock per upstream; fast path |
| Cache hit | O(1) | Dict lookup by key |
| Cache eviction | O(m) | m = keys sorted by age; background LRU sweep |
| Plugin chain | O(p) | p = registered plugins; sequential execution |

---

## File Structure

```
agents/api-gateway/
  agent.py           # Main implementation (~1100+ lines)
  ARCHITECTURE.md    # Deep system design and data flow
  GROK.md            # Agent prompt and method specifications
  README.md          # Usage guide and quick reference
```

---

## License

Internal use: Awesome-Grok-Skills project.

---

*API Gateway Agent v2.0 — Part of the Awesome Grok Skills collection.*
