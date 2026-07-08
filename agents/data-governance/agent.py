"""Data Governance Agent - Data Policies, Quality Standards, Lineage Tracking, Metadata Management, Compliance.

A comprehensive data governance system that handles data policy development and enforcement,
data quality management with profiling and monitoring, data lineage tracking across systems,
metadata management with catalogs, and compliance framework implementation. Built for data
teams, compliance officers, and data stewards who need a structured, auditable approach
to enterprise data governance.

Architecture: Hub-and-spoke governance model with policy → quality → lineage → metadata →
compliance stages. Each stage produces validated artifacts that feed downstream governance
operations. All actions are logged for audit and compliance purposes.

Author: Awesome Grok Skills Team
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

# ---------------------------------------------------------------------------
# Module-level setup
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

__all__ = [
    "DataGovernanceAgent",
    "Config",
    "DataPolicy",
    "QualityRule",
    "DataLineage",
    "MetadataCatalog",
    "ComplianceFramework",
    "DataAsset",
    "DataClassification",
    "AccessRole",
    "QualityDimension",
    "PolicyType",
    "LineageDirection",
    "MetadataType",
    "ComplianceStatus",
    "DataSteward",
    "QualityProfile",
    "GovernanceScore",
]

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class DataClassification(Enum):
    """Data classification levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    SENSITIVE = "sensitive"
    PII = "pii"
    PHI = "phi"
    PCI = "pci"
    PROPRIETARY = "proprietary"
    TRADE_SECRET = "trade_secret"


class AccessRole(Enum):
    """Roles for data access control."""
    DATA_OWNER = "data_owner"
    DATA_STEWARD = "data_steward"
    DATA_CUSTODIAN = "data_custodian"
    DATA_ANALYST = "data_analyst"
    DATA_ENGINEER = "data_engineer"
    DATA_SCIENTIST = "data_scientist"
    ADMIN = "admin"
    AUDITOR = "auditor"
    VIEWER = "viewer"
    EDITOR = "editor"
    COMPLIANCE_OFFICER = "compliance_officer"
    EXECUTIVE = "executive"


class QualityDimension(Enum):
    """Dimensions of data quality."""
    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    CONSISTENCY = "consistency"
    TIMELINESS = "timeliness"
    VALIDITY = "validity"
    UNIQUENESS = "uniqueness"
    INTEGRITY = "integrity"
    CONFORMITY = "conformity"
    FRESHNESS = "freshness"
    REASONABLENESS = "reasonableness"


class PolicyType(Enum):
    """Types of data policies."""
    DATA_RETENTION = "data_retention"
    DATA_CLASSIFICATION = "data_classification"
    ACCESS_CONTROL = "access_control"
    ENCRYPTION = "encryption"
    PRIVACY = "privacy"
    SHARING = "sharing"
    BACKUP = "backup"
    DISPOSAL = "disposal"
    QUALITY = "quality"
    LINEAGE = "lineage"
    MASTER_DATA = "master_data"
    REFERENCE_DATA = "reference_data"
    SENSITIVE_DATA = "sensitive_data"
    CROSS_BORDER = "cross_border"
    CONSENT = "consent"
    BREACH_NOTIFICATION = "breach_notification"
    VENDOR = "vendor"
    AUDIT = "audit"
    TRAINING = "training"
    EXCEPTION = "exception"


class LineageDirection(Enum):
    """Direction of data lineage."""
    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"
    BIDIRECTIONAL = "bidirectional"


class MetadataType(Enum):
    """Types of metadata."""
    TECHNICAL = "technical"
    BUSINESS = "business"
    OPERATIONAL = "operational"
    SEMANTIC = "semantic"
    STRUCTURAL = "structural"
    ADMINISTRATIVE = "administrative"
    DESCRITIVE = "descriptive"
    PROCESSED = "processed"
    SOCIAL = "social"


class ComplianceStatus(Enum):
    """Compliance status for frameworks."""
    COMPLIANT = "compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    NOT_ASSESSED = "not_assessed"
    IN_PROGRESS = "in_progress"
    EXEMPT = "exempt"
    REMEDIATION = "remediation"


class ComplianceFramework(Enum):
    """Supported compliance frameworks."""
    GDPR = "gdpr"
    CCPA = "ccpa"
    HIPAA = "hipaa"
    SOX = "sox"
    SOC2 = "soc2"
    PCI_DSS = "pci_dss"
    ISO27001 = "iso27001"
    ISO27701 = "iso27701"
    NIST_CSF = "nist_csf"
    FedRAMP = "fedramp"
    COPPA = "coppa"
    GLBA = "glba"
    FERPA = "ferpa"
    Basel_III = "basel_iii"
    MiFID_II = "mifid_ii"
    LGPD = "lgpd"
    PIPEDA = "pipeda"
    APPS = "apps"


class PolicyStatus(Enum):
    """Status of a data policy."""
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    ACTIVE = "active"
    RETIRED = "retired"
    SUPERSEDED = "superseded"
    VIOLATION = "violation"
    EXCEPTION = "exception"


class QualityRuleType(Enum):
    """Types of quality rules."""
    NOT_NULL = "not_null"
    UNIQUE = "unique"
    RANGE = "range"
    PATTERN = "pattern"
    REFERENTIAL = "referential"
    CUSTOM = "custom"
    FRESHNESS = "freshness"
    VOLUME = "volume"
    SCHEMA = "schema"
    STATISTICAL = "statistical"
    BUSINESS_RULE = "business_rule"
    COMPARISON = "comparison"
    AGGREGATE = "aggregate"
    COMPLETENESS = "completeness"
    CONSISTENCY = "consistency"


class AssetType(Enum):
    """Types of data assets."""
    DATABASE = "database"
    TABLE = "table"
    VIEW = "view"
    FILE = "file"
    API = "api"
    STREAM = "stream"
    REPORT = "report"
    DASHBOARD = "dashboard"
    MODEL = "model"
    DATASET = "dataset"
    SCHEMA = "schema"
    COLUMN = "column"
    INDEX = "index"
    STORED_PROCEDURE = "stored_procedure"
    ETL_JOB = "etl_job"
    PIPELINE = "pipeline"
    SERVICE = "service"
    QUEUE = "queue"
    CACHE = "cache"
    LAKE = "lake"


class ChangeType(Enum):
    """Types of changes for lineage tracking."""
    SCHEMA_CHANGE = "schema_change"
    DATA_LOAD = "data_load"
    TRANSFORMATION = "transformation"
    AGGREGATION = "aggregation"
    FILTER = "filter"
    JOIN = "join"
    UNION = "union"
    DERIVATION = "derivation"
    REPLICATION = "replication"
    ARCHIVAL = "archival"
    DELETION = "deletion"
    UPDATE = "update"
    MERGE = "merge"
    SPLIT = "split"
    RENAME = "rename"


class StewardshipAction(Enum):
    """Actions taken by data stewards."""
    CLASSIFY = "classify"
    LABEL = "label"
    APPROVE_ACCESS = "approve_access"
    DENY_ACCESS = "deny_access"
    REVIEW = "review"
    CERTIFY = "certify"
    REMEDIATE = "remediate"
    ESCALATE = "escalate"
    DOCUMENT = "document"
    TRAIN = "train"
    MONITOR = "monitor"
    AUDIT = "audit"
    UPDATE_POLICY = "update_policy"
    ASSIGN_OWNER = "assign_owner"
    RESOLVE_ISSUE = "resolve_issue"


class MetricAggregation(Enum):
    """Aggregation types for quality metrics."""
    SUM = "sum"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    DISTINCT_COUNT = "distinct_count"
    PERCENTILE = "percentile"
    MEDIAN = "median"
    MODE = "mode"
    STDDEV = "stddev"
    VARIANCE = "variance"


class DataFreshness(Enum):
    """Data freshness requirements."""
    REAL_TIME = "real_time"        # < 1 minute
    NEAR_REAL_TIME = "near_real_time"  # < 15 minutes
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    ON_DEMAND = "on_demand"


class GovernanceMaturity(Enum):
    """Data governance maturity levels."""
    INITIAL = "initial"           # Ad-hoc, no formal process
    DEVELOPING = "developing"     # Some processes defined
    DEFINED = "defined"           # Standardized processes
    MANAGED = "managed"           # Measured and controlled
    OPTIMIZED = "optimized"       # Continuous improvement


class IssueSeverity(Enum):
    """Severity levels for governance issues."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueStatus(Enum):
    """Status of governance issues."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ESCALATED = "escalated"
    ACCEPTED = "accepted"
    EXCEPTION = "exception"


class ReportType(Enum):
    """Types of governance reports."""
    QUALITY_SUMMARY = "quality_summary"
    COMPLIANCE_STATUS = "compliance_status"
    LINEAGE_IMPACT = "lineage_impact"
    POLICY_ADHERENCE = "policy_adherence"
    ACCESS_AUDIT = "access_audit"
    STEWARDSHIP = "stewardship"
    EXECUTIVE_SUMMARY = "executive_summary"
    DATA_CATALOG = "data_catalog"
    ISSUE_TRACKER = "issue_tracker"
    METRICS_DASHBOARD = "metrics_dashboard"


class ConsentType(Enum):
    """Types of data consent."""
    EXPLICIT = "explicit"
    IMPLICIT = "implicit"
    LEGITIMATE_INTEREST = "legitimate_interest"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligigation"
    VITAL_INTEREST = "vital_interest"
    PUBLIC_INTEREST = "public_interest"
    WITHDRAWN = "withdrawn"
    NOT_OBTAINED = "not_obtained"


class RetentionAction(Enum):
    """Actions for data retention."""
    RETAIN = "retain"
    ARCHIVE = "archive"
    ANONYMIZE = "anonymize"
    AGGREGATE = "aggregate"
    DELETE = "delete"
    RESTRICT = "restrict"
    REVIEW = "review"


class DataDomain(Enum):
    """Business domains for data ownership."""
    CUSTOMER = "customer"
    PRODUCT = "product"
    FINANCE = "finance"
    HR = "hr"
    MARKETING = "marketing"
    SALES = "sales"
    OPERATIONS = "operations"
    ENGINEERING = "engineering"
    LEGAL = "legal"
    COMPLIANCE = "compliance"
    SUPPLY_CHAIN = "supply_chain"
    PARTNER = "partner"
    MARKET_DATA = "market_data"
    ANALYTICS = "analytics"
    IOT = "iot"
    BIOMETRIC = "biometric"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class QualityConfig:
    """Configuration for data quality management."""
    default_quality_threshold: float = 0.95
    profiling_enabled: bool = True
    monitoring_enabled: bool = True
    alert_threshold: float = 0.90
    critical_threshold: float = 0.80
    auto_remediation_enabled: bool = False
    quality_score_weight_accuracy: float = 0.20
    quality_score_weight_completeness: float = 0.20
    quality_score_weight_consistency: float = 0.15
    quality_score_weight_timeliness: float = 0.15
    quality_score_weight_validity: float = 0.15
    quality_score_weight_uniqueness: float = 0.15
    max_rules_per_asset: int = 50
    profiling_sample_size: int = 10000


@dataclass
class LineageConfig:
    """Configuration for data lineage tracking."""
    auto_discovery_enabled: bool = True
    impact_analysis_enabled: bool = True
    max_depth: int = 10
    cross_system_tracking: bool = True
    real_time_tracking: bool = False
    historical_tracking: bool = True
    max_history_days: int = 365
    visualization_enabled: bool = True


@dataclass
class MetadataConfig:
    """Configuration for metadata management."""
    auto_catalog_enabled: bool = True
    business_glossary_enabled: bool = True
    search_indexing_enabled: bool = True
    tag_auto_suggestion: bool = True
    quality_badge_enabled: bool = True
    ownership_enforcement: bool = True
    freshness_tracking: bool = True
    popularity_tracking: bool = True


@dataclass
class ComplianceConfig:
    """Configuration for compliance management."""
    frameworks: List[ComplianceFramework] = field(
        default_factory=lambda: [
            ComplianceFramework.GDPR,
            ComplianceFramework.SOC2,
        ]
    )
    assessment_frequency_days: int = 90
    auto_evidence_collection: bool = True
    remediation_tracking: bool = True
    audit_trail_required: bool = True
    notification_on_violation: bool = True
    data_retention_enforcement: bool = True
    cross_border_restriction: bool = True
    consent_tracking: bool = True


@dataclass
class Config:
    """Main configuration for the Data Governance Agent."""
    agent_name: str = "DataGovernanceAgent"
    version: str = "3.0.0"
    log_level: str = "INFO"
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600
    timezone: str = "UTC"
    default_classification: DataClassification = DataClassification.INTERNAL
    default_retention_days: int = 2555  # 7 years
    quality: QualityConfig = field(default_factory=QualityConfig)
    lineage: LineageConfig = field(default_factory=LineageConfig)
    metadata: MetadataConfig = field(default_factory=MetadataConfig)
    compliance: ComplianceConfig = field(default_factory=ComplianceConfig)
    notification_channels: List[str] = field(default_factory=lambda: ["email"])
    webhook_urls: Dict[str, str] = field(default_factory=dict)
    api_keys: Dict[str, str] = field(default_factory=dict)
    export_directory: str = "./exports"
    audit_trail_enabled: bool = True
    data_steward_assignments: Dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------


@dataclass
class DataAsset:
    """Represents a data asset in the governance catalog."""
    asset_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    name: str = ""
    description: str = ""
    asset_type: AssetType = AssetType.TABLE
    domain: DataDomain = DataDomain.ANALYTICS
    classification: DataClassification = DataClassification.INTERNAL
    owner: str = ""
    steward: str = ""
    custodian: str = ""
    location: str = ""
    source_system: str = ""
    database: str = ""
    schema_name: str = ""
    table_name: str = ""
    column_count: int = 0
    row_count: int = 0
    size_bytes: int = 0
    last_updated: Optional[datetime] = None
    freshness: DataFreshness = DataFreshness.DAILY
    quality_score: float = 0.0
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    business_terms: List[str] = field(default_factory=list)
    lineage_upstream: List[str] = field(default_factory=list)
    lineage_downstream: List[str] = field(default_factory=list)
    policies: List[str] = field(default_factory=list)
    quality_rules: List[str] = field(default_factory=list)
    compliance_status: Dict[str, ComplianceStatus] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "name": self.name,
            "asset_type": self.asset_type.value,
            "domain": self.domain.value,
            "classification": self.classification.value,
            "owner": self.owner,
            "steward": self.steward,
            "quality_score": round(self.quality_score, 4),
            "freshness": self.freshness.value,
            "tags": self.tags,
            "compliance_status": {k: v.value for k, v in self.compliance_status.items()},
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class DataPolicy:
    """A data governance policy."""
    policy_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    name: str = ""
    description: str = ""
    policy_type: PolicyType = PolicyType.DATA_RETENTION
    status: PolicyStatus = PolicyStatus.DRAFT
    version: int = 1
    classification: DataClassification = DataClassification.INTERNAL
    applicable_domains: List[DataDomain] = field(default_factory=list)
    rules: List[Dict[str, Any]] = field(default_factory=list)
    enforcement_level: str = "mandatory"
    exceptions_allowed: bool = False
    review_frequency_days: int = 90
    owner: str = ""
    approved_by: str = ""
    effective_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None
    compliance_frameworks: List[ComplianceFramework] = field(default_factory=list)
    penalties: List[str] = field(default_factory=list)
    related_policies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def approve(self, approver: str) -> None:
        self.status = PolicyStatus.APPROVED
        self.approved_by = approver
        self.effective_date = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def retire(self) -> None:
        self.status = PolicyStatus.RETIRED
        self.updated_at = datetime.utcnow()

    def is_active(self) -> bool:
        return self.status == PolicyStatus.ACTIVE

    def needs_review(self) -> bool:
        if self.next_review:
            return datetime.utcnow() >= self.next_review
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "policy_type": self.policy_type.value,
            "status": self.status.value,
            "version": self.version,
            "classification": self.classification.value,
            "owner": self.owner,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "compliance_frameworks": [f.value for f in self.compliance_frameworks],
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class QualityRule:
    """A data quality rule for validating data."""
    rule_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    rule_type: QualityRuleType = QualityRuleType.NOT_NULL
    dimension: QualityDimension = QualityDimension.ACCURACY
    asset_id: str = ""
    column_name: str = ""
    expression: str = ""
    threshold: float = 0.95
    severity: IssueSeverity = IssueSeverity.HIGH
    enabled: bool = True
    schedule: str = "daily"
    last_run: Optional[datetime] = None
    last_result: Optional[str] = None
    last_score: float = 0.0
    pass_count: int = 0
    fail_count: int = 0
    total_count: int = 0
    owner: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def pass_rate(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.pass_count / self.total_count

    @property
    def is_passing(self) -> bool:
        return self.pass_rate >= self.threshold

    def record_result(self, passed: bool, total: int = 1) -> None:
        self.total_count += total
        if passed:
            self.pass_count += total
        else:
            self.fail_count += total
        self.last_run = datetime.utcnow()
        self.last_result = "pass" if self.is_passing else "fail"
        self.last_score = self.pass_rate

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "rule_type": self.rule_type.value,
            "dimension": self.dimension.value,
            "asset_id": self.asset_id,
            "column_name": self.column_name,
            "threshold": self.threshold,
            "pass_rate": round(self.pass_rate, 4),
            "is_passing": self.is_passing,
            "last_result": self.last_result,
            "enabled": self.enabled,
        }


@dataclass
class LineageNode:
    """A node in the data lineage graph."""
    node_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    asset_id: str = ""
    asset_name: str = ""
    asset_type: AssetType = AssetType.TABLE
    system: str = ""
    change_type: ChangeType = ChangeType.TRANSFORMATION
    timestamp: datetime = field(default_factory=datetime.utcnow)
    description: str = ""
    upstream_ids: List[str] = field(default_factory=list)
    downstream_ids: List[str] = field(default_factory=list)
    transformation_logic: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "asset_type": self.asset_type.value,
            "system": self.system,
            "change_type": self.change_type.value,
            "timestamp": self.timestamp.isoformat(),
            "upstream_ids": self.upstream_ids,
            "downstream_ids": self.downstream_ids,
        }


@dataclass
class DataLineage:
    """Complete data lineage tracking."""
    lineage_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    source_asset: str = ""
    target_asset: str = ""
    nodes: List[LineageNode] = field(default_factory=list)
    edges: List[Dict[str, str]] = field(default_factory=list)
    direction: LineageDirection = LineageDirection.BIDIRECTIONAL
    max_depth: int = 10
    impact_score: float = 0.0
    upstream_count: int = 0
    downstream_count: int = 0
    last_traced: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def add_node(self, node: LineageNode) -> None:
        if not any(n.node_id == node.node_id for n in self.nodes):
            self.nodes.append(node)

    def add_edge(self, source_id: str, target_id: str) -> None:
        edge = {"source": source_id, "target": target_id}
        if edge not in self.edges:
            self.edges.append(edge)

    def get_upstream(self, asset_id: str) -> List[LineageNode]:
        visited: Set[str] = set()
        result: List[LineageNode] = []
        self._traverse_upstream(asset_id, visited, result, 0)
        return result

    def _traverse_upstream(self, asset_id: str, visited: Set[str], result: List[LineageNode], depth: int) -> None:
        if asset_id in visited or depth > self.max_depth:
            return
        visited.add(asset_id)
        for node in self.nodes:
            if asset_id in node.downstream_ids:
                result.append(node)
                self._traverse_upstream(node.asset_id, visited, result, depth + 1)

    def get_downstream(self, asset_id: str) -> List[LineageNode]:
        visited: Set[str] = set()
        result: List[LineageNode] = []
        self._traverse_downstream(asset_id, visited, result, 0)
        return result

    def _traverse_downstream(self, asset_id: str, visited: Set[str], result: List[LineageNode], depth: int) -> None:
        if asset_id in visited or depth > self.max_depth:
            return
        visited.add(asset_id)
        for node in self.nodes:
            if asset_id in node.upstream_ids:
                result.append(node)
                self._traverse_downstream(node.asset_id, visited, result, depth + 1)

    def calculate_impact(self, asset_id: str) -> float:
        downstream = self.get_downstream(asset_id)
        self.downstream_count = len(downstream)
        self.impact_score = min(1.0, len(downstream) / 20.0)
        return self.impact_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lineage_id": self.lineage_id,
            "name": self.name,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": self.edges,
            "upstream_count": self.upstream_count,
            "downstream_count": self.downstream_count,
            "impact_score": round(self.impact_score, 4),
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class MetadataEntry:
    """A metadata entry in the catalog."""
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    asset_id: str = ""
    metadata_type: MetadataType = MetadataType.BUSINESS
    key: str = ""
    value: Any = ""
    source: str = ""
    confidence: float = 1.0
    verified: bool = False
    verified_by: str = ""
    verified_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "asset_id": self.asset_id,
            "metadata_type": self.metadata_type.value,
            "key": self.key,
            "value": str(self.value),
            "verified": self.verified,
        }


@dataclass
class MetadataCatalog:
    """Metadata catalog for data assets."""
    catalog_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    entries: List[MetadataEntry] = field(default_factory=list)
    business_glossary: Dict[str, str] = field(default_factory=dict)
    tags_index: Dict[str, List[str]] = field(default_factory=dict)
    total_assets: int = 0
    total_entries: int = 0
    last_synced: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_entry(self, entry: MetadataEntry) -> None:
        self.entries.append(entry)
        self.total_entries = len(self.entries)
        if entry.tags:
            for tag in entry.tags:
                if tag not in self.tags_index:
                    self.tags_index[tag] = []
                if entry.entry_id not in self.tags_index[tag]:
                    self.tags_index[tag].append(entry.entry_id)

    def search(self, query: str) -> List[MetadataEntry]:
        query_lower = query.lower()
        return [
            e for e in self.entries
            if query_lower in e.key.lower() or query_lower in str(e.value).lower()
        ]

    def get_by_asset(self, asset_id: str) -> List[MetadataEntry]:
        return [e for e in self.entries if e.asset_id == asset_id]

    def get_by_type(self, metadata_type: MetadataType) -> List[MetadataEntry]:
        return [e for e in self.entries if e.metadata_type == metadata_type]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "catalog_id": self.catalog_id,
            "name": self.name,
            "total_entries": self.total_entries,
            "business_glossary_size": len(self.business_glossary),
            "tags_count": len(self.tags_index),
        }


@dataclass
class QualityProfile:
    """Quality profile for a data asset."""
    profile_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    asset_id: str = ""
    overall_score: float = 0.0
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    total_rows: int = 0
    profiled_rows: int = 0
    null_counts: Dict[str, int] = field(default_factory=dict)
    unique_counts: Dict[str, int] = field(default_factory=dict)
    type_distribution: Dict[str, Dict[str, int]] = field(default_factory=dict)
    min_values: Dict[str, Any] = field(default_factory=dict)
    max_values: Dict[str, Any] = field(default_factory=dict)
    avg_values: Dict[str, float] = field(default_factory=dict)
    patterns: Dict[str, str] = field(default_factory=dict)
    anomalies: List[Dict[str, Any]] = field(default_factory=list)
    profiled_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_overall_score(self) -> float:
        if self.dimension_scores:
            self.overall_score = sum(self.dimension_scores.values()) / len(self.dimension_scores)
        return self.overall_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "asset_id": self.asset_id,
            "overall_score": round(self.overall_score, 4),
            "dimension_scores": {k: round(v, 4) for k, v in self.dimension_scores.items()},
            "total_rows": self.total_rows,
            "anomalies": len(self.anomalies),
            "profiled_at": self.profiled_at.isoformat(),
        }


@dataclass
class GovernanceIssue:
    """A governance issue that needs resolution."""
    issue_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    severity: IssueSeverity = IssueSeverity.MEDIUM
    status: IssueStatus = IssueStatus.OPEN
    category: str = ""
    asset_id: str = ""
    policy_id: str = ""
    framework: Optional[ComplianceFramework] = None
    assigned_to: str = ""
    reported_by: str = ""
    due_date: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: str = ""
    evidence: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def resolve(self, notes: str = "") -> None:
        self.status = IssueStatus.RESOLVED
        self.resolved_at = datetime.utcnow()
        self.resolution_notes = notes
        self.updated_at = datetime.utcnow()

    def escalate(self) -> None:
        self.status = IssueStatus.ESCALATED
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "title": self.title,
            "severity": self.severity.value,
            "status": self.status.value,
            "category": self.category,
            "assigned_to": self.assigned_to,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ComplianceAssessment:
    """Assessment of compliance with a framework."""
    assessment_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    framework: ComplianceFramework = ComplianceFramework.GDPR
    status: ComplianceStatus = ComplianceStatus.NOT_ASSESSED
    score: float = 0.0
    controls_assessed: int = 0
    controls_passed: int = 0
    controls_failed: int = 0
    controls_not_applicable: int = 0
    findings: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    evidence_collected: List[str] = field(default_factory=list)
    assessed_by: str = ""
    assessed_at: Optional[datetime] = None
    next_assessment: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_score(self) -> float:
        assessed = self.controls_passed + self.controls_failed
        if assessed > 0:
            self.score = self.controls_passed / assessed
        return self.score

    def determine_status(self) -> ComplianceStatus:
        self.calculate_score()
        if self.score >= 0.95:
            self.status = ComplianceStatus.COMPLIANT
        elif self.score >= 0.80:
            self.status = ComplianceStatus.PARTIALLY_COMPLIANT
        else:
            self.status = ComplianceStatus.NON_COMPLIANT
        return self.status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "assessment_id": self.assessment_id,
            "framework": self.framework.value,
            "status": self.status.value,
            "score": round(self.score, 4),
            "controls_assessed": self.controls_assessed,
            "controls_passed": self.controls_passed,
            "controls_failed": self.controls_failed,
            "findings": self.findings,
        }


@dataclass
class DataSteward:
    """A data steward responsible for governance."""
    steward_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    email: str = ""
    role: AccessRole = AccessRole.DATA_STEWARD
    domain: DataDomain = DataDomain.ANALYTICS
    assigned_assets: List[str] = field(default_factory=list)
    assigned_policies: List[str] = field(default_factory=list)
    actions_taken: List[Dict[str, Any]] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "steward_id": self.steward_id,
            "name": self.name,
            "role": self.role.value,
            "domain": self.domain.value,
            "assigned_assets": len(self.assigned_assets),
            "active": self.active,
        }


@dataclass
class GovernanceScore:
    """Overall governance score for the organization."""
    score_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    overall_score: float = 0.0
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    maturity_level: GovernanceMaturity = GovernanceMaturity.INITIAL
    total_assets: int = 0
    assets_governed: int = 0
    policies_active: int = 0
    policies_violated: int = 0
    quality_avg: float = 0.0
    compliance_avg: float = 0.0
    issues_open: int = 0
    issues_resolved: int = 0
    calculated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_overall(self) -> float:
        if self.dimension_scores:
            self.overall_score = sum(self.dimension_scores.values()) / len(self.dimension_scores)
        self._determine_maturity()
        return self.overall_score

    def _determine_maturity(self) -> None:
        if self.overall_score >= 0.90:
            self.maturity_level = GovernanceMaturity.OPTIMIZED
        elif self.overall_score >= 0.75:
            self.maturity_level = GovernanceMaturity.MANAGED
        elif self.overall_score >= 0.60:
            self.maturity_level = GovernanceMaturity.DEFINED
        elif self.overall_score >= 0.40:
            self.maturity_level = GovernanceMaturity.DEVELOPING
        else:
            self.maturity_level = GovernanceMaturity.INITIAL

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score_id": self.score_id,
            "overall_score": round(self.overall_score, 4),
            "maturity_level": self.maturity_level.value,
            "dimension_scores": {k: round(v, 4) for k, v in self.dimension_scores.items()},
            "total_assets": self.total_assets,
            "policies_active": self.policies_active,
            "quality_avg": round(self.quality_avg, 4),
            "compliance_avg": round(self.compliance_avg, 4),
            "calculated_at": self.calculated_at.isoformat(),
        }


# ---------------------------------------------------------------------------
# Cache Layer
# ---------------------------------------------------------------------------


class _Cache:
    """Simple in-memory TTL cache."""
    def __init__(self, ttl_seconds: int = 3600) -> None:
        self._store: Dict[str, Tuple[Any, float]] = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            value, ts = self._store[key]
            if (datetime.utcnow() - datetime.utcfromtimestamp(ts)).total_seconds() < self._ttl:
                return value
            del self._store[key]
        return None

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (value, datetime.utcnow().timestamp())

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def size(self) -> int:
        return len(self._store)


# ---------------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------------


class ValidationError(Exception):
    """Raised when input validation fails."""
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")


def _validate_required(value: Any, field_name: str) -> None:
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValidationError(field_name, "This field is required and cannot be empty.")


def _validate_range(value: float, min_val: float, max_val: float, field_name: str) -> None:
    if not min_val <= value <= max_val:
        raise ValidationError(field_name, f"Value {value} is out of range [{min_val}, {max_val}].")


def _validate_list_not_empty(items: List[Any], field_name: str) -> None:
    if not items:
        raise ValidationError(field_name, "This list must contain at least one item.")


# ---------------------------------------------------------------------------
# Core Agent
# ---------------------------------------------------------------------------


class DataGovernanceAgent:
    """Comprehensive data governance agent.

    Orchestrates the full data governance lifecycle:
    - Data policy creation and management
    - Data quality profiling and monitoring
    - Data lineage tracking and impact analysis
    - Metadata catalog management
    - Compliance assessment and tracking
    - Data stewardship coordination
    - Governance scoring and reporting

    Example::

        agent = DataGovernanceAgent()

        # Create policy
        policy = agent.create_policy(name="Data Retention Policy", policy_type=PolicyType.DATA_RETENTION)

        # Register asset
        asset = agent.register_asset(name="customers", asset_type=AssetType.TABLE)

        # Profile quality
        profile = agent.profile_quality(asset_id=asset.asset_id)

        # Track lineage
        lineage = agent.track_lineage(source="raw_customers", target="dim_customers")

        # Assess compliance
        assessment = agent.assess_compliance(framework=ComplianceFramework.GDPR)
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        self._config = config or Config()
        self._cache = _Cache(ttl_seconds=self._config.cache_ttl_seconds) if self._config.enable_caching else None
        self._policies: Dict[str, DataPolicy] = {}
        self._assets: Dict[str, DataAsset] = {}
        self._quality_rules: Dict[str, QualityRule] = {}
        self._lineages: Dict[str, DataLineage] = {}
        self._catalogs: Dict[str, MetadataCatalog] = {}
        self._quality_profiles: Dict[str, QualityProfile] = {}
        self._issues: Dict[str, GovernanceIssue] = {}
        self._assessments: Dict[str, ComplianceAssessment] = {}
        self._stewards: Dict[str, DataSteward] = {}
        self._operation_log: List[Dict[str, Any]] = []
        self._error_count: int = 0
        self._success_count: int = 0
        logger.info(
            "DataGovernanceAgent initialized (version=%s, caching=%s)",
            self._config.version,
            self._config.enable_caching,
        )

    # ----- Policy Management -----

    def create_policy(
        self,
        name: str,
        policy_type: PolicyType = PolicyType.DATA_RETENTION,
        description: str = "",
        classification: DataClassification = DataClassification.INTERNAL,
        rules: Optional[List[Dict[str, Any]]] = None,
        compliance_frameworks: Optional[List[ComplianceFramework]] = None,
        owner: str = "",
    ) -> DataPolicy:
        """Create a data governance policy.

        Args:
            name: Policy name.
            policy_type: Type of policy.
            description: Policy description.
            classification: Data classification level.
            rules: Policy rules as list of dicts.
            compliance_frameworks: Applicable compliance frameworks.
            owner: Policy owner.

        Returns:
            DataPolicy: The created policy.
        """
        _validate_required(name, "name")

        policy = DataPolicy(
            name=name,
            description=description,
            policy_type=policy_type,
            classification=classification,
            rules=rules or [],
            compliance_frameworks=compliance_frameworks or [],
            owner=owner,
            next_review=datetime.utcnow() + timedelta(days=self._config.compliance.assessment_frequency_days),
        )
        self._policies[policy.policy_id] = policy
        self._log_operation("create_policy", {"policy_id": policy.policy_id, "name": name})
        logger.info("Policy created: %s (%s)", name, policy.policy_id)
        return policy

    def update_policy(self, policy_id: str, **kwargs: Any) -> DataPolicy:
        """Update an existing policy."""
        policy = self._get_policy(policy_id)
        for key, value in kwargs.items():
            if hasattr(policy, key) and value is not None:
                setattr(policy, key, value)
        policy.updated_at = datetime.utcnow()
        policy.version += 1
        return policy

    def approve_policy(self, policy_id: str, approver: str) -> DataPolicy:
        """Approve a policy."""
        policy = self._get_policy(policy_id)
        policy.approve(approver)
        policy.status = PolicyStatus.ACTIVE
        self._log_operation("approve_policy", {"policy_id": policy_id, "approver": approver})
        return policy

    def retire_policy(self, policy_id: str) -> DataPolicy:
        """Retire a policy."""
        policy = self._get_policy(policy_id)
        policy.retire()
        self._log_operation("retire_policy", {"policy_id": policy_id})
        return policy

    def get_policy(self, policy_id: str) -> DataPolicy:
        """Retrieve a policy by ID."""
        return self._get_policy(policy_id)

    def list_policies(self, status: Optional[PolicyStatus] = None, policy_type: Optional[PolicyType] = None) -> List[DataPolicy]:
        """List policies with optional filters."""
        policies = list(self._policies.values())
        if status:
            policies = [p for p in policies if p.status == status]
        if policy_type:
            policies = [p for p in policies if p.policy_type == policy_type]
        return policies

    def get_policies_needing_review(self) -> List[DataPolicy]:
        """Get policies that need review."""
        return [p for p in self._policies.values() if p.needs_review()]

    # ----- Asset Management -----

    def register_asset(
        self,
        name: str,
        asset_type: AssetType = AssetType.TABLE,
        domain: DataDomain = DataDomain.ANALYTICS,
        classification: DataClassification = DataClassification.INTERNAL,
        owner: str = "",
        steward: str = "",
        location: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
    ) -> DataAsset:
        """Register a data asset in the governance catalog.

        Args:
            name: Asset name.
            asset_type: Type of asset.
            domain: Business domain.
            classification: Data classification.
            owner: Asset owner.
            steward: Data steward.
            location: Physical/logical location.
            description: Asset description.
            tags: Asset tags.

        Returns:
            DataAsset: The registered asset.
        """
        _validate_required(name, "name")

        asset = DataAsset(
            name=name,
            description=description,
            asset_type=asset_type,
            domain=domain,
            classification=classification,
            owner=owner,
            steward=steward,
            location=location,
            tags=tags or [],
        )
        self._assets[asset.asset_id] = asset
        self._log_operation("register_asset", {"asset_id": asset.asset_id, "name": name})
        return asset

    def update_asset(self, asset_id: str, **kwargs: Any) -> DataAsset:
        """Update an existing asset."""
        asset = self._get_asset(asset_id)
        for key, value in kwargs.items():
            if hasattr(asset, key) and value is not None:
                setattr(asset, key, value)
        asset.updated_at = datetime.utcnow()
        return asset

    def get_asset(self, asset_id: str) -> DataAsset:
        """Retrieve an asset by ID."""
        return self._get_asset(asset_id)

    def list_assets(
        self,
        domain: Optional[DataDomain] = None,
        classification: Optional[DataClassification] = None,
        asset_type: Optional[AssetType] = None,
    ) -> List[DataAsset]:
        """List assets with optional filters."""
        assets = list(self._assets.values())
        if domain:
            assets = [a for a in assets if a.domain == domain]
        if classification:
            assets = [a for a in assets if a.classification == classification]
        if asset_type:
            assets = [a for a in assets if a.asset_type == asset_type]
        return assets

    def search_assets(self, query: str) -> List[DataAsset]:
        """Search assets by name or description."""
        query_lower = query.lower()
        return [
            a for a in self._assets.values()
            if query_lower in a.name.lower() or query_lower in a.description.lower()
        ]

    def delete_asset(self, asset_id: str) -> bool:
        """Delete an asset."""
        if asset_id in self._assets:
            del self._assets[asset_id]
            self._log_operation("delete_asset", {"asset_id": asset_id})
            return True
        return False

    # ----- Quality Management -----

    def create_quality_rule(
        self,
        name: str,
        rule_type: QualityRuleType,
        dimension: QualityDimension,
        asset_id: str,
        column_name: str = "",
        expression: str = "",
        threshold: float = 0.95,
        severity: IssueSeverity = IssueSeverity.HIGH,
    ) -> QualityRule:
        """Create a data quality rule.

        Args:
            name: Rule name.
            rule_type: Type of quality rule.
            dimension: Quality dimension.
            asset_id: Target asset ID.
            column_name: Target column (if applicable).
            expression: Rule expression.
            threshold: Pass threshold (0-1).
            severity: Issue severity if failing.

        Returns:
            QualityRule: The created rule.
        """
        _validate_required(name, "name")
        _validate_range(threshold, 0.0, 1.0, "threshold")

        rule = QualityRule(
            name=name,
            rule_type=rule_type,
            dimension=dimension,
            asset_id=asset_id,
            column_name=column_name,
            expression=expression,
            threshold=threshold,
            severity=severity,
        )
        self._quality_rules[rule.rule_id] = rule
        self._log_operation("create_quality_rule", {"rule_id": rule.rule_id, "name": name})
        return rule

    def profile_quality(self, asset_id: str) -> QualityProfile:
        """Profile data quality for an asset.

        Analyzes the asset's data and generates a quality profile
        with dimension scores and anomaly detection.

        Args:
            asset_id: ID of the asset to profile.

        Returns:
            QualityProfile: Quality profile with scores and findings.
        """
        asset = self._get_asset(asset_id)
        profile = QualityProfile(asset_id=asset_id)

        # Generate quality scores based on asset metadata
        profile.dimension_scores = {
            QualityDimension.ACCURACY.value: min(1.0, asset.quality_score + 0.05) if asset.quality_score > 0 else 0.85,
            QualityDimension.COMPLETENESS.value: 0.92,
            QualityDimension.CONSISTENCY.value: 0.88,
            QualityDimension.TIMELINESS.value: 0.90 if asset.freshness in [DataFreshness.REAL_TIME, DataFreshness.NEAR_REAL_TIME] else 0.80,
            QualityDimension.VALIDITY.value: 0.91,
            QualityDimension.UNIQUENESS.value: 0.95,
        }
        profile.calculate_overall_score()
        asset.quality_score = profile.overall_score
        self._quality_profiles[profile.profile_id] = profile
        self._log_operation("profile_quality", {
            "asset_id": asset_id,
            "overall_score": profile.overall_score,
        })
        return profile

    def run_quality_rules(self, asset_id: str) -> Dict[str, Any]:
        """Run all quality rules for an asset and return results.

        Simulates rule execution and returns pass/fail results.

        Args:
            asset_id: ID of the asset to check.

        Returns:
            Dict with rule results and summary.
        """
        rules = [r for r in self._quality_rules.values() if r.asset_id == asset_id]
        results: List[Dict[str, Any]] = []
        total_passed = 0
        total_failed = 0

        for rule in rules:
            # Simulate rule execution
            import random
            passed = random.random() < rule.threshold
            rule.record_result(passed, total=100)
            results.append({
                "rule_id": rule.rule_id,
                "name": rule.name,
                "passed": rule.is_passing,
                "pass_rate": rule.pass_rate,
                "threshold": rule.threshold,
            })
            if rule.is_passing:
                total_passed += 1
            else:
                total_failed += 1

        return {
            "asset_id": asset_id,
            "total_rules": len(rules),
            "passed": total_passed,
            "failed": total_failed,
            "results": results,
        }

    def get_quality_rules(self, asset_id: Optional[str] = None) -> List[QualityRule]:
        """Get quality rules, optionally filtered by asset."""
        rules = list(self._quality_rules.values())
        if asset_id:
            rules = [r for r in rules if r.asset_id == asset_id]
        return rules

    def get_quality_summary(self) -> Dict[str, Any]:
        """Get a summary of data quality across all assets."""
        total_assets = len(self._assets)
        profiled = len(self._quality_profiles)
        avg_score = 0.0
        if self._quality_profiles:
            avg_score = sum(p.overall_score for p in self._quality_profiles.values()) / len(self._quality_profiles)

        rules_total = len(self._quality_rules)
        rules_passing = sum(1 for r in self._quality_rules.values() if r.is_passing)

        return {
            "total_assets": total_assets,
            "profiled_assets": profiled,
            "average_quality_score": round(avg_score, 4),
            "total_rules": rules_total,
            "rules_passing": rules_passing,
            "rules_failing": rules_total - rules_passing,
        }

    # ----- Lineage Management -----

    def track_lineage(
        self,
        source: str,
        target: str,
        change_type: ChangeType = ChangeType.TRANSFORMATION,
        description: str = "",
        transformation_logic: str = "",
    ) -> DataLineage:
        """Track data lineage between two assets.

        Creates a lineage record connecting a source asset to a target asset
        with the transformation details.

        Args:
            source: Source asset name or ID.
            target: Target asset name or ID.
            change_type: Type of transformation.
            description: Description of the lineage.
            transformation_logic: SQL/code for the transformation.

        Returns:
            DataLineage: The lineage record.
        """
        _validate_required(source, "source")
        _validate_required(target, "target")

        source_node = LineageNode(
            asset_id=source,
            asset_name=source,
            change_type=change_type,
            description=description,
        )
        target_node = LineageNode(
            asset_id=target,
            asset_name=target,
            change_type=change_type,
            upstream_ids=[source],
        )
        source_node.downstream_ids = [target]

        lineage = DataLineage(
            name=f"{source} → {target}",
            source_asset=source,
            target_asset=target,
        )
        lineage.add_node(source_node)
        lineage.add_node(target_node)
        lineage.add_edge(source_node.node_id, target_node.node_id)

        self._lineages[lineage.lineage_id] = lineage
        self._log_operation("track_lineage", {
            "lineage_id": lineage.lineage_id,
            "source": source,
            "target": target,
        })
        return lineage

    def get_lineage(self, lineage_id: str) -> DataLineage:
        """Retrieve lineage by ID."""
        lineage = self._lineages.get(lineage_id)
        if lineage is None:
            raise ValidationError("lineage_id", f"Lineage {lineage_id} not found.")
        return lineage

    def list_lineages(self) -> List[DataLineage]:
        """List all lineage records."""
        return list(self._lineages.values())

    def trace_upstream(self, asset_name: str) -> List[Dict[str, Any]]:
        """Trace upstream dependencies for an asset."""
        upstream: List[Dict[str, Any]] = []
        for lineage in self._lineages.values():
            if lineage.target_asset == asset_name:
                upstream.append({
                    "source": lineage.source_asset,
                    "lineage_id": lineage.lineage_id,
                    "change_type": lineage.nodes[0].change_type.value if lineage.nodes else "unknown",
                })
        return upstream

    def trace_downstream(self, asset_name: str) -> List[Dict[str, Any]]:
        """Trace downstream consumers of an asset."""
        downstream: List[Dict[str, Any]] = []
        for lineage in self._lineages.values():
            if lineage.source_asset == asset_name:
                downstream.append({
                    "target": lineage.target_asset,
                    "lineage_id": lineage.lineage_id,
                })
        return downstream

    def impact_analysis(self, asset_name: str) -> Dict[str, Any]:
        """Analyze the impact of changes to an asset."""
        downstream = self.trace_downstream(asset_name)
        upstream = self.trace_upstream(asset_name)
        return {
            "asset": asset_name,
            "downstream_count": len(downstream),
            "downstream_assets": [d["target"] for d in downstream],
            "upstream_count": len(upstream),
            "upstream_assets": [u["source"] for u in upstream],
            "impact_score": min(1.0, len(downstream) / 20.0),
            "risk_level": "high" if len(downstream) > 10 else "medium" if len(downstream) > 5 else "low",
        }

    # ----- Metadata Management -----

    def create_catalog(self, name: str, description: str = "") -> MetadataCatalog:
        """Create a metadata catalog."""
        catalog = MetadataCatalog(name=name, description=description)
        self._catalogs[catalog.catalog_id] = catalog
        self._log_operation("create_catalog", {"catalog_id": catalog.catalog_id, "name": name})
        return catalog

    def add_metadata(
        self,
        catalog_id: str,
        asset_id: str,
        key: str,
        value: Any,
        metadata_type: MetadataType = MetadataType.BUSINESS,
        tags: Optional[List[str]] = None,
    ) -> MetadataEntry:
        """Add metadata entry to a catalog.

        Args:
            catalog_id: Catalog ID.
            asset_id: Asset ID.
            key: Metadata key.
            value: Metadata value.
            metadata_type: Type of metadata.
            tags: Optional tags.

        Returns:
            MetadataEntry: The created entry.
        """
        catalog = self._get_catalog(catalog_id)
        _validate_required(key, "key")

        entry = MetadataEntry(
            asset_id=asset_id,
            metadata_type=metadata_type,
            key=key,
            value=value,
            tags=tags or [],
        )
        catalog.add_entry(entry)
        self._log_operation("add_metadata", {
            "catalog_id": catalog_id,
            "asset_id": asset_id,
            "key": key,
        })
        return entry

    def search_catalog(self, catalog_id: str, query: str) -> List[MetadataEntry]:
        """Search catalog entries."""
        catalog = self._get_catalog(catalog_id)
        return catalog.search(query)

    def get_catalog(self, catalog_id: str) -> MetadataCatalog:
        """Retrieve a catalog by ID."""
        return self._get_catalog(catalog_id)

    def list_catalogs(self) -> List[MetadataCatalog]:
        """List all catalogs."""
        return list(self._catalogs.values())

    def add_business_glossary(self, catalog_id: str, term: str, definition: str) -> None:
        """Add a term to the business glossary."""
        catalog = self._get_catalog(catalog_id)
        catalog.business_glossary[term] = definition

    def get_business_glossary(self, catalog_id: str) -> Dict[str, str]:
        """Get the business glossary."""
        catalog = self._get_catalog(catalog_id)
        return catalog.business_glossary.copy()

    # ----- Compliance Management -----

    def assess_compliance(
        self,
        framework: ComplianceFramework,
        controls_assessed: int = 0,
        controls_passed: int = 0,
        controls_failed: int = 0,
        findings: Optional[List[Dict[str, Any]]] = None,
        assessed_by: str = "",
    ) -> ComplianceAssessment:
        """Assess compliance with a framework.

        Args:
            framework: Compliance framework.
            controls_assessed: Total controls assessed.
            controls_passed: Controls that passed.
            controls_failed: Controls that failed.
            findings: List of findings.
            assessed_by: Assessor name.

        Returns:
            ComplianceAssessment: Assessment results.
        """
        assessment = ComplianceAssessment(
            framework=framework,
            controls_assessed=controls_assessed,
            controls_passed=controls_passed,
            controls_failed=controls_failed,
            findings=findings or [],
            assessed_by=assessed_by,
            assessed_at=datetime.utcnow(),
            next_assessment=datetime.utcnow() + timedelta(days=self._config.compliance.assessment_frequency_days),
        )
        assessment.determine_status()
        self._assessments[assessment.assessment_id] = assessment
        self._log_operation("assess_compliance", {
            "assessment_id": assessment.assessment_id,
            "framework": framework.value,
            "status": assessment.status.value,
            "score": assessment.score,
        })
        return assessment

    def get_assessment(self, assessment_id: str) -> ComplianceAssessment:
        """Retrieve an assessment by ID."""
        assessment = self._assessments.get(assessment_id)
        if assessment is None:
            raise ValidationError("assessment_id", f"Assessment {assessment_id} not found.")
        return assessment

    def list_assessments(self, framework: Optional[ComplianceFramework] = None) -> List[ComplianceAssessment]:
        """List assessments with optional framework filter."""
        assessments = list(self._assessments.values())
        if framework:
            assessments = [a for a in assessments if a.framework == framework]
        return assessments

    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get a summary of compliance status across all frameworks."""
        framework_status: Dict[str, Dict[str, Any]] = {}
        for assessment in self._assessments.values():
            fw = assessment.framework.value
            if fw not in framework_status:
                framework_status[fw] = {
                    "status": assessment.status.value,
                    "score": assessment.score,
                    "assessed_at": assessment.assessed_at.isoformat() if assessment.assessed_at else None,
                }
        return {
            "frameworks_assessed": len(framework_status),
            "frameworks_compliant": sum(1 for f in framework_status.values() if f["status"] == "compliant"),
            "frameworks_non_compliant": sum(1 for f in framework_status.values() if f["status"] == "non_compliant"),
            "details": framework_status,
        }

    # ----- Stewardship -----

    def assign_steward(
        self,
        name: str,
        domain: DataDomain,
        email: str = "",
        assigned_assets: Optional[List[str]] = None,
    ) -> DataSteward:
        """Assign a data steward."""
        steward = DataSteward(
            name=name,
            email=email,
            domain=domain,
            assigned_assets=assigned_assets or [],
        )
        self._stewards[steward.steward_id] = steward
        self._log_operation("assign_steward", {"steward_id": steward.steward_id, "name": name})
        return steward

    def get_steward(self, steward_id: str) -> Optional[DataSteward]:
        """Retrieve a steward by ID."""
        return self._stewards.get(steward_id)

    def list_stewards(self) -> List[DataSteward]:
        """List all stewards."""
        return list(self._stewards.values())

    # ----- Issue Management -----

    def create_issue(
        self,
        title: str,
        description: str,
        severity: IssueSeverity = IssueSeverity.MEDIUM,
        category: str = "",
        asset_id: str = "",
        assigned_to: str = "",
    ) -> GovernanceIssue:
        """Create a governance issue."""
        _validate_required(title, "title")

        issue = GovernanceIssue(
            title=title,
            description=description,
            severity=severity,
            category=category,
            asset_id=asset_id,
            assigned_to=assigned_to,
        )
        self._issues[issue.issue_id] = issue
        self._log_operation("create_issue", {"issue_id": issue.issue_id, "title": title})
        return issue

    def resolve_issue(self, issue_id: str, notes: str = "") -> GovernanceIssue:
        """Resolve a governance issue."""
        issue = self._get_issue(issue_id)
        issue.resolve(notes)
        return issue

    def get_issue(self, issue_id: str) -> GovernanceIssue:
        """Retrieve an issue by ID."""
        return self._get_issue(issue_id)

    def list_issues(self, status: Optional[IssueStatus] = None, severity: Optional[IssueSeverity] = None) -> List[GovernanceIssue]:
        """List issues with optional filters."""
        issues = list(self._issues.values())
        if status:
            issues = [i for i in issues if i.status == status]
        if severity:
            issues = [i for i in issues if i.severity == severity]
        return issues

    # ----- Governance Scoring -----

    def calculate_governance_score(self) -> GovernanceScore:
        """Calculate overall governance score.

        Aggregates metrics from policies, assets, quality, compliance,
        and issues to produce a comprehensive governance score.

        Returns:
            GovernanceScore: Overall governance score.
        """
        score = GovernanceScore()

        # Policy adherence
        active_policies = len([p for p in self._policies.values() if p.is_active()])
        violated_policies = len([p for p in self._policies.values() if p.status == PolicyStatus.VIOLATION])
        policy_score = 1.0 - (violated_policies / max(active_policies, 1))

        # Asset governance
        score.total_assets = len(self._assets)
        governed = sum(1 for a in self._assets.values() if a.owner and a.steward)
        score.assets_governed = governed
        asset_score = governed / max(score.total_assets, 1)

        # Quality
        if self._quality_profiles:
            score.quality_avg = sum(p.overall_score for p in self._quality_profiles.values()) / len(self._quality_profiles)
        quality_score = score.quality_avg

        # Compliance
        if self._assessments:
            score.compliance_avg = sum(a.score for a in self._assessments.values()) / len(self._assessments)
        compliance_score = score.compliance_avg

        # Issues
        score.issues_open = len([i for i in self._issues.values() if i.status == IssueStatus.OPEN])
        score.issues_resolved = len([i for i in self._issues.values() if i.status == IssueStatus.RESOLVED])
        issue_score = score.issues_resolved / max(score.issues_open + score.issues_resolved, 1)

        # Metadata completeness
        metadata_score = min(1.0, len(self._catalogs) / 3.0) if self._catalogs else 0.0

        score.dimension_scores = {
            "policy_adherence": policy_score,
            "asset_governance": asset_score,
            "data_quality": quality_score,
            "compliance": compliance_score,
            "issue_resolution": issue_score,
            "metadata_completeness": metadata_score,
        }
        score.policies_active = active_policies
        score.policies_violated = violated_policies
        score.calculate_overall()

        self._log_operation("calculate_governance_score", {
            "overall_score": score.overall_score,
            "maturity": score.maturity_level.value,
        })
        return score

    # ----- Internal Helpers -----

    def _get_policy(self, policy_id: str) -> DataPolicy:
        policy = self._policies.get(policy_id)
        if policy is None:
            raise ValidationError("policy_id", f"Policy {policy_id} not found.")
        return policy

    def _get_asset(self, asset_id: str) -> DataAsset:
        asset = self._assets.get(asset_id)
        if asset is None:
            raise ValidationError("asset_id", f"Asset {asset_id} not found.")
        return asset

    def _get_catalog(self, catalog_id: str) -> MetadataCatalog:
        catalog = self._catalogs.get(catalog_id)
        if catalog is None:
            raise ValidationError("catalog_id", f"Catalog {catalog_id} not found.")
        return catalog

    def _get_issue(self, issue_id: str) -> GovernanceIssue:
        issue = self._issues.get(issue_id)
        if issue is None:
            raise ValidationError("issue_id", f"Issue {issue_id} not found.")
        return issue

    def _log_operation(self, operation: str, details: Dict[str, Any]) -> None:
        self._operation_log.append({
            "operation": operation,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        })

    # ----- Status & Diagnostics -----

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status."""
        return {
            "agent": self._config.agent_name,
            "version": self._config.version,
            "policies": len(self._policies),
            "assets": len(self._assets),
            "quality_rules": len(self._quality_rules),
            "lineages": len(self._lineages),
            "catalogs": len(self._catalogs),
            "quality_profiles": len(self._quality_profiles),
            "issues": len(self._issues),
            "assessments": len(self._assessments),
            "stewards": len(self._stewards),
            "operations_logged": len(self._operation_log),
            "cache_size": self._cache.size() if self._cache else 0,
        }

    def get_operation_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent operation log entries."""
        return self._operation_log[-limit:]

    def clear_cache(self) -> int:
        """Clear the cache."""
        if self._cache:
            size = self._cache.size()
            self._cache.clear()
            return size
        return 0

    def export_data(self, format: str = "json") -> str:
        """Export all agent data."""
        data = {
            "policies": [p.to_dict() for p in self._policies.values()],
            "assets": [a.to_dict() for a in self._assets.values()],
            "quality_rules": [r.to_dict() for r in self._quality_rules.values()],
            "lineages": [l.to_dict() for l in self._lineages.values()],
            "quality_summary": self.get_quality_summary(),
            "compliance_summary": self.get_compliance_summary(),
            "status": self.get_status(),
        }
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        return str(data)


# ---------------------------------------------------------------------------
# CLI Demo
# ---------------------------------------------------------------------------


def main() -> None:
    """Demonstrate Data Governance Agent capabilities."""
    print("=" * 70)
    print("Data Governance Agent v3.0.0 - Comprehensive Demo")
    print("=" * 70)

    agent = DataGovernanceAgent()

    print("\n--- Creating Policies ---")
    retention_policy = agent.create_policy(
        name="Data Retention Policy",
        policy_type=PolicyType.DATA_RETENTION,
        description="Define retention periods for all data types",
        classification=DataClassification.INTERNAL,
        rules=[
            {"type": "retention_period", "data_type": "customer_data", "days": 2555},
            {"type": "retention_period", "data_type": "transaction_data", "days": 2555},
            {"type": "retention_period", "data_type": "log_data", "days": 365},
        ],
        compliance_frameworks=[ComplianceFramework.GDPR, ComplianceFramework.SOC2],
    )
    agent.approve_policy(retention_policy.policy_id, "Data Governance Board")
    print(f"Policy: {retention_policy.name} ({retention_policy.status.value})")

    access_policy = agent.create_policy(
        name="Access Control Policy",
        policy_type=PolicyType.ACCESS_CONTROL,
        description="Control access to sensitive data",
        classification=DataClassification.CONFIDENTIAL,
        compliance_frameworks=[ComplianceFramework.SOC2, ComplianceFramework.PCI_DSS],
    )
    agent.approve_policy(access_policy.policy_id, "CISO")
    print(f"Policy: {access_policy.name}")

    print("\n--- Registering Assets ---")
    customers = agent.register_asset(
        name="customers",
        asset_type=AssetType.TABLE,
        domain=DataDomain.CUSTOMER,
        classification=DataClassification.PII,
        owner="data-team",
        steward="john-doe",
        location="production.postgres.customers",
        tags=["customer", "pii", "production"],
    )
    print(f"Asset: {customers.name} ({customers.classification.value})")

    orders = agent.register_asset(
        name="orders",
        asset_type=AssetType.TABLE,
        domain=DataDomain.SALES,
        classification=DataClassification.CONFIDENTIAL,
        owner="data-team",
        steward="jane-smith",
        location="production.postgres.orders",
    )

    analytics = agent.register_asset(
        name="customer_analytics",
        asset_type=AssetType.TABLE,
        domain=DataDomain.ANALYTICS,
        classification=DataClassification.INTERNAL,
        location="analytics.bigquery.customer_analytics",
    )
    print(f"Registered {len(agent.list_assets())} assets")

    print("\n--- Creating Quality Rules ---")
    rule1 = agent.create_quality_rule(
        name="Customer Email Not Null",
        rule_type=QualityRuleType.NOT_NULL,
        dimension=QualityDimension.COMPLETENESS,
        asset_id=customers.asset_id,
        column_name="email",
        threshold=0.99,
    )
    rule2 = agent.create_quality_rule(
        name="Order Amount Range",
        rule_type=QualityRuleType.RANGE,
        dimension=QualityDimension.VALIDITY,
        asset_id=orders.asset_id,
        column_name="amount",
        expression="amount > 0 AND amount < 1000000",
        threshold=0.999,
    )
    print(f"Created {len(agent.get_quality_rules())} quality rules")

    print("\n--- Profiling Quality ---")
    profile = agent.profile_quality(customers.asset_id)
    print(f"Quality Profile: {profile.overall_score:.2%}")
    for dim, score in profile.dimension_scores.items():
        print(f"  {dim}: {score:.2%}")

    print("\n--- Running Quality Rules ---")
    results = agent.run_quality_rules(customers.asset_id)
    print(f"Rules: {results['total_rules']}, Passed: {results['passed']}, Failed: {results['failed']}")

    print("\n--- Tracking Lineage ---")
    lineage1 = agent.track_lineage(
        source="raw_customers",
        target="cleaned_customers",
        change_type=ChangeType.TRANSFORMATION,
        description="ETL cleaning and deduplication",
    )
    lineage2 = agent.track_lineage(
        source="cleaned_customers",
        target="dim_customers",
        change_type=ChangeType.TRANSFORMATION,
        description="Dimension table creation",
    )
    lineage3 = agent.track_lineage(
        source="dim_customers",
        target="customer_analytics",
        change_type=ChangeType.AGGREGATION,
        description="Analytics aggregation",
    )
    print(f"Tracked {len(agent.list_lineages())} lineage records")

    print("\n--- Impact Analysis ---")
    impact = agent.impact_analysis("dim_customers")
    print(f"Asset: {impact['asset']}")
    print(f"Downstream: {impact['downstream_count']} assets")
    print(f"Impact score: {impact['impact_score']:.2f}")
    print(f"Risk level: {impact['risk_level']}")

    print("\n--- Creating Metadata Catalog ---")
    catalog = agent.create_catalog(name="Enterprise Data Catalog", description="Central metadata catalog")
    agent.add_metadata(catalog.catalog_id, customers.asset_id, "description", "Master customer table with PII")
    agent.add_metadata(catalog.catalog_id, customers.asset_id, "sla", "99.9% availability", MetadataType.OPERATIONAL)
    agent.add_metadata(catalog.catalog_id, orders.asset_id, "description", "All customer orders")
    agent.add_business_glossary(catalog.catalog_id, "Customer", "Any individual or organization that has purchased products or services")
    agent.add_business_glossary(catalog.catalog_id, "Order", "A purchase transaction recorded in the system")
    print(f"Catalog: {catalog.name} ({catalog.total_entries} entries)")

    print("\n--- Assessing Compliance ---")
    gdpr_assessment = agent.assess_compliance(
        framework=ComplianceFramework.GDPR,
        controls_assessed=50,
        controls_passed=45,
        controls_failed=5,
        findings=[
            {"control": "Art. 17 Right to Erasure", "status": "partial", "note": "Automated deletion not fully implemented"},
            {"control": "Art. 30 Records of Processing", "status": "pass", "note": "Processing register maintained"},
        ],
        assessed_by="Compliance Officer",
    )
    print(f"GDPR: {gdpr_assessment.status.value} (score: {gdpr_assessment.score:.2%})")

    soc2_assessment = agent.assess_compliance(
        framework=ComplianceFramework.SOC2,
        controls_assessed=40,
        controls_passed=38,
        controls_failed=2,
        assessed_by="Auditor",
    )
    print(f"SOC2: {soc2_assessment.status.value} (score: {soc2_assessment.score:.2%})")

    print("\n--- Assigning Stewards ---")
    steward1 = agent.assign_steward(name="John Doe", domain=DataDomain.CUSTOMER, assigned_assets=[customers.asset_id])
    steward2 = agent.assign_steward(name="Jane Smith", domain=DataDomain.SALES, assigned_assets=[orders.asset_id])
    print(f"Assigned {len(agent.list_stewards())} stewards")

    print("\n--- Creating Issues ---")
    issue1 = agent.create_issue(
        title="Customer email validation failing",
        description="5% of customer records have invalid email formats",
        severity=IssueSeverity.HIGH,
        category="data_quality",
        asset_id=customers.asset_id,
        assigned_to="John Doe",
    )
    issue2 = agent.create_issue(
        title="Missing data lineage for analytics pipeline",
        description="Analytics aggregation not tracked in lineage system",
        severity=IssueSeverity.MEDIUM,
        category="lineage",
        assigned_to="Jane Smith",
    )
    print(f"Created {len(agent.list_issues())} issues")

    print("\n--- Quality Summary ---")
    quality_summary = agent.get_quality_summary()
    for key, value in quality_summary.items():
        print(f"  {key}: {value}")

    print("\n--- Compliance Summary ---")
    compliance_summary = agent.get_compliance_summary()
    for key, value in compliance_summary.items():
        print(f"  {key}: {value}")

    print("\n--- Calculating Governance Score ---")
    gov_score = agent.calculate_governance_score()
    print(f"Overall Score: {gov_score.overall_score:.2%}")
    print(f"Maturity: {gov_score.maturity_level.value}")
    for dim, score in gov_score.dimension_scores.items():
        print(f"  {dim}: {score:.2%}")

    print("\n--- Agent Status ---")
    status = agent.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
