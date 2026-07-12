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