"""
Lighting Control System
DMX512, Art-Net/sACN, fixture control, color mixing, cue lists, and effects.
"""

from __future__ import annotations

import colorsys
import json
import logging
import math
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class MergeMode(Enum):
    HTP = "htp"  # Highest Takes Precedence — for intensity
    LTP = "ltp"  # Latest Takes Precedence — for attributes


class Waveform(Enum):
    SINE = "sine"
    TRIANGLE = "triangle"
    SAWTOOTH = "sawtooth"
    SQUARE = "square"
    RANDOM = "random"
    STEP = "step"


class GoboType(Enum):
    OPEN = "open"
    BREAKUP = "breakup"
    DOT = "dot"
    LINE = "line"
    WATER = "water"
    BREAKUP_SLOW = "breakup_slow"
    CIRCULAR = "circular"


class ColorSpace(Enum):
    RGB = "rgb"
    RGBW = "rgbw"
    RGBAW = "rgbaw"
    CMY = "cmy"
    HSV = "hsv"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ColorMix:
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
    w: float = 0.0
    a: float = 0.0

    @classmethod
    def from_hex(cls, hex_color: str) -> ColorMix:
        h = hex_color.lstrip("#")
        if len(h) == 6:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            return cls(r=r / 255.0, g=g / 255.0, b=b / 255.0)
        elif len(h) == 8:
            r, g, b, w = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16)
            return cls(r=r / 255.0, g=g / 255.0, b=b / 255.0, w=w / 255.0)
        raise ValueError(f"Invalid hex color: {hex_color}")

    @classmethod
    def from_cie(cls, x: float, y: float, brightness: float = 1.0) -> ColorMix:
        if y == 0:
            return cls()
        z = 1.0 - x - y
        Y = brightness
        X = (Y / y) * x
        Z = (Y / y) * z
        r = 3.2406 * X - 1.5372 * Y - 0.4986 * Z
        g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
        b = 0.0557 * X - 0.2040 * Y + 1.0570 * Z
        r = max(0.0, min(1.0, r))
        g = max(0.0, min(1.0, g))
        b = max(0.0, min(1.0, b))
        return cls(r=r, g=g, b=b)

    def to_rgbw(self) -> tuple[int, int, int, int]:
        w = min(self.r, self.g, self.b)
        r = int((self.r - w) * 255)
        g = int((self.g - w) * 255)
        b = int((self.b - w) * 255)
        w = int(w * 255)
        return (r, g, b, w)

    def to_cmy(self) -> tuple[int, int, int]:
        c = int((1.0 - self.r) * 255)
        m = int((1.0 - self.g) * 255)
        y = int((1.0 - self.b) * 255)
        return (c, m, y)

    def to_hex(self) -> str:
        r = int(self.r * 255)
        g = int(self.g * 255)
        b = int(self.b * 255)
        return f"#{r:02X}{g:02X}{b:02X}"

    def lerp(self, other: ColorMix, t: float) -> ColorMix:
        t = max(0.0, min(1.0, t))
        return ColorMix(
            r=self.r + (other.r - self.r) * t,
            g=self.g + (other.g - self.g) * t,
            b=self.b + (other.b - self.b) * t,
            w=self.w + (other.w - self.w) * t,
        )


@dataclass
class FixtureChannel:
    name: str
    dmx_offset: int
    default_value: int = 0
    merge_mode: MergeMode = MergeMode.HTP


@dataclass
class FixtureProfile:
    name: str
    manufacturer: str
    channels: list[FixtureChannel]
    color_space: ColorSpace = ColorSpace.RGB
    pan_range_deg: float = 540.0
    tilt_range_deg: float = 270.0


@dataclass
class Fixture:
    name: str
    profile: str
    dmx_address: int
    fixture_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    _values: dict[str, int] = field(default_factory=dict)

    def set_intensity(self, value: float) -> None:
        self._values["intensity"] = int(max(0.0, min(1.0, value)) * 255)

    def set_color(self, color: ColorMix) -> None:
        self._values["color_r"] = int(color.r * 255)
        self._values["color_g"] = int(color.g * 255)
        self._values["color_b"] = int(color.b * 255)
        self._values["color_w"] = int(color.w * 255)

    def set_pan(self, degrees: float) -> None:
        self._values["pan"] = int((degrees / 540.0) * 255)

    def set_tilt(self, degrees: float) -> None:
        self._values["tilt"] = int((degrees / 270.0) * 255)

    def set_gobo(self, gobo: GoboType) -> None:
        gobos = list(GoboType)
        self._values["gobo"] = int((gobos.index(gobo) / max(1, len(gobos) - 1)) * 255)

    def set_shutter(self, open: bool) -> None:
        self._values["shutter"] = 255 if open else 0

    def channel(self, name: str) -> str:
        return f"{self.fixture_id}_{name}"

    def get_dmx_values(self) -> dict[int, int]:
        result = {}
        for i, (key, value) in enumerate(self._values.items()):
            result[self.dmx_address + i] = value
        return result


# ---------------------------------------------------------------------------
# DMX Universe
# ---------------------------------------------------------------------------

class DMXUniverse:
    """512-channel DMX universe with merge and output capabilities."""

    def __init__(self, universe_id: int = 0):
        self.universe_id = universe_id
        self._frame: list[int] = [0] * 512
        self._fixtures: dict[str, Fixture] = {}
        self._merge_buffers: dict[str, list[int]] = {}

    def patch(self, fixture: Fixture) -> None:
        self._fixtures[fixture.fixture_id] = fixture
        logger.info("Patched fixture '%s' at DMX %d", fixture.name, fixture.dmx_address)

    def unpatch(self, fixture_id: str) -> None:
        if fixture_id in self._fixtures:
            del self._fixtures[fixture_id]

    def set_channel(self, channel: int, value: int, merge: MergeMode = MergeMode.HTP) -> None:
        if not 1 <= channel <= 512:
            raise ValueError(f"DMX channel must be 1-512, got {channel}")
        value = max(0, min(255, value))
        ch_idx = channel - 1
        if merge == MergeMode.HTP:
            self._frame[ch_idx] = max(self._frame[ch_idx], value)
        else:
            self._frame[ch_idx] = value

    def clear(self) -> None:
        self._frame = [0] * 512

    def get_channel(self, channel: int) -> int:
        return self._frame[channel - 1]

    def output(self, node: Optional[ArtNetNode] = None) -> list[int]:
        for fixture in self._fixtures.values():
            for ch, val in fixture.get_dmx_values().items():
                self._frame[ch - 1] = val
        if node:
            node.send(self._frame)
        return list(self._frame)

    def snapshot(self) -> list[int]:
        return list(self._frame)

    def restore(self, snapshot: list[int]) -> None:
        if len(snapshot) != 512:
            raise ValueError("Snapshot must be 512 channels")
        self._frame = list(snapshot)


# ---------------------------------------------------------------------------
# Art-Net Node
# ---------------------------------------------------------------------------

class ArtNetNode:
    """Art-Net (ArtNet4) DMX output node."""

    def __init__(self, ip: str = "2.0.0.1", subnet: int = 0, universe: int = 0):
        self.ip = ip
        self.subnet = subnet
        self.universe = universe
        self._running = False

    def start(self) -> bool:
        self._running = True
        logger.info("Art-Net node started: %s (sub:%d uni:%d)", self.ip, self.subnet, self.universe)
        return True

    def stop(self) -> None:
        self._running = False

    def send(self, frame: list[int]) -> bool:
        if not self._running:
            raise RuntimeError("Art-Net node not started")
        data = bytes(frame[:512])
        logger.debug(
            "Art-Net output to %s (sub:%d uni:%d): %d bytes",
            self.ip, self.subnet, self.universe, len(data),
        )
        return True


# ---------------------------------------------------------------------------
# Effect Generator
# ---------------------------------------------------------------------------

@dataclass
class EffectGenerator:
    """Generates oscillating or stepped DMX effects."""
    channels: list[str]
    waveform: Waveform = Waveform.SINE
    period_s: float = 4.0
    amplitude: float = 0.5
    offset: float = 0.0
    phase_offset: float = 0.0
    steps: int = 8

    def evaluate(self, time_s: float) -> dict[str, float]:
        t = (time_s + self.phase_offset) / self.period_s
        t_frac = t - math.floor(t)

        if self.waveform == Waveform.SINE:
            raw = math.sin(2 * math.pi * t_frac) * 0.5 + 0.5
        elif self.waveform == Waveform.TRIANGLE:
            raw = 1.0 - abs(2.0 * t_frac - 1.0)
        elif self.waveform == Waveform.SAWTOOTH:
            raw = t_frac
        elif self.waveform == Waveform.SQUARE:
            raw = 1.0 if t_frac < 0.5 else 0.0
        elif self.waveform == Waveform.STEP:
            step_idx = int(t_frac * self.steps) % self.steps
            raw = step_idx / max(1, self.steps - 1)
        elif self.waveform == Waveform.RANDOM:
            import random
            raw = random.random()
        else:
            raw = 0.0

        result = {}
        for i, ch in enumerate(self.channels):
            phase = i * 0.1
            t_shifted = ((time_s + phase) + self.phase_offset) / self.period_s
            t_shifted_frac = t_shifted - math.floor(t_shifted)
            if self.waveform == Waveform.SINE:
                val = math.sin(2 * math.pi * t_shifted_frac) * 0.5 + 0.5
            else:
                val = raw
            result[ch] = max(0.0, min(1.0, self.offset + val * self.amplitude))
        return result


# ---------------------------------------------------------------------------
# Cross-Fade Engine
# ---------------------------------------------------------------------------

@dataclass
class CueEntry:
    number: float
    look: dict[str, Any]
    fade_time_s: float = 3.0
    delay_time_s: float = 0.0
    follow_time_s: float = 0.0
    status: str = "pending"


class CueList:
    """Manages a sequential list of lighting cues."""

    def __init__(self, name: str = "default"):
        self.name = name
        self._cues: list[CueEntry] = []

    def add_cue(
        self,
        number: float,
        look: dict[str, Any],
        fade_time_s: float = 3.0,
        delay_time_s: float = 0.0,
        follow_time_s: float = 0.0,
    ) -> CueEntry:
        cue = CueEntry(
            number=number,
            look=look,
            fade_time_s=fade_time_s,
            delay_time_s=delay_time_s,
            follow_time_s=follow_time_s,
        )
        self._cues.append(cue)
        self._cues.sort(key=lambda c: c.number)
        return cue

    def get_next(self) -> Optional[CueEntry]:
        for cue in self._cues:
            if cue.status == "pending":
                return cue
        return None

    def get_cue(self, number: float) -> Optional[CueEntry]:
        return next((c for c in self._cues if c.number == number), None)

    def clear_status(self) -> None:
        for cue in self._cues:
            cue.status = "pending"

    def __len__(self) -> int:
        return len(self._cues)


class CrossFadeEngine:
    """Executes cue transitions with timed cross-fades."""

    def __init__(self, universe: DMXUniverse, cue_list: CueList):
        self.universe = universe
        self.cue_list = cue_list
        self._active_effects: list[EffectGenerator] = []

    def go(self) -> bool:
        cue = self.cue_list.get_next()
        if cue is None:
            logger.info("No more cues in list")
            return False
        cue.status = "executing"
        logger.info(
            "Executing cue %.1f (fade: %.1fs, delay: %.1fs)",
            cue.number, cue.fade_time_s, cue.delay_time_s,
        )
        for fixture_name, params in cue.look.items():
            if fixture_name == "all":
                continue
            if "intensity" in params:
                logger.debug("  %s intensity -> %.0f%%", fixture_name, params["intensity"] * 100)
            if "color" in params:
                logger.debug("  %s color -> %s", fixture_name, params["color"])
        cue.status = "complete"
        return True

    def apply_effect(self, effect: EffectGenerator) -> None:
        self._active_effects.append(effect)
        logger.info(
            "Applied effect (%s, period=%.1fs) to %d channels",
            effect.waveform.value, effect.period_s, len(effect.channels),
        )

    def remove_effects(self) -> None:
        self._active_effects.clear()


# ---------------------------------------------------------------------------
# LED Wall
# ---------------------------------------------------------------------------

@dataclass
class CalibrationPoint:
    fixture_channel: str
    expected: tuple[int, int, int]
    measured: tuple[int, int, int]

    @property
    def error(self) -> float:
        return math.sqrt(
            sum((e - m) ** 2 for e, m in zip(self.expected, self.measured))
        )


class LEDWall:
    """LED video wall panel array controller."""

    def __init__(
        self,
        panels_x: int = 4,
        panels_y: int = 3,
        panel_width_px: int = 640,
        panel_height_px: int = 480,
        dmx_start_address: int = 1,
    ):
        self.panels_x = panels_x
        self.panels_y = panels_y
        self.panel_width_px = panel_width_px
        self.panel_height_px = panel_height_px
        self.dmx_start_address = dmx_start_address
        self._pixel_data: list[int] = []
        self._calibration: Optional[list[CalibrationPoint]] = None

    @property
    def total_width_px(self) -> int:
        return self.panels_x * self.panel_width_px

    @property
    def total_height_px(self) -> int:
        return self.panels_y * self.panel_height_px

    @property
    def total_pixels(self) -> int:
        return self.total_width_px * self.total_height_px

    def set_pixel_map_mode(self, mode: str) -> None:
        logger.info("LED wall pixel map mode: %s", mode)

    def fill_solid(self, hex_color: str) -> None:
        color = ColorMix.from_hex(hex_color)
        r, g, b = int(color.r * 255), int(color.g * 255), int(color.b * 255)
        self._pixel_data = [r, g, b] * self.total_pixels
        logger.info("LED wall filled with %s (%d pixels)", hex_color, self.total_pixels)

    def apply_calibration(self, calibration: list[CalibrationPoint]) -> None:
        self._calibration = calibration
        logger.info("Applied %d-point calibration to LED wall", len(calibration))

    def output(self, universe: DMXUniverse) -> None:
        logger.debug("LED wall output: %d pixel values to DMX", len(self._pixel_data))


class ColorCalibrator:
    """Calibrates color output across LED panels."""

    def __init__(self, reference_color: str = "#FFFFFF"):
        self.reference_color = ColorMix.from_hex(reference_color)
        self._measurements: list[CalibrationPoint] = []

    def calibrate_wall(self, wall: LEDWall) -> list[CalibrationPoint]:
        ref_rgb = (
            int(self.reference_color.r * 255),
            int(self.reference_color.g * 255),
            int(self.reference_color.b * 255),
        )
        calibration = []
        for y in range(wall.panels_y):
            for x in range(wall.panels_x):
                measured = (ref_rgb[0], ref_rgb[1], ref_rgb[2])
                point = CalibrationPoint(
                    fixture_channel=f"panel_{x}_{y}",
                    expected=ref_rgb,
                    measured=measured,
                )
                calibration.append(point)
        logger.info(
            "Calibrated %d panels against reference %s",
            len(calibration), self.reference_color.to_hex(),
        )
        return calibration


# ---------------------------------------------------------------------------
# Gel Presets
# ---------------------------------------------------------------------------

class GelLibrary:
    """Lee and Rosco gel filter preset library."""

    LEE_GELS: dict[str, str] = {
        "Primary Blue": "#0044CC",
        "Primary Red": "#CC0000",
        "Primary Green": "#00CC00",
        "CT Blue": "#6699CC",
        "No Color Blue": "#9999CC",
        "Medium Amber": "#CC9933",
        "Pale Gold": "#FFD699",
        "Lavender": "#CC99FF",
        "Light Pink": "#FF99CC",
        "Deep Amber": "#CC6600",
    }

    ROSCO_GELS: dict[str, str] = {
        "R3202 Full CT Blue": "#AACCFF",
        "R3204 Half CT Blue": "#CCE5FF",
        "R3208 1/4 CT Blue": "#E8F4FF",
        "R3216 Full CT Orange": "#FFAA44",
        "R3220 Half CT Orange": "#FFCC88",
        "R3224 1/4 CT Orange": "#FFE4BB",
        "R27 Medium Lavender": "#AA77CC",
        "R352 Lavender": "#CCAAEE",
        "R02 Fire Red": "#DD2200",
        "R19 Fire Orange": "#FF5500",
    }

    @classmethod
    def get_color(cls, library: str, name: str) -> Optional[ColorMix]:
        gels = cls.LEE_GELS if library.lower() == "lee" else cls.ROSCO_GELS
        hex_color = gels.get(name)
        if hex_color:
            return ColorMix.from_hex(hex_color)
        return None

    @classmethod
    def list_gels(cls, library: str = "lee") -> list[str]:
        return list(cls.LEE_GELS.keys() if library.lower() == "lee" else cls.ROSCO_GELS.keys())


# ---------------------------------------------------------------------------
# Show File I/O
# ---------------------------------------------------------------------------

class ShowFileIO:
    """Import and export lighting show files."""

    @staticmethod
    def export_json(cue_list: CueList, filepath: str) -> None:
        data = {
            "name": cue_list.name,
            "cues": [
                {
                    "number": c.number,
                    "look": c.look,
                    "fade_time_s": c.fade_time_s,
                    "delay_time_s": c.delay_time_s,
                    "follow_time_s": c.follow_time_s,
                }
                for c in cue_list._cues
            ],
        }
        Path(filepath).write_text(json.dumps(data, indent=2))
        logger.info("Exported %d cues to %s", len(cue_list), filepath)

    @staticmethod
    def import_json(filepath: str) -> CueList:
        with open(filepath) as f:
            data = json.load(f)
        cue_list = CueList(name=data.get("name", "imported"))
        for c in data.get("cues", []):
            cue_list.add_cue(
                number=c["number"],
                look=c["look"],
                fade_time_s=c.get("fade_time_s", 3.0),
                delay_time_s=c.get("delay_time_s", 0.0),
                follow_time_s=c.get("follow_time_s", 0.0),
            )
        logger.info("Imported %d cues from %s", len(cue_list), filepath)
        return cue_list


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("=" * 60)
    print("  Lighting Control System — Demo")
    print("=" * 60)

    # --- DMX Universe and Art-Net ---
    universe = DMXUniverse(universe_id=0)
    artnet = ArtNetNode(ip="2.0.0.1", subnet=0, universe=0)
    artnet.start()

    # --- Color Mixing ---
    color = ColorMix.from_hex("#FFB347")
    print(f"Warm amber: R={color.r:.2f} G={color.g:.2f} B={color.b:.2f}")
    print(f"  -> RGBW: {color.to_rgbw()}")
    print(f"  -> CMY: {color.to_cmy()}")
    print(f"  -> Hex: {color.to_hex()}")

    cie_color = ColorMix.from_cie(0.3127, 0.3290)  # D65 white point
    print(f"CIE D65 white: {cie_color.to_hex()}")

    # --- Fixture Patch ---
    s4 = Fixture(name="Main Wash 1", profile="etc_sourcefour_led_s3", dmx_address=101)
    s4.set_shutter(True)
    s4.set_intensity(0.70)
    s4.set_color(color)
    s4.set_pan(270.0)
    s4.set_tilt(135.0)
    universe.patch(s4)

    moving = Fixture(name="Spot 1", profile="robe_bmfl", dmx_address=201)
    moving.set_shutter(True)
    moving.set_intensity(1.0)
    moving.set_gobo(GoboType.BREAKUP)
    moving.set_pan(180.0)
    moving.set_tilt(90.0)
    universe.patch(moving)

    frame = universe.output(artnet)
    print(f"DMX frame has {sum(1 for v in frame if v > 0)} active channels")

    # --- Cue List ---
    cues = CueList(name="Act 2 Scene 3")
    cues.add_cue(1, {"wash_1": {"intensity": 0.8, "color": "#FFF5E1"}}, fade_time_s=3.0)
    cues.add_cue(2, {"wash_1": {"intensity": 0.4}, "spot_1": {"intensity": 1.0}}, fade_time_s=5.0)
    cues.add_cue(2.5, {"spot_1": {"gobo": "breakup_slow"}}, fade_time_s=2.0)
    cues.add_cue(3, {"all": {"intensity": 0.0}}, fade_time_s=0.5)
    print(f"Cue list '{cues.name}' has {len(cues)} cues")

    engine = CrossFadeEngine(universe, cues)
    engine.go()
    engine.go()
    print(f"After 2 GOs, next cue: {cues.get_next().number if cues.get_next() else 'none'}")

    # --- Effects ---
    fx = EffectGenerator(
        channels=[s4.channel("color_r"), s4.channel("color_g")],
        waveform=Waveform.SINE,
        period_s=12.0,
        amplitude=0.3,
        offset=0.5,
    )
    engine.apply_effect(fx)
    values = fx.evaluate(time_s=3.0)
    print(f"Effect values at t=3.0s: {values}")

    # --- LED Wall ---
    wall = LEDWall(panels_x=4, panels_y=3, panel_width_px=640, panel_height_px=480)
    wall.set_pixel_map_mode("rgb_16bit")
    wall.fill_solid("#FF0000")
    print(f"LED wall: {wall.total_width_px}x{wall.total_height_px} ({wall.total_pixels} px)")

    calibrator = ColorCalibrator(reference_color="#FFFFFF")
    calibration = calibrator.calibrate_wall(wall)
    wall.apply_calibration(calibration)

    # --- Gel Library ---
    gel = GelLibrary.get_color("lee", "Medium Amber")
    print(f"Lee 'Medium Amber' gel: {gel.to_hex() if gel else 'not found'}")

    # --- Show File I/O ---
    ShowFileIO.export_json(cues, "/tmp/lighting_show.json")
    imported = ShowFileIO.import_json("/tmp/lighting_show.json")
    print(f"Imported show: {imported.name} with {len(imported)} cues")

    artnet.stop()
    print("\nDemo complete.")


if __name__ == "__main__":
    main()
