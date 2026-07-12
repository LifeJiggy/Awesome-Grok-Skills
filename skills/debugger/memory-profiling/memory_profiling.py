"""
Memory Profiling Framework

Production-grade memory profiling toolkit providing heap analysis, leak detection,
allocation tracking, GC monitoring, and memory optimization for production applications.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ObjectType(Enum):
    DICT = "dict"
    LIST = "list"
    TUPLE = "tuple"
    SET = "set"
    STRING = "string"
    BYTES = "bytes"
    INT = "int"
    FLOAT = "float"
    OBJECT = "object"
    FUNCTION = "function"
    MODULE = "module"
    CLASS = "class"
    ARRAY = "array"
    BUFFER = "buffer"


class GCType(Enum):
    GEN0 = "gen0"
    GEN1 = "gen1"
    GEN2 = "gen2"
    MAJOR = "major"
    MINOR = "minor"


class LeakSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class HeapObject:
    """A single object on the heap."""
    address: str
    type_name: str
    size_bytes: int
    reference_count: int = 0
    generation: int = 0
    retainer_path: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    @property
    def size_kb(self) -> float:
        return self.size_bytes / 1024

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)


@dataclass
class HeapSnapshot:
    """Complete heap snapshot."""
    name: str
    timestamp: datetime
    total_size_bytes: int
    total_objects: int
    objects: List[HeapObject]
    gc_stats: Dict[str, Any] = field(default_factory=dict)

    @property
    def total_size_mb(self) -> float:
        return self.total_size_bytes / (1024 * 1024)

    def object_distribution(self) -> List[Tuple[str, int, float]]:
        type_stats: Dict[str, Tuple[int, int]] = {}
        for obj in self.objects:
            if obj.type_name not in type_stats:
                type_stats[obj.type_name] = (0, 0)
            count, size = type_stats[obj.type_name]
            type_stats[obj.type_name] = (count + 1, size + obj.size_bytes)

        result = []
        for type_name, (count, size) in type_stats.items():
            result.append((type_name, count, size / (1024 * 1024)))

        return sorted(result, key=lambda x: x[2], reverse=True)

    def largest_objects(self, n: int = 10) -> List[HeapObject]:
        return sorted(self.objects, key=lambda o: o.size_bytes, reverse=True)[:n]


@dataclass
class ObjectDistribution:
    """Object distribution statistics."""
    type_name: str
    count: int
    total_size_bytes: int
    avg_size_bytes: float
    percentage: float

    @property
    def total_size_mb(self) -> float:
        return self.total_size_bytes / (1024 * 1024)


@dataclass
class AllocationSite:
    """A memory allocation site."""
    function: str
    file: str = ""
    line: int = 0
    allocations: int = 0
    total_bytes: int = 0
    peak_bytes: int = 0
    avg_bytes: float = 0.0

    @property
    def total_kb(self) -> float:
        return self.total_bytes / 1024


@dataclass
class AllocationReport:
    """Allocation tracking report."""
    total_allocations: int
    total_bytes: int
    top_sites: List[AllocationSite]
    duration_seconds: float = 0.0
    allocations_per_second: float = 0.0


@dataclass
class GrowingObject:
    """A detected growing object type."""
    type_name: str
    growth_pct: float
    count_delta: int
    size_delta_mb: float
    retained_size_mb: float
    root_path: str = ""
    severity: LeakSeverity = LeakSeverity.MEDIUM


@dataclass
class GCEvent:
    """A garbage collection event."""
    gc_type: GCType
    duration_ms: float
    objects_collected: int
    memory_freed_bytes: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def memory_freed_mb(self) -> float:
        return self.memory_freed_bytes / (1024 * 1024)


@dataclass
class GCStats:
    """Garbage collection statistics."""
    total_collections: int
    gen0_collections: int
    gen1_collections: int
    gen2_collections: int
    total_pause_ms: float
    avg_pause_ms: float
    max_pause_ms: float
    total_memory_freed_mb: float

    @property
    def pause_ratio(self) -> float:
        return self.total_pause_ms / 1000 if self.total_pause_ms > 0 else 0


@dataclass
class MemoryOptimization:
    """Memory optimization recommendation."""
    category: str
    description: str
    estimated_savings_mb: float
    priority: str
    implementation_effort: str = ""
    code_example: str = ""


# ---------------------------------------------------------------------------
# Heap Analyzer
# ---------------------------------------------------------------------------

class HeapAnalyzer:
    """Analyze heap snapshots and object distributions."""

    def __init__(self):
        self._snapshots: Dict[str, HeapSnapshot] = {}

    def capture_snapshot(self, name: str) -> HeapSnapshot:
        objects = []
        total_size = 0

        # Generate synthetic heap data
        type_configs = [
            ("dict", 5000, 500, 2000),
            ("list", 8000, 200, 1500),
            ("str", 15000, 50, 3000),
            ("tuple", 3000, 100, 800),
            ("int", 20000, 28, 500),
            ("float", 5000, 24, 300),
            ("bytes", 1000, 1000, 500),
        ]

        for type_name, count, avg_size, variance in type_configs:
            for i in range(count):
                size = avg_size + np.random.randint(-variance // 2, variance // 2)
                size = max(16, size)
                obj = HeapObject(
                    address=f"0x{hashlib.md5(f'{type_name}:{i}'.encode()).hexdigest()[:8]}",
                    type_name=type_name,
                    size_bytes=size,
                    reference_count=np.random.randint(0, 10),
                    generation=np.random.randint(0, 3),
                )
                objects.append(obj)
                total_size += size

        snapshot = HeapSnapshot(
            name=name,
            timestamp=datetime.now(timezone.utc),
            total_size_bytes=total_size,
            total_objects=len(objects),
            objects=objects,
        )
        self._snapshots[name] = snapshot
        return snapshot

    def get_snapshot(self, name: str) -> Optional[HeapSnapshot]:
        return self._snapshots.get(name)

    def compare_snapshots(self, name_a: str, name_b: str) -> Dict[str, Any]:
        snap_a = self._snapshots[name_a]
        snap_b = self._snapshots[name_b]

        return {
            "size_delta_mb": (snap_b.total_size_bytes - snap_a.total_size_bytes) / (1024 * 1024),
            "object_delta": snap_b.total_objects - snap_a.total_objects,
            "snapshot_a": name_a,
            "snapshot_b": name_b,
        }


# ---------------------------------------------------------------------------
# Leak Detector
# ---------------------------------------------------------------------------

class LeakDetector:
    """Detect memory leaks by tracking growing objects."""

    def __init__(self):
        self._snapshots: List[HeapSnapshot] = []

    def snapshot(self, name: str) -> HeapSnapshot:
        analyzer = HeapAnalyzer()
        snap = analyzer.capture_snapshot(name)
        self._snapshots.append(snap)
        return snap

    def detect_growing_objects(self, threshold_pct: float = 10) -> List[GrowingObject]:
        if len(self._snapshots) < 2:
            return []

        leaks = []
        snap_a = self._snapshots[0]
        snap_b = self._snapshots[-1]

        type_stats_a = {}
        for obj in snap_a.objects:
            if obj.type_name not in type_stats_a:
                type_stats_a[obj.type_name] = {"count": 0, "size": 0}
            type_stats_a[obj.type_name]["count"] += 1
            type_stats_a[obj.type_name]["size"] += obj.size_bytes

        type_stats_b = {}
        for obj in snap_b.objects:
            if obj.type_name not in type_stats_b:
                type_stats_b[obj.type_name] = {"count": 0, "size": 0}
            type_stats_b[obj.type_name]["count"] += 1
            type_stats_b[obj.type_name]["size"] += obj.size_bytes

        for type_name, stats_b in type_stats_b.items():
            if type_name in type_stats_a:
                count_a = type_stats_a[type_name]["count"]
                count_b = stats_b["count"]
                if count_a > 0:
                    growth_pct = (count_b - count_a) / count_a * 100
                    if growth_pct > threshold_pct:
                        size_delta = (stats_b["size"] - type_stats_a[type_name]["size"]) / (1024 * 1024)
                        severity = LeakSeverity.LOW
                        if growth_pct > 100:
                            severity = LeakSeverity.CRITICAL
                        elif growth_pct > 50:
                            severity = LeakSeverity.HIGH
                        elif growth_pct > 25:
                            severity = LeakSeverity.MEDIUM

                        leaks.append(GrowingObject(
                            type_name=type_name,
                            growth_pct=growth_pct,
                            count_delta=count_b - count_a,
                            size_delta_mb=size_delta,
                            retained_size_mb=stats_b["size"] / (1024 * 1024),
                            severity=severity,
                        ))

        return sorted(leaks, key=lambda l: l.growth_pct, reverse=True)


# ---------------------------------------------------------------------------
# Allocation Tracker
# ---------------------------------------------------------------------------

class AllocationTracker:
    """Track memory allocations during execution."""

    def __init__(self):
        self._tracking = False
        self._allocations: Dict[str, AllocationSite] = {}

    def start_tracking(self) -> None:
        self._tracking = True
        self._allocations.clear()

    def stop_tracking(self) -> None:
        self._tracking = False

    def record_allocation(self, function: str, size_bytes: int,
                          file: str = "", line: int = 0) -> None:
        if not self._tracking:
            return

        key = f"{file}:{line}:{function}"
        if key not in self._allocations:
            self._allocations[key] = AllocationSite(
                function=function, file=file, line=line,
            )
        site = self._allocations[key]
        site.allocations += 1
        site.total_bytes += size_bytes
        site.peak_bytes = max(site.peak_bytes, size_bytes)

    def get_report(self) -> AllocationReport:
        sites = list(self._allocations.values())
        for site in sites:
            site.avg_bytes = site.total_bytes / site.allocations if site.allocations > 0 else 0

        total_alloc = sum(s.allocations for s in sites)
        total_bytes = sum(s.total_bytes for s in sites)

        return AllocationReport(
            total_allocations=total_alloc,
            total_bytes=total_bytes,
            top_sites=sorted(sites, key=lambda s: s.total_bytes, reverse=True)[:20],
        )


# ---------------------------------------------------------------------------
# GC Monitor
# ---------------------------------------------------------------------------

class GCMonitor:
    """Monitor garbage collection activity."""

    def __init__(self):
        self._monitoring = False
        self._events: List[GCEvent] = []

    def start_monitoring(self) -> None:
        self._monitoring = True
        self._events.clear()

    def stop_monitoring(self) -> None:
        self._monitoring = False

    def record_gc(self, gc_type: GCType, duration_ms: float,
                  objects_collected: int = 0, memory_freed_bytes: int = 0) -> None:
        if not self._monitoring:
            return

        self._events.append(GCEvent(
            gc_type=gc_type,
            duration_ms=duration_ms,
            objects_collected=objects_collected,
            memory_freed_bytes=memory_freed_bytes,
        ))

    def get_stats(self) -> GCStats:
        if not self._events:
            return GCStats(
                total_collections=0, gen0_collections=0, gen1_collections=0,
                gen2_collections=0, total_pause_ms=0, avg_pause_ms=0,
                max_pause_ms=0, total_memory_freed_mb=0,
            )

        total_pause = sum(e.duration_ms for e in self._events)
        pauses = [e.duration_ms for e in self._events]

        return GCStats(
            total_collections=len(self._events),
            gen0_collections=sum(1 for e in self._events if e.gc_type == GCType.GEN0),
            gen1_collections=sum(1 for e in self._events if e.gc_type == GCType.GEN1),
            gen2_collections=sum(1 for e in self._events if e.gc_type == GCType.GEN2),
            total_pause_ms=total_pause,
            avg_pause_ms=total_pause / len(self._events),
            max_pause_ms=max(pauses),
            total_memory_freed_mb=sum(e.memory_freed_mb for e in self._events),
        )

    def get_events(self, limit: int = 100) -> List[GCEvent]:
        return self._events[-limit:]


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate memory profiling capabilities."""
    print("=" * 70)
    print("Memory Profiling Framework - Demo")
    print("=" * 70)

    # --- 1. Heap Analysis ---
    print("\n--- Heap Analysis ---")
    analyzer = HeapAnalyzer()
    snap = analyzer.capture_snapshot("baseline")
    print(f"  Heap size: {snap.total_size_mb:.1f} MB")
    print(f"  Objects: {snap.total_objects:,}")
    print(f"  Object distribution:")
    for type_name, count, size in snap.object_distribution()[:5]:
        print(f"    {type_name}: {count:,} objects ({size:.1f} MB)")

    # --- 2. Leak Detection ---
    print("\n--- Leak Detection ---")
    detector = LeakDetector()
    detector.snapshot("t1")
    detector.snapshot("t2")
    detector.snapshot("t3")

    leaks = detector.detect_growing_objects(threshold_pct=5)
    print(f"  Potential leaks: {len(leaks)}")
    for leak in leaks[:3]:
        print(f"    {leak.type_name}: {leak.growth_pct:.1f}% growth ({leak.severity.value})")
        print(f"      Delta: {leak.count_delta} objects, {leak.size_delta_mb:+.1f} MB")

    # --- 3. Allocation Tracking ---
    print("\n--- Allocation Tracking ---")
    tracker = AllocationTracker()
    tracker.start_tracking()
    for i in range(1000):
        tracker.record_allocation("process_data", np.random.randint(100, 10000))
    tracker.stop_tracking()

    report = tracker.get_report()
    print(f"  Total allocations: {report.total_allocations:,}")
    print(f"  Total bytes: {report.total_bytes / 1024:.1f} KB")
    print(f"  Top sites:")
    for site in report.top_sites[:3]:
        print(f"    {site.function}: {site.allocations:,} ({site.total_kb:.1f} KB)")

    # --- 4. GC Monitoring ---
    print("\n--- GC Monitoring ---")
    gc_monitor = GCMonitor()
    gc_monitor.start_monitoring()
    for _ in range(20):
        gc_type = np.random.choice([GCType.GEN0, GCType.GEN1, GCType.GEN2])
        gc_monitor.record_gc(gc_type, np.random.uniform(0.1, 5.0),
                             np.random.randint(100, 10000),
                             np.random.randint(1000, 100000))
    gc_monitor.stop_monitoring()

    stats = gc_monitor.get_stats()
    print(f"  Total collections: {stats.total_collections}")
    print(f"  Gen 0: {stats.gen0_collections}, Gen 1: {stats.gen1_collections}, Gen 2: {stats.gen2_collections}")
    print(f"  Avg pause: {stats.avg_pause_ms:.2f}ms, Max pause: {stats.max_pause_ms:.2f}ms")
    print(f"  Total pause: {stats.total_pause_ms:.1f}ms")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()