# Integration Agent Architecture

## Executive Summary

The Integration Agent is an enterprise-grade system integration platform that connects heterogeneous applications, services, and data stores across cloud, on-premises, and hybrid environments. It provides five core capabilities: API orchestration with resilience patterns, data transformation pipelines, ETL job management, message queue operations, and webhook-driven event processing.

The architecture is organized as a layered engine system where each integration concern is encapsulated in an independent engine. The `IntegrationAgent` orchestrator coordinates these engines behind a unified facade, enabling complex multi-system workflows while maintaining strict separation of concerns.

## Design Principles

**Resilience Over Perfection.** Every external call assumes failure. Circuit breakers prevent cascade failures. Retry strategies handle transient errors. Dead-letter queues capture messages that cannot be processed. The system degrades gracefully rather than failing catastrophically.

**Schema First.** Data transformations are defined by explicit schemas, not ad-hoc string manipulation. Field mappings, type casts, and validation rules are declared upfront and enforced at every pipeline step.

**Observable by Default.** Every API call, transformation, queue publish, and webhook delivery is logged with structured metadata. The system produces comprehensive metrics without requiring additional instrumentation.

**Idempotent Operations.** All integration operations are safe to retry. Message publishing uses unique identifiers. Pipeline runs track their own state. Duplicate delivery is handled at the consumer level.

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             Integration Agent                                     │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                       API Orchestration Layer                               │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │  Connection   │  │  Endpoint    │  │  Circuit     │  │  Retry       │  │  │
│  │  │  Registry     │  │  Mappings    │  │  Breaker     │  │  Engine      │  │  │
│  │  │               │  │              │  │              │  │              │  │  │
│  │  │  - OAuth2     │  │  - Source    │  │  - CLOSED    │  │  - Fixed     │  │  │
│  │  │  - API Key    │  │  - Dest      │  │  - OPEN      │  │  - Exponential│ │  │
│  │  │  - Basic      │  │  - Field map │  │  - HALF_OPEN │  │  - Linear    │  │  │
│  │  │  - JWT        │  │  - Transforms│  │              │  │  - Fibonacci │  │  │
│  │  │  - Mutual TLS │  │              │  │              │  │              │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Data Transformation Layer                                │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │  Field        │  │  Format      │  │  Schema      │  │  Validate &  │  │  │
│  │  │  Mapping      │  │  Conversion  │  │  Normalizer  │  │  Deduplicate │  │  │
│  │  │               │  │              │  │              │  │              │  │  │
│  │  │  - rename     │  │  - JSON↔CSV  │  │  - lowercase │  │  - unique    │  │  │
│  │  │  - reorder    │  │  - XML↔JSON  │  │  - trim      │  │  - by key    │  │  │
│  │  │  - filter     │  │  - YAML      │  │  - cast      │  │  - merge     │  │  │
│  │  │  - default    │  │  - Protobuf  │  │  - regex     │  │              │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                      ETL Pipeline Layer                                     │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │  Pipeline     │  │  Scheduler   │  │  Run         │  │  Metrics     │  │  │
│  │  │  Definitions  │  │  (cron)      │  │  Tracker     │  │  Aggregator  │  │  │
│  │  │               │  │              │  │              │  │              │  │  │
│  │  │  - source     │  │  - cron expr │  │  - pending   │  │  - success % │  │  │
│  │  │  - dest       │  │  - next run  │  │  - running   │  │  - duration  │  │  │
│  │  │  - transforms │  │  - last run  │  │  - success   │  │  - throughput│  │  │
│  │  │  - schedule   │  │              │  │  - failed    │  │              │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                     Message Queue Layer                                     │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │  Queue        │  │  Topic       │  │  Subscription│  │  Dead Letter │  │  │
│  │  │  Manager      │  │  Router      │  │  Manager     │  │  Queue       │  │  │
│  │  │               │  │              │  │              │  │              │  │  │
│  │  │  - P2P        │  │  - filter    │  │  - subscribe │  │  - failed    │  │  │
│  │  │  - Pub/Sub    │  │  - route     │  │  - unsubscribe│ │  - retry     │  │  │
│  │  │  - FIFO       │  │  - partition │  │  - wildcard  │  │  - inspect   │  │  │
│  │  │  - Priority   │  │              │  │              │  │              │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                       Webhook Layer                                         │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                    │  │
│  │  │  Webhook      │  │  Event       │  │  Delivery    │                    │  │
│  │  │  Registry     │  │  Router      │  │  Tracker     │                    │  │
│  │  │               │  │              │  │              │                    │  │
│  │  │  - register   │  │  - match     │  │  - success   │                    │  │
│  │  │  - secrets    │  │  - filter    │  │  - failure   │                    │  │
│  │  │  - retry      │  │  - fan-out   │  │  - latency   │                    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                    │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Component Deep-Dive

### API Orchestration Engine

#### Connection Management

Each external system is registered as a `SystemConnection` with authentication credentials, timeout settings, retry configuration, and health check endpoints.

```python
conn = api_engine.add_connection(
    name="Salesforce",
    base_url="https://api.salesforce.com",
    auth_type=AuthType.OAUTH2,
    timeout=30,
    max_retries=3,
    retry_strategy=RetryStrategy.EXPONENTIAL,
    rate_limit_per_second=100,
    health_check_url="/health",
)
```

#### Circuit Breaker Implementation

The circuit breaker prevents cascading failures by tracking consecutive failures per connection.

```
State Transitions:
  CLOSED ──[failures >= threshold]──→ OPEN
  OPEN ──[timeout elapsed]──→ HALF_OPEN
  HALF_OPEN ──[success]──→ CLOSED
  HALF_OPEN ──[failure]──→ OPEN

Configuration:
  failure_threshold: 5 (default)
  timeout_seconds: 60 (default)
```

#### Retry Strategy Formulas

| Strategy | Delay Calculation | Use Case |
|----------|-------------------|----------|
| FIXED | delay = base | APIs with fixed rate limits |
| EXPONENTIAL | delay = base × 2^attempt | General purpose backoff |
| LINEAR | delay = base × (attempt + 1) | Progressive backoff |
| FIBONACCI | delay = base × fib(attempt) | Balanced between aggressive and conservative |

#### Orchestration Flow Execution

Multi-step flows execute sequentially, stopping on the first failure:

```
steps = [
    {"connection_id": "salesforce", "method": "GET", "path": "/contacts"},
    {"connection_id": "hubspot", "method": "POST", "path": "/contacts"},
]

flow_result = api_engine.orchestrate_flow(steps)
# Returns: flow_id, steps_completed, failed, duration_ms, per-step results
```

### Data Transformation Engine

#### Transform Pipeline

Transformations execute in sequence, each receiving the output of the previous step:

```
Raw Data → MAP → NORMALIZE → FILTER → VALIDATE → Clean Data
```

#### Supported Transform Types

**MAP** — Rename and reorder fields:
```python
result = engine.map_fields(data, {"old_name": "new_name", "keep_field": "keep_field"})
```

**FILTER** — Include or exclude fields:
```python
result = engine.filter_fields(data, include_fields=["name", "email"])
result = engine.filter_fields(data, exclude_fields=["internal_id", "debug"])
```

**NORMALIZE** — Apply value transformations:
```python
rules = {
    "email": {"type": "lowercase"},
    "phone": {"type": "regex_replace", "pattern": r"[^\d]", "replacement": ""},
    "age": {"type": "cast", "target": "int"},
    "name": {"type": "trim"},
    "status": {"type": "default", "value": "unknown"},
}
result = engine.normalize_data(data, rules)
```

**DEDUPLICATE** — Remove duplicate records:
```python
unique = engine.deduplicate(records, key_fields=["email", "domain"])
```

**AGGREGATE** — Group and compute:
```python
aggregated = engine.aggregate_data(
    records=records,
    group_by=["region", "quarter"],
    aggregations={"revenue": "sum", "deals": "count", "avg_deal": "avg"},
)
```

#### Format Conversion

Supports bidirectional conversion between JSON, XML, CSV, and YAML:

```python
json_str = engine.convert_format(csv_data, DataFormat.CSV, DataFormat.JSON)
csv_str = engine.convert_format(json_data, DataFormat.JSON, DataFormat.CSV)
```

### ETL Pipeline Manager

#### Pipeline Execution Flow

```
1. Pipeline triggered (manual or cron)
2. Create PipelineRun record (status: PENDING)
3. Set status to RUNNING
4. Execute extraction phase
5. Execute transformation steps
6. Execute loading phase
7. Record final counts (extracted, transformed, loaded, failed)
8. Set status to SUCCESS or FAILED
9. Update pipeline aggregate metrics
```

#### Metrics Tracking

Each pipeline maintains rolling statistics:
```python
metrics = etl_manager.get_pipeline_metrics(pipeline_id)
# Returns: success_rate, avg_duration, total_records, last_run, next_run
```

### Message Queue Manager

#### Queue Type Behaviors

**Point-to-Point**: Each message delivered to exactly one consumer. Used for task distribution.

**Publish-Subscribe**: Each message delivered to all subscribers. Used for event broadcasting.

**FIFO**: Messages delivered in strict order. Used for sequence-dependent processing.

**Priority**: Higher-priority messages delivered first. Used for urgent notifications.

**Dead-Letter**: Captures messages that fail processing after retry exhaustion.

#### Message Flow

```
Publisher → Topic/Queue → [Filter] → Subscription → Consumer Queue → Consumer
                                            │
                                      [on failure]
                                            │
                                            ↓
                                    Dead Letter Queue
```

### Webhook Manager

#### Webhook Lifecycle

```
1. Register webhook (URL, events, secret)
2. Event occurs in system
3. Event router matches event type to registered webhooks
4. For each matching webhook:
   a. Construct payload with event data
   b. Sign payload with HMAC using webhook secret
   c. POST to webhook URL
   d. Record delivery status (success/failure, latency)
5. On failure: apply retry policy (exponential backoff)
6. Log all delivery attempts for audit
```

## Data Flow: End-to-End Integration

### Cross-System Data Synchronization

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Source   │───→│  API     │───→│ Transform│───→│  Dest    │
│  System   │    │  Call    │    │  Engine  │    │  System  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
      │               │               │               │
      │          ┌────▼────┐    ┌─────▼─────┐    ┌───▼────┐
      │          │ Circuit │    │ Validation│    │Webhook │
      │          │ Breaker │    │ & Logging │    │Notify  │
      │          └─────────┘    └───────────┘    └────────┘
      │
  ┌───▼────┐
  │Health  │
  │Check   │
  └────────┘
```

### ETL + Queue Fan-Out

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Schedule │───→│ Extract  │───→│Transform │───→│   Load   │
│ Trigger  │    │          │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └────┬─────┘
                                                      │
                                               ┌──────▼──────┐
                                               │   Message   │
                                               │   Queue     │
                                               └──────┬──────┘
                                                      │
                              ┌────────────────────────┼────────────────────────┐
                              │                        │                        │
                       ┌──────▼──────┐          ┌──────▼──────┐          ┌──────▼──────┐
                       │  Consumer A │          │  Consumer B │          │  Consumer C │
                       │  (CRM)      │          │  (Analytics)│          │  (Billing)  │
                       └─────────────┘          └─────────────┘          └─────────────┘
```

## Security Model

- OAuth2 tokens stored per-connection, refreshed automatically
- Webhook payloads signed with HMAC-SHA256
- API keys and secrets never logged
- TLS required for all external connections
- Rate limiting prevents abuse and protects downstream systems
- Circuit breaker prevents resource exhaustion during outages

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| API call overhead | < 100ms | Excluding network latency |
| Transform throughput | > 10K records/sec | Single-threaded |
| ETL pipeline (10K records) | < 5s | End-to-end |
| Queue publish latency | < 10ms p99 | In-memory queues |
| Webhook delivery | < 500ms p95 | Including network |
| Circuit breaker detection | < 1s | From failure to open |

## Extension Points

- Custom transform types via the `TransformType` enum
- New auth types via the `AuthType` enum
- Custom retry strategies by extending `RetryStrategy`
- Pipeline step plugins via the transform pipeline interface
- Webhook signature algorithms via configuration
