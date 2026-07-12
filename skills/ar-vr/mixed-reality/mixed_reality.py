"""
Mixed Reality Module — Camera passthrough, plane detection, mesh reconstruction,
spatial anchoring, occlusion, lighting estimation, and scene understanding.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PlaneClassification(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    FLOOR = "floor"
    WALL = "wall"
    CEILING = "ceiling"
    TABLE = "table"
    SEAT = "seat"
    DOOR = "door"
    WINDOW = "window"
    UNKNOWN = "unknown"


class MeshResolution(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DepthMode(Enum):
    OFF = "off"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class OcclusionMode(Enum):
    DISABLED = "disabled"
    DEPTH_BUFFER = "depth_buffer"
    SCENE_MESH = "scene_mesh"
    SEMANTIC = "semantic"


class PassthroughStatus(Enum):
    DISABLED = "disabled"
    STARTING = "starting"
    ACTIVE = "active"
    ERROR = "error"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class DetectedPlane:
    """A detected real-world plane."""
    plane_id: str
    classification: PlaneClassification
    center: Tuple[float, float, float]
    normal: Tuple[float, float, float]
    extent_x: float = 1.0
    extent_z: float = 1.0
    area_sqm: float = 1.0
    confidence: float = 0.9
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    alignment: str = "gravity"

    @property
    def is_horizontal(self) -> bool:
        return self.classification in (
            PlaneClassification.HORIZONTAL, PlaneClassification.FLOOR,
            PlaneClassification.TABLE, PlaneClassification.SEAT,
        )

    @property
    def is_vertical(self) -> bool:
        return self.classification in (
            PlaneClassification.VERTICAL, PlaneClassification.WALL,
            PlaneClassification.DOOR, PlaneClassification.WINDOW,
        )

    def contains_point(self, x: float, z: float, margin: float = 0.1) -> bool:
        return (abs(x - self.center[0]) <= self.extent_x / 2 + margin and
                abs(z - self.center[2]) <= self.extent_z / 2 + margin)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plane_id": self.plane_id,
            "classification": self.classification.value,
            "center": self.center,
            "area_sqm": round(self.area_sqm, 2),
            "confidence": round(self.confidence, 2),
        }


@dataclass
class MeshData:
    """Reconstructed mesh data."""
    vertices: List[Tuple[float, float, float]] = field(default_factory=list)
    triangles: List[Tuple[int, int, int]] = field(default_factory=list)
    normals: List[Tuple[float, float, float]] = field(default_factory=list)
    uvs: List[Tuple[float, float]] = field(default_factory=list)

    @property
    def vertex_count(self) -> int:
        return len(self.vertices)

    @property
    def triangle_count(self) -> int:
        return len(self.triangles)

    @property
    def byte_size(self) -> int:
        return self.vertex_count * 12 + self.triangle_count * 12

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vertices": self.vertex_count,
            "triangles": self.triangle_count,
            "byte_size": self.byte_size,
        }


@dataclass
class SpatialAnchorMR:
    """A mixed reality spatial anchor."""
    anchor_id: str
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float, float] = (0, 0, 0, 1)
    name: str = ""
    cloud_synced: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    track_state: str = "tracking"
    associated_plane: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "anchor_id": self.anchor_id,
            "position": self.position,
            "name": self.name,
            "cloud_synced": self.cloud_synced,
            "track_state": self.track_state,
        }


@dataclass
class LightingEstimate:
    """Environment lighting estimation."""
    ambient_intensity: float = 1000.0
    ambient_temperature: float = 6500.0
    main_light_direction: Tuple[float, float, float] = (0, -1, 0)
    main_light_intensity: float = 1000.0
    spherical_harmonics: List[float] = field(default_factory=lambda: [0.0] * 27)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def is_dim(self) -> bool:
        return self.ambient_intensity < 300

    @property
    def color_temperature(self) -> str:
        if self.ambient_temperature < 4000:
            return "warm"
        elif self.ambient_temperature < 5500:
            return "neutral"
        return "cool"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intensity": round(self.ambient_intensity, 0),
            "temperature_k": round(self.ambient_temperature, 0),
            "color": self.color_temperature,
        }


@dataclass
class SceneObject:
    """A detected real-world object."""
    object_id: str
    label: str
    confidence: float
    position: Tuple[float, float, float] = (0, 0, 0)
    bounding_box: Optional[Dict[str, float]] = None
    volume立方米: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "object_id": self.object_id,
            "label": self.label,
            "confidence": round(self.confidence, 2),
            "position": self.position,
        }


@dataclass
class PlacedObject:
    """A virtual object placed in the mixed reality scene."""
    object_id: str
    mesh_path: str
    anchor_id: str
    offset: Tuple[float, float, float] = (0, 0, 0)
    scale: Tuple[float, float, float] = (1, 1, 1)
    occlusion_enabled: bool = True
    shadow_casting: bool = True
    interactable: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "object_id": self.object_id,
            "mesh": self.mesh_path,
            "anchor": self.anchor_id,
            "occlusion": self.occlusion_enabled,
        }


@dataclass
class PassthroughConfig:
    """Configuration for camera passthrough."""
    depth_mode: DepthMode = DepthMode.MEDIUM
    color_adjustments: Dict[str, float] = field(default_factory=dict)
    edge_rendering: bool = True
    seamless_blend: bool = True
    chromatic_aberration_correction: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "depth_mode": self.depth_mode.value,
            "edge_rendering": self.edge_rendering,
            "seamless": self.seamless_blend,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class PassthroughManager:
    """Manage camera passthrough for mixed reality."""

    def __init__(self, platform: str = "quest_3", depth_mode: str = "medium",
                 color_adjustments: Optional[Dict[str, float]] = None):
        self.platform = platform
        self.config = PassthroughConfig(
            depth_mode=DepthMode(depth_mode),
            color_adjustments=color_adjustments or {},
        )
        self._status = PassthroughStatus.DISABLED

    def enable(self) -> None:
        self._status = PassthroughStatus.ACTIVE

    def disable(self) -> None:
        self._status = PassthroughStatus.DISABLED

    @property
    def status(self) -> str:
        return self._status.value

    def set_depth_mode(self, mode: str) -> None:
        self.config.depth_mode = DepthMode(mode)


class PlaneDetector:
    """Detect real-world planes from depth data."""

    def __init__(self, min_area: float = 0.25, max_planes: int = 50):
        self.min_area = min_area
        self.max_planes = max_planes
        self._detected_planes: Dict[str, DetectedPlane] = {}

    def detect(self, max_planes: int = 20, min_area_sqm: float = 0.25) -> List[DetectedPlane]:
        """Detect planes in the environment."""
        planes = []
        classifications = [
            PlaneClassification.FLOOR, PlaneClassification.WALL,
            PlaneClassification.TABLE, PlaneClassification.CEILING,
        ]
        for i in range(min(max_planes, 4)):
            plane = DetectedPlane(
                plane_id=f"PLANE-{uuid.uuid4().hex[:8].upper()}",
                classification=classifications[i % len(classifications)],
                center=(0, 0, i * 2),
                normal=(0, 1, 0) if i % 2 == 0 else (0, 0, 1),
                area_sqm=2.0 + i * 0.5,
                confidence=0.85 + i * 0.03,
            )
            self._detected_planes[plane.plane_id] = plane
            planes.append(plane)
        return planes

    def find_plane(self, classification: Optional[str] = None,
                   min_area: float = 0.0) -> Optional[DetectedPlane]:
        for plane in self._detected_planes.values():
            if classification and plane.classification.value != classification:
                continue
            if plane.area_sqm >= min_area:
                return plane
        return None

    def get_planes(self) -> List[DetectedPlane]:
        return list(self._detected_planes.values())


class MeshReconstructor:
    """Reconstruct 3D mesh from depth data."""

    def __init__(self, resolution: str = "medium", max_triangles: int = 100000):
        self.resolution = MeshResolution(resolution)
        self.max_triangles = max_triangles

    def reconstruct(self) -> MeshData:
        """Reconstruct mesh from depth data."""
        import random
        vertex_count = {"low": 1000, "medium": 5000, "high": 20000}.get(self.resolution.value, 5000)
        vertices = [(random.uniform(-5, 5), random.uniform(0, 3), random.uniform(-5, 5))
                    for _ in range(vertex_count)]
        triangle_count = min(vertex_count * 2, self.max_triangles)
        triangles = [(i, i+1, i+2) for i in range(0, triangle_count, 3)]
        normals = [(0, 1, 0)] * vertex_count

        return MeshData(vertices=vertices, triangles=triangles, normals=normals)


class OcclusionManager:
    """Manage virtual object occlusion by real-world geometry."""

    def __init__(self, depth_buffer: str = "environment"):
        self.depth_buffer = depth_buffer
        self._occluded_objects: Dict[str, bool] = {}

    def enable_for_object(self, object_id: str) -> None:
        self._occluded_objects[object_id] = True

    def disable_for_object(self, object_id: str) -> None:
        self._occluded_objects[object_id] = False

    def is_occluded(self, object_id: str) -> bool:
        return self._occluded_objects.get(object_id, False)


class LightingEstimator:
    """Estimate real-world environment lighting."""

    def estimate(self) -> LightingEstimate:
        import random
        return LightingEstimate(
            ambient_intensity=random.uniform(200, 2000),
            ambient_temperature=random.uniform(3000, 7000),
            main_light_direction=(random.uniform(-0.3, 0.3), -1, random.uniform(-0.3, 0.3)),
            main_light_intensity=random.uniform(500, 3000),
        )


class SceneUnderstanding:
    """Semantic understanding of the real-world scene."""

    def analyze(self, planes: List[DetectedPlane], mesh: Optional[MeshData] = None) -> List[SceneObject]:
        objects = []
        for plane in planes:
            if plane.classification == PlaneClassification.TABLE:
                objects.append(SceneObject(
                    object_id=f"OBJ-{uuid.uuid4().hex[:8].upper()}",
                    label="table",
                    confidence=plane.confidence,
                    position=plane.center,
                ))
            elif plane.classification == PlaneClassification.FLOOR:
                objects.append(SceneObject(
                    object_id=f"OBJ-{uuid.uuid4().hex[:8].upper()}",
                    label="floor",
                    confidence=plane.confidence,
                    position=plane.center,
                ))
        return objects


class MRSceneManager:
    """Manage virtual objects in the mixed reality scene."""

    def __init__(self):
        self._anchors: Dict[str, SpatialAnchorMR] = {}
        self._placed_objects: Dict[str, PlacedObject] = {}

    def place_object(self, object_id: str, mesh_path: str,
                     plane_id: str, offset: Tuple[float, float, float] = (0, 0, 0)) -> SpatialAnchorMR:
        anchor = SpatialAnchorMR(
            anchor_id=f"ANC-{uuid.uuid4().hex[:8].upper()}",
            position=(0, 0.5, 2),
            name=object_id,
            associated_plane=plane_id,
        )
        self._anchors[anchor.anchor_id] = anchor

        placed = PlacedObject(
            object_id=object_id, mesh_path=mesh_path,
            anchor_id=anchor.anchor_id, offset=offset,
        )
        self._placed_objects[object_id] = placed
        return anchor

    def remove_object(self, object_id: str) -> bool:
        placed = self._placed_objects.pop(object_id, None)
        if placed:
            self._anchors.pop(placed.anchor_id, None)
            return True
        return False

    def get_placed_objects(self) -> List[PlacedObject]:
        return list(self._placed_objects.values())


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the mixed reality toolkit."""
    print("Mixed Reality Toolkit")
    print("=" * 60)

    # Passthrough
    pt = PassthroughManager(platform="quest_3", depth_mode="medium")
    pt.enable()
    print(f"Passthrough: {pt.status}")

    # Plane detection
    detector = PlaneDetector()
    planes = detector.detect(max_planes=5)
    print(f"\nDetected {len(planes)} planes:")
    for p in planes:
        print(f"  {p.classification.value}: {p.area_sqm:.2f}m² ({p.confidence:.0%})")

    # Find table
    table = detector.find_plane(classification="table", min_area=0.5)
    if table:
        print(f"\nFound table: {table.plane_id}")

    # Mesh
    mesh = MeshReconstructor(resolution="medium")
    mesh_data = mesh.reconstruct()
    print(f"\nMesh: {mesh_data.vertex_count} vertices, {mesh_data.triangle_count} triangles")

    # Place object
    scene = MRSceneManager()
    if table:
        anchor = scene.place_object("coffee-mug", "models/mug.glb", table.plane_id, offset=(0, 0.05, 0))
        print(f"\nPlaced object at {anchor.position}")

    # Lighting
    estimator = LightingEstimator()
    light = estimator.estimate()
    print(f"\nLighting: {light.ambient_intensity:.0f} lux, {light.color_temperature}")

    # Scene understanding
    understanding = SceneUnderstanding()
    objects = understanding.analyze(planes, mesh_data)
    print(f"\nScene objects: {len(objects)}")
    for obj in objects:
        print(f"  {obj.label} ({obj.confidence:.0%})")


if __name__ == "__main__":
    main()
