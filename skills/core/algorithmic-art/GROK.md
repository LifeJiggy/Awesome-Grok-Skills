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

---

## Advanced Configuration

### Resolution and Quality Settings

Configure art generation quality parameters.

```python
art_config = ArtConfig(
    resolution={"width": 1920, "height": 1080, "dpi": 300},
    anti_aliasing=True,
    supersampling=4,  # 4x supersampling for smoother edges
    color_depth=24,  # RGB
    output_formats=["png", "svg", "pdf"],
)
```

### Color Palette Configuration

Define color palettes for art generation.

```python
palettes = ColorPalettes(
    palettes={
        "sunset": ["#FF6B6B", "#FFE66D", "#4ECDC4", "#1A535C"],
        "neon": ["#FF00FF", "#00FFFF", "#FFFF00", "#FF0080"],
        "nature": ["#2D5016", "#8B4513", "#87CEEB", "#FFD700"],
    },
    default_palette="sunset",
)
```

### Animation Settings

Configure animation parameters.

```python
animation_config = AnimationConfig(
    fps=30,
    duration_seconds=10,
    easing_functions=["ease_in_out", "elastic", "bounce"],
    output_format="gif",
)
```

---

## Architecture Patterns

### Fractal Rendering Pipeline

```python
class FractalPipeline:
    def __init__(self):
        self.stages = [
            CoordinateMapping(),
            IterationComputation(),
            ColorMapping(),
            AntiAliasing(),
        ]

    def render(self, fractal_type, params):
        data = self.initialize_grid(params)
        for stage in self.stages:
            data = stage.process(data)
        return data
```

### Procedural Generation Pattern

```python
class ProceduralGenerator:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.noise = PerlinNoise(seed=seed)

    def generate(self, pattern_type, params):
        return self.patterns[pattern_type](params)
```

### Animation Pipeline

```python
class AnimationPipeline:
    def __init__(self):
        self.frames = []

    def add_keyframe(self, time, state):
        self.frames.append(Keyframe(time, state))

    def interpolate(self, fps):
        frames = []
        for t in np.arange(0, self.duration, 1/fps):
            state = self.interpolate_state(t)
            frames.append(self.render_frame(state))
        return frames
```

---

## Integration Guide

### Matplotlib Integration

```python
import matplotlib.pyplot as plt

def render_fractal_mandelbrot(data):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(data, cmap='viridis')
    ax.set_title('Mandelbrot Set')
    plt.savefig('mandelbrot.png', dpi=300)
```

### Pillow Integration

```python
from PIL import Image

def create_art_image(data, palette):
    img = Image.new('RGB', (data.shape[1], data.shape[0]))
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            color = palette[int(data[y, x]) % len(palette)]
            img.putpixel((x, y), color)
    return img
```

### SVG Generation

```python
def generate_svg(pattern, width, height):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
    for element in pattern.elements:
        svg += element.to_svg()
    svg += '</svg>'
    return svg
```

---

## Performance Optimization

### GPU Acceleration

```python
# Use Numba for GPU acceleration
from numba import cuda

@cuda.jit
def mandelbrot_kernel(data, max_iter):
    x, y = cuda.grid(2)
    if x < data.shape[0] and y < data.shape[1]:
        c = complex(x / data.shape[0] * 3.5 - 2.5, y / data.shape[1] * 2.0 - 1.0)
        z = 0
        for i in range(max_iter):
            z = z * z + c
            if abs(z) > 2:
                data[x, y] = i
                break
```

### Parallel Rendering

```python
from concurrent.futures import ProcessPoolExecutor

def parallel_render(patterns, num_workers=4):
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(render_pattern, p) for p in patterns]
        return [f.result() for f in futures]
```

---

## Security Considerations

### Resource Limits

```python
# Prevent resource exhaustion
limiter = ResourceLimiter(
    max_memory_mb=1024,
    max_cpu_seconds=300,
    max_output_size_mb=100,
)
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Art looks jagged | No anti-aliasing | Enable supersampling |
| Colors look wrong | Wrong palette mapping | Check color mapping |
| Animation stuttering | Low FPS | Increase FPS or reduce complexity |
| Out of memory | High resolution | Reduce resolution or use tiling |

---

## API Reference

### FractalGenerator

```python
class FractalGenerator:
    def mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter) -> np.ndarray
    def julia(width, height, c, max_iter) -> np.ndarray
    def sierpinski(order) -> ArtResult
    def koch(order) -> ArtResult
```

### PatternCreator

```python
class PatternCreator:
    def voronoi(width, height, num_points, colors) -> ArtResult
    def delaunay(points, colors) -> ArtResult
    def tessellation(pattern_type, params) -> ArtResult
```

### NoiseGenerator

```python
class NoiseGenerator:
    def generate_perlin(width, height, scale) -> NoiseField
    def generate_simplex(width, height, scale) -> NoiseField
    def generate_fractal(width, height, octaves) -> NoiseField
```

---

## Data Models

### ArtResult

```python
@dataclass
class ArtResult:
    data: np.ndarray
    width: int
    height: int
    pattern_type: str
    render_time_ms: float
    metadata: dict
```

### NoiseField

```python
@dataclass
class NoiseField:
    data: np.ndarray
    width: int
    height: int
    min_value: float
    max_value: float
    scale: float
```

---

## Deployment Guide

### Art Generation Service

```yaml
services:
  art-service:
    image: algorithmic-art:latest
    ports:
      - "8080:8080"
    environment:
      - MAX_RESOLUTION=4096x2160
      - GPU_ENABLED=true
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `art.render.time` | Render time per image | > 10s |
| `art.memory.peak` | Peak memory usage | > 1GB |
| `art.gpu.utilization` | GPU utilization | < 50% |

---

## Testing Strategy

### Art Tests

```python
def test_fractal_generation():
    gen = FractalGenerator()
    result = gen.mandelbrot(100, 100, -2.0, 1.0, -1.5, 1.5, 100)
    assert result.shape == (100, 100)
    assert result.max() > 0
```

---

## Versioning & Migration

### Art Versioning

Track art generation parameters for reproducibility.

---

## Advanced Configuration (Extended)

### Resolution and Quality Settings

Configure art generation quality parameters.

```python
art_config = ArtConfig(
    resolution={"width": 1920, "height": 1080, "dpi": 300},
    anti_aliasing=True,
    supersampling=4,
    color_depth=24,
    output_formats=["png", "svg", "pdf", "gif"],
    max_iterations=1000,
    escape_radius=2.0,
)
```

### Color Palette Configuration

Define color palettes for art generation.

```python
palettes = ColorPalettes(
    palettes={
        "sunset": ["#FF6B6B", "#FFE66D", "#4ECDC4", "#1A535C"],
        "neon": ["#FF00FF", "#00FFFF", "#FFFF00", "#FF0080"],
        "nature": ["#2D5016", "#8B4513", "#87CEEB", "#FFD700"],
        "ocean": ["#006994", "#0099CC", "#66CCFF", "#FFFFFF"],
        "fire": ["#FF0000", "#FF6600", "#FFCC00", "#FFFF00"],
        "pastel": ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9"],
    },
    default_palette="sunset",
    interpolation="linear",
)
```

### Animation Settings

Configure animation parameters.

```python
animation_config = AnimationConfig(
    fps=30,
    duration_seconds=10,
    easing_functions=["ease_in_out", "elastic", "bounce", "linear"],
    output_format="gif",
    loop=True,
    optimize_gif=True,
)
```

---

## Architecture Patterns (Extended)

### Fractal Rendering Pipeline

```python
class FractalPipeline:
    def __init__(self):
        self.stages = [
            CoordinateMapping(),
            IterationComputation(),
            ColorMapping(),
            AntiAliasing(),
            PostProcessing(),
        ]

    def render(self, fractal_type, params):
        data = self.initialize_grid(params)
        for stage in self.stages:
            data = stage.process(data)
        return data

    def render_parallel(self, fractal_type, params, n_workers=4):
        chunks = self.split_grid(params, n_workers)
        with ProcessPoolExecutor(n_workers) as executor:
            results = [executor.submit(self.render_chunk, fractal_type, chunk) for chunk in chunks]
            return self.merge_chunks([r.result() for r in results])
```

### Procedural Generation Pattern

```python
class ProceduralGenerator:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.noise = PerlinNoise(seed=seed)

    def generate(self, pattern_type, params):
        pattern = self.patterns[pattern_type]
        return pattern.generate(self.rng, self.noise, params)

    def generate_batch(self, pattern_type, params, count):
        return [self.generate(pattern_type, params) for _ in range(count)]
```

### Animation Pipeline

```python
class AnimationPipeline:
    def __init__(self):
        self.frames = []
        self.keyframes = []

    def add_keyframe(self, time, state):
        self.keyframes.append(Keyframe(time, state))

    def interpolate(self, fps):
        frames = []
        duration = self.keyframes[-1].time - self.keyframes[0].time
        for t in np.arange(0, duration, 1/fps):
            state = self.interpolate_state(t)
            frames.append(self.render_frame(state))
        return frames

    def export(self, frames, output_path, format="gif"):
        if format == "gif":
            self.export_gif(frames, output_path)
        elif format == "mp4":
            self.export_mp4(frames, output_path)
```

### Pattern Composition

```python
class PatternComposer:
    def __init__(self):
        self.patterns = []

    def add_pattern(self, pattern, position=(0, 0), scale=1.0, opacity=1.0):
        self.patterns.append({
            'pattern': pattern,
            'position': position,
            'scale': scale,
            'opacity': opacity,
        })

    def compose(self):
        canvas = np.zeros((self.height, self.width, 3))
        for p in self.patterns:
            pattern_data = p['pattern'].generate()
            canvas = self.overlay(canvas, pattern_data, p['position'], p['scale'], p['opacity'])
        return canvas
```

---

## Integration Guide (Extended)

### Matplotlib Integration

```python
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def render_fractal_mandelbrot(data, palette='viridis'):
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(data, cmap=palette, extent=[-2.5, 1.0, -1.5, 1.5])
    ax.set_title('Mandelbrot Set', fontsize=16)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    plt.colorbar(im, ax=ax, label='Iteration Count')
    plt.savefig('mandelbrot.png', dpi=300, bbox_inches='tight')
    plt.close()
```

### Pillow Integration

```python
from PIL import Image, ImageDraw, ImageFont

def create_art_image(data, palette, width=800, height=600):
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        for x in range(width):
            color_idx = int(data[y, x]) % len(palette)
            color = palette[color_idx]
            draw.point((x, y), fill=color)
    
    return img
```

### SVG Generation

```python
def generate_svg_pattern(pattern, width=800, height=600):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
    svg += f'<rect width="{width}" height="{height}" fill="black"/>'
    
    for element in pattern.elements:
        svg += element.to_svg()
    
    svg += '</svg>'
    return svg
```

### Three.js Integration

```python
# Generate Three.js scene for 3D fractals
def generate_threejs_scene(fractal_data):
    scene = {
        'geometry': fractal_data.to_bufferGeometry(),
        'material': {
            'type': 'MeshBasicMaterial',
            'vertexColors': True,
        },
        'camera': {'position': [0, 0, 5], 'fov': 75},
    }
    return json.dumps(scene)
```

---

## Performance Optimization (Extended)

### GPU Acceleration

```python
# Use Numba for GPU acceleration
from numba import cuda
import numpy as np

@cuda.jit
def mandelbrot_kernel(data, max_iter, width, height):
    x, y = cuda.grid(2)
    if x < width and y < height:
        c_real = (x - width/2.0) * 4.0 / width
        c_imag = (y - height/2.0) * 4.0 / height
        z_real = 0.0
        z_imag = 0.0
        
        for i in range(max_iter):
            z_real_new = z_real * z_real - z_imag * z_imag + c_real
            z_imag = 2.0 * z_real * z_imag + c_imag
            z_real = z_real_new
            
            if z_real * z_real + z_imag * z_imag > 4.0:
                data[y, x] = i
                return
        data[y, x] = max_iter

# Launch kernel
data = np.zeros((height, width), dtype=np.int32)
threadsperblock = (16, 16)
blockspergrid_x = int(np.ceil(width / threadsperblock[0]))
blockspergrid_y = int(np.ceil(height / threadsperblock[1]))
blockspergrid = (blockspergrid_x, blockspergrid_y)

mandelbrot_kernel[blockspergrid, threadsperblock](data, 100, width, height)
```

### Parallel Rendering

```python
from concurrent.futures import ProcessPoolExecutor
import numpy as np

def parallel_render(patterns, num_workers=4):
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(render_pattern, p) for p in patterns]
        return [f.result() for f in futures]

def render_pattern(pattern):
    data = np.zeros((pattern.height, pattern.width))
    for y in range(pattern.height):
        for x in range(pattern.width):
            data[y, x] = pattern.compute(x, y)
    return data
```

### Caching

```python
class ArtCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            # LRU eviction
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        self.cache[key] = {'value': value, 'timestamp': time.time()}
```

---

## Security Considerations (Extended)

### Resource Limits

```python
class ResourceLimiter:
    def __init__(self, max_memory_mb=1024, max_cpu_seconds=300, max_output_mb=100):
        self.max_memory = max_memory_mb * 1024 * 1024
        self.max_cpu = max_cpu_seconds
        self.max_output = max_output_mb * 1024 * 1024

    def check_resources(self):
        import psutil
        process = psutil.Process()
        
        if process.memory_info().rss > self.max_memory:
            raise ResourceExhausted("Memory limit exceeded")
        
        cpu_time = process.cpu_times().user
        if cpu_time > self.max_cpu:
            raise ResourceExhausted("CPU time limit exceeded")
```

### Input Validation

```python
class InputValidator:
    def validate_dimensions(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive")
        if width > 10000 or height > 10000:
            raise ValueError("Dimensions too large")
        return True

    def validate_iterations(self, max_iter):
        if max_iter <= 0:
            raise ValueError("Iterations must be positive")
        if max_iter > 10000:
            raise ValueError("Too many iterations")
        return True
```

---

## Troubleshooting Guide (Extended)

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Art looks jagged | No anti-aliasing | Enable supersampling |
| Colors look wrong | Wrong palette mapping | Check color mapping |
| Animation stuttering | Low FPS | Increase FPS or reduce complexity |
| Out of memory | High resolution | Reduce resolution or use tiling |
| Render slow | No parallelization | Use parallel rendering |
| Export failed | Unsupported format | Check output format |

### Debug Mode

```python
class ArtDebugger:
    def debug_fractal(self, fractal_type, params):
        print(f"Fractal: {fractal_type}")
        print(f"Parameters: {params}")
        
        # Time each stage
        for stage in self.pipeline.stages:
            start = time.time()
            result = stage.process(params)
            elapsed = time.time() - start
            print(f"  {stage.name}: {elapsed:.3f}s")
        
        return result
```

---

## API Reference (Extended)

### FractalGenerator (Extended)

```python
class FractalGenerator:
    def mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter) -> np.ndarray
    def julia(width, height, c, max_iter) -> np.ndarray
    def burning_ship(width, height, max_iter) -> np.ndarray
    def sierpinski(order) -> ArtResult
    def koch(order) -> ArtResult
    def l_system(axiom, rules, iterations) -> ArtResult
    def generate_batch(fractal_type, params_list) -> List[ArtResult]
```

### PatternCreator (Extended)

```python
class PatternCreator:
    def voronoi(width, height, num_points, colors) -> ArtResult
    def delaunay(points, colors) -> ArtResult
    def tessellation(pattern_type, params) -> ArtResult
    def penrose_tiling(order) -> ArtResult
    def quasicrystal(width, height, symmetry) -> ArtResult
    def generate_variations(base_pattern, n_variations) -> List[ArtResult]
```

### NoiseGenerator (Extended)

```python
class NoiseGenerator:
    def generate_perlin(width, height, scale) -> NoiseField
    def generate_simplex(width, height, scale) -> NoiseField
    def generate_fractal(width, height, octaves) -> NoiseField
    def generate_turbulence(width, height, octaves) -> NoiseField
    def generate_worley(width, height, cell_size) -> NoiseField
    def combine(noise_fields, blend_mode) -> NoiseField
```

### MathematicalCurves (Extended)

```python
class MathematicalCurves:
    def rose_curve(k, d, resolution) -> Curve
    def lissajous(a, b, delta, resolution) -> Curve
    def butterfly(resolution) -> Curve
    def spirograph(R, r, d, resolution) -> Curve
    def parametric_3d(func, t_range, resolution) -> Curve3D
```

---

## Data Models (Extended)

### ArtResult

```python
@dataclass
class ArtResult:
    data: np.ndarray
    width: int
    height: int
    pattern_type: str
    render_time_ms: float
    metadata: dict
    color_palette: Optional[List[str]]
    iterations_used: int
    memory_used_bytes: int
```

### NoiseField

```python
@dataclass
class NoiseField:
    data: np.ndarray
    width: int
    height: int
    min_value: float
    max_value: float
    scale: float
    octaves: int
    noise_type: str
```

### Curve

```python
@dataclass
class Curve:
    points: np.ndarray
    num_points: int
    parameters: dict
    bounds: Tuple[float, float, float, float]
    length: float
    curvature: Optional[np.ndarray]
```

### AnimationFrame

```python
@dataclass
class AnimationFrame:
    frame_number: int
    timestamp: float
    data: np.ndarray
    state: dict
    render_time_ms: float
```

---

## Deployment Guide (Extended)

### Art Generation Service

```yaml
services:
  art-service:
    image: algorithmic-art:latest
    ports:
      - "8080:8080"
    environment:
      - MAX_RESOLUTION=4096x2160
      - GPU_ENABLED=true
      - CACHE_ENABLED=true
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - ./output:/output
      - ./cache:/cache
```

### Batch Processing Service

```python
class BatchArtProcessor:
    def __init__(self):
        self.queue = Queue()
        self.workers = []

    def submit(self, job):
        self.queue.put(job)

    def process_batch(self, batch_size=10):
        jobs = []
        for _ in range(batch_size):
            if not self.queue.empty():
                jobs.append(self.queue.get())
        
        with ProcessPoolExecutor() as executor:
            results = [executor.submit(self.process_job, job) for job in jobs]
            return [r.result() for r in results]
```

---

## Monitoring & Observability (Extended)

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `art.render.time` | Render time per image | > 10s |
| `art.memory.peak` | Peak memory usage | > 1GB |
| `art.gpu.utilization` | GPU utilization | < 50% |
| `art.cache.hit_rate` | Cache hit rate | < 0.8 |
| `art.export.size` | Export file size | > 10MB |

### Prometheus Metrics

```python
from prometheus_client import Histogram, Counter, Gauge

RENDER_TIME = Histogram('art_render_seconds', 'Art render time', ['fractal_type'])
RENDER_COUNT = Counter('art_renders_total', 'Total renders', ['fractal_type', 'status'])
MEMORY_USAGE = Gauge('art_memory_bytes', 'Memory usage')
GPU_UTILIZATION = Gauge('art_gpu_utilization', 'GPU utilization')
```

---

## Testing Strategy (Extended)

### Art Tests

```python
def test_fractal_generation():
    gen = FractalGenerator()
    result = gen.mandelbrot(100, 100, -2.0, 1.0, -1.5, 1.5, 100)
    assert result.shape == (100, 100)
    assert result.max() > 0

def test_noise_generation():
    noise = NoiseGenerator(scale=0.05)
    field = noise.generate_perlin(100, 100)
    assert field.width == 100
    assert field.height == 100
    assert 0 <= field.min_value <= field.max_value <= 1

def test_pattern_rendering():
    creator = PatternCreator()
    voronoi = creator.voronoi(800, 600, 50, "rainbow")
    assert voronoi.width == 800
    assert voronoi.height == 600
    assert voronoi.num_regions == 50
```

---

## Versioning & Migration (Extended)

### Art Versioning

Track art generation parameters for reproducibility.

```python
class ArtVersioner:
    def __init__(self):
        self.versions = {}

    def save_version(self, art_result, params):
        version_id = str(uuid.uuid4())
        self.versions[version_id] = {
            'timestamp': time.time(),
            'params': params,
            'metadata': art_result.metadata,
        }
        return version_id

    def recreate(self, version_id):
        version = self.versions[version_id]
        return self.generate(version['params'])
```

### Parameter Migration

```python
def migrate_params(old_params, from_version, to_version):
    """Migrate parameters between versions."""
    if from_version == "1.0" and to_version == "2.0":
        # Add new required parameters
        new_params = old_params.copy()
        new_params['supersampling'] = 1
        new_params['anti_aliasing'] = False
        return new_params
    return old_params
```

---

## Glossary (Extended)

| Term | Definition |
|------|-----------|
| **Mandelbrot Set** | Classic fractal defined by z = z^2 + c |
| **Julia Set** | Related fractal with different parameter |
| **Perlin Noise** | Gradient noise for organic textures |
| **Voronoi** | Partitioning of space into regions |
| **Cellular Automaton** | Grid of cells with simple rules |
| **L-System** | Grammar system for modeling plant growth |
| **Spirograph** | Mathematical curve from rolling circles |
| **Tessellation** | Tiling of a plane using shapes |
| **Supersampling** | Anti-aliasing by rendering at higher resolution |
| **Fractal Dimension** | Measure of fractal complexity |

---

## Changelog

### v2.0.0
- Added GPU acceleration
- Animation support
- SVG output

### v1.0.0
- Initial release with fractal generation

---

## Contributing Guidelines

- Document all parameters for reproducibility
- Use high-quality color palettes
- Optimize for both quality and performance

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
