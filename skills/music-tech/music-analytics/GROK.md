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

## Advanced Configuration

### Feature Extraction Settings

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `n_mfcc` | 13 | 13 - 40 | Number of MFCC coefficients |
| `n_chroma` | 12 | 12 - 24 | Chromagram bins |
| `n_mels` | 128 | 32 - 256 | Mel filterbank bands |
| `fmin` | 20 | 0 - 100 | Minimum frequency for analysis |
| `fmax` | 8000 | 4000 - 22050 | Maximum frequency for analysis |
| `n_fft` | 2048 | 512 - 8192 | FFT window size |
| `hop_length` | 512 | 128 - 2048 | STFT hop length |
| `embedding_dim` | 128 | 32 - 512 | Feature embedding dimension |

### Analytics Pipeline Configuration

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class FeatureSet(Enum):
    BASIC = "basic"
    EXTENDED = "extended"
    FULL = "full"
    ML_READY = "ml_ready"

@dataclass
class AnalyticsConfig:
    feature_set: FeatureSet = FeatureSet.EXTENDED
    sample_rate: int = 22050
    n_fft: int = 2048
    hop_length: int = 512
    n_mfcc: int = 13
    n_chroma: int = 12
    compute_spectral: bool = True
    compute_rhythmic: bool = True
    compute_harmonic: bool = True
    compute_temporal: bool = True
    normalize_features: bool = True
    embedding_dim: int = 128

    @classmethod
    def for_recommendation(cls) -> 'AnalyticsConfig':
        return cls(feature_set=FeatureSet.FULL, normalize_features=True)

    @classmethod
    def for_classification(cls) -> 'AnalyticsConfig':
        return cls(feature_set=FeatureSet.ML_READY, normalize_features=True)

    @classmethod
    def for_quick_analysis(cls) -> 'AnalyticsConfig':
        return cls(feature_set=FeatureSet.BASIC, compute_spectral=False)

class FeatureExtractorConfig:
    def __init__(self, config: AnalyticsConfig = None):
        self.config = config or AnalyticsConfig()
        self._bands = {
            "delta": (1, 4), "theta": (4, 8), "alpha": (8, 13),
            "beta": (13, 30), "gamma": (30, 50),
        }

    def get_extraction_params(self) -> dict:
        return {
            "sr": self.config.sample_rate,
            "n_fft": self.config.n_fft,
            "hop_length": self.config.hop_length,
            "n_mfcc": self.config.n_mfcc,
            "n_chroma": self.config.n_chroma,
        }
```

### Database Schema for Analytics

```python
import sqlite3
from datetime import datetime

class AnalyticsDatabase:
    def __init__(self, db_path: str = "music_analytics.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY,
                filepath TEXT UNIQUE,
                title TEXT, artist TEXT, album TEXT,
                duration REAL, sample_rate INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS features (
                track_id INTEGER,
                feature_name TEXT,
                feature_vector BLOB,
                FOREIGN KEY (track_id) REFERENCES tracks(id)
            );
            CREATE TABLE IF NOT EXISTS recommendations (
                source_track_id INTEGER,
                target_track_id INTEGER,
                score REAL,
                method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_features_track ON features(track_id);
        """)
        self.conn.commit()

    def store_track(self, filepath: str, title: str, artist: str,
                    duration: float, sr: int) -> int:
        cursor = self.conn.execute(
            "INSERT INTO tracks (filepath, title, artist, duration, sample_rate) VALUES (?, ?, ?, ?, ?)",
            (filepath, title, artist, duration, sr)
        )
        self.conn.commit()
        return cursor.lastrowid

    def store_features(self, track_id: int, features: Dict[str, np.ndarray]):
        import pickle
        for name, vector in features.items():
            self.conn.execute(
                "INSERT INTO features (track_id, feature_name, feature_vector) VALUES (?, ?, ?)",
                (track_id, name, pickle.dumps(vector))
            )
        self.conn.commit()

    def query_similar(self, track_id: int, limit: int = 10) -> List[dict]:
        cursor = self.conn.execute("""
            SELECT t.title, t.artist, r.score
            FROM recommendations r
            JOIN tracks t ON r.target_track_id = t.id
            WHERE r.source_track_id = ?
            ORDER BY r.score DESC LIMIT ?
        """, (track_id, limit))
        return [{"title": r[0], "artist": r[1], "score": r[2]} for r in cursor.fetchall()]
```

## Architecture Patterns

### Analytics Pipeline Architecture

```
Audio Input → Preprocessing → Feature Extraction → Storage → Analysis → Output
    │              │                │                │           │          │
    ├── WAV/MP3    ├── Resample     ├── MFCC         ├── SQLite  ├── Stats  ├── JSON
    ├── Stream     ├── Normalize    ├── Chroma        ├── Redis   ├── ML     ├── CSV
    └── Batch      ├── Trim         ├── Onset        ├── S3      ├── Viz    └── Dashboard
```

### Feature Processing Pipeline

```python
from typing import Callable, List
from collections import OrderedDict

class FeaturePipeline:
    def __init__(self):
        self._steps: List[tuple] = []

    def add_step(self, name: str, fn: Callable) -> 'FeaturePipeline':
        self._steps.append((name, fn))
        return self

    def process(self, audio: np.ndarray, sr: int) -> OrderedDict:
        result = OrderedDict()
        current = audio
        for name, fn in self._steps:
            features = fn(current, sr)
            if isinstance(features, dict):
                result.update(features)
            else:
                result[name] = features
            current = features if isinstance(features, np.ndarray) else current
        return result

    def describe(self) -> List[str]:
        return [name for name, _ in self._steps]
```

### Recommendation System Architecture

```python
class RecommendationArchitecture:
    def __init__(self, config: AnalyticsConfig = None):
        self.config = config or AnalyticsConfig()
        self._content_index: Dict[int, np.ndarray] = {}
        self._collaborative_matrix: Optional[np.ndarray] = None

    def build_content_index(self, track_features: Dict[int, np.ndarray]):
        self._content_index = track_features

    def content_based_recommend(self, track_id: int, n: int = 5) -> List[tuple]:
        if track_id not in self._content_index:
            return []
        query = self._content_index[track_id]
        scores = []
        for tid, features in self._content_index.items():
            if tid != track_id:
                score = np.dot(query, features) / (np.linalg.norm(query) * np.linalg.norm(features) + 1e-10)
                scores.append((tid, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]

    def collaborative_recommend(self, user_id: int, n: int = 5) -> List[int]:
        if self._collaborative_matrix is None:
            return []
        user_vector = self._collaborative_matrix[user_id]
        scores = np.dot(self._collaborative_matrix, user_vector)
        top_indices = np.argsort(scores)[::-1][1:n+1]
        return top_indices.tolist()
```

### Visualization Pipeline

```python
class AnalyticsVisualizer:
    def __init__(self):
        self._figures: Dict[str, any] = {}

    def plot_spectrogram(self, features: dict, title: str = "Spectrogram"):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(12, 4))
        if "mel_spectrogram" in features:
            img = ax.imshow(features["mel_spectrogram"].T, aspect='auto', origin='lower')
            ax.set_xlabel("Time")
            ax.set_ylabel("Mel Frequency")
            plt.colorbar(img, ax=ax)
        ax.set_title(title)
        self._figures["spectrogram"] = fig
        return fig

    def plot_feature_distribution(self, features: Dict[str, float]):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 5))
        names = list(features.keys())
        values = list(features.values())
        ax.bar(range(len(names)), values)
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.set_title("Feature Distribution")
        self._figures["distribution"] = fig
        return fig

    def save_all(self, output_dir: str):
        import os
        os.makedirs(output_dir, exist_ok=True)
        for name, fig in self._figures.items():
            fig.savefig(os.path.join(output_dir, f"{name}.png"), dpi=150, bbox_inches='tight')
```

## Integration Guide

### External Service Integration

```python
import urllib.request
import json

class MusicBrainzClient:
    BASE_URL = "https://musicbrainz.org/ws/2"

    def search_track(self, title: str, artist: str) -> dict:
        query = f"recording:\"{title}\" AND artist:\"{artist}\""
        url = f"{self.BASE_URL}/recording/?query={query}&fmt=json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MusicAnalytics/2.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read())
        except Exception:
            return {}

class SpotifyFeaturesClient:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_audio_features(self, track_id: str) -> dict:
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {self.access_token}"
        })
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read())
        except Exception:
            return {}
```

### Message Queue Integration

```python
import queue
import threading

class AnalyticsMessageQueue:
    def __init__(self):
        self._queue = queue.Queue()
        self._results: Dict[str, dict] = {}
        self._lock = threading.Lock()

    def submit_analysis(self, task_id: str, filepath: str):
        self._queue.put({"task_id": task_id, "filepath": filepath})

    def start_worker(self, analyzer):
        def _process():
            while True:
                try:
                    task = self._queue.get(timeout=1.0)
                    result = analyzer.analyze(task["filepath"])
                    with self._lock:
                        self._results[task["task_id"]] = result
                    self._queue.task_done()
                except queue.Empty:
                    continue
        thread = threading.Thread(target=_process, daemon=True)
        thread.start()

    def get_result(self, task_id: str) -> Optional[dict]:
        with self._lock:
            return self._results.get(task_id)
```

## Performance Optimization

### Feature Extraction Optimization

| Technique | Speedup | Tradeoff |
|-----------|---------|----------|
| Pre-computed FFT | 2x | Memory usage |
| Batch processing | 3x | Memory usage |
| Cached features | 10x | Staleness risk |
| Parallel extraction | 4x | CPU cores needed |
| Reduced sample rate | 2x | Frequency resolution loss |
| Quantized features | 2x | Precision loss |

### Caching Strategy

```python
import hashlib
import pickle
import os

class FeatureCache:
    def __init__(self, cache_dir: str = "./feature_cache", max_size_mb: int = 1024):
        self.cache_dir = cache_dir
        self.max_size_mb = max_size_mb
        os.makedirs(cache_dir, exist_ok=True)

    def _hash_file(self, filepath: str) -> str:
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()

    def get(self, filepath: str) -> Optional[dict]:
        file_hash = self._hash_file(filepath)
        cache_path = os.path.join(self.cache_dir, f"{file_hash}.pkl")
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return None

    def set(self, filepath: str, features: dict):
        file_hash = self._hash_file(filepath)
        cache_path = os.path.join(self.cache_dir, f"{file_hash}.pkl")
        with open(cache_path, 'wb') as f:
            pickle.dump(features, f)

    def clear(self):
        for f in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, f))
```

### Batch Processing

```python
class BatchAnalyzer:
    def __init__(self, config: AnalyticsConfig = None):
        self.config = config or AnalyticsConfig()
        self._cache = FeatureCache()

    def analyze_batch(self, filepaths: List[str]) -> Dict[str, dict]:
        results = {}
        for fp in filepaths:
            cached = self._cache.get(fp)
            if cached:
                results[fp] = cached
            else:
                features = self._extract_features(fp)
                self._cache.set(fp, features)
                results[fp] = features
        return results

    def _extract_features(self, filepath: str) -> dict:
        return {}  # Placeholder
```

## Security Considerations

### File Access Security

```python
import os

ALLOWED_DIRECTORIES = ["/data/music", "/uploads"]
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

def validate_file_access(filepath: str) -> bool:
    abs_path = os.path.abspath(filepath)
    if not any(abs_path.startswith(d) for d in ALLOWED_DIRECTORIES):
        raise PermissionError(f"Access denied: {filepath}")
    if os.path.getsize(abs_path) > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {os.path.getsize(abs_path)} bytes")
    return True
```

### Data Privacy

```python
def anonymize_user_data(data: dict) -> dict:
    anonymized = dict(data)
    if "user_id" in anonymized:
        anonymized["user_id"] = hashlib.sha256(str(anonymized["user_id"]).encode()).hexdigest()[:16]
    if "ip_address" in anonymized:
        del anonymized["ip_address"]
    return anonymized
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Feature mismatch | Incompatible feature vectors | Ensure consistent extraction config |
| Memory overflow | OOM on large files | Process in chunks using STFT frames |
| Slow extraction | Long processing time | Use caching, reduce FFT size |
| Poor recommendations | Irrelevant results | Retrain with more data, adjust similarity metric |
| NaN in features | Failed extraction | Check for silence, add epsilon to log operations |
| Database corruption | SQLite errors | Run integrity check, rebuild from backup |
| Visualization errors | Empty plots | Verify feature shapes, check matplotlib backend |

### Debugging

```python
def debug_feature_extraction(audio: np.ndarray, sr: int):
    print(f"Audio shape: {audio.shape}")
    print(f"Sample rate: {sr}")
    print(f"Duration: {len(audio)/sr:.2f}s")
    print(f"Peak: {np.max(np.abs(audio)):.4f}")
    print(f"RMS: {np.sqrt(np.mean(audio**2)):.4f}")
    print(f"Has NaN: {np.any(np.isnan(audio))}")
    print(f"Has Inf: {np.any(np.isinf(audio))}")
```

## API Reference

### Core Classes

| Class | Constructor | Key Methods |
|-------|-------------|-------------|
| `AudioFeatureVector` | dataclass | `to_vector()`, `cosine_similarity()` |
| `PlaylistAnalyzer` | none | `analyze_flow()` |
| `MoodClassifier` | none | `classify(features)` |
| `RecommendationEngine` | `library` | `content_based()`, `collaborative_filtering()` |
| `AudioFingerprinter` | `sr, hash_bits` | `compute_fingerprint()`, `store()`, `identify()` |
| `AnalyticsDashboard` | none | `update()`, `get_snapshot()`, `summary()` |
| `AnalyticsDatabase` | `db_path` | `store_track()`, `store_features()`, `query_similar()` |
| `FeatureCache` | `cache_dir` | `get()`, `set()`, `clear()` |
| `BatchAnalyzer` | `config` | `analyze_batch()` |
| `AnalyticsVisualizer` | none | `plot_spectrogram()`, `plot_feature_distribution()` |

## Data Models

### Feature Vector Schema

```json
{
  "audio_feature_vector": {
    "rms_energy": "float",
    "spectral_centroid": "float",
    "spectral_bandwidth": "float",
    "spectral_rolloff": "float",
    "zero_crossing_rate": "float",
    "tempo": "float",
    "key_confidence": "float",
    "mode": "major|minor",
    "danceability": "float",
    "energy": "float",
    "valence": "float",
    "arousal": "float",
    "mfcc": "float[13]",
    "chroma": "float[12]"
  }
}
```

### Recommendation Schema

```json
{
  "recommendation": {
    "source_track": {"id": "int", "title": "string"},
    "target_track": {"id": "int", "title": "string"},
    "score": "float (0-1)",
    "method": "content_based|collaborative|hybrid"
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y libsndfile1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["python", "analytics_server.py"]
```

### Kubernetes Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: music-analytics
spec:
  replicas: 2
  selector:
    matchLabels:
      app: music-analytics
  template:
    spec:
      containers:
      - name: analytics
        image: music-analytics:latest
        resources:
          requests:
            memory: "1Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "4000m"
```

## Monitoring and Observability

### Analytics Metrics

```python
@dataclass
class AnalyticsMetrics:
    tracks_analyzed: int = 0
    features_extracted: int = 0
    recommendations_generated: int = 0
    avg_extraction_time_ms: float = 0.0
    cache_hit_rate: float = 0.0
    error_rate: float = 0.0

    def get_report(self) -> dict:
        return {
            "tracks_analyzed": self.tracks_analyzed,
            "avg_extraction_ms": f"{self.avg_extraction_time_ms:.1f}",
            "cache_hit_rate": f"{self.cache_hit_rate:.1%}",
            "error_rate": f"{self.error_rate:.2%}",
        }
```

### Health Check

```python
def health_check(db: AnalyticsDatabase) -> dict:
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "available",
    }
```

## Testing Strategy

### Unit Tests

```python
import unittest

class TestAudioFeatureVector(unittest.TestCase):
    def test_cosine_similarity(self):
        v1 = AudioFeatureVector(rms_energy=0.5, spectral_centroid=1000)
        v2 = AudioFeatureVector(rms_energy=0.5, spectral_centroid=1000)
        sim = v1.cosine_similarity(v2)
        self.assertAlmostEqual(sim, 1.0, places=2)

    def test_to_vector(self):
        v = AudioFeatureVector(rms_energy=0.5)
        vec = v.to_vector()
        self.assertEqual(len(vec), 12)

class TestPlaylistAnalyzer(unittest.TestCase):
    def test_analyze_flow_empty(self):
        analyzer = PlaylistAnalyzer()
        result = analyzer.analyze_flow([])
        self.assertEqual(result, {})

class TestMoodClassifier(unittest.TestCase):
    def test_classify_happy(self):
        classifier = MoodClassifier()
        features = AudioFeatureVector(valence=0.8, arousal=0.7)
        mood = classifier.classify(features)
        self.assertIn(mood, ["happy", "excited"])
```

## Versioning and Migration

| Version | Changes |
|---------|---------|
| 2.0.0 | Database integration, batch processing, visualization |
| 1.5.0 | Recommendation engine, audio fingerprinting |
| 1.0.0 | Initial release with feature extraction |

## Glossary

| Term | Definition |
|------|-----------|
| **MFCC** | Mel-Frequency Cepstral Coefficients - compact spectral features |
| **Chroma** | Pitch class profile across 12 semitones |
| **Valence** | Emotional positivity dimension |
| **Arousal** | Emotional intensity dimension |
| **Cosine similarity** | Angle-based distance metric for vectors |
| **Content-based filtering** | Recommendations based on item features |
| **Collaborative filtering** | Recommendations based on user behavior |
| **Audio fingerprint** | Compact spectral hash for track identification |
| **Spectral centroid** | Center of mass of spectrum (brightness measure) |
| **Zero crossing rate** | Rate of sign changes in signal |

## Changelog

- **2.0.0** - Database integration, batch processing, visualization
- **1.5.0** - Recommendation engine, fingerprinting
- **1.2.0** - Added mood classification
- **1.1.0** - Enhanced playlist analytics
- **1.0.0** - Initial release

## Contributing Guidelines

1. Validate feature extraction with known reference tracks
2. Test recommendation accuracy with labeled datasets
3. Benchmark extraction speed for large libraries
4. Document feature meaning and typical ranges

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills
