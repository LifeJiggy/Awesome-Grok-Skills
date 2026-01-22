# Database Administration Agent

## Overview

The **Database Administration Agent** provides comprehensive database management capabilities including performance optimization, backup/recovery, security, and high availability. This agent helps maintain healthy, performant, and secure database systems.

## Core Capabilities

### 1. Database Management
Day-to-day DBA operations:
- **Instance Management**: Start, stop, configure
- **Database Creation**: Schema design, initialization
- **User Management**: Authentication, authorization
- **Backup Scheduling**: Automated backup jobs
- **Monitoring Setup**: Performance baselines

### 2. Query Optimization
Improve database performance:
- **Execution Plan Analysis**: Query profiling
- **Index Management**: Create, rebuild, drop
- **Statistics Updates**: Histogram refresh
- **Query Rewrite**: Alternative formulations
- **Materialized Views**: Pre-computed results

### 3. Backup and Recovery
Data protection and restoration:
- **Full Backups**: Complete database snapshots
- **Incremental Backups**: Transaction log backups
- **Point-in-Time Recovery**: Restore to specific time
- **Disaster Recovery**: DR procedures, testing
- **Backup Verification**: Integrity checks

### 4. Security Management
Database security hardening:
- **Access Control**: User permissions, roles
- **Encryption**: Data at rest, in transit
- **Auditing**: Activity logging, compliance
- **Vulnerability Assessment**: Security scanning
- **Compliance Reporting**: Regulatory requirements

### 5. Replication Management
High availability configuration:
- **Primary/Replica Setup**: Master-slave replication
- **Multi-Master**: Active-active configuration
- **Failover Procedures**: Automatic promotion
- **Lag Monitoring**: Replication delay tracking
- **Conflict Resolution**: Data consistency

## Usage Examples

### Connect and Manage

```python
from db_admin import DatabaseManager, DatabaseConfig

db = DatabaseManager()
config = DatabaseConfig(
    host='localhost',
    port=5432,
    database='mydb',
    user='admin',
    password='pass',
    database_type=DatabaseType.POSTGRESQL
)
conn = db.connect(config)
```

### Optimize Query

```python
from db_admin import QueryOptimizer

optimizer = QueryOptimizer()
plan = optimizer.explain_query("SELECT * FROM users WHERE email = ?")
print(f"Plan: {plan['plan']['operation']}")
print(f"Rows: {plan['plan']['rows_examined']}")
recommendations = optimizer.suggest_indexes(slow_queries)
```

### Backup Management

```python
from db_admin import BackupManager

backup = BackupManager()
b = backup.create_backup('mydb', BackupType.FULL, '/backups/mydb.dump')
print(f"Backup: {b['id']}, Size: {b['size_gb']}GB")

restored = backup.restore_database(b['id'], 'mydb_restored')
print(f"Restored: {restored['rows_restored']}")
```

### Monitor Performance

```python
from db_admin import PerformanceMonitor

monitor = PerformanceMonitor()
metrics = monitor.get_database_metrics('mydb')
print(f"Cache hit: {metrics['cache_hit_ratio']}")
print(f"Connections: {metrics['connections']}")
slow_queries = monitor.get_slow_queries(threshold_ms=1000)
```

### Configure Replication

```python
from db_admin import ReplicationManager

replication = ReplicationManager()
setup = replication.setup_replication('primary', 'replica_1', 'async')
print(f"Replication: {setup['status']}, Lag: {setup['lag_seconds']}s")

failover = replication.failover('replica_1')
print(f"Failover: {failover['downtime_seconds']}s downtime")
```

## Performance Optimization

### Index Strategies

| Index Type | Use Case | Example |
|------------|----------|---------|
| B-Tree | Equality, range queries | `CREATE INDEX idx ON table(col)` |
| Hash | Exact match | `CREATE INDEX idx ON table(col) USING HASH` |
| GIN | Array, JSONB | `CREATE INDEX idx ON table USING GIN(col)` |
| GiST | Geometric | `CREATE INDEX idx ON table USING GIST(geom)` |

### Query Patterns

### Before (Slow)
```sql
SELECT * FROM orders WHERE YEAR(created_at) = 2024
```
- Full table scan

### After (Fast)
```sql
SELECT * FROM orders WHERE created_at >= '2024-01-01' 
AND created_at < '2025-01-01'
```
- Index usage

## Backup Strategies

### Backup Types

| Type | Size | Recovery Time | Use Case |
|------|------|---------------|----------|
| Full | Large | Longer | Weekly |
| Incremental | Small | Varies | Daily |
| Differential | Medium | Medium | Monthly |
| Continuous | Minimal | Immediate | Critical |

### Recovery Point Objectives

| Tier | RPO | Strategy |
|------|-----|----------|
| Critical | <1 min | Continuous archiving |
| Important | <1 hour | Hourly incremental |
| Standard | <24 hours | Daily full |

## Security Best Practices

### Defense in Depth
1. **Network Security**: Firewall, VPN
2. **Authentication**: Strong passwords, MFA
3. **Authorization**: Principle of least privilege
4. **Encryption**: TLS, transparent data encryption
5. **Auditing**: Comprehensive logging
6. **Updates**: Patch management

### Compliance Requirements

| Standard | Requirements | Frequency |
|----------|--------------|-----------|
| SOC 2 | Access controls, encryption | Annual audit |
| PCI-DSS | Cardholder data protection | Quarterly scan |
| HIPAA | PHI protection | Annual risk assessment |
| GDPR | Data privacy | Ongoing |

## High Availability

### HA Architectures

```
┌─────────────────────────────────────┐
│           Load Balancer             │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│Replica│ │Primary│ │Replica│
└───────┘ └───────┘ └───────┘
```

### Failover Types
- **Automatic**: Heartbeat detection, auto-promote
- **Manual**: DBA-initiated, controlled
- **Planned**: Maintenance windows

## Monitoring Metrics

### Database Metrics
- **Connections**: Active/max connections
- **Query Performance**: Response time percentiles
- **Throughput**: Queries/second
- **Cache Hit Ratio**: Buffer pool efficiency
- **Lock Contention**: Waits, deadlocks
- **Replication Lag**: Seconds behind

### Alert Thresholds
| Metric | Warning | Critical |
|--------|---------|----------|
| Connections | 70% | 90% |
| Disk Usage | 80% | 95% |
| Slow Queries | 10/min | 50/min |
| Replication Lag | 30s | 5min |

## Common DBA Tasks

### Daily
- Check backup completion
- Review error logs
- Monitor disk space
- Check replication status

### Weekly
- Update statistics
- Review performance
- Analyze slow queries
- Test recovery procedures

### Monthly
- Security audits
- Capacity planning
- Patch updates
- Compliance reviews

## Related Skills

- [NoSQL Databases](../nosql-databases/mongodb-redis/README.md) - NoSQL management
- [Performance Optimization](../performance/caching-strategies/README.md) - Performance
- [Security Assessment](../security-assessment/vulnerability-management/README.md) - Security

---

**File Path**: `skills/database-admin/db-management/resources/db_admin.py`
