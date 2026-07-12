---
name: "digital-installations"
category: "art-tech"
version: "2.0.0"
tags: ["digital-art", "installations", "projection-mapping", "interactive", "museum", "exhibition"]
---

# Digital Installations

## Overview

Framework for creating and managing digital art installations across galleries, museums, public spaces, and event venues. This module provides projection mapping, interactive wall and floor displays, multi-screen synchronization, visitor interaction tracking, content scheduling, and hardware orchestration for projectors, LED panels, sensors, and audio systems. Supports permanent and temporary installations with remote monitoring and content management.

## Core Capabilities

- **Projection Mapping**: Warp, blend, and mask content across multiple projectors on complex surfaces
- **Multi-Screen Sync**: Frame-accurate synchronization across multiple displays and projectors
- **Interactive Surfaces**: Touch, proximity, and gesture interaction for wall and floor installations
- **Visitor Tracking**: Anonymous visitor counting, dwell time, flow patterns, and heat maps
- **Content Scheduling**: Time-based and event-based content rotation with playlist management
- **Hardware Control**: DMX lighting, motorized screens, audio systems, and sensor networks
- **Remote Management**: Web-based CMS for content upload, scheduling, and health monitoring
- **Durability**: Failover systems, auto-restart, and watchdog monitoring for 24/7 operation

## Usage

```python
from digital_installations import (
    Installation, Projector, InteractiveSurface, ContentScheduler
)

# Define installation
installation = Installation(
    name="Immersive Lobby",
    venue="Museum of Modern Art",
    spaces=[
        {"id": "wall-north", "type": "projection", "resolution": (3840, 2160), "projectors": 2},
        {"id": "floor-main", "type": "led", "resolution": (1920, 1080)},
        {"id": "screen-entry", "type": "display", "resolution": (1920, 1080)},
    ],
)

# Configure projectors
projector = Projector(
    id="proj-1",
    resolution=(1920, 1080),
    brightness_lumens=5000,
    throw_ratio=1.5,
    lens_shift=True,
)
warp_mesh = projector.calibrate(surface="wall-north", corner_points=[
    (0, 0), (1920, 0), (1920, 1080), (0, 1080),
])

# Interactive surface
surface = InteractiveSurface(
    surface_id="wall-north",
    input_type="depth_camera",
    max_touch_points=20,
    interaction_radius_m=2.0,
)
@surface.on_touch
def on_touch(point, gesture):
    print(f"Touch at {point} — gesture: {gesture}")

# Content scheduling
scheduler = ContentScheduler()
scheduler.add_playlist("morning", [
    {"content": "ambient_flow.mp4", "duration": 300, "transition": "crossfade"},
    {"content": "data_rain.mp4", "duration": 600, "transition": "fade"},
])
scheduler.add_playlist("evening", [
    {"content": "night_mode.mp4", "duration": 3600},
])
scheduler.schedule("morning", days=[1,2,3,4,5], start="08:00", end="12:00")
scheduler.schedule("evening", days=[0,1,2,3,4,5,6], start="18:00", end="23:00")
```

## Best Practices

- Always have a backup content source and auto-failover for public installations
- Test projection calibration in actual venue lighting conditions
- Use anonymous tracking only — never collect personal data in public installations
- Implement watchdog timers that auto-restart crashed content players
- Design content for minimum 2-hour loops to avoid visible repetition
- Calibrate color across projectors to ensure seamless blending
- Use depth cameras for touchless interaction in high-traffic public spaces
- Schedule content transitions during low-visitor periods
- Monitor temperature of projectors and LED panels — they overheat in enclosed spaces
- Design interactive thresholds generously — fat finger and cold hands need larger targets

## Related Modules

- **generative-art** — Content generation for installations
- **audio-visual** — Audio-reactive installation content
- **interactive-media** — Interaction design for public art
- **3d-rendering** — Real-time rendering for immersive installations
- **ambient-computing** → **smart-environments** — Building integration for installations
