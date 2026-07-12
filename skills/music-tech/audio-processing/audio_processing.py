"""
Audio Processing Module
Part of the music-tech skill domain.

Comprehensive digital audio signal processing: spectral analysis, filtering,
effects processing, feature extraction, and real-time audio streaming.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

try:
    import librosa
except ImportError:
    librosa = None

try:
    from scipy import signal as scipy_signal
except ImportError:
    scipy_signal = None


class AudioFormat(Enum):
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    OGG = "ogg"
    AIFF = "aiff"


class FilterType(Enum):
    LOWPASS = "lowpass"
    HIGHPASS = "highpass"
    BANDPASS = "bandpass"
    NOTCH = "notch"


class WindowFunction(Enum):
    HANNING = "hanning"
    HAMMING = "hamming"
    BLACKMAN = "blackman"
    KAISER = "kaiser"


@dataclass
class AudioBuffer:
    data: np.ndarray
    sample_rate: int
    channels: int = 1
    bit_depth: int = 16
    format: AudioFormat = AudioFormat.WAV

    @property
    def duration(self) -> float:
        return len(self.data) / self.sample_rate

    @property
    def num_samples(self) -> int:
        return len(self.data)

    @property
    def rms_energy(self) -> float:
        return float(np.sqrt(np.mean(self.data ** 2)))

    @property
    def peak_amplitude(self) -> float:
        return float(np.max(np.abs(self.data)))

    def normalize(self, target_db: float = -3.0) -> AudioBuffer:
        peak = np.max(np.abs(self.data))
        if peak == 0:
            return AudioBuffer(self.data.copy(), self.sample_rate, self.channels)
        target_linear = 10 ** (target_db / 20)
        normalized = self.data * (target_linear / peak)
        return AudioBuffer(normalized, self.sample_rate, self.channels)

    def trim_silence(self, threshold_db: float = -40.0) -> AudioBuffer:
        threshold = 10 ** (threshold_db / 20)
        mask = np.abs(self.data) > threshold
        if not np.any(mask):
            return AudioBuffer(np.array([]), self.sample_rate, self.channels)
        indices = np.where(mask)[0]
        trimmed = self.data[indices[0]:indices[-1] + 1]
        return AudioBuffer(trimmed, self.sample_rate, self.channels)


@dataclass
class AudioFeatures:
    rms_energy: float = 0.0
    spectral_centroid: float = 0.0
    spectral_bandwidth: float = 0.0
    spectral_rolloff: float = 0.0
    zero_crossing_rate: float = 0.0
    tempo: float = 0.0
    pitch_hz: float = 0.0
    mfcc: Optional[np.ndarray] = None
    chroma: Optional[np.ndarray] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "rms_energy": self.rms_energy,
            "spectral_centroid": self.spectral_centroid,
            "spectral_bandwidth": self.spectral_bandwidth,
            "spectral_rolloff": self.spectral_rolloff,
            "zero_crossing_rate": self.zero_crossing_rate,
            "tempo": self.tempo,
            "pitch_hz": self.pitch_hz,
        }
        if self.mfcc is not None:
            result["mfcc_mean"] = float(np.mean(self.mfcc))
            result["mfcc_std"] = float(np.std(self.mfcc))
        if self.chroma is not None:
            result["chroma_mean"] = float(np.mean(self.chroma))
        return result


class AudioFilter(ABC):
    @abstractmethod
    def apply(self, audio: np.ndarray, sr: int) -> np.ndarray:
        ...


class BandpassFilter(AudioFilter):
    def __init__(self, low_freq: float, high_freq: float, order: int = 5):
        self.low_freq = low_freq
        self.high_freq = high_freq
        self.order = order

    def apply(self, audio: np.ndarray, sr: int) -> np.ndarray:
        if scipy_signal is None:
            raise ImportError("scipy is required for filtering")
        nyq = 0.5 * sr
        low = self.low_freq / nyq
        high = self.high_freq / nyq
        b, a = scipy_signal.butter(self.order, [low, high], btype="band")
        return scipy_signal.filtfilt(b, a, audio)


class LowpassFilter(AudioFilter):
    def __init__(self, cutoff_freq: float, order: int = 5):
        self.cutoff_freq = cutoff_freq
        self.order = order

    def apply(self, audio: np.ndarray, sr: int) -> np.ndarray:
        if scipy_signal is None:
            raise ImportError("scipy is required for filtering")
        nyq = 0.5 * sr
        normalized_cutoff = self.cutoff_freq / nyq
        b, a = scipy_signal.butter(self.order, normalized_cutoff, btype="low")
        return scipy_signal.filtfilt(b, a, audio)


class HighpassFilter(AudioFilter):
    def __init__(self, cutoff_freq: float, order: int = 5):
        self.cutoff_freq = cutoff_freq
        self.order = order

    def apply(self, audio: np.ndarray, sr: int) -> np.ndarray:
        if scipy_signal is None:
            raise ImportError("scipy is required for filtering")
        nyq = 0.5 * sr
        normalized_cutoff = self.cutoff_freq / nyq
        b, a = scipy_signal.butter(self.order, normalized_cutoff, btype="high")
        return scipy_signal.filtfilt(b, a, audio)


class NotchFilter(AudioFilter):
    def __init__(self, center_freq: float, q_factor: float = 30.0):
        self.center_freq = center_freq
        self.q_factor = q_factor

    def apply(self, audio: np.ndarray, sr: int) -> np.ndarray:
        if scipy_signal is None:
            raise ImportError("scipy is required for filtering")
        b, a = scipy_signal.iirnotch(self.center_freq, self.q_factor, sr)
        return scipy_signal.filtfilt(b, a, audio)


class Compressor:
    def __init__(self, threshold_db: float = -20.0, ratio: float = 4.0,
                 attack_ms: float = 5.0, release_ms: float = 50.0):
        self.threshold_db = threshold_db
        self.ratio = ratio
        self.attack_ms = attack_ms
        self.release_ms = release_ms

    def process(self, audio: np.ndarray, sr: int) -> np.ndarray:
        threshold_linear = 10 ** (self.threshold_db / 20)
        attack_samples = int(sr * self.attack_ms / 1000)
        release_samples = int(sr * self.release_ms / 1000)
        envelope = np.zeros(len(audio))
        gain = np.ones(len(audio))

        current_env = 0.0
        for i in range(len(audio)):
            level = abs(audio[i])
            if level > current_env:
                coeff = 1.0 / max(attack_samples, 1)
            else:
                coeff = 1.0 / max(release_samples, 1)
            current_env = current_env + coeff * (level - current_env)
            envelope[i] = current_env

            if current_env > threshold_linear:
                over = current_env / threshold_linear
                compressed = threshold_linear * (over ** (1.0 / self.ratio))
                gain[i] = compressed / current_env
            else:
                gain[i] = 1.0

        return audio * gain


class Reverb:
    def __init__(self, decay: float = 0.5, wet: float = 0.3, predelay_ms: float = 20.0):
        self.decay = decay
        self.wet = wet
        self.predelay_ms = predelay_ms

    def process(self, audio: np.ndarray, sr: int) -> np.ndarray:
        predelay_samples = int(sr * self.predelay_ms / 1000)
        impulse_length = int(sr * self.decay)
        impulse = np.zeros(impulse_length)
        impulse[0] = 1.0

        for i in range(1, impulse_length):
            impulse[i] = (impulse[i - 1] * self.decay *
                          np.random.uniform(0.8, 1.0))

        reverb_tail = np.convolve(audio, impulse, mode="full")[:len(audio)]

        result = np.zeros(len(audio) + predelay_samples)
        result[predelay_samples:predelay_samples + len(audio)] = audio
        result = result[:len(audio)]

        return (1 - self.wet) * result + self.wet * reverb_tail


class Equalizer:
    def __init__(self, bands: Optional[List[Tuple[float, float, float]]] = None):
        self.bands = bands or []

    def add_band(self, freq: float, gain_db: float, q: float = 1.0) -> Equalizer:
        self.bands.append((freq, gain_db, q))
        return self

    def process(self, audio: np.ndarray, sr: int) -> np.ndarray:
        result = audio.copy()
        for freq, gain_db, q in self.bands:
            gain_linear = 10 ** (gain_db / 20)
            if gain_db > 0:
                b, a = self._peaking_eq(freq, gain_linear - 1, q, sr)
            elif gain_db < 0:
                b, a = self._peaking_eq(freq, gain_linear - 1, q, sr)
            else:
                continue
            result = scipy_signal.lfilter(b, a, result)
        return result

    def _peaking_eq(self, freq: float, gain: float, q: float, sr: int):
        A = 10 ** (abs(gain) / 40)
        w0 = 2 * np.pi * freq / sr
        alpha = np.sin(w0) / (2 * q)
        b0 = 1 + alpha * A
        b1 = -2 * np.cos(w0)
        b2 = 1 - alpha * A
        a0 = 1 + alpha / A
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha / A
        b = np.array([b0 / a0, b1 / a0, b2 / a0])
        a = np.array([1.0, a1 / a0, a2 / a0])
        return b, a


class SpectralAnalyzer:
    def __init__(self, sr: int = 22050, n_fft: int = 2048, hop_length: int = 512):
        self.sr = sr
        self.n_fft = n_fft
        self.hop_length = hop_length

    def fft(self, audio: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        spectrum = np.fft.rfft(audio)
        freqs = np.fft.rfftfreq(len(audio), 1.0 / self.sr)
        magnitudes = np.abs(spectrum)
        return freqs, magnitudes

    def stft(self, audio: np.ndarray) -> np.ndarray:
        if librosa is not None:
            return librosa.stft(audio, n_fft=self.n_fft, hop_length=self.hop_length)
        window = np.hanning(self.n_fft)
        frames = []
        for i in range(0, len(audio) - self.n_fft, self.hop_length):
            frame = audio[i:i + self.n_fft] * window
            frames.append(np.fft.rfft(frame))
        return np.array(frames).T

    def mel_spectrogram(self, audio: np.ndarray, n_mels: int = 128) -> np.ndarray:
        if librosa is not None:
            S = librosa.feature.melspectrogram(
                y=audio, sr=self.sr, n_mels=n_mels, n_fft=self.n_fft, hop_length=self.hop_length
            )
            return librosa.power_to_db(S, ref=np.max)
        stft_result = self.stft(audio)
        magnitude = np.abs(stft_result) ** 2
        mel_basis = self._mel_filterbank(n_mels, self.n_fft // 2 + 1)
        mel_spec = np.dot(mel_basis, magnitude)
        return 10 * np.log10(mel_spec + 1e-10)

    def chromagram(self, audio: np.ndarray, n_chroma: int = 12) -> np.ndarray:
        if librosa is not None:
            return librosa.feature.chroma_stft(
                y=audio, sr=self.sr, n_fft=self.n_fft, hop_length=self.hop_length
            )
        stft_result = self.stft(audio)
        magnitude = np.abs(stft_result) ** 2
        chroma_filter = self._chroma_filterbank(n_chroma, self.n_fft // 2 + 1)
        return np.dot(chroma_filter, magnitude)

    def _mel_filterbank(self, n_mels: int, n_freqs: int) -> np.ndarray:
        low_freq_mel = 0
        high_freq_mel = 2595 * np.log10(1 + (self.sr / 2) / 700)
        mel_points = np.linspace(low_freq_mel, high_freq_mel, n_mels + 2)
        hz_points = 700 * (10 ** (mel_points / 2595) - 1)
        bin_points = np.floor((self.n_fft + 1) * hz_points / self.sr).astype(int)

        filterbank = np.zeros((n_mels, n_freqs))
        for m in range(1, n_mels + 1):
            f_left = bin_points[m - 1]
            f_center = bin_points[m]
            f_right = bin_points[m + 1]
            for k in range(f_left, f_center):
                if f_center != f_left:
                    filterbank[m - 1, k] = (k - f_left) / (f_center - f_left)
            for k in range(f_center, f_right):
                if f_right != f_center:
                    filterbank[m - 1, k] = (f_right - k) / (f_right - f_center)
        return filterbank

    def _chroma_filterbank(self, n_chroma: int, n_freqs: int) -> np.ndarray:
        filterbank = np.zeros((n_chroma, n_freqs))
        for i in range(1, n_freqs):
            freq = i * self.sr / self.n_fft
            if freq > 0:
                pitch = 12 * np.log2(freq / 440.0) + 69
                chroma_bin = int(round(pitch)) % 12
                filterbank[chroma_bin, i] = 1.0
        return filterbank


class FeatureExtractor:
    def __init__(self, sr: int = 22050):
        self.sr = sr
        self.analyzer = SpectralAnalyzer(sr)

    def extract(self, audio: np.ndarray) -> AudioFeatures:
        rms = float(np.sqrt(np.mean(audio ** 2)))
        freqs, magnitudes = self.analyzer.fft(audio)

        centroid = 0.0
        total_mag = np.sum(magnitudes)
        if total_mag > 0:
            centroid = float(np.sum(freqs * magnitudes) / total_mag)

        rolloff_freq = 0.0
        cumulative = np.cumsum(magnitudes)
        rolloff_idx = np.searchsorted(cumulative, 0.85 * cumulative[-1])
        if rolloff_idx < len(freqs):
            rolloff_freq = float(freqs[rolloff_idx])

        zcr = float(np.sum(np.abs(np.diff(np.sign(audio)))) / (2 * len(audio)))

        pitch = 0.0
        if librosa is not None:
            pitches, magnitudes_pitch = librosa.piptrack(y=audio, sr=self.sr)
            idx = magnitudes_pitch.argmax()
            pitch = float(pitches.flat[idx])

        mfcc = None
        chroma = None
        if librosa is not None:
            mfcc = librosa.feature.mfcc(y=audio, sr=self.sr, n_mfcc=13)
            chroma = librosa.feature.chroma_stft(y=audio, sr=self.sr)

        return AudioFeatures(
            rms_energy=rms,
            spectral_centroid=centroid,
            spectral_bandwidth=float(np.sqrt(np.sum(((freqs - centroid) ** 2) * magnitudes) / total_mag)) if total_mag > 0 else 0.0,
            spectral_rolloff=rolloff_freq,
            zero_crossing_rate=zcr,
            pitch_hz=pitch,
            mfcc=mfcc,
            chroma=chroma,
        )


class AudioProcessor:
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self._filters: List[AudioFilter] = []
        self._effects: List[Callable[[np.ndarray, int], np.ndarray]] = []

    def add_filter(self, audio_filter: AudioFilter) -> AudioProcessor:
        self._filters.append(audio_filter)
        return self

    def add_effect(self, effect_fn: Callable[[np.ndarray, int], np.ndarray]) -> AudioProcessor:
        self._effects.append(effect_fn)
        return self

    def process(self, audio: np.ndarray) -> np.ndarray:
        result = audio.copy()
        for f in self._filters:
            result = f.apply(result, self.sr)
        for effect in self._effects:
            result = effect(result, self.sr)
        return result

    def chain_from_config(self, config: List[Dict[str, Any]]) -> np.ndarray:
        """Process audio from a list of effect configurations."""
        result = np.random.randn(self.sr * 2).astype(np.float32) * 0.1
        for step in config:
            effect_type = step.get("type", "")
            if effect_type == "compressor":
                comp = Compressor(
                    threshold_db=step.get("threshold", -20),
                    ratio=step.get("ratio", 4.0),
                )
                result = comp.process(result, self.sr)
            elif effect_type == "reverb":
                rev = Reverb(
                    decay=step.get("decay", 0.5),
                    wet=step.get("wet", 0.3),
                )
                result = rev.process(result, self.sr)
            elif effect_type == "lowpass":
                flt = LowpassFilter(step.get("cutoff", 1000))
                result = flt.apply(result, self.sr)
            elif effect_type == "highpass":
                flt = HighpassFilter(step.get("cutoff", 200))
                result = flt.apply(result, self.sr)
        return result


def main():
    print("=== Audio Processing Module ===")

    sr = 44100
    duration = 2.0
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    audio = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.3 * np.sin(2 * np.pi * 880 * t)
    audio += 0.05 * np.random.randn(len(audio))

    buffer = AudioBuffer(data=audio, sample_rate=sr)
    print(f"Duration: {buffer.duration:.2f}s")
    print(f"Peak: {buffer.peak_amplitude:.4f}")
    print(f"RMS: {buffer.rms_energy:.4f}")

    normalized = buffer.normalize(-6.0)
    print(f"Normalized peak: {normalized.peak_amplitude:.4f}")

    print("\n=== Spectral Analysis ===")
    analyzer = SpectralAnalyzer(sr)
    freqs, mags = analyzer.fft(audio)
    peak_freq = freqs[np.argmax(mags)]
    print(f"Peak frequency: {peak_freq:.1f} Hz")

    mel_spec = analyzer.mel_spectrogram(audio, n_mfcc=13)
    print(f"Mel spectrogram shape: {mel_spec.shape}")

    print("\n=== Feature Extraction ===")
    extractor = FeatureExtractor(sr)
    features = extractor.extract(audio)
    for key, value in features.to_dict().items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: (array)")

    print("\n=== Audio Effects ===")
    compressor = Compressor(threshold_db=-15, ratio=6)
    compressed = compressor.process(audio, sr)
    print(f"Original RMS: {np.sqrt(np.mean(audio**2)):.4f}")
    print(f"Compressed RMS: {np.sqrt(np.mean(compressed**2)):.4f}")

    reverb = Reverb(decay=0.4, wet=0.25)
    reverbed = reverb.process(audio, sr)
    print(f"Reverbed RMS: {np.sqrt(np.mean(reverbed**2)):.4f}")

    print("\n=== Filtering ===")
    bp = BandpassFilter(200, 2000)
    filtered = bp.apply(audio, sr)
    print(f"Bandpass (200-2000Hz) RMS: {np.sqrt(np.mean(filtered**2)):.4f}")

    notch = NotchFilter(440, q_factor=30)
    notched = notch.apply(audio, sr)
    print(f"Notch 440Hz RMS: {np.sqrt(np.mean(notched**2)):.4f}")

    print("\n=== Processing Chain ===")
    processor = AudioProcessor(sr)
    processor.add_filter(BandpassFilter(100, 3000))
    processor.add_effect(lambda a, s: Compressor(-18, 4).process(a, s))
    chain_result = processor.process(audio)
    print(f"Chain output RMS: {np.sqrt(np.mean(chain_result**2)):.4f}")

    print("\nDone.")


if __name__ == "__main__":
    main()
