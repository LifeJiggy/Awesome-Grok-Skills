# Database Administration Agent

Enterprise database lifecycle management — instance provisioning, backup/recovery, performance tuning, replication, security auditing, capacity planning, and real-time monitoring.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Instance Management](#instance-management)
  - [Backup & Recovery](#backup--recovery)
  - [Performance Tuning](#performance-tuning)
  - [Replication Management](#replication-management)
  - [Security Auditing](#security-auditing)
  - [Capacity Planning](#capacity-planning)
  - [Schema Management](#schema-management)
  - [Monitoring & Alerting](#monitoring--alerting)
  - [Recovery Planning](#recovery-planning)
- [API Reference](#api-reference)
  - [DatabaseAdminAgent](#databaseadminagent)
  - [DatabaseAdminConfig](#databaseadminconfig)
  - [Data Models](#data-models)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Database Administration Agent provides comprehensive, engine-agnostic database operations covering the full lifecycle: provisioning, monitoring, performance tuning, backup/recovery, replication management, security auditing, capacity planning, and disaster recovery. It supports PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, ClickHouse, Cassandra, and DynamoDB.

**Key capabilities:**
- Multi-engine instance management with status lifecycle tracking
- 6 backup types with retention policies and automated cleanup
- Performance analysis with bottleneck detection and index recommendations
- Replication topology management with lag monitoring and failover
- Security auditing with CWE mapping and compliance framework alignment
- Capacity forecasting with trend classification and growth projection
- Schema change tracking with rollback SQL generation
- Real-time alerting with configurable thresholds and severity levels

---

## Features

| Feature | Description |
|---------|-------------|
| **Instance Management** | Register, track, and manage database instances across 8 engines |
| **Backup & Recovery** | Full, incremental, differential, snapshot, WAL, logical dump with retention |
| **Performance Tuning** | Metric aggregation, bottleneck detection, index and config recommendations |
| **Replication** | Topology management, lag monitoring, semi-sync/async, failover execution |
| **Security Auditing** | 7 security checks with CWE mapping and compliance framework tracking |
| **Capacity Planning** | Growth rate computation, multi-horizon forecasting, trend classification |
| **Schema Management** | Change history, rollback SQL generation, reversible change tracking |
| **Monitoring** | Threshold-based alerting with severity, cooldown, and resolution tracking |
| **Recovery Planning** | RTO/RPO definition, step-by-step plans, simulated testing |
| **Dashboard** | Real-time overview of instances, storage, replication, security, alerts |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│              DATABASE ADMINISTRATION AGENT                 │
├──────────────────────────────────────────────────────────┤
│  Instance Mgmt → Backup/Recovery → Performance Tuning    │
│  → Replication → Security Audit → Capacity Planning      │
│  → Schema Mgmt → Monitoring/Alerting → Recovery Plans    │
└──────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system architecture with component deep dives, data flow diagrams, and design patterns.

---

## Quick Start

```python
from agents.database_admin.agent import (
    DatabaseAdminAgent, DatabaseEngine, InstanceStatus,
    BackupType, PerformanceMetric, MetricType,
)

agent = DatabaseAdminAgent()

# Register an instance
instance = agent.register_instance(
    "my-postgres", DatabaseEngine.POSTGRESQL,
    host="db.example.com", port=5432,
    database="myapp", storage_gb=100,
)

# Create a backup
backup = agent.create_backup(instance.instance_id, BackupType.FULL)
print(f"Backup: {backup.backup_id} ({backup.status.value})")

# Analyze performance
analysis = agent.analyze_performance(instance.instance_id)
print(f"Health: {analysis.overall_health}, Score: {analysis.score}")

# Dashboard
dashboard = agent.generate_dashboard()
print(dashboard)
```

---

## Installation

### From Source

```bash
cd Awesome-Grok-Skills
pip install -e .
```

### Direct Usage

```bash
python agents/database-admin/agent.py
```

### Requirements

- Python 3.10+
- No external dependencies (uses only standard library)

---

## Usage

### Instance Management

```python
agent = DatabaseAdminAgent()

# Register instances
primary = agent.register_instance(
    "prod-primary", DatabaseEngine.POSTGRESQL,
    host="db-primary.internal", port=5432,
    database="app_production", version="15.4",
    region="us-east-1", size="db.r5.xlarge",
    storage_gb=500, tags={"env": "production", "team": "platform"},
)

# List instances
all_instances = agent.list_instances()
pg_only = agent.list_instances(engine=DatabaseEngine.POSTGRESQL)
running = agent.list_instances(status=InstanceStatus.RUNNING)

# Update status
agent.update_instance_status(primary.instance_id, InstanceStatus.MAINTENANCE)

# Deprovision (must be stopped first, or use force=True)
agent.update_instance_status(primary.instance_id, InstanceStatus.STOPPED)
agent.deprovision_instance(primary.instance_id)
```

### Backup & Recovery

```python
# Create different backup types
full = agent.create_backup(instance_id, BackupType.FULL, retention_days=30)
incremental = agent.create_backup(instance_id, BackupType.INCREMENTAL)
wal = agent.create_backup(instance_id, BackupType.WAL_ARCHIVE)

# List and query backups
all_backups = agent.list_backups(instance_id)
full_only = agent.list_backups(instance_id, backup_type=BackupType.FULL)
latest = agent.get_latest_backup(instance_id)

# Restore
agent.restore_backup(full.backup_id)

# Clean up expired backups
result = agent.cleanup_expired_backups(instance_id)
print(f"Removed {result['expired_removed']} backups, retained {result['retained']}")
```

### Performance Tuning

```python
# Record metrics (typically from monitoring agent or database driver)
for _ in range(100):
    agent.record_metric(PerformanceMetric(
        metric_type=MetricType.QUERY_TIME,
        value=random.uniform(10, 500),
        instance_id=instance_id,
    ))

# Analyze
analysis = agent.analyze_performance(instance_id)
print(f"Score: {analysis.score}")
print(f"Health: {analysis.overall_health}")
print(f"Bottlenecks: {analysis.bottlenecks}")
print(f"Index recs: {len(analysis.index_recommendations)}")
print(f"Config recs: {len(analysis.config_recommendations)}")

# Find slow queries
slow = agent.get_slow_queries(instance_id, threshold_ms=200)
for q in slow:
    print(f"  {q.query_hash}: {q.execution_time_ms:.1f}ms ({q.rows_examined} rows scanned)")
```

### Replication Management

```python
# Create replication link
link = agent.add_replication_link(
    source_id=primary.instance_id,
    target_id=replica.instance_id,
    role=ReplicationRole.READ_REPLICA,
    sync_mode="async",
)

# Monitor lag
agent.update_replication_lag(link.link_id, lag_seconds=2.5)

# Get summary
summary = agent.get_replication_summary()
print(f"Total: {summary['total_links']}")
print(f"Healthy: {summary['healthy']}")
print(f"Lagging: {summary['lagging']}")
print(f"Max lag: {summary['max_lag_seconds']:.1f}s")

# Failover (if primary fails)
result = agent.failover(primary.instance_id, replica.instance_id)
print(f"Failover: {result['source']} -> {result['target']}")
```

### Security Auditing

```python
# Run full security audit
findings = agent.run_security_audit(instance_id)
for f in findings:
    print(f"[{f.level.value.upper()}] {f.title}")
    print(f"  CWE: {f.cwe_id}")
    print(f"  Recommendation: {f.recommendation}")
    print(f"  Compliance: {', '.join(f.compliance_frameworks)}")

# Get summary
summary = agent.get_security_summary()
print(f"Total findings: {summary['total_findings']}")
print(f"By level: {summary['by_level']}")

# Remediate
agent.remediate_finding(findings[0].finding_id)
```

### Capacity Planning

```python
# Forecast with historical data
forecast = agent.forecast_capacity(
    instance_id, "storage_gb", current_value=350,
    historical_values=[300, 310, 315, 320, 325, 330, 340, 350],
)
print(f"Current: {forecast.current_value}GB")
print(f"30-day: {forecast.projected_value_30d:.0f}GB")
print(f"90-day: {forecast.projected_value_90d:.0f}GB")
print(f"365-day: {forecast.projected_value_365d:.0f}GB")
print(f"Trend: {forecast.trend.value}")
print(f"Days until full: {forecast.days_until_full}")
print(f"Recommendation: {forecast.recommendation}")
```

### Schema Management

```python
# Record schema changes
from agents.database_admin.agent import SchemaChange, SchemaChangeType

change = SchemaChange(
    instance_id=instance_id,
    change_type=SchemaChangeType.ADD_COLUMN,
    object_name="email_verified",
    sql_statement="ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;",
    executed_by="dba@company.com",
    reversible=True,
)
agent.record_schema_change(change)

# View history
history = agent.get_schema_history(instance_id=instance_id)
for c in history:
    print(f"  {c.change_type.value}: {c.object_name} ({c.executed_at})")

# Generate rollback SQL
rollback = agent.generate_rollback_sql(change.change_id)
print(f"Rollback: {rollback}")
```

### Monitoring & Alerting

```python
# Check alerts against thresholds
alerts = agent.check_alerts(instance_id)
for a in alerts:
    print(f"[{a.severity.value}] {a.message}")

# Get active alerts
active = agent.get_active_alerts()
critical = agent.get_active_alerts(instance_id)
critical_only = [a for a in agent.get_active_alerts() if a.severity == AlertSeverity.CRITICAL]

# Resolve
if alerts:
    agent.resolve_alert(alerts[0].alert_id)
```

### Recovery Planning

```python
# Create DR plan
plan = agent.create_recovery_plan(
    name="Production DR Plan",
    instance_ids=[primary.instance_id, replica.instance_id],
    rto_minutes=30,
    rpo_minutes=5,
    steps=[
        {"order": 1, "action": "assess", "description": "Assess failure scope"},
        {"order": 2, "action": "notify", "description": "Notify incident team"},
        {"order": 3, "action": "failover", "description": "Failover to replica"},
        {"order": 4, "action": "verify", "description": "Verify data integrity"},
    ],
)

# Test the plan
test = agent.test_recovery_plan(plan.plan_id)
print(f"RTO achieved: {test['rto_achieved']:.1f} min (target: {plan.rto_minutes})")
print(f"RPO achieved: {test['rpo_achieved']:.1f} min (target: {plan.rpo_minutes})")

# List all plans
plans = agent.get_recovery_plans()
```

### Dashboard

```python
dashboard = agent.generate_dashboard()
print(f"Instances: {dashboard['instances']}")
print(f"Storage: {dashboard['storage']}")
print(f"Replication: {dashboard['replication']}")
print(f"Security: {dashboard['security']}")
print(f"Alerts: {dashboard['alerts']}")
print(f"Backups: {dashboard['backups']}")
```

---

## API Reference

### DatabaseAdminAgent

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register_instance` | name, engine, host, port, database, **kwargs | DatabaseInstance | Register a database instance |
| `get_instance` | instance_id | DatabaseInstance | Get instance by ID |
| `list_instances` | engine?, status?, region? | List[DatabaseInstance] | List with filters |
| `update_instance_status` | instance_id, status | Dict | Update instance status |
| `deprovision_instance` | instance_id, force? | Dict | Remove an instance |
| `create_backup` | instance_id, backup_type, retention_days | BackupRecord | Create a backup |
| `list_backups` | instance_id, backup_type?, status? | List[BackupRecord] | List backups |
| `restore_backup` | backup_id, target_instance_id? | Dict | Restore from backup |
| `get_latest_backup` | instance_id | BackupRecord? | Get most recent backup |
| `cleanup_expired_backups` | instance_id | Dict | Remove expired backups |
| `record_metric` | metric | None | Record a performance metric |
| `analyze_performance` | instance_id | PerformanceAnalysis | Full performance analysis |
| `record_query_plan` | instance_id, plan | None | Record a query plan |
| `get_slow_queries` | instance_id, threshold_ms? | List[QueryPlan] | Get slow queries |
| `add_replication_link` | source_id, target_id, role, sync_mode | ReplicationLink | Create replication link |
| `get_replication_status` | source_id? | List[ReplicationLink] | Get replication status |
| `update_replication_lag` | link_id, lag_seconds | Dict | Update lag measurement |
| `get_replication_summary` | - | Dict | Overall replication summary |
| `failover` | source_id, target_id | Dict | Execute failover |
| `run_security_audit` | instance_id | List[SecurityFinding] | Run security audit |
| `get_security_summary` | instance_id? | Dict | Security findings summary |
| `remediate_finding` | finding_id | Dict | Mark finding remediated |
| `forecast_capacity` | instance_id, metric, current_value, historical_values? | CapacityForecast | Forecast capacity |
| `record_schema_change` | change | SchemaChange | Record schema change |
| `get_schema_history` | instance_id?, change_type?, limit? | List[SchemaChange] | Get schema history |
| `generate_rollback_sql` | change_id | str? | Generate rollback SQL |
| `check_alerts` | instance_id | List[Alert] | Check alert thresholds |
| `get_active_alerts` | instance_id? | List[Alert] | Get unresolved alerts |
| `resolve_alert` | alert_id | Dict | Mark alert resolved |
| `create_recovery_plan` | name, instance_ids, rto_minutes, rpo_minutes, steps? | RecoveryPlan | Create DR plan |
| `test_recovery_plan` | plan_id | Dict | Simulate plan test |
| `get_recovery_plans` | - | List[RecoveryPlan] | List all DR plans |
| `get_status` | - | Dict | Agent status summary |
| `generate_dashboard` | - | Dict | Comprehensive dashboard |

### DatabaseAdminConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_backup_type` | BackupType | FULL | Default backup type |
| `default_retention_days` | int | 30 | Default retention period |
| `max_concurrent_backups` | int | 3 | Max parallel backups |
| `backup_timeout_seconds` | int | 3600 | Backup operation timeout |
| `enable_compression` | bool | True | Compress backups |
| `enable_encryption` | bool | True | Encrypt backups |
| `max_replication_lag_seconds` | float | 30.0 | Max acceptable lag |
| `auto_failover_enabled` | bool | True | Allow automatic failover |
| `slow_query_threshold_ms` | float | 1000.0 | Slow query detection threshold |
| `connection_warning_threshold` | float | 0.80 | Connection pool warning % |
| `connection_critical_threshold` | float | 0.95 | Connection pool critical % |
| `disk_warning_threshold` | float | 0.75 | Disk usage warning % |
| `disk_critical_threshold` | float | 0.90 | Disk usage critical % |
| `cpu_warning_threshold` | float | 0.70 | CPU usage warning % |
| `cpu_critical_threshold` | float | 0.90 | CPU usage critical % |
| `require_ssl` | bool | True | Require SSL connections |
| `encryption_at_rest` | bool | True | Require encryption at rest |
| `audit_logging_enabled` | bool | True | Require audit logging |
| `capacity_alert_days` | int | 30 | Days threshold for capacity alerts |

---

## Examples

### Example 1: Full Production Setup

```python
agent = DatabaseAdminAgent()

# Register primary and replica
primary = agent.register_instance(
    "prod-pg", DatabaseEngine.POSTGRESQL,
    host="pg-primary.internal", port=5432,
    database="app", storage_gb=1000, size="db.r5.2xlarge",
    version="15.4", region="us-east-1",
    tags={"env": "production", "team": "data"},
)
replica = agent.register_instance(
    "prod-pg-replica", DatabaseEngine.POSTGRESQL,
    host="pg-replica.internal", port=5432,
    database="app", storage_gb=1000, size="db.r5.xlarge",
    version="15.4", region="us-east-1",
    tags={"env": "production", "team": "data"},
)

# Set up replication
link = agent.add_replication_link(primary.instance_id, replica.instance_id)

# Create initial backup
backup = agent.create_backup(primary.instance_id, BackupType.FULL)

# Run security audit
findings = agent.run_security_audit(primary.instance_id)

# Create DR plan
plan = agent.create_recovery_plan(
    "Production DR", [primary.instance_id, replica.instance_id],
    rto_minutes=15, rpo_minutes=5,
)

# Dashboard
print(agent.generate_dashboard())
```

### Example 2: Performance Monitoring Pipeline

```python
import random

agent = DatabaseAdminAgent()
instance = agent.register_instance("analytics", DatabaseEngine.CLICKHOUSE, ...)

# Simulate metric collection over time
for _ in range(200):
    agent.record_metric(PerformanceMetric(
        metric_type=MetricType.QUERY_TIME,
        value=random.uniform(5, 800),
        instance_id=instance.instance_id,
    ))
    agent.record_metric(PerformanceMetric(
        metric_type=MetricType.DISK_USAGE,
        value=random.uniform(50, 95),
        instance_id=instance.instance_id,
    ))

# Analyze
analysis = agent.analyze_performance(instance.instance_id)
if analysis.overall_health == "critical":
    alerts = agent.check_alerts(instance.instance_id)
    print(f"URGENT: {len(alerts)} alerts generated")
```

### Example 3: Capacity Planning Workflow

```python
# Monthly capacity review
for instance in agent.list_instances():
    # Check storage
    storage_forecast = agent.forecast_capacity(
        instance.instance_id, "storage_gb",
        instance.storage_used_gb,
        historical_values=[...],  # from monitoring
    )
    if storage_forecast.days_until_full and storage_forecast.days_until_full < 30:
        print(f"ALERT: {instance.name} will be full in {storage_forecast.days_until_full} days")

    # Check connections
    conn_forecast = agent.forecast_capacity(
        instance.instance_id, "connections",
        current_connections,
        historical_values=[...],
    )
    if conn_forecast.trend == CapacityTrend.GROWING:
        print(f"NOTE: {instance.name} connections growing, plan scaling")
```

---

## Configuration

### Default Configuration

```python
config = DatabaseAdminConfig(
    default_retention_days=30,
    max_concurrent_backups=3,
    enable_compression=True,
    enable_encryption=True,
    max_replication_lag_seconds=30.0,
    auto_failover_enabled=True,
    slow_query_threshold_ms=1000.0,
    connection_warning_threshold=0.80,
    disk_warning_threshold=0.75,
    cpu_warning_threshold=0.70,
    require_ssl=True,
    encryption_at_rest=True,
    audit_logging_enabled=True,
    capacity_alert_days=30,
)
agent = DatabaseAdminAgent(config)
```

---

## Best Practices

1. **Always register instances** before performing any operations on them
2. **Create backups before schema changes** — use `auto_backup_before_schema_change`
3. **Test recovery plans** at least quarterly to ensure they work
4. **Monitor replication lag** continuously and set appropriate thresholds
5. **Run security audits** after every configuration change
6. **Forecast capacity** monthly and plan scaling proactively
7. **Track schema changes** for audit trails and rollback capability
8. **Use multiple backup types** — full weekly, incremental daily, WAL continuous
9. **Address security findings** by severity: CRITICAL within 24h, HIGH within 1 week
10. **Review dashboards** daily for production systems

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `KeyError: Instance not found` | Register the instance first with `register_instance` |
| Backup fails | Check instance status is RUNNING, verify timeout settings |
| Performance score is 0 | Record metrics first using `record_metric` before analysis |
| Replication lag growing | Check network, replica resources, consider semi-sync |
| Security audit finds nothing | Verify instance `config` dict includes security settings |
| Capacity forecast is 0% growth | Provide `historical_values` for trend computation |
| Rollback SQL returns None | Check `change.reversible` is True and change type is supported |
| Alerts not firing | Verify metrics are recent (within 5 minutes) and thresholds are set |

---

## Contributing

Contributions welcome. Guidelines:

1. Add new database engines via the `DatabaseEngine` enum
2. Add new backup types via the `BackupType` enum
3. Add new security checks in `run_security_audit` with CWE mapping
4. Add new metric types via the `MetricType` enum
5. Add new monitoring checks with appropriate thresholds
6. Include type hints for all new methods
7. Add comprehensive docstrings for public APIs
8. Test edge cases: empty instances, single metrics, missing data

---

## License

MIT License — See [LICENSE](../../LICENSE) for details.
