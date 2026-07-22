---
name: "authentication"
category: "api-gateway"
version: "2.0.0"
tags: ["authentication", "oauth2", "jwt", "api-keys", "mtls", "sso", "identity"]
---

# Gateway Authentication

## Overview

Gateway-level authentication and authorization framework for API gateways supporting OAuth 2.0 (all grant types), API key validation, JWT verification, mTLS client certificates, HMAC request signing, and SSO integration. This module provides centralized authentication middleware that validates credentials before requests reach backend services, with token introspection, JWKS caching, session management, and multi-tenant authentication support.

## Core Capabilities

- **OAuth 2.0 Gateway**: Validate access tokens via introspection, JWT verification, and token exchange
- **API Key Management**: Validate, rotate, and revoke API keys with scope-based access control
- **JWT Verification**: JWKS-based signature verification with key rotation and caching
- **mTLS Support**: Client certificate validation against trusted CA bundles
- **HMAC Signing**: Request signature validation for webhook and inter-service authentication
- **Token Introspection**: RFC 7662 token introspection with caching
- **SSO Integration**: SAML, OIDC, and LDAP integration for enterprise SSO
- **Multi-Tenant**: Tenant-aware authentication with per-tenant identity providers

## Usage

```python
from authentication import (
    AuthMiddleware, OAuth2Config, APIKeyStore, JWTVerifier, MTLSConfig
)

# Configure OAuth 2.0
oauth = OAuth2Config(
    issuer="https://auth.example.com",
    audience="https://api.example.com",
    jwks_uri="https://auth.example.com/.well-known/jwks.json",
    introspection_endpoint="https://auth.example.com/introspect",
    scopes_supported=["read", "write", "admin"],
)

# API key store
api_keys = APIKeyStore()
api_keys.add_key(
    key_id="ak_live_abc123",
    name="Production App",
    scopes=["read", "write"],
    rate_limit=1000,
    expires_at="2025-12-31T23:59:59Z",
)

# JWT verifier
jwt_verifier = JWTVerifier(oauth)

# MTLS config
mtls = MTLSConfig(
    client_ca_bundle="/etc/ssl/client-ca.pem",
    verify_client_cert=True,
    allowed_cn_patterns=["*.internal.example.com"],
)

# Create middleware
auth = AuthMiddleware(
    oauth_config=oauth,
    api_key_store=api_keys,
    jwt_verifier=jwt_verifier,
    mtls_config=mtls,
    routes={
        "/api/public/*": {"auth": False},
        "/api/admin/*": {"required_scopes": ["admin"]},
        "/api/users/*": {"required_scopes": ["read"]},
    },
)

# Authenticate request
result = auth.authenticate(
    path="/api/users/123",
    headers={"Authorization": "Bearer eyJhbGciOi..."},
    method="GET",
)
print(f"Authenticated: {result.authenticated}")
print(f"User: {result.user_id}")
print(f"Scopes: {result.scopes}")
print(f"Method: {result.auth_method}")
```

## Best Practices

- Always validate JWT signatures against the issuer's JWKS endpoint — never skip verification
- Use short-lived access tokens (15 minutes) with refresh token rotation
- Implement token introspection caching (5-10 minutes) to reduce latency
- Apply different authentication levels per route — public endpoints need no auth
- Use API keys only for server-to-server communication, not for end-user authentication
- Implement mTLS for service-to-service communication in zero-trust architectures
- Monitor authentication failures for brute-force and credential stuffing attacks
- Cache JWKS keys with appropriate TTL (1 hour) and handle key rotation gracefully
- Use HMAC signing for webhook endpoints to prevent request forgery
- Implement graceful degradation — if identity provider is down, fail closed (deny)

## Related Modules

- **api-security** — Security middleware and OWASP protections
- **api-gateway** → **api-management** — Gateway configuration with auth plugins
- **api-gateway** → **rate-limiting** — Rate limiting tied to authenticated consumers
- **zero-trust** → **identity-verification** — Zero-trust identity verification
- **api-gateway** → **caching** — Token and JWKS caching strategies

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
| 401 Unauthorized on valid token | JWKS cache stale | Force JWKS refresh, check token expiry |
| mTLS handshake failure | Certificate chain incomplete | Include intermediate CA certs |
| OAuth callback error | redirect_uri mismatch | Update registered redirect URIs |
| Token introspection timeout | IdP overloaded | Increase timeout, implement caching |
| API key validation slow | Unindexed lookup | Add database index on key field |

### Debug Mode

```yaml
# Enable debug logging for authentication
auth:
  debug: true
  log_token_claims: true
  log_failed_attempts: true
  log_successful_attempts: false
```

```bash
# Validate a JWT token
curl -s http://localhost:8080/auth/validate \
  -H "Authorization: Bearer eyJhbGciOi..." | jq .

# Check JWKS cache status
curl -s http://localhost:8080/auth/jwks/cache | jq .

# Force JWKS refresh
curl -X POST http://localhost:8080/auth/jwks/refresh

# View API key status
curl -s http://localhost:8080/auth/api-keys/ak_live_abc123 | jq .
```

### Token Debugging

```python
import jwt
import requests

# Decode JWT without verification (for debugging only)
def debug_jwt(token):
    # Decode header
    header = jwt.get_unverified_header(token)
    print(f"Algorithm: {header['alg']}")
    print(f"Key ID: {header.get('kid', 'N/A')}")

    # Decode payload
    payload = jwt.decode(token, options={"verify_signature": False})
    print(f"Issuer: {payload.get('iss')}")
    print(f"Audience: {payload.get('aud')}")
    print(f"Scopes: {payload.get('scope')}")
    print(f"Expires: {payload.get('exp')}")

    return payload
```

## Security Hardening

### Security Headers

```yaml
security_headers:
  # HSTS
  strict_transport_security:
    max_age: 31536000
    include_subdomains: true
    preload: true

  # Content Security
  content_security_policy:
    default_src: "'self'"
    script_src: "'self'"
    style_src: "'self' 'unsafe-inline'"
    img_src: "'self' data:"

  # Clickjacking
  x_frame_options: "DENY"

  # MIME sniffing
  x_content_type_options: "nosniff"

  # Referrer
  referrer_policy: "strict-origin-when-cross-origin"
```

### OAuth 2.0 Security

```yaml
oauth2:
  # Token settings
  access_token_ttl: 900      # 15 minutes
  refresh_token_ttl: 86400   # 24 hours
  rotation:
    enabled: true
    on_usage: false
    on_refresh: true

  # PKCE
  pkce:
    required: true
    methods: ["S256"]

  # Token binding
  token_binding:
    enabled: true
    method: "tls_cert"

  # Scope validation
  scope_validation:
    strict: true
    allowed_scopes:
      - "read"
      - "write"
      - "admin"
```

### API Key Security

```yaml
api_keys:
  # Key generation
  length: 32
  prefix: "ak_"
  charset: "alphanumeric"

  # Rotation
  rotation:
    enabled: true
    max_age_days: 90
    warning_days: 14

  # Usage tracking
  tracking:
    enabled: true
    log_ip: true
    log_user_agent: true

  # Revocation
  revocation:
    immediate: true
    grace_period: 3600  # 1 hour for graceful revocation
```

## Configuration Reference

### OAuth 2.0 Flows

```yaml
oauth2_flows:
  # Authorization Code (with PKCE)
  authorization_code:
    enabled: true
    pkce_required: true
    state_required: true
    nonce_required: true

  # Client Credentials
  client_credentials:
    enabled: true
    client_authentication: "client_secret_basic"

  # Device Authorization
  device_code:
    enabled: true
    interval: 5
    expires_in: 600

  # Resource Owner Password (deprecated)
  password:
    enabled: false  # Not recommended
```

### JWT Configuration

```yaml
jwt:
  # Verification
  verification:
    issuer: "https://auth.example.com"
    audience: "https://api.example.com"
    algorithms: ["RS256", "ES256"]

  # JWKS
  jwks:
    uri: "https://auth.example.com/.well-known/jwks.json"
    cache_ttl: 3600
    refresh_interval: 300

  # Claims
  claims:
    required: ["sub", "iss", "exp", "aud"]
    custom:
      - name: "scope"
        required: true
      - name: "tenant_id"
        required: false
```

### mTLS Configuration

```yaml
mtls:
  enabled: true
  client_ca:
    bundle: "/etc/ssl/client-ca.pem"
    verify_chain: true
    check_revocation: true

  # Certificate validation
  validation:
    min_key_size: 2048
    allowed_algorithms: ["RSA", "ECDSA"]
    max_cert_age_days: 365

  # Client identity
  identity:
    extract_from: "cn"  # or "san"
    cn_patterns:
      - "*.internal.example.com"
      - "service-*.prod"
```

## Migration Guide

### Auth Provider Migration

```bash
# Export current auth config
auth-cli export --format yaml > auth-config-v1.yaml

# Migrate to new provider
auth-cli migrate \
  --input auth-config-v1.yaml \
  --output auth-config-v2.yaml \
  --target-provider "new-idp"

# Validate configuration
auth-cli validate --input auth-config-v2.yaml

# Deploy with token migration
auth-cli deploy \
  --input auth-config-v2.yaml \
  --migrate-tokens \
  --grace-period 3600
```

### API Key Migration

```bash
# Export API keys
auth-cli export-keys --format csv > api-keys.csv

# Generate new keys for all consumers
auth-cli rotate-all --grace-period 86400

# Monitor migration progress
auth-cli status --watch
```

## FAQ

**Q: How often should I rotate API keys?**
A: Rotate every 90 days. Implement automated rotation with a 14-day warning period.

**Q: Can I use multiple auth methods on the same endpoint?**
A: Yes. Configure fallback order: mTLS -> JWT -> API Key. The first successful method wins.

**Q: What happens if the IdP is down?**
A: The gateway fails closed (denies requests) unless you configure a cached fallback for recently validated tokens.

**Q: How do I handle token revocation?**
A: Use token introspection for real-time validation, or implement short-lived tokens (15 min) with refresh token rotation.

## Benchmarks

| Operation | Throughput | Latency p50 | Latency p99 |
|-----------|-----------|-------------|-------------|
| JWT verification | 50,000 req/s | 1ms | 5ms |
| API key validation | 80,000 req/s | 0.5ms | 2ms |
| mTLS handshake | 10,000 req/s | 5ms | 15ms |
| Token introspection | 20,000 req/s | 2ms | 10ms |
| OAuth token exchange | 15,000 req/s | 3ms | 12ms |

## Code Examples

### Custom Auth Provider

```python
class CustomAuthProvider:
    def __init__(self, config):
        self.config = config
        self.client = httpx.AsyncClient()

    async def validate_token(self, token: str) -> AuthResult:
        """Validate token against custom provider."""
        try:
            response = await self.client.post(
                self.config["introspection_endpoint"],
                data={"token": token},
                auth=(self.config["client_id"], self.config["client_secret"])
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("active"):
                    return AuthResult(
                        authenticated=True,
                        user_id=data["sub"],
                        scopes=data.get("scope", "").split(),
                    )

            return AuthResult(authenticated=False)

        except Exception as e:
            logger.error(f"Auth provider error: {e}")
            return AuthResult(authenticated=False)
```

### Scope-Based Authorization

```python
from functools import wraps

def require_scopes(*required_scopes):
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            auth_result = kwargs.get("auth_result")

            if not auth_result or not auth_result.authenticated:
                return Response(status=401)

            # Check if user has ALL required scopes
            user_scopes = set(auth_result.scopes)
            if not set(required_scopes).issubset(user_scopes):
                missing = set(required_scopes) - user_scopes
                return Response(
                    status=403,
                    json={"error": "insufficient_scope", "missing": list(missing)}
                )

            return await f(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@app.route("/api/admin/users", methods=["GET"])
@require_scopes("admin", "users:read")
async def list_users():
    return jsonify(users)
```

## Advanced Monitoring

### Authentication Metrics

```yaml
metrics:
  - name: "auth_attempts_total"
    type: "counter"
    labels: ["method", "status", "reason"]
    description: "Total authentication attempts"

  - name: "auth_latency_seconds"
    type: "histogram"
    labels: ["method"]
    description: "Authentication latency"

  - name: "token_validation_total"
    type: "counter"
    labels: ["type", "status"]
    description: "Token validation attempts"
```

### Alert Rules

```yaml
groups:
  - name: auth-alerts
    rules:
      - alert: HighAuthFailureRate
        expr: sum(rate(auth_attempts_total{status="failed"}[5m])) / sum(rate(auth_attempts_total[5m])) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High authentication failure rate (>10%)"

      - alert: BruteForceDetected
        expr: sum(rate(auth_attempts_total{status="failed"}[1m])) by (source_ip) > 10
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Potential brute force from {{ $labels.source_ip }}"

      - alert: JWKSRefreshFailed
        expr: increase(jwks_refresh_errors_total[5m]) > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "JWKS refresh failed"
```

## Capacity Planning

### Auth Resource Requirements

| Concurrent Users | JWT Validation/sec | API Key Lookups/sec | Redis Memory |
|-----------------|-------------------|--------------------| ------------|
| 1K | 1K | 1K | 50MB |
| 10K | 10K | 10K | 200MB |
| 100K | 50K | 80KB | 1GB |
| 1M | 200K | 500KB | 8GB |

### JWKS Cache Sizing

```
Average JWKS size: 5KB
Cache entries: 10 (one per IdP)
Total cache size: 50KB
Refresh frequency: Every 5 minutes
Redis operations: 12/hour per IdP
```
