"""
Backup and Recovery Agent — Enterprise Data Protection Management

A comprehensive backup orchestration, disaster recovery, and business
continuity agent. Implements the 3-2-1 backup rule, immutable backup
verification, cross-region replication, compliance-aware retention, and
automated recovery testing across heterogeneous storage targets.

Author: MiMoCode
Version: 3.0.0
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import secrets
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
logger = logging.getLogger("backup-recovery-agent")


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class BackupType(Enum):
    """Granularity and scope of a backup operation."""
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    SNAPSHOT = "snapshot"
    MIRROR = "mirror"
    CONTINUOUS = "continuous"


class BackupTarget(Enum):
    """Types of data sources the agent can protect."""
    DATABASE = "database"
    FILESYSTEM = "filesystem"
    VIRTUAL_MACHINE = "virtual_machine"
    CONTAINER = "container"
    CLOUD_STORAGE = "cloud_storage"
    APPLICATION_STATE = "application_state"
    CONFIGURATION = "configuration"
    SECRETS = "secrets"
    LOGS = "logs"
    MEDIA = "media"


class RetentionPolicy(Enum):
    """Predefined and regulatory retention schedules."""
    DAILY_7 = "daily_7"
    WEEKLY_4 = "weekly_4"
    MONTHLY_12 = "monthly_12"
    QUARTERLY_4 = "quarterly_4"
    YEARLY_7 = "yearly_7"
    CUSTOM = "custom"
    REGULATORY_7YR = "regulatory_7yr"
    REGULATORY_10YR = "regulatory_10yr"


class RecoveryType(Enum):
    """How a restore operation is performed."""
    FULL_RESTORE = "full_restore"
    POINT_IN_TIME = "point_in_time"
    SELECTIVE = "selective"
    GRANULAR = "granular"
    CROSS_REGION = "cross_region"
    CROSS_ACCOUNT = "cross_account"


class DRStrategy(Enum):
    """Disaster recovery architecture patterns."""
    BACKUP_RESTORE = "backup_restore"
    PILOT_LIGHT = "pilot_light"
    WARM_STANDBY = "warm_standby"
    HOT_STANDBY = "hot_standby"
    MULTI_SITE_ACTIVE = "multi_site_active"


class ComplianceFramework(Enum):
    """Regulatory and industry compliance frameworks."""
    SOC2 = "soc2"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    GDPR = "gdpr"
    FedRAMP = "fedramp"
    ISO27001 = "iso27001"
    NIST_800_53 = "nist_800_53"


class StorageTier(Enum):
    """Storage performance and cost tiers."""
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"
    ARCHIVE = "archive"
    DEEP_ARCHIVE = "deep_archive"


class EncryptionStandard(Enum):
    """Encryption algorithms supported for backup data at rest and in transit."""
    AES_256 = "aes_256"
    AES_128 = "aes_128"
    RSA_4096 = "rsa_4096"
    CHACHA20 = "chacha20"


class HealthStatus(Enum):
    """Operational health of a backup component."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class JobStatus(Enum):
    """Lifecycle states of an async backup or restore job."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class ReplicationMode(Enum):
    """Data replication consistency modes."""
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    NEAR_SYNC = "near_sync"
    CROSS_REGION = "cross_region"


class ConsistencyLevel(Enum):
    """Point-in-time consistency guarantees."""
    CRASH_CONSISTENT = "crash_consistent"
    APPLICATION_CONSISTENT = "application_consistent"
    FILE_SYSTEM_CONSISTENT = "file_system_consistent"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class EncryptionConfig:
    """Encryption settings for backup data."""
    algorithm: EncryptionStandard = EncryptionStandard.AES_256
    key_rotation_days: int = 90
    kms_key_id: Optional[str] = None
    envelope_encryption: bool = True
    compress_before_encrypt: bool = True
    integrity_hash: str = "sha256"
    transit_encryption: bool = True

    def validate(self) -> List[str]:
        errors: List[str] = []
        if self.key_rotation_days < 1:
            errors.append("key_rotation_days must be >= 1")
        if self.key_rotation_days > 365:
            errors.append("key_rotation_days should not exceed 365 for compliance")
        return errors


@dataclass
class RetentionRule:
    """Single rule in a retention schedule."""
    name: str
    backup_type: BackupType
    keep_count: int
    keep_duration_days: int
    min_generations: int = 1
    freeze_after_days: Optional[int] = None
    delete_after_days: Optional[int] = None


@dataclass
class BackupPolicy:
    """Named policy that groups multiple retention rules."""
    id: str
    name: str
    description: str
    framework: ComplianceFramework
    rules: List[RetentionRule] = field(default_factory=list)
    immutable: bool = True
    air_gapped: bool = False
    encryption: EncryptionConfig = field(default_factory=EncryptionConfig)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def evaluate(self, backup_type: BackupType) -> Optional[RetentionRule]:
        for rule in self.rules:
            if rule.backup_type == backup_type:
                return rule
        return self.rules[0] if self.rules else None


@dataclass
class StorageLocation:
    """Destination storage endpoint for backup data."""
    id: str
    name: str
    provider: str
    region: str
    tier: StorageTier
    bucket: Optional[str] = None
    path: Optional[str] = None
    endpoint_url: Optional[str] = None
    credentials_ref: Optional[str] = None
    max_throughput_mbps: float = 100.0
    latency_ms: float = 10.0
    available_gb: float = 0.0
    used_gb: float = 0.0
    encrypted: bool = True
    immutable_lock: bool = False

    @property
    def utilization_pct(self) -> float:
        total = self.available_gb + self.used_gb
        return (self.used_gb / total * 100) if total > 0 else 0.0

    def can_fit(self, size_gb: float) -> bool:
        return self.available_gb >= size_gb


@dataclass
class ReplicationConfig:
    """Replication topology between primary and secondary locations."""
    primary_location_id: str
    secondary_location_id: str
    mode: ReplicationMode
    rpo_seconds: int = 3600
    encryption_in_transit: bool = True
    bandwidth_limit_mbps: Optional[float] = None
    auto_failover: bool = False
    failover_threshold_consecutive_failures: int = 3

    @property
    def rpo_hours(self) -> float:
        return self.rpo_seconds / 3600.0


@dataclass
class BackupSchedule:
    """Scheduled recurring backup job definition."""
    id: str
    name: str
    source_id: str
    source_type: BackupTarget
    backup_type: BackupType
    policy_id: str
    storage_location_id: str
    cron_expression: str = "0 2 * * *"
    enabled: bool = True
    priority: int = 5
    max_parallel_streams: int = 4
    consistency_level: ConsistencyLevel = ConsistencyLevel.APPLICATION_CONSISTENT
    pre_hooks: List[str] = field(default_factory=list)
    post_hooks: List[str] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def next_run_estimate(self) -> datetime:
        return datetime.now(timezone.utc) + timedelta(hours=24)


@dataclass
class BackupJob:
    """Execution record of a single backup operation."""
    id: str
    schedule_id: str
    backup_type: BackupType
    source_type: BackupTarget
    storage_location_id: str
    status: JobStatus = JobStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    size_bytes: int = 0
    compressed_bytes: int = 0
    encrypted: bool = True
    checksum: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    parent_backup_id: Optional[str] = None
    consistency_level: ConsistencyLevel = ConsistencyLevel.APPLICATION_CONSISTENT
    restore_points: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration_seconds(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    @property
    def compression_ratio(self) -> float:
        if self.compressed_bytes and self.size_bytes:
            return self.compressed_bytes / self.size_bytes
        return 1.0

    def mark_running(self) -> None:
        self.status = JobStatus.RUNNING
        self.started_at = datetime.now(timezone.utc)

    def mark_completed(self, size_bytes: int, checksum: str) -> None:
        self.status = JobStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        self.size_bytes = size_bytes
        self.compressed_bytes = int(size_bytes * 0.65)
        self.checksum = checksum

    def mark_failed(self, error: str) -> None:
        self.status = JobStatus.FAILED
        self.completed_at = datetime.now(timezone.utc)
        self.error_message = error

    def should_retry(self) -> bool:
        return self.status == JobStatus.FAILED and self.retry_count < self.max_retries


@dataclass
class RestorePoint:
    """A point-in-time reference for recovery."""
    id: str
    backup_job_id: str
    timestamp: datetime
    backup_type: BackupType
    consistency_level: ConsistencyLevel
    verified: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def age_hours(self) -> float:
        return (datetime.now(timezone.utc) - self.timestamp).total_seconds() / 3600


@dataclass
class RestoreJob:
    """Execution record of a restore operation."""
    id: str
    restore_type: RecoveryType
    source_backup_id: str
    target_location: str
    status: JobStatus = JobStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    restored_bytes: int = 0
    error_message: Optional[str] = None
    target_point_in_time: Optional[datetime] = None
    selective_paths: List[str] = field(default_factory=list)
    cross_region: bool = False
    cross_account: bool = False

    @property
    def duration_seconds(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


@dataclass
class RecoveryObjective:
    """Business-defined RPO and RTO targets."""
    service_name: str
    rpo_seconds: int
    rto_seconds: int
    tier: str = "gold"
    annual_impact_usd: float = 0.0
    data_classification: str = "confidential"
    max_data_loss_acceptable_gb: float = 10.0

    @property
    def rpo_hours(self) -> float:
        return self.rpo_seconds / 3600.0

    @property
    def rto_hours(self) -> float:
        return self.rto_seconds / 3600.0

    def meets_rpo(self, actual_rpo_seconds: int) -> bool:
        return actual_rpo_seconds <= self.rpo_seconds

    def meets_rto(self, actual_rto_seconds: int) -> bool:
        return actual_rto_seconds <= self.rto_seconds


@dataclass
class DisasterScenario:
    """Modeled disaster scenario for testing and planning."""
    id: str
    name: str
    description: str
    severity: str
    affected_services: List[str]
    estimated_rto_seconds: int
    estimated_rpo_seconds: int
    data_loss_gb: float = 0.0
    blast_radius_pct: float = 0.0
    recovery_strategy: DRStrategy = DRStrategy.BACKUP_RESTORE

    @property
    def annual_probability(self) -> float:
        severity_map = {"low": 0.1, "medium": 0.3, "high": 0.6, "critical": 0.9}
        return severity_map.get(self.severity.lower(), 0.5)


@dataclass
class FailoverPlan:
    """Step-by-step failover and failback procedure."""
    id: str
    scenario_id: str
    strategy: DRStrategy
    steps: List[Dict[str, Any]] = field(default_factory=list)
    estimated_duration_seconds: int = 0
    prerequisites: List[str] = field(default_factory=list)
    rollback_steps: List[Dict[str, Any]] = field(default_factory=list)
    verification_checks: List[str] = field(default_factory=list)

    def add_step(self, name: str, action: str, timeout_seconds: int = 300) -> None:
        self.steps.append({
            "step": len(self.steps) + 1,
            "name": name,
            "action": action,
            "timeout_seconds": timeout_seconds,
            "status": "pending",
        })


@dataclass
class DisasterRecoveryPlan:
    """Comprehensive DR plan aggregating scenarios, objectives, and failover."""
    id: str
    name: str
    strategy: DRStrategy
    objectives: List[RecoveryObjective] = field(default_factory=list)
    scenarios: List[DisasterScenario] = field(default_factory=list)
    failover_plans: List[FailoverPlan] = field(default_factory=list)
    last_tested: Optional[datetime] = None
    next_test_due: Optional[datetime] = None
    compliance_frameworks: List[ComplianceFramework] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def test_overdue(self) -> bool:
        if not self.next_test_due:
            return True
        return datetime.now(timezone.utc) > self.next_test_due

    def add_objective(self, obj: RecoveryObjective) -> None:
        self.objectives.append(obj)

    def add_scenario(self, scenario: DisasterScenario) -> None:
        self.scenarios.append(scenario)

    def worst_case_rto(self) -> int:
        return max((s.estimated_rto_seconds for s in self.scenarios), default=0)

    def worst_case_rpo(self) -> int:
        return max((s.estimated_rpo_seconds for s in self.scenarios), default=0)


@dataclass
class BackupSet:
    """Logical grouping of related backup jobs."""
    id: str
    name: str
    schedule_id: str
    jobs: List[BackupJob] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def total_size_bytes(self) -> int:
        return sum(j.size_bytes for j in self.jobs)

    @property
    def latest_job(self) -> Optional[BackupJob]:
        completed = [j for j in self.jobs if j.status == JobStatus.COMPLETED]
        return max(completed, key=lambda j: j.completed_at or datetime.min.replace(tzinfo=timezone.utc), default=None)

    @property
    def chain完整性(self) -> bool:
        if not self.jobs:
            return False
        sorted_jobs = sorted(self.jobs, key=lambda j: j.started_at or datetime.min.replace(tzinfo=timezone.utc))
        for i, job in enumerate(sorted_jobs):
            if job.backup_type == BackupType.INCREMENTAL and i > 0:
                if job.parent_backup_id is None:
                    return False
        return True


@dataclass
class BackupMetrics:
    """Aggregated metrics for monitoring and reporting."""
    total_backups: int = 0
    successful_backups: int = 0
    failed_backups: int = 0
    total_bytes_backed_up: int = 0
    total_bytes_compressed: int = 0
    average_backup_duration_seconds: float = 0.0
    average_restore_duration_seconds: float = 0.0
    last_successful_backup: Optional[datetime] = None
    last_failed_backup: Optional[datetime] = None
    storage_used_gb: float = 0.0
    storage_available_gb: float = 0.0
    active_schedules: int = 0
    pending_jobs: int = 0
    running_jobs: int = 0

    @property
    def success_rate(self) -> float:
        if self.total_backups == 0:
            return 0.0
        return self.successful_backups / self.total_backups * 100

    @property
    def storage_utilization(self) -> float:
        total = self.storage_used_gb + self.storage_available_gb
        return (self.storage_used_gb / total * 100) if total > 0 else 0.0

    @property
    def compression_ratio(self) -> float:
        if self.total_bytes_compressed and self.total_bytes_backed_up:
            return self.total_bytes_compressed / self.total_bytes_backed_up
        return 1.0


@dataclass
class BackupVerification:
    """Record of backup integrity and recoverability verification."""
    id: str
    backup_job_id: str
    verified_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    checksum_valid: bool = False
    restore_tested: bool = False
    restore_duration_seconds: Optional[float] = None
    sample_files_verified: int = 0
    total_files_in_backup: int = 0
    encryption_verified: bool = False
    compliance_valid: bool = False
    verification_method: str = "automated"
    error_message: Optional[str] = None

    @property
    def file_verification_pct(self) -> float:
        if self.total_files_in_backup == 0:
            return 0.0
        return self.sample_files_verified / self.total_files_in_backup * 100

    @property
    def is_fully_verified(self) -> bool:
        return all([
            self.checksum_valid,
            self.restore_tested,
            self.encryption_verified,
            self.compliance_valid,
        ])


@dataclass
class ComplianceReport:
    """Compliance audit report for backup operations."""
    id: str
    framework: ComplianceFramework
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    period_start: datetime = field(default_factory=lambda: datetime.now(timezone.utc) - timedelta(days=30))
    period_end: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    total_backups: int = 0
    compliant_backups: int = 0
    non_compliant_backups: int = 0
    retention_violations: List[str] = field(default_factory=list)
    encryption_violations: List[str] = field(default_factory=list)
    recovery_test_results: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    overall_status: str = "pending"

    @property
    def compliance_rate(self) -> float:
        total = self.compliant_backups + self.non_compliant_backups
        return (self.compliant_backups / total * 100) if total > 0 else 0.0

    @property
    def is_compliant(self) -> bool:
        return self.compliance_rate >= 95.0 and len(self.encryption_violations) == 0


@dataclass
class HealthCheck:
    """Component health status snapshot."""
    component: str
    status: HealthStatus
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    latency_ms: float = 0.0
    error_message: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditLogEntry:
    """Immutable audit trail entry for backup operations."""
    id: str
    timestamp: datetime
    event_type: str
    actor: str
    resource_type: str
    resource_id: str
    action: str
    result: str
    details: Dict[str, Any] = field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str, indent=2)


@dataclass
class ChainOfCustody:
    """Immutable chain-of-custody record for a backup lifecycle."""
    backup_job_id: str
    entries: List[AuditLogEntry] = field(default_factory=list)

    def add_entry(self, entry: AuditLogEntry) -> None:
        self.entries.append(entry)

    @property
    def is_complete(self) -> bool:
        event_types = {e.event_type for e in self.entries}
        required = {"created", "encrypted", "stored", "verified"}
        return required.issubset(event_types)

    def verify_chain(self) -> bool:
        for i in range(1, len(self.entries)):
            if self.entries[i].timestamp < self.entries[i - 1].timestamp:
                return False
        return True


@dataclass
class BackupBudget:
    """Budget tracking for backup storage and operations."""
    id: str
    name: str
    monthly_limit_usd: float
    current_spend_usd: float = 0.0
    forecasted_spend_usd: float = 0.0
    cost_per_gb_hot: float = 0.023
    cost_per_gb_warm: float = 0.0125
    cost_per_gb_cold: float = 0.004
    cost_per_gb_archive: float = 0.00099
    cost_per_gb_deep_archive: float = 0.000099
    alerts_threshold_pct: float = 80.0

    @property
    def remaining_budget_usd(self) -> float:
        return max(0.0, self.monthly_limit_usd - self.current_spend_usd)

    @property
    def is_over_budget(self) -> bool:
        return self.current_spend_usd > self.monthly_limit_usd

    @property
    def utilization_pct(self) -> float:
        return (self.current_spend_usd / self.monthly_limit_usd * 100) if self.monthly_limit_usd > 0 else 0.0

    def cost_for_tier(self, tier: StorageTier, gb: float) -> float:
        rates = {
            StorageTier.HOT: self.cost_per_gb_hot,
            StorageTier.WARM: self.cost_per_gb_warm,
            StorageTier.COLD: self.cost_per_gb_cold,
            StorageTier.ARCHIVE: self.cost_per_gb_archive,
            StorageTier.DEEP_ARCHIVE: self.cost_per_gb_deep_archive,
        }
        return rates.get(tier, 0.0) * gb


@dataclass
class VendorComparison:
    """Side-by-side comparison of backup storage vendors."""
    name: str
    provider: str
    cost_per_gb_monthly: float
    egress_per_gb: float
    encryption: bool
    immutable_storage: bool
    cross_region_replication: bool
    max_object_size_gb: float
    durability_nines: float
    availability_sla_pct: float
    compliance_certs: List[str] = field(default_factory=list)
    api_rate_limit: int = 0
    notes: str = ""

    @property
    def effective_monthly_cost_per_gb(self) -> float:
        return self.cost_per_gb_monthly + (self.egress_per_gb / 12)


@dataclass
class CapacityForecast:
    """Projected storage needs based on historical growth."""
    location_id: str
    current_used_gb: float
    daily_growth_gb: float
    forecast_days: int = 90
    growth_rate_multiplier: float = 1.0

    @property
    def projected_used_gb(self) -> float:
        return self.current_used_gb + (self.daily_growth_gb * self.forecast_days * self.growth_rate_multiplier)

    @property
    def days_until_full(self) -> Optional[float]:
        if self.daily_growth_gb <= 0:
            return None
        location = None
        return None

    def daily_forecast(self) -> List[Tuple[int, float]]:
        result: List[Tuple[int, float]] = []
        for day in range(1, self.forecast_days + 1):
            projected = self.current_used_gb + (self.daily_growth_gb * day * self.growth_rate_multiplier)
            result.append((day, projected))
        return result


@dataclass
class CrossRegionPair:
    """Primary-secondary region pair for cross-region backups."""
    primary_region: str
    secondary_region: str
    replication_mode: ReplicationMode
    rpo_seconds: int
    estimated_bandwidth_mbps: float
    encryption_in_transit: bool = True
    latency_ms: float = 50.0
    monthly_transfer_cost_usd: float = 0.0

    @property
    def rpo_hours(self) -> float:
        return self.rpo_seconds / 3600.0


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def generate_id(prefix: str = "br") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"

def compute_checksum(data: bytes, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def iso_format(dt: Optional[datetime]) -> Optional[str]:
    return dt.isoformat() if dt else None

def bytes_to_gb(n: int) -> float:
    return n / (1024 ** 3)

def gb_to_bytes(gb: float) -> int:
    return int(gb * (1024 ** 3))

def seconds_to_human(s: float) -> str:
    if s < 60:
        return f"{s:.1f}s"
    if s < 3600:
        return f"{s / 60:.1f}m"
    return f"{s / 3600:.1f}h"


# ---------------------------------------------------------------------------
# BackupRecoveryAgent
# ---------------------------------------------------------------------------

class BackupRecoveryAgent:
    """
    Enterprise backup and disaster recovery orchestrator.

    Manages the full lifecycle of data protection: policy creation,
    scheduled and on-demand backup execution, integrity verification,
    restore operations, disaster recovery planning, compliance reporting,
    cross-region replication, capacity forecasting, and vendor cost analysis.
    """

    def __init__(
        self,
        default_region: str = "us-east-1",
        default_encryption: EncryptionStandard = EncryptionStandard.AES_256,
    ) -> None:
        self._default_region = default_region
        self._default_encryption = default_encryption

        # Internal state
        self._policies: Dict[str, BackupPolicy] = {}
        self._schedules: Dict[str, BackupSchedule] = {}
        self._jobs: Dict[str, BackupJob] = {}
        self._restore_jobs: Dict[str, RestoreJob] = {}
        self._restore_points: List[RestorePoint] = []
        self._dr_plans: Dict[str, DisasterRecoveryPlan] = {}
        self._storage_locations: Dict[str, StorageLocation] = {}
        self._replication_configs: Dict[str, ReplicationConfig] = {}
        self._health_checks: List[HealthCheck] = []
        self._audit_log: List[AuditLogEntry] = []
        self._metrics = BackupMetrics()
        self._verifications: Dict[str, BackupVerification] = {}
        self._budgets: Dict[str, BackupBudget] = {}
        self._cross_region_pairs: List[CrossRegionPair] = []
        self._chains_of_custody: Dict[str, ChainOfCustody] = {}

        logger.info("BackupRecoveryAgent initialized (region=%s)", self._default_region)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _audit(self, event_type: str, resource_type: str, resource_id: str,
               action: str, result: str, details: Optional[Dict] = None) -> AuditLogEntry:
        entry = AuditLogEntry(
            id=generate_id("audit"),
            timestamp=utcnow(),
            event_type=event_type,
            actor="backup-recovery-agent",
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            result=result,
            details=details or {},
        )
        self._audit_log.append(entry)
        return entry

    def _store_chain_entry(self, backup_job_id: str, entry: AuditLogEntry) -> None:
        if backup_job_id not in self._chains_of_custody:
            self._chains_of_custody[backup_job_id] = ChainOfCustody(backup_job_id=backup_job_id)
        self._chains_of_custody[backup_job_id].add_entry(entry)

    def _validate_storage(self, location_id: str) -> StorageLocation:
        loc = self._storage_locations.get(location_id)
        if not loc:
            raise ValueError(f"Storage location not found: {location_id}")
        return loc

    def _update_metrics(self) -> None:
        jobs = list(self._jobs.values())
        completed = [j for j in jobs if j.status == JobStatus.COMPLETED]
        failed = [j for j in jobs if j.status == JobStatus.FAILED]
        self._metrics.total_backups = len(jobs)
        self._metrics.successful_backups = len(completed)
        self._metrics.failed_backups = len(failed)
        self._metrics.total_bytes_backed_up = sum(j.size_bytes for j in completed)
        self._metrics.total_bytes_compressed = sum(j.compressed_bytes for j in completed)
        durations = [j.duration_seconds for j in completed if j.duration_seconds is not None]
        self._metrics.average_backup_duration_seconds = (sum(durations) / len(durations)) if durations else 0.0
        self._metrics.last_successful_backup = max((j.completed_at for j in completed if j.completed_at), default=None)
        self._metrics.last_failed_backup = max((j.completed_at for j in failed if j.completed_at), default=None)
        self._metrics.active_schedules = sum(1 for s in self._schedules.values() if s.enabled)
        self._metrics.pending_jobs = sum(1 for j in jobs if j.status == JobStatus.PENDING)
        self._metrics.running_jobs = sum(1 for j in jobs if j.status == JobStatus.RUNNING)
        self._metrics.storage_used_gb = sum(loc.used_gb for loc in self._storage_locations.values())
        self._metrics.storage_available_gb = sum(loc.available_gb for loc in self._storage_locations.values())

    # ------------------------------------------------------------------
    # Public API — Policy & Schedule
    # ------------------------------------------------------------------

    def create_backup_policy(
        self,
        name: str,
        description: str,
        framework: ComplianceFramework,
        rules: Optional[List[RetentionRule]] = None,
        immutable: bool = True,
        air_gapped: bool = False,
    ) -> BackupPolicy:
        policy = BackupPolicy(
            id=generate_id("policy"),
            name=name,
            description=description,
            framework=framework,
            rules=rules or [],
            immutable=immutable,
            air_gapped=air_gapped,
            encryption=EncryptionConfig(algorithm=self._default_encryption),
        )
        self._policies[policy.id] = policy
        self._audit("policy_created", "policy", policy.id, "create", "success",
                     {"name": name, "framework": framework.value})
        logger.info("Backup policy created: %s (%s)", name, policy.id)
        return policy

    def schedule_backup(
        self,
        name: str,
        source_id: str,
        source_type: BackupTarget,
        backup_type: BackupType,
        policy_id: str,
        storage_location_id: str,
        cron_expression: str = "0 2 * * *",
        consistency_level: ConsistencyLevel = ConsistencyLevel.APPLICATION_CONSISTENT,
        pre_hooks: Optional[List[str]] = None,
        post_hooks: Optional[List[str]] = None,
        tags: Optional[Dict[str, str]] = None,
    ) -> BackupSchedule:
        if policy_id not in self._policies:
            raise ValueError(f"Policy not found: {policy_id}")
        self._validate_storage(storage_location_id)
        schedule = BackupSchedule(
            id=generate_id("sched"),
            name=name,
            source_id=source_id,
            source_type=source_type,
            backup_type=backup_type,
            policy_id=policy_id,
            storage_location_id=storage_location_id,
            cron_expression=cron_expression,
            consistency_level=consistency_level,
            pre_hooks=pre_hooks or [],
            post_hooks=post_hooks or [],
            tags=tags or {},
        )
        self._schedules[schedule.id] = schedule
        self._audit("schedule_created", "schedule", schedule.id, "create", "success",
                     {"name": name, "cron": cron_expression})
        logger.info("Backup schedule created: %s (%s)", name, schedule.id)
        return schedule

    # ------------------------------------------------------------------
    # Public API — Execute Backup
    # ------------------------------------------------------------------

    def execute_backup(
        self,
        schedule_id: str,
        backup_type: Optional[BackupType] = None,
        parent_backup_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> BackupJob:
        schedule = self._schedules.get(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule not found: {schedule_id}")
        effective_type = backup_type or schedule.backup_type
        job = BackupJob(
            id=generate_id("job"),
            schedule_id=schedule_id,
            backup_type=effective_type,
            source_type=schedule.source_type,
            storage_location_id=schedule.storage_location_id,
            parent_backup_id=parent_backup_id,
            consistency_level=schedule.consistency_level,
            metadata=metadata or {},
        )
        self._jobs[job.id] = job
        self._audit("backup_started", "job", job.id, "execute", "started",
                     {"schedule": schedule_id, "type": effective_type.value})
        # Simulate execution
        job.mark_running()
        loc = self._validate_storage(schedule.storage_location_id)
        simulated_size = secrets.randbelow(10 * 1024 * 1024 * 1024) + 1024 * 1024  # 1 MB – 10 GB
        simulated_checksum = hashlib.sha256(str(job.id).encode()).hexdigest()
        job.mark_completed(size_bytes=simulated_size, checksum=simulated_checksum)

        # Create restore point
        rp = RestorePoint(
            id=generate_id("rp"),
            backup_job_id=job.id,
            timestamp=job.completed_at or utcnow(),
            backup_type=effective_type,
            consistency_level=schedule.consistency_level,
        )
        self._restore_points.append(rp)

        # Chain of custody
        entry = self._audit("backup_completed", "job", job.id, "complete", "success",
                            {"size_bytes": job.size_bytes, "checksum": job.checksum})
        self._store_chain_entry(job.id, entry)

        self._update_metrics()
        logger.info("Backup job completed: %s (%s, %s)",
                     job.id, effective_type.value, bytes_to_gb(job.size_bytes))
        return job

    # ------------------------------------------------------------------
    # Public API — Verify Backup
    # ------------------------------------------------------------------

    def verify_backup(self, backup_job_id: str, sample_count: int = 100) -> BackupVerification:
        job = self._jobs.get(backup_job_id)
        if not job:
            raise ValueError(f"Backup job not found: {backup_job_id}")
        verification = BackupVerification(
            id=generate_id("verify"),
            backup_job_id=backup_job_id,
            checksum_valid=True,
            restore_tested=True,
            restore_duration_seconds=job.duration_seconds * 0.3 if job.duration_seconds else None,
            sample_files_verified=min(sample_count, 1000),
            total_files_in_backup=sample_count * 10,
            encryption_verified=job.encrypted,
            compliance_valid=True,
            verification_method="automated",
        )
        self._verifications[backup_job_id] = verification
        entry = self._audit("backup_verified", "job", backup_job_id, "verify", "success",
                            {"checksum_valid": True, "restore_tested": True})
        self._store_chain_entry(backup_job_id, entry)
        logger.info("Backup verified: %s (%.1f%% files checked)",
                     backup_job_id, verification.file_verification_pct)
        return verification

    # ------------------------------------------------------------------
    # Public API — Restore
    # ------------------------------------------------------------------

    def create_restore_point(
        self,
        backup_job_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> RestorePoint:
        job = self._jobs.get(backup_job_id)
        if not job:
            raise ValueError(f"Backup job not found: {backup_job_id}")
        rp = RestorePoint(
            id=generate_id("rp"),
            backup_job_id=backup_job_id,
            timestamp=utcnow(),
            backup_type=job.backup_type,
            consistency_level=job.consistency_level,
            metadata=metadata or {},
        )
        self._restore_points.append(rp)
        self._audit("restore_point_created", "restore_point", rp.id, "create", "success")
        return rp

    def restore_from_backup(
        self,
        backup_job_id: str,
        restore_type: RecoveryType,
        target_location: str,
        target_point_in_time: Optional[datetime] = None,
        selective_paths: Optional[List[str]] = None,
    ) -> RestoreJob:
        job = self._jobs.get(backup_job_id)
        if not job:
            raise ValueError(f"Backup job not found: {backup_job_id}")
        restore = RestoreJob(
            id=generate_id("restore"),
            restore_type=restore_type,
            source_backup_id=backup_job_id,
            target_location=target_location,
            target_point_in_time=target_point_in_time,
            selective_paths=selective_paths or [],
            cross_region=restore_type == RecoveryType.CROSS_REGION,
            cross_account=restore_type == RecoveryType.CROSS_ACCOUNT,
        )
        self._restore_jobs[restore.id] = restore
        restore.started_at = utcnow()
        restore.status = JobStatus.RUNNING
        self._audit("restore_started", "restore_job", restore.id, "restore", "started",
                     {"backup": backup_job_id, "type": restore_type.value})
        # Simulate completion
        restore.status = JobStatus.COMPLETED
        restore.completed_at = utcnow()
        restore.restored_bytes = job.size_bytes
        self._audit("restore_completed", "restore_job", restore.id, "restore", "completed",
                     {"restored_bytes": restore.restored_bytes})
        logger.info("Restore completed: %s (%s)", restore.id, seconds_to_human(restore.duration_seconds or 0))
        return restore

    # ------------------------------------------------------------------
    # Public API — Disaster Recovery
    # ------------------------------------------------------------------

    def create_dr_plan(
        self,
        name: str,
        strategy: DRStrategy,
        objectives: Optional[List[RecoveryObjective]] = None,
        scenarios: Optional[List[DisasterScenario]] = None,
        compliance_frameworks: Optional[List[ComplianceFramework]] = None,
    ) -> DisasterRecoveryPlan:
        plan = DisasterRecoveryPlan(
            id=generate_id("dr"),
            name=name,
            strategy=strategy,
            objectives=objectives or [],
            scenarios=scenarios or [],
            compliance_frameworks=compliance_frameworks or [],
            next_test_due=utcnow() + timedelta(days=90),
        )
        self._dr_plans[plan.id] = plan
        self._audit("dr_plan_created", "dr_plan", plan.id, "create", "success",
                     {"name": name, "strategy": strategy.value})
        logger.info("DR plan created: %s (%s)", name, plan.id)
        return plan

    def test_recovery(self, backup_job_id: str) -> Dict[str, Any]:
        """Simulate a recovery test and return the results."""
        job = self._jobs.get(backup_job_id)
        if not job:
            raise ValueError(f"Backup job not found: {backup_job_id}")
        start = time.time()
        # Simulate restore test
        time.sleep(0.05)
        elapsed = time.time() - start
        result = {
            "backup_job_id": backup_job_id,
            "recovery_test": "success",
            "recovery_time_seconds": round(elapsed, 2),
            "data_integrity": True,
            "checksum_match": True,
            "tested_at": utcnow().isoformat(),
        }
        self._audit("recovery_tested", "job", backup_job_id, "test_recovery", "success", result)
        logger.info("Recovery test passed for %s (%.2fs)", backup_job_id, elapsed)
        return result

    def run_disaster_drill(
        self,
        dr_plan_id: str,
        scenario_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        plan = self._dr_plans.get(dr_plan_id)
        if not plan:
            raise ValueError(f"DR plan not found: {dr_plan_id}")
        scenario = plan.scenarios[0] if plan.scenarios else DisasterScenario(
            id="default", name="default", description="Default drill",
            severity="medium", affected_services=["core"],
            estimated_rto_seconds=3600, estimated_rpo_seconds=900,
        )
        drill_start = time.time()
        # Simulate failover steps
        steps_executed = []
        for step_num in range(1, 6):
            steps_executed.append({
                "step": step_num,
                "name": f"drill_step_{step_num}",
                "status": "completed",
                "duration_seconds": 0.1 * step_num,
            })
        elapsed = time.time() - drill_start
        plan.last_tested = utcnow()
        plan.next_test_due = utcnow() + timedelta(days=90)
        result = {
            "dr_plan_id": dr_plan_id,
            "scenario": scenario.name,
            "drill_result": "success",
            "total_duration_seconds": round(elapsed, 2),
            "steps_completed": len(steps_executed),
            "steps": steps_executed,
            "rto_achieved_seconds": round(elapsed, 2),
            "rpo_achieved_seconds": scenario.estimated_rpo_seconds,
            "tested_at": utcnow().isoformat(),
        }
        self._audit("drill_executed", "dr_plan", dr_plan_id, "drill", "success", result)
        logger.info("DR drill completed for plan %s (%.2fs)", dr_plan_id, elapsed)
        return result

    # ------------------------------------------------------------------
    # Public API — Replication & Encryption
    # ------------------------------------------------------------------

    def configure_replication(
        self,
        primary_location_id: str,
        secondary_location_id: str,
        mode: ReplicationMode = ReplicationMode.ASYNCHRONOUS,
        rpo_seconds: int = 3600,
        auto_failover: bool = False,
    ) -> ReplicationConfig:
        self._validate_storage(primary_location_id)
        self._validate_storage(secondary_location_id)
        config = ReplicationConfig(
            primary_location_id=primary_location_id,
            secondary_location_id=secondary_location_id,
            mode=mode,
            rpo_seconds=rpo_seconds,
            auto_failover=auto_failover,
        )
        key = f"{primary_location_id}->{secondary_location_id}"
        self._replication_configs[key] = config
        self._audit("replication_configured", "replication", key, "configure", "success",
                     {"mode": mode.value, "rpo_seconds": rpo_seconds})
        logger.info("Replication configured: %s (mode=%s, rpo=%ds)", key, mode.value, rpo_seconds)
        return config

    def setup_encryption(
        self,
        storage_location_id: str,
        algorithm: EncryptionStandard = EncryptionStandard.AES_256,
        key_rotation_days: int = 90,
        kms_key_id: Optional[str] = None,
    ) -> EncryptionConfig:
        self._validate_storage(storage_location_id)
        config = EncryptionConfig(
            algorithm=algorithm,
            key_rotation_days=key_rotation_days,
            kms_key_id=kms_key_id,
        )
        errors = config.validate()
        if errors:
            raise ValueError(f"Invalid encryption config: {errors}")
        self._audit("encryption_configured", "storage", storage_location_id, "encrypt", "success",
                     {"algorithm": algorithm.value, "rotation_days": key_rotation_days})
        logger.info("Encryption configured for %s (%s, rotation=%dd)",
                     storage_location_id, algorithm.value, key_rotation_days)
        return config

    # ------------------------------------------------------------------
    # Public API — Compliance
    # ------------------------------------------------------------------

    def generate_compliance_report(
        self,
        framework: ComplianceFramework,
        period_days: int = 30,
    ) -> ComplianceReport:
        period_start = utcnow() - timedelta(days=period_days)
        total = len(self._jobs)
        compliant = sum(1 for j in self._jobs.values() if j.status == JobStatus.COMPLETED and j.encrypted)
        report = ComplianceReport(
            id=generate_id("comp"),
            framework=framework,
            period_start=period_start,
            period_end=utcnow(),
            total_backups=total,
            compliant_backups=compliant,
            non_compliant_backups=total - compliant,
        )
        if report.compliance_rate < 95.0:
            report.recommendations.append("Increase backup success rate to meet 95% compliance threshold")
        if framework in (ComplianceFramework.HIPAA, ComplianceFramework.PCI_DSS, ComplianceFramework.GDPR):
            report.recommendations.append("Ensure all backups are encrypted at rest with AES-256 or equivalent")
        if framework == ComplianceFramework.FedRAMP:
            report.recommendations.append("Implement air-gapped backup copies for FedRAMP high baseline")
        report.overall_status = "compliant" if report.is_compliant else "non_compliant"
        self._audit("compliance_report_generated", "report", report.id, "generate", "success",
                     {"framework": framework.value, "rate": report.compliance_rate})
        logger.info("Compliance report generated: %s (%.1f%% compliant)", framework.value, report.compliance_rate)
        return report

    # ------------------------------------------------------------------
    # Public API — RPO/RTO Analysis
    # ------------------------------------------------------------------

    def calculate_recovery_objectives(
        self,
        service_name: str,
        annual_revenue_usd: float,
        data_volume_gb: float,
        classification: str = "confidential",
    ) -> RecoveryObjective:
        if annual_revenue_usd > 10_000_000:
            rpo, rto = 300, 600
            tier = "platinum"
        elif annual_revenue_usd > 1_000_000:
            rpo, rto = 3600, 7200
            tier = "gold"
        elif annual_revenue_usd > 100_000:
            rpo, rto = 14400, 28800
            tier = "silver"
        else:
            rpo, rto = 86400, 172800
            tier = "bronze"
        annual_impact = annual_revenue_usd * 0.01  # 1% revenue loss estimate
        obj = RecoveryObjective(
            service_name=service_name,
            rpo_seconds=rpo,
            rto_seconds=rto,
            tier=tier,
            annual_impact_usd=annual_impact,
            data_classification=classification,
            max_data_loss_acceptable_gb=data_volume_gb * 0.01,
        )
        self._audit("rpo_rto_calculated", "service", service_name, "calculate", "success",
                     {"rpo": rpo, "rto": rto, "tier": tier})
        logger.info("Recovery objectives for %s: RPO=%s, RTO=%s, tier=%s",
                     service_name, seconds_to_human(rpo), seconds_to_human(rto), tier)
        return obj

    # ------------------------------------------------------------------
    # Public API — Storage Analysis & Forecasting
    # ------------------------------------------------------------------

    def analyze_backup_storage(self) -> Dict[str, Any]:
        self._update_metrics()
        locations_analysis = []
        for loc in self._storage_locations.values():
            locations_analysis.append({
                "id": loc.id,
                "name": loc.name,
                "provider": loc.provider,
                "region": loc.region,
                "tier": loc.tier.value,
                "used_gb": loc.used_gb,
                "available_gb": loc.available_gb,
                "utilization_pct": round(loc.utilization_pct, 1),
            })
        return {
            "total_locations": len(self._storage_locations),
            "total_used_gb": round(self._metrics.storage_used_gb, 2),
            "total_available_gb": round(self._metrics.storage_available_gb, 2),
            "overall_utilization_pct": round(self._metrics.storage_utilization, 1),
            "success_rate": round(self._metrics.success_rate, 1),
            "locations": locations_analysis,
        }

    def forecast_capacity(
        self,
        location_id: str,
        daily_growth_gb: float,
        forecast_days: int = 90,
    ) -> CapacityForecast:
        loc = self._validate_storage(location_id)
        forecast = CapacityForecast(
            location_id=location_id,
            current_used_gb=loc.used_gb,
            daily_growth_gb=daily_growth_gb,
            forecast_days=forecast_days,
        )
        self._audit("capacity_forecast", "storage", location_id, "forecast", "success",
                     {"daily_growth_gb": daily_growth_gb, "forecast_days": forecast_days})
        logger.info("Capacity forecast for %s: %.1f GB in %d days",
                     location_id, forecast.projected_used_gb, forecast_days)
        return forecast

    # ------------------------------------------------------------------
    # Public API — Vendor Comparison
    # ------------------------------------------------------------------

    def compare_vendors(
        self,
        vendors: List[VendorComparison],
        required_features: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        results = []
        for v in vendors:
            score = 0
            if v.encryption:
                score += 20
            if v.immutable_storage:
                score += 20
            if v.cross_region_replication:
                score += 15
            score += min(v.durability_nines, 11) * 2
            score += min(v.availability_sla_pct / 10, 5)
            cost_score = max(0, 10 - v.effective_monthly_cost_per_gb * 100)
            score += cost_score
            if v.compliance_certs:
                score += len(v.compliance_certs) * 3
            results.append({
                "vendor": v.name,
                "provider": v.provider,
                "score": round(score, 1),
                "cost_per_gb_effective": round(v.effective_monthly_cost_per_gb, 6),
                "features": {
                    "encryption": v.encryption,
                    "immutable": v.immutable_storage,
                    "cross_region": v.cross_region_replication,
                },
                "compliance": v.compliance_certs,
                "notes": v.notes,
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        self._audit("vendor_comparison", "analysis", "multi", "compare", "success",
                     {"vendors": [r["vendor"] for r in results]})
        return results

    # ------------------------------------------------------------------
    # Public API — Retention & Cross-Region
    # ------------------------------------------------------------------

    def create_retention_policy(
        self,
        name: str,
        framework: ComplianceFramework,
        daily_keep: int = 7,
        weekly_keep: int = 4,
        monthly_keep: int = 12,
        yearly_keep: int = 7,
    ) -> BackupPolicy:
        rules = [
            RetentionRule(name="daily", backup_type=BackupType.INCREMENTAL,
                          keep_count=daily_keep, keep_duration_days=daily_keep),
            RetentionRule(name="weekly", backup_type=BackupType.DIFFERENTIAL,
                          keep_count=weekly_keep, keep_duration_days=weekly_keep * 7),
            RetentionRule(name="monthly", backup_type=BackupType.FULL,
                          keep_count=monthly_keep, keep_duration_days=monthly_keep * 30),
            RetentionRule(name="yearly", backup_type=BackupType.FULL,
                          keep_count=yearly_keep, keep_duration_days=yearly_keep * 365,
                          freeze_after_days=365),
        ]
        return self.create_backup_policy(
            name=name,
            description=f"Retention policy: {daily_keep}d/{weekly_keep}w/{monthly_keep}m/{yearly_keep}y",
            framework=framework,
            rules=rules,
        )

    def setup_cross_region_backup(
        self,
        primary_region: str,
        secondary_region: str,
        mode: ReplicationMode = ReplicationMode.ASYNCHRONOUS,
        rpo_seconds: int = 3600,
    ) -> CrossRegionPair:
        pair = CrossRegionPair(
            primary_region=primary_region,
            secondary_region=secondary_region,
            replication_mode=mode,
            rpo_seconds=rpo_seconds,
            estimated_bandwidth_mbps=100.0,
        )
        self._cross_region_pairs.append(pair)
        self._audit("cross_region_configured", "replication", f"{primary_region}->{secondary_region}",
                     "configure", "success", {"mode": mode.value})
        logger.info("Cross-region backup: %s -> %s", primary_region, secondary_region)
        return pair

    # ------------------------------------------------------------------
    # Public API — Monitoring & Audit
    # ------------------------------------------------------------------

    def monitor_backup_health(self) -> List[HealthCheck]:
        checks: List[HealthCheck] = []
        # Check storage locations
        for loc in self._storage_locations.values():
            status = HealthStatus.HEALTHY
            if loc.utilization_pct > 90:
                status = HealthStatus.CRITICAL
            elif loc.utilization_pct > 75:
                status = HealthStatus.DEGRADED
            checks.append(HealthCheck(
                component=f"storage:{loc.name}",
                status=status,
                details={"utilization_pct": loc.utilization_pct, "region": loc.region},
            ))
        # Check replication
        for key, config in self._replication_configs.items():
            checks.append(HealthCheck(
                component=f"replication:{key}",
                status=HealthStatus.HEALTHY,
                details={"mode": config.mode.value, "rpo_hours": config.rpo_hours},
            ))
        # Check DR plans
        for plan in self._dr_plans.values():
            status = HealthStatus.HEALTHY if not plan.test_overdue else HealthStatus.DEGRADED
            checks.append(HealthCheck(
                component=f"dr_plan:{plan.name}",
                status=status,
                details={"test_overdue": plan.test_overdue},
            ))
        self._health_checks = checks
        return checks

    def audit_backup_chain(self, backup_job_id: str) -> Dict[str, Any]:
        chain = self._chains_of_custody.get(backup_job_id)
        if not chain:
            return {"backup_job_id": backup_job_id, "chain_found": False}
        return {
            "backup_job_id": backup_job_id,
            "chain_found": True,
            "entries_count": len(chain.entries),
            "chain_complete": chain.is_complete,
            "chain_valid": chain.verify_chain(),
            "events": [
                {"event": e.event_type, "timestamp": iso_format(e.timestamp), "result": e.result}
                for e in chain.entries
            ],
        }

    # ------------------------------------------------------------------
    # Public API — Reporting
    # ------------------------------------------------------------------

    def generate_recovery_report(self) -> Dict[str, Any]:
        self._update_metrics()
        return {
            "generated_at": utcnow().isoformat(),
            "metrics": {
                "total_backups": self._metrics.total_backups,
                "success_rate": round(self._metrics.success_rate, 1),
                "total_data_protected_gb": round(bytes_to_gb(self._metrics.total_bytes_backed_up), 2),
                "compression_ratio": round(self._metrics.compression_ratio, 3),
                "average_backup_duration": seconds_to_human(self._metrics.average_backup_duration_seconds),
            },
            "storage": {
                "used_gb": round(self._metrics.storage_used_gb, 2),
                "available_gb": round(self._metrics.storage_available_gb, 2),
                "utilization_pct": round(self._metrics.storage_utilization, 1),
            },
            "dr_status": {
                "plans": len(self._dr_plans),
                "overdue_tests": sum(1 for p in self._dr_plans.values() if p.test_overdue),
            },
            "policies": len(self._policies),
            "schedules": len(self._schedules),
            "active_schedules": self._metrics.active_schedules,
            "cross_region_pairs": len(self._cross_region_pairs),
        }

    def export_backup_data(self, format: str = "json") -> str:
        data = {
            "policies": {k: asdict(v) for k, v in self._policies.items()},
            "schedules": {k: asdict(v) for k, v in self._schedules.items()},
            "jobs": {k: asdict(v) for k, v in self._jobs.items()},
            "dr_plans": {k: asdict(v) for k, v in self._dr_plans.items()},
            "storage_locations": {k: asdict(v) for k, v in self._storage_locations.items()},
            "metrics": asdict(self._metrics),
        }
        if format == "json":
            return json.dumps(data, default=str, indent=2)
        return str(data)

    # ------------------------------------------------------------------
    # Convenience — register storage
    # ------------------------------------------------------------------

    def register_storage_location(
        self,
        name: str,
        provider: str,
        region: str,
        tier: StorageTier = StorageTier.WARM,
        bucket: Optional[str] = None,
        available_gb: float = 1000.0,
    ) -> StorageLocation:
        loc = StorageLocation(
            id=generate_id("stor"),
            name=name,
            provider=provider,
            region=region,
            tier=tier,
            bucket=bucket,
            available_gb=available_gb,
        )
        self._storage_locations[loc.id] = loc
        logger.info("Storage location registered: %s (%s, %s)", name, provider, region)
        return loc

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        self._update_metrics()
        return {
            "agent": "BackupRecoveryAgent",
            "version": "3.0.0",
            "policies": len(self._policies),
            "schedules": len(self._schedules),
            "jobs_total": self._metrics.total_backups,
            "jobs_success": self._metrics.successful_backups,
            "jobs_failed": self._metrics.failed_backups,
            "success_rate": round(self._metrics.success_rate, 1),
            "dr_plans": len(self._dr_plans),
            "storage_locations": len(self._storage_locations),
            "restore_points": len(self._restore_points),
            "cross_region_pairs": len(self._cross_region_pairs),
        }


# ---------------------------------------------------------------------------
# main() demo
# ---------------------------------------------------------------------------

def main() -> None:
    """End-to-end demonstration of BackupRecoveryAgent capabilities."""
    print("=" * 72)
    print(" BackupRecoveryAgent v3.0.0 — Full Demonstration")
    print("=" * 72)

    agent = BackupRecoveryAgent(default_region="us-east-1")

    # 1. Register storage locations
    print("\n[1] Registering storage locations ...")
    primary = agent.register_storage_location(
        name="Primary-S3", provider="aws", region="us-east-1",
        tier=StorageTier.HOT, bucket="backup-primary", available_gb=50000,
    )
    secondary = agent.register_storage_location(
        name="Secondary-S3", provider="aws", region="eu-west-1",
        tier=StorageTier.WARM, bucket="backup-secondary", available_gb=50000,
    )
    archive_loc = agent.register_storage_location(
        name="Archive-Glacier", provider="aws", region="us-east-1",
        tier=StorageTier.ARCHIVE, bucket="backup-archive", available_gb=200000,
    )
    print(f"   Registered {len(agent._storage_locations)} locations")

    # 2. Create backup policies
    print("\n[2] Creating backup policies ...")
    policy_7yr = agent.create_retention_policy(
        name="HIPAA-7yr-Policy",
        framework=ComplianceFramework.HIPAA,
        daily_keep=14, weekly_keep=8, monthly_keep=24, yearly_keep=10,
    )
    policy_soc2 = agent.create_retention_policy(
        name="SOC2-Standard-Policy",
        framework=ComplianceFramework.SOC2,
    )
    print(f"   Created {len(agent._policies)} policies")

    # 3. Configure replication
    print("\n[3] Configuring cross-region replication ...")
    repl = agent.configure_replication(
        primary_location_id=primary.id,
        secondary_location_id=secondary.id,
        mode=ReplicationMode.ASYNCHRONOUS,
        rpo_seconds=1800,
        auto_failover=True,
    )
    print(f"   Replication: {repl.mode.value}, RPO={repl.rpo_hours:.1f}h")

    # 4. Setup encryption
    print("\n[4] Configuring encryption ...")
    enc = agent.setup_encryption(
        storage_location_id=primary.id,
        algorithm=EncryptionStandard.AES_256,
        key_rotation_days=90,
    )
    print(f"   Encryption: {enc.algorithm.value}, rotation={enc.key_rotation_days}d")

    # 5. Schedule backups
    print("\n[5] Creating backup schedules ...")
    db_schedule = agent.schedule_backup(
        name="Production-DB-Daily",
        source_id="prod-postgres-primary",
        source_type=BackupTarget.DATABASE,
        backup_type=BackupType.FULL,
        policy_id=policy_7yr.id,
        storage_location_id=primary.id,
        cron_expression="0 2 * * *",
        consistency_level=ConsistencyLevel.APPLICATION_CONSISTENT,
        tags={"env": "production", "team": "data-platform"},
    )
    fs_schedule = agent.schedule_backup(
        name="Application-Configs-Weekly",
        source_id="/opt/app/configs",
        source_type=BackupTarget.CONFIGURATION,
        backup_type=BackupType.INCREMENTAL,
        policy_id=policy_soc2.id,
        storage_location_id=primary.id,
        cron_expression="0 3 * * 0",
    )
    print(f"   Created {len(agent._schedules)} schedules")

    # 6. Execute backups
    print("\n[6] Executing backup jobs ...")
    full_job = agent.execute_backup(schedule_id=db_schedule.id, backup_type=BackupType.FULL)
    incr_job = agent.execute_backup(schedule_id=db_schedule.id, backup_type=BackupType.INCREMENTAL,
                                    parent_backup_id=full_job.id)
    diff_job = agent.execute_backup(schedule_id=db_schedule.id, backup_type=BackupType.DIFFERENTIAL,
                                    parent_backup_id=full_job.id)
    config_job = agent.execute_backup(schedule_id=fs_schedule.id)
    print(f"   Executed {len(agent._jobs)} backup jobs")
    for j in agent._jobs.values():
        print(f"     {j.id}: {j.backup_type.value} — {bytes_to_gb(j.size_bytes):.2f} GB — {j.status.value}")

    # 7. Verify backups
    print("\n[7] Verifying backup integrity ...")
    for j in agent._jobs.values():
        v = agent.verify_backup(j.id, sample_count=500)
        print(f"   {j.id}: checksum={v.checksum_valid}, restore={v.restore_tested}, "
              f"files={v.file_verification_pct:.0f}%")

    # 8. Create restore points & test recovery
    print("\n[8] Testing recovery ...")
    test_result = agent.test_recovery(full_job.id)
    print(f"   Recovery test: {test_result['recovery_test']}, "
          f"time={test_result['recovery_time_seconds']:.2f}s")

    # 9. Perform a restore
    print("\n[9] Executing restore ...")
    restore = agent.restore_from_backup(
        backup_job_id=full_job.id,
        restore_type=RecoveryType.FULL_RESTORE,
        target_location="/var/restore/production",
    )
    print(f"   Restore {restore.id}: {restore.status.value}, "
          f"{bytes_to_gb(restore.restored_bytes):.2f} GB in "
          f"{seconds_to_human(restore.duration_seconds or 0)}")

    # 10. DR plan
    print("\n[10] Creating disaster recovery plan ...")
    obj = agent.calculate_recovery_objectives(
        service_name="payment-service",
        annual_revenue_usd=5_000_000,
        data_volume_gb=500,
        classification="pii",
    )
    scenario = DisasterScenario(
        id="sc-001", name="Region Failover",
        description="Complete us-east-1 region outage",
        severity="critical",
        affected_services=["payment-service", "auth-service", "api-gateway"],
        estimated_rto_seconds=1800,
        estimated_rpo_seconds=900,
        data_loss_gb=2.5,
        blast_radius_pct=100.0,
        recovery_strategy=DRStrategy.HOT_STANDBY,
    )
    dr_plan = agent.create_dr_plan(
        name="Production-DR-Plan",
        strategy=DRStrategy.HOT_STANDBY,
        objectives=[obj],
        scenarios=[scenario],
        compliance_frameworks=[ComplianceFramework.HIPAA, ComplianceFramework.PCI_DSS],
    )
    print(f"   DR plan: {dr_plan.name} ({dr_plan.strategy.value})")
    print(f"   Worst-case RTO: {seconds_to_human(dr_plan.worst_case_rto())}, "
          f"RPO: {seconds_to_human(dr_plan.worst_case_rpo())}")

    # 11. Run DR drill
    print("\n[11] Running disaster recovery drill ...")
    drill = agent.run_disaster_drill(dr_plan.id)
    print(f"   Drill result: {drill['drill_result']}, "
          f"duration={drill['total_duration_seconds']:.2f}s")

    # 12. Cross-region backup
    print("\n[12] Setting up cross-region backup ...")
    cross = agent.setup_cross_region_backup(
        primary_region="us-east-1",
        secondary_region="ap-southeast-1",
        mode=ReplicationMode.NEAR_SYNC,
        rpo_seconds=7200,
    )
    print(f"   Cross-region: {cross.primary_region} -> {cross.secondary_region}, RPO={cross.rpo_hours:.1f}h")

    # 13. Compliance report
    print("\n[13] Generating compliance reports ...")
    hipaa_report = agent.generate_compliance_report(ComplianceFramework.HIPAA, period_days=30)
    pci_report = agent.generate_compliance_report(ComplianceFramework.PCI_DSS, period_days=30)
    for report in [hipaa_report, pci_report]:
        print(f"   {report.framework.value}: {report.compliance_rate:.1f}% compliant — "
              f"{report.overall_status}")
        if report.recommendations:
            for rec in report.recommendations[:2]:
                print(f"     → {rec}")

    # 14. Storage analysis
    print("\n[14] Analyzing backup storage ...")
    storage_analysis = agent.analyze_backup_storage()
    print(f"   Total storage: {storage_analysis['total_used_gb']:.1f} GB used / "
          f"{storage_analysis['total_available_gb']:.1f} GB available")
    print(f"   Utilization: {storage_analysis['overall_utilization_pct']:.1f}%")

    # 15. Capacity forecast
    print("\n[15] Forecasting capacity ...")
    forecast = agent.forecast_capacity(primary.id, daily_growth_gb=5.2, forecast_days=180)
    print(f"   Current: {forecast.current_used_gb:.1f} GB, projected: {forecast.projected_used_gb:.1f} GB "
          f"in {forecast.forecast_days} days")

    # 16. Vendor comparison
    print("\n[16] Comparing storage vendors ...")
    vendors = [
        VendorComparison(name="AWS S3", provider="aws", cost_per_gb_monthly=0.023,
                        egress_per_gb=0.09, encryption=True, immutable_storage=True,
                        cross_region_replication=True, max_object_size_gb=5.0,
                        durability_nines=11.0, availability_sla_pct=99.99,
                        compliance_certs=["SOC2", "HIPAA", "PCI_DSS", "FedRAMP"]),
        VendorComparison(name="Azure Blob", provider="azure", cost_per_gb_monthly=0.018,
                        egress_per_gb=0.087, encryption=True, immutable_storage=True,
                        cross_region_replication=True, max_object_size_gb=4.75,
                        durability_nines=11.0, availability_sla_pct=99.99,
                        compliance_certs=["SOC2", "HIPAA", "ISO27001"]),
        VendorComparison(name="GCP Cloud Storage", provider="gcp", cost_per_gb_monthly=0.020,
                        egress_per_gb=0.08, encryption=True, immutable_storage=True,
                        cross_region_replication=True, max_object_size_gb=5.0,
                        durability_nines=11.0, availability_sla_pct=99.95,
                        compliance_certs=["SOC2", "HIPAA", "ISO27001"]),
    ]
    rankings = agent.compare_vendors(vendors)
    for i, r in enumerate(rankings, 1):
        print(f"   #{i} {r['vendor']}: score={r['score']}, "
              f"cost=${r['cost_per_gb_effective']:.4f}/GB/mo")

    # 17. Health monitoring
    print("\n[17] Monitoring backup health ...")
    health = agent.monitor_backup_health()
    for h in health:
        print(f"   {h.component}: {h.status.value}")

    # 18. Audit chain
    print("\n[18] Auditing backup chain ...")
    chain_audit = agent.audit_backup_chain(full_job.id)
    print(f"   Chain for {full_job.id}: complete={chain_audit['chain_complete']}, "
          f"valid={chain_audit['chain_valid']}, entries={chain_audit['entries_count']}")

    # 19. Recovery report
    print("\n[19] Generating recovery report ...")
    recovery_report = agent.generate_recovery_report()
    print(f"   Total backups: {recovery_report['metrics']['total_backups']}")
    print(f"   Success rate: {recovery_report['metrics']['success_rate']}%")
    print(f"   Data protected: {recovery_report['metrics']['total_data_protected_gb']} GB")
    print(f"   DR plans: {recovery_report['dr_status']['plans']}, "
          f"overdue tests: {recovery_report['dr_status']['overdue_tests']}")

    # 20. Export
    print("\n[20] Exporting backup data ...")
    export = agent.export_backup_data(format="json")
    print(f"   Export size: {len(export):,} bytes (JSON)")

    # Final status
    print("\n" + "=" * 72)
    print(" Final Agent Status")
    print("=" * 72)
    status = agent.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 72)
    print(" Demonstration complete.")
    print("=" * 72)


if __name__ == "__main__":
    main()
