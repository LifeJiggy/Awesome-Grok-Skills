---
name: brain-computer-interfaces
category: neural-science
version: 2.0.0
tags: [neural-science, bci, eeg, neural-interfaces, neurotechnology]
---

# Brain-Computer Interfaces

## Overview

Brain-Computer Interface (BCI) development toolkit covering EEG signal acquisition, neural signal processing, feature extraction, classification algorithms, and real-time BCI system design. This skill provides implementations for motor imagery classification, P300 speller systems, SSVEP-based interfaces, and hybrid BCI architectures for assistive technology and neuroscience research.

## Core Capabilities

- **EEG Signal Processing**: Bandpass filtering, artifact removal (ICA, CSP), re-referencing
- **Feature Extraction**: Common Spatial Patterns (CSP), band power, spectral features, connectivity
- **Classification**: LDA, SVM, CNN, LSTM for neural signal decoding
- **Paradigms**: Motor imagery, P300, SSVEP, error-related potentials
- **Real-time Processing**: Streaming EEG analysis with low-latency pipelines
- **Data Formats**: BDF, EDF, GDF, and Muse/OpenBCI CSV parsing
- **Visualization**: Topographic maps, spectrograms, and decoded output display
- **Device Integration**: OpenBCI, Muse, Emotiv, and generic serial EEG interfaces

## Usage Examples

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

class BciParadigm(Enum):
    MOTOR_IMAGERY = "motor_imagery"
    P300 = "p300"
    SSVEP = "ssvep"
    ERROR_POTENTIAL = "error_potential"

class MotorClass(Enum):
    LEFT_HAND = 0
    RIGHT_HAND = 1
    FEET = 2
    TONGUE = 3

@dataclass
class EegChannel:
    name: str
    index: int
    is_reference: bool = False
    sampling_rate: int = 256

@dataclass
class EegRecording:
    data: np.ndarray  # channels x samples
    channels: List[EegChannel]
    sampling_rate: int = 256
    paradigm: BciParadigm = BciParadigm.MOTOR_IMAGERY
    labels: Optional[np.ndarray] = None

    @property
    def num_channels(self) -> int:
        return self.data.shape[0]

    @property
    def num_samples(self) -> int:
        return self.data.shape[1]

    @property
    def duration(self) -> float:
        return self.num_samples / self.sampling_rate

class EegPreprocessor:
    def __init__(self, sampling_rate: int = 256):
        self.sr = sampling_rate

    def bandpass_filter(self, data: np.ndarray, low: float, high: float, order: int = 5) -> np.ndarray:
        nyq = self.sr / 2
        from scipy.signal import butter, filtfilt
        b, a = butter(order, [low / nyq, high / nyq], btype='band')
        return filtfilt(b, a, data, axis=-1)

    def notch_filter(self, data: np.ndarray, freq: float = 50.0) -> np.ndarray:
        from scipy.signal import iirnotch, filtfilt
        b, a = iirnotch(freq, 30, self.sr)
        return filtfilt(b, a, data, axis=-1)

    def common_average_reference(self, data: np.ndarray) -> np.ndarray:
        mean = np.mean(data, axis=0)
        return data - mean

    def remove_artifacts_ica(self, data: np.ndarray, n_components: int = None) -> np.ndarray:
        from sklearn.decomposition import FastICA
        n_comp = n_components or data.shape[0]
        ica = FastICA(n_components=n_comp, random_state=42)
        sources = ica.fit_transform(data.T).T
        for i in range(sources.shape[0]):
            if np.max(np.abs(sources[i])) > 3 * np.std(sources[i]):
                sources[i] = 0
        return ica.inverse_transform(sources.T).T

    def epoch(self, data: np.ndarray, events: List[int], window_start: int, window_end: int) -> np.ndarray:
        epochs = []
        for event in events:
            start = max(0, event + window_start)
            end = min(data.shape[1], event + window_end)
            epochs.append(data[:, start:end])
        return np.array(epochs)

class FeatureExtractor:
    def __init__(self, sampling_rate: int = 256):
        self.sr = sampling_rate

    def band_power(self, data: np.ndarray, low: float, high: float) -> float:
        from scipy.signal import welch
        freqs, psd = welch(data, fs=self.sr, nperseg=min(256, data.shape[-1]))
        mask = (freqs >= low) & (freqs <= high)
        return float(np.trapz(psd[mask], freqs[mask]))

    def csp_features(self, epochs: np.ndarray, labels: np.ndarray, n_filters: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        n_trials, n_channels, n_samples = epochs.shape
        covariances = np.array([np.dot(ep, ep.T) / n_samples for ep in epochs])
        class_0 = covariances[labels == 0].mean(axis=0)
        class_1 = covariances[labels == 1].mean(axis=0)
        combined = class_0 + class_1
        eigenvalues, eigenvectors = np.linalg.eig(np.linalg.solve(combined, class_0))
        sorted_idx = np.argsort(eigenvalues)[::-1]
        filters = eigenvectors[:, sorted_idx[:n_filters]]
        features = np.zeros((n_trials, 2 * n_filters))
        for i, ep in enumerate(epochs):
            projected = np.dot(filters.T, ep)
            for j in range(n_filters):
                features[i, j] = np.log(np.var(projected[j]))
                features[i, n_filters + j] = np.log(np.var(projected[j + n_filters]))
        return features, filters

    def spectral_features(self, data: np.ndarray) -> Dict[str, float]:
        from scipy.signal import welch
        freqs, psd = welch(data, fs=self.sr, nperseg=min(256, data.shape[-1]))
        total_power = np.trapz(psd, freqs)
        features = {"total_power": total_power}
        bands = {"delta": (1, 4), "theta": (4, 8), "alpha": (8, 13), "beta": (13, 30), "gamma": (30, 50)}
        for band_name, (low, high) in bands.items():
            mask = (freqs >= low) & (freqs <= high)
            power = np.trapz(psd[mask], freqs[mask])
            features[f"{band_name}_power"] = power
            features[f"{band_name}_ratio"] = power / total_power if total_power > 0 else 0
        return features

class BciClassifier:
    def __init__(self, model=None):
        self.model = model
        self.is_trained = False

    def train(self, features: np.ndarray, labels: np.ndarray):
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        if self.model is None:
            self.model = LinearDiscriminantAnalysis()
        self.model.fit(features, labels)
        self.is_trained = True

    def predict(self, features: np.ndarray) -> np.ndarray:
        if not self.is_trained:
            raise RuntimeError("Model not trained")
        return self.model.predict(features)

    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        if not self.is_trained:
            raise RuntimeError("Model not trained")
        return self.model.predict_proba(features)

class RealtimeBci:
    def __init__(self, paradigm: BciParadigm = BciParadigm.MOTOR_IMAGERY):
        self.paradigm = paradigm
        self.preprocessor = EegPreprocessor()
        self.extractor = FeatureExtractor()
        self.classifier = BciClassifier()
        self._buffer: List[np.ndarray] = []

    def process_chunk(self, chunk: np.ndarray) -> Optional[int]:
        self._buffer.append(chunk)
        if len(self._buffer) >= 8:
            data = np.concatenate(self._buffer, axis=1)
            self._buffer = []
            filtered = self.preprocessor.bandpass_filter(data, 8, 30)
            features = np.array([[self.extractor.band_power(ch, 8, 30) for ch in filtered]])
            if self.classifier.is_trained:
                return int(self.classifier.predict(features)[0])
        return None
```

## Best Practices

- Always apply bandpass filtering (1-50 Hz) to remove DC offset and muscle artifacts
- Use Common Average Reference (CAR) or Laplacian spatial filtering for noise reduction
- Apply ICA to remove eye blink and muscle artifacts from EEG recordings
- Use Common Spatial Patterns (CSP) for motor imagery feature extraction
- Train classifiers on sufficient trial counts (minimum 40-60 per class)
- Implement online calibration with feedback for user-specific adaptation
- Use sliding window classification with overlapping epochs for smooth output
- Validate BCI systems with offline cross-validation before online deployment
- Consider hybrid BCI approaches combining multiple paradigms for robustness
- Monitor signal quality metrics (SNR, impedance) during data acquisition

## Related Modules

- `eeg-analysis` - EEG data analysis and visualization
- `neural-modeling` - Computational neural modeling
- `cognitive-computing` - Cognitive process simulation
- `neuroprosthetics` - Neural prosthetic device interfaces

## Advanced Configuration

### Advanced EEG Preprocessing Pipeline

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

class PreprocessingPipeline:
    def __init__(self, sampling_rate: int = 256):
        self.sr = sampling_rate
        self.steps: List[Dict] = []

    def add_step(self, name: str, func, params: Dict = None):
        self.steps.append({"name": name, "func": func, "params": params or {}})

    def process(self, data: np.ndarray) -> np.ndarray:
        result = data.copy()
        for step in self.steps:
            result = step["func"](result, **step["params"])
        return result

class AdvancedEegPreprocessor:
    def __init__(self, sampling_rate: int = 256):
        self.sr = sampling_rate
        self.noise_estimates: Dict[str, float] = {}

    def adaptive_bandpass(self, data: np.ndarray, low: float = 1.0, high: float = 50.0) -> np.ndarray:
        nyq = self.sr / 2
        from scipy.signal import butter, filtfilt
        b, a = butter(4, [low / nyq, high / nyq], btype='band')
        return filtfilt(b, a, data, axis=-1)

    def wavelet_denoise(self, data: np.ndarray, wavelet: str = "db4", level: int = 5) -> np.ndarray:
        import pywt
        coeffs = pywt.wavedec(data, wavelet, level=level, axis=-1)
        for i in range(1, len(coeffs)):
            threshold = np.median(np.abs(coeffs[i])) * 0.6745 * np.sqrt(2 * np.log(coeffs[i].size))
            coeffs[i] = pywt.threshold(coeffs[i], threshold, mode='soft')
        return pywt.waverec(coeffs, wavelet, axis=-1)[:, :data.shape[-1]]

    def autoregressive_artifact_removal(self, data: np.ndarray, order: int = 16) -> np.ndarray:
        n_channels, n_samples = data.shape
        cleaned = np.zeros_like(data)
        for ch in range(n_channels):
            channel_data = data[ch]
            coeffs = np.polyfit(np.arange(order), channel_data[:order], order - 1)
            for i in range(order, n_samples):
                prediction = np.polyval(coeffs, np.arange(order))
                actual = channel_data[i-order:i]
                error = actual - prediction
                coeffs = np.polyfit(np.arange(order), channel_data[i-order:i], order - 1)
                if abs(error[-1]) > 3 * np.std(error):
                    cleaned[ch, i] = channel_data[i-1]
                else:
                    cleaned[ch, i] = channel_data[i]
            cleaned[ch, :order] = channel_data[:order]
        return cleaned

    def interpolate_bad_channels(self, data: np.ndarray, bad_channels: List[int],
                                  neighbor_map: Dict[int, List[int]]) -> np.ndarray:
        result = data.copy()
        for bad_ch in bad_channels:
            if bad_ch in neighbor_map:
                neighbors = neighbor_map[bad_ch]
                valid_neighbors = [n for n in neighbors if n not in bad_channels and n < data.shape[0]]
                if valid_neighbors:
                    result[bad_ch] = np.mean(data[valid_neighbors], axis=0)
        return result

    def segment_epochs(self, data: np.ndarray, events: List[int],
                       pre_samples: int = 256, post_samples: int = 512) -> np.ndarray:
        epochs = []
        for event in events:
            start = max(0, event - pre_samples)
            end = min(data.shape[1], event + post_samples)
            if end - start >= pre_samples + post_samples:
                epochs.append(data[:, start:end])
        return np.array(epochs) if epochs else np.array([])


class ChannelMontage:
    STANDARD_10_20 = {
        "Fp1": 0, "Fp2": 1, "F3": 2, "F4": 3, "C3": 4, "C4": 5,
        "P3": 6, "P4": 7, "O1": 8, "O2": 9, "F7": 10, "F8": 11,
        "T3": 12, "T4": 13, "T5": 14, "T6": 15, "Fz": 16, "Cz": 17,
        "Pz": 18, "Oz": 19,
    }

    STANDARD_10_10 = {
        "AF3": 0, "AF4": 1, "F1": 2, "F2": 3, "FC1": 4, "FC2": 5,
        "C1": 6, "C2": 7, "CP1": 8, "CP2": 9, "P1": 10, "P2": 11,
        "PO3": 12, "PO4": 13, "F5": 14, "F6": 15, "FC3": 16, "FC4": 17,
        "C5": 18, "C6": 19, "CP3": 20, "CP4": 21, "P5": 22, "P6": 23,
    }

    def __init__(self, channel_names: List[str]):
        self.channel_names = channel_names
        self.channel_map = {name: idx for idx, name in enumerate(channel_names)}

    def get_channel_index(self, name: str) -> Optional[int]:
        return self.channel_map.get(name)

    def get_neighborhood(self, channel_name: str, radius: int = 2) -> List[int]:
        idx = self.get_channel_index(channel_name)
        if idx is None:
            return []
        return [i for i in range(max(0, idx - radius), min(len(self.channel_names), idx + radius + 1))]

    def get_spatial_filters(self) -> Dict[str, np.ndarray]:
        laplacian = {}
        for name, idx in self.channel_map.items():
            neighbors = self.get_neighborhood(name, radius=1)
            if len(neighbors) > 1:
                kernel = np.zeros(len(self.channel_names))
                kernel[idx] = 1.0
                for n in neighbors:
                    if n != idx:
                        kernel[n] = -1.0 / (len(neighbors) - 1)
                laplacian[name] = kernel
        return laplacian
```

### Advanced Feature Extraction

```python
class AdvancedFeatureExtractor:
    def __init__(self, sampling_rate: int = 256):
        self.sr = sampling_rate

    def hjorth_parameters(self, data: np.ndarray) -> Dict[str, float]:
        diff1 = np.diff(data)
        diff2 = np.diff(diff1)
        activity = np.var(data)
        mobility = np.sqrt(np.var(diff1) / activity) if activity > 0 else 0
        complexity = np.sqrt(np.var(diff2) / np.var(diff1)) / mobility if mobility > 0 else 0
        return {"activity": activity, "mobility": mobility, "complexity": complexity}

    def higuchi_fractal_dimension(self, data: np.ndarray, kmax: int = 10) -> float:
        n = len(data)
        l_values = []
        x_range = range(1, kmax + 1)
        for k in x_range:
            l_k = 0
            for m in range(1, k + 1):
                indices = np.arange(m - 1, n, k)
                if len(indices) > 1:
                    segment = data[indices]
                    l_mk = np.sum(np.abs(np.diff(segment))) * (n - 1) / (k * len(indices) * k)
                    l_k += l_mk
            l_values.append(l_k / k)
        l_values = np.array(l_values)
        log_k = np.log(1.0 / np.array(list(x_range)))
        log_l = np.log(l_values + 1e-10)
        coeffs = np.polyfit(log_k, log_l, 1)
        return coeffs[0]

    def sample_entropy(self, data: np.ndarray, m: int = 2, r: float = 0.2) -> float:
        n = len(data)
        std = np.std(data)
        tolerance = r * std
        if std == 0 or n < m + 2:
            return 0.0
        def _count_matches(template_len: int) -> int:
            count = 0
            templates = np.array([data[i:i+template_len] for i in range(n - template_len)])
            for i in range(len(templates)):
                for j in range(i + 1, len(templates)):
                    if np.max(np.abs(templates[i] - templates[j])) < tolerance:
                        count += 1
            return count
        a = _count_matches(m)
        b = _count_matches(m + 1)
        if b == 0:
            return 0.0
        return -np.log(b / a) if a > 0 else 0.0

    def multiscale_entropy(self, data: np.ndarray, scales: int = 5) -> List[float]:
        entropies = []
        for scale in range(1, scales + 1):
            if scale == 1:
                coarse = data
            else:
                n = len(data) // scale
                coarse = np.array([np.mean(data[i*scale:(i+1)*scale]) for i in range(n)])
            entropies.append(self.sample_entropy(coarse))
        return entropies

    def phase_locking_value(self, data1: np.ndarray, data2: np.ndarray) -> float:
        from scipy.signal import hilbert
        analytic1 = hilbert(data1)
        analytic2 = hilbert(data2)
        phase1 = np.angle(analytic1)
        phase2 = np.angle(analytic2)
        phase_diff = phase1 - phase2
        plv = np.abs(np.mean(np.exp(1j * phase_diff)))
        return float(plv)

    def imaginary coherence(self, data1: np.ndarray, data2: np.ndarray, nperseg: int = 256) -> float:
        from scipy.signal import csd
        freqs, pxy = csd(data1, data2, fs=self.sr, nperseg=nperseg)
        freqs2, pxx = csd(data1, data1, fs=self.sr, nperseg=nperseg)
        freqs3, pyy = csd(data2, data2, fs=self.sr, nperseg=nperseg)
        coherence = np.abs(pxy) / np.sqrt(np.abs(pxx) * np.abs(pyy) + 1e-10)
        return float(np.mean(coherence))

    def differential_entropy(self, data: np.ndarray, band: Tuple[float, float]) -> float:
        from scipy.signal import welch
        freqs, psd = welch(data, fs=self.sr, nperseg=min(256, len(data)))
        mask = (freqs >= band[0]) & (freqs <= band[1])
        band_psd = psd[mask]
        band_psd = band_psd[band_psd > 0]
        if len(band_psd) == 0:
            return 0.0
        return float(0.5 * np.log(2 * np.pi * np.e * np.mean(band_psd)))
```

### Real-time BCI System Architecture

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum
import time
import threading
from collections import deque

class BciSystemState(Enum):
    IDLE = "idle"
    CALIBRATING = "calibrating"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"

@dataclass
class BciConfig:
    sampling_rate: int = 256
    n_channels: int = 16
    buffer_duration: float = 2.0
    window_duration: float = 0.5
    overlap: float = 0.25
    paradigm: str = "motor_imagery"
    low_freq: float = 8.0
    high_freq: float = 30.0
    n_classes: int = 2
    calibration_trials: int = 40
    confidence_threshold: float = 0.7

class RealtimeBciSystem:
    def __init__(self, config: BciConfig):
        self.config = config
        self.state = BciSystemState.IDLE
        self.preprocessor = AdvancedEegPreprocessor(config.sampling_rate)
        self.extractor = AdvancedFeatureExtractor(config.sampling_rate)
        self.classifier = BciClassifier()
        self._buffer = deque(maxlen=int(config.buffer_duration * config.sampling_rate))
        self._results: List[Dict] = []
        self._callbacks: List[Callable] = []
        self._lock = threading.Lock()
        self._calibration_data: List[np.ndarray] = []
        self._calibration_labels: List[int] = []

    def register_callback(self, callback: Callable):
        self._callbacks.append(callback)

    def push_samples(self, samples: np.ndarray):
        with self._lock:
            for i in range(samples.shape[1]):
                self._buffer.append(samples[:, i])
            if self.state == BciSystemState.RUNNING and len(self._buffer) >= int(self.config.window_duration * self.config.sampling_rate):
                self._process_window()

    def _process_window(self):
        window_size = int(self.config.window_duration * self.config.sampling_rate)
        window = np.array(list(self._buffer)[-window_size:]).T
        filtered = self.preprocessor.adaptive_bandpass(window, self.config.low_freq, self.config.high_freq)
        features = self._extract_features(filtered)
        if self.classifier.is_trained:
            prediction = self.classifier.predict(features.reshape(1, -1))[0]
            confidence = float(np.max(self.classifier.predict_proba(features.reshape(1, -1))))
            result = {
                "prediction": int(prediction),
                "confidence": confidence,
                "timestamp": time.time(),
                "state": self.state.value,
            }
            if confidence >= self.config.confidence_threshold:
                self._results.append(result)
                for callback in self._callbacks:
                    callback(result)

    def _extract_features(self, data: np.ndarray) -> np.ndarray:
        features = []
        for ch in range(data.shape[0]):
            band_power = self.extractor.band_power(data[ch], self.config.low_freq, self.config.high_freq)
            hjorth = self.extractor.hjorth_parameters(data[ch])
            features.extend([band_power, hjorth["activity"], hjorth["mobility"], hjorth["complexity"]])
        return np.array(features)

    def start_calibration(self):
        self.state = BciSystemState.CALIBRATING
        self._calibration_data = []
        self._calibration_labels = []

    def add_calibration_trial(self, data: np.ndarray, label: int):
        self._calibration_data.append(data)
        self._calibration_labels.append(label)

    def finish_calibration(self) -> bool:
        if len(self._calibration_data) < self.config.calibration_trials // 2:
            return False
        all_features = []
        for trial in self._calibration_data:
            filtered = self.preprocessor.adaptive_bandpass(trial, self.config.low_freq, self.config.high_freq)
            features = self._extract_features(filtered)
            all_features.append(features)
        X = np.array(all_features)
        y = np.array(self._calibration_labels)
        self.classifier.train(X, y)
        self.state = BciSystemState.RUNNING
        return True

    def start(self):
        self.state = BciSystemState.RUNNING

    def pause(self):
        self.state = BciSystemState.PAUSED

    def stop(self):
        self.state = BciSystemState.IDLE

    def get_results(self) -> List[Dict]:
        return self._results.copy()

    def get_statistics(self) -> Dict:
        return {
            "state": self.state.value,
            "buffer_size": len(self._buffer),
            "total_predictions": len(self._results),
            "avg_confidence": np.mean([r["confidence"] for r in self._results]) if self._results else 0,
        }
```

## Architecture Patterns

### P300 Speller System

```python
class P300SpellerSystem:
    def __init__(self, n_rows: int = 6, n_cols: int = 6, sampling_rate: int = 256):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.sr = sampling_rate
        self.matrix = self._create_matrix()
        self.preprocessor = AdvancedEegPreprocessor(sampling_rate)
        self.extractor = AdvancedFeatureExtractor(sampling_rate)
        self.classifier = BciClassifier()
        self.n_flashes = 10
        self.flash_duration = 0.1
        self.isi = 0.05
        self._target_char: Optional[str] = None
        self._flash_history: List[Dict] = []

    def _create_matrix(self) -> List[List[str]]:
        chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        matrix = []
        idx = 0
        for r in range(self.n_rows):
            row = []
            for c in range(self.n_cols):
                row.append(chars[idx] if idx < len(chars) else "")
                idx += 1
            matrix.append(row)
        return matrix

    def get_row_col_indices(self, char: str) -> Tuple[Optional[int], Optional[int]]:
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                if self.matrix[r][c] == char:
                    return r, c
        return None, None

    def simulate_flash(self, row_or_col: int, is_row: bool) -> Dict:
        flash = {
            "type": "row" if is_row else "col",
            "index": row_or_col,
            "characters": self.matrix[row_or_col] if is_row else [self.matrix[r][row_or_col] for r in range(self.n_rows)],
            "timestamp": time.time(),
        }
        self._flash_history.append(flash)
        return flash

    def process_response(self, eeg_data: np.ndarray, target_char: str = None) -> Dict:
        filtered = self.preprocessor.adaptive_bandpass(eeg_data, 1.0, 30.0)
        features = self.extractor.hjorth_parameters(filtered.flatten())
        p300_amplitude = np.max(filtered[filtered.shape[0]//2:, :]) if filtered.size > 0 else 0
        result = {
            "features": features,
            "p300_amplitude": p300_amplitude,
            "is_target": target_char is not None,
            "timestamp": time.time(),
        }
        return result

    def classify_flash(self, eeg_data: np.ndarray) -> float:
        filtered = self.preprocessor.adaptive_bandpass(eeg_data, 1.0, 30.0)
        features = self._extract_features(filtered)
        if self.classifier.is_trained:
            proba = self.classifier.predict_proba(features.reshape(1, -1))
            return float(proba[0][1]) if proba.shape[1] > 1 else 0.5
        return 0.5

    def _extract_features(self, data: np.ndarray) -> np.ndarray:
        features = []
        for ch in range(data.shape[0]):
            band = self.extractor.band_power(data[ch], 1.0, 30.0)
            hjorth = self.extractor.hjorth_parameters(data[ch])
            features.extend([band, hjorth["activity"], hjorth["mobility"], hjorth["complexity"]])
        return np.array(features)

    def determine_character(self, row_scores: List[float], col_scores: List[float]) -> str:
        best_row = int(np.argmax(row_scores))
        best_col = int(np.argmax(col_scores))
        return self.matrix[best_row][best_col]

    def calibrate(self, training_data: List[Dict]):
        features_list = []
        labels_list = []
        for trial in training_data:
            eeg = trial["eeg_data"]
            is_target = trial["is_target"]
            filtered = self.preprocessor.adaptive_bandpass(eeg, 1.0, 30.0)
            features = self._extract_features(filtered)
            features_list.append(features)
            labels_list.append(1 if is_target else 0)
        X = np.array(features_list)
        y = np.array(labels_list)
        self.classifier.train(X, y)
```

### SSVEP-Based BCI System

```python
class SsvepBciSystem:
    FREQUENCIES = {
        "left": 7.0, "right": 8.5, "up": 10.0, "down": 12.0,
        "select": 9.0, "back": 11.0, "menu": 13.0, "confirm": 14.0,
    }

    def __init__(self, sampling_rate: int = 256, n_channels: int = 8):
        self.sr = sampling_rate
        self.n_channels = n_channels
        self.preprocessor = AdvancedEegPreprocessor(sampling_rate)
        self.extractor = AdvancedFeatureExtractor(sampling_rate)
        self._target_freqs = list(self.FREQUENCIES.values())
        self._target_labels = list(self.FREQUENCIES.keys())
        self.window_size = int(1.0 * sampling_rate)
        self._buffer = deque(maxlen=self.window_size)

    def push_samples(self, samples: np.ndarray):
        for i in range(samples.shape[1]):
            self._buffer.append(samples[:, i])

    def detect_ssvep(self) -> Dict:
        if len(self._buffer) < self.window_size:
            return {"detected": False}
        data = np.array(list(self._buffer)).T
        filtered = self.preprocessor.adaptive_bandpass(data, 5.0, 50.0)
        from scipy.signal import welch
        freqs, psd = welch(filtered[0], fs=self.sr, nperseg=min(256, self.window_size))
        target_powers = {}
        for i, freq in enumerate(self._target_freqs):
            idx = np.argmin(np.abs(freqs - freq))
            harmonics_power = 0
            for h in range(1, 4):
                h_idx = np.argmin(np.abs(freqs - freq * h))
                harmonics_power += psd[h_idx]
            target_powers[self._target_labels[i]] = harmonics_power
        best_label = max(target_powers, key=target_powers.get)
        total_power = sum(target_powers.values())
        confidence = target_powers[best_label] / total_power if total_power > 0 else 0
        return {
            "detected": True,
            "label": best_label,
            "confidence": confidence,
            "frequency": self.FREQUENCIES[best_label],
            "powers": target_powers,
        }

    def canonical_correlation_analysis(self, data: np.ndarray, target_freq: float) -> float:
        n_samples = data.shape[1]
        t = np.arange(n_samples) / self.sr
        reference = np.column_stack([
            np.sin(2 * np.pi * target_freq * h * t) for h in range(1, 4)
        ] + [
            np.cos(2 * np.pi * target_freq * h * t) for h in range(1, 4)
        ])
        min_len = min(data.shape[1], reference.shape[0])
        X = data[:, :min_len].T
        Y = reference[:min_len]
        Cxx = np.cov(X.T) + np.eye(X.shape[1]) * 1e-6
        Cyy = np.cov(Y.T) + np.eye(Y.shape[1]) * 1e-6
        Cxy = np.cov(X.T, Y.T)[:X.shape[1], X.shape[1]:]
        try:
            inv_cxx = np.linalg.inv(Cxx)
            inv_cyy = np.linalg.inv(Cyy)
            M = inv_cxx @ Cxy @ inv_cyy @ Cxy.T
            eigenvalues = np.linalg.eigvals(M)
            max_corr = np.sqrt(np.max(np.real(eigenvalues)))
            return float(max_corr)
        except np.linalg.LinAlgError:
            return 0.0

    def filter_bank_ssvep(self, data: np.ndarray) -> Dict:
        bands = [(6, 90), (12, 30), (18, 30), (24, 30), (30, 45)]
        sub_band_scores = {}
        for label, freq in self.FREQUENCIES.items():
            sub_band_scores[label] = 0
            for low, high in bands:
                filtered = self.preprocessor.adaptive_bandpass(data, low, high)
                score = self.canonical_correlation_analysis(filtered, freq)
                sub_band_scores[label] += score
        best_label = max(sub_band_scores, key=sub_band_scores.get)
        return {"label": best_label, "scores": sub_band_scores}
```

### Hybrid BCI Architecture

```python
class HybridBciSystem:
    def __init__(self, config: BciConfig):
        self.config = config
        self.mi_system = RealtimeBciSystem(config)
        self.ssvep_system = SsvepBciSystem(config.sampling_rate, config.n_channels)
        self.p300_system = P300SpellerSystem()
        self._fusion_weights: Dict[str, float] = {"mi": 0.4, "ssvep": 0.35, "p300": 0.25}
        self._decision_buffer: List[Dict] = []
        self._fusion_threshold: float = 0.6

    def process_eeg(self, data: np.ndarray) -> Dict:
        mi_result = self.mi_system._extract_features(data)
        ssvep_result = self.ssvep_system.detect_ssvep()
        combined = {
            "mi_features": mi_result,
            "ssvep": ssvep_result,
            "timestamp": time.time(),
        }
        self._decision_buffer.append(combined)
        if len(self._decision_buffer) >= 5:
            return self._fuse_decisions()
        return combined

    def _fuse_decisions(self) -> Dict:
        recent = self._decision_buffer[-5:]
        self._decision_buffer = []
        votes: Dict[str, float] = {}
        for decision in recent:
            if "ssvep" in decision and decision["ssvep"].get("detected"):
                label = decision["ssvep"]["label"]
                conf = decision["ssvep"]["confidence"]
                votes[label] = votes.get(label, 0) + conf * self._fusion_weights["ssvep"]
        if votes:
            best = max(votes, key=votes.get)
            return {
                "decision": best,
                "confidence": votes[best],
                "fusion_method": "weighted_vote",
                "source": "hybrid",
            }
        return {"decision": None, "confidence": 0, "fusion_method": "weighted_vote"}

    def set_weights(self, mi: float = 0.4, ssvep: float = 0.35, p300: float = 0.25):
        total = mi + ssvep + p300
        self._fusion_weights = {"mi": mi/total, "ssvep": ssvep/total, "p300": p300/total}
```

## Integration Guide

### OpenBCI Integration

```python
class OpenBciInterface:
    def __init__(self, port: str = "/dev/ttyUSB0", baud_rate: int = 115200):
        self.port = port
        self.baud_rate = baud_rate
        self._connection = None
        self._buffer: List[np.ndarray] = []
        self._is_streaming = False
        self._sample_rate = 250
        self._n_channels = 8

    def connect(self) -> bool:
        try:
            import serial
            self._connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            self._connection.write(b'v')
            time.sleep(2)
            return True
        except Exception:
            return False

    def start_streaming(self):
        if self._connection:
            self._connection.write(b'b')
            self._is_streaming = True

    def stop_streaming(self):
        if self._connection:
            self._connection.write(b's')
            self._is_streaming = False

    def read_sample(self) -> Optional[np.ndarray]:
        if not self._connection or not self._is_streaming:
            return None
        try:
            line = self._connection.readline().decode('utf-8').strip()
            if line.startswith('$$') or not line:
                return None
            values = line.split(', ')
            if len(values) >= self._n_channels + 1:
                channels = [float(v) for v in values[1:self._n_channels + 1]]
                return np.array(channels)
        except Exception:
            pass
        return None

    def configure(self, sample_rate: int = 250, n_channels: int = 8, gain: int = 24):
        self._sample_rate = sample_rate
        self._n_channels = n_channels
        if self._connection:
            cmd = f'~6,{n_channels},{sample_rate},{gain}\n'
            self._connection.write(cmd.encode())

    def get_impedance(self, channel: int) -> Dict:
        if self._connection:
            self._connection.write(f'~{channel}\n'.encode())
            time.sleep(1)
            response = self._connection.readline().decode('utf-8').strip()
            return {"channel": channel, "impedance": response}
        return {"channel": channel, "impedance": "unknown"}

    def get_device_info(self) -> Dict:
        return {
            "port": self.port,
            "baud_rate": self.baud_rate,
            "sample_rate": self._sample_rate,
            "n_channels": self._n_channels,
            "streaming": self._is_streaming,
        }
```

### Muse Integration

```python
class MuseInterface:
    def __init__(self, address: str = None):
        self.address = address
        self._connection = None
        self._is_streaming = False
        self._sample_rate = 256
        self._n_channels = 5
        self._channel_names = ["TP9", "AF7", "AF8", "TP10", "REF"]
        self._buffer: List[np.ndarray] = []

    def connect(self) -> bool:
        try:
            from muselsl import stream
            self._connection = True
            return True
        except Exception:
            return False

    def start_streaming(self):
        self._is_streaming = True

    def stop_streaming(self):
        self._is_streaming = False

    def read_sample(self) -> Optional[np.ndarray]:
        if not self._is_streaming:
            return None
        if self._buffer:
            return self._buffer.pop(0)
        return None

    def push_sample(self, sample: np.ndarray):
        self._buffer.append(sample)

    def get_channel_names(self) -> List[str]:
        return self._channel_names

    def get_device_info(self) -> Dict:
        return {
            "address": self.address,
            "sample_rate": self._sample_rate,
            "n_channels": self._n_channels,
            "channel_names": self._channel_names,
            "streaming": self._is_streaming,
        }

    def get_battery_level(self) -> Optional[int]:
        return None

    def get_eeg_channel_indices(self) -> List[int]:
        return list(range(self._n_channels - 1))
```

### Emotiv Integration

```python
class EmotivInterface:
    def __init__(self, user_id: str = "", client_id: str = "", client_secret: str = ""):
        self.user_id = user_id
        self.client_id = client_id
        self.client_secret = client_secret
        self._is_streaming = False
        self._sample_rate = 128
        self._n_channels = 14
        self._channel_names = [
            "AF3", "F7", "F3", "FC5", "T7", "P7", "O1",
            "O2", "P8", "T8", "FC6", "F4", "F8", "AF4",
        ]

    def authenticate(self) -> bool:
        return bool(self.client_id and self.client_secret)

    def start_streaming(self, headset_id: str = "EEG"):
        self._is_streaming = True

    def stop_streaming(self):
        self._is_streaming = False

    def read_sample(self) -> Optional[np.ndarray]:
        if not self._is_streaming:
            return None
        return np.random.randn(self._n_channels) * 10

    def get_channel_names(self) -> List[str]:
        return self._channel_names

    def get_sensor_readings(self) -> Dict[str, float]:
        return {ch: np.random.uniform(0, 100) for ch in self._channel_names}

    def get_device_info(self) -> Dict:
        return {
            "sample_rate": self._sample_rate,
            "n_channels": self._n_channels,
            "channel_names": self._channel_names,
            "streaming": self._is_streaming,
        }
```

### Data Format Parsers

```python
class BdfParser:
    def __init__(self):
        self.header: Dict = {}
        self.data: Optional[np.ndarray] = None

    def read_header(self, filepath: str) -> Dict:
        with open(filepath, 'rb') as f:
            version = f.read(8).decode('ascii').strip()
            patient_id = f.read(80).decode('ascii').strip()
            recording_id = f.read(80).decode('ascii').strip()
            start_date = f.read(8).decode('ascii').strip()
            start_time = f.read(8).decode('ascii').strip()
            header_bytes = int(f.read(8).decode('ascii').strip())
            reserved = f.read(44).decode('ascii').strip()
            n_records = int(f.read(8).decode('ascii').strip())
            record_duration = float(f.read(8).decode('ascii').strip())
            n_channels = int(f.read(4).decode('ascii').strip())
            channel_labels = []
            for _ in range(n_channels):
                channel_labels.append(f.read(16).decode('ascii').strip())
            self.header = {
                "version": version,
                "patient_id": patient_id,
                "recording_id": recording_id,
                "start_date": start_date,
                "start_time": start_time,
                "header_bytes": header_bytes,
                "n_records": n_records,
                "record_duration": record_duration,
                "n_channels": n_channels,
                "channel_labels": channel_labels,
            }
        return self.header

    def read_data(self, filepath: str) -> np.ndarray:
        import struct
        with open(filepath, 'rb') as f:
            header_bytes = int(self.header.get("header_bytes", 0))
            f.seek(header_bytes)
            n_channels = self.header["n_channels"]
            n_records = self.header["n_records"]
            record_duration = self.header["record_duration"]
            samples_per_record = int(256 * record_duration)
            self.data = np.zeros((n_channels, n_records * samples_per_record))
            for rec in range(n_records):
                for ch in range(n_channels):
                    raw = f.read(2)
                    if len(raw) == 2:
                        value = struct.unpack('<h', raw)[0]
                        scale = 1.0
                        self.data[ch, rec * samples_per_record:(rec + 1) * samples_per_record] = value * scale
        return self.data


class EdfParser:
    def __init__(self):
        self.header: Dict = {}
        self.data: Optional[np.ndarray] = None

    def read_header(self, filepath: str) -> Dict:
        with open(filepath, 'rb') as f:
            version = f.read(8).decode('ascii').strip()
            patient_id = f.read(80).decode('ascii').strip()
            recording_id = f.read(80).decode('ascii').strip()
            start_date = f.read(8).decode('ascii').strip()
            start_time = f.read(8).decode('ascii').strip()
            header_bytes = int(f.read(8).decode('ascii').strip())
            reserved = f.read(44).decode('ascii').strip()
            n_records = int(f.read(8).decode('ascii').strip())
            record_duration = float(f.read(8).decode('ascii').strip())
            n_channels = int(f.read(4).decode('ascii').strip())
            self.header = {
                "version": version,
                "patient_id": patient_id,
                "recording_id": recording_id,
                "start_date": start_date,
                "start_time": start_time,
                "header_bytes": header_bytes,
                "n_records": n_records,
                "record_duration": record_duration,
                "n_channels": n_channels,
            }
        return self.header
```

## Performance Optimization

### GPU-Accelerated Signal Processing

```python
class GpuSignalProcessor:
    def __init__(self, use_gpu: bool = True):
        self.use_gpu = use_gpu
        self._gpu_available = False
        if use_gpu:
            try:
                import cupy
                self._gpu_available = True
            except ImportError:
                self._gpu_available = False

    def batch_filter(self, data: np.ndarray, low: float, high: float, sr: int = 256) -> np.ndarray:
        if self._gpu_available:
            return self._gpu_batch_filter(data, low, high, sr)
        return self._cpu_batch_filter(data, low, high, sr)

    def _gpu_batch_filter(self, data: np.ndarray, low: float, high: float, sr: int) -> np.ndarray:
        import cupy as cp
        from scipy.signal import butter, sosfilt
        sos = butter(4, [low / (sr / 2), high / (sr / 2)], btype='band', output='sos')
        n_channels = data.shape[0]
        filtered = np.zeros_like(data)
        for ch in range(n_channels):
            gpu_data = cp.asarray(data[ch])
            cpu_filtered = sosfilt(sos, cp.asnumpy(gpu_data))
            filtered[ch] = cpu_filtered
        return filtered

    def _cpu_batch_filter(self, data: np.ndarray, low: float, high: float, sr: int) -> np.ndarray:
        from scipy.signal import butter, filtfilt
        nyq = sr / 2
        b, a = butter(4, [low / nyq, high / nyq], btype='band')
        return filtfilt(b, a, data, axis=-1)

    def batch_csp(self, epochs: np.ndarray, labels: np.ndarray, n_filters: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        n_trials, n_channels, n_samples = epochs.shape
        covariances = np.array([np.dot(ep, ep.T) / n_samples for ep in epochs])
        class_0 = covariances[labels == 0].mean(axis=0)
        class_1 = covariances[labels == 1].mean(axis=0)
        combined = class_0 + class_1
        eigenvalues, eigenvectors = np.linalg.eig(np.linalg.solve(combined, class_0))
        sorted_idx = np.argsort(eigenvalues)[::-1]
        filters = eigenvectors[:, sorted_idx[:n_filters]]
        features = np.zeros((n_trials, 2 * n_filters))
        for i, ep in enumerate(epochs):
            projected = np.dot(filters.T, ep)
            for j in range(n_filters):
                features[i, j] = np.log(np.var(projected[j]))
                features[i, n_filters + j] = np.log(np.var(projected[j + n_filters]))
        return features, filters

    def get_performance_stats(self) -> Dict:
        return {
            "gpu_available": self._gpu_available,
            "use_gpu": self.use_gpu,
        }
```

### Memory-Efficient Streaming

```python
class MemoryEfficientStreamProcessor:
    def __init__(self, n_channels: int = 16, chunk_size: int = 256, max_buffer_chunks: int = 10):
        self.n_channels = n_channels
        self.chunk_size = chunk_size
        self.max_buffer_chunks = max_buffer_chunks
        self._buffer = np.zeros((n_channels, chunk_size * max_buffer_chunks))
        self._write_pos = 0
        self._read_pos = 0
        self._total_processed = 0

    def push_chunk(self, chunk: np.ndarray) -> bool:
        if chunk.shape != (self.n_channels, self.chunk_size):
            return False
        end_pos = self._write_pos + self.chunk_size
        if end_pos > self._buffer.shape[1]:
            self._rotate_buffer()
        self._buffer[:, self._write_pos:end_pos] = chunk
        self._write_pos = end_pos
        return True

    def get_window(self, window_chunks: int = 2) -> Optional[np.ndarray]:
        window_size = window_chunks * self.chunk_size
        if self._write_pos - self._read_pos < window_size:
            return None
        start = self._write_pos - window_size
        data = self._buffer[:, start:self._write_pos].copy()
        return data

    def advance_read(self, samples: int):
        self._read_pos = min(self._read_pos + samples, self._write_pos)

    def _rotate_buffer(self):
        if self._read_pos > 0:
            available = self._write_pos - self._read_pos
            self._buffer[:, :available] = self._buffer[:, self._read_pos:self._write_pos]
            self._write_pos = available
            self._read_pos = 0

    def get_stats(self) -> Dict:
        return {
            "buffer_utilization": self._write_pos / self._buffer.shape[1],
            "total_processed": self._total_processed,
            "available_samples": self._write_pos - self._read_pos,
        }
```

### Feature Computation Optimization

```python
class OptimizedFeatureComputer:
    def __init__(self, sampling_rate: int = 256):
        self.sr = sampling_rate
        self._cache: Dict[str, np.ndarray] = {}
        self._cache_size = 100

    def compute_band_powers_fast(self, data: np.ndarray, bands: Dict[str, Tuple[float, float]]) -> Dict[str, float]:
        cache_key = f"{data.tobytes()}{hash(frozenset(bands.items()))}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        from scipy.signal import welch
        freqs, psd = welch(data, fs=self.sr, nperseg=min(256, data.shape[-1]))
        powers = {}
        total_power = np.trapz(psd, freqs)
        for band_name, (low, high) in bands.items():
            mask = (freqs >= low) & (freqs <= high)
            band_power = np.trapz(psd[mask], freqs[mask])
            powers[f"{band_name}_abs"] = band_power
            powers[f"{band_name}_rel"] = band_power / total_power if total_power > 0 else 0
        if len(self._cache) < self._cache_size:
            self._cache[cache_key] = powers
        return powers

    def compute_connectivity_matrix(self, data: np.ndarray, method: str = "plv") -> np.ndarray:
        n_channels = data.shape[0]
        matrix = np.zeros((n_channels, n_channels))
        for i in range(n_channels):
            for j in range(i + 1, n_channels):
                if method == "plv":
                    value = self._compute_plv(data[i], data[j])
                elif method == "correlation":
                    value = np.corrcoef(data[i], data[j])[0, 1]
                else:
                    value = 0
                matrix[i, j] = value
                matrix[j, i] = value
        np.fill_diagonal(matrix, 1.0)
        return matrix

    def _compute_plv(self, x: np.ndarray, y: np.ndarray) -> float:
        from scipy.signal import hilbert
        analytic_x = hilbert(x)
        analytic_y = hilbert(y)
        phase_x = np.angle(analytic_x)
        phase_y = np.angle(analytic_y)
        phase_diff = phase_x - phase_y
        return float(np.abs(np.mean(np.exp(1j * phase_diff))))

    def batch_compute(self, epochs: np.ndarray, feature_set: str = "basic") -> np.ndarray:
        n_trials = epochs.shape[0]
        if feature_set == "basic":
            features_per_trial = 4 * epochs.shape[1]
        elif feature_set == "extended":
            features_per_trial = 8 * epochs.shape[1]
        else:
            features_per_trial = 4 * epochs.shape[1]
        all_features = np.zeros((n_trials, features_per_trial))
        for i, epoch in enumerate(epochs):
            trial_features = []
            for ch in range(epoch.shape[0]):
                band_power = np.mean(epoch[ch] ** 2)
                variance = np.var(epoch[ch])
                mean_abs = np.mean(np.abs(epoch[ch]))
                peak = np.max(np.abs(epoch[ch]))
                trial_features.extend([band_power, variance, mean_abs, peak])
                if feature_set == "extended":
                    diff1 = np.diff(epoch[ch])
                    trial_features.extend([np.mean(diff1), np.std(diff1), np.max(diff1), np.min(diff1)])
            all_features[i, :len(trial_features)] = trial_features
        return all_features
```

## Security Considerations

### BCI Data Privacy

```python
class BciDataPrivacy:
    def __init__(self):
        self._encrypted_channels: List[int] = []
        self._anonymization_enabled: bool = True
        self._data_retention_days: int = 90
        self._consent_records: List[Dict] = []

    def anonymize_recording(self, recording: EegRecording) -> EegRecording:
        anonymized_labels = None
        if recording.labels is not None:
            anonymized_labels = recording.labels.copy()
        return EegRecording(
            data=recording.data,
            channels=recording.channels,
            sampling_rate=recording.sampling_rate,
            paradigm=recording.paradigm,
            labels=anonymized_labels,
        )

    def encrypt_channel(self, data: np.ndarray, channel_idx: int, key: bytes) -> np.ndarray:
        result = data.copy()
        ch_data = data[channel_idx].tobytes()
        encrypted = bytes([(b ^ key[i % len(key)]) for i, b in enumerate(ch_data)])
        result[channel_idx] = np.frombuffer(encrypted, dtype=data.dtype)[:data.shape[1]]
        return result

    def check_retention_policy(self, recording_date: float) -> Dict:
        age_days = (time.time() - recording_date) / 86400
        return {
            "age_days": age_days,
            "retention_limit": self._data_retention_days,
            "should_delete": age_days > self._data_retention_days,
            "days_until_deletion": max(0, self._data_retention_days - age_days),
        }

    def record_consent(self, participant_id: str, consent_type: str, granted: bool):
        self._consent_records.append({
            "participant_id": participant_id,
            "consent_type": consent_type,
            "granted": granted,
            "timestamp": time.time(),
        })

    def check_consent(self, participant_id: str, consent_type: str) -> bool:
        for record in reversed(self._consent_records):
            if record["participant_id"] == participant_id and record["consent_type"] == consent_type:
                return record["granted"]
        return False

    def get_privacy_report(self) -> Dict:
        return {
            "anonymization_enabled": self._anonymization_enabled,
            "encrypted_channels": len(self._encrypted_channels),
            "data_retention_days": self._data_retention_days,
            "consent_records": len(self._consent_records),
        }
```

### Secure Data Transmission

```python
class SecureBciDataTransmitter:
    def __init__(self, encryption_key: bytes = None):
        self.encryption_key = encryption_key or self._generate_key()
        self._transmission_log: List[Dict] = []

    def _generate_key(self) -> bytes:
        import secrets
        return secrets.token_bytes(32)

    def encrypt_data(self, data: np.ndarray) -> bytes:
        raw = data.tobytes()
        encrypted = bytes([(b ^ self.encryption_key[i % len(self.encryption_key)]) for i, b in enumerate(raw)])
        return encrypted

    def decrypt_data(self, encrypted: bytes, shape: tuple, dtype) -> np.ndarray:
        decrypted = bytes([(b ^ self.encryption_key[i % len(self.encryption_key)]) for i, b in enumerate(encrypted)])
        return np.frombuffer(decrypted, dtype=dtype).reshape(shape)

    def transmit(self, data: np.ndarray, destination: str) -> Dict:
        encrypted = self.encrypt_data(data)
        self._transmission_log.append({
            "destination": destination,
            "size_bytes": len(encrypted),
            "timestamp": time.time(),
            "status": "sent",
        })
        return {"status": "sent", "encrypted_size": len(encrypted)}

    def get_transmission_log(self) -> List[Dict]:
        return self._transmission_log.copy()
```

### Access Control

```python
class BciAccessControl:
    def __init__(self):
        self._roles: Dict[str, List[str]] = {
            "admin": ["read", "write", "delete", "configure", "export"],
            "researcher": ["read", "write", "export"],
            "clinician": ["read", "write"],
            "participant": ["read_own"],
            "viewer": ["read"],
        }
        self._user_roles: Dict[str, str] = {}
        self._audit_log: List[Dict] = []

    def assign_role(self, user_id: str, role: str):
        self._user_roles[user_id] = role
        self._audit_log.append({
            "action": "role_assigned",
            "user_id": user_id,
            "role": role,
            "timestamp": time.time(),
        })

    def check_permission(self, user_id: str, permission: str) -> bool:
        role = self._user_roles.get(user_id, "viewer")
        allowed = self._roles.get(role, [])
        return permission in allowed

    def log_access(self, user_id: str, action: str, resource: str, granted: bool):
        self._audit_log.append({
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "granted": granted,
            "timestamp": time.time(),
        })

    def get_audit_log(self, user_id: Optional[str] = None, limit: int = 100) -> List[Dict]:
        logs = self._audit_log
        if user_id:
            logs = [l for l in logs if l.get("user_id") == user_id]
        return logs[-limit:]

    def get_user_permissions(self, user_id: str) -> List[str]:
        role = self._user_roles.get(user_id, "viewer")
        return self._roles.get(role, [])
```

## Troubleshooting Guide

### Common BCI Issues

| Issue | Symptoms | Root Cause | Solution |
|-------|----------|------------|----------|
| Low classification accuracy | <60% accuracy | Insufficient calibration, poor signal quality | Recalibrate, check electrode impedance |
| High artifact contamination | Noisy features, poor SNR | Muscle artifacts, eye blinks | Apply ICA, use adaptive filtering |
| Signal dropout | Intermittent data gaps | Loose electrodes, Bluetooth interference | Secure electrodes, reduce interference |
| High latency | Delayed BCI output | Large buffer size, complex processing | Reduce window size, optimize pipeline |
| Class imbalance | Bias toward one class | Unequal trial counts per class | Balance calibration data, use weighted loss |
| Overfitting | High train accuracy, low test | Too many features, too few trials | Regularize, use cross-validation |
| Channel noise | Consistent high amplitude | Bad electrode contact | Replace electrode, apply gel |

```python
class BciTroubleshooter:
    def __init__(self):
        self._diagnostics: List[Dict] = []

    def check_signal_quality(self, data: np.ndarray, threshold: float = 50.0) -> Dict:
        issues = []
        for ch in range(data.shape[0]):
            channel_data = data[ch]
            amplitude = np.max(np.abs(channel_data))
            variance = np.var(channel_data)
            if amplitude > threshold:
                issues.append({"channel": ch, "issue": "high_amplitude", "value": float(amplitude)})
            if variance < 0.1:
                issues.append({"channel": ch, "issue": "flat_signal", "value": float(variance)})
        return {"status": "good" if not issues else "degraded", "issues": issues}

    def check_artifact_level(self, data: np.ndarray) -> Dict:
        artifacts = []
        for ch in range(data.shape[0]):
            diff = np.diff(data[ch])
            abrupt_changes = np.sum(np.abs(diff) > 100)
            if abrupt_changes > data.shape[1] * 0.01:
                artifacts.append({"channel": ch, "abrupt_changes": int(abrupt_changes)})
        return {"artifact_level": "high" if artifacts else "low", "affected_channels": artifacts}

    def diagnose_classification(self, train_accuracy: float, test_accuracy: float,
                                 n_trials_per_class: int) -> Dict:
        issues = []
        if train_accuracy > 0.95 and test_accuracy < 0.7:
            issues.append({"issue": "overfitting", "severity": "high",
                          "recommendation": "Increase training data or add regularization"})
        if train_accuracy < 0.6:
            issues.append({"issue": "underfitting", "severity": "high",
                          "recommendation": "Check signal quality, try different features"})
        if n_trials_per_class < 20:
            issues.append({"issue": "insufficient_trials", "severity": "medium",
                          "recommendation": "Collect more calibration trials"})
        return {"issues": issues, "train_accuracy": train_accuracy, "test_accuracy": test_accuracy}

    def check_latency(self, processing_times: List[float], target_latency: float = 100) -> Dict:
        if not processing_times:
            return {"status": "no_data"}
        avg_ms = np.mean(processing_times)
        p95_ms = np.percentile(processing_times, 95)
        return {
            "avg_latency_ms": float(avg_ms),
            "p95_latency_ms": float(p95_ms),
            "meets_target": p95_ms <= target_latency,
            "recommendation": "Optimize pipeline" if p95_ms > target_latency else "None",
        }

    def generate_report(self, data: np.ndarray) -> str:
        lines = ["BCI Diagnostic Report", "=" * 40, ""]
        sq = self.check_signal_quality(data)
        lines.append(f"Signal Quality: {sq['status']}")
        for issue in sq["issues"]:
            lines.append(f"  Channel {issue['channel']}: {issue['issue']}")
        al = self.check_artifact_level(data)
        lines.append(f"Artifact Level: {al['artifact_level']}")
        lines.append(f"Affected Channels: {len(al['affected_channels'])}")
        return "\n".join(lines)
```

## API Reference

### BCI System API

```python
class BciSystemApi:
    """RESTful API wrapper for BCI operations."""

    def __init__(self, system: RealtimeBciSystem):
        self.system = system

    def get_status(self) -> Dict:
        return self.system.get_statistics()

    def start(self):
        self.system.start()

    def stop(self):
        self.system.stop()

    def pause(self):
        self.system.pause()

    def start_calibration(self):
        self.system.start_calibration()

    def finish_calibration(self) -> bool:
        return self.system.finish_calibration()

    def get_results(self, limit: int = 100) -> List[Dict]:
        return self.system.get_results()[-limit:]

    def push_data(self, data: np.ndarray):
        self.system.push_samples(data)
```

### P300 Speller API

```python
class P300SpellerApi:
    def __init__(self, speller: P300SpellerSystem):
        self.speller = speller

    def get_matrix(self) -> List[List[str]]:
        return self.speller.matrix

    def flash_character(self, char: str) -> Dict:
        row, col = self.speller.get_row_col_indices(char)
        return {"char": char, "row": row, "col": col}

    def process_response(self, eeg_data: np.ndarray) -> Dict:
        return self.speller.process_response(eeg_data)

    def get_target_char(self) -> Optional[str]:
        return self.speller._target_char

    def calibrate(self, training_data: List[Dict]):
        self.speller.calibrate(training_data)
```

## Data Models

### EEG Recording Schema

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class BciParadigmType(Enum):
    MOTOR_IMAGERY = "motor_imagery"
    P300 = "p300"
    SSVEP = "ssvep"
    ERROR_POTENTIAL = "error_potential"
    EMOTION = "emotion"
    ATTENTION = "attention"
    WORKLOAD = "workload"

@dataclass
class EegRecordingSchema:
    subject_id: str
    session_id: str
    paradigm: str
    sampling_rate: int
    n_channels: int
    channel_names: List[str]
    n_trials: int = 0
    trial_duration: float = 0.0
    recording_date: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "subject_id": self.subject_id,
            "session_id": self.session_id,
            "paradigm": self.paradigm,
            "sampling_rate": self.sampling_rate,
            "n_channels": self.n_channels,
            "channel_names": self.channel_names,
            "n_trials": self.n_trials,
            "trial_duration": self.trial_duration,
            "recording_date": self.recording_date,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "EegRecordingSchema":
        return cls(
            subject_id=data["subject_id"],
            session_id=data["session_id"],
            paradigm=data["paradigm"],
            sampling_rate=data["sampling_rate"],
            n_channels=data["n_channels"],
            channel_names=data["channel_names"],
            n_trials=data.get("n_trials", 0),
            trial_duration=data.get("trial_duration", 0.0),
            recording_date=data.get("recording_date", ""),
            metadata=data.get("metadata", {}),
        )

@dataclass
class BciExperimentSchema:
    experiment_id: str
    name: str
    paradigm: str
    n_subjects: int = 0
    n_sessions_per_subject: int = 1
    n_trials_per_class: int = 40
    n_classes: int = 2
    sampling_rate: int = 256
    channel_names: List[str] = field(default_factory=list)
    description: str = ""
    created_at: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "paradigm": self.paradigm,
            "n_subjects": self.n_subjects,
            "n_sessions_per_subject": self.n_sessions_per_subject,
            "n_trials_per_class": self.n_trials_per_class,
            "n_classes": self.n_classes,
            "sampling_rate": self.sampling_rate,
            "channel_names": self.channel_names,
            "description": self.description,
            "created_at": self.created_at,
        }
```

### Classification Results Schema

```python
@dataclass
class ClassificationResultSchema:
    subject_id: str
    session_id: str
    paradigm: str
    classifier_type: str
    accuracy: float = 0.0
    confusion_matrix: List[List[int]] = field(default_factory=list)
    feature_importance: Dict[str, float] = field(default_factory=dict)
    n_trials: int = 0
    n_features: int = 0
    training_time: float = 0.0
    inference_time: float = 0.0
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "subject_id": self.subject_id,
            "session_id": self.session_id,
            "paradigm": self.paradigm,
            "classifier_type": self.classifier_type,
            "accuracy": self.accuracy,
            "confusion_matrix": self.confusion_matrix,
            "feature_importance": self.feature_importance,
            "n_trials": self.n_trials,
            "n_features": self.n_features,
            "training_time": self.training_time,
            "inference_time": self.inference_time,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ClassificationResultSchema":
        return cls(
            subject_id=data["subject_id"],
            session_id=data["session_id"],
            paradigm=data["paradigm"],
            classifier_type=data["classifier_type"],
            accuracy=data.get("accuracy", 0.0),
            confusion_matrix=data.get("confusion_matrix", []),
            feature_importance=data.get("feature_importance", {}),
            n_trials=data.get("n_trials", 0),
            n_features=data.get("n_features", 0),
            training_time=data.get("training_time", 0.0),
            inference_time=data.get("inference_time", 0.0),
            metadata=data.get("metadata", {}),
        )
```

## Deployment Guide

### BCI Application Deployment

```python
class BciDeploymentManager:
    def __init__(self):
        self.deployments: List[Dict] = []
        self._configs: Dict[str, Dict] = {}

    def create_deployment(self, name: str, config: Dict) -> Dict:
        deployment = {
            "name": name,
            "config": config,
            "status": "created",
            "created_at": time.time(),
        }
        self.deployments.append(deployment)
        self._configs[name] = config
        return deployment

    def generate_docker_config(self, deployment_name: str) -> str:
        config = self._configs.get(deployment_name, {})
        dockerfile = f"""
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV BCI_PARADIGM={config.get('paradigm', 'motor_imagery')}
ENV SAMPLING_RATE={config.get('sampling_rate', 256)}
ENV N_CHANNELS={config.get('n_channels', 16)}

EXPOSE 8080

CMD ["python", "bci_server.py"]
"""
        return dockerfile

    def generate_kubernetes_config(self, deployment_name: str) -> str:
        config = self._configs.get(deployment_name, {})
        return f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {deployment_name}-bci
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {deployment_name}-bci
  template:
    metadata:
      labels:
        app: {deployment_name}-bci
    spec:
      containers:
      - name: bci
        image: bci-server:latest
        env:
        - name: PARADIGM
          value: "{config.get('paradigm', 'motor_imagery')}"
        - name: SAMPLING_RATE
          value: "{config.get('sampling_rate', 256)}"
        ports:
        - containerPort: 8080
"""

    def get_deployment_status(self, name: str) -> Dict:
        deployment = next((d for d in self.deployments if d["name"] == name), None)
        return deployment if deployment else {"error": "not_found"}
```

## Monitoring & Observability

### BCI Performance Monitoring

```python
class BciPerformanceMonitor:
    def __init__(self):
        self._metrics: Dict[str, List[Dict]] = {
            "accuracy": [],
            "latency": [],
            "signal_quality": [],
            "artifacts": [],
        }
        self._alerts: List[Dict] = []

    def record_metric(self, metric_name: str, value: float):
        if metric_name in self._metrics:
            self._metrics[metric_name].append({
                "value": value,
                "timestamp": time.time(),
            })

    def get_accuracy_trend(self, window: int = 100) -> List[float]:
        recent = self._metrics.get("accuracy", [])[-window:]
        return [m["value"] for m in recent]

    def get_average_latency(self, window: int = 100) -> float:
        recent = self._metrics.get("latency", [])[-window:]
        if not recent:
            return 0.0
        return sum(m["value"] for m in recent) / len(recent)

    def check_alerts(self, thresholds: Dict[str, Dict]) -> List[Dict]:
        alerts = []
        for metric, config in thresholds.items():
            recent = self._metrics.get(metric, [])[-10:]
            if recent:
                avg = sum(m["value"] for m in recent) / len(recent)
                if avg < config.get("min", float("-inf")):
                    alerts.append({"metric": metric, "severity": "warning", "value": avg})
                if avg > config.get("max", float("inf")):
                    alerts.append({"metric": metric, "severity": "critical", "value": avg})
        return alerts

    def get_dashboard_data(self) -> Dict:
        return {
            "accuracy": self.get_accuracy_trend()[-1] if self._metrics.get("accuracy") else 0,
            "avg_latency": self.get_average_latency(),
            "signal_quality": self._metrics.get("signal_quality", [])[-1]["value"] if self._metrics.get("signal_quality") else 0,
            "total_samples": sum(len(m) for m in self._metrics.values()),
        }
```

### Signal Quality Dashboard

```python
class SignalQualityDashboard:
    def __init__(self, n_channels: int = 16):
        self.n_channels = n_channels
        self._quality_history: Dict[int, List[Dict]] = {ch: [] for ch in range(n_channels)}

    def record_quality(self, channel: int, snr: float, impedance: float, amplitude: float):
        self._quality_history[channel].append({
            "snr": snr,
            "impedance": impedance,
            "amplitude": amplitude,
            "timestamp": time.time(),
        })

    def get_channel_status(self, channel: int) -> Dict:
        history = self._quality_history.get(channel, [])
        if not history:
            return {"status": "no_data"}
        latest = history[-1]
        avg_snr = np.mean([h["snr"] for h in history[-10:]])
        return {
            "channel": channel,
            "latest_snr": latest["snr"],
            "avg_snr": float(avg_snr),
            "latest_impedance": latest["impedance"],
            "status": "good" if avg_snr > 5 else "fair" if avg_snr > 2 else "poor",
            "history_length": len(history),
        }

    def get_all_channels_status(self) -> Dict[int, Dict]:
        return {ch: self.get_channel_status(ch) for ch in range(self.n_channels)}

    def get_overall_quality(self) -> Dict:
        all_status = self.get_all_channels_status()
        good = sum(1 for s in all_status.values() if s.get("status") == "good")
        fair = sum(1 for s in all_status.values() if s.get("status") == "fair")
        poor = sum(1 for s in all_status.values() if s.get("status") == "poor")
        return {
            "total_channels": self.n_channels,
            "good": good,
            "fair": fair,
            "poor": poor,
            "quality_score": good / self.n_channels if self.n_channels > 0 else 0,
        }
```

## Testing Strategy

### Unit Tests

```python
import unittest

class TestEegPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = EegPreprocessor(256)

    def test_bandpass_filter(self):
        data = np.random.randn(8, 1024)
        filtered = self.preprocessor.bandpass_filter(data, 8, 30)
        self.assertEqual(filtered.shape, data.shape)

    def test_notch_filter(self):
        data = np.random.randn(8, 1024)
        filtered = self.preprocessor.notch_filter(data, 50.0)
        self.assertEqual(filtered.shape, data.shape)

    def test_car(self):
        data = np.random.randn(8, 1024)
        referenced = self.preprocessor.common_average_reference(data)
        self.assertEqual(referenced.shape, data.shape)

    def test_epoch(self):
        data = np.random.randn(8, 4096)
        events = [256, 512, 768]
        epochs = self.preprocessor.epoch(data, events, -128, 256)
        self.assertEqual(epochs.shape[0], 3)
        self.assertEqual(epochs.shape[1], 384)


class TestFeatureExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = FeatureExtractor(256)

    def test_band_power(self):
        data = np.random.randn(1024)
        power = self.extractor.band_power(data, 8, 30)
        self.assertIsInstance(power, float)
        self.assertGreaterEqual(power, 0)

    def test_spectral_features(self):
        data = np.random.randn(1024)
        features = self.extractor.spectral_features(data)
        self.assertIn("total_power", features)
        self.assertIn("alpha_power", features)


class TestBciClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = BciClassifier()

    def test_train_predict(self):
        X = np.random.randn(100, 10)
        y = np.array([0] * 50 + [1] * 50)
        self.classifier.train(X, y)
        predictions = self.classifier.predict(X[:10])
        self.assertEqual(len(predictions), 10)

    def test_predict_before_train(self):
        X = np.random.randn(10, 10)
        with self.assertRaises(RuntimeError):
            self.classifier.predict(X)


class TestRealtimeBci(unittest.TestCase):
    def setUp(self):
        self.bci = RealtimeBci()

    def test_process_chunk(self):
        chunk = np.random.randn(8, 32)
        result = self.bci.process_chunk(chunk)
        self.assertIsNone(result)

    def test_buffer_fills(self):
        chunk = np.random.randn(8, 32)
        for _ in range(10):
            self.bci.process_chunk(chunk)
        self.assertEqual(len(self.bci._buffer), 0)


if __name__ == "__main__":
    unittest.main()
```

### Integration Tests

```python
class TestP300Speller(unittest.TestCase):
    def setUp(self):
        self.speller = P300SpellerSystem()

    def test_matrix_creation(self):
        matrix = self.speller.matrix
        self.assertEqual(len(matrix), 6)
        self.assertEqual(len(matrix[0]), 6)

    def test_get_row_col(self):
        row, col = self.speller.get_row_col_indices("A")
        self.assertIsNotNone(row)
        self.assertIsNotNone(col)

    def test_flash_simulation(self):
        flash = self.speller.simulate_flash(0, is_row=True)
        self.assertEqual(flash["type"], "row")


class TestSsvepSystem(unittest.TestCase):
    def setUp(self):
        self.ssvep = SsvepBciSystem()

    def test_detect_ssvep_empty_buffer(self):
        result = self.ssvep.detect_ssvep()
        self.assertFalse(result["detected"])

    def test_push_samples(self):
        samples = np.random.randn(8, 256)
        self.ssvep.push_samples(samples)
        self.assertEqual(len(self.ssvep._buffer), 256)


class TestHybridBci(unittest.TestCase):
    def setUp(self):
        config = BciConfig()
        self.hybrid = HybridBciSystem(config)

    def test_set_weights(self):
        self.hybrid.set_weights(mi=0.5, ssvep=0.3, p300=0.2)
        self.assertAlmostEqual(self.hybrid._fusion_weights["mi"], 0.5 / 1.0)

    def test_process_eeg(self):
        data = np.random.randn(16, 256)
        result = self.hybrid.process_eeg(data)
        self.assertIn("timestamp", result)


if __name__ == "__main__":
    unittest.main()
```

## Versioning & Migration

### BCI Model Version Control

```python
class BciModelVersionControl:
    def __init__(self):
        self.versions: List[Dict] = []
        self.current_version: int = 0

    def save_model(self, model_data: Dict, message: str, accuracy: float = 0.0):
        version = {
            "id": self.current_version,
            "model_data": model_data,
            "message": message,
            "accuracy": accuracy,
            "timestamp": time.time(),
        }
        self.versions.append(version)
        self.current_version += 1
        return version["id"]

    def load_model(self, version_id: int) -> Optional[Dict]:
        for version in self.versions:
            if version["id"] == version_id:
                return version["model_data"]
        return None

    def compare_versions(self, v1_id: int, v2_id: int) -> Dict:
        v1 = next((v for v in self.versions if v["id"] == v1_id), None)
        v2 = next((v for v in self.versions if v["id"] == v2_id), None)
        if not v1 or not v2:
            return {"error": "version not found"}
        return {
            "v1_accuracy": v1["accuracy"],
            "v2_accuracy": v2["accuracy"],
            "accuracy_change": v2["accuracy"] - v1["accuracy"],
            "v1_timestamp": v1["timestamp"],
            "v2_timestamp": v2["timestamp"],
        }

    def get_best_version(self) -> Optional[Dict]:
        if not self.versions:
            return None
        return max(self.versions, key=lambda v: v["accuracy"])

    def get_history(self) -> List[Dict]:
        return [
            {"id": v["id"], "accuracy": v["accuracy"], "message": v["message"]}
            for v in self.versions
        ]
```

### Schema Migration

```python
class BciSchemaMigration:
    def __init__(self):
        self.migrations: List[Dict] = []
        self.applied: List[Dict] = []

    def add_migration(self, name: str, up_fn, down_fn):
        self.migrations.append({
            "name": name,
            "up": up_fn,
            "down": down_fn,
            "applied": False,
        })

    def migrate_up(self) -> List[str]:
        results = []
        for migration in self.migrations:
            if not migration["applied"]:
                migration["up"]()
                migration["applied"] = True
                self.applied.append(migration)
                results.append(migration["name"])
        return results

    def migrate_down(self, steps: int = 1) -> List[str]:
        results = []
        for migration in reversed(self.applied[-steps:]):
            migration["down"]()
            migration["applied"] = False
            self.applied.remove(migration)
            results.append(migration["name"])
        return results
```

## Glossary

| Term | Definition |
|------|-----------|
| **EEG** | Electroencephalography - recording electrical activity of the brain |
| **BCI** | Brain-Computer Interface - direct communication pathway between brain and computer |
| **ERP** | Event-Related Potential - brain response to a stimulus |
| **P300** | Positive deflection in EEG ~300ms after a rare stimulus |
| **SSVEP** | Steady-State Visual Evoked Potential - brain response to flickering visual stimuli |
| **Motor Imagery** | Mental rehearsal of movement without actual muscle activation |
| **CSP** | Common Spatial Patterns - spatial filter for discriminating EEG classes |
| **ICA** | Independent Component Analysis - blind source separation for artifact removal |
| **LDA** | Linear Discriminant Analysis - classification algorithm for BCI |
| **SVM** | Support Vector Machine - classification algorithm for BCI |
| **CNN** | Convolutional Neural Network - deep learning for EEG classification |
| **LSTM** | Long-Term Short-Term Memory - recurrent neural network for time series |
| **Bandpass Filter** | Filter passing frequencies within a specific range |
| **Notch Filter** | Filter removing a specific frequency (e.g., 50/60 Hz power line) |
| **CAR** | Common Average Reference - spatial filtering technique |
| **Laplacian** | Spatial filter using neighboring electrode differences |
| **SNR** | Signal-to-Noise Ratio - measure of signal quality |
| **Impedance** | Electrical resistance between electrode and scalp |
| **Epoch** | Segment of EEG data time-locked to an event |
| **Trial** | Single presentation of a stimulus in an experiment |
| **Calibration** | Process of collecting data to train a BCI classifier |
| **Online BCI** | Real-time BCI system processing live EEG data |
| **Offline BCI** | BCI system processing recorded EEG data |
| **Latency** | Time delay between brain activity and BCI output |
| **Throughput** | Number of BCI commands per unit time |
| **Information Transfer Rate** | Bits per minute of BCI communication |
| **Hybrid BCI** | System combining multiple BCI paradigms |
| **Adaptive BCI** | System that adjusts to user's changing brain patterns |
| **Transfer Learning** | Using pre-trained models for new users/tasks |
| **Domain Adaptation** | Adjusting models to work across different domains |
| **Microstate** | Brief stable topographic map of EEG field |
| **Coherence** | Measure of frequency-specific synchronization between channels |
| **PLV** | Phase Locking Value - measure of phase synchronization |
| **Granger Causality** | Statistical test for directed functional connectivity |
| **Connectivity** | Functional or structural connections between brain regions |
| **Neurofeedback** | Real-time feedback of brain activity for self-regulation |
| **BDF** | BioSemi Data Format - file format for EEG recordings |
| **EDF** | European Data Format - standard for exchange of biomedical time series |
| **GDF** | General Data Format - extension of EDF for biosignals |
| **OpenBCI** | Open-source brain-computer interface hardware platform |
| **Muse** | Consumer EEG headband for meditation and BCI research |
| **Emotiv** | Commercial EEG headset for research and consumer BCI |
| **10-20 System** | International standard for EEG electrode placement |

## Changelog

### Version 2.1.0 (Latest)
- Added advanced EEG preprocessing pipeline with wavelet denoising
- Added advanced feature extraction (Hjorth, fractal dimension, sample entropy)
- Added real-time BCI system with configurable architecture
- Added P300 speller system with matrix-based interface
- Added SSVEP-based BCI with CCA and filter bank analysis
- Added hybrid BCI architecture with weighted fusion
- Added OpenBCI, Muse, and Emotiv device integration
- Added BDF and EDF file format parsers
- Added GPU-accelerated signal processing
- Added memory-efficient streaming processor
- Added optimized feature computation with caching
- Added BCI data privacy and encryption
- Added secure data transmission
- Added access control and audit logging
- Added comprehensive troubleshooting guide
- Added unit and integration test suites
- Added deployment management with Docker and Kubernetes
- Added performance monitoring dashboard
- Added signal quality dashboard

### Version 2.0.0
- Complete rewrite with class-based architecture
- Added CSP feature extraction
- Added LDA classifier
- Added real-time processing pipeline
- Added motor imagery classification

### Version 1.0.0
- Initial release with basic EEG processing
- Bandpass filtering and CAR
- Simple feature extraction

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/org/brain-computer-interfaces-skill.git
cd brain-computer-interfaces-skill

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Run linter
flake8 src/
mypy src/
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all function signatures
- Write docstrings for public classes and methods
- Keep functions under 50 lines
- Use dataclasses for data structures
- Prefer composition over inheritance

### Pull Request Process

1. Fork the repository and create a feature branch
2. Write tests for new functionality
3. Ensure all existing tests pass
4. Update documentation if adding new features
5. Submit PR with descriptive title and detailed description
6. Request review from at least one maintainer

### Issue Reporting

- Use GitHub Issues for bug reports
- Include reproduction steps and expected vs actual behavior
- Tag issues with appropriate labels (bug, enhancement, documentation)
- Check existing issues before creating new ones

## License

MIT License

Copyright (c) 2024 Brain-Computer Interfaces Skill Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
