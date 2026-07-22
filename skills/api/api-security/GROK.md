---
name: "api-security"
category: "api"
version: "2.0.0"
tags: ["api", "security", "authentication", "authorization", "oauth", "jwt", "rate-limiting", "owasp"]
---

# API Security

## Overview

Comprehensive API security framework covering authentication (OAuth 2.0, API keys, JWT, mTLS), authorization (RBAC, ABAC, scoped permissions), input validation, rate limiting, CORS, CSRF, injection prevention, and security headers. This module implements OWASP API Security Top 10 protections, provides security middleware for common frameworks, and offers automated security testing tools for identifying vulnerabilities in API endpoints.

## Core Capabilities

- **Authentication**: OAuth 2.0 (authorization code, client credentials, PKCE), API key management, JWT validation, and mTLS client certificates
- **Authorization**: Role-based access control (RBAC), attribute-based access control (ABAC), resource-level permissions, and API scope management
- **Input Validation**: Request schema validation, type coercion prevention, SQL injection detection, XSS filtering, and file upload validation
- **Rate Limiting**: Per-user, per-endpoint, and global rate limits with sliding window, token bucket, and leaky bucket algorithms
- **Security Headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, and CORS policy configuration
- **OWASP API Top 10**: Protections against BOLA, broken authentication, excessive data exposure, lack of rate limiting, and mass assignment
- **Security Testing**: Automated scanning for common API vulnerabilities with severity scoring
- **Audit Logging**: Complete API access logs with user, endpoint, timestamp, and response code

## Usage

```python
from api_security import (
    SecurityMiddleware, OAuthConfig, JWTValidator, RateLimiter, RBACPolicy
)

# Configure OAuth 2.0
oauth = OAuthConfig(
    issuer="https://auth.example.com",
    audience="https://api.example.com",
    scopes=["read:users", "write:users", "admin"],
    token_endpoint="https://auth.example.com/token",
    jwks_uri="https://auth.example.com/.well-known/jwks.json",
)

# JWT validation
validator = JWTValidator(oauth)
token = "eyJhbGciOiJSUzI1NiIs..."
result = validator.validate(token)
print(f"Valid: {result.valid}")
print(f"Scopes: {result.scopes}")
print(f"Expires: {result.expires_at}")

# Rate limiting
limiter = RateLimiter(
    default_limit=100,
    window_seconds=60,
    strategy="sliding_window",
)
limiter.add_limit("POST /api/users", limit=10, window=60)
limiter.add_limit("GET /api/search", limit=30, window=60)

# RBAC policy
rbac = RBACPolicy()
rbac.add_role("admin", permissions=["*"])
rbac.add_role("user", permissions=["read:own", "write:own"])
rbac.add_role("viewer", permissions=["read:all"])
rbac.add_assignment("user-123", "admin")

# Check authorization
authorized = rbac.check("user-123", "write:users")
print(f"Authorized: {authorized}")
```

## Best Practices

- Always use HTTPS — never transmit credentials over plaintext HTTP
- Implement OAuth 2.0 with PKCE for public clients (mobile, SPA)
- Use short-lived JWTs (15 minutes) with refresh token rotation
- Validate JWT signatures against the issuer's JWKS endpoint
- Apply rate limiting at every API endpoint — different limits for different operations
- Validate all input against a schema — never trust client data
- Use parameterized queries to prevent SQL injection
- Implement CORS with explicit origin allowlists — never use wildcard with credentials
- Log all authentication failures and rate limit violations for security monitoring
- Rotate API keys regularly and provide key revocation endpoints
- Use mTLS for service-to-service communication in microservice architectures
- Implement request signing (HMAC) for webhook endpoints

## Related Modules

- **api-design** — Secure API design patterns
- **api-versioning** — Version-aware security policy management
- **api-gateway** → **authentication** — Gateway-level authentication
- **api-gateway** → **rate-limiting** — Distributed rate limiting
- **zero-trust** → **security-framework** — Zero-trust principles for API security

## Advanced Configuration

### YAML Configuration
```yaml
version: "2.0.0"
settings:
  mode: "production"
  concurrency: 4
  timeout_ms: 30000
  cors:
    allowed_origins: ["https://app.example.com"]
    allow_credentials: true
  rate_limit:
    enabled: true
    requests_per_minute: 1000
```

### JSON Configuration
```json
{"version":"2.0.0","settings":{"mode":"production","cors":{"allowed_origins":["https://app.example.com"]}}}
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SKILL_MODE` | Runtime mode | `production` |
| `API_BASE_URL` | API base URL | `http://localhost:3000` |
| `SKILL_TIMEOUT` | Timeout (ms) | `30000` |
| `CORS_ORIGINS` | Allowed origins | `*` |

## Architecture Patterns

### System Architecture
```
+---------------------------------------------------+
|                   Client Layer                     |
|  +----------+  +----------+  +------------------+  |
|  |  Web App |  | Mobile   |  |  Third-Party     |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|                 Gateway Layer                      |
|  +------------------+---------------------------+  |
|  |  Rate Limiter / Auth / CORS / Transform      |  |
|  +------------------+---------------------------+  |
+-----------------+---------------------------------+
|              Application Layer                     |
|  +----------+  +----------+  +------------------+  |
|  |  Router  |  | Handler  |  |  Middleware       |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|                 Data Layer                          |
|  +----------+  +----------+  +------------------+  |
|  |  Cache   |  | Database |  |  External APIs   |  |
|  |  (Redis) |  |(Postgres)|  |                  |  |
|  +----------+  +----------+  +------------------+  |
+---------------------------------------------------+
```

### Request Lifecycle
```
Request -> Auth -> Rate Limit -> Validate -> Route -> Handler -> Response
  |         |        |           |         |        |
  |    [Token]  [Counter]   [Schema]    [Match]  [Logic]
  +---------+---------+----------+---------+--------+
                    Error Handling Pipeline
```

## Integration Guide

### React
```javascript
import { useApi } from '@skill/react';
function UsersList() {
  const { data, loading } = useApi('/api/users');
  return loading ? <Spinner /> : <UserTable users={data} />;
}
```

### Python SDK
```python
from skill_sdk import SkillClient
client = SkillClient(api_key="your-key")
users = client.users.list(page=1, limit=20)
```

## Performance Optimization

| Operation | Throughput | Latency (p50) | Latency (p99) |
|-----------|-----------|---------------|---------------|
| GET (cached) | 50,000 req/s | 2ms | 10ms |
| GET (uncached) | 10,000 req/s | 20ms | 100ms |
| POST | 5,000 req/s | 50ms | 200ms |

### Tips
1. Cache GET responses
2. Enable compression
3. Cursor-based pagination
4. Sparse fieldsets
5. Connection pooling

## Security Considerations

| Threat | Risk | Mitigation |
|--------|------|------------|
| Injection | High | Input validation |
| BOLA/IDOR | High | Authz checks |
| Mass assignment | High | Allowlist fields |
| CSRF | Medium | CSRF tokens |
| XSS | Medium | Content-Type headers |

### OWASP Checklist
- [ ] API1: Broken Object Level Auth
- [ ] API2: Broken Authentication
- [ ] API4: Unrestricted Resource Consumption

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| 429 | Rate limit | Backoff |
| 401 | Invalid token | Refresh token |
| 403 | No permission | Check roles |
| 404 | Wrong URL | Verify endpoint |
| 500 | Server error | Check logs |

## API Reference

### `validate_request(request) -> ValidationResult`
### `format_response(data, format) -> Response`
### `check_rate_limit(key, endpoint) -> RateLimitResult`

## Data Models

### Request Schema
```json
{"type":"object","required":["method","path"],"properties":{"method":{"type":"string"},"path":{"type":"string"}}}
```

### Response Schema
```json
{"type":"object","properties":{"data":{"type":"object"},"meta":{"type":"object"},"links":{"type":"object"}}}
```

## Deployment Guide

### Docker
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
HEALTHCHECK CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    spec:
      containers:
      - name: api
        image: api:2.0.0
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Monitoring & Observability

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `http_requests_total` | Counter | Total requests | -- |
| `http_request_duration_ms` | Histogram | Latency | p99 > 500ms |
| `http_errors_total` | Counter | Errors | > 5% |

## Testing Strategy

```python
def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200

def test_create_user():
    response = client.post("/api/users", json={"name": "Test"})
    assert response.status_code == 201
```

## Versioning & Migration

- Major version for breaking changes
- 6-month deprecation notice

### Changelog
- **[2.0.0]** -- New architecture
- **[1.5.0]** -- Added filtering
- **[1.0.0]** -- Initial release

## Glossary

| Term | Definition |
|------|------------|
| **Endpoint** | API route |
| **Payload** | Request/response data |
| **BOLA** | Broken Object Level Authorization |
| **CORS** | Cross-Origin Resource Sharing |
| **CSRF** | Cross-Site Request Forgery |
| **TTL** | Time-to-live |

## Changelog

### [2.0.0] -- 2024-12-01
- Major release

### [1.5.0] -- 2024-06-15
- Filtering added

### [1.0.0] -- 2024-01-01
- Initial release

## Contributing Guidelines

```bash
git clone https://github.com/example/api.git
cd api
npm install
npm run dev
```

## License

MIT License -- Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Detailed Configuration Reference

### Full YAML Configuration

```yaml
version: "2.0.0"
settings:
  mode: "production"
  environment: "staging"
  concurrency: 8
  timeout_ms: 30000
  keep_alive: true
  max_connections: 1000
  cors:
    enabled: true
    allowed_origins:
      - "https://app.example.com"
      - "https://admin.example.com"
    allowed_methods:
      - GET
      - POST
      - PUT
      - PATCH
      - DELETE
    allowed_headers:
      - Authorization
      - Content-Type
      - X-Request-ID
    allow_credentials: true
    max_age: 86400
  rate_limit:
    enabled: true
    default_requests_per_minute: 1000
    default_burst: 50
    strategies:
      - endpoint: "POST /api/users"
        requests_per_minute: 10
        burst: 5
      - endpoint: "GET /api/search"
        requests_per_minute: 30
        burst: 10
      - endpoint: "DELETE /api/users/*"
        requests_per_minute: 5
        burst: 2
  logging:
    level: "info"
    format: "json"
    output: "stdout"
    sensitive_fields:
      - password
      - token
      - secret
  tracing:
    enabled: true
    sample_rate: 0.1
    exporter: "otlp"
    endpoint: "http://localhost:4318"
  metrics:
    enabled: true
    prefix: "api"
    histogram_buckets: [5, 10, 25, 50, 100, 250, 500, 1000]
    labels:
      service: "user-api"
      environment: "production"
  cache:
    enabled: true
    backend: "redis"
    host: "localhost"
    port: 6379
    ttl_seconds: 300
    max_memory: "256mb"
    eviction_policy: "lru"
  database:
    pool_size: 20
    max_overflow: 10
    pool_timeout: 30
    pool_recycle: 1800
    echo: false
  health_check:
    enabled: true
    path: "/health"
    checks:
      - name: "database"
        type: "ping"
      - name: "cache"
        type: "ping"
      - name: "disk"
        type: "df"
        threshold_percent: 90
```

### Full JSON Configuration

```json
{
  "version": "2.0.0",
  "settings": {
    "mode": "production",
    "environment": "staging",
    "concurrency": 8,
    "timeout_ms": 30000,
    "keep_alive": true,
    "max_connections": 1000,
    "cors": {
      "enabled": true,
      "allowed_origins": [
        "https://app.example.com",
        "https://admin.example.com"
      ],
      "allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
      "allowed_headers": ["Authorization", "Content-Type", "X-Request-ID"],
      "allow_credentials": true,
      "max_age": 86400
    },
    "rate_limit": {
      "enabled": true,
      "default_requests_per_minute": 1000,
      "default_burst": 50,
      "strategies": [
        {
          "endpoint": "POST /api/users",
          "requests_per_minute": 10,
          "burst": 5
        },
        {
          "endpoint": "GET /api/search",
          "requests_per_minute": 30,
          "burst": 10
        }
      ]
    },
    "logging": {
      "level": "info",
      "format": "json",
      "output": "stdout",
      "sensitive_fields": ["password", "token", "secret"]
    },
    "tracing": {
      "enabled": true,
      "sample_rate": 0.1,
      "exporter": "otlp",
      "endpoint": "http://localhost:4318"
    },
    "metrics": {
      "enabled": true,
      "prefix": "api",
      "histogram_buckets": [5, 10, 25, 50, 100, 250, 500, 1000],
      "labels": {
        "service": "user-api",
        "environment": "production"
      }
    },
    "cache": {
      "enabled": true,
      "backend": "redis",
      "host": "localhost",
      "port": 6379,
      "ttl_seconds": 300,
      "max_memory": "256mb",
      "eviction_policy": "lru"
    },
    "database": {
      "pool_size": 20,
      "max_overflow": 10,
      "pool_timeout": 30,
      "pool_recycle": 1800,
      "echo": false
    },
    "health_check": {
      "enabled": true,
      "path": "/health",
      "checks": [
        {"name": "database", "type": "ping"},
        {"name": "cache", "type": "ping"},
        {"name": "disk", "type": "df", "threshold_percent": 90}
      ]
    }
  }
}
```

### Complete Environment Variables Reference

| Variable | Description | Default | Type | Required |
|----------|-------------|---------|------|----------|
| `SKILL_MODE` | Runtime mode (production, development, testing) | `production` | string | No |
| `API_BASE_URL` | Base URL for API endpoints | `http://localhost:3000` | url | No |
| `SKILL_TIMEOUT` | Request timeout in milliseconds | `30000` | integer | No |
| `CORS_ORIGINS` | Comma-separated allowed origins | `*` | string | No |
| `CORS_ALLOW_CREDENTIALS` | Allow credentials in CORS requests | `false` | boolean | No |
| `RATE_LIMIT_ENABLED` | Enable rate limiting | `true` | boolean | No |
| `RATE_LIMIT_RPM` | Default requests per minute | `1000` | integer | No |
| `LOG_LEVEL` | Logging level (debug, info, warn, error) | `info` | string | No |
| `LOG_FORMAT` | Log format (json, text) | `json` | string | No |
| `TRACING_ENABLED` | Enable distributed tracing | `true` | boolean | No |
| `TRACING_SAMPLE_RATE` | Trace sample rate (0.0 - 1.0) | `0.1` | float | No |
| `METRICS_ENABLED` | Enable metrics collection | `true` | boolean | No |
| `METRICS_PREFIX` | Metrics name prefix | `api` | string | No |
| `CACHE_BACKEND` | Cache backend (redis, memcached, memory) | `redis` | string | No |
| `CACHE_HOST` | Cache server host | `localhost` | string | Yes |
| `CACHE_PORT` | Cache server port | `6379` | integer | Yes |
| `CACHE_TTL` | Default cache TTL in seconds | `300` | integer | No |
| `DB_HOST` | Database host | `localhost` | string | Yes |
| `DB_PORT` | Database port | `5432` | integer | Yes |
| `DB_NAME` | Database name | `api_db` | string | Yes |
| `DB_USER` | Database user | `api_user` | string | Yes |
| `DB_PASSWORD` | Database password | -- | string | Yes |
| `DB_POOL_SIZE` | Connection pool size | `20` | integer | No |
| `DB_POOL_OVERFLOW` | Max overflow connections | `10` | integer | No |
| `HEALTH_CHECK_PATH` | Health check endpoint path | `/health` | string | No |

## Advanced Architecture Patterns

### Microservices Architecture

```
                          +-----------------+
                          |   API Gateway   |
                          |  (Kong/Envoy)  |
                          +--------+--------+
                                   |
                    +--------------+--------------+
                    |              |              |
             +------+------+ +----+----+ +------+------+
             |  User API   | | Order   | | Product API |
             |  Service    | | Service | |  Service    |
             +------+------+ +----+----+ +------+------+
                    |              |              |
             +------+------+ +----+----+ +------+------+
             |  User DB    | | Order   | | Product DB  |
             | (Postgres)  | | DB      | | (Postgres)  |
             +-------------+ |(Postgres)+-------------+
                             +----------+
```

### Event-Driven Architecture

```
+----------+     +---------+     +----------+     +----------+
| Producer | --> | Message | --> | Consumer | --> | Handler  |
| (API)    |     | Broker  |     | (Worker) |     | (Logic)  |
+----------+     | (Kafka) |     +----------+     +----------+
                 +---------+
                      |
                 +----+----+
                 | Dead    |
                 | Letter  |
                 | Queue   |
                 +---------+
```

### CQRS Pattern

```
Commands (Write)                    Queries (Read)
+------------------+                +------------------+
|  Command Handler |                |  Query Handler   |
+--------+---------+                +--------+---------+
         |                                   |
+--------v---------+                +--------v---------+
|  Write Database  | --sync-->     |  Read Database   |
|  (Postgres)      |                |  (Elasticsearch) |
+------------------+                +------------------+
```

## Comprehensive Security Patterns

### OAuth 2.0 Implementation

```python
from api_security import OAuth2Provider, TokenValidator

# Configure OAuth 2.0 provider
provider = OAuth2Provider(
    issuer="https://auth.example.com",
    audience="https://api.example.com",
    jwks_uri="https://auth.example.com/.well-known/jwks.json",
    token_endpoint="https://auth.example.com/token",
    authorization_endpoint="https://auth.example.com/authorize",
)

# Validate JWT token
validator = TokenValidator(provider)
token = "eyJhbGciOiJSUzI1NiIs..."
result = validator.validate(token)
if result.valid:
    print(f"User: {result.claims['sub']}")
    print(f"Scopes: {result.claims['scope']}")
else:
    print(f"Invalid: {result.error}")
```

### JWT Token Validation

```python
class JWTValidator:
    def __init__(self, provider):
        self.provider = provider
        self.jwks_cache = {}
        self.jwks_cache_ttl = 300

    def validate(self, token):
        try:
            # Decode header to get key ID
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")

            # Get signing key
            key = self._get_signing_key(kid)

            # Validate token
            claims = jwt.decode(
                token,
                key,
                algorithms=["RS256", "ES256"],
                audience=self.provider.audience,
                issuer=self.provider.issuer,
            )

            # Check expiration
            if claims["exp"] < time.time():
                return ValidationResult(valid=False, error="Token expired")

            # Check not before
            if claims.get("nbf", 0) > time.time():
                return ValidationResult(valid=False, error="Token not yet valid")

            return ValidationResult(valid=True, claims=claims)

        except jwt.InvalidTokenError as e:
            return ValidationResult(valid=False, error=str(e))

    def _get_signing_key(self, kid):
        if kid in self.jwks_cache:
            return self.jwks_cache[kid]

        jwks = requests.get(self.provider.jwks_uri).json()
        for key in jwks["keys"]:
            if key["kid"] == kid:
                signing_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                self.jwks_cache[kid] = signing_key
                return signing_key

        raise KeyError(f"Key {kid} not found in JWKS")
```

### RBAC Implementation

```python
class RBACPolicy:
    def __init__(self):
        self.roles = {}
        self.assignments = {}
        self.resource_permissions = {}

    def add_role(self, role_name, permissions):
        self.roles[role_name] = permissions

    def add_assignment(self, user_id, role_name):
        if user_id not in self.assignments:
            self.assignments[user_id] = []
        self.assignments[user_id].append(role_name)

    def check(self, user_id, permission):
        if user_id not in self.assignments:
            return False

        for role in self.assignments[user_id]:
            if role in self.roles:
                if permission in self.roles[role] or "*" in self.roles[role]:
                    return True

        return False

    def check_resource(self, user_id, resource_type, resource_id, action):
        # Check global permission
        if self.check(user_id, f"{action}:{resource_type}"):
            return True

        # Check resource-level permission
        permission_key = f"{action}:{resource_type}:{resource_id}"
        if self.check(user_id, permission_key):
            return True

        # Check ownership
        if self._is_owner(user_id, resource_type, resource_id):
            return self.check(user_id, f"{action}:own")

        return False
```

### Rate Limiting Implementation

```python
import redis
import time

class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client

    def check_rate_limit(self, key, limit, window):
        now = time.time()
        window_start = now - window

        pipe = self.redis.pipeline()

        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)

        # Count current requests
        pipe.zcard(key)

        # Add current request
        pipe.zadd(key, {str(now): now})

        # Set expiry
        pipe.expire(key, window)

        results = pipe.execute()
        current_count = results[1]

        return {
            "allowed": current_count < limit,
            "limit": limit,
            "remaining": max(0, limit - current_count - 1),
            "reset_at": int(now + window),
        }

    def get_rate_limit_headers(self, result):
        return {
            "X-RateLimit-Limit": str(result["limit"]),
            "X-RateLimit-Remaining": str(result["remaining"]),
            "X-RateLimit-Reset": str(result["reset_at"]),
        }
```

### CORS Configuration

```python
class CORSMiddleware:
    def __init__(self, app, config):
        self.app = app
        self.config = config

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive)
        origin = request.headers.get("origin")

        # Check if origin is allowed
        if self._is_origin_allowed(origin):
            # Handle preflight
            if request.method == "OPTIONS":
                response = Response(status_code=204)
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Methods"] = ", ".join(
                    self.config["allowed_methods"]
                )
                response.headers["Access-Control-Allow-Headers"] = ", ".join(
                    self.config["allowed_headers"]
                )
                response.headers["Access-Control-Max-Age"] = str(
                    self.config["max_age"]
                )
                if self.config["allow_credentials"]:
                    response.headers["Access-Control-Allow-Credentials"] = "true"
                return await response(scope, receive, send)

            # Handle actual request
            response = await self.app(scope, receive, send)
            response.headers["Access-Control-Allow-Origin"] = origin
            if self.config["allow_credentials"]:
                response.headers["Access-Control-Allow-Credentials"] = "true"
            return await response(scope, receive, send)

        return await self.app(scope, receive, send)

    def _is_origin_allowed(self, origin):
        if not origin:
            return False
        if "*" in self.config["allowed_origins"]:
            return True
        return origin in self.config["allowed_origins"]
```

### Input Validation

```python
from pydantic import BaseModel, EmailStr, validator

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str
    age: int = None
    role: str = "user"

    @validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @validator("age")
    def age_must_be_valid(cls, v):
        if v is not None and (v < 0 or v > 150):
            raise ValueError("Age must be between 0 and 150")
        return v

    @validator("role")
    def role_must_be_valid(cls, v):
        allowed_roles = ["admin", "user", "viewer"]
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of: {allowed_roles}")
        return v
```

## OWASP API Security Top 10

### API1: Broken Object Level Authorization (BOLA)

```
Risk: Accessing other users' data by manipulating resource IDs
Example: GET /api/users/123 (attacker changes to /api/users/456)

Mitigation:
- Validate user owns the resource before returning it
- Use UUIDs instead of sequential IDs
- Implement resource-level permissions
```

### API2: Broken Authentication

```
Risk: Weak authentication allowing unauthorized access
Example: No rate limiting on login, weak password policy

Mitigation:
- Implement OAuth 2.0 with PKCE
- Enforce strong password policies
- Rate limit authentication endpoints
- Implement account lockout after failed attempts
```

### API3: Broken Object Property Level Authorization

```
Risk: Exposing sensitive fields or allowing mass assignment
Example: User can set role=admin via PUT /api/users/123

Mitigation:
- Use allowlists for updatable fields
- Validate all input against schema
- Return only necessary fields in responses
```

### API4: Unrestricted Resource Consumption

```
Risk: No rate limiting allows DoS attacks
Example: Sending thousands of requests per second

Mitigation:
- Implement rate limiting per user/endpoint
- Set request size limits
- Implement pagination limits
- Add timeout for expensive operations
```

### API5: Broken Function Level Authorization

```
Risk: Accessing admin functions without authorization
Example: Regular user accessing DELETE /api/admin/users

Mitigation:
- Implement RBAC with least privilege
- Validate permissions on every endpoint
- Don't rely on UI hiding admin functions
```

### API6: Unrestricted Access to Sensitive Business Flows

```
Risk: Automating business processes for abuse
Example: Bulk purchasing limited items

Mitigation:
- Implement rate limiting on sensitive flows
- Add CAPTCHA for high-value operations
- Monitor for unusual patterns
```

### API7: Server-Side Request Forgery (SSRF)

```
Risk: Making requests to internal services
Example: User provides internal URL as input

Mitigation:
- Validate and sanitize all URLs
- Use allowlists for external requests
- Block internal IP ranges
```

### API8: Security Misconfiguration

```
Risk: Default configurations exposing vulnerabilities
Example: Verbose error messages, debug mode enabled

Mitigation:
- Disable debug mode in production
- Remove unnecessary features
- Implement security headers
```

### API9: Improper Inventory Management

```
Risk: Old API versions with vulnerabilities still accessible
Example: /api/v1/users with known vulnerabilities

Mitigation:
- Track all API versions
- Deprecate and remove old versions
- Monitor usage of deprecated endpoints
```

### API10: Unsafe Consumption of APIs

```
Risk: Trusting third-party API responses
Example: Using external API data without validation

Mitigation:
- Validate all external API responses
- Implement timeout and retry logic
- Don't trust external data blindly
```

## Security Testing Tools

### Automated Security Scanner

```python
class APISecurityScanner:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token
        self.findings = []

    def scan(self):
        self._test_bola()
        self._test_authentication()
        self._test_rate_limiting()
        self._test_input_validation()
        self._test_cors()
        return self.findings

    def _test_bola(self):
        # Test accessing other users' resources
        response = requests.get(
            f"{self.base_url}/api/users/1",
            headers={"Authorization": f"Bearer {self.auth_token}"}
        )
        if response.status_code == 200:
            self.findings.append(Finding(
                severity="high",
                title="Potential BOLA vulnerability",
                description="Endpoint returns data without ownership check",
            ))

    def _test_rate_limiting(self):
        # Send multiple requests rapidly
        for i in range(100):
            response = requests.get(
                f"{self.base_url}/api/users",
                headers={"Authorization": f"Bearer {self.auth_token}"}
            )
            if response.status_code == 429:
                break
        else:
            self.findings.append(Finding(
                severity="medium",
                title="No rate limiting detected",
                description="Endpoint allows unlimited requests",
            ))
```

### Security Headers Check

```python
class SecurityHeadersChecker:
    REQUIRED_HEADERS = {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Content-Security-Policy": "default-src 'self'",
    }

    def check(self, url):
        response = requests.get(url)
        missing = []
        for header, expected in self.REQUIRED_HEADERS.items():
            actual = response.headers.get(header)
            if not actual:
                missing.append(header)
            elif expected and expected not in actual:
                missing.append(f"{header} (incorrect value)")
        return missing
```

## Security Monitoring

### Security Event Types

| Event Type | Severity | Description | Action |
|------------|----------|-------------|--------|
| authentication_failure | Medium | Failed login attempt | Log, alert after 5 failures |
| authorization_failure | Medium | Unauthorized access attempt | Log, alert immediately |
| rate_limit_exceeded | Low | Rate limit hit | Log, monitor pattern |
| suspicious_input | High | Potential injection attempt | Log, alert, block |
| token_expired | Low | Expired token used | Log, return 401 |
| token_revoked | Medium | Revoked token used | Log, alert immediately |
| admin_action | Info | Administrative action taken | Log, audit trail |

### Audit Log Schema

```json
{
  "timestamp": "2024-12-01T12:00:00Z",
  "event_type": "authentication_failure",
  "user_id": "user-123",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "endpoint": "/api/auth/login",
  "method": "POST",
  "status_code": 401,
  "request_id": "req_abc123",
  "details": {
    "reason": "invalid_password",
    "attempt_count": 3
  }
}
```
