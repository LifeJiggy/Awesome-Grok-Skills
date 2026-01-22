# API Gateway Agent

## Overview

The **API Gateway Agent** provides comprehensive API management capabilities including rate limiting, authentication, analytics, routing, and transformation. This agent enables secure, scalable, and monitored API access.

## Core Capabilities

### 1. Rate Limiting
Control API usage:
- **Request Throttling**: Limit requests per time unit
- **Tiered Limits**: Different limits per plan
- **Quota Management**: Monthly/daily limits
- **Distributed Rate Limiting**: Cluster-aware
- **Retry-After Headers**: RFC compliance

### 2. Authentication Management
Secure API access:
- **API Keys**: Simple authentication
- **OAuth 2.0**: Authorization framework
- **JWT Tokens**: Stateless authentication
- **mTLS**: Mutual TLS for services
- **IP Whitelisting**: Access restrictions

### 3. API Analytics
Monitor API usage:
- **Request Metrics**: Volume, throughput
- **Performance Metrics**: Latency, response time
- **Error Tracking**: Status codes, failures
- **Usage Patterns**: Time-based analysis
- **Anomaly Detection**: Unusual patterns

### 4. API Routing
Manage traffic flow:
- **Path Routing**: Route by URL path
- **Header Routing**: Route by headers
- **Method Routing**: Different handlers per method
- **Canary Deployments**: Gradual rollouts
- **A/B Testing**: Traffic splitting

### 5. Response Transformation
Modify API responses:
- **Field Mapping**: Rename fields
- **Format Conversion**: JSON to XML
- **Data Aggregation**: Combine endpoints
- **Response Caching**: Reduce backend load
- **Template Rendering**: Dynamic content

## Usage Examples

### Rate Limiting

```python
from api_gateway import APIRateLimiter, RateLimitUnit

limiter = APIRateLimiter()
limit = limiter.create_rate_limit('basic', 100, RateLimitUnit.MINUTE)
print(f"Rate limit: {limit['limit']} per {limit['unit']}")

result = limiter.apply_rate_limit('api_key_123', 'basic')
print(f"Allowed: {result['allowed']}, Remaining: {result['remaining']}")

tiers = limiter.create_tiered_limits({
    'free': 100, 'pro': 1000, 'enterprise': 10000
})
```

### Authentication

```python
from api_gateway import APIAuthManager

auth = APIAuthManager()
key = auth.create_api_key('client_abc', ['read', 'write'])
print(f"API Key: {key['api_key']}")

validation = auth.validate_api_key(key['api_key'])
print(f"Valid: {validation['valid']}")

oauth = auth.create_oauth_config('client_123', ['https://callback.com'])
print(f"OAuth configured: {oauth['client_id']}")

jwt = auth.generate_jwt_token('user_123', {'role': 'admin'})
print(f"Token: {jwt['access_token'][:50]}...")
```

### Analytics

```python
from api_gateway import APIAnalytics

analytics = APIAnalytics()
metrics = analytics.get_api_metrics('users-api', '24h')
print(f"Total requests: {metrics['total_requests']}")
print(f"Avg latency: {metrics['avg_response_time_ms']}ms")
print(f"Error rate: {metrics['error_rate']:.2%}")

top = analytics.get_top_endpoints('users-api')
for endpoint in top:
    print(f"{endpoint['path']}: {endpoint['requests']} requests")

anomalies = analytics.detect_anomalies('users-api')
print(f"Anomalies found: {len(anomalies)}")
```

### Routing

```python
from api_gateway import APIRouter

router = APIRouter()
route = router.create_route(
    path='/api/v1/users',
    method='GET',
    backend='user-service:8080',
    middleware=['auth', 'logging', 'cors']
)
print(f"Route: {route['path']} -> {route['backend']}")

rewrites = router.configure_path_rewrites([
    {'pattern': '/api/v1/(.*)', 'replacement': '/internal/$1'}
])
print(f"Rewrite rules: {len(rewrites['rules'])}")

canary = router.setup_canary_deployment(
    '/api/v1/users',
    versions={'v1': 'users-v1', 'v2': 'users-v2'}
)
print(f"Canary traffic: v1 {canary['traffic_split']['v1']}%, v2 {canary['traffic_split']['v2']}%")
```

## API Gateway Patterns

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway                               │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Rate     │ │ Auth     │ │ Analytics│ │ Routing │  │
│  │ Limiting │ │ & Auth   │ │          │ │         │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Transform│ │ Caching │ │ Logging │ │ Circuit │  │
│  │          │ │         │ │         │ │ Breaker │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└──────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐     ┌────▼────┐     ┌────▼────┐
   │ Service │     │ Service │     │ Service │
   │    A    │     │    B    │     │    C    │
   └─────────┘     └─────────┘     └─────────┘
```

### Common Patterns

| Pattern | Description | Benefit |
|---------|-------------|---------|
| Gateway Aggregation | Combine multiple calls | Reduced round trips |
| Gateway Offloading | Handle auth, SSL centrally | Simplified services |
| Gateway Routing | Route to appropriate service | Flexible routing |
| Protocol Translation | HTTP to gRPC | Interoperability |

## Rate Limiting Strategies

### Token Bucket
```
Tokens added at rate R
Bucket capacity B
Each request consumes 1 token
```

### Leaky Bucket
```
Requests processed at rate R
Queue capacity B
Overflow requests rejected
```

### Sliding Window
```
Count requests in rolling window
Window divided into sub-windows
Smooth rate limiting
```

## Authentication Methods

| Method | Security | Complexity | Use Case |
|--------|----------|------------|----------|
| API Key | Low | Simple | Internal APIs |
| OAuth 2.0 | High | Complex | Third-party access |
| JWT | Medium | Medium | Stateless auth |
| mTLS | Very High | High | Service-to-service |

## Tools and Platforms

### Open Source
- **Kong**: Plugin-based gateway
- **APISIX**: Cloud-native,高性能
- **Tyk**: Fast, scalable
- **HAProxy**: Load balancer with gateway features

### Commercial
- **Amazon API Gateway**: AWS integration
- **Azure API Management**: Microsoft ecosystem
- **Apigee**: Google Cloud
- **MuleSoft**: Integration platform

## Use Cases

### 1. Microservices Architecture
- Centralized entry point
- Request aggregation
- Service isolation
- Cross-cutting concerns

### 2. Third-Party API Access
- Developer portals
- API key management
- Usage tracking
- Monetization

### 3. Mobile Backend
- Offline sync support
- Data transformation
- Rate limiting per user
- Push notification routing

### 4. Legacy Modernization
- API facade pattern
- Protocol translation
- Version management
- Deprecation handling

## Best Practices

1. **Security First**: Always use HTTPS, validate inputs
2. **Rate Limiting**: Prevent abuse and overload
3. **Monitoring**: Track usage and performance
4. **Caching**: Reduce backend load
5. **Versioning**: Support multiple API versions
6. **Documentation**: OpenAPI specs, developer portals

## Related Skills

- [Microservices](../microservices/service-architecture/README.md) - Service architecture
- [GraphQL](../graphql/api-design/README.md) - Alternative API design
- [Security Assessment](../security-assessment/api-security/README.md) - API security testing

---

**File Path**: `skills/api-gateway/api-management/resources/api_gateway.py`
