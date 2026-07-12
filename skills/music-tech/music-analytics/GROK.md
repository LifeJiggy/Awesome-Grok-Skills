---
name: music-analytics
category: music-tech
version: 2.0.0
tags: [music-tech, analytics, audio-features, recommendation, ml]
---

# Music Analytics

## Overview

Comprehensive music analytics platform for extracting, analyzing, and deriving insights from audio content. This skill covers audio feature extraction pipelines, playlist analysis, listening pattern detection, mood classification, similarity scoring, and recommendation engine foundations. Built for music streaming analytics, DJ performance analysis, and music discovery applications.

## Core Capabilities

- **Feature Extraction**: Timbral, rhythmic, harmonic, and structural features from audio
- **Mood Classification**: Valence-arousal model for emotional categorization of tracks
- **Similarity Scoring**: Track-to-track similarity using multi-dimensional feature vectors
- **Playlist Analytics**: Flow analysis, energy curves, key distribution, and BPM progression
- **Listening Patterns**: Play count analysis, skip prediction, and engagement metrics
- **Recommendation Engine**: Collaborative and content-based filtering foundations
- **Audio Fingerprinting**: Track identification via spectral hashing
- **Dashboard Metrics**: Real-time analytics for music platforms

## Usage Examples

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

@dataclass
class AudioFeatureVector:
    rms_energy: float = 0.0
    spectral_centroid: float = 0.0
    spectral_bandwidth: float = 0.0
    spectral_rolloff: float = 0.0
    zero_crossing_rate: float = 0.0
    tempo: float = 0.0
    key_confidence: float = 0.0
    mode: str = "major"
    time_signature: int = 4
    danceability: float = 0.0
    energy: float = 0.0
    valence: float = 0.0
    arousal: float = 0.0

    def to_vector(self) -> np.ndarray:
        return np.array([
            self.rms_energy, self.spectral_centroid, self.spectral_bandwidth,
            self.spectral_rolloff, self.zero_crossing_rate, self.tempo / 200,
            self.key_confidence, 1.0 if self.mode == "major" else 0.0,
            self.danceability, self.energy, self.valence, self.arousal,
        ])

    def cosine_similarity(self, other: 'AudioFeatureVector') -> float:
        a, b = self.to_vector(), other.to_vector()
        dot = np.dot(a, b)
        norm = np.linalg.norm(a) * np.linalg.norm(b)
        return dot / norm if norm > 0 else 0.0

@dataclass
class PlaylistTrack:
    title: str
    artist: str
    features: AudioFeatureVector
    play_count: int = 0
    skip_count: int = 0
    duration: float = 0.0

    @property
    def engagement_rate(self) -> float:
        total = self.play_count + self.skip_count
        return self.play_count / total if total > 0 else 0.0

class PlaylistAnalyzer:
    def analyze_flow(self, tracks: List[PlaylistTrack]) -> Dict:
        if not tracks:
            return {}

        bpms = [t.features.tempo for t in tracks]
        energies = [t.features.energy for t in tracks]
        valences = [t.features.valence for t in tracks]

        return {
            "num_tracks": len(tracks),
            "total_duration": sum(t.duration for t in tracks),
            "bpm_range": (min(bpms), max(bpms)),
            "bpm_std": float(np.std(bpms)),
            "energy_curve": energies,
            "avg_energy": float(np.mean(energies)),
            "energy_variance": float(np.var(energies)),
            "valence_curve": valences,
            "avg_valence": float(np.mean(valences)),
            "energy_flow_score": self._flow_score(energies),
            "key_distribution": self._key_distribution(tracks),
        }

    def _flow_score(self, values: List[float]) -> float:
        if len(values) < 2:
            return 1.0
        diffs = [abs(values[i+1] - values[i]) for i in range(len(values) - 1)]
        avg_diff = np.mean(diffs)
        return max(0, 1.0 - avg_diff)

    def _key_distribution(self, tracks: List[PlaylistTrack]) -> Dict[str, int]:
        keys = {}
        for t in tracks:
            mode = t.features.mode
            keys[mode] = keys.get(mode, 0) + 1
        return keys

class MoodClassifier:
    VALENCE_AROUSAL_QUADRANTS = {
        "happy": (0.5, 1.0, 0.5, 1.0),
        "sad": (0.0, 0.5, 0.0, 0.5),
        "angry": (0.0, 0.5, 0.5, 1.0),
        "calm": (0.5, 1.0, 0.0, 0.5),
        "excited": (0.7, 1.0, 0.7, 1.0),
        "melancholic": (0.0, 0.4, 0.0, 0.4),
    }

    def classify(self, features: AudioFeatureVector) -> str:
        v, a = features.valence, features.arousal
        best_mood = "neutral"
        best_distance = float("inf")
        for mood, (v_min, v_max, a_min, a_max) in self.VALENCE_AROUSAL_QUADRANTS.items():
            center_v = (v_min + v_max) / 2
            center_a = (a_min + a_max) / 2
            dist = np.sqrt((v - center_v)**2 + (a - center_a)**2)
            if dist < best_distance:
                best_distance = dist
                best_mood = mood
        return best_mood

class RecommendationEngine:
    def __init__(self, library: List[PlaylistTrack]):
        self.library = library

    def content_based(self, seed: PlaylistTrack, n: int = 5) -> List[PlaylistTrack]:
        scores = [(t, seed.features.cosine_similarity(t.features))
                  for t in self.library if t.title != seed.title]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [t for t, _ in scores[:n]]

    def collaborative_filtering(self, user_plays: Dict[str, int],
                                 n: int = 5) -> List[str]:
        play_counts = sorted(user_plays.items(), key=lambda x: x[1], reverse=True)
        top_genres = [t[0] for t in play_counts[:3]]
        return top_genres

class AudioFingerprinter:
    def __init__(self, sr: int = 44100, hash_bits: int = 64):
        self.sr = sr
        self.hash_bits = hash_bits
        self._database: Dict[str, np.ndarray] = {}

    def compute_fingerprint(self, audio: np.ndarray) -> np.ndarray:
        n_fft = 2048
        hop = 512
        spectrum = np.abs(np.fft.rfft(audio[:n_fft]))
        peaks = np.argsort(spectrum)[-20:]
        fingerprint = np.zeros(self.hash_bits)
        for i, p in enumerate(peaks[:self.hash_bits]):
            fingerprint[i % self.hash_bits] = p
        return fingerprint

    def store(self, track_id: str, audio: np.ndarray):
        self._database[track_id] = self.compute_fingerprint(audio)

    def identify(self, audio: np.ndarray) -> Optional[Tuple[str, float]]:
        query_fp = self.compute_fingerprint(audio)
        best_match = None
        best_score = 0.0
        for track_id, stored_fp in self._database.items():
            score = np.sum(query_fp == stored_fp) / self.hash_bits
            if score > best_score:
                best_score = score
                best_match = track_id
        return (best_match, best_score) if best_match and best_score > 0.5 else None

class AnalyticsDashboard:
    def __init__(self):
        self._metrics: Dict[str, any] = {}

    def update(self, key: str, value: any):
        self._metrics[key] = value

    def get_snapshot(self) -> Dict[str, any]:
        return dict(self._metrics)

    def summary(self) -> str:
        lines = [f"  {k}: {v}" for k, v in self._metrics.items()]
        return "\n".join(lines)
```

## Best Practices

- Normalize feature vectors before computing distances to prevent scale bias
- Use cosine similarity for high-dimensional audio feature comparison
- Maintain a diverse library for recommendation engines to avoid filter bubbles
- Weight recent plays higher than old ones in collaborative filtering
- Use spectral hashing for efficient large-scale audio fingerprint matching
- Analyze energy curves for playlist flow quality and DJ set optimization
- Track engagement rates alongside raw play counts for meaningful analytics
- Cache feature extraction results to avoid redundant computation
- Use PCA or t-SNE for visualization of high-dimensional audio features
- Validate mood classifiers with labeled human-annotated datasets

## Related Modules

- `audio-processing` - Low-level DSP and spectral analysis
- `music-generation` - AI-driven composition
- `sound-design` - Synthesis and effects
- `dj-tools` - DJ mixing and performance tools
