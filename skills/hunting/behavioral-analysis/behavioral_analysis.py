"""
Behavioral Analysis Module
Advanced behavioral pattern analysis for threat detection
"""

from __future__ import annotations

import logging
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, time
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import uuid

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class BaselineType(Enum):
    USER_LOGIN = "user_login"
    PROCESS_EXECUTION = "process_execution"
    NETWORK_FLOW = "network_flow"
    FILE_ACCESS = "file_access"
    DATA_TRANSFER = "data_transfer"
    APPLICATION_USAGE = "application_usage"


class BehaviorDimension(Enum):
    LOGIN_TIMES = "login_times"
    ACCESS_PATTERNS = "access_patterns"
    DATA_TRANSFER = "data_transfer"
    APPLICATION_USAGE = "application_usage"
    NETWORK_BEHAVIOR = "network_behavior"
    FILE_OPERATIONS = "file_operations"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnomalyType(Enum):
    STATISTICAL = "statistical"
    TEMPORAL = "temporal"
    BEHAVIORAL = "behavioral"
    CONTEXTUAL = "contextual"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Baseline:
    """Behavioral baseline for an entity."""
    entity_id: str
    baseline_type: BaselineType
    mean: float = 0.0
    std_dev: float = 0.0
    min_value: float = 0.0
    max_value: float = 0.0
    sample_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    histogram: Dict[str, int] = field(default_factory=dict)
    percentiles: Dict[int, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def z_score(self, value: float) -> float:
        if self.std_dev == 0:
            return 0.0
        return (value - self.mean) / self.std_dev

    def is_anomaly(self, value: float, threshold: float = 3.0) -> bool:
        return abs(self.z_score(value)) > threshold


@dataclass
class Anomaly:
    """Detected behavioral anomaly."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: str = ""
    anomaly_type: AnomalyType = AnomalyType.STATISTICAL
    description: str = ""
    severity: RiskLevel = RiskLevel.LOW
    confidence: int = 50
    detected_at: datetime = field(default_factory=datetime.utcnow)
    expected_value: float = 0.0
    observed_value: float = 0.0
    deviation_sigma: float = 0.0
    affected_dimensions: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    recommended_action: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "entity_id": self.entity_id,
            "type": self.anomaly_type.value,
            "description": self.description,
            "severity": self.severity.value,
            "confidence": self.confidence,
            "detected_at": self.detected_at.isoformat(),
            "expected": self.expected_value,
            "observed": self.observed_value,
            "deviation": self.deviation_sigma,
        }


@dataclass
class UserProfile:
    """Behavioral profile for a user."""
    user_id: str = ""
    typical_login_start: str = "09:00"
    typical_login_end: str = "17:00"
    avg_session_hours: float = 8.0
    top_resources: List[str] = field(default_factory=list)
    baseline_anomaly_score: float = 0.0
    login_time_distribution: Dict[int, int] = field(default_factory=dict)
    access_pattern: Dict[str, int] = field(default_factory=dict)
    data_transfer_baseline: float = 0.0
    last_updated: datetime = field(default_factory=datetime.utcnow)
    total_sessions: int = 0
    anomaly_history: List[Anomaly] = field(default_factory=list)


@dataclass
class ProcessBehavior:
    """Behavioral analysis result for a process."""
    process_name: str = ""
    command_line: str = ""
    parent_process: str = ""
    pid: int = 0
    risk_score: int = 0
    indicators: List[str] = field(default_factory=list)
    recommended_action: str = "monitor"
    behavior_features: Dict[str, Any] = field(default_factory=dict)
    analyzed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class NetworkFlow特征:
    """Network flow behavioral analysis."""
    src_ip: str = ""
    dst_ip: str = ""
    dst_port: int = 0
    protocol: str = ""
    bytes_sent: int = 0
    bytes_received: int = 0
    duration_seconds: float = 0.0
    risk_level: RiskLevel = RiskLevel.LOW
    anomaly_indicators: List[str] = field(default_factory=list)
    baseline_deviation: float = 0.0
    flow_features: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BehavioralEvent:
    """A single behavioral event."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: str = ""
    event_type: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    dimensions: Dict[str, float] = field(default_factory=dict)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    source: str = ""


@dataclass
class DataCollectorConfig:
    """Configuration for data collection."""
    sources: List[str] = field(default_factory=list)
    collection_interval_minutes: int = 5
    retention_days: int = 90
    batch_size: int = 1000


# ---------------------------------------------------------------------------
# Statistical Helpers
# ---------------------------------------------------------------------------

def compute_statistics(values: List[float]) -> Dict[str, float]:
    if not values:
        return {"mean": 0.0, "std_dev": 0.0, "min": 0.0, "max": 0.0}
    return {
        "mean": statistics.mean(values),
        "std_dev": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def compute_percentiles(values: List[float], percentiles: List[int] = None) -> Dict[int, float]:
    if percentiles is None:
        percentiles = [10, 25, 50, 75, 90, 95, 99]
    if not values:
        return {}
    sorted_vals = sorted(values)
    result = {}
    for p in percentiles:
        idx = int(len(sorted_vals) * p / 100)
        idx = min(idx, len(sorted_vals) - 1)
        result[p] = sorted_vals[idx]
    return result


# ---------------------------------------------------------------------------
# Data Collector
# ---------------------------------------------------------------------------

class DataCollector:
    """Collects behavioral data from various sources."""

    def __init__(self, sources: Optional[List[str]] = None) -> None:
        self.sources = sources or []
        self._collection_buffer: List[BehavioralEvent] = []

    def collect(self, hours: int = 24) -> List[BehavioralEvent]:
        logger.info("Collecting data from %d sources for last %d hours", len(self.sources), hours)
        # In production, this would query actual data sources
        events = []
        for source in self.sources:
            events.extend(self._collect_from_source(source, hours))
        return events

    def _collect_from_source(self, source: str, hours: int) -> List[BehavioralEvent]:
        # Placeholder for actual data collection
        return []

    def add_event(self, event: BehavioralEvent) -> None:
        self._collection_buffer.append(event)

    def flush_buffer(self) -> List[BehavioralEvent]:
        events = self._collection_buffer.copy()
        self._collection_buffer.clear()
        return events


# ---------------------------------------------------------------------------
# Behavioral Engine
# ---------------------------------------------------------------------------

class BehavioralEngine:
    """Main engine for behavioral analysis."""

    def __init__(self, window_days: int = 30, sensitivity: float = 0.8) -> None:
        self.window_days = window_days
        self.sensitivity = sensitivity
        self._baselines: Dict[str, Baseline] = {}
        self._anomalies: List[Anomaly] = []
        self._event_history: Dict[str, List[BehavioralEvent]] = defaultdict(list)

    def create_baseline(
        self,
        entity_id: str,
        baseline_type: BaselineType,
        data: List[Any],
    ) -> Baseline:
        key = f"{entity_id}:{baseline_type.value}"
        values = self._extract_numeric_values(data)
        stats = compute_statistics(values) if values else {"mean": 0.0, "std_dev": 0.0, "min": 0.0, "max": 0.0}
        percentiles = compute_percentiles(values) if values else {}

        baseline = Baseline(
            entity_id=entity_id,
            baseline_type=baseline_type,
            mean=stats["mean"],
            std_dev=stats["std_dev"],
            min_value=stats["min"],
            max_value=stats["max"],
            sample_count=len(values),
            percentiles=percentiles,
        )
        self._baselines[key] = baseline
        logger.info("Created baseline for %s (%s) with %d samples", entity_id, baseline_type.value, len(values))
        return baseline

    def _extract_numeric_values(self, data: List[Any]) -> List[float]:
        values = []
        for item in data:
            if isinstance(item, (int, float)):
                values.append(float(item))
            elif isinstance(item, dict):
                for v in item.values():
                    if isinstance(v, (int, float)):
                        values.append(float(v))
                        break
        return values

    def detect_anomalies(self, events: List[BehavioralEvent]) -> List[Anomaly]:
        anomalies = []
        for event in events:
            for dim_name, dim_value in event.dimensions.items():
                key = f"{event.entity_id}:{dim_name}"
                baseline = self._baselines.get(key)
                if baseline and baseline.sample_count > 10:
                    z = baseline.z_score(dim_value)
                    threshold = 3.0 / self.sensitivity
                    if abs(z) > threshold:
                        severity = self._classify_severity(abs(z))
                        anomaly = Anomaly(
                            entity_id=event.entity_id,
                            anomaly_type=AnomalyType.STATISTICAL,
                            description=f"Anomalous {dim_name}: {dim_value} (z-score: {z:.2f})",
                            severity=severity,
                            confidence=min(int(abs(z) * 20), 100),
                            expected_value=baseline.mean,
                            observed_value=dim_value,
                            deviation_sigma=z,
                            affected_dimensions=[dim_name],
                        )
                        anomalies.append(anomaly)
        self._anomalies.extend(anomalies)
        return anomalies

    def _classify_severity(self, deviation: float) -> RiskLevel:
        if deviation >= 5.0:
            return RiskLevel.CRITICAL
        elif deviation >= 4.0:
            return RiskLevel.HIGH
        elif deviation >= 3.0:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def get_entity_anomalies(self, entity_id: str) -> List[Anomaly]:
        return [a for a in self._anomalies if a.entity_id == entity_id]

    def get_baseline(self, entity_id: str, baseline_type: BaselineType) -> Optional[Baseline]:
        key = f"{entity_id}:{baseline_type.value}"
        return self._baselines.get(key)

    def update_baseline(self, entity_id: str, baseline_type: BaselineType, new_value: float) -> None:
        key = f"{entity_id}:{baseline_type.value}"
        baseline = self._baselines.get(key)
        if baseline:
            n = baseline.sample_count
            new_mean = (baseline.mean * n + new_value) / (n + 1)
            new_std = math.sqrt(
                ((baseline.std_dev ** 2 * n) + (new_value - baseline.mean) * (new_value - new_mean)) / (n + 1)
            )
            baseline.mean = new_mean
            baseline.std_dev = new_std
            baseline.sample_count = n + 1
            baseline.updated_at = datetime.utcnow()


# ---------------------------------------------------------------------------
# User Profiler
# ---------------------------------------------------------------------------

class UserProfiler:
    """Builds and scores user behavioral profiles."""

    def __init__(self, learning_period_days: int = 90) -> None:
        self.learning_period_days = learning_period_days
        self._profiles: Dict[str, UserProfile] = {}

    def build_profile(self, user_id: str, dimensions: Optional[List[BehaviorDimension]] = None) -> UserProfile:
        profile = UserProfile(user_id=user_id)
        # In production, this would analyze historical data
        profile.typical_login_start = "08:30"
        profile.typical_login_end = "17:30"
        profile.avg_session_hours = 8.5
        profile.baseline_anomaly_score = 0.15
        profile.total_sessions = 150
        self._profiles[user_id] = profile
        return profile

    def score_activity(self, user_id: str, activity: Dict[str, Any]) -> float:
        profile = self._profiles.get(user_id)
        if profile is None:
            return 0.5  # Unknown user, moderate score

        score = profile.baseline_anomaly_score

        # Check login time anomaly
        login_time = activity.get("login_time")
        if login_time:
            try:
                hour = int(login_time.split(":")[0])
                if hour < 6 or hour > 22:
                    score += 0.2
            except (ValueError, IndexError):
                pass

        # Check source IP anomaly
        source_ip = activity.get("source_ip")
        if source_ip and source_ip not in profile.access_pattern:
            score += 0.15

        return min(1.0, score)

    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        return self._profiles.get(user_id)


# ---------------------------------------------------------------------------
# Process Analyzer
# ---------------------------------------------------------------------------

class ProcessAnalyzer:
    """Analyzes process behavior for anomalies and threats."""

    KNOWN_SUSPICIOUS_PATTERNS = [
        ("powershell.exe", "-enc"),
        ("cmd.exe", "/c whoami"),
        ("certutil.exe", "-urlcache"),
        ("bitsadmin.exe", "/transfer"),
        ("mshta.exe", "http"),
        ("wscript.exe", "http"),
        ("cscript.exe", "http"),
        ("regsvr32.exe", "/s /n /u /i"),
    ]

    def __init__(self) -> None:
        self._process_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def analyze(
        self,
        process_name: str,
        command_line: str = "",
        parent_process: str = "",
        pid: int = 0,
    ) -> ProcessBehavior:
        risk_score = 0
        indicators = []

        # Check suspicious patterns
        cmd_lower = command_line.lower()
        for sus_proc, sus_pattern in self.KNOWN_SUSPICIOUS_PATTERNS:
            if sus_proc.lower() == process_name.lower() and sus_pattern.lower() in cmd_lower:
                indicators.append(f"Suspicious {process_name} pattern: {sus_pattern}")
                risk_score += 40

        # Check for encoded commands
        if "-enc" in cmd_lower or "-EncodedCommand" in cmd_lower:
            indicators.append("Encoded PowerShell command detected")
            risk_score += 30

        # Check for download cradles
        download_patterns = ["Invoke-WebRequest", "Invoke-Expression", "IEX", "DownloadString", "Net.WebClient"]
        for pattern in download_patterns:
            if pattern.lower() in cmd_lower:
                indicators.append(f"Download cradle pattern: {pattern}")
                risk_score += 25
                break

        # Parent process anomalies
        suspicious_parents = {"winword.exe", "excel.exe", "outlook.exe", "powerpnt.exe"}
        if parent_process.lower() in suspicious_parents and process_name.lower() in ("cmd.exe", "powershell.exe"):
            indicators.append(f"Suspicious parent-child: {parent_process} -> {process_name}")
            risk_score += 35

        risk_score = min(100, risk_score)

        if risk_score >= 80:
            action = "isolate_and_investigate"
        elif risk_score >= 50:
            action = "alert_and_monitor"
        elif risk_score >= 25:
            action = "monitor"
        else:
            action = "allow"

        return ProcessBehavior(
            process_name=process_name,
            command_line=command_line,
            parent_process=parent_process,
            pid=pid,
            risk_score=risk_score,
            indicators=indicators,
            recommended_action=action,
        )

    def trigger_alert(self, behavior: ProcessBehavior, priority: str = "medium") -> None:
        logger.warning(
            "PROCESS ALERT [%s]: %s (PID %d) — Risk: %d — Indicators: %s",
            priority, behavior.process_name, behavior.pid,
            behavior.risk_score, behavior.indicators,
        )


# ---------------------------------------------------------------------------
# Network Behavior Analyzer
# ---------------------------------------------------------------------------

class NetworkBehaviorAnalyzer:
    """Analyzes network flow behavior."""

    def __init__(self) -> None:
        self._flow_baselines: Dict[str, Baseline] = {}

    def analyze_flow(
        self,
        src_ip: str,
        dst_ip: str,
        dst_port: int,
        protocol: str,
        bytes_sent: int,
        bytes_received: int,
        duration_seconds: float,
    ) -> NetworkFlow特征:
        risk_level = RiskLevel.LOW
        indicators = []
        deviation = 0.0

        # Large data exfiltration indicator
        if bytes_received > 10 * 1024 * 1024:  # > 10MB received
            indicators.append("Large data transfer detected")
            risk_level = RiskLevel.MEDIUM
            deviation = 2.5

        # Unusual port usage
        well_known_ports = {80, 443, 53, 25, 110, 143, 993, 995}
        if dst_port not in well_known_ports and dst_port > 1024:
            indicators.append(f"Non-standard port: {dst_port}")
            deviation = max(deviation, 1.5)

        # Very long duration
        if duration_seconds > 3600:
            indicators.append(f"Long-duration connection: {duration_seconds:.0f}s")
            deviation = max(deviation, 2.0)

        # C2 beacon pattern (small periodic transfers)
        if 100 < bytes_sent < 1000 and duration_seconds < 60:
            indicators.append("Possible C2 beacon pattern")
            risk_level = RiskLevel.HIGH
            deviation = max(deviation, 3.5)

        return NetworkFlow特征(
            src_ip=src_ip,
            dst_ip=dst_ip,
            dst_port=dst_port,
            protocol=protocol,
            bytes_sent=bytes_sent,
            bytes_received=bytes_received,
            duration_seconds=duration_seconds,
            risk_level=risk_level,
            anomaly_indicators=indicators,
            baseline_deviation=deviation,
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the behavioral analysis module."""
    print("=" * 60)
    print("  Behavioral Analysis Module — Demo")
    print("=" * 60)

    # Initialize engine
    engine = BehavioralEngine(window_days=30, sensitivity=0.8)

    # Create baselines
    baseline = engine.create_baseline(
        entity_id="user-jsmith",
        baseline_type=BaselineType.USER_LOGIN,
        data=[8.0, 8.5, 9.0, 8.2, 8.8, 7.5, 9.2, 8.1, 8.7, 8.3],
    )
    print(f"\n[+] Baseline created for user-jsmith:")
    print(f"    Mean: {baseline.mean:.2f} hours")
    print(f"    Std Dev: {baseline.std_dev:.2f}")
    print(f"    Sample Count: {baseline.sample_count}")

    # User profiling
    profiler = UserProfiler(learning_period_days=90)
    profile = profiler.build_profile(user_id="jsmith")
    print(f"\n[+] User Profile for jsmith:")
    print(f"    Login Window: {profile.typical_login_start} - {profile.typical_login_end}")
    print(f"    Avg Session: {profile.avg_session_hours:.1f} hours")
    print(f"    Baseline Anomaly Score: {profile.baseline_anomaly_score:.2f}")

    # Score anomalous activity
    anomaly_score = profiler.score_activity(
        user_id="jsmith",
        activity={"login_time": "03:45", "source_ip": "198.51.100.99"},
    )
    print(f"    Anomalous Activity Score: {anomaly_score:.2f}")

    # Process analysis
    proc_analyzer = ProcessAnalyzer()
    proc_behavior = proc_analyzer.analyze(
        process_name="powershell.exe",
        command_line="powershell.exe -enc SQBmACgA...",
        parent_process="winword.exe",
        pid=4532,
    )
    print(f"\n[+] Process Analysis:")
    print(f"    Process: {proc_behavior.process_name} (PID {proc_behavior.pid})")
    print(f"    Risk Score: {proc_behavior.risk_score}")
    print(f"    Indicators: {proc_behavior.indicators}")
    print(f"    Recommended Action: {proc_behavior.recommended_action}")

    # Network flow analysis
    net_analyzer = NetworkBehaviorAnalyzer()
    flow_result = net_analyzer.analyze_flow(
        src_ip="10.0.1.100",
        dst_ip="198.51.100.42",
        dst_port=443,
        protocol="tcp",
        bytes_sent=512,
        bytes_received=2048,
        duration_seconds=30,
    )
    print(f"\n[+] Network Flow Analysis:")
    print(f"    {flow_result.src_ip} -> {flow_result.dst_ip}:{flow_result.dst_port}")
    print(f"    Risk Level: {flow_result.risk_level.value}")
    print(f"    Baseline Deviation: {flow_result.baseline_deviation:.2f}σ")
    print(f"    Indicators: {flow_result.anomaly_indicators}")

    # Engine statistics
    print(f"\n[+] Engine Statistics:")
    print(f"    Baselines: {len(engine._baselines)}")
    print(f"    Anomalies Detected: {len(engine._anomalies)}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
