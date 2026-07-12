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
