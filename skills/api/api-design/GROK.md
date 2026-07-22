---
name: "api-design"
category: "api"
version: "2.0.0"
tags: ["api", "rest", "design", "openapi", "http", "api-design", "best-practices"]
---

# API Design

## Overview

Comprehensive API design framework for creating consistent, intuitive, and scalable REST, GraphQL, and gRPC APIs. This module covers resource modeling, URL design, HTTP method semantics, request/response formatting, error handling, pagination, filtering, sorting, HATEOAS, content negotiation, and API-first design workflows. Includes OpenAPI 3.1 specification generation, design system enforcement, and API review checklists for teams building public and internal APIs.

## Core Capabilities

- **Resource Modeling**: Define resources with consistent naming, nesting depth limits, and relationship patterns (REST), schema design (GraphQL), and service definitions (gRPC)
- **URL Design**: RESTful URL patterns with proper pluralization, versioning paths, query parameter conventions, and path parameter guidelines
- **HTTP Semantics**: Correct use of methods (GET, POST, PUT, PATCH, DELETE), status codes (2xx, 3xx, 4xx, 5xx), and headers (ETag, Cache-Control, Location)
- **Response Formatting**: JSON:API, HAL, Siren, and custom envelope formats with consistent field naming (camelCase vs snake_case) and ISO 8601 timestamps
- **Error Handling**: RFC 7807 Problem Details, structured error responses, error codes, and retryable vs non-retryable error classification
- **Pagination**: Cursor-based, offset-based, and keyset pagination with consistent link headers and response metadata
- **Filtering & Sorting**: Query parameter conventions for filtering (operators, ranges), sorting (multi-field, direction), and field selection (sparse fieldsets)
- **OpenAPI Generation**: Auto-generate OpenAPI 3.1 specifications from code annotations or design-first schemas

## Usage

```python
from api_design import APIBuilder, Resource, Endpoint, HTTPMethod, ErrorCode

# Design an API with resources
api = APIBuilder(
    title="User Management API",
    version="1.0.0",
    base_url="https://api.example.com/v1",
    style="json_api",
)

# Define resources
api.add_resource(Resource(
    name="User",
    path="/users",
    fields={"name": "string", "email": "string", "role": "enum[admin,user]", "created_at": "datetime"},
    relationships={"organization": "Organization", "teams": "Team[]"},
    searchable_fields=["name", "email", "role"],
    sortable_fields=["name", "created_at", "email"],
    filterable_fields={"role": ["admin", "user"], "status": ["active", "inactive"]},
))

api.add_resource(Resource(
    name="Organization",
    path="/organizations",
    fields={"name": "string", "plan": "enum[free,pro,enterprise]", "member_count": "integer"},
    relationships={"users": "User[]"},
))

# Generate endpoints
endpoints = api.generate_endpoints("User")
for ep in endpoints:
    print(f"  {ep.method.value:7s} {ep.path}")
    print(f"    Description: {ep.description}")
    if ep.query_params:
        print(f"    Query params: {ep.query_params}")
    print(f"    Response: {ep.response_schema}")
```

```python
# Generate OpenAPI spec
openapi = api.to_openapi()
print(f"\nOpenAPI version: {openapi['openapi']}")
print(f"Paths: {len(openapi.get('paths', {}))}")
print(f"Schemas: {len(openapi.get('components', {}).get('schemas', {}))}")

# Validate design
from api_design import DesignValidator
validator = DesignValidator()
issues = validator.validate(api)
for issue in issues:
    print(f"  [{issue.severity}] {issue.message}")
```

## Best Practices

- Design APIs resource-oriented, not action-oriented — use /users not /getUsers
- Always pluralize resource names (/users, not /user)
- Limit resource nesting to 3 levels maximum (/users/{id}/teams/{id}/projects is too deep)
- Use HTTP methods correctly: GET (safe), POST (create), PUT (replace), PATCH (update), DELETE (idempotent)
- Return 201 with Location header for successful resource creation
- Use 204 No Content for successful deletions with no response body
- Implement consistent pagination with next/prev/first/last links
- Use ETags for conditional requests and optimistic concurrency control
- Return RFC 7807 Problem Details for all error responses
- Document every endpoint with request/response examples in OpenAPI

## Related Modules

- **api-versioning** — Version management strategies for API evolution
- **api-security** — Authentication and authorization for API endpoints
- **api-documentation** — Interactive documentation generation
- **api-monitoring** — API usage analytics and performance monitoring
- **backend** → **fastapi-best-practices** — FastAPI implementation of design principles

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

## Comprehensive API Design Patterns

### Resource Design Patterns

```python
# Single Resource
class UserResource:
    path = "/users/{id}"
    fields = {
        "id": "uuid",
        "email": "string",
        "name": "string",
        "role": "enum[admin,user,viewer]",
        "status": "enum[active,inactive,suspended]",
        "created_at": "datetime",
        "updated_at": "datetime",
        "last_login_at": "datetime"
    }
    relationships = {
        "organization": "Organization",
        "teams": "Team[]",
        "permissions": "Permission[]"
    }
    searchable_fields = ["email", "name", "role"]
    sortable_fields = ["name", "created_at", "email", "last_login_at"]
    filterable_fields = {
        "role": ["admin", "user", "viewer"],
        "status": ["active", "inactive", "suspended"],
        "organization_id": "uuid"
    }

# Nested Resource
class TeamMemberResource:
    path = "/teams/{team_id}/members/{member_id}"
    parent = "Team"
    fields = {
        "id": "uuid",
        "user": "User",
        "role": "enum[owner,admin,member]",
        "joined_at": "datetime"
    }

# Collection Resource
class AuditLogResource:
    path = "/audit-logs"
    fields = {
        "id": "uuid",
        "actor_id": "uuid",
        "action": "string",
        "resource_type": "string",
        "resource_id": "uuid",
        "changes": "jsonb",
        "timestamp": "datetime"
    }
    filterable_fields = {
        "actor_id": "uuid",
        "resource_type": "string",
        "action": "string",
        "timestamp_range": "datetime_range"
    }
    sortable_fields = ["timestamp", "actor_id", "action"]
    default_sort = "-timestamp"
```

### URL Design Patterns

```
# Collection endpoints
GET    /users                    # List users
POST   /users                    # Create user

# Single resource endpoints
GET    /users/{id}               # Get user
PUT    /users/{id}               # Replace user
PATCH  /users/{id}               # Update user
DELETE /users/{id}               # Delete user

# Nested resources
GET    /users/{id}/teams         # List user's teams
POST   /users/{id}/teams         # Add user to team
DELETE /users/{id}/teams/{tid}   # Remove user from team

# Sub-resources
GET    /users/{id}/avatar        # Get user avatar
PUT    /users/{id}/avatar        # Upload user avatar
DELETE /users/{id}/avatar        # Delete user avatar

# Action endpoints (use POST for non-CRUD actions)
POST   /users/{id}/activate      # Activate user
POST   /users/{id}/deactivate    # Deactivate user
POST   /users/{id}/reset-password # Reset password

# Bulk operations
POST   /users/bulk               # Bulk create users
DELETE /users/bulk               # Bulk delete users
PATCH  /users/bulk               # Bulk update users

# Search endpoint
GET    /users/search?q=alice      # Full-text search
GET    /users?filter[role]=admin  # Filtered list
GET    /users?sort=-created_at    # Sorted list
```

### HTTP Method Semantics

```
GET     - Read resource(s), safe, idempotent, cacheable
POST    - Create resource, not safe, not idempotent
PUT     - Replace resource, not safe, idempotent
PATCH   - Partial update, not safe, not idempotent
DELETE  - Delete resource, not safe, idempotent
HEAD    - Same as GET but no body, safe, idempotent
OPTIONS - CORS preflight, safe, idempotent
```

### Status Code Usage

```
200 OK                    - Successful GET, PUT, PATCH
201 Created               - Successful POST (include Location header)
202 Accepted              - Async operation accepted
204 No Content            - Successful DELETE, no response body
301 Moved Permanently     - Resource permanently relocated
304 Not Modified          - Cached response is still valid
400 Bad Request           - Invalid request syntax or parameters
401 Unauthorized          - Authentication required or failed
403 Forbidden             - Authenticated but not authorized
404 Not Found             - Resource does not exist
405 Method Not Allowed    - HTTP method not supported on endpoint
409 Conflict              - Resource state conflict (e.g., duplicate)
410 Gone                  - Resource permanently removed
415 Unsupported Media     - Request body format not supported
422 Unprocessable         - Validation errors in request body
429 Too Many Requests     - Rate limit exceeded
500 Internal Server Error - Unexpected server error
502 Bad Gateway           - Upstream service error
503 Service Unavailable   - Service temporarily down
504 Gateway Timeout       - Upstream service timeout
```

## Error Handling Deep Dive

### RFC 7807 Problem Details

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request body contains invalid fields",
  "instance": "/users/123",
  "errors": [
    {
      "field": "email",
      "code": "INVALID_FORMAT",
      "message": "Must be a valid email address",
      "received": "not-an-email"
    },
    {
      "field": "age",
      "code": "OUT_OF_RANGE",
      "message": "Must be between 0 and 150",
      "received": -5
    }
  ]
}
```

### Error Response Envelope

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "error": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      }
    ]
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2024-12-01T12:00:00Z"
  }
}
```

### Error Classification

| Category | Codes | Retryable | Action |
|----------|-------|-----------|--------|
| Client Error (4xx) | 400, 401, 403, 404, 405, 409, 422 | No | Fix request |
| Rate Limited (429) | 429 | Yes (after delay) | Backoff and retry |
| Server Error (5xx) | 500, 502, 503, 504 | Sometimes | Retry with backoff |
| Transient | 408, 429, 502, 503, 504 | Yes | Retry with exponential backoff |

## Pagination Deep Dive

### Cursor-Based Pagination

```json
{
  "data": [...],
  "links": {
    "self": "/api/users?cursor=abc123&limit=20",
    "next": "/api/users?cursor=def456&limit=20",
    "prev": "/api/users?cursor=xyz789&limit=20",
    "first": "/api/users?limit=20",
    "last": "/api/users?cursor=end&limit=20"
  },
  "meta": {
    "total_count": 1234,
    "has_more": true,
    "limit": 20
  }
}
```

### Offset-Based Pagination

```json
{
  "data": [...],
  "links": {
    "self": "/api/users?page[offset]=0&page[limit]=20",
    "next": "/api/users?page[offset]=20&page[limit]=20",
    "prev": null,
    "first": "/api/users?page[offset]=0&page[limit]=20",
    "last": "/api/users?page[offset]=1220&page[limit]=20"
  },
  "meta": {
    "total_count": 1234,
    "page": {
      "offset": 0,
      "limit": 20,
      "total_pages": 62
    }
  }
}
```

## Filtering and Sorting

### Filter Operators

```
GET /api/users?filter[name]=Alice                      # Exact match
GET /api/users?filter[name][contains]=Ali              # Contains
GET /api/users?filter[name][starts_with]=A             # Starts with
GET /api/users?filter[age][gte]=18                     # Greater than or equal
GET /api/users?filter[age][lte]=65                     # Less than or equal
GET /api/users?filter[created_at][gte]=2024-01-01      # Date range start
GET /api/users?filter[created_at][lte]=2024-12-31      # Date range end
GET /api/users?filter[role][in]=admin,viewer            # Multiple values
GET /api/users?filter[status][ne]=deleted               # Not equal
GET /api/users?filter[is_active]=true                   # Boolean
GET /api/users?filter[team_id][is_null]=true            # Null check
```

### Sorting

```
GET /api/users?sort=name                  # Ascending
GET /api/users?sort=-name                 # Descending
GET /api/users?sort=-created_at,name      # Multi-field sort
```

### Sparse Fieldsets

```
GET /api/users?fields=User[id,name,email]         # Select fields
GET /api/users?fields=User[id,name],Team[name]    # Multi-resource fields
```

## Content Negotiation

### Accept Header

```
Accept: application/json                    # JSON
Accept: application/vnd.api.v2+json         # Versioned JSON
Accept: application/xml                     # XML
Accept: application/hal+json                # HAL format
Accept: application/vnd.api+json            # JSON:API
```

### Content-Type Header

```
Content-Type: application/json              # JSON body
Content-Type: multipart/form-data           # File upload
Content-Type: application/x-www-form-urlencoded  # Form data
```

## HATEOAS Implementation

```json
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "name": "Alice",
      "email": "alice@example.com"
    },
    "links": {
      "self": "/api/users/123",
      "edit": "/api/users/123",
      "avatar": "/api/users/123/avatar",
      "teams": "/api/users/123/teams"
    },
    "relationships": {
      "organization": {
        "links": {
          "self": "/api/users/123/relationships/organization",
          "related": "/api/users/123/organization"
        },
        "data": {
          "type": "organization",
          "id": "456"
        }
      }
    }
  }
}
```

## Rate Limiting Strategies

### Token Bucket

```
Bucket size: 10 tokens
Refill rate: 1 token/second
Request cost: 1 token

GET /api/users      - 1 token
POST /api/users     - 2 tokens
DELETE /api/users   - 3 tokens
```

### Sliding Window

```
Window: 60 seconds
Limit: 100 requests

Request at T+0:    Count = 1   - Allowed
Request at T+30:   Count = 2   - Allowed
...
Request at T+59:   Count = 100 - Allowed
Request at T+60:   Count = 101 - Denied (429)
```

### Response Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 73
X-RateLimit-Reset: 1704067200
Retry-After: 30
```

## Authentication Patterns

### OAuth 2.0 Flows

```
Authorization Code Flow (Web Apps):
  1. Client -> Auth Server: GET /authorize?response_type=code&client_id=...
  2. Auth Server -> User: Login page
  3. User -> Auth Server: Credentials
  4. Auth Server -> Client: GET /callback?code=abc
  5. Client -> Auth Server: POST /token (code=abc)
  6. Auth Server -> Client: access_token, refresh_token

Client Credentials Flow (Service-to-Service):
  1. Client -> Auth Server: POST /token (grant_type=client_credentials)
  2. Auth Server -> Client: access_token

PKCE Flow (Mobile/SPA):
  1. Client generates code_verifier, code_challenge
  2. Client -> Auth Server: GET /authorize?code_challenge=...
  3. Auth Server -> Client: authorization_code
  4. Client -> Auth Server: POST /token (code=..., code_verifier=...)
  5. Auth Server -> Client: access_token, refresh_token
```

### JWT Structure

```
Header: {"alg": "RS256", "typ": "JWT", "kid": "key-id-123"}
Payload: {
  "iss": "https://auth.example.com",
  "sub": "user-123",
  "aud": "https://api.example.com",
  "exp": 1704067200,
  "iat": 1704063600,
  "scope": "read:users write:users",
  "email": "alice@example.com",
  "roles": ["admin"]
}
Signature: RSASHA256(base64(header) + "." + base64(payload), private_key)
```

## Data Validation Patterns

### Request Validation Schema

```json
{
  "type": "object",
  "required": ["email", "name"],
  "properties": {
    "email": {
      "type": "string",
      "format": "email",
      "maxLength": 255
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "pattern": "^[a-zA-Z\\s-]+$"
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 150
    },
    "role": {
      "type": "string",
      "enum": ["admin", "user", "viewer"]
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"},
      "maxItems": 10
    }
  },
  "additionalProperties": false
}
```

### Response Validation Schema

```json
{
  "type": "object",
  "required": ["data", "meta"],
  "properties": {
    "data": {
      "oneOf": [
        {"type": "object"},
        {"type": "array"}
      ]
    },
    "meta": {
      "type": "object",
      "properties": {
        "total_count": {"type": "integer"},
        "page": {"type": "object"}
      }
    },
    "links": {
      "type": "object",
      "properties": {
        "self": {"type": "string", "format": "uri"},
        "next": {"type": "string", "format": "uri"},
        "prev": {"type": "string", "format": "uri"}
      }
    }
  }
}
```

## API Testing Strategies

### Unit Tests

```python
import pytest
from api_design import APIBuilder, Resource

def test_resource_creation():
    api = APIBuilder(title="Test API", version="1.0.0")
    api.add_resource(Resource(
        name="User",
        path="/users",
        fields={"name": "string", "email": "string"},
    ))
    assert api.get_resource("User") is not None

def test_url_generation():
    api = APIBuilder(title="Test API", version="1.0.0")
    api.add_resource(Resource(
        name="User",
        path="/users",
        fields={"id": "uuid", "name": "string"},
    ))
    endpoints = api.generate_endpoints("User")
    assert any(ep.path == "/users" and ep.method == "GET" for ep in endpoints)
    assert any(ep.path == "/users" and ep.method == "POST" for ep in endpoints)
```

### Integration Tests

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_users(client: AsyncClient):
    response = await client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "meta" in data
    assert isinstance(data["data"], list)

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/users", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert response.status_code == 201
    assert "Location" in response.headers
    data = response.json()
    assert data["data"]["name"] == "Alice"

@pytest.mark.asyncio
async def test_create_user_validation_error(client: AsyncClient):
    response = await client.post("/api/users", json={
        "name": "",
        "email": "not-an-email"
    })
    assert response.status_code == 422
    data = response.json()
    assert len(data["errors"]) > 0
```

### Load Tests

```python
import asyncio
import aiohttp

async def load_test():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(1000):
            tasks.append(session.get("http://localhost:3000/api/users"))
        responses = await asyncio.gather(*tasks)
        success = sum(1 for r in responses if r.status == 200)
        print(f"Success rate: {success/len(responses)*100:.2f}%")
```

## Migration Guide Patterns

### Breaking Change Migration

```markdown
## Migration Guide: v1.x to v2.0

### Authentication Changes
- **Before**: API key in `X-API-Key` header
- **After**: OAuth 2.0 Bearer token in `Authorization` header

### Endpoint Changes
- **Removed**: `GET /api/v1/users/search` (use `GET /api/v2/users?q=` instead)
- **Renamed**: `GET /api/v1/users/me` -> `GET /api/v2/users/self`
- **Added**: `PATCH /api/v2/users/{id}` (partial updates)

### Response Format Changes
- **Before**: Flat response with `results` array
- **After**: JSON:API format with `data`, `meta`, `links`

### Deprecation Timeline
- v1.x supported until 2025-06-01
- Sunset header added to all v1.x responses starting 2025-03-01
```

## Performance Benchmarks

| Operation | p50 Latency | p95 Latency | p99 Latency | Throughput |
|-----------|-------------|-------------|-------------|------------|
| GET (cached) | 1ms | 3ms | 8ms | 100,000 req/s |
| GET (uncached) | 15ms | 45ms | 120ms | 15,000 req/s |
| POST (create) | 30ms | 80ms | 200ms | 8,000 req/s |
| PUT (replace) | 25ms | 65ms | 180ms | 9,000 req/s |
| PATCH (update) | 20ms | 55ms | 150ms | 10,000 req/s |
| DELETE | 10ms | 30ms | 80ms | 20,000 req/s |
| Bulk POST (100) | 200ms | 500ms | 1,200ms | 500 req/s |

## Security Headers Configuration

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; script-src 'self'
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## CORS Configuration

```json
{
  "allowed_origins": ["https://app.example.com"],
  "allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
  "allowed_headers": ["Authorization", "Content-Type", "X-Request-ID"],
  "exposed_headers": ["X-Request-ID", "X-RateLimit-Limit"],
  "allow_credentials": true,
  "max_age": 86400,
  "preflight_continue": false
}
```

## Monitoring Metrics Reference

### Standard Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `http_requests_total` | Counter | method, path, status | Total requests |
| `http_request_duration_ms` | Histogram | method, path | Request latency |
| `http_request_size_bytes` | Histogram | method, path | Request body size |
| `http_response_size_bytes` | Histogram | method, path | Response body size |
| `http_active_requests` | Gauge | method, path | Current active requests |
| `http_errors_total` | Counter | method, path, status | Error count |
| `http_rate_limit_rejected_total` | Counter | path | Rate limited requests |
| `http_cache_hits_total` | Counter | path | Cache hit count |
| `http_cache_misses_total` | Counter | path | Cache miss count |
| `db_query_duration_ms` | Histogram | operation | Database query latency |
| `db_connections_active` | Gauge | -- | Active DB connections |
| `db_connections_idle` | Gauge | -- | Idle DB connections |

### Alert Rules

```yaml
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"

      - alert: HighLatency
        expr: histogram_quantile(0.99, http_request_duration_ms) > 500
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p99 latency detected"

      - alert: RateLimitSpike
        expr: rate(http_rate_limit_rejected_total[5m]) > 100
        for: 2m
        labels:
          severity: info
        annotations:
          summary: "Rate limit rejections spiking"
```
