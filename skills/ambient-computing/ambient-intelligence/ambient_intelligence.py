"""
Ambient Intelligence Module — Proactive services, natural interaction, adaptive
environments, occupancy analytics, and personalization for invisible computing.
"""

from __future__ import annotations

import json
import math
import random
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

class InteractionMode(Enum):
    VOICE = "voice"
    GESTURE = "gesture"
    PRESENCE = "presence"
    TOUCH = "touch"
    GAZE = "gaze"
    PASSIVE = "passive"


class ComfortLevel(Enum):
    VERY_COLD = "very_cold"
    COLD = "cold"
    COMFORTABLE = "comfortable"
    WARM = "warm"
    HOT = "hot"


class LightingMode(Enum):
    BRIGHT = "bright"
    NORMAL = "normal"
    DIM = "dim"
    WARM = "warm"
    COOL = "cool"
    NIGHT = "night"
    FOCUS = "focus"
    RELAX = "relax"


class AudioMode(Enum):
    SILENT = "silent"
    LOW = "low"
    AMBIENT = "ambient"
    PRESENTATION = "presentation"
    CONFERENCE = "conference"


class ServiceStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LEARNING = "learning"
    ERROR = "error"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ComfortProfile:
    """User or zone comfort preferences."""
    temperature_f: float = 72.0
    humidity_pct: float = 45.0
    noise_db: float = 35.0
    light_lux: float = 300.0
    co2_max_ppm: int = 1000
    lighting_mode: LightingMode = LightingMode.NORMAL
    audio_mode: AudioMode = AudioMode.LOW

    def to_dict(self) -> Dict[str, Any]:
        return {
            "temperature_f": self.temperature_f,
            "humidity_pct": self.humidity_pct,
            "noise_db": self.noise_db,
            "light_lux": self.light_lux,
            "lighting": self.lighting_mode.value,
            "audio": self.audio_mode.value,
        }


@dataclass
class UserPreferences:
    """Individual user preferences for ambient personalization."""
    user_id: str
    preferences: Dict[str, Any] = field(default_factory=dict)
    learned_patterns: Dict[str, Any] = field(default_factory=dict)
    interaction_count: int = 0
    satisfaction_score: float = 0.8
    last_active: str = ""

    def get(self, key: str, default: Any = None) -> Any:
        return self.preferences.get(key, default)

    def update_preference(self, key: str, value: Any, confidence: float = 1.0) -> None:
        self.preferences[key] = value
        self.interaction_count += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "preferences": self.preferences,
            "satisfaction": round(self.satisfaction_score, 2),
        }


@dataclass
class AdaptiveZone:
    """A zone with adaptive environmental controls."""
    zone_id: str
    name: str
    adaptive_lighting: bool = True
    adaptive_climate: bool = True
    adaptive_audio: bool = True
    comfort_targets: Dict[str, Any] = field(default_factory=dict)
    current_state: Dict[str, Any] = field(default_factory=dict)
    occupant_count: int = 0
    comfort_score: float = 85.0

    def apply_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        changes = {}
        for key, value in settings.items():
            if key in self.comfort_targets and self.comfort_targets[key] != value:
                changes[key] = value
        self.current_state.update(settings)
        return changes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "occupants": self.occupant_count,
            "comfort_score": round(self.comfort_score, 1),
            "state": self.current_state,
        }


@dataclass
class ProactiveService:
    """A proactive service that anticipates user needs."""
    service_id: str
    name: str = ""
    trigger: str = ""
    actions: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    learning_enabled: bool = True
    status: ServiceStatus = ServiceStatus.ACTIVE
    execution_count: int = 0
    success_rate: float = 0.9
    last_executed: Optional[str] = None

    def evaluate_trigger(self, context: Dict[str, Any]) -> bool:
        trigger_parts = self.trigger.split("+")
        for part in trigger_parts:
            part = part.strip()
            if "time_between" in part:
                pass  # time check
            elif "user_arrives" in part:
                if context.get("occupant_count", 0) == 0:
                    return False
            elif context.get(part) is None:
                return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "name": self.name,
            "status": self.status.value,
            "executions": self.execution_count,
            "success_rate": round(self.success_rate, 2),
        }


@dataclass
class OccupancyData:
    """Occupancy analytics data point."""
    zone_id: str
    timestamp: str
    occupant_count: int
    duration_avg_min: float = 0.0
    peak_hour: int = 9
    utilization_pct: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone_id": self.zone_id,
            "occupants": self.occupant_count,
            "utilization": round(self.utilization_pct, 1),
        }


@dataclass
class AmbientEvent:
    """An event in the ambient environment."""
    event_id: str
    event_type: str
    zone_id: Optional[str] = None
    description: str = ""
    actions_taken: List[str] = field(default_factory=list)
    user_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "type": self.event_type,
            "zone": self.zone_id,
            "actions": self.actions_taken,
        }


@dataclass
class ConflictResolution:
    """Resolution for multi-occupant preference conflicts."""
    parameter: str
    user_values: Dict[str, float] = field(default_factory=dict)
    resolved_value: float = 0.0
    method: str = "weighted_average"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "parameter": self.parameter,
            "user_values": self.user_values,
            "resolved": self.resolved_value,
            "method": self.method,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class PersonalizationEngine:
    """Learn and apply individual user preferences in shared environments."""

    def __init__(self):
        self._users: Dict[str, UserPreferences] = {}
        self._conflict_history: List[ConflictResolution] = []

    def add_user(self, user_id: str, preferences: Optional[Dict[str, Any]] = None) -> UserPreferences:
        user = UserPreferences(user_id=user_id, preferences=preferences or {})
        self._users[user_id] = user
        return user

    def update_preference(self, user_id: str, key: str, value: Any) -> None:
        if user_id in self._users:
            self._users[user_id].update_preference(key, value)

    def get_user(self, user_id: str) -> Optional[UserPreferences]:
        return self._users.get(user_id)

    def resolve_conflicts(
        self, occupants: List[str], conflict_params: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Resolve preference conflicts between multiple occupants."""
        if not occupants:
            return {}

        conflict_params = conflict_params or ["temperature_f", "lighting_brightness"]
        resolved: Dict[str, Any] = {}

        for param in conflict_params:
            values = {}
            for uid in occupants:
                user = self._users.get(uid)
                if user:
                    val = user.get(param)
                    if val is not None and isinstance(val, (int, float)):
                        values[uid] = float(val)

            if values:
                avg = sum(values.values()) / len(values)
                resolution = ConflictResolution(
                    parameter=param,
                    user_values=values,
                    resolved_value=round(avg, 1),
                    method="weighted_average",
                )
                self._conflict_history.append(resolution)
                resolved[param] = resolution.resolved_value

        return resolved

    def learn_pattern(self, user_id: str, context: Dict[str, Any], action: str) -> None:
        if user_id in self._users:
            patterns = self._users[user_id].learned_patterns
            key = f"{context.get('time_of_day', 'unknown')}.{context.get('activity', 'unknown')}"
            if key not in patterns:
                patterns[key] = []
            patterns[key].append(action)

    def get_satisfaction(self, user_id: str) -> float:
        user = self._users.get(user_id)
        return user.satisfaction_score if user else 0.0


class OccupancyAnalytics:
    """Analyze space utilization and occupancy patterns."""

    def __init__(self):
        self._history: List[OccupancyData] = []
        self._current: Dict[str, int] = {}

    def update(self, zone_id: str, count: int) -> None:
        self._current[zone_id] = count
        self._history.append(OccupancyData(
            zone_id=zone_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            occupant_count=count,
        ))

    def get_utilization(self, zone_id: str) -> float:
        zone_data = [d for d in self._history if d.zone_id == zone_id]
        if not zone_data:
            return 0.0
        avg_occupancy = sum(d.occupant_count for d in zone_data) / len(zone_data)
        return min(100.0, avg_occupancy * 20)  # simplified

    def get_peak_hours(self, zone_id: str) -> Dict[int, float]:
        return {9: 85.0, 10: 90.0, 14: 80.0}  # simplified

    def get_summary(self) -> Dict[str, Any]:
        return {
            "zones_tracked": len(self._current),
            "total_occupants": sum(self._current.values()),
            "data_points": len(self._history),
        }


class AdaptiveLighting:
    """Adaptive lighting control based on context and preferences."""

    def adjust(
        self, zone: AdaptiveZone, context: Dict[str, Any],
        user_prefs: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        settings = {}
        time_hour = context.get("time_hour", 12)
        occupant_count = context.get("occupant_count", 0)

        if occupant_count == 0:
            settings["mode"] = LightingMode.NIGHT.value
            settings["brightness"] = 10
        elif time_hour < 8 or time_hour > 20:
            settings["mode"] = LightingMode.WARM.value
            settings["brightness"] = 60
        elif context.get("activity") == "meeting":
            settings["mode"] = LightingMode.DIM.value
            settings["brightness"] = 50
        elif context.get("activity") == "focused_work":
            settings["mode"] = LightingMode.FOCUS.value
            settings["brightness"] = 85
        else:
            settings["mode"] = LightingMode.NORMAL.value
            settings["brightness"] = 70

        if user_prefs:
            if "lighting_brightness" in user_prefs:
                settings["brightness"] = user_prefs["lighting_brightness"]
            if "lighting_temp" in user_prefs:
                settings["color_temp"] = user_prefs["lighting_temp"]

        zone.current_state.update(settings)
        return settings


class AdaptiveClimate:
    """Adaptive climate control."""

    def adjust(
        self, zone: AdaptiveZone, context: Dict[str, Any],
        user_prefs: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        settings = {}
        target_temp = zone.comfort_targets.get("temperature_f", 72)
        if user_prefs and "temperature_f" in user_prefs:
            target_temp = user_prefs["temperature_f"]

        settings["setpoint_f"] = target_temp
        settings["mode"] = "auto"
        settings["fan_speed"] = "auto"
        zone.current_state.update(settings)
        return settings


class AmbientEnvironment:
    """Main ambient intelligence environment orchestrator."""

    def __init__(self, name: str):
        self.name = name
        self._zones: Dict[str, AdaptiveZone] = {}
        self._services: Dict[str, ProactiveService] = {}
        self._personalization = PersonalizationEngine()
        self._occupancy = OccupancyAnalytics()
        self._lighting = AdaptiveLighting()
        self._climate = AdaptiveClimate()
        self._events: List[AmbientEvent] = []
        self._running = False

    def add_zone(self, **kwargs: Any) -> AdaptiveZone:
        zone = AdaptiveZone(**kwargs)
        self._zones[zone.zone_id] = zone
        return zone

    def add_service(self, service: ProactiveService) -> None:
        self._services[service.service_id] = service

    def start(self) -> None:
        self._running = True
        for zone in self._zones.values():
            self._occupancy.update(zone.zone_id, zone.occupant_count)

    def stop(self) -> None:
        self._running = False

    def process_context(self, context: Dict[str, Any]) -> List[AmbientEvent]:
        """Process context and trigger adaptive behaviors."""
        events = []
        zone_id = context.get("zone_id")
        zone = self._zones.get(zone_id) if zone_id else None

        if zone:
            # Adaptive lighting
            if zone.adaptive_lighting:
                lighting_settings = self._lighting.adjust(zone, context)
                event = AmbientEvent(
                    event_id=f"AMB-{uuid.uuid4().hex[:8].upper()}",
                    event_type="lighting_adjust",
                    zone_id=zone_id,
                    actions_taken=[f"lighting: {lighting_settings}"],
                )
                events.append(event)

            # Adaptive climate
            if zone.adaptive_climate:
                climate_settings = self._climate.adjust(zone, context)
                event = AmbientEvent(
                    event_id=f"AMB-{uuid.uuid4().hex[:8].upper()}",
                    event_type="climate_adjust",
                    zone_id=zone_id,
                    actions_taken=[f"climate: {climate_settings}"],
                )
                events.append(event)

            # Update comfort score
            zone.comfort_score = min(100, 70 + random.uniform(0, 30))

        # Check proactive services
        for service in self._services.values():
            if service.status == ServiceStatus.ACTIVE and service.evaluate_trigger(context):
                service.execution_count += 1
                service.last_executed = datetime.now(timezone.utc).isoformat()
                event = AmbientEvent(
                    event_id=f"SRV-{uuid.uuid4().hex[:8].upper()}",
                    event_type="service_triggered",
                    description=f"Service '{service.name}' activated",
                    actions_taken=service.actions[:3],
                )
                events.append(event)

        self._events.extend(events)
        return events

    def get_status(self) -> Dict[str, Any]:
        active_services = sum(1 for s in self._services.values() if s.status == ServiceStatus.ACTIVE)
        total_occupants = sum(z.occupant_count for z in self._zones.values())
        avg_comfort = (sum(z.comfort_score for z in self._zones.values()) / len(self._zones)
                      if self._zones else 0)
        return {
            "name": self.name,
            "running": self._running,
            "zones": len(self._zones),
            "occupants": total_occupants,
            "active_services": active_services,
            "comfort_score": round(avg_comfort, 1),
            "total_events": len(self._events),
        }


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the ambient intelligence platform."""
    print("Ambient Intelligence Platform")
    print("=" * 60)

    env = AmbientEnvironment(name="Smart Office Floor 3")

    # Add zones
    env.add_zone(zone_id="workspace", name="Open Workspace",
                adaptive_lighting=True, adaptive_climate=True,
                comfort_targets={"temperature_f": 72, "noise_db": 35})
    env.add_zone(zone_id="meeting-room", name="Meeting Room",
                adaptive_lighting=True, adaptive_climate=True,
                comfort_targets={"temperature_f": 71, "noise_db": 30})

    # Add services
    env.add_service(ProactiveService(
        service_id="morning", name="Morning Welcome",
        trigger="user_arrives",
        actions=["lighting(warm,70%)", "temperature(preferred)", "news(low)"],
    ))

    env.start()
    print(f"Environment: {env.name}")

    # Process context
    print("\n--- Context Processing ---")
    events = env.process_context({
        "zone_id": "workspace",
        "occupant_count": 5,
        "time_hour": 10,
        "activity": "focused_work",
    })
    for e in events:
        print(f"  {e.event_type}: {e.actions_taken}")

    # Personalization
    print("\n--- Personalization ---")
    pe = env._personalization
    pe.add_user("alice", {"temperature_f": 71, "lighting_brightness": 70})
    pe.add_user("bob", {"temperature_f": 69, "lighting_brightness": 90})
    resolved = pe.resolve_conflicts(["alice", "bob"], ["temperature_f", "lighting_brightness"])
    print(f"  Compromise: {resolved}")

    # Status
    status = env.get_status()
    print(f"\nStatus: {json.dumps(status, indent=2)}")


if __name__ == "__main__":
    main()
