"""
Brain-Computer Interface Pipeline
Neural signal processing and BCI
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from dataclasses import field
from enum import Enum


class SignalType(Enum):
    EEG = "eeg"
    ECoG = "ecog"
    MEG = "meg"
    fMRI = "fmri"
    EMG = "emg"


@dataclass
class NeuralSignal:
    signal_type: SignalType
    data: np.ndarray
    sampling_rate: float
    channel_names: List[str]
    timestamp: float
    metadata: Dict = field(default_factory=dict)


@dataclass
class BCISession:
    session_id: str
    subject_id: str
    start_time: float
    end_time: Optional[float]
    signals: List[NeuralSignal]
    events: List[Dict]


class SignalPreprocessor:
    """Neural signal preprocessing"""
    
    def __init__(self):
        self.notch_freq = 50.0
        self.highpass_freq = 0.5
        self.lowpass_freq = 100.0
    
    def preprocess(self, signal: NeuralSignal) -> NeuralSignal:
        """Apply preprocessing pipeline"""
        data = signal.data.copy()
        
        data = self._notch_filter(data, signal.sampling_rate)
        data = self._bandpass_filter(data, signal.sampling_rate)
        data = self._remove_baseline(data)
        data = self._normalize(data)
        
        return NeuralSignal(
            signal_type=signal.signal_type,
            data=data,
            sampling_rate=signal.sampling_rate,
            channel_names=signal.channel_names,
            timestamp=signal.timestamp,
            metadata={**signal.metadata, "preprocessed": True}
        )
    
    def _notch_filter(self, data: np.ndarray, fs: float) -> np.ndarray:
        """Apply notch filter for power line interference"""
        w0 = 2 * np.pi * self.notch_freq / fs
        Q = 30.0
        
        b = np.array([1, -2*np.cos(w0), 1])
        a = np.array([1, -2*np.cos(w0)*np.exp(-1/(2*Q)), np.exp(-1/Q)])
        
        from scipy.signal import lfilter
        return lfilter(b, a, data)
    
    def _bandpass_filter(self, data: np.ndarray, fs: float) -> np.ndarray:
        """Apply bandpass filter"""
        from scipy.signal import butter, filtfilt
        
        nyquist = fs / 2
        low = self.lowpass_freq / nyquist
        high = self.highpass_freq / nyquist
        
        b, a = butter(4, [low, high], btype="band")
        
        return filtfilt(b, a, data, axis=-1)
    
    def _remove_baseline(self, data: np.ndarray) -> np.ndarray:
        """Remove baseline drift"""
        if data.ndim > 1:
            return data - np.mean(data, axis=-1, keepdims=True)
        return data - np.mean(data)
    
    def _normalize(self, data: np.ndarray) -> np.ndarray:
        """Z-score normalization"""
        if data.ndim > 1:
            mean = np.mean(data, axis=-1, keepdims=True)
            std = np.std(data, axis=-1, keepdims=True)
            std[std == 0] = 1
            return (data - mean) / std
        mean, std = np.mean(data), np.std(data)
        return (data - mean) / std if std > 0 else data


class FeatureExtractor:
    """Extract features from neural signals"""
    
    def __init__(self):
        self.bands = {
            "delta": (0.5, 4),
            "theta": (4, 8),
            "alpha": (8, 13),
            "beta": (13, 30),
            "gamma": (30, 100)
        }
    
    def extract_band_power(self, 
                          data: np.ndarray,
                          sampling_rate: float) -> Dict[str, float]:
        """Extract power in different frequency bands"""
        from scipy.signal import welch
        
        freqs, psd = welch(data, fs=sampling_rate, nperseg=min(256, len(data)))
        
        band_powers = {}
        for band_name, (low, high) in self.bands.items():
            mask = (freqs >= low) & (freqs < high)
            band_powers[band_name] = np.trapz(psd[mask], freqs[mask])
        
        return band_powers
    
    def extract_features(self, 
                        signal: NeuralSignal,
                        include_temporal: bool = True,
                        include_spectral: bool = True) -> Dict:
        """Extract comprehensive feature set"""
        features = {}
        
        if include_temporal:
            features["mean"] = np.mean(signal.data, axis=-1)
            features["std"] = np.std(signal.data, axis=-1)
            features["variance"] = np.var(signal.data, axis=-1)
            features["rms"] = np.sqrt(np.mean(signal.data**2, axis=-1))
            features["skewness"] = self._skewness(signal.data)
            features["kurtosis"] = self._kurtosis(signal.data)
        
        if include_spectral:
            for i, channel in enumerate(signal.channel_names):
                if signal.data.ndim > 1 and i < signal.data.shape[0]:
                    channel_data = signal.data[i]
                else:
                    channel_data = signal.data
                
                band_powers = self.extract_band_power(channel_data, signal.sampling_rate)
                for band, power in band_powers.items():
                    features[f"{channel}_{band}_power"] = power
        
        return features
    
    def _skewness(self, data: np.ndarray) -> float:
        """Calculate skewness"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0
        return np.mean(((data - mean) / std) ** 3)
    
    def _kurtosis(self, data: np.ndarray) -> float:
        """Calculate kurtosis"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0
        return np.mean(((data - mean) / std) ** 4) - 3


class AdaptiveDecoder:
    """Adaptive BCI decoder with online learning"""
    
    def __init__(self, num_classes: int = 2):
        self.num_classes = num_classes
        self.weights = None
        self.bias = 0
        self.learning_rate = 0.1
        self.adaptation_rate = 0.01
        self.session_count = 0
    
    def initialize_classifier(self, input_dim: int):
        """Initialize classifier weights"""
        self.weights = np.random.randn(input_dim) * 0.1
        self.bias = 0
    
    def decode(self, features: np.ndarray) -> Tuple[np.ndarray, float]:
        """Decode features to class predictions"""
        if self.weights is None:
            raise ValueError("Classifier not initialized")
        
        scores = np.dot(self.weights, features) + self.bias
        probs = self._softmax(scores)
        
        return np.argmax(probs), np.max(probs)
    
    def update(self, features: np.ndarray, target: int):
        """Update classifier with new labeled data"""
        if self.weights is None:
            self.initialize_classifier(len(features))
        
        prediction, confidence = self.decode(features)
        error = target - prediction
        
        if error != 0:
            self.weights += self.learning_rate * error * features
            self.bias += self.learning_rate * error
        
        self.session_count += 1
    
    def adapt_online(self, features: np.ndarray, confidence: float):
        """Online adaptation based on confidence"""
        adaptation_strength = self.adaptation_rate * confidence
        self.weights *= (1 - adaptation_strength)
        self.weights += adaptation_strength * features
        self.session_count += 1
    
    def _softmax(self, scores: np.ndarray) -> np.ndarray:
        """Softmax function"""
        exp_scores = np.exp(scores - np.max(scores))
        return exp_scores / np.sum(exp_scores)


class MotorImageryClassifier:
    """Motor imagery BCI classifier"""
    
    def __init__(self):
        self.left_features = []
        self.right_features = []
        self.is_calibrated = False
    
    def calibrate(self, 
                  left_trials: List[np.ndarray],
                  right_trials: List[np.ndarray]):
        """Calibrate classifier with labeled trials"""
        extractor = FeatureExtractor()
        
        for trial in left_trials:
            features = extractor.extract_band_power(trial, 256)
            self.left_features.append(list(features.values()))
        
        for trial in right_trials:
            features = extractor.extract_band_power(trial, 256)
            self.right_features.append(list(features.values()))
        
        self.is_calibrated = True
    
    def classify_trial(self, trial: np.ndarray) -> Dict:
        """Classify motor imagery trial"""
        if not self.is_calibrated:
            return {"class": "unknown", "confidence": 0.0}
        
        extractor = FeatureExtractor()
        features = extractor.extract_band_power(trial, 256)
        feature_vec = np.array(list(features.values()))
        
        left_mean = np.mean(self.left_features, axis=0)
        right_mean = np.mean(self.right_features, axis=0)
        
        dist_left = np.linalg.norm(feature_vec - left_mean)
        dist_right = np.linalg.norm(feature_vec - right_mean)
        
        total = dist_left + dist_right
        left_prob = 1 - dist_left / total if total > 0 else 0.5
        
        return {
            "class": "left" if left_prob > 0.5 else "right",
            "confidence": abs(left_prob - 0.5) * 2,
            "left_probability": left_prob,
            "right_probability": 1 - left_prob
        }


class RealTimeProcessor:
    """Real-time neural signal processing"""
    
    def __init__(self, 
                 window_size: int = 256,
                 overlap: int = 128,
                 sampling_rate: float = 256.0):
        self.window_size = window_size
        self.overlap = overlap
        self.sampling_rate = sampling_rate
        self.buffer = {}


if __name__ == "__main__":
    preprocessor = SignalPreprocessor()
    extractor = FeatureExtractor()
    decoder = AdaptiveDecoder(num_classes=2)
    motor_classifier = MotorImageryClassifier()
    
    signal = NeuralSignal(
        signal_type=SignalType.EEG,
        data=np.random.randn(32, 1000),
        sampling_rate=256.0,
        channel_names=[f"EEG{i+1}" for i in range(32)],
        timestamp=0.0
    )
    
    preprocessed = preprocessor.preprocess(signal)
    features = extractor.extract_features(preprocessed)
    
    decoder.initialize_classifier(len(features))
    prediction, confidence = decoder.decode(np.array(list(features.values())))
    
    left_trial = np.random.randn(256)
    right_trial = np.random.randn(256)
    result = motor_classifier.classify_trial(left_trial)
    
    print(f"Preprocessed: {preprocessed.metadata}")
    print(f"Features extracted: {len(features)}")
    print(f"Prediction: {prediction}, Confidence: {confidence:.2f}")
    print(f"Motor imagery: {result}")
