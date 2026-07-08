---
name: "Integration Agent"
version: "2.0.0"
description: "System integration platform covering API orchestration, data transformation, ETL pipelines, message queues, service mesh, and webhook processing"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["integration", "api", "middleware", "etl", "message-queue", "webhook", "data-sync", "orchestration"]
category: "integration"
personality: "integration-architect"
use_cases: ["api-management", "data-synchronization", "etl-pipelines", "message-queuing", "webhook-processing", "service-mesh"]
complexity: "advanced"
dependencies: ["python>=3.8"]
---

# Integration Agent

> Connect heterogeneous systems with intelligent orchestration, transformation, and monitoring.

The Integration Agent provides a complete system integration platform for enterprises connecting cloud services, on-premises applications, data stores, and third-party APIs. It handles the hard parts of integration: retries, circuit breakers, data transformation, queue management, and delivery tracking.

---

## Core Principles

1. **Resilience First**: Circuit breakers and retries prevent cascade failures across integrated systems.
2. **Loose Coupling**: Systems communicate through well-defined interfaces, not shared state or direct dependencies.
3. **Idempotent Operations**: Every integration operation can be safely retried without side effects.
4. **Observable Pipelines**: Every data flow step is traceable, measurable, and auditable.
5. **Schema Evolution**: Transformations handle backward-compatible changes gracefully without breaking consumers.

---

## Capabilities

### 1. API Orchestration with Circuit Breakers

Register external system connections with authentication, timeouts, retry strategies, and health checks.

```python
from agents.integration.agent import IntegrationAgent, AuthType, HttpMethod, RetryStrategy, QueueType

agent = IntegrationAgent()

# Register system connections
salesforce = agent.api_engine.add_connection(
    name="Salesforce",
    base_url="https://api.salesforce.com",
    auth_type=AuthType.OAUTH2,
    timeout=30,
    max_retries=3,
    retry_strategy=RetryStrategy.EXPONENTIAL,
    rate_limit=100,
    health_check_url="/health",
)
print(f"Connection: {salesforce.connection_id}")
# → Connection: CONN-A1B2C3D4

hubspot = agent.api_engine.add_connection(
    name="HubSpot",
    base_url="https://api.hubspot.com",
    auth_type=AuthType.API_KEY,
    timeout=20,
    max_retries=2,
)

# Create field mapping between systems
mapping = agent.api_engine.create_mapping(
    source_conn=salesforce.connection_id,
    source_method=HttpMethod.GET,
    source_path="/services/data/v58.0/query",
    dest_conn=hubspot.connection_id,
    dest_method=HttpMethod.POST,
    dest_path="/crm/v3/objects/contacts",
    field_mappings={"Email": "email", "Name": "fullname", "Phone": "phone"},
    transforms=[{"type": "normalize", "rules": {"email": {"type": "lowercase"}}}],
)

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
# → Flow: 2/2 steps
```

**Circuit Breaker States:**
```
CLOSED (normal operation)
  │
  │  failures >= threshold (default: 5)
  ▼
OPEN (requests blocked for timeout_seconds)
  │
  │  timeout elapsed
  ▼
HALF_OPEN (one test request allowed)
  │
  ├── success → CLOSED
  └── failure → OPEN
```

**Retry Strategy Delays:**

| Strategy | Formula | Example (base=1s) |
|----------|---------|-------------------|
| FIXED | delay = base | 1s, 1s, 1s |
| EXPONENTIAL | delay = base × 2^attempt | 1s, 2s, 4s, 8s |
| LINEAR | delay = base × (attempt + 1) | 1s, 2s, 3s, 4s |
| FIBONACCI | delay = base × fib(attempt) | 1s, 1s, 2s, 3s, 5s |

---

### 2. Data Transformation Engine

Transform, normalize, and validate data between systems.

```python
# Map fields between systems
mapped = agent.transform_engine.map_fields(
    data={"email": "user@test.com", "name": "John Doe", "phone": "555-1234"},
    field_map={"email": "contact_email", "name": "full_name"},
)
# → {"contact_email": "user@test.com", "full_name": "John Doe", "phone": "555-1234"}

# Normalize data values
normalized = agent.transform_engine.normalize_data(
    data={"email": "  User@Test.COM  ", "age": "25", "status": ""},
    rules={
        "email": {"type": "lowercase"},
        "age": {"type": "cast", "target": "int"},
        "status": {"type": "default", "value": "unknown"},
    },
)
# → {"email": "user@test.com", "age": 25, "status": "unknown"}

# Filter fields
filtered = agent.transform_engine.filter_fields(
    data={"name": "John", "email": "j@test.com", "internal_id": 123, "debug": True},
    include_fields=["name", "email"],
)
# → {"name": "John", "email": "j@test.com"}

# Deduplicate records
unique = agent.transform_engine.deduplicate(
    records=[
        {"id": 1, "name": "Alice"},
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ],
    key_fields=["id"],
)
# → [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

# Aggregate data
aggregated = agent.transform_engine.aggregate_data(
    records=[
        {"region": "US", "quarter": "Q1", "revenue": 100},
        {"region": "US", "quarter": "Q1", "revenue": 200},
        {"region": "EU", "quarter": "Q1", "revenue": 150},
    ],
    group_by=["region", "quarter"],
    aggregations={"revenue": "sum"},
)
# → [{"region": "US", "quarter": "Q1", "revenue_sum": 300, "record_count": 2}, ...]

# Convert formats
json_str = agent.transform_engine.convert_format(
    {"key": "value"}, DataFormat.JSON, DataFormat.CSV
)
```

**Transform Types:**

| Type | Description | Example |
|------|-------------|---------|
| MAP | Rename/reorder fields | `email` → `contact_email` |
| FILTER | Include/exclude fields | Keep only name, email |
| NORMALIZE | Standardize values | lowercase, trim, cast types |
| AGGREGATE | Group and compute | SUM, AVG, COUNT by group |
| DEDUPLICATE | Remove duplicates | By key field combination |
| JOIN | Merge datasets | By common key field |
| ENRICH | Add computed fields | Derived values from existing |
| VALIDATE | Schema validation | Required fields, type checks |

---

### 3. ETL Pipeline Management

Define, schedule, and monitor extract/transform/load pipelines.

```python
# Create pipeline
pipeline = agent.etl_manager.create_pipeline(
    name="Sales Contact Sync",
    description="Sync contacts from Salesforce to HubSpot every 6 hours",
    source_type="salesforce",
    dest_type="hubspot",
    schedule_cron="0 */6 * * *",
    transforms=[
        {"type": "map", "field_map": {"Email": "email"}},
        {"type": "normalize", "rules": {"email": {"type": "lowercase"}}},
    ],
)

# Execute pipeline
run = agent.etl_manager.run_pipeline(pipeline.pipeline_id)
print(f"Run: {run.status.value} — {run.records_loaded} records in {run.duration_seconds}s")
# → Run: success — 975 records in 12.5s

# Get pipeline metrics
metrics = agent.etl_manager.get_pipeline_metrics(pipeline.pipeline_id)
# → {
#     "pipeline_id": "ETL-XXX",
#     "name": "Sales Contact Sync",
#     "status": "active",
#     "total_runs": 150,
#     "success_rate": 99.3,
#     "avg_duration": 11.8,
#     "total_records_processed": 145000,
# }
```

---

### 4. Message Queue Management

Publish, subscribe, and route messages between system components.

```python
# Create queue
queue = agent.queue_manager.create_queue(
    name="contact-events",
    queue_type=QueueType.PUBLISH_SUBSCRIBE,
    max_size=100000,
    message_ttl=3600,
)

# Subscribe to topics
agent.queue_manager.subscribe("contact.created", queue.queue_id)
agent.queue_manager.subscribe("contact.updated", queue.queue_id)

# Publish messages
msg = agent.queue_manager.publish_message(
    queue_id=queue.queue_id,
    topic="contact.created",
    payload={"email": "new@test.com", "name": "New User"},
    priority=1,
)
print(f"Published: {msg['message_id']}")

# Dead letter handling
agent.queue_manager.send_to_dead_letter(
    message={"original": "failed message payload"},
    reason="Transform validation error",
)

# Queue metrics
overview = agent.queue_manager.get_overview()
# → {
#     "total_queues": 5,
#     "total_messages_published": 25000,
#     "total_messages_delivered": 24800,
#     "delivery_rate": 99.2,
#     "dead_letter_count": 45,
# }
```

**Queue Types:**

| Type | Pattern | Use Case | Delivery |
|------|---------|----------|----------|
| POINT_TO_POINT | 1:1 | Task queues, job distribution | One consumer per message |
| PUBLISH_SUBSCRIBE | 1:N | Event broadcasting | All subscribers receive |
| TOPIC | filtered N:N | Selective delivery | Filtered by topic |
| FIFO | ordered | Sequence-dependent processing | Strict ordering |
| PRIORITY | weighted | Critical notifications | Higher priority first |
| DEAD_LETTER | failed msgs | Error handling and retry | Capture failed messages |

---

### 5. Webhook Processing

Register webhook endpoints and track event delivery.

```python
webhook = agent.webhook_manager.register_webhook(
    url="https://hooks.example.com/sync",
    events=["contact.created", "contact.updated", "contact.deleted"],
    secret="whsec_abc123def456",
    retry_policy={"max_retries": 3, "backoff": "exponential"},
)

# Trigger events
results = agent.webhook_manager.trigger_event("contact.created", {"email": "test@test.com"})
# → [{"webhook_id": "WH-XXX", "url": "https://hooks.example.com/sync", "status": "delivered"}]

# Webhook statistics
stats = agent.webhook_manager.get_webhook_stats()
# → {
#     "total_webhooks": 8,
#     "active": 7,
#     "total_delivered": 1250,
#     "total_failed": 12,
#     "success_rate": 99.0,
# }
```

---

## Data Models

### SystemConnection

| Field | Type | Description |
|-------|------|-------------|
| connection_id | str | Unique identifier (CONN-{hash}) |
| name | str | Connection name |
| base_url | str | API base URL |
| auth_type | AuthType | API_KEY, OAUTH2, BASIC, BEARER, MUTUAL_TLS, HMAC, JWT |
| status | ConnectionStatus | ACTIVE, INACTIVE, ERROR, DEGRADED, MAINTENANCE |
| timeout_seconds | int | Request timeout (default: 30) |
| max_retries | int | Maximum retry attempts (default: 3) |
| retry_strategy | RetryStrategy | NONE, FIXED, EXPONENTIAL, LINEAR, FIBONACCI |
| rate_limit_per_second | int | Max requests per second |

### ETLPipeline

| Field | Type | Description |
|-------|------|-------------|
| pipeline_id | str | Unique identifier (ETL-{hash}) |
| name | str | Pipeline name |
| source_type | str | Source system type |
| destination_type | str | Destination system type |
| status | PipelineStatus | DRAFT, ACTIVE, PAUSED, ERROR, COMPLETED, ARCHIVED |
| schedule_cron | str | Cron expression for scheduling |
| total_runs | int | Total execution count |
| success_runs | int | Successful execution count |
| avg_duration_seconds | float | Average run duration |

### MessageQueue

| Field | Type | Description |
|-------|------|-------------|
| queue_id | str | Unique identifier (Q-{hash}) |
| name | str | Queue name |
| queue_type | QueueType | POINT_TO_POINT, PUBLISH_SUBSCRIBE, TOPIC, FIFO, DEAD_LETTER, PRIORITY |
| max_size | int | Maximum queue size |
| messages_published | int | Total messages published |
| messages_delivered | int | Total messages delivered |
| messages_dead_lettered | int | Messages sent to dead letter |

---

## Checklists

### New Integration Setup
- [ ] Register source and destination connections
- [ ] Configure authentication (OAuth2, API key, etc.)
- [ ] Set rate limits and timeouts appropriately
- [ ] Define field mappings between systems
- [ ] Configure retry strategy and circuit breaker thresholds
- [ ] Set up health check endpoints
- [ ] Test with sample data end-to-end
- [ ] Configure monitoring and alerting
- [ ] Document data flow for operations team

### ETL Pipeline Deployment
- [ ] Define source query/parameters
- [ ] Define transformation steps
- [ ] Set loading strategy (upsert, insert, replace)
- [ ] Configure schedule (cron expression)
- [ ] Set error handling (retry, dead-letter)
- [ ] Test with production-like data volume
- [ ] Set up monitoring dashboard
- [ ] Define escalation procedures for failures

### Production Readiness
- [ ] Circuit breaker thresholds appropriate for load
- [ ] Retry delays not too aggressive (respect rate limits)
- [ ] Dead-letter queue monitored and alerting configured
- [ ] Health checks passing for all connections
- [ ] Metrics being collected and dashboarded
- [ ] Alerting configured for failure conditions
- [ ] Runbooks documented for common failure scenarios
- [ ] Load tested at expected peak volume

---

## Troubleshooting

### Connection Issues

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| Circuit breaker keeps opening | Target system unhealthy or auth expired | Check target health, refresh credentials |
| Requests timing out | Timeout too low or network issues | Increase timeout, check network connectivity |
| Authentication failures | Expired tokens or wrong credentials | Refresh OAuth tokens, verify API keys |
| Rate limit errors (429) | Too many requests per second | Reduce rate_limit, implement backoff |

### ETL Issues

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| Pipeline fails on extraction | Source connectivity or query error | Verify source is reachable, check query syntax |
| Data transformation errors | Schema mismatch or type errors | Review transformation rules, check data types |
| Duplicate records in destination | Missing dedup key or upsert not configured | Add deduplication step, configure upsert |
| Pipeline runs but loads 0 records | Empty source or filter too restrictive | Check source data, review filter criteria |

### Queue Issues

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| Messages not delivered | No subscribers or wrong topic | Verify subscription exists and matches topic |
| Dead letter queue growing | Consumer processing failures | Check consumer logs, review message format |
| Messages lost | TTL expired or queue full | Increase TTL or queue size |
| Ordering violated | Non-FIFO queue used | Switch to FIFO queue type |

### Webhook Issues

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| Delivery failures | Endpoint unreachable or SSL error | Verify URL, check SSL certificate |
| Signature verification fails | Secret mismatch | Verify webhook secret matches |
| High latency | Slow endpoint response | Optimize endpoint, increase timeout |
| Events not triggering | Event type not in subscription | Check webhook event registration |

---

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
})
```
