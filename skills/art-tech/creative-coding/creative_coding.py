"""
Creative Coding Module — Canvas drawing, animation systems, audio-reactive visuals,
data visualization, easing functions, and export for creative programming.
"""

from __future__ import annotations

import math
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


class BlendMode(Enum):
    NORMAL = "normal"
    ADD = "add"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"


class Easing(Enum):
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    EASE_IN_OUT_CUBIC = "ease_in_out_cubic"
    BOUNCE_OUT = "bounce_out"
    ELASTIC_OUT = "elastic_out"
    BACK_OUT = "back_out"

    def apply(self, t: float) -> float:
        t = max(0, min(1, t))
        if self == Easing.LINEAR:
            return t
        elif self == Easing.EASE_IN:
            return t * t
        elif self == Easing.EASE_OUT:
            return 1 - (1 - t) * (1 - t)
        elif self == Easing.EASE_IN_OUT:
            return 2 * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 2 / 2
        elif self == Easing.EASE_IN_OUT_CUBIC:
            return 4 * t * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2
        elif self == Easing.BOUNCE_OUT:
            n1, d1 = 7.5625, 2.75
            if t < 1/d1: return n1 * t * t
            elif t < 2/d1: t -= 1.5/d1; return n1 * t * t + 0.75
            elif t < 2.5/d1: t -= 2.25/d1; return n1 * t * t + 0.9375
            else: t -= 2.625/d1; return n1 * t * t + 0.984375
        elif self == Easing.ELASTIC_OUT:
            if t == 0 or t == 1: return t
            return 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1
        elif self == Easing.BACK_OUT:
            c1, c3 = 1.70158, c1 + 1
            return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
        return t


@dataclass
class Color:
    r: int = 255
    g: int = 255
    b: int = 255
    a: int = 255

    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def to_rgba(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)

    def lerp(self, other: "Color", t: float) -> "Color":
        return Color(
            int(self.r + (other.r - self.r) * t),
            int(self.g + (other.g - self.g) * t),
            int(self.b + (other.b - self.b) * t),
            int(self.a + (other.a - self.a) * t),
        )

    @classmethod
    def from_hsb(cls, h: float, s: float, b: float, a: int = 255) -> "Color":
        c = b * s
        x = c * (1 - abs((h/60) % 2 - 1))
        m = b - c
        if h < 60: r, g, bl = c, x, 0
        elif h < 120: r, g, bl = x, c, 0
        elif h < 180: r, g, bl = 0, c, x
        elif h < 240: r, g, bl = 0, x, c
        elif h < 300: r, g, bl = x, 0, c
        else: r, g, bl = c, 0, x
        return cls(int((r+m)*255), int((g+m)*255), int((bl+m)*255), a)


@dataclass
class AnimatedObject:
    object_id: str
    properties: Dict[str, float] = field(default_factory=dict)
    tweens: List[Dict[str, Any]] = field(default_factory=list)

    def update(self, dt: float) -> None:
        completed = []
        for tween in self.tweens:
            if tween.get("completed"):
                continue
            tween["elapsed"] = tween.get("elapsed", 0) + dt
            progress = min(1, tween["elapsed"] / tween["duration"])
            easing = tween.get("easing", Easing.LINEAR)
            eased_progress = easing.apply(progress)
            prop = tween["property"]
            start, end = tween["start"], tween["end"]
            self.properties[prop] = start + (end - start) * eased_progress
            if progress >= 1:
                tween["completed"] = True
                completed.append(tween)
        self.tweens = [t for t in self.tweens if not t.get("completed")]


@dataclass
class FrequencyBands:
    bass: float = 0.0
    low_mid: float = 0.0
    mid: float = 0.0
    high_mid: float = 0.0
    treble: float = 0.0
    volume: float = 0.0
    beat: bool = False

    def to_dict(self) -> Dict[str, float]:
        return {"bass": round(self.bass, 3), "mid": round(self.mid, 3), "treble": round(self.treble, 3), "volume": round(self.volume, 3)}


@dataclass
class DataPoint:
    label: str
    value: float
    color: Optional[Color] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class Canvas:
    def __init__(self, width: int = 1920, height: int = 1080, framerate: int = 60,
                 background: Tuple[int, int, int] = (10, 10, 15)):
        self.width = width
        self.height = height
        self.framerate = framerate
        self.background = background
        self._frames: List[Dict[str, Any]] = []
        self._current_frame: Dict[str, Any] = {"shapes": [], "time": 0}
        self._blend_mode = BlendMode.NORMAL

    def fill(self, color: Color) -> None:
        self._current_frame["fill"] = color.to_rgba()

    def stroke(self, color: Color) -> None:
        self._current_frame["stroke"] = color.to_rgba()

    def stroke_weight(self, weight: float) -> None:
        self._current_frame["stroke_weight"] = weight

    def no_fill(self) -> None:
        self._current_frame["fill"] = None

    def no_stroke(self) -> None:
        self._current_frame["stroke"] = None

    def rect(self, x: float, y: float, w: float, h: float) -> None:
        self._current_frame["shapes"].append({"type": "rect", "x": x, "y": y, "w": w, "h": h, "fill": self._current_frame.get("fill"), "stroke": self._current_frame.get("stroke")})

    def ellipse(self, x: float, y: float, w: float, h: float) -> None:
        self._current_frame["shapes"].append({"type": "ellipse", "x": x, "y": y, "w": w, "h": h, "fill": self._current_frame.get("fill")})

    def line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        self._current_frame["shapes"].append({"type": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": self._current_frame.get("stroke")})

    def clear(self) -> None:
        self._current_frame = {"shapes": [], "time": self._current_frame.get("time", 0)}

    def render_frame(self) -> Dict[str, Any]:
        frame = dict(self._current_frame)
        frame["width"] = self.width
        frame["height"] = self.height
        frame["background"] = self.background
        self._frames.append(frame)
        self.clear()
        return frame

    def save_frame(self, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        frame_data = self.render_frame()
        Path(path).write_text(json.dumps(frame_data, indent=2))

    def start_recording(self, path: str, framerate: int = 30, duration: float = 10) -> None:
        pass


class AnimationSystem:
    def __init__(self):
        self._objects: Dict[str, AnimatedObject] = {}

    def create_object(self, name: str, **properties: float) -> AnimatedObject:
        obj = AnimatedObject(object_id=name, properties=properties)
        self._objects[name] = obj
        return obj

    def tween(self, obj: AnimatedObject, property: str, start: float, end: float,
              duration: float = 1.0, easing: Easing = Easing.LINEAR, delay: float = 0) -> None:
        obj.tweens.append({
            "property": property, "start": start, "end": end,
            "duration": duration, "easing": easing, "delay": delay, "elapsed": 0,
        })

    def update(self, dt: float) -> None:
        for obj in self._objects.values():
            obj.update(dt)

    def get_object(self, name: str) -> Optional[AnimatedObject]:
        return self._objects.get(name)


class AudioReactive:
    def __init__(self, source: str = "microphone", fft_size: int = 1024):
        self.source = source
        self.fft_size = fft_size
        self._volume = 0.5

    def get_frequency_bands(self) -> FrequencyBands:
        import random
        return FrequencyBands(
            bass=random.uniform(0, 1), low_mid=random.uniform(0, 0.7),
            mid=random.uniform(0, 0.8), high_mid=random.uniform(0, 0.6),
            treble=random.uniform(0, 0.5), volume=random.uniform(0.3, 0.8),
            beat=random.random() > 0.8,
        )


class DataVisualizer:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def bar_chart(self, data: List[DataPoint], x: float, y: float, width: float, height: float,
                 palette: str = "warm") -> None:
        if not data:
            return
        max_val = max(d.value for d in data)
        bar_width = width / len(data) * 0.8
        gap = width / len(data) * 0.2
        for i, point in enumerate(data):
            bar_h = (point.value / max_val) * height if max_val > 0 else 0
            bx = x + i * (bar_width + gap)
            color = point.color or Color(255, 100, 50)
            self.canvas.fill(color)
            self.canvas.rect(bx, y + height - bar_h, bar_width, bar_h)

    def scatter_plot(self, data: List[Tuple[float, float]], x: float, y: float,
                    width: float, height: float, radius: float = 5) -> None:
        if not data:
            return
        max_x = max(d[0] for d in data) if data else 1
        max_y = max(d[1] for d in data) if data else 1
        for dx, dy in data:
            px = x + (dx / max_x) * width
            py = y + height - (dy / max_y) * height
            self.canvas.fill(Color(100, 200, 255))
            self.canvas.ellipse(px, py, radius * 2, radius * 2)


class ParticleSystem:
    def __init__(self, max_count: int = 1000, gravity: float = 0.01):
        self.max_count = max_count
        self.gravity = gravity
        self._particles: List[Dict[str, Any]] = []

    def emit(self, x: float, y: float, count: int = 10, color: Color = Color(255, 255, 255)) -> None:
        for _ in range(count):
            if len(self._particles) < self.max_count:
                self._particles.append({
                    "x": x, "y": y,
                    "vx": random.uniform(-2, 2), "vy": random.uniform(-3, -1),
                    "life": 1.0, "color": color.to_rgba(),
                })

    def update(self, dt: float) -> None:
        for p in self._particles:
            p["vy"] += self.gravity
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 0.02
        self._particles = [p for p in self._particles if p["life"] > 0]

    @property
    def count(self) -> int:
        return len(self._particles)


class ShaderSnippet:
    def __init__(self, name: str, fragment_code: str, uniforms: Optional[Dict[str, Any]] = None):
        self.name = name
        self.fragment_code = fragment_code
        self.uniforms = uniforms or {}

    def to_glsl(self) -> str:
        uniforms_glsl = "\n".join(f"uniform float {k};" for k in self.uniforms)
        return f"precision mediump float;\n{uniforms_glsl}\nvoid main() {{\n{self.fragment_code}\n}}"


def main():
    print("Creative Coding Toolkit")
    print("=" * 60)

    canvas = Canvas(width=800, height=600, framerate=60)
    canvas.fill(Color(255, 100, 50))
    canvas.ellipse(400, 300, 100, 100)
    canvas.fill(Color(50, 150, 255))
    canvas.rect(200, 200, 200, 150)
    frame = canvas.render_frame()
    print(f"Frame: {len(frame['shapes'])} shapes")

    anim = AnimationSystem()
    ball = anim.create_object("ball", x=0, y=300)
    anim.tween(ball, "x", 0, 800, duration=2.0, easing=Easing.EASE_IN_OUT_CUBIC)
    for _ in range(60):
        anim.update(1/60)
    print(f"Ball position: {anim.get_object('ball').properties}")

    audio = AudioReactive()
    bands = audio.get_frequency_baves() if hasattr(audio, 'get_frequency_baves') else audio.get_frequency_bands()
    print(f"Audio bands: {bands.to_dict()}")

    ps = ParticleSystem(max_count=500)
    ps.emit(400, 300, count=50, color=Color(255, 100, 50))
    for _ in range(30):
        ps.update(0.016)
    print(f"Particles: {ps.count}")

    viz = DataVisualizer(canvas)
    data = [DataPoint("A", 42), DataPoint("B", 78), DataPoint("C", 35)]
    print(f"Data points: {len(data)}")

    easing_test = Easing.BOUNCE_OUT.apply(0.5)
    print(f"Bounce out at t=0.5: {easing_test:.3f}")


if __name__ == "__main__":
    main()
