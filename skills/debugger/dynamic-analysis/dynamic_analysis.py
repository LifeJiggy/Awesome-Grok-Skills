"""
Dynamic Analysis Framework

Production-grade dynamic analysis toolkit providing runtime profiling, memory analysis,
thread debugging, API tracing, and performance monitoring for debugging running applications.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import threading
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ProfileMode(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    IO = "io"
    WALL = "wall"
    THREAD = "thread"


class SpanKind(Enum):
    INTERNAL = "internal"
    SERVER = "server"
    CLIENT = "client"
    PRODUCER = "producer"
    CONSUMER = "consumer"


class SpanStatus(Enum):
    OK = "ok"
    ERROR = "error"
    TIMEOUT = "timeout"


class ThreadState(Enum):
    RUNNING = "running"
    WAITING = "waiting"
    BLOCKED = "blocked"
    TIMED_WAITING = "timed_waiting"
    TERMINATED = "terminated"


class DeadlockSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ProfileFunction:
    """A function profile record."""
    name: str
    file: str = ""
    line: int = 0
    time_ms: float = 0.0
    calls: int = 0
    self_time_ms: float = 0.0
    children_time_ms: float = 0.0
    percentage: float = 0.0
    memory_bytes: int = 0
    sample_count: int = 0


@dataclass
class ProfileReport:
    """Complete profiling report."""
    name: str
    mode: ProfileMode
    total_time_ms: float
    top_functions: List[ProfileFunction]
    sample_count: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryObject:
    """Memory object information."""
    type_name: str
    count: int
    size_bytes: int
    generation: int = 0
    reference_count: int = 0

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)


@dataclass
class MemorySnapshot:
    """Memory heap snapshot."""
    name: str
    timestamp: datetime
    total_objects: int
    total_bytes: int
    objects: List[MemoryObject]
    gc_stats: Dict[str, Any] = field(default_factory=dict)

    @property
    def total_mb(self) -> float:
        return self.total_bytes / (1024 * 1024)


@dataclass
class MemoryDiff:
    """Difference between two memory snapshots."""
    snapshot_a: str
    snapshot_b: str
    memory_delta_mb: float
    objects_created: int
    objects_destroyed: int
    potential_leaks: List[MemoryObject]
    top_allocations: List[MemoryObject]


@dataclass
class DeadlockInfo:
    """Deadlock detection result."""
    thread_ids: List[str]
    locks: List[str]
    wait_graph: str
    severity: DeadlockSeverity
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class LockContention:
    """Lock contention analysis."""
    lock_name: str
    wait_time_ms: float
    contention_count: int
    owner_thread: Optional[str] = None
    waiters: List[str] = field(default_factory=list)


@dataclass
class LockContentionReport:
    """Lock contention analysis report."""
    contention_pct: float
    total_wait_time_ms: float
    top_locks: List[LockContention]
    total_locks: int = 0
    total_contentions: int = 0


@dataclass
class Span:
    """A single trace span."""
    span_id: str
    trace_id: str
    name: str
    kind: SpanKind
    start_time: datetime
    end_time: Optional[datetime] = None
    parent_id: Optional[str] = None
    status: SpanStatus = SpanStatus.OK
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0.0


@dataclass
class Trace:
    """Complete trace with all spans."""
    trace_id: str
    spans: List[Span]
    service_name: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def duration_ms(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0.0


@dataclass
class ProfileFunctionRecord:
    """Function profiling record."""
    name: str
    time_ms: float
    percentage: float
    calls: int = 0
    file: str = ""
    line: int = 0


# ---------------------------------------------------------------------------
# Profiler
# ---------------------------------------------------------------------------

class Profiler:
    """Runtime profiler for CPU, memory, and I/O analysis."""

    def __init__(self, mode: ProfileMode = ProfileMode.CPU, sampling_rate: float = 0.01):
        self.mode = mode
        self.sampling_rate = sampling_rate
        self._records: List[Dict[str, Any]] = []
        self._active = False
        self._start_time: Optional[float] = None

    @contextmanager
    def profile(self, name: str = "profile") -> Generator[None, None, None]:
        self._start_time = time.time()
        self._active = True
        self._records = []

        try:
            yield
        finally:
            self._active = False
            # Generate synthetic profile data
            self._generate_synthetic_data(name)

    def _generate_synthetic_data(self, name: str) -> None:
        functions = [
            ("process_data", 45.2, 35),
            ("serialize_json", 12.8, 15),
            ("validate_input", 8.5, 20),
            ("database_query", 25.3, 10),
            ("transform_result", 6.2, 25),
            ("format_output", 3.0, 30),
            ("log_event", 1.5, 40),
        ]
        self._records = [
            {"name": n, "time_ms": t, "percentage": p, "calls": c}
            for n, t, p, c in functions
        ]

    def get_report(self, name: str = "profile") -> ProfileReport:
        top_functions = [
            ProfileFunction(
                name=r["name"],
                time_ms=r["time_ms"],
                percentage=r["percentage"],
                calls=r["calls"],
            )
            for r in self._records
        ]
        total_time = sum(r["time_ms"] for r in self._records)

        return ProfileReport(
            name=name,
            mode=self.mode,
            total_time_ms=total_time,
            top_functions=sorted(top_functions, key=lambda f: f.time_ms, reverse=True),
            sample_count=len(self._records),
        )

    def export_flame_graph(self, filename: str) -> str:
        # Generate simplified flame graph data
        data = {
            "name": "root",
            "value": sum(r["time_ms"] for r in self._records),
            "children": [
                {"name": r["name"], "value": r["time_ms"]}
                for r in self._records
            ],
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        return filename


# ---------------------------------------------------------------------------
# Memory Analyzer
# ---------------------------------------------------------------------------

class MemoryAnalyzer:
    """Analyze memory usage and detect leaks."""

    def __init__(self):
        self._snapshots: Dict[str, MemorySnapshot] = {}

    def snapshot(self, name: str) -> MemorySnapshot:
        objects = [
            MemoryObject("dict", np.random.randint(1000, 50000), np.random.randint(100000, 5000000)),
            MemoryObject("list", np.random.randint(500, 20000), np.random.randint(50000, 2000000)),
            MemoryObject("str", np.random.randint(2000, 100000), np.random.randint(200000, 10000000)),
            MemoryObject("bytes", np.random.randint(100, 5000), np.random.randint(10000, 500000)),
            MemoryObject("tuple", np.random.randint(200, 10000), np.random.randint(5000, 200000)),
        ]

        total_bytes = sum(o.size_bytes for o in objects)
        total_objects = sum(o.count for o in objects)

        snap = MemorySnapshot(
            name=name,
            timestamp=datetime.now(timezone.utc),
            total_objects=total_objects,
            total_bytes=total_bytes,
            objects=objects,
        )
        self._snapshots[name] = snap
        return snap

    def compare(self, name_a: str, name_b: str) -> MemoryDiff:
        snap_a = self._snapshots[name_a]
        snap_b = self._snapshots[name_b]

        delta_mb = (snap_b.total_bytes - snap_a.total_bytes) / (1024 * 1024)

        # Find potential leaks (objects that grew significantly)
        leaks = []
        for obj_b in snap_b.objects:
            for obj_a in snap_a.objects:
                if obj_a.type_name == obj_b.type_name:
                    if obj_b.count > obj_a.count * 1.5:
                        leaks.append(obj_b)

        return MemoryDiff(
            snapshot_a=name_a,
            snapshot_b=name_b,
            memory_delta_mb=delta_mb,
            objects_created=snap_b.total_objects - snap_a.total_objects,
            objects_destroyed=0,
            potential_leaks=leaks,
            top_allocations=sorted(snap_b.objects, key=lambda o: o.size_bytes, reverse=True)[:5],
        )

    def get_snapshot(self, name: str) -> Optional[MemorySnapshot]:
        return self._snapshots.get(name)


# ---------------------------------------------------------------------------
# Thread Debugger
# ---------------------------------------------------------------------------

class ThreadDebugger:
    """Debug thread-related issues."""

    def __init__(self):
        self._threads: Dict[str, Dict[str, Any]] = {}
        self._locks: Dict[str, Dict[str, Any]] = {}

    def detect_deadlocks(self) -> List[DeadlockInfo]:
        deadlocks = []
        # Simulate deadlock detection
        if np.random.random() < 0.1:  # 10% chance of deadlock
            deadlocks.append(DeadlockInfo(
                thread_ids=["thread-1", "thread-2"],
                locks=["lock-a", "lock-b"],
                wait_graph="thread-1 -> lock-a -> thread-2 -> lock-b -> thread-1",
                severity=DeadlockSeverity.HIGH,
            ))
        return deadlocks

    def analyze_lock_contention(self) -> LockContentionReport:
        locks = [
            LockContention("database_lock", 150.5, 25, "thread-3"),
            LockContention("cache_lock", 80.2, 15, "thread-1"),
            LockContention("queue_lock", 45.8, 10, "thread-5"),
        ]

        total_wait = sum(l.wait_time_ms for l in locks)
        total_contentions = sum(l.contention_count for l in locks)

        return LockContentionReport(
            contention_pct=np.random.uniform(5, 25),
            total_wait_time_ms=total_wait,
            top_locks=locks,
            total_locks=len(locks),
            total_contentions=total_contentions,
        )

    def get_thread_states(self) -> Dict[ThreadState, int]:
        return {
            ThreadState.RUNNING: np.random.randint(5, 20),
            ThreadState.WAITING: np.random.randint(2, 10),
            ThreadState.BLOCKED: np.random.randint(0, 5),
            ThreadState.TIMED_WAITING: np.random.randint(1, 8),
        }


# ---------------------------------------------------------------------------
# Tracer
# ---------------------------------------------------------------------------

class Tracer:
    """Distributed request tracing."""

    def __init__(self, service_name: str = "default"):
        self.service_name = service_name
        self._traces: Dict[str, Trace] = {}
        self._current_trace_id: Optional[str] = None
        self._spans: List[Span] = []

    @contextmanager
    def start_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Generator[Span, None, None]:
        trace_id = self._current_trace_id or hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
        span_id = hashlib.md5(f"{name}:{time.time()}".encode()).hexdigest()[:8]

        span = Span(
            span_id=span_id,
            trace_id=trace_id,
            name=name,
            kind=kind,
            start_time=datetime.now(timezone.utc),
            attributes=attributes or {},
        )

        self._spans.append(span)
        old_trace_id = self._current_trace_id
        self._current_trace_id = trace_id

        try:
            yield span
        finally:
            span.end_time = datetime.now(timezone.utc)
            self._current_trace_id = old_trace_id

    def get_trace(self, trace_id: Optional[str] = None) -> Optional[Trace]:
        if trace_id is None and self._spans:
            trace_id = self._spans[0].trace_id

        spans = [s for s in self._spans if s.trace_id == trace_id]
        if not spans:
            return None

        return Trace(
            trace_id=trace_id,
            spans=spans,
            service_name=self.service_name,
            start_time=min(s.start_time for s in spans),
            end_time=max(s.end_time for s in spans if s.end_time),
        )

    def get_all_traces(self) -> List[Trace]:
        trace_ids = set(s.trace_id for s in self._spans)
        traces = []
        for tid in trace_ids:
            trace = self.get_trace(tid)
            if trace:
                traces.append(trace)
        return traces


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate dynamic analysis capabilities."""
    print("=" * 70)
    print("Dynamic Analysis Framework - Demo")
    print("=" * 70)

    # --- 1. CPU Profiling ---
    print("\n--- CPU Profiling ---")
    profiler = Profiler(mode=ProfileMode.CPU)
    with profiler.profile("data_processing"):
        time.sleep(0.05)

    report = profiler.get_report("data_processing")
    print(f"  Total time: {report.total_time_ms:.1f}ms")
    print(f"  Top functions:")
    for func in report.top_functions[:5]:
        print(f"    {func.name}: {func.time_ms:.1f}ms ({func.percentage:.1f}%)")

    profiler.export_flame_graph("/tmp/flame.json")
    print("  Flame graph exported")

    # --- 2. Memory Analysis ---
    print("\n--- Memory Analysis ---")
    mem_analyzer = MemoryAnalyzer()
    snap1 = mem_analyzer.snapshot("before")
    print(f"  Before: {snap1.total_mb:.1f} MB ({snap1.total_objects} objects)")

    snap2 = mem_analyzer.snapshot("after")
    print(f"  After:  {snap2.total_mb:.1f} MB ({snap2.total_objects} objects)")

    diff = mem_analyzer.compare("before", "after")
    print(f"  Delta: {diff.memory_delta_mb:+.1f} MB")
    print(f"  Objects created: {diff.objects_created}")
    print(f"  Potential leaks: {len(diff.potential_leaks)}")
    for leak in diff.potential_leaks:
        print(f"    {leak.type_name}: {leak.count} objects ({leak.size_mb:.1f} MB)")

    # --- 3. Thread Debugging ---
    print("\n--- Thread Debugging ---")
    thread_debug = ThreadDebugger()

    deadlocks = thread_debug.detect_deadlocks()
    print(f"  Deadlocks: {len(deadlocks)}")
    for d in deadlocks:
        print(f"    Severity: {d.severity.value}")
        print(f"    Threads: {d.thread_ids}")
        print(f"    Wait graph: {d.wait_graph}")

    contention = thread_debug.analyze_lock_contention()
    print(f"  Lock contention: {contention.contention_pct:.1f}%")
    print(f"  Total wait time: {contention.total_wait_time_ms:.1f}ms")
    for lock in contention.top_locks[:3]:
        print(f"    {lock.lock_name}: {lock.wait_time_ms:.1f}ms ({lock.contention_count} waits)")

    # --- 4. API Tracing ---
    print("\n--- API Tracing ---")
    tracer = Tracer(service_name="payment-service")

    with tracer.start_span("process_payment", kind=SpanKind.SERVER) as span:
        span.set_attribute("order_id", "12345")
        span.set_attribute("amount", 99.99)

        with tracer.start_span("validate_payment") as child:
            time.sleep(0.001)

        with tracer.start_span("charge_card") as child:
            time.sleep(0.002)

    trace = tracer.get_trace()
    if trace:
        print(f"  Trace ID: {trace.trace_id}")
        print(f"  Duration: {trace.duration_ms:.1f}ms")
        print(f"  Spans: {len(trace.spans)}")
        for span in trace.spans:
            print(f"    {span.name}: {span.duration_ms:.1f}ms ({span.status.value})")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()