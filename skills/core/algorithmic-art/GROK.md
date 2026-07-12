---
name: "algorithmic-art"
category: "core"
version: "2.0.0"
tags: ["core", "algorithmic-art", "generative-art", "creative-coding", "visualization"]
---

# Algorithmic Art

## Overview

The Algorithmic Art module provides tools and techniques for creating visual art through algorithms, mathematical functions, and programmatic generation. It covers fractal generation, procedural patterns, cellular automata, generative design, and data-driven art. The module supports both static image generation and animated visualizations.

This skill is useful for creative coders, data visualization artists, educators teaching math through art, and developers building generative design systems.

## Core Capabilities

- **Fractal Generation**: Mandelbrot set, Julia set, Sierpinski triangle, Koch snowflake, and L-systems
- **Procedural Patterns**: Penrose tiles, Voronoi diagrams, Delaunay triangulation, and tessellations
- **Cellular Automata**: Game of Life, Rule 30, Wolfram's elementary CA, and multi-state automata
- **Generative Design**: Genetic algorithms for visual evolution, style transfer, and composition
- **Mathematical Art**: Parametric curves (rose, Lissajous, butterfly), spirographs, and chaos theory
- **Data Visualization Art**: Turning datasets into artistic visualizations
- **Noise Generation**: Perlin noise, simplex noise, and fractal noise for organic textures
- **Animation**: Time-based generative art and procedural animation

## Usage Examples

```python
from algorithmic_art import (
    FractalGenerator,
    PatternCreator,
    CellularAutomaton,
    MathematicalCurves,
    NoiseGenerator,
)

# --- Fractal Generation ---
fractal = FractalGenerator()
mandelbrot = fractal.mandelbrot(
    width=800, height=600,
    x_min=-2.0, x_max=1.0,
    y_min=-1.5, y_max=1.5,
    max_iter=100,
)
print(f"Mandelbrot: {mandelbrot.width}x{mandelbrot.height}")
print(f"Pixels computed: {mandelbrot.total_pixels}")

# --- Sierpinski Triangle ---
sierpinski = fractal.sierpinski(order=6)
print(f"Sierpinski: {sierpinski.width}x{sierpinski.height}")
print(f"Triangles: {sierpinski.num_elements}")

# --- Voronoi Diagram ---
creator = PatternCreator()
voronoi = creator.voronoi(
    width=800, height=600,
    num_points=50,
    colors="rainbow",
)
print(f"Voronoi regions: {voronoi.num_regions}")

# --- Cellular Automaton ---
ca = CellularAutomaton(rule=30, width=100, generations=50)
evolution = ca.evolve()
print(f"Rule 30 evolution: {evolution.generations} generations")
print(f"Pattern: {evolution.pattern_type}")

# --- Mathematical Curves ---
curves = MathematicalCurves()
rose = curves.rose_curve(k=7, d=3, resolution=1000)
print(f"Rose curve: {rose.num_points} points")

lissajous = curves.lissajous(a=3, b=2, delta=3.14/2, resolution=1000)
print(f"Lissajous: {lissajous.num_points} points")

# --- Noise Generation ---
noise = NoiseGenerator(scale=0.05)
field = noise.generate_perlin(width=100, height=100)
print(f"Noise field: {field.width}x{field.height}")
print(f"Value range: {field.min_value:.3f} to {field.max_value:.3f}")
```

## Best Practices

- Use high iteration counts for smooth fractal rendering (100+ for Mandelbrot)
- Apply color mapping carefully — viridis and plasma are perceptually uniform
- Use noise functions for organic, natural-looking textures
- Combine multiple techniques (fractals + noise + color mapping) for richer art
- Use anti-aliasing (supersampling) for smoother renders
- Explore parameter spaces systematically — small changes can produce dramatically different results
- Use symmetry and repetition to create visually appealing compositions
- Generate at higher resolution than needed for crisp output
- Use animation to reveal the time dimension of generative art
- Document all parameters for reproducibility of artistic results

## Related Modules

- **efficient-code**: Efficient implementations of algorithms
- **code-golf**: Minimal code for artistic algorithms
- **meme-code-hybrids**: Fun with creative code
- **performance-tuning**: Optimizing art generation performance
