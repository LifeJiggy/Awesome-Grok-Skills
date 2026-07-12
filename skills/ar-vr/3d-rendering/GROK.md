---
name: "3d-rendering"
category: "ar-vr"
version: "2.0.0"
tags: ["3d-rendering", "gpu", "shaders", "optimization", "real-time", "ray-tracing", "pbr"]
---

# 3D Rendering

## Overview

Real-time 3D rendering optimization toolkit for game engines, XR applications, and interactive visualization. This module covers rendering pipeline optimization, shader management, level-of-detail (LOD) systems, GPU profiling, draw call batching, texture streaming, occlusion culling, and GPU-driven rendering. Supports Unity URP/HDRP, Unreal Engine, and WebGPU with platform-specific optimizations for mobile, desktop, and XR GPUs.

## Core Capabilities

- **Rendering Pipeline**: Configure forward, deferred, and forward+ rendering pipelines with MSAA, FXAA, and temporal anti-aliasing
- **LOD Management**: Automatic LOD generation and switching based on screen coverage and distance
- **Draw Call Optimization**: Static/dynamic batching, GPU instancing, and indirect rendering
- **Texture Management**: Streaming, compression (ASTC, ETC2, BC7), mipmapping, and texture atlasing
- **Shader Optimization**: Shader variant reduction, Uber shader splitting, and warm-up strategies
- **Occlusion Culling**: Hardware and software occlusion culling with hierarchical Z-buffer
- **GPU Profiling**: Frame time analysis, shader complexity, overdraw, and bandwidth profiling
- **Ray Tracing**: Real-time ray-traced reflections, shadows, and global illumination configuration

## Usage

```python
from three_d_rendering import (
    RenderPipeline, LODManager, DrawCallOptimizer, GPUProfiler
)

# Configure rendering pipeline
pipeline = RenderPipeline(
    backend="urp",
    msaa_samples=4,
    hdr=True,
    shadow_resolution=2046,
    render_scale=1.0,
    target_framerate=90,
)
print(f"Pipeline: {pipeline.backend}, MSAA: {pipeline.msaa_samples}x")

# LOD management
lod = LODManager()
lod.add_level("character_high", screen_coverage=0.3, distance_max=10)
lod.add_level("character_med", screen_coverage=0.1, distance_max=30)
lod.add_level("character_low", screen_coverage=0.02, distance_max=100)
lod.add_level("character_cull", screen_coverage=0.0, distance_max=999)
active = lod.get_active_level(screen_coverage=0.15, distance=20)
print(f"Active LOD: {active}")

# Draw call optimization
optimizer = DrawCallOptimizer()
optimizer.batch_static_objects("environment_batch")
optimizer.enable_gpu_instancing("foliage")
stats = optimizer.get_stats()
print(f"Draw calls: {stats['before']} → {stats['after']} ({stats['reduction_pct']:.0f}% reduction)")

# GPU profiling
profiler = GPUProfiler()
frame = profiler.capture_frame()
print(f"\nFrame time: {frame.frame_time_ms:.2f}ms ({frame.fps:.0f} FPS)")
print(f"  GPU: {frame.gpu_time_ms:.2f}ms")
print(f"  CPU: {frame.cpu_time_ms:.2f}ms")
print(f"  Draw calls: {frame.draw_calls}")
print(f"  Triangles: {frame.triangles_rendered:,}")
for pass_info in frame.render_passes:
    print(f"  Pass '{pass_info['name']}': {pass_info['time_ms']:.2f}ms")
```

## Best Practices

- Target 11.1ms frame time for 90fps XR, 16.7ms for 60fps desktop, 33.3ms for 30fps mobile
- Use static batching for non-moving environment geometry — it's free at build time
- Enable GPU instancing for repeated objects (foliage, rocks, particles) with same mesh/material
- Implement LOD with at least 3 levels — high, medium, low — before culling
- Use texture atlasing to reduce material count and draw calls
- Profile before optimizing — most performance issues are in 1-2 specific areas
- Use ASTC texture compression on mobile for best quality/size ratio
- Implement frustum culling as baseline — it's cheap and eliminates 50%+ of objects
- Use occlusion culling for indoor scenes with many occluded objects
- Minimize shader variants — each variant is a separate compiled shader

## Related Modules

- **ar-vr-development** — XR-specific rendering optimizations
- **mixed-reality** — Rendering in passthrough environments
- **spatial-computing** — Spatial data for rendering decisions
- **gesture-recognition** — Rendering interactive gesture feedback
- **art-tech** → **generative-art** — Procedural content generation
