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
- [License](#license)

## Overview

The Integration Agent connects heterogeneous systems across cloud, on-prem, and hybrid environments. It provides API orchestration with circuit breakers, data transformation pipelines, ETL job management, message queue operations, and webhook processing — all with built-in resilience and monitoring.

## Features

### API Orchestration
- Multi-service composition with step-by-step flows
- Circuit breaker pattern (CLOSED → OPEN → HALF_OPEN)
- Configurable retry strategies (fixed, exponential, linear, fibonacci)
- Rate limiting per connection
- Health check monitoring

### Data Transformation
- Field mapping and renaming
- Data normalization (lowercase, trim, cast, regex)
- Aggregation (sum, avg, count, min, max)
- Deduplication by key fields
- Format conversion (JSON, XML, CSV)

### ETL Pipelines
- Pipeline definition with source/destination types
- Cron-based scheduling
- Run tracking with success/failure metrics
- Duration and throughput monitoring

### Message Queues
- Multiple queue types (point-to-point, pub/sub, FIFO, priority)
- Topic routing and subscription management
- Dead-letter handling for failed messages
- Delivery rate tracking

### Webhook Processing
- Event-driven webhook registration
- Multi-event subscription
- Delivery tracking and statistics
- HMAC signature verification

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
```

### Webhooks

```python
webhook = agent.webhook_manager.register_webhook(
    url="https://hooks.example.com/sync",
    events=["contact.created", "contact.updated"],
    secret="whsec_abc123",
)

results = agent.webhook_manager.trigger_event("contact.created", {"email": "new@test.com"})
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

### DataTransformationEngine

| Method | Description |
|--------|-------------|
| `map_fields(data, field_map)` | Rename/map fields |
| `filter_fields(data, include, exclude)` | Filter fields |
| `normalize_data(data, rules)` | Apply normalization |
| `aggregate_data(records, group_by, aggs)` | Aggregate data |
| `deduplicate(records, key_fields)` | Remove duplicates |
| `convert_format(data, source, target)` | Convert formats |

### ETLPipelineManager

| Method | Description |
|--------|-------------|
| `create_pipeline(name, desc, src, dest, **kw)` | Create pipeline |
| `run_pipeline(pipeline_id)` | Execute pipeline |
| `get_pipeline_metrics(pipeline_id)` | Get pipeline stats |

### MessageQueueManager

| Method | Description |
|--------|-------------|
| `create_queue(name, type, **kw)` | Create queue |
| `publish_message(queue_id, topic, payload)` | Publish message |
| `subscribe(topic, queue_id)` | Subscribe to topic |

## Examples

See the full demo in `agent.py`.

## Configuration

```python
# Custom circuit breaker settings
agent.api_engine.circuit_threshold = 10
agent.api_engine.circuit_timeout_seconds = 120

# Custom retry strategy
conn = agent.api_engine.add_connection(
    name="API",
    base_url="https://api.example.com",
    auth_type=AuthType.API_KEY,
    retry_strategy=RetryStrategy.EXPONENTIAL,
    retries=5,
    timeout=60,
)
```

## Best Practices

1. **Always set timeouts** — prevent hanging connections
2. **Use circuit breakers** — prevent cascade failures
3. **Implement idempotent operations** — safe retries
4. **Monitor dead-letter queues** — catch silent failures
5. **Validate data at boundaries** — catch issues early
6. **Log all integration events** — enable debugging

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Circuit breaker keeps opening | Check target system health and auth |
| ETL pipeline failing | Verify source/dest connectivity and data format |
| Messages not delivered | Check topic subscription and consumer status |
| Webhook delivery failures | Verify URL, SSL, and payload size |

## License

MIT License - see LICENSE file for details.
