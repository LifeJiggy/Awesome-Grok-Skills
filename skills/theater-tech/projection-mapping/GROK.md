---
name: "projection-mapping"
category: "theater-tech"
version: "1.0.0"
tags: ["theater-tech", "projection-mapping", "media-server", "3d-calibration", "blending"]
---

# Projection Mapping System

## Overview

The projection mapping module provides a comprehensive Python API for 3D surface calibration, multi-projector alignment, edge blending, real-time content warping, and media server integration for theatrical and live entertainment environments. It abstracts the complexity of mapping flat or curved video content onto irregular 3D surfaces Ã¢â‚¬â€ architectural facades, scenic elements, performer costumes, stage floors, and custom-built set pieces Ã¢â‚¬â€ into a programmable pipeline that can be calibrated, tested, and automated from a single interface.

At its core, projection mapping solves the geometric problem of transforming a rectangular video source to fit an arbitrary 3D surface as seen from a specific projector position. The module implements homography-based warping for planar surfaces, mesh-based deformation for curved and organic shapes, and lenticular blending for multi-projector overlap zones. Each projector's output passes through a calibration pipeline: intrinsic lens correction (keystone, barrel distortion), extrinsic pose estimation (position and orientation relative to the surface), mesh warping (control-point-based deformation), and color matching (gamut and brightness alignment across projectors).

Multi-projector setups require seamless edge blending: where two projectors overlap, their outputs must cross-fade smoothly to create the illusion of a single continuous image. The module handles both horizontal and vertical blend regions, with configurable gamma curves to compensate for the additive brightness in overlap zones. For curved surfaces, the blend width varies across the overlap Ã¢â‚¬â€ wider at the center where projectors are more perpendicular, narrower at the edges where viewing angles are oblique.

Interactive projection mapping extends the pipeline with real-time tracking: the system can follow performer positions via computer vision (ArUco markers, depth cameras, or skeleton tracking) and adjust projected content to follow them across the stage. The module supports integration with depth sensors (Intel RealSense, Microsoft Azure Kinect) for 3D surface scanning, and it can generate mesh data from point clouds for automatic calibration of complex surfaces.

## Core Capabilities

- 3D surface calibration using homography (planar) and mesh-based (curved) warping techniques
- Multi-projector alignment with automatic keystone correction and pose estimation
- Edge blending with configurable gamma curves, blend widths, and overlap compensation
- Real-time content warping with GPU-accelerated mesh deformation
- Color calibration and matching across projectors (white balance, gamma, gamut)
- Interactive projection tracking via ArUco markers, depth sensors, and skeleton tracking
- Media server integration with disguise, Green Hippo, Resolume, and MadMapper
- Mesh deformation with control-point editing, Bezier interpolation, and animation

## Architecture

```
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š              Content & Media Server Layer                Ã¢â€â€š
Ã¢â€â€š     (NDI, SDI, Media Playback, Generative Content)      Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¤
Ã¢â€â€š              Warping & Blending Engine                   Ã¢â€â€š
Ã¢â€â€š   (Mesh Deformation, Edge Blending, Color Matching)     Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¤
Ã¢â€â€š              Calibration Pipeline                        Ã¢â€â€š
Ã¢â€â€š  (Homography, Keystone, Lens Correction, Pose Est.)     Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¤
Ã¢â€â€š              Surface & Projector Model                   Ã¢â€â€š
Ã¢â€â€š    (3D Mesh, Curvature, Projector Optics, Position)     Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¤
Ã¢â€â€š              Interactive Tracking Layer                  Ã¢â€â€š
Ã¢â€â€š     (ArUco, Depth Sensors, Skeleton, IR Markers)        Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

## Usage Examples

### Surface Definition and Projector Configuration

```python
from projection_mapping import ProjectionSurface, SurfaceType, Projector

# Define a curved scenic wall
wall = ProjectionSurface(
    name="Main Backdrop",
    surface_type=SurfaceType.CURVED,
    width_m=12.0,
    height_m=6.0,
    curvature_radius_m=8.0,
    control_points_x=16,
    control_points_y=8,
)
print(f"Surface '{wall.name}': {wall.get_dimensions()}")

# Configure a projector with lens correction
projector = Projector(
    name="Main Projector",
    resolution=(1920, 1200),
    brightness_lumens=20000,
    throw_ratio=1.2,
    position=(0, -8, 4),
)
projector.set_keystone(0.02, -0.01)
projector.set_barrel_distortion(0.05)

# Pixel-to-ray conversion for alignment
ray = projector.pixel_to_ray(960, 600)
print(f"Center ray direction: ({ray[0]:.4f}, {ray[1]:.4f}, {ray[2]:.4f})")
```

### Calibration Pipeline

```python
from projection_mapping import CalibrationPipeline, CalibrationMethod

# Full calibration for two projectors on a curved surface
pipeline = CalibrationPipeline(surface=wall, projectors=[projector1, projector2])
calibrations = pipeline.calibrate(
    method=CalibrationMethod.STRUCTURED_LIGHT,
    control_point_spacing_m=0.5,
    enable_lens_correction=True,
)
pipeline.save_calibration("backdrop_cal.json")

# Load calibration from file
pipeline.load_calibration("backdrop_cal.json")
homography = pipeline.get_homography("Main Projector")
```

### Edge Blending

```python
from projection_mapping import EdgeBlender, BlendRegion, BlendProfile

blender = EdgeBlender(
    blend_width_px=200,
    gamma_curve=2.2,
    blend_profile=BlendProfile.S_CURVE,
)

# Define overlap region between two projectors
region = BlendRegion(
    projector_a="Left Projector",
    projector_b="Right Projector",
    orientation="vertical",
    start_x=860,
    end_x=1060,
    blend_curve_gamma=2.2,
)
blender.add_region(region)

# Compute blend factor at any pixel position
factor = blender.compute_blend_value(960, region)
print(f"Blend factor at overlap center: {factor:.3f}")
```

### Mesh Deformation

```python
from projection_mapping import MeshDeformation

# Create and edit a warping mesh
mesh = MeshDeformation(rows=8, cols=8)
mesh.move_control_point(row=3, col=5, x=0.65, y=0.4, z=0.1)
mesh.smooth_region(center_row=4, center_col=4, radius=2, strength=0.5)

# Interpolate surface position at UV coordinates
uv_point = mesh.interpolate_surface(0.5, 0.5)
print(f"Surface at (0.5, 0.5): ({uv_point[0]:.3f}, {uv_point[1]:.3f}, {uv_point[2]:.3f})")

# Animate a control point
mesh.animate_control_point(
    row=6, col=4,
    target_x=0.7, target_y=0.8,
    duration_s=2.0, easing="ease_in_out",
)

# Export for media server
mesh.export_mesh("warp_data.json")
```

### Media Server Integration

```python
from projection_mapping import MediaServerBridge, MediaServerProtocol

bridge = MediaServerBridge(protocol=MediaServerProtocol.DISGUISE, ip="192.168.1.70")
bridge.connect()
bridge.push_calibration(mesh.get_warp_data())
bridge.set_content_layer(layer=1, media="backdrop_video.mov")
bridge.play(layer=1)
```

### Interactive Tracking

```python
from projection_mapping import InteractiveTracker, TrackingMethod

tracker = InteractiveTracker(tracking_method=TrackingMethod.ARUCO_MARKER)
events = tracker.process_frame([
    {"id": 1, "x": 480, "y": 300, "z": 0, "confidence": 0.95},
    {"id": 2, "x": 1200, "y": 700, "z": 0.5, "confidence": 0.88},
])
positions = tracker.get_active_positions()
print(f"Active markers: {positions}")

# Map camera coordinates to projection surface UV
uv = tracker.map_to_projection(480, 300, wall)
```

## Best Practices

1. **Always calibrate projection surfaces in the dark with all house lights off.** Ambient light contaminates structured-light scanning and causes inaccurate mesh generation. Even 5 lux of ambient can introduce 2mm of error in a 10m projection.

2. **Use at least 4x4 control points per meter for mesh warping on curved surfaces.** Sparse control points create visible faceting and jagged edges at oblique viewing angles. For a 12m wall, use at least 48x24 control points.

3. **Match projector color temperature before alignment, not after.** Post-alignment color correction introduces artifacts at blend boundaries where both projectors contribute. Use a colorimeter to match white points to within 100K.

4. **Set blend width to at least 10% of the projector resolution for seamless edges.** Narrow blends amplify brightness banding and make gamma mismatches visible. For 1920px wide output, use at least 200px blend width.

5. **Calibrate at show resolution and frame rate, not preview.** Some media servers apply different scaling in preview mode, making calibration inaccurate at full output. Always verify calibration with the final output pipeline.

6. **Use a colorimeter for projector white-point matching, not the naked eye.** Human vision adapts to color shifts; a meter doesn't. Match R, G, B primaries and white point separately for best results.

7. **Export calibration files before every performance and keep a backup on USB.** Media server crashes can corrupt live calibration data; recovery from backup is faster than recalibration.

8. **Test projection mapping with performers on stage before the show.** Performer shadows and body reflections can create hotspots and occlusion zones that aren't visible in empty-stage calibration.

9. **Use structured-light scanning for surfaces larger than 4m.** Manual calibration becomes imprecise at scale; structured-light gives sub-millimeter accuracy across the entire surface.

10. **Document projector throw distances and angles in your plot file.** When touring, you need to know exactly where each projector was positioned for rapid re-setup. Include photos of the projection coverage from the audience perspective.

## Configuration

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Blend Width | 200px | 50Ã¢â‚¬â€œ500px | Edge blend region width in pixels |
| Blend Gamma | 2.2 | 1.0Ã¢â‚¬â€œ3.0 | Gamma curve for blend compensation |
| Control Points | 8x8 | 2x2Ã¢â‚¬â€œ32x32 | Mesh resolution for warping |
| Mesh Smoothing | 0.5 | 0.0Ã¢â‚¬â€œ1.0 | Smoothing strength for control points |
| Color Temp Match | Ã‚Â±100K | Ã‚Â±50Ã¢â‚¬â€œ500K | White-point matching tolerance |

## Related Modules

- [lighting-control](../lighting-control/GROK.md) Ã¢â‚¬â€ Lighting color matching for projection ambient compensation
- [stage-automation](../stage-automation/GROK.md) Ã¢â‚¬â€ Automated scenic movement tracking for dynamic projection surfaces
- [sound-engineering](../sound-engineering/GROK.md) Ã¢â‚¬â€ Spatial audio alignment with projection-mapped environments
- [audience-engagement](../audience-engagement/GROK.md) Ã¢â‚¬â€ Interactive audience-triggered projection content

---

## Advanced Configuration

### Projector Lens Profile Calibration

```python
from projection_mapping import LensProfile, DistortionModel

lens = LensProfile(
    manufacturer="Panasonic",
    model="PT-RQ50K",
    throw_ratio=1.2,
    shift_range_mm=(-50, 50),
    distortion_model=DistortionModel.BROWN_CONRADY,
    distortion_coefficients=[0.05, -0.02, 0.01, 0.0, 0.0],
)
```

### Structured Light Scanner Configuration

```python
from projection_mapping import StructuredLightScanner

scanner = StructuredLightScanner(
    pattern_type="gray_code",
    resolution_px=(1920, 1200),
    exposure_ms=16,
    num_patterns=24,
    noise_threshold=0.02,
)
calibration = scanner.scan_surface(surface=wall)
scanner.export_mesh(calibration, "surface_mesh.obj")
```

## Architecture Patterns

### Multi-Projector Pipeline

```
Content Source (NDI/SDI)
        Ã¢â€â€š
        Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Color Match  Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Per-projector calibration
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
       Ã¢â€â€š
       Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Warp Engine  Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Mesh deformation per projector
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
       Ã¢â€â€š
       Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Blend Zone   Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Edge blending in overlap regions
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
       Ã¢â€â€š
       Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Output       Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Per-projector output
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

### Calibration Workflow

1. Surface definition (manual or 3D scan)
2. Projector placement and alignment
3. Structured light capture
4. Homography/mesh computation
5. Edge blend region identification
6. Color calibration across projectors
7. Verification projection and fine-tuning

## Integration Guide

### Media Server Bridge Protocol

```python
from projection_mapping import MediaServerBridge, Protocol

# disguise integration
disguise = MediaServerBridge(protocol=Protocol.DISGUISE, ip="192.168.1.70")
disguise.connect()
disguise.push_warp_data(mesh.export_warp_data())
disguise.set_layer_transport(1, "transport_mode", "auto")
```

### Interactive Tracking Integration

```python
from projection_mapping import InteractiveTracker, TrackingSource

tracker = InteractiveTracker()
tracker.add_source(TrackingSource.AZURE_KINECT, device_id="k4a_001")
tracker.add_source(TrackingSource.ARUCO_MARKER, camera_id="cam_001")
tracker.start()
```

## Performance Optimization

| Optimization | Impact |
|-------------|--------|
| GPU-accelerated warping | 60fps @ 4K per projector |
| Precomputed blend LUTs | Zero-latency blend transitions |
| Mesh LOD for curves | 50% fewer control points at distance |
| Content pre-buffering | No playback stutter during cues |
| Parallel projector calibration | 3x faster calibration |

## Security Considerations

- **Projector network isolation**: Dedicated VLAN for media servers and projectors
- **Content protection**: DRM on licensed projection content
- **Physical security**: Locked projector mounts with tamper detection
- **Remote access**: VPN-only access to media server management interfaces

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Blend band visible | Gamma mismatch | Recalibrate blend gamma curves |
| Warping distortion at edges | Insufficient control points | Increase mesh resolution |
| Color shift across projectors | Different lamp hours | Match white points with colorimeter |
| Content stutter | Network bandwidth | Use 10GbE for NDI, check switch capacity |
| Calibration drift | Projector movement | Re-calibrate, check mounting stability |
| Structured light noise | Ambient light | Ensure complete darkness during scan |

## API Reference

### ProjectionSurface

```python
class ProjectionSurface:
    def __init__(self, name: str, surface_type: SurfaceType, width_m: float, height_m: float, **kwargs)
    def get_dimensions(self) -> tuple
    def set_control_points(self, rows: int, cols: int) -> None
    def export_mesh(self, path: str) -> None
```

### Projector

```python
class Projector:
    def __init__(self, name: str, resolution: tuple, brightness_lumens: int, throw_ratio: float, position: tuple)
    def set_keystone(self, h: float, v: float) -> None
    def set_barrel_distortion(self, k1: float) -> None
    def pixel_to_ray(self, x: int, y: int) -> tuple
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class SurfaceType(Enum):
    PLANAR = "planar"
    CURVED = "curved"
    CYLINDRICAL = "cylindrical"
    SPHERICAL = "spherical"
    CUSTOM_MESH = "custom_mesh"

@dataclass
class CalibrationPoint:
    screen_x: float
    screen_y: float
    surface_x: float
    surface_y: float
    surface_z: float

@dataclass
class BlendRegion:
    projector_a: str
    projector_b: str
    orientation: str
    start_px: int
    end_px: int
    gamma: float
```

## Deployment Guide

### Installation

```bash
pip install projection-mapping
```

### Projector Setup

1. Mount projectors according to plot
2. Connect to media server network
3. Run structured light calibration in dark
4. Adjust mesh control points for surface fit
5. Configure edge blend regions
6. Match projector color temperatures
7. Verify full-surface coverage

## Monitoring & Observability

```python
from projection_mapping import MetricsCollector

collector = MetricsCollector()
collector.gauge("projection.fps", fps, tags={"projector": name})
collector.gauge("projection.gpu_utilization", pct)
collector.counter("projection.calibration.count", count)
collector.histogram("projection.warp_latency_ms", latency)
```

## Testing Strategy

```python
import pytest
from projection_mapping import ProjectionSurface, SurfaceType

def test_surface_dimensions():
    wall = ProjectionSurface(name="Test", surface_type=SurfaceType.CURVED, width_m=12.0, height_m=6.0)
    dims = wall.get_dimensions()
    assert dims == (12.0, 6.0)

def test_mesh_export():
    mesh = MeshDeformation(rows=8, cols=8)
    mesh.export_mesh("test_warp.json")
    import json
    with open("test_warp.json") as f:
        data = json.load(f)
    assert "control_points" in data
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Azure Kinect support | Add Kinect SDK dependency |
| 2.0.0 | New mesh format | Convert calibration files with migration tool |

## Glossary

| Term | Definition |
|------|-----------|
| **Homography** | 2D-to-2D projective transform for planar surfaces |
| **Edge Blending** | Smooth transition between overlapping projector outputs |
| **Structured Light** | 3D scanning using projected patterns |
| **ArUco Marker** | Fiducial marker for camera tracking |
| **NDI** | Network Device Interface for video over IP |
| **Warping** | Deforming projected image to match surface geometry |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with homography and mesh warping
- Multi-projector alignment and edge blending
- Media server integration (disguise, Resolume)
- Interactive tracking support

## Contributing Guidelines

```bash
git clone https://github.com/example/projection-mapping.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Projector Specification Reference

| Parameter | Standard Throw | Short Throw | Ultra-Short Throw |
|-----------|---------------|-------------|-------------------|
| Throw Ratio | 1.5-2.5:1 | 0.8-1.5:1 | 0.2-0.8:1 |
| Lens Shift | Ã‚Â±50% V | Ã‚Â±70% V | Fixed |
| Resolution | 1920x1200 | 1920x1200 | 4K (3840x2400) |
| Brightness | 10,000-20,000 lm | 5,000-15,000 lm | 3,000-10,000 lm |
| Best For | Large venue, high ceiling | Mid-size venue | Tight spaces, floor projection |

### Calibration Point Density Guide

| Surface Size | Min Control Points | Recommended | High Quality |
|-------------|-------------------|-------------|--------------|
| < 2m | 4x4 | 8x8 | 16x16 |
| 2-5m | 8x8 | 16x16 | 32x32 |
| 5-10m | 16x16 | 32x32 | 48x48 |
| 10-20m | 32x32 | 48x48 | 64x64 |
| > 20m | 48x48 | 64x64 | 96x96 |

### Edge Blending Reference

| Blend Width (px) | Projector Resolution | Coverage |
|------------------|---------------------|----------|
| 100 | 1920x1200 | 5% overlap |
| 200 | 1920x1200 | 10% overlap |
| 300 | 1920x1200 | 15% overlap |
| 400 | 1920x1200 | 20% overlap |
| 200 | 3840x2400 | 5% overlap |
| 400 | 3840x2400 | 10% overlap |

### Surface Material Reference

| Material | Reflectance | Gain | Best For |
|----------|------------|------|----------|
| Matte white | 90% | 1.0 | General purpose |
| High gain | 95% | 1.5-2.0 | Bright ambient |
| Silver | 85% | 1.2-1.5 | 3D, high contrast |
| Grey | 70% | 0.8 | Improved blacks |
| Beaded | 80% | 1.3 | Wide viewing angle |
| Perforated | 75% | 0.9 | Sound transparency |

### Color Calibration Workflow

1. Warm up projectors for 30 minutes
2. Set all projectors to same white point (D65)
3. Project color patches (RGBWCMY)
4. Measure with colorimeter at multiple points
5. Generate per-projector correction LUT
6. Apply LUT to all projectors
7. Verify match at blend boundaries
8. Document calibration settings

### Media Server Comparison

| Server | Protocol | Max Layers | Warping | Blending |
|--------|----------|-----------|---------|----------|
| disguise | Custom API | 8+ | Mesh | Multi-zone |
| Resolume | ND SMPTE | 6 | Grid | Per-output |
| MadMapper | Custom | 4 | Quad | Multi-zone |
| Green Hippo | Custom | 8+ | Mesh | Advanced |
| TouchDesigner | SOP | Unlimited | SOP-based | Custom |

### Troubleshooting Decision Tree

```
Projection alignment off
    Ã¢â€â€š
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Verify projector position Ã¢â€ â€™ Check mounting stability
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check lens shift Ã¢â€ â€™ Adjust mechanical lens shift
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Recalibrate Ã¢â€ â€™ Run structured light scan
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check surface flatness Ã¢â€ â€™ Verify no warping
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Check keystone Ã¢â€ â€™ Adjust digital keystone correction

Blend band visible
    Ã¢â€â€š
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check gamma matching Ã¢â€ â€™ Recalibrate blend curves
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check projector brightness Ã¢â€ â€™ Match output levels
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check blend width Ã¢â€ â€™ Increase if too narrow
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check surface uniformity Ã¢â€ â€™ Ensure consistent reflectance
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Check ambient light Ã¢â€ â€™ Eliminate competing light sources

Content stutter on media server
    Ã¢â€â€š
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check video codec Ã¢â€ â€™ Use ProRes or DNxHR
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check storage speed Ã¢â€ â€™ Use SSD or RAID
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check network bandwidth Ã¢â€ â€™ Use 10GbE for NDI
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check GPU utilization Ã¢â€ â€™ Reduce layer count
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Check content resolution Ã¢â€ â€™ Match projector output
```

### Performance Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Calibration accuracy | < 2mm error | 2-5mm | > 5mm |
| Blend smoothness | ÃŽâ€E < 1 | ÃŽâ€E 1-3 | ÃŽâ€E > 3 |
| Frame rate | 60 fps | 30-60 fps | < 30 fps |
| Input latency | < 1 frame | 1-2 frames | > 2 frames |
| Color match (projectors) | ÃŽâ€E < 2 | ÃŽâ€E 2-5 | ÃŽâ€E > 5 |
| Content load time | < 5s | 5-15s | > 15s |
| Interactive tracking latency | < 50ms | 50-100ms | > 100ms |

### Projection Throw Distance Calculator

```
Throw Distance = Throw Ratio Ãƒâ€” Image Width

Example:
  Projector: Throw Ratio 1.5:1
  Image Width: 6m
  Throw Distance: 1.5 Ãƒâ€” 6 = 9m

For angled projection:
  Horizontal Offset = tan(angle) Ãƒâ€” Throw Distance
  Vertical Offset = tan(angle) Ãƒâ€” Throw Distance
```

### Common Projection Scenarios

| Scenario | Projectors | Surface | Resolution | Complexity |
|----------|-----------|---------|-----------|------------|
| Single flat wall | 1 | Flat | 1920x1200 | Low |
| Multi-projector wall | 2-4 | Flat | 3840x2400 | Medium |
| Curved cyclorama | 2-6 | Curved | 3840x2400+ | High |
| 360Ã‚Â° cylinder | 4-8 | Cylindrical | 7680x2400+ | Very high |
| Object mapping | 1-4 | 3D object | Variable | Very high |
| Floor projection | 1-2 | Floor | 1920x1200 | Medium |

### Complete Warping Mesh Reference

| Grid Size | Control Points | Use Case | Accuracy |
|-----------|---------------|----------|----------|
| 2x2 | 4 | Simple planar | Low |
| 4x4 | 16 | Basic curved surface | Medium |
| 8x8 | 64 | Standard curved surface | Good |
| 16x16 | 256 | Complex organic shapes | High |
| 32x32 | 1024 | Very complex surfaces | Very high |

### Interactive Tracking System Comparison

| System | Latency | Accuracy | Range | Cost |
|--------|---------|----------|-------|------|
| ArUco Markers | 33ms | Ã‚Â±5mm | Camera FOV | Low |
| Intel RealSense | 33ms | Ã‚Â±2mm | 0.2-10m | Medium |
| Azure Kinect | 33ms | Ã‚Â±1mm | 0.5-5m | Medium |
| OptiTrack | 8ms | Ã‚Â±0.1mm | 1-15m | High |
| Vicon | 8ms | Ã‚Â±0.05mm | 1-30m | Very High |
| IR Markers | 16ms | Ã‚Â±10mm | 5-50m | Medium |

### Content Format Reference

| Format | Codec | Best For | Notes |
|--------|-------|----------|-------|
| ProRes 422 | Apple ProRes | General | Wide compatibility |
| ProRes 4444 | Apple ProRes | Alpha channel | Transparency support |
| DNxHR | Avid | Post-production | Cross-platform |
| H.264 | MPEG-4 | Streaming | Compression artifacts |
| H.265/HEVC | MPEG-4 | 4K content | Better compression |
| Animation | RLE | Graphics | Lossless, large files |

### Projector Maintenance Schedule

| Task | Frequency | Duration |
|------|-----------|----------|
| Clean air filter | Weekly | 10 min |
| Check lamp hours | Weekly | 5 min |
| Clean lens | Monthly | 15 min |
| Check ventilation | Monthly | 10 min |
| Calibrate color | Per production | 30 min |
| Replace lamp | As needed | 30 min |
| Full service | Annually | 2 hours |

### 3D Surface Scanning Workflow

```
1. Prepare Surface
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Ensure surface is clean and dry
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Apply matte white coating if needed
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Mark reference points with tape
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Darken room completely

2. Position Scanner
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Place structured light projector
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Position cameras at known offsets
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Calibrate camera-projector system
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Set exposure and focus

3. Capture Patterns
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Project gray code sequence (24 patterns)
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Capture each pattern with camera
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Verify pattern visibility
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Capture reference color patches

4. Process Point Cloud
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Generate depth map from patterns
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Convert to 3D point cloud
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Remove noise and outliers
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Export as OBJ/PLY mesh

5. Generate Warping Mesh
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Import surface mesh
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Generate control point grid
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Map projector pixels to surface
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Test with alignment pattern
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Export warping data for media server

### Complete Projector Settings Reference

| Parameter | Standard | Short Throw | Rear Projection |
|-----------|---------|-------------|-----------------|
| Brightness | 10,000+ lm | 5,000+ lm | 10,000+ lm |
| Contrast | > 10,000:1 | > 5,000:1 | > 10,000:1 |
| Resolution | 1920x1200 | 1920x1200 | 1920x1200+ |
| Lens shift | Ã‚Â±50% V | Fixed | Ã‚Â±50% V |
| Throw ratio | 1.5-2.5:1 | 0.8-1.5:1 | 1.0-2.0:1 |
| Lamp hours | 2,000-4,000 | 2,000-4,000 | 2,000-4,000 |

### Color Space Reference

| Color Space | Use Case | Gamut |
|------------|----------|-------|
| sRGB | Web content | Smallest |
| Rec. 709 | HD video | Standard |
| Rec. 2020 | 4K/HDR video | Wide |
| DCI-P3 | Cinema | Wide |
| Adobe RGB | Print | Wide |

### Projection Surface Preparation Guide

```
SURFACE PREPARATION CHECKLIST
    Ã¢â€“Â¡ Clean surface thoroughly (no dust, fingerprints)
    Ã¢â€“Â¡ Fill any holes or cracks with appropriate filler
    Ã¢â€“Â¡ Sand smooth any rough spots
    Ã¢â€“Â¡ Apply matte white projection paint (if needed)
    Ã¢â€“Â¡ Allow 24 hours drying time
    Ã¢â€“Â¡ Verify uniform reflectance with light meter
    Ã¢â€“Â¡ Mark reference points for calibration
    Ã¢â€“Â¡ Photograph surface from audience perspective
    Ã¢â€“Â¡ Document surface dimensions and curvature
```

### Multi-Projector Alignment Procedure

```
1. PHYSICAL ALIGNMENT
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Mount projectors securely
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Aim at center of respective surface areas
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Adjust lens shift for vertical alignment
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Verify overlap zones are sufficient
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Check for keystone distortion

2. DIGITAL ALIGNMENT
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Project alignment grid
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Adjust keystone correction
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Fine-tune zoom and focus
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Verify pixel-level alignment
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Document final positions

3. COLOR MATCHING
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Warm up projectors 30 minutes
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Project white field
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Measure with colorimeter
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Adjust RGB gains to match
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Verify at blend boundaries
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Generate correction LUT

4. EDGE BLENDING
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Identify overlap zones
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Set blend width (10%+ of resolution)
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Adjust blend gamma curves
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Verify smooth transition
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check for banding artifacts
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Fine-tune at multiple brightness levels

5. VERIFICATION
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Project test patterns
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Check color uniformity
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Verify blend smoothness
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Test with actual content
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Get designer approval
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Document final settings
```

### Content Resolution Recommendations

| Output Resolution | Content Resolution | Frame Rate | Bitrate |
|-------------------|-------------------|-----------|---------|
| 1920x1200 | 1920x1200 | 30 fps | 50 Mbps |
| 1920x1200 | 1920x1200 | 60 fps | 100 Mbps |
| 3840x2400 | 3840x2400 | 30 fps | 150 Mbps |
| 3840x2400 | 3840x2400 | 60 fps | 300 Mbps |

### Interactive Tracking Calibration

```
TRACKING CALIBRATION WORKFLOW
    Ã¢â€“Â¡ Position camera(s) for full stage view
    Ã¢â€“Â¡ Calibrate camera intrinsic parameters
    Ã¢â€“Â¡ Calibrate camera-projector homography
    Ã¢â€“Â¡ Place ArUco markers on tracking targets
    Ã¢â€“Â¡ Verify marker detection at all positions
    Ã¢â€“Â¡ Map camera coordinates to projection UV
    Ã¢â€“Â¡ Test tracking latency (< 50ms target)
    Ã¢â€“Â¡ Verify tracking across full stage area
    Ã¢â€“Â¡ Document camera positions and settings
    Ã¢â€“Â¡ Test with performers on stage
```
```


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
