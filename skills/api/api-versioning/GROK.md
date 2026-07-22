---
name: "api-versioning"
category: "api"
version: "2.0.0"
tags: ["api", "versioning", "backward-compatibility", "deprecation", "openapi", "migration"]
---

# API Versioning

## Overview

API versioning strategies and tooling for evolving APIs without breaking existing consumers. This module covers URL path versioning, header-based versioning, query parameter versioning, content negotiation (media type versioning), semantic versioning for APIs, deprecation workflows, backward/forward compatibility analysis, and automated migration tooling. Supports both REST and GraphQL APIs with version lifecycle management and consumer notification automation.

## Core Capabilities

- **Versioning Strategies**: URL path (/v1/users), query parameter (?version=2), custom header (X-API-Version), and media type (Accept: application/vnd.api.v2+json)
- **Semantic Versioning**: Major (breaking), minor (additive), and patch (fix) version management with automatic changelog generation
- **Compatibility Analysis**: Detect breaking changes between API versions (field removal, type changes, endpoint deletion, status code changes)
- **Deprecation Workflow**: Scheduled deprecation with sunset headers, migration guides, and consumer notification
- **Version Routing**: Route requests to the correct version handler with version negotiation and fallback
- **Schema Migration**: Generate migration scripts between OpenAPI schema versions
- **Consumer Tracking**: Monitor which API versions are in use and which consumers need migration
- **Dual-Version Support**: Run multiple API versions simultaneously with shared business logic

## Usage

```python
from api_versioning import (
    VersionManager, VersionStrategy, CompatibilityChecker, DeprecationPolicy
)

# Configure versioning
vm = VersionManager(
    current_version="2.0.0",
    strategy=VersionStrategy.URL_PATH,
    base_path="/api",
)

# Register versions
vm.register_version("1.0.0", status="deprecated", sunset_date="2025-06-01")
vm.register_version("1.1.0", status="deprecated", sunset_date="2025-06-01")
vm.register_version("2.0.0", status="current")
vm.register_version("2.1.0", status="beta")

# Check compatibility between versions
checker = CompatibilityChecker()
result = checker.check(
    old_schema="openapi_v1.json",
    new_schema="openapi_v2.json",
)
print(f"Breaking changes: {result.breaking_changes}")
print(f"Additive changes: {result.additive_changes}")
for change in result.changes:
    print(f"  [{change.severity}] {change.description}")
    if change.breaking:
        print(f"    Migration: {change.migration_guide}")

# Deprecation policy
policy = DeprecationPolicy(
    notice_period_days=90,
    require_sunset_header=True,
    notify_consumers=True,
    max_supported_versions=3,
)
deprecation = policy.create_deprecation(
    version="1.0.0",
    replacement="2.0.0",
    reason="Security improvements and new features",
)
print(f"\nDeprecation notice:")
print(f"  Sunset: {deprecation['sunset_date']}")
print(f"  Link: {deprecation['migration_url']}")
```

## Best Practices

- Use semantic versioning: increment major for breaking changes, minor for additions, patch for fixes
- Always support at least 2 major versions simultaneously during transition periods
- Use URL path versioning (/v1/, /v2/) for maximum visibility and ease of implementation
- Add Sunset and Deprecation headers to all responses for deprecated versions
- Provide migration guides with before/after examples for every breaking change
- Monitor API version usage to identify consumers still on old versions
- Use feature flags within versions to gradually roll out new behavior
- Never remove a field or endpoint in a minor version — deprecate first
- Support content negotiation for clients that cannot change URLs easily
- Automate compatibility checking in CI/CD to catch accidental breaking changes

## Related Modules

- **api-design** — Resource and endpoint design principles that versioning preserves
- **api-security** — Authentication changes that may require version coordination
- **api-documentation** — Version-specific documentation generation
- **api-monitoring** — Track version usage and migration progress
- **backend** → **fastapi-best-practices** — FastAPI versioning implementation patterns

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

## Comprehensive Versioning Patterns

### URL Path Versioning

```
GET /api/v1/users         # Version 1
GET /api/v2/users         # Version 2
GET /api/v2.1/users       # Minor version

# Implementation
class VersionRouter:
    def __init__(self):
        self.routers = {}
        self.fallback_version = None

    def add_version(self, version, router):
        self.routers[version] = router
        if not self.fallback_version:
            self.fallback_version = version

    def route(self, request):
        version = extract_version_from_path(request.path)
        if version in self.routers:
            return self.routers[version].route(request)
        return self.routers[self.fallback_version].route(request)
```

### Header-Based Versioning

```
# Request
GET /api/users
Accept: application/vnd.api.v2+json
X-API-Version: 2

# Implementation
class HeaderVersionRouter:
    def __init__(self):
        self.routers = {}
        self.default_version = "1"

    def route(self, request):
        version = request.headers.get("X-API-Version")
        if not version:
            accept = request.headers.get("Accept", "")
            version = extract_version_from_accept(accept)
        version = version or self.default_version
        return self.routers.get(version, self.routers[self.default_version]).route(request)
```

### Query Parameter Versioning

```
# Request
GET /api/users?version=2

# Implementation
class QueryVersionRouter:
    def __init__(self):
        self.routers = {}
        self.default_version = "1"

    def route(self, request):
        version = request.query.get("version", self.default_version)
        return self.routers.get(version, self.routers[self.default_version]).route(request)
```

## Compatibility Analysis Deep Dive

### Breaking Changes Detection

```python
class CompatibilityAnalyzer:
    BREAKING_CHANGES = {
        "endpoint_removed": "critical",
        "field_removed": "critical",
        "field_type_changed": "critical",
        "required_field_added": "critical",
        "status_code_changed": "high",
        "response_field_removed": "high",
        "parameter_became_required": "high",
        "enum_value_removed": "high",
        "default_value_changed": "medium",
        "response_field_added": "low",
        "new_endpoint_added": "none",
        "new_optional_param_added": "none",
        "new_enum_value_added": "none",
    }

    def analyze(self, old_spec, new_spec):
        changes = []
        for endpoint in old_spec["paths"]:
            if endpoint not in new_spec["paths"]:
                changes.append(Change(
                    type="endpoint_removed",
                    severity="critical",
                    endpoint=endpoint,
                    migration="Endpoint has been removed",
                ))
            else:
                changes.extend(self._compare_endpoint(
                    old_spec["paths"][endpoint],
                    new_spec["paths"][endpoint],
                    endpoint
                ))
        return changes

    def _compare_endpoint(self, old, new, path):
        changes = []
        for method in old:
            if method not in new:
                changes.append(Change(
                    type="endpoint_removed",
                    severity="critical",
                    endpoint=f"{method} {path}",
                ))
            else:
                changes.extend(self._compare_schemas(
                    old[method].get("responses", {}),
                    new[method].get("responses", {}),
                    f"{method} {path}"
                ))
        return changes
```

### Compatibility Matrix

| Change Type | v1 -> v2 | Minor | Patch | Notes |
|-------------|----------|-------|-------|-------|
| Add endpoint | Yes | Yes | Yes | Non-breaking |
| Remove endpoint | No | No | No | Always breaking |
| Add optional param | Yes | Yes | Yes | Non-breaking |
| Add required param | No | No | No | Breaking |
| Add response field | Yes | Yes | Yes | Non-breaking |
| Remove response field | No | No | No | Breaking |
| Change field type | No | No | No | Always breaking |
| Add enum value | Yes | Yes | Yes | Non-breaking |
| Remove enum value | No | No | No | Breaking |
| Change default value | Depends | No | No | Check consumers |
| Change status code | No | No | No | Breaking |
| Change error format | No | No | No | Breaking |

## Deprecation Workflows

### Sunset Header

```
Sunset: Sat, 01 Jun 2025 00:00:00 GMT
Deprecation: Sun, 01 Dec 2024 00:00:00 GMT
Link: <https://docs.example.com/migration/v1-to-v2>; rel="deprecation"
```

### Deprecation Timeline

```
2024-06-01: v2.0.0 released, v1.x marked as deprecated
2024-07-01: Sunset header added to all v1.x responses
2024-09-01: First migration reminder email sent to consumers
2024-11-01: Second migration reminder with usage stats
2025-01-01: Warning responses for v1.x with migration guidance
2025-03-01: Rate limiting tightened on v1.x endpoints
2025-06-01: v1.x sunset, all requests return 410 Gone
```

### Consumer Notification Script

```python
class DeprecationNotifier:
    def __init__(self, consumer_registry, notification_service):
        self.consumers = consumer_registry
        self.notifier = notification_service

    def notify_consumers(self, deprecated_version, replacement_version, sunset_date):
        consumers = self.consumers.get_by_version(deprecated_version)
        for consumer in consumers:
            self.notifier.send(
                to=consumer.contact_email,
                subject=f"API v{deprecated_version} Deprecation Notice",
                template="deprecation_notice",
                context={
                    "consumer_name": consumer.name,
                    "deprecated_version": deprecated_version,
                    "replacement_version": replacement_version,
                    "sunset_date": sunset_date,
                    "usage_stats": self._get_usage_stats(consumer, deprecated_version),
                    "migration_guide_url": f"https://docs.example.com/migration/{deprecated_version}-to-{replacement_version}",
                }
            )

    def _get_usage_stats(self, consumer, version):
        return {
            "total_requests_30d": self._count_requests(consumer, version, days=30),
            "endpoints_used": self._get_endpoints_used(consumer, version),
            "last_request_at": self._get_last_request(consumer, version),
        }
```

## Schema Migration Tools

### OpenAPI Diff Tool

```python
from api_versioning import OpenAPIDiffer

differ = OpenAPIDiffer()
diff = differ.diff("openapi_v1.json", "openapi_v2.json")

print(f"Breaking changes: {len(diff.breaking_changes)}")
print(f"Non-breaking changes: {len(diff.non_breaking_changes)}")

for change in diff.breaking_changes:
    print(f"  [{change.severity}] {change.type}: {change.description}")
    print(f"    Location: {change.path}")
    print(f"    Migration: {change.migration_guide}")
```

### Migration Script Generator

```python
from api_versioning import MigrationGenerator

generator = MigrationGenerator()
migration = generator.generate(
    old_version="1.0.0",
    new_version="2.0.0",
    old_spec="openapi_v1.json",
    new_spec="openapi_v2.json",
)

# Generate client migration script
client_script = migration.generate_client_migration(language="python")
with open("migrate_client.py", "w") as f:
    f.write(client_script)

# Generate server migration notes
server_notes = migration.generate_server_notes()
with open("MIGRATION.md", "w") as f:
    f.write(server_notes)
```

## Version Lifecycle Management

### Version States

```
Draft -> Beta -> Current -> Deprecated -> Sunset

Draft:    Internal testing, not public
Beta:     Public testing, may change
Current:  Stable, recommended for production
Deprecated: Still functional, migration recommended
Sunset:   Removed, returns 410 Gone
```

### Version State Machine

```python
class VersionStateMachine:
    VALID_TRANSITIONS = {
        "draft": ["beta", "cancelled"],
        "beta": ["current", "draft", "cancelled"],
        "current": ["deprecated"],
        "deprecated": ["sunset"],
        "sunset": [],
        "cancelled": [],
    }

    def transition(self, current_state, target_state):
        if target_state not in self.VALID_TRANSITIONS.get(current_state, []):
            raise InvalidTransition(
                f"Cannot transition from {current_state} to {target_state}"
            )
        return target_state
```

## Consumer Tracking

### Consumer Registry

```python
class ConsumerRegistry:
    def register(self, consumer):
        self.db.consumers.insert({
            "id": consumer.id,
            "name": consumer.name,
            "contact_email": consumer.email,
            "versions_used": [],
            "registered_at": datetime.utcnow(),
        })

    def track_usage(self, consumer_id, version, endpoint, timestamp):
        self.db.consumer_usage.insert({
            "consumer_id": consumer_id,
            "version": version,
            "endpoint": endpoint,
            "timestamp": timestamp,
        })

    def get_consumers_by_version(self, version):
        return self.db.consumers.find({
            "versions_used": version
        })

    def get_usage_stats(self, consumer_id, version):
        return self.db.consumer_usage.aggregate([
            {"$match": {"consumer_id": consumer_id, "version": version}},
            {"$group": {
                "_id": "$endpoint",
                "total_requests": {"$sum": 1},
                "last_used": {"$max": "$timestamp"},
            }}
        ])
```

## Dual-Version Support

### Shared Business Logic Pattern

```python
# Shared service layer
class UserService:
    def get_user(self, user_id):
        return self.db.users.find_by_id(user_id)

    def create_user(self, data):
        return self.db.users.create(data)

# Version-specific serializers
class UserSerializerV1:
    def serialize(self, user):
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }

class UserSerializerV2:
    def serialize(self, user):
        return {
            "id": user.id,
            "attributes": {
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "status": user.status,
            },
            "relationships": {
                "organization": {
                    "id": user.organization_id,
                }
            }
        }

# Version-specific handlers
class UserHandlerV1:
    def __init__(self, service, serializer):
        self.service = service
        self.serializer = serializer

    def get(self, user_id):
        user = self.service.get_user(user_id)
        return self.serializer.serialize(user)

class UserHandlerV2(UserHandlerV1):
    pass  # Uses V2 serializer
```

## API Versioning Metrics

### Metrics to Track

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `api_version_requests_total` | Counter | version, endpoint | Requests per version |
| `api_version_latency_ms` | Histogram | version, endpoint | Latency per version |
| `api_version_errors_total` | Counter | version, endpoint, status | Errors per version |
| `api_version_consumers` | Gauge | version | Active consumers per version |
| `api_deprecation_requests_total` | Counter | version | Requests to deprecated versions |

### Migration Progress Dashboard

```python
class MigrationDashboard:
    def get_migration_status(self):
        versions = self.version_manager.get_all_versions()
        return {
            "versions": [
                {
                    "version": v.version,
                    "status": v.status,
                    "sunset_date": v.sunset_date,
                    "active_consumers": self._get_consumer_count(v.version),
                    "requests_per_day": self._get_daily_requests(v.version),
                    "migration_percentage": self._get_migration_percentage(v.version),
                }
                for v in versions
            ],
            "total_consumers": self._get_total_consumers(),
            "consumers_migrated": self._get_migrated_consumers(),
            "days_until_sunset": self._get_days_until_sunset(),
        }
```

## API Versioning Best Practices Summary

### Do's

1. Use semantic versioning for all API versions
2. Support at least 2 major versions during transition
3. Add Sunset headers to all deprecated version responses
4. Provide migration guides with before/after examples
5. Monitor version usage to track migration progress
6. Automate compatibility checking in CI/CD
7. Use feature flags within versions for gradual rollout
8. Document all breaking changes in changelogs
9. Send deprecation notices to all affected consumers
10. Provide tooling to help consumers migrate

### Don'ts

1. Don't remove fields or endpoints in minor versions
2. Don't break backward compatibility without deprecation
3. Don't skip versions (v1 -> v3 without v2)
4. Don't use query parameter versioning for breaking changes
5. Don't deprecate versions without a clear sunset date
6. Don't forget to update SDKs for new versions
7. Don't assume consumers will migrate on their own
8. Don't ignore version-specific metrics
9. Don't mix versioning strategies (URL + header)
10. Don't forget to clean up old version code after sunset
