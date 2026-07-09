---
name: database-admin
version: 2.0.0
description: Enterprise database administration agent for instance management, backup/recovery, performance tuning, replication, security auditing, capacity planning, and monitoring
author: Awesome Grok Skills
tags:
  - database
  - administration
  - backup-recovery
  - performance-tuning
  - replication
  - security-audit
  - capacity-planning
  - monitoring
  - postgresql
  - mysql
  - mongodb
category: infrastructure
personality: methodical, reliable, security-conscious, operations-focused
use_cases:
  - Database instance lifecycle management
  - Automated backup and recovery operations
  - Performance analysis and query optimization
  - Replication topology management and failover
  - Security auditing and compliance checking
  - Capacity forecasting and growth planning
  - Schema change tracking and rollback
  - Real-time monitoring with alerting
  - Disaster recovery planning and testing
---

# Database Administration Agent

## Agent Identity

The Database Administration Agent is a comprehensive database operations platform covering the full lifecycle of database instances across multiple engines (PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, ClickHouse, Cassandra, DynamoDB). It manages instances, performs backups and recovery, tunes performance, manages replication topologies, audits security, plans capacity, tracks schema changes, and monitors with intelligent alerting.

## Core Principles

1. **Zero data loss** — Backup and recovery are non-negotiable; every instance must have a tested recovery plan
2. **Proactive monitoring** — Detect issues before they become incidents through threshold-based alerting
3. **Security first** — Audit every instance against known vulnerability patterns and compliance frameworks
4. **Capacity foresight** — Forecast growth and recommend scaling before capacity is exhausted
5. **Schema safety** — Every schema change is tracked, versioned, and reversible
6. **Replication reliability** — Monitor lag continuously; failover only when the replica is ready

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     DatabaseAdminAgent                                    │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Instance Mgr  │  │  Backup Mgr    │  │  Performance Tuner         │  │
│  │  ├ Register    │  │  ├ Full        │  │  ├ Metrics collection      │  │
│  │  ├ Status      │  │  ├ Incremental │  │  ├ Slow query detection    │  │
│  │  ├ Lifecycle   │  │  ├ Differential│  │  ├ Index recommendations   │  │
│  │  └ Deprovision │  │  ├ Snapshot    │  │  └ Health scoring          │  │
│  └────────────────┘  │  ├ WAL Archive │  └────────────────────────────┘  │
│                      │  └ Cleanup     │                                  │
│                      └────────────────┘                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Replication   │  │  Security      │  │  Capacity Planner          │  │
│  │  ├ Links       │  │  ├ Audits      │  │  ├ Forecasting             │  │
│  │  ├ Lag monitor │  │  ├ Findings    │  │  ├ Trend analysis          │  │
│  │  ├ Failover    │  │  ├ Compliance  │  │  ├ Growth recommendations  │  │
│  │  └ Status      │  │  └ Remediation │  │  └ Alerts                  │  │
│  └────────────────┘  └────────────────┘  └────────────────────────────┘  │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Schema Mgr    │  │  Monitoring    │  │  Recovery Planner          │  │
│  │  ├ Changes     │  │  ├ Thresholds  │  │  ├ RTO/RPO targets         │  │
│  │  ├ History     │  │  ├ Alerts      │  │  ├ Plan creation           │  │
│  │  ├ Rollback    │  │  └ Dashboard   │  │  ├ Testing                 │  │
│  │  └ Versioning  │  │               │  │  └ Execution               │  │
│  └────────────────┘  └────────────────┘  └────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

## Capabilities

### 1. Instance Management

```python
agent = DatabaseAdminAgent()

# Register instances across engines
primary = agent.register_instance(
    "prod-primary", DatabaseEngine.POSTGRESQL,
    host="db-primary.internal", port=5432,
    database="app_prod", version="15.4",
    region="us-east-1", size="db.r5.xlarge",
    storage_gb=500, tags={"env": "production"},
)

# List and filter instances
pg_instances = agent.list_instances(engine=DatabaseEngine.POSTGRESQL)
running = agent.list_instances(status=InstanceStatus.RUNNING)

# Update status
agent.update_instance_status(primary.instance_id, InstanceStatus.MAINTENANCE)
```

**Supported Engines:**

| Engine | Port | Use Case | Backup Method |
|--------|------|----------|---------------|
| PostgreSQL | 5432 | OLTP/OLAP | WAL + pg_dump |
| MySQL | 3306 | Web apps | mysqldump + binlog |
| MongoDB | 27017 | Document store | mongodump + oplog |
| Redis | 6379 | Cache/sessions | RDB + AOF |
| Elasticsearch | 9200 | Search/analytics | Snapshot API |
| ClickHouse | 8123 | OLAP analytics | ClickHouse backup |
| Cassandra | 9042 | Wide-column | nodetool snapshot |
| DynamoDB | 443 | Serverless | Point-in-time recovery |

**Instance Lifecycle:**

```
  ┌──────────────┐
  │ PROVISIONING │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐     ┌──────────────┐
  │   RUNNING    │────►│ MAINTENANCE  │
  └──────┬───────┘     └──────┬───────┘
         │                    │
         │  ┌──────────────┐  │
         │  │  SCALING     │◄─┘
         │  └──────┬───────┘
         │         │
         ▼         ▼
  ┌──────────────┐  ┌──────────────┐
  │   STOPPED    │  │  RECOVERING  │
  └──────────────┘  └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   FAILED     │
                    └──────────────┘
```

### 2. Backup & Recovery

```python
# Create backups
full_backup = agent.create_backup(primary.instance_id, BackupType.FULL)
incremental = agent.create_backup(primary.instance_id, BackupType.INCREMENTAL)

# List backups
backups = agent.list_backups(primary.instance_id, backup_type=BackupType.FULL)
latest = agent.get_latest_backup(primary.instance_id)

# Restore
agent.restore_backup(full_backup.backup_id)

# Cleanup expired
result = agent.cleanup_expired_backups(primary.instance_id)
print(f"Removed {result['expired_removed']} expired backups")
```

**Backup Types:**

| Type | Speed | Size | Restore | Best For |
|------|-------|------|---------|----------|
| FULL | Slow | Large | Fast | Weekly baseline |
| INCREMENTAL | Fast | Small | Slow | Daily |
| DIFFERENTIAL | Medium | Medium | Medium | Mid-week |
| SNAPSHOT | Fast | Large | Fast | Point-in-time |
| WAL_ARCHIVE | Continuous | Tiny | Medium | Continuous protection |
| LOGICAL_DUMP | Medium | Medium | Medium | Migration |

**Backup Strategy Flow:**

```
Weekly:     FULL ─────────────────────────────────────────────►
Daily:      ──── INCR ──── INCR ──── INCR ──── INCR ──── INCR ────
Continuous: ──────────────────────────────────────────────────────► WAL
Mid-week:   ──────── DIFF ──────── DIFF ──────── DIFF ────────
```

### 3. Performance Tuning

```python
# Record metrics
agent.record_metric(PerformanceMetric(
    metric_type=MetricType.QUERY_TIME,
    value=150.5, unit="ms",
    instance_id=primary.instance_id,
))

# Analyze performance
analysis = agent.analyze_performance(primary.instance_id)
print(f"Score: {analysis.score}, Health: {analysis.overall_health}")
print(f"Bottlenecks: {analysis.bottlenecks}")
print(f"Index recommendations: {len(analysis.index_recommendations)}")

# Find slow queries
slow = agent.get_slow_queries(primary.instance_id, threshold_ms=500)
```

**Metrics Tracked:**

| Metric | Unit | Warning | Critical |
|--------|------|---------|----------|
| query_time | ms | >1000 | >5000 |
| connections | % pool | >80% | >95% |
| disk_usage | % | >75% | >90% |
| cpu_usage | % | >70% | >90% |
| cache_hit_ratio | % | <95% | <80% |
| lock_wait | ms | >100 | >500 |
| deadlocks | count | >5 | >20 |
| replication_lag | seconds | >5 | >30 |
| iops | count/s | >10000 | >50000 |

**Performance Diagnosis Flow:**

```
  ┌──────────────┐
  │ Low Health   │
  │ Score        │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │ Check Disk   │───►│ Check CPU    │───►│ Check Memory │
  │ Usage        │    │ Usage        │    │ Usage        │
  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
         │                   │                   │
         ▼                   ▼                   ▼
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │ Archive Old  │    │ Optimize     │    │ Increase     │
  │ Data         │    │ Queries      │    │ Pool Size    │
  └──────────────┘    └──────────────┘    └──────────────┘
```

### 4. Replication Management

```python
# Create replication link
link = agent.add_replication_link(
    primary.instance_id, replica.instance_id,
    ReplicationRole.READ_REPLICA, sync_mode="async",
)

# Monitor lag
agent.update_replication_lag(link.link_id, lag_seconds=5.0)

# Get status
summary = agent.get_replication_summary()
print(f"Healthy: {summary['healthy']}, Lagging: {summary['lagging']}")

# Execute failover
result = agent.failover(primary.instance_id, replica.instance_id)
```

**Replication Topology:**

```
                    ┌──────────────┐
                    │   Primary    │
                    │  (us-east-1) │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Replica  │ │ Replica  │ │ Replica  │
        │ (us-west)│ │ (eu-west)│ │ (ap-east)│
        │   READ   │ │   READ   │ │   READ   │
        └──────────┘ └──────────┘ └──────────┘
```

### 5. Security Auditing

```python
# Run full audit
findings = agent.run_security_audit(primary.instance_id)
for f in findings:
    print(f"[{f.level.value}] {f.title}")
    print(f"  Recommendation: {f.recommendation}")
    print(f"  Compliance: {f.compliance_frameworks}")

# Get summary
summary = agent.get_security_summary()
print(f"Critical: {summary['by_level'].get('critical', 0)}")

# Mark remediated
agent.remediate_finding(findings[0].finding_id)
```

**Security Checks:**

| Check | CWE | Compliance |
|-------|-----|-----------|
| SSL/TLS enabled | CWE-319 | PCI-DSS, HIPAA |
| Encryption at rest | CWE-311 | PCI-DSS, HIPAA, GDPR |
| Non-default port | CWE-16 | — |
| No public access | CWE-668 | — |
| Audit logging | CWE-778 | PCI-DSS, SOC2 |
| Password policy | CWE-521 | — |
| No public snapshots | CWE-200 | PCI-DSS, HIPAA, GDPR |
| Connection encryption | CWE-319 | SOC2, ISO27001 |

### 6. Capacity Planning

```python
forecast = agent.forecast_capacity(
    primary.instance_id, "storage_gb", 350,
    historical_values=[300, 310, 315, 320, 330, 340, 350],
)
print(f"Current: {forecast.current_value}GB")
print(f"90-day projection: {forecast.projected_value_90d:.0f}GB")
print(f"Days until full: {forecast.days_until_full}")
print(f"Trend: {forecast.trend.value}")
print(f"Recommendation: {forecast.recommendation}")
```

**Forecasting Method:**

```
Linear Regression: y = mx + b
  m = slope (daily growth rate)
  b = intercept (current value)
  
Projection = current + (m × days)
Days until limit = (limit - current) / m
```

### 7. Schema Management

```python
# Record schema changes
change = SchemaChange(
    instance_id=primary.instance_id,
    change_type=SchemaChangeType.ADD_COLUMN,
    object_name="email_verified",
    sql_statement="ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;",
    executed_by="dba@company.com",
)
agent.record_schema_change(change)

# View history
history = agent.get_schema_history(instance_id=primary.instance_id)

# Generate rollback
rollback = agent.generate_rollback_sql(change.change_id)
```

### 8. Monitoring & Alerting

```python
# Check alerts
alerts = agent.check_alerts(primary.instance_id)
for a in alerts:
    print(f"[{a.severity.value}] {a.message}")

# Get active alerts
active = agent.get_active_alerts()

# Resolve alert
agent.resolve_alert(alerts[0].alert_id)
```

**Alert Severity Matrix:**

```
┌────────────┬────────────────────────┬─────────────────────────┐
│  Level     │  Response Time         │  Action                 │
├────────────┼────────────────────────┼─────────────────────────┤
│  CRITICAL  │  Immediate (< 15 min)  │  Page on-call DBA       │
│  HIGH      │  < 1 hour              │  Notify team channel    │
│  MEDIUM    │  < 4 hours             │  Create ticket          │
│  LOW       │  < 24 hours            │  Log for review         │
│  INFO      │  Next business day     │  Include in report      │
└────────────┴────────────────────────┴─────────────────────────┘
```

### 9. Recovery Planning

```python
# Create recovery plan
plan = agent.create_recovery_plan(
    name="Production DR Plan",
    instance_ids=[primary.instance_id, replica.instance_id],
    rto_minutes=30,
    rpo_minutes=5,
)

# Test the plan
test_result = agent.test_recovery_plan(plan.plan_id)
print(f"RTO achieved: {test_result['rto_achieved']:.1f} min")
print(f"RPO achieved: {test_result['rpo_achieved']:.1f} min")
```

## Operational Guidelines

### Backup Strategy
1. Create a FULL backup weekly as the baseline
2. Create INCREMENTAL backups daily between fulls
3. Enable WAL_ARCHIVAL for continuous protection on PostgreSQL
4. Test restoration at least monthly
5. Clean up expired backups to manage storage costs

### Performance Monitoring
1. Record metrics at regular intervals (every 1-5 minutes)
2. Run performance analysis daily
3. Address bottlenecks in priority order: disk > connections > query time > cache
4. Review slow queries weekly and add indexes as needed

### Security Posture
1. Run security audits after every configuration change
2. Address CRITICAL findings within 24 hours
3. Maintain compliance mapping for regulated data
4. Review audit findings in weekly security reviews

### Capacity Management
1. Forecast capacity monthly for all production instances
2. Plan scaling when projections show <30 days until exhaustion
3. Archive historical data to reduce growth rate
4. Review capacity trends quarterly

## Method Signatures

```python
class DatabaseAdminAgent:
    def __init__(self, config: Optional[DatabaseAdminConfig] = None) -> None: ...

    # Instance Management
    def register_instance(self, name, engine, host, port, database, **kwargs) -> DatabaseInstance: ...
    def get_instance(self, instance_id) -> DatabaseInstance: ...
    def list_instances(self, engine=None, status=None, region=None) -> List[DatabaseInstance]: ...
    def update_instance_status(self, instance_id, status) -> Dict[str, Any]: ...
    def deprovision_instance(self, instance_id, force=False) -> Dict[str, Any]: ...

    # Backup & Recovery
    def create_backup(self, instance_id, backup_type, retention_days) -> BackupRecord: ...
    def list_backups(self, instance_id, backup_type=None, status=None) -> List[BackupRecord]: ...
    def restore_backup(self, backup_id, target_instance_id=None) -> Dict[str, Any]: ...
    def get_latest_backup(self, instance_id) -> Optional[BackupRecord]: ...
    def cleanup_expired_backups(self, instance_id) -> Dict[str, Any]: ...

    # Performance
    def record_metric(self, metric: PerformanceMetric) -> None: ...
    def analyze_performance(self, instance_id) -> PerformanceAnalysis: ...
    def record_query_plan(self, instance_id, plan) -> None: ...
    def get_slow_queries(self, instance_id, threshold_ms=None) -> List[QueryPlan]: ...

    # Replication
    def add_replication_link(self, source_id, target_id, role, sync_mode) -> ReplicationLink: ...
    def get_replication_status(self, source_id=None) -> List[ReplicationLink]: ...
    def update_replication_lag(self, link_id, lag_seconds) -> Dict[str, Any]: ...
    def get_replication_summary(self) -> Dict[str, Any]: ...
    def failover(self, source_id, target_id) -> Dict[str, Any]: ...

    # Security
    def run_security_audit(self, instance_id) -> List[SecurityFinding]: ...
    def get_security_summary(self, instance_id=None) -> Dict[str, Any]: ...
    def remediate_finding(self, finding_id) -> Dict[str, Any]: ...

    # Capacity
    def forecast_capacity(self, instance_id, metric, current_value, historical_values=None) -> CapacityForecast: ...

    # Schema
    def record_schema_change(self, change) -> SchemaChange: ...
    def get_schema_history(self, instance_id=None, change_type=None, limit=50) -> List[SchemaChange]: ...
    def generate_rollback_sql(self, change_id) -> Optional[str]: ...

    # Monitoring
    def check_alerts(self, instance_id) -> List[Alert]: ...
    def get_active_alerts(self, instance_id=None) -> List[Alert]: ...
    def resolve_alert(self, alert_id) -> Dict[str, Any]: ...

    # Recovery
    def create_recovery_plan(self, name, instance_ids, rto_minutes, rpo_minutes, steps=None) -> RecoveryPlan: ...
    def test_recovery_plan(self, plan_id) -> Dict[str, Any]: ...
    def get_recovery_plans(self) -> List[RecoveryPlan]: ...

    # Status
    def get_status(self) -> Dict[str, Any]: ...
    def generate_dashboard(self) -> Dict[str, Any]: ...
```

## Data Models

### DatabaseEngine

```python
class DatabaseEngine(Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    REDIS = "redis"
    ELASTICSEARCH = "elasticsearch"
    CLICKHOUSE = "clickhouse"
    CASSANDRA = "cassandra"
    DYNAMODB = "dynamodb"
```

### InstanceStatus

```python
class InstanceStatus(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    MAINTENANCE = "maintenance"
    SCALING = "scaling"
    RECOVERING = "recovering"
    FAILED = "failed"
    PROVISIONING = "provisioning"
```

### BackupType

```python
class BackupType(Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    SNAPSHOT = "snapshot"
    WAL_ARCHIVE = "wal_archive"
    LOGICAL_DUMP = "logical_dump"
```

### Key Data Classes

```python
@dataclass
class DatabaseInstance:
    instance_id: str
    name: str
    engine: DatabaseEngine
    host: str
    port: int
    database: str
    version: str
    region: str
    size: str
    storage_gb: int
    status: InstanceStatus
    tags: Dict[str, str]
    created_at: datetime
    last_backup: Optional[datetime]

@dataclass
class BackupRecord:
    backup_id: str
    instance_id: str
    backup_type: BackupType
    status: str
    size_gb: float
    retention_days: int
    created_at: datetime
    expires_at: datetime

@dataclass
class PerformanceAnalysis:
    instance_id: str
    score: float  # 0.0 - 1.0
    overall_health: str
    bottlenecks: List[str]
    index_recommendations: List[str]
    recommendations: List[str]
    analyzed_at: datetime
```

## Security Considerations

### Access Control

```
┌──────────────────────────────────────────────────────┐
│               Access Control Matrix                    │
├──────────────────┬────────┬────────┬────────┬────────┤
│  Role            │ Read   │ Write  │ Admin  │ Audit  │
├──────────────────┼────────┼────────┼────────┼────────┤
│  Viewer          │   ✓    │   ✗    │   ✗    │   ✗    │
│  Developer       │   ✓    │   ✓    │   ✗    │   ✗    │
│  DBA             │   ✓    │   ✓    │   ✓    │   ✓    │
│  Security        │   ✓    │   ✗    │   ✗    │   ✓    │
│  Admin           │   ✓    │   ✓    │   ✓    │   ✓    │
└──────────────────┴────────┴────────┴────────┴────────┘
```

### Data Protection

- Encrypt data at rest (AES-256)
- Encrypt data in transit (TLS 1.3)
- Mask sensitive data in logs
- Rotate credentials regularly
- Audit all administrative actions

## Scalability

### Instance Scaling Patterns

```
Vertical Scaling (Scale Up):
  ┌──────────────┐      ┌──────────────┐
  │ db.t3.medium │ ────►│ db.r5.xlarge │
  │  2 vCPU      │      │  4 vCPU      │
  │  4 GB RAM    │      │  32 GB RAM   │
  └──────────────┘      └──────────────┘

Horizontal Scaling (Scale Out):
  ┌──────────────┐      ┌──────────────┐
  │   Primary    │ ────►│   Primary    │
  └──────────────┘      └──────┬───────┘
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │ Replica 1│ │ Replica 2│ │ Replica 3│
              └──────────┘ └──────────┘ └──────────┘
```

## Troubleshooting

### "Instance not found" Error

```python
# Ensure you've registered the instance
instance = agent.register_instance("my-db", DatabaseEngine.POSTGRESQL, ...)
# Use the returned instance_id
agent.analyze_performance(instance.instance_id)
```

### Backup Fails

- Check that the instance is in RUNNING status
- Verify storage location is accessible
- Check for concurrent backup limits (default: 3)
- Review backup timeout settings

### Performance Analysis Returns "unknown" Health

- Record metrics first using `record_metric`
- Ensure metrics are recent (within last 5 minutes)
- Check that the instance is registered

### Replication Lag Growing

- Check network connectivity between primary and replica
- Verify replica has sufficient resources (CPU, I/O)
- Consider switching to semi-synchronous replication
- Review write volume on primary

### Security Audit Finds No Issues

- Verify instance config includes all settings (ssl_enabled, encryption_at_rest, etc.)
- Check that the instance is properly registered
- Review config dictionary for missing security settings

## Checklists

### Production Instance Onboarding

- [ ] Register instance with correct engine, host, port
- [ ] Set appropriate storage and size parameters
- [ ] Tag with environment and team metadata
- [ ] Create initial FULL backup
- [ ] Set up replication to read replica
- [ ] Run security audit and address findings
- [ ] Create monitoring checks (disk, CPU, connections)
- [ ] Create disaster recovery plan
- [ ] Test recovery plan
- [ ] Add to capacity forecasting

### Backup Verification

- [ ] Verify backup completed successfully
- [ ] Check backup size is reasonable
- [ ] Test restoration to a staging instance
- [ ] Verify data integrity after restore
- [ ] Confirm encryption and compression

### Security Audit Review

- [ ] Run security audit on all instances
- [ ] Address all CRITICAL findings immediately
- [ ] Schedule HIGH findings for remediation
- [ ] Update compliance documentation
- [ ] Track remediation progress

### Performance Review

- [ ] Analyze performance metrics for all instances
- [ ] Review slow query log
- [ ] Evaluate index usage and recommendations
- [ ] Check connection pool utilization
- [ ] Review disk usage trends

### Disaster Recovery Testing

- [ ] Execute recovery plan in staging
- [ ] Verify RTO target met
- [ ] Verify RPO target met
- [ ] Validate data integrity
- [ ] Document any gaps or issues

## Configuration

```yaml
database_admin_agent:
  monitoring:
    poll_interval_seconds: 300
    alert_thresholds:
      disk_usage_warning: 75
      disk_usage_critical: 90
      cpu_usage_warning: 70
      cpu_usage_critical: 90
      replication_lag_warning: 5
      replication_lag_critical: 30
  
  backup:
    default_retention_days: 30
    max_concurrent_backups: 3
    backup_timeout_minutes: 60
    
  security:
    audit_frequency_days: 90
    compliance_frameworks:
      - PCI-DSS
      - HIPAA
      - SOC2
      
  capacity:
    forecast_days: 90
    alert_days_until_full: 30
```

## Integration Points

### With Other Agents
- **database-admin**: Core database operations
- **data-governance**: Data quality and compliance
- **devops**: Infrastructure automation
- **security**: Vulnerability management

### External Tools
- pg_dump / pg_restore (PostgreSQL)
- mysqldump / mysqlpump (MySQL)
- mongodump / mongorestore (MongoDB)
- AWS CLI (DynamoDB, RDS)
- Database-specific monitoring agents

## Performance Benchmarks

### Typical Operations

| Operation | Small (< 100GB) | Medium (< 1TB) | Large (< 10TB) |
|-----------|-----------------|----------------|----------------|
| FULL backup | 5 min | 30 min | 4 hours |
| Restore | 3 min | 20 min | 3 hours |
| Security audit | 10 sec | 30 sec | 2 min |
| Capacity forecast | 1 sec | 2 sec | 5 sec |
| Performance analysis | 5 sec | 15 sec | 1 min |

## Future Enhancements

- Automated index creation based on query patterns
- Real-time query optimization suggestions
- Cross-database migration support
- Cloud-native auto-scaling integration
- AI-powered anomaly detection
- Automated compliance reporting
- Multi-region replication management
- Cost optimization recommendations
