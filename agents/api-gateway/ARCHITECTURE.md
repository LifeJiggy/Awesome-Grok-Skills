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

### 7.2 Defense in Depth
1. **Network Layer**: IP whitelist/blacklist at rate limiter level.
2. **Authentication Layer**: Per-endpoint auth enforcement.
3. **Authorization Layer**: Scopes and roles in JWT claims.
4. **Input Validation**: Method, size, content-type, CORS.
5. **Output Sanitization**: Response transformation, security headers.
6. **Audit Logging**: Every request logged with identity and outcome.

### 7.3 CORS Handling
- Preflight `OPTIONS` requests automatically answered.
- `Access-Control-Allow-Origin` dynamically set from `cors_origins`.
- `Access-Control-Allow-Credentials` configurable per endpoint.

### 7.4 Security Headers
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

## 13. Future Roadmap

- **Phase 1**: Full-rate-limiting, auth, routing, circuit breaker, caching (completed).
- **Phase 2**: Distributed cache (Redis), cluster state sharing, gRPC gateway support.
- **Phase 3**: API keys management UI, service mesh integration (Istio/Linkerd).
- **Phase 4**: AI-driven anomaly detection, auto-tuned rate limits, predictive circuit breaking.
