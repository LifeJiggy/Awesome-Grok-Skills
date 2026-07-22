---
name: "Database Management"
version: "2.0.0"
description: "Core database management operations including lifecycle management, resource allocation, space management, configuration tuning, and maintenance scheduling for production databases"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database-admin", "management", "lifecycle", "resources", "maintenance", "configuration"]
category: "database-admin"
personality: "dba-operator"
use_cases: ["database lifecycle", "space management", "configuration tuning", "maintenance windows", "resource monitoring"]
---

# Database Management

> Core database management operations providing lifecycle management, resource allocation, space management, configuration tuning, and maintenance scheduling for reliable production database operations.

## Overview

The Database Management module provides essential operations for day-to-day database administration. It implements database lifecycle operations (create, clone, resize, archive, drop), tablespace and storage management, automatic vacuuming and reindexing, connection and resource monitoring, configuration parameter management, and maintenance window scheduling. Every operation includes safety checks, rollback capability, and comprehensive audit logging.

## Core Capabilities

### 1. Database Lifecycle Management
- Create databases with templates and initial configurations
- Clone databases for testing and staging environments
- Resize databases (add/remove tablespaces)
- Archive old data to cold storage
- Drop databases with confirmation and backup verification

### 2. Space Management
- Table and index size monitoring
- Bloat detection and estimation
- Tablespace utilization tracking
- Automatic VACUUM and ANALYZE scheduling
- Dead tuple cleanup and space reclamation

### 3. Configuration Management
- Parameter listing and documentation
- Runtime configuration changes (ALTER SYSTEM)
- Configuration file diff and validation
- Parameter impact analysis
- Configuration history and rollback

### 4. Resource Monitoring
- Connection count and usage tracking
- Lock monitoring and deadlock detection
- Memory usage per database
- I/O statistics and throughput
- Background worker monitoring

### 5. Maintenance Scheduling
- Automated VACUUM schedules
- REINDEX scheduling
- Statistics update scheduling
- Backup window management
- Maintenance task dependency chains

### 6. Health Dashboard
- Database size and growth trends
- Table bloat estimation
- Index usage statistics
- Connection pool utilization
- Replication lag monitoring

## Usage Examples

### Database Lifecycle

```python
from db_management import DatabaseManager, LifecycleAction

manager = DatabaseManager(connection_string="postgresql://admin:pass@localhost/admin")

# Create a new database
db = manager.create_database(
    name="analytics_prod",
    template="template0",
    encoding="UTF-8",
    locale="en_US.UTF-8",
    owner="app_user",
    tablespace="fast_ssd",
)
print(f"Created database: {db.name} ({db.size_mb:.1f} MB)")

# Clone for testing
clone = manager.clone_database(
    source="analytics_prod",
    target="analytics_staging",
    copy_data=True,
    copy_privileges=False,
)
print(f"Cloned to: {clone.name}")

# Archive old data
archive = manager.archive_data(
    database="analytics_prod",
    table="events",
    older_than_days=90,
    archive_to="s3://backups/archive/",
)
print(f"Archived {archive.rows_archived} rows ({archive.size_mb:.1f} MB)")
```

### Space Management

```python
from db_management import SpaceManager

space = SpaceManager(connection_string="postgresql://admin:pass@localhost/analytics")

# Get database size
db_size = space.get_database_size()
print(f"Database size: {db_size.total_mb:.1f} MB")
print(f"  Tables: {db_size.tables_mb:.1f} MB")
print(f"  Indexes: {db_size.indexes_mb:.1f} MB")
print(f"  Free: {db_size.free_mb:.1f} MB")

# Detect bloat
bloat = space.detect_bloat()
for table in bloat:
    print(f"  {table.name}: {table.bloat_pct:.1f}% bloat ({table.wasted_mb:.1f} MB)")

# Run vacuum
vacuum_result = space.vacuum(table="events", full=False, analyze=True)
print(f"Vacuum: {vacuum_result.duration_seconds:.1f}s, reclaimed {vacuum_result.space_reclaimed_mb:.1f} MB")
```

### Configuration Management

```python
from db_management import ConfigManager

config = ConfigManager(connection_string="postgresql://admin:pass@localhost/postgres")

# List current parameters
params = config.get_parameters(category="memory")
for p in params:
    print(f"  {p.name}: {p.value} (unit: {p.unit}, category: {p.category})")

# Change a parameter
result = config.set_parameter(
    name="shared_buffers",
    value="4GB",
    context="postmaster",  # requires restart
    reload=False,
)
print(f"Changed: {result.parameter} = {result.new_value}")
print(f"Requires restart: {result.requires_restart}")

# Configuration diff
diff = config.diff_configurations("production", "staging")
for change in diff:
    print(f"  {change.parameter}: {change.production_value} → {change.staging_value}")
```

### Maintenance Scheduling

```python
from db_management import MaintenanceScheduler, MaintenanceTask

scheduler = MaintenanceScheduler(connection_string="postgresql://admin:pass@localhost/admin")

# Schedule VACUUM
scheduler.schedule(
    task=MaintenanceTask.VACUUM,
    schedule="0 2 * * *",  # daily at 2am
    targets=["orders", "events", "sessions"],
    options={"analyze": True, "verbose": False},
)

# Schedule REINDEX
scheduler.schedule(
    task=MaintenanceTask.REINDEX,
    schedule="0 3 * * 0",  # weekly on Sunday at 3am
    targets=["orders_idx", "events_created_idx"],
)

# Run maintenance window
result = scheduler.run_maintenance_window(
    start_hour=2,
    end_hour=6,
    tasks=[MaintenanceTask.VACUUM, MaintenanceTask.ANALYZE],
)
print(f"Maintenance completed: {result.tasks_completed} tasks in {result.duration_seconds:.0f}s")
```

## Best Practices

### Lifecycle Management
- Always verify backup existence before dropping a database
- Use CLONE for test environments instead of restoring from backup
- Archive data older than your retention policy to reduce active data size
- Test database creation scripts in staging before production

### Space Management
- Schedule daily VACUUM for high-update tables
- Monitor bloat weekly — aim for < 20% bloat on critical tables
- Use pg_repack for online table reorganization without locks
- Track tablespace usage to prevent disk space exhaustion

### Configuration
- Document all parameter changes with justification
- Test configuration changes in staging first
- Use ALTER SYSTEM for persistent changes; SET for session-level
- Keep configuration history for at least 90 days

### Maintenance
- Schedule VACUUM during low-traffic windows
- Run ANALYZE after VACUUM to update statistics
- Monitor maintenance task duration — sudden increases indicate problems
- Use maintenance windows to batch operations and minimize impact

## Related Modules

- **backup-recovery**: Backup and disaster recovery operations
- **performance-tuning**: Query and server performance optimization
- **security-hardening**: Database security configuration
- **monitoring**: Real-time database monitoring and alerting

---

## Advanced Configuration

### Advanced Lifecycle Management

```python
from db_management import DatabaseManager, LifecycleAction, CloneOptions

manager = DatabaseManager(connection_string="postgresql://admin:pass@localhost/admin")

# Create database with advanced options
db = manager.create_database(
    name="analytics_prod",
    template="template0",
    encoding="UTF-8",
    locale="en_US.UTF-8",
    owner="app_user",
    tablespace="fast_ssd",
    connection_limit=100,
    allow_connections=True,
    is_template=False,
)

# Advanced clone with selective data copy
clone = manager.clone_database(
    source="analytics_prod",
    target="analytics_staging",
    options=CloneOptions(
        copy_data=True,
        copy_privileges=False,
        copy_indexes=True,
        copy_constraints=True,
        exclude_tables=["audit_log", "sessions"],
        truncate_excluded=True,
    ),
)
```

### Advanced Space Management

```python
from db_management import SpaceManager, VacuumStrategy, ReindexStrategy

space = SpaceManager(connection_string="postgresql://admin:pass@localhost/analytics")

# Configure advanced vacuum strategy
vacuum_config = VacuumStrategy(
    mode="adaptive",  # adaptive, aggressive, conservative
    min_dead_tuples=1000,
    scale_factor=0.1,
    max_timeout_minutes=60,
    analyze_after_vacuum=True,
    verbose_logging=False,
)

# Run adaptive vacuum
result = space.vacuum_adaptive(
    tables=["orders", "events", "sessions"],
    strategy=vacuum_config,
)
print(f"Vacuum completed: {result.tables_vacuumed} tables")
print(f"Space reclaimed: {result.space_reclaimed_mb:.1f} MB")
print(f"Duration: {result.duration_seconds:.1f}s")

# Online reindex with minimal locking
reindex_result = space.reindex_online(
    table="orders",
    index="orders_created_idx",
    strategy=ReindexStrategy.CONCURRENTLY,
)
print(f"Reindex: {reindex_result.duration_seconds:.1f}s, no locks held")
```

### Advanced Configuration Management

```python
from db_management import ConfigManager, ConfigChange

config = ConfigManager(connection_string="postgresql://admin:pass@localhost/postgres")

# Batch configuration changes
changes = [
    ConfigChange("shared_buffers", "8GB", "postmaster"),
    ConfigChange("effective_cache_size", "24GB", "postmaster"),
    ConfigChange("work_mem", "256MB", "user"),
    ConfigChange("maintenance_work_mem", "2GB", "user"),
    ConfigChange("max_connections", "200", "postmaster"),
]

result = config.apply_batch(changes, validate_first=True)
print(f"Applied {result.applied} changes")
print(f"Skipped {result.skipped} changes")
print(f"Requires restart: {result.requires_restart}")

# Configuration validation
validation = config.validate_configuration()
print(f"Configuration valid: {validation.is_valid}")
for warning in validation.warnings:
    print(f"  Warning: {warning}")
```

## Architecture Patterns

### Database Management Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Database Management Layer                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Lifecycle  │  │   Space     │  │    Config   │        │
│  │  Manager    │  │   Manager   │  │    Manager  │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                 │
│  ┌──────┴────────────────┴────────────────┴──────┐        │
│  │              Database Connection Pool          │        │
│  └─────────────────────┬─────────────────────────┘        │
│                        │                                    │
│  ┌─────────────────────┴─────────────────────────┐        │
│  │              Audit & Logging Layer             │        │
│  └───────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### Maintenance Task Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   Maintenance Task Flow                     │
├─────────────────────────────────────────────────────────────┤
│  1. Schedule Task                                           │
│     └─► Cron expression + target tables                     │
│  2. Validate Prerequisites                                  │
│     └─► Check locks, connections, disk space                │
│  3. Acquire Lock                                            │
│     └─► Advisory lock or table lock                         │
│  4. Execute Task                                            │
│     └─► VACUUM, REINDEX, ANALYZE                            │
│  5. Verify Completion                                       │
│     └─► Check task status, duration                         │
│  6. Release Lock                                            │
│     └─► Release advisory lock                               │
│  7. Log Result                                              │
│     └─► Audit log + metrics                                 │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with FastAPI
from fastapi import FastAPI, Depends
from db_management import DatabaseManager

app = FastAPI()
db_manager = DatabaseManager(connection_string=connection_string)

async def get_db():
    async with db_manager.get_connection() as conn:
        yield conn

@app.get("/admin/database/stats")
async def get_database_stats(conn = Depends(get_db)):
    stats = await conn.execute("SELECT * FROM pg_stat_database")
    return stats.fetchall()
```

### Monitoring Integration

```python
# Integration with Prometheus
from prometheus_client import Counter, Histogram, Gauge

DB_SIZE = Gauge('db_size_bytes', 'Database size', ['database'])
TABLE_SIZE = Gauge('db_table_size_bytes', 'Table size', ['table'])
VACUUM_DURATION = Histogram('db_vacuum_duration_seconds', 'Vacuum duration')
MAINTENANCE_TASKS = Counter('db_maintenance_tasks_total', 'Maintenance tasks', ['type'])

class MetricsCollector:
    def record_database_size(self, database: str, size_bytes: int):
        DB_SIZE.labels(database=database).set(size_bytes)
    
    def record_table_size(self, table: str, size_bytes: int):
        TABLE_SIZE.labels(table=table).set(size_bytes)
    
    def record_vacuum(self, duration_seconds: float):
        VACUUM_DURATION.observe(duration_seconds)
        MAINTENANCE_TASKS.labels(type='vacuum').inc()
```

## Performance Optimization

### Space Management Optimization

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Database size growth | < 5%/month | 5-10%/month | > 10%/month |
| Table bloat | < 10% | 10-20% | > 20% |
| Dead tuples | < 1000 | 1000-10000 | > 10000 |
| Free space | > 20% | 10-20% | < 10% |

### Configuration Optimization

```sql
-- Analyze configuration impact
SELECT
    name,
    setting,
    unit,
    category,
    short_desc
FROM pg_settings
WHERE category IN ('Memory', 'Write-Ahead Log', 'Checkpoints')
ORDER BY category, name;

-- Check current configuration
SHOW shared_buffers;
SHOW effective_cache_size;
SHOW work_mem;
SHOW maintenance_work_mem;
```

### Maintenance Optimization

```python
from db_management import MaintenanceOptimizer

optimizer = MaintenanceOptimizer()

# Optimize maintenance schedule
schedule = optimizer.optimize_schedule(
    tables=["orders", "events", "sessions"],
    time_window_hours=4,  # 4-hour maintenance window
    priority="space_reclaim",  # space_reclaim, performance, availability
)

for task in schedule.tasks:
    print(f"  {task.time}: {task.type} on {task.table}")
    print(f"    Estimated duration: {task.estimated_duration_seconds:.0f}s")
    print(f"    Expected benefit: {task.estimated_benefit}")
```

## Security Considerations

### Access Control

```python
from db_management import AccessControlManager

access = AccessControlManager(connection_string=connection_string)

# Audit user privileges
audit = access.audit_privileges()
print(f"Total users: {audit.total_users}")
print(f"Total roles: {audit.total_roles}")
print(f"Privileged users: {audit.privileged_users}")

for user in audit.users_with_excessive_privileges:
    print(f"  {user.name}: {user.excessive_privileges}")
```

### Configuration Security

```python
from db_management import SecurityAuditor

security = SecurityAuditor(connection_string=connection_string)

# Check configuration security
audit = security.audit_configuration()
print(f"Security score: {audit.score:.1f}%")

for issue in audit.issues:
    print(f"  [{issue.severity}] {issue.description}")
    print(f"    Recommendation: {issue.recommendation}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Disk space full | Cannot write WAL | Increase disk space, archive old data |
| Lock contention | Queries blocking | Check lock holders, optimize queries |
| Connection exhaustion | Too many clients | Increase max_connections, use pooling |
| Vacuum not running | Dead tuples accumulating | Check autovacuum settings, run manual vacuum |
| Configuration drift | Performance degradation | Compare configs, apply recommended settings |

### Diagnostic Queries

```sql
-- Check database size
SELECT
    datname,
    pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;

-- Check table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) AS table_size,
    pg_size_pretty(pg_indexes_size(schemaname || '.' || tablename)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC;

-- Check bloat
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
    n_dead_tup,
    n_live_tup,
    ROUND(n_dead_tup::float / NULLIF(n_live_tup, 0) * 100, 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## API Reference

### DatabaseManager

```python
class DatabaseManager:
    def __init__(self, connection_string: str)
    def create_database(self, name: str, **kwargs) -> DatabaseInfo
    def clone_database(self, source: str, target: str, options: CloneOptions = None) -> DatabaseInfo
    def drop_database(self, name: str, confirm: bool = False) -> DropResult
    def archive_data(self, database: str, table: str, older_than_days: int, archive_to: str) -> ArchiveResult
    def list_databases(self) -> list[DatabaseInfo]
    def get_database_size(self, name: str) -> SizeInfo
```

### SpaceManager

```python
class SpaceManager:
    def __init__(self, connection_string: str)
    def get_database_size(self) -> SizeInfo
    def get_table_sizes(self) -> list[TableSize]
    def detect_bloat(self) -> list[BloatInfo]
    def vacuum(self, table: str = None, full: bool = False, analyze: bool = True) -> VacuumResult
    def vacuum_adaptive(self, tables: list[str], strategy: VacuumStrategy) -> VacuumResult
    def reindex(self, table: str = None, index: str = None) -> ReindexResult
    def reindex_online(self, table: str, index: str, strategy: ReindexStrategy) -> ReindexResult
```

### ConfigManager

```python
class ConfigManager:
    def __init__(self, connection_string: str)
    def get_parameters(self, category: str = None) -> list[Parameter]
    def set_parameter(self, name: str, value: str, context: str = "superuser") -> ConfigChangeResult
    def apply_batch(self, changes: list[ConfigChange], validate_first: bool = True) -> BatchResult
    def diff_configurations(self, env1: str, env2: str) -> list[ConfigDiff]
    def validate_configuration(self) -> ValidationResult
    def get_configuration_history(self) -> list[ConfigHistory]
```

### MaintenanceScheduler

```python
class MaintenanceScheduler:
    def __init__(self, connection_string: str)
    def schedule(self, task: MaintenanceTask, schedule: str, targets: list[str], options: dict = None) -> ScheduleResult
    def run_maintenance_window(self, start_hour: int, end_hour: int, tasks: list[MaintenanceTask]) -> WindowResult
    def get_schedules(self) -> list[Schedule]
    def get_history(self, limit: int = 100) -> list[MaintenanceHistory]
    def cancel_task(self, task_id: str) -> CancelResult
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class DatabaseState(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    CORRUPTED = "corrupted"

class MaintenanceTask(Enum):
    VACUUM = "vacuum"
    ANALYZE = "analyze"
    REINDEX = "reindex"
    CHECK = "check"
    CLUSTER = "cluster"

@dataclass
class DatabaseInfo:
    name: str
    owner: str
    encoding: str
    collate: str
    ctype: str
    size_bytes: int
    state: DatabaseState
    created_at: datetime
    last_vacuum: Optional[datetime]
    last_analyze: Optional[datetime]

@dataclass
class TableSize:
    schema_name: str
    table_name: str
    total_size_bytes: int
    table_size_bytes: int
    index_size_bytes: int
    row_count: int
    dead_tuples: int
    live_tuples: int

@dataclass
class BloatInfo:
    schema_name: str
    table_name: str
    bloat_percentage: float
    wasted_bytes: int
    dead_tuples: int
    live_tuples: int

@dataclass
class ConfigChange:
    parameter: str
    value: str
    context: str
    requires_restart: bool = False
    applied_at: Optional[datetime] = None
    applied_by: Optional[str] = None
```

## Deployment Guide

### Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: db-management
spec:
  replicas: 1
  selector:
    matchLabels:
      app: db-management
  template:
    metadata:
      labels:
        app: db-management
    spec:
      containers:
      - name: db-management
        image: db-management:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Monitoring & Observability

### Metrics Collection

```python
from db_management import MetricsCollector

collector = MetricsCollector()

# Collect database metrics
collector.gauge("db.size.bytes", size_bytes, tags={"database": name})
collector.gauge("db.table.size.bytes", table_size_bytes, tags={"table": name})
collector.gauge("db.bloat.percentage", bloat_percentage, tags={"table": name})

# Collect maintenance metrics
collector.histogram("db.vacuum.duration.seconds", duration)
collector.counter("db.vacuum.total", count)
collector.gauge("db.dead.tuples", dead_count, tags={"table": name})
```

### Alerting Rules

```yaml
groups:
  - name: database_management_alerts
    rules:
      - alert: DatabaseDiskSpaceHigh
        expr: db_disk_usage_percent > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Database disk space above 80%"
          
      - alert: TableBloatHigh
        expr: db_bloat_percentage > 20
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Table bloat above 20%"
          
      - alert: DeadTuplesAccumulating
        expr: db_dead_tuples > 10000
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Dead tuples accumulating"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from db_management import DatabaseManager, SpaceManager

@pytest.fixture
def manager():
    return DatabaseManager(connection_string="postgresql://localhost/test")

def test_create_database(manager):
    db = manager.create_database(name="test_db")
    assert db.name == "test_db"
    assert db.state == DatabaseState.ACTIVE

def test_vacuum(manager):
    space = SpaceManager(connection_string="postgresql://localhost/test")
    result = space.vacuum(table="test_table")
    assert result.success
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| PostgreSQL | 12 | 15+ |
| Python | 3.9 | 3.11+ |

## Glossary

| Term | Definition |
|------|------------|
| **VACUUM** | PostgreSQL operation to reclaim space from dead tuples |
| **REINDEX** | Rebuild an index to reclaim space and improve performance |
| **ANALYZE** | Update table statistics for query planner |
| **Bloat** | Unused space in tables/indexes due to updates/deletes |
| **Dead Tuples** | Rows marked for deletion but not yet reclaimed |
| **Tablespace** | Location where database stores data files |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added adaptive vacuum strategy
- New online reindex capability
- Improved configuration management
- Added batch configuration changes

### Version 2.5.0 (2023-12-01)
- Added maintenance scheduling
- New space management dashboard
- Improved bloat detection
- Added configuration validation

## Contributing Guidelines

```bash
# Clone and setup
git clone https://github.com/awesome-grok/db-management.git
cd db-management
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills