---
name: "Database Monitoring"
version: "2.0.0"
description: "Comprehensive database monitoring toolkit with real-time metrics, alerting, dashboard creation, log aggregation, health checks, and capacity planning for production database operations"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database-admin", "monitoring", "alerting", "dashboards", "health-checks", "capacity-planning"]
category: "database-admin"
personality: "monitoring-engineer"
use_cases: ["real-time monitoring", "alerting", "dashboards", "health checks", "capacity planning"]
---

# Database Monitoring

> Production-grade database monitoring framework providing real-time metrics collection, alerting, dashboard creation, log aggregation, health checks, and capacity planning for comprehensive database observability.

## Overview

The Database Monitoring module provides a complete observability stack for production databases. It implements real-time metric collection (connections, locks, replication, I/O), threshold-based alerting with notification routing, dashboard creation with customizable panels, centralized log aggregation, automated health checks, and capacity planning with trend analysis. Every component includes health self-monitoring and graceful degradation.

## Core Capabilities

### 1. Real-time Metrics Collection
- Connection pool metrics (active, idle, waiting, total)
- Lock metrics (held, waiting, deadlocks)
- Replication lag and throughput
- Cache hit ratios and buffer usage
- Query throughput (TPS, QPS)
- I/O statistics (reads, writes, WAL)
- Disk usage and growth trends

### 2. Alerting System
- Threshold-based alerting (static and dynamic)
- Alert severity levels (info, warning, critical)
- Notification routing (email, Slack, PagerDuty, webhook)
- Alert grouping and deduplication
- Escalation policies
- Alert silencing and maintenance windows

### 3. Dashboard Creation
- Pre-built dashboard templates
- Custom metric visualization
- Real-time chart updates
- Drill-down capabilities
- Dashboard sharing and embedding
- Time-range selection and zoom

### 4. Health Checks
- Automated health check scheduling
- Multi-level health checks (basic, standard, comprehensive)
- Health status aggregation
- Dependency health monitoring
- Health check history and trends

### 5. Log Aggregation
- Centralized log collection
- Log parsing and enrichment
- Full-text search
- Log-based alerting
- Log retention management
- Structured log output

### 6. Capacity Planning
- Resource usage forecasting
- Growth trend analysis
- Capacity threshold alerts
- Cost optimization recommendations
- Scaling recommendation engine

## Usage Examples

### Real-time Metrics

```python
from monitoring import MetricsCollector, MetricType

collector = MetricsCollector(connection_string="postgresql://admin:pass@localhost/prod")

# Collect current metrics
metrics = collector.collect()

print(f"Connections: {metrics.active_connections}/{metrics.max_connections}")
print(f"TPS: {metrics.transactions_per_second:.1f}")
print(f"Cache hit ratio: {metrics.cache_hit_ratio:.3f}")
print(f"Replication lag: {metrics.replication_lag_ms:.0f}ms")
print(f"Disk usage: {metrics.disk_usage_pct:.1f}%")

# Get metric history
history = collector.get_history(
    metric="transactions_per_second",
    hours=24,
)
print(f"Avg TPS (24h): {history.average:.1f}")
print(f"Peak TPS: {history.maximum:.1f}")
```

### Alerting Configuration

```python
from monitoring import AlertManager, AlertRule, Severity

alert_mgr = AlertManager()

# Create alert rules
alert_mgr.add_rule(AlertRule(
    name="high_connections",
    metric="active_connections",
    condition="> 80% of max",
    severity=Severity.WARNING,
    notification_channels=["slack-ops"],
    description="Connection pool near capacity",
))

alert_mgr.add_rule(AlertRule(
    name="replication_lag",
    metric="replication_lag_bytes",
    condition="> 100MB",
    severity=Severity.CRITICAL,
    notification_channels=["pagerduty-oncall", "slack-ops"],
    escalation_policy="dba-oncall",
))

# Check alerts
active_alerts = alert_mgr.check_alerts()
print(f"Active alerts: {len(active_alerts)}")
for alert in active_alerts:
    print(f"  [{alert.severity.value}] {alert.name}: {alert.message}")
```

### Dashboard Creation

```python
from monitoring import DashboardBuilder, PanelType

builder = DashboardBuilder(title="Database Overview")

builder.add_panel(
    panel_type=PanelType.TIME_SERIES,
    title="Transactions Per Second",
    metric="transactions_per_second",
    position=(0, 0),
    size=(2, 1),
)

builder.add_panel(
    panel_type=PanelType.GAUGE,
    title="Cache Hit Ratio",
    metric="cache_hit_ratio",
    thresholds={"warning": 0.95, "critical": 0.90},
    position=(2, 0),
    size=(1, 1),
)

builder.add_panel(
    panel_type=PanelType.TABLE,
    title="Top Slow Queries",
    query="SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10",
    position=(0, 1),
    size=(3, 2),
)

dashboard = builder.build()
dashboard.save("database_overview.json")
```

### Health Checks

```python
from monitoring import HealthChecker, HealthStatus

checker = HealthChecker(connection_string="postgresql://admin:pass@localhost/prod")

# Run health check
health = checker.check(level="comprehensive")

print(f"Overall status: {health.status.value}")
print(f"Checks passed: {health.passed}/{health.total_checks}")

for check in health.checks:
    status_icon = "✓" if check.passed else "✗"
    print(f"  {status_icon} {check.name}: {check.message}")

# Schedule regular checks
checker.schedule(level="standard", interval_minutes=5)
```

### Capacity Planning

```python
from monitoring import CapacityPlanner

planner = CapacityPlanner(connection_string="postgresql://admin:pass@localhost/prod")

# Analyze current capacity
analysis = planner.analyze()

print("Current usage:")
for resource in analysis.resources:
    print(f"  {resource.name}: {resource.current_pct:.1f}% "
          f"(projected 30d: {resource.projected_30d_pct:.1f}%)")

# Get recommendations
recommendations = planner.get_recommendations()
for rec in recommendations:
    print(f"  [{rec.priority}] {rec.description}")
    print(f"    Action: {rec.action}")
```

## Best Practices

### Metrics Collection
- Collect metrics at 10-30 second intervals for production databases
- Monitor all critical metrics: connections, locks, replication, cache, I/O
- Store metric history for at least 30 days for trend analysis
- Use agent-based collection for minimal database impact

### Alerting
- Set alerts for actionable conditions only — avoid alert fatigue
- Use multiple severity levels with appropriate notification routing
- Implement escalation policies for critical alerts
- Test alert notifications regularly

### Dashboards
- Create role-specific dashboards (DBA, developer, management)
- Include both real-time and historical views
- Add drill-down capabilities for investigation
- Keep dashboards focused — one screen per topic

### Health Checks
- Run basic health checks every minute
- Run comprehensive checks every 5-15 minutes
- Monitor health check results for trends
- Include dependency checks (network, storage, replicas)

## Related Modules

- **db-management**: Database configuration and lifecycle management
- **performance-tuning**: Performance analysis and optimization
- **backup-recovery**: Backup monitoring and verification
- **security-hardening**: Security event monitoring

---

## Advanced Configuration

### Advanced Metrics Collection

```python
from monitoring import MetricsCollector, MetricType, CollectionConfig

collector = MetricsCollector(connection_string="postgresql://admin:pass@localhost/prod")

# Configure comprehensive metrics collection
config = CollectionConfig(
    # Core metrics
    include_connections=True,
    include_locks=True,
    include_replication=True,
    include_cache=True,
    include_io=True,
    include_query_stats=True,
    include_table_stats=True,
    include_index_stats=True,
    
    # Collection intervals
    connection_interval=10,
    lock_interval=10,
    replication_interval=5,
    cache_interval=30,
    io_interval=15,
    
    # Sampling
    enable_sampling=True,
    sampling_rate=0.1,  # 10% sampling for high-volume metrics
    
    # Retention
    retention_days=90,
    downsample_after_days=7,
)

collector.configure(config)

# Collect current metrics
metrics = collector.collect()
print(f"Connections: {metrics.connections.active}/{metrics.connections.max}")
print(f"TPS: {metrics.throughput.tps:.1f}")
print(f"Cache hit: {metrics.cache.hit_ratio:.3f}")
print(f"Replication lag: {metrics.replication.lag_ms:.0f}ms")
```

### Advanced Alerting

```python
from monitoring import AlertManager, AlertRule, Severity, NotificationChannel

alert_mgr = AlertManager()

# Configure advanced alerting rules
rules = [
    AlertRule(
        name="high_connections",
        metric="connections.active",
        condition="> {threshold}",
        threshold=80,  # percentage of max
        severity=Severity.WARNING,
        notification_channels=["slack-ops"],
        description="Connection pool near capacity",
        runbook_url="https://runbooks.example.com/high-connections",
    ),
    AlertRule(
        name="replication_lag_critical",
        metric="replication.lag_bytes",
        condition="> {threshold}",
        threshold=100_000_000,  # 100MB
        severity=Severity.CRITICAL,
        notification_channels=["pagerduty-oncall", "slack-ops"],
        escalation_policy="dba-oncall",
        description="Replication lag exceeds threshold",
        runbook_url="https://runbooks.example.com/replication-lag",
    ),
    AlertRule(
        name="slow_queries",
        metric="queries.slow_rate",
        condition="> {threshold}",
        threshold=10,  # queries per minute
        severity=Severity.WARNING,
        notification_channels=["slack-db"],
        description="High rate of slow queries",
        runbook_url="https://runbooks.example.com/slow-queries",
    ),
]

for rule in rules:
    alert_mgr.add_rule(rule)

# Configure notification channels
alert_mgr.configure_channel(
    name="slack-ops",
    type="slack",
    webhook_url="https://hooks.slack.com/services/xxx",
    channel="#ops-alerts",
)

alert_mgr.configure_channel(
    name="pagerduty-oncall",
    type="pagerduty",
    service_key="xxx",
    escalation_policy="dba-oncall",
)
```

### Advanced Dashboard Configuration

```python
from monitoring import DashboardBuilder, PanelType, DashboardTemplate

builder = DashboardBuilder(title="Production Database Overview")

# Create comprehensive dashboard
panels = [
    # Row 1: Key Metrics
    PanelType.STAT,  # Connections
    PanelType.STAT,  # TPS
    PanelType.STAT,  # Cache Hit
    PanelType.STAT,  # Replication Lag
    
    # Row 2: Time Series
    PanelType.TIME_SERIES,  # Connections over time
    PanelType.TIME_SERIES,  # TPS over time
    PanelType.TIME_SERIES,  # Query latency
    PanelType.TIME_SERIES,  # I/O throughput
    
    # Row 3: Detailed
    PanelType.TABLE,  # Top slow queries
    PanelType.HEATMAP,  # Query latency distribution
    PanelType.GAUGE,  # Disk usage
    PanelType.BAR,  # Table sizes
]

# Use template for consistent dashboard
template = DashboardTemplate()
dashboard = template.create_production_dashboard(
    title="Production Database",
    datasource="postgresql-prod",
    refresh_interval="10s",
)

dashboard.save("production_database.json")
```

## Architecture Patterns

### Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Monitoring Architecture                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Data Collection Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Agent-based │  │  Agentless  │  │  Pull-based │ │   │
│  │  │  Collection  │  │  Collection │  │  Collection │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Data Processing Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Aggregation │  │  Sampling   │  │  Enrichment │ │   │
│  │  │              │  │             │  │             │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Storage Layer                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Time Series │  │  Log Store  │  │  Event Store│ │   │
│  │  │  Database    │  │             │  │             │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Presentation Layer                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Dashboards  │  │  Alerts     │  │  Reports    │ │   │
│  │  │              │  │             │  │             │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Health Check Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Health Check Architecture                 │
├─────────────────────────────────────────────────────────────┤
│  Level 1: Basic (every 1 minute)                           │
│  └─► Connection test, server status                         │
│                                                             │
│  Level 2: Standard (every 5 minutes)                       │
│  └─► + Lock detection, replication status                   │
│                                                             │
│  Level 3: Comprehensive (every 15 minutes)                 │
│  └─► + Query performance, index health, bloat               │
│                                                             │
│  Level 4: Deep (daily)                                     │
│  └─► + Security audit, compliance check                     │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with FastAPI
from fastapi import FastAPI, Depends
from monitoring import MetricsCollector, HealthChecker

app = FastAPI()
collector = MetricsCollector(connection_string=connection_string)
health_checker = HealthChecker(connection_string=connection_string)

@app.get("/admin/metrics")
async def get_metrics():
    metrics = collector.collect()
    return {
        "connections": metrics.connections.__dict__,
        "throughput": metrics.throughput.__dict__,
        "cache": metrics.cache.__dict__,
        "replication": metrics.replication.__dict__,
    }

@app.get("/admin/health")
async def health_check():
    health = health_checker.check(level="comprehensive")
    return {
        "status": health.status.value,
        "checks": [c.__dict__ for c in health.checks],
    }
```

### Monitoring Integration

```python
# Integration with Prometheus
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry

# Create custom registry
registry = CollectorRegistry()

# Define metrics
CONNECTIONS = Gauge('db_connections_active', 'Active connections', registry=registry)
TPS = Gauge('db_tps', 'Transactions per second', registry=registry)
CACHE_HIT = Gauge('db_cache_hit_ratio', 'Cache hit ratio', registry=registry)
REPLICATION_LAG = Gauge('db_replication_lag_ms', 'Replication lag', registry=registry)
QUERY_DURATION = Histogram('db_query_duration_seconds', 'Query duration', registry=registry)

class PrometheusExporter:
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def export(self):
        metrics = self.collector.collect()
        CONNECTIONS.set(metrics.connections.active)
        TPS.set(metrics.throughput.tps)
        CACHE_HIT.set(metrics.cache.hit_ratio)
        REPLICATION_LAG.set(metrics.replication.lag_ms)
```

## Performance Optimization

### Monitoring Performance

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Collection overhead | < 1% | 1-5% | > 5% |
| Metric storage growth | < 1GB/day | 1-10GB/day | > 10GB/day |
| Alert latency | < 30s | 30-60s | > 60s |
| Dashboard load time | < 2s | 2-5s | > 5s |

### Optimized Collection

```python
from monitoring import OptimizedCollector

collector = OptimizedCollector()

# Configure optimized collection
collector.configure(
    # Sampling for high-volume metrics
    sampling={
        "query_duration": 0.1,  # 10% sampling
        "lock_duration": 0.5,   # 50% sampling
    },
    
    # Aggregation
    aggregation={
        "connections": {"interval": 10, "functions": ["avg", "max", "p95"]},
        "tps": {"interval": 30, "functions": ["avg", "max"]},
    },
    
    # Downsampling
    downsampling=[
        {"after_days": 7, "resolution": "5m"},
        {"after_days": 30, "resolution": "1h"},
        {"after_days": 90, "resolution": "1d"},
    ],
)
```

### Dashboard Optimization

```python
from monitoring import DashboardOptimizer

optimizer = DashboardOptimizer()

# Optimize dashboard for performance
optimized = optimizer.optimize(
    dashboard="production_overview",
    max_points_per_series=1000,
    enable_caching=True,
    cache_ttl_seconds=60,
    lazy_loading=True,
)

print(f"Original load time: {optimized.original_load_time:.1f}s")
print(f"Optimized load time: {optimized.optimized_load_time:.1f}s")
print(f"Improvement: {optimized.improvement_percentage:.1f}%")
```

## Security Considerations

### Monitoring Security

```python
from monitoring import SecurityConfig

security = SecurityConfig()

# Configure secure monitoring
security.configure(
    # Authentication
    require_auth=True,
    auth_method="token",
    
    # Authorization
    read_roles=["monitoring", "dba"],
    write_roles=["admin"],
    
    # Data protection
    mask_sensitive_metrics=True,
    sensitive_fields=["password", "token", "secret"],
    
    # Audit
    log_access=True,
    log_queries=True,
)
```

### Metric Access Control

```python
from monitoring import AccessControl

access = AccessControl()

# Configure metric access
access.configure(
    # Metric categories
    categories={
        "public": ["connections", "throughput", "cache"],
        "internal": ["locks", "replication", "io"],
        "sensitive": ["query_text", "user_activity"],
    },
    
    # Access rules
    rules=[
        {"role": "viewer", "categories": ["public"]},
        {"role": "dba", "categories": ["public", "internal"]},
        {"role": "admin", "categories": ["public", "internal", "sensitive"]},
    ],
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| High overhead | Monitoring impacting DB | Reduce collection frequency, enable sampling |
| Missing metrics | Gaps in graphs | Check agent connectivity, verify configuration |
| Alert storms | Too many alerts | Tune thresholds, implement alert grouping |
| Dashboard slow | Long load times | Optimize queries, enable caching |
| Storage full | Metrics not retained | Configure downsampling, increase retention |

### Diagnostic Queries

```sql
-- Check monitoring agent connections
SELECT
    client_addr,
    state,
    query,
    backend_start,
    state_change
FROM pg_stat_activity
WHERE application_name LIKE 'monitoring%'
ORDER BY state_change DESC;

-- Check statistics collector
SELECT
    relname,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 10;

-- Check replication monitoring
SELECT
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    pg_wal_lsn_diff(sent_lsn, replay_lsn) AS replication_lag_bytes
FROM pg_stat_replication;
```

## API Reference

### MetricsCollector

```python
class MetricsCollector:
    def __init__(self, connection_string: str)
    def configure(self, config: CollectionConfig)
    def collect(self) -> Metrics
    def get_history(self, metric: str, hours: int) -> MetricHistory
    def get_aggregated(self, metric: str, hours: int, interval: str) -> AggregatedMetrics
    def export_prometheus(self) -> str
    def export_json(self) -> str
```

### AlertManager

```python
class AlertManager:
    def __init__(self)
    def add_rule(self, rule: AlertRule)
    def remove_rule(self, name: str)
    def check_alerts(self) -> list[Alert]
    def acknowledge(self, alert_id: str) -> AcknowledgeResult
    def silence(self, rule_name: str, duration_minutes: int) -> SilenceResult
    def get_history(self, hours: int = 24) -> list[AlertHistory]
    def configure_channel(self, **kwargs)
```

### HealthChecker

```python
class HealthChecker:
    def __init__(self, connection_string: str)
    def check(self, level: str = "standard") -> HealthStatus
    def schedule(self, level: str, interval_minutes: int)
    def get_history(self, hours: int = 24) -> list[HealthCheck]
    def get_trends(self) -> HealthTrends
```

### DashboardBuilder

```python
class DashboardBuilder:
    def __init__(self, title: str)
    def add_panel(self, panel_type: PanelType, title: str, metric: str, **kwargs)
    def build(self) -> Dashboard
    def save(self, filename: str)
    def load(self, filename: str) -> Dashboard
    def export_grafana(self) -> str
    def export_json(self) -> str
```

### CapacityPlanner

```python
class CapacityPlanner:
    def __init__(self, connection_string: str)
    def analyze(self) -> CapacityAnalysis
    def forecast(self, days: int = 30) -> CapacityForecast
    def get_recommendations(self) -> list[CapacityRecommendation]
    def get_cost_optimization(self) -> list[CostRecommendation]
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class HealthStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class Metrics:
    connections: ConnectionMetrics
    throughput: ThroughputMetrics
    cache: CacheMetrics
    replication: ReplicationMetrics
    io: IOMetrics
    timestamp: datetime

@dataclass
class ConnectionMetrics:
    active: int
    idle: int
    waiting: int
    max: int
    utilization_pct: float

@dataclass
class ThroughputMetrics:
    tps: float
    qps: float
    transactions_total: int
    queries_total: int

@dataclass
class CacheMetrics:
    hit_ratio: float
    buffer_hit_ratio: float
    index_hit_ratio: float
    tuple_hit_ratio: float

@dataclass
class ReplicationMetrics:
    lag_bytes: int
    lag_ms: float
    replicas: List['ReplicaMetrics']

@dataclass
class Alert:
    id: str
    name: str
    severity: Severity
    message: str
    timestamp: datetime
    acknowledged: bool
    resolved: bool
    runbook_url: Optional[str]

@dataclass
class HealthCheck:
    name: str
    passed: bool
    message: str
    duration_ms: float
    timestamp: datetime
```

## Deployment Guide

### Docker Deployment

```yaml
version: '3.8'
services:
  monitoring:
    image: db-monitoring:latest
    environment:
      DATABASE_URL: ${DATABASE_URL}
      PROMETHEUS_URL: ${PROMETHEUS_URL}
    ports:
      - "9090:9090"
    volumes:
      - ./config:/config
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: db-monitoring
spec:
  replicas: 2
  selector:
    matchLabels:
      app: db-monitoring
  template:
    metadata:
      labels:
        app: db-monitoring
    spec:
      containers:
      - name: monitoring
        image: db-monitoring:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: url
        ports:
        - containerPort: 9090
```

## Testing Strategy

### Unit Tests

```python
import pytest
from monitoring import MetricsCollector, AlertManager

@pytest.fixture
def collector():
    return MetricsCollector(connection_string="postgresql://localhost/test")

def test_collect_metrics(collector):
    metrics = collector.collect()
    assert metrics.connections.active >= 0
    assert metrics.throughput.tps >= 0

def test_alert_manager():
    alert_mgr = AlertManager()
    alert_mgr.add_rule(AlertRule(
        name="test_alert",
        metric="test_metric",
        condition="> 100",
        severity=Severity.WARNING,
    ))
    assert len(alert_mgr.rules) == 1
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| PostgreSQL | 12 | 15+ |
| Prometheus | 2.0 | 2.45+ |

## Glossary

| Term | Definition |
|------|------------|
| **TPS** | Transactions Per Second |
| **QPS** | Queries Per Second |
| **SLA** | Service Level Agreement |
| **SLO** | Service Level Objective |
| **SLI** | Service Level Indicator |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added advanced metrics collection
- New capacity planning features
- Improved dashboard builder
- Added health check scheduling

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/monitoring.git
cd monitoring
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills