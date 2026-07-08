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
- **Version Management**: Lifecycle from draft to retirement with deprecation timelines
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
])

# 8. Export spec
agent.export_openapi(api.api_id, "./docs/openapi.json")
```

### Developer Portal Management

```python
# Register multiple developers
for name, email, tier in [
    ("Startup Inc", "dev@startup.io", "basic"),
    ("Enterprise Corp", "api@enterprise.com", "enterprise"),
]:
    dev = agent.register_developer(name, email, tier=tier)
    key, raw = agent.generate_api_key(dev.developer_id, "default", expires_days=365)
    print(f"{name}: {raw[:20]}...")

# Check usage
for dev in agent.list_developers():
    usage = agent.get_developer_usage(dev.developer_id)
    print(f"{dev.name}: {usage['total_requests']}/{usage['monthly_limit']}")
```

### Version Deprecation Workflow

```python
# Create v2 with breaking changes
v2 = agent.create_version(
    api.api_id, "v2",
    changelog=["Added batch operations", "Improved error messages"],
    breaking_changes=["Response envelope changed", "Auth header required"]
)

# Deprecate v1 (90-day notice)
agent.deprecate_version(api.api_id, "v1")

# Get deprecation plan
plan = agent.plan_deprecation(api.api_id, "v1")
print(f"Deprecation: {plan['deprecation_date']}")
print(f"Sunset: {plan['sunset_date']}")
print(f"Affected endpoints: {plan['affected_endpoints']}")

# Monitor remaining v1 traffic
status = agent.get_version_status(api.api_id)
for v in status["versions"]:
    print(f"{v['version']}: {v['status']} ({v['usage_percent']}% traffic)")
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
agent.create_version(api.api_id, "v1")

# Design v2 with breaking changes
v2 = agent.create_version(api.api_id, "v2", breaking_changes=["Pagination required"])
agent.add_endpoint(api.api_id, "/products", "GET", "List products (paginated)")

# Deprecate v1
agent.deprecate_version(api.api_id, "v1")

# View status
status = agent.get_version_status(api.api_id)
print(f"Current: {status['current_version']}")
for v in status["versions"]:
    print(f"  {v['version']}: {v['status']}")
```

### GraphQL API

```python
api = agent.design_api("GraphQL API", protocol="graphql", base_path="/graphql")
agent.add_endpoint(api.api_id, "/graphql", "POST", "GraphQL endpoint")
```

---

## Configuration

```python
from agent import Config

config = Config(
    default_rate_limit=1000,
    default_auth_type="jwt",
    api_key_length=32,
    max_versions_per_api=10,
    deprecation_notice_days=90,
    sunset_notice_days=180,
    alert_on_error_rate=5.0,
    alert_on_latency_ms=500.0,
    ssl_enabled=True,
    waf_enabled=True,
    cors_origins=["https://app.example.com"],
    caching_enabled=True,
    cache_ttl_seconds=300,
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
