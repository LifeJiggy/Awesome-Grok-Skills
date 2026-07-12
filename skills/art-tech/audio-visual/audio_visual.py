"""
Audio-Visual Module — Audio analysis, audio-reactive visuals, DMX lighting control,
MIDI mapping, and live performance engine for audio-visual synchronization.
"""

from __future__ import annotations

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


class VisualMode(Enum):
    SPECTRUM = "spectrum"
    WAVEFORM = "waveform"
    CIRCLE = "circle"
    PARTICLES = "particles"
    MESH = "mesh"
    FRACTAL = "fractal"


class DMXOutputMode(Enum):
    CONTINUOUS = "continuous"
    ON_BEAT = "on_beat"
    ONSET = "onset"


class MIDIMappingType(Enum):
    CC = "cc"
    NOTE = "note"
    PITCHBEND = "pitchbend"
    VELOCITY = "velocity"


@dataclass
class FrequencyBands:
    sub_bass: float = 0.0
    bass: float = 0.0
    low_mid: float = 0.0
    mid: float = 0.0
    high_mid: float = 0.0
    presence: float = 0.0
    brilliance: float = 0.0
    treble: float = 0.0
    volume: float = 0.0
    peak: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return {k: round(v, 3) for k, v in self.__dict__.items()}

    @property
    def energy(self) -> float:
        return (self.sub_bass + self.bass + self.mid + self.treble) / 4


@dataclass
class AudioAnalysis:
    timestamp: float = 0.0
    tempo_bpm: float = 120.0
    key: str = "C"
    mode: str = "major"
    loudness_lufs: float = -14.0
    bands: FrequencyBands = field(default_factory=FrequencyBands)
    beat_detected: bool = False
    onset_detected: bool = False
    spectral_centroid: float = 0.0
    spectral_rolloff: float = 0.0
    zero_crossing_rate: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bpm": round(self.tempo_bpm, 1),
            "key": self.key,
            "loudness": round(self.loudness_lufs, 1),
            "beat": self.beat_detected,
            "bands": self.bands.to_dict(),
        }


@dataclass
class VisualPreset:
    preset_id: str
    name: str
    mode: VisualMode
    color_palette: List[Tuple[int, int, int]]
    sensitivity: Dict[str, float] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
    blend_time_s: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.preset_id, "name": self.name, "mode": self.mode.value}


@dataclass
class DMXChannel:
    channel: int
    value: int = 0
    label: str = ""
    mode: DMXOutputMode = DMXOutputMode.CONTINUOUS


@dataclass
class MIDIMapping:
    mapping_id: str
    input_type: MIDIMappingType
    input_channel: int
    target_parameter: str
    min_val: float = 0.0
    max_val: float = 1.0
    smoothing: float = 0.1

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.mapping_id, "type": self.input_type.value, "channel": self.input_channel, "target": self.target_parameter}


@dataclass
class VisualFrame:
    frame_id: str
    width: int
    height: int
    audio_analysis: AudioAnalysis
    visual_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {"frame": self.frame_id, "resolution": f"{self.width}x{self.height}", "bpm": round(self.audio_analysis.tempo_bpm, 1)}


class AudioAnalyzer:
    def __init__(self, source: str = "system_audio", fft_size: int = 2048, sample_rate: int = 44100):
        self.source = source
        self.fft_size = fft_size
        self.sample_rate = sample_rate
        self._beat_history: List[float] = []
        self._tempo_estimate: float = 120.0

    def analyze(self) -> AudioAnalysis:
        import random
        bands = FrequencyBands(
            sub_bass=random.uniform(0, 1), bass=random.uniform(0, 1),
            low_mid=random.uniform(0, 0.8), mid=random.uniform(0, 0.9),
            high_mid=random.uniform(0, 0.7), presence=random.uniform(0, 0.6),
            brilliance=random.uniform(0, 0.5), treble=random.uniform(0, 0.5),
            volume=random.uniform(0.3, 0.9), peak=random.uniform(0.5, 1.0),
        )
        beat = random.random() > 0.85
        if beat:
            self._beat_history.append(time.time())
            if len(self._beat_history) > 10:
                self._beat_history = self._beat_history[-10:]
            if len(self._beat_history) >= 4:
                intervals = [self._beat_history[i+1] - self._beat_history[i]
                            for i in range(len(self._beat_history)-1)]
                avg_interval = sum(intervals) / len(intervals)
                self._tempo_estimate = 60.0 / avg_interval if avg_interval > 0 else 120

        keys = ["C", "D", "E", "F", "G", "A", "B"]
        return AudioAnalysis(
            timestamp=time.time(),
            tempo_bpm=self._tempo_estimate + random.uniform(-2, 2),
            key=random.choice(keys),
            mode=random.choice(["major", "minor"]),
            loudness_lufs=random.uniform(-20, -8),
            bands=bands,
            beat_detected=beat,
            onset_detected=random.random() > 0.9,
            spectral_centroid=random.uniform(500, 3000),
        )


class VisualGenerator:
    def __init__(self, resolution: Tuple[int, int] = (1920, 1080), output: str = "ndi"):
        self.resolution = resolution
        self.output = output
        self._mode = VisualMode.SPECTRUM
        self._palette: List[Tuple[int, int, int]] = [(255, 50, 50), (50, 100, 255)]
        self._sensitivity: Dict[str, float] = {"bass": 1.0, "mid": 1.0, "treble": 1.0}
        self._current_preset: Optional[VisualPreset] = None

    def set_mode(self, mode: str) -> None:
        self._mode = VisualMode(mode)

    def set_color_palette(self, colors: List[Tuple[int, int, int]]) -> None:
        self._palette = colors

    def set_sensitivity(self, bass: float = 1.0, mid: float = 1.0, treble: float = 1.0) -> None:
        self._sensitivity = {"bass": bass, "mid": mid, "treble": treble}

    def generate_frame(self, analysis: AudioAnalysis) -> VisualFrame:
        visual_data = {"mode": self._mode.value, "palette": self._palette}
        if self._mode == VisualMode.SPECTRUM:
            visual_data["bars"] = [
                {"freq": i, "amplitude": getattr(analysis.bands, band, 0) * self._sensitivity.get("bass", 1)}
                for i, band in enumerate(["sub_bass", "bass", "low_mid", "mid", "high_mid", "presence", "brilliance", "treble"])
            ]
        elif self._mode == VisualMode.WAVEFORM:
            visual_data["waveform"] = [random.uniform(-1, 1) for _ in range(256)]
        elif self._mode == VisualMode.PARTICLES:
            visual_data["particle_count"] = int(analysis.bands.energy * 500)
            visual_data["particle_speed"] = analysis.bands.volume * 2

        return VisualFrame(
            frame_id=f"VF-{uuid.uuid4().hex[:8]}",
            width=self.resolution[0], height=self.resolution[1],
            audio_analysis=analysis, visual_data=visual_data,
        )

    def load_preset(self, preset: VisualPreset) -> None:
        self._current_preset = preset
        self._mode = preset.mode
        self._palette = preset.color_palette

    def save_preset(self, name: str) -> VisualPreset:
        preset = VisualPreset(
            preset_id=f"VP-{uuid.uuid4().hex[:6]}", name=name,
            mode=self._mode, color_palette=list(self._palette),
            sensitivity=dict(self._sensitivity),
        )
        return preset


class DMXController:
    def __init__(self, port: str = "", universe: int = 1, channel_count: int = 512):
        self.port = port
        self.universe = universe
        self.channel_count = channel_count
        self._channels: Dict[int, DMXChannel] = {}
        self._buffer: List[int] = [0] * channel_count

    def set_channel(self, channel: int, value: int, label: str = "") -> None:
        value = max(0, min(255, value))
        self._channels[channel] = DMXChannel(channel=channel, value=value, label=label)
        self._buffer[channel - 1] = value

    def set_from_audio(self, channel: int, band_value: float, mode: DMXOutputMode = DMXOutputMode.CONTINUOUS) -> None:
        self.set_channel(channel, int(band_value * 255))
        if channel in self._channels:
            self._channels[channel].mode = mode

    def flush(self) -> None:
        pass  # In production: send DMX frame to hardware

    def blackout(self) -> None:
        self._buffer = [0] * self.channel_count
        self._channels.clear()

    def get_status(self) -> Dict[str, Any]:
        return {"universe": self.universe, "active_channels": len(self._channels), "port": self.port}


class MIDI_Mapper:
    def __init__(self):
        self._mappings: List[MIDIMapping] = []
        self._values: Dict[str, float] = {}

    def map_cc(self, cc: int, target: str, min_val: float = 0, max_val: float = 1, smoothing: float = 0.1) -> MIDIMapping:
        mapping = MIDIMapping(
            mapping_id=f"MIDI-{uuid.uuid4().hex[:6]}",
            input_type=MIDIMappingType.CC, input_channel=cc,
            target_parameter=target, min_val=min_val, max_val=max_val, smoothing=smoothing,
        )
        self._mappings.append(mapping)
        return mapping

    def map_note(self, note: int, target: str) -> MIDIMapping:
        mapping = MIDIMapping(
            mapping_id=f"MIDI-{uuid.uuid4().hex[:6]}",
            input_type=MIDIMappingType.NOTE, input_channel=note,
            target_parameter=target,
        )
        self._mappings.append(mapping)
        return mapping

    def process_cc(self, cc: int, value: int) -> Optional[str]:
        for mapping in self._mappings:
            if mapping.input_type == MIDIMappingType.CC and mapping.input_channel == cc:
                normalized = value / 127.0
                mapped = mapping.min_val + normalized * (mapping.max_val - mapping.min_val)
                self._values[mapping.target_parameter] = mapped
                return mapping.target_parameter
        return None

    def get_value(self, parameter: str) -> float:
        return self._values.get(parameter, 0.0)

    def get_all_mappings(self) -> List[MIDIMapping]:
        return list(self._mappings)


class PerformanceEngine:
    def __init__(self, fps: int = 60):
        self.fps = fps
        self._analyzers: List[AudioAnalyzer] = []
        self._visuals: List[VisualGenerator] = []
        self._dmx_controllers: List[DMXController] = []
        self._midi_mappers: List[MIDI_Mapper] = []
        self._running = False
        self._frame_count = 0

    def add_analyzer(self, analyzer: AudioAnalyzer) -> None:
        self._analyzers.append(analyzer)

    def add_visual(self, visual: VisualGenerator) -> None:
        self._visuals.append(visual)

    def add_dmx(self, dmx: DMXController) -> None:
        self._dmx_controllers.append(dmx)

    def add_midi(self, midi: MIDI_Mapper) -> None:
        self._midi_mappers.append(midi)

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running

    def process_frame(self) -> List[VisualFrame]:
        frames = []
        for analyzer in self._analyzers:
            analysis = analyzer.analyze()
            for visual in self._visuals:
                frame = visual.generate_frame(analysis)
                frames.append(frame)
            for dmx in self._dmx_controllers:
                dmx.set_from_audio(1, analysis.bands.bass)
                dmx.set_from_audio(2, analysis.bands.mid)
                dmx.set_from_audio(3, analysis.bands.treble)
                dmx.flush()
            self._frame_count += 1
        return frames


def main():
    print("Audio-Visual Toolkit")
    print("=" * 60)

    analyzer = AudioAnalyzer(source="system_audio", fft_size=2048)
    analysis = analyzer.analyze()
    print(f"BPM: {analysis.tempo_bpm:.1f}, Key: {analysis.key}, Loudness: {analysis.loudness_lufs:.1f} LUFS")
    print(f"Bands: {analysis.bands.to_dict()}")

    visual = VisualGenerator(resolution=(1920, 1080))
    visual.set_mode("spectrum")
    frame = visual.generate_frame(analysis)
    print(f"\nVisual frame: {frame.to_dict()}")

    preset = visual.save_preset("default_spectrum")
    print(f"Preset: {preset.to_dict()}")

    dmx = DMXController(port="/dev/ttyUSB0", universe=1)
    dmx.set_from_audio(1, analysis.bands.bass)
    dmx.set_from_audio(2, analysis.bands.mid)
    dmx.set_from_audio(3, analysis.bands.treble)
    dmx.flush()
    print(f"\nDMX: {dmx.get_status()}")

    midi = MIDI_Mapper()
    midi.map_cc(1, "visual.brightness", min_val=0.0, max_val=1.0)
    midi.map_note(60, "visual.preset_next")
    midi.process_cc(1, 100)
    print(f"MIDI brightness: {midi.get_value('visual.brightness'):.2f}")

    engine = PerformanceEngine(fps=60)
    engine.add_analyzer(analyzer)
    engine.add_visual(visual)
    engine.add_dmx(dmx)
    engine.add_midi(midi)
    engine.start()
    frames = engine.process_frame()
    print(f"\nPerformance: {len(frames)} frames rendered")


if __name__ == "__main__":
    main()
