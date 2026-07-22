---
name: "Backup & Recovery"
version: "2.0.0"
description: "Comprehensive backup and disaster recovery toolkit with automated scheduling, point-in-time recovery, backup verification, cross-region replication, and recovery orchestration for production databases"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database-admin", "backup", "recovery", "disaster-recovery", "point-in-time", "replication"]
category: "database-admin"
personality: "backup-engineer"
use_cases: ["automated backups", "point-in-time recovery", "disaster recovery", "backup verification", "recovery orchestration"]
---

# Backup & Recovery

> Production-grade backup and disaster recovery framework providing automated scheduling, point-in-time recovery, backup verification, cross-region replication, and recovery orchestration for zero-data-loss database operations.

## Overview

The Backup & Recovery module provides a complete disaster recovery toolkit for production databases. It implements incremental and full backup scheduling with retention policies, WAL archiving for point-in-time recovery, backup integrity verification with checksum validation, cross-region backup replication, recovery orchestration with RPO/RTO targets, and automated runbook execution for disaster scenarios. Every operation includes audit logging, progress tracking, and rollback capability.

## Core Capabilities

### 1. Backup Scheduling
- Full, incremental, and differential backup support
- Cron-based scheduling with timezone awareness
- Retention policies (daily, weekly, monthly, yearly)
- Backup window management to avoid peak hours
- Parallel backup streams for large databases

### 2. Point-in-Time Recovery (PITR)
- WAL archiving and management
- Recovery target timestamp/LSN specification
- Consistent recovery from any point in the archive
- Replay speed optimization
- Validation of recovery completeness

### 3. Backup Verification
- Automatic checksum validation
- Restore-to-test-environment verification
- Table-level integrity checks
- Backup age and freshness monitoring
- Corruption detection and alerting

### 4. Cross-Region Replication
- Synchronous and asynchronous backup replication
- Encryption in transit and at rest
- Bandwidth throttling for cost control
- Replication lag monitoring
- Automatic failover to secondary region

### 5. Recovery Orchestration
- Automated recovery runbooks
- RPO and RTO target tracking
- Recovery progress monitoring
- Post-recovery validation
- Communication and notification

### 6. Backup Catalog
- Centralized backup metadata storage
- Search and filter capabilities
- Backup lineage tracking
- Compliance reporting
- Cost attribution

## Usage Examples

### Automated Backup Scheduling

```python
from backup_recovery import BackupOrchestrator, BackupPolicy

orchestrator = BackupOrchestrator(connection_string="postgresql://admin:pass@localhost/prod")

# Define backup policy
policy = BackupPolicy(
    name="production_daily",
    full_schedule="0 2 * * *",  # Daily at 2am
    incremental_schedule="0 */4 * * *",  # Every 4 hours
    retention_days=30,
    retention_weekly=12,
    retention_monthly=12,
    compression=True,
    encryption_key_arn="arn:aws:kms:us-east-1:123456:key/abc-123",
    max_parallel_streams=4,
)

orchestrator.create_policy(policy)

# Trigger immediate backup
backup = orchestrator.run_backup(
    policy_name="production_daily",
    backup_type="full",
    tag="pre-deploy-v2.1.0",
)
print(f"Backup: {backup.filename} ({backup.size_mb:.1f} MB, {backup.duration_seconds:.0f}s)")
```

### Point-in-Time Recovery

```python
from backup_recovery import RecoveryManager, RecoveryTarget

recovery = RecoveryManager(connection_string="postgresql://admin:pass@localhost/prod")

# Recover to specific timestamp
target = RecoveryTarget(
    target_time="2024-01-15T14:30:00Z",
    target_action="promote",
    recovery_mode="archive",
)

result = recovery.recover(
    target=target,
    backup_dir="/backups/postgres",
    wal_archive="/archive/wal/",
    data_directory="/var/lib/postgresql/data",
)

print(f"Recovery: {result.status}")
print(f"Recovered to: {result.recovered_to}")
print(f"Duration: {result.duration_seconds:.0f}s")
print(f"Data loss: {result.estimated_data_loss_seconds:.0f}s")
```

### Backup Verification

```python
from backup_recovery import BackupVerifier

verifier = BackupVerifier(backup_dir="/backups/postgres")

# Verify latest backup
verification = verifier.verify_latest(
    checksum=True,
    restore_test=True,
    test_database="recovery_test",
)

print(f"Verification: {verification.status}")
print(f"Checksum valid: {verification.checksum_valid}")
print(f"Restore test: {verification.restore_test_passed}")
print(f"Tables verified: {verification.tables_verified}")
print(f"Issues: {verification.issues}")
```

### Disaster Recovery

```python
from backup_recovery import DisasterRecoveryManager

dr = DisasterRecoveryManager(primary_region="us-east-1", secondary_region="eu-west-1")

# Configure DR
dr.configure(
    replication_mode="async",
    rpo_target_seconds=300,
    rto_target_seconds=3600,
    automated_failover=True,
    notification_email="ops@company.com",
)

# Run DR drill
drill = dr.run_drill(target_rto=3600)
print(f"DR Drill: {drill.status}")
print(f"Actual RTO: {drill.actual_rto_seconds:.0f}s")
print(f"Actual RPO: {drill.actual_rpo_seconds:.0f}s")
print(f"Data verified: {drill.data_integrity_verified}")
```

## Best Practices

### Backup Strategy
- Follow the 3-2-1 rule: 3 copies, 2 different media, 1 offsite
- Test backup restoration monthly — untested backups are not backups
- Encrypt backups at rest and in transit
- Monitor backup completion and alert on failures

### Recovery Planning
- Define RPO (max data loss) and RTO (max downtime) for each database
- Document and test recovery procedures quarterly
- Maintain offline copies of recovery instructions
- Practice recovery on a fresh environment, not production

### Retention
- Keep daily backups for 7-30 days
- Keep weekly backups for 4-12 weeks
- Keep monthly backups for 12+ months
- Keep yearly backups for compliance (7+ years for financial data)

### Verification
- Verify checksums on every backup
- Perform restore tests quarterly
- Monitor backup sizes for unexpected changes
- Alert on backup failures within 15 minutes

## Related Modules

- **db-management**: Database lifecycle and space management
- **performance-tuning**: Backup performance optimization
- **security-hardening**: Backup encryption and access control
- **monitoring**: Backup monitoring and alerting

---

## Advanced Configuration

### Advanced Backup Policies

```python
from backup_recovery import BackupOrchestrator, BackupPolicy, RetentionPolicy

orchestrator = BackupOrchestrator(connection_string="postgresql://admin:pass@localhost/prod")

# Create comprehensive backup policy
policy = BackupPolicy(
    name="production_comprehensive",
    full_schedule="0 2 * * *",  # Daily at 2am
    incremental_schedule="0 */4 * * *",  # Every 4 hours
    differential_schedule="0 6 * * 1-5",  # Weekdays at 6am
    
    # Retention
    retention_days=30,
    retention_weekly=12,
    retention_monthly=12,
    retention_yearly=7,
    
    # Compression
    compression=True,
    compression_algorithm="zstd",
    compression_level=3,
    
    # Encryption
    encryption_key_arn="arn:aws:kms:us-east-1:123456:key/abc-123",
    encryption_algorithm="AES-256",
    
    # Performance
    max_parallel_streams=4,
    chunk_size_mb=64,
    buffer_size_mb=16,
    
    # Verification
    verify_after_backup=True,
    checksum_algorithm="sha256",
    
    # Notifications
    notify_on_success=False,
    notify_on_failure=True,
    notification_channels=["slack-ops", "email-ops"],
)

orchestrator.create_policy(policy)
```

### Advanced Retention Policies

```python
from backup_recovery import RetentionPolicy, RetentionRule

# Create retention policy with multiple rules
retention = RetentionPolicy(
    name="production_retention",
    rules=[
        RetentionRule(type="daily", keep_days=30, min_backups=7),
        RetentionRule(type="weekly", keep_weeks=12, min_backups=4),
        RetentionRule(type="monthly", keep_months=12, min_backups=3),
        RetentionRule(type="yearly", keep_years=7, min_backups=1),
        RetentionRule(type="tagged", tag="pre-deploy", keep_days=90),
        RetentionRule(type="tagged", tag="audit", keep_days=365),
    ],
    always_keep_last_n=3,
    never_delete_tagged=["compliance", "legal"],
)

orchestrator.set_retention(retention)
```

### Advanced PITR Configuration

```python
from backup_recovery import RecoveryManager, PITRConfig, WALArchiveConfig

# Configure advanced PITR
pitr_config = PITRConfig(
    # WAL archiving
    archive_mode="on",
    archive_command="aws s3 put s3://backups/wal/%f %p",
    archive_timeout=300,  # 5 minutes
    
    # Recovery options
    recovery_target_action="promote",
    recovery_target_timeline="latest",
    
    # Performance
    restore_command="aws s3 cp s3://backups/wal/%f %p",
    max_parallel_workers=4,
    
    # Validation
    validate_recovery=True,
    checksum_validation=True,
)

recovery = RecoveryManager(connection_string=connection_string)
recovery.configure_pitr(pitr_config)
```

## Architecture Patterns

### Backup Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Backup Architecture                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Backup Orchestrator                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │   Policy    │  │  Scheduler  │  │  Verifier   │ │   │
│  │  │   Engine    │  │             │  │             │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Backup Storage Layer                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Local      │  │  S3/GCS     │  │  Tape/Archive│ │   │
│  │  │  Storage    │  │  Cloud      │  │             │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Recovery Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                   Recovery Workflow                         │
├─────────────────────────────────────────────────────────────┤
│  1. Assess Situation                                        │
│     └─► Determine data loss extent, RTO/RPO requirements    │
│  2. Select Recovery Point                                   │
│     └─► Choose backup set + WAL range                       │
│  3. Prepare Environment                                     │
│     └─► Provision server, restore base backup               │
│  4. Restore Base Backup                                     │
│     └─► Decompress, verify checksums                        │
│  5. Replay WAL Archives                                     │
│     └─► Apply WAL files up to recovery target               │
│  6. Validate Recovery                                       │
│     └─► Check data integrity, run queries                   │
│  7. Promote to Production                                   │
│     └─► Update DNS, connection strings                      │
│  8. Post-Recovery Verification                              │
│     └─► Monitor, verify application connectivity            │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with CI/CD pipeline
from backup_recovery import BackupOrchestrator

orchestrator = BackupOrchestrator(connection_string=connection_string)

# Pre-deployment backup
def pre_deploy_backup(version: str):
    backup = orchestrator.run_backup(
        policy_name="production_daily",
        backup_type="full",
        tag=f"pre-deploy-{version}",
    )
    return backup.id

# Post-deployment verification
def verify_deployment(backup_id: str):
    verification = orchestrator.verify_backup(backup_id)
    return verification.success
```

### Monitoring Integration

```python
# Integration with Prometheus
from prometheus_client import Counter, Histogram, Gauge

BACKUP_SIZE = Gauge('db_backup_size_bytes', 'Backup size', ['type'])
BACKUP_DURATION = Histogram('db_backup_duration_seconds', 'Backup duration', ['type'])
BACKUP_SUCCESS = Counter('db_backup_success_total', 'Successful backups', ['policy'])
BACKUP_FAILURE = Counter('db_backup_failure_total', 'Failed backups', ['policy', 'error'])

class BackupMetrics:
    def record_backup(self, backup_type: str, size_bytes: int, duration: float, success: bool, policy: str):
        BACKUP_SIZE.labels(type=backup_type).set(size_bytes)
        BACKUP_DURATION.labels(type=backup_type).observe(duration)
        
        if success:
            BACKUP_SUCCESS.labels(policy=policy).inc()
        else:
            BACKUP_FAILURE.labels(policy=policy, error='unknown').inc()
```

## Performance Optimization

### Backup Performance Tuning

| Parameter | Default | Optimized | Impact |
|-----------|---------|-----------|--------|
| max_parallel_streams | 1 | 4 | 4x faster backup |
| chunk_size_mb | 32 | 64 | Better throughput |
| compression_level | 6 | 3 | Faster, slightly larger |
| buffer_size_mb | 8 | 16 | Better I/O |

### WAL Archiving Optimization

```python
from backup_recovery import WALOptimizer

optimizer = WALOptimizer()

# Optimize WAL archiving
optimizer.configure(
    archive_timeout=300,  # Archive every 5 minutes
    max_wal_senders=10,
    wal_keep_size="10GB",
    archive_command="aws s3 put s3://backups/wal/%f %p --storage-class STANDARD_IA",
)

# Monitor WAL generation
stats = optimizer.get_stats()
print(f"WAL generation rate: {stats.generation_rate_mb_per_min:.1f} MB/min")
print(f"WAL retention: {stats.retention_mb:.1f} MB")
print(f"Archive lag: {stats.archive_lag_seconds:.0f}s")
```

### Recovery Performance

```python
from backup_recovery import RecoveryOptimizer

optimizer = RecoveryOptimizer()

# Optimize recovery process
optimizer.configure(
    max_parallel_workers=8,
    restore_command="aws s3 cp s3://backups/%f %p",
    shared_buffers="4GB",
    work_mem="256MB",
)

# Estimate recovery time
estimate = optimizer.estimate_recovery_time(
    backup_size_gb=100,
    wal_size_gb=20,
    target_time="2024-01-15T14:30:00Z",
)
print(f"Estimated recovery time: {estimate.duration_minutes:.0f} minutes")
```

## Security Considerations

### Backup Encryption

```python
from backup_recovery import EncryptionManager

encryption = EncryptionManager()

# Configure backup encryption
encryption.configure(
    algorithm="AES-256-GCM",
    key_management="aws-kms",
    key_rotation_days=90,
    encrypt_metadata=True,
    encrypt_checksums=True,
)

# Verify encryption
status = encryption.get_status()
print(f"Encryption active: {status.active}")
print(f"Key rotation due: {status.next_rotation_date}")
```

### Backup Access Control

```python
from backup_recovery import AccessControl

access = AccessControl()

# Configure backup access
access.configure(
    backup_read_roles=["backup_admin", "disaster_recovery"],
    backup_write_roles=["backup_admin"],
    backup_delete_roles=["backup_admin"],
    backup_verify_roles=["backup_admin", "dba"],
)

# Audit backup access
audit = access.audit_access(days=30)
print(f"Total access events: {audit.total_events}")
for event in audit.events:
    print(f"  {event.timestamp}: {event.user} {event.action} {event.backup_id}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Backup fails | Error in backup log | Check disk space, permissions, network |
| WAL archive full | Disk space exhausted | Increase retention, archive to colder storage |
| Recovery slow | Long recovery time | Increase parallel workers, faster storage |
| Corrupted backup | Checksum mismatch | Use verified backup, investigate cause |
| Backup too large | Excessive storage costs | Enable compression, review retention |

### Diagnostic Queries

```sql
-- Check WAL archiving status
SELECT
    archived_count,
    last_archived_time,
    last_archived_wal,
    failed_count,
    last_failed_time,
    last_failed_wal
FROM pg_stat_archiver;

-- Check replication slots
SELECT
    slot_name,
    active,
    restart_lsn,
    confirmed_flush_lsn,
    pg_wal_lsn_diff(restart_lsn, confirmed_flush_lsn) AS retained_bytes
FROM pg_replication_slots;

-- Check backup-related settings
SHOW archive_mode;
SHOW archive_command;
SHOW archive_timeout;
SHOW max_wal_senders;
SHOW wal_keep_size;
```

## API Reference

### BackupOrchestrator

```python
class BackupOrchestrator:
    def __init__(self, connection_string: str)
    def create_policy(self, policy: BackupPolicy) -> PolicyResult
    def run_backup(self, policy_name: str, backup_type: str, tag: str = None) -> BackupResult
    def list_backups(self, policy_name: str = None, limit: int = 100) -> list[BackupInfo]
    def verify_backup(self, backup_id: str) -> VerificationResult
    def delete_backup(self, backup_id: str) -> DeleteResult
    def set_retention(self, retention: RetentionPolicy) -> RetentionResult
```

### RecoveryManager

```python
class RecoveryManager:
    def __init__(self, connection_string: str)
    def configure_pitr(self, config: PITRConfig) -> ConfigResult
    def recover(self, target: RecoveryTarget, **kwargs) -> RecoveryResult
    def get_recovery_history(self) -> list[RecoveryEvent]
    def estimate_recovery_time(self, backup_id: str, target_time: str) -> RecoveryEstimate
    def validate_recovery(self) -> ValidationResult
```

### DisasterRecoveryManager

```python
class DisasterRecoveryManager:
    def __init__(self, primary_region: str, secondary_region: str)
    def configure(self, **kwargs) -> ConfigResult
    def run_drill(self, target_rto: int = None) -> DrillResult
    def get_dr_status(self) -> DRStatus
    def get_dr_history(self) -> list[DREvent]
    def generate_runbook(self) -> str
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class BackupType(Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    WAL = "wal"

class BackupState(Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    VERIFYING = "verifying"
    EXPIRED = "expired"

class RecoveryTarget(Enum):
    TIMESTAMP = "timestamp"
    LSN = "lsn"
    TRANSACTION_ID = "transaction_id"
    NAME = "name"
    TIME = "time"

@dataclass
class BackupInfo:
    id: str
    filename: str
    backup_type: BackupType
    state: BackupState
    size_bytes: int
    compressed_size_bytes: int
    duration_seconds: float
    checksum: str
    created_at: datetime
    expires_at: Optional[datetime]
    tag: Optional[str]
    policy_name: str

@dataclass
class RecoveryTarget:
    target_type: RecoveryTarget
    target_value: str
    target_action: str = "promote"
    target_timeline: str = "latest"

@dataclass
class PITRConfig:
    archive_mode: str
    archive_command: str
    archive_timeout: int
    recovery_target_action: str
    recovery_target_timeline: str
    max_parallel_workers: int
```

## Deployment Guide

### Docker Deployment

```yaml
version: '3.8'
services:
  backup-worker:
    image: backup-worker:latest
    environment:
      DATABASE_URL: ${DATABASE_URL}
      BACKUP_S3_BUCKET: ${BACKUP_S3_BUCKET}
      KMS_KEY_ARN: ${KMS_KEY_ARN}
    volumes:
      - backup_data:/backups
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '2'
```

### Kubernetes CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: backup-worker:latest
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secrets
                  key: url
          backoffLimit: 3
          successfulJobsHistoryLimit: 7
          failedJobsHistoryLimit: 3
```

## Monitoring & Observability

### Metrics Collection

```python
from backup_recovery import MetricsCollector

collector = MetricsCollector()

# Collect backup metrics
collector.gauge("backup.size.bytes", size_bytes, tags={"type": backup_type, "policy": policy})
collector.histogram("backup.duration.seconds", duration, tags={"type": backup_type})
collector.counter("backup.success.total", 1, tags={"policy": policy})
collector.counter("backup.failure.total", 1, tags={"policy": policy, "error": error_type})
```

### Alerting Rules

```yaml
groups:
  - name: backup_alerts
    rules:
      - alert: BackupFailed
        expr: increase(db_backup_failure_total[1h]) > 0
        for: 0m
        labels:
          severity: critical
        annotations:
          summary: "Backup failure detected"
          
      - alert: BackupTooOld
        expr: time() - db_backup_last_success_timestamp > 86400
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: "No successful backup in 24 hours"
          
      - alert: WALArchiveLag
        expr: db_wal_archive_lag_seconds > 3600
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "WAL archive lag exceeds 1 hour"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from backup_recovery import BackupOrchestrator

@pytest.fixture
def orchestrator():
    return BackupOrchestrator(connection_string="postgresql://localhost/test")

def test_run_backup(orchestrator):
    backup = orchestrator.run_backup(policy_name="test", backup_type="full")
    assert backup.state == BackupState.COMPLETED

def test_verify_backup(orchestrator):
    verification = orchestrator.verify_backup(backup_id="test-backup-1")
    assert verification.success
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| PostgreSQL | 12 | 15+ |
| AWS CLI | 2.0 | 2.15+ |

## Glossary

| Term | Definition |
|------|------------|
| **PITR** | Point-in-Time Recovery |
| **WAL** | Write-Ahead Log |
| **RPO** | Recovery Point Objective - max data loss |
| **RTO** | Recovery Time Objective - max downtime |
| **LSN** | Log Sequence Number |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added advanced PITR configuration
- New retention policy engine
- Improved recovery performance
- Added DR drill automation

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/backup-recovery.git
cd backup-recovery
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills