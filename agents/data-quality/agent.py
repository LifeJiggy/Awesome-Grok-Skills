"""
Data Quality Agent - Comprehensive data validation, profiling, cleansing, monitoring, and anomaly detection.

Provides enterprise-grade data quality management including schema validation, statistical profiling,
automated cleansing pipelines, continuous monitoring with alerting, quality metrics computation,
and anomaly detection using statistical and machine learning approaches.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import re
import statistics
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Severity(Enum):
    """Issue severity levels for data quality problems."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class QualityDimension(Enum):
    """DAMA-style data quality dimensions."""
    COMPLETENESS = "completeness"
    ACCURACY = "accuracy"
    CONSISTENCY = "consistency"
    TIMELINESS = "timeliness"
    VALIDITY = "validity"
    UNIQUENESS = "uniqueness"
    INTEGRITY = "integrity"
    CONFORMANCE = "conformance"


class AnomalyMethod(Enum):
    """Statistical methods for anomaly detection."""
    ZSCORE = "zscore"
    IQR = "iqr"
    MAD = "mad"
    EWM_STD = "ewm_std"
    PERCENTILE = "percentile"
    ISOLATION_FOREST = "isolation_forest"


class ProfileType(Enum):
    """Types of column profiling operations."""
    NUMERIC = "numeric"
    TEXT = "text"
    DATETIME = "datetime"
    BOOLEAN = "boolean"
    CATEGORICAL = "categorical"
    JSON = "json"


class CleansingAction(Enum):
    """Actions available in cleansing pipelines."""
    DROP_ROWS = "drop_rows"
    FILL_MEAN = "fill_mean"
    FILL_MEDIAN = "fill_median"
    FILL_MODE = "fill_mode"
    FILL_VALUE = "fill_value"
    FILL_FORWARD = "fill_forward"
    FILL_BACKWARD = "fill_backward"
    TRIM_WHITESPACE = "trim_whitespace"
    LOWERCASE = "lowercase"
    UPPERCASE = "uppercase"
    REGEX_REPLACE = "regex_replace"
    DEDUPLICATE = "deduplicate"
    TYPE_CAST = "type_cast"
    CLIP = "clip"
    STRIP_CHARS = "strip_chars"
    HASH_PII = "hash_pii"
    MASK_PII = "mask_pii"


class MonitorStatus(Enum):
    """Status of a monitoring check."""
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    ERROR = "error"
    SKIPPED = "skipped"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class QualityIssue:
    """Represents a single data quality issue."""
    issue_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    dimension: QualityDimension = QualityDimension.VALIDITY
    severity: Severity = Severity.MEDIUM
    rule_name: str = ""
    message: str = ""
    affected_rows: int = 0
    affected_columns: List[str] = field(default_factory=list)
    sample_values: List[Any] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "dimension": self.dimension.value,
            "severity": self.severity.value,
            "rule_name": self.rule_name,
            "message": self.message,
            "affected_rows": self.affected_rows,
            "affected_columns": self.affected_columns,
            "sample_values": self.sample_values[:10],
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class ColumnProfile:
    """Statistical profile for a single column."""
    column_name: str
    profile_type: ProfileType = ProfileType.TEXT
    total_count: int = 0
    null_count: int = 0
    distinct_count: int = 0
    null_percentage: float = 0.0
    min_value: Any = None
    max_value: Any = None
    mean_value: Optional[float] = None
    median_value: Optional[float] = None
    std_dev: Optional[float] = None
    variance: Optional[float] = None
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None
    percentile_25: Optional[float] = None
    percentile_75: Optional[float] = None
    iqr: Optional[float] = None
    top_values: Dict[str, int] = field(default_factory=dict)
    avg_length: Optional[float] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern_distribution: Dict[str, int] = field(default_factory=dict)
    entropy: Optional[float] = None
    cardinality_ratio: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "column_name": self.column_name,
            "profile_type": self.profile_type.value,
            "total_count": self.total_count,
            "null_count": self.null_count,
            "distinct_count": self.distinct_count,
            "null_percentage": round(self.null_percentage, 4),
        }
        for attr in (
            "min_value", "max_value", "mean_value", "median_value",
            "std_dev", "variance", "skewness", "kurtosis",
            "percentile_25", "percentile_75", "iqr", "avg_length",
            "min_length", "max_length", "entropy", "cardinality_ratio",
        ):
            val = getattr(self, attr)
            if val is not None:
                result[attr] = round(val, 6) if isinstance(val, float) else val
        if self.top_values:
            result["top_values"] = dict(
                sorted(self.top_values.items(), key=lambda x: x[1], reverse=True)[:20]
            )
        if self.pattern_distribution:
            result["pattern_distribution"] = dict(
                sorted(self.pattern_distribution.items(), key=lambda x: x[1], reverse=True)[:10]
            )
        return result


@dataclass
class DatasetProfile:
    """Complete profile for a dataset."""
    dataset_name: str
    row_count: int = 0
    column_count: int = 0
    columns: List[ColumnProfile] = field(default_factory=list)
    overall_completeness: float = 0.0
    duplicate_rows: int = 0
    duplicate_percentage: float = 0.0
    memory_estimate_bytes: int = 0
    profiled_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_name": self.dataset_name,
            "row_count": self.row_count,
            "column_count": self.column_count,
            "overall_completeness": round(self.overall_completeness, 4),
            "duplicate_rows": self.duplicate_rows,
            "duplicate_percentage": round(self.duplicate_percentage, 4),
            "memory_estimate_bytes": self.memory_estimate_bytes,
            "profiled_at": self.profiled_at.isoformat(),
            "columns": [c.to_dict() for c in self.columns],
            "metadata": self.metadata,
        }


@dataclass
class QualityScore:
    """Composite quality score across dimensions."""
    overall: float = 0.0
    completeness: float = 0.0
    accuracy: float = 0.0
    consistency: float = 0.0
    timeliness: float = 0.0
    validity: float = 0.0
    uniqueness: float = 0.0
    dimensions: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall": round(self.overall, 4),
            "completeness": round(self.completeness, 4),
            "accuracy": round(self.accuracy, 4),
            "consistency": round(self.consistency, 4),
            "timeliness": round(self.timeliness, 4),
            "validity": round(self.validity, 4),
            "uniqueness": round(self.uniqueness, 4),
            "dimensions": {k: round(v, 4) for k, v in self.dimensions.items()},
        }


@dataclass
class ValidationRule:
    """Definition of a data validation rule."""
    rule_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    name: str = ""
    dimension: QualityDimension = QualityDimension.VALIDITY
    severity: Severity = Severity.MEDIUM
    column: Optional[str] = None
    rule_type: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    description: str = ""
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "dimension": self.dimension.value,
            "severity": self.severity.value,
            "column": self.column,
            "rule_type": self.rule_type,
            "parameters": self.parameters,
            "enabled": self.enabled,
            "description": self.description,
            "tags": self.tags,
        }


@dataclass
class AnomalyResult:
    """Result of an anomaly detection operation."""
    column: str
    method: AnomalyMethod
    anomaly_count: int = 0
    anomaly_indices: List[int] = field(default_factory=list)
    threshold: float = 0.0
    statistics: Dict[str, float] = field(default_factory=dict)
    values: List[Any] = field(default_factory=list)
    z_scores: List[float] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "column": self.column,
            "method": self.method.value,
            "anomaly_count": self.anomaly_count,
            "anomaly_indices": self.anomaly_indices[:50],
            "threshold": self.threshold,
            "statistics": {k: round(v, 6) for k, v in self.statistics.items()},
            "values": self.values[:20],
            "z_scores": [round(z, 4) for z in self.z_scores[:20]],
        }


@dataclass
class MonitorCheck:
    """A single monitoring check definition."""
    check_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    name: str = ""
    check_type: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    schedule: Optional[str] = None
    enabled: bool = True
    alert_on_fail: bool = True
    severity: Severity = Severity.HIGH
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "check_id": self.check_id,
            "name": self.name,
            "check_type": self.check_type,
            "parameters": self.parameters,
            "schedule": self.schedule,
            "enabled": self.enabled,
            "alert_on_fail": self.alert_on_fail,
            "severity": self.severity.value,
            "description": self.description,
        }


@dataclass
class MonitorResult:
    """Result of executing a monitoring check."""
    check_id: str
    check_name: str
    status: MonitorStatus
    message: str = ""
    actual_value: Any = None
    expected_value: Any = None
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "check_id": self.check_id,
            "check_name": self.check_name,
            "status": self.status.value,
            "message": self.message,
            "actual_value": self.actual_value,
            "expected_value": self.expected_value,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class CleansingStep:
    """A single step in a cleansing pipeline."""
    action: CleansingAction
    column: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    condition: Optional[str] = None
    order: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action.value,
            "column": self.column,
            "parameters": self.parameters,
            "condition": self.condition,
            "order": self.order,
        }


@dataclass
class CleansingResult:
    """Result of running a cleansing pipeline."""
    rows_before: int = 0
    rows_after: int = 0
    rows_affected: int = 0
    columns_affected: List[str] = field(default_factory=list)
    steps_executed: List[Dict[str, Any]] = field(default_factory=list)
    issues_fixed: int = 0
    remaining_issues: int = 0
    duration_ms: float = 0.0
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rows_before": self.rows_before,
            "rows_after": self.rows_after,
            "rows_affected": self.rows_affected,
            "columns_affected": self.columns_affected,
            "steps_executed": self.steps_executed,
            "issues_fixed": self.issues_fixed,
            "remaining_issues": self.remaining_issues,
            "duration_ms": round(self.duration_ms, 2),
            "warnings": self.warnings,
        }


@dataclass
class QualityReport:
    """Comprehensive quality assessment report."""
    dataset_name: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    score: QualityScore = field(default_factory=QualityScore)
    profile: Optional[DatasetProfile] = None
    issues: List[QualityIssue] = field(default_factory=list)
    anomalies: List[AnomalyResult] = field(default_factory=list)
    monitor_results: List[MonitorResult] = field(default_factory=list)
    cleansing_result: Optional[CleansingResult] = None
    summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_name": self.dataset_name,
            "timestamp": self.timestamp.isoformat(),
            "score": self.score.to_dict(),
            "profile": self.profile.to_dict() if self.profile else None,
            "issues": [i.to_dict() for i in self.issues],
            "anomalies": [a.to_dict() for a in self.anomalies],
            "monitor_results": [m.to_dict() for m in self.monitor_results],
            "cleansing_result": self.cleansing_result.to_dict() if self.cleansing_result else None,
            "summary": self.summary,
        }


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class DataQualityConfig:
    """Configuration for the Data Quality Agent."""
    zscore_threshold: float = 3.0
    iqr_multiplier: float = 1.5
    mad_threshold: float = 3.5
    percentile_lower: float = 1.0
    percentile_upper: float = 99.0
    ewm_span: int = 20
    ewm_threshold: float = 3.0
    max_sample_values: int = 100
    top_n_values: int = 20
    max_column_pattern_length: int = 50
    null_threshold_warn: float = 0.05
    null_threshold_fail: float = 0.20
    duplicate_threshold_warn: float = 0.01
    duplicate_threshold_fail: float = 0.05
    cardinality_high_threshold: float = 0.95
    cardinality_low_threshold: float = 0.01
    enable_entropy_calculation: bool = True
    enable_skewness_kurtosis: bool = True
    enable_pattern_detection: bool = True
    pii_patterns: Dict[str, str] = field(default_factory=lambda: {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\+?[\d\-\(\)\s]{7,15}",
        "ssn": r"\d{3}-\d{2}-\d{4}",
        "credit_card": r"\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}",
        "ip_address": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
    })
    custom_rules: List[ValidationRule] = field(default_factory=list)
    cleansing_default_steps: List[CleansingStep] = field(default_factory=list)
    monitor_checks: List[MonitorCheck] = field(default_factory=list)
    dimension_weights: Dict[str, float] = field(default_factory=lambda: {
        "completeness": 0.20,
        "accuracy": 0.20,
        "consistency": 0.15,
        "timeliness": 0.10,
        "validity": 0.20,
        "uniqueness": 0.15,
    })


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _compute_entropy(values: List[Any]) -> float:
    """Compute Shannon entropy of a value distribution."""
    if not values:
        return 0.0
    counter = Counter(values)
    n = len(values)
    entropy = 0.0
    for count in counter.values():
        p = count / n
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def _compute_skewness(values: List[float]) -> float:
    """Compute sample skewness of numeric values."""
    n = len(values)
    if n < 3:
        return 0.0
    mean = statistics.mean(values)
    std = statistics.stdev(values)
    if std == 0:
        return 0.0
    m3 = sum((x - mean) ** 3 for x in values) / n
    return m3 / (std ** 3)


def _compute_kurtosis(values: List[float]) -> float:
    """Compute excess kurtosis of numeric values."""
    n = len(values)
    if n < 4:
        return 0.0
    mean = statistics.mean(values)
    std = statistics.stdev(values)
    if std == 0:
        return 0.0
    m4 = sum((x - mean) ** 4 for x in values) / n
    return (m4 / (std ** 4)) - 3.0


def _detect_value_pattern(value: str) -> str:
    """Detect the general pattern of a string value."""
    if not value:
        return "empty"
    pattern = []
    for ch in value:
        if ch.isdigit():
            pattern.append("D")
        elif ch.isalpha():
            pattern.append("A" if ch.isupper() else "a")
        elif ch in " \t":
            pattern.append("S")
        else:
            pattern.append("P")
    result = "".join(pattern)
    if len(result) > 20:
        result = result[:20] + "..."
    return result


def _compute_z_scores(values: List[float]) -> List[float]:
    """Compute z-scores for a list of numeric values."""
    if len(values) < 2:
        return [0.0] * len(values)
    mean = statistics.mean(values)
    std = statistics.stdev(values)
    if std == 0:
        return [0.0] * len(values)
    return [(x - mean) / std for x in values]


def _compute_iqr_bounds(values: List[float], multiplier: float = 1.5) -> Tuple[float, float]:
    """Compute IQR-based outlier bounds."""
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    q1 = sorted_vals[n // 4]
    q3 = sorted_vals[3 * n // 4]
    iqr = q3 - q1
    return q1 - multiplier * iqr, q3 + multiplier * iqr


def _compute_mad(values: List[float]) -> float:
    """Compute Median Absolute Deviation."""
    med = statistics.median(values)
    return statistics.median(abs(x - med) for x in values)


def _hash_value(value: str, algorithm: str = "sha256") -> str:
    """Hash a string value for PII protection."""
    h = hashlib.new(algorithm)
    h.update(value.encode("utf-8"))
    return h.hexdigest()[:16]


def _mask_value(value: str, visible_chars: int = 4, mask_char: str = "*") -> str:
    """Mask a value showing only the last N characters."""
    if len(value) <= visible_chars:
        return mask_char * len(value)
    return mask_char * (len(value) - visible_chars) + value[-visible_chars:]


# ---------------------------------------------------------------------------
# Core Agent
# ---------------------------------------------------------------------------

class DataQualityAgent:
    """
    Enterprise-grade Data Quality Agent providing validation, profiling,
    cleansing, monitoring, anomaly detection, and quality scoring.
    """

    def __init__(self, config: Optional[DataQualityConfig] = None):
        self._config = config or DataQualityConfig()
        self._datasets: Dict[str, Any] = {}
        self._profiles: Dict[str, DatasetProfile] = {}
        self._rules: List[ValidationRule] = list(self._config.custom_rules)
        self._monitor_checks: Dict[str, List[MonitorCheck]] = defaultdict(list)
        self._monitor_history: Dict[str, List[MonitorResult]] = defaultdict(list)
        self._issue_history: List[QualityIssue] = []
        self._cleansing_pipelines: Dict[str, List[CleansingStep]] = {}
        logger.info("DataQualityAgent initialized with %d custom rules", len(self._rules))

    # -----------------------------------------------------------------------
    # Data ingestion
    # -----------------------------------------------------------------------

    def register_dataset(self, name: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Register a dataset for quality assessment."""
        self._datasets[name] = data
        logger.info("Registered dataset '%s' with %d rows", name, len(data))
        return {
            "dataset": name,
            "rows": len(data),
            "columns": list(data[0].keys()) if data else [],
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_dataset(self, name: str) -> List[Dict[str, Any]]:
        """Retrieve a registered dataset."""
        if name not in self._datasets:
            raise KeyError(f"Dataset '{name}' not found")
        return self._datasets[name]

    # -----------------------------------------------------------------------
    # Profiling
    # -----------------------------------------------------------------------

    def profile_dataset(self, name: str) -> DatasetProfile:
        """Generate a comprehensive statistical profile for a dataset."""
        data = self.get_dataset(name)
        if not data:
            logger.warning("Empty dataset '%s', returning empty profile", name)
            return DatasetProfile(dataset_name=name)

        columns = list(data[0].keys())
        column_profiles: List[ColumnProfile] = []

        for col in columns:
            values = [row.get(col) for row in data]
            cp = self._profile_column(col, values)
            column_profiles.append(cp)

        total_cells = len(data) * len(columns) if columns else 0
        filled_cells = sum(cp.total_count - cp.null_count for cp in column_profiles)
        overall_completeness = filled_cells / total_cells if total_cells > 0 else 0.0

        hash_keys = [json.dumps(row, sort_keys=True, default=str) for row in data]
        duplicate_count = len(data) - len(set(hash_keys))

        profile = DatasetProfile(
            dataset_name=name,
            row_count=len(data),
            column_count=len(columns),
            columns=column_profiles,
            overall_completeness=overall_completeness,
            duplicate_rows=duplicate_count,
            duplicate_percentage=duplicate_count / len(data) if data else 0.0,
            metadata={
                "unique_hash_count": len(set(hash_keys)),
            },
        )
        self._profiles[name] = profile
        logger.info("Profiled dataset '%s': %d rows x %d cols", name, len(data), len(columns))
        return profile

    def _profile_column(self, col_name: str, values: List[Any]) -> ColumnProfile:
        """Profile a single column of values."""
        total = len(values)
        null_count = sum(1 for v in values if v is None or v == "" or (isinstance(v, float) and math.isnan(v)))
        non_null = [v for v in values if v is not None and v != "" and not (isinstance(v, float) and math.isnan(v))]
        distinct = set(str(v) for v in non_null)
        distinct_count = len(distinct)

        cp = ColumnProfile(
            column_name=col_name,
            total_count=total,
            null_count=null_count,
            distinct_count=distinct_count,
            null_percentage=(null_count / total * 100) if total > 0 else 0.0,
            cardinality_ratio=(distinct_count / len(non_null)) if non_null else 0.0,
        )

        if not non_null:
            return cp

        numeric_vals: List[float] = []
        str_vals: List[str] = []
        for v in non_null:
            if isinstance(v, (int, float)):
                numeric_vals.append(float(v))
            else:
                str_vals.append(str(v))

        # Determine profile type
        if len(numeric_vals) > len(non_null) * 0.5:
            cp.profile_type = ProfileType.NUMERIC
            cp.min_value = min(numeric_vals)
            cp.max_value = max(numeric_vals)
            cp.mean_value = statistics.mean(numeric_vals)
            cp.median_value = statistics.median(numeric_vals)
            if len(numeric_vals) > 1:
                cp.std_dev = statistics.stdev(numeric_vals)
                cp.variance = statistics.variance(numeric_vals)
            sorted_num = sorted(numeric_vals)
            n = len(sorted_num)
            cp.percentile_25 = sorted_num[n // 4]
            cp.percentile_75 = sorted_num[3 * n // 4]
            cp.iqr = cp.percentile_75 - cp.percentile_25
            if self._config.enable_skewness_kurtosis:
                cp.skewness = _compute_skewness(numeric_vals)
                cp.kurtosis = _compute_kurtosis(numeric_vals)
        else:
            cp.profile_type = ProfileType.TEXT
            str_lengths = [len(s) for s in str_vals]
            cp.avg_length = statistics.mean(str_lengths) if str_lengths else 0.0
            cp.min_length = min(str_lengths) if str_lengths else 0
            cp.max_length = max(str_lengths) if str_lengths else 0
            cp.min_value = min(str_vals) if str_vals else None
            cp.max_value = max(str_vals) if str_vals else None

        # Top values
        cp.top_values = dict(Counter(str(v) for v in non_null).most_common(self._config.top_n_values))

        # Pattern distribution
        if self._config.enable_pattern_detection and str_vals:
            patterns = Counter(_detect_value_pattern(s) for s in str_vals[:self._config.max_sample_values])
            cp.pattern_distribution = dict(patterns.most_common(10))

        # Entropy
        if self._config.enable_entropy_calculation:
            cp.entropy = _compute_entropy([str(v) for v in non_null])

        return cp

    # -----------------------------------------------------------------------
    # Validation
    # -----------------------------------------------------------------------

    def add_rule(self, rule: ValidationRule) -> str:
        """Add a validation rule."""
        self._rules.append(rule)
        logger.info("Added validation rule '%s' (id=%s)", rule.name, rule.rule_id)
        return rule.rule_id

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a validation rule by ID."""
        before = len(self._rules)
        self._rules = [r for r in self._rules if r.rule_id != rule_id]
        removed = len(self._rules) < before
        if removed:
            logger.info("Removed rule %s", rule_id)
        return removed

    def list_rules(self) -> List[Dict[str, Any]]:
        """List all active validation rules."""
        return [r.to_dict() for r in self._rules if r.enabled]

    def validate_dataset(self, name: str) -> List[QualityIssue]:
        """Run all enabled validation rules against a dataset."""
        data = self.get_dataset(name)
        issues: List[QualityIssue] = []

        for rule in self._rules:
            if not rule.enabled:
                continue
            try:
                rule_issues = self._apply_rule(data, rule)
                issues.extend(rule_issues)
            except Exception as e:
                logger.error("Rule '%s' failed: %s", rule.name, e)
                issues.append(QualityIssue(
                    dimension=rule.dimension,
                    severity=Severity.HIGH,
                    rule_name=rule.name,
                    message=f"Rule execution error: {e}",
                    metadata={"rule_id": rule.rule_id, "error": str(e)},
                ))

        self._issue_history.extend(issues)
        logger.info("Validation of '%s' found %d issues", name, len(issues))
        return issues

    def _apply_rule(self, data: List[Dict[str, Any]], rule: ValidationRule) -> List[QualityIssue]:
        """Apply a single validation rule and return issues found."""
        issues: List[QualityIssue] = []
        column = rule.column

        if rule.rule_type == "not_null" and column:
            bad_rows = [i for i, row in enumerate(data) if row.get(column) is None or row.get(column) == ""]
            if bad_rows:
                issues.append(QualityIssue(
                    dimension=rule.dimension,
                    severity=rule.severity,
                    rule_name=rule.name,
                    message=f"Column '{column}' has {len(bad_rows)} null/empty values",
                    affected_rows=len(bad_rows),
                    affected_columns=[column],
                    sample_values=[data[i].get(column) for i in bad_rows[:5]],
                    metadata={"rule_id": rule.rule_id, "bad_row_indices": bad_rows[:100]},
                ))

        elif rule.rule_type == "unique" and column:
            seen: Dict[str, List[int]] = defaultdict(list)
            for i, row in enumerate(data):
                val = str(row.get(column, ""))
                seen[val].append(i)
            dupes = {k: v for k, v in seen.items() if len(v) > 1}
            if dupes:
                total_dup_rows = sum(len(v) - 1 for v in dupes.values())
                issues.append(QualityIssue(
                    dimension=QualityDimension.UNIQUENESS,
                    severity=rule.severity,
                    rule_name=rule.name,
                    message=f"Column '{column}' has {len(dupes)} duplicate values ({total_dup_rows} extra rows)",
                    affected_rows=total_dup_rows,
                    affected_columns=[column],
                    sample_values=list(dupes.keys())[:5],
                    metadata={"rule_id": rule.rule_id, "duplicate_values": {k: v[:5] for k, v in list(dupes.items())[:10]}},
                ))

        elif rule.rule_type == "regex" and column:
            pattern = rule.parameters.get("pattern", "")
            compiled = re.compile(pattern)
            bad_rows = [i for i, row in enumerate(data) if row.get(column) and not compiled.match(str(row.get(column, "")))]
            if bad_rows:
                issues.append(QualityIssue(
                    dimension=rule.dimension,
                    severity=rule.severity,
                    rule_name=rule.name,
                    message=f"Column '{column}' has {len(bad_rows)} values not matching pattern",
                    affected_rows=len(bad_rows),
                    affected_columns=[column],
                    sample_values=[data[i].get(column) for i in bad_rows[:5]],
                    metadata={"rule_id": rule.rule_id, "pattern": pattern},
                ))

        elif rule.rule_type == "range" and column:
            min_val = rule.parameters.get("min")
            max_val = rule.parameters.get("max")
            bad_rows = []
            for i, row in enumerate(data):
                val = row.get(column)
                if val is not None:
                    try:
                        num = float(val)
                        if (min_val is not None and num < min_val) or (max_val is not None and num > max_val):
                            bad_rows.append(i)
                    except (ValueError, TypeError):
                        bad_rows.append(i)
            if bad_rows:
                issues.append(QualityIssue(
                    dimension=rule.dimension,
                    severity=rule.severity,
                    rule_name=rule.name,
                    message=f"Column '{column}' has {len(bad_rows)} values outside range [{min_val}, {max_val}]",
                    affected_rows=len(bad_rows),
                    affected_columns=[column],
                    sample_values=[data[i].get(column) for i in bad_rows[:5]],
                    metadata={"rule_id": rule.rule_id, "min": min_val, "max": max_val},
                ))

        elif rule.rule_type == "allowed_values" and column:
            allowed = set(rule.parameters.get("values", []))
            bad_rows = [i for i, row in enumerate(data) if row.get(column) not in allowed]
            if bad_rows:
                issues.append(QualityIssue(
                    dimension=rule.dimension,
                    severity=rule.severity,
                    rule_name=rule.name,
                    message=f"Column '{column}' has {len(bad_rows)} values not in allowed set",
                    affected_rows=len(bad_rows),
                    affected_columns=[column],
                    sample_values=[data[i].get(column) for i in bad_rows[:5]],
                    metadata={"rule_id": rule.rule_id, "allowed_values": list(allowed)[:20]},
                ))

        elif rule.rule_type == "custom" and rule.parameters.get("function"):
            func_ref = rule.parameters["function"]
            for i, row in enumerate(data):
                try:
                    if not func_ref(row):
                        issues.append(QualityIssue(
                            dimension=rule.dimension,
                            severity=rule.severity,
                            rule_name=rule.name,
                            message=f"Custom rule failed for row {i}",
                            affected_rows=1,
                            affected_columns=[column] if column else [],
                            metadata={"rule_id": rule.rule_id, "row_index": i},
                        ))
                except Exception as e:
                    logger.warning("Custom rule function error on row %d: %s", i, e)

        return issues

    # -----------------------------------------------------------------------
    # Quality scoring
    # -----------------------------------------------------------------------

    def compute_quality_score(self, name: str) -> QualityScore:
        """Compute a composite quality score for a dataset across all dimensions."""
        issues = self.validate_dataset(name)
        profile = self._profiles.get(name) or self.profile_dataset(name)

        weights = self._config.dimension_weights
        scores: Dict[str, float] = {}

        # Completeness
        scores["completeness"] = profile.overall_completeness

        # Validity
        validity_issues = [i for i in issues if i.dimension == QualityDimension.VALIDITY]
        total_rows = profile.row_count or 1
        scores["validity"] = max(0.0, 1.0 - sum(i.affected_rows for i in validity_issues) / total_rows)

        # Uniqueness
        scores["uniqueness"] = max(0.0, 1.0 - profile.duplicate_percentage)

        # Accuracy (custom rules that flag accuracy)
        accuracy_issues = [i for i in issues if i.dimension == QualityDimension.ACCURACY]
        scores["accuracy"] = max(0.0, 1.0 - sum(i.affected_rows for i in accuracy_issues) / total_rows)

        # Consistency
        consistency_issues = [i for i in issues if i.dimension == QualityDimension.CONSISTENCY]
        scores["consistency"] = max(0.0, 1.0 - sum(i.affected_rows for i in consistency_issues) / total_rows)

        # Timeliness (default high unless temporal checks indicate otherwise)
        timeliness_issues = [i for i in issues if i.dimension == QualityDimension.TIMELINESS]
        scores["timeliness"] = max(0.0, 1.0 - len(timeliness_issues) / max(len(issues), 1))

        # Compute overall weighted score
        overall = 0.0
        total_weight = 0.0
        for dim, weight in weights.items():
            if dim in scores:
                overall += scores[dim] * weight
                total_weight += weight
        overall = overall / total_weight if total_weight > 0 else 0.0

        return QualityScore(
            overall=overall,
            completeness=scores.get("completeness", 0.0),
            accuracy=scores.get("accuracy", 0.0),
            consistency=scores.get("consistency", 0.0),
            timeliness=scores.get("timeliness", 0.0),
            validity=scores.get("validity", 0.0),
            uniqueness=scores.get("uniqueness", 0.0),
            dimensions=scores,
        )

    # -----------------------------------------------------------------------
    # Anomaly detection
    # -----------------------------------------------------------------------

    def detect_anomalies(
        self,
        name: str,
        column: str,
        method: AnomalyMethod = AnomalyMethod.ZSCORE,
        **kwargs: Any,
    ) -> AnomalyResult:
        """Detect anomalies in a numeric column using the specified method."""
        data = self.get_dataset(name)
        values = []
        indices = []
        for i, row in enumerate(data):
            v = row.get(column)
            if v is not None:
                try:
                    values.append(float(v))
                    indices.append(i)
                except (ValueError, TypeError):
                    continue

        if not values:
            return AnomalyResult(column=column, method=method)

        if method == AnomalyMethod.ZSCORE:
            return self._detect_zscore(column, values, indices, kwargs.get("threshold", self._config.zscore_threshold))
        elif method == AnomalyMethod.IQR:
            return self._detect_iqr(column, values, indices, kwargs.get("multiplier", self._config.iqr_multiplier))
        elif method == AnomalyMethod.MAD:
            return self._detect_mad(column, values, indices, kwargs.get("threshold", self._config.mad_threshold))
        elif method == AnomalyMethod.EWM_STD:
            return self._detect_ewm(column, values, indices, kwargs.get("span", self._config.ewm_span))
        elif method == AnomalyMethod.PERCENTILE:
            return self._detect_percentile(
                column, values, indices,
                kwargs.get("lower", self._config.percentile_lower),
                kwargs.get("upper", self._config.percentile_upper),
            )
        else:
            return AnomalyResult(column=column, method=method)

    def _detect_zscore(
        self, column: str, values: List[float], indices: List[int], threshold: float
    ) -> AnomalyResult:
        """Detect anomalies using z-score method."""
        z_scores = _compute_z_scores(values)
        anomaly_indices = [
            indices[i] for i, z in enumerate(z_scores) if abs(z) > threshold
        ]
        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0.0
        return AnomalyResult(
            column=column,
            method=AnomalyMethod.ZSCORE,
            anomaly_count=len(anomaly_indices),
            anomaly_indices=anomaly_indices,
            threshold=threshold,
            statistics={"mean": mean, "std_dev": std},
            values=[values[i] for i in anomaly_indices[:20]],
            z_scores=[z_scores[i] for i in range(len(z_scores)) if abs(z_scores[i]) > threshold][:20],
        )

    def _detect_iqr(
        self, column: str, values: List[float], indices: List[int], multiplier: float
    ) -> AnomalyResult:
        """Detect anomalies using IQR method."""
        lower, upper = _compute_iqr_bounds(values, multiplier)
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        q1 = sorted_vals[n // 4]
        q3 = sorted_vals[3 * n // 4]
        iqr = q3 - q1
        anomaly_indices = [
            indices[i] for i, v in enumerate(values) if v < lower or v > upper
        ]
        return AnomalyResult(
            column=column,
            method=AnomalyMethod.IQR,
            anomaly_count=len(anomaly_indices),
            anomaly_indices=anomaly_indices,
            threshold=multiplier,
            statistics={"q1": q1, "q3": q3, "iqr": iqr, "lower_bound": lower, "upper_bound": upper},
            values=[values[i] for i in anomaly_indices[:20]],
        )

    def _detect_mad(
        self, column: str, values: List[float], indices: List[int], threshold: float
    ) -> AnomalyResult:
        """Detect anomalies using Median Absolute Deviation."""
        med = statistics.median(values)
        mad = _compute_mad(values)
        if mad == 0:
            return AnomalyResult(column=column, method=AnomalyMethod.MAD, threshold=threshold)
        modified_z = [0.6745 * (v - med) / mad for v in values]
        anomaly_indices = [
            indices[i] for i, z in enumerate(modified_z) if abs(z) > threshold
        ]
        return AnomalyResult(
            column=column,
            method=AnomalyMethod.MAD,
            anomaly_count=len(anomaly_indices),
            anomaly_indices=anomaly_indices,
            threshold=threshold,
            statistics={"median": med, "mad": mad},
            values=[values[i] for i in anomaly_indices[:20]],
        )

    def _detect_ewm(
        self, column: str, values: List[float], indices: List[int], span: int
    ) -> AnomalyResult:
        """Detect anomalies using Exponentially Weighted Moving Std."""
        if len(values) < span:
            return AnomalyResult(column=column, method=AnomalyMethod.EWM_STD)
        alpha = 2.0 / (span + 1)
        ewm_mean = values[0]
        ewm_var = 0.0
        anomaly_indices = []
        for i in range(1, len(values)):
            diff = values[i] - ewm_mean
            ewm_mean = alpha * values[i] + (1 - alpha) * ewm_mean
            ewm_var = alpha * diff * diff + (1 - alpha) * ewm_var
            ewm_std = math.sqrt(ewm_var)
            if ewm_std > 0 and abs(values[i] - ewm_mean) / ewm_std > self._config.ewm_threshold:
                anomaly_indices.append(indices[i])

        return AnomalyResult(
            column=column,
            method=AnomalyMethod.EWM_STD,
            anomaly_count=len(anomaly_indices),
            anomaly_indices=anomaly_indices,
            threshold=self._config.ewm_threshold,
            statistics={"span": float(span), "alpha": alpha},
            values=[values[indices.index(idx)] for idx in anomaly_indices[:20] if idx in indices],
        )

    def _detect_percentile(
        self, column: str, values: List[float], indices: List[int], lower: float, upper: float
    ) -> AnomalyResult:
        """Detect anomalies using percentile-based thresholds."""
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        low_val = sorted_vals[max(0, int(lower / 100 * n))]
        high_val = sorted_vals[min(n - 1, int(upper / 100 * n))]
        anomaly_indices = [
            indices[i] for i, v in enumerate(values) if v < low_val or v > high_val
        ]
        return AnomalyResult(
            column=column,
            method=AnomalyMethod.PERCENTILE,
            anomaly_count=len(anomaly_indices),
            anomaly_indices=anomaly_indices,
            statistics={"lower_percentile": lower, "upper_percentile": upper, "lower_bound": low_val, "upper_bound": high_val},
            values=[values[i] for i in anomaly_indices[:20]],
        )

    # -----------------------------------------------------------------------
    # Cleansing
    # -----------------------------------------------------------------------

    def create_cleansing_pipeline(self, name: str, steps: List[CleansingStep]) -> Dict[str, Any]:
        """Create a named cleansing pipeline."""
        sorted_steps = sorted(steps, key=lambda s: s.order)
        self._cleansing_pipelines[name] = sorted_steps
        logger.info("Created cleansing pipeline '%s' with %d steps", name, len(sorted_steps))
        return {
            "pipeline": name,
            "steps": len(sorted_steps),
            "actions": [s.action.value for s in sorted_steps],
        }

    def run_cleansing_pipeline(
        self, dataset_name: str, pipeline_name: str
    ) -> CleansingResult:
        """Execute a cleansing pipeline on a dataset."""
        data = self.get_dataset(dataset_name)
        if pipeline_name not in self._cleansing_pipelines:
            raise KeyError(f"Pipeline '{pipeline_name}' not found")

        pipeline = self._cleansing_pipelines[pipeline_name]
        result = CleansingResult(rows_before=len(data))
        modified = list(data)
        columns_affected: Set[str] = set()
        steps_executed: List[Dict[str, Any]] = []

        for step in pipeline:
            before_count = len(modified)
            step_result: Dict[str, Any] = {"action": step.action.value, "column": step.column}
            try:
                if step.action == CleansingAction.DROP_ROWS:
                    if step.column:
                        modified = [r for r in modified if r.get(step.column) is not None and r.get(step.column) != ""]
                    elif step.parameters.get("condition"):
                        cond = step.parameters["condition"]
                        modified = [r for r in modified if not eval(cond, {"__builtins__": {}}, {"row": r})]

                elif step.action == CleansingAction.FILL_MEAN and step.column:
                    vals = [float(r[step.column]) for r in modified if r.get(step.column) is not None]
                    mean_val = statistics.mean(vals) if vals else 0
                    for r in modified:
                        if r.get(step.column) is None:
                            r[step.column] = mean_val
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.FILL_MEDIAN and step.column:
                    vals = [float(r[step.column]) for r in modified if r.get(step.column) is not None]
                    med_val = statistics.median(vals) if vals else 0
                    for r in modified:
                        if r.get(step.column) is None:
                            r[step.column] = med_val
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.FILL_MODE and step.column:
                    vals = [r[step.column] for r in modified if r.get(step.column) is not None]
                    if vals:
                        mode_val = Counter(vals).most_common(1)[0][0]
                        for r in modified:
                            if r.get(step.column) is None:
                                r[step.column] = mode_val
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.FILL_VALUE and step.column:
                    fill_val = step.parameters.get("value", "")
                    for r in modified:
                        if r.get(step.column) is None:
                            r[step.column] = fill_val
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.TRIM_WHITESPACE and step.column:
                    for r in modified:
                        if isinstance(r.get(step.column), str):
                            r[step.column] = r[step.column].strip()
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.LOWERCASE and step.column:
                    for r in modified:
                        if isinstance(r.get(step.column), str):
                            r[step.column] = r[step.column].lower()
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.UPPERCASE and step.column:
                    for r in modified:
                        if isinstance(r.get(step.column), str):
                            r[step.column] = r[step.column].upper()
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.REGEX_REPLACE and step.column:
                    pattern = step.parameters.get("pattern", "")
                    replacement = step.parameters.get("replacement", "")
                    compiled = re.compile(pattern)
                    for r in modified:
                        if isinstance(r.get(step.column), str):
                            r[step.column] = compiled.sub(replacement, r[step.column])
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.DEDUPLICATE:
                    seen: Set[str] = set()
                    unique_data = []
                    for r in modified:
                        key = json.dumps(r, sort_keys=True, default=str)
                        if key not in seen:
                            seen.add(key)
                            unique_data.append(r)
                    modified = unique_data

                elif step.action == CleansingAction.TYPE_CAST and step.column:
                    target_type = step.parameters.get("type", "str")
                    for r in modified:
                        if r.get(step.column) is not None:
                            try:
                                if target_type == "int":
                                    r[step.column] = int(r[step.column])
                                elif target_type == "float":
                                    r[step.column] = float(r[step.column])
                                elif target_type == "str":
                                    r[step.column] = str(r[step.column])
                            except (ValueError, TypeError):
                                pass
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.CLIP and step.column:
                    min_val = step.parameters.get("min")
                    max_val = step.parameters.get("max")
                    for r in modified:
                        if r.get(step.column) is not None:
                            try:
                                val = float(r[step.column])
                                if min_val is not None:
                                    val = max(val, float(min_val))
                                if max_val is not None:
                                    val = min(val, float(max_val))
                                r[step.column] = val
                            except (ValueError, TypeError):
                                pass
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.HASH_PII and step.column:
                    for r in modified:
                        if r.get(step.column) is not None:
                            r[step.column] = _hash_value(str(r[step.column]))
                    columns_affected.add(step.column)

                elif step.action == CleansingAction.MASK_PII and step.column:
                    visible = step.parameters.get("visible_chars", 4)
                    for r in modified:
                        if r.get(step.column) is not None:
                            r[step.column] = _mask_value(str(r[step.column]), visible)
                    columns_affected.add(step.column)

                step_result["rows_before"] = before_count
                step_result["rows_after"] = len(modified)
                step_result["status"] = "success"

            except Exception as e:
                step_result["status"] = "error"
                step_result["error"] = str(e)
                logger.error("Cleansing step '%s' failed: %s", step.action.value, e)

            steps_executed.append(step_result)

        self._datasets[dataset_name] = modified
        result.rows_after = len(modified)
        result.rows_affected = result.rows_before - result.rows_after
        result.columns_affected = sorted(columns_affected)
        result.steps_executed = steps_executed
        logger.info(
            "Cleansing pipeline '%s' on '%s': %d -> %d rows",
            pipeline_name, dataset_name, result.rows_before, result.rows_after,
        )
        return result

    # -----------------------------------------------------------------------
    # Monitoring
    # -----------------------------------------------------------------------

    def add_monitor_check(self, dataset_name: str, check: MonitorCheck) -> str:
        """Add a monitoring check for a dataset."""
        self._monitor_checks[dataset_name].append(check)
        logger.info("Added monitor check '%s' for dataset '%s'", check.name, dataset_name)
        return check.check_id

    def run_monitor_checks(self, dataset_name: str) -> List[MonitorResult]:
        """Execute all monitoring checks for a dataset."""
        checks = self._monitor_checks.get(dataset_name, [])
        results: List[MonitorResult] = []

        for check in checks:
            if not check.enabled:
                continue
            try:
                result = self._execute_check(dataset_name, check)
                results.append(result)
                self._monitor_history[dataset_name].append(result)
            except Exception as e:
                results.append(MonitorResult(
                    check_id=check.check_id,
                    check_name=check.name,
                    status=MonitorStatus.ERROR,
                    message=f"Check execution error: {e}",
                ))

        logger.info("Executed %d checks on '%s': %d passed, %d failed",
                     len(results), dataset_name,
                     sum(1 for r in results if r.status == MonitorStatus.PASS),
                     sum(1 for r in results if r.status == MonitorStatus.FAIL))
        return results

    def _execute_check(self, dataset_name: str, check: MonitorCheck) -> MonitorResult:
        """Execute a single monitoring check."""
        data = self.get_dataset(dataset_name)
        params = check.parameters

        if check.check_type == "row_count_min":
            min_rows = params.get("min", 0)
            actual = len(data)
            status = MonitorStatus.PASS if actual >= min_rows else MonitorStatus.FAIL
            return MonitorResult(
                check_id=check.check_id, check_name=check.name, status=status,
                message=f"Row count {actual} vs minimum {min_rows}",
                actual_value=actual, expected_value=min_rows,
            )

        elif check.check_type == "row_count_max":
            max_rows = params.get("max", float("inf"))
            actual = len(data)
            status = MonitorStatus.PASS if actual <= max_rows else MonitorStatus.WARN
            return MonitorResult(
                check_id=check.check_id, check_name=check.name, status=status,
                message=f"Row count {actual} vs maximum {max_rows}",
                actual_value=actual, expected_value=max_rows,
            )

        elif check.check_type == "null_percentage":
            column = params.get("column", "")
            max_pct = params.get("max_percentage", 100.0)
            values = [row.get(column) for row in data]
            null_count = sum(1 for v in values if v is None or v == "")
            actual_pct = (null_count / len(values) * 100) if values else 0.0
            status = MonitorStatus.PASS if actual_pct <= max_pct else MonitorStatus.FAIL
            return MonitorResult(
                check_id=check.check_id, check_name=check.name, status=status,
                message=f"Column '{column}' null percentage: {actual_pct:.2f}% vs max {max_pct}%",
                actual_value=actual_pct, expected_value=max_pct,
            )

        elif check.check_type == "freshness":
            column = params.get("timestamp_column", "")
            max_age_hours = params.get("max_age_hours", 24)
            now = datetime.now(timezone.utc)
            latest = None
            for row in data:
                val = row.get(column)
                if val:
                    try:
                        dt = datetime.fromisoformat(str(val))
                        if latest is None or dt > latest:
                            latest = dt
                    except (ValueError, TypeError):
                        pass
            if latest:
                age_hours = (now - latest).total_seconds() / 3600
                status = MonitorStatus.PASS if age_hours <= max_age_hours else MonitorStatus.FAIL
                return MonitorResult(
                    check_id=check.check_id, check_name=check.name, status=status,
                    message=f"Data freshness: {age_hours:.1f}h old vs max {max_age_hours}h",
                    actual_value=age_hours, expected_value=max_age_hours,
                )
            return MonitorResult(
                check_id=check.check_id, check_name=check.name,
                status=MonitorStatus.WARN, message=f"No parseable timestamps in '{column}'",
            )

        elif check.check_type == "schema_match":
            expected_columns = set(params.get("columns", []))
            actual_columns = set(data[0].keys()) if data else set()
            missing = expected_columns - actual_columns
            extra = actual_columns - expected_columns
            status = MonitorStatus.PASS if not missing else MonitorStatus.FAIL
            return MonitorResult(
                check_id=check.check_id, check_name=check.name, status=status,
                message=f"Missing columns: {missing}, Extra columns: {extra}",
                actual_value=list(actual_columns), expected_value=list(expected_columns),
                details={"missing": list(missing), "extra": list(extra)},
            )

        elif check.check_type == "custom":
            func = params.get("function")
            if func and callable(func):
                result = func(data)
                status = MonitorStatus.PASS if result.get("pass", True) else MonitorStatus.FAIL
                return MonitorResult(
                    check_id=check.check_id, check_name=check.name, status=status,
                    message=result.get("message", ""),
                    details=result,
                )

        return MonitorResult(
            check_id=check.check_id, check_name=check.name,
            status=MonitorStatus.SKIPPED, message=f"Unknown check type: {check.check_type}",
        )

    # -----------------------------------------------------------------------
    # Comprehensive assessment
    # -----------------------------------------------------------------------

    def assess_quality(self, dataset_name: str) -> QualityReport:
        """Run a comprehensive quality assessment on a dataset."""
        logger.info("Starting comprehensive quality assessment for '%s'", dataset_name)

        # Profile
        profile = self.profile_dataset(dataset_name)

        # Validate
        issues = self.validate_dataset(dataset_name)

        # Score
        score = self.compute_quality_score(dataset_name)

        # Anomalies on numeric columns
        anomalies: List[AnomalyResult] = []
        for cp in profile.columns:
            if cp.profile_type == ProfileType.NUMERIC:
                try:
                    anomaly = self.detect_anomalies(dataset_name, cp.column_name, AnomalyMethod.ZSCORE)
                    if anomaly.anomaly_count > 0:
                        anomalies.append(anomaly)
                except Exception as e:
                    logger.warning("Anomaly detection failed for column '%s': %s", cp.column_name, e)

        # Monitor checks
        monitor_results = self.run_monitor_checks(dataset_name)

        # Summary
        summary = {
            "total_issues": len(issues),
            "critical_issues": sum(1 for i in issues if i.severity == Severity.CRITICAL),
            "high_issues": sum(1 for i in issues if i.severity == Severity.HIGH),
            "medium_issues": sum(1 for i in issues if i.severity == Severity.MEDIUM),
            "low_issues": sum(1 for i in issues if i.severity == Severity.LOW),
            "anomaly_columns": len(anomalies),
            "total_anomalies": sum(a.anomaly_count for a in anomalies),
            "monitor_checks_passed": sum(1 for m in monitor_results if m.status == MonitorStatus.PASS),
            "monitor_checks_failed": sum(1 for m in monitor_results if m.status == MonitorStatus.FAIL),
            "quality_grade": self._grade_from_score(score.overall),
        }

        report = QualityReport(
            dataset_name=dataset_name,
            score=score,
            profile=profile,
            issues=issues,
            anomalies=anomalies,
            monitor_results=monitor_results,
            summary=summary,
        )
        logger.info("Assessment complete for '%s': score=%.2f, grade=%s",
                     dataset_name, score.overall, summary["quality_grade"])
        return report

    def _grade_from_score(self, score: float) -> str:
        """Convert a numeric quality score to a letter grade."""
        if score >= 0.95:
            return "A+"
        elif score >= 0.90:
            return "A"
        elif score >= 0.85:
            return "A-"
        elif score >= 0.80:
            return "B+"
        elif score >= 0.75:
            return "B"
        elif score >= 0.70:
            return "B-"
        elif score >= 0.65:
            return "C+"
        elif score >= 0.60:
            return "C"
        elif score >= 0.50:
            return "D"
        return "F"

    # -----------------------------------------------------------------------
    # Utility / status
    # -----------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent": "DataQualityAgent",
            "datasets_registered": len(self._datasets),
            "profiles_generated": len(self._profiles),
            "active_rules": sum(1 for r in self._rules if r.enabled),
            "total_rules": len(self._rules),
            "cleansing_pipelines": len(self._cleansing_pipelines),
            "monitor_checks_total": sum(len(v) for v in self._monitor_checks.values()),
            "issue_history_count": len(self._issue_history),
            "config": {
                "zscore_threshold": self._config.zscore_threshold,
                "iqr_multiplier": self._config.iqr_multiplier,
                "mad_threshold": self._config.mad_threshold,
            },
        }

    def export_report(self, report: QualityReport, format: str = "json") -> str:
        """Export a quality report to the specified format."""
        if format == "json":
            return json.dumps(report.to_dict(), indent=2, default=str)
        elif format == "summary":
            lines = [
                f"Quality Report: {report.dataset_name}",
                f"Score: {report.score.overall:.2%} ({report.summary.get('quality_grade', 'N/A')})",
                f"Rows: {report.profile.row_count if report.profile else 'N/A'}",
                f"Issues: {report.summary.get('total_issues', 0)}",
                f"  Critical: {report.summary.get('critical_issues', 0)}",
                f"  High: {report.summary.get('high_issues', 0)}",
                f"  Medium: {report.summary.get('medium_issues', 0)}",
                f"  Low: {report.summary.get('low_issues', 0)}",
                f"Anomalies: {report.summary.get('total_anomalies', 0)} across {report.summary.get('anomaly_columns', 0)} columns",
                f"Monitor checks: {report.summary.get('monitor_checks_passed', 0)} passed, {report.summary.get('monitor_checks_failed', 0)} failed",
            ]
            return "\n".join(lines)
        else:
            raise ValueError(f"Unsupported export format: {format}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Data Quality Agent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print("=" * 60)
    print("Data Quality Agent - Comprehensive Demo")
    print("=" * 60)

    agent = DataQualityAgent()

    # Create sample data
    sample_data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30, "salary": 75000, "dept": "Engineering"},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 25, "salary": 65000, "dept": "Marketing"},
        {"id": 3, "name": "Charlie", "email": None, "age": 35, "salary": 85000, "dept": "Engineering"},
        {"id": 4, "name": "Diana", "email": "diana@example.com", "age": 28, "salary": None, "dept": "Sales"},
        {"id": 5, "name": "Eve", "email": "eve@example.com", "age": 42, "salary": 95000, "dept": "Engineering"},
        {"id": 6, "name": "Frank", "email": "invalid-email", "age": -5, "salary": 55000, "dept": "Marketing"},
        {"id": 7, "name": "Grace", "email": "grace@example.com", "age": 31, "salary": 72000, "dept": "Sales"},
        {"id": 8, "name": "  Alice  ", "email": "alice@example.com", "age": 30, "salary": 75000, "dept": "Engineering"},
    ]

    # Register dataset
    result = agent.register_dataset("employees", sample_data)
    print(f"\nRegistered dataset: {result['rows']} rows, {len(result['columns'])} columns")

    # Add validation rules
    agent.add_rule(ValidationRule(
        name="email_not_null", dimension=QualityDimension.COMPLETENESS,
        severity=Severity.HIGH, column="email", rule_type="not_null",
        description="Email must not be null",
    ))
    agent.add_rule(ValidationRule(
        name="email_valid", dimension=QualityDimension.VALIDITY,
        severity=Severity.HIGH, column="email",
        rule_type="regex", parameters={"pattern": r"[^@]+@[^@]+\.[^@]+"},
        description="Email must be valid format",
    ))
    agent.add_rule(ValidationRule(
        name="age_range", dimension=QualityDimension.ACCURACY,
        severity=Severity.MEDIUM, column="age",
        rule_type="range", parameters={"min": 0, "max": 150},
        description="Age must be between 0 and 150",
    ))
    agent.add_rule(ValidationRule(
        name="unique_id", dimension=QualityDimension.UNIQUENESS,
        severity=Severity.CRITICAL, column="id", rule_type="unique",
        description="ID must be unique",
    ))

    # Run comprehensive assessment
    report = agent.assess_quality("employees")
    print(agent.export_report(report, "summary"))
    print(f"\nScore breakdown: {json.dumps(report.score.to_dict(), indent=2)}")

    # Cleansing pipeline
    pipeline_steps = [
        CleansingStep(action=CleansingAction.TRIM_WHITESPACE, column="name", order=1),
        CleansingStep(action=CleansingAction.LOWERCASE, column="email", order=2),
        CleansingStep(action=CleansingAction.DEDUPLICATE, order=3),
    ]
    agent.create_cleansing_pipeline("clean_employees", pipeline_steps)
    cleansing = agent.run_cleansing_pipeline("employees", "clean_employees")
    print(f"\nCleansing result: {json.dumps(cleansing.to_dict(), indent=2)}")

    # Agent status
    print(f"\nAgent Status: {json.dumps(agent.get_status(), indent=2)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
