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
    print(f"Touch at {point} Ã¢â‚¬â€ gesture: {gesture}")

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
- Use anonymous tracking only Ã¢â‚¬â€ never collect personal data in public installations
- Implement watchdog timers that auto-restart crashed content players
- Design content for minimum 2-hour loops to avoid visible repetition
- Calibrate color across projectors to ensure seamless blending
- Use depth cameras for touchless interaction in high-traffic public spaces
- Schedule content transitions during low-visitor periods
- Monitor temperature of projectors and LED panels Ã¢â‚¬â€ they overheat in enclosed spaces
- Design interactive thresholds generously Ã¢â‚¬â€ fat finger and cold hands need larger targets

## Related Modules

- **generative-art** Ã¢â‚¬â€ Content generation for installations
- **audio-visual** Ã¢â‚¬â€ Audio-reactive installation content
- **interactive-media** Ã¢â‚¬â€ Interaction design for public art
- **3d-rendering** Ã¢â‚¬â€ Real-time rendering for immersive installations
- **ambient-computing** Ã¢â€ â€™ **smart-environments** Ã¢â‚¬â€ Building integration for installations

## Advanced Configuration

### Projection Mapping Advanced

```python
from digital_installations import ProjectionMapping, ProjectionConfig, WarpingEngine

projection_config = ProjectionConfig(
    projectors=[
        {"id": "proj-1", "resolution": (1920, 1080), "brightness_lumens": 5000, "throw_ratio": 1.5},
        {"id": "proj-2", "resolution": (1920, 1080), "brightness_lumens": 5000, "throw_ratio": 1.5},
        {"id": "proj-3", "resolution": (1920, 1080), "brightness_lumens": 5000, "throw_ratio": 1.5},
    ],
    blending={
        "edge_blend_width": 100,  # pixels
        "blend_gamma": 2.2,
        "color_correction": True,
        "white_point_correction": True,
    },
    warping={
        "mesh_resolution": 20,  # 20x20 control points
        "interpolation": "bicubic",
        "brightness_uniformity": True,
        "geometric_correction": True,
    },
    calibration={
        "method": "automatic",  # manual, automatic, hybrid
        "camera_input": True,
        "pattern_type": "checkerboard",
        "subpixel_accuracy": True,
    },
)

# Initialize warping engine
warping = WarpingEngine(config=projection_config)

# Calibrate projectors
calibration_result = warping.calibrate()
print(f"Calibration accuracy: {calibration_result.accuracy:.3f}mm")
print(f"Color match: {calibration_result.color_delta:.2f} Delta E")

# Apply content
warping.set_content("projector_1", "video_wall.mp4")
warping.set_content("projector_2", "video_wall.mp4")
warping.set_content("projector_3", "video_wall.mp4")
```

### Multi-Screen Synchronization

```python
from digital_installations import MultiScreenSync, SyncConfig, FrameAccurateSync

sync_config = SyncConfig(
    displays=[
        {"id": "screen-1", "resolution": (3840, 2160), "refresh_rate": 60},
        {"id": "screen-2", "resolution": (3840, 2160), "refresh_rate": 60},
        {"id": "screen-3", "resolution": (3840, 2160), "refresh_rate": 60},
        {"id": "screen-4", "resolution": (3840, 2160), "refresh_rate": 60},
    ],
    sync_method="genlock",  # genlock, network, software
    sync_tolerance_ms=1.0,
    frame_accurate=True,
    color_sync=True,
    audio_sync=True,
)

# Initialize sync engine
sync = MultiScreenSync(config=sync_config)

# Start synchronized playback
sync.play("installation_video.mp4", loop=True)

# Monitor sync status
status = sync.get_status()
for display in status.displays:
    print(f"{display.id}: offset={display.offset_ms:.2f}ms, fps={display.current_fps:.1f}")
```

### Interactive Surface Advanced

```python
from digital_installations import InteractiveSurface, SurfaceConfig, TouchEngine

surface_config = SurfaceConfig(
    surface_id="wall-north",
    input_type="depth_camera",  # touch, depth_camera, lidar, radar
    resolution=(1920, 1080),
    interaction_radius_m=2.0,
    max_touch_points=20,
    latency_ms=16,
    calibration={
        "depth_accuracy_mm": 5,
        "noise_filter": True,
        "temporal_smoothing": True,
        "occlusion_handling": True,
    },
    gestures={
        "tap": {"min_duration_ms": 50, "max_duration_ms": 300},
        "hold": {"min_duration_ms": 500},
        "swipe": {"min_distance": 50, "max_duration_ms": 500},
        "pinch": {"min_distance": 20, "max_distance": 200},
        "rotate": {"min_angle": 10, "min_duration_ms": 200},
    },
)

# Initialize touch engine
touch_engine = TouchEngine(config=surface_config)

# Process touch input
@touch_engine.on_touch
def on_touch(point, gesture, confidence):
    print(f"Touch at {point} - gesture: {gesture} ({confidence:.2f})")
    
    if gesture == "tap":
        trigger_animation(point)
    elif gesture == "swipe":
        swipe_direction = touch_engine.get_swipe_direction(point)
        change_content(swipe_direction)
```

## Architecture Patterns

### Digital Installation Architecture

```
+------------------------------------------------------------------+
|                Digital Installation Architecture                  |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------+    +----------------+    +----------------+  |
|  |  Content       |    |  Playback      |    |  Output        |  |
|  |  Management    |    |  Engine        |    |  Layer         |  |
|  |                |    |                |    |                |  |
|  |  Media Library |    |  Video Player  |    |  Projectors    |  |
|  |  Playlists     |<-->|  Audio Engine  |<-->|  LED Panels    |  |
|  |  Scheduling    |    |  Renderer      |    |  Displays      |  |
|  +-------+--------+    +-------+--------+    +-------+--------+  |
|          |                    |                     |             |
|          v                    v                     v             |
|  +----------------------------------------------------------------+
|  |                    Control System                              |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  DMX         |  |  OSC         |  |  MIDI        |          |
|  |  |  Controller  |  |  Controller  |  |  Controller  |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Sensor      |  |  Lighting    |  |  Audio       |          |
|  |  |  Network     |  |  System      |  |  System      |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
|                              |                                    |
|                              v                                    |
|  +----------------------------------------------------------------+
|  |                    Monitoring & Control                        |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Health      |  |  Remote      |  |  Analytics   |          |
|  |  |  Monitoring  |  |  Control     |  |  Tracking    |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
+------------------------------------------------------------------+
```

### Content Scheduling System

```
Content Scheduling Pipeline
        |
        v
+-------------------+
|  Time-based       |  Check schedule
+-------------------+
        |
        v
+-------------------+
|  Event-based      |  Check triggers
+-------------------+
        |
        v
+-------------------+
|  Content Selection|  Choose content
+-------------------+
        |
        v
+-------------------+
|  Transition       |  Fade/cut/crossfade
+-------------------+
        |
        v
+-------------------+
|  Playback         |  Start new content
+-------------------+
        |
        v
+-------------------+
|  Monitoring       |  Track playback
+-------------------+
```

### Hardware Control Flow

```
Hardware Control Architecture
        |
        v
+-------------------+
|  Command Input    |  User/system command
+-------------------+
        |
        v
+-------------------+
|  Protocol Select  |  DMX/OSC/MIDI
+-------------------+
        |
        v
+-------------------+
|  Command Build    |  Create message
+-------------------+
        |
        v
+-------------------+
|  Send Command     |  Transmit to device
+-------------------+
        |
        v
+-------------------+
|  Acknowledge      |  Wait for response
+-------------------+
        |
        v
+-------------------+
|  Update State     |  Update device state
+-------------------+
```

## Integration Guide

### DMX Lighting Integration

```python
from digital_installations import DMXController, DMXChannel, LightingScene

# Initialize DMX controller
dmx = DMXController(
    interface="enttec_usb_pro",
    universe=1,
    start_channel=1,
)

# Define lighting channels
channels = {
    "red": DMXChannel(channel=1, name="Red"),
    "green": DMXChannel(channel=2, name="Green"),
    "blue": DMXChannel(channel=3, name="Blue"),
    "white": DMXChannel(channel=4, name="White"),
    "dimmer": DMXChannel(channel=5, name="Dimmer"),
    "strobe": DMXChannel(channel=6, name="Strobe"),
}

# Create lighting scenes
scene = LightingScene()
scene.set_channel(channels["red"], 255)
scene.set_channel(channels["green"], 128)
scene.set_channel(channels["blue"], 0)
scene.set_channel(channels["dimmer"], 200)

# Apply scene
dmx.apply_scene(scene)
dmx.flush()
```

### OSC Integration

```python
from digital_installations import OSCController, OSCMessage

# Initialize OSC controller
osc = OSCController(
    target_ip="192.168.1.100",
    target_port=9000,
    local_port=9001,
)

# Send OSC message
osc.send(OSCMessage(
    address="/installation/trigger",
    arguments=["start", 1.0, 0.5],
))

# Receive OSC messages
@osc.on_message
def on_message(address, *args):
    print(f"Received: {address} {args}")
    if address == "/sensor/data":
        process_sensor_data(args[0], args[1])
```

### Web-Based CMS Integration

```python
from digital_installations import InstallationCMS, CMSConfig

cms_config = CMSConfig(
    host="0.0.0.0",
    port=8080,
    auth={
        "method": "jwt",
        "secret": "your-secret-key",
        "token_expiry_hours": 24,
    },
    database={
        "type": "postgresql",
        "url": "postgresql://user:pass@localhost/installation",
    },
)

# Initialize CMS
cms = InstallationCMS(config=cms_config)

# Upload content
cms.upload_content(
    file="video.mp4",
    metadata={
        "name": "Main Loop",
        "duration": 300,
        "tags": ["ambient", "loop"],
    },
)

# Schedule content
cms.schedule_content(
    content_id="video-001",
    schedule={
        "days": [1, 2, 3, 4, 5],
        "start_time": "08:00",
        "end_time": "18:00",
    },
)
```

## Performance Optimization

### Playback Optimization

```python
from digital_installations import PlaybackOptimizer, PerformanceConfig

optimizer = PlaybackOptimizer(
    config=PerformanceConfig(
        target_fps=60,
        buffer_size_mb=256,
        predecode_frames=30,
    ),
    optimizations={
        "hardware_decoding": True,
        "gpu_acceleration": True,
        "memory_mapping": True,
        "frame_prefetch": True,
        "audio_sync": True,
    },
)

# Optimize video playback
optimizer.optimize_video("installation_video.mp4")

# Monitor performance
stats = optimizer.get_stats()
print(f"Frame drop rate: {stats.frame_drop_rate:.2%}")
print(f"Buffer usage: {stats.buffer_usage_mb:.1f}MB")
print(f"Decode time: {stats.decode_time_ms:.2f}ms")
```

### Memory Management

```python
from digital_installations import MemoryManager, MediaCache

memory_mgr = MemoryManager(
    total_budget_mb=4096,
    video_buffer_mb=2048,
    audio_buffer_mb=512,
    texture_buffer_mb=1024,
)

# Media caching
media_cache = MediaCache(
    max_size_mb=2048,
    eviction_policy="lru",
    preload_next=True,
)

# Monitor memory
stats = memory_mgr.get_stats()
print(f"Total usage: {stats.total_mb:.1f}MB")
print(f"Cache hit rate: {media_cache.hit_rate:.2%}")
```

## Security Considerations

### Network Security

```python
from digital_installations import NetworkSecurity, FirewallConfig

security = NetworkSecurity(
    firewall=FirewallConfig(
        allowed_ips=["192.168.1.0/24"],
        blocked_ports=[22, 3389],
        rate_limiting=True,
        ddos_protection=True,
    ),
    encryption={
        "control_channel": "tls",
        "media_streaming": "dtls",
        "api_access": "https",
    },
    authentication={
        "method": "certificate",
        "mutual_auth": True,
        "token_expiry_hours": 24,
    },
)

# Apply security policy
security.apply_policy()
```

### Content Protection

```python
from digital_installations import ContentProtection, DRMConfig

protection = ContentProtection(
    drm=DRMConfig(
        enabled=True,
        watermark=True,
        watermark_position="bottom_right",
        watermark_opacity=0.3,
        copy_protection=True,
    },
    encryption={
        "algorithm": "aes-256",
        "key_rotation_days": 7,
    },
)

# Protect content
protected_video = protection.encrypt("video.mp4")
secure_store.put("video.enc", protected_video)
```

## Troubleshooting Guide

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Projector misalignment** | Content misaligned | Recalibrate, check mounting |
| **Sync issues** | Displays not synced | Check sync signal, adjust timing |
| **DMX failures** | Lighting not responding | Check cable, verify channel mapping |
| **Content stuttering** | Jerky playback | Increase buffer, check disk speed |
| **Memory leaks** | Growing memory usage | Restart application, check for leaks |
| **Network latency** | Delayed control | Check network, reduce packet size |
| **Audio sync issues** | Sound out of sync | Adjust audio delay, check buffer |
| **Sensor errors** | No interaction | Check sensor connection, recalibrate |

## API Reference

```python
class Installation:
    """Installation management."""
    
    def __init__(self, name: str, venue: str, spaces: List[dict]):
        """Initialize installation."""
        
    def start(self) -> None:
        """Start installation."""
        
    def stop(self) -> None:
        """Stop installation."""
        
    def get_status(self) -> InstallationStatus:
        """Get installation status."""

class Projector:
    """Projector management."""
    
    def __init__(self, id: str, resolution: tuple, brightness_lumens: int):
        """Initialize projector."""
        
    def calibrate(self, surface: str, corner_points: List[tuple]) -> CalibrationResult:
        """Calibrate projector."""

class ContentScheduler:
    """Content scheduling."""
    
    def __init__(self):
        """Initialize scheduler."""
        
    def add_playlist(self, name: str, items: List[dict]) -> None:
        """Add playlist."""
        
    def schedule(self, playlist_name: str, days: List[int], start: str, end: str) -> None:
        """Schedule playlist."""
```

## Data Models

```python
@dataclass
class InstallationSpace:
    """Installation space."""
    id: str
    type: str  # projection, led, display
    resolution: tuple
    projectors: Optional[List[dict]]

@dataclass
class CalibrationResult:
    """Calibration result."""
    accuracy: float
    color_delta: float
    geometric_error: float
    calibration_time_s: float

@dataclass
class ContentItem:
    """Content item."""
    id: str
    name: str
    duration: float
    file_path: str
    metadata: dict

@dataclass
class ScheduleEntry:
    """Schedule entry."""
    playlist_name: str
    days: List[int]
    start_time: str
    end_time: str
    priority: int
```

## Deployment Guide

### Installation Setup

```python
from digital_installations import InstallationSetup, SetupConfig

setup_config = SetupConfig(
    name="Immersive Lobby",
    venue="Museum of Modern Art",
    spaces=[
        {"id": "wall-north", "type": "projection", "resolution": (3840, 2160)},
        {"id": "floor-main", "type": "led", "resolution": (1920, 1080)},
    ],
    hardware={
        "projectors": 4,
        "led_panels": 8,
        "sensors": 12,
        "audio_system": True,
        "lighting": True,
    },
)

# Setup installation
setup = InstallationSetup(config=setup_config)
setup.deploy()
```

## Monitoring & Observability

```python
from digital_installations import InstallationMonitor, Metrics

monitor = InstallationMonitor(
    metrics=Metrics(
        tracks=[
            "cpu_usage",
            "memory_usage",
            "disk_usage",
            "network_latency",
            "frame_rate",
            "error_rate",
        ],
        sample_rate=1.0,
    ),
    alerts={
        "cpu_high": {"threshold": 80, "action": "notify"},
        "memory_high": {"threshold": 85, "action": "restart"},
        "error_rate_high": {"threshold": 0.01, "action": "notify"},
    },
)

# Start monitoring
monitor.start()
```

## Testing Strategy

```python
import pytest
from digital_installations import Installation, Projector

class TestInstallation:
    def test_installation_start(self):
        installation = Installation(
            name="Test",
            venue="Test Venue",
            spaces=[],
        )
        installation.start()
        assert installation.is_running
    
    def test_projector_calibration(self):
        projector = Projector(
            id="proj-1",
            resolution=(1920, 1080),
            brightness_lumens=5000,
        )
        result = projector.calibrate(
            surface="wall",
            corner_points=[(0, 0), (1920, 0), (1920, 1080), (0, 1080)],
        )
        assert result.accuracy < 1.0
```

## Versioning & Migration

| Version | Changes | Breaking |
|---------|---------|----------|
| 2.0.0 | Added web CMS, improved sync | Yes |
| 1.5.0 | Added multi-projector support | No |
| 1.0.0 | Initial release | N/A |

## Glossary

| Term | Definition |
|------|------------|
| **Projection Mapping** | Warping content to fit surfaces |
| **Edge Blending** | Seamless projector overlap |
| **DMX** | Digital Multiplex lighting control |
| **OSC** | Open Sound Control protocol |
| **Genlock** | Frame synchronization signal |
| **Color Calibration** | Matching colors across devices |
| **Warping** | Geometric correction for projection |

## Changelog

### 2.0.0 (2024-01-15)
- Added web-based CMS
- Improved multi-screen sync
- Added interactive surfaces

### 1.5.0 (2023-10-01)
- Added DMX control
- Improved projection mapping

### 1.0.0 (2023-06-01)
- Initial release

## Contributing Guidelines

```bash
git clone https://github.com/company/digital-installations.git
cd digital-installations
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Company Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


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
