"""
DJ Tools Module
Part of the music-tech skill domain.

Automated DJ toolkit: BPM detection, key analysis, harmonic mixing,
crossfade automation, and intelligent playlist generation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

try:
    import librosa
except ImportError:
    librosa = None


class MixingMode(Enum):
    HARMONIC = "harmonic"
    ENERGY = "energy"
    BPM = "bpm"
    RANDOM = "random"


class CrossfadeType(Enum):
    LINEAR = "linear"
    EQUAL_POWER = "equal_power"
    EXPONENTIAL = "exponential"
    BEAT_ALIGNED = "beat_aligned"


class TransitionStyle(Enum):
    SMOOTH = "smooth"
    ABRUPT = "abrupt"
    SWEEP = "sweep"
    CUT = "cut"


CAMELOT_WHEEL: Dict[str, str] = {
    "A": "8B", "Am": "8A", "Bbm": "3A", "B": "10B",
    "Cm": "5A", "C": "5B", "Dbm": "12A", "Db": "12B",
    "Dm": "7A", "D": "7B", "Ebm": "2A", "Eb": "2B",
    "Em": "9A", "E": "9B", "Fm": "4A", "F": "4B",
    "Gbm": "11A", "Gb": "11B", "Gm": "6A", "G": "6B",
    "Abm": "1A", "Ab": "1B",
}

CAMELOT_TO_KEY = {v: k for k, v in CAMELOT_WHEEL.items()}

MAJOR_PROFILE = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MINOR_PROFILE = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
CHROMATIC_KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


@dataclass
class TrackMetadata:
    title: str = "Unknown"
    artist: str = "Unknown"
    bpm: float = 0.0
    key: str = ""
    camelot: str = ""
    duration: float = 0.0
    energy: float = 0.0
    danceability: float = 0.0
    loudness: float = 0.0
    spectral_centroid: float = 0.0
    file_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "artist": self.artist,
            "bpm": self.bpm,
            "key": self.key,
            "camelot": self.camelot,
            "duration": self.duration,
            "energy": self.energy,
            "danceability": self.danceability,
            "loudness": self.loudness,
        }


@dataclass
class BeatGrid:
    bpm: float = 0.0
    beats: List[float] = field(default_factory=list)
    beat_times: List[float] = field(default_factory=list)
    downbeats: List[int] = field(default_factory=list)

    @property
    def beat_interval(self) -> float:
        return 60.0 / self.bpm if self.bpm > 0 else 0.0

    def get_beat_at_time(self, time_sec: float) -> int:
        if self.beat_interval <= 0:
            return 0
        return int(time_sec / self.beat_interval)

    def get_next_downbeat(self, time_sec: float) -> float:
        beat = self.get_beat_at_time(time_sec)
        next_downbeat = (beat + 4 - beat % 4) * self.beat_interval
        return next_downbeat


@dataclass
class TransitionPlan:
    from_track: TrackMetadata
    to_track: TrackMetadata
    overlap_beats: int = 16
    crossfade_type: CrossfadeType = CrossfadeType.BEAT_ALIGNED
    transition_style: TransitionStyle = TransitionStyle.SMOOTH
    eq_blend: bool = True
    eq Frequencies: Tuple[float, float, float] = (250.0, 1000.0, 4000.0)

    @property
    def bpm_compatible(self) -> bool:
        ratio = self.from_track.bpm / self.to_track.bpm if self.to_track.bpm > 0 else 0
        return 0.9 <= ratio <= 1.1

    @property
    def key_compatible(self) -> bool:
        if not self.from_track.camelot or not self.to_track.camelot:
            return False
        return self.to_track.camelot in get_compatible_camelot(self.from_track.camelot)


@dataclass
class DJSession:
    tracks: List[TrackMetadata] = field(default_factory=list)
    current_index: int = 0
    mixing_mode: MixingMode = MixingMode.HARMONIC
    auto_transition: bool = True

    @property
    def current_track(self) -> Optional[TrackMetadata]:
        if 0 <= self.current_index < len(self.tracks):
            return self.tracks[self.current_index]
        return None

    @property
    def next_track(self) -> Optional[TrackMetadata]:
        if self.current_index + 1 < len(self.tracks):
            return self.tracks[self.current_index + 1]
        return None


def get_compatible_camelot(camelot: str) -> List[str]:
    compatible = [camelot]
    num = int(camelot[:-1])
    letter = camelot[-1]
    compatible.append(f"{num}{'A' if letter == 'B' else 'B'}")
    prev = (num - 1) if num > 1 else 12
    next_num = (num + 1) if num < 12 else 1
    compatible.append(f"{prev}{letter}")
    compatible.append(f"{next_num}{letter}")
    return compatible


class BPMAnalyzer:
    def __init__(self, sr: int = 44100, min_bpm: float = 60, max_bpm: float = 200):
        self.sr = sr
        self.min_bpm = min_bpm
        self.max_bpm = max_bpm

    def detect_bpm(self, audio: np.ndarray) -> float:
        audio_mono = audio.mean(axis=0) if audio.ndim > 1 else audio
        hop_length = 512

        if librosa is not None:
            tempo, _ = librosa.beat.beat_track(y=audio_mono, sr=self.sr, hop_length=hop_length)
            return float(tempo)

        ac = self._autocorrelation(audio_mono, hop_length)
        min_lag = int(60 * self.sr / (self.max_bpm * hop_length))
        max_lag = int(60 * self.sr / (self.min_bpm * hop_length))

        search_range = ac[min_lag:max_lag]
        if len(search_range) == 0:
            return 0.0

        peak_idx = np.argmax(search_range) + min_lag
        bpm = 60.0 * self.sr / (peak_idx * hop_length)
        return round(bpm, 1)

    def _autocorrelation(self, audio: np.ndarray, hop_length: int) -> np.ndarray:
        n_fft = 2048
        num_frames = max(1, (len(audio) - n_fft) // hop_length)
        correlation = np.zeros(n_fft // 2)

        for i in range(min(num_frames, 200)):
            start = i * hop_length
            frame = audio[start:start + n_fft]
            if len(frame) < n_fft:
                break
            frame = frame * np.hanning(n_fft)
            spectrum = np.fft.rfft(frame)
            power = np.abs(spectrum) ** 2
            ac = np.fft.irfft(power)
            correlation[:len(ac)] += ac[:len(correlation)]

        return correlation

    def detect_beat_grid(self, audio: np.ndarray) -> BeatGrid:
        bpm = self.detect_bpm(audio)
        beat_interval = 60.0 / bpm
        duration = len(audio) / self.sr
        num_beats = int(duration / beat_interval)

        beat_times = [i * beat_interval for i in range(num_beats)]
        downbeats = [i * 4 for i in range(num_beats // 4)]

        return BeatGrid(
            bpm=bpm,
            beats=list(range(num_beats)),
            beat_times=beat_times,
            downbeats=downbeats,
        )


class KeyDetector:
    def __init__(self, sr: int = 22050):
        self.sr = sr

    def detect_key(self, audio: np.ndarray) -> Tuple[str, str]:
        chroma = self._compute_chroma(audio)
        key_profiles = self._get_profiles()

        best_key = ""
        best_score = -1.0

        for key, profile in key_profiles.items():
            score = float(np.corrcoef(chroma, profile)[0, 1])
            if score > best_score:
                best_score = score
                best_key = key

        camelot = CAMELOT_WHEEL.get(best_key, "1B")
        return best_key, camelot

    def _compute_chroma(self, audio: np.ndarray) -> np.ndarray:
        n_fft = 4096
        audio_chunk = audio[:n_fft * 5] if len(audio) > n_fft * 5 else audio

        if librosa is not None:
            chroma = librosa.feature.chroma_stft(y=audio_chunk, sr=self.sr, n_fft=n_fft)
            return np.mean(chroma, axis=1)

        spectrum = np.abs(np.fft.rfft(audio_chunk[:n_fft]))
        chroma = np.zeros(12)
        for i, mag in enumerate(spectrum):
            freq = i * self.sr / n_fft
            if freq > 20:
                pitch = int(round(12 * np.log2(freq / 440.0) + 69)) % 12
                chroma[pitch] += mag
        return chroma / (np.max(chroma) + 1e-10)

    def _get_profiles(self) -> Dict[str, np.ndarray]:
        profiles = {}
        for i, k in enumerate(CHROMATIC_KEYS):
            profiles[k] = np.roll(MAJOR_PROFILE, -i)
            profiles[k + "m"] = np.roll(MINOR_PROFILE, -i)
        return profiles


class Crossfader:
    def create_crossfade(self, audio_a: np.ndarray, audio_b: np.ndarray,
                         overlap_samples: int, fade_type: CrossfadeType) -> np.ndarray:
        fade_out = self._get_fade_curve(overlap_samples, fade_type, direction="out")
        fade_in = self._get_fade_curve(overlap_samples, fade_type, direction="in")

        overlap_a = audio_a[-overlap_samples:] * fade_out
        overlap_b = audio_b[:overlap_samples] * fade_in

        result = np.zeros(len(audio_a) + len(audio_b) - overlap_samples)
        result[:len(audio_a) - overlap_samples] = audio_a[:len(audio_a) - overlap_samples]
        result[len(audio_a) - overlap_samples:len(audio_a)] = overlap_a + overlap_b
        result[len(audio_a):] = audio_b[overlap_samples:]

        return result

    def beat_aligned_crossfade(self, audio_a: np.ndarray, audio_b: np.ndarray,
                               sr: int, beat_grid_a: BeatGrid, beat_grid_b: BeatGrid,
                               overlap_beats: int = 16) -> np.ndarray:
        overlap_samples = int(overlap_beats * beat_grid_a.beat_interval * sr)
        overlap_samples = min(overlap_samples, len(audio_a), len(audio_b))
        return self.create_crossfade(audio_a, audio_b, overlap_samples, CrossfadeType.BEAT_ALIGNED)

    def _get_fade_curve(self, n: int, fade_type: CrossfadeType, direction: str) -> np.ndarray:
        t = np.linspace(0, 1, n)
        if fade_type == CrossfadeType.LINEAR:
            curve = t if direction == "in" else (1 - t)
        elif fade_type == CrossfadeType.EQUAL_POWER:
            curve = np.sin(t * np.pi / 2) if direction == "in" else np.cos(t * np.pi / 2)
        elif fade_type == CrossfadeType.EXPONENTIAL:
            curve = t ** 2 if direction == "in" else (1 - t) ** 2
        else:
            curve = np.sin(t * np.pi / 2) if direction == "in" else np.cos(t * np.pi / 2)
        return curve.astype(np.float32)

    def eq_blend(self, audio_a: np.ndarray, audio_b: np.ndarray,
                 freq_bands: Tuple[float, float, float] = (250, 1000, 4000),
                 sr: int = 44100) -> np.ndarray:
        result = np.zeros(max(len(audio_a), len(audio_b)))
        result[:len(audio_a)] += audio_a * 0.5
        result[:len(audio_b)] += audio_b * 0.5
        return result


class PlaylistBuilder:
    def __init__(self, mixing_mode: MixingMode = MixingMode.HARMONIC):
        self.mixing_mode = mixing_mode

    def build_set(self, tracks: List[TrackMetadata], start_index: int = 0,
                  max_tracks: int = 20) -> List[TrackMetadata]:
        if not tracks:
            return []

        selected: List[TrackMetadata] = []
        used = set()
        current = tracks[start_index] if start_index < len(tracks) else tracks[0]
        selected.append(current)
        used.add(current.title)

        for _ in range(max_tracks - 1):
            candidates = [t for t in tracks if t.title not in used]
            if not candidates:
                break

            if self.mixing_mode == MixingMode.HARMONIC:
                compatible_camelot = get_compatible_camelot(current.camelot)
                compat = [t for t in candidates if t.camelot in compatible_camelot]
                if compat:
                    candidates = compat

            best = max(candidates, key=lambda t: self._score_track(t, current))
            selected.append(best)
            used.add(best.title)
            current = best

        return selected

    def _score_track(self, track: TrackMetadata, current: TrackMetadata) -> float:
        score = 0.0

        if self.mixing_mode in (MixingMode.HARMONIC, MixingMode.BPM):
            if track.bpm > 0 and current.bpm > 0:
                bpm_diff = abs(track.bpm - current.bpm)
                score += max(0, 10 - bpm_diff)

        if self.mixing_mode == MixingMode.HARMONIC:
            if track.camelot and current.camelot:
                compatible = get_compatible_camelot(current.camelot)
                if track.camelot in compatible:
                    score += 10

        score += track.energy * 5
        score += track.danceability * 3

        return score

    def analyze_transition(self, from_track: TrackMetadata,
                           to_track: TrackMetadata) -> TransitionPlan:
        bpm_compatible = False
        if from_track.bpm > 0 and to_track.bpm > 0:
            ratio = from_track.bpm / to_track.bpm
            bpm_compatible = 0.9 <= ratio <= 1.1

        style = TransitionStyle.SMOOTH
        if not bpm_compatible:
            style = TransitionStyle.SWEEP

        return TransitionPlan(
            from_track=from_track,
            to_track=to_track,
            overlap_beats=16 if bpm_compatible else 32,
            transition_style=style,
            eq_blend=True,
        )


class LoopDetector:
    def __init__(self, sr: int = 44100):
        self.sr = sr

    def find_loop_points(self, audio: np.ndarray, beat_grid: BeatGrid,
                         min_beats: int = 4, max_beats: int = 32) -> List[Tuple[float, float]]:
        loop_points: List[Tuple[float, float]] = []
        beat_interval = beat_grid.beat_interval

        for n_beats in range(min_beats, max_beats + 1, 4):
            loop_length = int(n_beats * beat_interval * self.sr)
            for i in range(0, len(audio) - loop_length * 2, loop_length):
                segment_a = audio[i:i + loop_length]
                segment_b = audio[i + loop_length:i + 2 * loop_length]
                if len(segment_b) < loop_length:
                    break

                similarity = self._similarity(segment_a, segment_b)
                if similarity > 0.7:
                    start_time = i / self.sr
                    end_time = (i + loop_length) / self.sr
                    loop_points.append((start_time, end_time))

        return loop_points

    def _similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        if len(a) != len(b) or len(a) == 0:
            return 0.0
        a_norm = a / (np.max(np.abs(a)) + 1e-10)
        b_norm = b / (np.max(np.abs(b)) + 1e-10)
        return float(np.abs(np.dot(a_norm, b_norm)) / len(a))


def main():
    print("=== DJ Tools Module ===")

    sr = 44100
    duration = 4.0
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    audio_a = 0.4 * np.sin(2 * np.pi * 120 * t) + 0.2 * np.sin(2 * np.pi * 240 * t)
    audio_b = 0.4 * np.sin(2 * np.pi * 128 * t) + 0.2 * np.sin(2 * np.pi * 256 * t)

    print("\n=== BPM Detection ===")
    bpm_analyzer = BPMAnalyzer(sr)
    bpm_a = bpm_analyzer.detect_bpm(audio_a)
    bpm_b = bpm_analyzer.detect_bpm(audio_b)
    print(f"  Track A BPM: {bpm_a}")
    print(f"  Track B BPM: {bpm_b}")

    beat_grid = bpm_analyzer.detect_beat_grid(audio_a)
    print(f"  Beat interval: {beat_grid.beat_interval:.3f}s")
    print(f"  Total beats: {len(beat_grid.beats)}")

    print("\n=== Key Detection ===")
    key_detector = KeyDetector(sr)
    key_a, camelot_a = key_detector.detect_key(audio_a)
    key_b, camelot_b = key_detector.detect_key(audio_b)
    print(f"  Track A: {key_a} ({camelot_a})")
    print(f"  Track B: {key_b} ({camelot_b})")

    compatible = get_compatible_camelot(camelot_a)
    print(f"  Compatible with {camelot_a}: {compatible}")

    print("\n=== Crossfade ===")
    crossfader = Crossfader()
    mix = crossfader.create_crossfade(audio_a, audio_b, sr // 2, CrossfadeType.EQUAL_POWER)
    print(f"  Mix length: {len(mix)} samples ({len(mix)/sr:.2f}s)")

    print("\n=== Playlist Builder ===")
    builder = PlaylistBuilder(MixingMode.HARMONIC)
    tracks = [
        TrackMetadata("Track 1", "DJ A", 120, "C", "5B", 180, 0.7, 0.8, -8.0),
        TrackMetadata("Track 2", "DJ B", 122, "G", "6B", 200, 0.8, 0.9, -7.5),
        TrackMetadata("Track 3", "DJ C", 118, "Am", "8A", 190, 0.6, 0.7, -9.0),
        TrackMetadata("Track 4", "DJ D", 125, "Em", "9A", 175, 0.9, 0.85, -6.0),
        TrackMetadata("Track 5", "DJ E", 121, "D", "7B", 210, 0.75, 0.8, -8.5),
    ]

    dj_set = builder.build_set(tracks, start_index=0, max_tracks=5)
    print(f"  Generated set ({len(dj_set)} tracks):")
    for i, t in enumerate(dj_set):
        print(f"    {i+1}. {t.title} - {t.artist} ({t.bpm} BPM, {t.camelot})")

    print("\n=== Transition Analysis ===")
    if len(dj_set) >= 2:
        plan = builder.analyze_transition(dj_set[0], dj_set[1])
        print(f"  {plan.from_track.title} -> {plan.to_track.title}")
        print(f"  BPM compatible: {plan.bpm_compatible}")
        print(f"  Key compatible: {plan.key_compatible}")
        print(f"  Style: {plan.transition_style.value}")

    print("\nDone.")


if __name__ == "__main__":
    main()
