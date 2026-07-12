"""
Sound Engineering Control System
Mixing console control, speaker optimization, acoustic simulation, wireless coordination,
feedback suppression, spatial audio rendering, and monitor management.
"""

from __future__ import annotations

import logging
import math
import random
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ConsoleProtocol(Enum):
    OSC = "osc"
    MIDI = "midi"
    YAMAHA_CL = "yamaha_cl"
    MIDAS_M32 = "midas_m32"
    ALLEN_HEATH = "allen_heath"
    DIGICO = "digico"


class FrequencyBand(Enum):
    UHF_470_698 = "470-698 MHz"
    VHF_174_216 = "174-216 MHz"
    ISM_900 = "902-928 MHz"


class FilterType(Enum):
    LOW_SHELF = "low_shelf"
    PEAK = "peak"
    HIGH_SHELF = "high_shelf"
    LOW_PASS = "low_pass"
    HIGH_PASS = "high_pass"
    NOTCH = "notch"
    ALL_PASS = "all_pass"


class EasingType(Enum):
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"


class AutoMixMode(Enum):
    GAIN_SHARING = "gain_sharing"
    GATING = "gating"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class EQBand:
    band_id: int
    filter_type: FilterType = FilterType.PEAK
    frequency_hz: float = 1000.0
    gain_db: float = 0.0
    q: float = 1.0

    def compute_coefficients(self, sample_rate: float = 48000.0) -> dict[str, float]:
        """Compute biquad coefficients for this EQ band."""
        A = 10 ** (self.gain_db / 40.0)
        w0 = 2 * math.pi * self.frequency_hz / sample_rate
        alpha = math.sin(w0) / (2 * self.q)
        cos_w0 = math.cos(w0)

        if self.filter_type == FilterType.PEAK:
            b0 = 1 + alpha * A
            b1 = -2 * cos_w0
            b2 = 1 - alpha * A
            a0 = 1 + alpha / A
            a1 = -2 * cos_w0
            a2 = 1 - alpha / A
        elif self.filter_type == FilterType.LOW_SHELF:
            sqrt_A = math.sqrt(A)
            b0 = A * ((A + 1) - (A - 1) * cos_w0 + 2 * sqrt_A * alpha)
            b1 = 2 * A * ((A - 1) - (A + 1) * cos_w0)
            b2 = A * ((A + 1) - (A - 1) * cos_w0 - 2 * sqrt_A * alpha)
            a0 = (A + 1) + (A - 1) * cos_w0 + 2 * sqrt_A * alpha
            a1 = -2 * ((A - 1) + (A + 1) * cos_w0)
            a2 = (A + 1) + (A - 1) * cos_w0 - 2 * sqrt_A * alpha
        elif self.filter_type == FilterType.HIGH_PASS:
            b0 = (1 + cos_w0) / 2
            b1 = -(1 + cos_w0)
            b2 = (1 + cos_w0) / 2
            a0 = 1 + alpha
            a1 = -2 * cos_w0
            a2 = 1 - alpha
        else:
            b0, b1, b2, a0, a1, a2 = 1, 0, 0, 1, 0, 0

        return {"b0": b0 / a0, "b1": b1 / a0, "b2": b2 / a0, "a1": a1 / a0, "a2": a2 / a0}


@dataclass
class DynamicsProcessor:
    threshold_db: float = -20.0
    ratio: float = 4.0
    attack_ms: float = 10.0
    release_ms: float = 100.0
    knee_db: float = 6.0
    makeup_gain_db: float = 0.0

    def compute_gain(self, input_db: float) -> float:
        if input_db < self.threshold_db - self.knee_db / 2:
            return 0.0
        if input_db > self.threshold_db + self.knee_db / 2:
            over = input_db - self.threshold_db
            return -(over * (1 - 1 / self.ratio)) + self.makeup_gain_db
        # Soft knee region
        x = input_db - self.threshold_db + self.knee_db / 2
        return -(x * x / (2 * self.knee_db) * (1 - 1 / self.ratio)) + self.makeup_gain_db


@dataclass
class ChannelConfig:
    channel_id: int
    name: str = ""
    fader_db: float = 0.0
    muted: bool = False
    pan: float = 0.0  # -1.0 (left) to 1.0 (right)
    eq_bands: list[EQBand] = field(default_factory=list)
    dynamics: DynamicsProcessor = field(default_factory=DynamicsProcessor)
    highpass_hz: float = 0.0


@dataclass
class SpeakerBox:
    box_id: int
    sensitivity_db: float = 105.0
    max_spl_db: float = 136.0
    coverage_h_deg: float = 80.0
    coverage_v_deg: float = 50.0
    splay_angle_deg: float = 0.0
    distance_m: float = 0.0
    delay_ms: float = 0.0
    gain_db: float = 0.0


@dataclass
class WirelessChannel:
    number: int
    frequency_mhz: float
    im_margin_db: float = 0.0
    group: int = 0
    active: bool = False


@dataclass
class SoundObject:
    object_id: int
    name: str = ""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    size: float = 0.0
    diffusion: float = 0.0
    gain_db: float = 0.0


@dataclass
class MonitorMix:
    mix_id: int
    performer_name: str = ""
    channels: dict[int, float] = field(default_factory=dict)  # channel -> level_db


# ---------------------------------------------------------------------------
# Mixing Console
# ---------------------------------------------------------------------------

class MixingConsole:
    """Digital mixing console control interface."""

    def __init__(
        self,
        protocol: ConsoleProtocol = ConsoleProtocol.OSC,
        ip: str = "192.168.1.50",
        port: int = 8000,
        console_model: str = "yamaha_cl5",
        num_channels: int = 72,
    ):
        self.protocol = protocol
        self.ip = ip
        self.port = port
        self.console_model = console_model
        self.num_channels = num_channels
        self._connected = False
        self._channels: dict[int, ChannelConfig] = {}
        self._scenes: dict[int, dict[str, Any]] = {}

        for i in range(1, num_channels + 1):
            self._channels[i] = ChannelConfig(channel_id=i, name=f"Ch {i}")

    def connect(self) -> bool:
        logger.info(
            "Connecting to %s at %s:%d via %s",
            self.console_model, self.ip, self.port, self.protocol.value,
        )
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False
        logger.info("Disconnected from console")

    def _ensure_connected(self) -> None:
        if not self._connected:
            raise RuntimeError("Not connected to console")

    def set_channel_fader(self, channel: int, level_db: float) -> None:
        self._ensure_connected()
        level_db = max(-90.0, min(12.0, level_db))
        self._channels[channel].fader_db = level_db
        logger.debug("Channel %d fader: %.1f dB", channel, level_db)

    def set_channel_eq(
        self,
        channel: int,
        band: int,
        freq_hz: float,
        gain_db: float,
        q: float = 1.0,
        filter_type: FilterType = FilterType.PEAK,
    ) -> None:
        self._ensure_connected()
        eq = EQBand(
            band_id=band,
            filter_type=filter_type,
            frequency_hz=freq_hz,
            gain_db=gain_db,
            q=q,
        )
        self._channels[channel].eq_bands.append(eq)
        coeffs = eq.compute_coefficients()
        logger.debug("Channel %d EQ band %d: %.0f Hz, %+.1f dB (Q=%.2f)", channel, band, freq_hz, gain_db, q)

    def set_channel_gate(
        self, channel: int, threshold_db: float = -40.0, ratio: float = 4.0,
    ) -> None:
        self._ensure_connected()
        ch = self._channels[channel]
        ch.dynamics.threshold_db = threshold_db
        ch.dynamics.ratio = ratio
        logger.debug("Channel %d gate: threshold %.1f dB, ratio %.1f:1", channel, threshold_db, ratio)

    def set_channel_compressor(
        self,
        channel: int,
        threshold_db: float = -20.0,
        ratio: float = 3.0,
        attack_ms: float = 10.0,
        release_ms: float = 100.0,
    ) -> None:
        self._ensure_connected()
        ch = self._channels[channel]
        ch.dynamics.threshold_db = threshold_db
        ch.dynamics.ratio = ratio
        ch.dynamics.attack_ms = attack_ms
        ch.dynamics.release_ms = release_ms
        logger.debug(
            "Channel %d compressor: threshold %.1f dB, ratio %.1f:1, attack %.0fms, release %.0fms",
            channel, threshold_db, ratio, attack_ms, release_ms,
        )

    def set_mute(self, channel: int, muted: bool) -> None:
        self._ensure_connected()
        self._channels[channel].muted = muted
        logger.debug("Channel %d mute: %s", channel, muted)

    def set_pan(self, channel: int, position: float) -> None:
        self._ensure_connected()
        position = max(-1.0, min(1.0, position))
        self._channels[channel].pan = position

    def recall_scene(self, scene_number: int) -> bool:
        self._ensure_connected()
        logger.info("Recalling scene %d", scene_number)
        return True

    def store_scene(self, scene_number: int, name: str = "") -> None:
        self._ensure_connected()
        self._scenes[scene_number] = {
            "name": name,
            "channels": {ch: ch_config.fader_db for ch, ch_config in self._channels.items()},
        }
        logger.info("Stored scene %d: %s", scene_number, name)

    def get_channel_config(self, channel: int) -> ChannelConfig:
        return self._channels[channel]


# ---------------------------------------------------------------------------
# Speaker Array
# ---------------------------------------------------------------------------

class SpeakerArray:
    """Line array speaker system design and optimization."""

    SPEED_OF_SOUND = 343.0  # m/s at 20°C

    def __init__(
        self,
        num_boxes: int = 8,
        box_spacing_m: float = 1.0,
        splay_angles_deg: Optional[list[float]] = None,
        box_coverage_h_deg: float = 80.0,
        box_coverage_v_deg: float = 50.0,
        sensitivity_db: float = 105.0,
        max_spl_db: float = 136.0,
    ):
        self.num_boxes = num_boxes
        self.box_spacing_m = box_spacing_m
        self.box_coverage_h_deg = box_coverage_h_deg
        self.box_coverage_v_deg = box_coverage_v_deg
        self.boxes: list[SpeakerBox] = []

        for i in range(num_boxes):
            splay = splay_angles_deg[i] if splay_angles_deg and i < len(splay_angles_deg) else 0.0
            self.boxes.append(SpeakerBox(
                box_id=i + 1,
                sensitivity_db=sensitivity_db,
                max_spl_db=max_spl_db,
                coverage_h_deg=box_coverage_h_deg,
                coverage_v_deg=box_coverage_v_deg,
                splay_angle_deg=splay,
                distance_m=i * box_spacing_m,
            ))

    def calculate_coverage(self) -> dict[str, float]:
        total_splay = sum(b.splay_angle_deg for b in self.boxes)
        top_box_height = self.num_boxes * self.box_spacing_m * math.cos(math.radians(total_splay))
        return {
            "total_splay_deg": total_splay,
            "array_length_m": self.num_boxes * self.box_spacing_m,
            "top_box_height_m": top_box_height,
            "theoretical_coverage_h_deg": self.box_coverage_h_deg,
            "theoretical_coverage_v_deg": self.box_coverage_v_deg + total_splay,
        }

    def calculate_spl_at_distance(self, distance_m: float) -> float:
        if distance_m <= 0:
            return self.boxes[0].max_spl_db
        sensitivity = self.boxes[0].sensitivity_db
        directivity_gain = 10 * math.log10(self.num_boxes)
        spl = sensitivity + directivity_gain - 20 * math.log10(distance_m)
        return spl

    def optimize_delays(self, listener_distance_m: float) -> list[float]:
        delays = []
        nearest_distance = listener_distance_m
        for box in self.boxes:
            path_diff = box.distance_m
            delay_s = path_diff / self.SPEED_OF_SOUND
            delays.append(delay_s * 1000)  # Convert to ms
        return delays


# ---------------------------------------------------------------------------
# Room Simulator
# ---------------------------------------------------------------------------

class RoomSimulator:
    """Acoustic room simulation using image-source and statistical models."""

    def __init__(
        self,
        length_m: float = 30.0,
        width_m: float = 20.0,
        height_m: float = 12.0,
        rt60_target_s: float = 1.4,
        wall_absorption: float = 0.3,
    ):
        self.length_m = length_m
        self.width_m = width_m
        self.height_m = height_m
        self.rt60_target_s = rt60_target_s
        self.wall_absorption = wall_absorption
        self._source_pos = (0.0, 0.0, 1.5)
        self._listener_pos = (length_m / 2, width_m / 2, 1.2)

    def set_source_position(self, x: float, y: float, z: float) -> None:
        self._source_pos = (x, y, z)

    def set_listener_position(self, x: float, y: float, z: float) -> None:
        self._listener_pos = (x, y, z)

    def _image_source_distance(self, order: int, axis: int) -> float:
        room_dim = [self.length_m, self.width_m, self.height_m][axis]
        src = self._source_pos[axis]
        lst = self._listener_pos[axis]
        if order % 2 == 0:
            return abs(lst - src + order * room_dim)
        return abs(lst + src + (order - 1) * room_dim)

    def simulate(self, num_reflections: int = 6) -> dict[str, Any]:
        """Generate a simulated impulse response."""
        direct_dist = math.sqrt(sum((s - l) ** 2 for s, l in zip(self._source_pos, self._listener_pos)))
        direct_time_s = direct_dist / 343.0
        direct_level_db = -20 * math.log10(max(0.1, direct_dist))

        reflections = []
        for order in range(1, num_reflections + 1):
            for axis in range(3):
                dist = self._image_source_distance(order, axis)
                time_s = dist / 343.0
                attenuation = self.wall_absorption ** order
                level_db = -20 * math.log10(max(0.1, dist)) + 10 * math.log10(attenuation)
                reflections.append({"order": order, "axis": axis, "time_s": time_s, "level_db": level_db})

        reflections.sort(key=lambda r: r["time_s"])

        volume = self.length_m * self.width_m * self.height_m
        surface_area = 2 * (
            self.length_m * self.width_m + self.length_m * self.height_m + self.width_m * self.height_m
        )
        sabine_rt60 = 0.161 * volume / (surface_area * self.wall_absorption)

        return {
            "direct_time_s": direct_time_s,
            "direct_level_db": direct_level_db,
            "reflections": reflections[:20],
            "calculated_rt60_s": sabine_rt60,
            "target_rt60_s": self.rt60_target_s,
            "volume_m3": volume,
            "surface_area_m2": surface_area,
        }


# ---------------------------------------------------------------------------
# Delay Aligner
# ---------------------------------------------------------------------------

class DelayAligner:
    """Calculates delay compensation for distributed speaker systems."""

    SPEED_OF_SOUND = 343.0

    def __init__(
        self,
        main_array_distance_m: float,
        delay_tower_distance_m: float,
        speed_of_sound_mps: float = 343.0,
    ):
        self.main_array_distance_m = main_array_distance_m
        self.delay_tower_distance_m = delay_tower_distance_m
        self.speed_of_sound_mps = speed_of_sound_mps

    def calculate_delay(self) -> float:
        time_main = self.main_array_distance_m / self.speed_of_sound_mps
        time_delay = self.delay_tower_distance_m / self.speed_of_sound_mps
        delay_s = time_delay - time_main
        return max(0, delay_s * 1000)

    def calculate_distance_difference(self) -> float:
        return abs(self.delay_tower_distance_m - self.main_array_distance_m)


# ---------------------------------------------------------------------------
# Wireless Frequency Coordinator
# ---------------------------------------------------------------------------

class WirelessCoordinator:
    """RF frequency coordination for wireless microphone systems."""

    def __init__(
        self,
        band: FrequencyBand = FrequencyBand.UHF_470_698,
        num_channels: int = 24,
        intermod_spacing_khz: float = 300.0,
        exclusion_zones: Optional[list[tuple[float, float]]] = None,
    ):
        self.band = band
        self.num_channels = num_channels
        self.intermod_spacing_khz = intermod_spacing_khz
        self.exclusion_zones = exclusion_zones or []
        self._scan_data: list[dict[str, Any]] = []
        self._channels: list[WirelessChannel] = []

    def _get_band_edges(self) -> tuple[float, float]:
        if self.band == FrequencyBand.UHF_470_698:
            return (470.0, 698.0)
        elif self.band == FrequencyBand.VHF_174_216:
            return (174.0, 216.0)
        return (902.0, 928.0)

    def _is_in_exclusion_zone(self, freq_mhz: float) -> bool:
        for low, high in self.exclusion_zones:
            if low <= freq_mhz <= high:
                return True
        return False

    def _check_intermodulation(self, freq_mhz: float, existing: list[float]) -> tuple[bool, float]:
        min_margin = float("inf")
        for other in existing:
            diff_khz = abs(freq_mhz - other) * 1000
            if diff_khz < self.intermod_spacing_khz:
                return False, 0.0
            # Check 3rd order intermod products
            im_product = 2 * freq_mhz - other
            for e2 in existing:
                if abs(im_product - e2) * 1000 < self.intermod_spacing_khz:
                    return False, 0.0
            margin = diff_khz / self.intermod_spacing_khz
            min_margin = min(min_margin, margin)
        return True, min_margin

    def calculate_plan(self) -> "WirelessPlan":
        low, high = self._get_band_edges()
        available = high - low
        step = available / (self.num_channels + 1)
        assigned_freqs = []
        channels = []

        for i in range(self.num_channels):
            freq = low + step * (i + 1)
            if self._is_in_exclusion_zone(freq):
                freq += 10.0
            ok, margin = self._check_intermodulation(freq, assigned_freqs)
            if ok:
                assigned_freqs.append(freq)
                channels.append(WirelessChannel(
                    number=i + 1,
                    frequency_mhz=round(freq, 2),
                    im_margin_db=round(margin * 10, 1),
                    group=(i // 6) + 1,
                    active=True,
                ))

        return WirelessPlan(channels=channels, band=self.band)

    def scan_spectrum(self, duration_s: float = 5.0) -> list[dict[str, Any]]:
        logger.info("Scanning RF spectrum for %.1f seconds", duration_s)
        self._scan_data = [
            {"frequency_mhz": f, "level_dbm": random.uniform(-90, -40)}
            for f in range(470, 700, 1)
        ]
        return self._scan_data

    def recalculate_with_scan(self) -> "WirelessPlan":
        if not self._scan_data:
            return self.calculate_plan()
        occupied = [d["frequency_mhz"] for d in self._scan_data if d["level_dbm"] > -60]
        for freq in occupied:
            self.exclusion_zones.append((freq - 0.5, freq + 0.5))
        return self.calculate_plan()


@dataclass
class WirelessPlan:
    channels: list[WirelessChannel]
    band: FrequencyBand

    @property
    def active_count(self) -> int:
        return sum(1 for ch in self.channels if ch.active)

    @property
    def min_im_margin(self) -> float:
        margins = [ch.im_margin_db for ch in self.channels if ch.active]
        return min(margins) if margins else 0.0


# ---------------------------------------------------------------------------
# Feedback Suppressor
# ---------------------------------------------------------------------------

class FeedbackSuppressor:
    """Adaptive notch filter-based feedback suppression."""

    def __init__(self, num_filters: int = 8, sample_rate: float = 48000.0):
        self.num_filters = num_filters
        self.sample_rate = sample_rate
        self._active_filters: list[dict[str, float]] = []
        self._threshold_db = -40.0

    def detect_feedback(self, spectrum: list[float], freq_resolution_hz: float) -> list[dict[str, float]]:
        detected = []
        for i, level in enumerate(spectrum):
            if level > self._threshold_db:
                freq = i * freq_resolution_hz
                existing = any(abs(f["frequency_hz"] - freq) < 20 for f in self._active_filters)
                if not existing and len(self._active_filters) < self.num_filters:
                    notch = {
                        "frequency_hz": freq,
                        "gain_db": -12.0,
                        "q": 30.0,
                        "level_db": level,
                    }
                    self._active_filters.append(notch)
                    detected.append(notch)
                    logger.warning("Feedback detected at %.1f Hz (%.1f dB)", freq, level)
        return detected

    def get_notch_filters(self) -> list[dict[str, float]]:
        return list(self._active_filters)

    def clear_filters(self) -> None:
        self._active_filters.clear()

    def set_threshold(self, threshold_db: float) -> None:
        self._threshold_db = threshold_db


# ---------------------------------------------------------------------------
# Spatial Renderer
# ---------------------------------------------------------------------------

@dataclass
class AtmosConfig:
    num_objects: int = 16
    bed_channels: int = 7
    speaker_layout: str = "7.1.4"
    renderer_ip: str = "192.168.1.60"


class SpatialRenderer:
    """Spatial audio renderer for Dolby Atmos and immersive formats."""

    def __init__(self, config: AtmosConfig):
        self.config = config
        self._connected = False
        self._objects: dict[int, SoundObject] = {}
        self._animation_queue: list[dict[str, Any]] = []

    def connect(self) -> bool:
        logger.info(
            "Connecting to spatial renderer at %s (%s, %d objects)",
            self.config.renderer_ip, self.config.speaker_layout, self.config.num_objects,
        )
        self._connected = True
        return True

    def place_object(self, obj: SoundObject) -> None:
        self._objects[obj.object_id] = obj
        logger.debug(
            "Placed object '%s' at (%.2f, %.2f, %.2f) size=%.2f",
            obj.name, obj.x, obj.y, obj.z, obj.size,
        )

    def move_object(self, object_id: int, x: float, y: float, z: float) -> None:
        if object_id in self._objects:
            self._objects[object_id].x = x
            self._objects[object_id].y = y
            self._objects[object_id].z = z

    def remove_object(self, object_id: int) -> None:
        self._objects.pop(object_id, None)

    def animate_object(
        self,
        object_id: int,
        path: list[tuple[float, float, float]],
        duration_s: float,
        easing: str = "linear",
    ) -> None:
        self._animation_queue.append({
            "object_id": object_id,
            "path": path,
            "duration_s": duration_s,
            "easing": easing,
        })
        logger.info(
            "Animated object %d along %d-point path over %.1fs (%s)",
            object_id, len(path), duration_s, easing,
        )

    def get_object_positions(self) -> dict[int, tuple[float, float, float]]:
        return {oid: (o.x, o.y, o.z) for oid, o in self._objects.items()}


# ---------------------------------------------------------------------------
# Auto Mixer
# ---------------------------------------------------------------------------

class AutoMixer:
    """Automatic mixing for multi-microphone setups."""

    def __init__(self, num_channels: int = 8, mode: AutoMixMode = AutoMixMode.GAIN_SHARING):
        self.num_channels = num_channels
        self.mode = mode
        self._gains: list[float] = [0.0] * num_channels
        self._threshold_db: float = -50.0

    def process(self, input_levels_db: list[float]) -> list[float]:
        if len(input_levels_db) != self.num_channels:
            raise ValueError(f"Expected {self.num_channels} levels, got {len(input_levels_db)}")

        if self.mode == AutoMixMode.GAIN_SHARING:
            total = sum(10 ** (lvl / 20) for lvl in input_levels_db)
            if total == 0:
                self._gains = [0.0] * self.num_channels
            else:
                self._gains = [
                    20 * math.log10(max(1e-10, 10 ** (lvl / 20) / total))
                    for lvl in input_levels_db
                ]
        elif self.mode == AutoMixMode.GATING:
            max_level = max(input_levels_db)
            for i, lvl in enumerate(input_levels_db):
                if lvl > max_level - 6:
                    self._gains[i] = 0.0
                else:
                    self._gains[i] = -20.0

        return list(self._gains)


# ---------------------------------------------------------------------------
# Monitor Mix Manager
# ---------------------------------------------------------------------------

class MonitorMixManager:
    """Manages individual monitor mixes for performers."""

    def __init__(self, num_mixes: int = 12, num_channels: int = 48):
        self.num_mixes = num_mixes
        self.num_channels = num_channels
        self._mixes: dict[int, MonitorMix] = {
            i: MonitorMix(mix_id=i, performer_name=f"Performer {i}")
            for i in range(1, num_mixes + 1)
        }

    def set_mix_level(self, mix_id: int, channel: int, level_db: float) -> None:
        if mix_id not in self._mixes:
            raise ValueError(f"Mix {mix_id} not found")
        self._mixes[mix_id].channels[channel] = level_db
        logger.debug("Monitor mix %d, channel %d: %.1f dB", mix_id, channel, level_db)

    def set_performer_name(self, mix_id: int, name: str) -> None:
        self._mixes[mix_id].performer_name = name

    def get_mix(self, mix_id: int) -> MonitorMix:
        return self._mixes[mix_id]

    def create_default_mix(self, mix_id: int, vocal_channels: list[int], level_db: float = 0.0) -> None:
        for ch in range(1, self.num_channels + 1):
            if ch in vocal_channels:
                self.set_mix_level(mix_id, ch, level_db)
            else:
                self.set_mix_level(mix_id, ch, -12.0)


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("=" * 60)
    print("  Sound Engineering Control System — Demo")
    print("=" * 60)

    # --- Mixing Console ---
    console = MixingConsole(
        protocol=ConsoleProtocol.OSC,
        ip="192.168.1.50",
        console_model="yamaha_cl5",
    )
    console.connect()
    console.set_channel_fader(channel=1, level_db=-6.0)
    console.set_channel_eq(channel=1, band=1, freq_hz=80, gain_db=3.0, q=0.7)
    console.set_channel_compressor(channel=1, threshold_db=-20, ratio=3.0)
    console.set_mute(channel=1, muted=False)
    console.store_scene(scene_number=1, name="Opening Numbers")
    console.recall_scene(scene_number=1)
    ch1 = console.get_channel_config(1)
    print(f"Channel 1: fader={ch1.fader_db}dB, muted={ch1.muted}")

    # --- EQ Coefficients ---
    eq = EQBand(band_id=1, filter_type=FilterType.PEAK, frequency_hz=1000, gain_db=6.0, q=1.0)
    coeffs = eq.compute_coefficients()
    print(f"EQ coefficients: b0={coeffs['b0']:.4f}, a1={coeffs['a1']:.4f}")

    # --- Dynamics ---
    comp = DynamicsProcessor(threshold_db=-20, ratio=4.0)
    gain = comp.compute_gain(input_db=-10)
    print(f"Compressor gain at -10 dB input: {gain:.2f} dB")

    # --- Speaker Array ---
    array = SpeakerArray(
        num_boxes=8, box_spacing_m=1.0,
        splay_angles_deg=[0, 3, 5, 7, 9, 11, 14, 17],
        sensitivity_db=105, max_spl_db=136,
    )
    coverage = array.calculate_coverage()
    print(f"Array coverage: {coverage}")
    spl = array.calculate_spl_at_distance(distance_m=20)
    print(f"SPL at 20m: {spl:.1f} dB")

    # --- Room Simulation ---
    room = RoomSimulator(length_m=30, width_m=20, height_m=12, rt60_target_s=1.4)
    room.set_source_position(0, 0, 1.5)
    room.set_listener_position(20, 0, 1.2)
    ir = room.simulate(num_reflections=6)
    print(f"Direct time: {ir['direct_time_s']:.3f}s, RT60: {ir['calculated_rt60_s']:.2f}s")

    # --- Delay Alignment ---
    aligner = DelayAligner(main_array_distance_m=15, delay_tower_distance_m=25)
    delay = aligner.calculate_delay()
    print(f"Delay tower compensation: {delay:.2f} ms")

    # --- Wireless Coordination ---
    coord = WirelessCoordinator(
        band=FrequencyBand.UHF_470_698, num_channels=24,
        intermod_spacing_khz=300, exclusion_zones=[(512, 524)],
    )
    plan = coord.calculate_plan()
    print(f"Wireless plan: {plan.active_count} channels, min IM margin: {plan.min_im_margin:.1f} dB")

    # --- Feedback Suppressor ---
    fb = FeedbackSuppressor(num_filters=8)
    spectrum = [-70.0] * 100
    spectrum[45] = -30.0  # Simulated feedback peak
    detected = fb.detect_feedback(spectrum, freq_resolution_hz=100)
    print(f"Feedback detected: {len(detected)} frequencies")

    # --- Spatial Renderer ---
    atmos = AtmosConfig(num_objects=16, speaker_layout="7.1.4")
    renderer = SpatialRenderer(atmos)
    renderer.connect()
    rain = SoundObject(object_id=1, name="rain", x=0.3, y=-0.2, z=0.8, size=0.4)
    renderer.place_object(rain)
    renderer.animate_object(1, [(0.3, -0.2, 0.8), (0, 0, 1.0), (-0.3, 0.2, 0.8)], duration_s=10)
    print(f"Spatial objects: {renderer.get_object_positions()}")

    # --- Auto Mixer ---
    auto = AutoMixer(num_channels=4, mode=AutoMixMode.GAIN_SHARING)
    gains = auto.process([-20, -40, -35, -50])
    print(f"Auto-mix gains: {[f'{g:.1f}' for g in gains]} dB")

    # --- Monitor Mixes ---
    monitors = MonitorMixManager(num_mixes=8, num_channels=48)
    monitors.set_performer_name(1, "Lead Vocal")
    monitors.create_default_mix(1, vocal_channels=[1, 2], level_db=0.0)
    mix1 = monitors.get_mix(1)
    print(f"Monitor 1 ({mix1.performer_name}): {len(mix1.channels)} channels set")

    console.disconnect()
    print("\nDemo complete.")


if __name__ == "__main__":
    main()
