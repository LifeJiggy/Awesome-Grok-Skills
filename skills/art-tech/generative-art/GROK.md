---
name: "generative-art"
category: "art-tech"
version: "2.0.0"
tags: ["generative-art", "creative-coding", "procedural", "algorithmic", "glsl", "p5", "processing"]
---

# Generative Art

## Overview

Algorithmic and procedural art creation toolkit for producing visual art through code. This module provides creative coding frameworks, shader programming (GLSL/HLSL), noise-based generation, L-systems, cellular automata, particle systems, fractal generators, and output formats for print, web, and NFT minting. Supports p5.js, Processing, TouchDesigner, and custom GLSL shaders with real-time preview and high-resolution export.

## Core Capabilities

- **Noise Generation**: Perlin, Simplex, Worley, and Domain Warping noise with configurable octaves and seed control
- **L-Systems**: Grammar-based procedural generation for plant-like structures, fractals, and decorative patterns
- **Cellular Automata**: Conway's Game of Life, Wireworld, and custom rules for emergent pattern generation
- **Particle Systems**: Physics-based particle emitters with forces, attractors, and flocking behavior
- **Fractal Generators**: Mandelbrot, Julia, Sierpinski, Koch, and custom IFS fractals
- **Shader Programming**: GLSL fragment/vertex shaders with real-time preview and export
- **Color Palettes**: Algorithmic color harmony, palette extraction, and color field generation
- **Export**: High-resolution PNG, SVG, PDF, video (MP4/WebM), and NFT metadata generation

## Usage

```python
from generative_art import (
    NoiseGenerator, LSystem, ParticleSystem, FractalGenerator, ShaderPipeline
)

# Perlin noise field
noise = NoiseGenerator(seed=42)
field = noise.generate_field(width=800, height=600, scale=0.01, octaves=6, persistence=0.5)
print(f"Noise field: {field.width}x{field.height}, range: {field.min_val:.3f}-{field.max_val:.3f}")

# L-System tree
lsystem = LSystem(
    axiom="F",
    rules={"F": "FF+[+F-F-F]-[-F+F+F]"},
    angle=25,
    iterations=5,
)
svg = lsystem.generate_svg(width=800, height=600)
print(f"L-System: {lsystem axiom_length} axiom length, {len(lsystem.derived)} derived")

# Particle system
particles = ParticleSystem(max_particles=5000, gravity=(0, -0.01))
particles.add_emitter(position=(400, 500), rate=50, color=(255, 100, 50))
particles.add_force("wind", (0.02, 0))
particles.step(dt=0.016)
print(f"Active particles: {particles.active_count}")

# Mandelbrot fractal
fractal = FractalGenerator(type="mandelbrot", width=1920, height=1080)
image = fractal.render(center=(-0.5, 0), zoom=1.0, max_iterations=256)
print(f"Fractal: {image.width}x{image.height}, {fractal.max_iterations} iterations")

# GLSL shader
shader = ShaderPipeline(vertex="passthrough.vert", fragment="warp.frag")
shader.set_uniform("u_time", 0.0)
shader.set_uniform("u_resolution", (1920, 1080))
frame = shader.render()
print(f"Shader output: {frame.width}x{frame.height}")
```

## Best Practices

- Use seeds for reproducibility — every generative piece should be reproducible
- Start with simple parameters and gradually increase complexity
- Use domain warping on noise for organic, non-repetitive patterns
- Limit particle counts based on target frame rate — 5000 is comfortable for 60fps
- Use time-based animation loops for smooth, continuous generative art
- Export high-resolution versions for print (300 DPI minimum)
- Document all parameters and seeds for each piece
- Use color palettes with 3-5 colors maximum for cohesive compositions
- Test shader performance on target hardware before final export
- Use SVG export for scalable, resolution-independent generative graphics

## Related Modules

- **digital-installations** — Physical installation output from generative systems
- **creative-coding** — Broader creative coding workflows
- **audio-visual** — Generative visuals driven by audio input
- **interactive-media** — Interactive generative art experiences
- **3d-rendering** — 3D generative art and shader programming
