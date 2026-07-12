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