"""
Gesture Recognition Module — Hand tracking, body pose estimation, gesture libraries,
dynamic gesture detection, and gesture-to-action mapping.
"""

from __future__ import annotations

import json
import math
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple


class HandSide(Enum):
    LEFT = "left"
    RIGHT = "right"
    AMBIGUOUS = "ambiguous"


class GestureType(Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"
    SEQUENTIAL = "sequential"


@dataclass
class Landmark:
    x: float
    y: float
    z: float
    visibility: float = 1.0

    def distance_to(self, other: "Landmark") -> float:
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2)


@dataclass
class FingerState:
    name: str
    is_extended: bool
    bend_angle: float
    tip: Landmark
    pip: Landmark
    mcp: Landmark


@dataclass
class HandLandmarks:
    landmarks: Dict[str, Landmark]
    handedness: HandSide
    pinch_strength: float = 0.0
    grab_strength: float = 0.0
    confidence: float = 1.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def wrist(self) -> Landmark:
        return self.landmarks.get("WRIST", Landmark(0, 0, 0))

    @property
    def index_tip(self) -> Landmark:
        return self.landmarks.get("INDEX_FINGER_TIP", Landmark(0, 0, 0))

    @property
    def middle_tip(self) -> Landmark:
        return self.landmarks.get("MIDDLE_FINGER_TIP", Landmark(0, 0, 0))

    @property
    def thumb_tip(self) -> Landmark:
        return self.landmarks.get("THUMB_TIP", Landmark(0, 0, 0))

    @property
    def is_open_palm(self) -> bool:
        return self.grab_strength < 0.3 and self.pinch_strength < 0.3

    @property
    def is_pointing(self) -> bool:
        return self.grab_strength < 0.3 and self.index_tip.y < self.middle_tip.y

    @property
    def is_fist(self) -> bool:
        return self.grab_strength > 0.7

    @property
    def is_peace_sign(self) -> bool:
        return self.index_tip.y < self.middle_tip.y and self.grab_strength < 0.4

    def to_dict(self) -> Dict[str, Any]:
        return {
            "handedness": self.handedness.value,
            "pinch": round(self.pinch_strength, 2),
            "grab": round(self.grab_strength, 2),
            "open_palm": self.is_open_palm,
            "pointing": self.is_pointing,
        }


@dataclass
class BodyLandmarks:
    landmarks: Dict[str, Landmark]
    confidence: float = 1.0

    @property
    def is_standing(self) -> bool:
        hip = self.landmarks.get("LEFT_HIP", Landmark(0, 0, 0))
        ankle = self.landmarks.get("LEFT_ANKLE", Landmark(0, 0, 0))
        return (hip.y - ankle.y) > 0.5

    @property
    def arms_raised(self) -> bool:
        shoulder = self.landmarks.get("LEFT_SHOULDER", Landmark(0, 0, 0))
        wrist = self.landmarks.get("LEFT_WRIST", Landmark(0, 0, 0))
        return wrist.y < shoulder.y - 0.2

    @property
    def is_waving(self) -> bool:
        wrist = self.landmarks.get("LEFT_WRIST", Landmark(0, 0, 0))
        return wrist.y < 0.3

    def to_dict(self) -> Dict[str, Any]:
        return {"standing": self.is_standing, "arms_raised": self.arms_raised, "waving": self.is_waving}


@dataclass
class RecognizedGesture:
    name: str
    confidence: float
    gesture_type: GestureType
    hand: Optional[HandSide] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "confidence": round(self.confidence, 2), "type": self.gesture_type.value}


@dataclass
class GestureDefinition:
    name: str
    gesture_type: GestureType
    conditions: Dict[str, Any]
    description: str = ""
    action: str = ""

    def matches(self, hand: HandLandmarks) -> bool:
        if "min_pinch" in self.conditions and hand.pinch_strength < self.conditions["min_pinch"]:
            return False
        if "max_grab" in self.conditions and hand.grab_strength > self.conditions["max_grab"]:
            return False
        if self.conditions.get("open_palm") and not hand.is_open_palm:
            return False
        if self.conditions.get("pointing") and not hand.is_pointing:
            return False
        if self.conditions.get("fist") and not hand.is_fist:
            return False
        return True


@dataclass
class GestureMapping:
    gesture_name: str
    action: str
    context: str = "default"
    cooldown_s: float = 0.5
    enabled: bool = True
    last_triggered: Optional[float] = None

    def should_trigger(self) -> bool:
        if not self.enabled:
            return False
        if self.last_triggered and time.time() - self.last_triggered < self.cooldown_s:
            return False
        return True


class HandTracker:
    def __init__(self, model: str = "mediapipe_hands", max_hands: int = 2,
                 min_detection_confidence: float = 0.7, min_tracking_confidence: float = 0.5):
        self.model = model
        self.max_hands = max_hands
        self.min_detection = min_detection_confidence
        self.min_tracking = min_tracking_confidence
        self._history: List[List[HandLandmarks]] = []

    def process_frame(self, frame_data: Any = None) -> List[HandLandmarks]:
        import random
        hands = []
        for i in range(min(2, self.max_hands)):
            landmarks = {
                "WRIST": Landmark(random.uniform(0.3, 0.7), random.uniform(0.5, 0.8), 0),
                "THUMB_TIP": Landmark(random.uniform(0.2, 0.4), random.uniform(0.4, 0.6), 0.05),
                "INDEX_FINGER_TIP": Landmark(random.uniform(0.3, 0.5), random.uniform(0.2, 0.4), 0.05),
                "MIDDLE_FINGER_TIP": Landmark(random.uniform(0.4, 0.6), random.uniform(0.2, 0.4), 0.05),
                "RING_FINGER_TIP": Landmark(random.uniform(0.5, 0.7), random.uniform(0.3, 0.5), 0.05),
                "PINKY_TIP": Landmark(random.uniform(0.6, 0.8), random.uniform(0.4, 0.6), 0.05),
                "INDEX_FINGER_PIP": Landmark(random.uniform(0.3, 0.5), random.uniform(0.3, 0.5), 0.02),
                "MIDDLE_FINGER_PIP": Landmark(random.uniform(0.4, 0.6), random.uniform(0.3, 0.5), 0.02),
                "INDEX_FINGER_MCP": Landmark(random.uniform(0.3, 0.5), random.uniform(0.5, 0.6), 0),
                "MIDDLE_FINGER_MCP": Landmark(random.uniform(0.4, 0.6), random.uniform(0.5, 0.6), 0),
            }
            hand = HandLandmarks(
                landmarks=landmarks,
                handedness=HandSide.LEFT if i == 0 else HandSide.RIGHT,
                pinch_strength=random.uniform(0, 1),
                grab_strength=random.uniform(0, 1),
            )
            hands.append(hand)
        self._history.append(hands)
        return hands


class GestureLibrary:
    def __init__(self):
        self._gestures: Dict[str, GestureDefinition] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        self.add_gesture(GestureDefinition("pinch", GestureType.STATIC, {"min_pinch": 0.7}, "Thumb-index pinch"))
        self.add_gesture(GestureDefinition("grab", GestureType.STATIC, {"fist": True}, "Closed fist grab"))
        self.add_gesture(GestureDefinition("open_palm", GestureType.STATIC, {"open_palm": True}, "Open hand"))
        self.add_gesture(GestureDefinition("point", GestureType.STATIC, {"pointing": True}, "Index finger point"))
        self.add_gesture(GestureDefinition("peace", GestureType.STATIC, {}, "Peace sign"))

    def add_gesture(self, gesture: GestureDefinition) -> None:
        self._gestures[gesture.name] = gesture

    def recognize(self, hand: HandLandmarks) -> List[RecognizedGesture]:
        results = []
        for name, gesture in self._gestures.items():
            if gesture.matches(hand):
                results.append(RecognizedGesture(
                    name=name, confidence=hand.confidence,
                    gesture_type=gesture.gesture_type, hand=hand.handedness,
                ))
        return results


class GestureMapper:
    def __init__(self):
        self._mappings: List[GestureMapping] = []

    def add_mapping(self, gesture: str, action: str, context: str = "default",
                    cooldown_s: float = 0.5) -> GestureMapping:
        m = GestureMapping(gesture_name=gesture, action=action, context=context, cooldown_s=cooldown_s)
        self._mappings.append(m)
        return m

    def resolve(self, gesture_name: str, context: str = "default") -> Optional[str]:
        for m in self._mappings:
            if m.gesture_name == gesture_name and m.context == context and m.should_trigger():
                m.last_triggered = time.time()
                return m.action
        return None


class BodyPoseTracker:
    def __init__(self):
        self._history: List[BodyLandmarks] = []

    def process_frame(self, frame_data: Any = None) -> BodyLandmarks:
        import random
        landmarks = {
            "LEFT_SHOULDER": Landmark(0.3, 0.3, 0), "RIGHT_SHOULDER": Landmark(0.7, 0.3, 0),
            "LEFT_HIP": Landmark(0.35, 0.6, 0), "RIGHT_HIP": Landmark(0.65, 0.6, 0),
            "LEFT_WRIST": Landmark(0.2, 0.2, 0), "RIGHT_WRIST": Landmark(0.8, 0.2, 0),
            "LEFT_ANKLE": Landmark(0.35, 0.95, 0), "RIGHT_ANKLE": Landmark(0.65, 0.95, 0),
            "NOSE": Landmark(0.5, 0.15, 0),
        }
        pose = BodyLandmarks(landmarks=landmarks)
        self._history.append(pose)
        return pose


class DynamicGestureDetector:
    def __init__(self, max_history: int = 30):
        self.max_history = max_history
        self._landmark_history: List[List[Landmark]] = []

    def add_frame(self, hand: HandLandmarks) -> Optional[RecognizedGesture]:
        tips = [hand.index_tip]
        self._landmark_history.append(tips)
        if len(self._landmark_history) > self.max_history:
            self._landmark_history = self._landmark_history[-self.max_history:]

        if len(self._landmark_history) < 5:
            return None

        recent = self._landmark_history[-5:]
        dx = recent[-1][0].x - recent[0][0].x
        dy = recent[-1][0].y - recent[0][0].y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0.1:
            if abs(dx) > abs(dy):
                direction = "swipe_right" if dx > 0 else "swipe_left"
            else:
                direction = "swipe_down" if dy > 0 else "swipe_up"
            return RecognizedGesture(name=direction, confidence=min(1.0, distance * 5),
                                    gesture_type=GestureType.DYNAMIC, hand=hand.handedness)
        return None


def main():
    print("Gesture Recognition Toolkit")
    print("=" * 60)

    tracker = HandTracker(max_hands=2, min_detection_confidence=0.7)
    hands = tracker.process_frame()
    print(f"Hands detected: {len(hands)}")
    for h in hands:
        print(f"  {h.handedness.value}: pinch={h.pinch_strength:.2f}, grab={h.grab_strength:.2f}")

    library = GestureLibrary()
    for h in hands:
        gestures = library.recognize(h)
        for g in gestures:
            print(f"  Gesture: {g.name} ({g.confidence:.0%})")

    mapper = GestureMapper()
    mapper.add_mapping("pinch", "select", context="ui")
    mapper.add_mapping("grab", "grab", context="world")
    action = mapper.resolve("pinch", context="ui")
    print(f"\nMapped action: {action}")

    body = BodyPoseTracker()
    pose = body.process_frame()
    print(f"\nBody: standing={pose.is_standing}, arms_raised={pose.arms_raised}")

    dynamic = DynamicGestureDetector()
    for h in hands:
        gesture = dynamic.add_frame(h)
        if gesture:
            print(f"Dynamic: {gesture.name}")


if __name__ == "__main__":
    main()
