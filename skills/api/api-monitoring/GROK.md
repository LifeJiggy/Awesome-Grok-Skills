---
name: "api-monitoring"
category: "api"
version: "2.0.0"
tags: ["api", "monitoring", "analytics", "observability", "tracing", "metrics", "logging"]
---

# API Monitoring

## Overview

Comprehensive API monitoring and observability platform providing real-time metrics, distributed tracing, structured logging, error tracking, performance analytics, and SLA compliance monitoring. This module tracks request rates, latency percentiles (p50/p95/p99), error rates, throughput, and availability across all API endpoints with alerting, anomaly detection, and automated incident response. Supports OpenTelemetry, Prometheus, Grafana, Datadog, and custom monitoring backends.

## Core Capabilities

- **Request Metrics**: Track request count, rate, latency distribution, and throughput per endpoint, method, status code, and consumer
- **Distributed Tracing**: End-to-end request tracing across microservices with span hierarchy and bottleneck identification
- **Structured Logging**: JSON-structured API access logs with correlation IDs, user context, and performance data
- **Error Tracking**: Aggregate and categorize errors by type, endpoint, frequency, and impact with stack trace analysis
- **SLA Monitoring**: Track availability, latency, and error rate SLAs with automated compliance reporting
- **Anomaly Detection**: Statistical anomaly detection for traffic spikes, latency degradation, and error bursts
- **Alerting**: Configurable alerts on metrics thresholds with escalation policies and notification channels
- **Dashboard Generation**: Auto-generated monitoring dashboards with key API health indicators

## Usage

```python
from api_monitoring import (
    MetricsCollector, TraceCollector, AlertManager, SLATracker, DashboardGenerator
)

# Collect metrics
metrics = MetricsCollector()
metrics.record_request(
    method="GET", path="/api/users",
    status_code=200, latency_ms=45.2,
    consumer_id="client-app-1",
)
metrics.record_request(
    method="POST", path="/api/users",
    status_code=201, latency_ms=120.5,
    consumer_id="client-app-1",
)
metrics.record_request(
    method="GET", path="/api/users/123",
    status_code=404, latency_ms=12.1,
)

# Query metrics
summary = metrics.get_endpoint_summary("GET /api/users")
print(f"Requests: {summary['total_requests']}")
print(f"Avg latency: {summary['avg_latency_ms']:.1f}ms")
print(f"p99 latency: {summary['p99_latency_ms']:.1f}ms")
print(f"Error rate: {summary['error_rate']:.2%}")

# Distributed tracing
tracer = TraceCollector()
span = tracer.start_span("GET /api/users")
child = tracer.start_span("db.query", parent=span.span_id)
tracer.end_span(child)
tracer.end_span(span, attributes={"http.status_code": 200})

# SLA tracking
sla = SLATracker()
sla.define_sla(
    name="user-api-availability",
    metric="availability",
    target=99.9,
    window="30d",
)
status = sla.check("user-api-availability")
print(f"\nSLA: {status['name']} = {status['current']:.2f}% (target: {status['target']}%)")
print(f"Compliant: {status['compliant']}")

# Alerting
alerts = AlertManager()
alerts.add_rule(
    name="high-error-rate",
    metric="error_rate",
    condition="> 0.05",
    window_minutes=5,
    severity="critical",
    notify=["slack:#api-alerts", "email:ops@example.com"],
)
```

## Best Practices

- Monitor the four golden signals: latency, traffic, errors, and saturation
- Use structured JSON logs for machine parsing — include correlation IDs in every request
- Track p99 latency, not just averages — tail latency drives user experience
- Set SLAs at the 99th percentile, not the 50th — most users experience the tail
- Implement distributed tracing across all microservices for end-to-end visibility
- Create runbooks for every alert to reduce mean time to resolution (MTTR)
- Monitor API consumer behavior to detect anomalies early
- Use anomaly detection rather than static thresholds for dynamic traffic patterns
- Export metrics in Prometheus format for integration with Grafana dashboards
- Track both server-side and client-side latency for complete picture

## Related Modules

- **api-design** — Design patterns that affect monitoring (correlation IDs, status codes)
- **api-versioning** — Version-specific monitoring and consumer migration tracking
- **api-security** — Security event monitoring and threat detection
- **api-gateway** → **api-management** — Gateway-level metrics aggregation
- **backend** → **background-jobs** — Background job monitoring and metrics

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

## Comprehensive Monitoring Patterns

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_ms',
    'HTTP request latency in milliseconds',
    ['method', 'endpoint'],
    buckets=[5, 10, 25, 50, 100, 250, 500, 1000]
)

ACTIVE_REQUESTS = Gauge(
    'http_active_requests',
    'Number of active requests',
    ['method', 'endpoint']
)

ERROR_COUNT = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['method', 'endpoint', 'error_type']
)

# Middleware to collect metrics
class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        method = scope["method"]
        path = scope["path"]
        start_time = time.time()

        ACTIVE_REQUESTS.labels(method=method, endpoint=path).inc()

        async def send_response(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                duration = (time.time() - start_time) * 1000

                REQUEST_COUNT.labels(
                    method=method,
                    endpoint=path,
                    status_code=status_code
                ).inc()

                REQUEST_LATENCY.labels(
                    method=method,
                    endpoint=path
                ).observe(duration)

                if status_code >= 400:
                    ERROR_COUNT.labels(
                        method=method,
                        endpoint=path,
                        error_type="client" if status_code < 500 else "server"
                    ).inc()

                ACTIVE_REQUESTS.labels(method=method, endpoint=path).dec()

            await send(message)

        return await self.app(scope, receive, send_response)
```

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configure tracing
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Use in request handler
async def handle_request(request):
    with tracer.start_as_current_span("handle_request") as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", request.url)

        # Database query
        with tracer.start_as_current_span("db.query") as db_span:
            result = await db.execute("SELECT * FROM users")
            db_span.set_attribute("db.statement", "SELECT * FROM users")

        # External API call
        with tracer.start_as_current_span("external.api") as api_span:
            response = await httpx.get("https://external-api.com/data")
            api_span.set_attribute("http.status_code", response.status_code)

        return result
```

### Structured Logging

```python
import structlog
import json

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()

# Use in request handler
async def handle_request(request):
    request_id = request.headers.get("X-Request-ID")
    user_id = request.state.user_id

    log = logger.bind(
        request_id=request_id,
        user_id=user_id,
        method=request.method,
        path=request.path,
    )

    log.info("request_started")

    try:
        result = await process_request(request)
        log.info("request_completed", status_code=200)
        return result
    except Exception as e:
        log.error("request_failed", error=str(e), status_code=500)
        raise
```

### Alerting Rules

```yaml
# Prometheus alerting rules
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, rate(http_request_duration_ms_bucket[5m])) > 500
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p99 latency detected"
          description: "p99 latency is {{ $value }}ms"

      - alert: RateLimitSpike
        expr: rate(http_rate_limit_rejected_total[5m]) > 100
        for: 2m
        labels:
          severity: info
        annotations:
          summary: "Rate limit rejections spiking"

      - alert: HighMemoryUsage
        expr: process_resident_memory_bytes / 1024 / 1024 > 512
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value }}MB"

      - alert: HighCPUUsage
        expr: rate(process_cpu_seconds_total[5m]) > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
```

### Dashboard Configuration

```json
{
  "dashboard": {
    "title": "API Monitoring Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Latency Distribution",
        "type": "heatmap",
        "targets": [
          {
            "expr": "rate(http_request_duration_ms_bucket[5m])",
            "legendFormat": "{{le}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(http_errors_total[5m]) / rate(http_requests_total[5m])",
            "legendFormat": "Error Rate"
          }
        ],
        "thresholds": [
          {"value": 0.01, "color": "green"},
          {"value": 0.05, "color": "yellow"},
          {"value": 0.1, "color": "red"}
        ]
      },
      {
        "title": "Active Requests",
        "type": "gauge",
        "targets": [
          {
            "expr": "sum(http_active_requests)",
            "legendFormat": "Active"
          }
        ],
        "max": 1000
      }
    ]
  }
}
```

## SLA Definition and Monitoring

### SLA Definitions

```yaml
slas:
  - name: "availability"
    metric: "uptime_percentage"
    target: 99.9
    window: "30d"
    error_budget:
      total_minutes: 43200
      allowed_downtime_minutes: 43.2
    alert_threshold: 0.5

  - name: "latency_p99"
    metric: "http_request_duration_ms"
    target: 500
    percentile: 99
    window: "5m"
    alert_threshold: 0.8

  - name: "error_rate"
    metric: "http_errors_total / http_requests_total"
    target: 0.01
    window: "5m"
    alert_threshold: 0.5

  - name: "throughput"
    metric: "http_requests_total"
    target: 1000
    unit: "requests_per_second"
    window: "5m"
    alert_threshold: 0.7
```

### SLA Monitoring Implementation

```python
class SLAMonitor:
    def __init__(self, prometheus_client):
        self.prom = prometheus_client

    def check_availability(self, sla):
        query = f"""
            1 - (
                rate(http_errors_total{{status_code=~"5.."}}[30d])
                /
                rate(http_requests_total[30d])
            )
        """
        result = self.prom.query(query)
        current = float(result[0]["value"][1])
        return {
            "name": sla["name"],
            "target": sla["target"],
            "current": current * 100,
            "compliant": current * 100 >= sla["target"],
            "error_budget_remaining": self._calculate_error_budget(sla, current),
        }

    def _calculate_error_budget(self, sla, current):
        total_minutes = 43200  # 30 days
        allowed_downtime = total_minutes * (1 - sla["target"] / 100)
        actual_downtime = total_minutes * (1 - current)
        remaining = allowed_downtime - actual_downtime
        return max(0, remaining / allowed_downtime * 100)
```

## Anomaly Detection

### Statistical Anomaly Detection

```python
import numpy as np
from scipy import stats

class AnomalyDetector:
    def __init__(self, window_size=100, threshold=3.0):
        self.window_size = window_size
        self.threshold = threshold
        self.history = []

    def add_observation(self, value):
        self.history.append(value)
        if len(self.history) > self.window_size:
            self.history.pop(0)

    def is_anomaly(self, value):
        if len(self.history) < 10:
            return False

        mean = np.mean(self.history)
        std = np.std(self.history)

        if std == 0:
            return value != mean

        z_score = abs(value - mean) / std
        return z_score > self.threshold

    def get_statistics(self):
        if len(self.history) < 10:
            return None

        return {
            "mean": np.mean(self.history),
            "std": np.std(self.history),
            "min": np.min(self.history),
            "max": np.max(self.history),
            "median": np.median(self.history),
            "p95": np.percentile(self.history, 95),
            "p99": np.percentile(self.history, 99),
        }
```

## Health Check Implementation

### Comprehensive Health Check

```python
class HealthChecker:
    def __init__(self):
        self.checks = {}

    def add_check(self, name, check_func):
        self.checks[name] = check_func

    async def check_health(self):
        results = {}
        overall_status = "healthy"

        for name, check_func in self.checks.items():
            try:
                result = await check_func()
                results[name] = {
                    "status": "healthy",
                    **result
                }
            except Exception as e:
                results[name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                overall_status = "unhealthy"

        return {
            "status": overall_status,
            "checks": results,
            "timestamp": datetime.utcnow().isoformat(),
        }

# Usage
checker = HealthChecker()
checker.add_check("database", check_database)
checker.add_check("cache", check_cache)
checker.add_check("disk", check_disk_space)
checker.add_check("memory", check_memory)

# In FastAPI
@app.get("/health")
async def health():
    return await checker.check_health()
```
