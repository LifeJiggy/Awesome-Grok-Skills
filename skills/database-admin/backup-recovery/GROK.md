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