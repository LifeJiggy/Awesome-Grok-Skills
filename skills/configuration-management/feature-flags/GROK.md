---
name: "feature-flags"
category: "configuration-management"
version: "2.0.0"
tags: ["configuration-management", "feature-flags", "feature-toggles", "rollout", "A/B-testing"]
---

# Feature Flags

## Overview

The Feature Flags module provides tools for managing feature toggles, gradual rollouts, A/B testing, and kill switches. It covers flag lifecycle management, targeting rules, percentage rollouts, user segmentation, and flag analytics. The module supports operational flags, experiment flags, and permission flags patterns.

This skill is essential for product engineers, release managers, and platform teams implementing progressive delivery and feature flag-driven development.

## Core Capabilities

- **Flag Management**: Create, update, archive feature flags with lifecycle tracking
- **Targeting Rules**: User segment targeting, attribute-based rules, and percentage rollouts
- **A/B Testing**: Experiment assignment, variant management, and statistical significance tracking
- **Kill Switches**: Emergency feature disable, circuit breaker patterns, and degraded mode activation
- **Scheduled Rollouts**: Time-based flag scheduling, phased rollouts, and calendar-based releases
- **Analytics**: Flag usage tracking, impression counting, and conversion attribution
- **Multi-Environment**: Flag configuration per environment (dev, staging, production)
- **SDK Integration**: Client-side and server-side flag evaluation patterns

## Usage Examples

```python
from feature_flags import (
    FlagManager,
    TargetingEngine,
    ExperimentRunner,
    RolloutScheduler,
    FlagAnalytics,
)

# --- Flag Management ---
manager = FlagManager()
flag = manager.create_flag(
    key="new_checkout_flow",
    name="New Checkout Flow",
    description="Redesigned checkout experience",
    default_value=False,
    flag_type="boolean",
)
print(f"Flag: {flag.key}")
print(f"Status: {flag.status}")

# --- Targeting ---
engine = TargetingEngine()
engine.set_targeting(
    flag_key="new_checkout_flow",
    rules=[
        {"attribute": "country", "operator": "in", "values": ["US", "CA"]},
        {"attribute": "beta_user", "operator": "equals", "value": True},
    ],
    percentage_rollout=25,
)
is_enabled = engine.evaluate(
    flag_key="new_checkout_flow",
    context={"user_id": "u123", "country": "US", "beta_user": True},
)
print(f"Flag enabled for user: {is_enabled}")

# --- A/B Testing ---
runner = ExperimentRunner()
experiment = runner.create_experiment(
    flag_key="new_checkout_flow",
    variants=[
        {"name": "control", "weight": 50},
        {"name": "treatment", "weight": 50},
    ],
    primary_metric="conversion_rate",
)
print(f"Experiment: {experiment.experiment_id}")
print(f"Variants: {[v['name'] for v in experiment.variants]}")

# --- Rollout Scheduler ---
scheduler = RolloutScheduler()
schedule = scheduler.schedule_rollout(
    flag_key="new_checkout_flow",
    phases=[
        {"percentage": 10, "duration_hours": 24},
        {"percentage": 25, "duration_hours": 48},
        {"percentage": 50, "duration_hours": 72},
        {"percentage": 100, "duration_hours": 0},
    ],
)
print(f"Rollout phases: {len(schedule.phases)}")

# --- Analytics ---
analytics = FlagAnalytics()
analytics.record_impression("new_checkout_flow", "u123", variant="treatment")
stats = analytics.get_stats("new_checkout_flow")
print(f"Impressions: {stats.impressions}")
print(f"Unique users: {stats.unique_users}")
```

## Best Practices

- Separate operational flags (kill switches) from release flags (new features) Ã¢â‚¬â€ different lifecycle
- Use flag key naming convention: `team.feature_name` (e.g., `payments.new_checkout`)
- Set flag expiration dates Ã¢â‚¬â€ stale flags accumulate technical debt
- Implement flag cleanup automation Ã¢â‚¬â€ remove flags after full rollout
- Use targeting rules with fallthrough values for reliable evaluation
- Log all flag evaluations for debugging and audit trails
- Implement flag hooks for analytics integration
- Test flag states in CI/CD Ã¢â‚¬â€ test with flag ON and OFF
- Use gradual rollouts (10% -> 25% -> 50% -> 100%) for high-risk features
- Document all flags with owner, purpose, and expected cleanup date

## Related Modules

- **dynamic-config**: Runtime configuration changes
- **config-ops**: Configuration management patterns
- **environment-config**: Environment-specific flag settings
- **secrets-management**: Secret flag values management

---

## Advanced Configuration

### Flag Evaluation Architecture

Feature flag evaluation follows a layered resolution order: defaults, environment overrides, targeting rules, and experiment assignments. Understanding this hierarchy prevents unintended flag states.

```python
# Resolution order: Environment > Targeting > Default
evaluator = FlagEvaluator(
    resolution_order=["environment", "targeting", "experiment", "default"],
    cache_ttl_seconds=30,
)

# Multi-layer configuration
evaluator.configure({
    "new_checkout_flow": {
        "default": False,
        "environments": {
            "development": True,
            "staging": True,
            "production": False,
        },
        "targeting": [
            {"attribute": "user_id", "operator": "in", "values": ["internal-testers"]},
        ],
    }
})
```

### Prerequisite Flags

Flags can depend on other flags being enabled. This creates dependency chains for complex feature rollouts.

```python
flag_manager.create_flag(
    key="payments.new_ui",
    prerequisites=[{"flag_key": "payments.backend_v2", "variation": True}],
    default_value=False,
)
```

### Flag Scheduling

Schedule flag state transitions for time-based releases.

```python
scheduler.configure_flag_schedule(
    flag_key="holiday_theme",
    schedule=[
        {"state": True, "at": "2024-12-20T00:00:00Z", "environments": ["production"]},
        {"state": False, "at": "2025-01-02T00:00:00Z", "environments": ["production"]},
    ],
)
```

### Custom Scopes

Define custom scopes for flag targeting beyond standard user attributes.

```python
scope = CustomScope(
    name="subscription_tier",
    attributes=["free", "pro", "enterprise"],
    resolver=lambda ctx: ctx.get("subscription", "free"),
)
engine.register_scope(scope)
```

---

## Architecture Patterns

### Flag-as-Code Pattern

Store flag definitions in version control alongside application code for auditability and review.

```
flags/
  definitions/
    payments.yaml       # Flag definitions
    search.yaml
  targeting/
    payments.yaml       # Targeting rules
    search.yaml
  experiments/
    checkout_test.yaml  # Experiment configs
```

### GitOps Flag Management

Manage flag changes through Git workflows with pull request reviews.

```yaml
# .github/workflows/flag-deploy.yml
on:
  push:
    paths: ['flags/**']
jobs:
  deploy-flags:
    steps:
      - uses: actions/checkout@v4
      - run: flag-cli validate flags/
      - run: flag-cli deploy flags/ --environment production
```

### Multi-Tenant Flag Architecture

Isolate flag configurations per tenant for SaaS platforms.

```python
tenant_resolver = TenantFlagResolver(
    default_tenant="global",
    tenant_overrides_path="/etc/flags/tenants/",
)
# Tenant-specific overrides
tenant_resolver.set_override(
    tenant_id="enterprise-acme",
    flag_key="advanced_analytics",
    value=True,
)
```

### Event-Driven Flag Updates

React to flag changes through event streams for real-time system coordination.

```python
flag_events = FlagEventStream()
flag_events.on_change("payments.new_checkout", callback=lambda e: rebuild_cache())
flag_events.on_rollout_progress("payments.new_checkout", callback=lambda e: update_metrics(e.percentage))
```

---

## Integration Guide

### Backend SDK Integration

```python
# Python SDK initialization
from feature_flags_sdk import Client

client = Client(
    sdk_key="sdk-abc123",
    environment="production",
    event_processor=HTTPEventProcessor(endpoint="https://events.featureflags.io"),
)
client.initialize()

# Evaluate flag
if client.bool_var("new_checkout_flow", default=False, context={"user_id": "u123"}):
    render_new_checkout()
```

### Frontend SDK Integration

```javascript
// JavaScript SDK initialization
import { initialize } from '@featureflags/js-sdk';

const client = await initialize({
  sdkKey: 'sdk-abc123',
  environment: 'production',
  streaming: true,
});

// Evaluate flag with default fallback
const showNewUI = client.variation('new_ui_flag', false);
```

### CI/CD Pipeline Integration

```yaml
# Feature flag validation in CI
- name: Validate Flags
  run: |
    flag-cli validate --path ./flags --schema ./schemas/flag-schema.json
    flag-cli test --path ./flags --test-cases ./tests/flag-tests.yaml

- name: Check Flag Cleanup
  run: |
    flag-cli stale-flags --max-age-days 90 --fail-on-stale
```

### Mobile SDK Integration

```swift
// iOS SDK
let client = FFLagClient(sdkKey: "sdk-abc123")
client.start()

let showBanner = client.boolVariation("mobile_banner", false, context: userContext)
```

---

## Performance Optimization

### Flag Evaluation Caching

Cache flag evaluations to reduce SDK overhead and improve latency.

```python
cache = EvaluationCache(
    backend="redis",
    ttl_seconds=60,
    max_entries=10000,
    eviction="lru",
)
evaluator.set_cache(cache)

# Evaluation with cache: ~0.1ms vs ~5ms without cache
result = evaluator.evaluate("flag_key", context)
```

### Bulk Evaluation

Evaluate multiple flags in a single SDK call to reduce network round trips.

```python
flags = client.evaluate_all(context=user_context)
# Returns dict of flag_key -> value pairs
# Single network call instead of N calls
```

### Client-Side Streaming

Use Server-Sent Events for real-time flag updates without polling.

```python
streaming = StreamingConfig(
    enabled=True,
    reconnect_delay_ms=1000,
    max_reconnect_attempts=10,
)
client = Client(sdk_key=key, streaming=streaming)
```

### Flag Evaluation Profiling

Profile flag evaluation to identify slow targeting rules.

```python
profiler = FlagProfiler()
report = profiler.profile(evaluator, context_samples, n_iterations=1000)
print(f"P50 latency: {report.p50_us:.1f}us")
print(f"P99 latency: {report.p99_us:.1f}us")
print(f"Slowest rule: {report.slowest_rule}")
```

---

## Security Considerations

### Flag Data Classification

Classify flags by sensitivity level and apply appropriate access controls.

```python
FlagSecurityPolicy(
    classification_rules=[
        {"pattern": "admin.*", "level": "confidential", "requires_approval": True},
        {"pattern": "payment.*", "level": "sensitive", "audit_logging": True},
        {"pattern": "ui.*", "level": "internal"},
    ],
)
```

### Audit Logging

Log all flag changes for compliance and incident investigation.

```python
audit_logger = FlagAuditLogger(
    storage="s3://audit-logs/flags/",
    retention_days=365,
    fields=["flag_key", "old_value", "new_value", "changed_by", "timestamp"],
)
```

### Access Control

Implement role-based access for flag management operations.

```python
access_policy = FlagAccessPolicy(
    roles={
        "viewer": ["read"],
        "developer": ["read", "update_targeting"],
        "admin": ["read", "update_targeting", "create", "archive"],
    },
)
```

### Flag Secret Protection

Prevent sensitive flag values from being logged or exposed.

```python
client = Client(
    redact_log_fields=["api_key_flag", "secret_config"],
    mask_evaluations=True,
)
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Flag not evaluating | SDK not initialized | Call `client.initialize()` before evaluation |
| Stale flag values | Cache TTL too long | Reduce cache TTL or force refresh |
| Flag variation mismatch | Wrong context | Verify context attributes match targeting rules |
| High latency | No caching enabled | Enable evaluation cache |
| Experiment data missing | Event processor down | Check event processor health |
| Flag stuck in default | Prerequisite not met | Check prerequisite flag states |

### Debug Mode

Enable debug logging for flag evaluation diagnostics.

```python
import logging
logging.getLogger("feature_flags").setLevel(logging.DEBUG)

# Evaluation debug output
# [DEBUG] Evaluating flag 'new_checkout_flow' for user 'u123'
# [DEBUG] Environment: production (override: False)
# [DEBUG] Targeting rule 1: country IN [US, CA] -> MATCH
# [DEBUG] Targeting rule 2: beta_user == True -> NO MATCH
# [DEBUG] Fallthrough: False
# [DEBUG] Result: False (0.3ms)
```

### Flag Health Dashboard

Monitor flag health metrics for operational awareness.

```python
health = FlagHealthChecker()
status = health.check_all()
print(f"Total flags: {status.total}")
print(f"Stale flags: {status.stale_count}")
print(f"Flags without owner: {status.orphaned_count}")
print(f"Evaluation error rate: {status.error_rate:.2%}")
```

### Rollback Procedures

Emergency flag rollback in case of incidents.

```python
# Instant rollback to default values
client.emergency_disable(
    flag_keys=["new_checkout_flow", "experimental_search"],
    reason="Incident #1234 - checkout failures",
    notify=["#ops-alerts"],
)
```

---

## API Reference

### FlagManager

```python
class FlagManager:
    def create_flag(key: str, name: str, description: str,
                    default_value: Any, flag_type: str) -> Flag
    def update_flag(key: str, **kwargs) -> Flag
    def archive_flag(key: str, reason: str) -> None
    def get_flag(key: str) -> Flag
    def list_flags(filters: dict = None) -> List[Flag]
```

### TargetingEngine

```python
class TargetingEngine:
    def set_targeting(flag_key: str, rules: List[dict],
                      percentage_rollout: int = 100) -> None
    def evaluate(flag_key: str, context: dict) -> bool
    def evaluate_all(context: dict) -> Dict[str, bool]
    def get_serve_for_user(flag_key: str, user_hash: str) -> str
```

### ExperimentRunner

```python
class ExperimentRunner:
    def create_experiment(flag_key: str, variants: List[dict],
                          primary_metric: str) -> Experiment
    def assign_variant(experiment_id: str, user_id: str) -> str
    def record_metric(experiment_id: str, user_id: str,
                      metric_name: str, value: float) -> None
    def get_results(experiment_id: str) -> ExperimentResults
```

### FlagAnalytics

```python
class FlagAnalytics:
    def record_impression(flag_key: str, user_id: str,
                          variant: str = None) -> None
    def record_conversion(flag_key: str, user_id: str,
                          metric: str, value: float) -> None
    def get_stats(flag_key: str, period: str = "7d") -> FlagStats
    def get_segment_stats(flag_key: str, segment_by: str) -> SegmentStats
```

---

## Data Models

### Flag

```python
@dataclass
class Flag:
    key: str
    name: str
    description: str
    flag_type: str  # boolean, string, number, json
    default_value: Any
    status: str  # active, archived, stale
    created_at: datetime
    updated_at: datetime
    owner: str
    tags: List[str]
    expiration_date: Optional[datetime]
```

### TargetingRule

```python
@dataclass
class TargetingRule:
    rule_id: str
    attribute: str
    operator: str  # in, not_in, equals, contains, starts_with, regex
    values: List[Any]
    serve: str  # variation to serve when rule matches
    priority: int
```

### Experiment

```python
@dataclass
class Experiment:
    experiment_id: str
    flag_key: str
    variants: List[Variant]
    primary_metric: str
    status: str  # running, paused, completed
    started_at: datetime
    ended_at: Optional[datetime]
    sample_size: int
    statistical_significance: Optional[float]
```

---

## Deployment Guide

### Infrastructure Requirements

- Feature flag service: 2+ replicas for high availability
- Redis cache cluster: For flag evaluation caching
- Event processor: For analytics event ingestion
- Message queue: Kafka or RabbitMQ for event streaming

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: feature-flag-service
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: flag-service
          image: featureflags/server:latest
          ports:
            - containerPort: 8080
          env:
            - name: SDK_KEY
              valueFrom:
                secretKeyRef:
                  name: flag-secrets
                  key: sdk-key
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
```

### Multi-Region Deployment

Deploy flag infrastructure across regions for low-latency evaluation.

```python
region_config = MultiRegionConfig(
    primary_region="us-east-1",
    replica_regions=["eu-west-1", "ap-southeast-1"],
    replication_mode="async",
    conflict_resolution="last_writer_wins",
)
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `flag.evaluation.latency.p99` | P99 evaluation latency | > 10ms |
| `flag.evaluation.error_rate` | Evaluation failure rate | > 0.1% |
| `flag.update.propagation_delay` | Time for flag change to propagate | > 30s |
| `flag.stale.count` | Number of stale flags | > 10 |
| `flag.experiment.participation_rate` | Experiment participation rate | < 10% |

### Dashboards

```python
# Grafana dashboard configuration
dashboard = GrafanaDashboard(
    title="Feature Flags Overview",
    panels=[
        Panel("Evaluation Latency", query="histogram_quantile(0.99, flag_evaluation_duration_seconds)"),
        Panel("Active Flags", query="count(feature_flag_status{status='active'})"),
        Panel("Error Rate", query="rate(flag_evaluation_errors_total[5m])"),
    ],
)
```

### Alerting Rules

```yaml
groups:
  - name: feature-flags
    rules:
      - alert: HighFlagErrorRate
        expr: rate(flag_evaluation_errors_total[5m]) > 0.001
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High feature flag evaluation error rate"
```

---

## Testing Strategy

### Unit Testing Flag Evaluation

```python
def test_flag_evaluation():
    evaluator = MockEvaluator()
    evaluator.set_flag("test_flag", True)
    context = {"user_id": "test-user"}
    assert evaluator.evaluate("test_flag", context) == True

def test_flag_targeting():
    evaluator = MockEvaluator()
    evaluator.set_targeting("geo_flag", rules=[
        {"attribute": "country", "operator": "in", "values": ["US"]},
    ])
    us_context = {"country": "US"}
    eu_context = {"country": "DE"}
    assert evaluator.evaluate("geo_flag", us_context) == True
    assert evaluator.evaluate("geo_flag", eu_context) == False
```

### Integration Testing

```python
@pytest.mark.integration
def test_flag_end_to_end():
    client = Client(sdk_key="test-key", environment="test")
    client.initialize()
    result = client.bool_var("integration_test_flag", False)
    assert isinstance(result, bool)
```

### Load Testing

```python
def test_flag_evaluation_under_load():
    evaluator = create_evaluator_with_flags(n_flags=1000)
    context = generate_random_contexts(n=10000)
    results = parallel_evaluate(evaluator, context, n_workers=8)
    assert all(r.latency_ms < 10 for r in results)
```

---

## Versioning & Migration

### Flag Schema Versioning

```yaml
# flags/schema/v1/flag.yaml
schema_version: "1.0"
type: object
required: [key, name, flag_type, default_value]
properties:
  key:
    type: string
    pattern: "^[a-z][a-z0-9_]*$"
  flag_type:
    type: string
    enum: [boolean, string, number, json]
```

### Migration Guide

When upgrading flag SDK versions, follow the migration path:

```python
# v1 -> v2 migration
# Old: evaluate_flag("key", context)
# New: client.variation("key", default, context)

# v2 -> v3 migration
# Old: client.variation("key", default, context)
# New: client.variation("key", default, context)  # API stable
# New: Add event processor configuration
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **Flag** | A named toggle that controls feature behavior without code deployment |
| **Variation** | A possible value a flag can serve (e.g., true/false for boolean flags) |
| **Targeting** | Rules that determine which users see which flag variations |
| **Percentage Rollout** | Gradually exposing a flag variation to a percentage of users |
| **Kill Switch** | An operational flag that can instantly disable a feature |
| **Experiment** | A controlled test comparing flag variations for statistical significance |
| **Impression** | A single evaluation of a flag for a specific user context |
| **Fallthrough** | The default variation served when no targeting rules match |
| **Stale Flag** | A flag that has been fully rolled out and should be cleaned up |
| **Flag Key** | The unique identifier for a flag (e.g., `payments.new_checkout`) |

---

## Changelog

### v2.0.0
- Added experiment runner with statistical significance tracking
- New percentage rollout with graduated phases
- Multi-environment flag support
- SDK streaming for real-time flag updates

### v1.5.0
- Added scheduled flag rollouts
- Custom scope support for targeting
- Flag prerequisite chains

### v1.0.0
- Initial release with basic flag management
- Boolean, string, number, and JSON flag types
- Targeting rules with attribute-based conditions
- SDK integration for Python and JavaScript

---

## Contributing Guidelines

### Flag Naming Convention

Follow the `{team}.{feature}.{subfeature}` pattern:

```yaml
# Good
key: payments.new_checkout.flow_v2
key: search.relevance.ranking_algorithm
key: mobile.push_notifications.rate_limit

# Bad
key: my_flag
key: newStuff
key: flag123
```

### Flag Lifecycle

1. **Creation**: Define flag with owner, description, and cleanup date
2. **Development**: Enable in development environment
3. **Testing**: Enable in staging with test targeting rules
4. **Rollout**: Gradual percentage rollout in production
5. **Full Rollout**: 100% rollout
6. **Cleanup**: Remove flag code and archive flag definition

### Code Review Requirements

- All flag changes require peer review
- Targeting rule changes require security review
- Experiment creation requires data science approval
- Flag archival requires owner confirmation

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
