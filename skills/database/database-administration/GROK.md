---
name: "Database Administration"
version: "2.0.0"
description: "Comprehensive database administration toolkit with connection pooling, schema management, query execution, user access control, backup orchestration, and multi-database support for production database operations"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database", "administration", "connection-pooling", "schema-management", "backup", "multi-database"]
category: "database"
personality: "dba"
use_cases: ["database management", "connection pooling", "schema migrations", "backup orchestration", "access control"]
---

# Database Administration

> Production-grade database administration framework providing connection pooling, schema management, query execution, user access control, backup orchestration, and multi-database support for reliable database operations.

## Overview

The Database Administration module provides a unified API for managing relational and NoSQL databases in production environments. It implements connection pooling with health checks, schema versioning and migration, automated backup scheduling with point-in-time recovery, user and role-based access control, query logging and performance monitoring, and multi-database support (PostgreSQL, MySQL, SQLite, MongoDB). Every operation includes retry logic, timeout management, and structured audit logging.

## Core Capabilities

### 1. Connection Pool Management
- Thread-safe connection pooling with configurable min/max connections
- Health checks with automatic dead connection removal
- Connection lifecycle management (acquire, use, release)
- Read/write splitting for primary-replica setups
- Connection timeout and idle connection recycling

### 2. Schema Management
- Versioned schema migrations with forward/backward support
- Schema diffing between environments
- Automated migration generation from model changes
- Rollback support with dependency tracking
- Migration locking for concurrent deployment safety

### 3. Backup and Recovery
- Full, incremental, and differential backup scheduling
- Point-in-time recovery with WAL archiving
- Backup verification and integrity checks
- Cross-region backup replication
- Restore with configurable RPO and RTO targets

### 4. User and Access Control
- Role-based access control (RBAC) with hierarchical roles
- Database-level, schema-level, and table-level permissions
- API key management with rotation and expiration
- Audit logging of all access and privilege changes
- Row-level security policies

### 5. Query Execution and Monitoring
- Parameterized query execution with injection protection
- Query plan analysis and optimization hints
- Slow query detection and logging
- Connection and query metrics collection
- Deadlock detection and resolution

### 6. Multi-Database Support
- PostgreSQL, MySQL, SQLite, MongoDB, Redis
- Database-agnostic schema definitions
- Cross-database query federation
- Connection string parsing and management
- Driver auto-detection and fallback

## Usage Examples

### Connection Pool Setup

```python
from database_administration import ConnectionPool, PoolConfig

pool_config = PoolConfig(
    host="db-primary.example.com",
    port=5432,
    database="production",
    user="app_user",
    password_env_var="DB_PASSWORD",
    min_connections=5,
    max_connections=20,
    max_idle_time_seconds=300,
    connection_timeout_seconds=10,
    health_check_interval=60,
    enable_ssl=True,
)

pool = ConnectionPool(config=pool_config)

# Acquire and use a connection
with pool.acquire() as conn:
    result = conn.execute("SELECT * FROM users WHERE active = $1", True)
    print(f"Active users: {result.row_count}")
```

### Schema Migration

```python
from database_administration import MigrationManager, Migration

manager = MigrationManager(pool=pool)

# Create a migration
migration = Migration(
    version="20240115_001",
    description="Add user preferences table",
    up=[
        "CREATE TABLE user_preferences ("
        "  user_id UUID PRIMARY KEY REFERENCES users(id),"
        "  theme VARCHAR(20) DEFAULT 'light',"
        "  language VARCHAR(10) DEFAULT 'en',"
        "  notifications_enabled BOOLEAN DEFAULT TRUE"
        ");",
        "CREATE INDEX idx_user_preferences_user ON user_preferences(user_id);",
    ],
    down=[
        "DROP TABLE IF EXISTS user_preferences;",
    ],
)

manager.register(migration)
manager.migrate(target="20240115_001")

# Check migration status
status = manager.status()
for m in status:
    print(f"  {m.version}: {m.description} ({m.state})")
```

### Backup Orchestration

```python
from database_administration import BackupManager, BackupSchedule

backup = BackupManager(pool=pool, backup_dir="/backups/postgres")

# Schedule daily backups
schedule = BackupSchedule(
    name="daily_full",
    frequency="daily",
    time="02:00",
    retention_days=30,
    compression=True,
    encryption_key_env="BACKUP_ENCRYPTION_KEY",
)

backup.schedule(schedule)

# Run immediate backup
result = backup.run_full_backup(tag="pre-deploy")
print(f"Backup: {result.filename} ({result.size_mb:.1f} MB, {result.duration_seconds:.1f}s)")

# List available backups
backups = backup.list_backups(retention_days=7)
for b in backups:
    print(f"  {b.filename}: {b.size_mb:.1f} MB, {b.timestamp}")
```

### Access Control

```python
from database_administration import AccessControl, Role, Permission

acl = AccessControl(pool=pool)

# Define roles
admin_role = Role(
    name="admin",
    permissions=[
        Permission.ALL,
    ],
)

app_role = Role(
    name="app_service",
    permissions=[
        Permission.SELECT,
        Permission.INSERT,
        Permission.UPDATE,
        Permission.EXECUTE,
    ],
    row_level_security={
        "users": "organization_id = current_setting('app.org_id')::uuid",
    },
)

# Grant roles
acl.grant_role(user="db_admin", role=admin_role, database="production")
acl.grant_role(user="app_svc", role=app_role, database="production")

# Audit access
audit_log = acl.get_audit_log(user="app_svc", limit=10)
for entry in audit_log:
    print(f"  {entry.timestamp}: {entry.operation} on {entry.table}")
```

### Query Monitoring

```python
from database_administration import QueryMonitor, SlowQueryThreshold

monitor = QueryMonitor(pool=pool, threshold=SlowQueryThreshold(milliseconds=500))

# Execute monitored query
with monitor.track("user_lookup") as tracking:
    result = conn.execute("SELECT * FROM users WHERE email = $1", email)
    tracking.set_metadata("rows_returned", result.row_count)

# Get slow queries
slow = monitor.get_slow_queries(limit=10)
for q in slow:
    print(f"  {q.duration_ms:.0f}ms: {q.query[:80]}...")

# Performance metrics
metrics = monitor.get_metrics()
print(f"  Avg query time: {metrics.avg_duration_ms:.1f}ms")
print(f"  Queries/sec:    {metrics.queries_per_second:.1f}")
print(f"  Error rate:     {metrics.error_rate:.4f}")
```

## Best Practices

### Connection Pooling
- Set max_connections to 2-4x CPU cores for OLTP workloads
- Monitor idle connections — they consume memory on the database server
- Use read replicas for read-heavy workloads with explicit read/write splitting
- Always set connection timeouts to prevent pool exhaustion during database outages

### Schema Management
- Never modify production schemas manually — always use migrations
- Test migrations against a copy of production data before deploying
- Add indexes concurrently in production to avoid table locks
- Keep migrations small and focused — one logical change per migration

### Backup Strategy
- Follow the 3-2-1 rule: 3 copies, 2 different media, 1 offsite
- Verify backup integrity by restoring to a test environment monthly
- Set RPO (Recovery Point Objective) and RTO (Recovery Time Objective) for each database
- Encrypt backups at rest and in transit

### Access Control
- Follow least-privilege principle — grant only what's needed
- Use separate accounts for applications and administrators
- Rotate credentials regularly; use environment variables, not config files
- Enable audit logging for all databases containing sensitive data

## Related Modules

- **mongodb**: MongoDB-specific administration and operations
- **query-optimization**: Query performance analysis and optimization
- **data-modeling**: Schema design and entity relationship modeling
- **replication**: Database replication and high availability setup

---

## Advanced Configuration

### Connection Pool Tuning

```python
# Advanced pool configuration for high-throughput workloads
pool_config = PoolConfig(
    host="db-primary.example.com",
    port=5432,
    database="production",
    # Pool sizing
    min_connections=10,
    max_connections=50,
    max_overflow=20,  # Temporary connections above max
    # Timeouts
    connection_timeout_seconds=5,
    idle_timeout_seconds=300,
    max_lifetime_seconds=3600,
    # Health checks
    health_check_interval=30,
    health_check_timeout=5,
    # SSL/TLS
    enable_ssl=True,
    ssl_ca="/etc/ssl/certs/ca.pem",
    ssl_cert="/etc/ssl/certs/client.pem",
    ssl_key="/etc/ssl/private/client.key",
    ssl_verify=True,
    # Logging
    log_queries=True,
    log_slow_queries_threshold_ms=1000,
    # Retry logic
    retry_attempts=3,
    retry_delay_seconds=1,
    retry_backoff_multiplier=2,
)
```

### Query Execution Modes

```python
from database_administration import QueryExecutor, ExecutionMode

executor = QueryExecutor(pool=pool)

# Read-only mode with automatic read replica routing
result = executor.execute(
    "SELECT * FROM users WHERE active = true",
    mode=ExecutionMode.READ_ONLY,
    read_preference="replica",
)

# Write mode with primary routing
result = executor.execute(
    "INSERT INTO audit_log (action, user_id) VALUES ($1, $2)",
    params=["login", user_id],
    mode=ExecutionMode.WRITE,
)

# Transaction mode with isolation level
with executor.transaction(isolation_level="REPEATABLE READ") as tx:
    tx.execute("UPDATE accounts SET balance = balance - $1 WHERE id = $2", amount, from_id)
    tx.execute("UPDATE accounts SET balance = balance + $1 WHERE id = $2", amount, to_id)
```

### Advanced Backup Configuration

```python
from database_administration import BackupManager, BackupPolicy, RetentionPolicy

backup = BackupManager(pool=pool, backup_dir="/backups/postgres")

# Configure retention policy
retention = RetentionPolicy(
    daily_retention_days=7,
    weekly_retention_weeks=4,
    monthly_retention_months=12,
    yearly_retention_years=5,
    min_backups_to_keep=5,
    always_keep_last_n=3,
)
backup.set_retention(retention)

# Configure encrypted backups
policy = BackupPolicy(
    compression_algorithm="zstd",
    compression_level=3,
    encryption_algorithm="AES-256-GCM",
    encryption_key_env="BACKUP_ENCRYPTION_KEY",
    checksum_algorithm="sha256",
    parallel_threads=4,
    chunk_size_mb=64,
)
backup.set_policy(policy)
```

## Architecture Patterns

### Single Primary with Read Replicas

```
┌─────────────────┐
│   Application   │
└────────┬────────┘
         │
    ┌────┴────┐
    │  Proxy  │
    └────┬────┘
         │
    ┌────┴────┐
    │ Primary │ ◄─── Writes
    └────┬────┘
         │
    ┌────┴────┐
    │Replica 1│ ◄─── Reads
    └─────────┘
    ┌─────────┐
    │Replica 2│ ◄─── Reads
    └─────────┘
```

### Multi-Region Deployment

```
┌──────────────────┐     ┌──────────────────┐
│    Region A      │     │    Region B      │
│                  │     │                  │
│  ┌────────────┐  │     │  ┌────────────┐  │
│  │  Primary   │◄─┼─────┼──│  Replica   │  │
│  └─────┬──────┘  │     │  └─────┬──────┘  │
│        │         │     │        │         │
│  ┌─────┴──────┐  │     │  ┌─────┴──────┐  │
│  │  Replica   │  │     │  │  Replica   │  │
│  └────────────┘  │     │  └────────────┘  │
└──────────────────┘     └──────────────────┘
```

### Connection Pool Architecture

```
┌─────────────────────────────────────┐
│         Application Layer           │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│        Connection Pool Layer         │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │Conn1│ │Conn2│ │Conn3│ │ConnN│  │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘  │
└─────┼───────┼───────┼───────┼──────┘
      │       │       │       │
      └───────┴───────┴───────┘
               │
┌──────────────┴──────────────────────┐
│         Database Server             │
└─────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with FastAPI
from fastapi import FastAPI, Depends
from database_administration import DatabaseManager

app = FastAPI()
db = DatabaseManager(pool_config=pool_config)

async def get_db():
    async with db.acquire() as conn:
        yield conn

@app.get("/users/{user_id}")
async def get_user(user_id: str, conn = Depends(get_db)):
    result = await conn.execute("SELECT * FROM users WHERE id = $1", user_id)
    return result.first()
```

### ORM Integration

```python
# Integration with SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_administration import PoolProxy

# Create proxy that wraps our connection pool
proxy = PoolProxy(pool)

engine = create_engine(
    "postgresql://",
    creator=proxy.get_connection,
    pool_pre_ping=True,
    pool_recycle=3600,
)

Session = sessionmaker(bind=engine)
```

### Monitoring Integration

```python
# Integration with Prometheus
from prometheus_client import Counter, Histogram, Gauge

QUERY_COUNT = Counter('db_queries_total', 'Total queries', ['status'])
QUERY_DURATION = Histogram('db_query_duration_seconds', 'Query duration')
POOL_SIZE = Gauge('db_pool_connections', 'Pool connections', ['state'])

class MetricsCollector:
    def record_query(self, duration, success):
        QUERY_COUNT.labels(status='success' if success else 'error').inc()
        QUERY_DURATION.observe(duration)
    
    def record_pool(self, active, idle):
        POOL_SIZE.labels(state='active').set(active)
        POOL_SIZE.labels(state='idle').set(idle)
```

## Performance Optimization

### Connection Pool Optimization

| Metric | Recommended | Warning | Critical |
|--------|-------------|---------|----------|
| Active connections | < 80% max | 80-90% max | > 90% max |
| Idle connections | 10-20% of max | < 5% or > 50% | 0 or > 70% |
| Connection wait time | < 10ms | 10-100ms | > 100ms |
| Connection errors | 0 | < 1% | > 1% |

### Query Performance Tuning

```sql
-- Analyze slow queries
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Monitor table bloat
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    n_dead_tup,
    n_live_tup,
    ROUND(n_dead_tup::float / NULLIF(n_live_tup, 0) * 100, 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

### Caching Strategies

```python
from database_administration import QueryCache, CachePolicy

# Configure query cache
cache = QueryCache(
    max_size_mb=256,
    default_ttl_seconds=300,
    policy=CachePolicy.LRU,
    eviction_callback=lambda key: print(f"Evicted: {key}"),
)

# Cache frequent queries
@cache.memoize(ttl=600)
async def get_user_permissions(user_id: str):
    return await conn.execute(
        "SELECT permission FROM user_permissions WHERE user_id = $1",
        user_id
    )
```

## Security Considerations

### Authentication and Authorization

```python
from database_administration import SecurityManager

security = SecurityManager(pool=pool)

# Configure authentication methods
security.configure_auth(
    method="scram-sha-256",
    password_policy={
        "min_length": 16,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_digits": True,
        "require_special": True,
        "rotation_days": 90,
    },
)

# Create application user with limited privileges
security.create_user(
    username="app_readonly",
    password_env="APP_DB_PASSWORD",
    roles=["SELECT"],
    connection_limit=10,
    valid_until="2025-12-31",
)

# Enable row-level security
security.enable_row_level_security(
    table="users",
    policy_name="org_isolation",
    using="organization_id = current_setting('app.org_id')::uuid",
)
```

### Audit Logging

```python
# Configure comprehensive audit logging
security.configure_audit(
    log_connections=True,
    log_disconnections=True,
    log_ddl=True,
    log_dml=False,  # Can be expensive
    log_truncate=True,
    log_alter=True,
    log_grant=True,
    log_revoke=True,
)

# Query audit log
audit_entries = security.get_audit_log(
    start_date="2024-01-01",
    end_date="2024-01-31",
    filter_by_user="admin",
    filter_by_action="ALTER",
)
```

### Data Encryption

```python
# Configure encryption at rest
security.configure_encryption(
    column_encryption={
        "users.email": {"algorithm": "AES-256", "key_env": "EMAIL_ENCRYPTION_KEY"},
        "users.ssn": {"algorithm": "AES-256", "key_env": "SSN_ENCRYPTION_KEY"},
    },
    transparent_data_encryption=True,
    backup_encryption=True,
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Connection exhaustion | "Too many connections" error | Increase max_connections or optimize pool sizing |
| Slow queries | High mean_time in pg_stat_statements | Add indexes, rewrite queries, check statistics |
| Replication lag | Replicas falling behind | Check network, optimize WAL settings |
| Lock contention | Deadlocks in logs | Reduce transaction scope, add proper indexing |
| Disk space | Tables growing unbounded | Implement partitioning, archive old data |

### Diagnostic Queries

```sql
-- Check connection count by state
SELECT state, COUNT(*)
FROM pg_stat_activity
GROUP BY state;

-- Find long-running transactions
SELECT pid, now() - xact_start AS duration, query
FROM pg_stat_activity
WHERE state != 'idle'
AND xact_start < now() - interval '5 minutes'
ORDER BY duration DESC;

-- Check for table locks
SELECT
    l.mode,
    l.granted,
    a.query,
    a.pid
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE l.relation = 'users'::regclass;

-- Monitor background workers
SELECT * FROM pg_stat_activity
WHERE backend_type = 'background worker';
```

### Performance Debugging

```python
from database_administration import DiagnosticTool

diag = DiagnosticTool(pool=pool)

# Run comprehensive health check
health = diag.health_check()
print(f"Status: {health.status}")
print(f"Connections: {health.connection_count}/{health.max_connections}")
print(f"Cache hit ratio: {health.cache_hit_ratio:.2%}")
print(f"Replication lag: {health.replication_lag_seconds}s")

# Get detailed diagnostics
details = diag.detailed_diagnostics()
for check in details.checks:
    status = "PASS" if check.passed else "FAIL"
    print(f"[{status}] {check.name}: {check.message}")
```

## API Reference

### ConnectionPool

```python
class ConnectionPool:
    def __init__(self, config: PoolConfig)
    def acquire(self, timeout: float = None) -> ConnectionContext
    def execute(self, query: str, params: list = None) -> QueryResult
    def execute_many(self, query: str, params_list: list) -> QueryResult
    def get_stats(self) -> PoolStats
    def health_check(self) -> bool
    def resize(self, min_connections: int, max_connections: int)
    def close(self, timeout: float = 30)
```

### MigrationManager

```python
class MigrationManager:
    def __init__(self, pool: ConnectionPool)
    def register(self, migration: Migration)
    def migrate(self, target: str = None) -> MigrationResult
    def rollback(self, target: str) -> MigrationResult
    def status(self) -> list[MigrationStatus]
    def history(self) -> list[MigrationHistory]
    def generate_migration(self, name: str, changes: dict) -> Migration
    def validate(self, migration: Migration) -> ValidationResult
```

### BackupManager

```python
class BackupManager:
    def __init__(self, pool: ConnectionPool, backup_dir: str)
    def run_full_backup(self, tag: str = None) -> BackupResult
    def run_incremental(self, base_backup: str) -> BackupResult
    def list_backups(self, retention_days: int = None) -> list[BackupInfo]
    def restore(self, backup_id: str, target_time: datetime = None) -> RestoreResult
    def verify(self, backup_id: str) -> VerificationResult
    def schedule(self, schedule: BackupSchedule)
    def delete_old_backups(self) -> int
```

### AccessControl

```python
class AccessControl:
    def __init__(self, pool: ConnectionPool)
    def create_role(self, role: Role) -> Role
    def grant_role(self, user: str, role: Role, database: str)
    def revoke_role(self, user: str, role: str, database: str)
    def list_roles(self) -> list[Role]
    def list_users(self) -> list[User]
    def get_audit_log(self, user: str = None, limit: int = 100) -> list[AuditEntry]
    def check_permission(self, user: str, permission: Permission, resource: str) -> bool
```

### QueryMonitor

```python
class QueryMonitor:
    def __init__(self, pool: ConnectionPool, threshold: SlowQueryThreshold)
    def track(self, label: str) -> QueryTracking
    def get_slow_queries(self, limit: int = 10) -> list[SlowQuery]
    def get_metrics(self) -> QueryMetrics
    def get_plan(self, query: str) -> ExecutionPlan
    def explain(self, query: str) -> ExplainResult
    def reset_stats(self)
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List

class DatabaseType(Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    REDIS = "redis"

class ConnectionState(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    STALE = "stale"
    FAILED = "failed"

@dataclass
class ConnectionInfo:
    id: str
    state: ConnectionState
    created_at: datetime
    last_used: datetime
    query_count: int
    total_duration_ms: float
    database: str
    user: str
    client_address: str

@dataclass
class Migration:
    version: str
    description: str
    up: List[str]
    down: List[str]
    created_at: datetime
    applied_at: Optional[datetime]
    checksum: str
    dependencies: List[str]

@dataclass
class BackupInfo:
    id: str
    filename: str
    timestamp: datetime
    size_mb: float
    duration_seconds: float
    compressed: bool
    encrypted: bool
    verified: bool
    tag: Optional[str]
    checksum: str
```

## Deployment Guide

### Prerequisites

- Python 3.9+
- PostgreSQL 12+ / MySQL 8.0+ / MongoDB 4.4+
- pip or poetry for package management

### Installation

```bash
# Install via pip
pip install database-administration

# Install with optional dependencies
pip install database-administration[postgresql,monitoring,backup]

# Development installation
pip install -e ".[dev]"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_HOST=db-primary
ENV DB_PORT=5432
ENV DB_NAME=production

CMD ["python", "-m", "database_administration.server"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: db-admin
spec:
  replicas: 3
  selector:
    matchLabels:
      app: db-admin
  template:
    metadata:
      labels:
        app: db-admin
    spec:
      containers:
      - name: db-admin
        image: db-admin:latest
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: password
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
from database_administration import MetricsCollector

collector = MetricsCollector()

# Collect connection pool metrics
collector.gauge("db.pool.active_connections", pool.active_count())
collector.gauge("db.pool.idle_connections", pool.idle_count())
collector.gauge("db.pool.wait_time_ms", pool.avg_wait_time())

# Collect query metrics
collector.counter("db.queries.total", query_count, tags={"status": "success"})
collector.histogram("db.query.duration_ms", query_duration)
collector.counter("db.slow_queries.total", slow_count)
```

### Alerting Rules

```yaml
groups:
  - name: database_alerts
    rules:
      - alert: HighConnectionUsage
        expr: db_pool_active_connections / db_pool_max_connections > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High connection pool usage"
          
      - alert: SlowQueries
        expr: rate(db_slow_queries_total[5m]) > 10
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High rate of slow queries"
          
      - alert: ReplicationLag
        expr: db_replication_lag_seconds > 30
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Replication lag exceeds threshold"
```

### Dashboard Configuration

```json
{
  "title": "Database Administration Dashboard",
  "panels": [
    {
      "title": "Connection Pool",
      "type": "stat",
      "targets": ["db.pool.active_connections", "db.pool.idle_connections"]
    },
    {
      "title": "Query Performance",
      "type": "graph",
      "targets": ["db.query.duration_ms{quantile=\"0.95\"}"]
    },
    {
      "title": "Slow Queries",
      "type": "timeseries",
      "targets": ["rate(db.slow_queries_total[5m])"]
    }
  ]
}
```

## Testing Strategy

### Unit Tests

```python
import pytest
from database_administration import ConnectionPool, PoolConfig

@pytest.fixture
def pool():
    config = PoolConfig(
        host="localhost",
        database="test_db",
        min_connections=1,
        max_connections=5,
    )
    return ConnectionPool(config=config)

def test_pool_acquire_release(pool):
    with pool.acquire() as conn:
        result = conn.execute("SELECT 1")
        assert result.scalar() == 1

def test_pool_health_check(pool):
    assert pool.health_check() is True
```

### Integration Tests

```python
@pytest.mark.integration
def test_migration_rollback(pool):
    manager = MigrationManager(pool=pool)
    
    # Apply migration
    manager.migrate(target="20240115_001")
    status = manager.status()
    assert any(m.version == "20240115_001" for m in status)
    
    # Rollback
    manager.rollback(target="20240115_001")
    status = manager.status()
    assert not any(m.version == "20240115_001" and m.state == "applied" for m in status)
```

### Load Tests

```python
import asyncio
from database_administration import ConnectionPool

async def test_pool_under_load():
    pool = ConnectionPool(config=pool_config)
    
    async def worker():
        for _ in range(100):
            with pool.acquire() as conn:
                await conn.execute("SELECT pg_sleep(0.01)")
    
    # Run 50 concurrent workers
    await asyncio.gather(*[worker() for _ in range(50)])
    
    stats = pool.get_stats()
    assert stats.error_rate < 0.01
    assert stats.avg_wait_time_ms < 100
```

## Versioning & Migration

### Semantic Versioning

- **Major** (X.0.0): Breaking changes to API or behavior
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible

### Migration Path

```python
from database_administration import VersionManager

version_manager = VersionManager()

# Check current version
current = version_manager.current_version()
print(f"Current version: {current}")

# Check for available updates
updates = version_manager.check_updates()
for update in updates:
    print(f"Available: {update.version} ({update.release_date})")

# Generate migration path
migration_path = version_manager.get_migration_path(
    from_version="2.0.0",
    to_version="3.0.0",
)
for step in migration_path:
    print(f"Step: {step.description}")
```

### Breaking Changes Handling

```python
# Version compatibility wrapper
class BackwardCompatiblePool:
    def __init__(self, config, version="3.0.0"):
        self.version = version
        self.pool = ConnectionPool(config=config)
    
    def execute(self, *args, **kwargs):
        if self.version.startswith("2."):
            # Legacy behavior
            return self._execute_legacy(*args, **kwargs)
        else:
            # New behavior
            return self.pool.execute(*args, **kwargs)
```

## Glossary

| Term | Definition |
|------|------------|
| **Connection Pool** | A cache of database connections that can be reused |
| **WAL** | Write-Ahead Logging - ensures data durability |
| **RPO** | Recovery Point Objective - maximum acceptable data loss |
| **RTO** | Recovery Time Objective - maximum acceptable downtime |
| **RBAC** | Role-Based Access Control |
| **DDL** | Data Definition Language (CREATE, ALTER, DROP) |
| **DML** | Data Manipulation Language (SELECT, INSERT, UPDATE, DELETE) |
| **Replication Lag** | Time delay between primary and replica |
| **Split-Brain** | When two nodes both think they are primary |
| **Fencing** | Mechanism to prevent split-brain scenarios |

## Changelog

### Version 3.0.0 (2024-01-15)

- Added support for PostgreSQL 16
- New connection pool statistics API
- Improved migration locking mechanism
- Added backup verification checksums

### Version 2.5.0 (2023-12-01)

- Added MySQL 8.0 support
- New query monitoring dashboard
- Improved error handling and retry logic
- Added row-level security support

### Version 2.0.0 (2023-09-15)

- Major API redesign
- Added connection pooling
- New backup encryption support
- Improved migration system

### Version 1.5.0 (2023-06-01)

- Added SQLite support
- New audit logging
- Improved performance metrics

### Version 1.0.0 (2023-03-01)

- Initial release
- PostgreSQL support
- Basic connection pooling
- Schema migrations
- Backup and restore

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/awesome-grok/database-administration.git
cd database-administration

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
mypy .
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all public functions
- Write docstrings for all public classes and methods
- Keep functions under 50 lines
- Maximum line length: 88 characters

### Pull Request Process

1. Create a feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Submit pull request with clear description
6. Address review feedback

### Commit Messages

```
feat: Add connection pool statistics API
fix: Handle timeout errors in backup verification
docs: Update migration guide for v3.0
refactor: Simplify query monitoring logic
test: Add integration tests for failover
```

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