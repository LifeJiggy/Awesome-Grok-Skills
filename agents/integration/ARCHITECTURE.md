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
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                     Observability Layer                                     │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │  Structured  │  │  Metrics     │  │  Audit       │  │  Alert       │  │  │
│  │  │  Logging     │  │  Collector   │  │  Trail       │  │  Engine      │  │  │
│  │  │              │  │              │  │              │  │              │  │  │
│  │  │  - JSON      │  │  - counters  │  │  - who/when  │  │  - thresholds│  │  │
│  │  │  - levels    │  │  - gauges    │  │  - what      │  │  - channels  │  │  │
│  │  │  - context   │  │  - histograms│  │  - result    │  │  - escalation│  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │  │
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

#### Authentication Methods

| Auth Type | Token Location | Refresh | Use Case |
|-----------|---------------|---------|----------|
| API_KEY | Header or query param | Manual | SaaS services, partner APIs |
| OAUTH2 | Authorization header | Auto-refresh | Enterprise SaaS, Google, Salesforce |
| BASIC | Base64-encoded header | Per-session | Legacy systems, internal tools |
| BEARER | Authorization header | Per-token | REST APIs, microservices |
| MUTUAL_TLS | Client certificate | Certificate rotation | Financial, healthcare APIs |
| HMAC | Request signature | Per-request | Webhooks, payment gateways |
| JWT | Signed token | Auto-refresh | Service-to-service, Kubernetes |

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

**Circuit Breaker Metrics:**

| Metric | Description |
|--------|-------------|
| total_failures | Total failures recorded since creation |
| consecutive_failures | Current consecutive failure count |
| last_failure_time | Timestamp of last failure |
| state_changes | Count of state transitions |
| success_rate | Rolling 1-minute success percentage |

#### Retry Strategy Formulas

| Strategy | Delay Calculation | Use Case |
|----------|-------------------|----------|
| FIXED | delay = base | APIs with fixed rate limits |
| EXPONENTIAL | delay = base × 2^attempt | General purpose backoff |
| LINEAR | delay = base × (attempt + 1) | Progressive backoff |
| FIBONACCI | delay = base × fib(attempt) | Balanced between aggressive and conservative |

**Retry Decision Tree:**
```
Request fails
  │
  ├─ Is it a 4xx client error (not 429)?
  │   └─ Yes → Do NOT retry (bad request)
  │
  ├─ Is it a 429 (rate limited)?
  │   └─ Yes → Use Retry-After header or exponential backoff
  │
  ├─ Is it a 5xx server error?
  │   └─ Yes → Apply retry strategy
  │
  ├─ Is it a network timeout?
  │   └─ Yes → Apply retry strategy with longer delay
  │
  └─ Is it a connection refused?
      └─ Yes → Apply retry strategy, check circuit breaker
```

#### Rate Limiting

Rate limiting is enforced per connection to prevent abuse and protect downstream systems.

```python
rate_limiter = RateLimiter(
    max_requests=100,
    window_seconds=1,
    strategy="sliding_window",  # fixed_window, sliding_window, token_bucket
)

# Rate limit behavior
@rate_limiter.limit("salesforce")
def call_salesforce():
    ...
```

#### Orchestration Flow Execution

Multi-step flows execute sequentially, stopping on the first failure:

```python
steps = [
    {"connection_id": "salesforce", "method": "GET", "path": "/contacts"},
    {"connection_id": "hubspot", "method": "POST", "path": "/contacts"},
]

flow_result = api_engine.orchestrate_flow(steps)
# Returns: flow_id, steps_completed, failed, duration_ms, per-step results
```

**Flow Execution Patterns:**

| Pattern | Description | Use Case |
|---------|-------------|----------|
| SEQUENTIAL | Steps run one after another | Dependent steps |
| PARALLEL | Steps run simultaneously | Independent steps |
| PIPELINE | Output of step N feeds step N+1 | Data transformation chains |
| CONDITIONAL | Steps run based on previous results | Branching logic |
| SAGA | Compensating transactions on failure | Distributed transactions |

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

**JOIN** — Merge two datasets:
```python
joined = engine.join_datasets(
    left=customers,
    right=orders,
    left_key="customer_id",
    right_key="customer_id",
    join_type="left",  # inner, left, right, full
)
```

**ENRICH** — Add computed fields:
```python
enriched = engine.enrich_data(
    records=records,
    computed_fields={
        "full_name": lambda r: f"{r['first_name']} {r['last_name']}",
        "is_vip": lambda r: r.get("total_spent", 0) > 10000,
    },
)
```

**VALIDATE** — Schema validation:
```python
schema = {
    "email": {"type": "str", "required": True, "pattern": r"^[\w.-]+@[\w.-]+\.\w+$"},
    "age": {"type": "int", "min": 0, "max": 150},
    "name": {"type": "str", "required": True, "min_length": 1},
}
result = engine.validate_data(data, schema)
```

#### Format Conversion

Supports bidirectional conversion between JSON, XML, CSV, and YAML:

```python
json_str = engine.convert_format(csv_data, DataFormat.CSV, DataFormat.JSON)
csv_str = engine.convert_format(json_data, DataFormat.JSON, DataFormat.CSV)
```

**Format Conversion Matrix:**

| Source | JSON | XML | CSV | YAML |
|--------|------|-----|-----|------|
| JSON | - | Yes | Yes | Yes |
| XML | Yes | - | Yes | Yes |
| CSV | Yes | Yes | - | No |
| YAML | Yes | Yes | No | - |

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

**Pipeline State Machine:**
```
DRAFT → ACTIVE → RUNNING → SUCCESS
                       ↘ FAILED
ACTIVE → PAUSED → ACTIVE
ACTIVE → ARCHIVED
```

#### Extraction Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| FULL_DUMP | Extract all records | Small datasets, initial load |
| INCREMENTAL | Extract since last sync | Large datasets, regular sync |
| CHANGE_DATA_CAPTURE | Only changed records | Real-time sync, audit trail |
| QUERY_BASED | Parameterized extraction | Reporting, analytics |
| WEBHOOK_TRIGGERED | Event-driven extraction | Real-time sync |

#### Loading Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| INSERT | Append only | Logs, events, history |
| UPSERT | Insert or update | CRM sync, user data |
| REPLACE | Overwrite target | Reporting, snapshots |
| DELETE_INSERT | Delete and re-insert | Full refresh |
| MERGE | Smart merge with logic | Complex business rules |

#### Metrics Tracking

Each pipeline maintains rolling statistics:
```python
metrics = etl_manager.get_pipeline_metrics(pipeline_id)
# Returns: success_rate, avg_duration, total_records, last_run, next_run
```

**Pipeline Metrics Schema:**

| Metric | Type | Description |
|--------|------|-------------|
| pipeline_id | str | Unique pipeline identifier |
| total_runs | int | Number of executions |
| successful_runs | int | Number of successful runs |
| failed_runs | int | Number of failed runs |
| success_rate | float | Percentage of successful runs |
| avg_duration_seconds | float | Average run duration |
| total_records_extracted | int | Total records extracted |
| total_records_loaded | int | Total records loaded |
| last_run_timestamp | datetime | When the pipeline last ran |
| next_scheduled_run | datetime | When the pipeline is next scheduled |

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

**Message Lifecycle:**
```
PUBLISHED → DELIVERED → PROCESSED
           ↘ FAILED → RETRY → PROCESSED
                      ↘ FAILED (max retries) → DEAD_LETTER
```

#### Dead Letter Queue Management

```python
# Monitor dead letter queue
dlq_messages = queue_manager.get_dead_letter_messages(queue_id="Q-XXX")

# Retry failed messages
for msg in dlq_messages:
    queue_manager.retry_message(msg.message_id)

# Inspect and manually route
msg = queue_manager.inspect_message(msg_id="MSG-XXX")
queue_manager.route_message(msg, target_queue_id="Q-YYY")
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

**Webhook Security Model:**
```
Request Construction:
  Headers:
    Content-Type: application/json
    X-Webhook-Signature: HMAC-SHA256(secret, payload)
    X-Webhook-ID: unique-delivery-id
    X-Webhook-Timestamp: unix-timestamp

  Body:
    {
      "event": "contact.created",
      "timestamp": "2026-01-15T10:30:00Z",
      "data": { ... }
    }
```

**Delivery Retry Policy:**
| Attempt | Delay | Max |
|---------|-------|-----|
| 1 | 0s | Immediate |
| 2 | 1s | Exponential |
| 3 | 4s | Exponential |
| 4 | 16s | Exponential |
| 5 | 64s | Exponential (final) |

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

### Error Handling Flow

```
Operation fails
  │
  ├─ Transient error?
  │   ├─ Yes → Retry with backoff
  │   │         ├─ Retries exhausted → Dead letter queue
  │   │         └─ Success → Continue
  │   └─ No → Circuit breaker opens
  │
  ├─ Circuit breaker open?
  │   ├─ Yes → Wait for timeout → Half-open → Test request
  │   │         ├─ Success → Close circuit
  │   │         └─ Failure → Open circuit
  │   └─ No → Allow request
  │
  └─ Log error with context
      │
      ├─ Alert if threshold exceeded
      └─ Update metrics
```

## Security Model

- OAuth2 tokens stored per-connection, refreshed automatically
- Webhook payloads signed with HMAC-SHA256
- API keys and secrets never logged
- TLS required for all external connections
- Rate limiting prevents abuse and protects downstream systems
- Circuit breaker prevents resource exhaustion during outages

**Security Controls Matrix:**

| Control | Scope | Implementation |
|---------|-------|----------------|
| TLS 1.2+ | All external connections | Enforced at connection level |
| OAuth2 | Token-based auth | Auto-refresh with refresh tokens |
| HMAC-SHA256 | Webhook payloads | Per-webhook secret |
| Rate Limiting | Per-connection | Sliding window algorithm |
| Audit Logging | All operations | Structured JSON logs |
| Secret Redaction | All logs | Automatic pattern matching |

## Scalability

| Dimension | Capacity | Notes |
|-----------|----------|-------|
| Connections | 100+ | Per connection pool |
| Transform throughput | >10K records/sec | Single-threaded |
| ETL pipelines | 50+ concurrent | Thread pool managed |
| Queue throughput | >100K msg/sec | In-memory queues |
| Webhooks | 1000+ registrations | Fan-out delivery |

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| API call overhead | < 100ms | Excluding network latency |
| Transform throughput | > 10K records/sec | Single-threaded |
| ETL pipeline (10K records) | < 5s | End-to-end |
| Queue publish latency | < 10ms p99 | In-memory queues |
| Webhook delivery | < 500ms p95 | Including network |
| Circuit breaker detection | < 1s | From failure to open |

## Design Patterns

### Circuit Breaker Pattern
Prevents cascading failures by tracking consecutive failures and temporarily blocking requests to unhealthy systems.

### Retry with Backoff
Handles transient failures by retrying with increasing delays to avoid overwhelming the target system.

### Dead Letter Queue
Captures messages that cannot be processed for later inspection and manual handling.

### Facade Pattern
The `IntegrationAgent` class provides a unified interface to all engines, hiding internal complexity.

### Pipeline Pattern
ETL and transform operations are composed as sequential steps, each receiving the output of the previous step.

### Observer Pattern
Webhooks and event routing use observer-like patterns to decouple event producers from consumers.

## Extension Points

- Custom transform types via the `TransformType` enum
- New auth types via the `AuthType` enum
- Custom retry strategies by extending `RetryStrategy`
- Pipeline step plugins via the transform pipeline interface
- Webhook signature algorithms via configuration
- Custom queue consumers via the consumer interface
- New data format converters via the format converter registry

## Configuration Reference

```yaml
api_orchestration:
  default_timeout: 30
  default_max_retries: 3
  default_retry_strategy: exponential
  circuit_breaker:
    failure_threshold: 5
    timeout_seconds: 60
    half_open_max_attempts: 1
  rate_limiting:
    default_requests_per_second: 100
    strategy: sliding_window

data_transformation:
  default_encoding: utf-8
  max_record_size_bytes: 1048576
  validation_mode: strict  # strict, lenient

etl_pipelines:
  max_concurrent_pipelines: 10
  default_schedule: "0 */6 * * *"
  run_timeout_seconds: 3600
  retry_failed_runs: true

message_queues:
  default_ttl_seconds: 3600
  max_queue_size: 1000000
  max_message_size_bytes: 1048576
  dead_letter_max_size: 10000

webhooks:
  default_max_retries: 3
  delivery_timeout_seconds: 30
  signature_algorithm: hmac-sha256
  max_payload_size_bytes: 1048576
```
