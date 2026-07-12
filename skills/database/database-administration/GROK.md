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