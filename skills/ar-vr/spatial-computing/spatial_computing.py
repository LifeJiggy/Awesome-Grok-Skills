"""
Spatial Computing Module — Spatial anchors, world mapping, scene understanding,
spatial persistence, cloud synchronization, and spatial queries.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ElementType(Enum):
    FLOOR = "floor"
    WALL = "wall"
    CEILING = "ceiling"
    TABLE = "table"
    CHAIR = "chair"
    SHELF = "shelf"
    DOOR = "door"
    WINDOW = "window"
    UNKNOWN = "unknown"


class AnchorTrackingState(Enum):
    TRACKING = "tracking"
    LIMITED = "limited"
    STOPPED = "stopped"
    PAUSED = "paused"


class CoordinateSpace(Enum):
    WORLD = "world"
    BODY = "body"
    HEAD = "head"
    ANCHOR = "anchor"


@dataclass
class SpatialAnchor:
    anchor_id: str
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float, float] = (0, 0, 0, 1)
    name: str = ""
    persistent: bool = True
    cloud_anchor_id: Optional[str] = None
    tracking_state: AnchorTrackingState = AnchorTrackingState.TRACKING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"anchor_id": self.anchor_id, "position": self.position, "name": self.name, "cloud_id": self.cloud_anchor_id}


@dataclass
class WorldMesh:
    vertices: List[Tuple[float, float, float]] = field(default_factory=list)
    triangles: List[Tuple[int, int, int]] = field(default_factory=list)
    normals: List[Tuple[float, float, float]] = field(default_factory=list)
    semantic_labels: Dict[int, str] = field(default_factory=dict)

    @property
    def vertex_count(self) -> int:
        return len(self.vertices)

    @property
    def triangle_count(self) -> int:
        return len(self.triangles)


@dataclass
class SceneElement:
    element_id: str
    element_type: ElementType
    label: str
    confidence: float
    bounds: Dict[str, float] = field(default_factory=dict)
    center: Tuple[float, float, float] = (0, 0, 0)
    extents: Tuple[float, float, float] = (1, 1, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.element_id, "type": self.element_type.value, "label": self.label, "confidence": round(self.confidence, 2)}


@dataclass
class RaycastHit:
    point: Tuple[float, float, float]
    normal: Tuple[float, float, float]
    distance: float
    object_id: str = ""
    object_label: str = ""
    plane_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"point": self.point, "distance": round(self.distance, 2), "label": self.object_label}


@dataclass
class SpatialQueryResult:
    objects: List[Dict[str, Any]] = field(default_factory=list)
    count: int = 0


class SpatialAnchorService:
    def __init__(self, cloud_sync: bool = True):
        self.cloud_sync = cloud_sync
        self._anchors: Dict[str, SpatialAnchor] = {}

    def create_anchor(self, position: Tuple[float, float, float], rotation: Tuple[float, float, float, float] = (0, 0, 0, 1), name: str = "", persistent: bool = True) -> SpatialAnchor:
        anchor = SpatialAnchor(anchor_id=f"SA-{uuid.uuid4().hex[:8].upper()}", position=position, rotation=rotation, name=name, persistent=persistent)
        if self.cloud_sync:
            anchor.cloud_anchor_id = f"CLOUD-{uuid.uuid4().hex[:12].upper()}"
        self._anchors[anchor.anchor_id] = anchor
        return anchor

    def get_anchor(self, anchor_id: str) -> Optional[SpatialAnchor]:
        return self._anchors.get(anchor_id)

    def resolve_cloud_anchor(self, cloud_id: str) -> Optional[SpatialAnchor]:
        for a in self._anchors.values():
            if a.cloud_anchor_id == cloud_id:
                return a
        return None

    def list_anchors(self) -> List[SpatialAnchor]:
        return list(self._anchors.values())


class WorldMap:
    def __init__(self, resolution: str = "medium", max_depth_m: float = 10.0):
        self.resolution = resolution
        self.max_depth = max_depth_m

    def reconstruct(self) -> WorldMesh:
        import random
        n = {"low": 500, "medium": 2000, "high": 10000}.get(self.resolution, 2000)
        return WorldMesh(
            vertices=[(random.uniform(-5, 5), random.uniform(0, 3), random.uniform(-5, 5)) for _ in range(n)],
            triangles=[(i, i+1, i+2) for i in range(0, min(n*2, 5000), 3)],
            normals=[(0, 1, 0)] * n,
        )


class SceneUnderstanding:
    def analyze(self) -> List[SceneElement]:
        elements = []
        types = [ElementType.FLOOR, ElementType.WALL, ElementType.CEILING, ElementType.TABLE]
        for i, t in enumerate(types):
            elements.append(SceneElement(element_id=f"SE-{i}", element_type=t, label=t.value, confidence=0.85 + i * 0.03, center=(0, i*0.5, i*2)))
        return elements


class SpatialQuery:
    def __init__(self, world_map: WorldMap):
        self.world_map = world_map

    def raycast(self, origin: Tuple[float, float, float], direction: Tuple[float, float, float], max_distance: float = 10.0) -> Optional[RaycastHit]:
        return RaycastHit(point=(origin[0]+direction[0]*2, 0, origin[2]+direction[2]*2), normal=(0, 1, 0), distance=2.0, object_label="floor")

    def find_nearby(self, position: Tuple[float, float, float], radius: float = 2.0) -> List[Dict[str, Any]]:
        return [{"type": "floor", "distance": 0.5}, {"type": "wall", "distance": 1.8}]


class SpatialPersistence:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def save(self, key: str, data: Dict[str, Any], anchor_id: str) -> None:
        self._store[key] = {**data, "anchor_id": anchor_id, "saved_at": datetime.now(timezone.utc).isoformat()}

    def load(self, key: str) -> Optional[Dict[str, Any]]:
        return self._store.get(key)

    def list_keys(self) -> List[str]:
        return list(self._store.keys())


class SpatialAudio:
    def __init__(self):
        self._sources: Dict[str, Dict[str, Any]] = {}

    def add_source(self, source_id: str, position: Tuple[float, float, float], gain_db: float = 0.0, occlusion: float = 0.0) -> None:
        self._sources[source_id] = {"position": position, "gain_db": gain_db, "occlusion": occlusion}

    def update_position(self, source_id: str, position: Tuple[float, float, float]) -> None:
        if source_id in self._sources:
            self._sources[source_id]["position"] = position

    def get_sources(self) -> Dict[str, Dict[str, Any]]:
        return dict(self._sources)


def main():
    print("Spatial Computing Toolkit")
    print("=" * 60)

    svc = SpatialAnchorService(cloud_sync=True)
    a1 = svc.create_anchor((1.5, 1.0, 2.0), name="Display")
    print(f"Anchor: {a1.anchor_id}, Cloud: {a1.cloud_anchor_id}")

    wm = WorldMap(resolution="medium")
    mesh = wm.reconstruct()
    print(f"Mesh: {mesh.vertex_count} vertices, {mesh.triangle_count} triangles")

    scene = SceneUnderstanding()
    elements = scene.analyze()
    print(f"Scene elements: {len(elements)}")
    for e in elements:
        print(f"  {e.label}: {e.confidence:.0%}")

    query = SpatialQuery(wm)
    hit = query.raycast((0, 1.5, 0), (0, -1, 0))
    print(f"Raycast: {hit.distance:.1f}m on {hit.object_label}")

    persistence = SpatialPersistence()
    persistence.save("user-content", {"model": "cube"}, a1.anchor_id)
    loaded = persistence.load("user-content")
    print(f"Persisted: {loaded is not None}")

    audio = SpatialAudio()
    audio.add_source("s1", (1, 1, 2), gain_db=-6, occlusion=0.3)
    print(f"Audio sources: {len(audio.get_sources())}")


if __name__ == "__main__":
    main()
