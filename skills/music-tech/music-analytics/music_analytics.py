"""
Music Analytics Module
Part of the music-tech skill domain.

Comprehensive music analytics: feature extraction, mood classification,
similarity scoring, recommendation engines, and audio fingerprinting.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


class MoodCategory(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    CALM = "calm"
    EXCITED = "excited"
    MELANCHOLIC = "melancholic"
    NEUTRAL = "neutral"
    AGGRESSIVE = "aggressive"
    ROMANTIC = "romantic"


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
    danceability: float = 0.0
    energy: float = 0.0
    valence: float = 0.0
    arousal: float = 0.0
    loudness: float = 0.0
    instrumentalness: float = 0.0
    speechiness: float = 0.0

    def to_vector(self) -> np.ndarray:
        return np.array([
            self.rms_energy, self.spectral_centroid / 5000.0,
            self.spectral_bandwidth / 3000.0, self.spectral_rolloff / 10000.0,
            self.zero_crossing_rate, self.tempo / 200.0,
            self.key_confidence, 1.0 if self.mode == "major" else 0.0,
            self.danceability, self.energy, self.valence, self.arousal,
            (self.loudness + 60) / 60.0, self.instrumentalness, self.speechiness,
        ])

    def cosine_similarity(self, other: AudioFeatureVector) -> float:
        a, b = self.to_vector(), other.to_vector()
        norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def euclidean_distance(self, other: AudioFeatureVector) -> float:
        return float(np.linalg.norm(self.to_vector() - other.to_vector()))

    def manhattan_distance(self, other: AudioFeatureVector) -> float:
        return float(np.sum(np.abs(self.to_vector() - other.to_vector())))


@dataclass
class PlaylistTrack:
    title: str
    artist: str
    features: AudioFeatureVector
    play_count: int = 0
    skip_count: int = 0
    duration: float = 0.0
    genre: str = ""
    year: int = 0

    @property
    def engagement_rate(self) -> float:
        total = self.play_count + self.skip_count
        return self.play_count / total if total > 0 else 0.0

    @property
    def skip_rate(self) -> float:
        total = self.play_count + self.skip_count
        return self.skip_count / total if total > 0 else 0.0


class PlaylistAnalyzer:
    def analyze_flow(self, tracks: List[PlaylistTrack]) -> Dict[str, Any]:
        if not tracks:
            return {"error": "empty playlist"}

        bpms = [t.features.tempo for t in tracks]
        energies = [t.features.energy for t in tracks]
        valences = [t.features.valence for t in tracks]
        durations = [t.duration for t in tracks]

        return {
            "num_tracks": len(tracks),
            "total_duration_sec": sum(durations),
            "total_duration_min": sum(durations) / 60.0,
            "bpm_range": {"min": min(bpms), "max": max(bpms)},
            "bpm_mean": float(np.mean(bpms)),
            "bpm_std": float(np.std(bpms)),
            "energy_curve": energies,
            "energy_mean": float(np.mean(energies)),
            "energy_variance": float(np.var(energies)),
            "energy_flow_score": self._flow_score(energies),
            "valence_curve": valences,
            "valence_mean": float(np.mean(valences)),
            "valence_flow_score": self._flow_score(valences),
            "key_distribution": self._key_distribution(tracks),
            "genre_distribution": self._genre_distribution(tracks),
            "mood_arc": self._mood_arc(tracks),
        }

    def _flow_score(self, values: List[float]) -> float:
        if len(values) < 2:
            return 1.0
        diffs = [abs(values[i + 1] - values[i]) for i in range(len(values) - 1)]
        return max(0.0, 1.0 - float(np.mean(diffs)))

    def _key_distribution(self, tracks: List[PlaylistTrack]) -> Dict[str, int]:
        dist: Dict[str, int] = {}
        for t in tracks:
            key = t.features.mode
            dist[key] = dist.get(key, 0) + 1
        return dist

    def _genre_distribution(self, tracks: List[PlaylistTrack]) -> Dict[str, int]:
        dist: Dict[str, int] = {}
        for t in tracks:
            genre = t.genre or "unknown"
            dist[genre] = dist.get(genre, 0) + 1
        return dist

    def _mood_arc(self, tracks: List[PlaylistTrack]) -> List[str]:
        classifier = MoodClassifier()
        return [classifier.classify(t.features).value for t in tracks]


class MoodClassifier:
    QUADRANTS: Dict[MoodCategory, Tuple[float, float, float, float]] = {
        MoodCategory.HAPPY: (0.5, 1.0, 0.5, 1.0),
        MoodCategory.SAD: (0.0, 0.5, 0.0, 0.5),
        MoodCategory.ANGRY: (0.0, 0.5, 0.5, 1.0),
        MoodCategory.CALM: (0.5, 1.0, 0.0, 0.5),
        MoodCategory.EXCITED: (0.7, 1.0, 0.7, 1.0),
        MoodCategory.MELANCHOLIC: (0.0, 0.4, 0.0, 0.4),
        MoodCategory.AGGRESSIVE: (0.0, 0.3, 0.7, 1.0),
        MoodCategory.ROMANTIC: (0.4, 0.8, 0.2, 0.6),
    }

    def classify(self, features: AudioFeatureVector) -> MoodCategory:
        v, a = features.valence, features.arousal

        if features.energy > 0.8 and features.tempo > 140:
            return MoodCategory.EXCITED
        if features.energy < 0.2 and features.valence < 0.3:
            return MoodCategory.MELANCHOLIC
        if features.energy > 0.7 and features.valence < 0.3:
            return MoodCategory.ANGRY
        if features.energy < 0.3 and features.valence > 0.5:
            return MoodCategory.CALM

        best_mood = MoodCategory.NEUTRAL
        best_distance = float("inf")

        for mood, (v_min, v_max, a_min, a_max) in self.QUADRANTS.items():
            center_v = (v_min + v_max) / 2
            center_a = (a_min + a_max) / 2
            dist = math.sqrt((v - center_v) ** 2 + (a - center_a) ** 2)
            if dist < best_distance:
                best_distance = dist
                best_mood = mood

        return best_mood

    def classify_batch(self, tracks: List[PlaylistTrack]) -> Dict[str, int]:
        mood_counts: Dict[str, int] = {}
        for t in tracks:
            mood = self.classify(t.features)
            mood_counts[mood.value] = mood_counts.get(mood.value, 0) + 1
        return mood_counts


class RecommendationEngine:
    def __init__(self, library: List[PlaylistTrack]):
        self.library = library

    def content_based(self, seed: PlaylistTrack, n: int = 5,
                      weight_energy: float = 1.0,
                      weight_valence: float = 1.0,
                      weight_tempo: float = 0.5) -> List[Tuple[PlaylistTrack, float]]:
        scored: List[Tuple[PlaylistTrack, float]] = []
        for t in self.library:
            if t.title == seed.title and t.artist == seed.artist:
                continue
            base_sim = seed.features.cosine_similarity(t.features)
            energy_bonus = weight_energy * (1 - abs(seed.features.energy - t.features.energy))
            valence_bonus = weight_valence * (1 - abs(seed.features.valence - t.features.valence))
            tempo_bonus = weight_tempo * (1 - min(abs(seed.features.tempo - t.features.tempo) / 100, 1))
            total_score = base_sim + energy_bonus + valence_bonus + tempo_bonus
            scored.append((t, total_score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:n]

    def collaborative_filtering(self, user_plays: Dict[str, int],
                                n: int = 5) -> List[str]:
        sorted_plays = sorted(user_plays.items(), key=lambda x: x[1], reverse=True)
        return [title for title, _ in sorted_plays[:n]]

    def find_similar_tracks(self, query_features: AudioFeatureVector,
                            n: int = 5) -> List[Tuple[PlaylistTrack, float]]:
        scored = [(t, query_features.cosine_similarity(t.features))
                  for t in self.library]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:n]


class AudioFingerprinter:
    def __init__(self, hash_bits: int = 64):
        self.hash_bits = hash_bits
        self._database: Dict[str, np.ndarray] = {}

    def compute_fingerprint(self, audio: np.ndarray) -> np.ndarray:
        n_fft = 2048
        spectrum = np.abs(np.fft.rfft(audio[:n_fft])) if len(audio) >= n_fft else np.abs(np.fft.rfft(audio))
        peaks = np.argsort(spectrum)[-self.hash_bits:]
        fingerprint = np.zeros(self.hash_bits)
        for i, p in enumerate(peaks):
            fingerprint[i % self.hash_bits] = p
        return fingerprint

    def store(self, track_id: str, audio: np.ndarray):
        self._database[track_id] = self.compute_fingerprint(audio)

    def identify(self, audio: np.ndarray) -> Optional[Tuple[str, float]]:
        query = self.compute_fingerprint(audio)
        best_match = None
        best_score = 0.0
        for track_id, stored in self._database.items():
            score = float(np.sum(query == stored)) / self.hash_bits
            if score > best_score:
                best_score = score
                best_match = track_id
        return (best_match, best_score) if best_match and best_score > 0.5 else None

    @property
    def database_size(self) -> int:
        return len(self._database)


class AnalyticsDashboard:
    def __init__(self):
        self._metrics: Dict[str, Any] = {}
        self._history: List[Dict[str, Any]] = []

    def update(self, key: str, value: Any):
        self._metrics[key] = value
        self._history.append({"key": key, "value": value})

    def get(self, key: str, default: Any = None) -> Any:
        return self._metrics.get(key, default)

    def get_snapshot(self) -> Dict[str, Any]:
        return dict(self._metrics)

    def get_history(self, key: Optional[str] = None) -> List[Dict[str, Any]]:
        if key:
            return [h for h in self._history if h["key"] == key]
        return list(self._history)

    def summary(self) -> str:
        lines = [f"  {k}: {v}" for k, v in self._metrics.items()]
        return "Analytics Dashboard:\n" + "\n".join(lines)

    def clear(self):
        self._metrics.clear()
        self._history.clear()


class ListeningPatternAnalyzer:
    @staticmethod
    def analyze_play_patterns(tracks: List[PlaylistTrack]) -> Dict[str, Any]:
        if not tracks:
            return {"error": "no tracks"}

        total_plays = sum(t.play_count for t in tracks)
        total_skips = sum(t.skip_count for t in tracks)
        avg_engagement = np.mean([t.engagement_rate for t in tracks])

        most_played = max(tracks, key=lambda t: t.play_count)
        most_skipped = max(tracks, key=lambda t: t.skip_count)
        highest_engagement = max(tracks, key=lambda t: t.engagement_rate)

        return {
            "total_plays": total_plays,
            "total_skips": total_skips,
            "overall_skip_rate": total_skips / (total_plays + total_skips) if (total_plays + total_skips) > 0 else 0,
            "avg_engagement_rate": float(avg_engagement),
            "most_played": {"title": most_played.title, "plays": most_played.play_count},
            "most_skipped": {"title": most_skipped.title, "skips": most_skipped.skip_count},
            "highest_engagement": {"title": highest_engagement.title, "rate": highest_engagement.engagement_rate},
            "num_tracks": len(tracks),
        }

    @staticmethod
    def predict_skip(features: AudioFeatureVector) -> float:
        score = 0.0
        if features.energy < 0.2:
            score += 0.3
        if features.speechiness > 0.5:
            score += 0.2
        if features.instrumentalness > 0.8:
            score += 0.15
        if features.tempo < 60 or features.tempo > 180:
            score += 0.1
        return min(1.0, score)


def main():
    print("=== Music Analytics Module ===")

    tracks_data = [
        ("Summer Vibes", "DJ Sun", 0.8, 0.7, 128, 0.9, 0.8),
        ("Rainy Night", "Moon Beat", 0.3, 0.3, 85, 0.4, 0.2),
        ("Party Time", "Funk Master", 0.9, 0.9, 120, 0.95, 0.9),
        ("Deep Thought", "Ambient Soul", 0.2, 0.4, 70, 0.3, 0.5),
        ("Electric Rush", "Bass Theory", 0.85, 0.8, 140, 0.85, 0.85),
    ]

    tracks = []
    for title, artist, energy, valence, tempo, dance, mood_val in tracks_data:
        features = AudioFeatureVector(
            rms_energy=energy * 0.5,
            spectral_centroid=tempo * 30,
            tempo=tempo,
            energy=energy,
            valence=valence,
            danceability=dance,
            arousal=mood_val,
        )
        tracks.append(PlaylistTrack(
            title=title, artist=artist, features=features,
            play_count=int(energy * 100), skip_count=int((1 - energy) * 30),
            duration=200 + tempo, genre="electronic",
        ))

    print("\n=== Playlist Analysis ===")
    analyzer = PlaylistAnalyzer()
    flow = analyzer.analyze_flow(tracks)
    print(f"  Tracks: {flow['num_tracks']}")
    print(f"  Total duration: {flow['total_duration_min']:.1f} min")
    print(f"  BPM range: {flow['bpm_range']['min']}-{flow['bpm_range']['max']}")
    print(f"  Energy flow: {flow['energy_flow_score']:.3f}")
    print(f"  Mood arc: {flow['mood_arc']}")

    print("\n=== Mood Classification ===")
    classifier = MoodClassifier()
    for t in tracks:
        mood = classifier.classify(t.features)
        print(f"  {t.title}: {mood.value}")

    batch_moods = classifier.classify_batch(tracks)
    print(f"  Batch distribution: {batch_moods}")

    print("\n=== Recommendation Engine ===")
    engine = RecommendationEngine(tracks)
    recs = engine.content_based(tracks[0], n=3)
    print(f"  Recommendations for '{tracks[0].title}':")
    for t, score in recs:
        print(f"    {t.title} (score: {score:.3f})")

    print("\n=== Audio Fingerprinting ===")
    fp = AudioFingerprinter(hash_bits=32)
    for t in tracks:
        fake_audio = np.random.randn(2048).astype(np.float32)
        fp.store(t.title, fake_audio)
    print(f"  Database size: {fp.database_size}")

    query_audio = np.random.randn(2048).astype(np.float32)
    match = fp.identify(query_audio)
    print(f"  Query match: {match}")

    print("\n=== Listening Patterns ===")
    pattern_analyzer = ListeningPatternAnalyzer()
    patterns = pattern_analyzer.analyze_play_patterns(tracks)
    print(f"  Total plays: {patterns['total_plays']}")
    print(f"  Skip rate: {patterns['overall_skip_rate']:.2%}")
    print(f"  Most played: {patterns['most_played']['title']}")

    print("\n=== Dashboard ===")
    dashboard = AnalyticsDashboard()
    dashboard.update("total_tracks", len(tracks))
    dashboard.update("avg_energy", float(np.mean([t.features.energy for t in tracks])))
    dashboard.update("avg_valence", float(np.mean([t.features.valence for t in tracks])))
    print(dashboard.summary())

    print("\nDone.")


if __name__ == "__main__":
    main()
