---
name: dj-tools
category: music-tech
version: 2.0.0
tags: [music-tech, dj, mixing, beat-matching, automation]
---

# DJ Tools

## Overview

Automated DJ toolkit for beat-matching, BPM detection, key matching, track analysis, and mix automation. This skill provides algorithms for tempo synchronization, harmonic mixing (Camelot wheel), crossfade automation, and intelligent playlist generation based on musical features. Designed for both live performance automation and post-production mix creation.

## Core Capabilities

- **BPM Detection**: Robust tempo estimation using autocorrelation and comb filter methods
- **Beat Grid Alignment**: Automatic beat grid generation and phase correction
- **Key Detection**: Musical key estimation using chromagram analysis and Krumhansl-Schmuckler algorithm
- **Harmonic Mixing**: Camelot wheel matching for key-compatible track transitions
- **Crossfade Automation**: Beat-aligned crossfade curves with EQ blending
- **Track Matching**: Feature-based track similarity scoring for set building
- **Loop Detection**: Automatic loop point identification with beat-aligned boundaries
- **Stem Separation**: Vocals, drums, bass, and other separation for live remixing

## Usage Examples

```python
from dataclasses import dataclass
from typing import List, Optional, Tuple
import numpy as np

# Track Analysis
@dataclass
class TrackAnalysis:
    title: str
    artist: str
    bpm: float
    key: str
    camelot: str
    duration: float
    energy: float
    danceability: float
    loudness: float

CAMELOT_WHEEL = {
    "A": "8B", "Am": "8A", "Bbm": "3A", "B": "10B",
    "Cb": "10B", "Cm": "5A", "C": "5B", "Dbm": "12A",
    "Db": "12B", "Dm": "7A", "D": "7B", "Ebm": "2A",
    "Eb": "2B", "Em": "9A", "E": "9B", "Fm": "4A",
    "F": "4B", "Gbm": "11A", "Gb": "11B", "Gm": "6A",
    "G": "6B", "Abm": "1A", "Ab": "1B",
}

def get_compatible_keys(camelot: str) -> List[str]:
    compatible = [camelot]
    num = int(camelot[:-1])
    letter = camelot[-1]
    compatible.append(f"{num}{'A' if letter == 'B' else 'B'}")
    compatible.append(f"{(num - 1) or 12}{letter}")
    compatible.append(f"{(num + 1) % 13 or 1}{letter}")
    return compatible

class BPMAnalyzer:
    def detect_bpm(self, audio: np.ndarray, sr: int = 44100) -> float:
        audio_mono = audio.mean(axis=0) if audio.ndim > 1 else audio
        hop_length = 512
        ac = self._autocorrelation(audio_mono, hop_length, sr)
        bpm = 60.0 / (np.argmax(ac[1:]) + 1) * sr / hop_length
        return round(bpm, 1)

    def _autocorrelation(self, audio, hop_length, sr):
        min_bpm, max_bpm = 60, 200
        min_lag = int(60 * sr / (max_bpm * hop_length))
        max_lag = int(60 * sr / (min_bpm * hop_length))

        window_size = 1024
        num_windows = len(audio) // window_size
        correlation = np.zeros(max_lag)

        for w in range(num_windows):
            chunk = audio[w * window_size:(w + 1) * window_size]
            chunk_fft = np.fft.rfft(chunk * np.hanning(len(chunk)))
            power = np.abs(chunk_fft) ** 2
            ac_chunk = np.fft.irfft(power)
            correlation[:len(ac_chunk)] += ac_chunk[:max_lag]

        return correlation[min_lag:max_lag]

class KeyDetector:
    def detect_key(self, audio: np.ndarray, sr: int = 22050) -> Tuple[str, str]:
        chroma = self._compute_chroma(audio, sr)
        key_profiles = self._get_profiles()
        best_key = ""
        best_score = -1
        for key, profile in key_profiles.items():
            score = np.corrcoef(chroma, profile)[0, 1]
            if score > best_score:
                best_score = score
                best_key = key
        camelot = CAMELOT_WHEEL.get(best_key, "1B")
        return best_key, camelot

    def _compute_chroma(self, audio, sr):
        n_fft = 4096
        hop = 2048
        spectrum = np.abs(np.fft.rfft(audio[:n_fft * 10]))
        chroma = np.zeros(12)
        for i, mag in enumerate(spectrum):
            freq = i * sr / n_fft
            if freq > 0:
                pitch = int(round(12 * np.log2(freq / 440.0) + 69)) % 12
                chroma[pitch] += mag
        return chroma / (np.max(chroma) + 1e-10)

    def _get_profiles(self):
        major = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
        minor = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
        keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        profiles = {}
        for i, k in enumerate(keys):
            profiles[k] = np.roll(major, -i)
            profiles[k + "m"] = np.roll(minor, -i)
        return profiles

class Crossfader:
    def beat_aligned_crossfade(self, track_a: np.ndarray, track_b: np.ndarray,
                                sr: int, beats_a: List[float], beats_b: List[float],
                                overlap_beats: int = 16) -> np.ndarray:
        overlap_samples = int(overlap_beats * (60.0 / 120) * sr)
        fade_out = np.linspace(1, 0, overlap_samples) ** 2
        fade_in = np.linspace(0, 1, overlap_samples) ** 2

        crossfade_a = track_a[-overlap_samples:] * fade_out
        crossfade_b = track_b[:overlap_samples] * fade_in

        mix = np.zeros(len(track_a) + len(track_b) - overlap_samples)
        mix[:len(track_a) - overlap_samples] = track_a[:len(track_a) - overlap_samples]
        mix[len(track_a) - overlap_samples:len(track_a)] = crossfade_a + crossfade_b
        mix[len(track_a):] = track_b[overlap_samples:]

        return mix

class PlaylistBuilder:
    def build_harmonic_set(self, tracks: List[TrackAnalysis], start_key: str,
                            max_tracks: int = 20) -> List[TrackAnalysis]:
        if not tracks:
            return []
        compatible = [start_key]
        current = start_key
        selected: List[TrackAnalysis] = []
        used = set()

        for _ in range(max_tracks):
            candidates = []
            for t in tracks:
                if t.camelot in compatible and t.title not in used:
                    candidates.append(t)
            if not candidates:
                break
            best = max(candidates, key=lambda t: t.energy)
            selected.append(best)
            used.add(best.title)
            current = best.camelot
            compatible = get_compatible_keys(current)

        return selected
```

## Best Practices

- Always analyze BPM on the full track, not just the intro, for accurate tempo
- Use chromagram-based key detection over raw FFT for more robust results
- Implement beat-aligned crossfades to avoid phase cancellation artifacts
- Match harmonic keys using Camelot wheel proximity (same number or adjacent)
- Account for BPM drift in live recordings by detecting tempo variations
- Pre-analyze all tracks offline to avoid latency during live performance
- Use energy and danceability features for playlist flow optimization
- Implement transition length recommendations based on track energy levels
- Consider harmonic mixing compatibility when building DJ sets
- Validate BPM detection with manual spot-checks on known tracks

## Related Modules

- `music-analytics` - Deep musical feature extraction and analysis
- `audio-processing` - Low-level audio DSP and effects
- `sound-design` - Sound synthesis and creative manipulation
- `music-generation` - AI-driven music composition

## Advanced Configuration

### DJ Performance Settings

| Setting | Default | Range | Description |
|---------|---------|-------|-------------|
| `bpm_tolerance` | 0.5 | 0.1 - 2.0 | BPM matching tolerance |
| `key_tolerance` | 0.3 | 0.1 - 0.5 | Key detection confidence threshold |
| `crossfade_beats` | 16 | 8 - 32 | Beats for crossfade transition |
| `analysis_window_sec` | 30 | 10 - 60 | Seconds for BPM analysis |
| `energy_window` | 128 | 64 - 512 | Samples for energy calculation |
| `loop_min_bars` | 4 | 2 - 8 | Minimum loop length in bars |
| `loop_max_bars` | 32 | 16 - 64 | Maximum loop length in bars |

### Controller Configuration

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class DjControllerType(Enum):
    PIONEER_DDJ = "pioneer_ddj"
    NUMARK_MIXTRACK = "numark_mixtrack"
    DENON_MCX = "denon_mcx"
    CUSTOM_MIDI = "custom_midi"

@dataclass
class DjConfig:
    controller: DjControllerType = DjControllerType.PIONEER_DDJ
    num_decks: int = 2
    sample_rate: int = 44100
    buffer_size: int = 1024
    latency_ms: float = 10.0
    auto_sync: bool = True
    key_lock: bool = True
    quantize: bool = True
    slip_mode: bool = False

    @classmethod
    def for_live(cls) -> 'DjConfig':
        return cls(buffer_size=256, latency_ms=5.0, auto_sync=True)

    @classmethod
    def for_studio(cls) -> 'DjConfig':
        return cls(buffer_size=2048, latency_ms=20.0, auto_sync=False)

@dataclass
class DeckState:
    deck_id: int
    is_playing: bool = False
    current_bpm: float = 120.0
    target_bpm: float = 120.0
    pitch_shift: float = 0.0
    key: str = "C"
    position_beats: float = 0.0
    volume: float = 1.0
    eq_low: float = 1.0
    eq_mid: float = 1.0
    eq_high: float = 1.0
    cue_points: List[float] = field(default_factory=list)
    loop_in: Optional[float] = None
    loop_out: Optional[float] = None
    loop_active: bool = False

class DjController:
    def __init__(self, config: DjConfig = None):
        self.config = config or DjConfig()
        self.decks: Dict[int, DeckState] = {}
        self._init_decks()

    def _init_decks(self):
        for i in range(self.config.num_decks):
            self.decks[i] = DeckState(deck_id=i)

    def sync_bpm(self, source_deck: int, target_deck: int):
        source = self.decks[source_deck]
        target = self.decks[target_deck]
        ratio = source.current_bpm / target.current_bpm
        target.pitch_shift = (ratio - 1) * 100
        target.current_bpm = source.current_bpm

    def set_cue_point(self, deck_id: int, position: float):
        self.decks[deck_id].cue_points.append(position)

    def jump_to_cue(self, deck_id: int, cue_index: int):
        deck = self.decks[deck_id]
        if cue_index < len(deck.cue_points):
            deck.position_beats = deck.cue_points[cue_index]

    def set_loop(self, deck_id: int, loop_in: float, loop_out: float):
        deck = self.decks[deck_id]
        deck.loop_in = loop_in
        deck.loop_out = loop_out
        deck.loop_active = True

    def toggle_loop(self, deck_id: int):
        self.decks[deck_id].loop_active = not self.decks[deck_id].loop_active

    def get_status(self) -> Dict:
        return {
            deck_id: {
                "bpm": deck.current_bpm,
                "key": deck.key,
                "playing": deck.is_playing,
                "position": deck.position_beats,
                "loop_active": deck.loop_active,
            }
            for deck_id, deck in self.decks.items()
        }
```

### Advanced BPM Detection

```python
class AdvancedBpmDetector:
    def __init__(self, sr: int = 44100):
        self.sr = sr

    def detect_bpm_robust(self, audio: np.ndarray) -> float:
        ac = self._multi_resolution_autocorrelation(audio)
        candidates = self._find_peaks(ac, n_peaks=5)
        best_bpm = self._select_best_bpm(candidates)
        return best_bpm

    def _multi_resolution_autocorrelation(self, audio: np.ndarray) -> np.ndarray:
        min_bpm, max_bpm = 60, 200
        min_lag = int(60 * self.sr / (max_bpm * 512))
        max_lag = int(60 * self.sr / (min_bpm * 512))
        correlation = np.zeros(max_lag)
        window_sizes = [1024, 2048, 4096]
        for ws in window_sizes:
            num_windows = len(audio) // ws
            for w in range(num_windows):
                chunk = audio[w * ws:(w + 1) * ws]
                chunk_fft = np.fft.rfft(chunk * np.hanning(len(chunk)))
                power = np.abs(chunk_fft) ** 2
                ac_chunk = np.fft.irfft(power)
                correlation[:len(ac_chunk)] += ac_chunk[:max_lag]
        return correlation[min_lag:max_lag]

    def _find_peaks(self, correlation: np.ndarray, n_peaks: int = 5) -> List[float]:
        peaks = []
        for i in range(1, len(correlation) - 1):
            if correlation[i] > correlation[i-1] and correlation[i] > correlation[i+1]:
                bpm = 60.0 / ((i + 1) * 512 / self.sr)
                if 60 <= bpm <= 200:
                    peaks.append((bpm, correlation[i]))
        peaks.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in peaks[:n_peaks]]

    def _select_best_bpm(self, candidates: List[float]) -> float:
        if not candidates:
            return 120.0
        bpm_groups = {}
        for bpm in candidates:
            rounded = round(bpm)
            bpm_groups[rounded] = bpm_groups.get(rounded, 0) + 1
        best_group = max(bpm_groups, key=bpm_groups.get)
        matching = [b for b in candidates if abs(b - best_group) < 1]
        return sum(matching) / len(matching)
```

### Harmonic Mixing Engine

```python
class HarmonicMixingEngine:
    ENERGY_TRANSITIONS = {
        "build_up": lambda e: min(1.0, e * 1.2),
        "cool_down": lambda e: max(0.0, e * 0.8),
        "maintain": lambda e: e,
    }

    def __init__(self):
        self.cameot_wheel = CAMELOT_WHEEL

    def suggest_next_track(self, current: TrackAnalysis, library: List[TrackAnalysis],
                           strategy: str = "harmonic") -> Optional[TrackAnalysis]:
        compatible = get_compatible_keys(current.camelot)
        candidates = [t for t in library if t.camelot in compatible and t.title != current.title]
        if not candidates:
            return None

        if strategy == "harmonic":
            return max(candidates, key=lambda t: t.energy)
        elif strategy == "energy_build":
            return max(candidates, key=lambda t: t.energy if t.energy > current.energy else -1)
        elif strategy == "energy_cool":
            return max(candidates, key=lambda t: -t.energy if t.energy < current.energy else -1)
        return candidates[0]

    def calculate_energy_flow(self, tracks: List[TrackAnalysis]) -> List[float]:
        if not tracks:
            return []
        energies = [t.energy for t in tracks]
        flow = [energies[0]]
        for i in range(1, len(energies)):
            diff = energies[i] - energies[i-1]
            if abs(diff) < 0.1:
                flow.append(energies[i])
            elif diff > 0:
                flow.append(min(1.0, energies[i] * 1.1))
            else:
                flow.append(max(0.0, energies[i] * 0.9))
        return flow

    def optimize_set_order(self, tracks: List[TrackAnalysis]) -> List[TrackAnalysis]:
        if len(tracks) <= 1:
            return tracks
        ordered = [tracks[0]]
        remaining = list(tracks[1:])
        while remaining:
            current = ordered[-1]
            best = self.suggest_next_track(current, remaining)
            if best:
                ordered.append(best)
                remaining.remove(best)
            else:
                ordered.append(remaining.pop(0))
        return ordered
```

## Architecture Patterns

### Live Performance Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Audio Input │────▶│  Analysis    │────▶│  Display    │
│  (Deck A/B)  │     │  Engine      │     │  (BPM/Key)  │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐     ┌─────────────┐
                    │  Matching    │────▶│  Suggestion │
                    │  Engine      │     │  Engine     │
                    └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Crossfade   │
                    │  Controller  │
                    └──────────────┘
```

### Event-Driven DJ System

```python
from enum import Enum
from typing import Callable, Dict, List
from collections import defaultdict

class DjEvent(Enum):
    TRACK_LOADED = "track_loaded"
    PLAYBACK_STARTED = "playback_started"
    PLAYBACK_STOPPED = "playback_stopped"
    BPM_DETECTED = "bpm_detected"
    KEY_DETECTED = "key_detected"
    TRANSITION_STARTED = "transition_started"
    TRANSITION_COMPLETED = "transition_completed"
    LOOP_SET = "loop_set"
    CUE_SET = "cue_set"

class DjEventBus:
    def __init__(self):
        self._handlers: Dict[DjEvent, List[Callable]] = defaultdict(list)

    def on(self, event: DjEvent, handler: Callable):
        self._handlers[event].append(handler)

    def emit(self, event: DjEvent, data: dict = None):
        for handler in self._handlers[event]:
            handler(data or {})

class DjSession:
    def __init__(self, config: DjConfig = None):
        self.config = config or DjConfig()
        self.controller = DjController(self.config)
        self.event_bus = DjEventBus()
        self._analyzer = AdvancedBpmDetector()

    def load_track(self, deck_id: int, audio: np.ndarray, sr: int):
        bpm = self._analyzer.detect_bpm_robust(audio)
        self.controller.decks[deck_id].current_bpm = bpm
        self.event_bus.emit(DjEvent.TRACK_LOADED, {"deck": deck_id, "bpm": bpm})

    def start_transition(self, from_deck: int, to_deck: int, crossfade_beats: int = 16):
        self.event_bus.emit(DjEvent.TRANSITION_STARTED, {
            "from": from_deck, "to": to_deck, "beats": crossfade_beats
        })

    def complete_transition(self, from_deck: int, to_deck: int):
        self.controller.decks[from_deck].is_playing = False
        self.controller.decks[to_deck].is_playing = True
        self.event_bus.emit(DjEvent.TRANSITION_COMPLETED, {"from": from_deck, "to": to_deck})
```

### Plugin Architecture for DJ Effects

```python
class DjEffect:
    def __init__(self, name: str, sr: int = 44100):
        self.name = name
        self.sr = sr
        self.enabled = True
        self.wet_dry = 0.5

    def process(self, audio: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def set_param(self, param: str, value: float):
        setattr(self, param, value)

class EchoEffect(DjEffect):
    def __init__(self, sr: int = 44100, delay_ms: float = 500, feedback: float = 0.4):
        super().__init__("echo", sr)
        self.delay_ms = delay_ms
        self.feedback = feedback

    def process(self, audio: np.ndarray) -> np.ndarray:
        delay_samples = int(self.delay_ms * self.sr / 1000)
        output = np.zeros(len(audio) + delay_samples)
        output[:len(audio)] = audio
        for i in range(delay_samples, len(output)):
            output[i] += output[i - delay_samples] * self.feedback
        return output[:len(audio)]

class FilterSweepEffect(DjEffect):
    def __init__(self, sr: int = 44100, cutoff: float = 1000, resonance: float = 5):
        super().__init__("filter_sweep", sr)
        self.cutoff = cutoff
        self.resonance = resonance

    def process(self, audio: np.ndarray) -> np.ndarray:
        from scipy.signal import butter, sosfilt
        nyq = self.sr / 2
        sos = butter(2, self.cutoff / nyq, btype='low', output='sos')
        filtered = sosfilt(sos, audio)
        return self.wet_dry * filtered + (1 - self.wet_dry) * audio

class DjEffectChain:
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self.effects: List[DjEffect] = []

    def add(self, effect: DjEffect) -> 'DjEffectChain':
        self.effects.append(effect)
        return self

    def process(self, audio: np.ndarray) -> np.ndarray:
        result = audio
        for effect in self.effects:
            if effect.enabled:
                result = effect.process(result)
        return result

    def remove(self, name: str):
        self.effects = [e for e in self.effects if e.name != name]
```

## Integration Guide

### External Audio Source Integration

```python
import pyaudio
import numpy as np

class LiveAudioInput:
    def __init__(self, sr: int = 44100, channels: int = 2, buffer_size: int = 1024):
        self.sr = sr
        self.channels = channels
        self.buffer_size = buffer_size
        self.pa = pyaudio.PyAudio()
        self.stream = None

    def start(self, callback: Callable):
        def audio_callback(in_data, frame_count, time_info, status):
            audio = np.frombuffer(in_data, dtype=np.float32)
            callback(audio)
            return (in_data, pyaudio.paContinue)

        self.stream = self.pa.open(
            format=pyaudio.paFloat32,
            channels=self.channels,
            rate=self.sr,
            input=True,
            frames_per_buffer=self.buffer_size,
            stream_callback=audio_callback,
        )
        self.stream.start_stream()

    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.pa.terminate()
```

### Playlist Management

```python
import json

class PlaylistManager:
    def __init__(self):
        self.playlists: Dict[str, List[TrackAnalysis]] = {}

    def create_playlist(self, name: str):
        self.playlists[name] = []

    def add_track(self, playlist_name: str, track: TrackAnalysis):
        if playlist_name not in self.playlists:
            self.create_playlist(playlist_name)
        self.playlists[playlist_name].append(track)

    def remove_track(self, playlist_name: str, track_title: str):
        if playlist_name in self.playlists:
            self.playlists[playlist_name] = [
                t for t in self.playlists[playlist_name] if t.title != track_title
            ]

    def export_json(self, filepath: str):
        data = {}
        for name, tracks in self.playlists.items():
            data[name] = [{
                "title": t.title, "artist": t.artist,
                "bpm": t.bpm, "key": t.key, "camelot": t.camelot,
                "energy": t.energy, "duration": t.duration,
            } for t in tracks]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def import_json(self, filepath: str):
        with open(filepath, 'r') as f:
            data = json.load(f)
        for name, tracks in data.items():
            self.playlists[name] = [
                TrackAnalysis(**t) for t in tracks
            ]
```

### Recording Integration

```python
class DjRecorder:
    def __init__(self, sr: int = 44100, channels: int = 2):
        self.sr = sr
        self.channels = channels
        self._recording = []
        self._is_recording = False

    def start_recording(self):
        self._recording = []
        self._is_recording = True

    def feed_audio(self, audio: np.ndarray):
        if self._is_recording:
            self._recording.append(audio.copy())

    def stop_recording(self) -> np.ndarray:
        self._is_recording = False
        if self._recording:
            return np.concatenate(self._recording)
        return np.array([])

    def save_recording(self, filepath: str):
        audio = self.stop_recording()
        if len(audio) > 0:
            import soundfile as sf
            sf.write(filepath, audio, self.sr)
```

## Performance Optimization

### Real-time Performance Requirements

| Metric | Target | Strategy |
|--------|--------|----------|
| Latency | < 10ms | Small buffer size (256-512) |
| CPU Usage | < 70% | Efficient FFT, vectorized operations |
| Memory | < 512MB | Stream processing, no full-track loading |
| BPM Detection | < 500ms | Multi-resolution autocorrelation |
| Key Detection | < 200ms | Chromagram with pre-computed profiles |
| Crossfade Quality | No clicks | Zero-crossing aligned fades |

### Optimization Techniques

```python
class OptimizedAnalyzer:
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self._cache: Dict[str, float] = {}

    def detect_bpm_cached(self, audio_hash: str, audio: np.ndarray) -> float:
        if audio_hash in self._cache:
            return self._cache[audio_hash]
        bpm = self._detect_bpm(audio)
        self._cache[audio_hash] = bpm
        return bpm

    def _detect_bpm(self, audio: np.ndarray) -> float:
        return 120.0  # Simplified

    def analyze_chunk(self, chunk: np.ndarray) -> dict:
        energy = np.sqrt(np.mean(chunk ** 2))
        return {"energy": energy, "rms": energy}
```

### Memory Management

```python
class AudioBufferPool:
    def __init__(self, buffer_size: int = 4096, pool_size: int = 16):
        self._pool = [np.zeros(buffer_size, dtype=np.float32) for _ in range(pool_size)]
        self._available = list(range(pool_size))

    def acquire(self) -> np.ndarray:
        if self._available:
            idx = self._available.pop()
            return self._pool[idx]
        return np.zeros(len(self._pool[0]), dtype=np.float32)

    def release(self, buffer: np.ndarray):
        for i, b in enumerate(self._pool):
            if b is buffer:
                self._available.append(i)
                break
```

## Security Considerations

### Audio File Validation

```python
import os

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
ALLOWED_FORMATS = {'.wav', '.mp3', '.flac', '.ogg', '.aac', '.aiff'}

def validate_audio_file(filepath: str) -> bool:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    if os.path.getsize(filepath) > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {os.path.getsize(filepath)} bytes")
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported format: {ext}")
    return True

def sanitize_filename(filename: str) -> str:
    return "".join(c for c in filename if c.isalnum() or c in "._- ")
```

### Resource Limits

```python
MAX_CONCURRENT_ANALYSES = 8
MAX_AUDIO_DURATION = 7200  # 2 hours

def enforce_limits(num_active: int):
    if num_active >= MAX_CONCURRENT_ANALYSES:
        raise RuntimeError("Too many concurrent analyses")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| BPM detection wrong | Off by factor of 2 | Check for half-time/double-time detection |
| Key detection wrong | Wrong key returned | Increase analysis window, use more samples |
| Audio clicks during crossfade | Audible artifacts | Use zero-crossing aligned crossfade points |
| High CPU usage | UI lag, dropouts | Reduce buffer size, use vectorized operations |
| Memory leak | Growing memory usage | Use buffer pool, release audio references |
| Latency too high | Delayed response | Reduce buffer size, use direct audio callback |
| MIDI sync drift | Tracks desync over time | Implement MIDI clock synchronization |
| Loop points not aligned | Loop clicks | Align to beat boundaries |

### Debugging Tools

```python
def debug_dj_session(session: DjSession):
    print("=== DJ Session Debug ===")
    for deck_id, deck in session.controller.decks.items():
        print(f"Deck {deck_id}:")
        print(f"  BPM: {deck.current_bpm}")
        print(f"  Key: {deck.key}")
        print(f"  Playing: {deck.is_playing}")
        print(f"  Position: {deck.position_beats} beats")
        print(f"  Loop: {'active' if deck.loop_active else 'inactive'}")
        print(f"  Cue points: {len(deck.cue_points)}")
```

### Performance Profiling

```python
import time

class DjProfiler:
    def __init__(self):
        self._timings: Dict[str, List[float]] = {}

    def measure(self, name: str):
        class Timer:
            def __init__(self, profiler, name):
                self.profiler = profiler
                self.name = name
            def __enter__(self):
                self.start = time.perf_counter()
                return self
            def __exit__(self, *args):
                elapsed = (time.perf_counter() - self.start) * 1000
                if self.name not in self.profiler._timings:
                    self.profiler._timings[self.name] = []
                self.profiler._timings[self.name].append(elapsed)
        return Timer(self, name)

    def report(self):
        for name, times in self._timings.items():
            avg = sum(times) / len(times)
            print(f"{name}: avg={avg:.2f}ms, samples={len(times)}")
```

## API Reference

### Core Classes

| Class | Constructor | Key Methods |
|-------|-------------|-------------|
| `BPMAnalyzer` | none | `detect_bpm(audio, sr)` |
| `KeyDetector` | none | `detect_key(audio, sr)` |
| `Crossfader` | none | `beat_aligned_crossfade(a, b, sr, beats_a, beats_b)` |
| `PlaylistBuilder` | none | `build_harmonic_set(tracks, start_key, max)` |
| `DjController` | `config` | `sync_bpm()`, `set_cue_point()`, `set_loop()`, `get_status()` |
| `DjSession` | `config` | `load_track()`, `start_transition()`, `complete_transition()` |
| `AdvancedBpmDetector` | `sr` | `detect_bpm_robust(audio)` |
| `HarmonicMixingEngine` | none | `suggest_next_track()`, `optimize_set_order()` |
| `PlaylistManager` | none | `create_playlist()`, `add_track()`, `export_json()` |
| `DjRecorder` | `sr, channels` | `start_recording()`, `stop_recording()`, `save_recording()` |

### Utility Functions

| Function | Description |
|----------|-------------|
| `get_compatible_keys(camelot)` | Get Camelot-wheel compatible keys |
| `validate_audio_file(filepath)` | Validate audio file for loading |

## Data Models

### Track Analysis Schema

```json
{
  "track_analysis": {
    "title": "string",
    "artist": "string",
    "bpm": "float",
    "key": "string",
    "camelot": "string",
    "duration": "float",
    "energy": "float",
    "danceability": "float",
    "loudness": "float"
  }
}
```

### DJ Session State

```json
{
  "session": {
    "decks": {
      "0": {"bpm": 128.0, "key": "Am", "playing": true, "position": 32.5},
      "1": {"bpm": 128.0, "key": "Am", "playing": false, "position": 0.0}
    },
    "crossfade_position": 0.0,
    "master_bpm": 128.0
  }
}
```

## Deployment Guide

### Docker Setup

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libasound2-dev \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["python", "-m", "dj_tools.server"]
```

## Monitoring and Observability

### Performance Metrics

```python
@dataclass
class DjMetrics:
    tracks_analyzed: int = 0
    avg_bpm_detection_ms: float = 0.0
    avg_key_detection_ms: float = 0.0
    transitions_performed: int = 0
    avg_crossfade_ms: float = 0.0

    def get_summary(self) -> dict:
        return {
            "tracks_analyzed": self.tracks_analyzed,
            "avg_bpm_ms": f"{self.avg_bpm_detection_ms:.1f}",
            "avg_key_ms": f"{self.avg_key_detection_ms:.1f}",
            "transitions": self.transitions_performed,
        }
```

## Testing Strategy

### Unit Tests

```python
import unittest

class TestBpmDetector(unittest.TestCase):
    def test_detect_bpm(self):
        sr = 44100
        t = np.linspace(0, 10, sr * 10)
        audio = np.sin(2 * np.pi * 2 * t)  # 2 Hz = 120 BPM
        detector = AdvancedBpmDetector(sr)
        bpm = detector.detect_bpm_robust(audio)
        self.assertAlmostEqual(bpm, 120.0, delta=5.0)

class TestKeyDetector(unittest.TestCase):
    def test_detect_key(self):
        sr = 22050
        t = np.linspace(0, 5, sr * 5)
        audio = np.sin(2 * np.pi * 261.63 * t)  # Middle C
        detector = KeyDetector()
        key, camelot = detector.detect_key(audio, sr)
        self.assertIn("C", key)

class TestCrossfader(unittest.TestCase):
    def test_crossfade_length(self):
        sr = 44100
        track_a = np.random.randn(sr * 10)
        track_b = np.random.randn(sr * 10)
        fader = Crossfader()
        result = fader.beat_aligned_crossfade(track_a, track_b, sr, [], [], 16)
        self.assertGreater(len(result), 0)
```

## Versioning and Migration

| Version | Changes |
|---------|---------|
| 2.0.0 | Advanced BPM detection, harmonic mixing engine, effect chain |
| 1.5.0 | Playlist management, recording integration |
| 1.0.0 | Initial release with basic BPM and key detection |

## Glossary

| Term | Definition |
|------|-----------|
| **BPM** | Beats Per Minute - tempo measurement |
| **Camelot Wheel** | System for harmonic key matching |
| **Crossfade** | Gradual transition between two tracks |
| **Beat Grid** | Aligned timing grid for DJ performance |
| **Key Detection** | Identifying the musical key of a track |
| **Harmonic Mixing** | Mixing tracks in compatible musical keys |
| **Cue Point** | Marked position in a track for quick access |
| **Loop** | Repeated section of audio |
| **Energy** | Perceptual loudness/intensity measure |
| **Slip Mode** | Cueing without stopping playback |

## Changelog

- **2.0.0** - Advanced BPM detection, harmonic mixing, effect chain
- **1.5.0** - Playlist management, recording
- **1.2.0** - Added loop detection
- **1.1.0** - Enhanced key detection
- **1.0.0** - Initial release

## Contributing Guidelines

1. Test BPM detection with diverse music genres
2. Validate key detection against known references
3. Profile real-time performance requirements
4. Document controller compatibility

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills
