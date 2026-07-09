# API Gateway Agent - System Architecture

## 1. Overview

The API Gateway Agent is an enterprise-grade API management framework implementing a full-featured gateway with dynamic routing, rate limiting, authentication, circuit breaking, request/response transformation, caching, analytics, and plugin extensibility.

## 2. Design Principles

- **Zero-Trust Security**: Every request authenticated and authorized.
- **Resilience by Default**: Circuit breakers, retries, timeouts, and health checks.
- **Observability**: Structured analytics, request tracing, and operational metrics.
- **Extensibility**: Plugin architecture for custom middleware.
- **Performance**: Multi-algorithm rate limiting, in-memory caching, efficient load balancing.
- **Compliance**: CORS, security headers, input sanitization, audit logging.

## 3. System Architecture

```
                     ┌─────────────────────────────┐
                     │    Client / Consumer API     │
                     └──────────────┬──────────────┘
                                    │
                     ┌─────────────────────────────┐
                     │    Security Layer            │
                     │  - TLS/mTLS Termination      │
                     │  - Authentication            │
                     │    (API Key, JWT, OAuth2,    │
                     │     Basic, mTLS)             │
                     │  - IP Whitelist/Blacklist    │
                     │  - CORS Preflight            │
                     └──────────────┬──────────────┘
                                    │
                     ┌─────────────────────────────┐
                     │    Rate Limiting Layer       │
                     │  - Token Bucket              │
                     │  - Sliding Window            │
                     │  - Fixed Window              │
                     │  - Leaky Bucket              │
                     │  - Per-user/Per-endpoint     │
                     └──────────────┬──────────────┘
                                    │
                     ┌─────────────────────────────┐
                     │    Request Pipeline          │
                     │  - Method Validation         │
                     │  - Path Matching             │
                     │  - Request Validation        │
                     │    (size, headers, body)     │
                     │  - Request Transformation    │
                     └──────────────┬──────────────┘
                                    │
                     ┌─────────────────────────────┐
                     │    Load Balancing            │
                     │  - Round Robin               │
                     │  - Weighted Round Robin      │
                     │  - Least Connections         │
                     │  - IP Hash                   │
                     │  - Consistent Hash           │
                     │  - Random                    │
                     │  - Circuit Breaker per       │
                     │    upstream                  │
                     │  - Health Checking           │
                     └──────────────┬──────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
┌───────▼───────┐           ┌───────▼───────┐           ┌───────▼───────┐
│  Cache Layer  │           │   Upstream    │           │  Plugin       │
│  (In-Memory)  │           │   Services    │           │  Manager      │
│  - TTL        │           │  - Service A  │           │  - Auth       │
│  - Pattern    │           │  - Service B  │           │  - Logging    │
│    Invalidate │           │  - Service C  │           │  - Metrics    │
│  - Memory Mgmt│           │  - ...        │           │  - Custom     │
└───────────────┘           └───────────────┘           └───────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                     ┌─────────────────────────────┐
                     │    Response Pipeline         │
                     │  - Response Transformation   │
                     │  - Security Headers Injection│
                     │  - CORS Headers              │
                     │  - Cache Status Headers      │
                     └──────────────┬──────────────┘
                                    │
                     ┌─────────────────────────────┐
                     │    Analytics & Monitoring    │
                     │  - Request Logging           │
                     │  - Latency Percentiles       │
                     │  - Error Rate Tracking       │
                     │  - Rate Limit Hit Counting   │
                     │  - Cache Hit Ratio           │
                     │  - Circuit Breaker Metrics   │
                     └─────────────────────────────┘
```

## 4. Component Deep Dive

### 4.1 Rate Limiting

Four algorithms, all thread-safe due to `threading.Lock`:
- **Token Bucket**: Smooth burst handling with configurable capacity and refill rate.
- **Sliding Window**: Precise window with sorted timestamp array cleanup.
- **Fixed Window**: Simple counting at window boundaries.
- **Leaky Bucket**: Constant output rate regardless of input bursts.

Supports:
- Per-endpoint limits via endpoint path key.
- Per-user limits via identifier key (IP, API key, JWT sub).
- IP whitelist and blacklist (CIDR-prefix checks).

### 4.2 Circuit Breaker

State machine: `CLOSED → OPEN → HALF_OPEN → CLOSED`.

```
                    ┌──────────┐
         failures   │          │  success
        ┌──────────▶│   OPEN   │──────────┐
        │           │          │          │
        │           └──────────┘          │
        │                │                │
        │                │ timeout        │
        │                ▼                │
  ┌─────┴─────┐    ┌──────────┐    ┌─────┴──────┐
  │  CLOSED   │◀───│HALF_OPEN │◀───│  testing   │
  │           │    │          │    │            │
  └───────────┘    └──────────┘    └────────────┘
       │                                │
       └── failures exceed threshold ───┘
```

Uses a sliding monitoring window to count failures in the last `monitoring_window_seconds`.
- **CLOSED**: Requests pass; failures tracked.
- **OPEN**: Requests immediately rejected for `timeout_seconds`.
- **HALF_OPEN**: Limited requests allowed (`half_open_requests`) to test recovery.

Per-upstream-server circuit breakers prevent cascade failures.

### 4.3 Load Balancing

Six strategies:
- **Round Robin**: Simple sequential (with index counter).
- **Weighted Round Robin**: Hash-based weighted selection.
- **Least Connections**: Minimizes queue depth.
- **IP Hash / Consistent Hash**: Session affinity.
- **Random**: Uniform random selection.

Health filtering ensures only `is_healthy=True` servers receive traffic.

### 4.4 Caching

In-memory LRU-inspired cache with:
- Key generation for GET requests.
- TTL-based expiry with stale-while-revalidate support.
- Pattern-based invalidation (regex wildcards).
- Automatic eviction when `current_size_bytes + size_needed > max_size_bytes`.

### 4.5 Request Validation

Validates:
- HTTP method against endpoint configuration.
- Content-Length against `max_request_size_bytes`.
- Content-Type against allowed list.
- CORS origin against allowed list.

### 4.6 Authentication

Supported mechanisms:
- **API Key**: Prefix-matched headers with expiry, scope, and IP restrictions.
- **JWT**: Base64-decoded payload with expiration, issuer, audience checks.
- **Basic**: Base64-decoded username:password.
- **OAuth2**: Bearer token pass-through for integration with external IdPs.

### 4.7 Request/Response Transformation

Built-in transformers:
- JSON ↔ XML conversion.
- Case transformation (uppercase/lowercase).
- Field renaming, addition, removal.
- Value mapping.
- Base64 encoding/decoding.
- Field masking and trimming.

### 4.8 Analytics

Tracks per-request metrics:
- Endpoint, method, status code, latency.
- Cache hits/misses.
- Rate limit hits.
- Circuit breaker trips.
- Authentication failures.
- Request/response size distribution.

### 4.9 Plugin Architecture

Abstract `Plugin` base class with hooks:
- `on_request(request)` → modified request.
- `on_response(request, response)` → modified response.
- `on_error(request, error)` → error response.

Plugins registered in `PluginManager` enforce sequential processing.

### 4.10 Security Headers & CORS

- Security headers: `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`.
- CORS preflight handling with `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`.

## 5. Data Flow

```
Request ID Generation
    ↓
IP Whitelist/Blacklist Check
    ↓
Rate Limiting Check (per-identifier + per-endpoint)
    ↓
Authentication (API Key, JWT, Basic, OAuth2)
    ↓
Route Matching (path + method)
    ↓
Request Validation (size, headers, CORS)
    ↓
Request Transformation
    ↓
Load Balancing + Circuit Breaker
    ↓
Upstream Proxy (with retries & timeout)
    ↓
Response Transformation
    ↓
Cache Storage (if GET + caching enabled)
    ↓
Analytics Recording
    ↓
Plugin Processing (response/error hooks)
    ↓
HTTP Response
```

## 6. Configuration Reference

### 6.1 GatewayConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | `"api-gateway"` | Gateway instance name |
| `environment` | `GatewayEnvironment` | `DEVELOPMENT` | Deployment environment |
| `host` | `str` | `"0.0.0.0"` | Bind address |
| `port` | `int` | `8080` | HTTP port |
| `https_port` | `int` | `8443` | HTTPS port |
| `worker_processes` | `int` | `4` | Worker threads |
| `max_connections` | `int` | `10000` | Max concurrent connections |
| `read_timeout` | `int` | `30` | Seconds |
| `write_timeout` | `int` | `30` | Seconds |
| `idle_timeout` | `int` | `120` | Seconds |
| `keepalive_timeout` | `int` | `65` | Seconds |

### 6.2 EndpointConfig

- `path`: URL pattern with wildcard `*` support.
- `methods`: List of `HTTPMethod`.
- `upstream_url`: Backend service URL.
- `auth_type`: `AuthType`.
- `rate_limit`: Requests per window.
- `rate_limit_window`: Seconds per window.
- `rate_limit_algorithm`: `RateLimitAlgorithm`.
- `timeout_ms`, `retries`: Upstream timeout and retry policy.
- `caching_enabled`, `cache_ttl_seconds`: Response caching.
- `cors_enabled`, `cors_origins`, `cors_methods`: CORS config.
- `validate_request_body`, `max_request_size_bytes`: Request validation.
- `headers_to_add/remove`, `query_params_to_add/remove`: Header/query manipulation.
- `request_transform`, `response_transform`: Body transformation configs.

### 6.3 RateLimitConfig

- `default_requests_per_window`, `default_window_seconds`: Fallback limits.
- `per_endpoint_limits`: Dict keyed by path.
- `per_user_limits`: Dict keyed by user identifier.
- `ip_whitelist`, `ip_blacklist`: Prefix-matched IP lists.
- `algorithm`: Default algorithm.

### 6.4 CircuitBreakerConfig

- `failure_threshold`: Failures before opening.
- `success_threshold`: Successes needed to close from half-open.
- `timeout_seconds`: Open duration.
- `half_open_requests`: Max probes during half-open.
- `monitoring_window_seconds`: Rolling window for failure count.

## 7. Observability

### 7.1 Structured Logging

- JSON or text format.
- Configurable header sanitization.
- Request/response body logging (disabled in production by default).
- Log rotation by size with retention count.

### 7.2 Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `total_requests` | Counter | Total gateway requests |
| `total_errors` | Counter | Requests with status >= 400 |
| `error_rate` | Gauge | Percentage of errors |
| `average_latency_ms` | Gauge | Mean request latency |
| `requests_per_second` | Gauge | Gateway throughput |
| `rate_limit_hits` | Counter | Requests rejected by rate limiter |
| `circuit_breaker_trips` | Counter | CB state changes |
| `cache_hits`, `cache_misses` | Counter | Cache performance |

### 7.3 Health Check

Composite health endpoint reporting:
- Endpoint registration count.
- Upstream healthy/total server count.
- Cache status (size, hit rate).
- Rate limiter status.
- Authentication status (registered keys).
- Circuit breaker count.

## 8. Security Architecture

### 8.1 Defense in Depth

```
┌─────────────────────────────────────────┐
│ Layer 1: Network                        │
│  IP whitelist/blacklist at rate limiter │
├─────────────────────────────────────────┤
│ Layer 2: Authentication                 │
│  Per-endpoint auth enforcement          │
├─────────────────────────────────────────┤
│ Layer 3: Authorization                  │
│  Scopes and roles in JWT claims         │
├─────────────────────────────────────────┤
│ Layer 4: Input Validation               │
│  Method, size, content-type, CORS       │
├─────────────────────────────────────────┤
│ Layer 5: Output Sanitization            │
│  Response transformation, security hdrs │
├─────────────────────────────────────────┤
│ Layer 6: Audit Logging                  │
│  Every request logged with identity     │
└─────────────────────────────────────────┘
```

### 8.2 CORS Handling
- Preflight `OPTIONS` requests automatically answered.
- `Access-Control-Allow-Origin` dynamically set from `cors_origins`.
- `Access-Control-Allow-Credentials` configurable per endpoint.

### 8.3 Security Headers
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Content-Security-Policy: default-src 'self'`

## 9. Performance Considerations

### 9.1 Latency Targets
- Rate limit decision: < 1ms.
- Authentication: < 5ms (JWT) / < 1ms (API key).
- Cache hit response: < 2ms.
- Cache miss + upstream proxy: Sum of upstream latency + gateway overhead (< 5ms).

### 9.2 Throughput Optimization
- Lock-free hash maps for endpoint lookup.
- Thread-local limiter instances to avoid lock contention.
- Connection pooling to upstream (planned).
- Zero-copy header manipulation where possible.

### 9.3 Scalability
- Stateless gateway design allows horizontal scaling.
- Shared Redis cache for distributed deployments (planned).
- Metrics batch export to reduce collector overhead.

## 10. State Management

### 10.1 Configuration Export/Import
- `export_config()`: JSON-serializable gateway state.
- `import_config(config_dict)`: Hydrate endpoint registries from JSON.
- Use for backup, migration, and CI/CD integration.

### 10.2 Cache Management
- `invalidate_cache(pattern)`: Regex-based pattern invalidation.
- `clear_cache()`: Full cache flush.
- `get_cache_stats()`: Size, key count, hit rate, evictions.

## 11. Testing Strategy

### 11.1 Unit Tests
- Rate limiter algorithm correctness (token counts, window boundaries).
- Circuit breaker state transitions (closed → open → half-open → closed).
- Load balancing strategy determinism.
- Request path matching (wildcards, parameters).
- Authentication flows (API key, JWT validity/expiry).
- Request validation (method, size, CORS).
- Response transformation (all transformer types).

### 11.2 Integration Tests
- End-to-end `simulate_request()` flows.
- Multi-endpoint routing scenarios.
- Rate limit enforcement in realistic request bursts.
- Circuit breaker recovery behavior.
- Cache hit/miss sequences.

### 11.3 Contract Tests
- Response schema consistency.
- Header presence for security, CORS, and rate limiting.
- Analytics record completeness.

## 12. Operational Runbook

### 12.1 Startup
1. Create `GatewayConfig` with environment-specific settings.
2. Call `configure_gateway(config)` to register all endpoints.
3. Register API keys with `register_api_key()`.
4. Call `gateway.start()` to mark gateway as running.

### 12.2 Runtime Operations
- `get_status()`: Quick health snapshot.
- `get_statistics()`: Detailed breakdown including upstream pool and circuit breaker states.
- `health_check()`: Composite health for monitoring.
- `simulate_request()`: Test routing without real HTTP server.

### 12.3 Shutdown
- `gateway.stop()` to mark stopped.
- `export_config()` to persist state.
- `clear_cache()` to release memory.

### 12.4 Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| 429 on all requests | Rate limit too tight | Increase `rate_limit` or `window_seconds` |
| 503 on all requests | No healthy upstreams | Verify upstream service and health check path |
| 401 on valid requests | JWT expiry or key mismatch | Check `jwt_secret`, token `exp`, and `authorization` header format |
| Cache stale | TTL too long | Reduce `cache_ttl_seconds` or use `invalidate_cache()` |
| High latency | Upstream slow | Review upstream service performance or decrease `timeout_ms` |
| CORS errors | Origin not in allowed list | Add origin to `cors_origins` in endpoint config |
| Circuit breaker open | Upstream failing | Wait for timeout or fix upstream service |

## 13. Design Patterns

### 13.1 Pipeline Pattern
Every request flows through a sequential pipeline of middleware stages. Each stage can modify, reject, or pass the request forward.

### 13.2 Circuit Breaker Pattern
Prevents cascade failures by wrapping upstream calls in a state machine that opens the circuit after consecutive failures.

### 13.3 Strategy Pattern
Rate limiting, load balancing, and authentication each use interchangeable strategy implementations.

### 13.4 Plugin Pattern
Middleware-like hooks at request/response/error boundaries allow custom behavior without modifying core gateway logic.

## 14. Future Roadmap

- **Phase 1**: Full-rate-limiting, auth, routing, circuit breaker, caching (completed).
- **Phase 2**: Distributed cache (Redis), cluster state sharing, gRPC gateway support.
- **Phase 3**: API keys management UI, service mesh integration (Istio/Linkerd).
- **Phase 4**: AI-driven anomaly detection, auto-tuned rate limits, predictive circuit breaking.

---

## 15. Rate Limiting Algorithm Details

### Token Bucket

```
Capacity: 10 tokens
Refill Rate: 2 tokens/second

Time 0: [●●●●●●●●●●] 10 tokens
Time 1: Request 3 → [●●●●●●●●] 7 tokens
Time 2: Request 5 → [●●●●] 2 tokens
Time 3: Refill +2 → [●●●●●●] 6 tokens
Time 4: Request 8 → [●●] 2 tokens (7 allowed, 1 rejected)
```

Configuration:
```python
TokenBucketConfig(
    capacity=100,           # Max burst size
    refill_rate=10,         # Tokens per second
    refill_interval=1.0,    # Seconds between refills
)
```

### Sliding Window

```
Window Size: 60 seconds
Max Requests: 100

Request Log (sorted timestamps):
[1000, 1200, 1500, 2000, 2500, ...]

Current Time: 5000
Window Start: 5000 - 60000 = -55000

Count requests where timestamp > window_start:
Result: 45 requests → ALLOW (45 < 100)
```

### Fixed Window

```
Window Size: 60 seconds
Max Requests: 100
Window Start: Every 60 seconds (0, 60, 120, ...)

Window [0-60]: 87 requests → ALLOW
Window [60-120]: 102 requests → REJECT (2 over limit)
```

### Leaky Bucket

```
Bucket Capacity: 10
Leak Rate: 2/second

Input: [5, 3, 8, 2] requests at t=0,1,2,3

t=0: Add 5 → [●●●●●] (5 in bucket)
t=1: Leak 2, Add 3 → [●●●●●●] (6 in bucket)
t=2: Leak 2, Add 8 → [●●●●●●●●●●] (10, full; 4 rejected)
t=3: Leak 2, Add 2 → [●●●●●●●●] (8 in bucket)
```

---

## 16. Authentication Flow Details

### API Key Authentication

```
Request: Authorization: Bearer ak_abc123def456

1. Extract key from header
2. Hash key → lookup in registered_keys dict
3. Check:
   - expired? → 401
   - ip_restricted? → 403 if IP not in allowed list
   - scope includes endpoint? → 403 if not
4. Attach key metadata to request context
5. Proceed to next middleware
```

### JWT Authentication

```
Request: Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...

1. Split header → extract token
2. Base64-decode header → verify algorithm
3. Base64-decode payload → check:
   - exp > now? → 401 if expired
   - iss matches expected issuer? → 401 if not
   - aud includes this service? → 401 if not
   - nbf <= now? → 401 if not yet valid
4. Verify signature (HMAC or RSA)
5. Extract claims → attach to request context
6. Proceed to next middleware
```

### OAuth2 Bearer Token

```
Request: Authorization: Bearer oauth2_token_xyz

1. Extract token from header
2. Pass to external IdP for validation
3. IdP returns:
   - User identity
   - Scopes/roles
   - Token expiry
4. Cache validation result (TTL: 5 minutes)
5. Attach to request context
6. Proceed to next middleware
```

---

## 17. Cache Implementation Details

### Cache Key Generation

```python
def generate_cache_key(request):
    """Generate deterministic cache key from request."""
    parts = [
        request.method,
        request.path,
        sorted(request.query_params.items()),
        # Headers that affect response (Accept, Accept-Language)
        request.headers.get("Accept", ""),
    ]
    return hashlib.sha256(json.dumps(parts).encode()).hexdigest()
```

### Cache Invalidation Patterns

```python
# Exact key
cache.invalidate("GET:/api/users/123")

# Pattern match (regex)
cache.invalidate(r"GET:/api/users/.*")

# By prefix
cache.invalidate_prefix("GET:/api/")

# Full flush
cache.clear()
```

### Stale-While-Revalidate

```
Cache Entry:
  key: "GET:/api/products"
  value: {"products": [...]}
  created_at: 2026-07-06T10:00:00Z
  ttl: 300 seconds
  stale_ttl: 60 seconds  # Serve stale for 60s after TTL

Request at T+350s (within stale window):
  → Return stale data immediately
  → Trigger background revalidation
  → Update cache with fresh data

Request at T+370s (beyond stale window):
  → Return 503 or revalidate synchronously
```

---

## 18. Circuit Breaker Configuration Guide

### Failure Threshold Tuning

| Scenario | failure_threshold | success_threshold | timeout_seconds |
|----------|-------------------|-------------------|-----------------|
| Critical service | 3 | 2 | 30 |
| Standard service | 5 | 3 | 60 |
| Non-critical | 10 | 5 | 120 |
| External API | 5 | 3 | 120 |

### Monitoring Window

```python
CircuitBreakerConfig(
    failure_threshold=5,
    success_threshold=3,
    timeout_seconds=60,
    half_open_requests=3,
    monitoring_window_seconds=300,  # 5-minute rolling window
)
```

### State Transition Rules

```
CLOSED → OPEN:
  When: failures_in_window >= failure_threshold
  Effect: All requests rejected for timeout_seconds

OPEN → HALF_OPEN:
  When: timeout_seconds elapsed
  Effect: Allow half_open_requests probe requests

HALF_OPEN → CLOSED:
  When: success_count >= success_threshold
  Effect: Resume normal traffic

HALF_OPEN → OPEN:
  When: any probe request fails
  Effect: Reset timeout, reject all again
```

---

## 19. Load Balancer Strategy Selection

| Strategy | Use Case | Pros | Cons |
|----------|----------|------|------|
| Round Robin | Equal-capacity servers | Simple, fair | Ignores load |
| Weighted RR | Heterogeneous servers | Proportional | Weight management |
| Least Connections | Variable request times | Balanced load | Connection counting overhead |
| IP Hash | Session affinity | Sticky sessions | Uneven distribution |
| Consistent Hash | Cache affinity | Minimal reshuffling | Hash function dependency |
| Random | Stateless services | Zero overhead | Potential imbalance |

### Health Check Integration

```python
# Health check configuration per upstream
upstream = UpstreamServer(
    url="http://service-a:8080",
    health_check_path="/health",
    health_check_interval=30,  # seconds
    healthy_threshold=3,       # consecutive successes
    unhealthy_threshold=2,     # consecutive failures
)
```

---

## 20. Request/Response Transformation Examples

### JSON Field Renaming

```python
# Request transform: rename "user_id" to "userId"
request_transform = {
    "type": "rename_fields",
    "mappings": {"user_id": "userId", "created_at": "createdAt"}
}
```

### Value Mapping

```python
# Response transform: map status codes
response_transform = {
    "type": "value_map",
    "field": "status",
    "mapping": {"active": "ACTIVE", "inactive": "INACTIVE"}
}
```

### Field Masking

```python
# Mask sensitive fields in response
response_transform = {
    "type": "mask_fields",
    "fields": ["email", "phone", "ssn"],
    "mask_char": "*",
    "show_first": 3,
    "show_last": 2
}
# "john.doe@example.com" → "joh***@e***.com"
```

### Base64 Encoding

```python
# Request transform: encode body
request_transform = {
    "type": "base64_encode",
    "field": "body"
}
```

---

## 21. Security Headers Reference

| Header | Value | Purpose |
|--------|-------|---------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Force HTTPS |
| `X-Frame-Options` | `DENY` | Prevent clickjacking |
| `X-Content-Type-Options` | `nosniff` | Prevent MIME sniffing |
| `X-XSS-Protection` | `1; mode=block` | XSS filter |
| `Content-Security-Policy` | `default-src 'self'` | Resource policy |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Referrer control |
| `Permissions-Policy` | `camera=(), microphone=()` | Feature policy |

---

## 22. CORS Configuration Guide

### Simple Request

```
Request:
  Origin: https://app.example.com
  Method: GET
  Headers: Content-Type

Response:
  Access-Control-Allow-Origin: https://app.example.com
  Access-Control-Allow-Methods: GET, POST, PUT, DELETE
  Access-Control-Allow-Headers: Content-Type, Authorization
  Access-Control-Max-Age: 86400
```

### Preflight Request

```
Request (OPTIONS):
  Origin: https://app.example.com
  Access-Control-Request-Method: POST
  Access-Control-Request-Headers: Content-Type, Authorization

Response:
  Access-Control-Allow-Origin: https://app.example.com
  Access-Control-Allow-Methods: POST
  Access-Control-Allow-Headers: Content-Type, Authorization
  Access-Control-Max-Age: 86400
```

### CORS Misconfiguration Prevention

```python
# Bad: wildcard with credentials
cors_origins = ["*"]  # NEVER with credentials

# Good: explicit origins
cors_origins = ["https://app.example.com", "https://admin.example.com"]

# Good: regex for subdomains
cors_origins = [r"https://.*\.example\.com"]
```

---

## 23. Plugin Development Guide

### Creating a Custom Plugin

```python
from agents.api_gateway.plugins import Plugin

class RateTrackingPlugin(Plugin):
    """Track request rates per endpoint for custom analytics."""

    def __init__(self):
        self.request_counts = {}

    def on_request(self, request):
        endpoint = request.path
        self.request_counts[endpoint] = self.request_counts.get(endpoint, 0) + 1
        return request

    def on_response(self, request, response):
        # Add rate header
        endpoint = request.path
        response.headers["X-Request-Count"] = str(self.request_counts.get(endpoint, 0))
        return response

    def on_error(self, request, error):
        # Log error for rate tracking
        return {"error": str(error), "status": 500}
```

### Plugin Registration

```python
from agents.api_gateway.plugins import PluginManager

manager = PluginManager()
manager.register(RateTrackingPlugin())
manager.register(AuthLoggingPlugin())
manager.register(CustomMetricsPlugin())

# Plugins execute in registration order
gateway = APIGateway(plugin_manager=manager)
```

---

## 24. Analytics Dashboard Metrics

### Request Distribution

```
Endpoint Breakdown (Last Hour):
┌─────────────────────┬────────┬──────────┬──────────┐
│ Endpoint            │ Count  │ Avg (ms) │ Errors   │
├─────────────────────┼────────┼──────────┼──────────┤
│ GET /api/users      │ 1,247  │ 12ms     │ 3 (0.2%) │
│ POST /api/orders    │   892  │ 45ms     │ 12 (1.3%)│
│ GET /api/products   │ 3,456  │ 8ms      │ 0 (0.0%) │
│ PUT /api/cart       │   234  │ 23ms     │ 5 (2.1%) │
└─────────────────────┴────────┴──────────┴──────────┘
```

### Latency Percentiles

```
Latency Distribution (GET /api/users):
  p50:  10ms
  p75:  15ms
  p90:  22ms
  p95:  35ms
  p99:  89ms
  max: 234ms
```

### Cache Performance

```
Cache Stats:
  Total Keys: 1,456
  Hit Rate: 87.3%
  Miss Rate: 12.7%
  Evictions: 234
  Memory Used: 45.2 MB
  Memory Limit: 100 MB
```
