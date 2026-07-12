"""
AR/VR Development Module — Cross-platform XR project management, spatial interaction,
hand/eye tracking, performance optimization, multiplayer networking, and deployment.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Platform(Enum):
    QUEST_2 = "quest_2"
    QUEST_3 = "quest_3"
    QUEST_PRO = "quest_pro"
    VISION_PRO = "vision_pro"
    HOLOLENS_2 = "hololens_2"
    WEBXR = "webxr"
    DESKTOP_VR = "desktop_vr"
    ARKIT = "arkit"
    ARCORE = "arcore"


class Engine(Enum):
    UNITY = "unity"
    UNREAL = "unreal"
    WEBXR_FRAMEWORK = "webxr_framework"
    GODOT = "godot"


class InteractionType(Enum):
    HAND_TRACKING = "hand_tracking"
    CONTROLLER = "controller"
    EYE_TRACKING = "eye_tracking"
    GAZE = "gaze"
    VOICE = "voice"
    BODY_TRACKING = "body_tracking"
    ULTRALEAP = "ultraleap"


class RenderMode(Enum):
    STEREO = "stereo"
    MULTI_VIEW = "multi_view"
    SINGLE_PASS = "single_pass"
    SINGLE_PASS_INSTANCED = "single_pass_instanced"


class LocomotionType(Enum):
    TELEPORT = "teleport"
    SMOOTH = "smooth"
    ARM_SWING = "arm_swing"
    ROOM_SCALE = "room_scale"
    SEATED = "seated"


class BuildConfig(Enum):
    DEBUG = "debug"
    RELEASE = "release"
    PROFILE = "profile"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class XRProject:
    """XR project configuration."""
    name: str
    engine: str = "unity"
    platforms: List[Platform] = field(default_factory=lambda: [Platform.QUEST_3])
    target_framerate: int = 90
    render_scale: float = 1.0
    render_mode: RenderMode = RenderMode.SINGLE_PASS_INSTANCED
    color_space: str = "linear"
    physics_update_rate: int = 90
    tracking_space: str = "stage"
    interactions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    performance_profile: Optional["PerformanceProfile"] = None
    spatial_audio: bool = True
    hand_tracking: bool = True
    eye_tracking: bool = False
    passthrough: bool = False

    def add_interaction(self, interaction_type: InteractionType, config: Dict[str, Any]) -> None:
        self.interactions[interaction_type.value] = config

    def set_performance_profile(self, profile: "PerformanceProfile") -> None:
        self.performance_profile = profile

    def build(self, platform: Platform, configuration: str = "release") -> "BuildResult":
        return BuildResult(
            output_path=f"builds/{self.name}_{platform.value}_{configuration}.apk",
            platform=platform,
            config=BuildConfig(configuration),
            apk_size_mb=150.0 + len(self.interactions) * 5,
            build_time_s=120.0,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "engine": self.engine,
            "platforms": [p.value for p in self.platforms],
            "target_fps": self.target_framerate,
            "interactions": list(self.interactions.keys()),
        }


@dataclass
class PerformanceProfile:
    """Performance optimization profile for XR."""
    target_framerate: int = 90
    ms_per_frame: float = 11.1
    fixed_foveated_rendering_level: int = 3
    application_spacewarp: bool = True
    gpu_skinning: bool = True
    single_pass_stereo: bool = True
    occlusion_culling: bool = True
    gpu_instancing: bool = True
    draw_call_budget: int = 100
    triangle_budget: int = 750000
    texture_memory_mb: int = 512
    max_bone_weights: int = 2

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_fps": self.target_framerate,
            "ms_per_frame": self.ms_per_frame,
            "ffr_level": self.fixed_foveated_rendering_level,
            "draw_call_budget": self.draw_call_budget,
            "triangle_budget": self.triangle_budget,
        }


@dataclass
class BuildResult:
    """Result of an XR build."""
    output_path: str
    platform: Platform
    config: BuildConfig
    apk_size_mb: float = 0
    build_time_s: float = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    success: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.output_path,
            "platform": self.platform.value,
            "size_mb": round(self.apk_size_mb, 1),
            "build_time_s": round(self.build_time_s, 0),
            "success": self.success,
        }


@dataclass
class SpatialAnchor:
    """A persistent spatial anchor."""
    anchor_id: str
    position: Tuple[float, float, float] = (0, 0, 0)
    rotation: Tuple[float, float, float, float] = (0, 0, 0, 1)
    label: str = ""
    persistent: bool = True
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    cloud_synchronized: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "anchor_id": self.anchor_id,
            "position": self.position,
            "label": self.label,
            "persistent": self.persistent,
        }


@dataclass
class HandPose:
    """A captured hand pose."""
    hand: str  # "left" or "right"
    joints: Dict[str, Tuple[float, float, float]] = field(default_factory=dict)
    pinch_strength: float = 0.0
    grab_strength: float = 0.0
    gesture: str = "none"
    confidence: float = 1.0

    @property
    def is_pinching(self) -> bool:
        return self.pinch_strength > 0.7

    @property
    def is_grabbing(self) -> bool:
        return self.grab_strength > 0.7

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hand": self.hand,
            "gesture": self.gesture,
            "pinch": round(self.pinch_strength, 2),
            "grab": round(self.grab_strength, 2),
        }


@dataclass
class GazeData:
    """Eye/gaze tracking data."""
    origin: Tuple[float, float, float] = (0, 0, 0)
    direction: Tuple[float, float, float] = (0, 0, 1)
    confidence: float = 1.0
    pupil_diameter_mm: float = 3.5
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "origin": self.origin,
            "direction": self.direction,
            "confidence": round(self.confidence, 2),
            "pupil_mm": round(self.pupil_diameter_mm, 1),
        }


@dataclass
class SpatialObject:
    """A 3D spatial object in the XR scene."""
    object_id: str
    name: str
    mesh_path: str = ""
    position: Tuple[float, float, float] = (0, 0, 0)
    rotation: Tuple[float, float, float, float] = (0, 0, 0, 1)
    scale: Tuple[float, float, float] = (1, 1, 1)
    interactive: bool = True
    grabbable: bool = True
    physics_enabled: bool = False
    visibility: str = "visible"
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "object_id": self.object_id,
            "name": self.name,
            "position": self.position,
            "interactive": self.interactive,
        }


@dataclass
class XRSession:
    """An active XR session."""
    session_id: str
    user_id: str
    platform: Platform
    start_time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    tracking_quality: float = 1.0
    frame_rate: int = 90
    dropped_frames: int = 0
    interactions_count: int = 0

    @property
    def duration_seconds(self) -> float:
        start = datetime.fromisoformat(self.start_time)
        return (datetime.now(timezone.utc) - start).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "duration_s": round(self.duration_seconds, 1),
            "fps": self.frame_rate,
            "dropped_frames": self.dropped_frames,
        }


@dataclass
class NetworkSyncState:
    """Network synchronization state for multiplayer XR."""
    object_id: str
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float, float]
    velocity: Tuple[float, float, float] = (0, 0, 0)
    owner_id: str = ""
    timestamp: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "object_id": self.object_id,
            "position": self.position,
            "owner": self.owner_id,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class SpatialAnchorManager:
    """Manage persistent spatial anchors."""

    def __init__(self):
        self._anchors: Dict[str, SpatialAnchor] = {}

    def create(self, position: Tuple[float, float, float],
               rotation: Tuple[float, float, float, float] = (0, 0, 0, 1),
               label: str = "", persistent: bool = True) -> SpatialAnchor:
        anchor = SpatialAnchor(
            anchor_id=f"ANC-{uuid.uuid4().hex[:8].upper()}",
            position=position, rotation=rotation,
            label=label, persistent=persistent,
        )
        self._anchors[anchor.anchor_id] = anchor
        return anchor

    def get(self, anchor_id: str) -> Optional[SpatialAnchor]:
        return self._anchors.get(anchor_id)

    def update_position(self, anchor_id: str, position: Tuple[float, float, float]) -> bool:
        anchor = self._anchors.get(anchor_id)
        if anchor:
            anchor.position = position
            return True
        return False

    def delete(self, anchor_id: str) -> bool:
        return self._anchors.pop(anchor_id, None) is not None

    def list_persistent(self) -> List[SpatialAnchor]:
        return [a for a in self._anchors.values() if a.persistent]

    @property
    def count(self) -> int:
        return len(self._anchors)


class HandTracker:
    """Process hand tracking data and recognize gestures."""

    GESTURES = {
        "pinch": lambda pose: pose.pinch_strength > 0.7,
        "grab": lambda pose: pose.grab_strength > 0.7,
        "point": lambda pose: pose.joints.get("index_tip", (0, 0, 0))[2] > 0.5,
        "peace": lambda pose: pose.pinch_strength < 0.3,
        "thumbs_up": lambda pose: pose.joints.get("thumb_tip", (0, 0, 0))[1] > 0.5,
    }

    def __init__(self):
        self._pose_history: List[HandPose] = []

    def process_pose(self, pose: HandPose) -> HandPose:
        gesture = self._recognize_gesture(pose)
        pose.gesture = gesture
        self._pose_history.append(pose)
        return pose

    def _recognize_gesture(self, pose: HandPose) -> str:
        for gesture_name, check_fn in self.GESTURES.items():
            try:
                if check_fn(pose):
                    return gesture_name
            except (KeyError, IndexError):
                continue
        return "open_hand"

    def get_gesture_history(self, limit: int = 10) -> List[HandPose]:
        return self._pose_history[-limit:]


class GazeManager:
    """Process eye tracking and gaze data."""

    def __init__(self, foveated_rendering: bool = True):
        self.foveated_rendering = foveated_rendering
        self._gaze_history: List[GazeData] = []
        self._heat_map: Dict[str, int] = {}

    def process_gaze(self, gaze: GazeData) -> GazeData:
        self._gaze_history.append(gaze)
        key = f"{int(gaze.direction[0]*10)},{int(gaze.direction[1]*10)}"
        self._heat_map[key] = self._heat_map.get(key, 0) + 1
        return gaze

    def get_attention_hotspots(self, top_n: int = 5) -> List[Tuple[str, int]]:
        sorted_items = sorted(self._heat_map.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:top_n]

    def get_fixation_point(self, threshold_s: float = 0.3) -> Optional[Tuple[float, float, float]]:
        if len(self._gaze_history) < 5:
            return None
        recent = self._gaze_history[-5:]
        avg_direction = tuple(sum(g.direction[i] for g in recent) / len(recent) for i in range(3))
        return avg_direction


class XRNetworking:
    """Multiplayer XR networking with spatial synchronization."""

    def __init__(self, room_id: str = "default", max_players: int = 8):
        self.room_id = room_id
        self.max_players = max_players
        self._connected_players: Dict[str, Dict[str, Any]] = {}
        self._sync_states: Dict[str, NetworkSyncState] = {}
        self._message_log: List[Dict[str, Any]] = []

    def join_room(self, player_id: str) -> bool:
        if len(self._connected_players) >= self.max_players:
            return False
        self._connected_players[player_id] = {
            "joined_at": datetime.now(timezone.utc).isoformat(),
            "avatar": "default",
        }
        return True

    def leave_room(self, player_id: str) -> None:
        self._connected_players.pop(player_id, None)

    def sync_object(self, object_id: str, position: Tuple[float, float, float],
                    rotation: Tuple[float, float, float, float] = (0, 0, 0, 1),
                    ownership: str = "dynamic") -> NetworkSyncState:
        state = NetworkSyncState(
            object_id=object_id, position=position, rotation=rotation,
            timestamp=time.time(),
        )
        self._sync_states[object_id] = state
        return state

    def get_sync_state(self, object_id: str) -> Optional[NetworkSyncState]:
        return self._sync_states.get(object_id)

    @property
    def player_count(self) -> int:
        return len(self._connected_players)

    def get_room_info(self) -> Dict[str, Any]:
        return {
            "room_id": self.room_id,
            "players": self.player_count,
            "max_players": self.max_players,
            "synced_objects": len(self._sync_states),
        }


class XRPerformanceMonitor:
    """Monitor XR session performance metrics."""

    def __init__(self):
        self._frame_times: List[float] = []
        self._dropped_frames: int = 0
        self._target_ms: float = 11.1

    def record_frame(self, frame_time_ms: float) -> None:
        self._frame_times.append(frame_time_ms)
        if frame_time_ms > self._target_ms * 1.5:
            self._dropped_frames += 1

    def get_metrics(self) -> Dict[str, Any]:
        if not self._frame_times:
            return {"avg_ms": 0, "p99_ms": 0, "dropped": 0}
        sorted_times = sorted(self._frame_times)
        n = len(sorted_times)
        return {
            "avg_ms": round(sum(sorted_times) / n, 2),
            "p95_ms": round(sorted_times[int(n * 0.95)] if n > 20 else sorted_times[-1], 2),
            "p99_ms": round(sorted_times[int(n * 0.99)] if n > 100 else sorted_times[-1], 2),
            "dropped": self._dropped_frames,
            "total_frames": n,
            "target_ms": self._target_ms,
        }


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the AR/VR development toolkit."""
    print("AR/VR Development Toolkit")
    print("=" * 60)

    project = XRProject(
        name="SpatialCollab",
        engine="unity",
        platforms=[Platform.QUEST_3, Platform.WEBXR],
        target_framerate=90,
    )
    project.add_interaction(InteractionType.HAND_TRACKING, {"gesture_recognition": True})
    project.add_interaction(InteractionType.EYE_TRACKING, {"foveated_rendering": True})
    print(f"Project: {project.name} ({project.engine})")

    # Build
    result = project.build(Platform.QUEST_3, "release")
    print(f"Build: {result.output_path} ({result.apk_size_mb:.0f}MB, {result.build_time_s:.0f}s)")

    # Spatial anchors
    print("\n--- Spatial Anchors ---")
    anchors = SpatialAnchorManager()
    a1 = anchors.create((1.5, 1.0, 2.0), label="Whiteboard")
    a2 = anchors.create((0, 0.5, 3.0), label="Seat")
    print(f"Created {anchors.count} anchors")

    # Hand tracking
    print("\n--- Hand Tracking ---")
    tracker = HandTracker()
    pose = HandPose(hand="right", pinch_strength=0.85, grab_strength=0.2)
    processed = tracker.process_pose(pose)
    print(f"Gesture: {processed.gesture} (pinch: {processed.pinch_strength})")

    # Gaze
    print("\n--- Gaze Tracking ---")
    gaze_mgr = GazeManager(foveated_rendering=True)
    for i in range(10):
        gaze_mgr.process_gaze(GazeData(direction=(0.1 * i, 0, 1)))
    hotspots = gaze_mgr.get_attention_hotspots(3)
    print(f"Hotspots: {len(hotspots)}")

    # Multiplayer
    print("\n--- Multiplayer ---")
    net = XRNetworking(room_id="collab-001", max_players=8)
    net.join_room("player-1")
    net.join_room("player-2")
    net.sync_object("shared-model", (0, 1, 3))
    print(f"Room: {net.get_room_info()}")

    # Performance
    print("\n--- Performance ---")
    monitor = XRPerformanceMonitor()
    import random
    for _ in range(100):
        monitor.record_frame(random.uniform(8, 14))
    metrics = monitor.get_metrics()
    print(f"Avg: {metrics['avg_ms']}ms, Dropped: {metrics['dropped']}/{metrics['total_frames']}")


if __name__ == "__main__":
    main()
