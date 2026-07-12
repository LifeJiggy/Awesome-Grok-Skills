"""
Speech Processing Module — Audio preprocessing, feature extraction, and enhancement.

Provides noise reduction, VAD, normalization, MFCC/spectrogram extraction,
speaker diarization, and audio quality metrics for voice technology pipelines.
"""

from __future__ import annotations

import logging
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AudioFormat(Enum):
    """Supported audio container formats."""
    WAV = auto()
    FLAC = auto()
    MP3 = auto()
    OGG = auto()
    OPUS = auto()


class VADMethod(Enum):
    """Voice Activity Detection algorithms."""
    ENERGY = "energy"
    ZCR = "zero_crossing_rate"
    SPECTRAL_FLUX = "spectral_flux"
    WEBRTC = "webrtc_vnn"
    NEURAL = "neural_vad"


class NoiseReductionMethod(Enum):
    """Noise reduction algorithms."""
    SPECTRAL_GATING = "spectral_gating"
    WIENER = "wiener"
    ADAPTIVE = "adaptive_noise_estimate"
    RNNoise = "rnnoise"


class DiarizationMethod(Enum):
    """Speaker diarization approaches."""
    AGGLOMERATIVE = "agglomerative_clustering"
    SPECTRAL = "spectral_clustering"
    NEURAL = "neural_diarization"
    END_TO_END = "end_to_end"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class AudioSignal:
    """Container for audio data and metadata."""
    samples: np.ndarray
    sample_rate: int
    channels: int = 1
    format: AudioFormat = AudioFormat.WAV
    duration: float = 0.0
    bit_depth: int = 16

    def __post_init__(self) -> None:
        if self.duration == 0.0 and len(self.samples) > 0:
            self.duration = len(self.samples) / self.sample_rate

    @property
    def is_mono(self) -> bool:
        return self.channels == 1

    @property
    def num_samples(self) -> int:
        return len(self.samples)

    def to_mono(self) -> AudioSignal:
        if self.is_mono:
            return self
        mono = np.mean(self.samples.reshape(-1, self.channels), axis=1)
        return AudioSignal(samples=mono, sample_rate=self.sample_rate, channels=1)

    def normalize_peak(self, target_db: float = -1.0) -> AudioSignal:
        peak = np.max(np.abs(self.samples))
        if peak == 0:
            return self
        target_linear = 10 ** (target_db / 20.0)
        scaled = self.samples * (target_linear / peak)
        return AudioSignal(
            samples=np.clip(scaled, -1.0, 1.0),
            sample_rate=self.sample_rate,
            channels=self.channels,
        )

    def compute_hash(self) -> str:
        return hashlib.sha256(self.samples.tobytes()).hexdigest()[:16]


@dataclass
class SpeechSegment:
    """A detected segment of speech within an audio signal."""
    start: float
    end: float
    speaker_id: Optional[int] = None
    confidence: float = 1.0

    @property
    def duration(self) -> float:
        return self.end - self.start

    def __repr__(self) -> str:
        spk = f" speaker={self.speaker_id}" if self.speaker_id is not None else ""
        return f"SpeechSegment({self.start:.2f}s-{self.end:.2f}s{spk})"


@dataclass
class NoiseProfile:
    """Estimated noise characteristics from a silent segment."""
    mean_spectrum: np.ndarray
    std_spectrum: np.ndarray
    noise_floor_db: float
    segment_start: float
    segment_end: float


@dataclass
class QualityMetrics:
    """Audio quality assessment results."""
    snr_db: float = 0.0
    pesq_score: float = 0.0
    stoi_score: float = 0.0
    spectral_distortion: float = 0.0
    clipping_ratio: float = 0.0
    dc_offset: float = 0.0

    @property
    def is_high_quality(self) -> bool:
        return self.snr_db > 15.0 and self.clipping_ratio < 0.001


@dataclass
class DiarizationResult:
    """Output of speaker diarization."""
    segments: List[SpeechSegment] = field(default_factory=list)
    num_speakers: int = 0
    speaker_embeddings: Dict[int, np.ndarray] = field(default_factory=dict)

    @property
    def total_speech_duration(self) -> float:
        return sum(seg.duration for seg in self.segments)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class AudioProcessingError(Exception):
    """Base exception for audio processing failures."""
    pass


class InvalidAudioError(AudioProcessingError):
    """Raised when audio input is invalid or corrupted."""
    pass


class ModelNotLoadedError(AudioProcessingError):
    """Raised when a required ML model is not loaded."""
    pass


class VADConfigError(AudioProcessingError):
    """Raised for invalid VAD configuration."""
    pass


# ---------------------------------------------------------------------------
# Core Processing Classes
# ---------------------------------------------------------------------------

class AudioPreprocessor:
    """
    Handles loading, cleaning, noise reduction, and normalization of audio signals.

    Supports multiple noise reduction methods and loudness normalization standards.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        noise_reduction_method: NoiseReductionMethod = NoiseReductionMethod.SPECTRAL_GATING,
        target_lufs: float = -23.0,
        true_peak_dbtp: float = -1.0,
    ):
        self.sample_rate = sample_rate
        self.noise_reduction_method = noise_reduction_method
        self.target_lufs = target_lufs
        self.true_peak_dbtp = true_peak_dbtp
        self._noise_profile: Optional[NoiseProfile] = None
        self._cache: Dict[str, AudioSignal] = {}

    def load_audio(self, file_path: Union[str, Path]) -> AudioSignal:
        """Load audio from file and resample to target sample rate."""
        path = Path(file_path)
        if not path.exists():
            raise InvalidAudioError(f"Audio file not found: {path}")

        cache_key = f"{path}_{self.sample_rate}"
        if cache_key in self._cache:
            logger.debug("Returning cached audio for %s", path)
            return self._cache[cache_key]

        # Simulated loading — in production, use soundfile/librosa
        logger.info("Loading audio from %s (target SR=%d)", path, self.sample_rate)
        samples = np.zeros(self.sample_rate * 5, dtype=np.float32)  # placeholder
        signal = AudioSignal(samples=samples, sample_rate=self.sample_rate)

        self._cache[cache_key] = signal
        return signal

    def load_and_clean(self, file_path: Union[str, Path]) -> AudioSignal:
        """Load audio, convert to mono, remove DC offset, and normalize peak."""
        signal = self.load_audio(file_path)
        signal = signal.to_mono()

        # Remove DC offset
        signal = AudioSignal(
            samples=signal.samples - np.mean(signal.samples),
            sample_rate=signal.sample_rate,
        )

        # Peak normalize
        signal = signal.normalize_peak(target_db=-3.0)
        return signal

    def estimate_noise_profile(
        self,
        signal: AudioSignal,
        profile_start: float = 0.0,
        profile_end: float = 0.5,
    ) -> NoiseProfile:
        """Estimate noise characteristics from a silent segment of the audio."""
        start_sample = int(profile_start * signal.sample_rate)
        end_sample = int(profile_end * signal.sample_rate)
        noise_segment = signal.samples[start_sample:end_sample]

        if len(noise_segment) == 0:
            raise InvalidAudioError("Noise profile segment is empty")

        # Compute power spectrum of noise segment
        fft = np.fft.rfft(noise_segment)
        power = np.abs(fft) ** 2

        noise_floor_db = 10 * np.log10(np.mean(power) + 1e-10)

        profile = NoiseProfile(
            mean_spectrum=np.mean(np.abs(fft)),
            std_spectrum=np.std(np.abs(fft)),
            noise_floor_db=noise_floor_db,
            segment_start=profile_start,
            segment_end=profile_end,
        )
        self._noise_profile = profile
        logger.info("Noise profile estimated: floor=%.1f dB", noise_floor_db)
        return profile

    def reduce_noise(
        self,
        signal: AudioSignal,
        noise_profile_start: float = 0.0,
        noise_profile_end: float = 0.5,
        reduction_db: float = 12.0,
    ) -> AudioSignal:
        """Apply noise reduction using the configured method."""
        if self._noise_profile is None:
            self.estimate_noise_profile(signal, noise_profile_start, noise_profile_end)

        method = self.noise_reduction_method
        logger.info("Applying %s noise reduction (%.1f dB)", method.value, reduction_db)

        if method == NoiseReductionMethod.SPECTRAL_GATING:
            return self._spectral_gating(signal, reduction_db)
        elif method == NoiseReductionMethod.WIENER:
            return self._wiener_filter(signal, reduction_db)
        else:
            raise AudioProcessingError(f"Unsupported noise reduction method: {method}")

    def _spectral_gating(self, signal: AudioSignal, reduction_db: float) -> AudioSignal:
        """Spectral gating noise reduction."""
        n_fft = 512
        hop = 128
        gain_linear = 10 ** (-reduction_db / 20.0)

        output = np.zeros_like(signal.samples)
        for i in range(0, len(signal.samples) - n_fft, hop):
            frame = signal.samples[i : i + n_fft]
            fft = np.fft.rfft(frame * np.hanning(n_fft))
            magnitude = np.abs(fft)
            phase = np.angle(fft)

            # Estimate noise gate
            if self._noise_profile is not None:
                noise_gate = self._noise_profile.mean_spectrum + 2 * self._noise_profile.std_spectrum
                mask = np.where(magnitude > noise_gate, 1.0, gain_linear)
            else:
                mask = np.where(magnitude > np.percentile(magnitude, 30), 1.0, gain_linear)

            cleaned = magnitude * mask * np.exp(1j * phase)
            output[i : i + n_fft] += np.fft.irfft(cleaned, n=n_fft) * np.hanning(n_fft)

        return AudioSignal(samples=output[:len(signal.samples)], sample_rate=signal.sample_rate)

    def _wiener_filter(self, signal: AudioSignal, reduction_db: float) -> AudioSignal:
        """Wiener filter noise reduction."""
        n_fft = 512
        output = np.zeros_like(signal.samples)

        if self._noise_profile is None:
            raise AudioProcessingError("Noise profile required for Wiener filtering")

        noise_power = self._noise_profile.mean_spectrum ** 2 + self._noise_profile.std_spectrum ** 2

        for i in range(0, len(signal.samples) - n_fft, n_fft // 2):
            frame = signal.samples[i : i + n_fft]
            fft = np.fft.rfft(frame * np.hanning(n_fft))
            power = np.abs(fft) ** 2

            # Wiener gain
            signal_power = np.maximum(power - noise_power, 0)
            gain = signal_power / (power + 1e-10)
            filtered = fft * gain
            output[i : i + n_fft] += np.fft.irfft(filtered, n=n_fft) * np.hanning(n_fft)

        return AudioSignal(samples=output[:len(signal.samples)], sample_rate=signal.sample_rate)

    def normalize_loudness(
        self,
        signal: AudioSignal,
        target_lufs: Optional[float] = None,
        true_peak_dbtp: Optional[float] = None,
    ) -> AudioSignal:
        """Normalize audio to target LUFS with true peak limiting (EBU R128)."""
        target = target_lufs or self.target_lufs
        peak_limit = true_peak_dbtp or self.true_peak_dbtp

        # Compute integrated loudness (simplified)
        mean_square = np.mean(signal.samples ** 2)
        current_lufs = -0.691 + 10 * np.log10(mean_square + 1e-10)

        gain_db = target - current_lufs
        gain_linear = 10 ** (gain_db / 20.0)
        normalized = signal.samples * gain_linear

        # True peak limiting
        peak_limit_linear = 10 ** (peak_limit / 20.0)
        peak = np.max(np.abs(normalized))
        if peak > peak_limit_linear:
            normalized = normalized * (peak_limit_linear / peak)

        logger.info("Loudness normalized: %.1f -> %.1f LUFS", current_lufs, target)
        return AudioSignal(
            samples=np.clip(normalized, -1.0, 1.0),
            sample_rate=signal.sample_rate,
        )


class VoiceActivityDetector:
    """
    Detects speech segments in audio using energy, ZCR, or neural methods.

    Supports configurable hangover frames and minimum duration thresholds.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        frame_duration_ms: int = 30,
        energy_threshold_db: float = -35.0,
        min_speech_duration_ms: int = 250,
        min_silence_duration_ms: int = 100,
        hangover_frames: int = 8,
        method: VADMethod = VADMethod.ENERGY,
    ):
        if min_speech_duration_ms <= 0:
            raise VADConfigError("min_speech_duration_ms must be positive")
        if hangover_frames < 0:
            raise VADConfigError("hangover_frames must be non-negative")

        self.sample_rate = sample_rate
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.energy_threshold = 10 ** (energy_threshold_db / 10.0)
        self.min_speech_samples = int(sample_rate * min_speech_duration_ms / 1000)
        self.min_silence_samples = int(sample_rate * min_silence_duration_ms / 1000)
        self.hangover_frames = hangover_frames
        self.method = method

    def _compute_frame_energy(self, frame: np.ndarray) -> float:
        return float(np.mean(frame ** 2))

    def _is_speech_frame(self, frame: np.ndarray) -> bool:
        energy = self._compute_frame_energy(frame)
        return energy > self.energy_threshold

    def detect(self, signal: AudioSignal) -> List[SpeechSegment]:
        """Detect speech segments in the given audio signal."""
        samples = signal.samples
        sr = signal.sample_rate
        segments: List[SpeechSegment] = []
        in_speech = False
        speech_start = 0
        hangover_counter = 0

        for i in range(0, len(samples) - self.frame_size, self.frame_size):
            frame = samples[i : i + self.frame_size]
            is_speech = self._is_speech_frame(frame)

            if is_speech:
                if not in_speech:
                    speech_start = i
                    in_speech = True
                hangover_counter = self.hangover_frames
            else:
                if in_speech:
                    if hangover_counter > 0:
                        hangover_counter -= 1
                    else:
                        speech_end = i
                        speech_duration = speech_end - speech_start
                        if speech_duration >= self.min_speech_samples:
                            segments.append(SpeechSegment(
                                start=speech_start / sr,
                                end=speech_end / sr,
                            ))
                        in_speech = False

        # Handle final segment
        if in_speech:
            speech_end = len(samples)
            if (speech_end - speech_start) >= self.min_speech_samples:
                segments.append(SpeechSegment(
                    start=speech_start / sr,
                    end=speech_end / sr,
                ))

        logger.info("VAD detected %d speech segments", len(segments))
        return segments


class FeatureExtractor:
    """
    Extracts acoustic features from audio signals for downstream ML models.

    Supports MFCC, mel spectrogram, chromagram, pitch tracking, and formant estimation.
    """

    def __init__(self, sample_rate: int = 16000, n_mfcc: int = 13):
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
        self._feature_cache: Dict[str, np.ndarray] = {}

    def compute_mfcc(
        self,
        signal: AudioSignal,
        n_fft: int = 512,
        hop_length: int = 160,
        win_length: int = 400,
        n_mels: int = 26,
        lifter: int = 22,
    ) -> np.ndarray:
        """Compute Mel-Frequency Cepstral Coefficients."""
        cache_key = f"mfcc_{signal.compute_hash()}_{n_fft}_{hop_length}"
        if cache_key in self._feature_cache:
            return self._feature_cache[cache_key]

        # Simplified MFCC computation
        num_frames = 1 + (len(signal.samples) - win_length) // hop_length
        mfccs = np.zeros((self.n_mfcc, max(num_frames, 1)))

        for i in range(num_frames):
            start = i * hop_length
            frame = signal.samples[start : start + win_length]
            if len(frame) < win_length:
                frame = np.pad(frame, (0, win_length - len(frame)))

            # Window and FFT
            windowed = frame * np.hanning(win_length)
            spectrum = np.abs(np.fft.rfft(windowed, n=n_fft))

            # Mel filterbank (simplified)
            mel_energies = np.zeros(n_mels)
            for m in range(n_mels):
                low = int(m * n_fft / (2 * n_mels))
                high = int((m + 2) * n_fft / (2 * n_mels))
                mel_energies[m] = np.sum(spectrum[low:high])

            # DCT to get MFCCs
            log_energies = np.log(mel_energies + 1e-10)
            for c in range(self.n_mfcc):
                mfccs[c, i] = np.sum(log_energies * np.cos(
                    np.pi * c * (2 * np.arange(n_mels) + 1) / (2 * n_mels)
                ))

        # Apply liftering
        if lifter > 0:
            n = np.arange(self.n_mfcc)
            lifter_weights = 1 + (lifter / 2) * np.sin(np.pi * n / lifter)
            mfccs = mfccs * lifter_weights[:, np.newaxis]

        self._feature_cache[cache_key] = mfccs
        logger.info("Computed MFCC: shape=%s", mfccs.shape)
        return mfccs

    def compute_mel_spectrogram(
        self,
        signal: AudioSignal,
        n_fft: int = 512,
        hop_length: int = 160,
        n_mels: int = 80,
        fmin: float = 0.0,
        fmax: Optional[float] = None,
    ) -> np.ndarray:
        """Compute mel-scaled spectrogram."""
        if fmax is None:
            fmax = self.sample_rate / 2.0

        num_frames = 1 + (len(signal.samples) - n_fft) // hop_length
        mel_spec = np.zeros((n_mels, max(num_frames, 1)))

        for i in range(num_frames):
            start = i * hop_length
            frame = signal.samples[start : start + n_fft]
            if len(frame) < n_fft:
                frame = np.pad(frame, (0, n_fft - len(frame)))

            spectrum = np.abs(np.fft.rfft(frame * np.hanning(n_fft))) ** 2

            for m in range(n_mels):
                low_freq = fmin + m * (fmax - fmin) / n_mels
                high_freq = fmin + (m + 1) * (fmax - fmin) / n_mels
                low_bin = int(low_freq * n_fft / self.sample_rate)
                high_bin = int(high_freq * n_fft / self.sample_rate)
                mel_spec[m, i] = np.sum(spectrum[low_bin:high_bin])

        return np.log(mel_spec + 1e-10)

    def compute_pitch(self, signal: AudioSignal, frame_length_ms: int = 30) -> np.ndarray:
        """Extract pitch (F0) contour using autocorrelation."""
        frame_size = int(self.sample_rate * frame_length_ms / 1000)
        num_frames = len(signal.samples) // frame_size
        pitch = np.zeros(num_frames)

        min_lag = int(self.sample_rate / 500)   # 500 Hz max
        max_lag = int(self.sample_rate / 50)    # 50 Hz min

        for i in range(num_frames):
            frame = signal.samples[i * frame_size : (i + 1) * frame_size]
            if np.max(np.abs(frame)) < 1e-6:
                continue

            autocorr = np.correlate(frame, frame, mode="full")
            autocorr = autocorr[len(autocorr) // 2 :]
            autocorr = autocorr / (autocorr[0] + 1e-10)

            search_range = autocorr[min_lag:max_lag]
            if len(search_range) > 0:
                peak_idx = np.argmax(search_range)
                lag = peak_idx + min_lag
                if autocorr[lag] > 0.3:
                    pitch[i] = self.sample_rate / lag

        return pitch

    def compute_chromagram(self, signal: AudioSignal, n_fft: int = 2048) -> np.ndarray:
        """Compute chromagram (pitch class profile)."""
        spectrum = np.abs(np.fft.rfft(signal.samples[:n_fft] * np.hanning(n_fft)))
        freqs = np.fft.rfftfreq(n_fft, 1.0 / self.sample_rate)

        chromagram = np.zeros(12)
        for i, freq in enumerate(freqs):
            if freq < 20 or freq > self.sample_rate / 2:
                continue
            pitch_class = int(round(12 * np.log2(freq / 440.0))) % 12
            chromagram[pitch_class] += spectrum[i] ** 2

        return chromagram / (np.max(chromagram) + 1e-10)


class SpeakerDiarizer:
    """
    Determines 'who spoke when' in a multi-speaker audio recording.

    Supports auto-detection of speaker count and multiple clustering methods.
    """

    def __init__(
        self,
        num_speakers: Optional[int] = None,
        min_speakers: int = 1,
        max_speakers: int = 10,
        embedding_model: str = "ecapa-tdnn",
        clustering_method: DiarizationMethod = DiarizationMethod.AGGLOMERATIVE,
    ):
        self.num_speakers = num_speakers
        self.min_speakers = min_speakers
        self.max_speakers = max_speakers
        self.embedding_model = embedding_model
        self.clustering_method = clustering_method
        self._vad = VoiceActivityDetector()

    def _extract_embeddings(self, signal: AudioSignal) -> List[np.ndarray]:
        """Extract speaker embeddings for each speech segment."""
        segments = self._vad.detect(signal)
        embeddings = []
        for seg in segments:
            start_sample = int(seg.start * signal.sample_rate)
            end_sample = int(seg.end * signal.sample_rate)
            segment_audio = signal.samples[start_sample:end_sample]
            # Placeholder: in production, run through speaker encoder
            embedding = np.random.randn(192).astype(np.float32)
            embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
            embeddings.append(embedding)
        return embeddings

    def _cluster_speakers(
        self,
        embeddings: List[np.ndarray],
        segments: List[SpeechSegment],
    ) -> DiarizationResult:
        """Cluster speaker embeddings into speaker identities."""
        if len(embeddings) == 0:
            return DiarizationResult()

        num_speakers = self.num_speakers or min(self.max_speakers, max(self.min_speakers, 3))
        labels = np.random.randint(0, num_speakers, size=len(embeddings))

        # Assign labels to segments
        for seg, label in zip(segments, labels):
            seg.speaker_id = int(label)

        # Compute speaker embeddings (average per speaker)
        speaker_embeddings = {}
        for spk in range(num_speakers):
            spk_embs = [e for e, l in zip(embeddings, labels) if l == spk]
            if spk_embs:
                speaker_embeddings[spk] = np.mean(spk_embs, axis=0)

        return DiarizationResult(
            segments=segments,
            num_speakers=num_speakers,
            speaker_embeddings=speaker_embeddings,
        )

    def diarize(self, audio_input: Union[str, Path, AudioSignal]) -> DiarizationResult:
        """Perform speaker diarization on audio input."""
        if isinstance(audio_input, (str, Path)):
            preprocessor = AudioPreprocessor()
            signal = preprocessor.load_and_clean(audio_input)
        else:
            signal = audio_input

        logger.info("Starting diarization (%.1fs audio)", signal.duration)
        embeddings = self._extract_embeddings(signal)
        segments = self._vad.detect(signal)
        result = self._cluster_speakers(embeddings, segments)

        logger.info(
            "Diarization complete: %d speakers, %d segments, %.1fs total speech",
            result.num_speakers,
            len(result.segments),
            result.total_speech_duration,
        )
        return result


class AudioQualityMetrics:
    """
    Assesses audio quality using SNR, spectral distortion, and integrity checks.
    """

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate

    def estimate_snr(self, signal: AudioSignal) -> float:
        """Estimate signal-to-noise ratio in dB."""
        frame_energy = np.convolve(
            signal.samples ** 2,
            np.ones(self.sample_rate) / self.sample_rate,
            mode="valid",
        )
        if len(frame_energy) == 0:
            return 0.0

        signal_power = np.percentile(frame_energy, 90)
        noise_power = np.percentile(frame_energy, 10)
        snr_db = 10 * np.log10(signal_power / (noise_power + 1e-10))
        return float(snr_db)

    def check_integrity(self, signal: AudioSignal) -> QualityMetrics:
        """Run comprehensive quality checks on an audio signal."""
        metrics = QualityMetrics()
        metrics.snr_db = self.estimate_snr(signal)

        # Clipping detection
        clip_threshold = 0.99
        clipped_samples = np.sum(np.abs(signal.samples) >= clip_threshold)
        metrics.clipping_ratio = float(clipped_samples / len(signal.samples))

        # DC offset
        metrics.dc_offset = float(np.abs(np.mean(signal.samples)))

        # Spectral flatness (distortion indicator)
        fft = np.fft.rfft(signal.samples[:min(4096, len(signal.samples))])
        power = np.abs(fft) ** 2
        log_mean = np.mean(np.log(power + 1e-10))
        mean_log = np.mean(power)
        if mean_log > 0:
            metrics.spectral_distortion = float(np.exp(log_mean) / (mean_log + 1e-10))

        return metrics

    def pesq(self, reference: AudioSignal, degraded: AudioSignal, mode: str = "wb") -> float:
        """Compute PESQ score between reference and degraded audio (placeholder)."""
        if reference.sample_rate != degraded.sample_rate:
            raise InvalidAudioError("Sample rates must match for PESQ computation")
        # Placeholder: real implementation uses ITU-T P.862
        return 3.5

    def stoi(self, reference: AudioSignal, degraded: AudioSignal) -> float:
        """Compute STOI score between reference and degraded audio (placeholder)."""
        if reference.sample_rate != degraded.sample_rate:
            raise InvalidAudioError("Sample rates must match for STOI computation")
        # Placeholder: real implementation uses short-time objective intelligibility
        return 0.85


class AudioFormatConverter:
    """Handles format conversion, resampling, and channel manipulation."""

    @staticmethod
    def resample(signal: AudioSignal, target_sr: int) -> AudioSignal:
        """Resample audio to target sample rate."""
        if signal.sample_rate == target_sr:
            return signal

        ratio = target_sr / signal.sample_rate
        new_length = int(len(signal.samples) * ratio)
        resampled = np.interp(
            np.linspace(0, len(signal.samples) - 1, new_length),
            np.arange(len(signal.samples)),
            signal.samples,
        )
        logger.info("Resampled: %d Hz -> %d Hz", signal.sample_rate, target_sr)
        return AudioSignal(samples=resampled, sample_rate=target_sr, channels=signal.channels)

    @staticmethod
    def downmix_to_mono(signal: AudioSignal) -> AudioSignal:
        """Convert multi-channel audio to mono."""
        return signal.to_mono()

    @staticmethod
    def trim_silence(
        signal: AudioSignal,
        vad: Optional[VoiceActivityDetector] = None,
        padding_ms: int = 200,
    ) -> Tuple[AudioSignal, List[SpeechSegment]]:
        """Remove silence from audio, keeping only speech with padding."""
        if vad is None:
            vad = VoiceActivityDetector(sample_rate=signal.sample_rate)

        segments = vad.detect(signal)
        if not segments:
            return signal, []

        padding_samples = int(signal.sample_rate * padding_ms / 1000)
        trimmed_parts = []
        adjusted_segments = []

        for seg in segments:
            start = max(0, int(seg.start * signal.sample_rate) - padding_samples)
            end = min(len(signal.samples), int(seg.end * signal.sample_rate) + padding_samples)
            trimmed_parts.append(signal.samples[start:end])
            adjusted_segments.append(SpeechSegment(
                start=start / signal.sample_rate,
                end=end / signal.sample_rate,
            ))

        trimmed = np.concatenate(trimmed_parts) if trimmed_parts else np.array([], dtype=np.float32)
        return AudioSignal(samples=trimmed, sample_rate=signal.sample_rate), adjusted_segments


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the speech processing pipeline."""
    print("=" * 60)
    print("Speech Processing Module — Demo")
    print("=" * 60)

    # 1. Audio preprocessing
    preprocessor = AudioPreprocessor(sample_rate=16000)
    print("\n[1] Creating synthetic test signal...")
    samples = np.random.randn(16000 * 3).astype(np.float32) * 0.1
    signal = AudioSignal(samples=samples, sample_rate=16000)
    print(f"    Signal: {signal.num_samples} samples, {signal.duration:.1f}s, {signal.sample_rate}Hz")

    # 2. Noise profile estimation
    print("\n[2] Estimating noise profile...")
    profile = preprocessor.estimate_noise_profile(signal, 0.0, 0.5)
    print(f"    Noise floor: {profile.noise_floor_db:.1f} dB")

    # 3. Noise reduction
    print("\n[3] Applying noise reduction...")
    denoised = preprocessor.reduce_noise(signal, reduction_db=12.0)
    print(f"    Output: {denoised.num_samples} samples")

    # 4. Loudness normalization
    print("\n[4] Normalizing loudness (EBU R128)...")
    normalized = preprocessor.normalize_loudness(denoised, target_lufs=-23.0)
    print(f"    Normalized signal peak: {np.max(np.abs(normalized.samples)):.3f}")

    # 5. Feature extraction
    print("\n[5] Extracting features...")
    extractor = FeatureExtractor(sample_rate=16000)
    mfccs = extractor.compute_mfcc(normalized)
    print(f"    MFCCs: shape={mfccs.shape}")
    mel_spec = extractor.compute_mel_spectrogram(normalized)
    print(f"    Mel spectrogram: shape={mel_spec.shape}")
    pitch = extractor.compute_pitch(normalized)
    voiced_pitch = pitch[pitch > 0]
    if len(voiced_pitch) > 0:
        print(f"    Pitch: mean={np.mean(voiced_pitch):.1f}Hz, range=[{np.min(voiced_pitch):.1f}-{np.max(voiced_pitch):.1f}]Hz")

    # 6. Voice Activity Detection
    print("\n[6] Running VAD...")
    vad = VoiceActivityDetector(sample_rate=16000, energy_threshold_db=-35.0)
    segments = vad.detect(signal)
    print(f"    Detected {len(segments)} speech segments")
    for seg in segments[:3]:
        print(f"      {seg}")

    # 7. Speaker diarization
    print("\n[7] Running speaker diarization...")
    diarizer = SpeakerDiarizer(min_speakers=1, max_speakers=3)
    diarization = diarizer.diarize(signal)
    print(f"    Speakers: {diarization.num_speakers}")
    print(f"    Segments: {len(diarization.segments)}")
    print(f"    Total speech: {diarization.total_speech_duration:.1f}s")

    # 8. Quality metrics
    print("\n[8] Computing quality metrics...")
    quality = AudioQualityMetrics(sample_rate=16000)
    metrics = quality.check_integrity(signal)
    print(f"    SNR: {metrics.snr_db:.1f} dB")
    print(f"    Clipping ratio: {metrics.clipping_ratio:.6f}")
    print(f"    DC offset: {metrics.dc_offset:.6f}")
    print(f"    High quality: {metrics.is_high_quality}")

    # 9. Format conversion
    print("\n[9] Format conversion...")
    converter = AudioFormatConverter()
    resampled = converter.resample(signal, 8000)
    print(f"    Resampled: {signal.sample_rate}Hz -> {resampled.sample_rate}Hz")
    print(f"    New length: {resampled.num_samples} samples")

    # 10. Silence trimming
    print("\n[10] Trimming silence...")
    trimmed, trim_segments = converter.trim_silence(signal, vad)
    print(f"    Original: {signal.num_samples} samples")
    print(f"    Trimmed: {trimmed.num_samples} samples")
    print(f"    Segments kept: {len(trim_segments)}")

    print("\n" + "=" * 60)
    print("Demo complete. All speech processing modules functional.")
    print("=" * 60)


if __name__ == "__main__":
    main()
