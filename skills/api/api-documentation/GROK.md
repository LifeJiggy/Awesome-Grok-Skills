---
name: "api-documentation"
category: "api"
version: "2.0.0"
tags: ["api", "documentation", "openapi", "swagger", "interactive-docs", "sdk-generation"]
---

# API Documentation

## Overview

Automated API documentation generation platform that produces interactive, always-current documentation from OpenAPI 3.1 specifications, code annotations, and schema definitions. This module supports Swagger UI, Redoc, Stoplight Elements, and custom documentation themes with interactive try-it-now functionality, SDK code generation in 10+ languages, changelog generation, and documentation-as-code workflows with CI/CD integration.

## Core Capabilities

- **OpenAPI Generation**: Auto-generate OpenAPI 3.1 specs from FastAPI, Flask, Express, Django, and Spring Boot annotations
- **Interactive Docs**: Deploy Swagger UI, Redoc, or Stoplight Elements with try-it-now functionality
- **SDK Generation**: Auto-generate client SDKs in Python, TypeScript, Go, Java, Ruby, C#, PHP, and more
- **Multi-Version Docs**: Side-by-side documentation for multiple API versions with version switcher
- **Changelog Generation**: Auto-generate changelogs from OpenAPI schema diffs between versions
- **Code Samples**: Auto-generate code examples in multiple languages for every endpoint
- **Documentation Testing**: Validate documentation accuracy against running API endpoints
- **Theme Customization**: Custom branding, color schemes, and layout for documentation portals

## Usage

```python
from api_documentation import (
    DocGenerator, DocFormat, CodeSampleGenerator, SDKGenerator
)

# Generate documentation from OpenAPI spec
generator = DocGenerator(
    title="User Management API",
    version="2.0.0",
    description="RESTful API for user and organization management",
    contact={"name": "API Team", "email": "api@example.com"},
)

# Add endpoints
generator.add_endpoint(
    method="GET", path="/users",
    summary="List all users",
    description="Returns a paginated list of users with optional filtering",
    parameters=[
        {"name": "page[size]", "in": "query", "schema": {"type": "integer", "default": 20}},
        {"name": "filter[role]", "in": "query", "schema": {"type": "string", "enum": ["admin", "user"]}},
    ],
    response_schema={
        "type": "object",
        "properties": {
            "data": {"type": "array", "items": {"$ref": "#/components/schemas/User"}},
            "meta": {"$ref": "#/components/schemas/Pagination"},
        },
    },
    examples={
        "success": {"value": {"data": [{"id": "123", "name": "Alice"}], "meta": {"total": 42}}},
    },
)

# Generate docs
html = generator.generate(format=DocFormat.HTML)
swagger_json = generator.generate(format=DocFormat.OPENAPI_JSON)
print(f"Generated: {len(html)} chars HTML")
print(f"OpenAPI spec: {len(swagger_json)} chars JSON")

# Generate code samples
samples = CodeSampleGenerator()
for lang in ["python", "javascript", "go", "curl"]:
    code = samples.generate(
        method="GET", url="https://api.example.com/users",
        headers={"Authorization": "Bearer <token>"},
        language=lang,
    )
    print(f"\n{lang.upper()}:")
    print(f"  {code[:80]}...")
```

## Best Practices

- Generate documentation from the same schema used for validation — single source of truth
- Include request and response examples for every endpoint
- Document all error codes and their meanings with troubleshooting guidance
- Use API references (OpenAPI) separate from guides and tutorials
- Version documentation alongside the API — never let docs drift from implementation
- Include authentication guides with step-by-step getting started instructions
- Test documentation examples against the live API in CI/CD
- Provide SDK generation for popular languages to reduce integration friction
- Include rate limit and pagination documentation prominently
- Add changelog and migration guides for every version release

## Related Modules

- **api-design** — Resource design that drives documentation structure
- **api-versioning** — Version management for multi-version documentation
- **api-security** — Security documentation for authentication and authorization
- **api-monitoring** — API usage data to identify documentation gaps
- **backend** → **fastapi-best-practices** — FastAPI auto-documentation integration

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

## Comprehensive Documentation Patterns

### OpenAPI 3.1 Specification

```yaml
openapi: "3.1.0"
info:
  title: User Management API
  version: "2.0.0"
  description: |
    RESTful API for user and organization management.
    Provides CRUD operations for users, teams, and organizations
    with support for pagination, filtering, and sorting.
  contact:
    name: API Team
    email: api@example.com
    url: https://docs.example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v2
    description: Production
  - url: https://staging-api.example.com/v2
    description: Staging

paths:
  /users:
    get:
      operationId: listUsers
      summary: List all users
      description: Returns a paginated list of users with optional filtering
      tags: [Users]
      parameters:
        - name: page[size]
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: page[after]
          in: query
          schema:
            type: string
        - name: filter[role]
          in: query
          schema:
            type: string
            enum: [admin, user, viewer]
        - name: sort
          in: query
          schema:
            type: string
            enum: [name, -name, created_at, -created_at]
      responses:
        "200":
          description: Successful response
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserListResponse"
              example:
                data:
                  - id: "123"
                    type: "user"
                    attributes:
                      name: "Alice"
                      email: "alice@example.com"
                meta:
                  total_count: 42
                links:
                  self: "/api/users?page[after]=abc"
                  next: "/api/users?page[after]=def"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "429":
          $ref: "#/components/responses/RateLimited"

    post:
      operationId: createUser
      summary: Create a new user
      description: Creates a new user with the provided attributes
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUserRequest"
            example:
              name: "Alice"
              email: "alice@example.com"
              role: "user"
      responses:
        "201":
          description: User created
          headers:
            Location:
              description: URL of created user
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserResponse"
        "400":
          $ref: "#/components/responses/BadRequest"
        "422":
          $ref: "#/components/responses/ValidationError"

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        type:
          type: string
          enum: [user]
        attributes:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
              format: email
            role:
              type: string
              enum: [admin, user, viewer]
            status:
              type: string
              enum: [active, inactive, suspended]
            created_at:
              type: string
              format: date-time
            updated_at:
              type: string
              format: date-time

    CreateUserRequest:
      type: object
      required: [name, email]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
        role:
          type: string
          enum: [admin, user, viewer]
          default: user

    UserListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: "#/components/schemas/User"
        meta:
          type: object
          properties:
            total_count:
              type: integer
        links:
          type: object
          properties:
            self:
              type: string
            next:
              type: string
            prev:
              type: string

    UserResponse:
      type: object
      properties:
        data:
          $ref: "#/components/schemas/User"

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"

    RateLimited:
      description: Rate limit exceeded
      headers:
        Retry-After:
          description: Seconds until rate limit resets
          schema:
            type: integer
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"

    Error:
      description: Error response
      content:
        application/json:
          schema:
            type: object
            properties:
              type:
                type: string
              title:
                type: string
              status:
                type: integer
              detail:
                type: string
```

### Documentation-as-Code Workflow

```yaml
# .github/workflows/docs.yml
name: Documentation
on:
  push:
    branches: [main]
    paths:
      - "openapi/**"
      - "docs/**"

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate OpenAPI spec
        run: |
          python scripts/generate_openapi.py \
            --input src/api/ \
            --output docs/openapi.json

      - name: Validate OpenAPI spec
        run: |
          npx @redocly/cli lint docs/openapi.json

      - name: Generate SDK
        run: |
          openapi-generator-cli generate \
            -i docs/openapi.json \
            -g python \
            -o sdk/python/

      - name: Deploy docs
        run: |
          npx @redocly/cli build-docs docs/openapi.json \
            --output docs/index.html
          netlify deploy --dir=docs/
```

## SDK Generation Patterns

### Python SDK

```python
# Generated SDK example
from user_api import Client, models

client = Client(base_url="https://api.example.com/v2", api_key="your-key")

# List users
users = client.users.list(
    page_size=20,
    filter_role="admin",
    sort="-created_at"
)
for user in users.data:
    print(f"{user.attributes.name}: {user.attributes.email}")

# Create user
new_user = client.users.create(
    name="Bob",
    email="bob@example.com",
    role="user"
)
print(f"Created: {new_user.data.id}")
```

### TypeScript SDK

```typescript
// Generated SDK example
import { UserApi, Configuration } from 'user-api-sdk';

const config = new Configuration({
  basePath: 'https://api.example.com/v2',
  apiKey: 'your-key',
});

const api = new UserApi(config);

// List users
const users = await api.listUsers({
  pageSize: 20,
  filterRole: 'admin',
  sort: '-created_at',
});

users.data.forEach(user => {
  console.log(`${user.attributes.name}: ${user.attributes.email}`);
});

// Create user
const newUser = await api.createUser({
  name: 'Bob',
  email: 'bob@example.com',
  role: 'user',
});
console.log(`Created: ${newUser.data.id}`);
```

## Changelog Generation

### Automated Changelog

```python
class ChangelogGenerator:
    def __init__(self, old_spec, new_spec):
        self.old_spec = old_spec
        self.new_spec = new_spec

    def generate(self):
        changes = []
        changes.extend(self._find_added_endpoints())
        changes.extend(self._find_removed_endpoints())
        changes.extend(self._find_modified_endpoints())
        return self._format_changelog(changes)

    def _find_added_endpoints(self):
        added = []
        for path in self.new_spec["paths"]:
            if path not in self.old_spec["paths"]:
                for method in self.new_spec["paths"][path]:
                    if method in ["get", "post", "put", "patch", "delete"]:
                        added.append(Change(
                            type="added",
                            path=path,
                            method=method.upper(),
                            description=self._get_summary(path, method),
                        ))
        return added

    def _format_changelog(self, changes):
        lines = ["# Changelog\n"]
        for change in sorted(changes, key=lambda c: (c.type, c.path)):
            emoji = {"added": " Added", "removed": " Removed", "modified": " Changed"}
            lines.append(f"- {emoji.get(change.type, '')} {change.method} {change.path}")
            if change.description:
                lines.append(f"  {change.description}")
        return "\n".join(lines)
```

## Documentation Testing

### Documentation Accuracy Test

```python
class DocAccuracyTester:
    def __init__(self, spec_path, base_url):
        self.spec = load_openapi_spec(spec_path)
        self.base_url = base_url

    def test_all_endpoints(self):
        results = []
        for path, methods in self.spec["paths"].items():
            for method, operation in methods.items():
                if method in ["get", "post", "put", "patch", "delete"]:
                    result = self._test_endpoint(path, method, operation)
                    results.append(result)
        return results

    def _test_endpoint(self, path, method, operation):
        # Test with example values
        request = self._build_request_from_example(path, method, operation)
        response = requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            json=request.body,
            headers=request.headers,
        )

        # Verify response matches documented schema
        schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
        is_valid = validate_response(response.json(), schema)

        return TestResult(
            endpoint=f"{method.upper()} {path}",
            status_code=response.status_code,
            matches_doc=is_valid,
            documented_status=list(operation["responses"].keys()),
        )
```

## Interactive Documentation Features

### Try-It-Now Configuration

```yaml
# Redocly config
theme:
  tryItOut:
    enabled: true
    hideHostname: false
    requestInterceptor:
      enabled: true
      includeCredentials: false
    proxyServer: "https://cors-proxy.example.com"
  api:
    showExtensions: true
    showSchemaExamples: true
    jsonSchemaExpandLevel: 3
    hideDownloadButton: false
    sortPropsAlphabetically: true
```

### Custom Theme

```yaml
theme:
  colors:
    primary:
      main: "#1a73e8"
    success:
      main: "#34a853"
    warning:
      main: "#fbbc04"
    error:
      main: "#ea4335"
  typography:
    fontSize: "15px"
    fontFamily: "Inter, sans-serif"
    headings:
      fontFamily: "Inter, sans-serif"
      fontWeight: 700
  sidebar:
    backgroundColor: "#f8f9fa"
    textColor: "#333"
    activeTextColor: "#1a73e8"
  rightPanel:
    backgroundColor: "#1e1e1e"
    textColor: "#d4d4d4"
```
