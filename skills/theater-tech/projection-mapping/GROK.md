---
name: "projection-mapping"
category: "theater-tech"
version: "1.0.0"
tags: ["theater-tech", "projection-mapping", "media-server", "3d-calibration", "blending"]
---

# Projection Mapping System

## Overview

The projection mapping module provides a comprehensive Python API for 3D surface calibration, multi-projector alignment, edge blending, real-time content warping, and media server integration for theatrical and live entertainment environments. It abstracts the complexity of mapping flat or curved video content onto irregular 3D surfaces — architectural facades, scenic elements, performer costumes, stage floors, and custom-built set pieces — into a programmable pipeline that can be calibrated, tested, and automated from a single interface.

At its core, projection mapping solves the geometric problem of transforming a rectangular video source to fit an arbitrary 3D surface as seen from a specific projector position. The module implements homography-based warping for planar surfaces, mesh-based deformation for curved and organic shapes, and lenticular blending for multi-projector overlap zones. Each projector's output passes through a calibration pipeline: intrinsic lens correction (keystone, barrel distortion), extrinsic pose estimation (position and orientation relative to the surface), mesh warping (control-point-based deformation), and color matching (gamut and brightness alignment across projectors).

Multi-projector setups require seamless edge blending: where two projectors overlap, their outputs must cross-fade smoothly to create the illusion of a single continuous image. The module handles both horizontal and vertical blend regions, with configurable gamma curves to compensate for the additive brightness in overlap zones. For curved surfaces, the blend width varies across the overlap — wider at the center where projectors are more perpendicular, narrower at the edges where viewing angles are oblique.

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
┌─────────────────────────────────────────────────────────┐
│              Content & Media Server Layer                │
│     (NDI, SDI, Media Playback, Generative Content)      │
├─────────────────────────────────────────────────────────┤
│              Warping & Blending Engine                   │
│   (Mesh Deformation, Edge Blending, Color Matching)     │
├─────────────────────────────────────────────────────────┤
│              Calibration Pipeline                        │
│  (Homography, Keystone, Lens Correction, Pose Est.)     │
├─────────────────────────────────────────────────────────┤
│              Surface & Projector Model                   │
│    (3D Mesh, Curvature, Projector Optics, Position)     │
├─────────────────────────────────────────────────────────┤
│              Interactive Tracking Layer                  │
│     (ArUco, Depth Sensors, Skeleton, IR Markers)        │
└─────────────────────────────────────────────────────────┘
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
| Blend Width | 200px | 50–500px | Edge blend region width in pixels |
| Blend Gamma | 2.2 | 1.0–3.0 | Gamma curve for blend compensation |
| Control Points | 8x8 | 2x2–32x32 | Mesh resolution for warping |
| Mesh Smoothing | 0.5 | 0.0–1.0 | Smoothing strength for control points |
| Color Temp Match | ±100K | ±50–500K | White-point matching tolerance |

## Related Modules

- [lighting-control](../lighting-control/GROK.md) — Lighting color matching for projection ambient compensation
- [stage-automation](../stage-automation/GROK.md) — Automated scenic movement tracking for dynamic projection surfaces
- [sound-engineering](../sound-engineering/GROK.md) — Spatial audio alignment with projection-mapped environments
- [audience-engagement](../audience-engagement/GROK.md) — Interactive audience-triggered projection content
