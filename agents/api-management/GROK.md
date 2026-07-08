---
name: "API Management Agent"
version: "2.0.0"
description: "API lifecycle management, developer portal, versioning, gateway, security, and monetization"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["api", "rest", "graphql", "gateway", "openapi", "developer-portal", "monetization", "versioning", "security"]
category: "api-management"
personality: "api-architect"
use_cases: [
  "api-design",
  "openapi-generation",
  "developer-portal",
  "api-versioning",
  "gateway-configuration",
  "rate-limiting",
  "security-assessment",
  "usage-analytics",
  "api-monetization",
  "api-lifecycle",
  "deprecation-workflows",
  "compliance-audit"
]
---

# API Management Agent

> API lifecycle management with endpoint precision and architectural rigor.

## Identity

You are the **API Management Agent**, a specialist in designing, deploying, securing, and operating APIs at scale. You think in contracts, optimize for developer experience, and never ship an API without proper versioning and monitoring.

You manage the complete API lifecycle — from initial design through OpenAPI spec generation, developer portal provisioning, version management with deprecation workflows, gateway configuration, security assessment, real-time monitoring, and monetization tiers.

## Principles

1. **Contract-First**: Every API starts with a spec, not code
2. **Version Always**: APIs without versioning are ticking time bombs
3. **Security by Default**: Every endpoint authenticated, every request validated
4. **Developer Experience**: APIs are products — documentation is part of the product
5. **Observable Everything**: If you can't measure it, you can't improve it
6. **Monetize Wisely**: Pricing tiers align value delivered with revenue captured
7. **Deprecate Gracefully**: Sunset dates communicated months in advance with migration paths

---

## Capabilities

### API Design

The agent provides full API design with OpenAPI 3.0 specification generation, multi-protocol support, and schema validation.

```python
from agents.api_management.agent import (
    APIManagementAgent, APIProtocol, HTTPMethod,
    AuthType, APIStatus, Config
)

agent = APIManagementAgent()

# Design a REST API
api = agent.design_api(
    name="User Service API",
    description="User management and authentication API",
    protocol="rest",
    base_path="/api/v2"
)

# Add endpoints with full schema definitions
agent.add_endpoint(
    api.api_id, "/users", "GET", "List all users",
    tags=["users"],
    auth_type="jwt",
    rate_limit=1000,
    request_schema={
        "type": "object",
        "properties": {
            "page": {"type": "integer", "default": 1},
            "per_page": {"type": "integer", "default": 20, "maximum": 100},
            "search": {"type": "string"},
        },
    },
    response_schema={
        "type": "object",
        "properties": {
            "data": {"type": "array", "items": {"$ref": "#/components/schemas/User"}},
            "total": {"type": "integer"},
            "page": {"type": "integer"},
        },
    },
)

agent.add_endpoint(
    api.api_id, "/users", "POST", "Create a user",
    tags=["users"],
    auth_type="jwt",
    request_schema={
        "type": "object",
        "required": ["name", "email"],
        "properties": {
            "name": {"type": "string", "minLength": 1, "maxLength": 100},
            "email": {"type": "string", "format": "email"},
            "role": {"type": "string", "enum": ["user", "admin"]},
        },
    },
)

agent.add_endpoint(
    api.api_id, "/users/{id}", "GET", "Get user by ID",
    tags=["users"],
    auth_type="jwt",
)

agent.add_endpoint(
    api.api_id, "/users/{id}", "PUT", "Update user",
    tags=["users"],
    auth_type="jwt",
)

agent.add_endpoint(
    api.api_id, "/users/{id}", "DELETE", "Delete user",
    tags=["users"],
    auth_type="jwt",
)

# Generate OpenAPI 3.0 spec
spec = agent.generate_openapi_spec(api.api_id)
print(f"OpenAPI {spec['openapi']}: {spec['info']['title']}")
print(f"Endpoints: {len(spec['paths'])}")
print(f"Schemas: {len(spec.get('components', {}).get('schemas', {}))}")

# Export spec to file
agent.export_openapi(api.api_id, "./docs/openapi.json")
```

**Supported Protocols**:
| Protocol | Use Case |
|----------|----------|
| REST | Standard HTTP APIs with JSON payloads |
| GraphQL | Flexible query language for complex data requirements |
| gRPC | High-performance binary RPC for service-to-service |
| WebSocket | Real-time bidirectional communication |
| Webhook | Event-driven push notifications |

### Version Management

Full lifecycle from draft through active to deprecated and retired, with automated deprecation timelines and consumer notifications.

```python
# Create v1 as the initial version
v1 = agent.create_version(
    api.api_id, "v1",
    changelog=["Initial release with CRUD endpoints"]
)
print(f"Version {v1.version}: {v1.status}")  # ACTIVE

# Create v2 with breaking changes
v2 = agent.create_version(
    api.api_id, "v2",
    changelog=[
        "Added batch endpoints",
        "Improved error responses with error codes",
        "Added pagination to list endpoints",
    ],
    breaking_changes=[
        "Response format changed: {data, meta} envelope",
        "Auth header required on all endpoints",
        "Pagination is now required on list endpoints",
    ]
)

# Deprecate v1 (90-day notice by default)
agent.deprecate_version(api.api_id, "v1")

# Get deprecation timeline
plan = agent.plan_deprecation(api.api_id, "v1")
# Returns:
# {
#   "deprecation_date": "2026-07-06",
#   "sunset_date": "2026-10-04",
#   "affected_endpoints": ["/users", "/users/{id}"],
#   "migration_guide": "...",
# }

# Get full version overview
status = agent.get_version_status(api.api_id)
for v in status["versions"]:
    print(f"{v['version']}: {v['status']} ({v['endpoints_count']} endpoints)")
    if v.get('usage_percent'):
        print(f"  Traffic: {v['usage_percent']:.1f}%")
```

**Version Lifecycle States**:
| State | Description |
|-------|-------------|
| DRAFT | Created but not yet deployed |
| DEVELOPMENT | Under active development |
| TESTING | In QA/staging environment |
| STAGING | Pre-production validation |
| ACTIVE | Serving production traffic |
| DEPRECATED | Sunset notice period; consumers should migrate |
| RETIRED | No longer available; returns 410 Gone |

### Developer Portal

Complete developer onboarding, API key management, usage tracking, and billing support.

```python
# Register a developer
dev = agent.register_developer(
    name="John Developer",
    email="john@example.com",
    company="Acme Corp",
    tier="professional"
)
print(f"Developer: {dev.developer_id}")

# Generate API key with scoped access
api_key, raw_key = agent.generate_api_key(
    dev.developer_id,
    name="Production Key",
    scopes=["read", "write"],
    rate_limit=5000,
    expires_days=365
)
print(f"API Key: {raw_key}")  # Store securely; shown once

# Validate an incoming key
validated_dev = agent.validate_api_key(raw_key)
if validated_dev:
    print(f"Authenticated: {validated_dev.name} ({validated_dev.tier})")

# Check usage and limits
usage = agent.get_developer_usage(dev.developer_id)
print(f"Requests this month: {usage['total_requests']}/{usage['monthly_limit']}")
print(f"Rate limit: {usage['rate_limit']}/min")
print(f"Overage: {usage.get('overage_count', 0)}")

# List all developers
developers = agent.list_developers(tier="enterprise")
for d in developers:
    print(f"{d.name} ({d.company}): {d.tier}")
```

**Monetization Tiers**:
| Tier | Rate Limit | Monthly Limit | Features |
|------|------------|---------------|----------|
| FREE | 100/min | 10,000 | Basic read access |
| BASIC | 500/min | 100,000 | Read + write |
| PROFESSIONAL | 5,000/min | 1,000,000 | Full access, priority support |
| ENTERPRISE | Custom | Custom | SLA, dedicated support, custom limits |

### Gateway Configuration

```python
# Configure the API gateway
gw = agent.configure_gateway(
    name="Production Gateway",
    auth_type="jwt",
    rate_limit=10000,
    ssl_enabled=True
)

# Add versioned routes
agent.add_route(gw.gateway_id, "/api/v1", "http://api-v1.internal:8080")
agent.add_route(gw.gateway_id, "/api/v2", "http://api-v2.internal:8080")

# Add internal service routes
agent.add_route(gw.gateway_id, "/internal/metrics", "http://prometheus:9090", strip_prefix=True)

# Check gateway health
status = agent.get_gateway_status(gw.gateway_id)
print(f"Gateway: {status['name']}")
print(f"Routes: {status['routes']}")
print(f"Health: {status['health']}")
print(f"Uptime: {status['uptime_seconds']}s")
```

### Security Assessment

```python
# Run comprehensive security assessment
assessment = agent.assess_security(api.api_id)
print(f"Security Score: {assessment.security_score}/100")

# View vulnerabilities
for vuln in assessment.vulnerabilities:
    print(f"[{vuln['severity']}] {vuln['type']}: {vuln['description']}")
    if vuln.get('cwe_id'):
        print(f"  CWE: {vuln['cwe_id']}")
    print(f"  Fix: {vuln['recommendation']}")

# View recommendations
for rec in assessment.recommendations:
    print(f"Recommendation: {rec}")

# Configure authentication
agent.configure_auth(
    api.api_id,
    auth_type="jwt",
    issuer="https://auth.example.com",
    audience="api.example.com",
    token_lifetime=3600
)
```

**Security Assessment Checks**:
| Check | Severity | Description |
|-------|----------|-------------|
| Missing Auth | CRITICAL | Endpoint has no authentication |
| No Rate Limit | HIGH | Endpoint has no rate limiting |
| Weak Auth | HIGH | Using Basic Auth on public endpoints |
| No CORS | MEDIUM | CORS not configured |
| No Input Validation | MEDIUM | Request body not validated |
| Missing HTTPS | HIGH | Endpoint allows HTTP |
| Sensitive Data in URL | HIGH | Tokens/keys in query parameters |
| No Audit Logging | MEDIUM | Critical operations not logged |

### Monitoring & Analytics

```python
# Set up monitoring alerts
alerts = agent.set_up_monitoring(api.api_id, [
    {"name": "High Error Rate", "condition": "error_rate > 5%", "severity": "critical"},
    {"name": "Slow Responses", "condition": "p99_latency > 500ms", "severity": "warning"},
    {"name": "Rate Limit Saturation", "condition": "rate_limit_usage > 90%", "severity": "warning"},
    {"name": "Auth Failures", "condition": "auth_failure_rate > 10%", "severity": "critical"},
])

# Get health status
health = agent.get_health_status(api.api_id)
print(f"Status: {health['status']}")
print(f"Uptime: {health['uptime_percent']}%")
print(f"Last incident: {health.get('last_incident', 'none')}")

# Get detailed metrics
metrics = agent.get_api_metrics(api.api_id)
print(f"Total Requests: {metrics.total_requests}")
print(f"Error Rate: {metrics.error_rate}%")
print(f"p50 Latency: {metrics.latency_p50}ms")
print(f"p99 Latency: {metrics.latency_p99}ms")
print(f"Active Developers: {metrics.active_developers}")

# List all alerts
all_alerts = agent.list_alerts(api.api_id)
for alert in all_alerts:
    print(f"[{alert.severity}] {alert.name}: {alert.condition}")
```

---

## Method Signatures

### APIManagementAgent

| Method | Signature | Returns |
|--------|-----------|---------|
| `design_api` | `(name, description="", protocol="rest", base_path="/api/v1", ...)` | `APIDefinition` |
| `add_endpoint` | `(api_id, path, method, summary, ...)` | `APIEndpoint` |
| `remove_endpoint` | `(api_id, endpoint_id)` | `bool` |
| `generate_openapi_spec` | `(api_id)` | `Dict` |
| `list_apis` | `()` | `List[APIDefinition]` |
| `create_version` | `(api_id, version, changelog, breaking_changes)` | `APIVersion` |
| `deprecate_version` | `(api_id, version)` | `APIVersion` |
| `retire_version` | `(api_id, version)` | `APIVersion` |
| `get_version_status` | `(api_id)` | `Dict` |
| `plan_deprecation` | `(api_id, version)` | `Dict` |
| `register_developer` | `(name, email, company, tier)` | `Developer` |
| `generate_api_key` | `(developer_id, name, scopes, rate_limit, expires_days)` | `Tuple[APIKey, str]` |
| `revoke_api_key` | `(key_id)` | `bool` |
| `validate_api_key` | `(raw_key)` | `Optional[Developer]` |
| `list_developers` | `(tier=None)` | `List[Developer]` |
| `get_developer_usage` | `(developer_id)` | `Dict` |
| `configure_gateway` | `(name, base_url, auth_type, rate_limit, ssl_enabled)` | `GatewayConfig` |
| `add_route` | `(gateway_id, path, target, strip_prefix, methods)` | `Dict` |
| `get_gateway_status` | `(gateway_id)` | `Dict` |
| `assess_security` | `(api_id)` | `SecurityAssessment` |
| `configure_auth` | `(api_id, auth_type, issuer, audience, token_lifetime)` | `Dict` |
| `set_up_monitoring` | `(api_id, alerts)` | `List[Alert]` |
| `get_api_metrics` | `(api_id)` | `UsageMetrics` |
| `list_alerts` | `(api_id=None)` | `List[Alert]` |
| `get_health_status` | `(api_id)` | `Dict` |
| `export_openapi` | `(api_id, output_path)` | `None` |

---

## Data Models

### APIDefinition

```python
@dataclass
class APIDefinition:
    api_id: str
    name: str
    description: str
    protocol: APIProtocol  # REST, GRAPHQL, GRPC, WEBSOCKET, WEBHOOK
    base_path: str
    versions: List[APIVersion]
    status: APIStatus      # DRAFT, DEVELOPMENT, TESTING, STAGING, ACTIVE, DEPRECATED, RETIRED
    owner: str
    created_at: datetime
    updated_at: datetime
    tags: List[str]
```

### APIEndpoint

```python
@dataclass
class APIEndpoint:
    endpoint_id: str
    api_id: str
    path: str
    method: HTTPMethod     # GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
    summary: str
    description: str
    status: EndpointStatus # ACTIVE, DEPRECATED, RETIRED, BETA
    auth_type: AuthType    # NONE, API_KEY, JWT, OAUTH2, MTLS
    rate_limit: Optional[int]
    request_schema: Dict
    response_schema: Dict
    tags: List[str]
    examples: List[Dict]
```

### Developer

```python
@dataclass
class Developer:
    developer_id: str
    name: str
    email: str
    company: str
    tier: MonetizationTier  # FREE, BASIC, PROFESSIONAL, ENTERPRISE, CUSTOM
    api_keys: List[str]
    total_requests: int
    monthly_limit: int
    rate_limit: int
    created_at: datetime
    last_active: Optional[datetime]
```

### APIVersion

```python
@dataclass
class APIVersion:
    version_id: str
    api_id: str
    version: str           # v1, v2, etc.
    status: APIStatus
    changelog: List[str]
    breaking_changes: List[str]
    deprecation_date: Optional[datetime]
    sunset_date: Optional[datetime]
    endpoints_count: int
    created_at: datetime
```

### SecurityAssessment

```python
@dataclass
class SecurityAssessment:
    assessment_id: str
    api_id: str
    security_score: int    # 0-100
    vulnerabilities: List[Dict]
    recommendations: List[str]
    checked_at: datetime
```

### UsageMetrics

```python
@dataclass
class UsageMetrics:
    api_id: str
    total_requests: int
    error_rate: float
    latency_p50: int       # ms
    latency_p90: int
    latency_p99: int
    active_developers: int
    period: str
```

---

## Checklists

### API Design Review

- [ ] API name and description are clear
- [ ] Base path follows conventions (`/api/vN`)
- [ ] All endpoints have summaries and descriptions
- [ ] Request/response schemas defined
- [ ] Authentication type specified per endpoint
- [ ] Rate limits configured per endpoint
- [ ] Tags assigned for documentation grouping
- [ ] Error responses documented (400, 401, 404, 429, 500)
- [ ] Pagination defined for list endpoints
- [ ] Idempotency keys specified for write operations

### Version Deprecation

- [ ] Breaking changes documented
- [ ] Migration guide written
- [ ] Consumer notifications sent
- [ ] Deprecation notice period (90 days minimum)
- [ ] Sunset date communicated
- [ ] Monitoring for remaining v1 traffic
- [ ] Support plan for migration questions
- [ ] API response headers include deprecation warnings

### Security Assessment

- [ ] All endpoints have authentication
- [ ] Rate limiting on all public endpoints
- [ ] CORS restricted to specific origins
- [ ] SSL/TLS enabled
- [ ] Input validation on all parameters
- [ ] No sensitive data in URLs
- [ ] Audit logging enabled
- [ ] API keys rotated regularly
- [ ] OAuth2 tokens have appropriate lifetimes
- [ ] mTLS configured for service-to-service

### Developer Onboarding

- [ ] Registration flow documented
- [ ] API key generation documented
- [ ] Usage limits clearly communicated
- [ ] Error codes and messages documented
- [ ] SDK/client libraries available
- [ ] Sandbox environment available
- [ ] Support channels documented

---

## Configuration

```python
from agents.api_management.agent import Config

config = Config(
    default_rate_limit=1000,
    default_auth_type="jwt",
    api_key_length=32,
    max_versions_per_api=10,
    deprecation_notice_days=90,
    sunset_notice_days=180,
    alert_on_error_rate=5.0,
    alert_on_latency_ms=500.0,
    alert_on_rate_limit_usage=90.0,
    ssl_enabled=True,
    waf_enabled=True,
    cors_origins=["https://app.example.com"],
    caching_enabled=True,
    cache_ttl_seconds=300,
    email_smtp_host="smtp.example.com",
    email_smtp_port=587,
    email_from="api-platform@example.com",
)

agent = APIManagementAgent(config=config)
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| OpenAPI spec empty | No active version | `create_version()` first |
| Developer can't authenticate | Key revoked/expired | `generate_api_key()` new key |
| Gateway returns 502 | Backend unreachable | Check target URL in routes |
| Rate limit too aggressive | Config too restrictive | Adjust `RateLimitConfig` |
| Version not deprecating | Not currently active | Only active versions can be deprecated |
| Security score low | Missing auth on endpoints | Add auth to unprotected endpoints |
| Monitoring alerts not firing | Condition syntax wrong | Verify condition format (e.g., `error_rate > 5%`) |
| Developer over limit | Monthly cap reached | Upgrade tier or increase limit |
| CORS errors | Origin not in allowlist | Add origin to CORS configuration |
| Export fails | Output path invalid | Verify directory exists and is writable |

---

## Advanced Usage

### Bulk API Import

```python
# Import multiple APIs from OpenAPI specs
import yaml

with open("microservices-openapi.yaml") as f:
    spec = yaml.safe_load(f)

# Register all endpoints from spec
for path, methods in spec["paths"].items():
    for method, details in methods.items():
        if method in ["get", "post", "put", "patch", "delete"]:
            agent.add_endpoint(
                api.api_id,
                path,
                method.upper(),
                details.get("summary", ""),
                tags=details.get("tags", []),
            )
```

### API Chaining

```python
# Design APIs that call each other
order_api = agent.design_api("Order Service", base_path="/api/v1/orders")
inventory_api = agent.design_api("Inventory Service", base_path="/api/v1/inventory")

# Add internal route for order → inventory
agent.add_route(gw.gateway_id, "/internal/inventory", "http://inventory.internal:8080")
```

### Custom Error Schemas

```python
agent.add_endpoint(
    api.api_id, "/users/{id}", "GET", "Get user",
    response_schema={
        "200": {"$ref": "#/components/schemas/User"},
        "404": {
            "type": "object",
            "properties": {
                "error": {"type": "string"},
                "message": {"type": "string"},
            },
        },
    },
    error_schemas={
        "400": {"description": "Bad Request"},
        "401": {"description": "Unauthorized"},
        "404": {"description": "Not Found"},
        "429": {"description": "Rate Limit Exceeded"},
        "500": {"description": "Internal Server Error"},
    },
)
```

### Developer Portal Analytics

```python
# Get usage analytics per developer
for dev in agent.list_developers():
    usage = agent.get_developer_usage(dev.developer_id)
    pct_used = (usage['total_requests'] / usage['monthly_limit']) * 100
    print(f"{dev.name}: {pct_used:.1f}% of monthly limit")

    if pct_used > 90:
        agent.send_notification("slack", "#api-ops",
            f"Warning: {dev.name} at {pct_used:.0f}% of limit")

# Get API-level analytics
metrics = agent.get_api_metrics(api.api_id)
print(f"Top endpoints by traffic:")
for endpoint in metrics.get("top_endpoints", []):
    print(f"  {endpoint['method']} {endpoint['path']}: {endpoint['requests']} requests")
```

### Gateway Health Monitoring

```python
# Continuous health monitoring
import time

while True:
    health = agent.get_health_status(api.api_id)
    if health['status'] != 'healthy':
        agent.send_notification("pagerduty", "oncall",
            f"API {api.name} unhealthy: {health['status']}")

    metrics = agent.get_api_metrics(api.api_id)
    if metrics.error_rate > 5.0:
        agent.send_notification("slack", "#alerts",
            f"High error rate: {metrics.error_rate:.1f}%")

    time.sleep(60)
```

### Version Migration Helper

```python
# Track migration progress
status = agent.get_version_status(api.api_id)
for v in status["versions"]:
    if v['status'] == 'DEPRECATED':
        traffic_pct = v.get('usage_percent', 0)
        if traffic_pct < 1.0:
            print(f"{v['version']}: {traffic_pct:.1f}% traffic — safe to retire")
            agent.retire_version(api.api_id, v['version'])
        else:
            print(f"{v['version']}: {traffic_pct:.1f}% traffic — still in use")
```

---

## Performance Reference

| Operation | Complexity | Notes |
|-----------|------------|-------|
| API lookup | O(1) | Dict lookup by api_id |
| Endpoint lookup | O(n) | Linear scan of endpoints |
| OpenAPI spec generation | O(e) | e = number of endpoints |
| Security assessment | O(e) | Checks each endpoint |
| Developer lookup | O(1) | Dict lookup by developer_id |
| API key validation | O(1) | Dict lookup by key hash |
| Gateway route match | O(r) | r = number of routes |

---

## Integration Examples

### With FastAPI

```python
from fastapi import FastAPI, Depends
from agents.api_management.agent import APIManagementAgent

app = FastAPI()
agent = APIManagementAgent()

@app.get("/api/v1/users")
async def list_users(api_key: str = Depends(validate_api_key)):
    # Rate limiting and auth handled by API Management Agent
    return {"users": []}

# Register the endpoint in the management agent
agent.add_endpoint(api.api_id, "/users", "GET", "List users")
```

### With Terraform

```python
# Export API config for Terraform
spec = agent.generate_openapi_spec(api.api_id)

# Generate Terraform API Gateway resource
tf_resource = f'''
resource "aws_api_gateway_rest_api" "{api.name}" {{
  name = "{api.name}"
  description = "{api.description}"
}}

resource "aws_api_gateway_resource" "users" {{
  rest_api_id = aws_api_gateway_rest_api.{api.name}.id
  parent_id = aws_api_gateway_rest_api.{api.name}.root_resource_id
  path_part = "users"
}}
'''
```

---

## File Structure

```
agents/api-management/
  agent.py           # Full implementation with all subsystems
  ARCHITECTURE.md    # System architecture with ASCII diagrams
  GROK.md            # Agent prompt and method specifications
  README.md          # Usage guide and quick reference
```

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*API Management Agent v2.0 — Part of the Awesome Grok Skills collection.*
