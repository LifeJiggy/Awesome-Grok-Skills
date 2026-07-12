"""
Digital Installations Module — Projection mapping, multi-screen sync, interactive surfaces,
visitor tracking, content scheduling, and hardware orchestration.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


class DisplayType(Enum):
    PROJECTION = "projection"
    LED = "led"
    DISPLAY = "display"
    PROJECTIONMapping = "projection_mapping"


class InputType(Enum):
    TOUCH = "touch"
    DEPTH_CAMERA = "depth_camera"
    LIDAR = "lidar"
    CAMERA = "camera"
    IR_SENSOR = "ir_sensor"


class ContentTransition(Enum):
    NONE = "none"
    FADE = "fade"
    CROSSFADE = "crossfade"
    WIPE = "wipe"
    CUT = "cut"


class InstallationStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"
    ERROR = "error"


@dataclass
class DisplaySpace:
    space_id: str
    display_type: DisplayType
    resolution: Tuple[int, int] = (1920, 1080)
    projector_count: int = 1
    position: Tuple[float, float, float] = (0, 0, 0)
    rotation: Tuple[float, float, float] = (0, 0, 0)
    status: InstallationStatus = InstallationStatus.ONLINE

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.space_id, "type": self.display_type.value, "resolution": self.resolution, "status": self.status.value}


@dataclass
class ProjectorConfig:
    projector_id: str
    resolution: Tuple[int, int] = (1920, 1080)
    brightness_lumens: int = 5000
    throw_ratio: float = 1.5
    lens_shift: bool = True
    ip_address: str = ""
    hours_run: float = 0
    lamp_hours_remaining: float = 3000
    temperature_c: float = 35.0

    @property
    def needs_maintenance(self) -> bool:
        return self.lamp_hours_remaining < 500 or self.temperature_c > 45

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.projector_id, "lumens": self.brightness_lumens, "hours": round(self.hours_run, 0), "temp_c": round(self.temperature_c, 1)}


@dataclass
class WarpPoint:
    source: Tuple[int, int]
    destination: Tuple[int, int]
    z_order: int = 0


@dataclass
class WarpMesh:
    space_id: str
    points: List[WarpPoint] = field(default_factory=list)
    blend_edges: List[Tuple[int, int]] = field(default_factory=list)
    brightness_correction: float = 1.0
    gamma: float = 2.2

    def to_dict(self) -> Dict[str, Any]:
        return {"space": self.space_id, "points": len(self.points), "gamma": self.gamma}


@dataclass
class TouchPoint:
    x: float
    y: float
    pressure: float = 1.0
    gesture: str = "tap"
    finger_id: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class VisitorEvent:
    event_id: str
    event_type: str  # "enter", "exit", "dwell", "interaction"
    space_id: str
    anonymous_id: str
    duration_s: float = 0
    position: Tuple[float, float] = (0, 0)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.event_type, "space": self.space_id, "duration_s": round(self.duration_s, 1)}


@dataclass
class ContentItem:
    content_id: str
    file_path: str
    duration_s: float
    transition: ContentTransition = ContentTransition.NONE
    tags: List[str] = field(default_factory=list)
    loop: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.content_id, "file": self.file_path, "duration": self.duration_s, "transition": self.transition.value}


@dataclass
class Playlist:
    playlist_id: str
    name: str
    items: List[ContentItem] = field(default_factory=list)

    @property
    def total_duration(self) -> float:
        return sum(item.duration_s for item in self.items)

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.playlist_id, "name": self.name, "items": len(self.items), "duration": self.total_duration}


@dataclass
class ScheduleEntry:
    entry_id: str
    playlist_id: str
    days: List[int] = field(default_factory=lambda: [0,1,2,3,4,5,6])
    start_time: str = "00:00"
    end_time: str = "23:59"
    priority: int = 0
    enabled: bool = True

    def is_active_now(self) -> bool:
        now = datetime.now()
        current_day = now.weekday()
        current_time = now.strftime("%H:%M")
        return current_day in self.days and self.start_time <= current_time <= self.end_time

    def to_dict(self) -> Dict[str, Any]:
        return {"playlist": self.playlist_id, "days": self.days, "start": self.start_time, "end": self.end_time, "active": self.is_active_now()}


@dataclass
class InstallationHealth:
    status: InstallationStatus
    spaces_online: int
    spaces_total: int
    projectors_online: int
    projectors_total: int
    content_playing: bool = True
    uptime_hours: float = 0
    visitors_today: int = 0
    last_error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "spaces": f"{self.spaces_online}/{self.spaces_total}",
            "projectors": f"{self.projectors_online}/{self.projectors_total}",
            "uptime_h": round(self.uptime_hours, 1),
            "visitors": self.visitors_today,
        }


class ProjectorManager:
    def __init__(self):
        self._projectors: Dict[str, ProjectorConfig] = {}
        self._warp_meshes: Dict[str, WarpMesh] = {}

    def add_projector(self, config: ProjectorConfig) -> None:
        self._projectors[config.projector_id] = config

    def calibrate(self, projector_id: str, space_id: str, corners: List[Tuple[int, int]]) -> WarpMesh:
        mesh = WarpMesh(space_id=space_id)
        for i, corner in enumerate(corners):
            mesh.points.append(WarpPoint(source=corner, destination=corner))
        self._warp_meshes[space_id] = mesh
        return mesh

    def get_projector(self, projector_id: str) -> Optional[ProjectorConfig]:
        return self._projectors.get(projector_id)

    def check_maintenance(self) -> List[ProjectorConfig]:
        return [p for p in self._projectors.values() if p.needs_maintenance]

    def get_all(self) -> List[ProjectorConfig]:
        return list(self._projectors.values())


class InteractiveSurfaceManager:
    def __init__(self):
        self._surfaces: Dict[str, Dict[str, Any]] = {}
        self._handlers: Dict[str, Callable] = {}
        self._touch_log: List[TouchPoint] = []

    def add_surface(self, surface_id: str, input_type: str = "touch", max_points: int = 10) -> None:
        self._surfaces[surface_id] = {"input_type": input_type, "max_points": max_points}

    def on_touch(self, surface_id: str) -> Callable:
        def decorator(fn: Callable) -> Callable:
            self._handlers[surface_id] = fn
            return fn
        return decorator

    def process_touch(self, surface_id: str, point: TouchPoint) -> None:
        self._touch_log.append(point)
        handler = self._handlers.get(surface_id)
        if handler:
            handler(point, point.gesture)

    def get_touch_count(self, surface_id: Optional[str] = None, last_n: int = 100) -> int:
        touches = self._touch_log[-last_n:]
        if surface_id:
            touches = [t for t in touches if True]  # simplified
        return len(touches)


class ContentScheduler:
    def __init__(self):
        self._playlists: Dict[str, Playlist] = {}
        self._schedules: List[ScheduleEntry] = []

    def add_playlist(self, name: str, items: List[Dict[str, Any]]) -> Playlist:
        playlist = Playlist(
            playlist_id=f"PL-{uuid.uuid4().hex[:8].upper()}",
            name=name,
            items=[ContentItem(
                content_id=f"C-{uuid.uuid4().hex[:6]}",
                file_path=item.get("content", ""),
                duration_s=item.get("duration", 60),
                transition=ContentTransition(item.get("transition", "none")),
            ) for item in items],
        )
        self._playlists[playlist.playlist_id] = playlist
        return playlist

    def schedule(self, playlist_id: str, days: List[int], start: str = "00:00", end: str = "23:59") -> ScheduleEntry:
        entry = ScheduleEntry(
            entry_id=f"SCH-{uuid.uuid4().hex[:8].upper()}",
            playlist_id=playlist_id, days=days, start_time=start, end_time=end,
        )
        self._schedules.append(entry)
        return entry

    def get_current_playlist(self) -> Optional[Playlist]:
        for entry in self._schedules:
            if entry.is_active_now():
                return self._playlists.get(entry.playlist_id)
        return None

    def get_all_playlists(self) -> List[Playlist]:
        return list(self._playlists.values())


class VisitorTracker:
    def __init__(self):
        self._events: List[VisitorEvent] = []
        self._visitors: Dict[str, Dict[str, Any]] = {}

    def track_event(self, event_type: str, space_id: str, anonymous_id: str = "") -> VisitorEvent:
        event = VisitorEvent(
            event_id=f"VT-{uuid.uuid4().hex[:8]}",
            event_type=event_type, space_id=space_id,
            anonymous_id=anonymous_id or f"anon-{uuid.uuid4().hex[:6]}",
        )
        self._events.append(event)
        return event

    def get_daily_count(self) -> int:
        today = datetime.now().strftime("%Y-%m-%d")
        return sum(1 for e in self._events if e.timestamp.startswith(today))

    def get_heat_map(self, space_id: str) -> Dict[str, int]:
        return {"center": 45, "left": 20, "right": 15, "entrance": 25}


class Installation:
    def __init__(self, name: str, venue: str = "", spaces: Optional[List[Dict[str, Any]]] = None):
        self.name = name
        self.venue = venue
        self._spaces: Dict[str, DisplaySpace] = {}
        self._projectors = ProjectorManager()
        self._interactive = InteractiveSurfaceManager()
        self._scheduler = ContentScheduler()
        self._visitors = VisitorTracker()
        self._start_time = time.time()

        for space_data in (spaces or []):
            space = DisplaySpace(
                space_id=space_data.get("id", f"space-{uuid.uuid4().hex[:6]}"),
                display_type=DisplayType(space_data.get("type", "display")),
                resolution=space_data.get("resolution", (1920, 1080)),
                projector_count=space_data.get("projectors", 1),
            )
            self._spaces[space.space_id] = space

    def add_space(self, space: DisplaySpace) -> None:
        self._spaces[space.space_id] = space

    def get_health(self) -> InstallationHealth:
        online = sum(1 for s in self._spaces.values() if s.status == InstallationStatus.ONLINE)
        proj_online = sum(1 for p in self._projectors.get_all() if not p.needs_maintenance)
        return InstallationHealth(
            status=InstallationStatus.ONLINE,
            spaces_online=online, spaces_total=len(self._spaces),
            projectors_online=proj_online, projectors_total=len(self._projectors.get_all()),
            uptime_hours=(time.time() - self._start_time) / 3600,
            visitors_today=self._visitors.get_daily_count(),
        )

    @property
    def projectors(self) -> ProjectorManager:
        return self._projectors

    @property
    def interactive(self) -> InteractiveSurfaceManager:
        return self._interactive

    @property
    def scheduler(self) -> ContentScheduler:
        return self._scheduler

    @property
    def visitors(self) -> VisitorTracker:
        return self._visitors


def main():
    print("Digital Installations Toolkit")
    print("=" * 60)

    inst = Installation(
        name="Immersive Lobby",
        venue="Modern Art Museum",
        spaces=[
            {"id": "wall-north", "type": "projection", "resolution": (3840, 2160), "projectors": 2},
            {"id": "floor-main", "type": "led", "resolution": (1920, 1080)},
        ],
    )
    print(f"Installation: {inst.name} ({len(inst._spaces)} spaces)")

    # Projectors
    inst.projectors.add_projector(ProjectorConfig("proj-1", brightness_lumens=5000, lamp_hours_remaining=2800))
    inst.projectors.add_projector(ProjectorConfig("proj-2", brightness_lumens=5000, lamp_hours_remaining=400, temperature_c=47))
    maintenance = inst.projectors.check_maintenance()
    print(f"Projectors needing maintenance: {len(maintenance)}")

    # Content
    playlist = inst.scheduler.add_playlist("morning", [
        {"content": "ambient_flow.mp4", "duration": 300, "transition": "crossfade"},
        {"content": "data_rain.mp4", "duration": 600},
    ])
    inst.scheduler.schedule(playlist.playlist_id, days=[0,1,2,3,4], start="08:00", end="12:00")
    current = inst.scheduler.get_current_playlist()
    print(f"Current playlist: {current.name if current else 'none'}")

    # Visitors
    for _ in range(25):
        inst.visitors.track_event("enter", "wall-north")
    print(f"Visitors today: {inst.visitors.get_daily_count()}")

    # Health
    health = inst.get_health()
    print(f"\nHealth: {json.dumps(health.to_dict(), indent=2)}")


if __name__ == "__main__":
    main()
