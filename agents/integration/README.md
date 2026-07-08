# Integration Agent

> System integration platform covering API orchestration, data transformation, ETL pipelines, message queues, service mesh, and webhook processing.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [Performance](#performance)
- [Security](#security)
- [Extending the Agent](#extending-the-agent)
- [FAQ](#faq)
- [License](#license)

## Overview

The Integration Agent connects heterogeneous systems across cloud, on-prem, and hybrid environments. It provides API orchestration with circuit breakers, data transformation pipelines, ETL job management, message queue operations, and webhook processing — all with built-in resilience and monitoring.

Whether you need to sync data between Salesforce and HubSpot, run scheduled ETL jobs, process events through message queues, or deliver webhooks to external services, the Integration Agent handles the hard parts: retries, circuit breakers, rate limiting, data validation, and delivery tracking.

## Features

### API Orchestration
- Multi-service composition with step-by-step flows
- Circuit breaker pattern (CLOSED → OPEN → HALF_OPEN)
- Configurable retry strategies (fixed, exponential, linear, fibonacci)
- Rate limiting per connection
- Health check monitoring
- Support for OAuth2, API Key, Basic, JWT, Mutual TLS authentication

### Data Transformation
- Field mapping and renaming
- Data normalization (lowercase, trim, cast, regex)
- Aggregation (sum, avg, count, min, max)
- Deduplication by key fields
- Format conversion (JSON, XML, CSV, YAML)
- Join and enrich operations
- Schema validation

### ETL Pipelines
- Pipeline definition with source/destination types
- Cron-based scheduling
- Run tracking with success/failure metrics
- Duration and throughput monitoring
- Incremental and full-load extraction strategies
- UPSERT, INSERT, REPLACE loading strategies

### Message Queues
- Multiple queue types (point-to-point, pub/sub, FIFO, priority)
- Topic routing and subscription management
- Dead-letter handling for failed messages
- Delivery rate tracking
- Message TTL and size limits

### Webhook Processing
- Event-driven webhook registration
- Multi-event subscription
- Delivery tracking and statistics
- HMAC signature verification
- Retry policy with exponential backoff

### Observability
- Structured JSON logging
- Metrics collection (counters, gauges, histograms)
- Audit trail for all operations
- Alert engine with configurable thresholds

## Quick Start

### Installation

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Basic Usage

```python
from agents.integration.agent import IntegrationAgent, AuthType, HttpMethod, QueueType

agent = IntegrationAgent()

# Register connections
salesforce = agent.api_engine.add_connection(
    name="Salesforce",
    base_url="https://api.salesforce.com",
    auth_type=AuthType.OAUTH2,
)

hubspot = agent.api_engine.add_connection(
    name="HubSpot",
    base_url="https://api.hubspot.com",
    auth_type=AuthType.API_KEY,
)

# Create mapping
mapping = agent.api_engine.create_mapping(
    source_conn=salesforce.connection_id,
    source_method=HttpMethod.GET,
    source_path="/contacts",
    dest_conn=hubspot.connection_id,
    dest_method=HttpMethod.POST,
    dest_path="/crm/v3/objects/contacts",
    field_mappings={"Email": "email", "Name": "fullname"},
)

# Get dashboard
dashboard = agent.get_dashboard()
```

### Run the Demo

```bash
python agents/integration/agent.py
```

## Usage

### API Orchestration

```python
# Execute single API call
result = agent.api_engine.execute_request(
    salesforce.connection_id, HttpMethod.GET, "/contacts"
)

# Orchestrate multi-step flow
flow_result = agent.api_engine.orchestrate_flow([
    {"connection_id": salesforce.connection_id, "method": "GET", "path": "/contacts"},
    {"connection_id": hubspot.connection_id, "method": "POST", "path": "/contacts"},
])
print(f"Flow: {flow_result['steps_completed']}/{flow_result['steps_total']} steps")

# Check connection health
health = agent.api_engine.health_check_all()
for conn, status in health.items():
    print(f"{conn}: {status}")
```

### ETL Pipeline

```python
pipeline = agent.etl_manager.create_pipeline(
    name="Sales Contact Sync",
    description="Sync contacts Salesforce → HubSpot",
    source_type="salesforce",
    dest_type="hubspot",
    schedule_cron="0 */6 * * *",
)

run = agent.etl_manager.run_pipeline(pipeline.pipeline_id)
print(f"Loaded: {run.records_loaded} records in {run.duration_seconds}s")

# Get pipeline metrics
metrics = agent.etl_manager.get_pipeline_metrics(pipeline.pipeline_id)
print(f"Success rate: {metrics['success_rate']}%")
```

### Message Queue

```python
queue = agent.queue_manager.create_queue(
    name="contact-events",
    queue_type=QueueType.PUBLISH_SUBSCRIBE,
)

agent.queue_manager.subscribe("contact.created", queue.queue_id)

msg = agent.queue_manager.publish_message(
    queue_id=queue.queue_id,
    topic="contact.created",
    payload={"email": "user@test.com"},
)

# Monitor dead letter queue
dlq_messages = agent.queue_manager.get_dead_letter_messages(queue.queue_id)
```

### Data Transformation

```python
# Map fields
result = agent.transform_engine.map_fields(
    data={"email": "user@test.com", "name": "John"},
    field_map={"email": "contact_email"},
)

# Normalize
normalized = agent.transform_engine.normalize_data(
    data={"email": "  User@Test.COM  "},
    rules={"email": {"type": "lowercase"}},
)

# Aggregate
aggregated = agent.transform_engine.aggregate_data(
    records=[{"region": "US", "sales": 100}, {"region": "US", "sales": 200}],
    group_by=["region"],
    aggregations={"sales": "sum"},
)

# Join datasets
joined = agent.transform_engine.join_datasets(
    left=customers,
    right=orders,
    left_key="customer_id",
    right_key="customer_id",
    join_type="left",
)

# Validate data
schema = {"email": {"type": "str", "required": True}, "age": {"type": "int", "min": 0}}
result = agent.transform_engine.validate_data(data, schema)
```

### Webhooks

```python
webhook = agent.webhook_manager.register_webhook(
    url="https://hooks.example.com/sync",
    events=["contact.created", "contact.updated"],
    secret="whsec_abc123",
)

results = agent.webhook_manager.trigger_event("contact.created", {"email": "new@test.com"})

# Get webhook statistics
stats = agent.webhook_manager.get_webhook_stats()
print(f"Success rate: {stats['success_rate']}%")
```

## API Reference

### APIOrchestrationEngine

| Method | Description |
|--------|-------------|
| `add_connection(name, url, auth_type, **kw)` | Register a system connection |
| `create_mapping(source, method, path, dest, ...)` | Create endpoint mapping |
| `execute_request(conn_id, method, path, body)` | Execute API call |
| `orchestrate_flow(steps)` | Run multi-step flow |
| `health_check_all()` | Check all connection health |
| `get_connection_stats(conn_id)` | Get connection metrics |

### DataTransformationEngine

| Method | Description |
|--------|-------------|
| `map_fields(data, field_map)` | Rename/map fields |
| `filter_fields(data, include, exclude)` | Filter fields |
| `normalize_data(data, rules)` | Apply normalization |
| `aggregate_data(records, group_by, aggs)` | Aggregate data |
| `deduplicate(records, key_fields)` | Remove duplicates |
| `convert_format(data, source, target)` | Convert formats |
| `join_datasets(left, right, left_key, right_key)` | Join datasets |
| `enrich_data(records, computed_fields)` | Add computed fields |
| `validate_data(data, schema)` | Validate against schema |

### ETLPipelineManager

| Method | Description |
|--------|-------------|
| `create_pipeline(name, desc, src, dest, **kw)` | Create pipeline |
| `run_pipeline(pipeline_id)` | Execute pipeline |
| `get_pipeline_metrics(pipeline_id)` | Get pipeline stats |
| `pause_pipeline(pipeline_id)` | Pause pipeline |
| `resume_pipeline(pipeline_id)` | Resume pipeline |

### MessageQueueManager

| Method | Description |
|--------|-------------|
| `create_queue(name, type, **kw)` | Create queue |
| `publish_message(queue_id, topic, payload)` | Publish message |
| `subscribe(topic, queue_id)` | Subscribe to topic |
| `get_dead_letter_messages(queue_id)` | Get dead letter messages |
| `retry_message(message_id)` | Retry dead letter message |
| `get_overview()` | Get queue metrics |

### WebhookManager

| Method | Description |
|--------|-------------|
| `register_webhook(url, events, secret)` | Register webhook |
| `trigger_event(event_type, payload)` | Trigger event |
| `get_webhook_stats()` | Get webhook statistics |
| `remove_webhook(webhook_id)` | Remove webhook |

## Examples

### CRM Sync Pipeline

```python
from agents.integration.agent import IntegrationAgent, AuthType, HttpMethod

agent = IntegrationAgent()

# Register CRM systems
salesforce = agent.api_engine.add_connection(
    name="Salesforce",
    base_url="https://api.salesforce.com",
    auth_type=AuthType.OAUTH2,
    timeout=30,
)

hubspot = agent.api_engine.add_connection(
    name="HubSpot",
    base_url="https://api.hubspot.com",
    auth_type=AuthType.API_KEY,
    timeout=20,
)

# Create bidirectional sync pipeline
pipeline = agent.etl_manager.create_pipeline(
    name="CRM Bidirectional Sync",
    description="Keep contacts in sync between Salesforce and HubSpot",
    source_type="salesforce",
    dest_type="hubspot",
    schedule_cron="0 */4 * * *",  # Every 4 hours
    transforms=[
        {"type": "map", "field_map": {"Email": "email", "FirstName": "first_name"}},
        {"type": "normalize", "rules": {"email": {"type": "lowercase"}}},
        {"type": "deduplicate", "key_fields": ["email"]},
    ],
)

# Run the pipeline
run = agent.etl_manager.run_pipeline(pipeline.pipeline_id)
print(f"Sync complete: {run.records_loaded} contacts updated")

# Set up webhook for real-time updates
webhook = agent.webhook_manager.register_webhook(
    url="https://your-app.com/webhooks/crm",
    events=["contact.created", "contact.updated", "contact.deleted"],
    secret="whsec_your_secret_here",
)
```

### Event-Driven Microservices

```python
from agents.integration.agent import IntegrationAgent, QueueType

agent = IntegrationAgent()

# Create event bus
event_queue = agent.queue_manager.create_queue(
    name="event-bus",
    queue_type=QueueType.PUBLISH_SUBSCRIBE,
    max_size=1000000,
)

# Subscribe services to events
agent.queue_manager.subscribe("order.created", event_queue.queue_id)
agent.queue_manager.subscribe("order.updated", event_queue.queue_id)
agent.queue_manager.subscribe("payment.received", event_queue.queue_id)

# Publish events
agent.queue_manager.publish_message(
    queue_id=event_queue.queue_id,
    topic="order.created",
    payload={
        "order_id": "ORD-12345",
        "customer_id": "CUST-678",
        "total": 99.99,
        "items": [{"sku": "WIDGET-1", "qty": 2}],
    },
)

# Monitor queue health
overview = agent.queue_manager.get_overview()
print(f"Delivery rate: {overview['delivery_rate']}%")
```

### Data Quality Pipeline

```python
from agents.integration.agent import IntegrationAgent

agent = IntegrationAgent()

# Define validation schema
schema = {
    "email": {"type": "str", "required": True, "pattern": r"^[\w.-]+@[\w.-]+\.\w+$"},
    "age": {"type": "int", "min": 0, "max": 150},
    "name": {"type": "str", "required": True, "min_length": 1},
    "phone": {"type": "str", "pattern": r"^\+?[\d\s-]+$"},
}

# Transform and validate data
raw_data = [
    {"email": "  User@Test.COM  ", "age": "25", "name": "John Doe", "phone": "+1-555-1234"},
    {"email": "invalid-email", "age": "200", "name": "", "phone": "abc"},
]

# Normalize
normalized = [
    agent.transform_engine.normalize_data(record, {
        "email": {"type": "lowercase"},
        "age": {"type": "cast", "target": "int"},
    })
    for record in raw_data
]

# Validate
for record in normalized:
    result = agent.transform_engine.validate_data(record, schema)
    if not result["valid"]:
        print(f"Validation errors: {result['errors']}")
```

## Configuration

```python
agent = IntegrationAgent(config={
    "circuit_breaker_threshold": 5,
    "circuit_breaker_timeout": 60,
    "default_retry_strategy": "exponential",
    "default_timeout": 30,
    "rate_limit_default": 100,
    "etl_max_concurrent_pipelines": 10,
    "queue_default_ttl": 3600,
    "webhook_default_retries": 3,
    "log_level": "INFO",
    "metrics_enabled": True,
})
```

### Configuration Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `circuit_breaker_threshold` | 5 | Failures before circuit opens |
| `circuit_breaker_timeout` | 60 | Seconds before half-open |
| `default_retry_strategy` | exponential | Default retry backoff |
| `default_timeout` | 30 | Default request timeout (seconds) |
| `rate_limit_default` | 100 | Default requests per second |
| `etl_max_concurrent_pipelines` | 10 | Max parallel ETL runs |
| `queue_default_ttl` | 3600 | Default message TTL (seconds) |
| `webhook_default_retries` | 3 | Default webhook retry count |
| `log_level` | INFO | Logging level |
| `metrics_enabled` | True | Enable metrics collection |

## Best Practices

### Resilience
1. **Always set timeouts** — prevent hanging connections
2. **Use circuit breakers** — prevent cascade failures
3. **Implement idempotent operations** — safe retries
4. **Monitor dead-letter queues** — catch silent failures
5. **Configure retry budgets** — avoid infinite retry loops

### Data Quality
6. **Validate data at boundaries** — catch issues early
7. **Use schemas for transformations** — ensure consistency
8. **Deduplicate by meaningful keys** — prevent duplicates
9. **Log transformation details** — enable debugging

### Operations
10. **Log all integration events** — enable debugging
11. **Tag resources for cost allocation** — track expenses
12. **Set up alerting** — get notified of failures
13. **Document data flows** — help operations team
14. **Test with production-like data** — catch edge cases

### Security
15. **Never log secrets** — use redaction
16. **Use OAuth2 for SaaS integrations** — avoid API keys
17. **Sign webhook payloads** — verify authenticity
18. **Enforce TLS for all connections** — encrypt in transit

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Circuit breaker keeps opening | Target system unhealthy or auth expired | Check target health, refresh credentials |
| Requests timing out | Timeout too low or network issues | Increase timeout, check network connectivity |
| Authentication failures | Expired tokens or wrong credentials | Refresh OAuth tokens, verify API keys |
| Rate limit errors (429) | Too many requests per second | Reduce rate_limit, implement backoff |
| Pipeline fails on extraction | Source connectivity or query error | Verify source is reachable, check query syntax |
| Data transformation errors | Schema mismatch or type errors | Review transformation rules, check data types |
| Duplicate records in destination | Missing dedup key or upsert not configured | Add deduplication step, configure upsert |
| Messages not delivered | No subscribers or wrong topic | Verify subscription exists and matches topic |
| Dead letter queue growing | Consumer processing failures | Check consumer logs, review message format |
| Delivery failures | Endpoint unreachable or SSL error | Verify URL, check SSL certificate |
| Signature verification fails | Secret mismatch | Verify webhook secret matches |
| High latency | Slow endpoint response | Optimize endpoint, increase timeout |

## Architecture

For detailed architecture documentation, see [ARCHITECTURE.md](./ARCHITECTURE.md).

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Integration Agent                         │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│     API     │    Transform│    ETL      │    Queue         │
│  Orchestrate│   Engine    │  Manager    │    Manager       │
├─────────────┼─────────────┼─────────────┼──────────────────┤
│ - Connections│ - Map       │ - Pipelines │ - Pub/Sub        │
│ - Flows     │ - Filter    │ - Schedules │ - FIFO           │
│ - Circuit   │ - Normalize │ - Metrics   │ - Priority       │
│ - Retry     │ - Aggregate │ - Runs      │ - Dead Letter    │
├─────────────┴─────────────┴─────────────┴──────────────────┤
│                    Webhook Manager                           │
│  - Registration  - Events  - Delivery  - Retry              │
├─────────────────────────────────────────────────────────────┤
│                    Observability                              │
│  - Logging  - Metrics  - Audit  - Alerts                    │
└─────────────────────────────────────────────────────────────┘
```

## Performance

| Metric | Target | Notes |
|--------|--------|-------|
| API call overhead | < 100ms | Excluding network latency |
| Transform throughput | > 10K records/sec | Single-threaded |
| ETL pipeline (10K records) | < 5s | End-to-end |
| Queue publish latency | < 10ms p99 | In-memory queues |
| Webhook delivery | < 500ms p95 | Including network |
| Circuit breaker detection | < 1s | From failure to open |

## Security

- OAuth2 tokens stored per-connection, refreshed automatically
- Webhook payloads signed with HMAC-SHA256
- API keys and secrets never logged
- TLS required for all external connections
- Rate limiting prevents abuse and protects downstream systems
- Circuit breaker prevents resource exhaustion during outages

## Extending the Agent

### Custom Transform Types

```python
from agents.integration.transforms import TransformType

class CustomTransform(TransformType):
    CUSTOM_NORMALIZE = "custom_normalize"

# Register custom transform
agent.transform_engine.register_transform(
    CustomTransform.CUSTOM_NORMALIZE,
    lambda data, params: my_custom_transform(data, params),
)
```

### Custom Retry Strategies

```python
from agents.integration.retry import RetryStrategy

class CustomRetry(RetryStrategy):
    DECORRELATED_JITTER = "decorrelated_jitter"

# Register custom retry
agent.api_engine.register_retry_strategy(
    CustomRetry.DECORRELATED_JITTER,
    lambda base, attempt: decorrelated_jitter(base, attempt),
)
```

### Custom Auth Types

```python
from agents.integration.auth import AuthType

class CustomAuth(AuthType):
    SAML = "saml"

# Register custom auth
agent.api_engine.register_auth_handler(
    CustomAuth.SAML,
    lambda config: SAMLAuthHandler(config),
)
```

## FAQ

**Q: How does the circuit breaker work?**
A: The circuit breaker tracks consecutive failures per connection. When failures exceed the threshold, the circuit opens and blocks requests for the timeout period. After the timeout, it allows one test request (half-open). If it succeeds, the circuit closes; if it fails, it opens again.

**Q: What happens when a message fails processing?**
A: Failed messages are retried according to the queue's retry policy. After exhausting retries, messages are moved to the dead letter queue for inspection and manual handling.

**Q: Can I run multiple ETL pipelines concurrently?**
A: Yes. The agent supports concurrent pipeline execution up to the configured limit (default: 10). Each pipeline runs independently with its own state and metrics.

**Q: How are webhook payloads signed?**
A: Webhook payloads are signed using HMAC-SHA256 with the webhook's secret key. The signature is included in the `X-Webhook-Signature` header for verification by the receiving endpoint.

**Q: Can I customize the retry backoff strategy?**
A: Yes. The agent provides four built-in strategies (fixed, exponential, linear, fibonacci) and supports custom strategies via the retry strategy registry.

## License

MIT License - see LICENSE file for details.
