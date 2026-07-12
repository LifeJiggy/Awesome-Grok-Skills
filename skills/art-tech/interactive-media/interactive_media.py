"""
Interactive Media Module — Input processing, state machines, visitor profiles,
adaptive content, analytics, and multi-user interactive experiences.
"""

from __future__ import annotations

import json
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


class InputType(Enum):
    TOUCH = "touch"
    GESTURE = "gesture"
    PROXIMITY = "proximity"
    VOICE = "voice"
    BIOMETRIC = "biometric"
    MOTION = "motion"
    RFID = "rfid"
    NFC = "nfc"


class StateTransition(Enum):
    PROXIMITY_ENTER = "proximity_enter"
    PROXIMITY_EXIT = "proximity_exit"
    TOUCH_INTERACTION = "touch_interaction"
    VOICE_COMMAND = "voice_command"
    TIMER = "timer"
    COUNT_REACHED = "count_reached"
    MANUAL = "manual"


class VisitorEngagement(Enum):
    PASSIVE = "passive"
    CURIOUS = "curious"
    ENGAGED = "engaged"
    DEEP = "deep"


@dataclass
class TouchPoint:
    x: float
    y: float
    pressure: float = 1.0
    surface_id: str = ""
    gesture: str = "tap"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ProximityReading:
    sensor_id: str
    distance_m: float
    direction: Tuple[float, float] = (0, 0)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def is_present(self) -> bool:
        return self.distance_m < 3.0


@dataclass
class VoiceEvent:
    command: str
    confidence: float
    speaker_id: str = ""
    language: str = "en"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class State:
    state_id: str
    name: str
    content: str = ""
    duration_s: float = 0
    transition_on: Optional[str] = None
    next_state: Optional[str] = None
    on_enter: Optional[str] = None
    on_exit: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.state_id, "name": self.name, "content": self.content, "duration": self.duration_s}


@dataclass
class StateTransitionRecord:
    from_state: str
    to_state: str
    trigger: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {"from": self.from_state, "to": self.to_state, "trigger": self.trigger}


@dataclass
class VisitorProfile:
    visitor_id: str
    first_visit: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    visit_count: int = 1
    total_duration_s: float = 0
    total_interactions: int = 0
    interaction_types: Dict[str, int] = field(default_factory=dict)
    spaces_visited: List[str] = field(default_factory=list)
    preferred_content: Optional[str] = None
    engagement_level: VisitorEngagement = VisitorEngagement.PASSIVE
    visit_history: List[Dict[str, Any]] = field(default_factory=list)

    def record_visit(self, space: str, duration_s: float) -> None:
        self.total_duration_s += duration_s
        if space not in self.spaces_visited:
            self.spaces_visited.append(space)
        self.visit_history.append({"space": space, "duration": duration_s, "timestamp": datetime.now(timezone.utc).isoformat()})

    def record_interaction(self, type: str, count: int = 1) -> None:
        self.total_interactions += count
        self.interaction_types[type] = self.interaction_types.get(type, 0) + count
        self._update_engagement()

    def _update_engagement(self) -> None:
        score = self.total_interactions * 2 + self.visit_count * 5 + len(self.spaces_visited) * 3
        if score > 50:
            self.engagement_level = VisitorEngagement.DEEP
        elif score > 20:
            self.engagement_level = VisitorEngagement.ENGAGED
        elif score > 5:
            self.engagement_level = VisitorEngagement.CURIOUS

    def to_dict(self) -> Dict[str, Any]:
        return {
            "visitor_id": self.visitor_id,
            "visits": self.visit_count,
            "duration_s": round(self.total_duration_s, 1),
            "interactions": self.total_interactions,
            "engagement": self.engagement_level.value,
        }


@dataclass
class AnalyticsEvent:
    event_id: str
    event_type: str
    space_id: str
    visitor_id: str = ""
    duration_s: float = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.event_type, "space": self.space_id, "duration": round(self.duration_s, 1)}


@dataclass
class ContentVariant:
    variant_id: str
    name: str
    file_path: str
    target_engagement: VisitorEngagement = VisitorEngagement.PASSIVE
    trigger_conditions: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.variant_id, "name": self.name, "engagement": self.target_engagement.value}


class InputProcessor:
    def __init__(self):
        self._touch_surfaces: Dict[str, Dict[str, Any]] = {}
        self._proximity_sensors: Dict[str, Dict[str, Any]] = {}
        self._voice_config: Dict[str, Any] = {}
        self._input_log: List[Dict[str, Any]] = []

    def add_touch_surface(self, surface_id: str, max_points: int = 10) -> None:
        self._touch_surfaces[surface_id] = {"max_points": max_points, "touches": []}

    def add_proximity_sensor(self, sensor_id: str, range_m: float = 3.0) -> None:
        self._proximity_sensors[sensor_id] = {"range_m": range_m}

    def add_voice_recognition(self, language: str = "en", wake_word: str = "") -> None:
        self._voice_config = {"language": language, "wake_word": wake_word}

    def process_touch(self, surface_id: str, point: TouchPoint) -> None:
        self._input_log.append({"type": "touch", "surface": surface_id, "point": (point.x, point.y)})

    def process_proximity(self, sensor_id: str, reading: ProximityReading) -> None:
        self._input_log.append({"type": "proximity", "sensor": sensor_id, "distance": reading.distance_m})

    def get_input_count(self, input_type: Optional[str] = None, last_n: int = 100) -> int:
        inputs = self._input_log[-last_n:]
        if input_type:
            inputs = [i for i in inputs if i["type"] == input_type]
        return len(inputs)


class StateMachine:
    def __init__(self, initial_state: str = "idle"):
        self._states: Dict[str, State] = {}
        self._current_state: str = initial_state
        self._transitions: List[StateTransitionRecord] = []
        self._state_enter_time: float = time.time()

    def add_state(self, name: str, content: str = "", duration: float = 0,
                  transition_on: Optional[str] = None, next_state: Optional[str] = None, **kwargs: Any) -> State:
        state = State(state_id=f"STATE-{name}", name=name, content=content,
                     duration_s=duration, transition_on=transition_on, next_state=next_state, **kwargs)
        self._states[name] = state
        return state

    @property
    def current_state(self) -> Optional[State]:
        return self._states.get(self._current_state)

    @property
    def current_state_name(self) -> str:
        return self._current_state

    def trigger(self, trigger_type: str) -> Optional[str]:
        state = self.current_state
        if not state:
            return None

        if state.transition_on == trigger_type and state.next_state:
            old = self._current_state
            self._current_state = state.next_state
            self._state_enter_time = time.time()
            self._transitions.append(StateTransitionRecord(
                from_state=old, to_state=self._current_state, trigger=trigger_type,
            ))
            return self._current_state

        if state.duration_s > 0:
            elapsed = time.time() - self._state_enter_time
            if elapsed >= state.duration_s and state.next_state:
                old = self._current_state
                self._current_state = state.next_state
                self._state_enter_time = time.time()
                self._transitions.append(StateTransitionRecord(
                    from_state=old, to_state=self._current_state, trigger="timer",
                ))
                return self._current_state
        return None

    def force_state(self, state_name: str) -> None:
        if state_name in self._states:
            self._current_state = state_name
            self._state_enter_time = time.time()

    def get_transition_history(self, limit: int = 20) -> List[StateTransitionRecord]:
        return self._transitions[-limit:]


class AdaptiveContent:
    def __init__(self):
        self._variants: Dict[str, List[ContentVariant]] = {}

    def add_variant(self, state: str, variant: ContentVariant) -> None:
        if state not in self._variants:
            self._variants[state] = []
        self._variants[state].append(variant)

    def select_variant(self, state: str, engagement: VisitorEngagement) -> Optional[ContentVariant]:
        variants = self._variants.get(state, [])
        if not variants:
            return None
        matching = [v for v in variants if v.target_engagement == engagement]
        if matching:
            return matching[0]
        return variants[0] if variants else None


class Analytics:
    def __init__(self):
        self._events: List[AnalyticsEvent] = []
        self._visitor_profiles: Dict[str, VisitorProfile] = {}

    def track(self, event_type: str, space_id: str, visitor_id: str = "", **kwargs: Any) -> AnalyticsEvent:
        event = AnalyticsEvent(
            event_id=f"AE-{uuid.uuid4().hex[:8]}",
            event_type=event_type, space_id=space_id,
            visitor_id=visitor_id, **kwargs,
        )
        self._events.append(event)
        if visitor_id:
            if visitor_id not in self._visitor_profiles:
                self._visitor_profiles[visitor_id] = VisitorProfile(visitor_id=visitor_id)
            profile = self._visitor_profiles[visitor_id]
            if event_type == "visit":
                profile.record_visit(space_id, kwargs.get("duration_s", 0))
            elif event_type == "interaction":
                profile.record_interaction(kwargs.get("interaction_type", "unknown"))
        return event

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_events": len(self._events),
            "unique_visitors": len(self._visitor_profiles),
            "avg_duration": sum(p.total_duration_s for p in self._visitor_profiles.values()) / max(1, len(self._visitor_profiles)),
        }

    def get_visitor(self, visitor_id: str) -> Optional[VisitorProfile]:
        return self._visitor_profiles.get(visitor_id)


class InteractiveExperience:
    def __init__(self, name: str, max_concurrent_users: int = 20, input_types: Optional[List[str]] = None):
        self.name = name
        self.max_concurrent_users = max_concurrent_users
        self.input_types = input_types or []
        self._inputs = InputProcessor()
        self._state_machine = StateMachine()
        self._adaptive = AdaptiveContent()
        self._analytics = Analytics()
        self._active_visitors: Dict[str, VisitorProfile] = {}

    @property
    def inputs(self) -> InputProcessor:
        return self._inputs

    @property
    def state_machine(self) -> StateMachine:
        return self._state_machine

    @property
    def adaptive(self) -> AdaptiveContent:
        return self._adaptive

    @property
    def analytics(self) -> Analytics:
        return self._analytics

    def visitor_enter(self, visitor_id: str) -> bool:
        if len(self._active_visitors) >= self.max_concurrent_users:
            return False
        profile = VisitorProfile(visitor_id=visitor_id)
        self._active_visitors[visitor_id] = profile
        self._analytics.track("enter", "main", visitor_id)
        return True

    def visitor_exit(self, visitor_id: str) -> None:
        profile = self._active_visitors.pop(visitor_id, None)
        if profile:
            self._analytics.track("exit", "main", visitor_id, duration_s=profile.total_duration_s)

    @property
    def active_count(self) -> int:
        return len(self._active_visitors)


def main():
    print("Interactive Media Toolkit")
    print("=" * 60)

    exp = InteractiveExperience(name="Digital Garden", max_concurrent_users=20, input_types=["touch", "proximity", "voice"])

    inputs = exp.inputs
    inputs.add_touch_surface("wall-main", max_points=10)
    inputs.add_proximity_sensor("entrance", range_m=3.0)
    inputs.add_voice_recognition(language="en", wake_word="garden")
    print(f"Input surfaces: {len(inputs._touch_surfaces)}")

    sm = exp.state_machine
    sm.add_state("idle", content="ambient_loop.mp4", transition_on="proximity_enter", next_state="welcome")
    sm.add_state("welcome", content="welcome.mp4", duration=5, next_state="explore")
    sm.add_state("explore", content="interactive_garden.mp4", transition_on="touch_interaction", next_state="grow")
    sm.add_state("grow", content="growing.mp4", duration=10, next_state="explore")
    print(f"States: {len(sm._states)}")

    sm.trigger("proximity_enter")
    print(f"Current state: {sm.current_state_name}")

    exp.adaptive.add_variant("explore", ContentVariant("V1", "day_mode", "day.mp4", VisitorEngagement.PASSIVE))
    exp.adaptive.add_variant("explore", ContentVariant("V2", "night_mode", "night.mp4", VisitorEngagement.ENGAGED))
    variant = exp.adaptive.select_variant("explore", VisitorEngagement.ENGAGED)
    print(f"Adaptive content: {variant.name if variant else 'none'}")

    exp.visitor_enter("visitor-001")
    exp.visitor_enter("visitor-002")
    exp.analytics.track("interaction", "wall-main", "visitor-001", interaction_type="touch")
    exp.analytics.track("visit", "main", "visitor-001", duration_s=120)

    summary = exp.analytics.get_summary()
    print(f"\nAnalytics: {json.dumps(summary, indent=2)}")

    profile = exp.analytics.get_visitor("visitor-001")
    if profile:
        print(f"Visitor: {json.dumps(profile.to_dict(), indent=2)}")


if __name__ == "__main__":
    main()
