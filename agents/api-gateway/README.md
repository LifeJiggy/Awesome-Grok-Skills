# API Gateway Agent

Enterprise-grade API gateway providing routing, authentication, rate limiting, caching, circuit breaking, load balancing, request/response transformation, analytics, and plugin extensibility.

## Quick Start

```python
from agents.api_gateway.agent import APIGatewayAgent, GatewayConfig, EndpointConfig, HTTPMethod, AuthType

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

## Running the Agent

```bash
python agents/api-gateway/agent.py
```

## Capabilities

| Domain | Capabilities |
|--------|--------------|
| **Routing** | Dynamic path matching with wildcards and parameterized paths |
| **Authentication** | API key, JWT, OAuth2, Basic Auth, mTLS |
| **Rate Limiting** | Token Bucket, Sliding Window, Fixed Window, Leaky Bucket |
| **Load Balancing** | Round Robin, Weighted, Least Connections, IP Hash, Consistent Hash, Random |
| **Resilience** | Per-upstream circuit breaker, timeout, retries, health checks |
| **Transformation** | Request/response body transformation (JSON↔XML, field ops, base64, masking) |
| **Caching** | In-memory TTL cache with pattern invalidation |
| **Analytics** | Per-endpoint, per-status, per-auth-type metrics; cache hit ratio; latency tracking |
| **Plugins** | Plugin hooks: on_request, on_response, on_error |
| **Security** | CORS, security headers, IP whitelist/blacklist, request size limits |
| **Operations** | Config export/import, health check, upstream health updates, cache invalidation |
| **Cost** | Budget tracking, ROI, CPC, CPM, LTV/CAC estimation |

## Core API Reference

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
    method="GET", path="/api/v1/users",
    headers={"authorization": "Bearer <jwt>"},
    client_ip="10.0.0.1",
)
# Returns: {request_id, status, body, latency_ms, cached, upstream}
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

### Experimentation
```python
exp = agent.run_growth_experiment(experiment={"name": "CTA test", "hypothesis": "Variant B wins", "variant_a": "Buy", "variant_b": "Get Started"}, campaign_id="camp-1")
```

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

## Rate Limiting Reference

| Algorithm | Use Case |
|-----------|----------|
| Token Bucket | Allow smooth bursts with steady refill |
| Sliding Window | Smooth distribution across window |
| Fixed Window | Coarse-grained limits |
| Leaky Bucket | Constant output rate, no bursts |

## Circuit Breaker Reference

| State | Meaning | Transition |
|-------|---------|------------|
| `CLOSED` | Normal operation | → OPEN when `failure_count >= failure_threshold` |
| `OPEN` | Requests rejected | → HALF_OPEN after `timeout_seconds` |
| `HALF_OPEN` | Limited probes | → CLOSED when `successes >= success_threshold`; → OPEN on failure |

## Security & Privacy

- No credentials logged; API keys stored in-memory only.
- JWT validated with signature, expiration, issuer, audience checks.
- Sensitive headers (Authorization, X-API-Key, Cookie) excluded from logs.
- CORS origins restricted by configurable allow-list.
- Request body size enforced per endpoint.
- Security headers auto-injected (HSTS, X-Frame-Options, X-Content-Type-Options, CSP).

## Performance

| Operation | Target |
|-----------|--------|
| Route match | O(n) linear scan (small endpoint count) |
| Token bucket check | O(1) with lock |
| Sliding window | O(k) where k = valid entries per identifier |
| Circuit breaker check | O(1) with lock |
| Cache hit | O(1) dict lookup |
| Cache eviction | O(m) where m = keys sorted by age |

## State Management

```python
state = agent.export_config()
agent.import_config(state)   # Restore gateway state
```

Cache is not persisted across restarts; rebuild from scratch after import.

## File Structure

```
agents/api-gateway/
  agent.py           # Main implementation (~1100 lines)
  ARCHITECTURE.md    # Deep system design and data flow
  GROK.md            # Agent prompt and method specifications
  README.md          # Usage guide and quick reference
```

## Constraints

- Single-process, single-node gateway.
- Basic Auth demo credentials are illustrative; use LDAP/OAuth2 in production.
- TLS termination is configured but not performed; use NGINX, Envoy, or cloud load balancer.
- Consistent hash is a deterministic approximation; true consistent hashing requires a ring implementation.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| 429 on all requests | Rate limit too tight or IP blacklisted | Increase `default_requests_per_window` or inspect blacklist |
| 503 on all requests | No healthy upstreams | Check upstream health paths; verify services |
| 401 on valid requests | JWT secret/expiry mismatch | Verify secret, exp, iss, aud |
| Cache stale | TTL too long | Reduce `cache_ttl_seconds` or use `invalidate_cache()` |
| CB trips | Upstream unstable | Increase `failure_threshold`, reduce `timeout_seconds` |
