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
