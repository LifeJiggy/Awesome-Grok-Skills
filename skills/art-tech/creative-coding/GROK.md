---
name: "creative-coding"
category: "art-tech"
version: "2.0.0"
tags: ["creative-coding", "processing", "p5js", "openframeworks", "touchdesigner", "livecoding"]
---

# Creative Coding

## Overview

Creative coding toolkit for artists, designers, and creative technologists building visual, interactive, and generative experiences. This module provides frameworks for real-time visual programming, audio-reactive visuals, data-driven art, interactive installations, and live coding performances. Supports Processing, p5.js, OpenFrameworks, TouchDesigner, Hydra, and custom canvas/WebGL implementations with focus on artistic expression through code.

## Core Capabilities

- **Visual Programming**: Real-time canvas drawing, shape generation, color manipulation, and compositing
- **Audio-Reactive**: Microphone input, FFT analysis, beat detection, and frequency-band visualization
- **Data-Driven Art**: Transform datasets (CSV, JSON, API) into visual representations
- **Interactive Canvas**: Mouse, keyboard, touch, and tilt input for interactive generative art
- **Animation System**: Easing functions, tweening, particle systems, and physics simulation
- **Shader Integration**: GLSL fragment shaders for GPU-accelerated visual effects
- **Export & Recording**: Frame capture, video recording, GIF export, and print-ready output
- **Live Coding**: Hot-reload, live shader editing, and performance mode for live coding shows

## Usage

```python
from creative_coding import (
    Canvas, Color, Easing, AnimationSystem, AudioReactive, DataVisualizer
)

# Create canvas
canvas = Canvas(width=1920, height=1080, framerate=60, background=(10, 10, 15))

# Drawing primitives
canvas.fill(Color(255, 100, 50))
canvas.no_stroke()
canvas.ellipse(960, 540, 200, 200)

canvas.stroke(Color(255, 255, 255, 128))
canvas.stroke_weight(2)
canvas.line(0, 0, 1920, 1080)

# Animation system
anim = AnimationSystem()
ball = anim.create_object("ball", x=0, y=540)
anim.tween(ball, "x", 0, 1920, duration=3.0, easing=Easing.EASE_IN_OUT_CUBIC)
anim.tween(ball, "y", 540, 200, duration=1.5, easing=Easing.BOUNCE_OUT)

# Audio-reactive visuals
audio = AudioReactive(source="microphone", fft_size=1024)
bands = audio.get_frequency_bands()
canvas.fill(Color(bands["bass"] * 255, bands["mid"] * 255, bands["treble"] * 255))
canvas.rect(0, 0, 1920, 1080)

# Data visualization
viz = DataVisualizer(canvas)
data = [{"label": "A", "value": 42}, {"label": "B", "value": 78}, {"label": "C", "value": 35}]
viz.bar_chart(data, x=100, y=200, width=800, height=400, palette="warm")

# Export
canvas.save_frame("output/frame_####.png")
canvas.start_recording("output/animation.mp4", framerate=30, duration=10)
```

## Best Practices

- Start with a simple sketch and add complexity incrementally Ã¢â‚¬â€ resist the urge to build everything at once
- Use `randomSeed()` for reproducible randomness in generative compositions
- Save frames as image sequences for lossless recording Ã¢â‚¬â€ encode to video afterward
- Use easing functions for natural-feeling animations instead of linear interpolation
- Design at canvas resolution but think in relative coordinates for scalability
- Use blending modes (ADD, MULTIPLY, SCREEN) for layered visual effects
- Test on different screen sizes Ã¢â‚¬â€ creative code often breaks at non-standard resolutions
- Keep framerate stable by profiling expensive operations and using level-of-detail
- For audio-reactive work, smooth FFT data over 3-5 frames to prevent jittery visuals
- Use GLSL shaders for real-time effects that are too expensive on CPU

## Related Modules

- **generative-art** Ã¢â‚¬â€ Algorithmic art generation techniques
- **audio-visual** Ã¢â‚¬â€ Audio-visual synchronization and performance
- **interactive-media** Ã¢â‚¬â€ Interactive art and experience design
- **3d-rendering** Ã¢â‚¬â€ 3D creative coding and shader programming
- **digital-installations** Ã¢â‚¬â€ Physical installation output

## Advanced Configuration

### Canvas Configuration

```python
from creative_coding import Canvas, CanvasConfig, ColorMode

canvas_config = CanvasConfig(
    width=1920,
    height=1080,
    framerate=60,
    background=(10, 10, 15),
    color_mode=ColorMode.RGB,  # RGB, HSB, HSL
    color_range=255,
    smooth=True,
    anti_aliasing=True,
    pixel_density=1,  # Retina support
    blending_modes=["ADD", "MULTIPLY", "SCREEN", "OVERLAY"],
)

canvas = Canvas(config=canvas_config)

# Advanced drawing settings
canvas.set_drawing_settings(
    stroke_color=(255, 255, 255),
    stroke_weight=1,
    fill_color=(255, 100, 50),
    stroke_cap="round",
    stroke_join="round",
    blend_mode="ADD",
)

# Transform operations
canvas.push_matrix()
canvas.translate(960, 540)
canvas.rotate(45)
canvas.scale(1.5)
canvas.rect(-100, -100, 200, 200)
canvas.pop_matrix()
```

### Animation System Advanced

```python
from creative_coding import AnimationSystem, Easing, Tween

anim_system = AnimationSystem(
    framerate=60,
    auto_update=True,
)

# Create complex animations
ball = anim_system.create_object("ball", x=0, y=540, size=50, color=(255, 0, 0))

# Multi-property animation
anim_system.tween(ball, {
    "x": (0, 1920, 3.0, Easing.EASE_IN_OUT_CUBIC),
    "y": (540, 200, 1.5, Easing.BOUNCE_OUT),
    "size": (50, 100, 2.0, Easing.LINEAR),
    "color": ((255, 0, 0), (0, 0, 255), 3.0, Easing.LINEAR),
})

# Sequence animations
sequence = anim_system.sequence([
    {"object": "ball", "property": "x", "from": 0, "to": 1920, "duration": 2.0},
    {"object": "ball", "property": "y", "from": 540, "to": 0, "duration": 1.0, "delay": 0.5},
    {"object": "ball", "property": "size", "from": 100, "to": 50, "duration": 0.5},
])

# Parallel animations
parallel = anim_system.parallel([
    {"object": "ball1", "property": "x", "from": 0, "to": 1920, "duration": 3.0},
    {"object": "ball2", "property": "x", "from": 1920, "to": 0, "duration": 3.0},
])

# Physics simulation
physics = anim_system.add_physics(
    gravity=(0, 0.1),
    friction=0.99,
    bounce=0.8,
)
```

### Audio-Reactive Advanced

```python
from creative_coding import AudioReactive, FFTConfig, AudioAnalysis

audio_config = FFTConfig(
    source="microphone",
    fft_size=2048,
    hop_size=512,
    sample_rate=44100,
    window_function="hanning",
    frequency_bands={
        "sub_bass": (20, 60),
        "bass": (60, 250),
        "low_mid": (250, 500),
        "mid": (500, 2000),
        "high_mid": (2000, 4000),
        "presence": (4000, 6000),
        "brilliance": (6000, 20000),
    },
)

audio = AudioReactive(config=audio_config)

# Advanced analysis
analysis = audio.analyze()
print(f"BPM: {analysis.tempo_bpm:.1f}")
print(f"Beat strength: {analysis.beat_strength:.2f}")
print(f"Frequency bands: {analysis.bands}")
print(f"Spectral centroid: {analysis.spectral_centroid:.1f}Hz")
print(f"Spectral flux: {analysis.spectral_flux:.3f}")

# Audio-reactive visuals
@audio.on_beat
def on_beat(strength):
    # Trigger visual on beat
    canvas.fill(Color(strength * 255, 0, 0))
    canvas.rect(0, 0, canvas.width, canvas.height)

@audio.on_frequency_band
def on_frequency_band(band, amplitude):
    # Map frequency to visual
    if band == "bass":
        canvas.background(Color(amplitude * 255, 0, 0))
    elif band == "treble":
        particles.add_burst(canvas.width/2, canvas.height/2, amplitude * 100)
```

## Architecture Patterns

### Creative Coding Pipeline

```
+------------------------------------------------------------------+
|                 Creative Coding Pipeline                          |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------+    +----------------+    +----------------+  |
|  |  Input         |    |  Processing    |    |  Output        |  |
|  |  Layer         |    |  Engine        |    |  Layer         |  |
|  |                |    |                |    |                |  |
|  |  Mouse/Touch   |    |  Canvas        |    |  Screen        |  |
|  |  Keyboard      |<-->|  Animation     |<-->|  Recording     |  |
|  |  Audio         |    |  Physics       |    |  Streaming     |  |
|  |  Sensors       |    |  Particles     |    |  Export        |  |
|  +-------+--------+    +-------+--------+    +-------+--------+  |
|          |                    |                     |             |
|          v                    v                     v             |
|  +----------------------------------------------------------------+
|  |                    Core Systems                                |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Color       |  |  Math        |  |  Noise       |          |
|  |  |  System      |  |  Utilities   |  |  Generator   |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Particle    |  |  Easing      |  |  Shader      |          |
|  |  |  System      |  |  Functions   |  |  Pipeline    |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
+------------------------------------------------------------------+
```

### Real-Time Loop Architecture

```
Real-Time Loop (60fps)
        |
        v
+-------------------+
|  Handle Input     |  Process user input
+-------------------+
        |
        v
+-------------------+
|  Update State     |  Update animations, physics
+-------------------+
        |
        v
+-------------------+
|  Clear Canvas     |  Clear/background
+-------------------+
        |
        v
+-------------------+
|  Draw Content     |  Render shapes, images
+-------------------+
        |
        v
+-------------------+
|  Apply Effects    |  Filters, post-processing
+-------------------+
        |
        v
+-------------------+
|  Export Frame     |  Save if recording
+-------------------+
        |
        v
+-------------------+
|  Loop             |  Request next frame
+-------------------+
```

### Particle System Architecture

```
Particle System Pipeline
        |
        v
+-------------------+
|  Emit Particles   |  Create new particles
+-------------------+
        |
        v
+-------------------+
|  Apply Forces     |  Gravity, wind, attraction
+-------------------+
        |
        v
+-------------------+
|  Update Positions |  Move particles
+-------------------+
        |
        v
+-------------------+
|  Update Properties|  Size, color, alpha
+-------------------+
        |
        v
+-------------------+
|  Check Lifespan   |  Remove dead particles
+-------------------+
        |
        v
+-------------------+
|  Render Particles |  Draw to canvas
+-------------------+
```

## Integration Guide

### p5.js Integration

```javascript
// p5.js Creative Coding
let canvas;
let particles;
let audioReactive;

function setup() {
    canvas = createCanvas(1920, 1080);
    particles = new ParticleSystem(1000);
    audioReactive = new AudioReactive({
        source: 'microphone',
        fftSize: 2048,
    });
}

function draw() {
    // Audio analysis
    const analysis = audioReactive.analyze();
    
    // Clear with fade
    background(10, 10, 15, 25);
    
    // Audio-reactive visuals
    if (analysis.beat) {
        particles.addBurst(mouseX, mouseY, analysis.beatStrength * 100);
    }
    
    // Update and draw particles
    particles.addForce('gravity', createVector(0, 0.1));
    particles.update();
    particles.draw();
    
    // Interactive drawing
    if (mouseIsPressed) {
        particles.addEmitter(mouseX, mouseY, 10);
    }
}
```

### Processing Integration

```java
// Processing Creative Coding
import processing.svg.*;

PImage buffer;
ParticleSystem particles;
AudioReactive audio;

void setup() {
    size(1920, 1080, P2D);
    buffer = createGraphics(1920, 1080);
    particles = new ParticleSystem(1000);
    audio = new AudioReactive(this);
}

void draw() {
    // Audio analysis
    AudioAnalysis analysis = audio.analyze();
    
    // Fade background
    fill(10, 10, 15, 25);
    rect(0, 0, width, height);
    
    // Audio-reactive visuals
    if (analysis.isBeat()) {
        particles.addBurst(mouseX, mouseY, analysis.getBeatStrength() * 100);
    }
    
    // Update and draw particles
    particles.addForce(new PVector(0, 0.1));
    particles.update();
    particles.draw();
    
    // Export frame
    if (frameCount % 3 == 0) {
        saveFrame("output/frame_####.png");
    }
}
```

### GLSL Shader Integration

```glsl
// GLSL Fragment Shader for Creative Coding
#version 330 core

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform sampler2D u_texture;

out vec4 fragColor;

void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution;
    vec2 mouse = u_mouse / u_resolution;
    
    // Create dynamic pattern
    float d = distance(uv, mouse);
    float r = sin(d * 20.0 - u_time * 2.0) * 0.5 + 0.5;
    
    // Color mapping
    vec3 color1 = vec3(0.9, 0.3, 0.2);
    vec3 color2 = vec3(0.2, 0.4, 0.9);
    vec3 color = mix(color1, color2, r);
    
    // Add glow
    color += vec3(0.1) / (d + 0.1);
    
    fragColor = vec4(color, 1.0);
}
```

## Performance Optimization

### Rendering Optimization

```python
from creative_coding import RenderOptimizer, PerformanceConfig

optimizer = RenderOptimizer(
    config=PerformanceConfig(
        target_fps=60,
        max_frame_time_ms=16.7,
        buffer_size=3,  # Triple buffering
    ),
    optimizations={
        "spatial_hashing": True,
        "particle_culling": True,
        "level_of_detail": True,
        "shader_caching": True,
        "batch_rendering": True,
    },
)

# Optimize rendering
@optimizer.optimize_frame
def render_frame():
    # Spatial hashing for particles
    spatial_hash = optimizer.build_spatial_hash(particles, cell_size=50)
    
    # Cull off-screen particles
    visible_particles = optimizer.cull_offscreen(particles, viewport)
    
    # Batch render
    optimizer.batch_render(visible_particles)

# Monitor performance
stats = optimizer.get_stats()
print(f"Frame time: {stats.frame_time_ms:.2f}ms")
print(f"FPS: {stats.fps:.1f}")
print(f"Particles rendered: {stats.particles_rendered}")
print(f"Draw calls: {stats.draw_calls}")
```

### Memory Optimization

```python
from creative_coding import MemoryOptimizer, ObjectPool

memory_opt = MemoryOptimizer(
    object_pools={
        "particles": ObjectPool(max_size=10000, factory=lambda: Particle()),
        "shapes": ObjectPool(max_size=1000, factory=lambda: Shape()),
    },
    buffer_reuse=True,
    garbage_collection=True,
)

# Use object pooling
particle = memory_opt.pools["particles"].acquire()
particle.position = (x, y)
# ... use particle ...
memory_opt.pools["particles"].release(particle)
```

## Security Considerations

### Content Safety

```python
from creative_coding import ContentSafety, SafetyConfig

safety = ContentSafety(
    config=SafetyConfig(
        nsfw_detection=True,
        violence_detection=True,
        confidence_threshold=0.8,
    ),
)

# Check generated content
result = safety.check_frame(frame)
if not result.is_safe:
    print(f"Content flagged: {result.flags}")
```

### Export Security

```python
from creative_coding import ExportSecurity

security = ExportSecurity(
    watermark=True,
    watermark_text="Creative Coding",
    metadata={
        "artist": "Artist Name",
        "license": "CC-BY-NC",
    },
)

# Secure export
security.export_frame(frame, "output/frame.png")
```

## Troubleshooting Guide

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Low FPS** | Jittery animation | Reduce particle count, optimize shaders |
| **Memory leaks** | Growing memory usage | Check object pooling, release resources |
| **Audio sync issues** | Visuals out of sync | Adjust buffer size, check sample rate |
| **Shader errors** | Black screen | Validate GLSL code, check uniforms |
| **Export issues** | Corrupted files | Check format compatibility |
| **Input lag** | Delayed response | Reduce processing complexity |

## API Reference

```python
class Canvas:
    """Main drawing canvas."""
    
    def __init__(self, width: int, height: int, framerate: int = 60):
        """Initialize canvas."""
        
    def fill(self, color: tuple) -> None:
        """Set fill color."""
        
    def rect(self, x: float, y: float, w: float, h: float) -> None:
        """Draw rectangle."""
        
    def ellipse(self, x: float, y: float, w: float, h: float) -> None:
        """Draw ellipse."""

class AnimationSystem:
    """Animation management."""
    
    def create_object(self, name: str, **kwargs) -> AnimObject:
        """Create animatable object."""
        
    def tween(self, obj, property: str, from_val, to_val, duration: float, easing: Easing) -> None:
        """Create tween animation."""

class AudioReactive:
    """Audio analysis for visuals."""
    
    def __init__(self, source: str, fft_size: int = 2048):
        """Initialize audio reactive."""
        
    def analyze(self) -> AudioAnalysis:
        """Analyze audio input."""
```

## Data Models

```python
@dataclass
class Color:
    """Color representation."""
    r: int
    g: int
    b: int
    a: int = 255

@dataclass
class Vector2:
    """2D vector."""
    x: float
    y: float

@dataclass
class Particle:
    """Particle data."""
    position: Vector2
    velocity: Vector2
    color: Color
    size: float
    lifetime: float
    age: float

@dataclass
class AudioAnalysis:
    """Audio analysis result."""
    tempo_bpm: float
    beat_strength: float
    bands: dict
    spectral_centroid: float
```

## Deployment Guide

### Build Configuration

```python
from creative_coding import BuildConfig

config = BuildConfig(
    platforms=["web", "desktop"],
    output_formats=["png", "svg", "mp4", "gif"],
    quality={
        "image": {"dpi": 300},
        "video": {"fps": 30, "codec": "h264"},
    },
)
```

## Monitoring & Observability

```python
from creative_coding import Metrics, HealthCheck

metrics = Metrics(
    tracks=["frame_time", "memory_usage", "particle_count"],
    sample_rate=0.1,
)

health = HealthCheck(
    checks=[
        {"name": "fps", "threshold": 55},
        {"name": "memory_usage_mb", "threshold": 1500},
    ],
)
```

## Testing Strategy

```python
import pytest
from creative_coding import Canvas, AnimationSystem

class TestCanvas:
    def test_canvas_creation(self):
        canvas = Canvas(width=1920, height=1080)
        assert canvas.width == 1920
        assert canvas.height == 1080

class TestAnimation:
    def test_tween(self):
        anim = AnimationSystem()
        obj = anim.create_object("test", x=0)
        anim.tween(obj, "x", 0, 100, duration=1.0)
        assert obj.x == 0
```

## Versioning & Migration

| Version | Changes | Breaking |
|---------|---------|----------|
| 2.0.0 | Added GLSL shaders, improved performance | Yes |
| 1.5.0 | Added audio-reactive visuals | No |
| 1.0.0 | Initial release | N/A |

## Glossary

| Term | Definition |
|------|------------|
| **Easing** | Rate of change over time |
| **Tween** | Animation between two values |
| **FFT** | Fast Fourier Transform |
| **Particle System** | Physics-based particle simulation |
| **Shader** | GPU program for visual effects |
| **Blending Mode** | How colors combine |
| **Frame Rate** | Frames per second |

## Changelog

### 2.0.0 (2024-01-15)
- Added GLSL shader support
- Improved performance
- Added audio-reactive visuals

### 1.5.0 (2023-10-01)
- Added particle system
- Added animation system

### 1.0.0 (2023-06-01)
- Initial release

## Contributing Guidelines

```bash
git clone https://github.com/company/creative-coding.git
cd creative-coding
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
