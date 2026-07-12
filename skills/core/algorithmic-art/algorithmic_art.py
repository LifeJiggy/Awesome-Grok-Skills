"""
Algorithmic Art Module
Fractals, patterns, cellular automata, mathematical curves, and noise generation.
"""

from __future__ import annotations

import cmath
import math
import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Canvas:
    """Art canvas."""
    width: int = 800
    height: int = 600
    pixels: List[List[int]] = field(default_factory=list)
    total_pixels: int = 0
    num_elements: int = 0

    def __post_init__(self):
        if not self.pixels:
            self.pixels = [[0] * self.width for _ in range(self.height)]
        self.total_pixels = self.width * self.height


@dataclass
class FractalResult:
    """Fractal generation result."""
    width: int
    height: int
    total_pixels: int
    num_iterations: int = 0
    escape_values: List[List[int]] = field(default_factory=list)


@dataclass
class PatternResult:
    """Pattern generation result."""
    width: int
    height: int
    num_regions: int = 0
    num_points: int = 0
    points: List[Tuple[float, float]] = field(default_factory=list)


@dataclass
class CAEvolution:
    """Cellular automaton evolution."""
    rule: int
    width: int
    generations: int
    pattern_type: str = ""
    history: List[List[int]] = field(default_factory=list)
    density: float = 0.0


@dataclass
class CurveResult:
    """Mathematical curve result."""
    name: str
    num_points: int
    points: List[Tuple[float, float]] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NoiseField:
    """Noise generation result."""
    width: int
    height: int
    min_value: float = 0.0
    max_value: float = 1.0
    values: List[List[float]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Fractal Generator
# ---------------------------------------------------------------------------

class FractalGenerator:
    """Generate fractal art."""

    def mandelbrot(
        self,
        width: int = 800,
        height: int = 600,
        x_min: float = -2.0,
        x_max: float = 1.0,
        y_min: float = -1.5,
        y_max: float = 1.5,
        max_iter: int = 100,
    ) -> FractalResult:
        escape: List[List[int]] = []
        for py in range(height):
            row: List[int] = []
            for px in range(width):
                x = x_min + (x_max - x_min) * px / width
                y = y_min + (y_max - y_min) * py / height
                c = complex(x, y)
                z = 0 + 0j
                iteration = 0
                while abs(z) <= 2 and iteration < max_iter:
                    z = z * z + c
                    iteration += 1
                row.append(iteration)
            escape.append(row)
        return FractalResult(
            width=width, height=height,
            total_pixels=width * height,
            num_iterations=max_iter,
            escape_values=escape,
        )

    def julia(
        self,
        width: int = 800,
        height: int = 600,
        c: complex = -0.7 + 0.27015j,
        max_iter: int = 100,
    ) -> FractalResult:
        escape: List[List[int]] = []
        for py in range(height):
            row: List[int] = []
            for px in range(width):
                x = -1.5 + 3.0 * px / width
                y = -1.5 + 3.0 * py / height
                z = complex(x, y)
                iteration = 0
                while abs(z) <= 2 and iteration < max_iter:
                    z = z * z + c
                    iteration += 1
                row.append(iteration)
            escape.append(row)
        return FractalResult(width=width, height=height, total_pixels=width * height, num_iterations=max_iter, escape_values=escape)

    def sierpinski(self, order: int = 5) -> Canvas:
        size = 2 ** order
        grid = [[0] * size for _ in range(size)]
        count = 0
        for y in range(size):
            for x in range(size):
                if (x & y) == 0:
                    grid[y][x] = 1
                    count += 1
        return Canvas(width=size, height=size, pixels=grid, num_elements=count)

    def koch_snowflake(self, order: int = 4) -> CurveResult:
        points: List[Tuple[float, float]] = []
        side_length = 400
        height_tri = side_length * math.sqrt(3) / 2
        p1 = (200, 300 + height_tri / 3)
        p2 = (600, 300 + height_tri / 3)
        p3 = (400, 300 - height_tri * 2 / 3)
        points.extend(self._koch_line(p1, p2, order))
        points.extend(self._koch_line(p2, p3, order))
        points.extend(self._koch_line(p3, p1, order))
        return CurveResult(name="Koch Snowflake", num_points=len(points), points=points)

    def _koch_line(
        self, p1: Tuple[float, float], p2: Tuple[float, float], depth: int
    ) -> List[Tuple[float, float]]:
        if depth == 0:
            return [p1, p2]
        dx = (p2[0] - p1[0]) / 3
        dy = (p2[1] - p1[1]) / 3
        a = (p1[0] + dx, p1[1] + dy)
        b = (p2[0] - dx, p2[1] - dy)
        angle = -math.pi / 3
        peak = (
            a[0] + dx * math.cos(angle) - dy * math.sin(angle),
            a[1] + dx * math.sin(angle) + dy * math.cos(angle),
        )
        points = self._koch_line(p1, a, depth - 1)
        points.extend(self._koch_line(a, peak, depth - 1))
        points.extend(self._koch_line(peak, b, depth - 1))
        points.extend(self._koch_line(b, p2, depth - 1))
        return points


# ---------------------------------------------------------------------------
# Pattern Creator
# ---------------------------------------------------------------------------

class PatternCreator:
    """Create geometric patterns."""

    def voronoi(
        self,
        width: int = 800,
        height: int = 600,
        num_points: int = 50,
        seed: int = 42,
    ) -> PatternResult:
        rng = random.Random(seed)
        points = [(rng.uniform(0, width), rng.uniform(0, height)) for _ in range(num_points)]
        return PatternResult(width=width, height=height, num_regions=num_points, points=points)

    def delaunay(
        self,
        width: int = 800,
        height: int = 600,
        num_points: int = 30,
        seed: int = 42,
    ) -> PatternResult:
        rng = random.Random(seed)
        points = [(rng.uniform(0, width), rng.uniform(0, height)) for _ in range(num_points)]
        triangles = num_points * 2 - 2
        return PatternResult(width=width, height=height, num_regions=triangles, points=points)

    def penrose_tiling(self, order: int = 3) -> PatternResult:
        num_kites = sum(5 * 4 ** i for i in range(order))
        return PatternResult(width=800, height=600, num_regions=num_kites)


# ---------------------------------------------------------------------------
# Cellular Automaton
# ---------------------------------------------------------------------------

class CellularAutomaton:
    """Cellular automaton simulation."""

    def __init__(self, rule: int = 30, width: int = 100, generations: int = 50):
        self.rule = rule
        self.width = width
        self.generations = generations

    def evolve(self) -> CAEvolution:
        history: List[List[int]] = []
        current = [0] * self.width
        current[self.width // 2] = 1
        for gen in range(self.generations):
            history.append(current[:])
            next_gen = [0] * self.width
            for i in range(1, self.width - 1):
                left, center, right = current[i-1], current[i], current[i+1]
                pattern = (left << 2) | (center << 1) | right
                next_gen[i] = (self.rule >> pattern) & 1
            current = next_gen
        total = sum(sum(row) for row in history)
        density = total / (self.width * self.generations)
        pattern_type = "chaotic" if 0.2 < density < 0.6 else "periodic" if density > 0.1 else "dying"
        return CAEvolution(
            rule=self.rule, width=self.width, generations=self.generations,
            pattern_type=pattern_type, history=history, density=round(density, 3),
        )

    def game_of_life(self, grid: List[List[int]], generations: int = 10) -> List[List[int]]:
        current = [row[:] for row in grid]
        for _ in range(generations):
            h, w = len(current), len(current[0])
            next_grid = [[0] * w for _ in range(h)]
            for i in range(h):
                for j in range(w):
                    neighbors = sum(
                        current[(i+di) % h][(j+dj) % w]
                        for di in [-1, 0, 1] for dj in [-1, 0, 1]
                        if not (di == 0 and dj == 0)
                    )
                    if current[i][j]:
                        next_grid[i][j] = 1 if neighbors in (2, 3) else 0
                    else:
                        next_grid[i][j] = 1 if neighbors == 3 else 0
            current = next_grid
        return current


# ---------------------------------------------------------------------------
# Mathematical Curves
# ---------------------------------------------------------------------------

class MathematicalCurves:
    """Generate mathematical curves."""

    def rose_curve(
        self, k: int = 7, d: int = 3, resolution: int = 1000
    ) -> CurveResult:
        points: List[Tuple[float, float]] = []
        for i in range(resolution):
            theta = 2 * math.pi * i / resolution
            r = math.cos(k * theta / d)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.append((x, y))
        return CurveResult(name="Rose Curve", num_points=resolution, points=points, parameters={"k": k, "d": d})

    def lissajous(
        self, a: int = 3, b: int = 2, delta: float = math.pi / 2, resolution: int = 1000
    ) -> CurveResult:
        points: List[Tuple[float, float]] = []
        for i in range(resolution):
            t = 2 * math.pi * i / resolution
            x = math.sin(a * t + delta)
            y = math.sin(b * t)
            points.append((x, y))
        return CurveResult(name="Lissajous", num_points=resolution, points=points, parameters={"a": a, "b": b})

    def butterfly_curve(self, resolution: int = 2000) -> CurveResult:
        points: List[Tuple[float, float]] = []
        for i in range(resolution):
            t = 2 * math.pi * i / resolution
            r = math.exp(math.sin(t)) - 2 * math.cos(4 * t) + math.sin((2 * t - math.pi) / 24) ** 5
            x = r * math.sin(t)
            y = r * math.cos(t)
            points.append((x, y))
        return CurveResult(name="Butterfly Curve", num_points=resolution, points=points)

    def spirograph(
        self, R: float = 100, r: float = 60, d: float = 80, resolution: int = 2000
    ) -> CurveResult:
        points: List[Tuple[float, float]] = []
        for i in range(resolution):
            t = 2 * math.pi * i / resolution
            x = (R - r) * math.cos(t) + d * math.cos((R - r) * t / r)
            y = (R - r) * math.sin(t) + d * math.sin((R - r) * t / r)
            points.append((x, y))
        return CurveResult(name="Spirograph", num_points=resolution, points=points)


# ---------------------------------------------------------------------------
# Noise Generator
# ---------------------------------------------------------------------------

class NoiseGenerator:
    """Generate noise patterns."""

    def __init__(self, scale: float = 0.1, seed: int = 42):
        self.scale = scale
        self.seed = seed
        self._rng = random.Random(seed)
        self._gradients: Dict[Tuple[int, int], Tuple[float, float]] = {}

    def _gradient(self, ix: int, iy: int) -> Tuple[float, float]:
        key = (ix, iy)
        if key not in self._gradients:
            angle = self._rng.uniform(0, 2 * math.pi)
            self._gradients[key] = (math.cos(angle), math.sin(angle))
        return self._gradients[key]

    def _fade(self, t: float) -> float:
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, a: float, b: float, t: float) -> float:
        return a + t * (b - a)

    def perlin_2d(self, x: float, y: float) -> float:
        xi = int(math.floor(x))
        yi = int(math.floor(y))
        xf = x - xi
        yf = y - yi
        u = self._fade(xf)
        v = self._fade(yf)
        g00 = self._gradient(xi, yi)
        g10 = self._gradient(xi + 1, yi)
        g01 = self._gradient(xi, yi + 1)
        g11 = self._gradient(xi + 1, yi + 1)
        n00 = g00[0] * xf + g00[1] * yf
        n10 = g10[0] * (xf - 1) + g10[1] * yf
        n01 = g01[0] * xf + g01[1] * (yf - 1)
        n11 = g11[0] * (xf - 1) + g11[1] * (yf - 1)
        nx0 = self._lerp(n00, n10, u)
        nx1 = self._lerp(n01, n11, u)
        return self._lerp(nx0, nx1, v)

    def generate_perlin(self, width: int = 100, height: int = 100) -> NoiseField:
        values: List[List[float]] = []
        for y in range(height):
            row: List[float] = []
            for x in range(width):
                val = self.perlin_2d(x * self.scale, y * self.scale)
                row.append(val)
            values.append(row)
        all_vals = [v for row in values for v in row]
        return NoiseField(
            width=width, height=height,
            min_value=min(all_vals), max_value=max(all_vals),
            values=values,
        )

    def fractal_noise(
        self, width: int = 100, height: int = 100, octaves: int = 4
    ) -> NoiseField:
        values: List[List[float]] = [[0.0] * width for _ in range(height)]
        amplitude = 1.0
        frequency = 1.0
        for _ in range(octaves):
            noise = self.generate_perlin(width, height)
            for y in range(height):
                for x in range(width):
                    values[y][x] += noise.values[y][x] * amplitude
            amplitude *= 0.5
            frequency *= 2
        all_vals = [v for row in values for v in row]
        return NoiseField(
            width=width, height=height,
            min_value=min(all_vals), max_value=max(all_vals),
            values=values,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Algorithmic Art Demo")
    print("=" * 60)

    print("\n[1] Mandelbrot Set")
    fractal = FractalGenerator()
    mandelbrot = fractal.mandelbrot(80, 60, max_iter=50)
    print(f"  Size: {mandelbrot.width}x{mandelbrot.height}")
    print(f"  Pixels: {mandelbrot.total_pixels}")

    print("\n[2] Julia Set")
    julia = fractal.julia(80, 60, c=-0.7+0.27015j)
    print(f"  Size: {julia.width}x{julia.height}")

    print("\n[3] Sierpinski Triangle")
    sierpinski = fractal.sierpinski(5)
    print(f"  Size: {sierpinski.width}x{sierpinski.height}")
    print(f"  Elements: {sierpinski.num_elements}")

    print("\n[4] Koch Snowflake")
    koch = fractal.koch_snowflake(4)
    print(f"  Points: {koch.num_points}")

    print("\n[5] Voronoi Diagram")
    creator = PatternCreator()
    voronoi = creator.voronoi(80, 60, 20)
    print(f"  Regions: {voronoi.num_regions}")

    print("\n[6] Cellular Automata (Rule 30)")
    ca = CellularAutomaton(rule=30, width=50, generations=30)
    evolution = ca.evolve()
    print(f"  Generations: {evolution.generations}")
    print(f"  Density: {evolution.density}")
    print(f"  Type: {evolution.pattern_type}")

    print("\n[7] Game of Life")
    gol = CellularAutomaton(width=10, generations=5)
    initial = [[0]*10 for _ in range(10)]
    initial[4][4] = initial[4][5] = initial[4][6] = 1
    initial[3][5] = 1
    initial[5][4] = 1
    final = gol.game_of_life(initial, 5)
    alive = sum(sum(row) for row in final)
    print(f"  Final alive cells: {alive}")

    print("\n[8] Mathematical Curves")
    curves = MathematicalCurves()
    rose = curves.rose_curve(k=5, d=2)
    print(f"  Rose: {rose.num_points} points")
    lissajous = curves.lissajous(a=3, b=2)
    print(f"  Lissajous: {lissajous.num_points} points")
    butterfly = curves.butterfly_curve(1500)
    print(f"  Butterfly: {butterfly.num_points} points")
    spiro = curves.spirograph(R=100, r=60, d=80)
    print(f"  Spirograph: {spiro.num_points} points")

    print("\n[9] Perlin Noise")
    noise = NoiseGenerator(scale=0.1)
    perlin = noise.generate_perlin(50, 50)
    print(f"  Field: {perlin.width}x{perlin.height}")
    print(f"  Range: {perlin.min_value:.3f} to {perlin.max_value:.3f}")

    print("\n[10] Fractal Noise")
    fractal_noise = noise.fractal_noise(50, 50, octaves=4)
    print(f"  Field: {fractal_noise.width}x{fractal_noise.height}")

    print("\n" + "=" * 60)
    print("  Algorithmic art demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
