---
name: "ar-vr-development"
category: "ar-vr"
version: "2.0.0"
tags: ["ar", "vr", "xr", "mixed-reality", "unity", "unreal", "webxr", "oculus"]
---

# AR/VR Development

## Overview

Comprehensive AR/VR/XR development toolkit covering cross-platform immersive application development for Meta Quest, Apple Vision Pro, HoloLens, and WebXR. This module provides Unity and Unreal Engine project scaffolding, spatial interaction patterns, hand/eye tracking integration, performance optimization for mobile XR, multiplayer networking, and deployment pipelines. Supports both native and web-based immersive experiences with focus on comfort, accessibility, and performance.

## Core Capabilities

- **Cross-Platform XR**: Build once for Quest 3, Vision Pro, HoloLens 2, and WebXR with platform abstraction layers
- **Spatial Interaction**: Grab, poke, ray-cast, and gaze-based interaction patterns with haptic feedback
- **Hand Tracking**: Full hand tracking with gesture recognition, pinch detection, and skeletal hand models
- **Eye Tracking**: Foveated rendering, gaze-based UI, and attention analytics
- **Performance Optimization**: Frame time budgets, foveated rendering, async spacewarp, and level-of-detail for XR
- **Multiplayer XR**: Shared spatial experiences with networked object synchronization and voice chat
- **Passthrough AR**: Camera passthrough with depth occlusion and plane detection
- **Deployment**: Automated build pipelines for app stores and enterprise distribution

## Usage

```python
from ar_vr_development import (
    XRProject, Platform, InteractionType, PerformanceProfile
)

# Create XR project
project = XRProject(
    name="SpatialCollaboration",
    engine="unity",
    platforms=[Platform.QUEST_3, Platform.WEBXR],
    target_framerate=90,
    render_scale=1.0,
)

# Configure interactions
project.add_interaction(InteractionType.HAND_TRACKING, {
    "gesture_recognition": True,
    "grab_distance_m": 0.5,
    "haptic_feedback": True,
})
project.add_interaction(InteractionType.EYE_TRACKING, {
    "foveated_rendering": True,
    "gaze_ui": True,
    "attention_heatmap": True,
})

# Performance profile
profile = PerformanceProfile(
    target_framerate=90,
    ms_per_frame=11.1,
    fixed_foveated_rendering_level=3,
    application_spacewarp=True,
    gpu_skinning=True,
    single_pass_stereo=True,
)
project.set_performance_profile(profile)

# Build
result = project.build(platform=Platform.QUEST_3, configuration="release")
print(f"Build: {result.output_path}")
print(f"Size: {result.apk_size_mb:.1f} MB")
print(f"Build time: {result.build_time_s:.0f}s")
```

```python
# Spatial anchor management
from ar_vr_development import SpatialAnchorManager

anchors = SpatialAnchorManager()
anchor = anchors.create(
    position=(1.5, 1.0, 2.0),
    rotation=(0, 0, 0, 1),
    label="Virtual Whiteboard",
    persistent=True,
)
print(f"Anchor: {anchor.anchor_id} at {anchor.position}")

# Multiplayer
from ar_vr_development import XRNetworking
network = XRNetworking(room_id="collab-room-001", max_players=8)
network.sync_object("shared-model-01", position=(0, 1, 3), ownership="dynamic")
```

## Best Practices

- Target 90fps minimum — any frame drops cause motion sickness in VR
- Use fixed foveated rendering to reduce GPU load without visible quality loss
- Implement comfort vignetting during locomotion to reduce simulator sickness
- Design for seated, standing, and room-scale experiences — don't assume full room
- Use spatial audio for all interactive objects to enhance presence
- Test with users of different heights and physical abilities
- Implement teleport locomotion as default — smooth locomotion causes nausea for many
- Use passthrough for AR experiences rather than virtual-only environments
- Keep UI at arm's length (0.5-1.5m) and within 30° of center gaze
- Optimize draw calls aggressively — mobile XR GPUs have strict thermal limits

## Related Modules

- **mixed-reality** — MR-specific patterns and passthrough integration
- **spatial-computing** — Spatial anchors, meshes, and scene understanding
- **3d-rendering** — Optimized 3D rendering pipelines for XR
- **gesture-recognition** — Hand and eye gesture recognition systems
- **ar-vr** → **ar-vr-development** — Development workflow and tooling
