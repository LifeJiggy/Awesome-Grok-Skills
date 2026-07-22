---
name: "Database Replication"
version: "2.0.0"
description: "Comprehensive database replication toolkit with primary-replica setup, conflict resolution, replication monitoring, failover management, and multi-region deployment for high availability and disaster recovery"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database", "replication", "high-availability", "failover", "multi-region", "disaster-recovery"]
category: "database"
personality: "replication-engineer"
use_cases: ["primary-replica setup", "conflict resolution", "failover management", "replication monitoring", "disaster recovery"]
---

# Database Replication

> Production-grade database replication framework providing primary-replica configuration, conflict resolution, replication monitoring, automatic failover, and multi-region deployment for high availability and disaster recovery.

## Overview

The Database Replication module provides a complete toolkit for setting up and managing database replication topologies. It implements primary-replica (master-slave) configuration, multi-primary (master-master) setups, conflict detection and resolution strategies, replication lag monitoring, automatic failover with leader election, read replica load balancing, and cross-region replication for disaster recovery. Every operation includes health monitoring, alerting thresholds, and automated recovery procedures.

## Core Capabilities

### 1. Replication Topology Management
- Primary-replica (async and semi-sync) configuration
- Multi-primary (active-active) topology setup
- Cascading replication chains
- Circular replication with conflict prevention
- Replication slot management for WAL retention

### 2. Conflict Resolution
- Last-Writer-Wins (LWW) based on timestamps
- Merge-based conflict resolution
- Custom conflict resolution functions
- Conflict logging and audit trail
- Automatic vs manual conflict handling

### 3. Replication Monitoring
- Replication lag tracking (bytes and time)
- WAL position monitoring
- Replication slot health
- Throughput metrics per replica
- Alerting thresholds and notifications

### 4. Failover Management
- Automatic failover with health checks
- Manual failover with controlled switchover
- Split-brain prevention with fencing
- Replica promotion procedures
- Original primary rejoin after recovery

### 5. Read/Write Splitting
- Automatic read routing to replicas
- Read-after-write consistency guarantees
- Connection string management for applications
- Load balancing across replicas
- Health-aware routing

### 6. Disaster Recovery
- Cross-region replication setup
- RPO and RTO management
- Backup replication verification
- Failover runbook automation
- Recovery point validation

## Usage Examples

### Primary-Replica Setup

```python
from replication import ReplicationManager, TopologyType, SyncMode

manager = ReplicationManager()

# Configure primary
primary = manager.configure_primary(
    host="db-primary.example.com",
    port=5432,
    database="production",
    wal_level="replica",
    max_wal_senders=10,
    wal_keep_size="1GB",
)

# Add replicas
replica1 = manager.add_replica(
    host="db-replica-1.example.com",
    port=5432,
    primary_host="db-primary.example.com",
    sync_mode=SyncMode.ASYNC,
    standby_mode="streaming",
)

replica2 = manager.add_replica(
    host="db-replica-2.example.com",
    port=5432,
    primary_host="db-primary.example.com",
    sync_mode=SyncMode.SEMI_SYNC,
)

print(f"Primary: {primary.host}")
print(f"Replicas: {len(manager.get_replicas())}")
```

### Replication Monitoring

```python
from replication import ReplicationMonitor, AlertThreshold

monitor = ReplicationMonitor(manager)

# Check replication status
status = monitor.get_status()
for replica in status.replicas:
    print(f"  {replica.host}:")
    print(f"    Lag: {replica.lag_bytes} bytes ({replica.lag_seconds:.1f}s)")
    print(f"    State: {replica.state}")
    print(f"    WAL position: {replica.wal_position}")

# Set up alerts
monitor.set_alert(
    metric="replication_lag_bytes",
    threshold=100_000_000,  # 100MB
    callback=lambda alert: print(f"ALERT: {alert.message}"),
)

# Get metrics
metrics = monitor.get_metrics()
print(f"  Total lag: {metrics.total_lag_bytes} bytes")
print(f"  Average lag: {metrics.avg_lag_seconds:.1f}s")
```

### Automatic Failover

```python
from replication import FailoverManager, FailoverStrategy

failover = FailoverManager(manager, strategy=FailoverStrategy.AUTOMATIC)

# Configure health checks
failover.configure_health_check(
    interval_seconds=10,
    timeout_seconds=5,
    failure_threshold=3,
)

# Configure failover rules
failover.configure_rules(
    auto_promote_replica=True,
    max_failover_time_seconds=60,
    require_sync_replica=False,
    fencing_enabled=True,
)

# Monitor and trigger failover
result = failover.check_and_failover()
if result.failover_triggered:
    print(f"Failover completed: {result.new_primary}")
    print(f"Duration: {result.duration_seconds:.1f}s")
    print(f"Promoted replica: {result.promoted_replica}")
```

### Multi-Primary Configuration

```python
from replication import MultiPrimaryManager, ConflictResolution

multi_primary = MultiPrimaryManager()

# Configure active-active
node_a = multi_primary.add_node(
    host="db-region-a.example.com",
    region="us-east",
    conflict_resolution=ConflictResolution.LAST_WRITER_WINS,
)

node_b = multi_primary.add_node(
    host="db-region-b.example.com",
    region="eu-west",
    conflict_resolution=ConflictResolution.LAST_WRITER_WINS,
)

# Set up conflict prevention
multi_primary.configure_conflict_prevention(
    partition_keys=["tenant_id"],
    route_writes_to_nearest=True,
)

# Monitor conflicts
conflicts = multi_primary.get_recent_conflicts(hours=24)
print(f"Conflicts in last 24h: {len(conflicts)}")
for conflict in conflicts:
    print(f"  {conflict.table}: {conflict.resolution_strategy}")
```

### Disaster Recovery Setup

```python
from replication import DisasterRecoveryManager

dr = DisasterRecoveryManager(manager)

# Configure cross-region replication
dr.configure_cross_region(
    primary_region="us-east-1",
    replica_regions=["eu-west-1", "ap-southeast-1"],
    async_replication=True,
)

# Set RPO and RTO targets
dr.set_targets(
    rpo_seconds=30,  # Max 30 seconds of data loss
    rto_seconds=300,  # Max 5 minutes to recover
)

# Validate DR setup
validation = dr.validate()
print(f"RPO met: {validation.rpo_met}")
print(f"RTO met: {validation.rto_met}")
print(f"Replication health: {validation.replication_health}")
```

## Best Practices

### Replication Configuration
- Use streaming replication over file-based for automatic WAL management
- Keep replication lag under 1 second for production workloads
- Monitor replication slots — expired slots cause WAL accumulation
- Use synchronous replication only when data loss is unacceptable

### Failover Strategy
- Always test failover in staging before enabling in production
- Implement fencing to prevent split-brain scenarios
- Use at least 3 replicas for quorum-based failover decisions
- Monitor failover events and set up alerting

### Multi-Region
- Use conflict-free replicated data types (CRDTs) where possible
- Partition data by region to minimize cross-region conflicts
- Implement read-local, write-leader patterns for consistency
- Test cross-region failover regularly

### Monitoring
- Track replication lag continuously — alert on > 10 seconds
- Monitor WAL generation rate — sudden spikes indicate issues
- Set up runbooks for common replication failures
- Validate backup integrity after any failover event

## Related Modules

- **database-administration**: Database management and connection pooling
- **query-optimization**: Read replica query routing optimization
- **mongodb**: MongoDB replica set operations
- **data-modeling**: Schema considerations for replicated databases

---

## Advanced Configuration

### Advanced Replication Topologies

```python
from replication import TopologyManager, TopologyType

topology = TopologyManager()

# Configure cascading replication
cascade = topology.create_cascade(
    primary="db-primary",
    intermediates=[
        {"host": "db-intermediate-1", "sync_mode": "async"},
        {"host": "db-intermediate-2", "sync_mode": "async"},
    ],
    final_replicas=[
        "db-replica-1",
        "db-replica-2",
        "db-replica-3",
    ],
)

# Configure geographic replication
geo_topology = topology.create_geo_distributed(
    primary_region="us-east-1",
    secondary_regions=[
        {"region": "eu-west-1", "sync_mode": "semi_sync", "priority": 5},
        {"region": "ap-southeast-1", "sync_mode": "async", "priority": 3},
    ],
    read_replicas=[
        {"region": "us-west-2", "sync_mode": "async"},
        {"region": "eu-central-1", "sync_mode": "async"},
    ],
)
```

### Conflict Resolution Strategies

```python
from replication import ConflictResolver, ResolutionStrategy

resolver = ConflictResolver(strategy=ResolutionStrategy.CUSTOM)

# Custom conflict resolution function
def resolve_conflict(local_version, remote_version):
    """
    Custom resolution: prefer higher version, then most recent.
    """
    if local_version.get('version', 0) > remote_version.get('version', 0):
        return local_version
    elif local_version.get('version', 0) < remote_version.get('version', 0):
        return remote_version
    else:
        # Same version, prefer most recent
        if local_version.get('updated_at') > remote_version.get('updated_at'):
            return local_version
        return remote_version

resolver.set_resolution_function(resolve_conflict)

# Configure conflict prevention
resolver.configure_prevention(
    partition_key="tenant_id",
    route_writes_to_partition_owner=True,
    enable_optimistic_locking=True,
    version_field="version",
)
```

### Advanced Failover Configuration

```python
from replication import FailoverManager, FailoverStrategy, FencingMode

failover = FailoverManager(strategy=FailoverStrategy.AUTOMATIC)

# Configure sophisticated failover rules
failover.configure_rules(
    # Health check parameters
    health_check_interval_seconds=5,
    health_check_timeout_seconds=3,
    failure_threshold=3,
    recovery_threshold=2,
    
    # Failover behavior
    auto_promote_replica=True,
    max_failover_time_seconds=30,
    require_sync_replica=False,
    min_healthy_replicas=2,
    
    # Fencing configuration
    fencing_enabled=True,
    fencing_mode=FencingMode.STONITH,
    fencing_timeout_seconds=10,
    
    # Split-brain prevention
    quorum_size=3,
    require_unanimous_vote=False,
    split_brain_detection=True,
)

# Configure automatic primary rejoin
failover.configure_rejoin(
    auto_rejoin=True,
    rejoin_delay_seconds=60,
    max_rejoin_attempts=3,
    require_data_sync=True,
)
```

## Architecture Patterns

### Primary-Replica with Load Balancer

```
┌─────────────────────────────────────────────────────────────┐
│                     Load Balancer                           │
│                    (HAProxy/PgBouncer)                      │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │   Primary     │ │   Replica 1   │ │   Replica 2   │
    │   (Read/Write)│ │   (Read Only) │ │   (Read Only) │
    └───────┬───────┘ └───────────────┘ └───────────────┘
            │
            │ Streaming Replication
            │
            └─────────────────────────────────────────────┘
```

### Multi-Primary Active-Active

```
┌─────────────────────────────────────────────────────────────┐
│                        Region A                             │
│  ┌───────────────┐      ┌───────────────┐                  │
│  │   Primary A   │◄────►│   Primary B   │                  │
│  │   (us-east)   │      │   (eu-west)   │                  │
│  └───────┬───────┘      └───────┬───────┘                  │
└──────────┼───────────────────────┼──────────────────────────┘
           │                       │
           │    Bidirectional      │
           │    Replication        │
           │                       │
           ▼                       ▼
    ┌───────────────┐      ┌───────────────┐
    │   Replica A   │      │   Replica B   │
    │   (us-west)   │      │   (ap-east)   │
    └───────────────┘      └───────────────┘
```

### Disaster Recovery Topology

```
┌─────────────────────────────────────────────────────────────┐
│                    Primary Region (us-east-1)               │
│  ┌───────────────┐      ┌───────────────┐                  │
│  │   Primary     │      │   Replica     │                  │
│  └───────┬───────┘      └───────────────┘                  │
└──────────┼──────────────────────────────────────────────────┘
           │
           │ Asynchronous Replication
           │ (RPO: 30 seconds)
           ▼
┌─────────────────────────────────────────────────────────────┐
│                  DR Region (eu-west-1)                      │
│  ┌───────────────┐      ┌───────────────┐                  │
│  │   DR Primary  │      │   DR Replica  │                  │
│  └───────┬───────┘      └───────────────┘                  │
└──────────┼──────────────────────────────────────────────────┘
           │
           │ Asynchronous Replication
           │ (RPO: 5 minutes)
           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Archive Region (ap-south-1)                │
│  ┌───────────────┐                                         │
│  │   Archive     │                                         │
│  └───────────────┘                                         │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with FastAPI
from fastapi import FastAPI, Depends, Request
from replication import ReplicationManager, ReadPreference

app = FastAPI()
manager = ReplicationManager()

async def get_read_connection(request: Request):
    # Route reads based on consistency requirements
    if request.headers.get("X-Require-Consistent-Read"):
        conn = await manager.get_primary_connection()
    else:
        conn = await manager.get_read_replica(preference=ReadPreference.NEAREST)
    return conn

async def get_write_connection():
    return await manager.get_primary_connection()

@app.get("/users/{user_id}")
async def get_user(user_id: str, conn = Depends(get_read_connection)):
    return await conn.execute("SELECT * FROM users WHERE id = $1", user_id)

@app.post("/users")
async def create_user(user: UserCreate, conn = Depends(get_write_connection)):
    return await conn.execute("INSERT INTO users ...", ...)
```

### Connection Pool Integration

```python
# Integration with connection pooling
from replication import ReplicationPool, PoolConfig
from database_administration import ConnectionPool

# Create read/write split pool
rw_pool = ReplicationPool(
    primary_config=PoolConfig(host="db-primary", port=5432),
    replica_configs=[
        PoolConfig(host="db-replica-1", port=5432),
        PoolConfig(host="db-replica-2", port=5432),
    ],
    read_preference=ReadPreference.NEAREST,
    max_connections_per_replica=20,
)

# Use with existing connection pool
pool = ConnectionPool(proxy=rw_pool)
```

### Monitoring Integration

```python
# Integration with Prometheus
from prometheus_client import Counter, Histogram, Gauge

REPLICATION_LAG = Gauge('db_replication_lag_seconds', 'Replication lag', ['replica'])
FAILOVER_COUNT = Counter('db_failover_total', 'Failover events')
READ_OPERATIONS = Counter('db_read_operations_total', 'Read operations', ['target'])

class ReplicationMetrics:
    def record_lag(self, replica: str, lag_seconds: float):
        REPLICATION_LAG.labels(replica=replica).set(lag_seconds)
    
    def record_failover(self):
        FAILOVER_COUNT.inc()
    
    def record_read(self, target: str):
        READ_OPERATIONS.labels(target=target).inc()
```

## Performance Optimization

### Replication Performance Tuning

| Parameter | Default | Recommended | Description |
|-----------|---------|-------------|-------------|
| wal_level | replica | replica | WAL level for replication |
| max_wal_senders | 10 | 20-50 | Max WAL sender processes |
| wal_keep_size | 1GB | 10GB | WAL retention size |
| hot_standby | on | on | Allow reads on standby |
| max_replication_slots | 10 | 20-50 | Max replication slots |
| synchronous_commit | on | on/off | Sync commit durability |

### Read Replica Optimization

```python
from replication import ReadReplicaOptimizer

optimizer = ReadReplicaOptimizer()

# Configure read routing optimization
optimizer.configure(
    # Load balancing
    algorithm="round_robin",  # round_robin, least_connections, weighted
    
    # Health-aware routing
    health_check_interval=10,
    unhealthy_threshold=3,
    healthy_threshold=2,
    
    # Consistency guarantees
    max_lag_seconds=5,
    require_healthy=True,
    
    # Connection pooling
    max_connections_per_replica=50,
    idle_timeout_seconds=300,
)

# Get optimized connection
conn = await optimizer.get_connection(
    consistency="eventual",  # eventual, bounded_staleness, strong
    max_staleness_seconds=30,
    region="us-east",
)
```

### WAL Optimization

```python
from replication import WALOptimizer

wal_optimizer = WALOptimizer()

# Optimize WAL settings
wal_optimizer.configure(
    wal_level="replica",
    wal_compression="lz4",
    wal_buffers="64MB",
    checkpoint_timeout="15min",
    max_wal_size="10GB",
    min_wal_size="1GB",
    wal_writer_delay="200ms",
    commit_delay=0,
    commit_siblings=0,
)

# Monitor WAL generation
wal_stats = wal_optimizer.get_stats()
print(f"WAL generation rate: {wal_stats.generation_rate_mb_per_min:.1f} MB/min")
print(f"WAL retention: {wal_stats.retention_mb:.1f} MB")
print(f"Replication slots: {wal_stats.active_slots}")
```

## Security Considerations

### Replication Security

```python
from replication import SecurityManager

security = SecurityManager()

# Configure secure replication
security.configure(
    # SSL/TLS for replication
    replication_ssl=True,
    ssl_ca="/etc/ssl/certs/ca.pem",
    ssl_cert="/etc/ssl/certs/replication.pem",
    ssl_key="/etc/ssl/private/replication.key",
    ssl_verify=True,
    
    # Authentication
    auth_method="scram-sha-256",
    password_encryption="scram-sha-256",
    
    # Network security
    replication_ip_mask="10.0.0.0/8",
    allow_replication_from=["10.0.1.0/24", "10.0.2.0/24"],
)
```

### Audit Logging

```python
from replication import AuditLogger

audit = AuditLogger()

# Log replication events
audit.log_event(
    event_type="FAILOVER",
    details={
        "old_primary": "db-primary-1",
        "new_primary": "db-replica-2",
        "cause": "health_check_failure",
        "duration_seconds": 25.5,
    },
    user="system",
)

# Generate audit report
report = audit.generate_report(
    start_date="2024-01-01",
    end_date="2024-01-31",
    event_types=["FAILOVER", "REPLICATION_LAG", "ROLE_CHANGE"],
)

print(f"Total events: {report.total_events}")
print(f"Failovers: {report.failover_count}")
print(f"Max lag: {report.max_lag_seconds}s")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Replication lag | Replicas falling behind | Check network, increase WAL settings |
| WAL accumulation | Disk filling up | Increase wal_keep_size, check replication slots |
| Split-brain | Multiple primaries | Enable fencing, use quorum |
| Failover failure | Cannot promote replica | Check health checks, verify quorum |
| Connection refused | Cannot connect to replica | Check pg_hba.conf, verify SSL certificates |

### Diagnostic Queries

```sql
-- Check replication status on primary
SELECT
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    pg_wal_lsn_diff(sent_lsn, replay_lsn) AS replication_lag_bytes
FROM pg_stat_replication;

-- Check replication slot status
SELECT
    slot_name,
    slot_type,
    active,
    restart_lsn,
    confirmed_flush_lsn,
    pg_wal_lsn_diff(restart_lsn, confirmed_flush_lsn) AS retained_bytes
FROM pg_replication_slots;

-- Check WAL generation rate
SELECT
    pg_current_wal_lsn() AS current_lsn,
    pg_walfile_name(pg_current_wal_lsn()) AS current_wal_file;

-- Check primary connection info
SELECT * FROM pg_stat_wal_receiver;
```

### Performance Debugging

```python
from replication import DiagnosticTool

diag = DiagnosticTool()

# Run comprehensive diagnostics
diagnostics = diag.run_diagnostics()

print("Replication Status:")
for replica in diagnostics.replicas:
    print(f"  {replica.host}:")
    print(f"    State: {replica.state}")
    print(f"    Lag: {replica.lag_bytes} bytes ({replica.lag_seconds:.1f}s)")
    print(f"    WAL position: {replica.wal_position}")

print("\nWAL Statistics:")
print(f"  Generation rate: {diagnostics.wal.generation_rate_mb_per_min:.1f} MB/min")
print(f"  Retention: {diagnostics.wal.retention_mb:.1f} MB")
print(f"  Slots active: {diagnostics.wal.active_slots}")

print("\nHealth Checks:")
for check in diagnostics.health_checks:
    status = "PASS" if check.passed else "FAIL"
    print(f"  [{status}] {check.name}: {check.message}")
```

## API Reference

### ReplicationManager

```python
class ReplicationManager:
    def __init__(self, primary_config: Config = None)
    def configure_primary(self, host: str, port: int, **kwargs) -> PrimaryConfig
    def add_replica(self, host: str, port: int, **kwargs) -> ReplicaConfig
    def remove_replica(self, host: str)
    def get_primary(self) -> PrimaryConfig
    def get_replicas(self) -> list[ReplicaConfig]
    def get_status(self) -> ReplicationStatus
    def promote_replica(self, host: str) -> PromotionResult
    def demote_primary(self) -> DemotionResult
```

### FailoverManager

```python
class FailoverManager:
    def __init__(self, manager: ReplicationManager, strategy: FailoverStrategy = FailoverStrategy.AUTOMATIC)
    def configure_health_check(self, interval_seconds: int, timeout_seconds: int, failure_threshold: int)
    def configure_rules(self, **kwargs)
    def configure_fencing(self, mode: FencingMode, timeout_seconds: int)
    def check_health(self) -> HealthStatus
    def check_and_failover(self) -> FailoverResult
    def manual_failover(self, target_host: str) -> FailoverResult
    def get_failover_history(self) -> list[FailoverEvent]
```

### DisasterRecoveryManager

```python
class DisasterRecoveryManager:
    def __init__(self, manager: ReplicationManager)
    def configure_cross_region(self, primary_region: str, replica_regions: list[str], async_replication: bool = True)
    def set_targets(self, rpo_seconds: int, rto_seconds: int)
    def validate(self) -> DRValidation
    def test_failover(self) -> TestResult
    def get_dr_status(self) -> DRStatus
    def generate_runbook(self) -> str
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class TopologyType(Enum):
    PRIMARY_REPLICA = "primary_replica"
    MULTI_PRIMARY = "multi_primary"
    CASCADING = "cascading"
    CIRCULAR = "circular"

class SyncMode(Enum):
    ASYNC = "async"
    SEMI_SYNC = "semi_sync"
    SYNC = "sync"

class ReplicaState(Enum):
    STARTING = "starting"
    STREAMING = "streaming"
    BACKUP = "backup"
    DISCONNECTED = "disconnected"
    UNKNOWN = "unknown"

class FailoverStrategy(Enum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    SEMI_AUTOMATIC = "semi_automatic"

class FencingMode(Enum):
    STONITH = "stonith"
    DISK_FENCE = "disk_fence"
    NETWORK_FENCE = "network_fence"

@dataclass
class ReplicationSlot:
    name: str
    active: bool
    restart_lsn: str
    confirmed_flush_lsn: str
    retained_bytes: int

@dataclass
class ReplicaConfig:
    host: str
    port: int
    sync_mode: SyncMode
    state: ReplicaState
    lag_bytes: int
    lag_seconds: float
    wal_position: str
    last_updated: datetime

@dataclass
class FailoverEvent:
    timestamp: datetime
    old_primary: str
    new_primary: str
    cause: str
    duration_seconds: float
    success: bool
    details: Dict[str, any]
```

## Deployment Guide

### Prerequisites

- PostgreSQL 12+ (or MySQL 8.0+, MongoDB 4.4+)
- Python 3.9+
- Network connectivity between nodes
- Sufficient disk space for WAL

### Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  primary:
    image: postgres:15
    command: >
      postgres
      -c wal_level=replica
      -c max_wal_senders=10
      -c wal_keep_size=10GB
      -c hot_standby=on
      -c max_replication_slots=10
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - primary_data:/var/lib/postgresql/data

  replica:
    image: postgres:15
    command: >
      postgres
      -c hot_standby=on
    ports:
      - "5433:5432"
    environment:
      PGUSER: replication_user
      PGPASSWORD: ${REPLICATION_PASSWORD}
    depends_on:
      - primary
    volumes:
      - replica_data:/var/lib/postgresql/data

volumes:
  primary_data:
  replica_data:
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-primary
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
      role: primary
  template:
    metadata:
      labels:
        app: postgres
        role: primary
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

## Monitoring & Observability

### Replication Metrics

```python
from replication import MetricsCollector

collector = MetricsCollector()

# Collect replication metrics
collector.gauge("replication.lag_bytes", lag_bytes, tags={"replica": replica_host})
collector.gauge("replication.lag_seconds", lag_seconds, tags={"replica": replica_host})
collector.gauge("replication.wal_position", wal_position, tags={"replica": replica_host})

# Collect failover metrics
collector.counter("failover.total", 1, tags={"cause": cause, "success": success})
collector.histogram("failover.duration_seconds", duration)

# Collect health check metrics
collector.gauge("health_check.status", 1 if healthy else 0, tags={"replica": replica_host})
```

### Alerting Rules

```yaml
groups:
  - name: replication_alerts
    rules:
      - alert: ReplicationLagHigh
        expr: db_replication_lag_seconds > 30
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Replication lag exceeds threshold"
          
      - alert: ReplicationLagCritical
        expr: db_replication_lag_seconds > 300
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Replication lag is critically high"
          
      - alert: ReplicaDisconnected
        expr: db_replication_connected == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Replica disconnected from primary"
          
      - alert: FailoverDetected
        expr: increase(db_failover_total[5m]) > 0
        for: 0m
        labels:
          severity: warning
        annotations:
          summary: "Failover event detected"
```

### Dashboard Configuration

```json
{
  "title": "Replication Monitoring Dashboard",
  "panels": [
    {
      "title": "Replication Lag",
      "type": "graph",
      "targets": ["db_replication_lag_seconds"]
    },
    {
      "title": "WAL Position",
      "type": "graph",
      "targets": ["db_wal_position"]
    },
    {
      "title": "Health Status",
      "type": "stat",
      "targets": ["db_health_status"],
      "thresholds": {
        "critical": 0,
        "warning": 1,
        "good": 2
      }
    }
  ]
}
```

## Testing Strategy

### Unit Tests

```python
import pytest
from replication import ReplicationManager, FailoverManager

@pytest.fixture
def manager():
    return ReplicationManager(primary_config=primary_config)

def test_add_replica(manager):
    replica = manager.add_replica(
        host="db-replica-1",
        port=5432,
        sync_mode=SyncMode.ASYNC,
    )
    assert replica.host == "db-replica-1"
    assert replica.sync_mode == SyncMode.ASYNC

def test_failover_detection(failover_manager):
    # Simulate primary failure
    failover_manager.simulate_failure("db-primary")
    
    # Check failover
    result = failover_manager.check_and_failover()
    assert result.failover_triggered
    assert result.new_primary == "db-replica-1"
```

### Integration Tests

```python
@pytest.mark.integration
def test_replication_flow():
    manager = ReplicationManager()
    
    # Insert data on primary
    primary_conn = manager.get_primary_connection()
    await primary_conn.execute(
        "INSERT INTO test_table (data) VALUES ($1)",
        "test_data"
    )
    
    # Wait for replication
    await asyncio.sleep(1)
    
    # Read from replica
    replica_conn = manager.get_replica_connection()
    result = await replica_conn.execute("SELECT * FROM test_table WHERE data = $1", "test_data")
    assert result.row_count == 1
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| PostgreSQL | 12 | 15+ |
| MySQL | 8.0 | 8.0+ |
| MongoDB | 4.4 | 6.0+ |

### Migration Path

```python
from replication import MigrationManager

migration = MigrationManager()

# Check current configuration version
current = migration.current_version()
print(f"Current replication config version: {current}")

# Generate migration script
script = migration.generate_migration(
    from_version="2.0.0",
    to_version="3.0.0",
    changes=[
        "Add replication slot support",
        "Update failover configuration",
        "Enable WAL compression",
    ]
)

print(f"Migration script: {script.path}")
print(f"Breaking changes: {script.breaking_changes}")
```

## Glossary

| Term | Definition |
|------|------------|
| **Primary** | Database accepting read and write operations |
| **Replica** | Database copy receiving replicated data |
| **Replication Lag** | Time delay between primary and replica |
| **WAL** | Write-Ahead Log for data durability |
| **Fencing** | Mechanism to prevent split-brain scenarios |
| **Split-Brain** | When two nodes both think they are primary |
| **Failover** | Automatic switching to a replica when primary fails |
| **RPO** | Recovery Point Objective - max acceptable data loss |
| **RTO** | Recovery Time Objective - max acceptable downtime |
| **Quorum** | Minimum nodes needed for consensus |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added multi-primary active-active support
- New conflict resolution engine
- Improved failover with fencing
- Added geographic replication topology

### Version 2.5.0 (2023-12-01)
- Added cascading replication support
- New read replica load balancing
- Improved WAL optimization tools
- Added disaster recovery runbook generation

### Version 2.0.0 (2023-09-15)
- Major API redesign
- Added semi-synchronous replication
- New replication monitoring dashboard
- Improved failover detection

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/awesome-grok/replication.git
cd replication

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
mypy .
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