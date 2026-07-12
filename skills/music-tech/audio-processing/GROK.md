---
name: audio-processing
category: music-tech
version: 2.0.0
tags: [music-tech, audio-processing, dsp, signal-processing, python]
---

# Audio Processing

## Overview

Digital audio signal processing toolkit covering the complete pipeline from raw waveform manipulation to advanced spectral analysis. This skill provides production-quality implementations of audio transforms (FFT, STFT, MFCC), filtering (FIR, IIR), effects processing (reverb, compression, equalization), format conversion, and real-time audio streaming with Python's librosa, scipy.signal, pydub, and soundfile libraries.

## Core Capabilities

- **Spectral Analysis**: FFT, STFT, mel spectrograms, chromagrams, and spectral features extraction
- **Filtering**: FIR/IIR filter design, bandpass/lowpass/highpass filtering, noise reduction
- **Effects Processing**: Reverb, delay, compression, limiting, equalization, distortion
- **Audio Features**: Pitch detection, onset detection, tempo estimation, beat tracking
- **Format Conversion**: Sample rate conversion, bit depth conversion, channel routing
- **Streaming**: Real-time audio I/O with PyAudio, PortAudio, and callback-based pipelines
- **Visualization**: Waveform plotting, spectrograms, frequency response curves
- **Machine Learning Prep**: Feature extraction pipelines for audio classification and transcription

## Usage Examples

```python
import numpy as np
import librosa
from scipy import signal
from scipy.io import wavfile
from dataclasses import dataclass

# Spectral Analysis Pipeline
@dataclass
class AudioFeatures:
    sample_rate: int
    duration: float
    rms_energy: float
    spectral_centroid: float
    spectral_bandwidth: float
    tempo: float
    pitch_hz: float
    mfcc: np.ndarray

def extract_features(audio_path: str, sr: int = 22050) -> AudioFeatures:
    y, sr = librosa.load(audio_path, sr=sr)
    duration = librosa.get_duration(y=y, sr=sr)

    rms = np.sqrt(np.mean(y**2))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_hz = float(pitches[np.argmax(magnitudes)])

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    return AudioFeatures(
        sample_rate=sr, duration=duration, rms_energy=rms,
        spectral_centroid=spectral_centroid, spectral_bandwidth=spectral_bandwidth,
        tempo=float(tempo), pitch_hz=pitch_hz, mfcc=mfcc
    )

# FIR Filter Design and Application
def design_bandpass_filter(lowcut: float, highcut: float, sr: int, order: int = 5):
    nyq = 0.5 * sr
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a

def apply_filter(audio: np.ndarray, b: np.ndarray, a: np.ndarray) -> np.ndarray:
    return signal.filtfilt(b, a, audio)

# Real-time Audio Effects Chain
class AudioEffectsChain:
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self.effects = []

    def add_compressor(self, threshold: float = -20, ratio: float = 4, attack: float = 0.005):
        self.effects.append(("compressor", threshold, ratio, attack))
        return self

    def add_reverb(self, decay: float = 0.5, wet: float = 0.3):
        self.effects.append(("reverb", decay, wet))
        return self

    def add_equalizer(self, bands: list):
        self.effects.append(("eq", bands))
        return self

    def process(self, audio: np.ndarray) -> np.ndarray:
        result = audio.copy()
        for effect in self.effects:
            if effect[0] == "compressor":
                result = self._apply_compressor(result, effect[1], effect[2])
            elif effect[0] == "reverb":
                result = self._apply_reverb(result, effect[1], effect[2])
        return result

    def _apply_compressor(self, audio, threshold, ratio):
        threshold_linear = 10 ** (threshold / 20)
        mask = np.abs(audio) > threshold_linear
        compressed = audio.copy()
        compressed[mask] = np.sign(audio[mask]) * (
            threshold_linear + (np.abs(audio[mask]) - threshold_linear) / ratio
        )
        return compressed

    def _apply_reverb(self, audio, decay, wet):
        impulse = np.zeros(int(self.sr * decay))
        impulse[0] = 1.0
        impulse[1:int(self.sr * decay * 0.3)] *= decay
        impulse[1:int(self.sr * decay * 0.3)] *= np.random.uniform(0.5, 1.0, int(self.sr * decay * 0.3))
        reverb_signal = np.convolve(audio, impulse, mode='full')[:len(audio)]
        return (1 - wet) * audio + wet * reverb_signal

# Onset Detection and Beat Tracking
def analyze_rhythm(audio_path: str) -> dict:
    y, sr = librosa.load(audio_path)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    return {
        "tempo": float(tempo),
        "num_onsets": len(onset_frames),
        "onset_times": onset_times.tolist(),
        "beat_times": beat_times.tolist(),
    }

# Spectrogram Generation
def generate_spectrogram(audio_path: str, output_path: str):
    import matplotlib.pyplot as plt
    y, sr = librosa.load(audio_path)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    S_dB = librosa.power_to_db(S, ref=np.max)

    fig, ax = plt.subplots(1, 1, figsize=(12, 4))
    img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000, ax=ax)
    ax.set(title='Mel-frequency spectrogram')
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
```

## Best Practices

- Always work with float32 normalized audio [-1.0, 1.0] to avoid clipping and precision loss
- Use `librosa.load()` with a consistent sample rate for feature extraction pipelines
- Apply windowing (Hann, Hamming) before FFT to reduce spectral leakage
- Use `scipy.signal.filtfilt` for zero-phase filtering in offline processing
- Design filters with sufficient order to achieve desired roll-off without numerical instability
- Use Mel spectrograms for ML-based audio tasks; raw spectrograms for analytical tasks
- Profile memory with large audio files by processing in chunks (STFT frames)
- Normalize output audio before writing to disk to prevent clipping
- Validate sample rates match across the pipeline to avoid pitch/speed artifacts
- Use `soundfile` over `scipy.io.wavfile` for broader format support and metadata preservation

## Related Modules

- `sound-design` - Sound synthesis and creative audio manipulation
- `music-generation` - AI-driven music composition and arrangement
- `dj-tools` - DJ-specific audio manipulation and mixing utilities
- `music-analytics` - Audio feature extraction for analytics and recommendations
