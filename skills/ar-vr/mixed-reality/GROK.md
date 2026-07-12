---
name: "mixed-reality"
category: "ar-vr"
version: "2.0.0"
tags: ["mixed-reality", "passthrough", "occlusion", "spatial-anchor", "world-meshing", "vision-pro"]
---

# Mixed Reality

## Overview

Mixed reality development toolkit for building experiences that blend virtual content with the physical world using camera passthrough, depth sensing, plane detection, mesh reconstruction, and spatial anchoring. This module supports Apple Vision Pro (visionOS), Meta Quest passthrough, HoloLens spatial mapping, and WebXR hit-test modules with focus on realistic occlusion, lighting estimation, and world-understanding for immersive AR applications.

## Core Capabilities

- **Camera Passthrough**: Real-time camera passthrough with depth occlusion for virtual object placement
- **Plane Detection**: Horizontal and vertical plane detection with classification (floor, wall, table, ceiling)
- **Mesh Reconstruction**: Real-time 3D mesh generation from depth data for environmental understanding
- **Spatial Anchors**: Persistent, cloud-synchronized anchors that survive session boundaries
- **Occlusion**: Virtual object occlusion by real-world geometry using depth buffers
- **Lighting Estimation**: Real-time environment lighting estimation for realistic virtual object rendering
- **Scene Understanding**: Semantic classification of real-world surfaces and objects
- **Shared MR Experiences**: Multi-user shared mixed reality with synchronized spatial content

## Usage

```python
from mixed_reality import (
    PassthroughManager, PlaneDetector, MeshReconstructor, OcclusionManager
)

# Configure passthrough
passthrough = PassthroughManager(
    platform="quest_3",
    depth_mode="medium",
    color_adjustments={"brightness": 1.0, "contrast": 1.1},
)
passthrough.enable()
print(f"Passthrough: {passthrough.status}")

# Plane detection
detector = PlaneDetector()
planes = detector.detect(max_planes=20, min_area_sqm=0.25)
for plane in planes:
    print(f"  {plane.classification}: {plane.area_sqm:.2f}m² at ({plane.center[0]:.1f}, {plane.center[1]:.1f}, {plane.center[2]:.1f})")

# Mesh reconstruction
mesh = MeshReconstructor(resolution="medium", max_triangles=100000)
mesh_data = mesh.reconstruct()
print(f"Mesh: {mesh_data.vertex_count} vertices, {mesh_data.triangle_count} triangles")

# Occlusion
occlusion = OcclusionManager(depth_buffer="environment")
occlusion.enable_for_object("virtual-character")
```

```python
# Place virtual object on detected plane
from mixed_reality import MRSceneManager

scene = MRSceneManager()
# Find a horizontal surface
table = detector.find_plane(classification="table", min_area=0.5)
if table:
    anchor = scene.place_object(
        object_id="coffee-mug",
        mesh_path="models/mug.glb",
        plane_id=table.plane_id,
        offset=(0, 0.05, 0),
    )
    print(f"Placed mug on table at {anchor.position}")
```

## Best Practices

- Always use depth-based occlusion for virtual objects — objects floating over real geometry break presence
- Detect planes before placing objects — never assume surfaces exist
- Use environment lighting estimation to match virtual object shadows and reflections
- Test passthrough quality in different lighting conditions — low light degrades depth sensing
- Implement mesh collision for interactive virtual objects that should interact with real surfaces
- Use persistent anchors for objects that should stay in place across sessions
- Limit mesh resolution to maintain performance — medium resolution is sufficient for most interactions
- Implement scene semantics (floor, wall, furniture) for context-aware object placement
- Account for passthrough latency (~12ms) when synchronizing virtual and real movements
- Test MR experiences on actual hardware — simulator passthrough differs from real cameras

## Related Modules

- **ar-vr-development** — Cross-platform XR development patterns
- **spatial-computing** — Spatial anchors, meshes, and scene understanding
- **3d-rendering** — Optimized rendering for passthrough environments
- **gesture-recognition** — Hand tracking in mixed reality contexts
- **ambient-computing** → **proximity-sensing** — Physical space awareness
