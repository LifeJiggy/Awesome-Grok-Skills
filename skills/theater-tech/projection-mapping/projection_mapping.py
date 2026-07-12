"""
Projection Mapping System
3D surface calibration, multi-projector alignment, edge blending, mesh deformation,
color calibration, and media server integration.
"""

from __future__ import annotations

import json
import logging
import math
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SurfaceType(Enum):
    PLANAR = "planar"
    CYLINDRICAL = "cylindrical"
    SPHERICAL = "spherical"
    CURVED = "curved"
    CUSTOM_MESH = "custom_mesh"


class BlendProfile(Enum):
    LINEAR = "linear"
    S_CURVE = "s_curve"
    SMOOTH_STEP = "smooth_step"
    GAUSSIAN = "gaussian"


class CalibrationMethod(Enum):
    CHECKERBOARD = "checkerboard"
    STRUCTURED_LIGHT = "structured_light"
    MANUAL = "manual"
    ARUCO_MARKER = "aruco_marker"
    DEPTH_SCAN = "depth_scan"


class MediaServerProtocol(Enum):
    DISGUISE = "disguise"
    GREEN_HIPPO = "green_hippo"
    RESOLUME = "resolume"
    MADMAPPER = "madmapper"
    OSC = "osc"
    NDI = "ndi"


class TrackingMethod(Enum):
    ARUCO_MARKER = "aruco_marker"
    DEPTH_CAMERA = "depth_camera"
    SKELETON = "skeleton"
    INFRARED = "infrared"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ControlPoint:
    row: int
    col: int
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    source_x: float = 0.0
    source_y: float = 0.0

    def distance_to(self, other: ControlPoint) -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )


@dataclass
class ProjectorConfig:
    name: str
    resolution: tuple[int, int] = (1920, 1200)
    brightness_lumens: int = 20000
    throw_ratio: float = 1.2
    lens_shift_vertical: float = 0.0
    lens_shift_horizontal: float = 0.0
    position: tuple[float, float, float] = (0.0, -8.0, 4.0)
    orientation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    gamma: float = 2.2
    color_temp_k: int = 6500


@dataclass
class CalibrationData:
    projector_name: str
    surface_name: str
    homography_matrix: list[list[float]] = field(default_factory=lambda: [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    mesh_data: Optional[list[list[ControlPoint]]] = None
    lens_correction: dict[str, float] = field(default_factory=dict)
    keystone: dict[str, float] = field(default_factory=dict)
    created_at: str = ""


@dataclass
class BlendRegion:
    projector_a: str
    projector_b: str
    orientation: str = "vertical"
    start_x: int = 0
    end_x: int = 200
    start_y: int = 0
    end_y: int = 0
    blend_curve_gamma: float = 2.2


@dataclass
class TrackingEvent:
    timestamp: float
    marker_id: int
    x: float
    y: float
    z: float
    confidence: float


# ---------------------------------------------------------------------------
# Projection Surface
# ---------------------------------------------------------------------------

class ProjectionSurface:
    """Defines a projection target surface with optional curvature."""

    def __init__(
        self,
        name: str = "Surface",
        surface_type: SurfaceType = SurfaceType.PLANAR,
        width_m: float = 10.0,
        height_m: float = 6.0,
        curvature_radius_m: Optional[float] = None,
        control_points_x: int = 8,
        control_points_y: int = 6,
    ):
        self.name = name
        self.surface_type = surface_type
        self.width_m = width_m
        self.height_m = height_m
        self.curvature_radius_m = curvature_radius_m
        self.control_points_x = control_points_x
        self.control_points_y = control_points_y
        self._mesh: list[list[ControlPoint]] = self._generate_mesh()

    def _generate_mesh(self) -> list[list[ControlPoint]]:
        mesh = []
        for row in range(self.control_points_y):
            row_points = []
            for col in range(self.control_points_x):
                u = col / max(1, self.control_points_x - 1)
                v = row / max(1, self.control_points_y - 1)

                x = u * self.width_m - self.width_m / 2
                y = v * self.height_m

                if self.surface_type == SurfaceType.CYLINDRICAL and self.curvature_radius_m:
                    angle = (u - 0.5) * (self.width_m / self.curvature_radius_m)
                    x = self.curvature_radius_m * math.sin(angle)
                    z = self.curvature_radius_m * (1 - math.cos(angle))
                elif self.surface_type == SurfaceType.CURVED and self.curvature_radius_m:
                    curve_factor = math.sin(math.pi * u) * 0.3
                    z = curve_factor * self.curvature_radius_m
                else:
                    z = 0.0

                point = ControlPoint(
                    row=row, col=col,
                    x=x, y=y, z=z,
                    source_x=u, source_y=v,
                )
                row_points.append(point)
            mesh.append(row_points)
        return mesh

    def get_mesh(self) -> list[list[ControlPoint]]:
        return self._mesh

    def get_dimensions(self) -> dict[str, float]:
        return {"width_m": self.width_m, "height_m": self.height_m}


# ---------------------------------------------------------------------------
# Projector
# ---------------------------------------------------------------------------

class Projector:
    """Projector configuration and intrinsic correction."""

    def __init__(self, name: str = "Projector", **kwargs: Any):
        self.config = ProjectorConfig(name=name, **kwargs)
        self._keystone_h = 0.0
        self._keystone_v = 0.0
        self._barrel_distortion = 0.0

    @property
    def name(self) -> str:
        return self.config.name

    def set_keystone(self, horizontal: float, vertical: float) -> None:
        self._keystone_h = max(-1.0, min(1.0, horizontal))
        self._keystone_v = max(-1.0, min(1.0, vertical))
        logger.info("Keystone correction: H=%.2f, V=%.2f", self._keystone_h, self._keystone_v)

    def set_barrel_distortion(self, amount: float) -> None:
        self._barrel_distortion = max(-1.0, min(1.0, amount))

    def get_correction_data(self) -> dict[str, Any]:
        return {
            "keystone_h": self._keystone_h,
            "keystone_v": self._keystone_v,
            "barrel_distortion": self._barrel_distortion,
            "gamma": self.config.gamma,
            "color_temp_k": self.config.color_temp_k,
        }

    def pixel_to_ray(self, px: int, py: int) -> tuple[float, float, float]:
        """Convert a pixel coordinate to a 3D ray direction."""
        nx = (px / self.config.resolution[0] - 0.5) * 2.0
        ny = (0.5 - py / self.config.resolution[1]) * 2.0
        fx = self.config.resolution[0] / (2 * math.tan(math.radians(30)))
        fy = self.config.resolution[1] / (2 * math.tan(math.radians(20)))
        return (nx / fx, ny / fy, 1.0)


# ---------------------------------------------------------------------------
# Calibration Pipeline
# ---------------------------------------------------------------------------

class CalibrationPipeline:
    """Full calibration pipeline for projection mapping."""

    def __init__(
        self,
        surface: ProjectionSurface,
        projectors: Optional[list[Projector]] = None,
    ):
        self.surface = surface
        self.projectors = projectors or []
        self._calibrations: list[CalibrationData] = []

    def calibrate(
        self,
        method: CalibrationMethod = CalibrationMethod.CHECKERBOARD,
        control_point_spacing_m: float = 0.5,
        enable_lens_correction: bool = True,
    ) -> list[CalibrationData]:
        logger.info(
            "Calibrating %d projectors on surface '%s' using %s method",
            len(self.projectors), self.surface.name, method.value,
        )
        self._calibrations = []
        for proj in self.projectors:
            cal = CalibrationData(
                projector_name=proj.name,
                surface_name=self.surface.name,
                mesh_data=self.surface.get_mesh(),
                lens_correction={"enabled": enable_lens_correction},
                created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
            self._calibrations.append(cal)
            logger.info("Calibrated projector '%s'", proj.name)
        return self._calibrations

    def save_calibration(self, filepath: str) -> None:
        data = {
            "surface": self.surface.name,
            "projectors": [
                {
                    "name": cal.projector_name,
                    "homography": cal.homography_matrix,
                    "lens_correction": cal.lens_correction,
                    "keystone": cal.keystone,
                    "created_at": cal.created_at,
                }
                for cal in self._calibrations
            ],
        }
        Path(filepath).write_text(json.dumps(data, indent=2))
        logger.info("Calibration saved to %s", filepath)

    def load_calibration(self, filepath: str) -> list[CalibrationData]:
        with open(filepath) as f:
            data = json.load(f)
        self._calibrations = [
            CalibrationData(
                projector_name=p["name"],
                surface_name=data["surface"],
                homography_matrix=p["homography"],
                lens_correction=p.get("lens_correction", {}),
                keystone=p.get("keystone", {}),
                created_at=p.get("created_at", ""),
            )
            for p in data.get("projectors", [])
        ]
        logger.info("Loaded %d projector calibrations from %s", len(self._calibrations), filepath)
        return self._calibrations

    def get_homography(self, projector_name: str) -> list[list[float]]:
        cal = next((c for c in self._calibrations if c.projector_name == projector_name), None)
        return cal.homography_matrix if cal else [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


# ---------------------------------------------------------------------------
# Edge Blender
# ---------------------------------------------------------------------------

class EdgeBlender:
    """Edge blending for multi-projector overlap zones."""

    def __init__(
        self,
        blend_width_px: int = 200,
        gamma_curve: float = 2.2,
        blend_profile: BlendProfile = BlendProfile.LINEAR,
    ):
        self.blend_width_px = blend_width_px
        self.gamma_curve = gamma_curve
        self.blend_profile = blend_profile
        self._regions: list[BlendRegion] = []

    def add_region(self, region: BlendRegion) -> None:
        self._regions.append(region)
        logger.info(
            "Added blend region: %s <-> %s (%s, %d px)",
            region.projector_a, region.projector_b,
            region.orientation, self.blend_width_px,
        )

    def compute_blend_value(self, position_px: int, region: BlendRegion) -> float:
        """Compute blend factor (0.0 to 1.0) for a pixel in the blend zone."""
        blend_start = region.start_x
        blend_end = region.end_x
        t = (position_px - blend_start) / max(1, blend_end - blend_start)
        t = max(0.0, min(1.0, t))

        if self.blend_profile == BlendProfile.LINEAR:
            value = t
        elif self.blend_profile == BlendProfile.S_CURVE:
            value = t * t * (3 - 2 * t)
        elif self.blend_profile == BlendProfile.SMOOTH_STEP:
            value = t * t * t * (t * (6 * t - 15) + 10)
        elif self.blend_profile == BlendProfile.GAUSSIAN:
            value = 0.5 * (1 + math.erfc(-(t - 0.5) * 4))
        else:
            value = t

        # Gamma correction for additive blending
        value = value ** (1.0 / self.gamma_curve)
        return max(0.0, min(1.0, value))

    def get_all_regions(self) -> list[BlendRegion]:
        return list(self._regions)


# ---------------------------------------------------------------------------
# Color Matcher
# ---------------------------------------------------------------------------

class ColorMatcher:
    """Color calibration and matching across multiple projectors."""

    def __init__(self, reference_projector: str = "Main Projector"):
        self.reference_projector = reference_projector
        self._profiles: dict[str, dict[str, float]] = {}

    def measure_and_correct(
        self,
        projectors: list[str],
        color_space: str = "rec709",
    ) -> dict[str, dict[str, float]]:
        corrections = {}
        for proj in projectors:
            if proj == self.reference_projector:
                corrections[proj] = {"r_gain": 1.0, "g_gain": 1.0, "b_gain": 1.0, "gamma": 2.2}
                continue
            correction = {
                "r_gain": 0.98 + (hash(proj) % 5) / 100,
                "g_gain": 1.0 + (hash(proj) % 3) / 100,
                "b_gain": 0.99 + (hash(proj) % 4) / 100,
                "gamma": 2.2,
            }
            corrections[proj] = correction
            self._profiles[proj] = correction
            logger.info("Color correction for '%s': %s", proj, correction)
        return corrections

    def get_correction(self, projector: str) -> dict[str, float]:
        return self._profiles.get(projector, {"r_gain": 1.0, "g_gain": 1.0, "b_gain": 1.0, "gamma": 2.2})


# ---------------------------------------------------------------------------
# Mesh Deformation
# ---------------------------------------------------------------------------

class MeshDeformation:
    """Warping mesh for projection mapping with control point editing."""

    def __init__(self, rows: int = 8, cols: int = 8):
        self.rows = rows
        self.cols = cols
        self._control_points: list[list[ControlPoint]] = []
        self._animations: list[dict[str, Any]] = []
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(ControlPoint(row=r, col=c, x=c / max(1, cols - 1), y=r / max(1, rows - 1)))
            self._control_points.append(row)

    @classmethod
    def from_file(cls, filepath: str) -> MeshDeformation:
        with open(filepath) as f:
            data = json.load(f)
        mesh = cls(rows=data.get("rows", 8), cols=data.get("cols", 8))
        for r, row_data in enumerate(data.get("control_points", [])):
            for c, cp_data in enumerate(row_data):
                if r < mesh.rows and c < mesh.cols:
                    mesh._control_points[r][c].x = cp_data.get("x", 0)
                    mesh._control_points[r][c].y = cp_data.get("y", 0)
                    mesh._control_points[r][c].z = cp_data.get("z", 0)
        logger.info("Loaded mesh from %s: %dx%d control points", filepath, mesh.rows, mesh.cols)
        return mesh

    def move_control_point(self, row: int, col: int, x: float, y: float, z: float = 0.0) -> None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self._control_points[row][col].x = x
            self._control_points[row][col].y = y
            self._control_points[row][col].z = z

    def smooth_region(self, center_row: int, center_col: int, radius: int, strength: float) -> None:
        for r in range(max(0, center_row - radius), min(self.rows, center_row + radius + 1)):
            for c in range(max(0, center_col - radius), min(self.cols, center_col + radius + 1)):
                dist = math.sqrt((r - center_row) ** 2 + (c - center_col) ** 2)
                if dist <= radius:
                    factor = (1.0 - dist / radius) * strength
                    avg_x = sum(
                        self._control_points[rr][cc].x
                        for rr in range(max(0, r - 1), min(self.rows, r + 2))
                        for cc in range(max(0, c - 1), min(self.cols, c + 2))
                    ) / 9.0
                    self._control_points[r][c].x = (
                        self._control_points[r][c].x * (1 - factor) + avg_x * factor
                    )

    def interpolate_surface(self, u: float, v: float) -> tuple[float, float, float]:
        """Bilinear interpolation of the mesh at parametric coordinates (u, v)."""
        fu = u * (self.cols - 1)
        fv = v * (self.rows - 1)
        c0 = int(fu)
        r0 = int(fv)
        c1 = min(c0 + 1, self.cols - 1)
        r1 = min(r0 + 1, self.rows - 1)
        du = fu - c0
        dv = fv - r0

        x = (
            self._control_points[r0][c0].x * (1 - du) * (1 - dv) +
            self._control_points[r0][c1].x * du * (1 - dv) +
            self._control_points[r1][c0].x * (1 - du) * dv +
            self._control_points[r1][c1].x * du * dv
        )
        y = (
            self._control_points[r0][c0].y * (1 - du) * (1 - dv) +
            self._control_points[r0][c1].y * du * (1 - dv) +
            self._control_points[r1][c0].y * (1 - du) * dv +
            self._control_points[r1][c1].y * du * dv
        )
        z = (
            self._control_points[r0][c0].z * (1 - du) * (1 - dv) +
            self._control_points[r0][c1].z * du * (1 - dv) +
            self._control_points[r1][c0].z * (1 - du) * dv +
            self._control_points[r1][c1].z * du * dv
        )
        return (x, y, z)

    def animate_control_point(
        self, row: int, col: int, target_x: float, target_y: float,
        duration_s: float, easing: str = "linear",
    ) -> None:
        self._animations.append({
            "row": row, "col": col,
            "target_x": target_x, "target_y": target_y,
            "duration_s": duration_s, "easing": easing,
        })
        logger.info("Animate CP[%d,%d] to (%.3f, %.3f) over %.1fs", row, col, target_x, target_y, duration_s)

    def get_warp_data(self) -> dict[str, Any]:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "control_points": [
                [{"x": cp.x, "y": cp.y, "z": cp.z} for cp in row]
                for row in self._control_points
            ],
        }

    def export_mesh(self, filepath: str) -> None:
        Path(filepath).write_text(json.dumps(self.get_warp_data(), indent=2))
        logger.info("Mesh exported to %s", filepath)


# ---------------------------------------------------------------------------
# Media Server Bridge
# ---------------------------------------------------------------------------

class MediaServerBridge:
    """Bridge to external media servers."""

    def __init__(self, protocol: MediaServerProtocol = MediaServerProtocol.DISGUISE, ip: str = "192.168.1.70"):
        self.protocol = protocol
        self.ip = ip
        self._connected = False
        self._layers: dict[int, dict[str, Any]] = {}

    def connect(self) -> bool:
        logger.info("Connecting to %s media server at %s", self.protocol.value, self.ip)
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False

    def push_calibration(self, warp_data: dict[str, Any]) -> bool:
        self._ensure_connected()
        logger.info("Pushing warp data to %s (%d control points)", self.protocol.value,
                     sum(len(row) for row in warp_data.get("control_points", [])))
        return True

    def set_content_layer(self, layer: int, media: str) -> None:
        self._ensure_connected()
        self._layers[layer] = {"media": media, "playing": False}
        logger.info("Layer %d assigned: %s", layer, media)

    def play(self, layer: Optional[int] = None) -> None:
        self._ensure_connected()
        if layer is not None:
            self._layers[layer]["playing"] = True
        else:
            for l in self._layers:
                self._layers[l]["playing"] = True
        logger.info("Playing on %s", self.protocol.value)

    def stop(self, layer: Optional[int] = None) -> None:
        if layer is not None:
            self._layers[layer]["playing"] = False
        else:
            for l in self._layers:
                self._layers[l]["playing"] = False

    def _ensure_connected(self) -> None:
        if not self._connected:
            raise RuntimeError("Not connected to media server")


# ---------------------------------------------------------------------------
# Interactive Tracker
# ---------------------------------------------------------------------------

class InteractiveTracker:
    """Tracks markers or performers for interactive projection."""

    def __init__(
        self,
        tracking_method: TrackingMethod = TrackingMethod.ARUCO_MARKER,
        camera_resolution: tuple[int, int] = (1920, 1080),
    ):
        self.tracking_method = tracking_method
        self.camera_resolution = camera_resolution
        self._events: list[TrackingEvent] = []
        self._active_markers: dict[int, TrackingEvent] = {}

    def process_frame(self, detections: list[dict[str, Any]]) -> list[TrackingEvent]:
        events = []
        for det in detections:
            event = TrackingEvent(
                timestamp=time.time(),
                marker_id=det.get("id", 0),
                x=det.get("x", 0.0),
                y=det.get("y", 0.0),
                z=det.get("z", 0.0),
                confidence=det.get("confidence", 0.0),
            )
            events.append(event)
            self._active_markers[event.marker_id] = event
        self._events.extend(events)
        return events

    def get_active_positions(self) -> dict[int, tuple[float, float, float]]:
        return {mid: (e.x, e.y, e.z) for mid, e in self._active_markers.items()}

    def map_to_projection(self, x: float, y: float, surface: ProjectionSurface) -> tuple[float, float]:
        """Map camera-space coordinates to surface UV coordinates."""
        u = x / self.camera_resolution[0]
        v = y / self.camera_resolution[1]
        return (u, v)


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("=" * 60)
    print("  Projection Mapping System — Demo")
    print("=" * 60)

    # --- Surface ---
    wall = ProjectionSurface(
        name="Main Backdrop",
        surface_type=SurfaceType.CURVED,
        width_m=12.0, height_m=6.0,
        curvature_radius_m=8.0,
        control_points_x=16, control_points_y=8,
    )
    print(f"Surface '{wall.name}': {wall.get_dimensions()}, mesh {wall.control_points_x}x{wall.control_points_y}")

    # --- Projector ---
    proj1 = Projector(name="Main Projector", resolution=(1920, 1200), throw_ratio=1.2)
    proj1.set_keystone(0.02, -0.01)
    ray = proj1.pixel_to_ray(960, 600)
    print(f"Projector '{proj1.name}' ray at center: ({ray[0]:.4f}, {ray[1]:.4f}, {ray[2]:.4f})")

    proj2 = Projector(name="Side Projector", resolution=(1920, 1200), throw_ratio=1.4)

    # --- Calibration ---
    pipeline = CalibrationPipeline(surface=wall, projectors=[proj1, proj2])
    cals = pipeline.calibrate(method=CalibrationMethod.STRUCTURED_LIGHT, control_point_spacing_m=0.5)
    pipeline.save_calibration("/tmp/projection_cal.json")

    # --- Edge Blending ---
    blender = EdgeBlender(blend_width_px=200, blend_profile=BlendProfile.S_CURVE)
    region = BlendRegion(projector_a="Main Projector", projector_b="Side Projector", start_x=860, end_x=1060)
    blender.add_region(region)
    blend_val = blender.compute_blend_value(960, region)
    print(f"Blend factor at overlap center: {blend_val:.3f}")

    # --- Color Matching ---
    matcher = ColorMatcher(reference_projector="Main Projector")
    corrections = matcher.measure_and_correct(["Main Projector", "Side Projector"])
    print(f"Color corrections: {corrections}")

    # --- Mesh Deformation ---
    mesh = MeshDeformation(rows=8, cols=8)
    mesh.move_control_point(row=3, col=5, x=0.65, y=0.4, z=0.1)
    mesh.smooth_region(center_row=4, center_col=4, radius=2, strength=0.5)
    uv_point = mesh.interpolate_surface(0.5, 0.5)
    print(f"Mesh interpolated at (0.5, 0.5): ({uv_point[0]:.3f}, {uv_point[1]:.3f}, {uv_point[2]:.3f})")
    mesh.animate_control_point(row=6, col=4, target_x=0.7, target_y=0.8, duration_s=2.0, easing="ease_in_out")
    mesh.export_mesh("/tmp/mesh_warp.json")

    # --- Media Server ---
    msv = MediaServerBridge(protocol=MediaServerProtocol.DISGUISE, ip="192.168.1.70")
    msv.connect()
    msv.push_calibration(mesh.get_warp_data())
    msv.set_content_layer(layer=1, media="backdrop_video.mov")
    msv.play(layer=1)

    # --- Interactive Tracker ---
    tracker = InteractiveTracker(tracking_method=TrackingMethod.ARUCO_MARKER)
    events = tracker.process_frame([
        {"id": 1, "x": 480, "y": 300, "z": 0, "confidence": 0.95},
        {"id": 2, "x": 1200, "y": 700, "z": 0.5, "confidence": 0.88},
    ])
    positions = tracker.get_active_positions()
    print(f"Active markers: {positions}")
    uv = tracker.map_to_projection(480, 300, wall)
    print(f"Mapped to surface UV: ({uv[0]:.3f}, {uv[1]:.3f})")

    msv.disconnect()
    print("\nDemo complete.")


if __name__ == "__main__":
    main()
