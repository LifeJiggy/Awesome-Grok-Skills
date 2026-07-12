"""
Context-Aware Computing Module — Multi-dimensional context modeling, sensor fusion,
activity recognition, location intelligence, and adaptive application behavior.
"""

from __future__ import annotations

import json
import math
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ContextDimension(Enum):
    LOCATION = "location"
    ACTIVITY = "activity"
    IDENTITY = "identity"
    TEMPORAL = "temporal"
    SOCIAL = "social"
    ENVIRONMENTAL = "environmental"
    DEVICE = "device"
    PREFERENCE = "preference"


class ActivityType(Enum):
    STILL = "still"
    WALKING = "walking"
    RUNNING = "running"
    CYCLING = "cycling"
    SITTING = "sitting"
    SLEEPING = "sleeping"
    COOKING = "cooking"
    EXERCISING = "exercising"
    MEETING = "meeting"
    COMMUTING = "commuting"
    SHOPPING = "shopping"
    UNKNOWN = "unknown"


class LocationType(Enum):
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    VEHICLE = "vehicle"
    UNKNOWN = "unknown"


class PrivacyLevel(Enum):
    PUBLIC = "public"
    ANONYMIZED = "anonymized"
    PRIVATE = "private"
    SENSITIVE = "sensitive"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ContextSnapshot:
    """A complete context snapshot at a point in time."""
    user_id: str
    timestamp: str
    dimensions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    confidence: float = 1.0
    privacy_level: PrivacyLevel = PrivacyLevel.PRIVATE

    def get(self, dimension: ContextDimension, key: Optional[str] = None) -> Any:
        dim_data = self.dimensions.get(dimension.value, {})
        if key:
            return dim_data.get(key)
        return dim_data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "dimensions": self.dimensions,
            "confidence": self.confidence,
        }


@dataclass
class LocationContext:
    """Location context information."""
    location_type: LocationType
    building: str = ""
    floor: int = 0
    room: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    accuracy_m: float = 10.0
    venue: str = ""
    zone: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.location_type.value,
            "building": self.building,
            "floor": self.floor,
            "room": self.room,
            "lat": self.latitude,
            "lon": self.longitude,
            "accuracy_m": self.accuracy_m,
        }


@dataclass
class ActivityContext:
    """Activity recognition context."""
    primary_activity: str
    confidence: float
    secondary_activity: str = "unknown"
    duration_seconds: float = 0.0
    transition_from: Optional[str] = None
    activity_history: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary": self.primary_activity,
            "confidence": round(self.confidence, 3),
            "secondary": self.secondary_activity,
            "duration_s": round(self.duration_seconds, 1),
        }


@dataclass
class EnvironmentalContext:
    """Environmental sensor context."""
    temperature_f: float = 72.0
    humidity_pct: float = 50.0
    noise_level_db: float = 40.0
    light_lux: float = 300.0
    air_quality_aqi: int = 50
    co2_ppm: int = 400
    uv_index: float = 3.0
    pressure_hpa: float = 1013.25

    def to_dict(self) -> Dict[str, Any]:
        return {
            "temperature_f": round(self.temperature_f, 1),
            "humidity_pct": round(self.humidity_pct, 1),
            "noise_db": round(self.noise_level_db, 1),
            "light_lux": round(self.light_lux, 1),
            "aqi": self.air_quality_aqi,
        }


@dataclass
class SensorReading:
    """A single sensor data point."""
    sensor_type: str
    values: Dict[str, float]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    accuracy: float = 1.0
    sensor_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.sensor_type, "values": self.values, "timestamp": self.timestamp}


@dataclass
class ActivityPrediction:
    """Result of activity recognition."""
    activity: str
    confidence: float
    start_time: str
    end_time: Optional[str] = None
    supporting_sensors: List[str] = field(default_factory=list)
    probability_distribution: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "activity": self.activity,
            "confidence": round(self.confidence, 3),
            "start": self.start_time,
            "end": self.end_time,
        }


@dataclass
class UserPreference:
    """A learned or explicit user preference."""
    preference_id: str
    key: str
    value: Any
    context_condition: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    learned: bool = False
    last_used: str = ""

    def matches_context(self, context: Dict[str, Any]) -> bool:
        for k, v in self.context_condition.items():
            if context.get(k) != v:
                return False
        return True


@dataclass
class AdaptiveRule:
    """A rule for adaptive application behavior."""
    rule_id: str
    name: str
    context_condition: Dict[str, Any]
    behavior: Dict[str, Any]
    enabled: bool = True
    priority: int = 0
    cooldown_s: float = 60.0
    last_triggered: Optional[str] = None
    trigger_count: int = 0

    def matches(self, context: Dict[str, Any]) -> bool:
        for key, expected in self.context_condition.items():
            actual = context.get(key)
            if isinstance(expected, dict):
                for ek, ev in expected.items():
                    if actual is not None and isinstance(actual, dict) and actual.get(ek) != ev:
                        return False
            elif actual != expected:
                return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "enabled": self.enabled,
            "trigger_count": self.trigger_count,
        }


@dataclass
class ContextChange:
    """A detected change in context."""
    change_id: str
    dimension: str
    key: str
    old_value: Any
    new_value: Any
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "change_id": self.change_id,
            "dimension": self.dimension,
            "key": self.key,
            "old": self.old_value,
            "new": self.new_value,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class ContextManager:
    """Manages multi-dimensional context for a user."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self._context: Dict[str, Dict[str, Any]] = {}
        self._history: List[ContextSnapshot] = []
        self._change_listeners: List[Callable] = []

    def update_dimension(self, dimension: ContextDimension, data: Dict[str, Any]) -> List[ContextChange]:
        """Update a context dimension and detect changes."""
        dim_key = dimension.value
        old_data = self._context.get(dim_key, {})
        self._context[dim_key] = {**old_data, **data}

        changes = []
        for key, new_value in data.items():
            old_value = old_data.get(key)
            if old_value != new_value:
                change = ContextChange(
                    change_id=f"CTX-{uuid.uuid4().hex[:8].upper()}",
                    dimension=dim_key,
                    key=key,
                    old_value=old_value,
                    new_value=new_value,
                    confidence=0.9,
                )
                changes.append(change)
                for listener in self._change_listeners:
                    listener(change)

        return changes

    def get_context(self) -> Dict[str, Any]:
        return dict(self._context)

    def get_snapshot(self) -> ContextSnapshot:
        snapshot = ContextSnapshot(
            user_id=self.user_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            dimensions=dict(self._context),
        )
        self._history.append(snapshot)
        return snapshot

    def on_change(self, callback: Callable) -> None:
        self._change_listeners.append(callback)

    def get_history(self, limit: int = 100) -> List[ContextSnapshot]:
        return self._history[-limit:]

    def get_flattened_context(self) -> Dict[str, Any]:
        flat = {}
        for dim, data in self._context.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    flat[f"{dim}.{key}"] = value
            else:
                flat[dim] = data
        return flat


class ActivityRecognizer:
    """Recognize user activities from sensor data using ML models."""

    # Simplified activity classification rules
    ACCEL_THRESHOLDS = {
        "still": (0.0, 0.1),
        "walking": (0.3, 1.5),
        "running": (1.5, 5.0),
        "sitting": (0.0, 0.05),
    }

    def __init__(self, model: str = "lstm_v2"):
        self.model = model
        self._activity_buffer: List[ActivityPrediction] = []

    def recognize(self, sensor_stream: List[Dict[str, Any]]) -> List[ActivityPrediction]:
        """Recognize activities from a sensor data stream."""
        predictions = []
        for reading in sensor_stream:
            accel_magnitude = math.sqrt(
                reading.get("accel_x", 0) ** 2 +
                reading.get("accel_y", 0) ** 2 +
                (reading.get("accel_z", 9.8) - 9.8) ** 2
            )

            activity = "still"
            confidence = 0.9
            for act, (low, high) in self.ACCEL_THRESHOLDS.items():
                if low <= accel_magnitude < high:
                    activity = act
                    confidence = 0.85 + min(accel_magnitude / 10, 0.1)
                    break

            if accel_magnitude >= 5.0:
                activity = "running"
                confidence = 0.88

            prediction = ActivityPrediction(
                activity=activity,
                confidence=confidence,
                start_time=reading.get("timestamp", ""),
                probability_distribution={activity: confidence, "other": 1 - confidence},
            )
            predictions.append(prediction)
            self._activity_buffer.append(prediction)

        return predictions

    def get_dominant_activity(self, window_minutes: int = 5) -> Optional[ActivityPrediction]:
        if not self._activity_buffer:
            return None
        recent = self._activity_buffer[-10:]
        activity_counts: Dict[str, int] = {}
        for p in recent:
            activity_counts[p.activity] = activity_counts.get(p.activity, 0) + 1
        dominant = max(activity_counts, key=activity_counts.get)
        return ActivityPrediction(
            activity=dominant,
            confidence=activity_counts[dominant] / len(recent),
            start_time=recent[0].start_time,
        )


class LocationEngine:
    """Location intelligence using multiple positioning methods."""

    def __init__(self):
        self._wifi_fingerprints: Dict[str, Dict[str, float]] = {}
        self._beacon_positions: Dict[str, Tuple[float, float]] = {}

    def add_wifi_fingerprint(self, location_id: str, fingerprints: Dict[str, float]) -> None:
        self._wifi_fingerprints[location_id] = fingerprints

    def add_beacon(self, beacon_id: str, position: Tuple[float, float]) -> None:
        self._beacon_positions[beacon_id] = position

    def locate_by_wifi(self, observed_rssi: Dict[str, float]) -> Optional[str]:
        best_match = None
        best_distance = float("inf")
        for loc_id, fingerprint in self._wifi_fingerprints.items():
            distance = sum((observed_rssi.get(b, -100) - fingerprint.get(b, -100)) ** 2
                          for b in set(observed_rssi) | set(fingerprint)) ** 0.5
            if distance < best_distance:
                best_distance = distance
                best_match = loc_id
        return best_match

    def locate_by_beacons(self, beacon_ranges: Dict[str, float]) -> Optional[Tuple[float, float]]:
        if len(beacon_ranges) < 3:
            return None
        # Simplified trilateration
        positions = []
        for beacon_id, distance in beacon_ranges.items():
            if beacon_id in self._beacon_positions:
                positions.append((*self._beacon_positions[beacon_id], distance))
        if len(positions) >= 3:
            x = sum(p[0] for p in positions) / len(positions)
            y = sum(p[1] for p in positions) / len(positions)
            return (x, y)
        return None


class AdaptiveEngine:
    """Adaptive behavior engine that responds to context changes."""

    def __init__(self, context_manager: ContextManager):
        self.context_manager = context_manager
        self._rules: List[AdaptiveRule] = []
        self._applied_behaviors: List[Dict[str, Any]] = []

    def add_rule(self, context_condition: Dict[str, Any], behavior: Dict[str, Any],
                 name: str = "", cooldown_s: float = 60.0) -> AdaptiveRule:
        rule = AdaptiveRule(
            rule_id=f"ARULE-{uuid.uuid4().hex[:8].upper()}",
            name=name or f"Rule-{len(self._rules) + 1}",
            context_condition=context_condition,
            behavior=behavior,
            cooldown_s=cooldown_s,
        )
        self._rules.append(rule)
        return rule

    def evaluate(self) -> List[Dict[str, Any]]:
        """Evaluate all rules against current context and return triggered behaviors."""
        flat_context = self.context_manager.get_flattened_context()
        triggered = []
        for rule in sorted(self._rules, key=lambda r: r.priority, reverse=True):
            if not rule.enabled:
                continue
            if rule.matches(flat_context):
                now = time.time()
                if rule.last_triggered:
                    from datetime import datetime as dt
                    last = dt.fromisoformat(rule.last_triggered).timestamp()
                    if now - last < rule.cooldown_s:
                        continue
                rule.last_triggered = datetime.now(timezone.utc).isoformat()
                rule.trigger_count += 1
                triggered.append({
                    "rule": rule.name,
                    "behavior": rule.behavior,
                    "context": flat_context,
                })
                self._applied_behaviors.append(triggered[-1])
        return triggered

    def get_active_rules(self) -> List[AdaptiveRule]:
        return [r for r in self._rules if r.enabled]


class ContextHistory:
    """Store and query historical context data."""

    def __init__(self, max_entries: int = 10000):
        self.max_entries = max_entries
        self._entries: List[ContextSnapshot] = []

    def store(self, snapshot: ContextSnapshot) -> None:
        self._entries.append(snapshot)
        if len(self._entries) > self.max_entries:
            self._entries = self._entries[-self.max_entries:]

    def query(self, dimension: Optional[str] = None, since_minutes: int = 60) -> List[ContextSnapshot]:
        cutoff = datetime.now(timezone.utc).isoformat()
        results = self._entries[-100:]
        if dimension:
            results = [s for s in results if dimension in s.dimensions]
        return results

    def get_duration_in_state(self, dimension: str, key: str, value: Any) -> float:
        """Calculate total time spent in a specific context state."""
        total_seconds = 0.0
        for i in range(1, len(self._entries)):
            prev = self._entries[i - 1].dimensions.get(dimension, {}).get(key)
            if prev == value:
                total_seconds += 300  # simplified time delta
        return total_seconds


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the context-aware computing framework."""
    print("Context-Aware Computing Framework")
    print("=" * 60)

    # Context manager
    ctx = ContextManager(user_id="user-001")
    ctx.update_dimension(ContextDimension.LOCATION, {
        "type": "indoor", "building": "office", "floor": 3, "room": "conference-A",
    })
    ctx.update_dimension(ContextDimension.ACTIVITY, {
        "primary": "meeting", "confidence": 0.92,
    })
    ctx.update_dimension(ContextDimension.ENVIRONMENTAL, {
        "temperature_f": 72.5, "humidity_pct": 45, "noise_level_db": 42,
    })

    context = ctx.get_context()
    print(f"Location: {context['location']['room']}")
    print(f"Activity: {context['activity']['primary']} ({context['activity']['confidence']})")
    print(f"Temp: {context['environmental']['temperature_f']}°F")

    # Activity recognition
    print("\n--- Activity Recognition ---")
    recognizer = ActivityRecognizer()
    readings = [
        {"accel_x": 0.02, "accel_y": 0.01, "accel_z": 9.8, "timestamp": "T12:00:00"},
        {"accel_x": 0.5, "accel_y": -0.3, "accel_z": 9.5, "timestamp": "T12:00:01"},
        {"accel_x": 0.8, "accel_y": -0.5, "accel_z": 9.3, "timestamp": "T12:00:02"},
        {"accel_x": 2.0, "accel_y": -1.0, "accel_z": 8.5, "timestamp": "T12:00:03"},
    ]
    activities = recognizer.recognize(readings)
    for a in activities:
        print(f"  {a.activity}: {a.confidence:.2f}")

    # Adaptive behavior
    print("\n--- Adaptive Engine ---")
    adaptive = AdaptiveEngine(ctx)
    adaptive.add_rule(
        context_condition={"activity.primary": "meeting"},
        behavior={"mute_notifications": True, "dnd": True},
        name="Meeting Mode",
    )
    adaptive.add_rule(
        context_condition={"location.room": "conference-A", "activity.primary": "meeting"},
        behavior={"lights": "dim", "projector": "on"},
        name="Conference Room Setup",
    )
    changes = adaptive.evaluate()
    for c in changes:
        print(f"  Rule '{c['rule']}' triggered → {c['behavior']}")

    # Location engine
    print("\n--- Location Engine ---")
    loc_engine = LocationEngine()
    loc_engine.add_beacon("beacon-1", (0, 0))
    loc_engine.add_beacon("beacon-2", (10, 0))
    loc_engine.add_beacon("beacon-3", (5, 8))
    position = loc_engine.locate_by_beacons({"beacon-1": 2.1, "beacon-2": 8.5, "beacon-3": 4.2})
    if position:
        print(f"  Position: ({position[0]:.1f}, {position[1]:.1f})")

    # Snapshot
    snapshot = ctx.get_snapshot()
    print(f"\nSnapshot: {len(snapshot.dimensions)} dimensions stored")


if __name__ == "__main__":
    main()
