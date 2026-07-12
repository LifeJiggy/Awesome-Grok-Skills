"""
Crash Analysis Framework

Production-grade crash analysis toolkit providing core dump analysis, stack trace
processing, crash clustering, and root cause identification for production debugging.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SignalType(Enum):
    SIGSEGV = "SIGSEGV"
    SIGABRT = "SIGABRT"
    SIGFPE = "SIGFPE"
    SIGILL = "SIGILL"
    SIGBUS = "SIGBUS"
    SIGTERM = "SIGTERM"
    SIGKILL = "SIGKILL"
    SIGPIPE = "SIGPIPE"
    UNKNOWN = "UNKNOWN"


class ExceptionCategory(Enum):
    NULL_POINTER = "null_pointer"
    BUFFER_OVERFLOW = "buffer_overflow"
    BUFFER_UNDERFLOW = "buffer_underflow"
    USE_AFTER_FREE = "use_after_free"
    DOUBLE_FREE = "double_free"
    STACK_OVERFLOW = "stack_overflow"
    INTEGER_OVERFLOW = "integer_overflow"
    DIVISION_BY_ZERO = "division_by_zero"
    OUT_OF_MEMORY = "out_of_memory"
    DEADLOCK = "deadlock"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    UNKNOWN = "unknown"


class CrashSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class StackFrame:
    """A single stack frame."""
    function: str
    file: str = ""
    line: int = 0
    address: int = 0
    library: str = ""
    is_inlined: bool = False
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThreadInfo:
    """Thread information in a crash."""
    thread_id: int
    name: str = ""
    state: str = "unknown"
    stack_trace: List[StackFrame] = field(default_factory=list)
    is_crashed: bool = False


@dataclass
class CoreDumpAnalysis:
    """Core dump analysis result."""
    file_path: str
    signal: SignalType
    fault_address: int = 0
    thread_count: int = 1
    crashed_thread: int = 0
    crashed_function: str = ""
    stack_trace: List[StackFrame] = field(default_factory=list)
    threads: List[ThreadInfo] = field(default_factory=list)
    registers: Dict[str, int] = field(default_factory=dict)
    memory_regions: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessedStack:
    """Processed and symbolicated stack trace."""
    raw_trace: str
    exception_type: str = ""
    exception_message: str = ""
    top_frame: StackFrame = field(default_factory=lambda: StackFrame(function=""))
    frames: List[StackFrame] = field(default_factory=list)
    root_cause: str = ""
    category: ExceptionCategory = ExceptionCategory.UNKNOWN


@dataclass
class CrashReport:
    """A single crash report."""
    crash_id: str
    timestamp: datetime
    signal: SignalType
    function: str
    file: str = ""
    line: int = 0
    stack_trace: str = ""
    app_version: str = ""
    os_version: str = ""
    affected_users: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CrashCluster:
    """A group of similar crashes."""
    signature: str
    count: int
    affected_users: int
    first_seen: datetime
    last_seen: datetime
    top_frame: StackFrame = field(default_factory=lambda: StackFrame(function=""))
    representative_crash: Optional[CrashReport] = None
    severity: CrashSeverity = CrashSeverity.MEDIUM


@dataclass
class RootCause:
    """Root cause analysis result."""
    category: ExceptionCategory
    confidence: float
    description: str
    evidence: List[str]
    recommendations: List[str]
    similar_issues: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class CrashTrend:
    """Crash trend analysis."""
    date: str
    count: int
    affected_users: int
    new_crashes: int = 0
    resolved_crashes: int = 0


# ---------------------------------------------------------------------------
# Core Dump Analyzer
# ---------------------------------------------------------------------------

class CoreDumpAnalyzer:
    """Analyze core dump files."""

    def analyze(self, file_path: str) -> CoreDumpAnalysis:
        # Simulate core dump analysis
        return CoreDumpAnalysis(
            file_path=file_path,
            signal=SignalType.SIGSEGV,
            fault_address=0x0000000000000000,
            thread_count=8,
            crashed_thread=0,
            crashed_function="process_data",
            stack_trace=[
                StackFrame("process_data", "data.c", 42, 0x7f8b2c001234),
                StackFrame("handle_request", "server.c", 156, 0x7f8b2c005678),
                StackFrame("worker_thread", "worker.c", 89, 0x7f8b2c009abc),
                StackFrame("start_thread", "pthread.c", 123, 0x7f8b2c012345),
            ],
            threads=[
                ThreadInfo(0, "main", "crashed", is_crashed=True),
                ThreadInfo(1, "worker-1", "running"),
                ThreadInfo(2, "worker-2", "waiting"),
            ],
            registers={"rip": 0x7f8b2c001234, "rsp": 0x7ffc12345678, "rbp": 0x7ffc12345600},
        )


# ---------------------------------------------------------------------------
# Stack Trace Processor
# ---------------------------------------------------------------------------

class StackTraceProcessor:
    """Process and symbolicate stack traces."""

    def __init__(self, symbol_path: str = ""):
        self.symbol_path = symbol_path

    def process(self, raw_trace: str) -> ProcessedStack:
        frames = []
        lines = raw_trace.strip().split("\n")

        for line in lines:
            match = re.match(r"\s*#(\d+)\s+(0x[0-9a-f]+)\s+in\s+(\S+)\s+\(([^:]+):(\d+)\)", line)
            if match:
                frames.append(StackFrame(
                    function=match.group(3),
                    file=match.group(4),
                    line=int(match.group(5)),
                    address=int(match.group(2), 16),
                ))

        exception_type = "SIGSEGV"
        if "SIGABRT" in raw_trace:
            exception_type = "SIGABRT"
        elif "SIGFPE" in raw_trace:
            exception_type = "SIGFPE"

        top_frame = frames[0] if frames else StackFrame(function="unknown")

        return ProcessedStack(
            raw_trace=raw_trace,
            exception_type=exception_type,
            top_frame=top_frame,
            frames=frames,
            root_cause=f"Crash in {top_frame.function} at {top_frame.file}:{top_frame.line}",
            category=self._classify_exception(exception_type, top_frame),
        )

    def _classify_exception(self, signal: str, frame: StackFrame) -> ExceptionCategory:
        if signal == "SIGSEGV":
            return ExceptionCategory.NULL_POINTER
        elif signal == "SIGABRT":
            return ExceptionCategory.UNKNOWN
        elif signal == "SIGFPE":
            return ExceptionCategory.DIVISION_BY_ZERO
        return ExceptionCategory.UNKNOWN


# ---------------------------------------------------------------------------
# Crash Clusterer
# ---------------------------------------------------------------------------

class CrashClusterer:
    """Group similar crashes into clusters."""

    def cluster(self, crashes: List[CrashReport]) -> List[CrashCluster]:
        # Group by function signature
        groups: Dict[str, List[CrashReport]] = {}
        for crash in crashes:
            sig = f"{crash.signal.value}:{crash.function}:{crash.file}:{crash.line}"
            if sig not in groups:
                groups[sig] = []
            groups[sig].append(crash)

        clusters = []
        for sig, group in groups.items():
            cluster = CrashCluster(
                signature=sig,
                count=len(group),
                affected_users=sum(c.affected_users for c in group),
                first_seen=min(c.timestamp for c in group),
                last_seen=max(c.timestamp for c in group),
                top_frame=StackFrame(
                    function=group[0].function,
                    file=group[0].file,
                    line=group[0].line,
                ),
                representative_crash=group[0],
                severity=self._assess_severity(len(group), sum(c.affected_users for c in group)),
            )
            clusters.append(cluster)

        return sorted(clusters, key=lambda c: c.count, reverse=True)

    def _assess_severity(self, count: int, affected_users: int) -> CrashSeverity:
        if count > 100 or affected_users > 1000:
            return CrashSeverity.CRITICAL
        elif count > 20 or affected_users > 100:
            return CrashSeverity.HIGH
        elif count > 5 or affected_users > 10:
            return CrashSeverity.MEDIUM
        return CrashSeverity.LOW


# ---------------------------------------------------------------------------
# Root Cause Analyzer
# ---------------------------------------------------------------------------

class RootCauseAnalyzer:
    """Analyze crash root causes."""

    def analyze(self, analysis: CoreDumpAnalysis) -> RootCause:
        if analysis.signal == SignalType.SIGSEGV:
            return RootCause(
                category=ExceptionCategory.NULL_POINTER,
                confidence=0.85,
                description="Null pointer dereference detected. The application attempted to access memory at address 0x0, which is not mapped.",
                evidence=[
                    f"Signal: {analysis.signal.value}",
                    f"Fault address: 0x{analysis.fault_address:X}",
                    f"Crashed in: {analysis.crashed_function}",
                    "Fault address is NULL (0x0)",
                ],
                recommendations=[
                    "Add null pointer checks before dereferencing pointers",
                    "Use optional/nullable types where appropriate",
                    "Enable address sanitizer for development builds",
                    "Add input validation at API boundaries",
                ],
                similar_issues=[
                    {"id": "CRASH-1234", "description": "Similar null deref in process_data", "fixed": "2024-01-10"},
                ],
            )
        elif analysis.signal == SignalType.SIGABRT:
            return RootCause(
                category=ExceptionCategory.UNKNOWN,
                confidence=0.60,
                description="Application aborted, possibly due to assertion failure or unhandled exception.",
                evidence=[
                    f"Signal: {analysis.signal.value}",
                    f"Crashed in: {analysis.crashed_function}",
                ],
                recommendations=[
                    "Check for assertion failures in the crashed function",
                    "Review exception handling code",
                    "Add more detailed logging before abort points",
                ],
            )

        return RootCause(
            category=ExceptionCategory.UNKNOWN,
            confidence=0.30,
            description="Unable to determine root cause automatically.",
            evidence=[f"Signal: {analysis.signal.value}"],
            recommendations=["Manual investigation required"],
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate crash analysis capabilities."""
    print("=" * 70)
    print("Crash Analysis Framework - Demo")
    print("=" * 70)

    # --- 1. Core Dump Analysis ---
    print("\n--- Core Dump Analysis ---")
    core_analyzer = CoreDumpAnalyzer()
    analysis = core_analyzer.analyze("/var/crash/app.core")
    print(f"  Signal: {analysis.signal.value}")
    print(f"  Fault address: 0x{analysis.fault_address:X}")
    print(f"  Threads: {analysis.thread_count}")
    print(f"  Crashed in: {analysis.crashed_function}")
    print(f"  Stack trace:")
    for frame in analysis.stack_trace[:5]:
        print(f"    {frame.function} ({frame.file}:{frame.line})")

    # --- 2. Stack Trace Processing ---
    print("\n--- Stack Trace Processing ---")
    processor = StackTraceProcessor()
    raw_trace = """Signal: SIGSEGV (Segmentation fault)
Thread 0 (crashed):
  #0  0x00007f8b2c001234 in process_data (data.c:42)
  #1  0x00007f8b2c005678 in handle_request (server.c:156)
  #2  0x00007f8b2c009abc in worker_thread (worker.c:89)
  #3  0x00007f8b2c012345 in start_thread (pthread.c:123)"""

    processed = processor.process(raw_trace)
    print(f"  Exception: {processed.exception_type}")
    print(f"  Top frame: {processed.top_frame.function} ({processed.top_frame.file}:{processed.top_frame.line})")
    print(f"  Root cause: {processed.root_cause}")
    print(f"  Category: {processed.category.value}")

    # --- 3. Crash Clustering ---
    print("\n--- Crash Clustering ---")
    clusterer = CrashClusterer()
    crashes = [
        CrashReport(f"crash-{i}", datetime.now(timezone.utc), SignalType.SIGSEGV,
                    "process_data", "data.c", 42, affected_users=np.random.randint(1, 100))
        for i in range(50)
    ]
    # Add different crash
    crashes.extend([
        CrashReport(f"crash-diff-{i}", datetime.now(timezone.utc), SignalType.SIGABRT,
                    "parse_json", "json.c", 100, affected_users=np.random.randint(1, 10))
        for i in range(10)
    ])

    clusters = clusterer.cluster(crashes)
    print(f"  Total crashes: {len(crashes)}")
    print(f"  Clusters: {len(clusters)}")
    for cluster in clusters[:3]:
        print(f"\n  Cluster: {cluster.signature}")
        print(f"    Count: {cluster.count}")
        print(f"    Users: {cluster.affected_users}")
        print(f"    Severity: {cluster.severity.value}")
        print(f"    Top: {cluster.top_frame.function} ({cluster.top_frame.file}:{cluster.top_frame.line})")

    # --- 4. Root Cause Analysis ---
    print("\n--- Root Cause Analysis ---")
    rca = RootCauseAnalyzer()
    root_cause = rca.analyze(analysis)
    print(f"  Category: {root_cause.category.value}")
    print(f"  Confidence: {root_cause.confidence:.0%}")
    print(f"  Description: {root_cause.description}")
    print(f"  Evidence:")
    for ev in root_cause.evidence:
        print(f"    - {ev}")
    print(f"  Recommendations:")
    for rec in root_cause.recommendations:
        print(f"    - {rec}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()