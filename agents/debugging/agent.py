"""
Debugging Agent - Debugging methodologies, root cause analysis, logging strategies, profiling, tracing, and error resolution.

Provides systematic debugging capabilities including error classification, stack trace analysis,
root cause analysis using structured methodologies, performance profiling, distributed tracing
simulation, logging strategy optimization, and automated fix suggestion generation.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import re
import statistics
import time
import traceback
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
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

class ErrorCategory(Enum):
    """Classification of error types."""
    RUNTIME = "runtime"
    TYPE_ERROR = "type_error"
    REFERENCE_ERROR = "reference_error"
    SYNTAX_ERROR = "syntax_error"
    LOGIC_ERROR = "logic_error"
    PERFORMANCE = "performance"
    MEMORY = "memory"
    NETWORK = "network"
    CONCURRENCY = "concurrency"
    SECURITY = "security"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    DATA = "data"
    PERMISSION = "permission"
    TIMEOUT = "timeout"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    UNKNOWN = "unknown"


class Severity(Enum):
    """Severity level for issues."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class DebugPhase(Enum):
    """Phases of the debugging methodology."""
    REPRODUCE = "reproduce"
    ISOLATE = "isolate"
    HYPOTHESIZE = "hypothesize"
    INVESTIGATE = "investigate"
    FIX = "fix"
    VERIFY = "verify"
    PREVENT = "prevent"


class ProfilingType(Enum):
    """Types of profiling operations."""
    CPU = "cpu"
    MEMORY = "memory"
    IO = "io"
    NETWORK = "network"
    DATABASE = "database"
    FUNCTION = "function"
    LINE = "line"
    OBJECT = "object"


class TraceSpanStatus(Enum):
    """Status of a trace span."""
    OK = "ok"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class LogStrategy(Enum):
    """Logging strategy recommendations."""
    STRUCTURED = "structured"
    LEVELED = "leveled"
    CORRELATED = "correlated"
    SAMPLING = "sampling"
    REDACTION = "redaction"
    AGGREGATION = "aggregation"
    REALTIME = "realtime"
    BUFFERED = "buffered"


class FixType(Enum):
    """Types of suggested fixes."""
    CODE_CHANGE = "code_change"
    CONFIG_CHANGE = "config_change"
    DEPENDENCY_UPDATE = "dependency_update"
    INFRASTRUCTURE = "infrastructure"
    WORKAROUND = "workaround"
    ARCHITECTURE = "architecture"
    MONITORING = "monitoring"
    DOCUMENTATION = "documentation"


class RootCauseCategory(Enum):
    """Categories for root cause analysis."""
    CODE_DEFECT = "code_defect"
    DESIGN_FLAW = "design_flaw"
    CONFIGURATION_ERROR = "configuration_error"
    DEPENDENCY_FAILURE = "dependency_failure"
    RESOURCE_LIMIT = "resource_limit"
    CONCURRENCY_ISSUE = "concurrency_issue"
    DATA_CORRUPTION = "data_corruption"
    SECURITY_VULNERABILITY = "security_vulnerability"
    EXTERNAL_DEPENDENCY = "external_dependency"
    HUMAN_ERROR = "human_error"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ErrorInfo:
    """Parsed information from an error or exception."""
    error_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    category: ErrorCategory = ErrorCategory.UNKNOWN
    severity: Severity = Severity.MEDIUM
    message: str = ""
    error_type: str = ""
    stack_trace: str = ""
    source_file: str = ""
    source_line: int = 0
    source_function: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    context: Dict[str, Any] = field(default_factory=dict)
    stack_frames: List[Dict[str, Any]] = field(default_factory=list)
    first_occurrence: Optional[datetime] = None
    occurrence_count: int = 1
    resolved: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_id": self.error_id,
            "category": self.category.value,
            "severity": self.severity.value,
            "message": self.message,
            "error_type": self.error_type,
            "stack_trace": self.stack_trace[:2000],
            "source_file": self.source_file,
            "source_line": self.source_line,
            "source_function": self.source_function,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context,
            "stack_frames": self.stack_frames[:20],
            "occurrence_count": self.occurrence_count,
            "resolved": self.resolved,
        }


@dataclass
class RootCauseAnalysis:
    """Result of a root cause analysis investigation."""
    analysis_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    issue_description: str = ""
    category: RootCauseCategory = RootCauseCategory.UNKNOWN
    root_cause: str = ""
    contributing_factors: List[str] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    hypothesis: str = ""
    confirmed: bool = False
    confidence: float = 0.0
    phases_completed: List[str] = field(default_factory=list)
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "analysis_id": self.analysis_id,
            "issue_description": self.issue_description,
            "category": self.category.value,
            "root_cause": self.root_cause,
            "contributing_factors": self.contributing_factors,
            "evidence": self.evidence[:20],
            "hypothesis": self.hypothesis,
            "confirmed": self.confirmed,
            "confidence": round(self.confidence, 2),
            "phases_completed": self.phases_completed,
            "timeline": self.timeline[:30],
            "recommendations": self.recommendations,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ProfileResult:
    """Result of a profiling operation."""
    profile_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    profiling_type: ProfilingType = ProfilingType.CPU
    duration_seconds: float = 0.0
    samples: int = 0
    top_functions: List[Dict[str, Any]] = field(default_factory=list)
    hotspots: List[Dict[str, Any]] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "profiling_type": self.profiling_type.value,
            "duration_seconds": round(self.duration_seconds, 3),
            "samples": self.samples,
            "top_functions": self.top_functions[:20],
            "hotspots": self.hotspots[:20],
            "summary": self.summary,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class TraceSpan:
    """A single span in a distributed trace."""
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    trace_id: str = ""
    parent_span_id: Optional[str] = None
    operation: str = ""
    service: str = ""
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    status: TraceSpanStatus = TraceSpanStatus.OK
    tags: Dict[str, str] = field(default_factory=dict)
    logs: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent_span_id": self.parent_span_id,
            "operation": self.operation,
            "service": self.service,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": round(self.duration_ms, 2),
            "status": self.status.value,
            "tags": self.tags,
            "error": self.error,
        }


@dataclass
class TraceAnalysis:
    """Analysis of a distributed trace."""
    trace_id: str = ""
    total_duration_ms: float = 0.0
    span_count: int = 0
    error_spans: int = 0
    slowest_spans: List[Dict[str, Any]] = field(default_factory=list)
    critical_path: List[str] = field(default_factory=list)
    bottleneck_service: str = ""
    bottleneck_operation: str = ""
    service_breakdown: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "total_duration_ms": round(self.total_duration_ms, 2),
            "span_count": self.span_count,
            "error_spans": self.error_spans,
            "slowest_spans": self.slowest_spans[:10],
            "critical_path": self.critical_path,
            "bottleneck_service": self.bottleneck_service,
            "bottleneck_operation": self.bottleneck_operation,
            "service_breakdown": {k: round(v, 2) for k, v in self.service_breakdown.items()},
            "recommendations": self.recommendations,
        }


@dataclass
class LogEntry:
    """A structured log entry."""
    entry_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    level: str = "INFO"
    message: str = ""
    source: str = ""
    function: str = ""
    line: int = 0
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "message": self.message,
            "source": self.source,
            "function": self.function,
            "line": self.line,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "extra": self.extra,
            "error": self.error,
        }


@dataclass
class LogAnalysis:
    """Analysis of log patterns and issues."""
    total_entries: int = 0
    by_level: Dict[str, int] = field(default_factory=dict)
    error_patterns: List[Dict[str, Any]] = field(default_factory=list)
    frequent_messages: List[Dict[str, Any]] = field(default_factory=list)
    time_distribution: Dict[str, int] = field(default_factory=dict)
    correlated_errors: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_entries": self.total_entries,
            "by_level": self.by_level,
            "error_patterns": self.error_patterns[:20],
            "frequent_messages": self.frequent_messages[:20],
            "time_distribution": self.time_distribution,
            "correlated_errors": self.correlated_errors[:10],
            "recommendations": self.recommendations,
        }


@dataclass
class FixSuggestion:
    """A suggested fix for a debugging issue."""
    fix_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    fix_type: FixType = FixType.CODE_CHANGE
    title: str = ""
    description: str = ""
    affected_files: List[str] = field(default_factory=list)
    code_change: Optional[str] = None
    confidence: float = 0.0
    risk_level: Severity = Severity.LOW
    prerequisites: List[str] = field(default_factory=list)
    testing_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fix_id": self.fix_id,
            "fix_type": self.fix_type.value,
            "title": self.title,
            "description": self.description,
            "affected_files": self.affected_files,
            "code_change": self.code_change,
            "confidence": round(self.confidence, 2),
            "risk_level": self.risk_level.value,
            "prerequisites": self.prerequisites,
            "testing_notes": self.testing_notes,
        }


@dataclass
class DebugSession:
    """A complete debugging session tracking all activities."""
    session_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    issue_title: str = ""
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: Optional[datetime] = None
    current_phase: DebugPhase = DebugPhase.REPRODUCE
    errors: List[ErrorInfo] = field(default_factory=list)
    root_cause: Optional[RootCauseAnalysis] = None
    profiles: List[ProfileResult] = field(default_factory=list)
    traces: List[TraceAnalysis] = field(default_factory=list)
    log_analysis: Optional[LogAnalysis] = None
    fixes: List[FixSuggestion] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    status: str = "active"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "issue_title": self.issue_title,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "current_phase": self.current_phase.value,
            "errors_count": len(self.errors),
            "root_cause": self.root_cause.to_dict() if self.root_cause else None,
            "profiles_count": len(self.profiles),
            "traces_count": len(self.traces),
            "fixes_count": len(self.fixes),
            "notes_count": len(self.notes),
            "status": self.status,
        }


@dataclass
class LoggingConfig:
    """Configuration for logging strategy analysis."""
    current_level: str = "INFO"
    format: str = "text"
    structured: bool = False
    correlation_ids: bool = False
    sampling_rate: float = 1.0
    redaction_patterns: List[str] = field(default_factory=list)
    output_targets: List[str] = field(default_factory=lambda: ["console"])
    retention_days: int = 30
    alert_on_error: bool = True
    performance_logging: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "current_level": self.current_level,
            "format": self.format,
            "structured": self.structured,
            "correlation_ids": self.correlation_ids,
            "sampling_rate": self.sampling_rate,
            "redaction_patterns": self.redaction_patterns,
            "output_targets": self.output_targets,
            "retention_days": self.retention_days,
            "alert_on_error": self.alert_on_error,
            "performance_logging": self.performance_logging,
        }


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class DebuggingConfig:
    """Configuration for the Debugging Agent."""
    max_stack_frames: int = 50
    max_error_history: int = 1000
    max_log_entries: int = 10000
    slow_threshold_ms: float = 1000.0
    very_slow_threshold_ms: float = 5000.0
    memory_warning_mb: float = 512.0
    memory_critical_mb: float = 1024.0
    cpu_warning_percent: float = 70.0
    cpu_critical_percent: float = 90.0
    io_warning_ms: float = 100.0
    io_critical_ms: float = 500.0
    min_samples_for_analysis: int = 10
    confidence_threshold: float = 0.7
    max_hypotheses: int = 5
    enable_auto_categorization: bool = True
    enable_pattern_detection: bool = True
    enable_correlation: bool = True
    known_error_patterns: Dict[str, ErrorCategory] = field(default_factory=lambda: {
        "NullReferenceException": ErrorCategory.REFERENCE_ERROR,
        "TypeError": ErrorCategory.TYPE_ERROR,
        "ValueError": ErrorCategory.DATA,
        "KeyError": ErrorCategory.DATA,
        "IndexError": ErrorCategory.DATA,
        "AttributeError": ErrorCategory.RUNTIME,
        "ImportError": ErrorCategory.DEPENDENCY,
        "ModuleNotFoundError": ErrorCategory.DEPENDENCY,
        "ConnectionError": ErrorCategory.NETWORK,
        "TimeoutError": ErrorCategory.TIMEOUT,
        "MemoryError": ErrorCategory.MEMORY,
        "PermissionError": ErrorCategory.PERMISSION,
        "FileNotFoundError": ErrorCategory.DATA,
        "IOError": ErrorCategory.IO,
        "OSError": ErrorCategory.RESOURCE_EXHAUSTION,
        "RecursionError": ErrorCategory.RUNTIME,
        "AssertionError": ErrorCategory.LOGIC_ERROR,
        "RuntimeError": ErrorCategory.RUNTIME,
        "SyntaxError": ErrorCategory.SYNTAX_ERROR,
        "StopIteration": ErrorCategory.RUNTIME,
        "UnicodeDecodeError": ErrorCategory.DATA,
        "JSONDecodeError": ErrorCategory.DATA,
        "KeyboardInterrupt": ErrorCategory.RUNTIME,
        "SystemExit": ErrorCategory.RUNTIME,
    })


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _parse_stack_trace(stack_trace: str) -> List[Dict[str, Any]]:
    """Parse a stack trace string into structured frames."""
    frames = []
    lines = stack_trace.strip().split("\n")
    for line in lines:
        line = line.strip()
        # Python-style: File "path", line N, in function
        match = re.match(r'File "([^"]+)", line (\d+), in (\w+)', line)
        if match:
            frames.append({
                "file": match.group(1),
                "line": int(match.group(2)),
                "function": match.group(3),
            })
        # JavaScript-style: at function (file:line:col)
        match = re.match(r'at (\S+) \(([^:]+):(\d+):(\d+)\)', line)
        if match:
            frames.append({
                "function": match.group(1),
                "file": match.group(2),
                "line": int(match.group(3)),
                "column": int(match.group(4)),
            })
        # Simple: at file:line
        match = re.match(r'at ([^:]+):(\d+)', line)
        if match:
            frames.append({
                "file": match.group(1),
                "line": int(match.group(2)),
            })
    return frames


def _classify_error(error_type: str, message: str, config: DebuggingConfig) -> ErrorCategory:
    """Classify an error based on its type and message."""
    if error_type in config.known_error_patterns:
        return config.known_error_patterns[error_type]
    msg_lower = message.lower()
    if "timeout" in msg_lower:
        return ErrorCategory.TIMEOUT
    if "connection" in msg_lower or "network" in msg_lower:
        return ErrorCategory.NETWORK
    if "memory" in msg_lower or "heap" in msg_lower:
        return ErrorCategory.MEMORY
    if "permission" in msg_lower or "access denied" in msg_lower:
        return ErrorCategory.PERMISSION
    if "config" in msg_lower or "setting" in msg_lower:
        return ErrorCategory.CONFIGURATION
    return ErrorCategory.UNKNOWN


def _determine_severity(category: ErrorCategory, context: Dict[str, Any]) -> Severity:
    """Determine severity based on error category and context."""
    critical_categories = {ErrorCategory.MEMORY, ErrorCategory.SECURITY, ErrorCategory.DATA_CORRUPTION if hasattr(ErrorCategory, 'DATA_CORRUPTION') else ErrorCategory.DATA}
    high_categories = {ErrorCategory.NETWORK, ErrorCategory.CONCURRENCY, ErrorCategory.RESOURCE_EXHAUSTION, ErrorCategory.TIMEOUT}
    if category in critical_categories:
        return Severity.CRITICAL
    if category in high_categories:
        return Severity.HIGH
    if category in {ErrorCategory.RUNTIME, ErrorCategory.TYPE_ERROR, ErrorCategory.REFERENCE_ERROR}:
        return Severity.MEDIUM
    return Severity.LOW


def _compute_entropy(values: List[str]) -> float:
    """Compute Shannon entropy of a value distribution."""
    if not values:
        return 0.0
    counter = Counter(values)
    n = len(values)
    return -sum((c / n) * math.log2(c / n) for c in counter.values())


def _find_common_pattern(strings: List[str]) -> Optional[str]:
    """Find the longest common prefix pattern in a list of strings."""
    if not strings:
        return None
    prefix = strings[0]
    for s in strings[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return None
    return prefix if len(prefix) > 3 else None


# ---------------------------------------------------------------------------
# Core Agent
# ---------------------------------------------------------------------------

class DebuggingAgent:
    """
    Enterprise-grade Debugging Agent providing systematic debugging methodology,
    root cause analysis, performance profiling, distributed tracing, logging
    strategy optimization, and automated fix suggestion generation.
    """

    def __init__(self, config: Optional[DebuggingConfig] = None):
        self._config = config or DebuggingConfig()
        self._sessions: Dict[str, DebugSession] = {}
        self._error_history: List[ErrorInfo] = []
        self._error_index: Dict[str, ErrorInfo] = {}
        self._log_entries: List[LogEntry] = []
        self._trace_store: Dict[str, List[TraceSpan]] = defaultdict(list)
        self._profiles: List[ProfileResult] = []
        logger.info("DebuggingAgent initialized")

    # -----------------------------------------------------------------------
    # Session Management
    # -----------------------------------------------------------------------

    def create_session(self, issue_title: str) -> DebugSession:
        """Create a new debugging session."""
        session = DebugSession(issue_title=issue_title)
        self._sessions[session.session_id] = session
        logger.info("Created debugging session '%s' for: %s", session.session_id, issue_title)
        return session

    def get_session(self, session_id: str) -> DebugSession:
        """Retrieve a debugging session."""
        if session_id not in self._sessions:
            raise KeyError(f"Session '{session_id}' not found")
        return self._sessions[session_id]

    def advance_phase(self, session_id: str, phase: DebugPhase) -> DebugSession:
        """Advance a debugging session to the next phase."""
        session = self.get_session(session_id)
        session.current_phase = phase
        logger.info("Session '%s' advanced to phase: %s", session_id, phase.value)
        return session

    def end_session(self, session_id: str) -> DebugSession:
        """End a debugging session."""
        session = self.get_session(session_id)
        session.ended_at = datetime.now(timezone.utc)
        session.status = "completed"
        logger.info("Session '%s' ended", session_id)
        return session

    def list_sessions(self, status: Optional[str] = None) -> List[DebugSession]:
        """List debugging sessions."""
        sessions = list(self._sessions.values())
        if status:
            sessions = [s for s in sessions if s.status == status]
        return sessions

    # -----------------------------------------------------------------------
    # Error Analysis
    # -----------------------------------------------------------------------

    def analyze_error(
        self,
        error_message: str,
        error_type: str = "",
        stack_trace: str = "",
        context: Optional[Dict[str, Any]] = None,
    ) -> ErrorInfo:
        """Analyze an error and classify it with structured information."""
        category = ErrorCategory.UNKNOWN
        if self._config.enable_auto_categorization and error_type:
            category = _classify_error(error_type, error_message, self._config)

        severity = _determine_severity(category, context or {})
        frames = _parse_stack_trace(stack_trace) if stack_trace else []

        source_file = ""
        source_line = 0
        source_function = ""
        if frames:
            last_app_frame = next(
                (f for f in frames if not f.get("file", "").startswith("<")),
                frames[0],
            )
            source_file = last_app_frame.get("file", "")
            source_line = last_app_frame.get("line", 0)
            source_function = last_app_frame.get("function", "")

        error = ErrorInfo(
            category=category,
            severity=severity,
            message=error_message,
            error_type=error_type,
            stack_trace=stack_trace[:5000],
            source_file=source_file,
            source_line=source_line,
            source_function=source_function,
            context=context or {},
            stack_frames=frames[:self._config.max_stack_frames],
        )

        # Check for recurring errors
        error_key = f"{error_type}:{error_message[:100]}"
        if error_key in self._error_index:
            existing = self._error_index[error_key]
            existing.occurrence_count += 1
            error = existing
        else:
            self._error_index[error_key] = error
            self._error_history.append(error)

        self._error_history = self._error_history[-self._config.max_error_history:]
        logger.info("Error analyzed: [%s] %s (category=%s, severity=%s)",
                     error_type, error_message[:80], category.value, severity.value)
        return error

    def get_error_history(
        self,
        category: Optional[ErrorCategory] = None,
        severity: Optional[Severity] = None,
        limit: int = 50,
    ) -> List[ErrorInfo]:
        """Get error history with optional filters."""
        errors = self._error_history
        if category:
            errors = [e for e in errors if e.category == category]
        if severity:
            errors = [e for e in errors if e.severity == severity]
        return errors[-limit:]

    def get_error_patterns(self) -> List[Dict[str, Any]]:
        """Identify patterns in error history."""
        patterns: List[Dict[str, Any]] = []
        by_type: Dict[str, List[ErrorInfo]] = defaultdict(list)
        for error in self._error_history:
            by_type[error.error_type or error.category.value].append(error)

        for error_type, errors in by_type.items():
            if len(errors) >= 2:
                files = [e.source_file for e in errors if e.source_file]
                common_file = _find_common_pattern(files) if files else None
                patterns.append({
                    "error_type": error_type,
                    "count": len(errors),
                    "category": errors[0].category.value,
                    "common_source": common_file,
                    "first_seen": min(e.timestamp for e in errors).isoformat(),
                    "last_seen": max(e.timestamp for e in errors).isoformat(),
                    "severity": max((e.severity for e in errors), key=lambda s: list(Severity).index(s)).value,
                })
        return sorted(patterns, key=lambda p: p["count"], reverse=True)

    def resolve_error(self, error_id: str) -> bool:
        """Mark an error as resolved."""
        for error in self._error_history:
            if error.error_id == error_id:
                error.resolved = True
                return True
        return False

    # -----------------------------------------------------------------------
    # Root Cause Analysis
    # -----------------------------------------------------------------------

    def start_root_cause_analysis(self, issue_description: str) -> RootCauseAnalysis:
        """Begin a structured root cause analysis."""
        rca = RootCauseAnalysis(issue_description=issue_description)
        rca.phases_completed.append(DebugPhase.REPRODUCE.value)
        rca.timeline.append({
            "phase": DebugPhase.REPRODUCE.value,
            "action": "Analysis started",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        logger.info("Root cause analysis started: %s", issue_description[:80])
        return rca

    def add_rca_evidence(
        self,
        rca: RootCauseAnalysis,
        evidence_type: str,
        description: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> RootCauseAnalysis:
        """Add evidence to a root cause analysis."""
        rca.evidence.append({
            "type": evidence_type,
            "description": description,
            "data": data or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return rca

    def form_hypothesis(
        self,
        rca: RootCauseAnalysis,
        hypothesis: str,
        category: RootCauseCategory = RootCauseCategory.UNKNOWN,
    ) -> RootCauseAnalysis:
        """Form a hypothesis during root cause analysis."""
        rca.hypothesis = hypothesis
        rca.category = category
        rca.phases_completed.append(DebugPhase.HYPOTHESIZE.value)
        rca.timeline.append({
            "phase": DebugPhase.HYPOTHESIZE.value,
            "action": f"Hypothesis: {hypothesis}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return rca

    def confirm_root_cause(
        self,
        rca: RootCauseAnalysis,
        root_cause: str,
        confidence: float,
        contributing_factors: Optional[List[str]] = None,
        recommendations: Optional[List[str]] = None,
    ) -> RootCauseAnalysis:
        """Confirm the root cause of an issue."""
        rca.root_cause = root_cause
        rca.confidence = confidence
        rca.confirmed = confidence >= self._config.confidence_threshold
        rca.contributing_factors = contributing_factors or []
        rca.recommendations = recommendations or []
        rca.phases_completed.extend([
            DebugPhase.INVESTIGATE.value,
            DebugPhase.FIX.value,
            DebugPhase.VERIFY.value,
            DebugPhase.PREVENT.value,
        ])
        rca.timeline.append({
            "phase": DebugPhase.INVESTIGATE.value,
            "action": f"Root cause confirmed: {root_cause}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        logger.info("Root cause confirmed: %s (confidence=%.2f)", root_cause[:80], confidence)
        return rca

    def generate_fix_suggestions(
        self,
        rca: RootCauseAnalysis,
    ) -> List[FixSuggestion]:
        """Generate fix suggestions based on root cause analysis."""
        suggestions: List[FixSuggestion] = []
        if rca.category == RootCauseCategory.CODE_DEFECT:
            suggestions.append(FixSuggestion(
                fix_type=FixType.CODE_CHANGE,
                title="Fix code defect",
                description=f"Address the code defect: {rca.root_cause}",
                confidence=rca.confidence,
                risk_level=Severity.LOW,
                testing_notes="Run unit tests and integration tests after fix",
            ))
        elif rca.category == RootCauseCategory.CONFIGURATION_ERROR:
            suggestions.append(FixSuggestion(
                fix_type=FixType.CONFIG_CHANGE,
                title="Fix configuration",
                description=f"Update configuration: {rca.root_cause}",
                confidence=rca.confidence,
                risk_level=Severity.MEDIUM,
                testing_notes="Verify configuration in staging before production",
            ))
        elif rca.category == RootCauseCategory.DEPENDENCY_FAILURE:
            suggestions.append(FixSuggestion(
                fix_type=FixType.DEPENDENCY_UPDATE,
                title="Update or replace dependency",
                description=f"Address dependency issue: {rca.root_cause}",
                confidence=rca.confidence,
                risk_level=Severity.MEDIUM,
                testing_notes="Check compatibility matrix before updating",
            ))
        elif rca.category == RootCauseCategory.RESOURCE_LIMIT:
            suggestions.append(FixSuggestion(
                fix_type=FixType.INFRASTRUCTURE,
                title="Scale resources",
                description=f"Increase resource allocation: {rca.root_cause}",
                confidence=rca.confidence,
                risk_level=Severity.LOW,
                testing_notes="Monitor resource usage after scaling",
            ))
        elif rca.category == RootCauseCategory.CONCURRENCY_ISSUE:
            suggestions.append(FixSuggestion(
                fix_type=FixType.CODE_CHANGE,
                title="Fix concurrency issue",
                description=f"Address race condition or deadlock: {rca.root_cause}",
                confidence=rca.confidence,
                risk_level=Severity.HIGH,
                testing_notes="Load test with concurrent access patterns",
            ))
        elif rca.category == RootCauseCategory.DESIGN_FLAW:
            suggestions.append(FixSuggestion(
                fix_type=FixType.ARCHITECTURE,
                title="Address design flaw",
                description=f"Architectural improvement needed: {rca.root_cause}",
                confidence=rca.confidence,
                risk_level=Severity.HIGH,
                prerequisites=["Architecture review", "Impact analysis"],
                testing_notes="Full regression test suite",
            ))

        # Always add monitoring suggestion
        suggestions.append(FixSuggestion(
            fix_type=FixType.MONITORING,
            title="Add monitoring for this issue class",
            description="Implement monitoring to detect recurrence of this issue",
            confidence=0.9,
            risk_level=Severity.LOW,
        ))

        return suggestions

    # -----------------------------------------------------------------------
    # Performance Profiling
    # -----------------------------------------------------------------------

    def create_profile(
        self,
        profiling_type: ProfilingType,
        duration_seconds: float,
        samples: int,
        top_functions: Optional[List[Dict[str, Any]]] = None,
        hotspots: Optional[List[Dict[str, Any]]] = None,
        summary: Optional[Dict[str, Any]] = None,
    ) -> ProfileResult:
        """Create a profiling result from collected data."""
        result = ProfileResult(
            profiling_type=profiling_type,
            duration_seconds=duration_seconds,
            samples=samples,
            top_functions=top_functions or [],
            hotspots=hotspots or [],
            summary=summary or {},
        )

        # Generate recommendations based on profiling type
        result.recommendations = self._generate_profile_recommendations(result)
        self._profiles.append(result)
        logger.info("Profile created: %s (%.3fs, %d samples)",
                     profiling_type.value, duration_seconds, samples)
        return result

    def _generate_profile_recommendations(self, profile: ProfileResult) -> List[str]:
        """Generate recommendations based on profiling results."""
        recommendations = []
        if profile.profiling_type == ProfilingType.CPU:
            if profile.top_functions:
                top = profile.top_functions[0]
                if top.get("percentage", 0) > 30:
                    recommendations.append(
                        f"Function '{top.get('name', 'unknown')}' consumes {top.get('percentage', 0):.1f}% of CPU time. Consider optimization or caching."
                    )
            if profile.summary.get("total_time_ms", 0) > self._config.slow_threshold_ms:
                recommendations.append("Total execution time exceeds slow threshold. Profile individual functions for optimization targets.")

        elif profile.profiling_type == ProfilingType.MEMORY:
            peak_mb = profile.summary.get("peak_memory_mb", 0)
            if peak_mb > self._config.memory_warning_mb:
                recommendations.append(f"Peak memory usage ({peak_mb:.1f}MB) exceeds warning threshold. Check for memory leaks or large allocations.")
            if profile.summary.get("allocation_count", 0) > 100000:
                recommendations.append("High allocation count detected. Consider object pooling or reducing temporary allocations.")

        elif profile.profiling_type == ProfilingType.IO:
            if profile.summary.get("total_io_time_ms", 0) > self._config.io_warning_ms:
                recommendations.append("I/O time is significant. Consider batching operations or adding caching.")
            if profile.summary.get("io_operations", 0) > 1000:
                recommendations.append("High I/O operation count. Consider bulk operations or connection pooling.")

        elif profile.profiling_type == ProfilingType.DATABASE:
            if profile.summary.get("slow_queries", 0) > 0:
                recommendations.append(f"{profile.summary['slow_queries']} slow queries detected. Add indexes or optimize query patterns.")
            if profile.summary.get("n_plus_one", False):
                recommendations.append("N+1 query pattern detected. Use eager loading or batch queries.")

        if not recommendations:
            recommendations.append("No critical performance issues detected in this profile.")
        return recommendations

    def analyze_profiles(self) -> Dict[str, Any]:
        """Analyze all collected profiles and generate a summary."""
        if not self._profiles:
            return {"message": "No profiles available for analysis"}

        by_type: Dict[str, List[ProfileResult]] = defaultdict(list)
        for p in self._profiles:
            by_type[p.profiling_type.value].append(p)

        summary: Dict[str, Any] = {
            "total_profiles": len(self._profiles),
            "by_type": {k: len(v) for k, v in by_type.items()},
            "recommendations": [],
        }

        for ptype, profiles in by_type.items():
            latest = profiles[-1]
            summary[f"{ptype}_latest"] = latest.summary
            summary["recommendations"].extend(latest.recommendations)

        return summary

    # -----------------------------------------------------------------------
    # Distributed Tracing
    # -----------------------------------------------------------------------

    def create_trace_span(
        self,
        trace_id: str,
        operation: str,
        service: str,
        parent_span_id: Optional[str] = None,
        duration_ms: float = 0.0,
        status: TraceSpanStatus = TraceSpanStatus.OK,
        error: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ) -> TraceSpan:
        """Create a trace span."""
        span = TraceSpan(
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            operation=operation,
            service=service,
            duration_ms=duration_ms,
            status=status,
            error=error,
            tags=tags or {},
        )
        if duration_ms > 0:
            span.end_time = span.start_time + timedelta(milliseconds=duration_ms)
        self._trace_store[trace_id].append(span)
        return span

    def analyze_trace(self, trace_id: str) -> TraceAnalysis:
        """Analyze a distributed trace for performance and errors."""
        spans = self._trace_store.get(trace_id, [])
        if not spans:
            return TraceAnalysis(trace_id=trace_id)

        total_duration = max((s.duration_ms for s in spans), default=0.0)
        error_spans = [s for s in spans if s.status == TraceSpanStatus.ERROR]
        sorted_by_duration = sorted(spans, key=lambda s: s.duration_ms, reverse=True)

        # Service breakdown
        service_time: Dict[str, float] = defaultdict(float)
        for s in spans:
            service_time[s.service] += s.duration_ms

        bottleneck_service = max(service_time, key=service_time.get) if service_time else ""

        # Critical path (simplified: longest chain)
        critical_path = [s.operation for s in sorted_by_duration[:5]]

        analysis = TraceAnalysis(
            trace_id=trace_id,
            total_duration_ms=total_duration,
            span_count=len(spans),
            error_spans=len(error_spans),
            slowest_spans=[s.to_dict() for s in sorted_by_duration[:10]],
            critical_path=critical_path,
            bottleneck_service=bottleneck_service,
            bottleneck_operation=sorted_by_duration[0].operation if sorted_by_duration else "",
            service_breakdown=dict(service_time),
        )

        # Generate recommendations
        if error_spans:
            analysis.recommendations.append(
                f"{len(error_spans)} spans have errors. Investigate: {error_spans[0].error}"
            )
        if total_duration > self._config.very_slow_threshold_ms:
            analysis.recommendations.append(
                f"Total trace duration ({total_duration:.1f}ms) is very slow. Focus on bottleneck: {bottleneck_service}"
            )
        elif total_duration > self._config.slow_threshold_ms:
            analysis.recommendations.append(
                f"Total trace duration ({total_duration:.1f}ms) is slow. Consider optimization."
            )
        if len(spans) > 100:
            analysis.recommendations.append("High span count. Consider reducing trace granularity or sampling.")

        return analysis

    def get_trace_spans(self, trace_id: str) -> List[TraceSpan]:
        """Get all spans for a trace."""
        return self._trace_store.get(trace_id, [])

    # -----------------------------------------------------------------------
    # Log Analysis
    # -----------------------------------------------------------------------

    def add_log_entry(self, entry: LogEntry) -> None:
        """Add a log entry for analysis."""
        self._log_entries.append(entry)
        self._log_entries = self._log_entries[-self._config.max_log_entries:]

    def add_log_entries(self, entries: List[LogEntry]) -> None:
        """Add multiple log entries."""
        for entry in entries:
            self.add_log_entry(entry)

    def analyze_logs(self) -> LogAnalysis:
        """Analyze collected log entries for patterns and issues."""
        if not self._log_entries:
            return LogAnalysis()

        analysis = LogAnalysis(total_entries=len(self._log_entries))

        # Count by level
        level_counter = Counter(e.level for e in self._log_entries)
        analysis.by_level = dict(level_counter)

        # Error patterns
        error_entries = [e for e in self._log_entries if e.level in ("ERROR", "CRITICAL")]
        if error_entries:
            message_patterns: Dict[str, List[LogEntry]] = defaultdict(list)
            for entry in error_entries:
                # Normalize message (remove variable parts)
                normalized = re.sub(r'\d+', 'N', entry.message)
                normalized = re.sub(r'[a-f0-9]{8,}', 'ID', normalized)
                message_patterns[normalized].append(entry)

            for pattern, entries in sorted(message_patterns.items(), key=lambda x: len(x[1]), reverse=True):
                analysis.error_patterns.append({
                    "pattern": pattern[:200],
                    "count": len(entries),
                    "first_seen": min(e.timestamp for e in entries).isoformat(),
                    "last_seen": max(e.timestamp for e in entries).isoformat(),
                    "sample_message": entries[0].message[:200],
                })

        # Frequent messages
        msg_counter = Counter(e.message[:100] for e in self._log_entries)
        analysis.frequent_messages = [
            {"message": msg, "count": count}
            for msg, count in msg_counter.most_common(20)
        ]

        # Time distribution (by hour)
        hour_counter = Counter(e.timestamp.hour for e in self._log_entries)
        analysis.time_distribution = {str(h): c for h, c in sorted(hour_counter.items())}

        # Correlated errors (errors from same source close in time)
        if self._config.enable_correlation and len(error_entries) > 1:
            correlated = self._find_correlated_errors(error_entries)
            analysis.correlated_errors = correlated

        # Recommendations
        if error_entries:
            error_rate = len(error_entries) / len(self._log_entries)
            if error_rate > 0.1:
                analysis.recommendations.append(f"High error rate: {error_rate:.1%} of logs are errors")
            if analysis.error_patterns:
                top_pattern = analysis.error_patterns[0]
                if top_pattern["count"] > 10:
                    analysis.recommendations.append(
                        f"Recurring error pattern ({top_pattern['count']} occurrences): {top_pattern['pattern'][:80]}"
                    )
        if not analysis.recommendations:
            analysis.recommendations.append("No significant issues detected in log analysis")

        return analysis

    def _find_correlated_errors(self, error_entries: List[LogEntry]) -> List[Dict[str, Any]]:
        """Find errors that are temporally or spatially correlated."""
        correlations: List[Dict[str, Any]] = []
        by_source: Dict[str, List[LogEntry]] = defaultdict(list)
        for entry in error_entries:
            by_source[entry.source or "unknown"].append(entry)

        for source, entries in by_source.items():
            if len(entries) > 1:
                sorted_entries = sorted(entries, key=lambda e: e.timestamp)
                time_diffs = [
                    (sorted_entries[i + 1].timestamp - sorted_entries[i].timestamp).total_seconds()
                    for i in range(len(sorted_entries) - 1)
                ]
                avg_gap = statistics.mean(time_diffs) if time_diffs else 0
                correlations.append({
                    "source": source,
                    "error_count": len(entries),
                    "avg_time_between_seconds": round(avg_gap, 2),
                    "pattern": "burst" if avg_gap < 60 else "intermittent",
                })
        return correlations

    # -----------------------------------------------------------------------
    # Logging Strategy
    # -----------------------------------------------------------------------

    def analyze_logging_strategy(self, config: LoggingConfig) -> Dict[str, Any]:
        """Analyze current logging configuration and suggest improvements."""
        analysis: Dict[str, Any] = {
            "current_config": config.to_dict(),
            "issues": [],
            "recommendations": [],
            "strategies": [],
        }

        if not config.structured:
            analysis["issues"].append("Logs are not structured. Makes automated parsing difficult.")
            analysis["recommendations"].append("Switch to structured logging (JSON format) for machine-parseable logs.")
            analysis["strategies"].append(LogStrategy.STRUCTURED.value)

        if not config.correlation_ids:
            analysis["issues"].append("No correlation IDs. Difficult to trace requests across services.")
            analysis["recommendations"].append("Add correlation IDs (trace_id, request_id) to all log entries.")
            analysis["strategies"].append(LogStrategy.CORRELATED.value)

        if config.current_level == "DEBUG" and config.sampling_rate == 1.0:
            analysis["issues"].append("DEBUG level logging at 100% sampling. May cause performance issues.")
            analysis["recommendations"].append("Implement sampling (1-10%) for DEBUG logs in production.")
            analysis["strategies"].append(LogStrategy.SAMPLING.value)

        if not config.redaction_patterns:
            analysis["issues"].append("No PII redaction patterns configured.")
            analysis["recommendations"].append("Add redaction patterns for sensitive data (emails, tokens, passwords).")
            analysis["strategies"].append(LogStrategy.REDACTION.value)

        if len(config.output_targets) == 1 and "console" in config.output_targets:
            analysis["issues"].append("Logs only go to console. No persistence or centralization.")
            analysis["recommendations"].append("Add file or centralized logging (ELK, Datadog, CloudWatch).")
            analysis["strategies"].append(LogStrategy.AGGREGATION.value)

        if not config.performance_logging:
            analysis["issues"].append("Performance logging is disabled.")
            analysis["recommendations"].append("Enable performance logging to track response times and throughput.")
            analysis["strategies"].append(LogStrategy.REALTIME.value)

        if not analysis["issues"]:
            analysis["recommendations"].append("Logging configuration appears adequate. Review periodically.")

        return analysis

    def optimize_logging(self, config: LoggingConfig) -> LoggingConfig:
        """Apply recommended optimizations to logging configuration."""
        optimized = LoggingConfig(
            current_level=config.current_level,
            format="json",
            structured=True,
            correlation_ids=True,
            sampling_rate=0.1 if config.current_level == "DEBUG" else config.sampling_rate,
            redaction_patterns=config.redaction_patterns or [
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                r"password[=:]\s*\S+",
                r"token[=:]\s*\S+",
                r"api[_-]?key[=:]\s*\S+",
            ],
            output_targets=["console", "file"],
            retention_days=config.retention_days,
            alert_on_error=True,
            performance_logging=True,
        )
        return optimized

    # -----------------------------------------------------------------------
    # Comprehensive Debug
    # -----------------------------------------------------------------------

    def debug_issue(
        self,
        error_message: str,
        error_type: str = "",
        stack_trace: str = "",
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Perform a comprehensive debug analysis on an issue."""
        # Create session
        session = self.create_session(f"Debug: {error_message[:100]}")

        # Analyze error
        error = self.analyze_error(error_message, error_type, stack_trace, context)
        session.errors.append(error)

        # Start root cause analysis
        rca = self.start_root_cause_analysis(error_message)
        self.add_rca_evidence(rca, "error_info", error.message, error.to_dict())

        if error.stack_frames:
            self.add_rca_evidence(rca, "stack_trace", f"Stack trace with {len(error.stack_frames)} frames", {
                "frames": error.stack_frames[:5],
            })

        if error.source_file:
            self.add_rca_evidence(rca, "source_location", f"Error in {error.source_file}:{error.source_line}", {
                "file": error.source_file,
                "line": error.source_line,
                "function": error.source_function,
            })

        # Check for patterns
        patterns = self.get_error_patterns()
        if patterns:
            matching = [p for p in patterns if p["error_type"] == error.error_type]
            if matching:
                self.add_rca_evidence(rca, "error_pattern", f"Recurring pattern: {matching[0]['count']} occurrences", matching[0])

        session.root_cause = rca
        session.advance_phase(session.session_id, DebugPhase.HYPOTHESIZE)

        # Generate fix suggestions
        fixes = self.generate_fix_suggestions(rca)
        session.fixes = fixes

        return {
            "session": session.to_dict(),
            "error": error.to_dict(),
            "root_cause_analysis": rca.to_dict(),
            "fix_suggestions": [f.to_dict() for f in fixes],
        }

    # -----------------------------------------------------------------------
    # Status & Reporting
    # -----------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent": "DebuggingAgent",
            "active_sessions": sum(1 for s in self._sessions.values() if s.status == "active"),
            "total_sessions": len(self._sessions),
            "error_history_count": len(self._error_history),
            "unresolved_errors": sum(1 for e in self._error_history if not e.resolved),
            "log_entries_count": len(self._log_entries),
            "traces_count": len(self._trace_store),
            "profiles_count": len(self._profiles),
        }

    def generate_debug_report(self, session_id: str) -> str:
        """Generate a comprehensive debug report for a session."""
        session = self.get_session(session_id)
        lines = [
            f"Debug Report: {session.issue_title}",
            f"Session: {session.session_id}",
            f"Status: {session.status}",
            f"Phase: {session.current_phase.value}",
            f"Started: {session.started_at.isoformat()}",
            f"Errors: {len(session.errors)}",
        ]
        if session.root_cause:
            rca = session.root_cause
            lines.extend([
                f"\nRoot Cause: {rca.root_cause or 'Not determined'}",
                f"Confidence: {rca.confidence:.0%}",
                f"Category: {rca.category.value}",
                f"Contributing factors: {', '.join(rca.contributing_factors) or 'None'}",
            ])
        if session.fixes:
            lines.append("\nFix Suggestions:")
            for fix in session.fixes:
                lines.append(f"  [{fix.fix_type.value}] {fix.title}")
                lines.append(f"    {fix.description}")
                lines.append(f"    Confidence: {fix.confidence:.0%}")
        if session.notes:
            lines.append("\nNotes:")
            for note in session.notes:
                lines.append(f"  - {note}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Debugging Agent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print("=" * 60)
    print("Debugging Agent - Comprehensive Demo")
    print("=" * 60)

    agent = DebuggingAgent()

    # Analyze an error
    print("\n--- Error Analysis ---")
    error = agent.analyze_error(
        error_message="TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'",
        error_type="TypeError",
        stack_trace='File "app/models/user.py", line 42, in get_balance\n    return self.balance + bonus\nFile "app/views/dashboard.py", line 128, in show\n    balance = user.get_balance()',
        context={"user_id": 12345, "action": "get_balance"},
    )
    print(f"Error: {error.error_id}")
    print(f"Category: {error.category.value}")
    print(f"Severity: {error.severity.value}")
    print(f"Source: {error.source_file}:{error.source_line}")
    print(f"Function: {error.source_function}")

    # Root cause analysis
    print("\n--- Root Cause Analysis ---")
    rca = agent.start_root_cause_analysis("TypeError when fetching user balance")
    agent.add_rca_evidence(rca, "error", error.message, error.to_dict())
    agent.form_hypothesis(rca, "bonus field is None for some users due to missing default", RootCauseCategory.DATA_CORRUPTION)
    agent.confirm_root_cause(
        rca,
        "bonus column allows NULL values but code assumes non-null",
        confidence=0.9,
        contributing_factors=["No NOT NULL constraint on bonus column", "Missing null check in get_balance"],
        recommendations=["Add NOT NULL DEFAULT 0 to bonus column", "Add null check in get_balance method"],
    )
    print(f"Root Cause: {rca.root_cause}")
    print(f"Confidence: {rca.confidence:.0%}")

    # Fix suggestions
    fixes = agent.generate_fix_suggestions(rca)
    print(f"\nFix Suggestions: {len(fixes)}")
    for fix in fixes:
        print(f"  [{fix.fix_type.value}] {fix.title} (confidence={fix.confidence:.0%})")

    # Profiling
    print("\n--- Performance Profiling ---")
    profile = agent.create_profile(
        profiling_type=ProfilingType.CPU,
        duration_seconds=2.5,
        samples=1000,
        top_functions=[
            {"name": "get_balance", "percentage": 45.2, "calls": 10000},
            {"name": "calculate_bonus", "percentage": 22.1, "calls": 10000},
            {"name": "fetch_user", "percentage": 15.8, "calls": 5000},
        ],
        summary={"total_time_ms": 2500, "function_count": 150},
    )
    print(f"Profile: {profile.profiling_type.value}, {profile.duration_seconds}s")
    print(f"Recommendations: {profile.recommendations}")

    # Distributed tracing
    print("\n--- Distributed Tracing ---")
    trace_id = uuid.uuid4().hex[:16]
    agent.create_trace_span(trace_id, "http_request", "api-gateway", duration_ms=250)
    agent.create_trace_span(trace_id, "authenticate", "auth-service", parent_span_id="span1", duration_ms=30)
    agent.create_trace_span(trace_id, "query_balance", "user-service", parent_span_id="span1", duration_ms=150)
    agent.create_trace_span(trace_id, "db_query", "database", parent_span_id="span3", duration_ms=120, status=TraceSpanStatus.ERROR, error="Connection timeout")
    trace_analysis = agent.analyze_trace(trace_id)
    print(f"Trace: {trace_analysis.span_count} spans, {trace_analysis.total_duration_ms}ms total")
    print(f"Bottleneck: {trace_analysis.bottleneck_service}")
    print(f"Error spans: {trace_analysis.error_spans}")

    # Log analysis
    print("\n--- Log Analysis ---")
    for i in range(100):
        agent.add_log_entry(LogEntry(
            level="INFO" if i % 10 != 0 else "ERROR",
            message=f"Processing request {i}" if i % 10 != 0 else f"Failed to process request {i}: timeout",
            source="app.views.dashboard",
        ))
    log_analysis = agent.analyze_logs()
    print(f"Total entries: {log_analysis.total_entries}")
    print(f"By level: {log_analysis.by_level}")
    print(f"Error patterns: {len(log_analysis.error_patterns)}")
    print(f"Recommendations: {log_analysis.recommendations}")

    # Logging strategy
    print("\n--- Logging Strategy ---")
    config = LoggingConfig(current_level="DEBUG", format="text", structured=False)
    strategy = agent.analyze_logging_strategy(config)
    print(f"Issues: {len(strategy['issues'])}")
    for issue in strategy["issues"]:
        print(f"  - {issue}")
    optimized = agent.optimize_logging(config)
    print(f"Optimized: structured={optimized.structured}, correlation_ids={optimized.correlation_ids}")

    # Debug issue (comprehensive)
    print("\n--- Comprehensive Debug ---")
    result = agent.debug_issue(
        error_message="ConnectionError: Unable to connect to database",
        error_type="ConnectionError",
        stack_trace='File "app/db/pool.py", line 88, in get_connection\n    return psycopg2.connect(dsn)\nFile "app/config.py", line 45, in get_dsn\n    return f"host={config.DB_HOST}"',
    )
    print(f"Session: {result['session']['session_id']}")
    print(f"Fixes: {len(result['fix_suggestions'])}")

    # Status
    print(f"\nAgent Status: {json.dumps(agent.get_status(), indent=2)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
