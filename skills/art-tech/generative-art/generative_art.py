"""
Generative Art Module — Noise generation, L-systems, particle systems, fractals,
shader pipelines, color palettes, and export for algorithmic art creation.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


class NoiseType(Enum):
    PERLIN = "perlin"
    SIMPLEX = "simplex"
    WORLEY = "worley"
    VALUE = "value"


class FractalType(Enum):
    MANDELBROT = "mandelbrot"
    JULIA = "julia"
    SIERPINSKI = "sierpinski"
    KOCH = "koch"
    BURNINGSHIP = "burningship"


class ExportFormat(Enum):
    PNG = "png"
    SVG = "svg"
    PDF = "pdf"
    MP4 = "mp4"
    JSON = "json"


@dataclass
class ColorPalette:
    name: str
    colors: List[Tuple[int, int, int]]
    background: Tuple[int, int, int] = (0, 0, 0)

    def get_color(self, t: float) -> Tuple[int, int, int]:
        t = max(0, min(1, t))
        idx = t * (len(self.colors) - 1)
        i = int(idx)
        frac = idx - i
        c1 = self.colors[min(i, len(self.colors)-1)]
        c2 = self.colors[min(i+1, len(self.colors)-1)]
        return tuple(int(c1[j] + (c2[j] - c1[j]) * frac) for j in range(3))

    @classmethod
    def warm(cls) -> "ColorPalette":
        return cls("warm", [(255, 87, 51), (255, 195, 0), (255, 230, 109)])

    @classmethod
    def ocean(cls) -> "ColorPalette":
        return cls("ocean", [(0, 119, 182), (0, 180, 216), (144, 224, 239)])

    @classmethod
    def sunset(cls) -> "ColorPalette":
        return cls("sunset", [(253, 94, 83), (230, 57, 70), (69, 19, 105)])


@dataclass
class NoiseField:
    width: int
    height: int
    values: List[List[float]]
    min_val: float = 0.0
    max_val: float = 1.0
    seed: int = 0

    def get(self, x: int, y: int) -> float:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.values[y][x]
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {"width": self.width, "height": self.height, "range": f"{self.min_val:.3f}-{self.max_val:.3f}"}


@dataclass
class Particle:
    id: str
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    life: float = 1.0
    decay: float = 0.01
    size: float = 3.0
    color: Tuple[int, int, int] = (255, 255, 255)

    @property
    def alive(self) -> bool:
        return self.life > 0

    def update(self, dt: float, forces: Dict[str, Tuple[float, float]]) -> None:
        for fx, fy in forces.values():
            self.vx += fx * dt
            self.vy += fy * dt
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay * dt
        self.vx *= 0.99
        self.vy *= 0.99


@dataclass
class LSystemResult:
    axiom: str
    derived: str
    iterations: int
    svg_path: str = ""

    @property
    def axiom_length(self) -> int:
        return len(self.axiom)

    def to_dict(self) -> Dict[str, Any]:
        return {"iterations": self.iterations, "derived_length": len(self.derived)}


@dataclass
class FractalResult:
    width: int
    height: int
    center: Tuple[float, float]
    zoom: float
    max_iterations: int
    escape_values: List[List[int]]
    render_time_ms: float = 0.0

    @property
    def max_val(self) -> int:
        return max(max(row) for row in self.escape_values) if self.escape_values else 0

    def to_dict(self) -> Dict[str, Any]:
        return {"width": self.width, "height": self.height, "max_iter": self.max_iterations}


@dataclass
class ShaderUniform:
    name: str
    value: Any
    uniform_type: str = "float"


class NoiseGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        self._perm = list(range(256))
        random.seed(seed)
        random.shuffle(self._perm)
        self._perm *= 2

    def _fade(self, t: float) -> float:
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, a: float, b: float, t: float) -> float:
        return a + t * (b - a)

    def _grad(self, hash_val: int, x: float, y: float) -> float:
        h = hash_val & 3
        u = x if h < 2 else y
        v = y if h < 2 else x
        return (u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v)

    def noise2d(self, x: float, y: float) -> float:
        xi, yi = int(math.floor(x)) & 255, int(math.floor(y)) & 255
        xf, yf = x - math.floor(x), y - math.floor(y)
        u, v = self._fade(xf), self._fade(yf)
        aa = self._perm[self._perm[xi] + yi]
        ab = self._perm[self._perm[xi] + yi + 1]
        ba = self._perm[self._perm[xi + 1] + yi]
        bb = self._perm[self._perm[xi + 1] + yi + 1]
        return self._lerp(
            self._lerp(self._grad(aa, xf, yf), self._grad(ba, xf-1, yf), u),
            self._lerp(self._grad(ab, xf, yf-1), self._grad(bb, xf-1, yf-1), u),
            v,
        )

    def generate_field(self, width: int, height: int, scale: float = 0.01,
                      octaves: int = 4, persistence: float = 0.5) -> NoiseField:
        values = []
        min_v, max_v = float("inf"), float("-inf")
        for y in range(height):
            row = []
            for x in range(width):
                val = 0
                amp = 1.0
                freq = scale
                for _ in range(octaves):
                    val += self.noise2d(x * freq, y * freq) * amp
                    amp *= persistence
                    freq *= 2
                val = (val + 1) / 2
                row.append(val)
                min_v = min(min_v, val)
                max_v = max(max_v, val)
            values.append(row)
        return NoiseField(width=width, height=height, values=values, min_val=min_v, max_val=max_v, seed=self.seed)


class LSystem:
    def __init__(self, axiom: str, rules: Dict[str, str], angle: float = 25, iterations: int = 4):
        self.axiom = axiom
        self.rules = rules
        self.angle = angle
        self.iterations = iterations
        self.derived = self._derive()

    def _derive(self) -> str:
        current = self.axiom
        for _ in range(self.iterations):
            next_str = ""
            for char in current:
                next_str += self.rules.get(char, char)
            current = next_str
        return current

    def generate_svg(self, width: int = 800, height: int = 600) -> str:
        x, y, a = width / 2, height * 0.9, -90
        paths = []
        path_d = f"M{x},{y}"
        stack = []
        step = 5
        for char in self.derived:
            if char == "F":
                rad = math.radians(a)
                x += math.cos(rad) * step
                y += math.sin(rad) * step
                path_d += f"L{x:.1f},{y:.1f}"
            elif char == "+":
                a += self.angle
            elif char == "-":
                a -= self.angle
            elif char == "[":
                stack.append((x, y, a))
            elif char == "]":
                if stack:
                    x, y, a = stack.pop()
                    paths.append(path_d)
                    path_d = f"M{x:.1f},{y:.1f}"
        paths.append(path_d)
        paths_svg = "".join(f'<path d="{p}" stroke="white" fill="none" stroke-width="0.5"/>' for p in paths)
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect fill="black" width="{width}" height="{height}"/>{paths_svg}</svg>'


class ParticleSystem:
    def __init__(self, max_particles: int = 5000, gravity: Tuple[float, float] = (0, 0.01)):
        self.max_particles = max_particles
        self.gravity = gravity
        self._particles: List[Particle] = []
        self._emitters: List[Dict[str, Any]] = []
        self._forces: Dict[str, Tuple[float, float]] = {}

    def add_emitter(self, position: Tuple[float, float], rate: int = 10,
                   color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        self._emitters.append({"position": position, "rate": rate, "color": color})

    def add_force(self, name: str, force: Tuple[float, float]) -> None:
        self._forces[name] = force

    def step(self, dt: float = 0.016) -> None:
        for emitter in self._emitters:
            for _ in range(emitter["rate"]):
                if len(self._particles) < self.max_particles:
                    p = Particle(
                        id=f"P-{uuid.uuid4().hex[:6]}",
                        x=emitter["position"][0] + random.uniform(-5, 5),
                        y=emitter["position"][1],
                        vx=random.uniform(-0.5, 0.5),
                        vy=random.uniform(-2, -0.5),
                        color=emitter["color"],
                    )
                    self._particles.append(p)

        forces = {"gravity": self.gravity, **self._forces}
        for p in self._particles:
            if p.alive:
                p.update(dt, forces)

        self._particles = [p for p in self._particles if p.alive]

    @property
    def active_count(self) -> int:
        return len(self._particles)


class FractalGenerator:
    def __init__(self, type: str = "mandelbrot", width: int = 800, height: int = 600):
        self.type = FractalType(type)
        self.width = width
        self.height = height
        self.max_iterations = 256

    def render(self, center: Tuple[float, float] = (-0.5, 0), zoom: float = 1.0,
              max_iterations: int = 256) -> FractalResult:
        self.max_iterations = max_iterations
        escape = []
        for py in range(self.height):
            row = []
            for px in range(self.width):
                x0 = (px - self.width / 2) / (0.5 * zoom * self.width) + center[0]
                y0 = (py - self.height / 2) / (0.5 * zoom * self.height) + center[1]
                x, y = 0.0, 0.0
                iteration = 0
                while x*x + y*y <= 4 and iteration < max_iterations:
                    xtemp = x*x - y*y + x0
                    y = 2*x*y + y0
                    x = xtemp
                    iteration += 1
                row.append(iteration)
            escape.append(row)
        return FractalResult(
            width=self.width, height=self.height, center=center,
            zoom=zoom, max_iterations=max_iterations, escape_values=escape,
        )


class ShaderPipeline:
    def __init__(self, vertex: str = "", fragment: str = ""):
        self.vertex = vertex
        self.fragment = fragment
        self._uniforms: Dict[str, ShaderUniform] = {}

    def set_uniform(self, name: str, value: Any) -> None:
        self._uniforms[name] = ShaderUniform(name=name, value=value)

    def render(self, width: int = 1920, height: int = 1080) -> Dict[str, Any]:
        return {"width": width, "height": height, "uniforms": len(self._uniforms)}


class ColorPaletteGenerator:
    @staticmethod
    def from_harmony(base_hue: float, count: int = 5, saturation: float = 0.7, lightness: float = 0.5) -> ColorPalette:
        colors = []
        for i in range(count):
            h = (base_hue + i * (360 / count)) % 360
            r, g, b = ColorPaletteGenerator._hsl_to_rgb(h, saturation, lightness)
            colors.append((r, g, b))
        return ColorPalette(name=f"harmony_{base_hue:.0f}", colors=colors)

    @staticmethod
    def _hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
        c = (1 - abs(2*l - 1)) * s
        x = c * (1 - abs((h/60) % 2 - 1))
        m = l - c/2
        if h < 60: r, g, b = c, x, 0
        elif h < 120: r, g, b = x, c, 0
        elif h < 180: r, g, b = 0, c, x
        elif h < 240: r, g, b = 0, x, c
        elif h < 300: r, g, b = x, 0, c
        else: r, g, b = c, 0, x
        return (int((r+m)*255), int((g+m)*255), int((b+m)*255))

    @staticmethod
    def extract_palette(image_data: Any, n_colors: int = 5) -> ColorPalette:
        return ColorPalette(name="extracted", colors=[(random.randint(0,255), random.randint(0,255), random.randint(0,255)) for _ in range(n_colors)])


def main():
    print("Generative Art Toolkit")
    print("=" * 60)

    noise = NoiseGenerator(seed=42)
    field = noise.generate_field(100, 100, scale=0.05, octaves=4)
    print(f"Noise field: {field.to_dict()}")

    lsys = LSystem(axiom="F", rules={"F": "FF+[+F-F-F]-[-F+F+F]"}, angle=25, iterations=4)
    svg = lsys.generate_svg(400, 400)
    print(f"L-System: {lsys.iterations} iterations, derived length: {len(lsys.derived)}")

    ps = ParticleSystem(max_particles=1000)
    ps.add_emitter(position=(200, 300), rate=20, color=(255, 100, 50))
    ps.add_force("wind", (0.02, 0))
    for _ in range(60):
        ps.step(0.016)
    print(f"Particles: {ps.active_count} active")

    frac = FractalGenerator(type="mandelbrot", width=200, height=150)
    result = frac.render(center=(-0.5, 0), zoom=1.0, max_iterations=64)
    print(f"Fractal: {result.to_dict()}")

    palette = ColorPaletteGenerator.from_harmony(200, count=5)
    print(f"Palette: {palette.name}, colors: {palette.colors}")

    shader = ShaderPipeline(fragment="warp.frag")
    shader.set_uniform("u_time", 1.5)
    shader.set_uniform("u_resolution", (1920, 1080))
    out = shader.render()
    print(f"Shader: {out}")


if __name__ == "__main__":
    main()
