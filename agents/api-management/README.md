# API Management Agent

> API lifecycle management — design, deploy, secure, and operate APIs at scale.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Configuration](#configuration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

---

## Overview

The API Management Agent provides end-to-end API lifecycle management including design with OpenAPI 3.0, developer portal, versioning with deprecation workflows, gateway configuration, security assessment, and usage analytics.

### What It Does

- **API Design**: Create APIs with OpenAPI 3.0 specification generation
- **Version Management**: Full lifecycle from draft to retirement with deprecation timelines
- **Developer Portal**: Register developers, generate API keys, track usage
- **Gateway Configuration**: Routing, rate limiting, circuit breaking, load balancing
- **Security Assessment**: Vulnerability scanning, auth configuration, compliance checks
- **Monitoring**: Real-time metrics, alerts, health checks
- **Monetization**: Pricing tiers, usage-based billing, overage handling

---

## Features

| Feature | Description |
|---------|-------------|
| API Design | OpenAPI 3.0 spec generation from endpoints |
| Versioning | Full lifecycle with deprecation and sunset |
| Developer Portal | Registration, API keys, usage tracking |
| Rate Limiting | Token bucket, sliding window, fixed window, leaky bucket |
| Gateway | Routing, SSL, CORS, WAF, circuit breaker |
| Security | Assessment, auth config, RBAC |
| Monitoring | Metrics, alerts, health checks |
| Monetization | Tiers (Free → Enterprise), pricing plans |
| Multi-Protocol | REST, GraphQL, gRPC, WebSocket |
| Compliance | Security scoring, vulnerability tracking, audit logging |

---

## Quick Start

```python
from agents.api_management.agent import APIManagementAgent

agent = APIManagementAgent()

# Design an API
api = agent.design_api("User API", base_path="/api/v1")

# Add endpoints
agent.add_endpoint(api.api_id, "/users", "GET", "List users")
agent.add_endpoint(api.api_id, "/users", "POST", "Create user")

# Generate OpenAPI spec
spec = agent.generate_openapi_spec(api.api_id)

# Security assessment
assessment = agent.assess_security(api.api_id)
print(f"Security Score: {assessment.security_score}")
```

### Run the Agent

```bash
python agents/api-management/agent.py --design "User API" /api/v1
python agents/api-management/agent.py --security api-xxxx
python agents/api-management/agent.py --status
```

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

### Optional Dependencies

```bash
pip install fastapi uvicorn pydantic redis prometheus-client pyyaml
```

---

## Usage

### Complete API Lifecycle

```python
from agents.api_management.agent import APIManagementAgent

agent = APIManagementAgent()

# 1. Design
api = agent.design_api("Payment API", description="Payment processing API")

# 2. Add endpoints
agent.add_endpoint(api.api_id, "/payments", "POST", "Create payment", auth_type="jwt")
agent.add_endpoint(api.api_id, "/payments/{id}", "GET", "Get payment", auth_type="jwt")
agent.add_endpoint(api.api_id, "/payments/{id}/refund", "POST", "Refund payment", auth_type="jwt")

# 3. Create version
agent.create_version(api.api_id, "v1")

# 4. Register developer
dev = agent.register_developer("Acme Corp", "dev@acme.com", tier="professional")
key, raw = agent.generate_api_key(dev.developer_id, "prod-key", rate_limit=5000)

# 5. Configure gateway
gw = agent.configure_gateway("Production", auth_type="jwt", rate_limit=10000)
agent.add_route(gw.gateway_id, "/api/v1", "http://payment.internal:8080")

# 6. Security assessment
assessment = agent.assess_security(api.api_id)
print(f"Score: {assessment.security_score}/100")

# 7. Set up monitoring
agent.set_up_monitoring(api.api_id, [
    {"name": "High Errors", "condition": "error_rate > 5%", "severity": "critical"},
    {"name": "Slow Responses", "condition": "p99_latency > 500ms", "severity": "warning"},
])

# 8. Export spec
agent.export_openapi(api.api_id, "./docs/openapi.json")
```

### Developer Portal Management

```python
# Register multiple developers with different tiers
developers = [
    ("Startup Inc", "dev@startup.io", "basic"),
    ("Enterprise Corp", "api@enterprise.com", "enterprise"),
    ("Consultant", "freelancer@dev.io", "professional"),
]

for name, email, tier in developers:
    dev = agent.register_developer(name, email, tier=tier)
    key, raw = agent.generate_api_key(dev.developer_id, "default", expires_days=365)
    print(f"{name}: {raw[:20]}...")

# Check usage for all developers
for dev in agent.list_developers():
    usage = agent.get_developer_usage(dev.developer_id)
    print(f"{dev.name}: {usage['total_requests']}/{usage['monthly_limit']} requests")
    if usage['total_requests'] / usage['monthly_limit'] > 0.8:
        print(f"  WARNING: {dev.name} approaching monthly limit")
```

### Version Deprecation Workflow

```python
# Create v2 with breaking changes
v2 = agent.create_version(
    api.api_id, "v2",
    changelog=["Added batch operations", "Improved error messages", "New pagination model"],
    breaking_changes=["Response envelope changed", "Auth header required", "Pagination required"]
)

# Deprecate v1 (90-day notice by default)
agent.deprecate_version(api.api_id, "v1")

# Get deprecation plan
plan = agent.plan_deprecation(api.api_id, "v1")
print(f"Deprecation: {plan['deprecation_date']}")
print(f"Sunset: {plan['sunset_date']}")
print(f"Affected endpoints: {plan['affected_endpoints']}")

# Monitor remaining v1 traffic
status = agent.get_version_status(api.api_id)
for v in status["versions"]:
    print(f"{v['version']}: {v['status']} ({v['usage_percent']:.1f}% traffic)")
```

### Security Assessment

```python
assessment = agent.assess_security(api.api_id)
print(f"Security Score: {assessment.security_score}/100")

# Categorize vulnerabilities
for vuln in assessment.vulnerabilities:
    severity = vuln['severity']
    if severity == 'critical':
        print(f"CRITICAL: {vuln['type']} — {vuln['recommendation']}")
    elif severity == 'high':
        print(f"HIGH: {vuln['type']} — {vuln['recommendation']}")

# Apply recommendations
for rec in assessment.recommendations:
    print(f"TODO: {rec}")
```

### Monitoring & Alerts

```python
# Set up comprehensive monitoring
alerts = agent.set_up_monitoring(api.api_id, [
    {"name": "High Error Rate", "condition": "error_rate > 5%", "severity": "critical"},
    {"name": "Slow Responses", "condition": "p99_latency > 500ms", "severity": "warning"},
    {"name": "Rate Limit Saturation", "condition": "rate_limit_usage > 90%", "severity": "warning"},
    {"name": "Auth Failures Spike", "condition": "auth_failure_rate > 10%", "severity": "critical"},
])

# Check health
health = agent.get_health_status(api.api_id)
print(f"Status: {health['status']}")
print(f"Uptime: {health['uptime_percent']}%")

# Get metrics
metrics = agent.get_api_metrics(api.api_id)
print(f"Requests: {metrics.total_requests}")
print(f"Error Rate: {metrics.error_rate}%")
print(f"p99 Latency: {metrics.latency_p99}ms")
```

---

## API Reference

### APIManagementAgent

| Method | Description |
|--------|-------------|
| `design_api(name, ...)` | Create API definition |
| `add_endpoint(api_id, path, method, summary)` | Add endpoint to API |
| `remove_endpoint(api_id, endpoint_id)` | Remove endpoint |
| `generate_openapi_spec(api_id)` | Generate OpenAPI 3.0 spec |
| `list_apis()` | List all APIs |
| `create_version(api_id, version, ...)` | Create new API version |
| `deprecate_version(api_id, version)` | Mark version as deprecated |
| `retire_version(api_id, version)` | Mark version as retired |
| `get_version_status(api_id)` | Version overview |
| `plan_deprecation(api_id, version)` | Deprecation timeline |
| `register_developer(name, email, ...)` | Register developer |
| `generate_api_key(developer_id, name, ...)` | Generate API key |
| `revoke_api_key(key_id)` | Revoke API key |
| `validate_api_key(raw_key)` | Validate API key |
| `list_developers(tier)` | List developers |
| `get_developer_usage(developer_id)` | Developer usage stats |
| `configure_gateway(name, ...)` | Configure gateway |
| `add_route(gateway_id, path, target)` | Add gateway route |
| `get_gateway_status(gateway_id)` | Gateway health |
| `assess_security(api_id)` | Security assessment |
| `configure_auth(api_id, ...)` | Configure authentication |
| `set_up_monitoring(api_id, alerts)` | Set up monitoring alerts |
| `get_api_metrics(api_id)` | Get usage metrics |
| `list_alerts(api_id)` | List monitoring alerts |
| `get_health_status(api_id)` | Health check |
| `export_openapi(api_id, output_path)` | Export OpenAPI spec |

### Enums

| Enum | Values |
|------|--------|
| `APIStatus` | DRAFT, DEVELOPMENT, TESTING, STAGING, ACTIVE, DEPRECATED, RETIRED |
| `APIProtocol` | REST, GRAPHQL, GRPC, WEBSOCKET, WEBHOOK |
| `HTTPMethod` | GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS |
| `AuthType` | NONE, API_KEY, BASIC, OAUTH2, JWT, MTLS |
| `RateLimitAlgorithm` | TOKEN_BUCKET, SLIDING_WINDOW, FIXED_WINDOW, LEAKY_BUCKET |
| `MonetizationTier` | FREE, BASIC, PROFESSIONAL, ENTERPRISE, CUSTOM |
| `LoadBalancerAlgorithm` | ROUND_ROBIN, LEAST_CONNECTIONS, IP_HASH, WEIGHTED, CONSISTENT_HASH |

---

## Examples

### REST API with Multiple Versions

```python
agent = APIManagementAgent()

# Design v1
api = agent.design_api("Catalog API", base_path="/api/v1")
agent.add_endpoint(api.api_id, "/products", "GET", "List products")
agent.add_endpoint(api.api_id, "/products/{id}", "GET", "Get product")
agent.add_endpoint(api.api_id, "/products/{id}/reviews", "GET", "Get reviews")
agent.create_version(api.api_id, "v1")

# Design v2 with breaking changes
v2 = agent.create_version(api.api_id, "v2", breaking_changes=["Pagination required"])
agent.add_endpoint(api.api_id, "/products", "GET", "List products (paginated)")
agent.add_endpoint(api.api_id, "/products/{id}", "GET", "Get product (enhanced)")
agent.add_endpoint(api.api_id, "/products/search", "GET", "Search products")

# Deprecate v1
agent.deprecate_version(api.api_id, "v1")

# View status
status = agent.get_version_status(api.api_id)
print(f"Current: {status['current_version']}")
for v in status["versions"]:
    print(f"  {v['version']}: {v['status']} ({v['endpoints_count']} endpoints)")
```

### GraphQL API

```python
api = agent.design_api("GraphQL API", protocol="graphql", base_path="/graphql")
agent.add_endpoint(api.api_id, "/graphql", "POST", "GraphQL endpoint", auth_type="jwt")
agent.add_endpoint(api.api_id, "/graphql", "GET", "GraphQL playground (dev only)")

# Generate spec
spec = agent.generate_openapi_spec(api.api_id)
```

### Enterprise Developer Portal

```python
# Register enterprise customer
enterprise_dev = agent.register_developer(
    name="MegaCorp Inc",
    email="api@megacorp.com",
    company="MegaCorp",
    tier="enterprise"
)

# Generate production key with high limits
prod_key, raw = agent.generate_api_key(
    enterprise_dev.developer_id,
    name="Production API Key",
    scopes=["read", "write", "admin"],
    rate_limit=50000,
    expires_days=365
)

# Generate sandbox key
sandbox_key, raw_sandbox = agent.generate_api_key(
    enterprise_dev.developer_id,
    name="Sandbox Key",
    scopes=["read"],
    rate_limit=1000,
    expires_days=90
)

# Track usage
usage = agent.get_developer_usage(enterprise_dev.developer_id)
print(f"Production: {usage['total_requests']}/{usage['monthly_limit']}")
```

### Gateway with Multiple Routes

```python
gw = agent.configure_gateway("Production Gateway", auth_type="jwt", rate_limit=50000)

# Versioned API routes
agent.add_route(gw.gateway_id, "/api/v1", "http://api-v1.internal:8080")
agent.add_route(gw.gateway_id, "/api/v2", "http://api-v2.internal:8080")

# Internal service routes
agent.add_route(gw.gateway_id, "/internal/metrics", "http://prometheus:9090", strip_prefix=True)
agent.add_route(gw.gateway_id, "/internal/logs", "http://elasticsearch:9200", strip_prefix=True)

# Health check
status = agent.get_gateway_status(gw.gateway_id)
print(f"Routes: {status['routes']}, Health: {status['health']}")
```

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

## Best Practices

1. **Always Version**: Never modify an API without creating a new version
2. **Deprecation Notice**: Give consumers at least 90 days before sunset
3. **Rate Limit Everything**: Set rate limits on every public endpoint
4. **Document Breaking Changes**: Every version upgrade needs a changelog
5. **Assess Security Regularly**: Run security assessments before each release
6. **Monitor Continuously**: Set up alerts for error rates and latency
7. **Rotate API Keys**: Encourage developers to rotate keys every 90 days
8. **Export Specs**: Keep OpenAPI specs in version control
9. **Use Tags**: Group endpoints by tags for organized documentation
10. **Define Schemas**: Always define request/response schemas for validation
11. **Idempotency Keys**: Require idempotency keys for write operations
12. **Pagination**: Use cursor-based pagination for large datasets

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| OpenAPI spec empty | No active version | Create a version first |
| Can't add endpoint | API not found | Verify `api_id` from `design_api()` |
| Developer auth fails | Key revoked/expired | Generate new API key |
| Gateway 502 | Backend unreachable | Check route target URL |
| Version deprecation fails | Version not active | Only active versions can be deprecated |
| Security score low | Missing auth on endpoints | Add auth to unprotected endpoints |
| Rate limit errors | Limits too restrictive | Adjust `RateLimitConfig` values |
| Monitoring alerts not firing | Condition syntax wrong | Verify condition format |
| Developer over limit | Monthly cap reached | Upgrade tier or increase limit |
| CORS errors | Origin not in allowlist | Add origin to CORS configuration |

---

## Advanced Usage

### Bulk API Import from OpenAPI Spec

```python
import yaml

with open("microservices-openapi.yaml") as f:
    spec = yaml.safe_load(f)

api = agent.design_api(spec["info"]["title"], description=spec["info"]["description"])

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

agent.create_version(api.api_id, "v1")
agent.export_openapi(api.api_id, "./imported-api.json")
```

### Multi-Version Traffic Shifting

```python
# Gradually shift traffic from v1 to v2
status = agent.get_version_status(api.api_id)
for v in status["versions"]:
    if v['version'] == 'v1' and v.get('usage_percent', 0) > 10:
        print(f"v1 still at {v['usage_percent']:.0f}% — continue migration")
    elif v['version'] == 'v2' and v.get('usage_percent', 0) < 90:
        print(f"v2 at {v['usage_percent']:.0f}% — monitor stability")
```

### Developer Onboarding Automation

```python
# Automated onboarding for new partners
partners = [
    {"name": "Partner A", "email": "api@partnerA.com", "tier": "professional"},
    {"name": "Partner B", "email": "dev@partnerB.com", "tier": "enterprise"},
]

for partner in partners:
    dev = agent.register_developer(partner["name"], partner["email"], tier=partner["tier"])
    key, raw = agent.generate_api_key(
        dev.developer_id,
        name="Production Key",
        scopes=["read", "write"],
        expires_days=365,
    )

    # Send onboarding email
    agent.send_notification(
        "email",
        partner["email"],
        f"Welcome to {api.name}",
        f"Your API key: {raw}\nDocumentation: https://docs.example.com",
    )
```

### Compliance Reporting

```python
# Generate compliance report
assessment = agent.assess_security(api.api_id)

report = {
    "api_name": api.name,
    "security_score": assessment.security_score,
    "vulnerabilities": len(assessment.vulnerabilities),
    "critical_findings": len([v for v in assessment.vulnerabilities if v['severity'] == 'critical']),
    "authenticated_endpoints": sum(1 for e in api.endpoints if e.auth_type != 'NONE'),
    "total_endpoints": len(api.endpoints),
    "rate_limited_endpoints": sum(1 for e in api.endpoints if e.rate_limit),
}
print(json.dumps(report, indent=2))
```

### Gateway Failover Configuration

```python
# Configure failover routes
gw = agent.configure_gateway("Failover Gateway", auth_type="jwt", rate_limit=10000)

# Primary route
agent.add_route(gw.gateway_id, "/api/v1", "http://primary-api:8080")

# Backup route (if primary fails)
agent.add_route(gw.gateway_id, "/api/v1", "http://backup-api:8080")
```

### Rate Limit Dashboard

```python
# Monitor rate limit usage across developers
for dev in agent.list_developers():
    usage = agent.get_developer_usage(dev.developer_id)
    if usage['total_requests'] / usage['monthly_limit'] > 0.8:
        print(f"ALERT: {dev.name} at {usage['total_requests']}/{usage['monthly_limit']}")
```

### API Version Sunset Automation

```python
# Automated sunset process
status = agent.get_version_status(api.api_id)
for v in status["versions"]:
    if v['status'] == 'DEPRECATED':
        plan = agent.plan_deprecation(api.api_id, v['version'])
        from datetime import datetime
        sunset = datetime.fromisoformat(plan['sunset_date'])
        if sunset < datetime.now():
            agent.retire_version(api.api_id, v['version'])
            print(f"Retired {v['version']} (past sunset date)")
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `API_NOT_FOUND` | 404 | API does not exist |
| `VERSION_NOT_FOUND` | 404 | Version does not exist |
| `ENDPOINT_NOT_FOUND` | 404 | Endpoint does not exist |
| `DEVELOPER_NOT_FOUND` | 404 | Developer does not exist |
| `KEY_REVOKED` | 401 | API key has been revoked |
| `KEY_EXPIRED` | 401 | API key has expired |
| `RATE_LIMITED` | 429 | Developer exceeded rate limit |
| `MONTHLY_LIMIT` | 429 | Developer exceeded monthly limit |
| `INVALID_SPEC` | 400 | OpenAPI spec validation failed |
| `VERSION_CONFLICT` | 409 | Version already exists |

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

---

## Files

- `agent.py` — Full implementation with all subsystems
- `ARCHITECTURE.md` — System architecture with ASCII diagrams
- `GROK.md` — Agent identity, capabilities, and usage patterns
- `README.md` — This file

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*API Management Agent v2.0 — Part of the Awesome Grok Skills collection.*
