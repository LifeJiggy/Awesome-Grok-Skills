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

- Start with a simple sketch and add complexity incrementally — resist the urge to build everything at once
- Use `randomSeed()` for reproducible randomness in generative compositions
- Save frames as image sequences for lossless recording — encode to video afterward
- Use easing functions for natural-feeling animations instead of linear interpolation
- Design at canvas resolution but think in relative coordinates for scalability
- Use blending modes (ADD, MULTIPLY, SCREEN) for layered visual effects
- Test on different screen sizes — creative code often breaks at non-standard resolutions
- Keep framerate stable by profiling expensive operations and using level-of-detail
- For audio-reactive work, smooth FFT data over 3-5 frames to prevent jittery visuals
- Use GLSL shaders for real-time effects that are too expensive on CPU

## Related Modules

- **generative-art** — Algorithmic art generation techniques
- **audio-visual** — Audio-visual synchronization and performance
- **interactive-media** — Interactive art and experience design
- **3d-rendering** — 3D creative coding and shader programming
- **digital-installations** — Physical installation output
