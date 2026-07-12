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