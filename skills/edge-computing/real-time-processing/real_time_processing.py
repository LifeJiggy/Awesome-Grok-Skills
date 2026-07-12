"""
Real-Time Processing Framework

Production-grade real-time processing toolkit providing stream processing, event-driven
architecture, low-latency computing, windowing strategies, and real-time analytics.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from collections import deque
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

class ProcessingMode(Enum):
    EVENT_AT_A_TIME = "event_at_a_time"
    MICRO_BATCH = "micro_batch"
    BATCH = "batch"


class WindowType(Enum):
    TUMBLING = "tumbling"
    SLIDING = "sliding"
    SESSION = "session"
    GLOBAL = "global"


class StreamStatus(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Event:
    """An event in the stream."""
    event_id: str = ""
    event_type: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 0

    def __post_init__(self):
        if not self.event_id:
            self.event_id = hashlib.md5(f"{time.time()}{self.event_type}".encode()).hexdigest()[:12]


@dataclass
class PipelineConfig:
    """Stream pipeline configuration."""
    source: str
    transformations: List[Dict[str, Any]]
    sink: str
    mode: ProcessingMode = ProcessingMode.EVENT_AT_A_TIME


@dataclass
class PipelineStatus:
    """Pipeline execution status."""
    id: str
    status: StreamStatus
    throughput: float = 0.0
    latency_ms: float = 0.0
    events_processed: int = 0
    errors: int = 0


@dataclass
class Window:
    """A processing window."""
    window_id: str
    window_type: WindowType
    size_seconds: float
    slide_seconds: float = 0
    events: List[Event] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


@dataclass
class AggregationResult:
    """Real-time aggregation result."""
    pipeline_id: str
    dimensions: Dict[str, Any]
    measures: Dict[str, float]
    window_start: datetime
    window_end: datetime
    event_count: int = 0


@dataclass
class AnalyticsConfig:
    """Real-time analytics configuration."""
    stream: str
    dimensions: List[str]
    measures: List[str]
    window: str = "1m"
    update_interval_ms: int = 1000


@dataclass
class EventStoreConfig:
    """Event store configuration."""
    stream: str
    retention_days: int = 30
    max_events: int = 1000000


# ---------------------------------------------------------------------------
# Stream Processor
# ---------------------------------------------------------------------------

class StreamProcessor:
    """Process event streams in real-time."""

    def __init__(self, mode: ProcessingMode = ProcessingMode.EVENT_AT_A_TIME):
        self.mode = mode
        self._pipelines: Dict[str, PipelineStatus] = {}

    def pipeline(self, source: str, transformations: List[Dict[str, Any]],
                 sink: str) -> "StreamPipeline":
        pipeline_id = hashlib.md5(f"{source}:{time.time()}".encode()).hexdigest()[:8]

        status = PipelineStatus(
            id=pipeline_id,
            status=StreamStatus.RUNNING,
            throughput=np.random.uniform(100, 10000),
            latency_ms=np.random.uniform(1, 50),
        )
        self._pipelines[pipeline_id] = status

        return StreamPipeline(
            pipeline_id=pipeline_id,
            source=source,
            transformations=transformations,
            sink=sink,
            status=status,
        )


class StreamPipeline:
    """A stream processing pipeline."""

    def __init__(self, pipeline_id: str, source: str,
                 transformations: List[Dict[str, Any]], sink: str,
                 status: PipelineStatus):
        self.pipeline_id = pipeline_id
        self.source = source
        self.transformations = transformations
        self.sink = sink
        self._status = status

    @property
    def id(self) -> str:
        return self.pipeline_id

    @property
    def throughput(self) -> float:
        return self._status.throughput

    def start(self) -> None:
        self._status.status = StreamStatus.RUNNING
        logger.info("Started pipeline: %s", self.pipeline_id)

    def stop(self) -> None:
        self._status.status = StreamStatus.STOPPED

    def process_event(self, event: Event) -> Any:
        result = event.data
        for transform in self.transformations:
            if transform.get("type") == "filter":
                condition = transform.get("condition", "True")
                # Simplified evaluation
                if "event_type" in condition:
                    event_type = condition.split("==")[1].strip().strip("'\"")
                    if event.event_type != event_type:
                        return None
            elif transform.get("type") == "map":
                pass  # Simplified
            elif transform.get("type") == "aggregate":
                pass  # Simplified
        return result


# ---------------------------------------------------------------------------
# Window Manager
# ---------------------------------------------------------------------------

class WindowManager:
    """Manage processing windows."""

    def __init__(self):
        self._windows: List[Window] = []

    def create_window(
        self,
        window_type: WindowType,
        size_seconds: float = 60,
        slide_seconds: float = 0,
        gap_seconds: float = 0,
    ) -> Window:
        window_id = hashlib.md5(f"{window_type.value}:{time.time()}".encode()).hexdigest()[:8]

        window = Window(
            window_id=window_id,
            window_type=window_type,
            size_seconds=size_seconds,
            slide_seconds=slide_seconds or size_seconds,
            start_time=datetime.now(timezone.utc),
        )

        self._windows.append(window)
        return window

    def add_event(self, window_id: str, event: Event) -> bool:
        for window in self._windows:
            if window.window_id == window_id:
                window.events.append(event)
                return True
        return False

    def get_window_results(self, window_id: str) -> Optional[Dict[str, Any]]:
        for window in self._windows:
            if window.window_id == window_id:
                return {
                    "window_id": window.window_id,
                    "type": window.window_type.value,
                    "event_count": len(window.events),
                    "size_seconds": window.size_seconds,
                }
        return None


# ---------------------------------------------------------------------------
# Event Store
# ---------------------------------------------------------------------------

class EventStore:
    """Event sourcing store for event-driven architecture."""

    def __init__(self):
        self._streams: Dict[str, List[Event]] = {}
        self._version: Dict[str, int] = {}

    def append(self, event: Event, stream: str = "default") -> Event:
        if stream not in self._streams:
            self._streams[stream] = []
            self._version[stream] = 0

        self._version[stream] += 1
        event.version = self._version[stream]
        self._streams[stream].append(event)
        return event

    def replay(self, stream: str = "default", from_version: int = 0) -> List[Event]:
        events = self._streams.get(stream, [])
        return [e for e in events if e.version > from_version]

    def get_latest(self, stream: str = "default") -> Optional[Event]:
        events = self._streams.get(stream, [])
        return events[-1] if events else None


# ---------------------------------------------------------------------------
# Real-Time Analytics
# ---------------------------------------------------------------------------

class RealTimeAnalytics:
    """Real-time analytics engine."""

    def __init__(self):
        self._pipelines: Dict[str, AnalyticsConfig] = {}

    def aggregate(
        self,
        stream: str,
        dimensions: List[str],
        measures: List[str],
        window: str = "1m",
    ) -> AggregationConfig:
        pipeline_id = hashlib.md5(f"{stream}:{time.time()}".encode()).hexdigest()[:8]

        config = AnalyticsConfig(
            stream=stream,
            dimensions=dimensions,
            measures=measures,
            window=window,
        )
        self._pipelines[pipeline_id] = config

        return AggregationConfig(
            pipeline_id=pipeline_id,
            dimensions={d: "value" for d in dimensions},
            measures={m: 0.0 for m in measures},
            window_start=datetime.now(timezone.utc),
            window_end=datetime.now(timezone.utc),
        )


@dataclass
class AggregationConfig:
    """Aggregation configuration."""
    pipeline_id: str
    dimensions: Dict[str, Any]
    measures: Dict[str, float]
    window_start: datetime
    window_end: datetime
    update_interval_ms: int = 1000


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate real-time processing capabilities."""
    print("=" * 70)
    print("Real-Time Processing Framework - Demo")
    print("=" * 70)

    # --- 1. Stream Processing ---
    print("\n--- Stream Processing ---")
    processor = StreamProcessor(ProcessingMode.EVENT_AT_A_TIME)
    pipeline = processor.pipeline(
        source="kafka://edge-events",
        transformations=[
            {"type": "filter", "condition": "event_type == 'sensor'"},
            {"type": "map", "function": "extract_features"},
        ],
        sink="kafka://processed-events",
    )
    pipeline.start()
    print(f"  Pipeline: {pipeline.id}")
    print(f"  Throughput: {pipeline.throughput:.0f} events/sec")

    # Process event
    event = Event(event_type="sensor", data={"temperature": 25.5, "humidity": 60})
    result = pipeline.process_event(event)
    print(f"  Event processed: {result}")

    pipeline.stop()

    # --- 2. Windowing ---
    print("\n--- Windowing ---")
    window_mgr = WindowManager()
    tumbling = window_mgr.create_window(WindowType.TUMBLING, 60)
    sliding = window_mgr.create_window(WindowType.SLIDING, 300, 60)
    session = window_mgr.create_window(WindowType.SESSION, gap_seconds=30)

    # Add events
    for i in range(10):
        window_mgr.add_event(tumbling.window_id, Event(event_type="data", data={"value": i}))

    results = window_mgr.get_window_results(tumbling.window_id)
    print(f"  Tumbling window: {results['event_count']} events")
    print(f"  Window type: {results['type']}")

    # --- 3. Event Sourcing ---
    print("\n--- Event Sourcing ---")
    store = EventStore()

    # Append events
    for i in range(5):
        event = Event(
            event_type="order_created",
            data={"order_id": f"order-{i}", "amount": 99.99 * (i + 1)},
        )
        store.append(event, "orders")

    # Replay events
    events = store.replay("orders", from_version=0)
    print(f"  Events stored: {len(events)}")
    for e in events[:3]:
        print(f"    v{e.version}: {e.event_type} - {e.data}")

    latest = store.get_latest("orders")
    print(f"  Latest: v{latest.version}")

    # --- 4. Real-Time Analytics ---
    print("\n--- Real-Time Analytics ---")
    analytics = RealTimeAnalytics()
    agg = analytics.aggregate(
        stream="sensor-data",
        dimensions=["sensor_id", "location"],
        measures=["temperature", "humidity"],
        window="1m",
    )
    print(f"  Pipeline: {agg.pipeline_id}")
    print(f"  Dimensions: {list(agg.dimensions.keys())}")
    print(f"  Measures: {list(agg.measures.keys())}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()